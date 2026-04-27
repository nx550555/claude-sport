# Session_62 フェーズ5 完了 引き継ぎサマリ

> **新セッション読込必須**: このファイルは Session_62 (2026-04-27) のフェーズ5 (柱D 記録対象判断テーブル明文化) 完了時点のスナップショット。新セッションでは **フェーズ6 (統合動作確認 + 議題1〜8 協議)** から再開する。

---

## 1. Session_62 全体構造の現在地

| フェーズ | 内容 | 実施状況 |
|---|---|---|
| フェーズ1 | 改修対象ファイルの現状把握 | ✅ 完了・ユーザー承認済 |
| フェーズ2 | 柱A: ルール改訂統制プロトコル新設 (rule_pipeline.json + CLAUDE.md + memory) | ✅ 完了・ユーザー承認済 |
| フェーズ3 | 柱B: 結果反映 STEP 0.5 scope外UPSET スキャン SOP 新設 (CLAUDE.md) | ✅ 完了・ユーザー承認済 |
| フェーズ4 ステージ1 | 柱C 4-1: MISS 重要度3段階分類 (Class A/B/C + confidence_drift 枠組み) | ✅ 完了・ユーザー承認済 |
| フェーズ4 ステージ2 | 柱C 4-2: fetch 件数規定 (A=3 / B=2 / C=1 + WebSearch カウント外 + [FETCH_FAILED]) | ✅ 完了・ユーザー承認済 |
| フェーズ4 ステージ3 | 柱C 4-3: 情報源タグ義務化 (5種タグ [FETCH/FETCHER/SEARCH/MEMORY/INFER]) | ✅ 完了・ユーザー承認済 |
| **フェーズ5** | **柱D: 記録対象判断テーブル明文化 (3区分 full_record/reference_only/skip_record + match_status enum + Cup戦細分化 + 境界曖昧リーグ SOP)** | ✅ **完了・ユーザー承認済** |
| フェーズ6 | 統合動作確認 (シミュレーション + 議題1〜8 協議) | 🔴 **新セッションで実施** |
| (4本柱完了後別タスク) | A-3 遡及判断 + Session_61 ペンディング事項 + Session_61 9件振り分け実施 | 🔴 4本柱 全フェーズ完了後 |

**重要原則 (Session_62 全期間共通)**:
1. 各フェーズ/ステージ完了時にユーザー承認を待つ
2. 既存の rules_*.json / records / upset_patterns.json への書き込みは本作業中は実施しない (メタルール側の改修のみ)
3. 不明点があれば実装を止めて質問
4. 「ついでにこれもやっておきました」は禁止
5. Session_61 ペンディング事項 (Modified 8件 + Untracked 4件 / R024→R025 再付番 / ready_to_implement P020/P024) は **4本柱 全フェーズ完了まで一切手を付けない**

---

## 2. フェーズ5 で改修した3ファイル + memory 2件

### 2.1 git 管轄内 (3ファイル / 2 commit)

| # | ファイル | 変更概要 | commit |
|---|---|---|---|
| 1 | `CLAUDE.md` | 【柱D: 記録対象判断テーブル】セクション新設 (9サブセクション・約185行追加) + 【柱B: 結果反映 STEP 0.5】既存セクションに「Claude 推奨区分」列追加 + ユーザー判断依頼テキスト微調整 ((A)=区分1 / (B)=区分2 / (C)=区分3 対応明示) + 反映時の record_class 必須付与言及 | 1 (`68c6130`) |
| 2 | `monitoring/health_check.py` | 12項目目 `miss_analysis_tag_compliance` に `record_class == "skip_record"` フィルタ追加 (区分3 試合は走査対象外) + ヘッダーコメント更新 | 1 (`68c6130`) |
| 3 | `monitoring/session62_phase6_agenda.md` | 議題5-8 追加 (各議題3案 / 判断必要時期 / 現時点ステータス: 議題記録のみ・実装変更なし) + 末尾文言更新 (「フェーズ5 進行中」→「フェーズ6 進行中」/「議題5・6」→「議題9・10」) | 2 (`292db7e`) |

### 2.2 CLAUDE.md 柱D セクション 9サブセクション構成

| サブセクション | 内容 |
|---|---|
| (背景) | Session_61 由来 9件境界事例の経緯記録 |
| 1. 3区分定義 (record_class) | full_record / reference_only / skip_record + 判定条件テーブル |
| 2. match_status enum 仕様 | 5値 enum (completed / retired / walkover / cancelled / postponed) + 区分・prediction_hit・miss_class 連動表 |
| 3. record_class フィールド付与ルール | 新規のみ・遡及なし・記述例 (JSON) |
| 4. 大会優先度テーブル | 16種目 scope内/外 + Cup戦細分化 (UCL Knockout=1 / UCL Group=2 / UEL=2 / FA Cup R5+=2 / R4-=3 / 各国カップ=3) + チーム戦テニス全=区分3 |
| 5. リーグ内 round/week 階層 | CLAUDE.md インライン記述 (rules_*.json 改訂は柱A 承認必須のため対象外) |
| 6. 新リーグ追加 SOP | 5ステップワークフロー |
| 7. 既存柱との整合性 | 柱A / 柱B / 柱C / health_check 整合確認テーブル |
| 8. 境界曖昧リーグ個別判断 SOP | 6リーグ表 + ユーザー追加運用 + 個別判断ワークフロー |
| 9. Session_61 由来 9件 振り分け案 | 4本柱完了後の別タスクで実施・本フェーズは記録のみ |

### 2.3 git 管轄外 memory 2件 (commit 対象外)

| # | ファイル | 変更概要 |
|---|---|---|
| 4 | `memory/feedback_no_fabrication.md` | frontmatter (name + description) 更新 + 末尾に「Session_62 フェーズ5 追加 (2026-04-27): 柱D 区分3 (skip_record) はタグ義務対象外」セクション追記 (6サブセクション: record_class 別タグ義務適用範囲 / 良い例・悪い例 / health_check.py 連携 / 既存原則との整合性 / How to apply / Why) |
| 5 | `memory/MEMORY.md` (memory index) | feedback_no_fabrication エントリの description を「フェーズ4 4-3 反映」→「フェーズ4 4-3 + フェーズ5 反映」に更新 |

### 2.4 Session_62 全体 commit 履歴 (累計 9 commit)

| commit | message | フェーズ |
|---|---|---|
| `563d149` | Session_62 phase2 柱A: ルール改訂統制プロトコル新設 | フェーズ2 |
| `5b6378c` | Session_62 phase3 柱B: 結果反映 STEP 0.5 scope外UPSET スキャン SOP 新設 | フェーズ3 |
| `dc69fea` | Session_62 phase1-3 monitoring: 引き継ぎサマリ + フェーズ6 議題リスト | フェーズ1-3 |
| `87a8c81` | Session_62 phase4 stages1-2: 柱C 4-1 MISS 重要度3段階分類 + 4-2 fetch 件数規定 | フェーズ4 ステージ1-2 |
| `74e1b87` | Session_62 phase4 stages1-2 monitoring: 議題3 + stage1to2 引継ぎサマリ | フェーズ4 ステージ1-2 |
| `84cabdd` | Session_62 phase4 stage3: 柱C 4-3 情報源タグ義務化 | フェーズ4 ステージ3 |
| `9e92305` | Session_62 phase4 stage3 monitoring: 議題4 追加 + phase4 完了引継ぎサマリ | フェーズ4 ステージ3 |
| **`68c6130`** | **Session_62 phase5: 柱D 記録対象判断テーブル新設 + 柱B 推奨区分列追加 + health_check 区分フィルタ** | **フェーズ5** |
| **`292db7e`** | **Session_62 phase5 monitoring: 議題5-8 追加** | **フェーズ5** |

すべて push 済 (origin/main と同期)。

---

## 3. 18論点全件確定済の確認

### カテゴリ別

| カテゴリ | 論点 | 確定 |
|---|---|---|
| **区分定義** | a-1 (3区分) / a-2 (命名 full_record/reference_only/skip_record) | ✅ |
| **Session_61 由来9件** | b-1 (Swiatek retire=区分2) / b-2 (Bondar=区分1) / b-3 (9件遡及登録は4本柱完了後別タスク統合) | ✅ |
| **大会優先度** | c-1 (match_status enum 5値) / c-2-1 (テニス R1 階層化) / c-2-2 (Cup戦細分化) / c-2-3 (チーム戦テニス全=区分3) / c-3 (CLAUDE.md インライン) / c-4 (新リーグ SOP) | ✅ |
| **既存柱整合** | d-1 (柱B 列追加) / d-2 (health_check フィルタ) / d-3 (既存遡及付与なし) | ✅ |
| **境界曖昧リーグ** | e-1 (個別判断 SOP) / e-2 (6リーグ + ユーザー追加) | ✅ |
| **議題追加** | f-1 (議題5) / f-2 (議題6) / f-3 (議題7) / f-4 (議題8) | ✅ |

### 詳細確定内容 (再掲)

- **a-1 / a-2**: 3区分採用 / `full_record` / `reference_only` / `skip_record`
- **b-1**: Swiatek retire vs Li Madrid R3 = 区分2 (reference_only)
- **b-2**: Bondar-Svitolina (#7 seed) Madrid R2 = 区分1 (full_record)
- **b-3**: Session_61 由来9件遡及登録は4本柱完了後の別タスクで統合実施 (本フェーズは記録のみ)
- **c-1**: match_status enum 5値 (completed / retired / walkover / cancelled / postponed) 導入
- **c-2-1**: テニス R1 階層化 — Masters R1=区分1 / ATP500 R1=区分2 / ATP250 R1=区分3 (WTA も同様)
- **c-2-2**: Cup戦細分化 — UCL Knockout (R16+)=区分1 / UCL Group=区分2 / UEL 全般=区分2 / FA Cup R5+=区分2 / FA Cup R4-=区分3 / 各国カップ全般 (DFB-Pokal / Coupe de France 等)=区分3
- **c-2-3**: チーム戦テニス (Davis Cup / United Cup / Laver Cup) 全=区分3 (ベット対象外・ELO 機能せず)
- **c-3**: scope_rounds 詳細を CLAUDE.md インライン記述 (rules_*.json 改訂は柱A 承認必須のため本フェーズ範囲外)
- **c-4**: 新リーグ追加 SOP を本プロトコルに含める
- **d-1**: 柱B 既存テーブルに「Claude 推奨区分」列追加 (本フェーズで実施)
- **d-2**: health_check.py に `record_class == "skip_record"` フィルタ追加 (本フェーズで実施)
- **d-3**: 既存 records への record_class フィールド遡及付与なし (新規エントリのみ付与)
- **e-1**: 境界曖昧リーグ個別判断 SOP 導入
- **e-2**: 境界曖昧リーグ表 6リーグ (ATP 500 R1 / ATP 250 R1 / WTA 125K / Pro D2 / Premiership 下位 / Super League PO) + ユーザー追加運用
- **f-1〜f-4**: 議題5-8 を agenda.md に追加 (議題5 match_status 遡及範囲 / 議題6 大会優先度テーブル維持責任 / 議題7 区分2 cumulative 集計除外境界 / 議題8 境界曖昧リーグ判断踏襲有効期限)

---

## 4. フェーズ6 で実施すべき作業の詳細

### 4.1 改修対象ファイル

**変更ファイル**: なし (シミュレーションのみ)

ただし、議題1〜8 の協議結果次第で、以下のファイルに小幅な追記が発生する可能性あり (協議結果に依存):
- `CLAUDE.md` (議題確定後の運用追記)
- `core/rule_pipeline.json` の `instructions_for_claude` (議題1 evidence 時間的独立性確定時)
- `monitoring/health_check.py` (議題2 STEP 0.5 実施保証の機械チェッカー導入時)
- `core/rules_*.json` (議題3 confidence_drift 種目別閾値確定時 → 柱A 承認必須プロセス適用)

### 4.2 実施内容

1. **仮想 Session_63 開始時のワークフロー全工程書き出し**
   - STEP 0 (health_check 実行)
   - STEP 1 (BACKLOG / user_feedback_log / pending_actions / claude_error_log / rule_pipeline / framework 読込)
   - 結果反映 STEP 0.5 (scope外UPSET スキャン → ユーザー (A)/(B)/(C) 判断 → 区分1/2/3 反映)
   - MISS 分析 (柱C: miss_class 付与 → fetch 件数規定 → 5種タグ付与)
   - ルール提案 (柱A: ready_for_proposal → 提案レポート生成 → ユーザー承認/却下/修正後再提案 → 実装)
   - 記録対象判断 (柱D: record_class 付与 → match_status enum 設定 → 境界曖昧リーグ個別判断)

2. **Session_61 と比較した変化の明示**
   | 観点 | Session_61 (旧) | Session_62 完了後 (新) |
   |---|---|---|
   | scope外UPSET 検出 | ユーザー質問契機の受動的検出 | 柱B STEP 0.5 SOP 化で自発的検出 |
   | ルール implement | 同一 turn 内 evidence 3/3 → implement | 柱A 承認制プロセス (ready_for_proposal → 提案レポート → ユーザー承認 → 次セッション以降に実装) |
   | MISS 分析根拠 | 記憶ベース推論 (タグなし) | 柱C 5種タグ義務 ([FETCH/FETCHER/SEARCH/MEMORY/INFER]) |
   | 境界事例判断 | Claude 自発判断 (Bristol-Newcastle / Northampton-Bath / Swiatek retire 等) | 柱D 3区分テーブル参照 (full_record / reference_only / skip_record) |
   | fetch 件数 | 平均 1件未満 (WebFetch 本文取得 0件成功) | 柱C 4-2 Class 別件数規定 (A=3 / B=2 / C=1) |
   | health_check 検査項目 | 11項目 | 12項目 (miss_analysis_tag_compliance + record_class フィルタ) |

3. **議題1〜8 の協議・確定**
   下記 5. 議題リスト1〜8 の現状 を参照。各議題について案を絞り込み、確定方針を決定する。

4. **ユーザー「想定通り」承認 → 4本柱 実装作業 完了**

---

## 5. 議題リスト1〜8 の現状

### 議題1: evidence の時間的独立性

- **追加日**: 2026-04-27 (フェーズ2 完了時)
- **論点**: R024 evidence 3件目 (A041 Baptiste-Paolini) 自体が同一 turn 内「ついで検出」だった点も新プロトコル違反。forbidden_practices 拡張可否
- **案**: (A) 異セッション独立検出 / (B) 異試合日 / (C) 同セッション複数追加時は次セッション以降に proposal / (D) ユーザー質問契機 evidence は別カウント
- **判断必要時期**: フェーズ6 統合動作確認時 or A-3 遡及判断時
- **現時点ステータス**: 議題記録のみ・実装変更なし

### 議題2: STEP 0.5 実施保証の仕組み

- **追加日**: 2026-04-27 (フェーズ3 完了時)
- **論点**: 柱B 結果反映 STEP 0.5 SOP の実施を毎回確実に保証する仕組みが弱い (commit message 任意記述のみ)
- **案**: (A) `scripts/verify_step05_executed.py` 機械チェッカー / (B) `monitoring/step05_log.jsonl` 構造化ログ / (C) commit hook + `[STEP05:DONE]` タグ / (D) records JSON `step05_scanned_at` フィールド必須化 / (E) 出力フォーマット強制 (CHECK-4 連携)
- **判断必要時期**: フェーズ6 統合動作確認時
- **現時点ステータス**: 議題記録のみ・実装変更なし

### 議題3: confidence_drift 種目別閾値の確定

- **追加日**: 2026-04-27 (フェーズ4 ステージ1 完了時)
- **論点**: 柱C 4-1 で導入した `confidence_drift=high` の薄勝ち基準が種目別に未確定 (TBD)
- **案 (種目別薄勝ち基準候補)**:
  - テニス: 3セット縺れ / fav が 1セットでも落とした
  - NHL: OT/SO 勝利 / regulation 1点差 (空ネット除く)
  - NBA: 1桁差 (9点差以下) / 4Q ガベージ前 1桁
  - MLB: 1点差 / walk-off / 延長戦勝利
  - サッカー: 1点差 / 後半AT で勝ち越し
  - NFL: TD1個差以内 (8点差以下) / 4Q 残数分で同点進行
  - NRL/Super Rugby/Premiership/Top14/Pro D2/Super League: TD1個差以内 (7点差以下)
- **判断必要時期**: フェーズ6 統合動作確認時 (議題7 と同時)
- **現時点ステータス**: 議題記録のみ・実装変更なし

### 議題4: タグ付与の粒度ガイドライン

- **追加日**: 2026-04-27 (フェーズ4 ステージ3 完了時)
- **論点**: 「論理的に独立した主張」の判定基準が記述者依存・短い接続句 (10文字未満) の扱い・推論連鎖中間タグ要否・否定主張・程度副詞付き事実・複合主語の扱い
- **案**: 解釈A (主張ごと別タグ・現行運用) / 解釈B (1主張のデータ列挙として段落末1タグ可)
- **判断必要時期**: フェーズ6 統合動作確認時
- **現時点ステータス**: 議題記録のみ・実装変更なし (現行は記述者判断 + health_check 文単位検出 + 短い接続句 10文字未満 はカウント対象外)

### 議題5: match_status 遡及範囲

- **追加日**: 2026-04-27 (フェーズ5 ステップ4 完了時)
- **論点**: 既存 records (100件超) への match_status enum 遡及付与判定
- **案**: (A) 既存 void:true 一律 cancelled 遡及 / (B) retired/walkover 区別判定実装 / (C) 新規のみ運用 (現行)
- **判断必要時期**: フェーズ6 統合動作確認時
- **現時点ステータス**: 議題記録のみ・実装変更なし

### 議題6: 大会優先度テーブル維持責任

- **追加日**: 2026-04-27 (フェーズ5 ステップ4 完了時)
- **論点**: 柱A サブセクション1 (CLAUDE.md=B区分・承認必須) と 柱D サブセクション6 (新リーグ追加=柱A 適用対象外) の矛盾
- **案**: (A) 全 B区分 / (B) 例外規定化 (現行) / (C) 名称変更=B区分 + 新リーグ追加=対象外 階層化
- **判断必要時期**: フェーズ6 統合動作確認時
- **現時点ステータス**: 議題記録のみ・実装変更なし

### 議題7: 区分2 (reference_only) cumulative 集計除外境界

- **追加日**: 2026-04-27 (フェーズ5 ステップ4 完了時)
- **論点**: Track 1 (ベット推奨収益性) は区分1 のみ寄与で確定。Track 2 (全試合モデル品質) で区分2 を含めるか議論
- **案**: (A) Track 2 も区分1 のみ (現行) / (B) Track 2 は区分1+2 / (C) by_record_class 別軸集計 + 議題3 連動
- **判断必要時期**: フェーズ6 統合動作確認時 (議題3 と同時協議が整合的)
- **現時点ステータス**: 議題記録のみ・実装変更なし

### 議題8: 境界曖昧リーグ判断踏襲の有効期限

- **追加日**: 2026-04-27 (フェーズ5 ステップ4 完了時)
- **論点**: シーズン跨ぎ・round 階層・大会フォーマット変更時の踏襲継続性
- **案**: (A) シーズン単位リセット / (B) フォーマット変更時のみ再判断 / (C) round 階層ごとに踏襲粒度分離
- **判断必要時期**: フェーズ6 統合動作確認時
- **現時点ステータス**: 議題記録のみ・実装変更なし

---

## 6. 4本柱完了後の遡及判断タスク予告

### 6.1 凍結維持中の対象 (12件 + 候補 2本 + ルール3件)

#### Session_61 由来 Modified 8件
- `core/dashboard_stats.json`
- `core/rules_tennis.json` (R017 v2.0 + R024 v1.0 追加で v2.5)
- `dashboard.html`
- `records/mlb/2026.json`
- `records/nrl/2026.json`
- `records/soccer/2025-26.json`
- `records/tennis/2026-ATP.json`
- `stats/upset_patterns.json` (A036-A043 追加で 41件)

#### Session_61 由来 Untracked 4件
- `monitoring/session_61_handoff.md`
- `scripts/_session61_writeback.py`
- `scripts/_session61_rule_feedback.py`
- `scripts/_session61_phase2_upsets.py`

#### ready_to_implement 候補 2本
- P020 → R014 (NRL): R1-R8 + PD差6pt以上 + desperate team → 信頼度上限78% + 追加-5%
- P024 → N_NBA_new2 (NBA): star scorer (>25ppg RS) OFF/ON で L4 -8〜+8% (return cycle 双方向)

#### 遡及判断対象ルール 3件
- **R017 v2.0** (home strict-define): evidence 1件改訂 → 取り消し / 承認 / 修正後再構築判断 (議題1 evidence 時間的独立性参照)
- **R024 v1.0** (form slump): evidence 3件は満たすが同 turn 内 implement・反例検証なし → 取り消し / 承認 / 修正後再構築判断
- **P030 ID 衝突解消**: proposed_rule_id "R024" → "R025" 等への再付番判断

### 6.2 Session_61 9件振り分け実施 (柱D サブセクション9 のテーブル参照)

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

### 6.3 既存 pending (前セッションから持越し)
- PA092: UCL SF Atletico-Arsenal (4/30) / PSG-Bayern (4/29) STEP 4.5 lineups 確認
- PA103: GEN007 UPSET_PICK_Lite 採否判断 (Phase2 移行後 9日経過、発動 0件)
- PA099: NBA G3/G4 残 (ORL-DET / PHX-OKC / MIN-DEN G4)
- フィード再取得: lineups (健全性 WARN)
- BACKLOG.md Session_60 残: dashboard 成長分析タブ AUTO ブロック実装、cumulative_history.json 連動

---

## 7. 新セッションでの再開手順

### 7.1 新セッション開始時の必須読込

1. CLAUDE.md (柱A + 柱B + 柱C 4-1+4-2+4-3 + 柱D を含む最新版)
2. **本ファイル (`monitoring/session_62_phase5_complete_handoff.md`)** ← 最初に読む
3. `monitoring/session_62_phase4_complete_handoff.md` (フェーズ4 完了サマリ)
4. `monitoring/session_62_stage1to2_handoff.md` (フェーズ4 ステージ1-2 完了サマリ)
5. `monitoring/session_62_phase1to3_handoff.md` (フェーズ1-3 完了サマリ)
6. `monitoring/session_61_handoff.md` (Session_61 運用品質診断 v2)
7. `monitoring/session62_phase6_agenda.md` (議題1〜8 すべて確認)
8. STEP 0 (health_check) 実行 — 12項目目 `miss_analysis_tag_compliance` が `record_class == "skip_record"` フィルタ含めて動作することを確認
9. STEP 1 必須ファイル群 (BACKLOG.md / user_feedback_log.md / pending_actions.md / claude_error_log.md / rule_pipeline.json / framework.json)

### 7.2 新セッション最初のタスク

**フェーズ6 (統合動作確認 + 議題1〜8 協議) 着手から再開する**。具体的順序:

1. フェーズ6 着手前に、議題1〜8 の確定方針案をユーザーに提示
2. ユーザー協議で各議題の案を絞り込み
3. 議題確定後、必要に応じて以下のファイルに小幅な追記:
   - `CLAUDE.md` (議題確定後の運用追記)
   - `core/rule_pipeline.json` の `instructions_for_claude` (議題1 確定時)
   - `monitoring/health_check.py` (議題2 機械チェッカー導入時)
   - `core/rules_*.json` (議題3 confidence_drift 閾値確定時 → 柱A 承認必須プロセス適用)
4. 仮想 Session_63 開始時のワークフロー全工程書き出し
5. Session_61 と比較した変化の明示
6. ユーザー「想定通り」承認 → **4本柱 実装作業 完了**
7. (別タスク) A-3 遡及判断・Session_61 ペンディング事項・Session_61 9件振り分け実施 着手

### 7.3 新セッション着手時の禁止事項 (再掲)

- rules_*.json / records / upset_patterns.json への書き込み禁止 (フェーズ6 はシミュレーションが中心、議題確定で柱A 承認必須プロセス起動するもののみ書き込み)
- core/framework.json は本フェーズで一切触らない
- Session_61 ペンディング事項 12件 + ready_to_implement 候補 P020/P024 は 4本柱完了まで凍結継続
- 「ついでにこれもやっておきました」は禁止
- 各フェーズ/議題確定時に必ずユーザー承認を待つ
- 不明点があれば実装を止めて質問

---

## 8. Session_61 由来 12件 + ready_to_implement 候補の凍結方針継続

**4本柱 全フェーズ (フェーズ1-6) 完了まで一切手を付けない** 凍結方針を継続維持:

### Modified 8件 (再掲)
- `core/dashboard_stats.json`
- `core/rules_tennis.json` (R017 v2.0 + R024 v1.0 追加で v2.5)
- `dashboard.html`
- `records/mlb/2026.json`
- `records/nrl/2026.json`
- `records/soccer/2025-26.json`
- `records/tennis/2026-ATP.json`
- `stats/upset_patterns.json` (A036-A043 追加で 41件)

### Untracked 4件 (再掲)
- `monitoring/session_61_handoff.md`
- `scripts/_session61_writeback.py`
- `scripts/_session61_rule_feedback.py`
- `scripts/_session61_phase2_upsets.py`

### ready_to_implement 候補 (再掲)
- P020 → R014 (NRL)
- P024 → N_NBA_new2 (NBA)

→ 上記 12件 + 候補 2本 + R017 v2.0 / R024 v1.0 / P030 ID衝突 すべて、フェーズ6 完了後の **A-3 遡及判断タスク** で扱う。フェーズ6 では一切触らない (議題協議で参照するのみ)。

---

**Session_62 フェーズ5 終了**: 2026-04-27
**新セッション最優先**: フェーズ6 (統合動作確認 + 議題1〜8 協議) 着手 → 議題確定 → 仮想 Session_63 ワークフロー書き出し → Session_61 比較 → ユーザー承認 → **4本柱 実装作業 完了**
