"""NRL 2026 ラダー（順位表）取得"""
import asyncio, sys
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=["--disable-gpu", "--no-sandbox", "--window-position=-10000,-10000"])
        ctx = await browser.new_context(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        page = await ctx.new_page()

        # NRL公式ラダー取得
        print("NRL公式サイトに接続中...", file=sys.stderr)
        try:
            await page.goto("https://www.nrl.com/ladder/", wait_until="domcontentloaded", timeout=20000)
        except Exception as e:
            print(f"nrl.com エラー: {e}", file=sys.stderr)

        await page.wait_for_timeout(4000)
        text = await page.evaluate("() => document.body.innerText")
        with open("nrl_ladder.txt", "w", encoding="utf-8") as f:
            f.write(text)
        print(f"nrl.com 保存完了: {len(text)} 文字", file=sys.stderr)

        # zerotackle取得
        print("zerotackle.com に接続中...", file=sys.stderr)
        try:
            await page.goto("https://www.zerotackle.com/nrl/nrl-ladder/", wait_until="domcontentloaded", timeout=20000)
        except Exception as e:
            print(f"zerotackle エラー: {e}", file=sys.stderr)

        await page.wait_for_timeout(3000)
        text2 = await page.evaluate("() => document.body.innerText")
        with open("nrl_ladder2.txt", "w", encoding="utf-8") as f:
            f.write(text2)
        print(f"zerotackle 保存完了: {len(text2)} 文字", file=sys.stderr)

        await browser.close()

asyncio.run(main())
print("完了 - nrl_ladder.txt と nrl_ladder2.txt を確認してください")
