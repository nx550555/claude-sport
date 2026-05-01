# Session Summary - 2026-05-01 (Session_61)

## 主な成果

### Verified化作業(計約95件)
- NHL pending 16件 verified化(一次ソース率100%、verified hit_rate 50%)
- NBA pending 4件 verified化(一次ソース率100%、verified hit_rate 100%、サンプル小)
- MLB pending 13件 verified化(一次ソース率100%、verified hit_rate 53.8%)
- UFL pending 6件 verified化(一次ソース率100%、verified hit_rate 25%)

### 新規ルール候補(発見、まだ正式実装前)
- P_NHL_drought_g1_surge (evidence 1件、replicability=low)
- P_NHL_finale_motivation_gap (evidence 2件、replicability=medium)
- P_NBA_roster_quality_gap (evidence 1件、replicability=low)
- P_MLB_daily_SP_dominance (evidence 6件、replicability=high) ← 構造的問題
- P_MLB_l1_contrarian_caution (evidence 数件、replicability=medium)
- P_UFL_undefeated_overpriced (replicability=low)
- P_UFL_home_edge_recalibration (replicability=medium)
- P015 補強(UFL [8] LOU/DAL +28点 blowout)

### MLB STEP 4.5 問題発見と部分対応
- 発見: 仕組みは存在するが MLB では機能していない(provisional_go=0、step45全件PENDING)
- 原因1: MLBエントリに kickoff/first_pitch フィールドなし → lineup_watch トリガから漏れる
- 原因2: mlb-morning job が fetch のみで EV再計算→tier昇格→notify 連鎖が未実装
- 原因3: L1指標(team wRC+/FIP)が daily SP variance を捕捉できない構造的限界

### Approach A+B 実装(MLB STEP 4.5の下流整備)
- CLAUDE.md MLBセクション追加(8項目: first_pitch必須、STEP 4.5自動実行パス明示)
- lineup_watch.yml mlb-morning job 拡張(notify scan step追加)
- 欠落スクリプト2件をTODOコメントで明示(commit a5ac9c8)

### Approach C Stage 1 実装(MLB L1見直し)
- M012 (SP-confirmed L1 re-screening) 追加: 新tier "awaiting_lineup" 導入
- M013 (SP matchup differential as L1 tertiary) 追加: SP FIP差/xERA差 0.5以上 を第3指標に
- CLAUDE.md MLBセクション項目9・10追加
- commit 13c32a2

## 数値現状(Session_61末)

| 指標 | 値 | 件数 |
|---|---|---|
| 全体 hit_rate | 67.3% | 320件 (A) |
| verified hit_rate | 64.9% | 74件 (B) |
| legacy hit_rate | 66.7% | 246件 (C) |

スポーツ別準拠率:
- MLB: 86.7% (15件中13件)
- UFL: 57.1% (7件中4件)
- WTA: 25.7% (74件中19件)
- ATP: 22.8% (101件中23件)
- NHL: 17.9% (67件中12件)
- NBA: 7.9% (38件中3件)
- その他(NRL/Soccer/SuperLeague/Premiership/Top14/ProD2/AHL): 0%

## 次回(Session_62)への申し送り

### 中断地点
Approach C Stage 1完了済み。Stage 2(scripts/recalc_ev_from_lineup.py + scripts/promote_provisional_to_go.py 作成)が次の判断ポイント。

### 短期PENDING
- Approach C Stage 2: スクリプト2件作成 → Stage 3: lineup_watch.yml TODOコメント解除
- 残スポーツpendingのverified化(NRL 14, Soccer 29, AHL 35, Premiership 8, Top14 14, Pro D2 7, Super League 5)
- ATP/WTA verified deep のうち analysis null残り1件(ATP #6 Landaluce)

### 中期PENDING
- ルール候補8件の正式昇格判断(柱A protocol で次セッション以降にレポート生成)
- legacy データのGO/Q3_output_a/Q4(計72件)選別verified化
- 実運用再開(Z3): 現在pending試合のスクリーニング

### 構造的気づき
- 仕組みが「存在する」と「機能している」は別: MLB STEP 4.5で実証
- スポーツ横断パターンは限定的: NHLとNBAで挙動異なる(PO G1 upset傾向)
- verified vs legacy の差は最終的に縮小: サンプル増加で 73.8%→64.9%へ
- speculative confidence_levelの活用が機能: motivational narrative の捏造圧力が緩和

### Communication パターン(Session_60-61で確立)
- ask_user_input_v0 で多択質問(Ayumuさんはタップ式好む)
- コードブロックで Claude Code 指示(コピーボタン用)
- Ayumuさんが本質に引き戻す瞬間が複数回(段階1〜2で精度向上ループの本筋を見失いそうになる Claude を矯正)
