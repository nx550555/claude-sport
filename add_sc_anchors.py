#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""dashboard.html の各 sport-card に SC:xxx アンカーコメントを挿入する（初回のみ実行）"""

path = r"C:\Users\ohwada\Desktop\claude_sport\dashboard.html"
with open(path, encoding='utf-8') as f:
    content = f.read()

# 各 sport card の固有ヘッダー文字列と対応するキー
# (old_header, sc_key)
anchors = [
    # sport-card の開始 div の直前に <!-- SC:KEY --> を挿入
    # 各カードは <div class="sport-card">\n        <div class="sport-card-header" ... HEADER で一意に識別
    ('sport-card">\n        <div class="sport-card-header" style="color:#79c0ff;">', 'ATP'),
    ('sport-card">\n        <div class="sport-card-header" style="color:#f9a8d4;">', 'WTA'),
    ('sport-card">\n        <div class="sport-card-header" style="color:#a5f3fc;">', 'NHL'),
    ('sport-card">\n        <div class="sport-card-header" style="color:#fca5a5;">\U0001f3c8 UFL', 'UFL'),
    ('sport-card">\n        <div class="sport-card-header" style="color:#86efac;">', 'NRL'),
    ('sport-card">\n        <div class="sport-card-header" style="color:#c4b5fd;">', 'SRP'),
    ('sport-card">\n        <div class="sport-card-header" style="color:#fca5a5;">\U0001f3c0 NBA', 'NBA'),
    ('sport-card">\n        <div class="sport-card-header" style="color:#bfdbfe;">', 'SL'),
]

ok = 0
for marker, key in anchors:
    anchor_tag = f'<!-- SC:{key} -->'
    # 既に挿入済みならスキップ
    if anchor_tag in content:
        print(f'SKIP (already): SC:{key}')
        continue
    # <div class="sport-card"> の直前を探す
    # markerの前の <div class="sport-card"> を探して SC コメントを前に挿入
    pos = content.find(marker)
    if pos < 0:
        print(f'MISS: {key} marker not found')
        continue
    # sport-card div の開始位置
    card_div = '<div class="sport-card">'
    card_pos = content.rfind(card_div, 0, pos)
    if card_pos < 0:
        print(f'MISS: {key} no sport-card div before marker')
        continue
    # アンカーを card_div の直前に挿入
    content = content[:card_pos] + f'{anchor_tag}\n      ' + content[card_pos:]
    ok += 1
    print(f'OK: SC:{key} inserted')

# 終了アンカー: 各 SC の次の SC の前に /SC を挿入
# 各 SC:KEY の後、次の SC: または preseason-card の前に /SC:KEY を挿入
import re

for _, key in anchors:
    start_tag = f'<!-- SC:{key} -->'
    end_tag   = f'<!-- /SC:{key} -->'
    if end_tag in content:
        print(f'SKIP end (already): /SC:{key}')
        continue
    if start_tag not in content:
        continue
    idx = content.index(start_tag)
    # 次の SC: または preseason-card を探す
    search = content[idx + len(start_tag):]
    next_sc = re.search(r'<!-- SC:|<div class="preseason-card">', search)
    if not next_sc:
        print(f'MISS: end of {key} not found')
        continue
    insert_pos = idx + len(start_tag) + next_sc.start()
    # insert_pos の手前の </div>\n      </div> を探す
    before = content[idx:insert_pos]
    # 最後の </div> pair を探す
    last_close = before.rfind('</div>\n      </div>')
    if last_close >= 0:
        actual_end = idx + last_close + len('</div>\n      </div>')
    else:
        actual_end = insert_pos
    content = content[:actual_end] + f'\n      {end_tag}' + content[actual_end:]
    print(f'OK: /SC:{key} inserted')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print(f'\nTotal OK: {ok}')
print('dashboard.html saved with SC anchors.')
