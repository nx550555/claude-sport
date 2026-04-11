import asyncio
import sys
from playwright.async_api import async_playwright

async def fetch_wta():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        ctx = await browser.new_context(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        page = await ctx.new_page()
        try:
            await page.goto('https://matchstat.com/predictions-tips/tennis/wta-1x2-predictions-today/', wait_until='domcontentloaded', timeout=25000)
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
        await page.wait_for_timeout(3000)
        text = await page.evaluate("() => document.body.innerText")
        await browser.close()
        return text

text = asyncio.run(fetch_wta())
with open('wta_text.txt', 'w', encoding='utf-8') as f:
    f.write(text)

import re
idx = text.find('Apr')
if idx < 0:
    idx = 0
chunk = text[idx:idx+4000]
# clean special chars
for char in ['\u2022','\u25c0','\u25b6','\u203a','\u2713','\u2714','\u2192','\u25ba']:
    chunk = chunk.replace(char, '*')
with open('wta_chunk.txt', 'w', encoding='utf-8') as f:
    f.write(chunk)
print("Done - check wta_chunk.txt and wta_text.txt")
