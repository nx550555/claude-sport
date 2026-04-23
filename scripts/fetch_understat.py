# -*- coding: utf-8 -*-
"""
understat.com xG Fetcher (Soccer 5 big leagues)

[Session_56 2026-04-23 書き直し / PA085]
- 旧: HTML 内 `var teamsData = JSON.parse('\\x7b...');` を正規表現で抽出
- 現: understat の HTML は JavaScript 変数 teamsData 非埋め込みに変更された
  (curl 18KB / Playwright 172KB いずれも teamsData=0)
- 新方式: Playwright でページを完全レンダリング → `<table>` 要素を直接 HTML パースして
  チーム別の xG/xGA/Pts をスコア行から取得する

使い方:
  python scripts/fetch_understat.py                   # days-stale 3
  python scripts/fetch_understat.py --days-stale 0    # 強制
  python scripts/fetch_understat.py --league EPL      # 1リーグのみ
  python scripts/fetch_understat.py --season 2025     # 2025-26 = "2025"

出力: stats/external_feeds/soccer_understat_YYYY-MM-DD.json

対象 5 リーグ: EPL / La_liga / Bundesliga / Serie_A / Ligue_1
"""
from __future__ import annotations
import argparse
import json
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FEED_DIR = ROOT / "stats" / "external_feeds"
FEED_DIR.mkdir(parents=True, exist_ok=True)
JST = timezone(timedelta(hours=9))
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")

LEAGUE_URLS = {
    "EPL":        "https://understat.com/league/EPL/{season}",
    "La_liga":    "https://understat.com/league/La_liga/{season}",
    "Bundesliga": "https://understat.com/league/Bundesliga/{season}",
    "Serie_A":    "https://understat.com/league/Serie_A/{season}",
    "Ligue_1":    "https://understat.com/league/Ligue_1/{season}",
}

LEAGUE_DISPLAY = {
    "EPL":        "Premier League",
    "La_liga":    "La Liga",
    "Bundesliga": "Bundesliga",
    "Serie_A":    "Serie A",
    "Ligue_1":    "Ligue 1",
}


def latest_feed() -> Path | None:
    files = sorted(FEED_DIR.glob("soccer_understat_*.json"))
    return files[-1] if files else None


def age_days(p: Path) -> float:
    m = datetime.fromtimestamp(p.stat().st_mtime, tz=JST)
    return (datetime.now(JST) - m).total_seconds() / 86400


def fetch_html_rendered(url: str) -> str:
    """Playwright で Cloudflare 突破してフルレンダリング HTML を返す。
    teamsData は消失済のため DOM table の <tr> を得ることが目的。"""
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        ctx = browser.new_context(user_agent=UA)
        page = ctx.new_page()
        page.goto(url, wait_until="networkidle", timeout=60000)
        # テーブル本体が描画されるのを待つ (複数行に team link がある状態)
        try:
            page.wait_for_function(
                "() => document.querySelectorAll('table a[href^=\"team/\"]').length >= 18",
                timeout=20000,
            )
        except Exception:
            pass
        content = page.content()
        browser.close()
    return content


_CELL_RX = re.compile(r"<td[^>]*>(.*?)</td>", flags=re.S)
_ROW_RX = re.compile(r"<tr[^>]*>(.*?)</tr>", flags=re.S)
_TABLE_RX = re.compile(r"<table[^>]*>(.*?)</table>", flags=re.S)
_TEAM_LINK_RX = re.compile(r'<a\s+href="team/([^"/]+)/[^"]+"[^>]*>([^<]+)</a>')
_NUM_RX = re.compile(r"-?\d+(?:\.\d+)?")


def _strip(s: str) -> str:
    return re.sub(r"<[^>]+>", " ", s).strip()


def _first_num(s: str) -> float | None:
    m = _NUM_RX.search(s)
    return float(m.group(0)) if m else None


def parse_league_table(html: str) -> list[dict]:
    """最初に出現する <table> を league standing として解釈。

    Column layout (Session_56 時点 understat.com 実測):
      0: rank, 1: team (link), 2: M, 3: W, 4: D, 5: L,
      6: G, 7: GA, 8: PTS, 9: xG, 10: xGA, 11: xPTS
    xG / xGA / xPTS セルは "値 <sup>±diff</sup>" 形式のため、
    第1 数値 (主値) のみを採用する。
    """
    m = _TABLE_RX.search(html)
    if not m:
        return []
    tbl = m.group(1)
    teams = []
    for r in _ROW_RX.findall(tbl):
        cells = _CELL_RX.findall(r)
        if len(cells) < 12:
            continue
        # team セル
        team_m = _TEAM_LINK_RX.search(cells[1])
        if not team_m:
            continue
        team_slug = team_m.group(1)
        team_name = team_m.group(2).strip()
        try:
            gp = int(_strip(cells[2]))
            w = int(_strip(cells[3]))
            d = int(_strip(cells[4]))
            l_ = int(_strip(cells[5]))
            g = int(_strip(cells[6]))
            ga = int(_strip(cells[7]))
            pts = int(_strip(cells[8]))
        except ValueError:
            continue
        xg = _first_num(cells[9])
        xga = _first_num(cells[10])
        xpts = _first_num(cells[11])
        if gp <= 0 or xg is None or xga is None:
            continue
        teams.append({
            "team_slug": team_slug,
            "team": team_name,
            "games_played": gp,
            "wins": w,
            "draws": d,
            "losses": l_,
            "scored": g,
            "missed": ga,
            "points": pts,
            "xG": round(xg, 2),
            "xGA": round(xga, 2),
            "xG_per_game": round(xg / gp, 3),
            "xGA_per_game": round(xga / gp, 3),
            "xGD": round(xg - xga, 2),
            "xGD_per_game": round((xg - xga) / gp, 3),
            "xPoints": round(xpts, 2) if xpts is not None else None,
        })
    teams.sort(key=lambda x: x["xGD"], reverse=True)
    return teams


def process(league: str, season: str) -> dict:
    url = LEAGUE_URLS[league].format(season=season)
    print(f"[FETCH] {league} {season}: {url}")
    html = fetch_html_rendered(url)
    teams = parse_league_table(html)
    return {
        "source": url,
        "league_key": league,
        "league_display": LEAGUE_DISPLAY[league],
        "season": f"{season}-{int(season)+1}",
        "teams": teams,
        "team_count": len(teams),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days-stale", type=int, default=3)
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--league", default="all", choices=["all"] + list(LEAGUE_URLS))
    ap.add_argument("--season", default="2025", help="2025 = 2025-26 season")
    args = ap.parse_args()

    latest = latest_feed()
    if latest:
        age = age_days(latest)
        print(f"[INFO] latest feed: {latest.name} (age={age:.1f}d)")
        if args.check:
            sys.exit(0 if age <= args.days_stale else 1)
        if age <= args.days_stale and args.days_stale > 0:
            # parse=0 空フィードは skip せず再取得 (Session_56 修復対応)
            try:
                with open(latest, "r", encoding="utf-8") as f:
                    prev = json.load(f)
                prev_total = sum(v.get("team_count", 0) for v in prev.get("leagues", {}).values())
            except Exception:
                prev_total = 0
            if prev_total > 0:
                print(f"[SKIP] age <= {args.days_stale}d and teams>0, skipping fetch.")
                sys.exit(0)
            print(f"[RETRY] previous feed had 0 teams, re-fetching.")
    elif args.check:
        print("[WARN] no feed yet.")
        sys.exit(1)

    leagues = list(LEAGUE_URLS) if args.league == "all" else [args.league]
    payload = {
        "source_group": "understat.com",
        "fetched_at": datetime.now(JST).isoformat(),
        "season": f"{args.season}-{int(args.season)+1}",
        "leagues": {},
    }
    failed = []
    for lg in leagues:
        try:
            r = process(lg, args.season)
            payload["leagues"][LEAGUE_DISPLAY[lg]] = r
            print(f"  -> {lg}: teams={r['team_count']}")
        except Exception as e:
            print(f"[ERR] {lg}: {e}")
            failed.append(lg)

    if len(failed) == len(leagues):
        print("[GEN006] all leagues fetch failed.")
        sys.exit(2)

    today = datetime.now(JST).strftime("%Y-%m-%d")
    out = FEED_DIR / f"soccer_understat_{today}.json"
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    team_total = sum(v.get("team_count", 0) for v in payload["leagues"].values())
    print(f"[OK] saved: {out} (leagues={len(payload['leagues'])}, teams_total={team_total}, failed={failed})")
    if team_total == 0:
        sys.exit(2)


if __name__ == "__main__":
    main()
