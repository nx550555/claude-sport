# ベッティング分析システム — Claude Code 引き継ぎファイル
# このファイルをClaude Codeセッションの最初に読ませてください

---

## あなたへの指示

このファイルを読んだら、以下を実行してください：

**【毎回必須】最初に必ず読む：**
1. `C:\Users\ohwada\Desktop\claude_sport\BACKLOG.md` を読み込む
   - `[~]` 作業中の項目があれば「前回途中になっています」と報告する
   - `[ ]` 未着手の項目があれば一覧を表示する
2. `C:\Users\ohwada\Desktop\claude_sport\monitoring\user_feedback_log.md` を読み込む
   - `OPEN` の項目があれば「未解決の指摘があります」と報告する
3. `C:\Users\ohwada\Desktop\claude_sport\monitoring\pending_actions.md` を読み込む
   - `PENDING` / `WAITING` / `IN_PROGRESS` の項目を一覧で報告する
4. `C:\Users\ohwada\Desktop\claude_sport\monitoring\claude_error_log.md` を読み込む
   - `ACTIVE` のエラーを必ず把握する（このセッションで同じミスをしないため）
   - **ミスが発覚したら即座にこのファイルに追記する**（CE001, CE002...の連番で）
5. `C:\Users\ohwada\Desktop\claude_sport\core\rule_pipeline.json` を読み込む
   - `current_count >= trigger_threshold` の候補があれば「ルール追加トリガー発動：〇〇を実装します」と報告してそのまま実装する
6. `C:\Users\ohwada\Desktop\claude_sport\core\framework.json` の `phase_transition.triggers` を確認する
   - 以下の4つのトリガーを全件チェックし、いずれか1つでも条件を満たしていたら即座にユーザーへ報告する
   - **T1（サンプル数）**: いずれかのスポーツで `hit!=null` の確認済み試合が20件以上か？
     → records/{sport}/*.json を読み込んでhit!=nullをカウントする
   - **T2（アップセット蓄積）**: `stats/upset_patterns.json` のconfirmed_upsets がテニス合計10件以上 OR 他スポーツ1種目で5件以上か？
     → upset_patterns.json を読み込んでスポーツ別にカウントする
   - **T3（ルール実装数）**: `core/rule_pipeline.json` の `implemented_rules` が3件以上か？
     → rule_pipeline.json の implemented_rules 件数をカウントする（現在: 3件→既に達成済み確認要）
   - **T4（予測精度）**: `stats/cumulative.json` のhit_rateが70%以上かつ達成から90日以上経過しているか？
     → cumulative.json を確認する
   - いずれかのトリガーが条件を満たした場合は: 「【フェーズ移行トリガー発動: Tx】〇〇が条件を満たしました。Phase2（アップセット積極予測）への移行を検討しますか？」と報告する
   - framework.json の triggers[].met を true に、met_date に当日日付を記録する

**【毎回必須】アクティブ推奨の最新情報チェック（GEN003）：**
セッション開始時、GO/CAUTIONのpending推奨が1件でもあれば、以下を全件実行する：

1. `records/` の各スポーツJSONから `status: "pending"` かつ `tier: "go"/"caution"` の試合を全件取得
2. 各試合について WebSearch で以下を確認（検索キーワード例: "チーム名 injury news 日付"）
   - 先発・出場選手の変更（怪我・出場停止・体調不良）
   - コーチ・戦術の突発的変更
   - 会場・日程の変更
   - 当初分析時から変わりうるその他の重大情報
3. 判定：
   - 重大情報あり → 元の推奨を見直し（GO→CAUTION / CAUTION→SKIP / 推奨チーム変更）
   - 情報なし → 「〇〇: 最新情報なし、推奨維持」と一行報告
4. 変更があれば records JSON・ダッシュボードを即座に更新する

⚠️ この確認を飛ばして分析・記録に入ることは禁止。

**【毎回必須】抜け漏れチェック（②の要件）：**
以下を確認して「現状チェック」として報告する：
- hit:null の未確認試合が records/ にないか
- BACKLOG.md の [ ] 未着手項目で対応できるものはないか
- 前回の分析ログ（daily_reports/）と今回の状況に乖離がないか
- 今日・明日に試合がある種目でスクリーニングが必要なものはないか

**【タスク完了後・毎回必須】残タスク確認プロトコル（機能③）：**
一つの指示・タスクを完了したら、必ず以下を実行する：
1. `monitoring/pending_actions.md` を確認する
2. PENDING / WAITING / IN_PROGRESS のアクションを列挙して報告する
3. 「まだ X 件残っています。不要なものがあれば教えてください」と確認を求める
4. ユーザーが「不要」「スキップ」と明示するまでPENDINGを削除しない
5. 新しいタスクが発生したら即座に pending_actions.md に追記する

**【指摘・意見・質問を受けたとき・毎回必須】フィードバック記録（機能①）：**
ユーザーから指摘・意見・質問があったら：
1. 即座に `monitoring/user_feedback_log.md` に追記する（FB001, FB002...）
2. ステータスは OPEN でスタート
3. 対応完了後もユーザーが確認するまで RESOLVED にしない
4. `monitoring/check_protocol.md` のCHECK-3を参照して精度を保つ

**【応答送信前・毎回必須】自己チェック（機能②）：**
`monitoring/check_protocol.md` の4つのチェックを通過させる：
- CHECK-1: 基本方針チェック（オッズ起点・統計自取得・全試合対象・ファイル書込）
- CHECK-2: 情報精度チェック（ハルシネーション・数値・チーム名・EV計算）
- CHECK-3: フィードバック解決チェック（OPEN項目・新規追記）
- CHECK-4: アクション確認チェック（残PENDING報告）

**【スクリーニング完了後・毎回必須】高確率予想・マルチベット出力：**
全スポーツのスクリーニングが完了したら以下を実行する：

1. **出力A（高確率予想リスト）**を生成する
   - L1〜L4で「確実視できる」と判断した試合のみ抽出（少しでも迷いがある試合は含めない）
   - ⚠️ **EVは関係しない**。オッズが低くてもベット価値がなくても、予測として自信があれば含める
   - ⚠️ GOより多くなることが正常（EVフィルターがない分、高確率だがオッズ短い試合も入る）
   - 確実性（推定勝率）が高い順に出力。該当なし → 「該当なし」と出力
   - 出力形式: No. | 試合名 | スポーツ | 推奨 | 推定勝率 | オッズ | 確実と判断した理由
2. **出力B（高確率マルチベット）**を計算する
   - 出力Aが2件以上の場合のみ実行（1件以下 → 「マルチ構成不可」と出力）
   - マルチオッズ = 各オッズの積 / 全体推定勝率 = 各勝率の積 / マルチEV = (全体推定勝率 × マルチオッズ) - 1
   - EV+の組み合わせをマルチEV高い順に上位5パターン出力
   - 全組み合わせがEV-なら「EV+の組み合わせなし」と出力
3. `records/multi_bets.json` の sessions 配列に追記する
4. `dashboard.html` の「高確率予想」「マルチベット」タブを更新する
5. **出力Aのアップセット分析への活用**：
   - 出力Aに含まれた試合の `prediction_hit` を結果確認後に必ず更新する
   - 出力A内で `prediction_hit: false`（外れ）だった試合は必ず `miss_analysis` を records JSON に追記する
   - miss_analysis の内容を `rules_{sport}.json` に知見として追記する（アップセット要因の蓄積）
   - 特に「高確率予想に入ったがMISSした」試合はアップセットの典型例として `rule_pipeline.json` の候補にも記録する

**【記録更新後・毎回必須】ダッシュボード同期プロトコル（整合性保証）：**
試合結果を records/*.json に書き込んだら、必ず以下を実行する：

1. `core/dashboard_stats.json` を更新する（各sport の go_count / confirmed_count / hit_count / hit_rate / ev_total / pending_count を再計算）
2. `python sync_sport_cards.py` を実行してダッシュボードに反映する
3. dashboard.html の「アクティブ推奨」タブから完了した試合を削除する
4. 更新後に概要big-stat・各スポーツカードの全数値を目視で確認し、不整合があれば即修正する

⚠️ **records更新 → dashboard_stats.json更新 → sync実行 の3ステップを必ずセットで行うこと。**
⚠️ **この手順を省略してダッシュボードの数字がずれることは絶対に禁止。**

**【会話終了時】セッション終了手順（③の要件）：**
ユーザーが「会話を終了する」「終わり」「終了」「記録して」などと言ったら：
1. このセッションで行った作業を `session_logs/YYYY-MM-DD_HH.md` に保存する
2. BACKLOG.md の完了項目を [x] に更新する
3. 次回への申し送り事項を BACKLOG.md の「未完了」欄に追記する
4. `git add -A && git commit -m "Session end YYYY-MM-DD" && git push origin main` を実行する
5. 「セッション終了。次回は〇〇から再開します。」と報告する

**【自発的セッション保存+リセット提案】コンテキスト管理プロトコル：**

以下のいずれかの条件を満たした場合、ユーザーへの確認なしにセッションログを自動保存し、会話のリセットを提案する。

**トリガー条件（どれか1つでも該当したら実行）：**
- T1: システムリマインダーに「was read before the last conversation was summarized」が複数含まれている（コンテキスト圧縮が発生済みの確実なサイン）
- T2: 大きなフェーズが完了し、次に別の大きなフェーズが始まる直前（例：遡り調査完了→ルール実装開始 / スクリーニング完了→結果確認フェーズ移行）
- T3: WebSearch / WebFetch / 複数ファイル書き込みを含む主要タスクが3件以上完了し、かつ次のタスクが明確に残っている状態
- T4: ユーザーが「記録して」「セッション保存して」「ログ残して」と言った（明示的な保存要求）

**実行手順：**
1. `session_logs/YYYY-MM-DD_HH.md` にこのセッションの作業サマリを保存する
2. `BACKLOG.md` の完了項目を [x] に更新し、未完了を残す
3. `git add -A && git commit && git push` を実行する
4. 以下のメッセージをユーザーに送る：

```
セッションログを保存しました（session_logs/YYYY-MM-DD_HH.md）。
コンテキストが大きくなってきたため、ここで会話をリセットすることをお勧めします。
新しい会話を開始して「CLAUDE_CODE_START.md を読んで」と伝えると、
ここから続きを再開できます。
次のタスク: [残っている最優先タスクを1〜3件列挙]
```

**注意：**
- T1（圧縮発生済み）の場合は強く推奨（精度が落ちている可能性が高い）
- T2・T3はフェーズの切れ目に提案するため、作業の途中で割り込まない
- 保存後もユーザーが「続けて」と言えばそのまま作業を継続する

**テニス（ATP）の作業をするとき：**
1. `C:\Users\ohwada\Desktop\claude_sport\core\rules_tennis.json` を読み込む
2. `C:\Users\ohwada\Desktop\claude_sport\records\tennis\2026-ATP.json` を読み込む
3. **ユーザーが提供するJSONデータを起点にスクリーニングを開始する**（自分でオッズを調べない）
   - 大会名ではなくオッズが立っている試合を起点にすること
   - 新規試合は predictions 配列に tournament フィールド付きで追記する

**テニス（WTA）の作業をするとき：**
1. `C:\Users\ohwada\Desktop\claude_sport\core\rules_wta.json` を読み込む
2. `C:\Users\ohwada\Desktop\claude_sport\records\wta\2026.json` を読み込む

**NHL（アイスホッケー）の作業をするとき：**
1. `C:\Users\ohwada\Desktop\claude_sport\core\rules_nhl.json` を読み込む
2. `C:\Users\ohwada\Desktop\claude_sport\records\nhl\2025-26.json` を読み込む

**UFL（アメフト）の作業をするとき：**
1. `C:\Users\ohwada\Desktop\claude_sport\core\rules_ufl.json` を読み込む
2. `C:\Users\ohwada\Desktop\claude_sport\records\ufl\2026.json` を読み込む

**NFL（アメフト・9月開幕）の作業をするとき：**
1. `C:\Users\ohwada\Desktop\claude_sport\core\rules_nfl.json` を読み込む
2. `C:\Users\ohwada\Desktop\claude_sport\records\nfl\2026-27.json` を読み込む

**CFL（カナダアメフト・6月開幕）の作業をするとき：**
1. `C:\Users\ohwada\Desktop\claude_sport\core\rules_cfl.json` を読み込む
2. `C:\Users\ohwada\Desktop\claude_sport\records\cfl\2026.json` を読み込む

**NRL（ラグビーリーグ）の作業をするとき：**
1. `C:\Users\ohwada\Desktop\claude_sport\core\rules_nrl.json` を読み込む
2. `C:\Users\ohwada\Desktop\claude_sport\records\nrl\2026.json` を読み込む

**Super Rugby Pacific（ラグビーユニオン）の作業をするとき：**
1. `C:\Users\ohwada\Desktop\claude_sport\core\rules_superrugby.json` を読み込む
2. `C:\Users\ohwada\Desktop\claude_sport\records\superrugby\2026.json` を読み込む

**NBA（バスケットボール）の作業をするとき：**
1. `C:\Users\ohwada\Desktop\claude_sport\core\rules_nba.json` を読み込む
2. `C:\Users\ohwada\Desktop\claude_sport\records\nba\2025-26.json` を読み込む

3. 現在の状況を把握して「引き継ぎ完了」と報告する
4. 次の指示を待つ

---

## 【絶対禁止】架空情報の生成

選手名・チーム名・スコア・オッズ・怪我・出場情報など、架空の具体的情報を生成することは絶対禁止。

**情報の明示ルール（必ず守ること）：**
- 実際に検索・確認した情報 → そのまま具体的に記載する
- サンプル・フォーマット例を示す場合 → 必ず「【サンプル】」と明記し、`[選手名]` `[チーム名]` `[オッズ]` のようなプレースホルダーを使う
- 確認していない情報 → 「未確認」と書く
- 不明な情報 → 「不明」と書く

**絶対にやってはいけないこと：**
- 実在しない選手名・選手の怪我・出場情報・スコア・オッズを具体的な値として生成する
- 「例として」「イメージとして」という理由で架空の具体的情報を提示する（プレースホルダーを使わず）
- 未確認の情報を確認済みであるかのように記載する

このシステムはベット判断に直結するため、架空情報は実害につながる。

---

## このシステムの根幹となる価値観（必ず理解してから作業すること）

### 目的
市場（オッズ・大衆予想）とは独立して、根拠を持って正しい勝者を予測できるシステムを育てること。

### 予測とベットは別物
- **予測**：全試合を対象に勝者を予測する。外れても問題ない。**外れた理由が検証の源泉**になる
- **ベット推奨**：予測の中で信頼度≥75% AND EV>+5%を満たした試合のみ
- **EV閾値はベットするかどうかの基準であり、予測するかどうかの基準ではない**

### 記録の原則（v3.0以降）
スクリーニングした全試合に対して `predicted_winner`・`prediction_confidence`・`prediction_basis` を記録する。
tier=skip であっても予測勝者は必ず記入する。試合後に `prediction_hit` を更新することで予測精度が追跡できる。

### MISSの扱い
MISSは損失ではなく学習の機会。`miss_analysis` に「なぜ実際の勝者がモデル予測を上回ったか」を書き、
その知見を `rules_{sport}.json` に追記する。この積み重ねが予測精度の向上につながる。

### 長期目標
均衡した試合でも根拠を持って勝者を導き出せるようになること。現在のL1閾値（大きな実力差のみ対象）は
学習初期の安全設計。精度向上とともに対象試合を広げていく。

---

## プロジェクト概要

Ayumu が開発中のマルチスポーツ対応ベッティング分析システム。
**対象4種目：テニス / アイスホッケー / アメフト / ラグビー**

| 種目 | リーグ | 状態 |
|---|---|---|
| テニス | ATP | 稼働中（MC2026 F待ち 4/12） |
| テニス | WTA | 稼働中（Stuttgart 4/13開幕） |
| アイスホッケー | NHL | 稼働中（プレーオフ直前） |
| アメフト | UFL | 稼働中（Week3〜、〜6月） |
| アメフト | NFL | プレシーズン（9月開幕） |
| アメフト | CFL | プレシーズン（6月開幕） |
| ラグビーリーグ | NRL | 稼働中（Round6〜、〜9月） |
| ラグビーユニオン | Super Rugby Pacific | 稼働中（〜7月） |
| バスケットボール | NBA | 稼働中（2025-26 レギュラーシーズン終盤・プレーオフ直前） |

### フォルダ構成
```
C:\Users\ohwada\Desktop\claude_sport\
├── CLAUDE_CODE_START.md        ← このファイル（毎回最初に読む）
├── core/
│   ├── rules_tennis.json       ← ATPテニスルール v2.0
│   ├── rules_wta.json          ← WTAテニスルール v1.0
│   ├── rules_nhl.json          ← NHLルール v1.2
│   ├── rules_ufl.json          ← UFLルール v1.0（アメフト）
│   ├── rules_nfl.json          ← NFLルール v1.0（アメフト・9月〜）
│   ├── rules_cfl.json          ← CFLルール v1.0（カナダアメフト・6月〜）
│   ├── rules_nrl.json          ← NRLルール v1.0（ラグビーリーグ）
│   ├── rules_superrugby.json   ← Super Rugby Pacificルール v1.0（ラグビーユニオン）
│   ├── rules_nba.json          ← NBAルール v1.0（バスケットボール）
│   ├── rule_pipeline.json      ← ルール追加トリガー管理（候補追跡・閾値到達で自動実装）
│   └── framework.json          ← 共通設定
├── records/
│   ├── tennis/
│   │   └── 2026-ATP.json       ← ATP 2026シーズン全予測・結果（大会横断）
│   ├── wta/
│   │   └── 2026.json           ← WTA 2026の全予測・結果
│   ├── nhl/
│   │   └── 2025-26.json        ← NHL 2025-26の全予測・結果
│   ├── ufl/
│   │   └── 2026.json           ← UFL 2026の全予測・結果
│   ├── nfl/
│   │   └── 2026-27.json        ← NFL 2026-27の全予測・結果
│   ├── cfl/
│   │   └── 2026.json           ← CFL 2026の全予測・結果
│   ├── nrl/
│   │   └── 2026.json           ← NRL 2026の全予測・結果
│   ├── superrugby/
│   │   └── 2026.json           ← Super Rugby Pacific 2026の全予測・結果
│   └── nba/
│       └── 2025-26.json        ← NBA 2025-26の全予測・結果
├── stats/
│   └── cumulative.json         ← 累積統計（全種目）
└── dashboard.html              ← 閲覧用ダッシュボード（ルート直下・単一ファイル）
```

---

## 現在の状況

**→ `monitoring/pending_actions.md` を参照すること（毎セッション自動読み込み済み）**
このファイルには「現在の状況」を書かない。pending_actions.md・cumulative.json が常に最新状態を持つ。

---

## 分析フロー（種目共通）

```
① ユーザーが提供するJSONデータ（試合一覧・オッズ）を起点にスクリーニング開始
   ※ 自分でOddsPortal等を調べない。データはユーザーから受け取る。
② 対象スポーツのL1指標でスクリーニング
③ 候補のみL2〜L4を深掘り
④ 全試合に predicted_winner / prediction_confidence / prediction_basis を記録する（v3.0）
   ※ tier=skip であっても予測勝者は必ず記入する（EV閾値はベット判断のみに使う）
⑤ 信頼度≥75% AND EV>+5% → GO推奨として出力（ベット推奨トラック）
⑥ 結果確認後 → records/{sport}/{year}.json を更新（prediction_hit も更新する）
⑦ MISSがあれば miss_analysis に要因分類（L1/L2/L3/L4/External）を記録する
⑧ MISSの知見を rules_{sport}.json に追記して上書き保存
```

---

## 各種目のL1指標（早見表）

| リーグ | L1指標 | ソース | 閾値 |
|---|---|---|---|
| ATP | クレーcElo差 | tennisabstract.com | 差100以上 |
| WTA | クレーcElo差 | tennisabstract.com（Women's） | 差80以上 |
| NHL | xGF% | moneypuck.com/teams.htm | 差5pt以上 |
| UFL | 得失点差/試合 | theufl.com/stats | 差4点以上 |
| NFL | Total DVOA | footballoutsiders.com | 差10%以上 |
| CFL | 得失点差/試合 | cfl.ca/stats | 差5点以上 |
| NRL | 得失点差/試合 | nrl.com/draw | 差6点以上 |
| Super Rugby | 得失点差/試合 | super.rugby/stats | 差7点以上 |

---

## 重要な注意事項

- **記録はJSONファイルに直接書き込む**（チャット内だけで終わらせない）
- **ルール更新は必ずrules_{sport}.jsonを上書き保存する**
- **累積統計はstats/cumulative.jsonに反映する**
- **ダッシュボードは結果更新のたびに再生成する**
- **NRL（ラグビーリーグ）とSuper Rugby（ラグビーユニオン）は別競技・別ルールファイル**
- **NFL・CFLはオフシーズン中。開幕前にルールファイルを再確認してから稼働開始**

---

*このファイルはClaude Codeセッションの「記憶の入口」です。*
*毎回最初に読み込ませることで、どのセッションでも継続できます。*
