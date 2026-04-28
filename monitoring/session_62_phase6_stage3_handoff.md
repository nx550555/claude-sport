# Session_62 フェーズ6 第3段階 完了 引き継ぎサマリ

> **新セッション読込必須**: このファイルは Session_62 (2026-04-28) のフェーズ6 (統合動作確認 + 議題1〜9 協議) のうち、**第3段階 (議題1〜9 協議完了)** 時点のスナップショット。新セッションでは **第4段階 (CLAUDE.md / health_check.py / memory への実装反映)** から再開する。

---

## 1. Session_62 全体構造の現在地

| フェーズ | 内容 | 実施状況 |
|---|---|---|
| フェーズ1 | 改修対象ファイルの現状把握 | ✅ 完了・ユーザー承認済 |
| フェーズ2 | 柱A: ルール改訂統制プロトコル新設 | ✅ 完了・ユーザー承認済 |
| フェーズ3 | 柱B: 結果反映 STEP 0.5 scope外UPSET スキャン SOP 新設 | ✅ 完了・ユーザー承認済 |
| フェーズ4 ステージ1 | 柱C 4-1: MISS 重要度3段階分類 | ✅ 完了・ユーザー承認済 |
| フェーズ4 ステージ2 | 柱C 4-2: fetch 件数規定 | ✅ 完了・ユーザー承認済 |
| フェーズ4 ステージ3 | 柱C 4-3: 情報源タグ義務化 | ✅ 完了・ユーザー承認済 |
| フェーズ5 | 柱D: 記録対象判断テーブル新設 | ✅ 完了・ユーザー承認済 |
| フェーズ6 第1段階 | 仮想 Session_63 ワークフロー書き出し | ✅ 完了・ユーザー承認済 |
| フェーズ6 第2段階 | Session_61 vs Session_63 比較表 (10観点 + 逸脱パターン7種) | ✅ 完了・ユーザー承認済 |
| **フェーズ6 第3段階** | **議題1〜9 協議 (連動議題グルーピング順)** | ✅ **完了・ユーザー承認済 (2026-04-28)** |
| フェーズ6 第4段階 | 議題確定後の最終調整 (CLAUDE.md / health_check.py / memory / agenda.md 反映) | 🔴 **新セッションで実施** |
| フェーズ6 第5段階 | フェーズ6 完了報告 + Session_62 全体総括 + 引継ぎサマリ作成 | 🔴 第4段階完了後に実施 |
| (4本柱完了後別タスク) | A-3 遡及判断 + Session_61 ペンディング事項 + Session_61 9件振り分け実施 + 議題5/7/9 統合実施 | 🔴 4本柱 全フェーズ完了後 |

**重要原則 (Session_62 全期間共通)**:
1. 各段階完了時にユーザー承認を待つ
2. 既存の rules_*.json / records / upset_patterns.json への書き込みは本作業中は実施しない (メタルール側の改修のみ)
3. 不明点があれば実装を止めて質問
4. 「ついでにこれもやっておきました」は禁止
5. Session_61 ペンディング事項 (Modified 8件 + Untracked 4件 / R024→R025 再付番 / ready_to_implement P020/P024) は **4本柱 全フェーズ完了まで一切手を付けない**
6. 議題5 / 議題7 / 議題9 の実装は4本柱完了後の遡及判断タスクと統合実施

---

## 2. 議題1〜9 確定内容詳細

### 議題1: evidence の時間的独立性 (単独・即時反映)

**確定方針**: **案C + 案A 併用** — 異セッション独立検出を原則 + proposal は次セッション以降。

- evidence 3件は原則として **異なるセッション** での独立検出であること (案A)
- 同セッション内で複数件 evidence が追加された場合は、最後の追加から **次セッション以降** に proposal 生成を必須化 (案C)
- ユーザー質問契機 evidence の別カウント (案D) は不採用 (検出契機による区別はせず、独立性のみで判定)

**実装箇所**:
- `core/rule_pipeline.json` の `approval_workflow.step1_threshold_reached` 拡張 (evidence 時間的独立性チェック追加)
- `core/rule_pipeline.json` の `forbidden_practices` 追加項目 (同一 turn 内 evidence 検出 → implement の禁止)
- CLAUDE.md【ルール改訂統制プロトコル】サブセクション3「新規ルール実装プロセス」に「evidence 時間的独立性チェック」追記

---

### 議題2: STEP 0.5 実施保証の仕組み (単独・即時反映)

**確定方針**: **案A + 案D 併用** — 機械チェッカー + records `step05_scanned_at` フィールド。

- records エントリに `step05_scanned_at` フィールドを必須付与 (prediction_hit 確定時に同時付与) (案D)
- `monitoring/health_check.py` に **13項目目** として STEP 0.5 実施確認検査を追加 (案A 相当の機械チェッカー)
- 結果反映 commit に対し、対象試合 records の `step05_scanned_at` 未付与を WARN/ALERT 化
- (案B) 構造化ログ / (案C) commit hook / (案E) 出力フォーマット強制 は不採用

**実装箇所**:
- `monitoring/health_check.py` 13項目目として STEP 0.5 実施確認 (records JSON 走査 + step05_scanned_at 検出 + ALERT/WARN 化)
- 柱B 結果反映 STEP 0.5 SOP に「step05_scanned_at 必須付与」追記
- CLAUDE.md【結果反映 STEP 0.5・毎回必須】サブセクション2「スキャン実行手順」に step05_scanned_at 付与タイミング明示

---

### 議題3: confidence_drift 種目別閾値 (議題7と連動・即時反映)

**確定方針**: **Claude Code 提示の暫定案を採用**。

| 種目 | 薄勝ち閾値 (confidence_drift=high 付与基準) |
|---|---|
| ATP / WTA テニス | 3セット縺れ (2-1 で勝利) |
| NHL | OT 突入 OR regulation 1点差 |
| NBA | 1桁差 (1〜9点差) |
| MLB | 1点差 |
| サッカー (5大リーグ) | 1点差 |
| NFL | TD 1個差以内 (1〜8点差) |
| ラグビー (Premiership / Top14 / Pro D2 / NRL / Super League / Super Rugby) | TD 1個差以内 (リーグ系=6点差以内 / ユニオン系=7点差以内) |

- 推定勝率 ≥ 80% で予想 + 上記閾値内で勝利 → `confidence_drift: "high"` 付与必須
- フェーズ6 第3段階確定をもって `confidence_drift` フィールド付与は **必須化** (フェーズ4 ステージ1 「枠組みのみ」状態を解除)

**実装箇所**: 柱C 4-1 セクションに「confidence_drift 種目別閾値テーブル」追加 + 「具体閾値確定までは任意」の文言を「フェーズ6 第3段階確定をもって必須化」に置換

---

### 議題4: タグ付与の粒度ガイドライン (単独・即時反映)

**確定方針**: **解釈B + 但し書き5項目**。

ガイドライン確定内容:
1. **同一 source からの複数データ列挙は段落末1タグ可** (解釈B 採用)
2. **source が異なる主張は別タグ必須** (但し書き①)
3. **INFER と FETCH/FETCHER/SEARCH の混在文は両方タグ必須** (但し書き②)
4. **否定主張も事実に基づく場合はタグ必須** (但し書き③)
5. **INFER の推論連鎖は末尾1タグでOK** (但し書き④)

**実装箇所**: 柱C 4-3 セクションに「タグ付与の粒度ガイドライン」サブセクション追加 + `memory/feedback_no_fabrication.md` 補強 (但し書き5項目を追記)

---

### 議題5: match_status 遡及範囲 (議題6と連動・別タスク統合)

**確定方針**: **案B 採用** — retired/walkover 区別判定して遡及付与。

- 既存 records 100件超の `void: true` エントリを WebSearch で再確認し、`match_status` を `retired` / `walkover` / `cancelled` / `postponed` のいずれかに判定
- 既存 `void: true` フィールドは後方互換用として維持 (削除せず・両方併存)
- **実装は4本柱完了後の遡及判断タスクと統合実施** (Session_61 由来 12件 + 9件振り分け + R024→R025 再付番タスク等と一括処理)
- **フェーズ6 第4段階では agenda.md 記録のみ・実装変更なし**

**実装箇所 (別タスク)**: `records/{sport}/*.json` 全件走査 + WebSearch 再確認 + match_status 付与スクリプト

---

### 議題6: 大会優先度テーブル維持責任 (議題5と連動・即時反映)

**確定方針**: **案C 採用** — 名称変更=B区分 + 新リーグ追加=対象外 階層化。

- **既存大会の名称変更** (例: ATP 250 → ATP Tour 250) → **B区分 (柱A 承認必須)**
- **新リーグ追加** (例: 新スポーツ・新リーグの scope 追加) → **柱A 適用対象外、追記のみ**
- 名称変更 / 新リーグ追加の境界判断は **ケースバイケース対応**

**実装箇所**:
- 柱D サブセクション6「新リーグ追加 SOP」の文言修正 (「柱A 適用対象外、追記のみ」→「新リーグ追加=柱A 適用対象外・名称変更=B区分・両者の境界判断はケースバイケース」)
- 柱A サブセクション1「適用対象 (承認必須ファイル)」に「CLAUDE.md 既存大会の名称変更は B区分 / 新リーグ追加は対象外」の階層化規定追記

---

### 議題7: 区分2 cumulative 集計除外境界 (議題3と連動・別タスク統合)

**確定方針**: **案C 採用** — `by_record_class` 別軸集計。

- **Track 1 (ベット推奨収益性)** = **区分1 のみ** (現行維持)
- **Track 2 (全試合モデル品質)** = **`by_record_class` 別軸集計** (区分1 のみ + 区分1+2 並列追跡)
- cumulative.json に `by_record_class` セクション新設 (`record_class_1_only` / `record_class_1_and_2`)
- **cumulative.json 改修・dashboard.html 改修は4本柱完了後の別タスク**
- **フェーズ6 第4段階では柱D サブセクション1 文言改訂のみ即時反映** (`by_record_class` 別軸集計対象との記述追加)

**実装箇所 (即時反映)**:
- 柱D サブセクション1「3区分定義」の cumulative 寄与記述を「区分2 は Track 1 集計対象外、Track 2 では `by_record_class` 別軸集計対象」に改訂
- 柱C サブセクション v3.0 2トラック精度管理整合表を更新 (区分2 の Track 2 寄与を「○ (by_record_class 別軸)」に)

**実装箇所 (別タスク)**: cumulative.json 改修 + dashboard.html 表示拡張

---

### 議題8: 境界曖昧リーグ判断踏襲の有効期限 (単独・即時反映)

**確定方針**: **案B 原則 + シーズン跨ぎ見直し提案 + フォーマット変更時強制再判断**。

- **同一フォーマット継続中** は前回判断を踏襲 (案B 原則)
- **シーズン跨ぎ時** は Claude Code が **見直し提案を1回** 行う
- **大会フォーマット変更時** は **強制再判断** (Claude 自発判断禁止・ユーザー判断必須)

**シーズン跨ぎ判定基準 (種目別)**:

| 種目 | シーズン跨ぎ判定基準 |
|---|---|
| ATP / WTA テニス | ATP/WTA Tour カレンダー (1月〜11月) で年度跨ぎ |
| NHL / NBA / MLB / NFL (北米プロ) | 各リーグのレギュラーシーズン開幕日 |
| サッカー (5大リーグ) | ヨーロッパシーズン (8月〜5月) で年度跨ぎ |
| ラグビー (Premiership / Top14 / Pro D2 / NRL / Super Rugby / Super League) | 各リーグの公式シーズン開幕日 |
| CFL / UFL / AHL | 各リーグのレギュラーシーズン開幕日 |

**実装箇所**: 柱D サブセクション8「境界曖昧リーグ個別判断 SOP」に「踏襲有効期限」サブセクション追加

---

### 議題9: ルール提案レポート (d) シミュレーション計算ロジック (単独・別タスク統合)

**確定方針**: **案B 採用** — 半自動 (Claude 手動計算 + memory ガイドライン化)。

- フェーズ6 第3段階では「案B 採用」を確定
- **memory ガイドライン作成は4本柱完了後の遡及判断タスクと統合実施**
- **フェーズ6 第4段階では agenda.md 記録のみ・実装変更なし**
- ガイドライン記載予定内容:
  - 該当条件試合の抽出方法
  - hit_rate / EV 再計算式
  - 計算根拠の記述義務 (検算可能な形)

**実装箇所 (別タスク)**: `memory/feedback_rule_simulation_guideline.md` 新規作成

---

## 3. 第4段階で実装すべき改修対象ファイル

### 3.1 即時反映 (フェーズ6 第4段階で実施)

| ファイル | 反映議題 | 反映内容概要 |
|---|---|---|
| `CLAUDE.md`【ルール改訂統制プロトコル】(柱A) | 議題1 / 議題6 | evidence 時間的独立性チェック追加 + 名称変更B区分/新リーグ追加対象外 階層化 |
| `CLAUDE.md`【結果反映 STEP 0.5】(柱B) | 議題2 | step05_scanned_at 必須付与規定追記 |
| `CLAUDE.md`【柱C】4-1 | 議題3 | confidence_drift 種目別閾値テーブル追加 + 必須化文言置換 |
| `CLAUDE.md`【柱C】4-3 | 議題4 | タグ付与の粒度ガイドライン サブセクション追加 (但し書き5項目) |
| `CLAUDE.md`【柱D】サブセクション1, 6, 8 | 議題6 / 議題7 / 議題8 | 新リーグ追加 SOP 文言修正 + 区分2 集計記述改訂 + 踏襲有効期限サブセクション追加 |
| `core/rule_pipeline.json` | 議題1 | instructions_for_claude + approval_workflow + forbidden_practices に evidence 時間的独立性 |
| `monitoring/health_check.py` | 議題2 | 13項目目 STEP 0.5 実施確認検査追加 |
| `memory/feedback_no_fabrication.md` | 議題4 | タグ付与の粒度ガイドライン 但し書き5項目補強 |

### 3.2 別タスク統合 (フェーズ6 では agenda.md 記録のみ)

| 議題 | 別タスク内容 | 実施タイミング |
|---|---|---|
| **議題5** | 既存 records 100件超の void:true エントリ → WebSearch 再確認 → match_status 遡及付与 | 4本柱完了後の遡及判断タスク |
| **議題7** | cumulative.json 改修 (`by_record_class` セクション新設) + dashboard.html 表示拡張 | 4本柱完了後の遡及判断タスク |
| **議題9** | `memory/feedback_rule_simulation_guideline.md` 新規作成 | 4本柱完了後の遡及判断タスク |

---

## 4. 第4段階の推奨実装順序

各ステップで commit を分割し、ユーザー承認を待つ。

| 順序 | ステップ | 改修ファイル | 反映議題 |
|---|---|---|---|
| 1 | **柱A 改訂** | `core/rule_pipeline.json` + `CLAUDE.md`【柱A】 | 議題1 (evidence 時間的独立性) + 議題6 (階層化) |
| 2 | **柱B 改訂** | `CLAUDE.md`【柱B】 | 議題2 (step05_scanned_at 規定) |
| 3 | **柱C 4-1 改訂** | `CLAUDE.md`【柱C】4-1 | 議題3 (confidence_drift 種目別閾値) |
| 4 | **柱C 4-3 改訂** | `CLAUDE.md`【柱C】4-3 + `memory/feedback_no_fabrication.md` | 議題4 (粒度ガイドライン) |
| 5 | **柱D 改訂** | `CLAUDE.md`【柱D】サブセクション1, 6, 8 | 議題6 + 議題7 文言改訂 + 議題8 |
| 6 | **health_check.py 13項目目追加** | `monitoring/health_check.py` | 議題2 (機械チェッカー) |
| 7 | **commit + push (柱単位で複数 commit に分割)** | (上記すべて) | (全議題) |

第4段階完了後、第5段階 (フェーズ6 完了報告 + Session_62 全体総括 + 引継ぎサマリ作成) に進む。

---

## 5. 4本柱の確定状態 (フェーズ1-5 完了内容 + フェーズ6 確定議題)

### 5.1 4本柱本体 (フェーズ1-5 完了)

| 柱 | 内容 | 主要実装ファイル |
|---|---|---|
| **柱A** | rule 改訂承認制 (auto_implement DISABLED + approval_workflow 4ステップ + forbidden_practices 3項目) | `core/rule_pipeline.json` + `CLAUDE.md`【ルール改訂統制プロトコル】6サブセクション + `memory/feedback_git_upload.md` 階層化 (A/B/C 区分) |
| **柱B** | 結果反映 STEP 0.5 scope外UPSET スキャン SOP (Claude 推奨区分列含む) | `CLAUDE.md`【結果反映 STEP 0.5】6サブセクション + (A)/(B)/(C) ↔ 区分1/2/3 マッピング明示 |
| **柱C** | 一次ソース fetch 義務化 (4-1 MISS 重要度3段階 + 4-2 fetch 件数規定 + 4-3 5種タグ義務) | `CLAUDE.md`【柱C】4-1/4-2/4-3 + `memory/feedback_miss_analysis_depth.md` + `memory/feedback_no_fabrication.md` + `monitoring/health_check.py` 12項目目 |
| **柱D** | 記録対象判断テーブル (3区分 + match_status enum 5値 + Cup戦細分化 + 境界曖昧リーグ SOP) | `CLAUDE.md`【柱D】9サブセクション |

### 5.2 フェーズ6 第3段階で確定した追加議題 (第4段階で実装反映)

| 柱 | 追加議題 | 反映内容 |
|---|---|---|
| **柱A** | 議題1 (evidence 時間的独立性) + 議題6 (名称変更B区分階層化) | approval_workflow + forbidden_practices 拡張 + サブセクション1 階層化規定 |
| **柱B** | 議題2 (step05_scanned_at + 機械チェッカー) | サブセクション2 step05_scanned_at 規定追記 + health_check 13項目目 |
| **柱C** | 議題3 (confidence_drift 種目別閾値) + 議題4 (粒度ガイドライン) | 4-1 閾値テーブル + 必須化 / 4-3 粒度ガイドライン サブセクション |
| **柱D** | 議題6 (階層化) + 議題7 (by_record_class) + 議題8 (踏襲有効期限) | サブセクション1 文言改訂 + サブセクション6 文言修正 + サブセクション8 踏襲有効期限追加 |

### 5.3 別タスク統合対象 (フェーズ6 では agenda.md 記録のみ)

| 議題 | 別タスク内容 |
|---|---|
| 議題5 | match_status 遡及付与 (既存 void:true エントリ再確認) |
| 議題7 | cumulative.json by_record_class セクション新設 + dashboard.html 表示拡張 |
| 議題9 | memory/feedback_rule_simulation_guideline.md 新規作成 |

---

## 6. Session_62 全体 commit 履歴 (累計 14 commit 予定 / 第3段階完了時点)

| commit | message | フェーズ |
|---|---|---|
| `563d149` | Session_62 phase2 柱A: ルール改訂統制プロトコル新設 | フェーズ2 |
| `5b6378c` | Session_62 phase3 柱B: 結果反映 STEP 0.5 scope外UPSET スキャン SOP 新設 | フェーズ3 |
| `dc69fea` | Session_62 phase1-3 monitoring: 引き継ぎサマリ + フェーズ6 議題リスト | フェーズ1-3 |
| `87a8c81` | Session_62 phase4 stages1-2: 柱C 4-1 MISS 重要度3段階分類 + 4-2 fetch 件数規定 | フェーズ4 ステージ1-2 |
| `74e1b87` | Session_62 phase4 stages1-2 monitoring: 議題3 + stage1to2 引継ぎサマリ | フェーズ4 ステージ1-2 |
| `84cabdd` | Session_62 phase4 stage3: 柱C 4-3 情報源タグ義務化 | フェーズ4 ステージ3 |
| `9e92305` | Session_62 phase4 stage3 monitoring: 議題4 追加 + phase4 完了引継ぎサマリ | フェーズ4 ステージ3 |
| `68c6130` | Session_62 phase5: 柱D 記録対象判断テーブル新設 + 柱B 推奨区分列追加 + health_check 区分フィルタ | フェーズ5 |
| `292db7e` | Session_62 phase5 monitoring: 議題5-8 追加 | フェーズ5 |
| `7fb7396` | Session_62 phase5 complete handoff: フェーズ6 向け引継ぎサマリ新規作成 | フェーズ5 |
| `86db87e` | Session_62 phase6 stage1-2 monitoring: 議題9 追加 | フェーズ6 第1-2段階 |
| `ae4f072` | Session_62 phase6 stage1-2 handoff: フェーズ6 第3段階向け引継ぎサマリ新規作成 | フェーズ6 第1-2段階 |
| **(本commit 1)** | **Session_62 phase6 stage3: 議題1〜9 確定方針 反映** | **フェーズ6 第3段階** |
| **(本commit 2)** | **Session_62 phase6 stage3 handoff: 第4段階 (実装反映) 向け引継ぎサマリ新規作成** | **フェーズ6 第3段階** |

---

## 7. 4本柱完了後の遡及判断タスク予告

### 7.1 凍結維持中の対象 (12件 + 候補 2本 + ルール3件 + 議題3件)

#### Session_61 由来 Modified 8件 (引き続き未 commit)
- `core/dashboard_stats.json`
- `core/rules_tennis.json` (R017 v2.0 + R024 v1.0 追加で v2.5)
- `dashboard.html`
- `records/mlb/2026.json`
- `records/nrl/2026.json`
- `records/soccer/2025-26.json`
- `records/tennis/2026-ATP.json`
- `stats/upset_patterns.json` (A036-A043 追加で 41件)

#### Session_61 由来 Untracked 4件 (引き続き未 commit)
- `monitoring/session_61_handoff.md`
- `scripts/_session61_writeback.py`
- `scripts/_session61_rule_feedback.py`
- `scripts/_session61_phase2_upsets.py`

#### ready_to_implement 候補 2本
- P020 → R014 (NRL): R1-R8 + PD差6pt以上 + desperate team → 信頼度上限78% + 追加-5%
- P024 → N_NBA_new2 (NBA): star scorer (>25ppg RS) OFF/ON で L4 -8〜+8% (return cycle 双方向)

#### 遡及判断対象ルール 3件
- **R017 v2.0** (home strict-define): evidence 1件改訂 → 取り消し / 承認 / 修正後再構築判断
- **R024 v1.0** (form slump): evidence 3件は満たすが同 turn 内 implement・反例検証なし → 取り消し / 承認 / 修正後再構築判断
- **P030 ID 衝突解消**: proposed_rule_id "R024" → "R025" 等への再付番判断

#### フェーズ6 確定議題のうち別タスク統合 3件 (新規)
- **議題5**: match_status 遡及付与 (既存 records 100件超の void:true エントリ → WebSearch 再確認)
- **議題7**: cumulative.json `by_record_class` セクション新設 + dashboard.html 表示拡張
- **議題9**: `memory/feedback_rule_simulation_guideline.md` 新規作成

### 7.2 Session_61 9件振り分け実施 (柱D サブセクション9 のテーブル参照)

| # | 試合 | 推奨区分 | match_status |
|---|---|---|---|
| 1 | Bristol 52-19 Newcastle Premiership | 区分1 (full_record) | completed |
| 2 | Northampton 41-38 Bath Premiership | 区分1 (full_record) | completed (date 訂正のみ 4/26→4/25) |
| 3 | Swiatek retire vs Li Madrid R3 | 区分2 (reference_only) | retired |
| 4 | Bondar d. Svitolina (#7 seed) Madrid R2 | 区分1 (full_record) | completed |
| 5 | PHI G4 vs PIT (NHL Playoffs) | 区分1 (full_record) | completed |
| 6 | TOR 93-89 CLE G4 (NBA Playoffs) | 区分1 (full_record) | completed |
| 7 | HOU 115-96 LAL G4 (NBA Playoffs) | 区分1 (full_record) | completed |
| 8 | Baptiste d. Paolini Madrid R3 | 区分1 (full_record) | completed |
| 9 | Pliskova(Q) d. Mertens(#19) Madrid R3 | 区分1 (full_record) | completed |

### 7.3 既存 pending (前セッションから持越し)
- PA092: UCL SF Atletico-Arsenal (4/30) / PSG-Bayern (4/29) STEP 4.5 lineups 確認
- PA103: GEN007 UPSET_PICK_Lite 採否判断 (Phase2 移行後 9日経過、発動 0件)
- PA099: NBA G3/G4 残 (ORL-DET / PHX-OKC / MIN-DEN G4)
- フィード再取得: lineups (健全性 WARN)
- BACKLOG.md Session_60 残: dashboard 成長分析タブ AUTO ブロック実装、cumulative_history.json 連動

---

## 8. 新セッションでの再開手順

### 8.1 新セッション開始時の必須読込

1. CLAUDE.md (柱A + 柱B + 柱C 4-1+4-2+4-3 + 柱D を含む最新版)
2. **本ファイル (`monitoring/session_62_phase6_stage3_handoff.md`)** ← 最初に読む
3. `monitoring/session_62_phase6_stage1to2_handoff.md` (フェーズ6 第1-2段階完了サマリ)
4. `monitoring/session_62_phase5_complete_handoff.md` (フェーズ5 完了サマリ)
5. `monitoring/session62_phase6_agenda.md` (議題1〜9 全件確定方針)
6. `monitoring/session_61_handoff.md` (Session_61 運用品質診断 v2)
7. STEP 0 (health_check) 実行 — 12項目目 `miss_analysis_tag_compliance` 動作確認 (13項目目は本セッションで追加予定)
8. STEP 1 必須ファイル群 (BACKLOG.md / user_feedback_log.md / pending_actions.md / claude_error_log.md / rule_pipeline.json / framework.json)

### 8.2 新セッション最初のタスク

**フェーズ6 第4段階 (CLAUDE.md / health_check.py / memory への実装反映) 着手から再開する**。具体的順序:

1. 第4段階着手前に、確定議題1〜9 のうち即時反映対象 (議題1/2/3/4/6/8 + 議題7 文言のみ) と別タスク統合対象 (議題5/7/9) の境界をユーザーと再確認
2. 推奨実装順序 §4 に従い、柱単位で改修を実施
3. 各柱の改修ごとに commit + push し、ユーザー承認を得てから次の柱に進む
4. 第4段階完了後、第5段階 (フェーズ6 完了報告 + Session_62 全体総括 + 引継ぎサマリ作成) 着手
5. 第5段階完了 → **4本柱 実装作業 完了**
6. (別タスク) A-3 遡及判断・Session_61 ペンディング事項・Session_61 9件振り分け実施・議題5/7/9 統合実施 着手

### 8.3 新セッション着手時の禁止事項 (再掲)

- rules_*.json / records / upset_patterns.json への書き込み禁止 (第4段階はメタルール側の改修のみ)
- core/framework.json は本フェーズで一切触らない
- Session_61 ペンディング事項 12件 + ready_to_implement 候補 P020/P024 は 4本柱完了まで凍結継続
- 議題5 / 議題7 / 議題9 の実装は4本柱完了後の遡及判断タスクと統合実施
- 「ついでにこれもやっておきました」は禁止
- 第4段階で CLAUDE.md / memory への追記は柱A ルール改訂統制プロトコルに従いユーザー承認必須
- 不明点があれば実装を止めて質問

---

**Session_62 フェーズ6 第3段階 終了**: 2026-04-28
**新セッション最優先**: フェーズ6 第4段階 (CLAUDE.md / health_check.py / memory への実装反映) 着手 → 推奨実装順序に従い柱単位で改修 → 第5段階 完了報告 → **4本柱 実装作業 完了**
