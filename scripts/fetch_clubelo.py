# -*- coding: utf-8 -*-
"""
clubelo.com Club Elo Fetcher (Soccer L1 L1 指標)

clubelo.com は以下の CSV を直接公開しているため Playwright 不要:
  http://api.clubelo.com/{YYYY-MM-DD}  -> 全世界のクラブ Elo レーティング (指定日時点)
  http://api.clubelo.com/{ClubName}    -> 1クラブの時系列履歴

使い方:
  python scripts/fetch_clubelo.py                   # days-stale 3
  python scripts/fetch_clubelo.py --days-stale 0    # 強制
  python scripts/fetch_clubelo.py --date 2026-04-23 # 指定日

出力: stats/external_feeds/soccer_clubelo_YYYY-MM-DD.json

対象リーグ: Premier League (ENG) / La Liga (ESP) / Bundesliga (GER) / Serie A (ITA) / Ligue 1 (FRA)
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

CSV_URL = "http://api.clubelo.com/{date}"

# 対象 5 リーグ (clubelo の Country コード)
TARGET_COUNTRIES = {
    "ENG": "Premier League",
    "ESP": "La Liga",
    "GER": "Bundesliga",
    "ITA": "Serie A",
    "FRA": "Ligue 1",
}

# clubelo は1部リーグのみに Level=1 が付く仕様 (2部以下は除外)
TARGET_LEVEL = 1


def latest_feed() -> Path | None:
    files = sorted(FEED_DIR.glob("soccer_clubelo_*.json"))
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


def fetch_csv(date: str) -> list[dict]:
    url = CSV_URL.format(date=date)
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


def build_payload(date: str) -> dict:
    rows = fetch_csv(date)
    clubs_by_league: dict[str, list[dict]] = {k: [] for k in TARGET_COUNTRIES}
    all_clubs: dict[str, dict] = {}

    for r in rows:
        country = (r.get("Country") or "").strip()
        level = _num(r.get("Level"))
        if country not in TARGET_COUNTRIES:
            continue
        if level != TARGET_LEVEL:
            continue

        club = (r.get("Club") or "").strip()
        if not club:
            continue

        rank_raw = _num(r.get("Rank"))
        rank = int(rank_raw) if isinstance(rank_raw, (int, float)) else None
        entry = {
            "club": club,
            "country": country,
            "league": TARGET_COUNTRIES[country],
            "rank": rank,
            "elo": _num(r.get("Elo")),
            "level": level,
            "from": r.get("From"),
            "to": r.get("To"),
        }
        clubs_by_league[country].append(entry)
        all_clubs[club] = entry

    return {
        "source": CSV_URL.format(date=date),
        "fetched_at": datetime.now(JST).isoformat(),
        "snapshot_date": date,
        "leagues": {TARGET_COUNTRIES[k]: v for k, v in clubs_by_league.items()},
        "clubs": all_clubs,
        "club_count": len(all_clubs),
        "league_counts": {TARGET_COUNTRIES[k]: len(v) for k, v in clubs_by_league.items()},
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days-stale", type=int, default=3)
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--date", default=None, help="YYYY-MM-DD (default: today JST)")
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

    date = args.date or datetime.now(JST).strftime("%Y-%m-%d")
    print(f"[FETCH] clubelo snapshot {date} ...")
    try:
        data = build_payload(date)
    except Exception as e:
        print(f"[ERR] fetch failed: {e}")
        print("[GEN006] soccer_clubelo fetch failed.")
        sys.exit(2)

    today = datetime.now(JST).strftime("%Y-%m-%d")
    out = FEED_DIR / f"soccer_clubelo_{today}.json"
    out.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[OK] saved: {out} (clubs={data['club_count']}, leagues={data['league_counts']})")


if __name__ == "__main__":
    main()
