# -*- coding: utf-8 -*-
"""
怪我 / 出場情報フィード
- NHL: Daily Faceoff starting goalies + injured players
- NBA: NBA.com injury report / Rotowire fallback
- Tennis: tennisabstract Tour drawsheet (currently-active withdrawals)

出力:
  stats/external_feeds/nhl_injuries_YYYY-MM-DD.json
  stats/external_feeds/nba_injuries_YYYY-MM-DD.json
  stats/external_feeds/tennis_withdrawals_YYYY-MM-DD.json
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
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0 Safari/537.36"


def _num(v):
    if v is None:
        return None
    s = str(v).strip()
    if s in ("", "-"):
        return None
    try:
        return float(s)
    except ValueError:
        return v


def age_days(p: Path) -> float:
    m = datetime.fromtimestamp(p.stat().st_mtime, tz=JST)
    return (datetime.now(JST) - m).total_seconds() / 86400


def latest_feed(kind: str) -> Path | None:
    files = sorted(FEED_DIR.glob(f"{kind}_*.json"))
    return files[-1] if files else None


def playwright_html(url: str, wait_selector: str | None = None) -> str:
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        b = pw.chromium.launch(headless=True, args=["--disable-blink-features=AutomationControlled"])
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


# ================ NHL ================

def fetch_nhl_goalies() -> list[dict]:
    html = playwright_html("https://www.dailyfaceoff.com/starting-goalies/")
    out = []
    # Daily Faceoff は各マッチアップを section で表示。team/goalie ペアを正規表現で抽出
    matches = re.findall(
        r'<div[^>]*class="[^"]*starting-goalies-card[^"]*"[^>]*>(.*?)</div>\s*</div>',
        html, flags=re.S
    )
    # フォールバック: 単純に team + goalie name を探す
    if not matches:
        # 最低限、ページ全文から goalie 名をテキスト抽出
        pairs = re.findall(
            r'<h4[^>]*class="[^"]*team[^"]*"[^>]*>(.*?)</h4>.*?<h4[^>]*class="[^"]*goalie[^"]*"[^>]*>(.*?)</h4>',
            html, flags=re.S
        )
        for team, goalie in pairs:
            out.append({
                "team": html_lib.unescape(re.sub(r'<[^>]+>', '', team)).strip(),
                "goalie": html_lib.unescape(re.sub(r'<[^>]+>', '', goalie)).strip(),
            })
    return out


def fetch_nhl_injuries() -> list[dict]:
    """ESPN NHL injuries (チームごとにテーブル)"""
    import subprocess, shutil
    html = ""
    if shutil.which("curl"):
        r = subprocess.run(
            ["curl", "-sL", "--compressed", "-A", UA, "--max-time", "30",
             "https://www.espn.com/nhl/injuries"],
            capture_output=True, text=True, encoding="utf-8", errors="replace"
        )
        html = r.stdout
    if not html:
        html = playwright_html("https://www.espn.com/nhl/injuries")

    # ESPN は 複数の small テーブル (NAME/POS/EST.RETURN/STATUS/COMMENT) で構成
    out = []
    # チーム見出しを追跡するため順序でパース
    team_ctx = None
    # チーム名はテーブル前の <span class="injuries__teamName"> か similar に含まれる
    parts = re.split(r'(<tr[^>]*>.*?</tr>)', html, flags=re.S)
    for part in parts:
        # team context 更新
        m = re.search(r'data-teamname[^=]*="([^"]+)"', part)
        if m:
            team_ctx = html_lib.unescape(m.group(1))
        # あるいは team logo alt
        m2 = re.search(r'<img[^>]*class="[^"]*Image[^"]*"[^>]*alt="([^"]+)"', part)
        if m2 and 'logo' not in (m2.group(1) or '').lower():
            team_ctx = html_lib.unescape(m2.group(1))

        if part.startswith("<tr"):
            cells = re.findall(r'<(?:td|th)[^>]*>(.*?)</(?:td|th)>', part, flags=re.S)
            clean = [html_lib.unescape(re.sub(r'<[^>]+>', '', c)).strip() for c in cells]
            if len(clean) >= 4 and clean[0] and clean[0].upper() != "NAME":
                out.append({
                    "player": clean[0],
                    "team": team_ctx,
                    "position": clean[1] if len(clean) > 1 else None,
                    "estimated_return": clean[2] if len(clean) > 2 else None,
                    "status": clean[3] if len(clean) > 3 else None,
                    "comment": clean[4] if len(clean) > 4 else None,
                })
    return out


def process_nhl():
    goalies = []
    injuries = []
    try:
        goalies = fetch_nhl_goalies()
        print(f"  NHL goalies (dailyfaceoff): {len(goalies)}")
    except Exception as e:
        print(f"  [WARN] goalies fetch failed: {e}")
    try:
        injuries = fetch_nhl_injuries()
        print(f"  NHL injuries (espn): {len(injuries)}")
    except Exception as e:
        print(f"  [WARN] injuries fetch failed: {e}")

    if not goalies and not injuries:
        raise RuntimeError("both goalies and injuries failed")

    payload = {
        "source_goalies": "https://www.dailyfaceoff.com/starting-goalies/ (often blocked, WebSearch fallback)",
        "source_injuries": "https://www.espn.com/nhl/injuries",
        "fetched_at": datetime.now(JST).isoformat(),
        "starting_goalies": goalies,
        "injuries": injuries,
    }
    today = datetime.now(JST).strftime("%Y-%m-%d")
    out = FEED_DIR / f"nhl_injuries_{today}.json"
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[OK] saved {out}")


# ================ NBA ================

def fetch_nba_injuries() -> list[dict]:
    """Rotowire の無料injury ページ (比較的アクセス可能)"""
    html = playwright_html("https://www.rotowire.com/basketball/injury-report.php")
    out = []
    # Rotowire は HTML table で表示
    tables = re.findall(r'<table[^>]*>(.*?)</table>', html, flags=re.S)
    for t in tables:
        rows = re.findall(r'<tr[^>]*>(.*?)</tr>', t, flags=re.S)
        for r in rows:
            cells = re.findall(r'<(?:td|th)[^>]*>(.*?)</(?:td|th)>', r, flags=re.S)
            clean = [html_lib.unescape(re.sub(r'<[^>]+>', '', c)).strip() for c in cells]
            if len(clean) >= 4 and clean[0] and not clean[0].lower().startswith("player"):
                out.append({
                    "player": clean[0],
                    "team": clean[1] if len(clean) > 1 else None,
                    "position": clean[2] if len(clean) > 2 else None,
                    "injury": clean[3] if len(clean) > 3 else None,
                    "status": clean[4] if len(clean) > 4 else None,
                    "estimated_return": clean[5] if len(clean) > 5 else None,
                })
    return out


def process_nba():
    injuries = fetch_nba_injuries()
    print(f"  NBA injuries: {len(injuries)}")
    if not injuries:
        raise RuntimeError("no rows parsed")
    payload = {
        "source": "https://www.rotowire.com/basketball/injury-report.php",
        "fetched_at": datetime.now(JST).isoformat(),
        "injuries": injuries,
    }
    today = datetime.now(JST).strftime("%Y-%m-%d")
    out = FEED_DIR / f"nba_injuries_{today}.json"
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[OK] saved {out}")


# ================ Tennis ================

def fetch_tennis_withdrawals() -> list[dict]:
    """ATP/WTA Live rankings 付近からの出場辞退情報はサイト依存。
    ここでは tennisabstract の atp_calendar をチェック (withdrawn 情報は少ない)
    より確実には、大会の draw ページを直接読むが、ここでは雛形のみ。"""
    # 現状、構造化された withdrawal フィードは存在しないため、運用は WebSearch ベース
    return []


def process_tennis():
    print("  Tennis withdrawals: 構造化フィード未存在のため WebSearch 併用運用継続 (placeholder only)")
    payload = {
        "source": "WebSearch-based (no structured feed available)",
        "fetched_at": datetime.now(JST).isoformat(),
        "note": "テニス選手の大会途中棄権は tennisabstract や ATP/WTA 公式でも構造化フィード提供なし。試合24h前に大会 Order of Play を WebSearch する運用を継続。",
        "withdrawals": [],
    }
    today = datetime.now(JST).strftime("%Y-%m-%d")
    out = FEED_DIR / f"tennis_withdrawals_{today}.json"
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[OK] saved {out} (placeholder)")


# ================ main ================

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days-stale", type=int, default=1)  # 怪我情報は毎日更新
    ap.add_argument("--sport", default="all", choices=["nhl", "nba", "tennis", "all"])
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    targets = {
        "nhl":    ("nhl_injuries",       process_nhl),
        "nba":    ("nba_injuries",       process_nba),
        "tennis": ("tennis_withdrawals", process_tennis),
    }
    sports = list(targets.keys()) if args.sport == "all" else [args.sport]

    overall_fail = False
    for s in sports:
        kind, proc = targets[s]
        latest = latest_feed(kind)
        if latest:
            age = age_days(latest)
            print(f"[INFO] {s}: {latest.name} age={age:.1f}d")
            if args.check:
                if age > args.days_stale:
                    overall_fail = True
                continue
            if age <= args.days_stale and args.days_stale > 0:
                print(f"[SKIP] {s} fresh.")
                continue
        elif args.check:
            overall_fail = True
            continue
        try:
            print(f"[FETCH] {s} injuries ...")
            proc()
        except Exception as e:
            print(f"[ERR] {s}: {e}")
            print(f"[GEN006] {kind} fetch failed.")
            overall_fail = True

    sys.exit(2 if overall_fail else 0)


if __name__ == "__main__":
    main()
