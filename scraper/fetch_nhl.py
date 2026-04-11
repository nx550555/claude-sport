"""Fetch tonight's NHL games from matchstat and NHL schedule"""
import asyncio, sys
from playwright.async_api import async_playwright

async def fetch(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        ctx = await browser.new_context(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        page = await ctx.new_page()
        try:
            await page.goto(url, wait_until='domcontentloaded', timeout=25000)
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
        await page.wait_for_timeout(3000)
        text = await page.evaluate("() => document.body.innerText")
        await browser.close()
        return text

async def main():
    # Try NHL.com schedule
    url = "https://www.nhl.com/schedule/2026-04-10"
    text = await fetch(url)
    with open('nhl_schedule.txt', 'w', encoding='utf-8') as f:
        f.write(text)

    # Clean and print relevant section
    import re
    # find today's games
    lines = text.split('\n')
    for i, line in enumerate(lines):
        if any(x in line for x in ['April 10', 'Apr 10', 'Tonight', 'Game', 'vs', ' at ']):
            print(lines[max(0,i-1):i+3])

    print("\n--- First 3000 chars ---")
    clean = text[:3000]
    for c in ['\u2022','\u25c0','\u25b6','\u203a','\u2022','\xa9']:
        clean = clean.replace(c, '*')
    print(clean)

asyncio.run(main())
