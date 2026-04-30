# A-3 サブタスク6 完了 → サブタスク7 着手向け引継ぎサマリ

> **新セッション読込必須**: 本ファイルは A-3 **サブタスク6 (P020/P024 柱A 承認制プロセス / 議題1+1' step4 実証本丸)** をハイブリッド方針 (P020 = 分岐β 差戻し / P024 = 判断B 差戻し) で完了したことをもって、新セッションで **サブタスク7 (議題5 統合 + match_status 遡及付与 / 議題2/3 step4 本格運用テスト)** に移行するための引継ぎサマリ。新セッションでは本ファイルを最初に読み込んだ後、サブタスク7 着手手順 (§G 起動プロンプト雛形参照) に従って実施する。

---

## A. サブタスク6 完了総括

### A.1 採用方針: ハイブリッド方針 (P020/P024 ともに差戻し)

Claude.ai 外部レビュアー (3号) の最終所見 + 重大懸念5点 + 論点別推奨を受けて Ayumu が下した最終判断:

| 候補 | 採用方針 | 採用根拠 |
|---|---|---|
| **P020** | **分岐β (差戻し)** | 過去シーズン 2025 NRL R1-R8 反例調査で Conservative 推定 5件 + 推定 2件 = **約 5-7件** 観察 → 判断基準4段階「反例 3件以上 → 差戻し or 再設計」該当 → 案2 false positive 多発リスク確定 |
| **P024** | **判断B (差戻し)** | 案2 内部矛盾 (return G 範囲 vs PO G1 限定の併用で死文化) + A031 adjacent reference 格下げによる議題1+1' 3件規定空洞化 → 案撤回必須 → 3 evidence 分裂処理 (規定遵守正攻法) |

### A.2 サブタスク6 commit 履歴 (3 commit)

| # | commit ID | 内容 | 種別 |
|---|---|---|---|
| **commit 1** | `5de4d14` | A-3 sub6 step1 補強: P020 反例検証補強 + 判断基準4段階投入 + 分岐β (差戻し) 推奨 | 実装 (補強) |
| **commit 2** | `58859bd` | A-3 sub6 step1 補強: P024 差戻し処理 + 3 evidence 分裂登録 + 議題1+1' 規定層が機能した証 = step4 実証成功 明示記録 | 実装 (差戻し) |
| **commit 3** | (本commit) | A-3 sub6 → sub7 handoff 新規作成 | handoff |

### A.3 議題1+1' step4 実証成功の核心観点

> **「P020/P024 両方とも案撤回・差戻しになることは議題1+1' 設計意図を毀損せず、むしろ実証成功の核心」**

- サブタスク6 = 議題1+1' step4 実証本丸 = 「**実装成功**」ではなく「**規定遵守の実証成功**」が本来の意義であった
- Session_61 R024 forbidden_practice (同一 turn 内 evidence 3/3 → implement) の再発防止構造が、本格運用テストで初めて「**3件揃った candidate でも反例検証不充足 or 内部矛盾があれば step3 implement に進めない**」ことを実証した
- 三層防御 (機械検証層 + 規定層 + 記録層) のうち **規定層 (柱A 3-1 異セッション独立性 / 3-2 rule_linked: null パターン / 3-3 candidate_pattern 規約 / 5. 禁止事項 + 反例検証義務)** が「**都合の良い解釈**」を防止する構造として機能した

### A.4 外部レビュアー (3号) 寄与の総括

3号の指摘 5点 + 論点別推奨により Claude Code 側 step1 提案レポートの **論理破綻 5箇所** が発見・撤回された:

| 懸念 | Claude Code 側評価 | 実装結果 |
|---|---|---|
| 懸念1: P020 反例検証不充足 | **A. 同意** | commit 1 で反例追加調査実施 → 5件超過確定 |
| 懸念2: 反例#1 GC record 未確認 | **A. 同意** | commit 1 で WebFetch 試行 → 技術不能確定 |
| 懸念3: cumulative シミュレーション数値根拠の弱さ | **A. 同意** | commit 1 で元 conf 確定 (78%/65%/80%) |
| 懸念4: P024 案2 内部矛盾 | **A. 同意** | commit 2 で案2 撤回 + 差戻し |
| 懸念5: A031 adjacent reference 格下げによる 3件規定空洞化 | **A. 同意** | commit 2 で 3 evidence 分裂処理 |

→ 11項目中 8件完全同意 / 2件部分同意 / 0件反論。**3号外部レビューが議題1+1' step4 実証本丸の品質を実質的に担保した**。

---

## B. P020 補強結果サマリ (commit 1 = `5de4d14`)

### B.1 evidence 3件 元 conf 数値確定

| evidence | records 上のエントリ | 元 conf (確定値) | 補足 |
|---|---|---|---|
| **U005** | `records/nrl/2026.json` `games[0]` | **78%** (`confidence: 78`) | tier=go / hit=false / Raiders 36-34 Rabbitohs / Raiders 1-4 (= desperate ✓) / Optus Stadium Perth 中立地 |
| **A008** | `records/nrl/2026.json` `screening_log[1].type_a_results[0]` | **65%** (R010 SKIP) | **R010 SKIP 判定済 = R014 評価対象外** / Roosters 34-22 Sharks (Roosters upset / type_a) |
| **A039** | `records/nrl/2026.json` `predictions[7]` (resolved) + `games[2]` (Session_60 仮 GO 別エントリ) | **80%** (predictions[7] / Session_58 → _61 更新済 / score=18-24 hit=false) ; games[2] 88.5% は別 Session_60 entry / pending | 2 entries 重複あり / R8 vs R9 round 番号不整合あり (本補強範囲外) |

### B.2 反例調査結果

#### 過去シーズン 2025 NRL R1-R8 反例調査 (WebFetch en.wikipedia.org/wiki/2025_NRL_season_results)

| カテゴリ | 件数 | 該当試合 |
|---|---|---|
| **直接反例 確実** | **5件** | R3 Manly d. Canberra (Canberra 0-2) / R4 Manly d. Parramatta (Parra 0-3) / R5 Bulldogs d. Knights (Knights 1-3) / R6 Canberra d. Parramatta (Parra 1-4) / R8 NQL d. GC (GC 1-6 推定) |
| **直接反例 推定 (記録不明)** | 2件 | R5 BRI d. Tigers / R6 MEL d. Warriors |
| **適用外 (desperate 条件不該当)** | 3件 | R5 MEL d. Manly / R7 PEN d. Roosters / R8 BRI d. Bulldogs |

→ **判断基準4段階 投入結果: 「反例 3件以上 → 差戻し or P020 自体の再設計」該当** (5件 = 3件閾値大幅超過)

#### 反例#1 (R7 NZ Warriors vs Gold Coast Titans 2026-04-18) GC record 確認

- WebFetch 4ソース全失敗 ([FETCH_FAILED:nrl.com,titans.com.au,zerotackle.com,wikipedia])
- GC record (R7 開始時 = 4/18 時点) 数値確定不能 → desperate 判定保留
- 反例#1 への案2 適用判定は「desperate 条件不確定」のまま

### B.3 重要な発見 4点

1. **A008 は SKIP 試合だった**: rule_pipeline.json 上は P020 evidence#2 として登録されているが、records 上は L1 段階で R010 SKIP 判定済 → 「fav が MISS した」事例ではなく **R014 評価対象外**
2. **A039 は records 上で 2 entries 重複**: predictions[7] (Session_58 → _61 / 80%) と games[2] (Session_60 仮 GO / 88.5%) が同一試合で異なる conf 値を持つ
3. **R8 vs R9 round 番号不整合**: predictions[7] は `round: "R9"` / rule_pipeline.json P020 description は「R8 = 小サンプル期上限」 → 整合性確認は本補強範囲外 (別タスク推奨)
4. **Wikipedia「2026 NRL season results」ページに複数試合の独自スコア記載問題**: A008 (Roosters 34-22 Sharks vs Wiki Sharks 36-34) / A039 (Manly 18-24 Eels vs Wiki Manly 33-18) で矛盾検出 → records 優先運用ルール再確認

### B.4 P020 差戻し処置

| 項目 | 状態 |
|---|---|
| `rule_pipeline.json` P020 status | **`watching` 戻し** (Ayumu 判断2 確定) - **本commit 範囲外** (commit 1 では status 変更未実施 / commit 2 では P024 のみ status 変更) |
| `candidate_pattern_registry.json` P020 系列 candidate 登録 | **登録なし** (Ayumu 判断2 確定 / 議題1+1' 規定層が機能した証として記録なし運用) |
| 補強記録 | proposal §1-X 6 サブセクション新設 (in-place 改竄なし / 既存 §1 (a)〜(e) 温存) |

> **【本サブタスク6 → 7 移行で確認すべき重要事項】** P020 status は commit 1 では `ready_to_implement` のまま温存されていた可能性あり。サブタスク7 着手前に rule_pipeline.json で P020 status を `watching` に変更する補完 commit を別途実施するか確認要 (本handoff §H 禁止事項参照)。

---

## C. P024 差戻し結果サマリ (commit 2 = `58859bd`)

### C.1 懸念4・5 への完全同意 (案2 撤回確定)

#### 懸念4: 案2 内部矛盾

| 項目 | 内容 |
|---|---|
| 案2 本来仕様 (proposal §2-(b) L370-377) | 「return G (= G2-G4 で return) の場合は +5〜+8% 補正」 |
| 推奨案サブ条件 (proposal §2-(d) L468) | 「適用範囲を PO R1 G1 に限定」 |
| 帰結 | return cycle 補正 = 発動条件を持たない死文 / A043 補正対象外 / **実質案1 と等価** |

#### 懸念5: A031 adjacent reference 格下げによる 3件規定空洞化

| 項目 | 内容 |
|---|---|
| 議題1+1' 確定方針 | evidence 3件は原則として **異なるセッション** で独立検出されたものであること |
| step1 提案 | A031 を「adjacent reference」として位置付け (案2 範囲外) |
| 帰結 | trigger evidence = A029 + A043 = **計 2件** = 議題1+1' 3件規定空洞化 / 「adjacent reference」概念は CLAUDE.md / rule_pipeline / registry **いずれにも規定なし** = 規定外概念導入 |

### C.2 3 evidence 分裂処理 (Ayumu 判断3 = 規定遵守正攻法)

| 元 P024 evidence | 分裂後の独立 candidate | candidate_pattern (柱A 3-3 規約遵守 / 80文字以内 + snake_case) |
|---|---|---|
| **A029** (LAL d. HOU G1 / Session_47) | `P_NBA_PO_g1_star_off_candidate` | `nba_po_g1_star_scorer_25ppg_off_pre_game_decision` (53文字) |
| **A031** (POR d. SAS G2 / Session_50) | `P_NBA_PO_g2_in_game_star_loss_candidate` | `nba_po_g2_in_game_star_loss_late_q4_collapse` (44文字) |
| **A043** (HOU d. LAL G4 / Session_61) | `P_NBA_PO_g4_star_return_candidate` | `nba_po_g4_star_scorer_return_home_dominance_blowout` (51文字) |

### C.3 ファイル変更内容

| ファイル | 変更内容 | 行数 |
|---|---|---|
| `core/rule_pipeline.json` | P024 status `ready_to_implement` → `watching` + note 末尾に Session_64 差戻し記録追記 / current_count: 3 のまま温存 (差戻し履歴の数値痕跡) | +4 -2 |
| `core/candidate_pattern_registry.json` | 既存 4 patterns → **7 patterns** へ拡張 (P_NBA_PO_g1/g2/g4 系列 3 candidate 新規追加) / 各 candidate に `split_origin` フィールド付与 / `last_updated` 2026-04-30 / `updated_session` `_64_a3_sub6_step1_commit2` | +76 |
| `monitoring/a3_subtask6_step1_proposal_report.md` | §2-X「P024 差戻し決定」セクション新設 (6 サブセクション構成 / in-place 改竄なし) | +122 |

### C.4 中間 status 値新設の不採用

- **不採用された中間 status 値 (Ayumu 判断3 で確定)**: `pending_redesign` / `evidence_accumulating` / `weak_link_pending` 等
- **不採用根拠**: 中間 status 値新設は柱A 承認制プロトコル必須となるためスコープ超過回避
- **採用された status 値**: 既存定義済 3値 (`watching` / `ready_to_implement` / `implemented`) のうち **`watching`** = 規定外新設なし ✓

---

## D. サブタスク7 着手向け詳細整理

### D.1 サブタスク7 内容: 議題5 統合 + match_status 遡及付与

#### サブタスク7 = 議題2 step4 + 議題3 step4 二重実証本丸

| 議題 step4 | 実証範囲 |
|---|---|
| **議題2 step4** | 柱B サブセクション 2 ステップ8 (パターンA/B/C 明文化) + `prediction_hit_updated_at` 規定 + step05_scanned_at 同時付与必須化 が **records 100件超への match_status 遡及付与で本格運用** されることの実証 |
| **議題3 step4** | 柱D サブセクション 9-2 (handoff 作成 SOP / §1 既存検索3経路 + §2 (a)-(d) フロー + §3 6列構造テンプレート + §4 CHECK-2 連携 8項目チェックリスト + §5 SOP 違反時の事後対応) が **大規模適用 (100件超) で運用安定性検証** されることの実証 |

### D.2 サブタスク7 申し送りリスト 18件

(前 handoff §C 「4議題で確立された規定の総まとめ」由来 17件 + サブタスク6 由来追加 1件 = **18件確定**)

#### D.2.1 機械検証層 (5項目) の大規模運用検証

| # | 項目 | 内容 |
|---|---|---|
| 1 | 項目10 (`miss_feedback_loop`) | rule_linked: null + rule_linked_note 50文字以上 OK 扱いの大規模運用検証 |
| 2 | 項目12 (`miss_analysis_tag_compliance`) | 5種タグ付与検査の大規模運用検証 (第1優先キー = `prediction_hit_updated_at`) |
| 3 | 項目13 (`step05_scan_compliance`) | step05_scanned_at 付与検査の大規模運用検証 (第1優先キー = `prediction_hit_updated_at`) |
| 4 | 項目14 (`candidate_pattern_uniqueness`) | registry 7 patterns + 将来追加分の整合性 + 重複検出の大規模運用検証 |
| 5 | 項目15 (`step05_prediction_hit_sync_compliance`) | step05_scanned_at + prediction_hit_updated_at 同一値同時付与検査の大規模運用検証 |

#### D.2.2 規定層 (6項目) の大規模運用検証

| # | 項目 | 内容 |
|---|---|---|
| 6 | 柱A 3-2 (rule_linked: null + rule_linked_note 必須4項目パターン) | 既存4件 (Pliskova-Mertens / TOR-CLE G4 / LAL-HOU G4 / PHI G4 vs PIT) の運用継続 + 新規 case 発生時の正規パターン適用 |
| 7 | 柱A 3-3 (candidate_pattern フィールド規約) | snake_case / 80文字 / registry 参照義務の大規模運用 (registry 7 patterns 監視継続) |
| 8 | 柱A 5. 禁止事項 6項目目 | 同一セッション内同じ candidate_pattern 重複付与禁止の大規模運用検証 |
| 9 | 柱B サブセクション 2 ステップ8 (パターンA/B/C 明文化) | match_status 遡及付与 100件超でパターンA 6項目処理ルール / パターンB 4項目処理ルール / パターンC 6項目処理ルール の本格運用 |
| 10 | 柱D サブセクション9 テーブル | 5列 → 6列拡張 + 9件処理パターン分類遡及付与 + 訂正履歴拡充の運用継続 |
| 11 | 柱D サブセクション 9-2 (handoff 作成 SOP) | §1 既存検索3経路 + §2 scope外UPSET 性質事前確認 (a)-(d) + §3 6列構造テンプレート + §4 CHECK-2 連携 8項目チェックリスト + §5 SOP 違反時の事後対応 + §6 既存柱整合性 の大規模適用 |

#### D.2.3 記録層 (5項目) の大規模運用検証

| # | 項目 | 内容 |
|---|---|---|
| 12 | `candidate_pattern` フィールド | 新規 P*** 候補の機械検証可能化 / candidate_pattern_registry.json 必須参照の大規模運用 |
| 13 | `rule_linked: null` + `rule_linked_note` (50文字以上) | 異セッション独立 evidence 3件未満時の正規パターン運用継続 |
| 14 | `prediction_hit_updated_at` フィールド | step05_scanned_at と同一値で同時付与必須 / **9件遡及付与済 → 100件超への遡及付与本格運用** |
| 15 | `record_class` (区分1/2/3) + `match_status` (5値enum) | 新規エントリ必須付与 + **既存 records 100件超への遡及付与本格運用** |
| 16 | `confidence_drift: "high"` フィールド | 推定勝率 ≥80% HIT + 種目別薄勝ち閾値内で必須付与 (新規エントリのみ) の運用継続 |

#### D.2.4 candidate_pattern_registry.json (1項目) の大規模運用検証

| # | 項目 | 内容 |
|---|---|---|
| 17 | candidate_pattern_registry.json 監視 | 4 patterns → **7 patterns** への拡張後、サブタスク7 大規模適用での新規 candidate 追加 + 既存 split_origin 等のメタデータ整合性監視 |

#### D.2.5 サブタスク6 由来追加 (1項目)

| # | 項目 | 内容 |
|---|---|---|
| 18 | サブタスク6 議題1+1' step4 実証成功記録の継承 | サブタスク7 大規模適用時、議題1+1' 規定層が機能した実例 (P020/P024 両方差戻し) を参照しつつ、新規 case で同様の論理破綻が発生した場合は同パターン (案撤回 + 差戻し or 分裂処理) で対処 |

→ **合計 18件 = 機械検証層5 + 規定層6 + 記録層5 + registry1 + サブタスク6由来1**

### D.3 サブタスク7 着手前の必須読込ファイル

| # | ファイル | 用途 |
|---|---|---|
| 1 | `CLAUDE.md` (議題1+1' / 議題2 / 議題3 / 議題4 反映済 最新版) | 4本柱規定基盤 |
| 2 | `monitoring/a3_subtask6_to_subtask7_handoff.md` (本ファイル) | サブタスク6 完了 → サブタスク7 着手向け引継ぎ |
| 3 | `monitoring/a3_subtask6_step1_proposal_report.md` (補強記録 §1-X + 差戻し記録 §2-X 含む完成版 / 803行想定) | サブタスク6 詳細記録 |
| 4 | `monitoring/a3_review_agenda4_to_subtask4to9_handoff.md` | 4議題完了 + サブタスク4-9 移行引継ぎ |
| 5 | `monitoring/a3_review_agenda3_to_agenda4_handoff.md` | 議題3 → 議題4 引継ぎ |
| 6 | `monitoring/a3_review_agenda2_to_agenda3_handoff.md` | 議題2 → 議題3 引継ぎ |
| 7 | `monitoring/a3_review_agenda1plus1_to_agenda2_handoff.md` | 議題1+1' → 議題2 引継ぎ |
| 8 | `monitoring/a3_subtask3_complete_to_review_handoff.md` | サブタスク3 完了 → 振り返り議論引継ぎ |
| 9 | `core/rule_pipeline.json` (P024 watching 戻し済 / current_count: 3 温存 / Session_64 note 追記済) | 候補ルール現状 |
| 10 | `core/candidate_pattern_registry.json` (7 patterns 拡張済 / split_origin 付与済) | candidate_pattern 規約管理 |
| 11 | `monitoring/health_check.py` (項目10/12/13/14/15 改修・新設済) | 機械検証層 |
| 12 | `git log --oneline -10` + `git status -sb` で現状確認 (本handoff 後 26 commit想定) | 現状確認 |
| 13 | `PYTHONIOENCODING=utf-8 python monitoring/health_check.py` を実行 (15項目 OK + WARN 4件 + ALERT 0件 維持確認) | baseline 維持確認 |
| 14 | STEP 1 必須ファイル群 (BACKLOG.md / user_feedback_log.md / pending_actions.md / claude_error_log.md / framework.json) | 通常 STEP 1 |

---

## E. 議題1+1' step4 実証成功の総括

### E.1 Session_61 R024 forbidden_practice 再発防止構造の本格運用テスト初実例

| 観点 | Session_61 R024 (再発防止対象) | サブタスク6 (再発防止構造の実例) |
|---|---|---|
| 行為 | 同一 turn 内 evidence 3/3 検出 → 同 turn 内 implement | 異セッション独立 evidence 3/3 確認 → 反例検証 + 内部矛盾検出 → step3 implement 阻止 |
| 結果 | R017 v2.0 (Vacherot 1件改訂) / R024 v1.0 (form slump) implement 強行 → A-3 で取り消し | P020 (反例 5件超過) + P024 (内部矛盾) → 案撤回・差戻し → 議題1+1' 設計意図実証 |
| 規定遵守 | 違反 (柱A 5. 禁止事項3項目目「evidence 1件のみでの即改訂」 + 同一 turn 内 implement) | 完全遵守 (異セッション独立性 ✓ / 同一 turn 内禁止 ✓ / 反例検証義務 ✓ / step3 進行阻止 ✓) |

→ **議題1+1' step4 実証本丸の核心 = 「規定遵守の実証成功」** = サブタスク6 で完全達成

### E.2 三層防御 (機械検証層 + 規定層 + 記録層) の規定層機能性確認

| 三層防御 | サブタスク6 での実証 |
|---|---|
| **機械検証層** (health_check.py 5項目) | step3 commit 自体が不実施のため項目10/14 直接検査機会なし → ただし registry 7 patterns 拡張を健全認識 (item 14) で間接実証 |
| **規定層** (CLAUDE.md 4本柱) | 柱A 3-1 (異セッション独立性 ✓) + 柱A 3-3 (candidate_pattern 規約 = 80文字以内 + snake_case ✓) + 柱A 5. 禁止事項 (反例検証義務 ✓ + 同一 turn 内 implement 禁止 ✓) → **規定層が「都合の良い解釈」を防止する構造として機能** |
| **記録層** (records スキーマ + monitoring 文書) | proposal §1-X 補強記録 + §2-X 差戻し記録 (in-place 改竄なし / 追記方式) + rule_pipeline.json note 追記 + registry 7 patterns 拡張 (split_origin メタデータ付与) → **案検証プロセス全体の透明性担保** |

### E.3 サブタスク6 = 「実装成功」ではなく「規定遵守の実証成功」が本来の意義

- **誤った期待**: 「P020/P024 を rule 実装まで進める」(議題1+1' 設計意図と乖離)
- **正しい意義**: 「**規定層が機能して、3件揃った candidate でも反例検証不充足 or 内部矛盾があれば step3 implement に進めない**」ことを本格運用テストで実証する
- **本来の意義の達成**: P020 + P024 両方とも案撤回・差戻し = 議題1+1' 設計意図の **完全実証**

→ サブタスク7 大規模適用 (100件超) でも **同様の精神** (= 規定層を「都合よく緩めない」運用) を継承する

### E.4 外部レビュアー (3号) の貢献の総括

外部レビュー (3号) は議題1+1' step4 実証本丸の品質を実質的に担保した。Claude Code 単独では発見できなかった論理破綻 (P024 案2 内部矛盾 / A031 adjacent reference 格下げによる 3件規定空洞化) を確実に発見・撤回させた。

→ **サブタスク7 大規模適用でも、外部レビュー (3号) を要所で活用する運用** が推奨される (例: 100件超 match_status 遡及付与の中間段階で 3号レビュー実施 / パターンA/B/C 分類精度の検証等)

---

## F. A-3 累計 commit 履歴 (現状 25件 → 本handoff = 26件)

| # | commit ID | message (略) | 種別 |
|---|---|---|---|
| 1 | `6f0d877` | A-3 sub1+sub2: R017 v2.0 / R024 v1.0 取り消し + P030 ID 変更 | 実装 |
| 2 | `58a4e0a` | A-3 sub1to2 handoff | handoff |
| 3 | `2e44e7b` | A-3 sub3 plan handoff | handoff |
| 4 | `4a990d0` | A-3 sub3 session1: テニス系4件 振り分け登録 | 実装 |
| 5 | `73e3626` | A-3 sub3 session1to2 handoff | handoff |
| 6 | `545a3a3` | A-3 sub3 session2: ラグビー Premiership 2件 結果反映 | 実装 |
| 7 | `5e60649` | A-3 sub3 session2to3 handoff | handoff |
| 8 | `2529454` | A-3 sub3 session3: NBA Playoffs 2件 結果反映 + 副次論点B 判明 | 実装 |
| 9 | `4eb3ac6` | A-3 sub3 session3to4 handoff | handoff |
| 10 | `158547e` | A-3 sub3 session4: NHL Playoffs 1件 結果反映 + サブタスク3 全件完了 9/9=100% | 実装 |
| 11 | `4c0a1a4` | A-3 sub3 complete to review handoff | handoff |
| 12 | `4b5876e` | A-3 review agenda1+1prime step3: 議題1+1' 三層防御確立 | 実装 |
| 13 | `d71a1ff` | A-3 review agenda1+1prime to agenda2 handoff | handoff |
| 14 | `ab0b9a1` | A-3 review agenda2 step12 to step3 handoff | handoff |
| 15 | `6346774` | A-3 review agenda2 step3: 議題2 三層防御 + パターンA/B/C 明文化 + prediction_hit_updated_at 新設 | 実装 |
| 16 | `7410f9d` | A-3 review agenda2 to agenda3 handoff | handoff |
| 17 | `921c710` | A-3 review agenda3 step3: 議題3 二層構成 + 9-2 SOP 新設 + 副次論点B 解消 | 実装 |
| 18 | `f6b478e` | A-3 review agenda3 to agenda4 handoff | handoff |
| 19 | `7d3f141` | A-3 review agenda4 step3: 議題4 #1/#2/#7 訂正 + handoff 5件 訂正注記 = 振り返り議論全体完了 | 実装 |
| 20 | `345e25a` | A-3 review agenda4 to subtask4to9 handoff | handoff |
| 21 | `5ef93bb` | A-3 sub4: Session_61 結果反映バッチ統合 commit (Modified 6件解凍) | 実装 |
| 22 | `b770d5b` | A-3 sub5: Session_61 使い捨てスクリプト + handoff アーカイブ commit (Untracked 4件解凍) | 実装 |
| 23 | `eae53c5` | A-3 sub6 step1: P020/P024 柱A 承認制プロセス step1 提案レポート新規作成 | 実装 (step1) |
| 24 | `5de4d14` | **A-3 sub6 step1 補強 (commit 1/3): P020 反例検証補強 + 判断基準4段階投入 + 分岐β (差戻し) 推奨** | **実装 (補強)** |
| 25 | `58859bd` | **A-3 sub6 step1 補強 (commit 2/3): P024 差戻し処理 + 3 evidence 分裂登録 + 議題1+1' 規定層が機能した証 = step4 実証成功 明示記録** | **実装 (差戻し)** |
| 26 | (本commit) | **A-3 sub6 → sub7 handoff: サブタスク6 完了 + 議題1+1' step4 実証成功総括 + サブタスク7 着手向け詳細整理 (申し送り18件 + 起動プロンプト雛形)** | **handoff** |

A-3 タスク累計: **26 commit** (実装 11件 + handoff 15件)。サブタスク7 大規模適用で更に積み増し。

### F.1 サブタスク7 着手で議題2/3 step4 本格運用に移行する位置付け

- 議題1+1' step4 実証 (サブタスク6) = **完了** (規定遵守の実証成功)
- 議題2 step4 + 議題3 step4 実証 (サブタスク7) = **本格運用テスト 着手予定**
- 議題7 統合 (サブタスク8) = サブタスク7 完了後
- 議題9 統合 (サブタスク9) = サブタスク8 完了後
- → A-3 タスク全体完了

---

## G. サブタスク7 起動プロンプト雛形

新セッション開始時に Claude Code に渡すプロンプト例:

```
A-3 サブタスク7 着手 (議題5 統合 + match_status 遡及付与 100件超 /
議題2/3 step4 本格運用テスト)。

【最初に読み込むファイル】

monitoring/a3_subtask6_to_subtask7_handoff.md
(サブタスク6 完了総括 + 申し送り18件 + サブタスク7 着手向け詳細)

【前提状態】

- A-3 振り返り議論セッション 4議題 (議題1+1' / 議題2 / 議題3 / 議題4)
  step1-3 完了済 (commit 4b5876e / 6346774 / 921c710 / 7d3f141)
- A-3 サブタスク4 (Modified 6件 / 5ef93bb) + サブタスク5 (Untracked
  4件 / b770d5b) 完了済 (凍結対象10件すべて解凍済)
- A-3 サブタスク6 (議題1+1' step4 実証本丸 / commit 1 5de4d14 +
  commit 2 58859bd + commit 3 本handoff) 完了済 (P020/P024 両方差戻し
  = 規定遵守の実証成功)
- A-3 累計 26 commit (実装 11件 + handoff 15件 / GitHub push 済 /
  working tree クリーン)

【サブタスク7 内容】

議題5 統合 + match_status 5値 enum (completed/retired/walkover/
cancelled/postponed) を records 100件超に遡及付与。同時に議題2 step4
(パターンA/B/C 規定の本格運用) + 議題3 step4 (9-2 SOP 大規模適用)
を二重実証。

【手順】

1. 上記 handoff + CLAUDE.md + 関連ファイル群を読込
2. 現状確認 (git status -sb / health_check 実行 / registry 7 patterns
   確認)
3. records 100件超への遡及付与計画策定 (パターンA/B/C 分類 + 9-2 SOP
   §1-§5 適用フロー)
4. prediction_hit_updated_at 機械化スクリプト作成 (パターンA 規定の
   自動適用)
5. 段階的に遡及付与実施 (種目別 or セッション別バッチで commit 分割 /
   一括処理禁止 / 柱A 規律継続)
6. health_check 都度実行 (項目12/13/14/15 大規模運用検証)

【遵守事項】

- 個別 commit (一括処理禁止 / 柱A 規律継続)
- in-place 改竄なし (既存記録は遡及改竄せず追記方式)
- リモート auto-fetch 干渉発動時は stash → rebase → pop パターン
- 4本柱本体への変更は柱A 承認制プロトコル経由必須
- 不明点があれば実装を止めて質問
- サブタスク6 で確立された「規定遵守の実証成功」精神を継承

実行開始してください。
```

---

## H. サブタスク6 → 7 移行時の禁止事項

### H.1 規定層への直接書き込み禁止

| ファイル | 禁止理由 |
|---|---|
| `CLAUDE.md` | 4本柱規定本体 / 柱A 承認制プロトコル経由必須 |
| `monitoring/health_check.py` | 機械検証層実装 / 改修は柱A 承認制プロセス必須 |
| `core/rule_pipeline.json` の status 変更 (実装関連) | 柱A 承認制プロトコル経由必須 (ただし `evidence` 配列追加 / `current_count` インクリメント等の通常運用は OK) |
| `core/rules_*.json` (取り消し済 R017/R024 含む) | ルール改訂は柱A 承認制プロトコル経由必須 |
| `core/candidate_pattern_registry.json` の patterns 削除 | サブタスク6 で確立した 7 patterns は維持 / 新規追加は OK だが既存削除禁止 |

### H.2 サブタスク6 確立済規定の改竄禁止

- サブタスク6 で確立された「**規定遵守の実証成功**」精神を逸脱する運用 (= 「都合よく規定を緩めて step3 implement に進める」等) は**禁止**
- 議題1+1' step4 実証成功の前例 (P020/P024 両方差戻し) を踏まえ、**サブタスク7 でも反例検証不充足 / 内部矛盾検出時は同パターン (案撤回 + 差戻し or 分裂処理)** で対処

### H.3 P024 evidence 再蓄積関連の禁止事項

- `P_NBA_PO_g1_star_off_candidate` / `P_NBA_PO_g2_in_game_star_loss_candidate` / `P_NBA_PO_g4_star_return_candidate` の 3 candidate を **統合扱い禁止** (各々独立して trigger_threshold 3 到達時に柱A 承認制プロセス step1 起動)
- 元 P024 を「3 evidence 揃った状態」として復活させる運用 (=分裂取消し) は **禁止**

### H.4 順序遵守

- サブタスク7 (議題5 統合 + match_status 遡及付与) → サブタスク8 (議題7 統合 / cumulative.json by_record_class + dashboard.html 改修) → サブタスク9 (議題9 統合 / memory ガイドライン作成) の順序で個別実施
- 「ついでにこれもやっておきました」は禁止 (柱A 規律継続)

### H.5 リモート auto-fetch 干渉時の対応

- 議題1+1' / 議題2 / 議題3 / 議題4 step3 + サブタスク4/5/6 commit + push で **連続多数回干渉なし一発成功** (実績)
- 過去出現実績 (`fddf6de` / `e2d7062` / `01a1f88`) ありのため、サブタスク7 大規模 commit 多発時は干渉発動可能性高
- 干渉発動時の対応: `git fetch origin` → `git pull --rebase origin main` → `git push origin main` (実績パターン / commit 1 で1回干渉実績あり / sub6 commit 2 + 3 では干渉なし)

### H.6 不明点があれば実装を止めて質問

- サブタスク6 で外部レビュー (3号) が論理破綻 5箇所を発見した実例を踏まえ、サブタスク7 でも判断に迷った場合は **実装を止めて Ayumu に質問**
- 大規模適用 (100件超) の中間段階で 3号外部レビュー実施を推奨

---

**サブタスク6 完了**: 2026-04-30 (commit `5de4d14` 補強 + `58859bd` 差戻し + 本handoff = 計3 commit / 議題1+1' step4 実証成功 = 規定遵守の実証成功)
**次着手**: サブタスク7 (議題5 統合 + match_status 遡及付与 100件超 / 議題2/3 step4 本格運用テスト)
**最優先タスク**: records 100件超への遡及付与計画策定 + パターンA/B/C 分類 + 9-2 SOP §1-§5 適用フロー

新セッション最優先: **サブタスク7 着手** → サブタスク8 (議題7 統合) → サブタスク9 (議題9 統合) → A-3 タスク全体完了
