# -*- coding: utf-8 -*-
"""
Tennis Abstract MCP (Match Charting Project) Leaders Fetcher
直近52週のサーブ・リターン統計を ATP/WTA ごとに取得

出力: stats/external_feeds/tennis_{atp|wta}_player_stats_YYYY-MM-DD.json
スキーマ:
  {
    "serve": [ {player, matches, unret_pct, rip_w_pct, sv_impact, 1st_unret_pct, ...}, ...],
    "return": [ {player, matches, return_pts_won, ...}, ...]
  }
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
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0 Safari/537.36"

URLS = {
    "atp": {
        "serve":  "https://tennisabstract.com/reports/mcp_leaders_serve_men_last52.html",
        "return": "https://tennisabstract.com/reports/mcp_leaders_return_men_last52.html",
        "rally":  "https://tennisabstract.com/reports/mcp_leaders_rally_men_last52.html",
    },
    "wta": {
        "serve":  "https://tennisabstract.com/reports/mcp_leaders_serve_women_last52.html",
        "return": "https://tennisabstract.com/reports/mcp_leaders_return_women_last52.html",
        "rally":  "https://tennisabstract.com/reports/mcp_leaders_rally_women_last52.html",
    },
}


def _num(v):
    if v is None:
        return None
    s = str(v).strip().replace("\xa0", " ").replace("%", "")
    if s in ("", "-"):
        return None
    try:
        return float(s)
    except ValueError:
        return v


def fetch_html(url: str) -> str:
    if shutil.which("curl"):
        r = subprocess.run(
            ["curl", "-sL", "--compressed", "-A", UA, "--max-time", "30", url],
            capture_output=True, text=True, encoding="utf-8", errors="replace"
        )
        if r.returncode == 0 and r.stdout and "cf_chl_tk" not in r.stdout:
            return r.stdout
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        b = pw.chromium.launch(headless=True)
        c = b.new_context(user_agent=UA)
        p = c.new_page()
        p.goto(url, wait_until="domcontentloaded", timeout=60000)
        try:
            p.wait_for_selector("table#reportable tr", timeout=20000)
        except Exception:
            pass
        content = p.content()
        b.close()
    return content


def parse_table(html: str) -> tuple[list, list]:
    m = re.search(r'<table[^>]*id="reportable"[^>]*>(.*?)</table>', html, flags=re.S)
    if not m:
        raise RuntimeError("id='reportable' not found")
    t = m.group(1)

    # ヘッダー抽出
    hs = re.findall(r'<th[^>]*>(.*?)</th>', t, flags=re.S)
    headers = [html_lib.unescape(re.sub(r'<[^>]+>', '', h)).replace('\xa0', ' ').strip() for h in hs]

    # 行抽出
    rows = re.findall(r'<tr[^>]*>(.*?)</tr>', t, flags=re.S)
    out = []
    for r in rows:
        cells = re.findall(r'<td[^>]*>(.*?)</td>', r, flags=re.S)
        if not cells:
            continue
        clean = [html_lib.unescape(re.sub(r'<[^>]+>', '', c)).replace('\xa0', ' ').strip() for c in cells]
        if not clean[0]:
            continue
        entry = {"player": clean[0]}
        for i, h in enumerate(headers[1:], start=1):
            if i < len(clean):
                entry[h] = _num(clean[i])
        out.append(entry)
    return headers, out


def age_days(p: Path) -> float:
    m = datetime.fromtimestamp(p.stat().st_mtime, tz=JST)
    return (datetime.now(JST) - m).total_seconds() / 86400


def latest_feed(tour: str) -> Path | None:
    files = sorted(FEED_DIR.glob(f"tennis_{tour}_player_stats_*.json"))
    return files[-1] if files else None


def process(tour: str):
    print(f"[FETCH] {tour.upper()} player stats (serve + return + rally)")
    result = {
        "tour": tour,
        "source_note": "tennisabstract Match Charting Project (MCP) Leaders - last 52 weeks",
        "fetched_at": datetime.now(JST).isoformat(),
    }
    for kind, url in URLS[tour].items():
        html = fetch_html(url)
        headers, rows = parse_table(html)
        result[kind] = {
            "source": url,
            "headers": headers,
            "rows": rows,
            "count": len(rows),
        }
        print(f"  - {kind}: {len(rows)} players")

    today = datetime.now(JST).strftime("%Y-%m-%d")
    out = FEED_DIR / f"tennis_{tour}_player_stats_{today}.json"
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[OK] saved {out}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days-stale", type=int, default=7)
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--tour", default="both", choices=["atp", "wta", "both"])
    args = ap.parse_args()

    tours = ["atp", "wta"] if args.tour == "both" else [args.tour]
    for t in tours:
        latest = latest_feed(t)
        if latest:
            age = age_days(latest)
            print(f"[INFO] {t}: latest={latest.name} age={age:.1f}d")
            if args.check:
                if age > args.days_stale:
                    sys.exit(1)
                continue
            if age <= args.days_stale and args.days_stale > 0:
                print(f"[SKIP] {t} fresh.")
                continue
        elif args.check:
            sys.exit(1)

        try:
            process(t)
        except Exception as e:
            print(f"[ERR] {t}: {e}")
            print(f"[GEN006] tennis_{t}_player_stats fetch failed.")
            sys.exit(2)


if __name__ == "__main__":
    main()
