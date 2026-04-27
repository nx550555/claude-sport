# ベッティング分析システム — Claude Code 引き継ぎファイル
# このファイルをClaude Codeセッションの最初に読ませてください

---

## あなたへの指示

このファイルを読んだら、以下を実行してください：

**【毎回必須】STEP 0: システム健全性スキャン（Session_45で新設）**
他の何より先に以下を実行：
1. `python C:\Users\ohwada\Desktop\claude_sport\monitoring\health_check.py` を実行
2. 出力結果を確認:
   - `[OK] システム健全` → STEP 1 に進む
   - `[WARN] 警告` → STEP 1 に進むが、警告項目は今セッション中に対処する
   - `[ALERT] 異常` → STEP 1 に進む前に必ず異常を対処する
3. 終了コード: 0=正常 / 1=警告 / 2=異常
4. `C:\Users\ohwada\Desktop\claude_sport\monitoring\missed_tasks_log.md` を読み込み、前セッション未実施項目を次に優先対処する候補リストに加える

**【STEP 0.5 Session_47追加 2026-04-21 / Session_54 で soccer/mlb/lineups 追加】外部スタッツフィード更新 (GEN006)**
以下の fetcher を順に実行（--days-stale 3 なら 3日以上古ければ再取得、新しければ SKIP）:
```
python scripts/fetch_moneypuck.py --days-stale 3              # NHL team xGF%
python scripts/fetch_nhl_players.py --days-stale 3            # NHL skaters + goalies
python scripts/fetch_basketball_reference.py --days-stale 3   # NBA team NRtg
python scripts/fetch_nba_players.py --days-stale 3            # NBA per_game + advanced
python scripts/fetch_tennis_elo.py --days-stale 3             # ATP/WTA cElo
python scripts/fetch_tennis_player_stats.py --days-stale 7    # テニス serve/return last52
python scripts/fetch_rugby_football.py --days-stale 3 --league all   # 8リーグ standings
python scripts/fetch_injuries.py --days-stale 1 --sport all   # NHL/NBA 怪我情報
python scripts/fetch_clubelo.py --days-stale 3                # サッカー 5リーグ Club Elo
python scripts/fetch_understat.py --days-stale 3              # サッカー 5リーグ xG data
python scripts/fetch_fangraphs.py --days-stale 3              # MLB team FIP/wRC+
python scripts/fetch_baseball_savant.py --days-stale 3        # MLB Statcast xwOBA/xERA
python scripts/fetch_lineups.py --days-stale 0.5 --sport all  # スタメン (12h以内なら skip)
```
- exit code 0 or [SKIP] なら問題なし。exit code 2 (fetch failed) なら GEN006 ユーザー依頼発動
- `python scripts/stats_feed_reader.py` で feed_status() 全件を確認（health_check v4 で自動チェック済）
- **【Session_55 2026-04-23 修復メモ】** fetch_lineups.py (rotowire 全4スポーツ) / fetch_baseball_savant.py の parser 修復完了。
- **【Session_56 2026-04-23 修復メモ】** PA085 / PA086 も修復完了:
  - **fetch_understat.py**: `teamsData` JS 変数消失 → Playwright レンダリング後の HTML `<table>` 直接パース方式に書き直し。5リーグ 96 teams 取得。**soccer L1 の Elo×xG クロスチェック復活**
  - **fetch_fangraphs.py**: Cloudflare 突破不可 → 公式 MLB StatsAPI (`statsapi.mlb.com`) に切替。wRC+ は OPS+ proxy / FIP は生スタッツから計算（wRC_plus_is_proxy / FIP_is_computed フラグ付き）。30 teams 取得。**MLB L1 の Savant×StatsAPI クロスチェック復活**
  - 計算由来の値であることは `wRC_plus_is_proxy=true` フラグで明示されるため、分析時は Savant xwOBA/xERA を主、StatsAPI FIP/OPS+ を副の位置付けで使用
  - parse=0 空フィードは health_check v7 が ALERT 判定する
- Claude 分析内で:
  ```python
  from scripts.stats_feed_reader import (
    feed_status, stale_feeds,
    get_team_xgf, get_nrtg, get_tennis_elo,
    get_nhl_skater, get_nhl_goalie, get_nba_player_stats,
    get_nhl_injuries_for_team, get_nba_injuries_for_team,
    get_tennis_serve_stats, get_tennis_return_stats,
    get_league_standings, get_league_team,
    # Session_54 追加
    get_club_elo, get_league_elo_ranking, get_team_xg, get_soccer_all_teams,
    get_mlb_team, get_mlb_savant, get_mlb_all_teams,
    get_lineup, get_lineup_all
  )
  ```

---

**【毎回必須】STEP 1: 最初に必ず読む：**
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

**【Session_57 追加 2026-04-24 提案#6】日付基準統一 (CE021/CE022 再発防止):**

全 records の `date` フィールドは以下の基準で統一する:

| スポーツ | date 基準 |
|---|---|
| NHL / NBA / MLB / NFL / UFL / CFL / AHL | **ET (Eastern Time)** - 北米現地試合日 |
| NRL / Super Rugby | AEST - オーストラリア/NZ現地 |
| Premiership / Super League | BST - 英国現地 |
| Top14 / Pro D2 | CET - フランス現地 |
| ATP / WTA | local tournament 日 (大会開催地タイムゾーン) |
| Soccer (5大リーグ) | local league 日 |

**変換ルール (重要):**
- NHL 試合: JST で 4/24 午前 = ET 4/23 夜開催 → records には **ET 4/23** と記録する (× JST 4/24 ではない)
- 結果確認時 WebSearch で「April 22 ET」と出たら records date は "2026-04-22" で記録
- 混在した date が既存 records に残っている場合は `scripts/audit_date_basis.py` で検出、訂正時は CE0xx として記録する
- 単位: `YYYY-MM-DD` 形式を遵守

**【Session_57 追加 2026-04-24 提案#2】draw sheet 照合必須化 (CE019 再発防止):**
- tennis (ATP/WTA) の seeded player は R1 bye が標準 → 初戦は R2 で開催される
- `date` フィールドを訂正する場合は、必ず以下の一次ソースで round 構造を確認する:
  - ATP: `atptour.com/en/scores/current/{tournament}/draws` または `wtafiles.wtatennis.com/pdf/draws/` 
  - 同様にラグビー playoffs/PO は fixtures ページの round 構造を確認
- WebSearch snippet のみでの date 修正は**禁止**。必ず WebFetch で draw sheet を開き、該当選手が R1/R2/R3 のどのラウンドから登場するかを確認する
- seeded player + "match date X" の snippet は、R1 bye を考慮せず誤訂正を誘発するため特に注意
- この手順違反で CE019 (Mertens 4/23→4/24 再訂正) が発生 → Session_52 GEN003 誤訂正が根本原因

⚠️ この確認を飛ばして分析・記録に入ることは禁止。

**【毎回必須・最重要】システム改善提案の常時義務（GEN007 Session_54 2026-04-23 制定）：**

ユーザーとの継続契約ルール。セッションをまたいで維持する。

**Claude は以下のいずれかを認識したら、分析を一時停止して必ず改善提案を出す:**
- 新規スポーツ/リーグで当初設計の fetcher/rules が機能しない (正しいデータ取れない等)
- 手動運用されているがデータ性質的に自動化すべき (定期取得すべき)
- L1 指標が市場効率性で機能せず GO が長期間発生しない
- 同じ MISS パターンが繰り返されているがルール化されていない
- 現行 STEP 4.5 未カバー要因 (審判・天候・会場サブ要因 等) が MISS に寄与
- health_check WARN/ALERT が長期放置
- CE 系 data_error が同根で 2件以上連続発生 (構造的バグ疑い)
- fetcher 取得失敗率 30% 超 (情報源 or スクレイピング方式の見直し要)
- ユーザー手動運用の負担が特定箇所に集中 (自動化余地)
- ルールが増えすぎて矛盾/重複発生 (ルール統合/整理提案)

**提案フォーマット (必須)**:
```
【GEN007 改善提案】
現象: (観察した事実)
影響: (正答率・運用効率・判断精度のどれに効くか)
提案: (ファイル名・ルールID・自動化範囲を具体的に)
工数感: 即日 / 1セッション / 複数セッション
ユーザー判断依頼: 採択/却下/保留
```

**判断フロー**:
1. Claude が問題認識 → 分析停止
2. 提案提示
3. ユーザー回答: 採択/却下/保留
4. 採択 → 即実装 or 明示時期に実装
5. 却下 → 却下理由を rules_log.json に記録 (繰り返し禁止)
6. 保留 → pending_actions.md に保留タスク登録

⚠️ **遠慮して提案しないことの方がルール違反**。改善提案は控えめにせず、気付いた時点で積極的に出す。ユーザー側が『不要』と判断すれば即却下可。このシステムの最終目的は正答率向上であり、仕組みを変えずに使い続けることは目的に反する。

---

**【毎回必須】既分析データの再提供時ルール（GEN004）：**
ユーザーが `手動試合データ/*.json` を提供した際、過去に受取・分析済みの試合が再度含まれている場合は以下の手順で処理する：

1. **試合照合**：提供データの各試合を `records/{sport}/*.json` と照合する
   - 一致判定基準: 同一対戦カード + 同一日付 / または round + player/team名一致
2. **オッズ比較**：既分析済み試合について、新オッズと記録済み `rec_odds`（GO/CAUTIONのみ）を比較
3. **判定分岐**：
   - **新規試合** → 通常のスクリーニング実行
   - **既分析 + オッズ変化あり** → EV再計算（`(推定勝率 × 新オッズ) - 1`）して records JSON の `rec_odds` と `ev` を更新。閾値を割り込めば tier 変更（GO→CAUTION等）
   - **既分析 + オッズ変化なし** → 何もしない（ログに「既分析・変化なし」と一行記録）
4. **オッズ変化の許容範囲**：±0.01 未満は「変化なし」扱い。±0.01以上は再計算。
5. **記録**: 再計算実行時は records の該当試合に `odds_updated_at` フィールドを追加（いつ・どう変化したか）

この手順は提供されたデータ起点のルーチン処理。ユーザーへの確認なしで実行可。

---

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

**【STEP 4.5 追加 Session_54 2026-04-23】スタメン確認フロー（必須）：**

対象スポーツ: **NBA / NFL / サッカー / MLB / ラグビー全種 (NRL/Super Rugby/Premiership/Top 14/Pro D2/Super League)**

L1 スクリーニング通過後 → GO昇格判定の間に以下を実行する:

1. **L1 通過試合を `tier: "provisional_go"` (仮GO候補) として records に記録**
2. **スタメン取得**: `python scripts/fetch_lineups.py --sport {sport}` を実行、または `scripts/stats_feed_reader.py::get_lineup(sport, team, date)` で読み込み
3. **主力欠場チェック (スポーツ別)**:
   - **NBA**: 欠場者 (DNP/Out) + ミニットリストリクション (Load Management)
   - **NFL**: QB 出場可否 + 主要スキルポジション (WR1/RB1/TE1)
   - **サッカー**: GK 起用 + 主力FW (得点源) + CB + キャプテン + フォーメーション変更
   - **MLB**: 先発投手 (SP) 確定 + 打線左右構成 + 3-4-5番出場
   - **ラグビー**: フロントロー (Prop/Hooker) + SO (スタンドオフ = #10) / halves (リーグ系は 6/7)
4. **L4 ルールを適用し confidence を再計算**
5. **再計算後も `conf>=75% AND EV>+5%` (Basic は `conf>=78% AND EV>+7%`) を満たせば `tier: "go"` に昇格**
6. **正式GO昇格と同時にメール通知を送信** (`scripts/notify_go_candidate.py`)
   - 内容: 試合名・キックオフ時刻・推奨ベット・オッズ・conf・EV・確認済みスタメン・判断期限

**タイミング (キックオフからの逆算):**
| スポーツ | スタメン発表 | 実行タイミング |
|---|---|---|
| サッカー | 75分前 | キックオフ75分前に fetch_lineups.py |
| MLB | 前日夜〜当日朝 | JST 10:00 に fetch_lineups.py |
| NBA | 90分前 | キックオフ90分前に fetch_lineups.py |
| NFL | 90分前 | キックオフ90分前に fetch_lineups.py |
| ラグビー | 48時間前〜75分前 | キックオフ75分前に fetch_lineups.py |

⚠️ スタメン未発表の状態で GO 昇格判定は禁止。`provisional_go` のままキックオフを迎えた場合は `tier: "caution_waiting"` に自動格下げ。

---

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
   - **[Session_45 仕様訂正 2026-04-20]** 以下の両方を必ず出力する：
     - **(A) 総合勝率 TOP 5**（全体勝率降順。EV問わず・参考情報）
     - **(B) EV最大 TOP 5**（EV降順。EV+ があればベット推奨候補、全EV-なら損失幅最小の組み合わせを参考列挙）
   - EV+が存在する場合は **(B)** を中心にベット推奨として取り扱う
   - 全EV-の場合も「EV+の組み合わせなし」と一言で済ませず、(A)(B) TOP 5 は必ず掲載する（情報価値担保）
   - Session_29実例: Musetti/Louisville/Renegades のような個別EV+試合が2件以上揃うと EV+マルチが成立する
3. `records/multi_bets.json` の sessions 配列に追記する
4. `dashboard.html` の「高確率予想」「マルチベット」タブを更新する
5. **出力Aのアップセット分析への活用**：
   - 出力Aに含まれた試合の `prediction_hit` を結果確認後に必ず更新する
   - 出力A内で `prediction_hit: false`（外れ）だった試合は必ず `miss_analysis` を records JSON に追記する
   - miss_analysis の内容を `rules_{sport}.json` に知見として追記する（アップセット要因の蓄積）
   - 特に「高確率予想に入ったがMISSした」試合はアップセットの典型例として `rule_pipeline.json` の候補にも記録する

**【結果反映 STEP 0.5・毎回必須】scope外 UPSET スキャン SOP（Session_62 2026-04-27 制定）：**

> **背景**: Session_61 で Phase2 scope外UPSET (TOR-CLE / Baptiste-Paolini / HOU-LAL 等 9件) の検出がユーザー質問契機で行われた。自発的に検出する SOP が定義されておらず、結果として R024 implement トリガーを偶発的に獲得していた。本 SOP は scope外UPSET 検出を「結果反映フローに組み込まれた必須工程」として標準化し、受動的検出構造を排除する。

**位置付け**: 試合結果を records/*.json に書き込んだ **直後**、ダッシュボード同期プロトコル (下記) の **直前** に必ず実行する。

### 1. スキャン対象の定義

結果確認した試合のうち、以下のいずれかに該当する全試合を「scope外UPSET 候補」としてスキャン:

- **市場 favorite 敗戦**: 試合の市場 favorite 側オッズ ≤ 1.50 (= implied prob ≥ 66.7%) であった試合で、その favorite が敗戦した
- **GO/CAUTION 推奨と無関係**: tier=skip / 未スクリーニング / 推奨対象外として処理した試合も含める (今までの推奨外であっても scope外検出する)
- **records 未登録試合も対象**: 同日同スポーツで結果確認したが records にエントリがない試合 (Bristol-Newcastle Premiership 等の Session_61 検出例) も拾う

### 2. スキャン実行手順

1. 当該結果反映バッチで取得した全試合データから、以下の3条件を機械的に判定:
   - (a) 市場 favorite オッズ ≤ 1.50 か
   - (b) 該当 favorite が敗戦したか
   - (c) (a) かつ (b) を満たすか
2. (c) を満たす試合を「scope外UPSET 候補リスト」として列挙
3. リスト件数が 0 件 → 「scope外UPSET なし」と一行報告して STEP 0.5 終了
4. リスト件数が 1 件以上 → **ユーザーに以下フォーマットで提示**:

```
【scope外UPSET 検出: N件】
| # | 試合 | スポーツ | 市場fav | favオッズ | 結果 | records登録状況 |
|---|---|---|---|---|---|---|
| 1 | XXX vs YYY 4/27 | NBA | XXX | 1.42 | YYY win | 未登録 |
| 2 | ... | ... | ... | ... | ... | 登録済 (tier=skip) |

【ユーザー判断依頼】
各試合について以下のいずれかを返答してください:
(A) records に新規登録する (未登録試合のみ) / upset_patterns に Axxx として登録する
(B) upset_patterns 登録のみ (records 既登録 or 登録対象外の場合)
(C) 無視 (記録対象外と判断)
```

5. ユーザー回答を待つ。Claude 自発判断による upset_patterns / records 反映は **禁止** (柱A 承認制と整合)
6. ユーザー回答後にのみ、指示された範囲で upset_patterns.json / records/*.json に反映

### 3. スキャン後の rule_pipeline.json への影響

ユーザーが (A) または (B) を承認した case のみ、対応する候補ルール (P***) の `evidence` 配列に追加する:

- evidence 追加自体は「日常運用ファイル更新 (A 区分)」として確認不要 (`feedback_git_upload.md` 階層化ルール参照)
- ただし `current_count` インクリメントの結果 `current_count >= trigger_threshold` に到達した場合は status を `ready_for_proposal` に変更し、**次セッション開始時** に提案レポート生成 (柱A 承認制プロセスに乗せる)
- 同一セッション内 (同一 turn 内) での implement は禁止 (Session_61 R024 forbidden_practice)

### 4. 記憶ベース推論の禁止

scope外UPSET 候補の miss_analysis を記述する際、記憶ベース補完 (例: Session_61 A038「Madrid altitude (1500m) で sub-altitude ball change が rhythm 破壊」) は禁止。柱C 情報源タグ義務化 (フェーズ4 で実装予定) に従い、必ず [FETCH:URL] / [SEARCH] / [MEMORY] / [INFER] のいずれかを付与する。

### 5. SOP の運用境界

- **適用シーン**: 「結果確認」「結果反映」「prediction_hit 更新」を伴う全セッション
- **非適用シーン**: スクリーニングのみ (結果未確定時) / 提案レポート生成のみ / dashboard 同期単独実行
- **frequency**: 結果反映バッチごとに最低 1回。ユーザーが「結果確認終わり」と区切った時点で STEP 0.5 を実行

### 6. Session_61 逸脱パターンの再発防止

- **逸脱**: 「アップセットありませんでしたか」というユーザー質問への応答中に scope外UPSET スキャンを実施した
- **本 SOP による防止**: 結果反映時の必須工程として組み込まれるため、ユーザー質問の有無に関わらず実行される
- **検証方法**: 結果反映 commit と同時に「STEP 0.5 実施済」ログを `monitoring/pending_actions.md` または記録 commit message に明示

---

**【記録更新後・毎回必須】ダッシュボード同期プロトコル（整合性保証）：**
試合結果を records/*.json に書き込んだら、必ず以下を実行する：

1. `core/dashboard_stats.json` を更新する（各sport の go_count / confirmed_count / hit_count / hit_rate / ev_total / pending_count を再計算）
2. `python sync_sport_cards.py` を実行してダッシュボードに反映する
3. dashboard.html の「アクティブ推奨」タブから完了した試合を削除する
4. **【2026-04-20 追加】** `records/multi_bets.json` の `sessions` 配列末尾の日付が本日 or 最新セッションか確認し、古ければ新規sessionエントリを追記する（output_a/output_b / GOが出なくても「該当なし」として記録）
5. **【2026-04-20 追加】** dashboard.html の「予測精度」タブ・「成長分析」タブの末尾数値（big-stat / 累積EV / 種目別正答率）を dashboard_stats.json と突き合わせて更新する
6. **【2026-04-20 追加】** dashboard.html の「高確率予想」「マルチベット」タブ先頭の **🎯 アクティブ候補** セクション（未確定=ベット対象）を最新状態に更新する。試合完了した候補は累計履歴へ移し、新規pending GO推奨を追加。アクティブ1件以下の場合はマルチ構成不可と明示。
7. 更新後に概要big-stat・各スポーツカード・予測精度タブ・成長分析タブ・高確率予想タブ（アクティブ候補+累計履歴）・マルチベットタブ（アクティブマルチ+累計履歴）の全数値を目視で確認し、不整合があれば即修正する

⚠️ **records更新 → dashboard_stats.json更新 → multi_bets.json更新 → sync実行 → 予測精度/成長分析タブ更新 の5ステップを必ずセットで行うこと（2026-04-20改訂）。**
⚠️ **この手順を省略してダッシュボードの数字がずれることは絶対に禁止。**

**【運用改善 2026-04-20 Session_44】** Session_30〜43で multi_bets.json 更新が抜け、ダッシュボードの高確率予想・マルチベットタブが Session_29 のまま停滞していた事故の再発防止策:
- 毎セッション終了時に「multi_bets.json の最新 session date == 本日 or 直近スクリーニング日か？」を必須チェック
- 全SKIPのセッションでも「候補なし」session エントリを追記し、スクリーニング実施痕跡を残す
- pending_actions.md に常設タスク `PA-PERM01: 出力A/B 最新化確認` を追加（毎セッション冒頭でOPEN→終了時にDONE）

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
3. **【Session_46 追加 2026-04-20】試合前48時間以内に必ず両チームの team sheet を確認**（怪我人ローテーション / SR006）
4. **【Session_46 追加 2026-04-20】試合当日の天候予報 (metservice.com) を必ず確認**（大雨×パスラン型チームの崩壊リスク / SR007）

**NBA（バスケットボール）の作業をするとき：**
1. `C:\Users\ohwada\Desktop\claude_sport\core\rules_nba.json` を読み込む
2. `C:\Users\ohwada\Desktop\claude_sport\records\nba\2025-26.json` を読み込む

**England Premiership（ラグビーユニオン・英国）の作業をするとき：**
1. `C:\Users\ohwada\Desktop\claude_sport\core\rules_premiership.json` を読み込む
2. `C:\Users\ohwada\Desktop\claude_sport\records\premiership\2026.json` を読み込む
3. **【Session_46 追加 2026-04-20】試合前48時間以内に必ず両チームの team sheet を確認**（怪我人ローテーション / P006）。Champions Cup週・6 Nations明けは主力欠場顕著
4. **【Session_46 追加 2026-04-20】試合当日の天候予報 (metoffice.gov.uk) を必ず確認**（大雨×パスラン型チームの崩壊 / P007）

**Top 14（ラグビーユニオン・フランス1部）の作業をするとき：**
1. `C:\Users\ohwada\Desktop\claude_sport\core\rules_top14.json` を読み込む
2. `C:\Users\ohwada\Desktop\claude_sport\records\top14\2026.json` を読み込む
3. **【Session_46 追加 2026-04-20】試合前48時間以内に必ず両チームの team sheet を確認**（怪我人ローテーション / T006）。特にChampions Cup 翌週は主力大量欠場に注意
4. **【Session_46 追加 2026-04-20】試合当日の天候予報 (meteofrance.fr) を必ず確認**（大雨×パスラン型チームの崩壊 / T007）

**Pro D2（ラグビーユニオン・フランス2部）の作業をするとき：**
1. `C:\Users\ohwada\Desktop\claude_sport\core\rules_prod2.json` を読み込む
2. `C:\Users\ohwada\Desktop\claude_sport\records\prod2\2026.json` を読み込む
3. **【Session_46 追加 2026-04-20】試合前48時間以内に必ず両チームの team sheet を確認**（怪我人ローテーション / D006）
4. **【Session_46 追加 2026-04-20】試合当日の天候予報 (meteofrance.fr) を必ず確認**（大雨×パスラン型チームの崩壊 / D007）

**Super League（ラグビーリーグ・英国）の作業をするとき：**
1. 暫定: NRLルールを準拠 (`core/rules_nrl.json` 参照)。独自rules_superleague.jsonは未作成
2. `C:\Users\ohwada\Desktop\claude_sport\records\superleague\2026.json` を読み込む

**AHL（American Hockey League・アイスホッケー）の作業をするとき：**
1. `C:\Users\ohwada\Desktop\claude_sport\core\rules_ahl.json` を読み込む
2. `C:\Users\ohwada\Desktop\claude_sport\records\ahl\2025-26.json` を読み込む
3. Basic Tier運用（xGF%なし・GF%のみ）。精度はNHLより劣る前提で扱う

**サッカー（Premier League / La Liga / Bundesliga / Serie A / Ligue 1）の作業をするとき【Session_54 新規追加】:**
1. `C:\Users\ohwada\Desktop\claude_sport\core\rules_soccer.json` を読み込む
2. `C:\Users\ohwada\Desktop\claude_sport\records\soccer\2025-26.json` を読み込む
3. L1 = clubelo Elo (50pt以上差) + understat xGD/G (0.6以上差) のクロスチェック
4. **STEP 4.5 必須**: キックオフ75分前に `fetch_lineups.py --sport soccer` → GK/主力FW/CB/キャプテン/フォーメーション確認 → EV再計算
5. データソース: clubelo.com (Elo) / understat.com (xG) / rotowire.com/soccer/lineups.php (XI)

**MLB（メジャーリーグベースボール）の作業をするとき【Session_54 新規追加】:**
1. `C:\Users\ohwada\Desktop\claude_sport\core\rules_mlb.json` を読み込む
2. `C:\Users\ohwada\Desktop\claude_sport\records\mlb\2026.json` を読み込む
3. L1 = FanGraphs wRC+ (10pt以上差) + FIP (0.4以上差) のクロスチェック
4. **STEP 4.5 必須**: JST 10:00 頃に `fetch_lineups.py --sport mlb` → 先発投手確定 + 打線左右 + 3-4-5番確認 → EV再計算
5. データソース: FanGraphs (FIP/wRC+) / Baseball Savant (xwOBA/xERA) / rotowire.com/baseball/daily-lineups.php
6. 先発投手が未確定の状態でGO判断は禁止 (M002)

3. 現在の状況を把握して「引き継ぎ完了」と報告する
4. 次の指示を待つ

---

## 【ルール改訂統制プロトコル】Session_62 2026-04-27 制定

Session_61 で R024 (form slump 補正) を同一 turn 内で evidence 3/3 → implement したことを契機に、ルール改訂全般をユーザー承認制に移行する。

### 1. 適用対象 (承認必須ファイル)

以下のファイル変更は本プロトコルの適用対象。**ユーザー承認なしでの編集を禁止**:

- `core/rules_*.json` (R*** / N*** / W*** / M*** / S*** 等のルール本体) の **追加・改訂・削除**
- `core/rule_pipeline.json` の P*** 候補の **status 変更** (特に `implemented` / `approved_pending_implementation` / `rejected` への移行)
- `core/framework.json` の改訂
- その他、予測モデルの判定ロジックに影響する設定ファイル

### 2. 適用対象外 (従来通り確認不要)

以下は日常運用ファイルとして従来通り確認なしで編集可:

- `records/{sport}/*.json` (試合結果・予測記録)
- `dashboard.html` および `core/dashboard_stats.json`
- `scripts/*.py` (fetcher / sync / 分析ヘルパー)
- `monitoring/*.md` (pending_actions / user_feedback_log / claude_error_log 等)
- `stats/*.json` の運用統計更新 (cumulative.json 等)
- `BACKLOG.md` / `session_logs/*.md`
- `core/rule_pipeline.json` の `evidence` 追加 / `current_count` インクリメント (status 変更を伴わない範囲)

### 3. 新規ルール実装プロセス (rule_pipeline.json 経由)

1. P*** 候補の `current_count >= trigger_threshold` 到達 → status を `ready_for_proposal` に変更 (この変更自体は確認不要)
2. **次セッション開始時** に『実装提案レポート』を生成。同一セッション内・同一 turn 内での implement は禁止
3. 提案レポートの必須項目:
   - (a) 候補ルール ID と提案タイトル
   - (b) 既存ルールへの影響範囲 (関連 R*** ID と影響予測)
   - (c) evidence 3件の引用元 URL と **一次ソース fetch の有無** (WebFetch 本文取得済か WebSearch スニペットのみか)
   - (d) 承認時の cumulative.json への影響シミュレーション (過去予測への遡及適用で hit_rate / EV がどう変動するか)
   - (e) 却下時の代替案 (より緩い補正値、適用条件絞り込み等)
4. ユーザー判断: `承認` / `却下` / `修正後再提案`
5. 承認後にのみ `rules_*.json` への実装を実行

### 4. 既存ルール改訂プロセス (R*** / N*** 等の v_X.0 → v_Y.0)

既存 implemented ルールの body / evidence / application を変更する場合も承認必須:

1. **改訂前に「v_X.0 → v_Y.0 差分レポート」を生成**
   - 旧定義 (適用条件・補正値・閾値)
   - 新定義 (上記の対応箇所)
   - 改訂根拠の evidence (最低 3件 + **反例検証** 必須)
   - 影響範囲 (適用対象選手・チーム・試合のリスト、過去予測への遡及影響)
2. **evidence 1件のみでの即改訂は禁止** (Session_61 R017 v2.0 の Vacherot 1件改訂は逸脱事例)
3. ユーザー承認後に rules_*.json を編集

### 5. 禁止事項 (再発防止)

以下は Session_61 で発生した逸脱パターン。**いずれも禁止**:

- 同一 turn 内での `evidence 3/3 到達 → implement` (R024 の過剰スピード実装)
- ユーザー質問への応答中に「ついでに」ルール改訂を実行
- evidence 1件のみでのルール改訂 (反例検証なし)
- ユーザー確認なしの既存ルール v_X.0 → v_Y.0 改訂
- 「次のセッション開始時」を待たずの自動実装

### 6. 競合解消ルール

`memory/feedback_git_upload.md` の「コミット・プッシュ・ファイル書き込みは確認なしで即実行」の規定と本プロトコルが衝突する場合、**本プロトコルが優先**する。日常運用ファイルは従来通り確認不要、判定ロジックに影響するファイルは承認必須、という階層化で運用する。

---

## 【柱C: 一次ソース fetch 義務化】Session_62 2026-04-27 制定

> **背景**: Session_61 運用品質診断 v2 で、WebFetch 本文取得 0件成功・SNS/監督会見 0件・構造化スタッツサイト 0件のまま miss_analysis を記述し、記憶ベース推論で「Madrid altitude (1500m) で sub-altitude ball change が rhythm 破壊」のような事実根拠を伴わない主張を evidence として採用した事象が発生 (項目C 自己評価 2/5)。本プロトコルは MISS の重要度に応じた fetch 統制を義務化し、一次ソースに基づく分析品質を担保する。
>
> 本セクションは段階的に追記される。ステージ1 (4-1 MISS 重要度3段階分類) を本フェーズで先行実装し、ステージ2 (4-2 fetch 件数規定) / ステージ3 (4-3 情報源タグ義務化) は後続ステージで追記する。

### 4-1. MISS 重要度3段階分類

records/{sport}/*.json の `prediction_hit=false` エントリには `miss_class` フィールドを必須付与する。**新規 MISS 発生時のみ付与開始** (既存記録への遡及付与は実施しない)。

#### 判定条件 (機械判定可能な tier / quadrant ベース)

| Class | 判定条件 | 運用上の意義 |
|---|---|---|
| **A: 高重要度** | `tier ∈ {go, upset_pick}` の MISS (実損失あり) | ベット P&L に直結。予測モデルの根幹に関わる失敗 |
| **B: 中重要度** | (a) `tier ∈ {caution, caution_margin, provisional_go}` の MISS / (b) `quadrant=Q3_output_a` (conf≥85%) の MISS | ベット影響なしだが確実視判断のズレ。Track 2 (モデル品質) の信頼性に影響 |
| **C: 低重要度** | (a) `tier=skip` の MISS / (b) `quadrant=Q3_mid` (80≤conf<85%) の MISS / (c) `quadrant=Q4_upset_watch` HIT / (d) **scope外UPSET** (records 未登録だが市場fav≤1.50 敗戦) | 予測対象外・参考データ。ルール強化のための長期蓄積用 |

#### confidence_drift フラグ (HIT 内 confidence 乖離大の追跡)

HIT であっても推定勝率と試合内容に大きな乖離がある場合、`confidence_drift` フィールドを付与し Class B 相当の深掘り対象とする。

- **フィールド定義**: `confidence_drift: "high" | null` (2値構造。`"low"` は本フェーズでは未定義のため不採用。将来拡張時にフェーズ6 / 別タスクで再設計する)
- **判定基準**: 「推定勝率 ≥ 80% で予想したのに、実際は接戦/僅差勝利だった場合」に `"high"` を付与
- **種目別の薄勝ち閾値**: **TBD: フェーズ6 統合動作確認時に確定**
  - 想定例 (確定前の参考): テニス 3セット縺れ / NHL OT勝利 / NBA 1桁差 / サッカー 1点差 / MLB 1点差 / NFL TD1個差以内 / NRL TD1個差以内
  - 各種目の具体数値は本フェーズでは確定せず、フェーズ6 で協議
- **本フェーズでは枠組みのみ実装**。具体閾値確定までは `confidence_drift` フィールド付与は任意。確定後に必須化

#### miss_class フィールド必須付与ルール

- **対象**: フェーズ4 承認後の **新規** `prediction_hit=false` エントリのみ
- **遡及付与なし**: 既存 records/*.json 100件超への遡及付与は実施しない
- **付与タイミング**: 結果反映で `prediction_hit=false` を確定した時点で同時付与
- **値**: `"A"` / `"B"` / `"C"` の3値必須 (空・null は禁止)
- **scope外UPSET の扱い**: records 未登録 → ユーザー承認後に records 登録時に `miss_class: "C"` 付与
- **記述例**:
  ```json
  {
    "match": "...",
    "tier": "go",
    "prediction_hit": false,
    "miss_class": "A",
    "miss_analysis": "..."
  }
  ```

#### v3.0 2トラック精度管理との整合性

- **Track 1 (ベット推奨収益性)**: Class A / B(a) のみ寄与
- **Track 2 (全試合モデル品質)**: Class A / B / C 全件寄与
- 既存 `prediction_hit` フィールドは維持。`miss_class` は補助フィールドとして追加するのみ
- `cumulative.json` への `by_miss_class` 集計セクション追加は本フェーズ範囲外 (フェーズ6 後の別タスクで検討)

### 4-2. fetch 件数規定

MISS 分析で参照する一次ソースの最低件数を Class 別に規定する。本規定は **新規 MISS 発生時の調査強度** を統制するもので、既存記録への遡及適用は実施しない。

#### Class 別 WebFetch 必須件数

| Class | WebFetch 最低成功件数 | ソース内訳必須要件 |
|---|---|---|
| **A: 高重要度** | **3 件以上** | (a) 公式試合レポート 1件 / (b) 詳細スタッツサイト 1件 / (c) 選手・監督コメント or ニュース記事 1件 |
| **B: 中重要度** | **2 件以上** | (a) 公式試合レポート 1件 / (b) 詳細スタッツ or ニュース記事 1件 |
| **C: 低重要度** | **1 件以上** | (a) 公式試合レポート or 信頼スタッツサイト 1件 |
| **HIT confidence_drift=high** | Class B 相当 (2 件以上) | Class B 内訳に準じる |

#### WebSearch スニペット原則

WebSearch のスニペット (検索結果リスト内の抜粋テキスト) は **fetch カウント対象外**。理由:

- スニペットは検索エンジン側の要約であり、元記事の前後文脈が省略される
- 抜粋部分の正確性が検証できない
- Week / Round / 日付の混同を誘発する (CE013 再発リスク)

fetch は **WebFetch で本文取得した URL のみ** を有効カウントとする。WebSearch は補助情報 (URL 候補の発見・スニペット予備調査) として位置付け、確定根拠としては扱わない。

#### fetcher 経由 (構造化スタッツ) のカウント

`scripts/fetch_*.py` 経由で取得済の構造化スタッツデータ (`stats/feeds/*.json` 配下) は **WebFetch 1件相当としてカウント可**。ただし以下の条件を満たすこと:

- 該当 fetcher の最終取得が `--days-stale` 規定内 (鮮度 OK) であること
- `scripts/stats_feed_reader.py` の `feed_status()` で `OK` 判定であること
- タグは `[FETCHER:src]` で別タグ扱い (具体仕様はステージ3 で定義)

#### fetch 失敗時の運用 (3回試行 + [FETCH_FAILED] フラグ)

WebFetch で 403 / 404 / timeout が発生した場合:

1. **試行1**: 同種別の代替ソース 1件を試行 (例: atptour.com 失敗 → tennisabstract.com)
2. **試行2**: 別種別ソースを 1件試行 (例: スタッツサイト失敗 → ESPN記事)
3. **試行3**: 計3回試行しても fetch 必須件数を満たせなければ、以下を実施:
   - `miss_analysis` に `[FETCH_FAILED:URL1, URL2, URL3]` タグを明示 (具体タグ仕様はステージ3 で定義)
   - 当該 records エントリに `investigation_status: "investigation_incomplete"` を付与
   - 次セッション再試行を `monitoring/pending_actions.md` に登録

#### investigation_incomplete のまま evidence 加算禁止 (柱A 整合)

`investigation_status: "investigation_incomplete"` のまま `core/rule_pipeline.json` の `evidence` 配列への加算は **禁止**。理由:

- evidence 蓄積は最終的に `current_count >= trigger_threshold` 到達時に提案レポート生成 → ルール実装に繋がる
- 不完全調査による evidence 加算は柱A 承認制プロセスの根拠を毀損する
- 調査完了 (規定件数達成 or ユーザー判断による打切り) してから evidence 加算する運用とする

#### claude_sport で参照する一次ソースサイト推奨リスト

| 種目 | 公式試合レポート | 詳細スタッツ | コメント / ニュース |
|---|---|---|---|
| **ATP テニス** | atptour.com | tennisabstract.com | espn.com (tennis) / theathletic.com |
| **WTA テニス** | wtatennis.com | tennisabstract.com (Women's) | espn.com / theathletic.com |
| **NHL** | nhl.com (gamecenter) | moneypuck.com / naturalstattrick.com | espn.com / theathletic.com |
| **NBA** | nba.com (boxscore) | basketball-reference.com / cleaningtheglass.com | espn.com / theathletic.com |
| **MLB** | mlb.com | baseballsavant.mlb.com / fangraphs.com | espn.com / theathletic.com |
| **NFL** | nfl.com | pro-football-reference.com / footballoutsiders.com | espn.com / theathletic.com |
| **CFL** | cfl.ca | cfl.ca/stats | tsn.ca |
| **UFL** | theufl.com | theufl.com/stats | espn.com |
| **NRL** | nrl.com (match center) | nrl.com/draw | foxsports.com.au |
| **Super League** | superleague.co.uk | rugby-league.com | bbc.co.uk/sport/rugby-league |
| **Super Rugby** | super.rugby | super.rugby/stats | rugbypass.com |
| **Premiership** | premiershiprugby.com | premiershiprugby.com/stats | rugbypass.com / bbc.co.uk |
| **Top 14 / Pro D2** | lnr.fr | lnr.fr/stats | rugbypass.com / midi-olympique.fr |
| **AHL** | theahl.com | theahl.com/stats | thehockeynews.com |
| **サッカー (5大リーグ)** | premierleague.com / laliga.com / bundesliga.com / legaseriea.it / ligue1.com | understat.com / fbref.com | espn.com / bbc.co.uk |
| **横断 (全種目)** | flashscore.com / sofascore.com | sofascore.com / flashscore.com | (該当なし) |

注意:
- 上記リストは **fetch 対象としての候補一覧** であり、各サイトの WebFetch 成功実績は本フェーズでは未検証。実績は運用で蓄積する
- Cloudflare 等の保護で WebFetch が 403 失敗するサイト (例: Session_61 で atptour.com 失敗) は試行1 で代替へフォールバックする
- fetcher 経由 (`scripts/fetch_*.py`) で既に成功実績があるサイト (moneypuck / basketball-reference / understat / baseball-savant 等) は fetcher 経由カウントを優先利用すること

### 4-3. 情報源タグ義務化 (ステージ3 で追記予定)

(本ステージでは未実装。ステージ3 で 5種タグ仕様 + 主張ごと付与 + タグなし禁止 + 良い例/悪い例 + CHECK-2 連携 + セッション固有スクリプト生成時のタグ義務を追記する)

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

### 🧭 スクリーニング4象限フレームワーク（Session_45 正式化）

ユーザー構想の ①-1〜①-4 を運用仕様として明文化。**全試合は必ず以下4象限のいずれかに分類してタグ付け**する。

|  | **EV+（ベット推奨）** | **EV-（ベットしないが予測）** |
|---|---|---|
| **本命側（Favorite）** | **Q1_go**<br>conf≥75% AND EV>+5% | **Q3_output_a**<br>conf≥85%（EV問わず）<br>**Q3_mid**<br>conf 80-84%（追跡中・別集計） |
| **アップセット側（Dog）** | **Q2_upset_pick**<br>UF≥3 AND div≥15pp | **Q4_upset_watch**<br>dog odds≥3.0 AND UF≥2 |
| **（どれも該当しない）** | → **skip**（L1差なし・UF因子なし・確実性低） | → **skip** |

**【Session_56 2026-04-23 追加】Q3_mid の取り扱い:**
- Q3_output_a (conf≥85%) とは別バケットで管理。cumulative.json / dashboard.html / multi_bets.json で**必ず分離表示**する
- 目的: 中確実性帯の予測精度を別軸で追跡し、L1+L2深掘りで 85%以上に引き上げられる試合パターンを発見する
- 統合・混在は禁止 (Q3_output_a の hit_rate を薄めないため)

**4象限の運用ルール（必須遵守）：**
1. **全試合に `quadrant` フィールドを付与**（Q1_go / Q2_upset_pick / Q3_output_a / **Q3_mid** / Q4_upset_watch / skip のいずれか）
2. **Q1〜Q4 すべて深掘り対象**：Q1だけでなく Q2/Q3/Q4 も ②深掘り分析（WebSearch・スタッツ・怪我・フォーム等）を実施する
3. **③検証は全象限で実施**：GO hit/miss だけでなく、Q3出力A・Q2/Q4 アップセット予測の精度も `stats/cumulative.json` の `by_quadrant` で追跡
4. **④ルール強化は全象限の知見から**：Q3のMISS/Q4でのUPSET発生などもrule_pipelineに登録

**分類手順（GEN005+Q3/Q4拡張）：**
1. L1-L4 で本命側の confidence を算出
2. UF因子（UF01〜UFA06）を**機械的に全件walkthrough**し、該当数を記録
3. 市場乖離（div pp = fav_implied - dog_implied）を計算
4. 以下のテーブルで4象限分類：
   - UF 0-1個 + conf<80% + EV<+5% → **skip**
   - UF 0-1個 + conf<80% + EV>+5% → **Q1_go** (conf≥75% 必須)
   - UF 0-1個 + 80≤conf<85% → **Q3_mid** (Session_56 新設・別集計追跡)
   - UF 0-1個 + conf≥85% → **Q3_output_a**
   - UF 2個 + div 10-15pp → **Q4_upset_watch**（CAUTION相当）
   - UF 3個以上 + div≥15pp → **Q2_upset_pick**
5. Q1 と Q2 は同一試合で排他（同時成立禁止）
6. Q3 と Q4 は共存可（本命側高確実 + アップセット観察値）

### Phase1 → Phase2 移行（2026-04-18実施）
Phase1最終成績 **19/24 (79.2%) / +4.10u** でT3達成 → Phase2に移行。Phase2では **UPSET_PICK**（旧GAMBLE_BETから改名）を正式運用。

**GEN005衝突解消ルール（スクリーニング時の必須プロセス）:**
1. L1〜L4で本命側の confidence を算出
2. 同時に UF因子（upset_factors）を全てチェック
3. 以下のテーブルで推奨トラック決定:
   - **UF因子 0-1個 + 乖離<10pp** → GO推奨（通常）
   - **UF因子 2個 + 乖離10-15pp** → CAUTION（ベット見送り・検証用）
   - **UF因子 3個以上 + 乖離≥15pp** → **UPSET_PICK**（アンダードッグ推奨）
4. GO と UPSET_PICK は同一試合で**排他**（同時成立禁止）
5. stake は両トラックとも **1u 統一**（過去GB001のみ当時stake 0.25uを記録保持）

**重要な意識変更:** 「GAMBLE_BET」（ギャンブル）ではなく「UPSET_PICK」（分析による逆張り予測）。アップセット要因が検知できる時点で本命の確信度は必然的に揺らぐため、排他運用で推奨トラックを明確化する。

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
