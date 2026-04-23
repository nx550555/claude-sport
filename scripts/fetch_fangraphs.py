# -*- coding: utf-8 -*-
"""
FanGraphs MLB Team Stats Fetcher (FIP / wRC+)

FanGraphs の leaders ページ (team=0&season=YYYY) はサーバーサイドで
CSV 形式のエクスポートを提供。URL に &type=8 (dashboard) &team=0 (team stats) で
チーム一覧を取得可能。

使い方:
  python scripts/fetch_fangraphs.py                   # days-stale 3
  python scripts/fetch_fangraphs.py --days-stale 0    # 強制
  python scripts/fetch_fangraphs.py --season 2026     # シーズン指定

出力: stats/external_feeds/mlb_fangraphs_YYYY-MM-DD.json

取得カラム: Team / G / wRC+ / FIP / xFIP / K% / BB% / HR/9 / WAR / ERA / R / RA / Run_Diff
"""
from __future__ import annotations
import argparse
import html as html_lib
import json
import re
import shutil
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FEED_DIR = ROOT / "stats" / "external_feeds"
FEED_DIR.mkdir(parents=True, exist_ok=True)
JST = timezone(timedelta(hours=9))
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")

# FanGraphs team batting & team pitching dashboards
URLS = {
    "batting": "https://www.fangraphs.com/leaders/major-league?pos=all&stats=bat&lg=all&type=8&season={season}&month=0&ind=0&team=0,ts&rost=0&age=&filter=&players=0",
    "pitching": "https://www.fangraphs.com/leaders/major-league?pos=all&stats=pit&lg=all&type=8&season={season}&month=0&ind=0&team=0,ts&rost=0&age=&filter=&players=0",
}


def latest_feed() -> Path | None:
    files = sorted(FEED_DIR.glob("mlb_fangraphs_*.json"))
    return files[-1] if files else None


def age_days(p: Path) -> float:
    m = datetime.fromtimestamp(p.stat().st_mtime, tz=JST)
    return (datetime.now(JST) - m).total_seconds() / 86400


def _num(v):
    if v is None:
        return None
    s = str(v).strip().replace(",", "").replace("%", "")
    if s in ("", "-", "—"):
        return None
    try:
        return float(s)
    except ValueError:
        return v


def fetch_html(url: str) -> str:
    """FanGraphs は SPA のため Playwright で table 描画まで待つ必要あり。
    curl でも HTML に table が含まれるケースがある (SSR時) ので両方試行。"""
    if shutil.which("curl"):
        r = subprocess.run(
            ["curl", "-sL", "--compressed", "-A", UA, "--max-time", "30", url],
            capture_output=True, text=True, encoding="utf-8", errors="replace"
        )
        if r.returncode == 0 and r.stdout and "rgMasterTable" in r.stdout:
            return r.stdout
    # Playwright fallback
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        ctx = browser.new_context(user_agent=UA)
        page = ctx.new_page()
        page.goto(url, wait_until="domcontentloaded", timeout=60000)
        try:
            page.wait_for_selector("table.rgMasterTable tbody tr", timeout=30000)
        except Exception:
            pass
        content = page.content()
        browser.close()
    return content


def parse_table(html: str) -> list[dict]:
    m = re.search(r'<table[^>]*class="[^"]*rgMasterTable[^"]*"[^>]*>(.*?)</table>', html, flags=re.S)
    if not m:
        return []
    tbody_m = re.search(r'<tbody[^>]*>(.*?)</tbody>', m.group(1), flags=re.S)
    thead_m = re.search(r'<thead[^>]*>(.*?)</thead>', m.group(1), flags=re.S)
    if not tbody_m or not thead_m:
        return []
    # ヘッダ取得
    header_cells = re.findall(r'<th[^>]*>(.*?)</th>', thead_m.group(1), flags=re.S)
    headers = [html_lib.unescape(re.sub(r'<[^>]+>', '', h)).strip() for h in header_cells]
    # 行取得
    rows = re.findall(r'<tr[^>]*>(.*?)</tr>', tbody_m.group(1), flags=re.S)
    out = []
    for r in rows:
        cells = re.findall(r'<td[^>]*>(.*?)</td>', r, flags=re.S)
        if not cells:
            continue
        vals = [html_lib.unescape(re.sub(r'<[^>]+>', '', c)).strip() for c in cells]
        if len(vals) != len(headers):
            continue
        row = {h: _num(v) if h not in ("Team", "#", "Name") else v for h, v in zip(headers, vals)}
        out.append(row)
    return out


def process_mode(mode: str, season: str) -> list[dict]:
    url = URLS[mode].format(season=season)
    print(f"[FETCH] MLB {mode} {season}: {url}")
    html = fetch_html(url)
    rows = parse_table(html)
    print(f"  -> {len(rows)} teams parsed")
    return rows


def merge_batting_pitching(batting: list[dict], pitching: list[dict]) -> list[dict]:
    """Team 名をキーに左右結合"""
    by_team: dict[str, dict] = {}
    for b in batting:
        t = (b.get("Team") or "").strip()
        if not t:
            continue
        by_team[t] = {"team": t, "batting": b}
    for p in pitching:
        t = (p.get("Team") or "").strip()
        if not t:
            continue
        by_team.setdefault(t, {"team": t})["pitching"] = p

    merged = []
    for t, d in by_team.items():
        bat = d.get("batting", {})
        pit = d.get("pitching", {})
        entry = {
            "team": t,
            "wRC_plus": bat.get("wRC+"),
            "wOBA": bat.get("wOBA"),
            "ISO": bat.get("ISO"),
            "K_pct_bat": bat.get("K%"),
            "BB_pct_bat": bat.get("BB%"),
            "WAR_bat": bat.get("WAR"),
            "R": bat.get("R"),
            "FIP": pit.get("FIP"),
            "xFIP": pit.get("xFIP"),
            "ERA": pit.get("ERA"),
            "K_pct_pit": pit.get("K%"),
            "BB_pct_pit": pit.get("BB%"),
            "HR_per_9": pit.get("HR/9"),
            "WAR_pit": pit.get("WAR"),
            "IP": pit.get("IP"),
        }
        # Run differential proxy
        if isinstance(entry["R"], (int, float)) and isinstance(pit.get("R"), (int, float)):
            entry["run_diff"] = entry["R"] - pit.get("R")
        merged.append(entry)
    merged.sort(key=lambda x: x.get("wRC_plus") or 0, reverse=True)
    return merged


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
            print(f"[SKIP] age <= {args.days_stale}d, skipping fetch.")
            sys.exit(0)
    elif args.check:
        print("[WARN] no feed yet.")
        sys.exit(1)

    try:
        batting = process_mode("batting", args.season)
        pitching = process_mode("pitching", args.season)
    except Exception as e:
        print(f"[ERR] fetch failed: {e}")
        print("[GEN006] mlb_fangraphs fetch failed.")
        sys.exit(2)

    merged = merge_batting_pitching(batting, pitching)
    data = {
        "source_batting": URLS["batting"].format(season=args.season),
        "source_pitching": URLS["pitching"].format(season=args.season),
        "fetched_at": datetime.now(JST).isoformat(),
        "season": args.season,
        "teams": merged,
        "team_count": len(merged),
    }
    today = datetime.now(JST).strftime("%Y-%m-%d")
    out = FEED_DIR / f"mlb_fangraphs_{today}.json"
    out.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[OK] saved: {out} (teams={data['team_count']})")


if __name__ == "__main__":
    main()
