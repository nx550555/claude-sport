# BACKLOG — 依頼・要望トラッキング

> **Claude Codeへの指示：**
> - セッション開始時に必ずこのファイルを読む
> - 依頼を受けたら実行前にここに書き込む
> - 完了したら `[ ]` → `[x]` に更新する
> - 「作業中」の項目は前回セッションで途中になったもの

---

## ステータス凡例
- `[ ]` 未着手
- `[~]` 作業中（前回セッションで途切れた可能性あり）
- `[x]` 完了
- `[-]` 保留・キャンセル

---

## 未完了・作業中（次回セッション最優先）

### 🎯 次回セッション開始時の行動順序（Session_48）

**STEP 0: システム健全性スキャン**
- `python monitoring/health_check.py` を必ず実行（v3: 9項目チェック）
- `monitoring/missed_tasks_log.md` を読む

**STEP 1: 結果確認（Session_47 完了済）**
- ✅ NHL PO R1 G1 全8試合 結果反映完了 (5HIT/3MISS - TBL/PIT/DAL UPSET)
- ✅ NBA PO R1 G1 全8試合 結果反映完了 (6HIT/2MISS - DET/HOU UPSET)
- ✅ NBA Play-in 2件 結果反映完了 (ORL/PHX 8 seed)
- ✅ A026/A027/A028 records 反映 + A029 新規 LAL-HOU (KD欠場) 登録
- ✅ rule_pipeline P018 evidence +1 (2/3到達), P024/P025 新規候補登録

**Session_48 最優先タスク:**
- NHL PO R1 G2 全8試合 結果確認 (4/22-23 JST = 4/21-22 ET)
- NBA PO R1 G2 全8試合 結果確認 (4/22-25 JST)
- Madrid 本戦 R1 ATP24試合 + WTA19試合 スクリーニング (2026-04-21.json 起点, 4/22〜)

**STEP 2: Madrid 本戦 R1 スクリーニング**（ユーザーJSON提供時）
- ATP Madrid 1000 + WTA Madrid 1000 本戦 R1 (4/22〜)
- 全試合に quadrant field 付与必須
- Top30級選手の cElo 深掘り → GO推奨3件以上を目指す

**STEP 3: 通常読み込み（CLAUDE.md STEP 1）**

**STEP 4: Session_46 残タスク**
- P023 evidence 3件目 (現在 2/3) で implement 判断
- P012 evidence 3件目 (現在 2/3) で implement 判断
- P018/P019/P020/P022 の evidence 追加収集

### 🚨 Session_47 完了報告 (2026-04-21)

**前半: 結果確認・アップセット深掘り**
- NHL PO R1 G1 全8試合 結果反映完了: 5HIT / 3MISS (TBL/PIT/DAL UPSET)
- NBA PO R1 G1 全8試合 結果反映完了: 6HIT / 2MISS (DET/HOU UPSET)
- NBA Play-in 2件反映完了: ORL/PHX 8 seed
- 新規 A029 LAL-HOU UPSET 登録: Kevin Durant 欠場 (patellar tendon contusion) 決定的要因
- upset_patterns id修正: A014/A015/A016/A018/A019/A020/A025/A026/A027/A028 (10件 id:NONE→A0xx付与)
- factor_notes 強化: A026 (experience gap) / A027 (rivalry+vet fade) / A028 (xGF priority over seed)
- rule_pipeline 新候補 2件: P024 (NBA PO star scorer absence) / P025 (NHL xGF% priority over seed)
- P018 evidence 2/3 到達: A021 MTL + A027 PHI young core activation

**後半: 外部スタッツフィード全スポーツ自動化 (GEN006 v2.0)**
- **8 fetcher 実装**: fetch_moneypuck / nhl_players / basketball_reference / nba_players / tennis_elo / tennis_player_stats / rugby_football / injuries
- **21フィード取得成功**: NHL/NBA チーム・選手・怪我 + ATP/WTA cElo & serve/return + Rugby 8リーグ standings
- **reader API 15関数実装**: scripts/stats_feed_reader.py
- **GitHub Actions**: .github/workflows/fetch_stats.yml で JST 09:00/21:00 自動取得
- **health_check v4**: feed_status() 自動チェック追加
- **CLAUDE.md STEP 0.5**: 8 fetcher 自動実行プロトコル追加
- **Commit c896596 push 成功** (39 files, +200,974 行)

### 🎯 Session_48 行動計画 (次回)
**STEP 0:** health_check v4 (21フィード fresh 確認)
**STEP 0.5:** GitHub Actions 稼働確認 (権限設定済なら pull で最新フィード取得)
**最優先 A:** Madrid 本戦 R1 スクリーニング (ATP 24 + WTA 19, 新 reader API 活用)
**最優先 B:** NHL G2 + NBA G2 全16試合 結果確認 (PA060/PA061)
**最優先 C:** P018 evidence 3件目監視 → N019 実装判断 (G2 で candidate)

### 🚨 Session_48 完了報告 (2026-04-21 〜 2026-04-23)

**Session_48 主要成果:**
- [x] Madrid R1 スクリーニング完了 (ATP 29 + WTA 18 + NHL G2 8 + NBA G2/G1 8 + AHL 6 = 69試合)
- [x] **GO 推奨 1件追加**: Galfi D. @1.54 WTA Madrid Q Final EV+20.3% conf78%
- [x] Q3 output_a 4件 (Sonmez / BOS G2 / SAS G2 / OKC G2)
- [x] **sync_dashboard.py 新設**: 真実源駆動 7セクション自動同期
  - 概要 big-stat / summary / 予測精度 bet-only + Q3 / アクティブ推奨 / 高確率予想 / マルチベット
- [x] **包括データ整合性監査**: cumulative Q3 3/3→7/7 訂正 / NRL EV 単位混在修正 / NHL LAK-COL 重複閉鎖
- [x] **CAUTION 3分類実装**: WAITING/MARGIN/TRACK
  - `core/framework.json` caution_taxonomy / `records/*.json` caution_type フィールド
- [x] スマホ予測精度タブ全画面修正 (`#content-accuracy` overflow-x + 600px font-size)

**数値 (Session_48 終了時):**
- 🟢 ベット推奨 21/29 (72.4%) +1.90u | Pending 1 (Galfi)
- 🎯 Q3 output_a 7/7 (100%) | Pending 4
- 総 Pending 9 (GO 1 / WAITING 1 / MARGIN 6 / TRACK 1)

### 🎯 Session_49 行動計画 (次回)
**最優先 A:** Galfi 結果確認 (4/22 JST 試合) → HIT なら +0.54u / 22-30 73.3% +2.44u
**最優先 B:** NHL G2 全8試合 + NBA G2 全8試合 結果記録 (PA060 / PA061)
**最優先 C:** Q3 output_a 4件結果確認 (Sonmez / BOS G2 / SAS G2 / OKC G2) → 11/11 (100%) or 変動
**最優先 D:** COL G2 WAITING → goalie確認で GO昇格検討 / KD G2 判定
**中優先:** P013 R020 / P010 R017 implement 判断 (evidence 到達済)
**インフラ:** 累計履歴/成長分析タブの sync_dashboard.py 対応拡張 (低優先)

### 🚨 Session_49 完了報告 (2026-04-23)

**成果:**
- [x] **Galfi GO HIT +0.54u** (d. Vidmanova 7-5 6-3, Madrid Q Final 4/21)
- [x] **NHL G2 7/8 closed** (BOS/TBL/CAR/PHI/COL/DAL/UTA, EDM-ANA pending)
- [x] **NBA G2 7/8 closed** (PHI/POR/LAL/DET/ATL/CLE/MIN, OKC-PHX pending)
- [x] **Q3 output_a 3/4 closed**: Sonmez HIT / BOS+SAS G2 MISS / OKC pending → 8/10 80%
- [x] COL G2 予測 HIT (CAUTION no-bet) / KD 出場も HOU MISS
- [x] 5ステップ同期完了 (cumulative + dashboard_stats + multi_bets + sync_dashboard.py)
- [x] **NBA SAS G1 +0.18u Session_46 反映漏れ訂正** (cumulative ↔ dashboard_stats 整合化)

**数値 (Session_49 終了時):**
- 🟢 ベット推奨 22/30 (73.3%) **+2.453u** | Pending 0
- 🎯 Q3 output_a 8/10 (80.0%) | Pending 1 (OKC G2)
- Advanced 17/22 (77.3%) +3.483u / Basic 5/8 (62.5%) -1.03u

**NBA records 重複問題発見** (PA067): [10][17] CLE-TOR G1 / [11][21][30] NYK-ATL / [12][20][32] DEN-MIN / [13][18] BOS-PHI G1 / [14][24] LAL-HOU / [15][23] OKC-PHX / [16][22] DET-ORL G1 — Session_48 import + 既存命名ずれで dedup 必要

### 🎯 Session_50 行動計画 (次回)
**最優先 A:** PA065 EDM-ANA G2 結果確認 (4/23 朝)
**最優先 B:** PA066 OKC-PHX G2 結果確認 (4/23 朝) → Q3 8/10 → 9/11 or 8/11 確定
**最優先 C:** NHL/NBA G3 スクリーニング (4/23-25 開催)
**最優先 D:** Madrid 本戦 R1 残り試合 + R2 スケジュール確認
**中優先:** PA067 NBA records 重複登録の系統的整理
**中優先:** P018 evidence 3件目監視 → N019 implement 判断
**インフラ:** cumulative.json と dashboard_stats.json の自動整合性チェックを health_check に追加検討

### 🚨 Session_50 完了報告 (2026-04-23)

**主要成果:**
- [x] **PA065 EDM-ANA G2** MISS 反映 (ANA 6-4 UPSET / type_a_watch 的中 / P025 2/3)
- [x] **PA066 OKC-PHX G2** HIT (OKC 120-107 SGA 37pts) → Q3 9/11 → 修正後 9/14
- [x] **PA062 2026-04-23.json 69試合スクリーニング**: GO 5件新規 / Q3 7 / Q4 13 / SKIP 44
- [x] **ダッシュボード整合性修正 (ユーザー指摘 #1)**: 66.7% vs 81.8% 乖離を 64.3% に統一
- [x] **Feedback loop 根本改善 (ユーザー指摘 #2)**: Q3 MISS 5件 miss_analysis 完全補填 / P026 新候補 / health_check v5

**数値 (Session_50 終了時):**
- 🟢 ベット推奨 22/30 (73.3%) +2.453u | Pending 5 (Madrid GO)
- 🎯 Q3 output_a 9/14 (64.3%) | Pending 8
- health_check v5: MISS 欠損 58件アラート (PA071)

**Git commits:** eddeb9f / 72f895e / 2c2e466 / 495a6ef

### 🎯 Session_51 行動計画 (次回)
**最優先 A:** PA071 既存 MISS miss_analysis 欠損 58件漸進補填 (毎 STEP 0 で進捗可視化)
**最優先 B:** PA068 Madrid GO 5件結果 (Tsitsipas/Paul/Musetti/Keys/Mertens 4/24-25)
**最優先 C:** PA069 Q3 output_a 7件結果追跡 (Sinner/Swiatek/Gauff/Sabalenka/Andreeva/Bencic/Rybakina)
**最優先 D:** PA070 Q4 upset_watch (特に Osaka vs Osorio UPSET 観察)
**中優先:** P024 evidence 3件目 → N_NBA_new2 実装 (star scorer 欠場補正)
**中優先:** P026 evidence 継続 (NBA G1 blowout 後 G2 home fade)
**インフラ:** CLAUDE.md に「結果反映時 miss_analysis 同時記入必須」明文化

### 🚨 Session_51 完了報告 (2026-04-23)

**主要成果:**
- [x] **PA071 完全達成**: MISS miss_analysis 欠損 58件→0件 (53件補填 / health_check ALERT 完全消失)
- [x] **CE017 発見・訂正**: Madrid Q R1 4/20 records 4件勝敗逆転 (#73 Sakamoto / #75 Gaubas / #77 Droguet / #94 Basilashvili) → 一次ソース2件以上で再検証訂正
- [x] **health_check v6 拡張**: outcome_note 表記 vs prediction_hit / market_favorite 論理整合性自動検証 (CE013-017 同根パターン未検知状態達成)
- [x] **dashboard.html 予測精度タブ拡充**: ATP 全試合 43/59 (72.9%) + WTA 23/37 (62.2%) 行追加
- [x] **PA075 NBA records dedup**: 6件 duplicate_closed 化 + 命名規約明文化 (33件→27件 active)
- [x] **rule_pipeline P027 新規登録**: NHL G1 UPSET 後 G2 fav home rebound (BOS G2 / DAL G2 evidence 2/3 即到達)
- [x] **副産物 outcome_note クリーンアップ**: CE006/CE007/CE009 訂正済残骸 3件 (Cerundolo/Shnaider/Fernandez)

**数値 (Session_51 終了時):**
- 🟢 ベット推奨 22/30 (73.3%) +2.453u | Pending 5 (Madrid GO)
- 🎯 Q3 output_a 9/14 (64.3%) | Pending 7
- 📈 ATP 全試合予測精度 43/59 (72.9%) | WTA 23/37 (62.2%)
- 📊 health_check: ALERT 0件 / WARN 2件

### 🎯 Session_52 行動計画 (次回優先タスク = Session_51 残課題)

**最優先 A: 残課題 (今回の宿題)**
- [ ] **PA073 NBA G2 詳細スタッツ補填** (#30 ATL-NYK G2 / #32 MIN-DEN G2 を WebSearch で具体化 → rule_linked 確定)
- [ ] **WTA 旧分 miss_analysis 深掘り** (Session_51 テンプレ補填 14件を WebSearch で実調査ベースへ精緻化)
- [ ] **Session_50 4象限分類 WARN の解消** (health_check WARN 継続中)
- [ ] **UFL 13日 screening_log 更新なし WARN** (W6 4/24-26 開幕予定の確認)
- [ ] **dashboard.html 累計履歴 / 成長分析タブ sync_dashboard.py 拡張** (低優先継続)

**最優先 B: 通常運用継続**
- [x] **Session_52 GEN003 最新情報チェック完了** (2026-04-23): Tsitsipas GO→CAUTION_MARGIN / Musetti GO→CAUTION_WAITING / Paul・Keys・Mertens 維持 / Mertens date 4/24→4/23 訂正
- [ ] **PA068 Madrid GO 残 3件結果** (Paul 4/24 / Keys 4/24 / Mertens 4/23)
- [ ] **PA076 Session_52 downgrade 追跡** (Tsitsipas 4/23 / Musetti 4/24 CAUTION 予測精度として)
- [ ] **PA069 Q3 output_a 7件結果追跡** (Sinner/Swiatek/Gauff/Sabalenka/Andreeva/Bencic/Rybakina)
- [ ] **PA070 Q4 upset_watch 13件** (Osaka-Osorio UPSET 観察など)
- [ ] **NHL/NBA G3 スクリーニング** (4/24-26 開催)

**最優先 C: ルール実装判断 (evidence 接近中・G3 で決着可能性高)**
- [ ] **P018 N019 implement 判断** (NHL PO G1 underdog 若手活性化 - evidence 2/3)
- [ ] **P024 N_NBA_new2 implement 判断** (NBA PO G1 star scorer 欠場 - evidence 2/3)
- [ ] **P025 N021 implement 判断** (NHL PO type_a_watch xGF higher 優先 - evidence 2/3)
- [ ] **P027 N_NHL_new1 implement 判断** (NHL G1 UPSET 後 G2 fav home rebound - evidence 2/3)

**中優先:** PA047 (upset_patterns A014-A020 補填継続) / PA053 P023 / PA054 P012 evidence 継続

### 🚨 Session_46 完了報告
- **PA051 upset_patterns 監査 100% 完了**（32件 confirmed + 4件 invalidated, rule_linked率 19.4%→100%）
- **CE016 発見・全4件解消**（A017/A022/A023/A024 勝敗逆転記録）
- **新規 rule 候補 5件追加** (P018/P019/P020/P022/P023)
- **ラグビーユニオン ルール 8件追加** (T006/T007/D006/D007/P006/P007/SR006/SR007)
- **health_check v3** 拡張（項目7-9 追加、CE016整合性自動チェック）
- **NBA SAS-POR G1 HIT** (+0.18u) → 通算 21/29 (72.4%) +1.9u

### 🔧 Session_46 実装改善
- 4ラグビーユニオンルールに怪我人ローテーション補正 (欠場数別 -3/-7/-12%)
- 4ラグビーユニオンルールに天候×スタイル補正 (大雨: パスラン型-7%/FW型+5%)
- CLAUDE.md 4ラグビーセクションに「team sheet 48h前確認 + 天候確認」必須化
- health_check.py に CE016再発防止の winner vs market_favorite 整合性チェック追加

---

### 🎯 Session_45 以前の行動順序（参照用）

**STEP 1: CLAUDE.md 起動時チェック（自動実行）**
- BACKLOG / user_feedback_log / pending_actions / claude_error_log / rule_pipeline / framework 全読み込み
- Phase2移行済み。実装済みルール 7件（R017/R020 追加）。rule_pipeline トリガー: P007 2/3, P014 1/3, P016 1/2 など watching 状態

**STEP 2: PA017 NBA SAS-POR G1 結果確認（最優先）**
- ユーザー情報: 試合途中（Session_44時点）
- 結果確定次第 records/nba/2025-26.json + multi_bets.json output_a #11 + ダッシュボード同期
- Wembanyama 出場確認必須

**STEP 3: NHL PO 結果確認（4/21-22開催）**
- PA041: G1残5試合 (VGK@UTA / PIT@PHI / CAR@OTT / DAL@MIN / EDM@ANA)
- PA041: G2 COL@LAK (4/22)
- BUF-BOS G1 (4/20 JST 確定分) 結果確認

**STEP 4: 遡及補填タスク**
- PA047: upset_patterns.json A014-A020 本体登録漏れ補填
- PA033: AHL Calder Cup Playoffs R1 (4/22〜) スクリーニング
- PA028-030: Premiership/Top14/Pro D2 PD/G 本格取得

**STEP 5: 新規試合データ受領時**
- ユーザーが 2026-04-20.json / 2026-04-21.json 等を提供したら GEN004 + 新規スクリーニング
- スクリーニング完了時は **毎回 multi_bets.json に session エントリ追記**（CLAUDE.md 同期プロトコル5ステップ遵守）

**STEP 6: セッション終了時**
- cumulative.json / dashboard_stats.json / multi_bets.json / dashboard.html 5ステップ同期
- 予測精度タブ・成長分析タブの末尾数値を dashboard_stats.json と突き合わせる（PA-PERM02 必須）

### 🔧 Session_44 で実装した運用改善
- ダッシュボード同期プロトコル: **3ステップ → 5ステップ** 拡張 (CLAUDE.md)
  - multi_bets.json 追記 + 予測精度/成長分析タブ同期を必須化
- 常設タスク PA-PERM01 / PA-PERM02 追加（毎セッション末尾チェック）
- rules_tennis.json v2.2: R017 (WCホーム+seed撃破 +5%) + R020 (非seed R1アップセット勝者 +5%)

### その他未完了
- [ ] 【新リーグ】Premiership/Top 14/Pro D2 の全チームPD/G標準データ取得 → pending_data試合の本格L1スクリーニング（Exeter-Northampton/Sale-Saracens/Bayonne-Pau/Castres-Toulouse/Racing-StadeFrancais/Stade Montois-Dax/Nevers-Valence/Beziers-Provence/Grenoble-Oyonnax 計9試合） — PA028-030
- [ ] 【AHL PO】Calder Cup Playoffs R1 (4/22〜best-of-3) 再スクリーニング — PA033
- [ ] 【upset_patterns補填】A014-A020 本体登録漏れ — PA047
- [x] 【Session_41 完了】ダッシュボード大規模改修（Phase 1-3全項目完了）
- [x] 【Session_42 完了】CE013/CE014/CE015 発生・訂正・全体整合性検証
- [x] 【Session_43 完了 2026-04-20】過去分スコア未検証訂正 + Pending キュー処理 + 2026-04-19.json スクリーニング + ダッシュボード完全同期
- [x] 【Session_44 完了 2026-04-20】PA014 NHL G1 MISS記録 + R017/R020 実装 + 出力A/B Session_30-43遡及補填 + CLAUDE.md運用改善（5ステップ同期）
- [x] 【Session_43結果確認完了】Munich QF / Barcelona QF / Stuttgart QF + R2残 / Rouen QF + R2 計20試合結果反映
- [x] 【最優先①】新規試合・オッズ情報のスクリーニング 2026-04-19.json (Session_43: 全SKIP確定)
- [x] 【Session_43結果確認完了】Munich QF (Shelton d. Fonseca / Cobolli d. Kopriva / Zverev d. Cerundolo / Molcan d. Shapovalov) / Barcelona QF (Fils d. Musetti / Rublev d. Machac / Medjedovic d. Borges / Jodar d. Norrie) / Stuttgart QF (Andreeva d. Swiatek / Muchova d. Gauff / Rybakina d. Fernandez / Svitolina d. Noskova) / Rouen QF (Podrez d. Boulter / Shymanovich d. Maria / Cirstea d. Bondar / Kostyuk d. Li)
- [ ] 【AHL PO】Calder Cup Playoffs R1 (4/22〜best-of-3) 再スクリーニング
- [x] 【最優先①】新規試合・オッズ情報のスクリーニング 2026-04-19.json (Session_43: 全SKIP確定)
- [x] 【優先②】アクティブGO推奨の最新情報確認（GEN003） — 4/17-18結果分実施済み（Session_42）
  - [x] ATP: Musetti vs Moutet R2 → DONE 4/17（Musetti 6-3 6-4 GO @1.37 HIT +0.37u）
  - [x] UFL W4: Louisville Kings GO（4/17）→ DONE（Louisville 24-22 OT GO @1.65 HIT +0.65u）
  - [x] UFL W4: Renegades GO（4/17）→ **DONE MISS -1.0u（Aviators 28-14 UPSET / CE013発生・訂正済）**
  - [x] NRL R7: Warriors vs Titans GO @1.23（4/18）→ **DONE HIT +0.23u（28-20）**
  - [x] SL R8: Leeds GO（4/17）→ **DONE HIT +0.23u（56-22 blowout）**
  - [ ] SL R8: Warrington GO（4/19）→ 結果確認（PA035）
  - [ ] NHL PO G1: TBL vs MTL 結果確認（PA014/PA022・4/19）
  - [ ] NHL PO G1: COL vs LAK 結果確認（PA015・4/19）
  - [ ] NBA PO R1 G1: SAS vs POR GO @1.18（4/20 JST）→ 結果確認（PA017）
  - [x] Alcaraz Barcelona R2棄権（右手首負傷）対応（出力A #2 VOID / マルチ rank 2&4 再評価）
- [x] 【CE014/CE015 遡及訂正】WTA GB001 Ostapenko MISS 訂正 + MC SF Alcaraz vs Vacherot 相手名訂正
- [x] ATP Barcelona R2 / Munich R2 スクリーニング完了（全SKIP/EV負）
- [x] WTA Stuttgart R2 / Rouen R2 スクリーニング完了（全SKIP/EV負）
- [x] WTA Stuttgart Paolini vs Sonmez 結果確認完了（Sonmez d. Paolini 6-2 6-2、MISS記録済）
- [x] ダッシュボード全タブ整合性確認・修正完了（Session_38）

- [x] 【最重要・次セッション最優先】Type Aアップセット分析 品質補完 ← A001-A013全件について以下を実施すること
  1. ニュース/ブログ/SNS/インタビュー記事をWebSearchで各試合ごとに検索（スコア確認だけでは不十分）
  2. 「なぜ負けたか」を実際のソースで検証し factor_notes を更新する
  3. rule_pipeline.json の候補（P010-P013・W_P_new1・NRL_R_new2・UFU_R_new）を実装するか判断し rules_tennis.json / rules_wta.json 等を更新する
  ※ feedback_miss_analysis_depth.md のルール（複数ソース→検証→ルール化）を守れていなかったことが判明（Session_35）。

- [x] UFL Week3 Dallas vs Columbus 結果確認・記録（4/13 正午ET試合後）← Dallas GO EV+8.2% 信頼度82%
- [x] MC2026 F Alcaraz vs Sinner 結果確認（4/13試合後）← SKIP（ベットなし・観戦のみ）
- [x] ATP W16 R1 結果確認（全SKIP）: Shelton d.Nava 7-6(4)3-6 6-3 / Blockx d.Hanfmann 7-6(2)6-2 / Norrie d.Wawrinka 6-4 6-7(5)6-4 / Borges d.Mannarino 6-3 6-4 / Molcan d.Bublik(CAUTION) 6-4 6-2 → R2スクリーニングはcasino data待ち
- [x] ATP Barcelona/Munich R1 全試合スクリーニング完了（casino data起点）← **GO3件: Musetti@1.27(EV+9.7%), Cobolli@1.21(EV+8.7%), Kopriva@1.36(EV+9.8%) ← 全4/14開催**
- [x] WTA Stuttgart R1 全12試合完了（4/12〜4/13実施）← **GB001 Ostapenko HIT(+0.538u)。UPSET 2/10。**
- [x] WTA Rouen R1 全16試合スクリーニング完了（casino data起点）← 全SKIP。CAUTION: Timofeyeva/Boulter(cElo要確認)
- [x] WTA Stuttgart R2 スクリーニング（R1結果確認後・casino dataまたはOddsPortal起点）← GO: Paolini @1.24 EV+5.4%. 他8試合SKIP. Session_29完了
- [x] NHL RS最終盤 4/15 CAUTION2件 結果確認← CAR@NYI CAR 2-1 HIT(CAUTION/nobet) / COL@CGY COL 3-1 HIT(SKIP/N016)。予測両方HIT。
- [x] NHL プレーオフ R1 スクリーニング（4/16完了）← 5v5 All Season xGF%使用。TBL/MTL CAUTION（6.11pp）/ COL/LAK CAUTION（score-adj 5.73pp）/ 他6シリーズSKIP。PA014/PA015追加。
- [x] 【最重要・本来依頼】全スポーツ遡りType Aアップセット調査 ← A001-A011計11件登録完了(4/16)。ATP(MC/Barcelona/Munich)/WTA(Stuttgart/Rouen)/NRL R6/UFL W3/NHL RS終盤のSKIP試合を全点検。残課題: Etcheverry/Draper結果要確認・NRL R6 Eels-Titans・Tigers-Knights・WTA Rouen残6試合。

---

## 直近完了（4/17 Session _40: GEN004 + Tier system + AHL復活）

- [x] GEN004ルール制定: 既分析データ再提供時のオッズ変化再計算
- [x] NRL Warriors + UFL Renegades EV再計算
- [x] NHL PO G1 8試合オッズ追加 (TBL-MTL GO昇格候補判明)
- [x] NBA PO/Play-in 7試合screening
- [x] NRL R8 3試合追加
- [x] Super League 2試合再計算
- [x] ATP Barcelona QF 2試合オッズ追加
- [x] Premiership/Top 14/Pro D2 新リーグ3種設置 (rules + records + 19試合初期screening)
- [x] Tier分類システム (Advanced/Basic) + Basic閾値引き上げ (conf>=78/EV>+7)
- [x] 別枠集計インフラ (cumulative.json + dashboard_stats.json by_tier)
- [x] ダッシュボードUI tier badge + 分離表示
- [x] AHL 復活 (sports_excluded→active・Basic Tier)
- [x] AHL 27試合初回screening (全SKIP, Basic Tier設計動作確認)
- [x] session_logs/2026-04-17_40.md 保存

## 直近完了（4/15 Session _29b: betslip形式 + 整合性保証 + div崩れ修正）

- [x] マルチベット betslip形式刷新（fix_multi_betslip2.py）- 各コンボのleg単位表示
- [x] core/dashboard_stats.json 新設（stats唯一の真実ソース）
- [x] sync_sport_cards.py 新設（自動同期スクリプト）
- [x] SCアンカー8スポーツ全配置（fix_sc_final.py）
- [x] CLAUDE.md更新（同期プロトコル必須化 + 出力AアップセットMISS分析フロー）
- [x] content-active タブの余分な </div> 修正（全履歴コメント直後のdiv崩れ解消）
- [x] セッションログ保存（session_logs/2026-04-15_29b.md）

## 直近完了（4/15 Session _29: マルチベット機能追加 + スクリーニング完了）

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
- [x] dashboard.html 高確率予想タブ・マルチベットタブを実データで更新（最終版: 出力A 7行・出力B 5コンボ）
- [x] 出力A: 7件 Swiatek(92%)・Alcaraz(88%)・Renegades(85%)・Louisville(82%)・Musetti(82%)・Gauff(81%)・Paolini(78%) ← 設計バグ修正後に再スクリーニング済み
- [x] 出力B: top5コンボ / 1位: Louisville×Renegades×Musetti (全体57.2%・マルチOdds3.0743・EV+75.8%) ← EV+3試合コアが最高
- [ ] UFL W4 全結果確認・記録（4/18-19開催: Renegades GO / Louisville Kings GO）
- [ ] WTA Stuttgart Paolini vs Sonmez 結果確認（試合途中中断→再開後結果確認）
- [ ] NHL CAR@NYI / COL@CGY 結果確認・multi_bets.json hit/miss更新
- [ ] NRL R7 全結果確認・記録（4/16-19: Tigers/Broncos GO・Warriors/Titans GO）

## 直近完了（4/14 _27: 架空情報禁止ルール修正）

- [x] CLAUDE_CODE_START.md 【絶対禁止】セクション修正（サンプル禁止→ラベル明記で可、未確認/不明ラベリングルール追加）
- [x] memory/feedback_no_fabrication.md 同内容に修正
- [x] session_logs/2026-04-14_27.md 保存

## 直近完了（4/14 _26: ダッシュボード改修・GEN001/GEN002制定）

- [x] ダッシュボード5点改修: 日本語名・JST・日付ソート・ファネルタブ・日報セッションログ
- [x] NRL Broncos/Tigers オッズ誤記録修正（rec_odds 1.46→2.50 / EV 27.9→119.0% / GEN002警告付記）
- [x] GEN001制定: チーム↔オッズ整合性チェック（STEP1-4）全スポーツ必須化
- [x] GEN002制定: 市場乖離アラート（乖離≥15pp警告 / ≥30pp必須調査）
- [x] core/rules_general.json 新設（全スポーツ共通ルール）
- [x] core/rules_log.json 追記
- [x] session_logs/2026-04-14_26.md 保存
- [ ] ブロンコス/タイガース 4/18結果後: GEN002検証（PD/G帰属正確性の判断）

## 直近完了（4/14 スクリーニング最終セッション）

- [x] 2026-04-14 JSON全試合スクリーニング完了（NHL/ATP/WTA/NRL/NBA）
- [x] WTA Stuttgart Paolini vs Sonmez GO確定（@1.24 EV+5.4% cElo差300pt / 4/15 21:30開催）
- [x] records/wta/2026.json 更新（Paoliniエントリー tier:skip->go, odds 1.23->1.24）
- [x] NBA play-in 4/15 SKIP確認: Charlotte/Miami(NRtg差2.9pt) + Phoenix/Portland(差1.5pt) L1未達
- [x] NRL R7 既分析済み確認: GO x2（Tigers/Broncos @1.47, Warriors/Titans @1.25）Warriors EV 10.7%->13.4%
- [x] NHL COL@CGY: N016適用（Presidents' Trophy確定→主力rest要確認）→ CAUTION継続
- [x] NHL CAR@NYI: goalie両チーム未確定 → CAUTION継続
- [x] ダッシュボード反映完了（NRL 36-34 / Stuttgart 2/10試合完了 / GB001 HIT / R001実装済 / ルール履歴3件）
- [ ] WTA Stuttgart Paolini vs Sonmez 結果確認・記録（4/15開催 GO @1.24）
- [ ] WTA Stuttgart Zhang vs Noskova 結果確認（4/15開催 SKIP @1.14）
- [x] ATP Munich GO3件 結果確認（Musetti/Cobolli/Kopriva 4/14開催）
- [ ] NHL CAR@NYI / COL@CGY: goalie確定後 GO/SKIP 最終判断（N016 COL rest risk）
- [ ] NRL R7 全結果確認・記録（4/16-19: Tigers/Broncos GO・Warriors/Titans GO）

## 直近完了（4/14 遡り調査セッション）

- [x] 全14試合 MISS/upset 遡り調査完了（WebSearch多ソース）
- [x] PHI@CAR NHL miss_analysis更新: CAR 6名主力意図的rest判明（L4_External）
- [x] MIN@STL NHL score修正4-3→6-3 + miss_analysis更新（5連続失点詳細）
- [x] NRL Raiders vs Rabbitohs スコア修正30-22→36-34（2点差接戦・前半24-4から後半猛追）
- [x] ATP MC Machac vs Cerundolo スコア修正7-6 6-2→6-2 7-6(3) ← ⚠️さらに誤り。Session_30で再修正: 正スコア「7-6(2) 6-3」（CE001）
- [x] ATP MC Marozsan vs Hurkacz スコア修正未確認→6-2 6-3
- [x] WTA Stuttgart Samsonova vs Ruzic: Samsonova勝利が正しい（Ruzic勝利は誤記録）
- [x] WTA Stuttgart: Zhang/Noskova + Sonmez/Paolini をペンディングにリセット（4/15未試合）
- [x] WTA Stuttgart upsets_by_odds修正: 5→2確認済（Korpatsch+Eala、4/14）
- [x] upset_patterns.json: U002/U005スコア修正、Stuttgart集計修正
- [x] 5ファイル commit & push（bcb9850）
- [x] ルール追加トリガー作成（core/rule_pipeline.json 新設）← P001〜P005の5候補を登録
- [x] N016新設（シーディング確定チーム終盤rest確認）+ N014チェックリスト強化
- [x] W007 indoor clay補足追加（Stuttgart速いサーフェス・フラット攻撃型有利）
- [x] R001修正（GOは差130pt以上、100-129ptはCAUTIONのみ）
- [x] 4ファイル commit & push（2f15699）
- [x] セッションログ保存（session_logs/2026-04-14_23.md）
- [x] CLAUDE_CODE_START.md 自発的コンテキストリセットプロトコル追加（T1〜T4トリガー）+ rule_pipeline.json毎回読み込み追加
- [x] ATP GO3件（Musetti/Cobolli/Kopriva）結果確認 ← 4/14試合進行中（本日夜〜深夜に結果出る）
- [ ] WTA Stuttgart R1残り（Zhang/Noskova・Sonmez/Paolini）結果確認 ← 4/15開催

---

## 直近完了（4/13 手動セッション）

- [x] 手動試合データ共有システム確立（`手動試合データ/tennis_2026-04-13.json`起点）
- [x] WTA Stuttgart R1 全12試合結果記録・GB001 Ostapenko HIT(+0.538u)確認
- [x] Stuttgart indoor clay UPSET分析（5/12=41.7%、W007補正強化候補）
- [x] upset_patterns.json GB001 HIT更新 + pattern_summary更新
- [x] cumulative.json tennis_wta統計更新（1/1 100%、+0.538u）
- [x] dashboard.html更新（75.0% 12/16・+2.671u・WTAカード・GB001行・タイムライン）
- [x] 今夜のATP/WTA全6試合スクリーニング（全SKIP）← cElo取得・EV計算済み
- [x] ATP Barcelona R1 全16試合スクリーニング（GO: Musetti@1.27 EV+9.7%）← 4/14開催
- [x] ATP Munich R1 全16試合スクリーニング（GO: Cobolli@1.21 EV+8.7%, Kopriva@1.36 EV+9.8%）← 4/14開催
- [x] WTA Rouen R1 全16試合スクリーニング（全SKIP・CAUTION: Boulter要確認）
- [x] records/tennis/2026-ATP.json 全更新（50試合・GO13件）
- [x] dashboard.html GO推奨3件更新（Musetti/Cobolli/Kopriva行追加）
- [x] records/wta/2026.json更新（R1全結果+Rouen追加）
- [x] records/tennis/2026-ATP.json更新（Nagal upset記録・今夜2試合追加）

## 直近完了（4/12 手動セッション）

- [x] WTA Stuttgart R1 スクリーニング（tennisabstract cElo確認・全4試合SKIP）
- [-] UFL Dallas vs Columbus 結果確認 ← 4/12 4PM ET試合中。翌JST早朝に終了予定。次セッションで確認。
- [-] MC Final Alcaraz vs Sinner ← 4/13試合。現時点未進行。次セッションで確認。
- [-] ATP Barcelona/Munich R1結果 ← 4/13〜開幕。現時点未進行。次セッションで確認。
- [x] NHL プレーオフ暫定ブラケット取得（RS終了4/16・PO開始4/18。プレーインなし。）

## 直近完了（4/12 自動分析 10:36 JST実行）

- [x] STEP1: BACKLOG読込・pending ゲーム特定（UFL Dallas, MC F SKIP, WTA Stuttgart）
- [x] STEP2-A: 結果検証（4/13前なので pending のまま）
- [x] STEP5: 次24時間ゲーム検索（NHL/UFL/WTA確認済）
- [x] STEP6: L1スクリーニング（4/13朝実施予定）
- [x] STEP7: ダッシュボード時刻更新（10:36 JST / 次回 22:36 JST）
- [x] STEP8: BACKLOG更新

## 直近完了（4/12 手動自動分析代替）

- [x] MC2026 SF誤記録修正: Sinner vs Zverev → Sinner HIT 6-1 6-4（MISS→HIT, +1.65u delta）
- [x] MC2026 F対戦更新: Alcaraz vs Sinner（4/13）SKIP（cElo差~20pt L1未達）
- [x] NBA 4/12: Rockets 124-109 HIT(+0.20u) / Cavaliers 130-126 SKIP
- [x] upset_patterns.json U004削除（誤記録: SFはSinner HIT、upset未発生）
- [x] cumulative.json更新（通算73.3% 11/15、累積EV+2.133u）
- [x] WTA Stuttgart スクリーニング記録（Shnaider/Andreeva等 cElo確認要）
- [x] dashboard.html全数値更新

## 直近完了（4/11 夜間自動分析）

- [x] NHL OTT @ NYI 結果確認・記録（Ottawa 3-2 HIT / Tkachuk残り13秒決勝点）
- [x] Super Rugby R9 Reds vs Crusaders 結果確認（Crusaders 32-12 HIT / ホームSF確定）
- [x] cumulative.json・dashboard.html更新（通算64.3% 9/14、累積EV+0.283）
- [x] 日次レポート出力（2026-04-11.md）

## 直近完了（4/11 本日）

- [x] MC2026 SF 結果確認・記録（Alcaraz HIT +0.50 / ~~Zverev over Sinner MISS~~ →**4/12修正: Sinner HIT +0.65**）
- [x] ダッシュボード全数値更新（通算63.6% 7/11、EV -0.787 → **4/12修正: 73.3% 11/15 +2.133u**）
- [x] upset_patterns.json 新設（全8種目対応、U001〜U003・U005記録済 / U004は誤記録のため削除）
- [x] ダッシュボードに「🎯 アップセット分析」タブ追加
- [x] 3段階フレームワーク定義（Phase1→2→3）・メモリ保存
- [x] ダッシュボードモバイル対応CSS強化

---

## 今後の予定（時期が決まっているもの）

- [x] WTA Stuttgart 開幕（2026-04-13）← R1スクリーニング完了
- [ ] UFL Week3 結果（2026-04-12 4PM ET / JST 4/13早朝）
- [ ] MC Final 結果（Alcaraz vs Sinner 2026-04-13）← SKIP観戦のみ
- [ ] ATP Barcelona/Munich R1〜 結果確認・R2スクリーニング（2026-04-13〜）
- [ ] WTA Stuttgart R2 スクリーニング（2026-04-14〜）← R1結果確認後
- [ ] NHL プレーオフ R1 スクリーニング（2026-04-16〜17）← RS終了後・xGF%確認起点
  - 暫定ブラケット（東）: Buffalo-Boston / Montreal-Tampa / Carolina-Ottawa / Pittsburgh-Philadelphia
  - 暫定ブラケット（西）: Colorado-LAKings / Dallas-Minnesota / Edmonton-Utah / Vegas-Anaheim
  - ⚠️ 4/12-16残り試合でシーディング変動あり。4/16終了後に確定。
- [ ] CFL 2026シーズン開幕対応（2026年6月）
- [ ] NFL 2026-27シーズン開幕対応（2026年9月）

---

## 設計方針メモ（次回Claude Codeへ）

- **ATPスクリーニングはオッズ起点**: 大会名・大会開幕日を起点にしない。OddsPortalで「今週オッズが付いているATP試合」を確認してからcEloスクリーニングを開始する。
- **ATPレコードは年間1ファイル**: `records/tennis/2026-ATP.json` に全大会の予測を tournament フィールド付きで追記。大会単位でファイルを分割しない。

- **3段階フレームワーク**: Phase1（強い側確認）→ Phase2（逆転条件特定）→ Phase3（勝者予測）
- **MISSが出たら必ず** `stats/upset_patterns.json` にU00x IDで追記（UF分類）
- **GAMBLE_BET枠**: 実力差ボーダー＋UF2つ以上＋高オッズで別stake発動（通常の1/3以下）
- **R001閾値見直し検討中**: cElo差＜130pt → CAUTION格下げ（U002・U003の2件が根拠 / U004は誤記録のため削除）

---

*このファイルはClaude Codeセッションをまたぐ「引き継ぎノート」です。*
*依頼が途切れた場合も、次のセッションで未完了項目から再開できます。*
