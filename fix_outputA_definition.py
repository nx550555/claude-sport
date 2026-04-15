#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fix Output A definition in CLAUDE.md"""

path = r"C:\Users\ohwada\Desktop\claude_sport\CLAUDE.md"
with open(path, encoding='utf-8') as f:
    content = f.read()

old = """1. **出力A（高確率予想リスト）**を生成する
   - L1〜L4で「確実視できる」と判断した試合のみ抽出（少しでも迷いがある試合は含めない）
   - 確実性が高い順に出力。該当なし → 「該当なし」と出力
   - 出力形式: No. | 試合名 | スポーツ | 推奨 | 推定勝率 | オッズ | 確実と判断した理由"""

new = """1. **出力A（高確率予想リスト）**を生成する
   - L1〜L4で「確実視できる」と判断した試合のみ抽出（少しでも迷いがある試合は含めない）
   - ⚠️ **EVは関係しない**。オッズが低くてもベット価値がなくても、予測として自信があれば含める
   - ⚠️ GOより多くなることが正常（EVフィルターがない分、高確率だがオッズ短い試合も入る）
   - 確実性（推定勝率）が高い順に出力。該当なし → 「該当なし」と出力
   - 出力形式: No. | 試合名 | スポーツ | 推奨 | 推定勝率 | オッズ | 確実と判断した理由"""

if old in content:
    content = content.replace(old, new)
    print("CLAUDE.md Output A definition: updated")
else:
    print("ERROR: anchor not found")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("CLAUDE.md: OK")
