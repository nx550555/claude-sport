# A-3 サブタスク1+2 完了 引継ぎサマリ — サブタスク3 着手向け

> **新セッション読込必須**: 本ファイルは A-3 遡及判断タスク (Session_62 完了後の負債清算タスク) の **サブタスク1 (R017 v2.0 / R024 v1.0 取り消し) + サブタスク2 (P030 ID 衝突解消)** 完了をもって、次セッションでサブタスク3 (Session_61 9件振り分け実施) に着手するための引継ぎサマリ。新セッションでは本ファイルを最初に読み込んだ後、サブタスク3 から作業を継続する。

---

## 1. A-3 タスク全体構造 (9サブタスク中 2件完了 / 7件残)

A-3 遡及判断タスクは Session_61 で凍結された負債を 4本柱 (Session_62 で完了) に基づいて清算するタスク群。9つのサブタスクで構成される。

| # | サブタスク | ステータス | 完了日 / commit |
|---|---|---|---|
| **1** | **R017 v2.0 / R024 v1.0 取り消し / 承認 / 修正後再構築判断** | ✅ **完了 (取り消し承認)** | 2026-04-28 / `6f0d877` |
| **2** | **R024 → R025 ID再付番 (P030 ID衝突解消)** | ✅ **完了 (P30-β 採用)** | 2026-04-28 / `6f0d877` (サブタスク1 と同一 commit) |
| 3 | **Session_61 9件振り分け実施** (柱D サブセクション9 テーブル) | 🔵 次サブタスク (新セッション着手予定) | — |
| 4 | Modified 8件の整合性確保 + commit (rules_tennis.json は処理済 → 残 7件) | 🔵 凍結維持 | — |
| 5 | Untracked 4件のアーカイブ / 削除判断 (Session_61 ハンドオフ + 使い捨てスクリプト 3本) | 🔵 凍結維持 | — |
| 6 | ready_to_implement 候補 P020 / P024 の柱A 承認制プロセス適用 | 🔵 凍結維持 | — |
| 7 | 議題5 統合: match_status 遡及付与 (既存 records 100件超 → WebSearch 再確認) | 🔵 凍結維持 | — |
| 8 | 議題7 統合: cumulative.json `by_record_class` + dashboard.html 改修 | 🔵 凍結維持 | — |
| 9 | 議題9 統合: memory/feedback_rule_simulation_guideline.md 新規作成 | 🔵 凍結維持 | — |

各サブタスクごとにユーザー承認を得てから次に進む方針 (同一セッション内で全件完了は想定せず、複数セッションに分割実施)。

---

## 2. サブタスク1+2 の確定方針と実装結果

### 2.1 サブタスク1: R017 v2.0 / R024 v1.0 取り消し

**確定方針**: 取り消し承認 (案A 採用)

| 対象 | 取り消し理由 (柱A 違反内容) | 実装内容 |
|---|---|---|
| **R017 v2.0** (home strict-define) | evidence 1件 (A037 Vacherot Madrid R2 MISS) のみで v1.0 → v2.0 改訂。柱A §4「evidence 1件のみでの即改訂禁止 / 反例検証必須」違反。柱A §5「ユーザー確認なしの既存ルール v_X.0 → v_Y.0 改訂禁止」違反 | rules_tennis.json から v2.0 改訂を巻き戻し、v1.0 (2026-04-20 implemented) に復帰。home要件 strict-define 関連の title / body / evidence / application / version_history を完全削除 |
| **R024 v1.0** (form slump 補正 -10%) | 同一 turn 内 evidence 3/3 (A041 Baptiste-Paolini) → implement (柱A 議題1「同一 turn 内 evidence 3件目検出 → implement の禁止」違反)。evidence 3件中 2件 (U007_R2 / A041) が同一選手 Paolini で独立性疑義。反例検証なし | rules_tennis.json から R024 エントリ全体を削除。rule_pipeline.json の `implemented_rules` から P007 エントリ削除。candidates 側の P007 は `status: "ready_to_implement"` のまま維持 (Session_61 implement 直前状態) |

### 2.2 サブタスク2: P030 ID 衝突解消

**確定方針**: P30-β 採用 (proposed_rule_id を R024 → R025 に変更)

- **背景**: R024 削除に伴い ID 再利用 (P30-α) は混乱を招くため、新規 ID として P030 の proposed_rule_id を **R025** に変更
- **実装**: rule_pipeline.json 内 P030 エントリの `proposed_rule_id` フィールド値を `"R024"` → `"R025"` に変更
- **その他フィールド維持**: P030 の status (`watching`) / current_count (1) / trigger_threshold (3) / evidence (1件) / title (Madrid altitude (1500m) + Masters interB2B 重複ペナルティ) はすべて無変更

### 2.3 実装結果サマリ

| 変更ファイル | 変更内容 |
|---|---|
| `core/rules_tennis.json` | v2.5 → v2.3 巻き戻し (Session_61 未 commit 改訂のロールバック / git history 上には差分なし、commit message で記録) |
| `core/rule_pipeline.json` | implemented_rules から P007 (R024 form slump) エントリ削除 + P030 proposed_rule_id を R024→R025 に変更 (1 file changed, 1 insertion(+), 11 deletions(-)) |

### 2.4 柱A approval_workflow の A-3 初運用実演

A-3 サブタスク1+2 は柱A 承認制プロトコルの **A-3 タスク初運用として完全実演**された:

1. **取り消し提案レポート (a)〜(e) 生成** (柱A §3 step2_proposal_report 必須項目に従う)
   - (a) 候補ID と提案タイトル
   - (b) 既存ルールへの影響範囲 (関連 R*** ID + 適用対象試合数概算)
   - (c) 取り消し根拠 (柱A §4/§5 違反箇所の引用 + 議題1 確定方針との対比 + evidence の質問題)
   - (d) cumulative.json への影響シミュレーション (議題9 案B 半自動)
   - (e) 取り消し却下時の代替案 (案B 承認・事後追認 / 案C 修正後再構築)
2. **ユーザー判断**: R017 取り消し承認 / R024 取り消し承認 / P030 P30-β 採用
3. **実装**: 3ステップ (rules_tennis.json 巻き戻し → rule_pipeline.json 整理 → commit + push) で順次実施、各ステップ完了時にユーザー承認を待機

### 2.5 議題9 案B (半自動シミュレーション) の実演結果

| 対象 | cumulative 影響 | 算出根拠 |
|---|---|---|
| **R017 v2.0 取り消し** | **0件 / 0u** | v2.0 改訂後の新規予測未発生のため、取り消し時点で hit_rate / EV に変動なし |
| **R024 v1.0 取り消し** | **1件 / -1.0u 相当** | A041 Paolini Madrid R3 のみが R024 適用済 (SKIP downgrade)。取り消し後は補正なしで conf 76% → GO相当に再評価。Baptiste 勝利 = Paolini MISS のため、GO 推奨で MISS する仮想計算となり -1.0u 相当の悪化 |

### 2.6 維持された記録

- A037 evidence は `stats/upset_patterns.json` に維持
- A001 / A007 / A041 evidence は upset_patterns.json + rule_pipeline.json (P007 candidates 側) に維持
- records/tennis の miss_analysis テキストはすべて維持 (予測時点の正当性尊重)
- P007 candidates の current_count (3) / trigger_threshold (3) / evidence 配列 (U007 / U007_R2 / A041) は維持

---

## 3. サブタスク3 (Session_61 9件振り分け実施) の詳細

### 3.1 9件の試合データ + 推奨区分 + 登録先 (柱D サブセクション9 テーブル参照)

| # | 試合 | 推奨区分 | match_status | 登録先 | 備考 |
|---|---|---|---|---|---|
| 1 | Bristol 52-19 Newcastle Premiership | **区分1 (full_record)** | completed | `records/premiership/2026.json` (新規エントリ追加) | scope内大会 / regular round / 試合成立 / 市場fav 敗戦 (UPSET) |
| 2 | Northampton 41-38 Bath Premiership | **区分1 (full_record)** | completed | `records/premiership/2026.json` (既存エントリの date 訂正 4/26→4/25) | scope内 / 既 records 登録 |
| 3 | Swiatek retire vs Li Madrid R3 | **区分2 (reference_only)** | retired | `stats/upset_patterns.json` のみ (records 本体には未登録) | Swiatek (#1 シード) retire は UPSET 性質あり |
| 4 | Bondar d. Svitolina (#7 seed) Madrid R2 | **区分1 (full_record)** | completed | `records/wta/2026.json` (新規エントリ追加) | scope内 (WTA Masters 相当) / R2 / #7 seed 敗退 (UPSET) |
| 5 | PHI G4 vs PIT (NHL Playoffs) | **区分1 (full_record)** | completed | `records/nhl/2025-26.json` (新規エントリ追加) | scope内 / Playoffs / 試合成立 |
| 6 | TOR 93-89 CLE G4 (NBA Playoffs) | **区分1 (full_record)** | completed | `records/nba/2025-26.json` (新規エントリ追加) | scope内 / Playoffs / 市場fav CLE 敗戦 (UPSET) |
| 7 | HOU 115-96 LAL G4 (NBA Playoffs) | **区分1 (full_record)** | completed | `records/nba/2025-26.json` (新規エントリ追加) | scope内 / Playoffs / 市場fav LAL 敗戦 (UPSET) |
| 8 | Baptiste d. Paolini Madrid R3 | **区分1 (full_record)** | completed | `records/wta/2026.json` (新規エントリ追加) | scope内 (WTA Masters) / R3 / Paolini fav 敗戦 (UPSET) |
| 9 | Pliskova(Q) d. Mertens(#19) Madrid R3 | **区分1 (full_record)** | completed | `records/wta/2026.json` (新規エントリ追加) | scope内 / R3 / Mertens (#19) 敗戦 (UPSET) |

### 3.2 区分別件数

| 区分 | 件数 |
|---|---|
| 区分1 (full_record) | **8件** (#1, 2, 4, 5, 6, 7, 8, 9) |
| 区分2 (reference_only) | **1件** (#3 Swiatek retire) |
| 区分3 (skip_record) | 0件 |

### 3.3 各エントリへの必須付与フィールド

#### 区分1 (full_record) 8件への必須付与
- `record_class: "full_record"` (柱D サブセクション3 規定)
- `match_status: "completed"` (柱D サブセクション2 規定)
- `step05_scanned_at: "<ISO 8601 UTC タイムスタンプ>"` (柱B サブセクション2 ステップ7 規定 / prediction_hit 確定時に同時付与)
- `prediction_hit: <true|false>` (実結果に基づき判定)
- **prediction_hit=false の場合は追加で**:
  - `miss_class: "<A|B|C>"` (柱C 4-1 規定)
  - `miss_analysis` テキストに 5種タグ ([FETCH:URL] / [FETCHER:src] / [SEARCH] / [MEMORY] / [INFER]) 必須付与 (柱C 4-3 規定)
  - 4-2 fetch 件数規定 (Class A=3 / B=2 / C=1) 遵守

#### 区分2 (reference_only) 1件 (Swiatek retire) への必須付与
- `record_class: "reference_only"` (柱D サブセクション3 規定)
- `match_status: "retired"` (柱D サブセクション2 規定)
- upset_patterns.json への参考登録のみ (records 本体には登録しない)
- miss_class 付与は任意 (柱C 4-1 規定 / UPSET 性質追跡用に "C" 付与可)
- タグ義務は適用 (簡略可) (柱D サブセクション7 整合性表より)

### 3.4 サブタスク3 着手時の作業フロー

1. 各試合の結果情報を WebSearch / WebFetch で一次確認 (柱C 4-2 fetch 件数規定遵守)
2. 各試合の prediction_hit を判定 (8件は prediction_hit=false が多数想定)
3. 各 records ファイルに新規エントリを追加 (フィールド構造は既存エントリに準拠)
4. 各エントリに必須付与フィールド (record_class / match_status / step05_scanned_at / miss_class / 5種タグ) を同時付与
5. miss_analysis テキストの一次ソース fetch (Class A / B / C 別件数遵守)
6. 区分2 (Swiatek) は upset_patterns.json のみへの登録
7. health_check.py 13項目目 (`step05_scan_compliance`) と 12項目目 (`miss_analysis_tag_compliance`) の通過確認
8. cumulative.json への反映は **本サブタスクでは実施しない** (議題7 統合 = サブタスク8 で別途実施)
9. dashboard.html / dashboard_stats.json 同期も **本サブタスクでは凍結維持** (サブタスク4 / 8 で実施)

### 3.5 重要な注意事項

- **タグ付与必須化**: フェーズ4 ステージ3 承認日 (2026-04-27) 以降の新規 miss_analysis のため、本サブタスク3 で追加するエントリは **必ず 5種タグ義務を適用する**
- **step05_scanned_at 必須化**: フェーズ6 第3段階確定日 (2026-04-28) 以降の新規 prediction_hit 確定エントリのため、本サブタスク3 で追加するエントリは **必ず付与する**
- **記憶ベース推論禁止**: Madrid altitude (1500m) のような記憶ベース主張は `[MEMORY]` タグでのみ記述可。evidence 化禁止 (柱C 4-3 規定)
- **fetch 失敗時の対処**: 3回試行で規定件数未達なら `[FETCH_FAILED:URL1,URL2,URL3]` + `investigation_status: "investigation_incomplete"` 付与 (柱C 4-2 規定)

---

## 4. サブタスク4〜9 の概要 (4本柱完了後のタスク継続)

### サブタスク4: Modified 7件の整合性確保 + commit
- 残存 Modified 7件: dashboard_stats.json / dashboard.html / records (mlb / nrl / soccer / tennis-ATP) / upset_patterns.json
- サブタスク3 (Session_61 9件振り分け) の結果反映として dashboard / cumulative 含む整合性確保 + 一括 commit
- サブタスク3 完了後に着手

### サブタスク5: Untracked 4件のアーカイブ / 削除判断
- 対象: monitoring/session_61_handoff.md + scripts/_session61_phase2_upsets.py / _session61_rule_feedback.py / _session61_writeback.py
- A-3 完了後にアーカイブまたは削除判断 (使い捨てスクリプトの保存 vs 削除)

### サブタスク6: ready_to_implement 候補 P020 / P024 の柱A 承認制プロセス適用
- P020 → R014 (NRL): R1-R8 + PD差6pt以上 + desperate team → 信頼度上限78% + 追加-5%。evidence 3/3 (U005 + A008 + A039 Manly MISS Session_61)
- P024 → N_NBA_new2 (NBA): star scorer (>25ppg RS) OFF/ON で L4 -8〜+8% (return cycle 双方向)。evidence 3/3 (A029 KD G1 + A031 Wemby G2 + A043 KD return G4 Session_61)
- 柱A approval_workflow に従い実装提案レポート生成 → ユーザー判断
- 議題1 確定方針 (異セッション独立検出 + proposal は次セッション以降) を遵守

### サブタスク7: 議題5 統合 (match_status 遡及付与)
- 既存 records 100件超の `void: true` エントリを WebSearch で再確認
- `match_status` を `retired` / `walkover` / `cancelled` / `postponed` のいずれかに判定
- 既存 `void: true` フィールドは後方互換用として維持
- 実装手順: `scripts/_retroactive_match_status.py` 等の使い捨てスクリプト想定

### サブタスク8: 議題7 統合 (cumulative.json / dashboard.html 改修)
- `stats/cumulative.json` に `by_record_class` セクション新設:
  - `record_class_1_only`: 区分1 のみの hit_rate / EV / sport別 / quadrant別
  - `record_class_1_and_2`: 区分1+2 合算の hit_rate / EV / sport別 / quadrant別
- `dashboard.html` で Track 2 の二軸表示を実装 (区分1 のみ + 区分1+2 並列表示)
- `cumulative_history.json` 連動も同タスクで実施 (Session_60 残タスク)

### サブタスク9: 議題9 統合 (memory ガイドライン作成)
- 柱A サブセクション3 必須項目 (d) (シミュレーション計算ロジック) の半自動運用ガイドライン
- 記載内容: 該当条件試合の抽出方法 / hit_rate / EV 再計算式 / 計算根拠の記述義務
- 4本柱完了後の柱A 運用初動段階で具体化 (A-3 サブタスク1+2 が初運用 → ガイドライン記述に反映可)

---

## 5. 凍結対象 11件の現状 (Modified 7 + Untracked 4)

### Modified 7件 (引き続き未 commit 維持)

| ファイル | 内容 | 処理予定サブタスク |
|---|---|---|
| `core/dashboard_stats.json` | Session_61 で更新分 | サブタスク4 (整合性確保 commit) |
| `dashboard.html` | Session_61 で更新分 | サブタスク4 / サブタスク8 |
| `records/mlb/2026.json` | Session_61 で更新分 | サブタスク4 |
| `records/nrl/2026.json` | Session_61 で更新分 (A039 Manly MISS 記録含む) | サブタスク4 / サブタスク6 (P020 関連) |
| `records/soccer/2025-26.json` | Session_61 で更新分 | サブタスク4 |
| `records/tennis/2026-ATP.json` | Session_61 で更新分 (A037 Vacherot Madrid R2 MISS / A038 Shapovalov 等) | サブタスク3 / サブタスク4 |
| `stats/upset_patterns.json` | A036-A043 追加で 41件 (Swiatek retire = サブタスク3 の区分2 登録予定) | サブタスク3 / サブタスク4 |

### Untracked 4件 (引き続き未 commit 維持)

| ファイル | 処理予定サブタスク |
|---|---|
| `monitoring/session_61_handoff.md` | サブタスク5 (アーカイブ / 削除判断) |
| `scripts/_session61_phase2_upsets.py` | サブタスク5 |
| `scripts/_session61_rule_feedback.py` | サブタスク5 |
| `scripts/_session61_writeback.py` | サブタスク5 |

---

## 6. 新セッション再開手順

### 6.1 新セッション開始時の必須読込

1. **CLAUDE.md** (柱A + 柱B + 柱C 4-1+4-2+4-3 + 柱D 含む最新版)
2. **本ファイル (`monitoring/a3_subtask1to2_handoff.md`)** ← 最初に読む (A-3 サブタスク1+2 完了状態 + サブタスク3 詳細)
3. `monitoring/session_62_complete_handoff.md` (Session_62 全体総括 + 4本柱最終確定状態)
4. `monitoring/session_61_handoff.md` (Session_61 運用品質診断 v2 + Session_61 由来 12件詳細)
5. `monitoring/session62_phase6_agenda.md` (議題1〜9 全件確定方針 + 第4段階完了サマリ)
6. STEP 0 (`PYTHONIOENCODING=utf-8 python monitoring/health_check.py`) 実行 — 13項目 OK + WARN 既存 + ALERT 0件確認
7. STEP 1 必須ファイル群 (BACKLOG.md / user_feedback_log.md / pending_actions.md / claude_error_log.md / rule_pipeline.json / framework.json)

### 6.2 新セッション最初のタスク (A-3 サブタスク3 着手)

サブタスク3 (Session_61 9件振り分け実施) を以下の流れで進める:

1. **準備フェーズ**: 9件の試合データを記憶 (本ファイル §3.1) と照合し、各試合の一次ソース URL を整理
2. **段階1: 区分2 (Swiatek retire) の登録**: 1件のみのため最初に処理 (upset_patterns.json への参考登録 / record_class: reference_only / match_status: retired)
3. **段階2: 区分1 (full_record) 8件の登録**:
   - 段階2-1: テニス (4件: Bondar / Baptiste / Pliskova / Northampton 41-38 Bath は Premiership) → records/wta/2026.json + records/premiership/2026.json
     - 注: Northampton-Bath は既存エントリの date 訂正 (4/26→4/25)。残3件のテニスは新規追加
   - 段階2-2: ラグビー (1件: Bristol-Newcastle) → records/premiership/2026.json (新規)
   - 段階2-3: NHL (1件: PHI G4 vs PIT) → records/nhl/2025-26.json (新規)
   - 段階2-4: NBA (2件: TOR-CLE G4 / HOU-LAL G4) → records/nba/2025-26.json (新規)
4. **段階3: 各エントリへの必須付与フィールド検証**: record_class / match_status / step05_scanned_at / miss_class / 5種タグ
5. **段階4: health_check.py 通過確認**: 13項目目 (step05_scan_compliance) + 12項目目 (miss_analysis_tag_compliance)
6. **段階5: commit + push**: サブタスク3 完了として 1 commit にまとめる
   - 注: dashboard / cumulative への反映はサブタスク4 / 8 で別途実施

### 6.3 新セッション着手時の禁止事項 (再掲)

- 4本柱本体 (柱A / 柱B / 柱C / 柱D) の規定本体への変更禁止 (改訂が必要なら柱A 承認制プロトコル適用)
- `core/framework.json` は触らない (凍結維持継続)
- `core/rules_tennis.json` (取り消し済) / `core/dashboard_stats.json` / records (サブタスク3 対象 4件以外) / stats / cumulative.json / dashboard.html への書き込み禁止 (サブタスク3 範囲外)
- 「ついでにこれもやっておきました」は禁止 (柱A 規律継続)
- 不明点があれば実装を止めて質問

---

## 7. A-3 累計 commit 履歴

| # | commit ID | message | サブタスク |
|---|---|---|---|
| 1 | `6f0d877` | A-3 sub1+sub2: R017 v2.0 / R024 v1.0 取り消し + P030 ID 変更 | サブタスク1 + サブタスク2 |
| 2 | (本commit) | A-3 sub1to2 handoff: サブタスク3 (Session_61 9件振り分け実施) 向け引継ぎサマリ新規作成 | handoff |

A-3 タスク開始からの累計 commit 数: **2件** (うち実装 1件 + handoff 1件)

---

## 8. A-3 サブタスク1+2 完了の総括

### 8.1 達成事項

- **柱A 承認制プロトコルの A-3 タスク初運用成功**: 取り消し提案レポート (a)〜(e) 生成 → ユーザー承認 → 3ステップ実装 → ユーザー承認 → 完了 の全プロセスが想定通り機能
- **議題9 案B (半自動シミュレーション) の初実演**: cumulative 影響を手動計算 + 計算根拠の段階記述で算出 (R017 影響 0 / R024 影響 -1.0u)
- **R024 削除に伴う ID 衝突解消**: P30-β 採用で P030 proposed_rule_id を R025 に変更 → 将来の Madrid altitude 候補実装時の ID 混乱を予防
- **逸脱ルール 2件の取り消し完了**: R017 v2.0 (1件 evidence 改訂) + R024 v1.0 (同一 turn 内 implement) を両方とも取り消し、Session_61 の品質劣化を清算

### 8.2 4本柱の運用初動成果

| 柱 | A-3 サブタスク1+2 での適用例 |
|---|---|
| **柱A** (rule 改訂承認制) | A-3 サブタスク1+2 全体が柱A approval_workflow の実演。提案レポート (a)〜(e) + ユーザー承認 + 段階的実装の流れが正常に機能 |
| **柱B** (STEP 0.5 SOP) | サブタスク3 で適用予定 (本サブタスクでは結果反映なし) |
| **柱C** (一次ソース fetch 義務化) | サブタスク3 で 5種タグ + 4-2 fetch 件数規定 (Class A=3 / B=2 / C=1) を適用予定 |
| **柱D** (記録対象判断) | サブタスク3 で record_class + match_status 必須付与を適用予定。本サブタスク1+2 では P30-β 採用で柱D サブセクション9 テーブルとの整合確保 |

### 8.3 残課題と継続性

- **凍結対象 11件**: サブタスク3〜5 で順次解消予定 (rules_tennis.json は処理済 → 12件 → 11件)
- **議題5 / 議題7 cumulative 改修部分 / 議題9** の3件: サブタスク7 / 8 / 9 で別タスク統合実施
- **柱A 運用継続**: P020 / P024 の承認制プロセスはサブタスク6 で実演

A-3 サブタスク1+2 完了をもって、Session_62 で構築した 4本柱 (特に柱A 承認制プロトコル + 議題9 半自動シミュレーション) が **A-3 タスク初運用として完全に機能した** ことが実証された。新セッションでサブタスク3 から着手し、Session_61 の負債清算を継続する。

---

**A-3 サブタスク1+2 終了**: 2026-04-28
**サブタスク3 着手予定**: 新セッション開始時

新セッション最優先: **A-3 サブタスク3 (Session_61 9件振り分け実施) 着手** → 区分2 Swiatek retire 1件 + 区分1 8件を順次処理 → 各 records ファイルへの登録 + 必須付与フィールド (record_class / match_status / step05_scanned_at / miss_class / 5種タグ) → health_check 通過確認 → commit + push
