# -*- coding: utf-8 -*-
"""
tennisabstract.com ATP/WTA Elo Rating Fetcher

取得カラム: Elo_Rank / Player / Age / Elo / hElo(hard) / cElo(clay) / gElo(grass) / Peak_Elo / ATP_Rank

使い方:
  python scripts/fetch_tennis_elo.py                 # days-stale 3
  python scripts/fetch_tennis_elo.py --days-stale 0  # 強制
  python scripts/fetch_tennis_elo.py --tour atp      # ATP のみ
  python scripts/fetch_tennis_elo.py --tour wta      # WTA のみ
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

URLS = {
    "atp": "https://tennisabstract.com/reports/atp_elo_ratings.html",
    "wta": "https://tennisabstract.com/reports/wta_elo_ratings.html",
}


def _num(v):
    if v is None:
        return None
    s = str(v).strip().replace("\xa0", "").replace(",", "")
    if s in ("", "-", "—"):
        return None
    try:
        return float(s)
    except ValueError:
        return v


def age_days(p: Path) -> float:
    m = datetime.fromtimestamp(p.stat().st_mtime, tz=JST)
    return (datetime.now(JST) - m).total_seconds() / 86400


def latest_feed(tour: str) -> Path | None:
    files = sorted(FEED_DIR.glob(f"tennis_{tour}_elo_*.json"))
    return files[-1] if files else None


def fetch_html(url: str) -> str:
    """curl → Playwright fallback"""
    if shutil.which("curl"):
        r = subprocess.run(
            ["curl", "-sL", "--compressed", "-A", UA, "--max-time", "30", url],
            capture_output=True, text=True, encoding="utf-8", errors="replace"
        )
        if r.returncode == 0 and r.stdout and "cf_chl_tk" not in r.stdout:
            return r.stdout
    # Playwright fallback
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        ctx = browser.new_context(user_agent=UA)
        page = ctx.new_page()
        page.goto(url, wait_until="domcontentloaded", timeout=60000)
        try:
            page.wait_for_selector("table#reportable tr", timeout=20000)
        except Exception:
            pass
        content = page.content()
        browser.close()
    return content


def parse_elo(html: str) -> list[dict]:
    m = re.search(r'<table[^>]*id="reportable"[^>]*>(.*?)</table>', html, flags=re.S)
    if not m:
        raise RuntimeError("id='reportable' not found")
    t = m.group(1)
    rows = re.findall(r'<tr[^>]*>(.*?)</tr>', t, flags=re.S)
    out = []
    for r in rows:
        cells = re.findall(r'<td[^>]*>(.*?)</td>', r, flags=re.S)
        if len(cells) < 16:
            continue
        clean = [html_lib.unescape(re.sub(r'<[^>]+>', '', c)).replace('\xa0', ' ').strip() for c in cells]
        # ヘッダー順: Rank / Player / Age / Elo / '' / hRank / hElo / cRank / cElo / gRank / gElo / '' / PeakElo / PeakMonth / '' / ATPRank / LogDiff
        try:
            entry = {
                "elo_rank": int(_num(clean[0]) or 0),
                "player": clean[1],
                "age": _num(clean[2]),
                "elo": _num(clean[3]),
                "hard_elo_rank": int(_num(clean[5]) or 0),
                "hard_elo": _num(clean[6]),
                "clay_elo_rank": int(_num(clean[7]) or 0),
                "clay_elo": _num(clean[8]),
                "grass_elo_rank": int(_num(clean[9]) or 0),
                "grass_elo": _num(clean[10]),
                "peak_elo": _num(clean[12]),
                "peak_month": clean[13],
                "atp_rank": _num(clean[15]) if len(clean) > 15 else None,
                "log_diff": _num(clean[16]) if len(clean) > 16 else None,
            }
            if entry["player"]:
                out.append(entry)
        except (ValueError, IndexError):
            continue
    return out


def process(tour: str):
    url = URLS[tour]
    print(f"[FETCH] {tour.upper()} elo: {url}")
    html = fetch_html(url)
    players = parse_elo(html)
    data = {
        "source": url,
        "tour": tour,
        "fetched_at": datetime.now(JST).isoformat(),
        "player_count": len(players),
        "columns_note": "elo=全体 / hard_elo=ハード / clay_elo=クレー / grass_elo=芝。いずれも rank と レーティング値。",
        "players": players,
    }
    today = datetime.now(JST).strftime("%Y-%m-%d")
    out = FEED_DIR / f"tennis_{tour}_elo_{today}.json"
    out.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[OK] saved {out} (players={len(players)})")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days-stale", type=int, default=3)
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--tour", default="both", choices=["atp", "wta", "both"])
    args = ap.parse_args()

    tours = ["atp", "wta"] if args.tour == "both" else [args.tour]

    for tour in tours:
        latest = latest_feed(tour)
        if latest:
            age = age_days(latest)
            print(f"[INFO] {tour}: latest={latest.name} age={age:.1f}d")
            if args.check:
                if age > args.days_stale:
                    sys.exit(1)
                continue
            if age <= args.days_stale and args.days_stale > 0:
                print(f"[SKIP] {tour} fresh.")
                continue
        elif args.check:
            print(f"[WARN] {tour}: no feed")
            sys.exit(1)

        try:
            process(tour)
        except Exception as e:
            print(f"[ERR] {tour}: {e}")
            print(f"[GEN006] tennis_{tour}_elo fetch failed.")
            sys.exit(2)


if __name__ == "__main__":
    main()
