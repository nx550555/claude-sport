#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Session _29 BACKLOG update"""

backlog_path = r"C:\Users\ohwada\Desktop\claude_sport\BACKLOG.md"
with open(backlog_path, encoding='utf-8-sig') as f:
    content = f.read()

# 1. WTA Stuttgart R2 スクリーニング: [ ] -> [x]
content = content.replace(
    '- [ ] WTA Stuttgart R2 スクリーニング（R1結果確認後・casino dataまたはOddsPortal起点）',
    '- [x] WTA Stuttgart R2 スクリーニング（R1結果確認後・casino dataまたはOddsPortal起点）← GO: Paolini @1.24 EV+5.4%. 他8試合SKIP. Session_29完了'
)

# 2. NHL RS最終盤 CAUTION: [~] -> update with result pending
content = content.replace(
    '- [~] NHL RS最終盤 4/15 CAUTION2件 → N006（先発G）確認待ち（22〜24時JST）← CAR@NYI(CAR 1.90 EV+42.5%) / COL@CGY(COL 1.60 EV+24.8%)',
    '- [ ] NHL RS最終盤 4/15 CAUTION2件 結果確認← CAR@NYI(CAR 1.90) / COL@CGY(COL 1.60 EV+24.8% ただしN016でSKIP相当). 結果要確認'
)

# 3. Add new completed section after the existing "直近完了" header blocks
new_section = '''## 直近完了（4/15 Session _29: マルチベット機能追加 + スクリーニング完了）

- [x] add_multi_bet.md 実装完了: 「高確率予想（出力A）」「高確率マルチベット（出力B）」タブをdashboard.htmlに追加
- [x] CLAUDE.md スクリーニング後フロー追記（出力A→B→記録→ダッシュボード更新手順）
- [x] records/multi_bets.json 新設（セッション _29 エントリー記録済み）
- [x] 2026-04-15.json 全44試合スクリーニング完了（NBA/NHL/UFL/ATP/WTA Stuttgart/WTA Rouen）
- [x] UFL Week4 全4試合スクリーニング完了: GO×2（Renegades@1.36・Louisville Kings@1.65）・CAUTION×1（Defenders/QB未確認）・SKIP×1（Stallions vs Storm）
- [x] WTA Stuttgart R2 スクリーニング完了（GO: Paolini @1.24 EV+5.4%）
- [x] WTA Rouen R2 スクリーニング完了（全SKIP）
- [x] NBA play-in 全SKIP確認（NRtg差全て5pt未満）
- [x] NHL 4/15 CAUTION2件記録（CAR@NYI / COL@CGY - pending_games）
- [x] records/ufl/2026.json 更新（Renegades GO・Defenders CAUTION・Stallions SKIP追記）
- [x] records/wta/2026.json 更新（Paolini round R1->R2修正・R2/Rouen R2 screening log追加）
- [x] dashboard.html 高確率予想タブ・マルチベットタブを実データで更新
- [x] 出力A: 1位 Renegades(85%/@1.36) / 2位 Paolini(78%/@1.24)
- [x] 出力B: Renegades×Paolini (全体66.3%・マルチOdds1.686・EV+11.8%)
- [ ] UFL W4 全結果確認・記録（4/18-19開催: Renegades GO / Louisville Kings GO）
- [ ] WTA Stuttgart Paolini vs Sonmez 結果確認（試合途中中断→再開後結果確認）
- [ ] NHL CAR@NYI / COL@CGY 結果確認・multi_bets.json hit/miss更新
- [ ] NRL R7 全結果確認・記録（4/16-19: Tigers/Broncos GO・Warriors/Titans GO）

'''

# Insert the new section before the first "## 直近完了" section
insert_marker = '## 直近完了（4/14 _27: 架空情報禁止ルール修正）'
if insert_marker in content:
    content = content.replace(insert_marker, new_section + insert_marker)
    print("Added Session _29 completed section")
else:
    print("WARNING: insert marker not found, appending at end")
    content += '\n' + new_section

with open(backlog_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("BACKLOG.md: OK")
