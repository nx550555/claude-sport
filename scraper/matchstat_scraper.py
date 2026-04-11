"""
matchstat.com スクレイパー (Playwright + Chromium)
使用方法: python matchstat_scraper.py
"""

import asyncio
import json
import sys
from playwright.async_api import async_playwright

TARGET_URL = "https://matchstat.com/predictions-tips/tennis/all-picks-today/"

async def scrape_matchstat():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=["--disable-gpu", "--no-sandbox", "--window-position=-10000,-10000"])
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await context.new_page()

        print(f"接続中: {TARGET_URL}", file=sys.stderr)

        try:
            await page.goto(TARGET_URL, wait_until="networkidle", timeout=30000)
        except Exception as e:
            print(f"タイムアウト/エラー: {e}", file=sys.stderr)
            # domcontentloadedで再試行
            await page.goto(TARGET_URL, wait_until="domcontentloaded", timeout=30000)

        # Wait for match data to appear
        await page.wait_for_timeout(3000)

        # ページタイトル確認
        title = await page.title()
        print(f"ページタイトル: {title}", file=sys.stderr)

        # HTML取得・保存
        content = await page.content()

        with open("matchstat_raw.html", "w", encoding="utf-8") as f:
            f.write(content)

        print(f"HTML保存完了 ({len(content)} 文字)", file=sys.stderr)

        # Try to extract match data
        # Look for common match containers
        matches = []

        # 各セレクタを試行
        selectors_to_try = [
            ".match-row",
            ".match",
            ".prediction-row",
            "tr[data-match]",
            ".picks-table tr",
            ".match-item",
            "[class*='match']",
            "table tbody tr",
        ]

        for selector in selectors_to_try:
            elements = await page.query_selector_all(selector)
            if elements:
                print(f"  セレクタ '{selector}' で {len(elements)} 要素を検出", file=sys.stderr)

        # テキスト全文取得・保存
        body_text = await page.evaluate("() => document.body.innerText")

        with open("matchstat_text.txt", "w", encoding="utf-8") as f:
            f.write(body_text)

        print(f"テキスト保存完了 ({len(body_text)} 文字)", file=sys.stderr)
        print("\n--- テキスト先頭3000文字 ---", file=sys.stderr)
        print(body_text[:3000], file=sys.stderr)

        await browser.close()

        return {"title": title, "content_length": len(content), "text_preview": body_text[:2000]}

if __name__ == "__main__":
    result = asyncio.run(scrape_matchstat())
    print(json.dumps(result, ensure_ascii=False, indent=2))
