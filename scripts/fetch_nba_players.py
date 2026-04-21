# -*- coding: utf-8 -*-
"""
Basketball Reference NBA Player Stats Fetcher
(per_game + advanced)

出力:
  stats/external_feeds/nba_players_per_game_YYYY-MM-DD.json
  stats/external_feeds/nba_players_advanced_YYYY-MM-DD.json
"""
from __future__ import annotations
import argparse
import html as html_lib
import json
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FEED_DIR = ROOT / "stats" / "external_feeds"
FEED_DIR.mkdir(parents=True, exist_ok=True)
JST = timezone(timedelta(hours=9))
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0.0.0 Safari/537.36"

URLS = {
    "per_game": "https://www.basketball-reference.com/leagues/NBA_2026_per_game.html",
    "advanced": "https://www.basketball-reference.com/leagues/NBA_2026_advanced.html",
}
TABLE_IDS = {"per_game": "per_game_stats", "advanced": "advanced"}


def _num(v):
    if v is None:
        return None
    s = str(v).strip()
    if s in ("", "-", "—"):
        return None
    try:
        return float(s)
    except ValueError:
        return v


def age_days(p: Path) -> float:
    m = datetime.fromtimestamp(p.stat().st_mtime, tz=JST)
    return (datetime.now(JST) - m).total_seconds() / 86400


def latest_feed(kind: str) -> Path | None:
    files = sorted(FEED_DIR.glob(f"nba_players_{kind}_*.json"))
    return files[-1] if files else None


def fetch_html_playwright(url: str) -> str:
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True, args=["--disable-blink-features=AutomationControlled"])
        ctx = browser.new_context(user_agent=UA, locale="en-US")
        page = ctx.new_page()
        page.goto(url, wait_until="domcontentloaded", timeout=60000)
        try:
            # 何かしらの tbody tr が現れるまで待つ
            page.wait_for_selector("table tbody tr", timeout=30000)
        except Exception:
            pass
        content = page.content()
        browser.close()
    return content


def parse_stat_table(page: str, table_id: str) -> list[dict]:
    m = re.search(rf'<table[^>]*id="{table_id}"[^>]*>.*?</table>', page, flags=re.S)
    if not m:
        for cm in re.finditer(r'<!--(.*?)-->', page, flags=re.S):
            m2 = re.search(rf'<table[^>]*id="{table_id}"[^>]*>.*?</table>', cm.group(1), flags=re.S)
            if m2:
                m = m2
                break
    if not m:
        raise RuntimeError(f"table#{table_id} not found")

    tbody = re.search(r'<tbody.*?>(.*?)</tbody>', m.group(0), flags=re.S)
    if not tbody:
        raise RuntimeError("tbody not found")
    rows = []
    for tr in re.finditer(r'<tr[^>]*>(.*?)</tr>', tbody.group(1), flags=re.S):
        tr_open = re.search(r'<tr[^>]*>', tr.group(0)).group(0)
        if 'class="thead"' in tr_open:
            continue
        cells = {}
        for cell in re.finditer(
            r'<(th|td)[^>]*data-stat="([^"]+)"[^>]*>(.*?)</(th|td)>',
            tr.group(1), flags=re.S
        ):
            stat = cell.group(2)
            raw = cell.group(3)
            text = re.sub(r'<[^>]+>', '', raw).strip()
            text = html_lib.unescape(text)
            cells[stat] = text
        if cells.get("name_display") or cells.get("player"):
            # numeric化
            clean = {"player": cells.get("name_display") or cells.get("player")}
            for k, v in cells.items():
                if k in ("name_display", "player"):
                    continue
                clean[k] = _num(v)
            rows.append(clean)
    return rows


def process(kind: str):
    url = URLS[kind]
    tid = TABLE_IDS[kind]
    print(f"[FETCH-playwright] {kind}: {url}")
    page = fetch_html_playwright(url)
    rows = parse_stat_table(page, tid)
    payload = {
        "source": url,
        "fetched_at": datetime.now(JST).isoformat(),
        "kind": kind,
        "player_count": len(rows),
        "players": rows,
    }
    today = datetime.now(JST).strftime("%Y-%m-%d")
    out = FEED_DIR / f"nba_players_{kind}_{today}.json"
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[OK] saved {out} (rows={len(rows)})")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days-stale", type=int, default=3)
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--kind", default="both", choices=["per_game", "advanced", "both"])
    args = ap.parse_args()
    kinds = ["per_game", "advanced"] if args.kind == "both" else [args.kind]

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
            print(f"[GEN006] nba_players_{k} fetch failed.")
            sys.exit(2)


if __name__ == "__main__":
    main()
