# -*- coding: utf-8 -*-
"""
Baseball Savant (Statcast) MLB Team Advanced Metrics Fetcher

Baseball Savant は Statcast 由来の高度指標を CSV でエクスポート可能:
  https://baseballsavant.mlb.com/leaderboard/expected_statistics?type=team&year={year}&csv=true
    -> xBA / xSLG / xwOBA / xERA など「期待値系」指標 (運の影響を排除)

バッティング側・ピッチング側両方を取得し、チーム名で結合する。

使い方:
  python scripts/fetch_baseball_savant.py                   # days-stale 3
  python scripts/fetch_baseball_savant.py --days-stale 0    # 強制
  python scripts/fetch_baseball_savant.py --year 2026

出力: stats/external_feeds/mlb_savant_YYYY-MM-DD.json

取得カラム (概要):
  - bat: xBA / xSLG / xwOBA / avg_exit_velo / barrel_rate / hard_hit_pct
  - pit: xERA / p_xBA / p_xSLG / p_avg_exit_velo (被弾系)
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
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")

CSV_URLS = {
    "expected_batting":  "https://baseballsavant.mlb.com/leaderboard/expected_statistics?type=team&year={year}&position=&team=&filter=&min=q&csv=true",
    "expected_pitching": "https://baseballsavant.mlb.com/leaderboard/expected_statistics?type=teamPitchers&year={year}&position=&team=&filter=&min=q&csv=true",
}


def latest_feed() -> Path | None:
    files = sorted(FEED_DIR.glob("mlb_savant_*.json"))
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


def fetch_csv(url: str) -> list[dict]:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        raw = r.read().decode("utf-8", errors="replace")
    reader = csv.DictReader(io.StringIO(raw))
    return list(reader)


def process_mode(mode: str, year: str) -> list[dict]:
    url = CSV_URLS[mode].format(year=year)
    print(f"[FETCH] savant {mode} {year}: {url}")
    rows = fetch_csv(url)
    print(f"  -> {len(rows)} rows")
    return rows


def merge(batting: list[dict], pitching: list[dict]) -> list[dict]:
    """Baseball Savant は team name 表記が1系統。"entity_name" や "team_name" カラムに入っている"""
    def _team_key(row: dict) -> str:
        return (row.get("entity_name") or row.get("team_name") or row.get("Team") or "").strip()

    by_team: dict[str, dict] = {}
    for b in batting:
        t = _team_key(b)
        if not t:
            continue
        by_team[t] = {
            "team": t,
            "xBA": _num(b.get("xba")),
            "xSLG": _num(b.get("xslg")),
            "xwOBA": _num(b.get("xwoba")),
            "BA": _num(b.get("ba")),
            "SLG": _num(b.get("slg")),
            "wOBA": _num(b.get("woba")),
            "PA": _num(b.get("pa")),
            "diff_wOBA_xwOBA": _num(b.get("est_woba_minus_woba_diff")),
        }
    for p in pitching:
        t = _team_key(p)
        if not t:
            continue
        entry = by_team.setdefault(t, {"team": t})
        entry.update({
            "p_xERA": _num(p.get("xera")),
            "p_ERA": _num(p.get("era")),
            "p_xBA": _num(p.get("xba")),
            "p_xSLG": _num(p.get("xslg")),
            "p_xwOBA": _num(p.get("xwoba")),
            "p_BA": _num(p.get("ba")),
            "p_SLG": _num(p.get("slg")),
            "p_wOBA": _num(p.get("woba")),
        })
    out = list(by_team.values())
    out.sort(key=lambda x: (x.get("xwOBA") or 0), reverse=True)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days-stale", type=int, default=3)
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--year", default=str(datetime.now(JST).year))
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

    try:
        batting = process_mode("expected_batting", args.year)
        pitching = process_mode("expected_pitching", args.year)
    except Exception as e:
        print(f"[ERR] fetch failed: {e}")
        print("[GEN006] mlb_savant fetch failed.")
        sys.exit(2)

    merged = merge(batting, pitching)
    data = {
        "source_batting": CSV_URLS["expected_batting"].format(year=args.year),
        "source_pitching": CSV_URLS["expected_pitching"].format(year=args.year),
        "fetched_at": datetime.now(JST).isoformat(),
        "year": args.year,
        "teams": merged,
        "team_count": len(merged),
    }
    today = datetime.now(JST).strftime("%Y-%m-%d")
    out = FEED_DIR / f"mlb_savant_{today}.json"
    out.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[OK] saved: {out} (teams={data['team_count']})")


if __name__ == "__main__":
    main()
