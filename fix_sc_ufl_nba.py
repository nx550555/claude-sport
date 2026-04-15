#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""UFL と NBA の SC アンカーを挿入（string 検索版）"""
import re

path = r"C:\Users\ohwada\Desktop\claude_sport\dashboard.html"
with open(path, encoding='utf-8') as f:
    content = f.read()

# UFL カードのアンカー - fca5a5 色で UFL という文字を含むカード
# "🏈 UFL" はHTML上では絵文字+UFL
# まずカード全体を見つける
ufl_header = 'color:#fca5a5;">\U0001f3c8 UFL'
nba_header = 'color:#fca5a5;">\U0001f3c0 NBA'

for header, key in [(ufl_header, 'UFL'), (nba_header, 'NBA')]:
    start_tag = f'<!-- SC:{key} -->'
    end_tag   = f'<!-- /SC:{key} -->'

    if start_tag in content:
        print(f'SKIP start (exists): SC:{key}')
    else:
        pos = content.find(header)
        if pos < 0:
            print(f'MISS: {key} header not found')
            continue
        # <div class="sport-card"> の開始を探す（headerの前）
        card_div = '<div class="sport-card">'
        card_pos = content.rfind(card_div, 0, pos)
        if card_pos < 0:
            print(f'MISS: {key} no sport-card div')
            continue
        content = content[:card_pos] + f'\n      {start_tag}\n      ' + content[card_pos:]
        print(f'OK: SC:{key} inserted')

    # 終了アンカー
    if end_tag in content:
        print(f'SKIP end (exists): /SC:{key}')
        continue

    idx = content.index(start_tag)
    after = content[idx:]
    # 次の SC: または preseason-card を探す
    next_sc = re.search(r'<!-- SC:|<div class="preseason-card">', after[len(start_tag):])
    if not next_sc:
        print(f'MISS end: /SC:{key}')
        continue
    end_region = after[len(start_tag):len(start_tag) + next_sc.start()]
    last_matches = list(re.finditer(r'</div>\n      </div>', end_region))
    if not last_matches:
        print(f'MISS end closing div: /SC:{key}')
        continue
    insert_at = idx + len(start_tag) + last_matches[-1].end()
    content = content[:insert_at] + f'\n      {end_tag}' + content[insert_at:]
    print(f'OK: /SC:{key} inserted')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('\ndashboard.html saved.')

# 検証
with open(path, encoding='utf-8') as f:
    c2 = f.read()
for key in ['ATP', 'WTA', 'NHL', 'UFL', 'NRL', 'SRP', 'NBA', 'SL']:
    s = f'<!-- SC:{key} -->' in c2
    e = f'<!-- /SC:{key} -->' in c2
    status = 'OK' if (s and e) else f'PARTIAL(start={s},end={e})'
    print(f'  {key}: {status}')
