# -*- coding: utf-8 -*-
"""
MoneyPuck NHL Team xGF% Fetcher (A案 軽量版)

MoneyPuck は以下の CSV を直接公開しているため Playwright 不要。
  https://moneypuck.com/moneypuck/playerData/seasonSummary/{season}/{regular|playoffs}/teams.csv

使い方:
  python scripts/fetch_moneypuck.py                  # 既存キャッシュが3日以内ならスキップ
  python scripts/fetch_moneypuck.py --days-stale 0   # 強制取得
  python scripts/fetch_moneypuck.py --check          # 状態確認のみ
  python scripts/fetch_moneypuck.py --season 2025 --phase regular

出力: stats/external_feeds/nhl_moneypuck_YYYY-MM-DD.json

situation キー:
  "all"  = All Situations (default for L1)
  "5on5" = 5v5 (PDO/xGF% で最も信頼性高)
  "4on5" = Shorthanded PK
  "5on4" = Power Play
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

SEASON_DEFAULT = "2025"   # 2025-26 season = "2025"
PHASE_DEFAULT = "regular"  # or "playoffs"
CSV_URL = "https://moneypuck.com/moneypuck/playerData/seasonSummary/{season}/{phase}/teams.csv"

# 集計したい situation 一覧（L1 で最重要）
SITUATIONS_OF_INTEREST = ["all", "5on5"]


def latest_feed() -> Path | None:
    files = sorted(FEED_DIR.glob("nhl_moneypuck_*.json"))
    return files[-1] if files else None


def age_days(p: Path) -> float:
    m = datetime.fromtimestamp(p.stat().st_mtime, tz=JST)
    return (datetime.now(JST) - m).total_seconds() / 86400


def _num(v):
    if v is None:
        return None
    s = str(v).strip()
    if s in ("", "-", "N/A"):
        return None
    try:
        return float(s)
    except ValueError:
        return v


def fetch_csv(season: str, phase: str) -> list[dict]:
    url = CSV_URL.format(season=season, phase=phase)
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
            )
        },
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        raw = r.read().decode("utf-8")
    reader = csv.DictReader(io.StringIO(raw))
    return list(reader)


def build_payload(season: str, phase: str) -> dict:
    rows = fetch_csv(season, phase)
    teams_by_situation: dict[str, dict[str, dict]] = {}

    for r in rows:
        situ = r.get("situation", "")
        if situ not in SITUATIONS_OF_INTEREST:
            continue
        # MoneyPuck CSV は 'name'(abbr) と 'team'(abbr) 両方にチーム略称が入る
        tabbr = r.get("name") or r.get("team")
        if not tabbr:
            continue

        # score-adjusted xG For/Against は別カラム → 比率も算出
        sv_for = _num(r.get("scoreVenueAdjustedxGoalsFor"))
        sv_against = _num(r.get("scoreVenueAdjustedxGoalsAgainst"))
        sv_pct = None
        if isinstance(sv_for, (int, float)) and isinstance(sv_against, (int, float)) and (sv_for + sv_against) > 0:
            sv_pct = round(sv_for / (sv_for + sv_against) * 100, 2)

        xgf_pct_raw = _num(r.get("xGoalsPercentage"))
        # MoneyPuck の xGoalsPercentage は 0-1 範囲 (例: 0.47 = 47%)
        xgf_pct = round(xgf_pct_raw * 100, 2) if isinstance(xgf_pct_raw, (int, float)) else None

        cf_raw = _num(r.get("corsiPercentage"))
        cf_pct = round(cf_raw * 100, 2) if isinstance(cf_raw, (int, float)) else None
        ff_raw = _num(r.get("fenwickPercentage"))
        ff_pct = round(ff_raw * 100, 2) if isinstance(ff_raw, (int, float)) else None

        gf = _num(r.get("goalsFor"))
        ga = _num(r.get("goalsAgainst"))
        gf_pct = None
        if isinstance(gf, (int, float)) and isinstance(ga, (int, float)) and (gf + ga) > 0:
            gf_pct = round(gf / (gf + ga) * 100, 2)

        entry = {
            "team": tabbr,
            "games_played": _num(r.get("games_played")),
            "xGF_pct": xgf_pct,                   # 0-100%
            "xGF_pct_score_adj": sv_pct,          # score-adjusted %
            "CF_pct": cf_pct,
            "FF_pct": ff_pct,
            "GF": gf,
            "GA": ga,
            "GF_pct": gf_pct,
            "xGoalsFor": _num(r.get("xGoalsFor")),
            "xGoalsAgainst": _num(r.get("xGoalsAgainst")),
            "scoreVenueAdjustedxGoalsFor": sv_for,
            "scoreVenueAdjustedxGoalsAgainst": sv_against,
        }
        teams_by_situation.setdefault(situ, {})[tabbr] = entry

    return {
        "source": CSV_URL.format(season=season, phase=phase),
        "fetched_at": datetime.now(JST).isoformat(),
        "season": f"{season}-{int(season)+1}",
        "phase": phase,
        "situations_available": list(teams_by_situation.keys()),
        "teams": teams_by_situation.get("all", {}),    # default "all" for easy access
        "teams_5on5": teams_by_situation.get("5on5", {}),
        "team_count": len(teams_by_situation.get("all", {})),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days-stale", type=int, default=3)
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--season", default=SEASON_DEFAULT)
    ap.add_argument("--phase", default=PHASE_DEFAULT, choices=["regular", "playoffs"])
    args = ap.parse_args()

    latest = latest_feed()
    if latest:
        age = age_days(latest)
        print(f"[INFO] latest feed: {latest.name} (age={age:.1f}d)")
        if args.check:
            sys.exit(0 if age <= args.days_stale else 1)
        if age <= args.days_stale and args.days_stale > 0:
            print(f"[SKIP] age <= {args.days_stale}d, skipping fetch.")
            sys.exit(0)
    elif args.check:
        print("[WARN] no feed yet.")
        sys.exit(1)

    print(f"[FETCH] MoneyPuck {args.season} {args.phase} CSV ...")
    try:
        data = build_payload(args.season, args.phase)
    except Exception as e:
        print(f"[ERR] fetch failed: {e}")
        print("[GEN006] Claude セッション内でユーザーにスタッツ提供依頼を発動してください。")
        sys.exit(2)

    today = datetime.now(JST).strftime("%Y-%m-%d")
    tag = "" if args.phase == "regular" else f"_{args.phase}"
    out = FEED_DIR / f"nhl_moneypuck{tag}_{today}.json"
    out.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[OK] saved: {out} (teams={data['team_count']}, situations={data['situations_available']})")


if __name__ == "__main__":
    main()
