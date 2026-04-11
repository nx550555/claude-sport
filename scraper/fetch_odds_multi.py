"""
UFL + NRL オッズ取得スクレイパー
oddsportal.com から両リーグのオッズを取得
"""
import asyncio, sys, re
from playwright.async_api import async_playwright

URLS = {
    "ufl":  "https://www.oddsportal.com/american-football/usa/ufl/",
    "nrl":  "https://www.oddsportal.com/rugby-league/australia/nrl/",
}

async def fetch_text(page, url, label):
    print(f"\n→ {label} 取得中: {url}", file=sys.stderr)
    try:
        await page.goto(url, wait_until="domcontentloaded", timeout=25000)
    except Exception as e:
        print(f"  タイムアウト/エラー: {e}", file=sys.stderr)
    await page.wait_for_timeout(4000)
    text = await page.evaluate("() => document.body.innerText")
    fname = f"odds_{label}.txt"
    with open(fname, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"  保存完了: {len(text)} 文字 → {fname}", file=sys.stderr)
    return text

def extract_matches(text, sport):
    """oddsportalのテキストからマッチを抽出"""
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    matches = []
    i = 0
    while i < len(lines):
        line = lines[i]
        # oddsportalはチーム名が連続して、オッズが続く形式
        # パターン: "TeamA - TeamB" または "TeamA\nTeamB"
        # オッズ: 数字（1.xx〜5.xx）が続く
        if re.match(r'\d{1,2}:\d{2}', line) or re.match(r'\d{4}-\d{2}-\d{2}', line):
            # 時刻行の後にチーム情報
            if i+1 < len(lines):
                match_line = lines[i+1]
                if ' - ' in match_line or ' vs ' in match_line.lower():
                    parts = re.split(r' - | vs ', match_line, flags=re.IGNORECASE)
                    if len(parts) == 2:
                        team1, team2 = parts[0].strip(), parts[1].strip()
                        # 次の数値行を探す
                        odds = []
                        for j in range(i+2, min(i+8, len(lines))):
                            nums = re.findall(r'\d+\.\d{2}', lines[j])
                            odds.extend(nums)
                            if len(odds) >= 2:
                                break
                        if len(odds) >= 2:
                            matches.append({
                                "time": line,
                                "team1": team1,
                                "team2": team2,
                                "odds1": float(odds[0]),
                                "odds2": float(odds[1]),
                                "sport": sport
                            })
                            print(f"  ✓ 検出: {line} | {team1} vs {team2} | オッズ {odds[0]} / {odds[1]}", file=sys.stderr)
        i += 1
    return matches

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=["--disable-gpu", "--no-sandbox", "--window-position=-10000,-10000"])
        ctx = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await ctx.new_page()

        all_matches = {}
        for sport, url in URLS.items():
            text = await fetch_text(page, url, sport)
            matches = extract_matches(text, sport)
            all_matches[sport] = matches
            print(f"\n  {sport.upper()}: {len(matches)} 試合取得完了", file=sys.stderr)

            # テキストの最初の3000文字を表示（デバッグ用）
            clean = text[:3000]
            for c in ['\u2022','\xa9','\u25b6','\u25c0','\u2713','\u203a']:
                clean = clean.replace(c, '*')
            with open(f"odds_{sport}_preview.txt", "w", encoding="utf-8") as f:
                f.write(clean)

        await browser.close()
        return all_matches

result = asyncio.run(main())
for sport, matches in result.items():
    print(f"\n=== {sport.upper()} ===")
    for m in matches:
        print(f"  {m['time']} | {m['team1']} vs {m['team2']} | {m['odds1']} / {m['odds2']}")
