"""
matchstat.com フルスクレイパー + パーサー
本日のシングルス試合（オッズ付き）を全件取得
"""

import asyncio
import json
import re
import sys
from playwright.async_api import async_playwright

URLS = {
    "all_picks": "https://matchstat.com/predictions-tips/tennis/all-picks-today/",
    "wta_picks": "https://matchstat.com/predictions-tips/tennis/wta-1x2-predictions-today/",
    "atp_picks": "https://matchstat.com/predictions-tips/tennis/atp-1x2-predictions-today/",
}

async def fetch_page(page, url):
    print(f"\n→ 取得中: {url}", file=sys.stderr)
    try:
        await page.goto(url, wait_until="networkidle", timeout=30000)
    except Exception:
        try:
            await page.goto(url, wait_until="domcontentloaded", timeout=30000)
        except Exception as e:
            print(f"  エラー: {e}", file=sys.stderr)
            return ""
    await page.wait_for_timeout(2000)
    return await page.evaluate("() => document.body.innerText")

def parse_matches_from_text(text, source_label=""):
    """
    Parse match blocks from matchstat text content.
    Pattern:
      DATE TIME
      • TOURNAMENT
      • ROUND
      PLAYER1
      PLAYER2
        PROB1%  PROB2%    ODDS1  ODDS2
    """
    matches = []

    # Split by match blocks - each match has a time pattern
    # Look for blocks like "10 Apr at HH:MM PM"
    block_pattern = re.compile(
        r'(\d{1,2} \w+ at \d{1,2}:\d{2} (?:AM|PM))'
        r'(.*?)'
        r'(?=\d{1,2} \w+ at \d{1,2}:\d{2} (?:AM|PM)|$)',
        re.DOTALL
    )

    for m in block_pattern.finditer(text):
        time_str = m.group(1).strip()
        block = m.group(2).strip()

        # Extract tournament and round
        tournament = ""
        round_name = ""
        bullet_lines = re.findall(r'•\s*(.+)', block)
        if len(bullet_lines) >= 1:
            tournament = bullet_lines[0].strip()
        if len(bullet_lines) >= 2:
            round_name = bullet_lines[1].strip()

        # Remove bullet lines from block
        clean = re.sub(r'•.*\n?', '', block).strip()

        # Extract probabilities and odds
        prob_pattern = re.compile(r'(\d+\.?\d*)%\s*(\d+\.?\d*)%')
        odds_pattern = re.compile(r'(\d+\.\d{2})\s+(\d+\.\d{2})')

        probs = prob_pattern.search(clean)
        odds = odds_pattern.search(clean)

        if not probs or not odds:
            continue  # Skip if no odds data

        # Extract player names - lines before the numbers
        lines = [l.strip() for l in clean.split('\n') if l.strip()]
        player_lines = []
        for line in lines:
            # Skip lines with numbers, bullets, "PLAYERS", "BOOKIE", etc.
            if re.search(r'\d', line):
                break
            if line in ('PLAYERS', 'BOOKIE', 'PROBABILITY', 'ODDS', 'Above is implied from odds.', ''):
                continue
            if 'Login' in line or 'Register' in line or 'Unlock' in line:
                continue
            player_lines.append(line)

        if len(player_lines) < 2:
            # Try different approach - look for name patterns
            name_pattern = re.compile(r'^([A-Z][a-z]+\.?\s+[A-Z][a-zA-Z\s\-]+)$', re.MULTILINE)
            names = name_pattern.findall(clean)
            player_lines = names[:2]

        player1 = player_lines[0] if len(player_lines) > 0 else "P1"
        player2 = player_lines[1] if len(player_lines) > 1 else "P2"

        # Determine tour
        tour = "WTA" if any(wta in tournament for wta in [
            "WTA", "Upper Austria", "Linz", "Billie Jean King", "Ladies"
        ]) else "ATP"

        # Skip doubles (look for "/" in player names or "Doubles" in round)
        if "Doubles" in round_name or "/" in player1 or "/" in player2:
            continue

        match_data = {
            "time": time_str,
            "tournament": tournament,
            "round": round_name,
            "tour": tour,
            "player1": player1,
            "player2": player2,
            "prob1": float(probs.group(1)),
            "prob2": float(probs.group(2)),
            "odds1": float(odds.group(1)),
            "odds2": float(odds.group(2)),
            "source": source_label,
        }
        matches.append(match_data)
        print(f"  ✓ {time_str} | {tournament} {round_name} | {player1} vs {player2} | Odds: {odds.group(1)} / {odds.group(2)}", file=sys.stderr)

    return matches

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=["--disable-gpu", "--no-sandbox", "--window-position=-10000,-10000"])
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await context.new_page()

        all_matches = []

        # Fetch all picks page (ATP + WTA combined)
        text = await fetch_page(page, URLS["all_picks"])
        if text:
            with open("matchstat_all_text.txt", "w", encoding="utf-8") as f:
                f.write(text)
            matches = parse_matches_from_text(text, "all_picks")
            all_matches.extend(matches)

        # Deduplicate by (player1, player2, time)
        seen = set()
        unique_matches = []
        for m in all_matches:
            key = (m["player1"], m["player2"], m["time"])
            if key not in seen:
                seen.add(key)
                unique_matches.append(m)

        await browser.close()

        # Sort by time
        unique_matches.sort(key=lambda x: x["time"])

        print(f"\n=== シングルス試合数（重複除去後）: {len(unique_matches)}件 ===", file=sys.stderr)

        # Output JSON
        result = {
            "date": "2026-04-10",
            "total": len(unique_matches),
            "matches": unique_matches
        }

        # Write to file
        with open("matchstat_matches.json", "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        print("結果を matchstat_matches.json に保存しました", file=sys.stderr)
        return result

if __name__ == "__main__":
    result = asyncio.run(main())
    # Print summary to stdout
    for m in result["matches"]:
        ev1 = round((m["prob1"]/100) * m["odds1"] - 1, 3)
        ev2 = round((m["prob2"]/100) * m["odds2"] - 1, 3)
        print(f"[{m['tour']}] {m['tournament']} {m['round']} | {m['time']}")
        print(f"  {m['player1']:30s} {m['prob1']:5.1f}% @ {m['odds1']:.2f}  EV={ev1:+.1%}")
        print(f"  {m['player2']:30s} {m['prob2']:5.1f}% @ {m['odds2']:.2f}  EV={ev2:+.1%}")
        print()
