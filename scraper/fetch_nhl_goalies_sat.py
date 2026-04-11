"""
4月11日(土) NHL ゴーリー確認 + OTT/NYI ラインアップ調査
"""
import asyncio, sys
from playwright.async_api import async_playwright

URLS = {
    "goalies_sat": "https://www.dailyfaceoff.com/starting-goalies/",
    "ott_injuries": "https://www.dailyfaceoff.com/teams/ottawa-senators/game-lines/",
    "nyi_injuries": "https://www.dailyfaceoff.com/teams/new-york-islanders/game-lines/",
    "col_injuries": "https://www.dailyfaceoff.com/teams/colorado-avalanche/game-lines/",
    "vgk_injuries": "https://www.dailyfaceoff.com/teams/vegas-golden-knights/game-lines/",
}

async def fetch(page, key, url):
    print(f"\n→ [{key}] 取得中...", file=sys.stderr)
    try:
        await page.goto(url, wait_until="domcontentloaded", timeout=30000)
    except Exception as e:
        print(f"  エラー: {e}", file=sys.stderr)
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

        for key, url in URLS.items():
            await fetch(page, key, url)

        await browser.close()
        print("\n全データ取得完了", file=sys.stderr)

asyncio.run(main())
print("完了")
