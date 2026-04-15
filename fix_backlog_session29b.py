#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""BACKLOG.md: Session _29b update - Output A 7件・Output B top5 に修正"""

backlog_path = r"C:\Users\ohwada\Desktop\claude_sport\BACKLOG.md"
with open(backlog_path, encoding='utf-8-sig') as f:
    content = f.read()

# Output A/B 行を修正
content = content.replace(
    '- [x] 出力A: 1位 Renegades(85%/@1.36) / 2位 Paolini(78%/@1.24)',
    '- [x] 出力A: 7件 Swiatek(92%)・Alcaraz(88%)・Renegades(85%)・Louisville(82%)・Musetti(82%)・Gauff(81%)・Paolini(78%) ← 設計バグ修正後に再スクリーニング済み'
)

content = content.replace(
    '- [x] 出力B: Renegades×Paolini (全体66.3%・マルチOdds1.686・EV+11.8%)',
    '- [x] 出力B: top5コンボ / 1位: Louisville×Renegades×Musetti (全体57.2%・マルチOdds3.0743・EV+75.8%) ← EV+3試合コアが最高'
)

# dashboard・records更新行を追加
content = content.replace(
    '- [x] dashboard.html 高確率予想タブ・マルチベットタブを実データで更新',
    '- [x] dashboard.html 高確率予想タブ・マルチベットタブを実データで更新（最終版: 出力A 7行・出力B 5コンボ）'
)

with open(backlog_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("BACKLOG.md: updated")
