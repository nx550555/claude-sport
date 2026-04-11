"""
不足情報一括取得スクリプト
- NHL オッズ (OddsPortal)
- NHL xGF% (MoneyPuck)
- NHL ゴーリー確認 (DailyFaceoff)
- テニス cElo (tennisabstract)
"""
import asyncio, sys
from playwright.async_api import async_playwright

URLS = {
    "nhl_odds":    "https://www.oddsportal.com/hockey/usa/nhl/",
    "nhl_xgf":     "https://moneypuck.com/teams.htm",
    "nhl_goalies": "https://www.dailyfaceoff.com/starting-goalies/",
    "tennis_celo": "https://tennisabstract.com/reports/atp_elo_ratings.html",
}

async def fetch(page, key, url):
    print(f"\n→ [{key}] 取得中: {url}", file=sys.stderr)
    try:
        await page.goto(url, wait_until="domcontentloaded", timeout=30000)
    except Exception as e:
        print(f"  エラー: {e}", file=sys.stderr)
        try:
            await page.goto(url, wait_until="load", timeout=30000)
        except Exception as e2:
            print(f"  再試行失敗: {e2}", file=sys.stderr)
            return ""
    await page.wait_for_timeout(5000)
    text = await page.evaluate("() => document.body.innerText")
    out = f"{key}.txt"
    with open(out, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"  保存完了: {len(text)} 文字 → {out}", file=sys.stderr)
    return text

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=["--disable-gpu", "--no-sandbox", "--window-position=-10000,-10000"]
        )
        ctx = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await ctx.new_page()

        results = {}
        for key, url in URLS.items():
            results[key] = await fetch(page, key, url)

        await browser.close()
        print("\n全データ取得完了", file=sys.stderr)
        return results

asyncio.run(main())
print("完了 - nhl_odds.txt / nhl_xgf.txt / nhl_goalies.txt / tennis_celo.txt を確認してください")
