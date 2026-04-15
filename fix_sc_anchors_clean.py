#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SC アンカーを正しく挿入する (誤挿入をリセットして再挿入)
"""

path = r"C:\Users\ohwada\Desktop\claude_sport\dashboard.html"
with open(path, encoding='utf-8') as f:
    content = f.read()

# まず全ての誤挿入アンカーを削除
import re
content = re.sub(r'\s*<!-- (?:SC|/SC):[A-Z]+ -->\n?', '\n', content)
content = re.sub(r'\n{3,}', '\n\n', content)
print("既存アンカー全削除完了")

# sport-card ヘッダー色とキーのマッピング (色が一意な場合)
# UFL と NBA は同じ fca5a5 なので sport名で区別
CARDS = [
    ('color:#79c0ff;',  'ATP'),
    ('color:#f9a8d4;',  'WTA'),
    ('color:#a5f3fc;',  'NHL'),
    # UFL: fca5a5 + "UFL"
    # NBA: fca5a5 + "NBA"
    ('color:#86efac;',  'NRL'),
    ('color:#c4b5fd;',  'SRP'),
    ('color:#bfdbfe;',  'SL'),
]

# 一意な色でアンカーを挿入
for color, key in CARDS:
    pattern = r'(<div class="sport-card">)\s*\n\s*(<div class="sport-card-header" style="' + re.escape(color) + r'")'
    def make_repl(k):
        def repl(m):
            return f'\n      <!-- SC:{k} -->\n      {m.group(1)}\n        {m.group(2)}'
        return repl
    new_content, n = re.subn(pattern, make_repl(key), content)
    if n == 1:
        content = new_content
        print(f"OK: SC:{key} inserted (color={color})")
    else:
        print(f"MISS: SC:{key} (n={n})")

# UFL と NBA を sport 名で区別 (同じ色 fca5a5)
for sport_name, key in [('UFL', 'UFL'), ('NBA', 'NBA')]:
    pattern = (
        r'(<div class="sport-card">)\s*\n\s*'
        r'(<div class="sport-card-header" style="color:#fca5a5;">'
        r'[^\n]*' + re.escape(sport_name)
    )
    def make_repl2(k):
        def repl(m):
            return f'\n      <!-- SC:{k} -->\n      {m.group(1)}\n        {m.group(2)}'
        return repl
    new_content, n = re.subn(pattern, make_repl2(key), content)
    if n == 1:
        content = new_content
        print(f"OK: SC:{key} inserted (name={sport_name})")
    else:
        print(f"MISS: SC:{key} by name (n={n})")

# 終了アンカーを挿入: 各 SC:KEY の後の </div></div> の直後に /SC:KEY を追加
for color, key in CARDS + [('color:#fca5a5;', 'UFL'), ('color:#fca5a5;', 'NBA')]:
    start_tag = f'<!-- SC:{key} -->'
    end_tag   = f'<!-- /SC:{key} -->'
    if end_tag in content:
        print(f"SKIP end (exists): /SC:{key}")
        continue
    if start_tag not in content:
        print(f"SKIP end (no start): /SC:{key}")
        continue
    idx = content.index(start_tag)
    # start_tag から次の SC: or preseason-card を探す
    after = content[idx:]
    next_sc = re.search(r'<!-- SC:|<div class="preseason-card">', after[len(start_tag):])
    if not next_sc:
        print(f"MISS end: /SC:{key} (no next card)")
        continue
    end_region = after[len(start_tag):len(start_tag) + next_sc.start()]
    # end_region の中の最後の </div>\n      </div> を探す
    last = list(re.finditer(r'</div>\n      </div>', end_region))
    if not last:
        print(f"MISS end: /SC:{key} (no closing div)")
        continue
    insert_at = idx + len(start_tag) + last[-1].end()
    content = content[:insert_at] + f'\n      {end_tag}' + content[insert_at:]
    print(f"OK: /SC:{key} inserted")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("\ndashboard.html saved.")

# 確認
with open(path, encoding='utf-8') as f:
    c2 = f.read()
for _, key in CARDS + [('', 'UFL'), ('', 'NBA')]:
    start = f'<!-- SC:{key} -->' in c2
    end   = f'<!-- /SC:{key} -->' in c2
    print(f"  SC:{key}: start={start}, end={end}")
