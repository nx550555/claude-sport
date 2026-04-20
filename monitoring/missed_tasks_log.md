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

---
