# -*- coding: utf-8 -*-
"""
MLB Team Stats Fetcher (FIP proxy / wRC+ proxy)

[Session_56 2026-04-23 書き直し / PA086]
- 旧: FanGraphs leaders ページを curl/Playwright で取得 (HTML <table class="rgMasterTable">)
- 現: FanGraphs は Cloudflare challenge (Just a moment...) で headless Playwright でも突破不可
  → 公式 MLB StatsAPI に切替: https://statsapi.mlb.com/api/v1/teams/stats (無認証・無 Cloudflare)
- wRC+ と FIP は StatsAPI に存在しない ("sabermetrics" group は空) ため生スタッツから計算:
    FIP  = (13*HR + 3*(BB+HBP) - 2*K) / IP + cFIP
           cFIP = lgERA - (13*HR + 3*(BB+HBP) - 2*K) / IP   (リーグ平均でキャリブレーション)
    wRC+ proxy = 100 * (team_OPS / league_avg_OPS)   (簡易リーグ調整 OPS+)
- 出力ファイル名・構造は従来の mlb_fangraphs_*.json を踏襲 (stats_feed_reader.py 変更不要)
  source フィールドに statsapi.mlb.com を記録、計算由来の値は computed=true 明示

使い方:
  python scripts/fetch_fangraphs.py                   # days-stale 3
  python scripts/fetch_fangraphs.py --days-stale 0    # 強制
  python scripts/fetch_fangraphs.py --season 2026
"""
from __future__ import annotations
import argparse
import json
import shutil
import subprocess
import sys
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FEED_DIR = ROOT / "stats" / "external_feeds"
FEED_DIR.mkdir(parents=True, exist_ok=True)
JST = timezone(timedelta(hours=9))
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")

STATSAPI_BASE = "https://statsapi.mlb.com/api/v1/teams/stats"


def latest_feed() -> Path | None:
    files = sorted(FEED_DIR.glob("mlb_fangraphs_*.json"))
    return files[-1] if files else None


def age_days(p: Path) -> float:
    m = datetime.fromtimestamp(p.stat().st_mtime, tz=JST)
    return (datetime.now(JST) - m).total_seconds() / 86400


def http_get_json(url: str) -> dict:
    """curl があれば curl 使用、無ければ urllib。MLB StatsAPI は認証不要。"""
    if shutil.which("curl"):
        r = subprocess.run(
            ["curl", "-sL", "--compressed", "-A", UA, "--max-time", "30", url],
            capture_output=True, text=True, encoding="utf-8", errors="replace",
        )
        if r.returncode == 0 and r.stdout:
            return json.loads(r.stdout)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def fetch_stats(season: str, group: str) -> list[dict]:
    url = f"{STATSAPI_BASE}?season={season}&group={group}&stats=season&sportIds=1"
    print(f"[FETCH] MLB StatsAPI {group} {season}")
    data = http_get_json(url)
    stats = data.get("stats", [])
    if not stats:
        return []
    return stats[0].get("splits", [])


def _ip_to_outs(ip_str: str | float | None) -> float:
    """'123.2' = 123と2/3イニング = 123 + 2/3 = 123.667 を outs 基準で返す"""
    if ip_str is None:
        return 0.0
    try:
        s = str(ip_str)
        if "." in s:
            whole, frac = s.split(".", 1)
            whole = int(whole)
            frac_outs = int(frac[:1])  # .0 .1 .2
            return whole + frac_outs / 3.0
        return float(s)
    except (ValueError, TypeError):
        return 0.0


def _f(v) -> float:
    if v is None:
        return 0.0
    try:
        s = str(v).strip().replace(",", "").replace("%", "")
        if s in ("", "-", "—", ".---", "-.--"):
            return 0.0
        return float(s)
    except (ValueError, TypeError):
        return 0.0


def compute_team_stats(hitting: list[dict], pitching: list[dict]) -> list[dict]:
    """StatsAPI の hitting / pitching split を team 名でマージし、
    FIP と wRC+ proxy を計算して返す"""
    # league average OPS for wRC+ proxy
    valid_ops = [_f(s["stat"].get("ops")) for s in hitting if _f(s["stat"].get("atBats")) > 0]
    league_ops = sum(valid_ops) / len(valid_ops) if valid_ops else 0.720

    # league aggregates for FIP constant
    lg_hr = sum(_f(s["stat"].get("homeRuns")) for s in pitching)
    lg_bb = sum(_f(s["stat"].get("baseOnBalls")) for s in pitching)
    lg_hbp = sum(_f(s["stat"].get("hitByPitch")) for s in pitching)
    lg_k = sum(_f(s["stat"].get("strikeOuts")) for s in pitching)
    lg_er = sum(_f(s["stat"].get("earnedRuns")) for s in pitching)
    lg_ip = sum(_ip_to_outs(s["stat"].get("inningsPitched")) for s in pitching)
    if lg_ip > 0:
        lg_era = 9.0 * lg_er / lg_ip
        fip_kernel_lg = (13 * lg_hr + 3 * (lg_bb + lg_hbp) - 2 * lg_k) / lg_ip
        c_fip = lg_era - fip_kernel_lg
    else:
        lg_era = 4.00
        c_fip = 3.10

    by_team: dict[int, dict] = {}
    for s in hitting:
        team = s.get("team", {})
        tid = team.get("id")
        st = s.get("stat", {})
        by_team.setdefault(tid, {})["team"] = team.get("name")
        by_team[tid]["team_id"] = tid
        by_team[tid]["bat"] = st
    for s in pitching:
        team = s.get("team", {})
        tid = team.get("id")
        st = s.get("stat", {})
        by_team.setdefault(tid, {"team": team.get("name"), "team_id": tid})["pit"] = st

    results = []
    for tid, d in by_team.items():
        bat = d.get("bat", {}) or {}
        pit = d.get("pit", {}) or {}
        # Hitting proxy
        ops = _f(bat.get("ops"))
        wrc_plus_proxy = round(100 * ops / league_ops, 1) if league_ops > 0 else None

        # Pitching FIP
        ip_outs = _ip_to_outs(pit.get("inningsPitched"))
        if ip_outs > 0:
            hr = _f(pit.get("homeRuns"))
            bb = _f(pit.get("baseOnBalls"))
            hbp = _f(pit.get("hitByPitch"))
            k = _f(pit.get("strikeOuts"))
            fip = round((13 * hr + 3 * (bb + hbp) - 2 * k) / ip_outs + c_fip, 2)
        else:
            fip = None

        entry = {
            "team": d.get("team"),
            "team_id": tid,
            # Hitting
            "wRC_plus": wrc_plus_proxy,          # ★ wRC+ proxy (OPS+ 近似)
            "wRC_plus_is_proxy": True,
            "OPS": round(ops, 3) if ops else None,
            "OBP": round(_f(bat.get("obp")), 3) if bat.get("obp") else None,
            "SLG": round(_f(bat.get("slg")), 3) if bat.get("slg") else None,
            "AVG": round(_f(bat.get("avg")), 3) if bat.get("avg") else None,
            "HR_bat": int(_f(bat.get("homeRuns"))),
            "R": int(_f(bat.get("runs"))),
            "SO_bat": int(_f(bat.get("strikeOuts"))),
            "BB_bat": int(_f(bat.get("baseOnBalls"))),
            # Pitching
            "FIP": fip,                          # ★ FIP (生スタッツから計算)
            "FIP_is_computed": True,
            "ERA": round(_f(pit.get("era")), 2) if pit.get("era") else None,
            "WHIP": round(_f(pit.get("whip")), 3) if pit.get("whip") else None,
            "IP": pit.get("inningsPitched"),
            "K_pit": int(_f(pit.get("strikeOuts"))),
            "BB_pit": int(_f(pit.get("baseOnBalls"))),
            "HR_pit": int(_f(pit.get("homeRuns"))),
            "RA": int(_f(pit.get("runs"))),
        }
        # Run differential
        entry["run_diff"] = entry["R"] - entry["RA"]
        results.append(entry)

    results.sort(key=lambda x: (x.get("wRC_plus") or 0), reverse=True)
    return results, league_ops, c_fip, lg_era


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days-stale", type=int, default=3)
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--season", default=str(datetime.now(JST).year))
    args = ap.parse_args()

    latest = latest_feed()
    if latest:
        age = age_days(latest)
        print(f"[INFO] latest feed: {latest.name} (age={age:.1f}d)")
        if args.check:
            sys.exit(0 if age <= args.days_stale else 1)
        if age <= args.days_stale and args.days_stale > 0:
            try:
                with open(latest, "r", encoding="utf-8") as f:
                    prev = json.load(f)
                prev_total = prev.get("team_count", 0)
            except Exception:
                prev_total = 0
            if prev_total > 0:
                print(f"[SKIP] age <= {args.days_stale}d and teams>0, skipping fetch.")
                sys.exit(0)
            print("[RETRY] previous feed had 0 teams, re-fetching.")
    elif args.check:
        print("[WARN] no feed yet.")
        sys.exit(1)

    try:
        hitting = fetch_stats(args.season, "hitting")
        pitching = fetch_stats(args.season, "pitching")
    except Exception as e:
        print(f"[ERR] fetch failed: {e}")
        print("[GEN006] mlb_fangraphs fetch failed.")
        sys.exit(2)

    if not hitting or not pitching:
        print("[ERR] empty stats from MLB StatsAPI")
        print("[GEN006] mlb_fangraphs fetch failed.")
        sys.exit(2)

    merged, lg_ops, c_fip, lg_era = compute_team_stats(hitting, pitching)

    data = {
        "source": f"{STATSAPI_BASE}?season={args.season}&group=hitting|pitching",
        "source_note": "Switched from fangraphs.com to MLB StatsAPI (Cloudflare bypass). "
                       "wRC+ is OPS+ proxy (100 * team_OPS / league_avg_OPS). "
                       "FIP computed from (13*HR + 3*(BB+HBP) - 2*K)/IP + cFIP.",
        "fetched_at": datetime.now(JST).isoformat(),
        "season": args.season,
        "league_context": {
            "league_avg_OPS": round(lg_ops, 3),
            "league_avg_ERA": round(lg_era, 2),
            "cFIP_constant": round(c_fip, 2),
        },
        "teams": merged,
        "team_count": len(merged),
    }
    today = datetime.now(JST).strftime("%Y-%m-%d")
    out = FEED_DIR / f"mlb_fangraphs_{today}.json"
    out.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[OK] saved: {out} (teams={data['team_count']}, lgOPS={lg_ops:.3f}, lgERA={lg_era:.2f})")


if __name__ == "__main__":
    main()
