# -*- coding: utf-8 -*-
"""
understat.com xG Fetcher (Soccer 5 big leagues)

understat.com は公式 API 無し。各リーグのチームページ HTML に埋め込まれた
JSON (teamsData / datesData / playersData) を JavaScript 変数として
展開している。正規表現で JS 変数を抜き出してデコードする方式。

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


def fetch_html(url: str) -> str:
    """understat.com は Cloudflare で bot 防御している。curl で返る HTML には
    JS データ (teamsData) が埋め込まれていない場合が多い。返り値に teamsData が
    含まれていることを curl 成功の条件にする。含まれなければ Playwright にフォールバック。"""
    if shutil.which("curl"):
        r = subprocess.run(
            ["curl", "-sL", "--compressed", "-A", UA, "--max-time", "30", url],
            capture_output=True, text=True, encoding="utf-8", errors="replace"
        )
        if r.returncode == 0 and r.stdout and "teamsData" in r.stdout:
            return r.stdout
    # Playwright fallback (Cloudflare challenge を解ける可能性あり)
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        ctx = browser.new_context(user_agent=UA)
        page = ctx.new_page()
        page.goto(url, wait_until="domcontentloaded", timeout=60000)
        # teamsData が script tag に埋め込まれるまで短時間待機
        try:
            page.wait_for_function("() => document.documentElement.innerHTML.includes('teamsData')", timeout=20000)
        except Exception:
            pass
        content = page.content()
        browser.close()
    return content


def _decode_js_escaped(s: str) -> str:
    """understat は JSON.parse('\x7b...') 形式。\\x?? を実バイトに戻す"""
    return re.sub(r"\\x([0-9a-fA-F]{2})", lambda m: chr(int(m.group(1), 16)), s)


def extract_var(html: str, var_name: str) -> dict | list | None:
    """var teamsData = JSON.parse('\\x7b ... \\x7d'); を抜き出して dict/list にする"""
    pat = re.compile(
        r"var\s+" + re.escape(var_name) + r"\s*=\s*JSON\.parse\s*\(\s*['\"](.+?)['\"]\s*\)\s*;",
        flags=re.S,
    )
    m = pat.search(html)
    if not m:
        return None
    raw = _decode_js_escaped(m.group(1))
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return None


def parse_league(html: str) -> dict:
    teams_data = extract_var(html, "teamsData") or {}
    teams_out = []
    for tid, tinfo in teams_data.items():
        title = tinfo.get("title")
        history = tinfo.get("history") or []
        if not history:
            continue
        # 累計を集計
        gp = len(history)
        xG = sum(float(h.get("xG", 0) or 0) for h in history)
        xGA = sum(float(h.get("xGA", 0) or 0) for h in history)
        npxG = sum(float(h.get("npxG", 0) or 0) for h in history)
        npxGA = sum(float(h.get("npxGA", 0) or 0) for h in history)
        pts = sum(int(h.get("pts", 0) or 0) for h in history)
        scored = sum(int(h.get("scored", 0) or 0) for h in history)
        missed = sum(int(h.get("missed", 0) or 0) for h in history)
        ppda_sum = sum(
            (float(h.get("ppda", {}).get("att", 0) or 0)) /
            max(float(h.get("ppda", {}).get("def", 0) or 1), 1)
            for h in history
        )
        teams_out.append({
            "team_id": tid,
            "team": title,
            "games_played": gp,
            "xG": round(xG, 2),
            "xGA": round(xGA, 2),
            "npxG": round(npxG, 2),
            "npxGA": round(npxGA, 2),
            "xG_per_game": round(xG / gp, 3) if gp else None,
            "xGA_per_game": round(xGA / gp, 3) if gp else None,
            "xGD": round(xG - xGA, 2),
            "xGD_per_game": round((xG - xGA) / gp, 3) if gp else None,
            "points": pts,
            "scored": scored,
            "missed": missed,
            "ppda_avg": round(ppda_sum / gp, 3) if gp else None,
        })
    teams_out.sort(key=lambda x: x.get("xGD", 0), reverse=True)
    return {
        "teams": teams_out,
        "team_count": len(teams_out),
    }


def process(league: str, season: str) -> dict:
    url = LEAGUE_URLS[league].format(season=season)
    print(f"[FETCH] {league} {season}: {url}")
    html = fetch_html(url)
    parsed = parse_league(html)
    return {
        "source": url,
        "league_key": league,
        "league_display": LEAGUE_DISPLAY[league],
        "season": f"{season}-{int(season)+1}",
        **parsed,
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
            print(f"[SKIP] age <= {args.days_stale}d, skipping fetch.")
            sys.exit(0)
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
            payload["leagues"][LEAGUE_DISPLAY[lg]] = process(lg, args.season)
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


if __name__ == "__main__":
    main()
