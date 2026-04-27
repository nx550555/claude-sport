# Session_62 フェーズ4 完了 引き継ぎサマリ

> **新セッション読込必須**: このファイルは Session_62 (2026-04-27) のフェーズ4 全体 (ステージ1-3) 完了時点のスナップショット。新セッションでは **フェーズ5 (柱D 記録対象判断テーブル明文化)** から再開する。

---

## 1. Session_62 全体構造の現在地

| フェーズ | 内容 | 実施状況 |
|---|---|---|
| フェーズ1 | 改修対象ファイルの現状把握 | ✅ 完了・ユーザー承認済 |
| フェーズ2 | 柱A: ルール自動実装の停止 → 承認制 | ✅ 完了・ユーザー承認済 |
| フェーズ3 | 柱B: scope外 UPSET スキャン SOP 化 | ✅ 完了・ユーザー承認済 |
| フェーズ4 ステージ1 | 柱C 4-1 MISS 重要度3段階分類 | ✅ 完了・ユーザー承認済 |
| フェーズ4 ステージ2 | 柱C 4-2 fetch 件数規定 (+ confidence_drift 2値化ミニタスク) | ✅ 完了・ユーザー承認済 |
| **フェーズ4 ステージ3** | **柱C 4-3 情報源タグ義務化 (5種タグ)** | ✅ **完了・ユーザー承認済** |
| フェーズ5 | 柱D: 記録対象判断テーブル明文化 | 🔴 **新セッションで実施** |
| フェーズ6 | 統合動作確認 (シミュレーション) | 🔴 新セッションで実施 |
| (4本柱完了後別タスク) | A-3 遡及判断 + Session_61 ペンディング事項 | 🔴 4本柱 全フェーズ完了後 |

**重要原則 (Session_62 全期間共通)**:
1. 各フェーズ/ステージ完了時にユーザー承認を待つ
2. 既存の rules_*.json / records / upset_patterns.json への書き込みは本作業中は実施しない (メタルール側の改修のみ)
3. 不明点があれば実装を止めて質問
4. 「ついでにこれもやっておきました」は禁止
5. Session_61 ペンディング事項 (未反映 9試合 / R024→R025 再付番 / ready_to_implement P020/P024) は **4本柱 全フェーズ完了まで一切手を付けない**

---

## 2. フェーズ4 全体 (ステージ1-3) 総括

### 2.1 ステージ別実装内容

| ステージ | サブタスク | 実装内容 |
|---|---|---|
| ステージ1 | 4-1 MISS 重要度3段階分類 | Class A/B/C 判定条件 + confidence_drift 枠組み + miss_class フィールド付与ルール + v3.0 整合性 |
| ステージ1 後 ミニタスク | confidence_drift 2値化 | `"high" \| null` 構造 (`"low"` 不採用、フェーズ6 / 別タスクで再設計) |
| ステージ2 | 4-2 fetch 件数規定 | Class 別 WebFetch 必須件数 (A=3 / B=2 / C=1) + ソース内訳必須要件 + WebSearch スニペット原則 (カウント対象外) + fetcher 経由カウント条件 + fetch 失敗時 3回試行 + `[FETCH_FAILED]` フラグ + investigation_incomplete のまま evidence 加算禁止 + 一次ソース推奨リスト 16種目分 |
| ステージ3 | 4-3 情報源タグ義務化 | 5種タグ正式定義 + 主張ごと付与 + タグなし禁止 + 良い例/悪い例 (Session_61 A038 Shapovalov 引用) + `[FETCH_FAILED]` 詳細仕様 + `[FETCHER:src:proxy]` 仕様 + `[INFER]` ネスト記法不採用 + 遡及範囲新規のみ + CHECK-2 連携 + health_check 連携 (新項目) + セッション固有スクリプト生成時タグ義務 |

### 2.2 フェーズ4 全体で改修した8ファイル (累積)

| ファイル | ステージ1 | ステージ2 | ステージ3 |
|---|---|---|---|
| `CLAUDE.md` | 【柱C】新設 + 4-1 実装 | 4-2 実装 | 4-3 実装 |
| `memory/feedback_miss_analysis_depth.md` | 4-1 セクション追記 | 4-2 セクション追記 | (変更なし) |
| `memory/feedback_no_fabrication.md` | (変更なし) | (変更なし) | 4-3 セクション追記 |
| `memory/feedback_result_verification.md` | (変更なし) | (変更なし) | 整合性確認のみ・変更不要 |
| `monitoring/health_check.py` | (変更なし) | (変更なし) | 12項目目 `miss_analysis_tag_compliance` 追加 |
| `core/rule_pipeline.json` | (変更なし) | (変更なし) | `instructions_for_claude` 1項目追加 |
| `MEMORY.md` (memory index) | description 更新 | description 再更新 | description 再々更新 (`feedback_no_fabrication` エントリ) |
| `monitoring/session62_phase6_agenda.md` | 議題3 追加 (confidence_drift 種目別閾値) | (変更なし) | 議題4 追加 (タグ付与の粒度ガイドライン) |
| `monitoring/session_62_stage1to2_handoff.md` | (新規作成) | (新規作成・更新) | (本完了サマリで実質完了) |

### 2.3 git commit 構成 (フェーズ4 累積)

| commit | message | 含むファイル |
|---|---|---|
| `87a8c81` | Session_62 phase4 stages1-2: 柱C 4-1 + 4-2 | CLAUDE.md |
| `74e1b87` | Session_62 phase4 stages1-2 monitoring | session62_phase6_agenda.md (議題3) + session_62_stage1to2_handoff.md |
| (本セッション 1) | Session_62 phase4 stage3: 柱C 4-3 情報源タグ義務化 | CLAUDE.md / core/rule_pipeline.json / monitoring/health_check.py |
| (本セッション 2) | Session_62 phase4 stage3 monitoring: 議題4 追加 + phase4 完了引継ぎサマリ | monitoring/session62_phase6_agenda.md / monitoring/session_62_phase4_complete_handoff.md |

memory ファイル (`feedback_miss_analysis_depth.md` / `feedback_no_fabrication.md` / `MEMORY.md`) は Claude Code 内部の git 管轄外のため、リポジトリ commit には含まれない。

---

## 3. フェーズ4 13論点 全件確定済の確認

### サブタスク 4-1: MISS 重要度3段階分類

| # | 論点 | 確定 |
|---|---|---|
| Q1 | 重要度分類段階数 | ✅ **3段階 (Class A / B / C)** |
| Q2 | confidence_drift フラグ導入是非 | ✅ **導入** (枠組みのみ。種目別閾値は議題3 でフェーズ6 確定) |
| Q3 | confidence_drift の薄勝ち閾値 (種目別) | 🟡 **TBD: フェーズ6 で確定** (議題3 として記録) |
| Q4 | scope外UPSET の Class 帰属 | ✅ **Class C 内包** |

### サブタスク 4-2: fetch 件数規定

| # | 論点 | 確定 |
|---|---|---|
| Q1 | 規定方式 | ✅ **件数+種別 (両方規定)** |
| Q2 | Class 別件数 | ✅ **A=3 / B=2 / C=1** |
| Q3 | 失敗時運用 | ✅ **3回試行 + [FETCH_FAILED] フラグ** |
| Q4 | fetcher 経由カウント | ✅ **WebFetch 1件相当 + [FETCHER:src] / [FETCHER:src:proxy] 別タグ扱い** |
| Q5 | investigation_incomplete のまま evidence 加算 | ✅ **禁止** (柱A 整合) |

### サブタスク 4-3: 情報源タグ義務化

| # | 論点 | 確定 |
|---|---|---|
| Q1 | タグ仕様 | ✅ **5種 ([FETCH:URL] / [FETCHER:src] / [SEARCH] / [MEMORY] / [INFER])** + `[FETCHER:src:proxy]` / `[FETCH_FAILED:URLs]` |
| Q2 | タグ付与単位 | ✅ **主張ごと** (粒度ガイドラインは議題4 でフェーズ6 確定) |
| Q3 | タグなし主張の扱い | ✅ **禁止** (CHECK-2 + health_check 両方で検証) |
| Q4 | 遡及適用範囲 | ✅ **新規のみ** (既存 records / evidence は対象外) |
| Q5 | 準拠チェック | ✅ **両方併用** (CHECK-2 + health_check `miss_analysis_tag_compliance`) |
| Q6 | scripts 自動化 | ✅ **本フェーズ範囲内**: CLAUDE.md / memory に「セッション固有スクリプト (`_sessionXX_*.py`) 生成時にもタグ義務」と明記。既存 `_session61_*.py` 3本は使い捨てのため改修対象外 |

**13論点全件 (Q3 を除き) 確定済。Q3 (confidence_drift 種目別閾値) と Q2 (粒度ガイドライン) はフェーズ6 統合動作確認時に最終確定する**。

---

## 4. フェーズ5 (柱D 記録対象判断テーブル明文化) で実施すべき作業の概要

### 4.1 改修対象ファイル

- `CLAUDE.md`: 【柱D】記録対象判断テーブル セクション新設

### 4.2 サブタスク (新セッションでユーザーと協議して確定)

- 「記録対象判断テーブル」セクション新設
- 「記録対象 / 参考記録 / 無視可」の判断基準を表形式で明文化
- 境界事例の判断ルール:
  - Bristol-Newcastle Premiership (records 未登録だが市場fav≤1.50 敗戦 = scope外UPSET)
  - Northampton-Bath Premiership (date 訂正のみ必要)
  - Swiatek retire vs Li Madrid R3 (棄権の扱い)
  - Bondar-Svitolina Madrid R2 (#7 seed 敗退・records 未登録)
  - PHI G4 vs PIT (NHL records 未確認)
  - 上記すべて Session_61 で「scope外UPSET 検出のみ・records には未反映」となった事例
- scope の境界が曖昧なリーグ (例: ATP500 R1) はユーザー個別判断を仰ぐ運用を明記

### 4.3 想定される議題

- 棄権 (retire) / W-O / 試合不成立 の扱い (`void: true` フィールド との関係)
- 大会優先度 (Grand Slam / Masters 1000 / ATP 500 / ATP 250 等) と記録対象範囲
- リーグ内の round/week 階層と記録対象 (例: NRL Round 1-26 すべて vs Finals のみ)
- 新リーグ追加時の記録対象判断ワークフロー (記録 / 参考 / 無視可)

具体的境界条件は新セッションでユーザーと協議して確定する。

---

## 5. フェーズ6 (統合動作確認) の概要

### 5.1 実施内容

1. 仮想的な「次の Session_63 開始時」を想定したワークフローシミュレーション
2. 結果反映 → MISS 分析 → ルール提案 → 承認 → 実装までの全工程を書き出し
3. Session_61 と比較して何がどう変わるかを明示
4. ユーザーが「想定通り」と承認した時点で **4本柱 実装作業 完了**

### 5.2 議題 1〜4 の現状 (フェーズ6 で確定する論点)

| 議題 | 論点 | 確定時期 |
|---|---|---|
| 議題1 | evidence の時間的独立性 (R024 evidence 3件目が同一 turn 内「ついで検出」だった点の forbidden_practices 拡張可否) | フェーズ6 統合動作確認時 or A-3 遡及判断時 |
| 議題2 | STEP 0.5 (結果反映時 scope外UPSET スキャン) 実施を毎回確実に保証する仕組み (機械チェッカー / 構造化ログ / commit hook / 出力フォーマット強制 等) | フェーズ6 統合動作確認時 |
| 議題3 | confidence_drift 種目別閾値の確定 (テニス/NHL/NBA/MLB/サッカー/NFL/ラグビー全種の薄勝ち基準数値) | フェーズ6 統合動作確認時 |
| 議題4 | タグ付与の粒度ガイドライン (「論理的に独立した主張」の判定基準・短い接続句の扱い・推論連鎖の中間タグ要否) | フェーズ6 統合動作確認時 |

議題1〜4 はすべて `monitoring/session62_phase6_agenda.md` に記録済。実装変更なし・議題記録のみ。

### 5.3 フェーズ6 完了後 (別タスク) の予定作業

- A-3 遡及判断: R017 v2.0 / R024 v1.0 / P030-P033 の取り消し / 承認 / 修正後再構築 判断
- P030 ID 衝突解消: proposed_rule_id "R024" → "R025" 等への再付番
- ready_to_implement: P020 → R014 (NRL) / P024 → N_NBA_new2 (NBA) implement 判断
- Session_61 由来 12件 (Modified 8 + Untracked 4) の処理判断
- 既存 pending: PA092 / PA103 / PA099 / lineups フィード再取得 / BACKLOG.md Session_60 残

判断時は `monitoring/session62_phase6_agenda.md` の議題1 (evidence 時間的独立性) を参照する。

---

## 6. Session_61 由来 12件 + ready_to_implement 候補の凍結方針継続

**4本柱 全フェーズ (フェーズ1-6) 完了まで一切手を付けない** 凍結方針を継続維持:

### Modified 8件
- `core/dashboard_stats.json`
- `core/rules_tennis.json` (R017 v2.0 + R024 v1.0 追加で v2.5)
- `dashboard.html`
- `records/mlb/2026.json`
- `records/nrl/2026.json`
- `records/soccer/2025-26.json`
- `records/tennis/2026-ATP.json`
- `stats/upset_patterns.json` (A036-A043 追加で 41件)

### Untracked 4件
- `monitoring/session_61_handoff.md`
- `scripts/_session61_writeback.py`
- `scripts/_session61_rule_feedback.py`
- `scripts/_session61_phase2_upsets.py`

### ready_to_implement 候補
- P020 → R014 (NRL): R1-R8 + PD差6pt以上 + desperate team → 信頼度上限78% + 追加-5%
- P024 → N_NBA_new2 (NBA): star scorer (>25ppg RS) OFF/ON で L4 -8〜+8% (return cycle 双方向)

→ 上記 12件 + 候補 2本 すべて、フェーズ6 完了後の **A-3 遡及判断タスク** で扱う。フェーズ5 では一切触らない。

---

## 7. 新セッションでの再開手順

### 7.1 新セッション開始時の必須読込

1. CLAUDE.md (柱A + 柱B + 柱C 4-1+4-2+4-3 を含む最新版)
2. **本ファイル (`monitoring/session_62_phase4_complete_handoff.md`)** ← 最初に読む
3. `monitoring/session_62_phase1to3_handoff.md` (フェーズ1-3 完了サマリ)
4. `monitoring/session_62_stage1to2_handoff.md` (フェーズ4 ステージ1-2 完了サマリ)
5. `monitoring/session_61_handoff.md` (Session_61 運用品質診断 v2)
6. `monitoring/session62_phase6_agenda.md` (議題1〜4 すべて確認)
7. STEP 0 (health_check) 実行 — 12番目の検査項目 `miss_analysis_tag_compliance` が動作することを確認
8. STEP 1 必須ファイル群 (BACKLOG.md / user_feedback_log.md / pending_actions.md / claude_error_log.md / rule_pipeline.json / framework.json)

### 7.2 新セッション最初のタスク

**フェーズ5 (柱D 記録対象判断テーブル明文化) 着手から再開する**。具体的順序:

1. フェーズ5 着手前に、CLAUDE.md 新設「【柱D】記録対象判断テーブル」の具体案 (記録対象 / 参考記録 / 無視可 の判断基準テーブル + Session_61 由来の 9件境界事例の判断方針 + scope 境界曖昧時のユーザー判断ワークフロー) をユーザーに提示し承認を得る
2. ユーザー承認後、CLAUDE.md への実装を実施
3. フェーズ5 完了報告 → ユーザー承認待ち
4. フェーズ6 (統合動作確認シミュレーション) 着手前に、議題1〜4 の確定方針案をユーザーに提示
5. ユーザー承認後、フェーズ6 シミュレーション実施
6. フェーズ6 完了報告 → 4本柱 実装作業 完了
7. (別タスク) A-3 遡及判断・Session_61 ペンディング事項 着手

### 7.3 新セッション着手時の禁止事項 (再掲)

- rules_*.json / records / upset_patterns.json への書き込み禁止 (フェーズ5/6 のメタルール改修のみ)
- core/framework.json は本フェーズで一切触らない
- Session_61 由来 12件 + ready_to_implement P020/P024 は 4本柱完了まで凍結継続
- 「ついでにこれもやっておきました」は禁止
- 各フェーズ/ステージ完了時に必ずユーザー承認を待つ
- 不明点があれば実装を止めて質問

---

**Session_62 フェーズ4 終了**: 2026-04-27
**新セッション最優先**: フェーズ5 (柱D 記録対象判断テーブル明文化) の具体案提示 → ユーザー承認 → CLAUDE.md 実装
