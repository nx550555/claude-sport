# -*- coding: utf-8 -*-
"""
Basketball Reference NBA Team Ratings Fetcher (Playwright + curl フォールバック)

BBR は Cloudflare challenge を出す場合があり、素の urllib/curl では 403 or
JS challenge ページが返るため Playwright 実ブラウザで取得する。

出力: stats/external_feeds/nba_bbref_YYYY-MM-DD.json

使い方:
  python scripts/fetch_basketball_reference.py
  python scripts/fetch_basketball_reference.py --days-stale 0
"""
from __future__ import annotations
import argparse
import html
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
      "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")


def latest_feed() -> Path | None:
    files = sorted(FEED_DIR.glob("nba_bbref_*.json"))
    return files[-1] if files else None


def age_days(p: Path) -> float:
    m = datetime.fromtimestamp(p.stat().st_mtime, tz=JST)
    return (datetime.now(JST) - m).total_seconds() / 86400


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


def fetch_html_via_curl(url: str) -> str:
    """curl フォールバック（Cloudflare 未発動時のみ成功）"""
    if not shutil.which("curl"):
        return ""
    proc = subprocess.run(
        ["curl", "-sL", "--compressed", "-A", UA, "--max-time", "20", url],
        capture_output=True, text=True, encoding="utf-8", errors="replace"
    )
    out = proc.stdout or ""
    # Cloudflare challenge ページ検出
    if "cf_chl_tk" in out or '"challenge-platform"' in out:
        return ""
    return out


def fetch_html_via_playwright(url: str) -> str:
    """Playwright 実ブラウザで JS challenge 通過後の HTML を取得"""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        raise RuntimeError("playwright not installed. pip install playwright && playwright install chromium")

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True, args=["--disable-blink-features=AutomationControlled"])
        ctx = browser.new_context(user_agent=UA, locale="en-US")
        page = ctx.new_page()
        page.goto(url, wait_until="domcontentloaded", timeout=60000)
        # CF challenge 待機: ratings table が現れるか 15 秒経過まで待つ
        try:
            page.wait_for_selector("table#ratings tbody tr", timeout=30000)
        except Exception:
            # challenge 未通過の場合も一度 HTML を取る
            pass
        content = page.content()
        browser.close()
    return content


def parse_ratings_table(page: str) -> list[dict]:
    # live table
    m = re.search(r'<table[^>]*id="ratings"[^>]*>.*?</table>', page, flags=re.S)
    # コメント内テーブル
    if not m:
        for cm in re.finditer(r'<!--(.*?)-->', page, flags=re.S):
            m2 = re.search(r'<table[^>]*id="ratings"[^>]*>.*?</table>', cm.group(1), flags=re.S)
            if m2:
                m = m2
                break
    if not m:
        raise RuntimeError("id='ratings' table not found (CF challenge / layout change?)")

    table_html = m.group(0)
    tbody = re.search(r'<tbody.*?>(.*?)</tbody>', table_html, flags=re.S)
    if not tbody:
        raise RuntimeError("tbody not found")

    rows = []
    for tr in re.finditer(r'<tr[^>]*>(.*?)</tr>', tbody.group(1), flags=re.S):
        tr_open = re.search(r'<tr[^>]*>', tr.group(0)).group(0)
        if 'class="thead"' in tr_open or 'over_header' in tr_open:
            continue
        cells = {}
        for cell in re.finditer(
            r'<(th|td)[^>]*data-stat="([^"]+)"[^>]*>(.*?)</(th|td)>',
            tr.group(1), flags=re.S
        ):
            stat = cell.group(2)
            raw = cell.group(3)
            text = re.sub(r'<[^>]+>', '', raw).strip()
            text = html.unescape(text)
            cells[stat] = text
        if cells and (cells.get("team_name") or cells.get("team")):
            rows.append({
                "team": cells.get("team_name") or cells.get("team"),
                "conf": cells.get("conf_id"),
                "div": cells.get("div_id"),
                "wins": _num(cells.get("wins")),
                "losses": _num(cells.get("losses")),
                "win_pct": _num(cells.get("win_loss_pct")),
                "mov": _num(cells.get("mov")),
                "ortg": _num(cells.get("off_rtg")),
                "drtg": _num(cells.get("def_rtg")),
                "nrtg": _num(cells.get("net_rtg")),
                "mov_adj": _num(cells.get("mov_adj")),
                "ortg_adj": _num(cells.get("off_rtg_adj")),
                "drtg_adj": _num(cells.get("def_rtg_adj")),
                "nrtg_adj": _num(cells.get("net_rtg_adj")),
            })
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days-stale", type=int, default=3)
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--season", default="2026")
    ap.add_argument("--force-playwright", action="store_true", help="Skip curl attempt")
    args = ap.parse_args()

    latest = latest_feed()
    if latest:
        age = age_days(latest)
        print(f"[INFO] latest feed: {latest.name} (age={age:.1f}d)")
        if args.check:
            sys.exit(0 if age <= args.days_stale else 1)
        if age <= args.days_stale and args.days_stale > 0:
            print(f"[SKIP] fresh enough.")
            sys.exit(0)
    elif args.check:
        print("[WARN] no feed yet.")
        sys.exit(1)

    url = f"https://www.basketball-reference.com/leagues/NBA_{args.season}_ratings.html"
    print(f"[FETCH] {url} ...")

    page = ""
    teams: list = []
    # 1) まず curl（軽量）
    if not args.force_playwright:
        page = fetch_html_via_curl(url)
        if page:
            try:
                teams = parse_ratings_table(page)
                print(f"[OK-curl] parsed {len(teams)} teams via curl")
            except Exception as e:
                print(f"[INFO] curl page got but parse failed: {e}; fallback to Playwright ...")
                teams = []

    # 2) curl で取れなければ Playwright
    if not teams:
        try:
            print("[FETCH-playwright] using real browser ...")
            page = fetch_html_via_playwright(url)
            teams = parse_ratings_table(page)
            print(f"[OK-playwright] parsed {len(teams)} teams")
        except Exception as e:
            print(f"[ERR] {e}")
            print("[GEN006] Claude セッション内でユーザー依頼を発動してください。")
            sys.exit(2)

    data = {
        "source": url,
        "fetched_at": datetime.now(JST).isoformat(),
        "note": "NRtg = possession-adjusted net rating. *_adj = SOS adjusted values (preferred for L1 screening).",
        "teams": teams,
        "team_count": len(teams),
    }

    today = datetime.now(JST).strftime("%Y-%m-%d")
    out = FEED_DIR / f"nba_bbref_{today}.json"
    out.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[OK] saved {out} (teams={len(teams)})")


if __name__ == "__main__":
    main()
