# -*- coding: utf-8 -*-
"""
MoneyPuck NHL Player (Skaters + Goalies) Fetcher

取得:
  - skaters.csv: 全 skater の situation別 statline (xG/60, on-ice xGF%, GSAA, gameScore)
  - goalies.csv: 全 goalie の GSAA, GAA, SV%, 危険度別セーブ率

出力:
  stats/external_feeds/nhl_skaters_YYYY-MM-DD.json
  stats/external_feeds/nhl_goalies_YYYY-MM-DD.json
"""
from __future__ import annotations
import argparse
import csv
import io
import json
import sys
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FEED_DIR = ROOT / "stats" / "external_feeds"
FEED_DIR.mkdir(parents=True, exist_ok=True)
JST = timezone(timedelta(hours=9))

SEASON = "2025"   # 2025-26
PHASE = "regular"

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0 Safari/537.36"

URLS = {
    "skaters": f"https://moneypuck.com/moneypuck/playerData/seasonSummary/{SEASON}/{PHASE}/skaters.csv",
    "goalies": f"https://moneypuck.com/moneypuck/playerData/seasonSummary/{SEASON}/{PHASE}/goalies.csv",
}

SKATER_KEEP = {
    # 基本
    "playerId": "player_id", "name": "name", "team": "team", "position": "position",
    "situation": "situation", "games_played": "gp", "icetime": "toi_sec",
    "gameScore": "game_score",
    # オンアイス
    "onIce_xGoalsPercentage": "on_ice_xGF_pct",
    "onIce_corsiPercentage": "on_ice_CF_pct",
    # 個人貢献
    "I_F_xGoals": "i_xG",
    "I_F_goals": "i_goals",
    "I_F_shotsOnGoal": "i_sog",
    "I_F_primaryAssists": "i_primary_a",
    "I_F_secondaryAssists": "i_secondary_a",
    "I_F_highDangerxGoals": "i_hd_xG",
    "I_F_highDangerGoals": "i_hd_goals",
    "I_F_hits": "i_hits",
    "I_F_takeaways": "i_takeaways",
    "I_F_giveaways": "i_giveaways",
    # 被攻撃
    "OnIce_F_xGoals": "on_ice_xgf_raw",
    "OnIce_A_xGoals": "on_ice_xga_raw",
}

GOALIE_KEEP = {
    "playerId": "player_id", "name": "name", "team": "team", "position": "position",
    "situation": "situation", "games_played": "gp", "icetime": "toi_sec",
    "xGoals": "xGA_expected",
    "goals": "goals_allowed",
    "ongoal": "shots_on_goal",
    "lowDangerShots": "ld_shots",
    "mediumDangerShots": "md_shots",
    "highDangerShots": "hd_shots",
    "lowDangerGoals": "ld_goals",
    "mediumDangerGoals": "md_goals",
    "highDangerGoals": "hd_goals",
}


def _num(v):
    if v in (None, ""):
        return None
    try:
        f = float(v)
        return int(f) if f.is_integer() else round(f, 4)
    except (ValueError, TypeError):
        return v


def fetch_csv(url: str) -> list[dict]:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        raw = r.read().decode("utf-8", errors="replace")
    return list(csv.DictReader(io.StringIO(raw)))


def compress(rows: list[dict], keep: dict) -> list[dict]:
    out = []
    for r in rows:
        e = {}
        for src, dst in keep.items():
            if src in r:
                e[dst] = _num(r[src])
        out.append(e)
    return out


def age_days(p: Path) -> float:
    m = datetime.fromtimestamp(p.stat().st_mtime, tz=JST)
    return (datetime.now(JST) - m).total_seconds() / 86400


def latest_feed(kind: str) -> Path | None:
    files = sorted(FEED_DIR.glob(f"nhl_{kind}_*.json"))
    return files[-1] if files else None


def process(kind: str):
    url = URLS[kind]
    keep = SKATER_KEEP if kind == "skaters" else GOALIE_KEEP
    print(f"[FETCH] NHL {kind}: {url}")
    rows = fetch_csv(url)
    data_rows = compress(rows, keep)
    # Player-level dict: player_id -> [situations]
    by_pid = {}
    for e in data_rows:
        pid = e.get("player_id")
        if pid is None:
            continue
        by_pid.setdefault(str(pid), []).append(e)

    payload = {
        "source": url,
        "fetched_at": datetime.now(JST).isoformat(),
        "season": f"{SEASON}-{int(SEASON)+1}",
        "phase": PHASE,
        "kind": kind,
        "player_count": len(by_pid),
        "by_player_id": by_pid,
    }
    today = datetime.now(JST).strftime("%Y-%m-%d")
    out = FEED_DIR / f"nhl_{kind}_{today}.json"
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[OK] saved {out} (players={len(by_pid)})")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days-stale", type=int, default=3)
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--kind", default="both", choices=["skaters", "goalies", "both"])
    args = ap.parse_args()

    kinds = ["skaters", "goalies"] if args.kind == "both" else [args.kind]

    for k in kinds:
        latest = latest_feed(k)
        if latest:
            age = age_days(latest)
            print(f"[INFO] {k}: latest={latest.name} age={age:.1f}d")
            if args.check:
                if age > args.days_stale:
                    sys.exit(1)
                continue
            if age <= args.days_stale and args.days_stale > 0:
                print(f"[SKIP] {k} fresh.")
                continue
        elif args.check:
            sys.exit(1)

        try:
            process(k)
        except Exception as e:
            print(f"[ERR] {k}: {e}")
            print(f"[GEN006] nhl_{k} fetch failed.")
            sys.exit(2)


if __name__ == "__main__":
    main()
