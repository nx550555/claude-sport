# Session_62 フェーズ1〜3 引き継ぎサマリ

> **新セッション読込必須**: このファイルは Session_62 (2026-04-27) のフェーズ1〜3 (運用品質改善・柱A + 柱B) で実施した変更の完全リストと、フェーズ4〜6 で残っている作業をまとめたもの。新セッションではフェーズ4 から再開する。

---

## 1. Session_62 の全体構造

Session_61 運用品質診断 v2 (自己評価 2.3/5) を受けて確定した4本柱の改善作業を、6フェーズに分けて実施中:

| フェーズ | 内容 | 実施状況 |
|---|---|---|
| フェーズ1 | 改修対象ファイルの現状把握 (実装変更なし) | ✅ 完了・ユーザー承認済 |
| **フェーズ2** | **柱A: ルール自動実装の停止 → 承認制 (rule_pipeline.json + CLAUDE.md + memory)** | ✅ **完了・ユーザー承認済** |
| **フェーズ3** | **柱B: scope外 UPSET スキャン SOP 化 (CLAUDE.md)** | ✅ **完了・ユーザー承認待ち→本サマリ保存後に判断** |
| フェーズ4 | 柱C: 一次ソース fetch の義務化 (memory + CLAUDE.md) | 🔴 **新セッションで実施** |
| フェーズ5 | 柱D: 記録対象判断テーブルの明文化 (CLAUDE.md) | 🔴 新セッションで実施 |
| フェーズ6 | 統合動作確認 (シミュレーション) | 🔴 新セッションで実施 |

**重要原則 (Session_62 全期間共通)**:
1. 各フェーズ完了時にユーザー承認を待つ。一括で全フェーズを通さない
2. 既存の rules_*.json / records / upset_patterns.json への **データ書き込みは本作業中は実施しない** (メタルール側の改修のみ)
3. 不明点があれば実装を止めて質問
4. 「ついでにこれもやっておきました」は禁止
5. Session_61 ペンディング事項 C (未反映 9試合) と B (R024→R025 再付番) は **4本柱 全フェーズ完了まで一切手を付けない**

---

## 2. フェーズ1〜3 で変更したファイルと内容

### 2.1 フェーズ1: 現状把握

**変更ファイル**: なし (調査のみ)

**成果物**: CLAUDE.md 見出し構成 / rule_pipeline.json instructions_for_claude 全文 / memory 27ファイルの1行要約 / 改修対象ファイル4点 (CLAUDE.md / rule_pipeline.json / feedback_miss_analysis_depth.md / feedback_no_fabrication.md) の特定

### 2.2 フェーズ2: 柱A 実装

#### 変更ファイル一覧

| # | ファイル | 変更概要 |
|---|---|---|
| 1 | `core/rule_pipeline.json` | `instructions_for_claude` 改訂 (Session_62 追記2項目) + `trigger_check_protocol.auto_implement` を `DISABLED` 化 + `approval_workflow` (4ステップ + forbidden_practices 3項目) 新設 |
| 2 | `CLAUDE.md` | L417 直後 (L419「絶対禁止」直前) に **【ルール改訂統制プロトコル】** セクション新設 (6サブセクション) |
| 3 | `memory/feedback_git_upload.md` | 階層化ルール追記: A 区分 (確認不要) / B 区分 (承認必須) / C 区分 (競合時 B 優先) |
| 4 | `memory/MEMORY.md` | feedback_git_upload エントリの description を「階層化済 Session_62」に更新 |

#### 2.2.1 core/rule_pipeline.json 変更点

**旧**:
```
"閾値に達した候補は即時ルールファイルへ追加し、このファイルのstatusをimplementedに更新する"
"auto_implement": "current_count >= trigger_threshold の場合、次のセッション開始時に自動実装する"
```

**新**:
```
"閾値到達した候補は即時実装してはならない。status を 'ready_for_proposal' に変更し、次セッション開始時に『実装提案レポート』を生成してユーザー承認を待つ。"
"auto_implement": "DISABLED (Session_62 2026-04-27 廃止)。current_count >= trigger_threshold に達した時点で status を 'ready_for_proposal' に変更し、当該候補の自動実装は禁止する。"
"approval_workflow": {
  "step1_threshold_reached": "...",
  "step2_proposal_report": "(a)候補ID/(b)影響範囲/(c)evidence URL+一次ソース有無/(d)cumulative影響/(e)却下時代替案",
  "step3_user_decision": "承認/却下/修正後再提案",
  "step4_implement_or_revise": "...",
  "forbidden_practices": [
    "同一 turn 内での evidence 3/3 → implement",
    "ユーザー質問応答中のついで実装",
    "evidence 1件のみでの即改訂"
  ]
}
```

#### 2.2.2 CLAUDE.md 「ルール改訂統制プロトコル」サブセクション

1. 適用対象 (承認必須ファイル: `core/rules_*.json` / `core/rule_pipeline.json` の status 変更 / `core/framework.json`)
2. 適用対象外 (records / dashboard / scripts / monitoring / stats / BACKLOG / session_logs / evidence 追加)
3. 新規ルール実装プロセス (4ステップ + 提案レポート必須項目 a〜e)
4. 既存ルール改訂プロセス (差分レポート + 反例検証 + evidence 1件禁止)
5. 禁止事項 (Session_61 逸脱 5パターン明文化)
6. 競合解消ルール (本プロトコル優先)

#### 2.2.3 memory/feedback_git_upload.md 階層化

- A 区分 (確認不要): records / dashboard.html / dashboard_stats.json / scripts / monitoring / stats / BACKLOG / session_logs / git operations / `evidence` 追加・`current_count` インクリメント
- B 区分 (承認必須): `core/rules_*.json` 本体 / `rule_pipeline.json` の status 変更 / `core/framework.json`
- C 区分 (競合時 B 優先)

### 2.3 フェーズ3: 柱B 実装

#### 変更ファイル一覧

| # | ファイル | 変更概要 |
|---|---|---|
| 1 | `CLAUDE.md` | L273 の直後 (L275「ダッシュボード同期プロトコル」直前) に **【結果反映 STEP 0.5・毎回必須】scope外 UPSET スキャン SOP** を新設 (6サブセクション) |

#### 2.3.1 命名上の注意

CLAUDE.md には既に **STEP 0.5: 外部スタッツフィード更新** (セッション開始時実行) が存在するため、本 SOP は名称衝突を避けて **【結果反映 STEP 0.5】** と命名:

- 既存 STEP 0.5: セッション開始フロー / 外部スタッツフィード fetcher 実行
- 新設 STEP 0.5: 結果反映フロー / scope外UPSET スキャン

#### 2.3.2 結果反映 STEP 0.5 サブセクション構造

1. スキャン対象の定義 (市場 favorite ≤ 1.50 敗戦 / GO/CAUTION 推奨と無関係 / records 未登録試合も対象)
2. スキャン実行手順 (6ステップ + ユーザー提示テーブル形式 + (A)/(B)/(C) 判断依頼フォーマット)
3. スキャン後の rule_pipeline.json への影響 (evidence 追加は A 区分・status 変更は B 区分)
4. 記憶ベース推論の禁止 (柱C で実装予定の情報源タグ義務化と整合)
5. SOP の運用境界 (結果反映時のみ・スクリーニングのみは非適用)
6. Session_61 逸脱パターンの再発防止 (ユーザー質問契機の検出から自発検出への転換)

### 2.4 フェーズ2 補足: A-3 遡及確認レポート

**実施内容**: Session_61 で確認なく実装した R017 v2.0 / R024 v1.0 / P030-P033 の現状確認レポート生成のみ (実装の取り消し / 承認は **フェーズ6 完了後** に別タスクで実施)。

**4項目の判断材料**:
- R017 v2.0 (home strict-define): evidence 1件改訂 → 新プロトコル違反、ユーザー判断 (取り消し / 承認 / 修正後再構築)
- R024 v1.0 (form slump): evidence 3件は満たすが同 turn 内 implement・反例検証なし、ユーザー判断
- P030 (Madrid altitude): proposed_rule_id "R024" 衝突 → 再付番判断 (項目1/2 確定後)
- P031-P033 (Bundesliga / MLB streak / NRL Sydney derby): 候補登録は新プロトコル適用対象外、維持で問題なし

### 2.5 フェーズ2 完了時の追加観点記録

**新規ファイル**: `monitoring/session62_phase6_agenda.md`

**議題1: evidence の時間的独立性** (フェーズ6 統合動作確認 or A-3 遡及判断時に参照):
- R024 evidence 3件目 (A041 Baptiste-Paolini) 自体が同一 turn 内の「ついで検出」だった点も新プロトコル違反論点
- forbidden_practices 拡張時の判定基準案 (案A: 異セッション独立検出 / 案B: 異試合日 / 案C: 同セッション複数追加時は次セッション以降に proposal / 案D: ユーザー質問契機の evidence は別カウント)
- **議題記録のみ・実装変更なし**

---

## 3. フェーズ4〜6 で残っている作業

### 3.1 フェーズ4: 柱C 実装 (一次ソース fetch の義務化)

**改修対象ファイル**:
- `CLAUDE.md` (3箇所新設・既存改訂)
- `memory/feedback_miss_analysis_depth.md` (改訂)
- `memory/feedback_no_fabrication.md` (改訂)

**サブタスク**:

#### 4-1. MISS 重要度3段階分類 (CLAUDE.md 新設)

CLAUDE.md に新設するセクション。MISS を Class A/B/C 等の3段階に分類:
- (例) Class A: GO推奨 MISS (ベット損失あり) → 高重要度
- (例) Class B: CAUTION推奨 MISS / 出力A MISS → 中重要度
- (例) Class C: SKIP / 推奨外試合の MISS / scope外UPSET → 低重要度

具体的分類定義は新セッションでユーザーと協議して確定する。

#### 4-2. fetch 件数規定 (重要度別)

CLAUDE.md と memory/feedback_miss_analysis_depth.md 両方に明記:
- (例) Class A: WebFetch ≥3 件 + SNS/会見 ≥2 件
- (例) Class B: WebFetch ≥2 件 + SNS/会見 ≥1 件
- (例) Class C: WebFetch ≥1 件
- WebSearch スニペットは fetch にカウントしない原則

具体的件数は新セッションでユーザーと協議。

#### 4-3. 情報源タグの義務化 (memory/feedback_no_fabrication.md 改訂)

miss_analysis 内の全主張に以下のいずれかのタグを付与:
- `[FETCH:URL]` = 当該 URL を WebFetch で本文取得した事実
- `[SEARCH]` = WebSearch スニペットレベル
- `[MEMORY]` = 記憶ベースの推論
- `[INFER]` = fetch/search の組合せからの導出推論
- タグなしの主張は不可

### 3.2 フェーズ5: 柱D 実装 (記録対象判断テーブル)

**改修対象ファイル**: `CLAUDE.md` (新設)

**サブタスク**:
- 「記録対象判断テーブル」セクション新設
- 「記録対象 / 参考記録 / 無視可」の判断基準を表形式で明文化
- scope の境界が曖昧なリーグ (例: ATP500 R1) はユーザー個別判断を仰ぐ運用を明記

具体的境界条件は新セッションでユーザーと協議して確定する。

### 3.3 フェーズ6: 統合動作確認

**変更ファイル**: なし (シミュレーションのみ)

**実施内容**:
1. 仮想的な「次の Session_63 開始時」を想定
2. 結果反映 → MISS 分析 → ルール提案 → 承認 → 実装までのワークフローを書き出し
3. Session_61 と比較して何がどう変わるかを明示
4. ユーザーが「想定通り」と承認した時点で 4本柱 実装作業 完了

### 3.4 フェーズ6 完了後の別タスク (A-3 遡及判断)

フェーズ6 完了承認後、別タスクとして以下を実施:
- R017 v2.0 取り消し / 承認 / 修正後再構築 の判断
- R024 v1.0 取り消し / 承認 / 修正後再構築 の判断
- P030 ID 衝突 (R024 → R025 等) の解消
- P031-P033 維持確認

判断時は `monitoring/session62_phase6_agenda.md` の議題1 (evidence の時間的独立性) も参照する。

### 3.5 Session_61 ペンディング事項 (4本柱 全フェーズ完了後に着手)

- C: 未反映 9試合 (TOR-CLE G4 / HOU-LAL G4 / Baptiste-Paolini / Pliskova-Mertens / Bristol-Newcastle / Northampton-Bath date 訂正 / Swiatek retire / Bondar-Svitolina / PHI G4 vs PIT)
- B: P030 rule_id 衝突解消 (上記 A-3 判断と統合実施)
- ready_to_implement: P020 → R014 (NRL) / P024 → N_NBA_new2 (NBA) implement 判断
- 既存 pending: PA092 (UCL SF lineups) / PA103 (UPSET_PICK_Lite 採否) / PA099 (NBA G3/G4 残) / lineups フィード再取得 / BACKLOG.md Session_60 残

---

## 4. 新セッションでの再開手順

### 4.1 新セッション開始時の必須読込

1. CLAUDE.md (新規追加された **【ルール改訂統制プロトコル】** + **【結果反映 STEP 0.5: scope外 UPSET スキャン SOP】** を含む最新版)
2. **本ファイル (`monitoring/session_62_phase1to3_handoff.md`)** ← 最初に読む
3. `monitoring/session_61_handoff.md` (Session_61 運用品質診断 v2 の完全リスト)
4. `monitoring/session62_phase6_agenda.md` (議題1: evidence 時間的独立性)
5. STEP 0 (health_check) 実行
6. STEP 1 必須ファイル群 (BACKLOG.md / user_feedback_log.md / pending_actions.md / claude_error_log.md / rule_pipeline.json / framework.json)

### 4.2 新セッション最初のタスク

**フェーズ4 着手から再開する**。具体的には以下の順序:

1. フェーズ4 着手前に、フェーズ4 の3サブタスク (4-1 MISS 重要度分類 / 4-2 fetch 件数規定 / 4-3 情報源タグ義務化) の各サブタスクで Claude が想定する具体的内容案をユーザーに提示し、承認を得る
2. ユーザー承認後、CLAUDE.md / memory への実装を実施
3. フェーズ4 完了報告 → ユーザー承認待ち
4. フェーズ5 (柱D) 着手
5. フェーズ5 完了報告 → ユーザー承認待ち
6. フェーズ6 (統合動作確認シミュレーション) 着手
7. フェーズ6 完了報告 → 4本柱 実装作業 完了
8. (別タスク) A-3 遡及判断・Session_61 ペンディング事項C/B 着手

### 4.3 新セッション着手時の禁止事項 (再掲)

- rules_*.json / records / upset_patterns.json への書き込み禁止 (フェーズ4-6 のメタルール改修のみ)
- Session_61 ペンディング事項 C (未反映 9試合) / B (R024→R025 再付番) は触れない
- 「ついでにこれもやっておきました」は禁止
- 各フェーズ完了時に必ずユーザー承認を待つ
- 不明点があれば実装を止めて質問

---

## 5. Session_62 フェーズ1〜3 で変更したファイル 完全リスト

git status で確認すべき変更ファイル:

| ファイル | 区分 | 変更種別 |
|---|---|---|
| `core/rule_pipeline.json` | B (承認必須) | 改訂 (instructions_for_claude + trigger_check_protocol) |
| `CLAUDE.md` | (メタルール) | 2セクション追加 (ルール改訂統制プロトコル / 結果反映 STEP 0.5) |
| `C:\Users\ohwada\.claude\projects\C--Users-ohwada-Desktop-claude-sport\memory\feedback_git_upload.md` | (memory) | 階層化ルール追記 |
| `C:\Users\ohwada\.claude\projects\C--Users-ohwada-Desktop-claude-sport\memory\MEMORY.md` | (memory) | description 更新 |
| `monitoring/session62_phase6_agenda.md` | (新規) | フェーズ6/A-3 議題リスト新設 |
| `monitoring/session_62_phase1to3_handoff.md` | (新規) | 本ファイル |

memory ファイルは git 管轄外 (Claude Code 内部 memory) のため、リポジトリ commit には含まれない点に注意。

---

**Session_62 フェーズ1〜3 終了**: 2026-04-27
**新セッション最優先**: フェーズ4 (柱C: 一次ソース fetch の義務化) のサブタスク内容案提示 → ユーザー承認 → 実装
