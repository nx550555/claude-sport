#!/usr/bin/env python3
"""Session_30: BACKLOG.md / pending_actions.md 更新"""
import re

BASE = r"C:\Users\ohwada\Desktop\claude_sport"

# ─────────────────────────────────────────────
# BACKLOG.md 更新
# ─────────────────────────────────────────────
bl_path = BASE + r"\BACKLOG.md"
with open(bl_path, "r", encoding="utf-8-sig") as f:
    bl = f.read()

# 1. NHL 4/15 CAUTION2件 → [x] 完了
old1 = "- [ ] NHL RS最終盤 4/15 CAUTION2件 結果確認← CAR@NYI(CAR 1.90) / COL@CGY(COL 1.60 EV+24.8% ただしN016でSKIP相当). 結果要確認"
new1 = "- [x] NHL RS最終盤 4/15 CAUTION2件 結果確認← CAR@NYI CAR 2-1 HIT(CAUTION/nobet) / COL@CGY COL 3-1 HIT(SKIP/N016)。予測両方HIT。"
bl = bl.replace(old1, new1)

# 2. ATP W16 R1 今夜の結果確認 → [x] 完了
old2 = "- [ ] ATP W16 R1 今夜の結果確認（Nava/Shelton 21:10・Blockx/Hanfmann 22:20・Norrie/Wawrinka 23:00・Borges/Mannarino 23:00 全SKIP）→ 明日R2スクリーニング（casino data起点）"
new2 = "- [x] ATP W16 R1 結果確認（全SKIP）: Shelton d.Nava 7-6(4)3-6 6-3 / Blockx d.Hanfmann 7-6(2)6-2 / Norrie d.Wawrinka 6-4 6-7(5)6-4 / Borges d.Mannarino 6-3 6-4 / Molcan d.Bublik(CAUTION) 6-4 6-2 → R2スクリーニングはcasino data待ち"
bl = bl.replace(old2, new2)

changed = (new1 in bl) and (new2 in bl)
with open(bl_path, "w", encoding="utf-8") as f:
    f.write(bl)
print(f"[1] BACKLOG.md updated: changes={'OK' if changed else 'CHECK'}")

# ─────────────────────────────────────────────
# pending_actions.md 更新 - NHL CAUTION結果をDONEに
# ─────────────────────────────────────────────
pa_path = BASE + r"\monitoring\pending_actions.md"
with open(pa_path, "r", encoding="utf-8-sig") as f:
    pa = f.read()

# NHL CAR@NYI / COL@CGY 結果確認は独立したPA項目がなく、BACKLOG参照のみ
# PA002 (ATP W16 R2) はカジノデータ待ち - 変更なし
# PA004 (WTA Stuttgart R2) はパオリーニ戦不完了 - 変更なし
# 新規PA追加: WTA Stuttgart 試合suspension status
note_text = """
---
**Session_30 更新 (2026-04-15):**
- NHL CAR@NYI 2-1 HIT / COL@CGY 3-1 HIT (両CAUTION/SKIP・ベットなし・予測HIT) → pending_games cleared
- UFL DC vs STL CAUTION: Ta'amu確認済・L1データ追加 (DC+16.7/G vs STL-2.0/G、conf78%、EV+12.3%)
- NRL Warriors/Titans GO維持 (Capewell復帰確認) / Broncos REVOKED確認 (Luai+May復帰・Carrigan/Walsh/Paix全欠場)
- ATP W16 R1 全5試合結果記録済
- WTA Paolini vs Sonmez: 2ndセット中断中・未完了 (Sonmez 6-2 lead, 2nd set suspended)
- WTA Zhang vs Noskova: 1stセット中断・未完了
- P003 Stuttgart R1 trigger: 未達 (Paolini/Sonmez + Zhang/Noskova の2試合がまだ未完了)
"""

# Append session note to pending_actions if not already there
if "Session_30 更新" not in pa:
    pa = pa + note_text
    with open(pa_path, "w", encoding="utf-8") as f:
        f.write(pa)
    print("[2] pending_actions.md: Session_30 note追加")
else:
    print("[2] pending_actions.md: Session_30 note既存")

print("\n=== BACKLOG/pending_actions更新完了 ===")
