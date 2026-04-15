#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SC アンカーを全削除して正しい位置に再挿入する"""
import re

path = r"C:\Users\ohwada\Desktop\claude_sport\dashboard.html"
with open(path, encoding='utf-8') as f:
    content = f.read()

# 1. 全SC アンカーをクリア
content = re.sub(r'\s*<!-- (?:SC|/SC):[A-Z]+ -->', '', content)
print("全SC アンカー削除完了")

# 2. sport-card-header の色から正しくアンカーを付与
# 各カードのユニーク識別子 (header内のコンテンツ)
SPORT_ANCHORS = [
    # (ヘッダー内の一部テキスト, キー)
    ('color:#79c0ff;',  'ATP'),
    ('color:#f9a8d4;',  'WTA'),
    ('color:#a5f3fc;',  'NHL'),
    ('color:#fca5a5;">\U0001f3c8 UFL', 'UFL'),
    ('color:#86efac;',  'NRL'),
    ('color:#c4b5fd;',  'SRP'),
    ('color:#fca5a5;">\U0001f3c0 NBA', 'NBA'),
    ('color:#bfdbfe;',  'SL'),
]

# sport-cards セクションのみを対象に処理
section_start = content.find('<div class="sport-cards">')
section_end   = content.find('</div>', content.find('<div class="preseason-card">'))
section       = content[section_start:section_end]

# 全 sport-card ブロックを抽出
card_blocks = list(re.finditer(
    r'<div class="sport-card">[\s\S]+?</div>\s*\n\s*</div>',
    section
))
print(f"見つかった sport-card ブロック数: {len(card_blocks)}")

# 各ブロックにキーを割り当て
key_for_block = {}
for m in card_blocks:
    block = m.group()
    for identifier, key in SPORT_ANCHORS:
        if identifier in block:
            key_for_block[m.start()] = key
            break

print("ブロック→キー:", {k: v for k, v in sorted(key_for_block.items())})

# セクション内でアンカーを挿入（後ろから処理してオフセットズレを防ぐ）
for m in reversed(card_blocks):
    pos = m.start()
    end = m.end()
    key = key_for_block.get(pos)
    if not key:
        print(f"  [WARN] キー不明: pos={pos}, block_preview={m.group()[:60]!r}")
        continue
    block = m.group()
    # アンカー付きブロックに置換
    new_block = f'<!-- SC:{key} -->\n      {block}\n      <!-- /SC:{key} -->'
    # section内の位置を調整
    section = section[:pos] + new_block + section[end:]
    print(f"  OK: SC:{key}")

# section を content に戻す
content = content[:section_start] + section + content[section_start + len(content[section_start:section_end + 6]):]
# 正確にはsection_startからsection_endまでを置換
# まず元のsection_endを使わず、直接置換
original_section = content[section_start:]
# 元の <div class="sport-cards"> から </div>\n      </div> (preseason後) まで
# もっとシンプル: content の section_start 以降で sport-cards を置換
content = content[:section_start] + section + content[section_start + (section_end - section_start):]

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("\ndashboard.html saved.")

# 検証
with open(path, encoding='utf-8') as f:
    c2 = f.read()
all_ok = True
for _, key in SPORT_ANCHORS:
    s = f'<!-- SC:{key} -->' in c2
    e = f'<!-- /SC:{key} -->' in c2
    status = 'OK' if (s and e) else f'FAIL(start={s},end={e})'
    if not (s and e):
        all_ok = False
    print(f"  {key}: {status}")

if all_ok:
    print("\n全アンカーOK！sync_sport_cards.py を実行してください。")
