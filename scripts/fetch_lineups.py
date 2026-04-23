# -*- coding: utf-8 -*-
"""
STEP 4.5 スタメン確認統合 Fetcher

対象スポーツ: nba / nfl / soccer / mlb / rugby (nrl/superrugby/premiership/top14/prod2/super_league)

各スポーツのスタメン情報源:
  NBA:     rotowire.com/basketball/nba-lineups.php
  NFL:     rotowire.com/football/nfl-lineups.php
  MLB:     rotowire.com/baseball/daily-lineups.php
  Soccer:  rotowire.com/soccer/lineups.php
  Rugby:   各リーグ公式 team sheets (ESPN scrum or league sites)

使い方:
  python scripts/fetch_lineups.py --sport all            # 全スポーツ取得
  python scripts/fetch_lineups.py --sport soccer         # サッカーのみ
  python scripts/fetch_lineups.py --sport mlb --date 2026-04-23
  python scripts/fetch_lineups.py --days-stale 0         # 強制 (lineups は頻繁変更のため)

出力: stats/external_feeds/lineups_YYYY-MM-DD.json

構造:
{
  "fetched_at": "2026-04-23T18:30:00+09:00",
  "nba":    { "Lakers": {"starters":[...], "out":[...], "questionable":[...]}, ... },
  "nfl":    { ... },
  "soccer": { "Real Madrid": {"starters":[...], "formation":"4-3-3", "gk": "Courtois"}, ... },
  "mlb":    { "Yankees": {"lineup":[...], "starting_pitcher": "Cole"}, ... },
  "rugby":  { "Chiefs": {"starters":[...], "bench":[...], "captain":"..."}, ... }
}

lineups は 1 日内で複数回更新されるため、age_days < 1 でも最新 fetch 推奨。
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
    "nba":    "https://www.rotowire.com/basketball/nba-lineups.php",
    "nfl":    "https://www.rotowire.com/football/nfl-lineups.php",
    "mlb":    "https://www.rotowire.com/baseball/daily-lineups.php",
    "soccer": "https://www.rotowire.com/soccer/lineups.php",
}

SUPPORTED = ["nba", "nfl", "mlb", "soccer", "rugby"]
RUGBY_NOTE = "Rugby lineups: 公式 team sheets or ESPN scrum. Currently returns empty skeleton (user can feed manually)."


def today_feed(date: str | None = None) -> Path:
    d = date or datetime.now(JST).strftime("%Y-%m-%d")
    return FEED_DIR / f"lineups_{d}.json"


def age_hours(p: Path) -> float:
    m = datetime.fromtimestamp(p.stat().st_mtime, tz=JST)
    return (datetime.now(JST) - m).total_seconds() / 3600


def fetch_html(url: str, require_selector: str | None = None) -> str:
    """curl → Playwright fallback。Rotowire は SPA なので Playwright 優先が安全"""
    if shutil.which("curl"):
        r = subprocess.run(
            ["curl", "-sL", "--compressed", "-A", UA, "--max-time", "30", url],
            capture_output=True, text=True, encoding="utf-8", errors="replace"
        )
        if r.returncode == 0 and r.stdout and (not require_selector or require_selector.replace('.', '').replace('#', '') in r.stdout):
            return r.stdout
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        ctx = browser.new_context(user_agent=UA)
        page = ctx.new_page()
        page.goto(url, wait_until="domcontentloaded", timeout=60000)
        if require_selector:
            try:
                page.wait_for_selector(require_selector, timeout=20000)
            except Exception:
                pass
        content = page.content()
        browser.close()
    return content


def _clean(s: str) -> str:
    return html_lib.unescape(re.sub(r'<[^>]+>', '', s)).replace('\xa0', ' ').strip()


def parse_rotowire_game_cards(html: str, sport: str) -> dict:
    """Rotowire の各スポーツ共通的な lineups__item カードから情報抽出。
    Rotowire の HTML 構造は SPA だが、SSR で初期HTML に入っていることが多い。"""
    out: dict[str, dict] = {}
    # team name ... followed by player list
    # Rotowire classes vary; try general approach: extract all <div class="lineup">
    game_cards = re.findall(r'<div[^>]*class="[^"]*lineup__main[^"]*"[^>]*>(.*?)</div>\s*</div>\s*</div>', html, flags=re.S)
    if not game_cards:
        # Generic fallback: find team blocks by h4.lineup__name
        for m in re.finditer(
            r'<h4[^>]*class="[^"]*lineup__name[^"]*"[^>]*>(.*?)</h4>(.*?)(?=<h4[^>]*class="[^"]*lineup__name|$)',
            html, flags=re.S,
        ):
            team = _clean(m.group(1))
            block = m.group(2)
            if not team:
                continue
            players = [_clean(p) for p in re.findall(r'<a[^>]*class="[^"]*lineup__player[^"]*"[^>]*>(.*?)</a>', block, flags=re.S)]
            if not players:
                players = [_clean(p) for p in re.findall(r'<a[^>]*player[^"]*"[^>]*>(.*?)</a>', block, flags=re.S)]
            if players:
                out[team] = {"starters": players[:11 if sport == "soccer" else 9]}
    return out


def fetch_nba(html: str) -> dict:
    base = parse_rotowire_game_cards(html, "nba")
    return base


def fetch_nfl(html: str) -> dict:
    return parse_rotowire_game_cards(html, "nfl")


def fetch_mlb(html: str) -> dict:
    """MLB は先発投手 + 打線 1-9番 が別要素"""
    out: dict[str, dict] = {}
    # lineup__main block per team
    for m in re.finditer(
        r'<div[^>]*class="[^"]*lineup__team[^"]*"[^>]*>(.*?)</div>.*?<div[^>]*class="[^"]*lineup__list[^"]*"[^>]*>(.*?)</div>',
        html, flags=re.S,
    ):
        team_block = m.group(1)
        list_block = m.group(2)
        team_name_m = re.search(r'<a[^>]*>([^<]+)</a>', team_block)
        team = _clean(team_name_m.group(1)) if team_name_m else ""
        if not team:
            continue
        starters = [_clean(p) for p in re.findall(r'<li[^>]*>(.*?)</li>', list_block, flags=re.S)]
        # starting pitcher (if tagged)
        sp_m = re.search(r'lineup__player-highlight[^>]*>(.*?)</a>', list_block, flags=re.S)
        sp = _clean(sp_m.group(1)) if sp_m else None
        out[team] = {"lineup": starters[:9], "starting_pitcher": sp}
    # fallback if structure unmatched
    if not out:
        out = parse_rotowire_game_cards(html, "mlb")
    return out


def fetch_soccer(html: str) -> dict:
    """Soccer: formation + GK + 10 field players"""
    out: dict[str, dict] = {}
    # rotowire soccer: each team block includes formation and player list
    for m in re.finditer(
        r'<h4[^>]*class="[^"]*lineup__name[^"]*"[^>]*>(.*?)</h4>(.*?)(?=<h4[^>]*class="[^"]*lineup__name|</article>|$)',
        html, flags=re.S,
    ):
        team = _clean(m.group(1))
        block = m.group(2)
        if not team:
            continue
        players = [_clean(p) for p in re.findall(r'<a[^>]*class="[^"]*lineup__player[^"]*"[^>]*>(.*?)</a>', block, flags=re.S)]
        formation_m = re.search(r'lineup__formation[^>]*>([^<]+)<', block)
        form = _clean(formation_m.group(1)) if formation_m else None
        if players:
            out[team] = {
                "formation": form,
                "gk": players[0] if players else None,
                "starters": players[:11],
            }
    return out


def fetch_rugby_stub() -> dict:
    """ラグビーは公式 team sheets を個別取得する必要がある。
    初期実装では空の skeleton を返し、ユーザーが手動追加する想定。"""
    return {}


def fetch_sport(sport: str) -> dict:
    if sport == "rugby":
        return fetch_rugby_stub()
    url = URLS.get(sport)
    if not url:
        return {}
    print(f"[FETCH] {sport}: {url}")
    html = fetch_html(url, require_selector=".lineup__name")
    if sport == "nba":
        return fetch_nba(html)
    if sport == "nfl":
        return fetch_nfl(html)
    if sport == "mlb":
        return fetch_mlb(html)
    if sport == "soccer":
        return fetch_soccer(html)
    return {}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days-stale", type=float, default=0.5, help="age (days) above which to re-fetch. Default 0.5 = 12h")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--sport", default="all", choices=["all"] + SUPPORTED)
    ap.add_argument("--date", default=None, help="YYYY-MM-DD override")
    args = ap.parse_args()

    out_path = today_feed(args.date)
    if out_path.exists():
        age = age_hours(out_path) / 24
        print(f"[INFO] latest: {out_path.name} (age={age:.2f}d)")
        if args.check:
            sys.exit(0 if age <= args.days_stale else 1)
        if age <= args.days_stale and args.days_stale > 0:
            print(f"[SKIP] age <= {args.days_stale}d")
            sys.exit(0)
    elif args.check:
        print("[WARN] no lineups yet")
        sys.exit(1)

    sports = SUPPORTED if args.sport == "all" else [args.sport]
    payload = {
        "fetched_at": datetime.now(JST).isoformat(),
        "date": args.date or datetime.now(JST).strftime("%Y-%m-%d"),
        "sports_covered": sports,
        "rugby_note": RUGBY_NOTE,
    }
    failed = []
    for sp in sports:
        try:
            payload[sp] = fetch_sport(sp)
            n = len(payload[sp])
            print(f"  -> {sp}: {n} teams")
        except Exception as e:
            print(f"[ERR] {sp}: {e}")
            failed.append(sp)
            payload[sp] = {}

    # マージ: 既存 lineups_{date}.json があれば統合 (複数回 fetch 時の差分反映)
    if out_path.exists():
        try:
            existing = json.loads(out_path.read_text(encoding="utf-8-sig"))
            for sp in SUPPORTED:
                if sp in existing and sp not in payload:
                    payload[sp] = existing[sp]
                elif sp in existing and sp in payload:
                    # 新しい方を優先しつつ空欄の既存を補完
                    for team, lineup in existing[sp].items():
                        if team not in payload[sp]:
                            payload[sp][team] = lineup
        except Exception:
            pass

    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    total = sum(len(payload.get(sp, {})) for sp in SUPPORTED)
    print(f"[OK] saved: {out_path} (total teams={total}, failed={failed})")


if __name__ == "__main__":
    main()
