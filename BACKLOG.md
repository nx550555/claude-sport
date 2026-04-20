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

### 🎯 次回セッション開始時の行動順序（Session_47）

**STEP 0: システム健全性スキャン**
- `python monitoring/health_check.py` を必ず実行（v3: 9項目チェック）
- `monitoring/missed_tasks_log.md` を読む

**STEP 1: 結果確認（優先）**
- NHL EDM-ANA G1 (4/20 深夜・試合後判明見込み)
- NBA LAL-HOU G1 (4/20 深夜・試合後判明見込み)
- NBA G2 (CLE/NYK/DEN @ 4/21, SAS @ 4/22, BOS @ 4/23)
- NHL G1残5試合 + G2全7試合 (4/21-22)
- ORL-DET G1 結果の records/nba/2025-26.json 反映確認（A026 upset_patterns にあるが records 側未検証）
- NHL A021(TBL-MTL)/A027(PHI-PIT)/A028(MIN-DAL) の records/nhl/2025-26.json 反映確認

**STEP 2: Madrid 本戦 R1 スクリーニング**（ユーザーJSON提供時）
- ATP Madrid 1000 + WTA Madrid 1000 本戦 R1 (4/22〜)
- 全試合に quadrant field 付与必須
- Top30級選手の cElo 深掘り → GO推奨3件以上を目指す

**STEP 3: 通常読み込み（CLAUDE.md STEP 1）**

**STEP 4: Session_46 残タスク**
- P023 evidence 3件目 (現在 2/3) で implement 判断
- P012 evidence 3件目 (現在 2/3) で implement 判断
- P018/P019/P020/P022 の evidence 追加収集

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
