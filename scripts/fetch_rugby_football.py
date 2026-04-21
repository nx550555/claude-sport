# -*- coding: utf-8 -*-
"""
Rugby / American Football チーム standings Fetcher
リーグ横断で standings (PF/PA/PD, W/L, Points) を統一スキーマで取得

対応リーグ: nrl, superrugby, premiership, top14, prod2, superleague, ufl, cfl

出力: stats/external_feeds/{league}_standings_YYYY-MM-DD.json
統一スキーマ:
  {"league":"nrl","source":...,"fetched_at":...,"teams":[
    {"team":"Panthers","gp":6,"w":5,"l":1,"d":0,"pf":150,"pa":80,"pd":70,"pd_per_game":11.7,"pts":10}
  ]}
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

# 各リーグの URL と fetch 戦略
LEAGUES = {
    "nrl":        {"url": "https://www.nrl.com/ladder/", "strategy": "playwright_nrl"},
    "superrugby": {"url": "https://en.wikipedia.org/wiki/2026_Super_Rugby_Pacific_season", "strategy": "wikipedia_table"},
    "premiership":{"url": "https://en.wikipedia.org/wiki/2025%E2%80%9326_Premiership_Rugby", "strategy": "wikipedia_table"},
    "top14":      {"url": "https://en.wikipedia.org/wiki/2025%E2%80%9326_Top_14_season", "strategy": "wikipedia_table"},
    "prod2":      {"url": "https://en.wikipedia.org/wiki/2025%E2%80%9326_Rugby_Pro_D2_season", "strategy": "wikipedia_table"},
    "superleague":{"url": "https://en.wikipedia.org/wiki/2026_Super_League_season", "strategy": "wikipedia_table"},
    "ufl":        {"url": "https://en.wikipedia.org/wiki/2026_UFL_season", "strategy": "wikipedia_table"},
    "cfl":        {"url": "https://en.wikipedia.org/wiki/2026_CFL_season", "strategy": "wikipedia_table"},
}


def _num(v):
    if v is None:
        return None
    s = str(v).strip().replace("+", "").replace(",", "").replace("\xa0", "")
    if s in ("", "-", "–", "—"):
        return None
    try:
        return float(s) if "." in s else int(s)
    except ValueError:
        return v


def age_days(p: Path) -> float:
    m = datetime.fromtimestamp(p.stat().st_mtime, tz=JST)
    return (datetime.now(JST) - m).total_seconds() / 86400


def latest_feed(league: str) -> Path | None:
    files = sorted(FEED_DIR.glob(f"{league}_standings_*.json"))
    return files[-1] if files else None


def curl_html(url: str) -> str:
    if not shutil.which("curl"):
        return ""
    r = subprocess.run(
        ["curl", "-sL", "--compressed", "-A", UA, "--max-time", "30", url],
        capture_output=True, text=True, encoding="utf-8", errors="replace"
    )
    if r.returncode == 0 and r.stdout and "cf_chl_tk" not in r.stdout:
        return r.stdout
    return ""


def playwright_html(url: str, wait_selector: str | None = None) -> str:
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        b = pw.chromium.launch(headless=True)
        c = b.new_context(user_agent=UA, locale="en-US")
        p = c.new_page()
        p.goto(url, wait_until="domcontentloaded", timeout=60000)
        if wait_selector:
            try:
                p.wait_for_selector(wait_selector, timeout=20000)
            except Exception:
                pass
        else:
            p.wait_for_timeout(3000)
        content = p.content()
        b.close()
    return content


# ===== パーサー: リーグごとに適した実装 =====

def parse_wikipedia_table(html: str, prefer_keywords=("Team", "Club", "Franchise")) -> list[dict]:
    """Wikipedia のリーグ standings は class=\"wikitable\" に格納されている。
    最初にチーム名らしきカラム + PF/PA らしきカラムを含むテーブルを選ぶ。"""
    tables = re.findall(r'<table[^>]*class="[^"]*wikitable[^"]*"[^>]*>.*?</table>', html, flags=re.S)
    best_rows = None
    best_score = -1
    for t in tables:
        rows = _parse_generic_table(t)
        if not rows:
            continue
        # 先頭行見出しでランク付け
        header_row = rows[0]
        joined = " | ".join(str(c) for c in header_row).lower()
        score = 0
        for kw in ("pd", "pf", "pa", "points for", "for", "diff"):
            if kw in joined:
                score += 1
        for kw in prefer_keywords:
            if kw.lower() in joined:
                score += 2
        if score > best_score:
            best_score = score
            best_rows = rows
    if not best_rows:
        return []
    return _normalize_standings(best_rows)


def _parse_generic_table(table_html: str) -> list[list]:
    rows = []
    for tr in re.finditer(r'<tr[^>]*>(.*?)</tr>', table_html, flags=re.S):
        cells = re.findall(r'<(?:th|td)[^>]*>(.*?)</(?:th|td)>', tr.group(1), flags=re.S)
        clean = []
        for c in cells:
            # colspan/rowspan 処理は簡略化
            text = re.sub(r'<[^>]+>', '', c)
            text = html_lib.unescape(text).strip()
            clean.append(text)
        if clean:
            rows.append(clean)
    return rows


def _normalize_standings(rows: list[list]) -> list[dict]:
    """先頭行をヘッダとして team/gp/w/l/pf/pa/pd/pts を推定抽出"""
    if len(rows) < 2:
        return []
    hdr = [h.lower() for h in rows[0]]
    def idx(*keys):
        for k in keys:
            for i, h in enumerate(hdr):
                if k in h:
                    return i
        return None
    col_team = idx("team", "club", "franchise", "side")
    col_gp   = idx("played", "pld", "gp", " p ")
    col_w    = idx("won", "wins", " w ")
    col_l    = idx("lost", "losses", " l ")
    col_d    = idx("draw", "drawn", "ties", " d ")
    col_pf   = idx("points for", "pf", "for")
    col_pa   = idx("against", "pa")
    col_pd   = idx("diff", "pd", " +/-")
    col_pts  = idx("points", "pts")

    out = []
    for r in rows[1:]:
        if len(r) < 2 or col_team is None:
            continue
        team = r[col_team]
        # Wikipedia の position 列がある場合、team 部分がリンクを含むので clean
        team = re.sub(r'^\d+\s+', '', team).strip()
        if not team or len(team) > 80:
            continue
        entry = {
            "team": team,
            "gp":   _num(r[col_gp]) if col_gp is not None and col_gp < len(r) else None,
            "w":    _num(r[col_w])  if col_w  is not None and col_w  < len(r) else None,
            "l":    _num(r[col_l])  if col_l  is not None and col_l  < len(r) else None,
            "d":    _num(r[col_d])  if col_d  is not None and col_d  < len(r) else None,
            "pf":   _num(r[col_pf]) if col_pf is not None and col_pf < len(r) else None,
            "pa":   _num(r[col_pa]) if col_pa is not None and col_pa < len(r) else None,
            "pd":   _num(r[col_pd]) if col_pd is not None and col_pd < len(r) else None,
            "pts":  _num(r[col_pts]) if col_pts is not None and col_pts < len(r) else None,
        }
        # PD/game 計算
        if isinstance(entry["pd"], (int, float)) and isinstance(entry["gp"], (int, float)) and entry["gp"]:
            entry["pd_per_game"] = round(entry["pd"] / entry["gp"], 2)
        # Team 名に数字が付いてるケースを除外
        if re.match(r'^\d+$', str(entry["team"])):
            continue
        out.append(entry)
    return out


def parse_nrl(html: str) -> list[dict]:
    """NRL 実構造:
    raw order = [Pos, '', Pos#, Team, played, points, wins, drawn, lost, byes, for, against, diff, home, away, form, Next]
    """
    entries = re.findall(r'<tr[^>]*class="[^"]*ladder__row[^"]*"[^>]*>(.*?)</tr>', html, flags=re.S)
    out = []
    for e in entries:
        cells = re.findall(r'<(?:td|th)[^>]*>(.*?)</(?:td|th)>', e, flags=re.S)
        clean = [html_lib.unescape(re.sub(r'<[^>]+>', '', c)).strip() for c in cells]
        if len(clean) < 13:
            continue
        team = clean[3]
        if not team or team.lower() == "team":
            continue
        def _i(i):
            try:
                return int(clean[i])
            except (ValueError, IndexError):
                return None
        entry = {
            "team": team,
            "gp":   _i(4),
            "pts":  _i(5),
            "w":    _i(6),
            "d":    _i(7),
            "l":    _i(8),
            "byes": _i(9),
            "pf":   _i(10),
            "pa":   _i(11),
            "pd":   _i(12),
        }
        if isinstance(entry["pd"], int) and isinstance(entry["gp"], int) and entry["gp"]:
            entry["pd_per_game"] = round(entry["pd"] / entry["gp"], 2)
        out.append(entry)
    return out


def parse_superleague(html: str) -> list[dict]:
    """SuperLeague: table rows with team + stats"""
    tables = re.findall(r'<table[^>]*>(.*?)</table>', html, flags=re.S)
    for t in tables:
        rows = _parse_generic_table(t)
        if rows and any("for" in c.lower() or "pf" in c.lower() for c in rows[0]):
            return _normalize_standings(rows)
    return []


STRATEGIES = {
    "playwright_nrl": lambda url: (playwright_html(url, wait_selector=".ladder__row"), parse_nrl),
    "playwright_sl":  lambda url: (playwright_html(url), parse_superleague),
    "wikipedia_table": lambda url: (curl_html(url) or playwright_html(url), parse_wikipedia_table),
}


def process(league: str):
    conf = LEAGUES[league]
    url = conf["url"]
    strategy_name = conf["strategy"]
    print(f"[FETCH] {league}: {url} (strategy={strategy_name})")
    html, parser = STRATEGIES[strategy_name](url)
    if not html:
        raise RuntimeError("HTML empty")
    teams = parser(html)
    if not teams:
        raise RuntimeError("no teams parsed (site layout change?)")
    payload = {
        "league": league,
        "source": url,
        "strategy": strategy_name,
        "fetched_at": datetime.now(JST).isoformat(),
        "team_count": len(teams),
        "teams": teams,
    }
    today = datetime.now(JST).strftime("%Y-%m-%d")
    out = FEED_DIR / f"{league}_standings_{today}.json"
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[OK] saved {out} (teams={len(teams)})")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days-stale", type=int, default=3)
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--league", default="all",
                    choices=list(LEAGUES.keys()) + ["all"])
    args = ap.parse_args()

    leagues = list(LEAGUES.keys()) if args.league == "all" else [args.league]
    overall_fail = False
    for lg in leagues:
        latest = latest_feed(lg)
        if latest:
            age = age_days(latest)
            print(f"[INFO] {lg}: latest={latest.name} age={age:.1f}d")
            if args.check:
                if age > args.days_stale:
                    overall_fail = True
                continue
            if age <= args.days_stale and args.days_stale > 0:
                print(f"[SKIP] {lg} fresh.")
                continue
        elif args.check:
            overall_fail = True
            continue

        try:
            process(lg)
        except Exception as e:
            print(f"[ERR] {lg}: {e}")
            print(f"[GEN006] {lg}_standings fetch failed.")
            overall_fail = True
            # 続行して他リーグは試す

    sys.exit(2 if overall_fail else 0)


if __name__ == "__main__":
    main()
