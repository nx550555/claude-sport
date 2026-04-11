"""
4月11日(土) NHLゴーリー + 負傷情報取得
- dailyfaceoffの土曜タブをクリック
- rotowire NHL injury report
"""
import asyncio, sys
from playwright.async_api import async_playwright

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

        # 1) dailyfaceoff 土曜タブをクリックして取得
        print("→ dailyfaceoff 土曜ゴーリー取得中...", file=sys.stderr)
        try:
            await page.goto("https://www.dailyfaceoff.com/starting-goalies/", wait_until="domcontentloaded", timeout=30000)
            await page.wait_for_timeout(3000)
            # 土曜タブを探してクリック
            sat_tab = await page.query_selector("text=SATURDAY, APRIL 11")
            if sat_tab:
                await sat_tab.click()
                print("  土曜タブをクリックしました", file=sys.stderr)
                await page.wait_for_timeout(4000)
            else:
                # 別の方法で探す
                tabs = await page.query_selector_all("button, [role='tab'], .tab, a")
                for tab in tabs:
                    txt = await tab.inner_text()
                    if "SAT" in txt.upper() or "APR 11" in txt or "11" in txt:
                        print(f"  タブ発見: {txt.strip()}", file=sys.stderr)
                        await tab.click()
                        await page.wait_for_timeout(3000)
                        break
        except Exception as e:
            print(f"  エラー: {e}", file=sys.stderr)

        text_goalies = await page.evaluate("() => document.body.innerText")
        with open("goalies_saturday.txt", "w", encoding="utf-8") as f:
            f.write(text_goalies)
        print(f"  保存: {len(text_goalies)} 文字 → goalies_saturday.txt", file=sys.stderr)

        # 2) rotowire NHL injury report
        print("\n→ Rotowire NHL負傷情報取得中...", file=sys.stderr)
        try:
            await page.goto("https://www.rotowire.com/hockey/injury-report.php", wait_until="domcontentloaded", timeout=30000)
            await page.wait_for_timeout(4000)
        except Exception as e:
            print(f"  エラー: {e}", file=sys.stderr)
        text_injury = await page.evaluate("() => document.body.innerText")
        with open("nhl_injuries.txt", "w", encoding="utf-8") as f:
            f.write(text_injury)
        print(f"  保存: {len(text_injury)} 文字 → nhl_injuries.txt", file=sys.stderr)

        # 3) NHL.com 最新ニュース（OTT/NYI 関連情報）
        print("\n→ NHL公式ニュース取得中...", file=sys.stderr)
        try:
            await page.goto("https://www.nhl.com/news", wait_until="domcontentloaded", timeout=30000)
            await page.wait_for_timeout(4000)
        except Exception as e:
            print(f"  エラー: {e}", file=sys.stderr)
        text_news = await page.evaluate("() => document.body.innerText")
        with open("nhl_news.txt", "w", encoding="utf-8") as f:
            f.write(text_news)
        print(f"  保存: {len(text_news)} 文字 → nhl_news.txt", file=sys.stderr)

        await browser.close()
        print("\n完了", file=sys.stderr)

asyncio.run(main())
print("完了 - goalies_saturday.txt / nhl_injuries.txt / nhl_news.txt を確認")
