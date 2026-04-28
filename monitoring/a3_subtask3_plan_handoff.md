# A-3 サブタスク3 分割計画 + セッション1 (テニス系4件) 着手向け 引継ぎサマリ

> **新セッション読込必須**: 本ファイルは A-3 遡及判断タスク サブタスク3 (Session_61 9件振り分け実施) の **進め方確定** をもって、新セッションでセッション1 (テニス系4件) に着手するための引継ぎサマリ。新セッションでは本ファイルを最初に読み込んだ後、セッション1 (テニス系) から作業を継続する。

---

## 1. A-3 サブタスク3 全体構造 (9件の振り分け対象)

サブタスク3 は Session_61 で検出された scope外UPSET 9件を、柱D サブセクション9 テーブルに従って各 records ファイル / upset_patterns.json へ振り分け登録するタスク。

### 1.1 9件の試合データ + 推奨区分 + 登録先 (再掲)

| # | 試合 | 推奨区分 | match_status | 登録先 |
|---|---|---|---|---|
| 1 | Bristol 52-19 Newcastle Premiership | 区分1 (full_record) | completed | `records/premiership/2026.json` (新規エントリ追加) |
| 2 | Northampton 41-38 Bath Premiership | 区分1 (full_record) | completed | `records/premiership/2026.json` (既存エントリの date 訂正 4/26→4/25) |
| 3 | Swiatek retire vs Li Madrid R3 | **区分2 (reference_only)** | retired | `stats/upset_patterns.json` のみ (records 本体未登録) |
| 4 | Bondar d. Svitolina (#7 seed) Madrid R2 | 区分1 (full_record) | completed | `records/wta/2026.json` (新規エントリ追加) |
| 5 | PHI G4 vs PIT (NHL Playoffs) | 区分1 (full_record) | completed | `records/nhl/2025-26.json` (新規エントリ追加) |
| 6 | TOR 93-89 CLE G4 (NBA Playoffs) | 区分1 (full_record) | completed | `records/nba/2025-26.json` (新規エントリ追加) |
| 7 | HOU 115-96 LAL G4 (NBA Playoffs) | 区分1 (full_record) | completed | `records/nba/2025-26.json` (新規エントリ追加) |
| 8 | Baptiste d. Paolini Madrid R3 | 区分1 (full_record) | completed | `records/wta/2026.json` (新規エントリ追加) |
| 9 | Pliskova(Q) d. Mertens(#19) Madrid R3 | 区分1 (full_record) | completed | `records/wta/2026.json` (新規エントリ追加) |

### 1.2 区分別件数

| 区分 | 件数 |
|---|---|
| 区分1 (full_record) | 8件 (#1, 2, 4, 5, 6, 7, 8, 9) |
| 区分2 (reference_only) | 1件 (#3 Swiatek retire) |
| 区分3 (skip_record) | 0件 |

### 1.3 登録先ファイル別の処理件数

| 登録先ファイル | ファイル現状 | 新規追加件数 | 既存訂正件数 | 合計 |
|---|---|---|---|---|
| `records/premiership/2026.json` | 既存 (確認済) | 1件 (#1 Bristol-Newcastle) | 1件 (#2 Northampton-Bath date 訂正) | 2件 |
| `records/wta/2026.json` | 既存 (確認済 / top keys: sport, season, bet_type, rule_version, started, summary, tournaments, screening_log, last_updated) | 3件 (#4 Bondar / #8 Baptiste / #9 Pliskova) | 0件 | 3件 |
| `records/nhl/2025-26.json` | 既存 (確認済) | 1件 (#5 PHI G4) | 0件 | 1件 |
| `records/nba/2025-26.json` | 既存 (確認済) | 2件 (#6 TOR-CLE G4 / #7 HOU-LAL G4) | 0件 | 2件 |
| `stats/upset_patterns.json` | 既存 (Modified / A036-A043 で 41件状態) | 1件 (#3 Swiatek retire を A042 or A044 等として追加) | 0件 | 1件 |
| **合計** | — | **8件** | **1件** | **9件** |

> **重要**: 全ての対象ファイルは既存。「新規ファイル設計」は不要 — 既存スキーマに準拠して追記する運用とする。

---

## 2. 分割計画 (4セッション構成)

サブタスク3 は実装工程が多いため、種目ごとに4セッションに分割して処理する (選択肢B 採用)。

| セッション | 対象 | 件数 | 登録先ファイル |
|---|---|---|---|
| **セッション1** | **テニス系 4件** (Swiatek retire + WTA Madrid 3件) | 4件 | `stats/upset_patterns.json` + `records/wta/2026.json` |
| セッション2 | ラグビー 2件 (Premiership) | 2件 | `records/premiership/2026.json` |
| セッション3 | NBA Playoffs 2件 | 2件 | `records/nba/2025-26.json` |
| セッション4 | NHL Playoffs 1件 | 1件 | `records/nhl/2025-26.json` |

**着手順序の根拠**:
- セッション1 (テニス系) を先行: 既存 P007 evidence (U007 / U007_R2 / A041) との整合性確認が必要 + 件数最多 (4件) でスキーマ確認の機会大
- セッション2〜4 は独立処理可能 (種目間の整合性影響なし)

---

## 3. セッション1 (テニス系 4件) の詳細

### 3.1 各試合の登録先・想定 prediction・想定 hit・想定 miss_class

| # | 試合 | 登録先 | 想定 predicted_winner | 想定 prediction_hit | 想定 miss_class | UPSET 性質 / 備考 |
|---|---|---|---|---|---|---|
| **3** | Swiatek retire vs Li Madrid R3 | `stats/upset_patterns.json` のみ | (区分2 のため tier / predicted_winner 設定不要 or 任意) | retire のため判定対象外 | 任意 (UPSET 性質追跡用に "C" 付与可) | Swiatek (#1 シード) retire は UPSET 性質。試合中 retire か出場前 retire かで match_status が retired or walkover に分岐 |
| **4** | Bondar d. Svitolina (#7 seed) Madrid R2 | `records/wta/2026.json` (新規) | Svitolina (#7 seed / 市場fav想定) | false (UPSET MISS) | C 想定 (scope外UPSET 由来 / tier=skip 相当) | #7 seed Svitolina 敗退。Bondar (qualifier or low seed) 勝利 |
| **8** | Baptiste d. Paolini Madrid R3 | `records/wta/2026.json` (新規) | Paolini (市場fav) | false (UPSET MISS) | C 想定 (scope外UPSET 由来) | A041 evidence の元試合 (P007 candidates U007 / U007_R2 / A041 の3件目)。R024 取り消し済のため、本サブタスク3 では R024 適用なしで予測 |
| **9** | Pliskova(Q) d. Mertens(#19) Madrid R3 | `records/wta/2026.json` (新規) | Mertens (#19 / 市場fav想定) | false (UPSET MISS) | C 想定 (scope外UPSET 由来) | #19 Mertens 敗退。Pliskova(Q) qualifier 勝利 |

### 3.2 wta/2026.json 既存スキーマの構造

`records/wta/2026.json` は既存ファイル。確認済の top-level キー:

```
sport / season / bet_type / rule_version / started / summary /
tournaments / screening_log / last_updated
```

**スキーマ設計指針**:
- 新規エントリ追加先は `tournaments` 配列内の Madrid 大会エントリ (or `tournaments` 配下のラウンド階層) と推定
- フィールド構造は既存エントリ (例: Stuttgart 2026 R1/R2 / Rouen 2026 / Madrid R1/R2 既存試合) に準拠
- セッション1 着手時に該当ファイルを Read で開き、Madrid 大会エントリの構造を確認してから追記する
- `screening_log` 末尾に「Session_64 サブタスク3 セッション1 で Bondar / Baptiste / Pliskova 3件の遡及登録」記録を追加

### 3.3 区分2 (Swiatek retire) の特殊処理

| 項目 | 規定 / 判断 |
|---|---|
| **登録先** | `stats/upset_patterns.json` のみ (records 本体には登録しない) |
| **必須フィールド** | `record_class: "reference_only"` / `match_status: "retired"` (柱D サブセクション3 規定) |
| **prediction_hit 判定** | retire のため判定対象外 → `prediction_hit` フィールド自体を **付与しない** or `null` のいずれかを選択 (柱C 4-1 規定上は付与不要) |
| **step05_scanned_at 付与可否** | 柱B サブセクション2 ステップ7 規定は「prediction_hit を `true`/`false` に確定する全エントリに対し付与必須」 — retire で `prediction_hit` が確定しないなら **付与不要** と解釈。ただし区分2 でも upset_patterns 登録時刻として付与するなら任意付与可 |
| **miss_class 付与** | retire のため判定対象外 → 付与不要 (柱C 4-1 規定: 「prediction_hit=false エントリのみ対象」) |
| **タグ義務** | 適用 (簡略可) (柱D サブセクション7 整合性表より) → 5種タグを miss_analysis_text 等の記述箇所に付与 |
| **fetch 件数** | 区分2 = Class C 相当 (1件以上) |

**判断保留事項** (セッション1 着手時にユーザー確認):
- step05_scanned_at の付与可否 (柱B 規定の文言厳密解釈)
- match_status の選択 (試合中 retire = retired / 出場前 retire = walkover の確認)

### 3.4 Class 別 fetch 件数規定 (柱C 4-2)

| Class | サブタスク3 該当度 | 必要 WebFetch 件数 | サブタスク3 セッション1 想定 |
|---|---|---|---|
| **Class A** | tier ∈ {go, upset_pick} の MISS | 3件 (公式試合レポート + 詳細スタッツ + 選手・監督コメント) | 該当なし (本サブタスク3 で tier=skip 相当に設定予定) |
| **Class B** | tier ∈ {caution, caution_margin, provisional_go} の MISS / Q3_output_a (conf≥85%) の MISS | 2件 (公式試合レポート + 詳細スタッツ or ニュース) | 該当ありうる (Q3_output_a 条件次第) |
| **Class C** | tier=skip の MISS / Q3_mid (80≤conf<85%) の MISS / Q4_upset_watch HIT / **scope外UPSET** | 1件 (公式試合レポート or 信頼スタッツ) | **基本これに該当** (scope外UPSET 由来) |

→ セッション1 4件のうち、**Swiatek retire (区分2) + WTA Madrid 3件 (区分1 / Class C 想定)** は **WebFetch 1件以上** が最低要件。

#### 推奨一次ソース (柱C 4-2 リストより)

| 種目 | 公式試合レポート | 詳細スタッツ | コメント / ニュース |
|---|---|---|---|
| WTA テニス | wtatennis.com | tennisabstract.com (Women's) | espn.com / theathletic.com |

セッション1 で参照する具体的 URL は着手時に WebSearch で発見 → WebFetch で本文取得。

### 3.5 5種タグ義務化規定 (柱C 4-3)

セッション1 で追加する全エントリ (区分1 3件 + 区分2 1件) の miss_analysis (区分1) / miss_analysis_text (区分2) に **5種タグ義務適用**。

| タグ | 用途 | 件数カウント |
|---|---|---|
| `[FETCH:URL]` | WebFetch 本文取得済 URL を引用 | Class 別 fetch 件数の有効 1件 |
| `[FETCHER:src]` | 構造化スタッツ (鮮度 OK + feed_status OK) | WebFetch 1件相当 |
| `[FETCHER:src:proxy]` | proxy / 計算由来の値 (フラグ付き) | WebFetch 1件相当 |
| `[SEARCH]` | WebSearch スニペットレベル根拠 | カウント対象外 |
| `[MEMORY]` | 記憶ベース推論 | カウント対象外 / evidence 化禁止 |
| `[INFER]` | fetch / search からの導出推論 | カウント対象外 |

**タグ付与の粒度ガイドライン (議題4 解釈B)**:
- 同一 source 段落末1タグ可 (原則)
- 但し書き①: source 異なる主張は別タグ必須
- 但し書き②: INFER と FETCH/FETCHER/SEARCH 混在は両方タグ必須
- 但し書き③: 否定主張も事実根拠なら別タグ必須
- 但し書き④: INFER 連鎖は末尾1タグ可
- 短い接続句 (10文字未満) はカウント対象外

### 3.6 セッション1 着手時の作業フロー

1. **準備フェーズ**: 4試合の結果情報を WebSearch で発見 → WebFetch で本文取得 (Class C 規定の最低 1件以上 / より望ましい場合は 2件以上)
2. **段階1: 区分2 (Swiatek retire) の登録**:
   - `stats/upset_patterns.json` を Read で開き、A042 or A044 等の新規エントリ ID を決定 (既存 A036-A043 の最終 ID 確認後)
   - エントリ追加: `record_class: "reference_only"` / `match_status: "retired"` (or "walkover" 要確認) / 5種タグ付与
3. **段階2: 区分1 (Bondar / Baptiste / Pliskova) 3件の登録**:
   - `records/wta/2026.json` を Read で開き、Madrid 大会エントリの構造を確認
   - 各エントリに必須付与: `record_class: "full_record"` / `match_status: "completed"` / `step05_scanned_at: "<ISO 8601 UTC>"` / `prediction_hit: false` / `miss_class: "C"` (想定) / `miss_analysis` テキストに 5種タグ
4. **段階3: 必須付与フィールド検証**: 全 4エントリで record_class / match_status / step05_scanned_at / miss_class / 5種タグ揃いを目視 + grep 検証
5. **段階4: health_check.py 通過確認**: 13項目目 (`step05_scan_compliance`) + 12項目目 (`miss_analysis_tag_compliance`) が OK 維持を確認
6. **段階5: commit + push**: 「A-3 sub3 session1: テニス系4件 振り分け登録 (Swiatek retire 区分2 + WTA Madrid R2/R3 3件 区分1)」として 1 commit にまとめる
   - 注: dashboard / cumulative への反映はサブタスク4 / 8 で別途実施 (本セッションでは凍結維持)

### 3.7 セッション1 の重要な注意事項 (再掲)

- **タグ付与必須**: 全 miss_analysis / miss_analysis_text に 5種タグ義務適用
- **step05_scanned_at 必須**: 区分1 3件は prediction_hit 確定時に同時付与 / 区分2 1件は付与可否を着手時に判断
- **記憶ベース推論禁止**: Madrid altitude (1500m) 等の記憶ベース主張は `[MEMORY]` タグでのみ記述可・evidence 化禁止
- **fetch 失敗時**: 3回試行で規定件数未達なら `[FETCH_FAILED:URL1,URL2,URL3]` + `investigation_status: "investigation_incomplete"` 付与
- **R024 取り消し整合性**: Baptiste-Paolini Madrid R3 の予測再構成時、R024 (form slump 補正 -10%) は **適用しない** (取り消し済)。元の cElo +201pt 由来 conf 76% で記録するか、Session_61 当時の SKIP 判断 (R024 適用 conf 66%) を「予測時点の正当性尊重」として記録するかは着手時に判断

---

## 4. セッション2〜4 の概要 (本サマリでは詳細記載不要)

各セッション着手時に詳細化する。本サマリでは概要のみ。

### セッション2: ラグビー 2件 (Premiership)
- **対象**: #1 Bristol 52-19 Newcastle (区分1 新規) + #2 Northampton 41-38 Bath (区分1 既存 date 訂正 4/26→4/25)
- **登録先**: `records/premiership/2026.json` (既存)
- **特殊処理**: #2 Northampton-Bath は date 訂正のみ (新規エントリ追加なし)
- **5種タグ + Class 別 fetch 件数**: #1 Bristol-Newcastle は Class C 想定 (1件以上)
- **着手時に詳細化**

### セッション3: NBA Playoffs 2件
- **対象**: #6 TOR 93-89 CLE G4 + #7 HOU 115-96 LAL G4
- **登録先**: `records/nba/2025-26.json` (既存)
- **特殊処理**: 両者とも市場fav 敗戦 (CLE / LAL) → Class C 想定 (scope外UPSET 由来)
- **着手時に詳細化**

### セッション4: NHL Playoffs 1件
- **対象**: #5 PHI G4 vs PIT
- **登録先**: `records/nhl/2025-26.json` (既存)
- **特殊処理**: 試合結果と prediction_hit の判定が必要 (UPSET 性質の有無は結果次第)
- **着手時に詳細化**

---

## 5. 凍結対象 11件の現状 (サブタスク3 で順次解消開始)

### Modified 7件 (引き続き未 commit 維持)

| ファイル | 内容 | 処理予定セッション |
|---|---|---|
| `core/dashboard_stats.json` | Session_61 で更新分 | サブタスク4 (整合性確保 commit) |
| `dashboard.html` | Session_61 で更新分 | サブタスク4 / サブタスク8 |
| `records/mlb/2026.json` | Session_61 で更新分 | サブタスク4 |
| `records/nrl/2026.json` | Session_61 で更新分 (A039 Manly MISS 含む) | サブタスク4 / サブタスク6 |
| `records/soccer/2025-26.json` | Session_61 で更新分 | サブタスク4 |
| `records/tennis/2026-ATP.json` | Session_61 で更新分 (A037 Vacherot Madrid R2 / A038 Shapovalov 等) | サブタスク3 セッション1 (関連箇所のみ) / サブタスク4 |
| `stats/upset_patterns.json` | A036-A043 で 41件 (Swiatek retire = サブタスク3 セッション1 で区分2 登録予定) | **サブタスク3 セッション1** / サブタスク4 |

### Untracked 4件 (引き続き未 commit 維持)

| ファイル | 処理予定セッション |
|---|---|
| `monitoring/session_61_handoff.md` | サブタスク5 |
| `scripts/_session61_phase2_upsets.py` | サブタスク5 |
| `scripts/_session61_rule_feedback.py` | サブタスク5 |
| `scripts/_session61_writeback.py` | サブタスク5 |

### サブタスク3 でファイル状態が変動するもの

| ファイル | 現状 | サブタスク3 セッション後の予想状態 |
|---|---|---|
| `stats/upset_patterns.json` | Modified (A036-A043 41件) | セッション1 で +1 (Swiatek retire) → 42件 |
| `records/wta/2026.json` | (clean) | セッション1 で Modified (Bondar / Baptiste / Pliskova の 3件追加) |
| `records/premiership/2026.json` | (clean) | セッション2 で Modified (Bristol-Newcastle 追加 + Northampton-Bath date 訂正) |
| `records/nba/2025-26.json` | (clean) | セッション3 で Modified (TOR-CLE / HOU-LAL の 2件追加) |
| `records/nhl/2025-26.json` | (clean) | セッション4 で Modified (PHI G4 1件追加) |

---

## 6. 新セッション再開手順 (セッション1 テニス系 4件 着手向け)

### 6.1 新セッション開始時の必須読込

1. **CLAUDE.md** (柱A + 柱B + 柱C 4-1+4-2+4-3 + 柱D 含む最新版)
2. **本ファイル (`monitoring/a3_subtask3_plan_handoff.md`)** ← 最初に読む
3. `monitoring/a3_subtask1to2_handoff.md` (A-3 サブタスク1+2 完了状態 + サブタスク3 全体詳細)
4. `monitoring/session_62_complete_handoff.md` (Session_62 全体総括 + 4本柱最終確定状態)
5. `monitoring/session_61_handoff.md` (Session_61 由来 12件詳細 + 9件 振り分け案の元情報)
6. STEP 0 (`PYTHONIOENCODING=utf-8 python monitoring/health_check.py`) 実行 — 12項目 OK + WARN 既存 + ALERT 0件確認
7. STEP 1 必須ファイル群 (BACKLOG.md / user_feedback_log.md / pending_actions.md / claude_error_log.md / rule_pipeline.json / framework.json)

### 6.2 新セッション最初のタスク (セッション1 テニス系 4件 着手)

§3.6 の作業フローに従う。要約:

1. 4試合の結果情報を WebSearch + WebFetch で一次確認 (Class C = 1件以上 / 望ましくは 2件以上)
2. 段階1: 区分2 (Swiatek retire) → upset_patterns.json に追加
3. 段階2: 区分1 (Bondar / Baptiste / Pliskova) 3件 → wta/2026.json に追加
4. 段階3: 必須付与フィールド検証
5. 段階4: health_check.py 通過確認
6. 段階5: commit + push

### 6.3 新セッション着手時の禁止事項 (再掲)

- 4本柱本体 (柱A / 柱B / 柱C / 柱D) の規定本体への変更禁止
- `core/framework.json` / `core/rules_*.json` (取り消し済) は触らない (凍結維持)
- `core/dashboard_stats.json` / `dashboard.html` / `cumulative.json` への書き込み禁止 (サブタスク4 / 8 で別途実施)
- セッション1 範囲外の records ファイル (premiership / nhl / nba / mlb / nrl / soccer 等) への書き込み禁止
- Modified 状態の `records/tennis/2026-ATP.json` は本セッション1 では触らない (テニス系でも ATP は対象外)
- 「ついでにこれもやっておきました」は禁止 (柱A 規律継続)
- 不明点があれば実装を止めて質問

### 6.4 セッション1 着手時にユーザー確認すべき事項

1. **Swiatek retire の match_status**: 試合中 retire (`retired`) か出場前 retire (`walkover`) かを WebFetch で確認後、ユーザーに最終判断を仰ぐ
2. **step05_scanned_at の区分2 付与可否**: 柱B 規定の文言厳密解釈 (prediction_hit 確定エントリのみ対象) → 区分2 では付与不要と解釈する方針でよいか
3. **R024 取り消し整合性 (Baptiste-Paolini)**: 予測時点を Session_61 当時の SKIP 判断で記録するか / R024 取り消し後の補正なし conf で記録するか

---

## 7. A-3 累計 commit 履歴

| # | commit ID | message | サブタスク |
|---|---|---|---|
| 1 | `6f0d877` | A-3 sub1+sub2: R017 v2.0 / R024 v1.0 取り消し + P030 ID 変更 | サブタスク1 + サブタスク2 |
| 2 | `58a4e0a` | A-3 sub1to2 handoff: サブタスク3 (Session_61 9件振り分け実施) 向け引継ぎサマリ新規作成 | handoff |
| 3 | (本commit) | A-3 sub3 plan handoff: サブタスク3 分割計画 + セッション1 (テニス系4件) 向け引継ぎサマリ新規作成 | handoff |

A-3 タスク開始からの累計 commit 数: **3件** (うち実装 1件 + handoff 2件)

---

## 8. サブタスク3 進め方確定の総括

### 8.1 確定事項

- **進め方**: 選択肢B (種目ごとに分割処理) 採用 → 4セッション構成
- **セッション1 範囲**: テニス系 4件 (Swiatek retire 区分2 + WTA Madrid 3件 区分1)
- **セッション2〜4 範囲**: ラグビー 2件 / NBA 2件 / NHL 1件 (各セッション着手時に詳細化)
- **登録先ファイル**: 全て既存ファイル (新規ファイル設計不要・既存スキーマに準拠)

### 8.2 4本柱の運用準備完了

| 柱 | サブタスク3 セッション1 での適用予定 |
|---|---|
| **柱A** (rule 改訂承認制) | 該当なし (本サブタスクは記録登録のみ・ルール改訂なし) |
| **柱B** (STEP 0.5 SOP) | step05_scanned_at 必須付与 (区分1 3件 / 区分2 は判断保留) |
| **柱C** (一次ソース fetch 義務化) | 5種タグ義務適用 + Class C fetch 件数 (1件以上) 遵守 + miss_class 付与 |
| **柱D** (記録対象判断) | record_class + match_status 必須付与 (区分1=full_record/completed / 区分2=reference_only/retired) |

### 8.3 残課題と継続性

- **凍結対象 11件**: サブタスク3 で順次解消 (セッション1 後 = 11件 + 1件 Modified [wta/2026.json] / セッション4 後 = 11件 + 4件 Modified) → サブタスク4 で一括 commit
- **dashboard / cumulative 同期**: サブタスク3 では実施しない → サブタスク4 / 8 で実施
- **R024 取り消し整合性**: Baptiste-Paolini Madrid R3 の予測再構成時に判断必要

サブタスク3 進め方確定をもって、Session_64 以降での 4セッション分割実装の準備が整った。新セッション (Session_64) でセッション1 (テニス系 4件) から着手する。

---

**サブタスク3 進め方確定**: 2026-04-28
**セッション1 (テニス系 4件) 着手予定**: 新セッション開始時

新セッション最優先: **A-3 サブタスク3 セッション1 (テニス系 4件) 着手** → Swiatek retire (区分2) + Bondar / Baptiste / Pliskova (区分1 3件) を順次処理 → upset_patterns.json + wta/2026.json への登録 + 必須付与フィールド (record_class / match_status / step05_scanned_at / miss_class / 5種タグ) → health_check 通過確認 → commit + push
