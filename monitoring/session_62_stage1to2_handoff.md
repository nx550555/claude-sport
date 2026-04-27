# Session_62 フェーズ4 ステージ1-2 引き継ぎサマリ

> **新セッション読込必須**: このファイルは Session_62 (2026-04-27) のフェーズ4 ステージ1-2 (柱C 4-1 MISS 重要度3段階分類 + 4-2 fetch 件数規定) で実施した変更の完全リストと、ステージ3 で残っている作業をまとめたもの。新セッションではステージ3 から再開する。

---

## 1. Session_62 全体構造の現在地

| フェーズ | 内容 | 実施状況 |
|---|---|---|
| フェーズ1 | 改修対象ファイルの現状把握 | ✅ 完了・ユーザー承認済 |
| フェーズ2 | 柱A: ルール自動実装の停止 → 承認制 | ✅ 完了・ユーザー承認済 |
| フェーズ3 | 柱B: scope外 UPSET スキャン SOP 化 | ✅ 完了・ユーザー承認済 |
| **フェーズ4 ステージ1** | **柱C 4-1: MISS 重要度3段階分類** | ✅ **完了・ユーザー承認済** |
| **フェーズ4 ステージ2** | **柱C 4-2: fetch 件数規定 (+ confidence_drift 2値化)** | ✅ **完了・ユーザー承認済** |
| フェーズ4 ステージ3 | 柱C 4-3: 情報源タグ義務化 | 🔴 **新セッションで実施** |
| フェーズ5 | 柱D: 記録対象判断テーブル明文化 | 🔴 新セッションで実施 |
| フェーズ6 | 統合動作確認 (シミュレーション) | 🔴 新セッションで実施 |

**重要原則 (Session_62 全期間共通)**:
1. 各ステージ/フェーズ完了時にユーザー承認を待つ
2. 既存の rules_*.json / records / upset_patterns.json への書き込みは本作業中は実施しない
3. 不明点があれば実装を止めて質問
4. 「ついでにこれもやっておきました」は禁止
5. Session_61 ペンディング事項 (未反映 9試合 / R024→R025 再付番 / ready_to_implement P020/P024) は **4本柱 全フェーズ完了まで一切手を付けない**

---

## 2. フェーズ4 ステージ1-2 で変更したファイル 完全リスト

### 2.1 ステージ1 (柱C 4-1 MISS 重要度3段階分類)

| # | ファイル | 変更概要 |
|---|---|---|
| 1 | `CLAUDE.md` | L548 直後・L552「【絶対禁止】架空情報の生成」直前に **【柱C: 一次ソース fetch 義務化】** セクション新設。冒頭部 + 4-1 部分 (Class A/B/C 判定条件 + confidence_drift 枠組み + miss_class フィールド付与ルール + v3.0 整合性) を実装。4-2/4-3 はステージ2/3 で追記予定の placeholder のみ |
| 2 | `memory/feedback_miss_analysis_depth.md` | 末尾に「Session_62 フェーズ4 追加 (2026-04-27): MISS 重要度3段階分類」セクション追記 (Class 別判定条件 + confidence_drift + Why + How to apply、既存5ステップ手順との Mapping) |
| 3 | `monitoring/session62_phase6_agenda.md` | 議題3「confidence_drift 種目別閾値の確定」を追加。テニス/NHL/NBA/MLB/サッカー/NFL/ラグビー全種の薄勝ち基準候補をフェーズ6 確定用に列挙 |
| 4 | `MEMORY.md` (memory index) | feedback_miss_analysis_depth エントリ description を「Session_62 フェーズ4 4-1 反映」に更新 |

### 2.2 ミニタスク (ステージ2 着手前): confidence_drift 2値化

| # | ファイル | 変更概要 |
|---|---|---|
| 1 | `CLAUDE.md` | 4-1 セクション内 `confidence_drift` フィールド定義を `"high" | "low" | null` 3値 → `"high" | null` 2値に変更。`"low"` は本フェーズで未定義のため不採用、フェーズ6 / 別タスクで再設計 |
| 2 | `memory/feedback_miss_analysis_depth.md` | 同上の同期修正 |

### 2.3 ステージ2 (柱C 4-2 fetch 件数規定)

| # | ファイル | 変更概要 |
|---|---|---|
| 1 | `CLAUDE.md` | 4-2 placeholder を実体化。Class 別 WebFetch 必須件数表 (A=3 / B=2 / C=1 / drift=B 相当) + ソース内訳必須要件 + WebSearch スニペット原則 (fetch カウント対象外) + fetcher 経由カウント条件 (鮮度 OK + feed_status OK で WebFetch 1件相当) + fetch 失敗時 3回試行 + `[FETCH_FAILED]` タグ (具体仕様ステージ3 で定義) + `investigation_status: "investigation_incomplete"` 規定 + investigation_incomplete のまま evidence 加算禁止 (柱A 整合) + 一次ソース推奨リスト 16種目分 |
| 2 | `memory/feedback_miss_analysis_depth.md` | 末尾に「Session_62 フェーズ4 追加 (2026-04-27): fetch 件数規定」セクション追記 |
| 3 | `MEMORY.md` (memory index) | feedback_miss_analysis_depth エントリ description を「Session_62 フェーズ4 4-1+4-2 反映」に再更新 |

### 2.4 git commit 構成

ステージ1+2 を論理単位 (柱C 上半分) として 2 commit に統合:

| commit | message | 含むファイル |
|---|---|---|
| 1 | `Session_62 phase4 stages1-2: 柱C 4-1 + 4-2` | `CLAUDE.md` |
| 2 | `Session_62 phase4 stages1-2 monitoring` | `monitoring/session62_phase6_agenda.md` + `monitoring/session_62_stage1to2_handoff.md` (本ファイル) |

memory ファイル (`feedback_miss_analysis_depth.md` / `MEMORY.md`) は Claude Code 内部の git 管轄外のため、リポジトリ commit には含まれない。

---

## 3. フェーズ4 13論点の確定内容 (一括参照)

### サブタスク 4-1: MISS 重要度3段階分類

| # | 論点 | 確定 |
|---|---|---|
| Q1 | 重要度分類段階数 | **3段階 (Class A / B / C)** |
| Q2 | confidence_drift フラグ導入是非 | **導入** (枠組みのみ。種目別閾値は議題3 でフェーズ6 確定) |
| Q3 | confidence_drift の薄勝ち閾値 (種目別) | **TBD: フェーズ6 で確定** |
| Q4 | scope外UPSET の Class 帰属 | **Class C 内包** |

判定条件 (確定):
- **A: 高重要度** = `tier ∈ {go, upset_pick}` の MISS (実損失あり)
- **B: 中重要度** = `tier ∈ {caution, caution_margin, provisional_go}` の MISS / `quadrant=Q3_output_a` (conf≥85%) の MISS / `confidence_drift=high` の HIT
- **C: 低重要度** = `tier=skip` の MISS / `quadrant=Q3_mid` (80≤conf<85%) の MISS / `quadrant=Q4_upset_watch` HIT / scope外UPSET (records 未登録だが市場fav≤1.50 敗戦)

confidence_drift フィールド:
- 値: `"high" | null` (2値構造、`"low"` は不採用 — ミニタスクで決定)
- 判定基準: 推定勝率 ≥ 80% で予想したのに接戦/僅差勝利
- 種目別具体閾値は **議題3** でフェーズ6 確定

miss_class 付与:
- 新規 `prediction_hit=false` エントリのみ
- 値: `"A"` / `"B"` / `"C"` の3値必須 (空・null 禁止)
- 既存 records 100件超への遡及付与なし

### サブタスク 4-2: fetch 件数規定

| # | 論点 | 確定 |
|---|---|---|
| Q1 | 規定方式 | **件数+種別 (両方規定)** |
| Q2 | Class 別件数 | **A=3 / B=2 / C=1** |
| Q3 | 失敗時運用 | **3回試行 + [FETCH_FAILED] フラグ** |
| Q4 | fetcher 経由カウント | **WebFetch 1件相当 + [FETCHER:src] 別タグ扱い** |
| Q5 | investigation_incomplete のまま evidence 加算 | **禁止** (柱A 整合) |

ソース内訳必須要件:
- A: 公式試合レポート 1 / 詳細スタッツ 1 / コメント or ニュース 1
- B: 公式試合レポート 1 / 詳細スタッツ or ニュース 1
- C: 公式試合レポート or 信頼スタッツ 1
- HIT confidence_drift=high: B 相当

WebSearch スニペット原則:
- fetch カウント対象外 (補助情報のみ)
- WebFetch で本文取得した URL のみ有効カウント
- 理由: スニペットは前後文脈省略・正確性検証不可・Week/Round/日付混同リスク (CE013 再発)

fetcher 経由カウント条件:
- `--days-stale` 規定内 (鮮度 OK)
- `stats_feed_reader.feed_status()` で OK 判定
- タグは `[FETCHER:src]` で別タグ扱い (具体仕様ステージ3)

fetch 失敗時 3回試行:
1. 同種別の代替ソース 1件試行
2. 別種別ソース 1件試行
3. 計3回未達 → `[FETCH_FAILED:URLs]` タグ + `investigation_status: "investigation_incomplete"` + 次セッション再試行を pending_actions.md 登録

### サブタスク 4-3: 情報源タグ義務化 (ステージ3 で実装)

| # | 論点 | 確定 |
|---|---|---|
| Q1 | タグ仕様 | **5種 ([FETCH:URL] / [FETCHER:src] / [SEARCH] / [MEMORY] / [INFER])** |
| Q2 | タグ付与単位 | **主張ごと** |
| Q3 | タグなし主張の扱い | **禁止** (CHECK-2 + health_check 両方で検証) |
| Q4 | 遡及適用範囲 | **新規のみ** (既存 records / evidence は対象外) |
| Q5 | 準拠チェック | **両方併用** (CHECK-2 + health_check `miss_analysis_tag_compliance`) |
| Q6 | scripts 自動化 | **本フェーズ範囲内**: CLAUDE.md / memory に「セッション固有スクリプト (`_sessionXX_*.py`) 生成時にもタグ義務」と明記。既存 `_session61_*.py` 3本は使い捨てのため改修対象外 |

[INFER] 記法:
- `[INFER]` のみ (ネスト記法 `[INFER:[FETCH:url]]` は不採用)
- 同段落内の先行 FETCH/SEARCH タグを根拠とする運用

---

## 4. ユーザー確認待ち事項3 への回答 (ステージ3 着手時の前提として記録)

### fangraphs proxy 値の扱い

ステージ2 で確認した「fangraphs `wRC_plus_is_proxy=true` フラグ付きデータ等の proxy 値を fetcher 経由カウントとして同等扱いするか」への回答:

**ステージ3 で `[FETCHER:src:proxy]` 等の別タグとして区別する方針** で詳細定義する。

具体的にステージ3 で定義する内容:
- `[FETCHER:src]` = 通常の構造化スタッツデータ (一次計算値)
- `[FETCHER:src:proxy]` = proxy / 計算由来の値 (`wRC_plus_is_proxy=true` / `FIP_is_computed=true` 等のフラグ付きデータ)
- 件数カウントは同等 (WebFetch 1件相当) だが、根拠の信頼性が proxy であることを明示
- 適用例: fangraphs (StatsAPI 経由 wRC+ proxy) / fetch_fangraphs.py の Cloudflare 突破不可で StatsAPI 切替したデータ

---

## 5. ステージ3 で残っている作業

### 改修対象ファイル (6ファイル)

| # | ファイル | 変更概要 |
|---|---|---|
| 1 | `CLAUDE.md` | 【柱C】4-3 placeholder を実体化。5種タグ仕様 + `[FETCH:URL]` / `[FETCHER:src]` (+ `[FETCHER:src:proxy]`) / `[SEARCH]` / `[MEMORY]` / `[INFER]` 定義 + 主張ごと付与ルール + タグなし禁止 + 良い例/悪い例 + CHECK-2 連携 + セッション固有スクリプト生成時のタグ義務 + `[FETCH_FAILED]` 詳細仕様 |
| 2 | `memory/feedback_no_fabrication.md` | Session_62 フェーズ4 4-3 追加セクション末尾追記。5種タグ仕様 + 良い例/悪い例 + 遡及適用範囲 (新規のみ) |
| 3 | `memory/feedback_result_verification.md` | 整合性確認のみ (5種タグ運用と既存「一次ソース2つ + WebFetch 明示スコア確認」プロトコルの矛盾なきこと検証 → 不整合なら最小限追記) |
| 4 | `monitoring/health_check.py` | 新検査項目 `miss_analysis_tag_compliance` を実装。records/*.json の miss_analysis フィールドを走査しタグなし主張を機械検出 → WARN/FAIL 化 |
| 5 | `core/rule_pipeline.json` | `instructions_for_claude` に1項目追加: 「(Session_62 2026-04-27 フェーズ4 追加) evidence 配列への追加時、各 evidence エントリの記述は CLAUDE.md『柱C: 一次ソース fetch 義務化』の 5種タグ仕様 ([FETCH:URL] / [FETCHER:src] / [SEARCH] / [MEMORY] / [INFER]) に従うこと。タグなし主張の evidence 加算は禁止。」 |
| 6 | `MEMORY.md` (memory index) | feedback_no_fabrication エントリ description を「Session_62 フェーズ4 4-3 反映」に更新 |

### ステージ3 改修対象外 (再強調)

- `core/rules_*.json` (R*** / N*** / W*** / M*** / S*** ルール本体) — B区分・承認必須
- `core/framework.json` — B区分・承認必須・本フェーズで触らないこと **再強調**
- `core/dashboard_stats.json` / `dashboard.html` — 表示拡張は別タスク
- `records/{sport}/*.json` — 試合記録への遡及付与なし
- `stats/upset_patterns.json` — 既存 evidence への遡及付与なし
- `scripts/_session*_*.py` 全て — 使い捨てスクリプトのため対象外 (確定)
- BACKLOG.md / session_logs/

### ステージ3 着手前のユーザー承認プロセス

ステージ1-2 と同様、以下の手順で進める:

1. ステージ3 着手指示を受領
2. 不明点があれば実装前に質問 (今回は `[FETCHER:src:proxy]` の具体仕様を含む)
3. 6ファイル変更を順次実施
4. 完了報告 (出力フォーマット: 変更ファイル / 差分要約 / 自己点検 / ユーザー確認待ち事項)
5. ユーザー承認待ち
6. 承認後にフェーズ5 着手

---

## 6. confidence_drift 2値化の経緯記録

### 経緯

ステージ1 完了時、ユーザー側から「`"low"` の意味が現時点で未定義」との指摘を受領。ステージ2 着手前のミニタスクとして判断を求められた。

### Claude Code の判断

**`"high" | null` 2値構造を採用** (代替案「`"low"` を残し将来の拡張用と注記」は不採用)。

理由:
1. 現時点で `"low"` の判定基準・運用意図が未定義
2. 未使用 enum 値を残すと形骸化リスクあり
3. YAGNI 原則: 必要になった時点で再導入する方が保守コスト低い
4. フェーズ6 で薄勝ち閾値を確定する際、`"low"` 側の意味も同時に再設計するほうが整合性が高い

### `"low"` 再導入のタイミング

- フェーズ6 統合動作確認時 (議題3 confidence_drift 種目別閾値確定と同時)
- または別タスクで「強い側が予想より大差で勝った場合の追跡」が必要になった時点
- いずれの場合も新たな判定基準・運用意図の議論を経てから再導入する

---

## 7. Session_61 由来の未 commit ファイル 12件 — 凍結継続

ステージ1-2 でも触れず、ステージ3 でも触れない。**4本柱 全フェーズ完了後** の A-3 遡及判断で扱う。

### 凍結対象 12件

**Modified (8件)**:
- `core/dashboard_stats.json`
- `core/rules_tennis.json` (R017 v2.0 + R024 v1.0 追加で v2.5)
- `dashboard.html`
- `records/mlb/2026.json`
- `records/nrl/2026.json`
- `records/soccer/2025-26.json`
- `records/tennis/2026-ATP.json`
- `stats/upset_patterns.json` (A036-A043 追加で 41件)

**Untracked (4件)**:
- `monitoring/session_61_handoff.md`
- `scripts/_session61_writeback.py`
- `scripts/_session61_rule_feedback.py`
- `scripts/_session61_phase2_upsets.py`

### 4本柱完了後の別タスク内容 (再掲)

- R017 v2.0 取り消し / 承認 / 修正後再構築 の判断
- R024 v1.0 取り消し / 承認 / 修正後再構築 の判断
- P030 ID 衝突 (R024 → R025 等) の解消
- P031-P033 維持確認
- 議題1 (evidence の時間的独立性) を判断時に参照
- ready_to_implement: P020 → R014 (NRL) / P024 → N_NBA_new2 (NBA)
- 既存 pending: PA092 / PA103 / PA099 / lineups フィード再取得 / BACKLOG.md Session_60 残

---

## 8. 新セッションでの再開手順

### 8.1 新セッション開始時の必須読込

1. CLAUDE.md (柱A + 柱B + 柱C 4-1+4-2 を含む最新版)
2. **本ファイル (`monitoring/session_62_stage1to2_handoff.md`)** ← 最初に読む
3. `monitoring/session_62_phase1to3_handoff.md` (フェーズ1-3 完了サマリ)
4. `monitoring/session_61_handoff.md` (Session_61 運用品質診断 v2)
5. `monitoring/session62_phase6_agenda.md` (議題1: evidence 時間的独立性 / 議題2: STEP 0.5 実施保証 / 議題3: confidence_drift 種目別閾値)
6. STEP 0 (health_check) 実行
7. STEP 1 必須ファイル群 (BACKLOG.md / user_feedback_log.md / pending_actions.md / claude_error_log.md / rule_pipeline.json / framework.json)

### 8.2 新セッション最初のタスク

**ステージ3 着手から再開する**。具体的な順序:

1. ステージ3 着手前に、6ファイル変更内容の具体案 (`[FETCHER:src:proxy]` 詳細 + health_check 実装方針 + rule_pipeline.json 追記文言 + 良い例/悪い例 等) をユーザーに提示し承認を得る
2. ユーザー承認後、6ファイルへの実装を順次実施
3. ステージ3 完了報告 → ユーザー承認待ち
4. フェーズ5 (柱D 記録対象判断テーブル) 着手前の具体案提示
5. フェーズ5 完了報告 → ユーザー承認待ち
6. フェーズ6 (統合動作確認) 着手
7. フェーズ6 完了報告 → 4本柱 実装作業 完了
8. (別タスク) A-3 遡及判断・Session_61 ペンディング事項 着手

### 8.3 新セッション着手時の禁止事項 (再掲)

- rules_*.json / records / upset_patterns.json への書き込み禁止 (ステージ3 / フェーズ5/6 のメタルール改修のみ)
- core/framework.json は本フェーズで一切触らない (再強調)
- Session_61 ペンディング事項 12件は 4本柱完了まで凍結継続
- 「ついでにこれもやっておきました」は禁止
- 各ステージ/フェーズ完了時に必ずユーザー承認を待つ
- 不明点があれば実装を止めて質問

---

**Session_62 フェーズ4 ステージ1-2 終了**: 2026-04-27
**新セッション最優先**: ステージ3 (柱C 4-3 情報源タグ義務化) の具体案提示 → ユーザー承認 → 6ファイル変更実装
