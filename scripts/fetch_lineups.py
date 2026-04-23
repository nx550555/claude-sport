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


def fetch_html(url: str, require_marker: str | None = None) -> str:
    """curl → Playwright fallback。Rotowire は通常 SSR で lineup__main を返すが
    試合が無い日は lineup カード自体が空になるため、require_marker (e.g. "lineup__main")
    で存在検証する。curl 成功でも marker が無ければ Playwright に fallback しない
    (存在しない = 試合なし)。"""
    if shutil.which("curl"):
        r = subprocess.run(
            ["curl", "-sL", "--compressed", "-A", UA, "--max-time", "30", url],
            capture_output=True, text=True, encoding="utf-8", errors="replace"
        )
        if r.returncode == 0 and r.stdout:
            if not require_marker or require_marker in r.stdout:
                return r.stdout
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        ctx = browser.new_context(user_agent=UA)
        page = ctx.new_page()
        page.goto(url, wait_until="domcontentloaded", timeout=60000)
        if require_marker:
            try:
                page.wait_for_function(
                    f"() => document.documentElement.innerHTML.includes({json.dumps(require_marker)})",
                    timeout=20000,
                )
            except Exception:
                pass
        content = page.content()
        browser.close()
    return content


def _clean(s: str) -> str:
    return html_lib.unescape(re.sub(r'<[^>]+>', '', s)).replace('\xa0', ' ').strip()


def _game_blocks(html: str, sport: str) -> list[str]:
    """1ページ内の試合カード (<div class="lineup is-{sport}" ...>) 配列を返す。
    開始位置から次の同クラスまで or footer までをブロックとして切る。"""
    starts = [m.start() for m in re.finditer(
        rf'<div [^>]*class="lineup is-{sport}(?:[^"]*)"', html
    )]
    if not starts:
        return []
    # 終了境界候補
    end_pat = re.compile(
        rf'<div [^>]*class="lineup is-{sport}(?:[^"]*)"|<footer|</main'
    )
    blocks = []
    for i, s in enumerate(starts):
        # 次の start 以降で終了 marker を探す
        tail_from = starts[i + 1] if i + 1 < len(starts) else len(html)
        blocks.append(html[s:tail_from])
    return blocks


def _parse_team_meta(block: str) -> dict:
    """試合ブロックから home/visit の略称・正式名を抽出。
    MLB/Soccer は <div class="lineup__mteam ...">、NBA は <a class="lineup__mteam ...">"""
    abbrs = re.findall(r'<div class="lineup__abbr">([^<]+)</div>', block)
    mteams_raw = re.findall(
        r'<(?:a|div)[^>]*class="lineup__mteam[^"]*"[^>]*>(.*?)</(?:a|div)>',
        block, flags=re.S,
    )
    mteams = [re.sub(r'<span[^>]*>.*?</span>', '', m, flags=re.S) for m in mteams_raw]
    mteams = [_clean(m) for m in mteams]
    out: dict = {}
    if len(abbrs) >= 2 and len(mteams) >= 2:
        out["visit"] = {"abbr": abbrs[0].strip(), "name": mteams[0]}
        out["home"] = {"abbr": abbrs[1].strip(), "name": mteams[1]}
    return out


def _parse_player_list(block: str, side: str, sport: str) -> dict:
    """side = 'visit' | 'home'. スタメンを dict で返す"""
    ul_m = re.search(rf'<ul class="lineup__list is-{side}">(.*?)</ul>', block, flags=re.S)
    if not ul_m:
        return {"starters": [], "status": None}
    inner = ul_m.group(1)
    # status ("Expected Lineup" / "Confirmed" 等)
    status_m = re.search(r'<li class="lineup__status[^"]*">(.*?)</li>', inner, flags=re.S)
    status = _clean(status_m.group(1)) if status_m else None

    # highlight player (MLB: 先発投手 / NBA: 無し) — MLB のみ意味あり
    highlight_m = re.search(
        r'<li class="lineup__player-highlight[^"]*">.*?<a[^>]*>(.*?)</a>',
        inner, flags=re.S,
    )
    highlight = _clean(highlight_m.group(1)) if highlight_m else None

    # 通常プレイヤー (pos + name + bats/throws)
    # - li class: "lineup__player" または "lineup__player is-pct-play-100" 等
    # - pos div: class 末尾にスペース・style 等追加属性があり得る
    players = []
    for m in re.finditer(
        r'<li class="lineup__player[^"]*"[^>]*>\s*'
        r'(?:<div class="lineup__pos[^"]*"[^>]*>([^<]*)</div>)?\s*'
        r'<a(?:\s+title="([^"]*)")?[^>]*>([^<]+)</a>'
        r'(?:\s*<span class="lineup__(?:bats|throws)"[^>]*>([^<]*)</span>)?',
        inner, flags=re.S,
    ):
        pos = (m.group(1) or "").strip()
        title_name = (m.group(2) or "").strip()
        display_name = _clean(m.group(3) or "")
        hand = (m.group(4) or "").strip()
        players.append({
            "pos": pos,
            "name": title_name or display_name,
            "display_name": display_name,
            "hand": hand,
        })

    result: dict = {
        "status": status,
        "starters": players[:11 if sport == "soccer" else 9],
    }
    if sport == "mlb" and highlight:
        result["starting_pitcher"] = highlight
    return result


def parse_rotowire(html: str, sport: str) -> dict:
    """汎用: sport (nba/nfl/mlb/soccer) の試合カードを全部パースし
    { team_name: { ...side data } } で返す"""
    out: dict[str, dict] = {}
    blocks = _game_blocks(html, sport)
    for block in blocks:
        meta = _parse_team_meta(block)
        if not meta:
            continue
        for side in ("visit", "home"):
            if side not in meta:
                continue
            team_name = meta[side]["name"] or meta[side]["abbr"]
            data = _parse_player_list(block, side, sport)
            data["abbr"] = meta[side]["abbr"]
            data["side"] = side
            data["opponent"] = meta["home" if side == "visit" else "visit"]["name"]
            if sport == "soccer":
                # rotowire soccer では formation を明示する class が見当たらない (現状)
                data["gk"] = data["starters"][0]["name"] if data.get("starters") else None
            out[team_name] = data
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
    # rotowire の該当スポーツ試合カード marker
    html = fetch_html(url, require_marker=f'lineup is-{sport}')
    return parse_rotowire(html, sport)


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
