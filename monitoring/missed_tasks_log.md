# やり漏らしタスクログ（missed_tasks_log）

> **Claude Codeへの指示：**
> - セッション終了時に「CLAUDE.md記載のやるべきこと」vs「実際にやったこと」のギャップを記録する
> - 次セッション開始時 STEP 0 後の STEP 1 で必ず読み、未実施項目を優先対処する
> - Session_45 case-C で判明した構造的漏れ（①-3 出力A候補・①-4 アップセット観察の未運用）の再発防止用
> - ギャップがゼロでも必ずエントリを追加する（「ギャップなし」として記録）

---

## エントリ形式

```
## Session _XX (YYYY-MM-DD)

### 実施済み
- CLAUDE.md記載の必須手順で実施した項目

### 未実施・漏れ
- [次セッション対応] 項目と理由
- [保留] 項目と保留理由

### 気付き
- 次回以降の運用改善
```

---

## ログ

## Session _45 (2026-04-20) — 初回エントリ

### 実施済み
- CLAUDE.md STEP 1-5（BACKLOG / user_feedback_log / pending_actions / claude_error_log / rule_pipeline / framework 全読み込み）
- ATP Madrid Q R1 24試合予測→検証→UPSET分析
- upset_patterns.json A014-A020 本体登録補填 + A021-A028 追加（計11件 + 4件Madrid Q + 3件G1 = 計33件）
- 2026-04-20.json 114試合新手順一括スクリーニング（Q1-Q4タグ付け実施）
- NBA G1 8件 + NHL G1 6件 結果記録（出力A候補3/3 HIT確認）
- GO_CANDIDATE 19件の L1深掘り → edge検出困難を確認
- UPSET_PICK_CHECK 11件の UF factor walkthrough → 0件発動確認
- multi_bets.json session _45 エントリ作成（output_a 18件登録）
- rule_pipeline P017 候補追加（Top100 vet Q戦モチベ危機）
- dashboard.html アクティブ候補テーブル更新（SAS HIT + pending 10件 + WTA scope外注記）
- A案 4項目 + E追加 実装（health_check.py / CHECK-5 / missed_tasks_log.md / STEP 0 / 4象限フレームワーク）

### 未実施・漏れ
- [次セッション対応] **GO_CANDIDATE 19件の L2-L4 深掘り**（怪我・フォーム・H2H・コーチ・rest）でアクティブGO化試行
- [次セッション対応] **出力A候補18件の確定結果追跡**（4/21-27 順次試合決着）
- [次セッション対応] **WTA Madrid Q 40件 / Oeiras 17件の scope外記録**（今回は概要のみ、個別予測の詳細記録省略）
- [次セッション対応] **4象限 tagging を既存 records 全件に遡及追加**（現状は Session_45 新規分のみ quadrant field あり）
- [次セッション対応] **stats/cumulative.json に by_quadrant 集計セクションを追加**（今回は multi_bets.json に留めた）

### 気付き
- 市場効率性により市場オッズ単独判定では EV+ 試合はほぼ発生しない
- GO 生成には L1-L4 全層の深掘り + 市場乖離の発見が必須（今後の重点）
- UPSET_PICK 閾値（UF≥3 + div≥15pp）は実運用で極めて稀発動。UPSET_PICK_Lite (UF≥2 + div≥20pp / stake 0.5u) の追加検討候補
- 出力A候補は「EV負でも確実性高い予測」として継続記録し、予測精度指標を別軸で追跡すべき
- **[Session_45末尾 認識訂正・チーム名特定ミス]** ユーザー発言「ウェリントンの負けの分析はしてますか？」を2段階で誤解。
  - **1段目の誤解**: Hurricanes (Super Rugby, Wellington本拠地) と解釈 → 提供JSON対象外の Chiefs 22-17 Hurricanes (4/18 R10) を勝手に追加記録 → 「構造的問題」と誤認識し health_check.py v2 改善案（不在ラウンド検出）まで提出
  - **2段目の誤解解消**: ユーザー再指摘「調べる必要もなかった試合では？」でスコープ問題を認識 → スコープ訂正
  - **3段目の真相**: ユーザー再々指摘「ウェリントンウルフとの試合」= **Warrington Wolves (Super League)** が正解。Session_42 で既に完全分析済 (A020/P016 登録済・MISS -1.0u 確認済)
  - **revert 実施**: Hurricanes 記録を records/superrugby/2026.json から削除。scope_correction エントリを screening_log に残す。
  - **撤回**: health_check.py「不在ラウンド WebSearch スキャン」追加提案は撤回（全世界試合の自動追跡はスコープ爆発）
  - **教訓（ハードニング）**: ユーザーから「XXの分析は？」と聞かれた際の手順:
    1. **チーム名の正確な特定**（略称・別名・表記ブレは必ずユーザーに確認）
    2. **提供JSONにあるか確認**（既存 records 検索）
    3. **なければ追加分析するかユーザーに確認**してから進める
    4. 勝手に自動追加・構造改修しない

---

## Session _48 (2026-04-21 〜 2026-04-23)

### 実施済み
- CLAUDE.md STEP 0 health_check (WARN 2件) → STEP 1-5 必須ファイル全読み込み
- **PA062 Madrid R1 スクリーニング完了**: ATP 29 + WTA 18 + NHL G2 8 + NBA G2/G1 8 + AHL 6 = 69 試合
  - GO 1件 (Galfi @1.54 EV+20.3%)
  - Q3 output_a 4件 (Sonmez / BOS G2 / SAS G2 / OKC G2)
  - CAUTION 5件 (Jodar / LAK-COL G2 / Osorio / Lys + 旧 NRL stale)
- **GEN003 確認**: Galfi / Jodar / KD status WebSearch 実施
- records/wta/2026.json / 2026-ATP.json / nhl/2025-26.json / nba/2025-26.json / multi_bets.json 全更新
- **sync_dashboard.py 新設**: 真実源駆動 7セクション自動同期インフラ
- **包括データ整合性監査 + 修復**: cumulative Q3 3/3→7/7 訂正 / NRL EV 単位修正 / NHL LAK-COL 重複閉鎖 / UFL DC stale 閉鎖
- **CAUTION 3分類実装**: WAITING/MARGIN/TRACK (records caution_type / framework.json taxonomy)
- **UI 改善**: GO/CAUTION 視覚分離 / CAUTION 4サブセクション / スマホ予測精度タブ全画面修正

### 未実施・漏れ
- [次セッション対応] **PA060 NHL G2 全8試合 結果確認** (4/22-23 JST 以降決着)
- [次セッション対応] **PA061 NBA G2 全8試合 結果確認** (4/22-25 JST 以降決着)
- [次セッション対応] **Galfi 結果確認** (4/22) → HIT ならベット成績更新
- [次セッション対応] **Q3 output_a 4件結果確認** (→ 7/7 →11/11 or 変動)
- [次セッション対応] **COL G2 WAITING → goalie確認で GO昇格検討**
- [次セッション対応] **KD G2 出場判定**待ち
- [保留] **sync_dashboard.py 拡張** (累計履歴 / 成長分析タブ / ルール変更インパクト) — 低優先
- [保留] **PA028-030 Premiership/Top14/Pro D2 PD/G 取得** — 中優先継続
- [保留] **PA033 AHL Calder Cup PO スクリーニング** — 4/22 開幕済み

### 気付き
- **ダッシュボード連動の未実装セクションに気付いた**: ユーザー指摘「個々に更新して連動してないのでは？」で初めて sync_dashboard.py を作る決定 → 7 セクション真実源駆動化
- **複数タイプの問題が「CAUTION」1 つに混在していた**: ユーザー質問「監視とはどういう定義か」で気付き、WAITING/MARGIN/TRACK 3 分類に分解。今後の screening で caution_type を意識的に選ぶ指針が明確化
- **EV 単位混在 (percent vs fraction)** は records 書込時に検証されていなかったため、+9.2 と +0.092 が混在していた。sync_dashboard.py に `abs(ev) > 1.5` の警告表示は入れたが、**書込時バリデーション hook** が次の防衛線
- **NBA G1 3重記録**: Session_45/47/47' で異なる命名 ("Philadelphia 76ers @ Boston Celtics" / "Boston Celtics vs Philadelphia 76ers (G1 R1)" / "BOS vs PHI G1") で同じ試合を記録していた。命名規約の統一 or dedup 機構が必要
- **ユーザー指摘ベースの UX バグ検出**: 「EV- なのに推奨？」「個々のダッシュボード連動してない」「Q3 100% は正しいか？」「監視とは？」など、自己監査で検出できなかった UX/データ問題を 4 件発見。ユーザー視点を常に意識する必要
- **cumulative.json 数値の推移管理が甘い**: Session_45 時点の Q3 total=18 が Session_48 まで更新されず誤表示。BACKLOG/CLAUDE.md に「cumulative 再計算を各セッション末尾に実行」の項目追加を検討
