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
| # | 試合 | スポーツ | 市場fav | favオッズ | 結果 | records登録状況 | Claude 推奨区分 |
|---|---|---|---|---|---|---|---|
| 1 | XXX vs YYY 4/27 | NBA | XXX | 1.42 | YYY win | 未登録 | 区分1 (理由: scope内Playoffs) |
| 2 | ... | ... | ... | ... | ... | 登録済 (tier=skip) | 区分2 (理由: 既登録 + 関連試合) |

【ユーザー判断依頼】
各試合について以下のいずれかを返答してください:
(A) records に新規登録する (未登録試合のみ) / upset_patterns に Axxx として登録する = **区分1 (full_record)**
(B) upset_patterns 登録のみ (records 既登録 or 登録対象外の場合) = **区分2 (reference_only)**
(C) 無視 (記録対象外と判断) = **区分3 (skip_record)**

※ Claude 推奨区分は柱D 3区分定義 (CLAUDE.md 「【柱D: 記録対象判断テーブル】」セクション 1. 3区分定義 (record_class) 参照) に基づく。推奨区分はあくまで Claude 判断であり、最終判定はユーザー (A)/(B)/(C) 回答に従う。
```

5. ユーザー回答を待つ。Claude 自発判断による upset_patterns / records 反映は **禁止** (柱A 承認制と整合)
6. ユーザー回答後にのみ、指示された範囲で upset_patterns.json / records/*.json に反映 (反映時は新規エントリに `record_class` フィールドを必須付与: 柱D サブセクション3 参照)
7. **(Session_62 2026-04-28 フェーズ6 議題2 追加) `step05_scanned_at` フィールド必須付与**: prediction_hit を `true`/`false` に確定する全エントリに対し、同時に `step05_scanned_at` フィールドを必須付与する。STEP 0.5 スキャン実施有無を records JSON フィールドベースで機械検証可能とするため。
   - **付与タイミング**: prediction_hit 書き込みと同一の records 更新操作内で同時に付与すること (= 別 commit / 別 turn での後付けは不可)
   - **値の形式**: ISO 8601 形式の UTC タイムスタンプ (例: `"step05_scanned_at": "2026-04-28T14:30:00Z"`)。スキャン実施時点ではなく、prediction_hit 確定時点の時刻を記録
   - **scope外UPSET 検出 0件のセッション**: 検出 0件であっても prediction_hit を確定した全エントリに `step05_scanned_at` を付与する (= 「STEP 0.5 を実施したが検出 0件だった」という事実の記録)
   - **記述例**:
     ```json
     {
       "match": "...",
       "tier": "go",
       "prediction_hit": false,
       "miss_class": "A",
       "record_class": "full_record",
       "step05_scanned_at": "2026-04-28T14:30:00Z",
       "miss_analysis": "..."
     }
     ```
   - **遡及付与なし**: フェーズ6 第4段階 承認日 (= 2026-04-28) 以降の **新規** prediction_hit 確定エントリのみ対象。既存 records (prediction_hit 確定済) への遡及付与は実施しない
   - **機械検証**: `monitoring/health_check.py` の **13項目目 `step05_scan_compliance`** で承認日以降の prediction_hit 確定エントリに対し `step05_scanned_at` 未付与を検出 (完全未付与=ALERT / 部分未付与=WARN)。詳細は本 SOP サブセクション6 参照

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
- **検証方法 (旧 / Session_62 フェーズ3 制定時)**: 結果反映 commit と同時に「STEP 0.5 実施済」ログを `monitoring/pending_actions.md` または記録 commit message に明示
- **検証方法 (新 / Session_62 2026-04-28 フェーズ6 議題2 追加)**: 上記 commit message ベースの検証に加え、**records JSON フィールドベースの機械検証** へ移行する:
  - 反映時には `record_class` (柱D サブセクション3 規定) と `step05_scanned_at` (本 SOP サブセクション2 ステップ7 規定) を **同時付与** する
  - `monitoring/health_check.py` の **13項目目 `step05_scan_compliance`** が走査対象 records JSON を再帰走査し、承認日 (2026-04-28) 以降に prediction_hit が確定した全エントリに対し `step05_scanned_at` 付与状況を検査
  - 完全未付与 (= 承認日以降の prediction_hit 確定エントリ全件で `step05_scanned_at` フィールドが存在しない) → **ALERT** 化
  - 部分未付与 (= 一部のエントリのみ未付与) → **WARN** 化
  - 区分3 (`record_class: "skip_record"`) のエントリは走査対象外 (柱D サブセクション7 既存柱との整合性 参照)
  - 機械検証への移行により、commit message 任意記述に依存せず構造化された強制ログとして STEP 0.5 実施保証が担保される
- **commit message ログとの併用**: 機械検証への移行後も、結果反映 commit message に「STEP 0.5 実施済」または「STEP 0.5 検出 0件」を併記する運用は **継続**。両者の併用で人間可読性 + 機械検証の二重担保を実現

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

#### 1-1. CLAUDE.md 改訂の階層化規定 (Session_62 2026-04-28 フェーズ6 議題6 追加)

CLAUDE.md 改訂のうち、以下を **B区分 (承認必須)** と **対象外 (追記のみ)** に階層化する:

- **B区分 (承認必須)**: 既存大会の **名称変更** (例: `ATP 250 → ATP Tour 250` / `Premiership → Gallagher Premiership` 等)
  - 理由: 名称変更は判定ロジック (rules_*.json 内の大会名照合等) に影響するため、本プロトコルの適用対象として承認必須化する
- **柱A 適用対象外 (追記のみ)**: **新リーグ追加** (新スポーツ・新リーグの scope 追加で 柱D 大会優先度テーブル / scope_rounds 階層に行を追加するのみ)
  - 理由: 既存ロジック非影響・追加のみのため運用負荷軽減
- **境界判断**: 名称変更 / 新リーグ追加の境界判断は **ケースバイケース対応** (リーグ統合・分割・大会フォーマット変更等の中間ケースは個別判断 — Claude 自発判断禁止・ユーザー判断必須)

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

#### 3-1. evidence 時間的独立性チェック (Session_62 2026-04-28 フェーズ6 議題1 追加)

新規ルール実装プロセスの step1 (`current_count >= trigger_threshold` 到達時の status 変更) に、以下の時間的独立性チェックを義務化する:

- **原則**: evidence 3件は **異なるセッション** で独立検出されたものであること (= 各 evidence の検出セッション ID が一致しないこと)
- **同一セッション内で複数件 evidence が追加された場合**: 最後の evidence 追加から **次セッション以降** に proposal 生成を必須化 (= 同一セッション内 step2 proposal 生成の禁止)
- **同一 turn 内で evidence 3件目に到達した場合**: status を `ready_for_proposal` に変更可 (status 変更自体は確認不要) だが、proposal 生成は次セッション開始時まで待機する (= 同一 turn 内 implement 完全禁止)
- **ユーザー質問契機 evidence の別カウント**: 検出契機 (Claude 自発検出 / ユーザー質問契機 / scope外UPSET スキャン契機 等) による区別はせず、独立性のみで判定する (Session_62 2026-04-28 フェーズ6 議題1 確定方針: 案D 不採用)

**Session_61 由来の逸脱パターン (R024 で発生した二重時間的依存)**:

R024 (form slump 補正) では evidence 3件目 (A041 Baptiste-Paolini) が Session_61 内の scope外UPSET スキャン中に検出され、同 turn 内で `current_count` 3/3 到達 → implement に至った。これは (a) 同一 turn 内 implement、(b) 同一 turn 内 evidence 検出、の二重時間的依存に該当する。本プロトコルはこれを再発防止対象として明示的に禁止する。

**実装箇所**: `core/rule_pipeline.json` の `instructions_for_claude` / `approval_workflow.step1_threshold_reached` / `forbidden_practices` に同義の規定を実装済 (Session_62 2026-04-28 フェーズ6 第4段階 ステップ1)。

#### 3-2. rule_linked: null + rule_linked_note 必須パターン (Session_64 2026-04-29 議題1+1' 制定)

> **背景**: A-3 サブタスク3 (Session_61 9件振り分け) で計4件 (Pliskova-Mertens / TOR-CLE G4 / HOU-LAL G4 / PHI G4) が、議題1 確定方針 (異セッション独立 evidence 3件未満で正式 evidence カウント対象外) と health_check.py 項目10 (MISS feedback loop = miss_analysis + miss_layer + rule_linked 完全要件) の競合により ALERT 回避目的の弱紐付け文字列を `rule_linked` に付与する暫定対応 (案Q) が運用された。本サブセクションは案 (a)+(b)+(c) 統合採用 (議題1+1' 提案レポート step1) に基づき、`rule_linked: null` + `rule_linked_note` 50文字以上の正規パターンを規定する。

新規 P*** 候補の 1件目 evidence として記録する場合 (議題1 確定方針による異セッション独立 evidence 3件未満)、以下の正規パターンに従う:

##### 必須記載項目 (rule_linked_note / 4項目)

| # | 項目 | 内容 |
|---|---|---|
| 1 | **保留理由** | 「正式 evidence カウント対象外」を明示 |
| 2 | **候補パターン記述** | 想定される P*** 候補のパターン名 (自然言語で簡潔に) |
| 3 | **evidence 1件目位置付け** | 「本 case は本パターンの 1件目 evidence 候補」と明示 |
| 4 | **議題1 確定方針遵守宣言** | 「議題1 確定方針 (異セッション独立 evidence 3件) 遵守」を `[MEMORY:CLAUDE.md 柱A 議題1 確定方針]` タグ付きで明示 (機械検証可能化) |

##### 正規パターン例

- `rule_linked: null` (新規ケース) または既存 P*** 候補への弱紐付け string/list (既存4件は現状維持温存 / 論点1 確定方針)
- `rule_linked_note`: 上記4項目を含む 50文字以上の記述
- `potential_new_p_candidate_note`: 候補パターン詳細 + 異セッション独立 evidence 蓄積待ち宣言
- `candidate_pattern`: 標準化された候補 ID (柱A サブセクション3-3 参照)

##### 機械検証

- `monitoring/health_check.py` 項目10 (MISS feedback loop) 改訂: `rule_linked: null` でも `rule_linked_note` が 50文字以上の実質的記述ありなら OK 扱い (議題1 正規パターン)
- CHECK-2 自己点検 (Claude 側責務): 必須4項目の充足を文言検証。中身検証は機械化困難のため Claude が応答送信前/記録ファイル書き込み前に目視確認すること
- 柱C 4-3 5種タグ義務との整合: 必須4項目の項目4 で `[MEMORY:CLAUDE.md 柱A 議題1 確定方針]` タグ付与必須

##### 既存4件 (案Q 暫定対応) との関係

| # | 試合 | rule_linked | rule_linked_note | candidate_pattern (柱A 3-3 参照) |
|---|---|---|---|---|
| 1 | Pliskova-Mertens Madrid R3 | `"P006_candidate_clay_R2R3_short_recovery"` (現状維持温存) | 必須4項目準拠記述 | `wta_clay_pr_veteran_return_form_celo_underestimate` |
| 2 | TOR vs CLE G4 | `["P028_candidate"]` (現状維持温存) | 必須4項目準拠記述 | `nba_po_road_fav_series_lead_home_dog_close_game_upset` |
| 3 | LAL vs HOU G4 | `["P028_candidate"]` (現状維持温存) | 必須4項目準拠記述 | `nba_po_back_to_wall_blowout_via_q3_dominance_3p_variance_hit` |
| 4 | PHI G4 vs PIT | `["P_NHL_PO_close_out_home_fav_failure_candidate"]` (現状維持温存) | 必須4項目準拠記述 | `nhl_po_close_out_home_fav_failure_via_veteran_desperation` |

→ 既存4件の `rule_linked` は論点1 確定方針により温存。**新規ケースから真の `rule_linked: null` 採用を許容**。

#### 3-3. candidate_pattern フィールド規約 (Session_64 2026-04-29 議題1+1' 制定)

新規 P*** 候補の機械検証可能化のため、records スキーマに `candidate_pattern` フィールドを導入する。

##### 命名規則

- **形式**: `{sport}_{context}_{pattern_summary}` (snake_case / 全小文字 / アルファベット数字_のみ)
- **最大長**: 80文字
- **略称表 (sport)**: `nhl` / `nba` / `nfl` / `mlb` / `nrl` / `sr` (Super Rugby) / `prm` (Premiership) / `t14` (Top 14) / `pd2` (Pro D2) / `sl` (Super League) / `ufl` / `cfl` / `ahl` / `atp` / `wta` / `scc` (= soccer)

##### 付与義務

- **MISS エントリ + `rule_linked: null` パターン**: 必須
- **MISS エントリ + 弱紐付け (既存4件パターン)**: 必須 (3-2 必須4項目と整合)
- **HIT エントリ**: 任意・選択的 (HIT 側候補追跡で付与可・論点6 確定方針)

##### registry 参照義務

- 新規 `candidate_pattern` 値は `core/candidate_pattern_registry.json` に登録必須
- 既存値の重複付与は禁止 (議題1 同一 turn 内 evidence 加算回避)
- registry 未登録値の使用は health_check 項目14 で WARN 検出

##### 機械検証

- `monitoring/health_check.py` 項目14 (`candidate_pattern_uniqueness`) で以下を検証:
  - 同一セッション内同一値重複 → **WARN** (議題1 同一セッション内 evidence 加算回避の精神違反)
  - 同一 turn 内同一値検出 (= `step05_scanned_at` 完全一致) → **ALERT** (議題1 同一 turn 内 evidence 加算厳禁違反)
  - registry 未登録値 → **WARN**
  - 区分3 (skip_record) は走査対象外 (柱D 既存柱との整合性)

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
- 同一セッション内で同じ `candidate_pattern` 値の重複付与 (議題1 同一 turn 内 evidence 加算回避の精神 / Session_64 2026-04-29 議題1+1' 制定 / health_check.py 項目14 で機械検証)

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
- **判定対象**:
  - **対象**: 推定勝率 ≥ 80% の予想で **prediction_hit=true** (= HIT) のエントリのみ
  - **対象外 (フィールド null)**: 推定勝率 < 80% の予想 / 敗戦 (prediction_hit=false) / 試合不成立 (match_status ∈ {retired, walkover, cancelled, postponed}) / 区分3 (skip_record)
- **種目別の薄勝ち閾値テーブル (Session_62 2026-04-28 フェーズ6 議題3 確定)**:

| 種目 | 薄勝ち閾値 (`confidence_drift="high"` 付与基準) |
|---|---|
| **ATP / WTA テニス** | **3セット縺れ** (2-1 で勝利。tiebreak 含む 3-set go to distance を含む) |
| **NHL** | **OT 突入 OR regulation 1点差** (空ネット (ENG) 加点後の最終スコアではなく試合中の差分で判定) |
| **NBA** | **1桁差** (1〜9点差で勝利) |
| **MLB** | **1点差** (延長戦・walk-off 含む) |
| **サッカー (5大リーグ)** | **1点差** (90分終了時の差分基準。後半AT 勝ち越しを含む) |
| **NFL** | **TD 1個差以内** (1〜8点差で勝利) |
| **ラグビー (Premiership / Top14 / Pro D2 / NRL / Super League / Super Rugby)** | **TD 1個差以内** (リーグ系 NRL/Super League = 6点差以内 / ユニオン系 Premiership/Top14/Pro D2/Super Rugby = 7点差以内) |

- **機械判定の運用ルール**:
  - 種目別閾値判定は records JSON の `score` / `score_detail` フィールドに基づく機械判定とする
  - `confidence_drift="high"` HIT は柱C 4-1 の Class 別 fetch 件数規定で **Class B 相当 (中重要度)** の深掘り対象として扱う (4-2 サブセクション「Class 別 WebFetch 必須件数」参照)
  - confidence_drift HIT は v3.0 2トラック精度管理の Track 2 (モデル品質追跡) で別軸集計対象 (議題7 連動・cumulative.json 改修は別タスク)
- **付与必須化 (Session_62 2026-04-28 フェーズ6 第3段階確定をもって必須化)**:
  - フェーズ4 ステージ1 制定時の「枠組みのみ実装・付与は任意」状態を **解除**
  - 推定勝率 ≥ 80% で予想 + 上記閾値内で勝利 → `confidence_drift: "high"` 付与必須
  - フェーズ4 ステージ1 承認日 (2026-04-27) 以降の **新規** prediction_hit=true エントリ + 推定勝率 ≥ 80% のエントリのみ対象 (既存記録への遡及付与は実施しない)
  - 機械検証は `monitoring/health_check.py` への組込は本フェーズ範囲外 (今後別タスクで検討)
- **記述例**:
  ```json
  {
    "match": "...",
    "tier": "go",
    "prediction_winner": "X",
    "prediction_confidence": 0.85,
    "result": "X won 2-1 (final set tiebreak)",
    "prediction_hit": true,
    "confidence_drift": "high",
    "record_class": "full_record"
  }
  ```

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

### 4-3. 情報源タグ義務化

`miss_analysis` フィールド・`rule_pipeline.json` の `evidence` エントリ・session_logs の MISS 分析記述・`upset_patterns.json` の miss_analysis_text 等、**事実主張を含む全テキスト** に対し、5種タグのいずれかを主張ごとに付与する義務を課す。

#### 5種タグ仕様

| タグ | 用途 | 記述例 | カウント扱い |
|---|---|---|---|
| `[FETCH:URL]` | 当該 URL を **WebFetch で本文取得した事実根拠** | `Khachanov 6-2 6-3 で勝利 [FETCH:https://www.atptour.com/en/scores/...]` | Class 別 fetch 件数の有効 1件 |
| `[FETCHER:src]` | `scripts/fetch_*.py` 経由で取得済の構造化スタッツ (鮮度 OK + `feed_status()` OK 判定) | `Madrid Elo Khachanov 1812 vs Walton 1623 [FETCHER:tennis_elo]` | WebFetch 1件相当 |
| `[FETCHER:src:proxy]` | proxy / 計算由来の値 (`wRC_plus_is_proxy=true` / `FIP_is_computed=true` 等のフラグ付き) | `HOU 打線 wRC+ 118 (StatsAPI proxy) [FETCHER:fangraphs:proxy]` | WebFetch 1件相当だが信頼性が proxy であることを明示 |
| `[SEARCH]` | WebSearch スニペットレベルの根拠 (本文取得していない) | `Shapovalov は serve に苦戦したと報じられた [SEARCH]` | **fetch カウント対象外** (補助情報のみ) |
| `[MEMORY]` | 記憶ベースの推論 (検証不能・記述許容だが evidence 化禁止) | `Madrid は 1500m の altitude にあると一般に知られる [MEMORY]` | カウント対象外。evidence 配列への加算禁止 |
| `[INFER]` | fetch / search の組合せからの導出推論 | `→ サーブ依存型の rhythm が崩れた可能性 [INFER]` | カウント対象外 |

#### タグ付与単位 (主張ごと)

タグは **主張ごと** に付与する。段落一括での末尾1タグは禁止。

- **1主張 = 1事実言明 or 1推論結論**
- 複数主張を含む段落は、各主張の末尾にタグを付与
- 句読点単位ではなく「論理的に独立した主張」単位で区切る

#### タグ付与の粒度ガイドライン (Session_62 2026-04-28 フェーズ6 議題4 追加)

「主張ごと」の判定基準が記述者によってブレないよう、解釈B (同一 source 段落末1タグ可) を原則として採用し、5項目の但し書きで境界を明示する。本ガイドラインにより、同じ事実根拠を複数の Claude セッションで再生成しても、タグ付与単位の一貫性が確保される。

##### 原則 (解釈B): 同一 source からの複数データ列挙は段落末1タグ可

同一の一次ソース (= 同じ試合レポート / 同じ fetcher / 同じ search 結果) から抽出した複数データを列挙する場合、各データ点ごとにタグを付与せず **段落末1タグで足りる**。

**良い例**:
```
Khachanov 6-2 6-3 で勝利、1st serve in% 72% [FETCH:https://www.atptour.com/...]。
```
→ 同一試合レポート (atptour.com) からの抽出のため段落末1タグ可。

##### 但し書き① source が異なる主張は別タグ必須

source (= 一次ソース URL or fetcher名) が異なる主張は、原則 (解釈B) を適用せず **各主張ごとにタグ必須**。

**良い例**:
```
Khachanov 6-2 6-3 で勝利 [FETCH:https://www.atptour.com/...]。Walton クレー 8試合のみ [FETCHER:tennis_elo]。
```
→ atptour.com (試合結果) と tennis_elo fetcher (選手スタッツ) で source が異なるため、両主張にタグ必須。

##### 但し書き② INFER と FETCH/FETCHER/SEARCH の混在文は両方タグ必須

事実主張 (`[FETCH]` / `[FETCHER]` / `[SEARCH]`) と推論主張 (`[INFER]`) が混在する文・段落は、**両方にタグ必須**。

**良い例**:
```
xG はホーム 2.1 / アウェー 0.7 [FETCHER:understat]。→ ホーム側のシュート機会優位だが決定力差で接戦化した可能性 [INFER]。
```
→ 事実 (xG 数値) と推論 (接戦化の理由) の両方にタグ付与。INFER の根拠は同段落内の先行 FETCHER タグに依存。

##### 但し書き③ 否定主張も事実に基づく場合はタグ必須

「X ではない」「X は起きていない」のような **否定形の主張** であっても、それが事実に基づく場合はタグ必須。否定主張だからという理由でタグ省略は不可。

**良い例**:
```
Sinner は怪我なしで出場可能 [FETCH:https://www.atptour.com/en/players/...]。
```
→ 否定形 (怪我「なし」) であっても事実主張のためタグ必須。

##### 但し書き④ INFER の推論連鎖は末尾1タグでOK

`[INFER]` 主張の中で複数の中間推論を連鎖させる場合 (= 「A→B→C」のような推論ステップ)、各中間推論にタグを付与せず **末尾1タグで足りる**。中間推論はあくまで結論主張への論理ステップであり、独立主張とは扱わない。

**良い例**:
```
→ サーブ依存型 player の rhythm が標高で崩れた可能性 [INFER]。
```
→ 中間推論 (「サーブ依存型 → rhythm 崩壊 → 標高影響」) を連鎖させた結論にのみタグ付与。

##### 短い接続句のカウント対象外規定 (既存 health_check 規定との整合)

「なお、」「ただし、」「したがって、」のような **10文字未満の短い接続句** は、独立主張ではなく接続表現として扱い、タグ付与不要。`monitoring/health_check.py` の 12項目目 `miss_analysis_tag_compliance` が文単位タグ検出時に「短い接続句 10文字未満はカウント対象外」とする既存規定 (L538-539) と整合させる運用。

##### 解釈緩和の影響 (health_check 判定との整合)

本粒度ガイドライン導入後も、`monitoring/health_check.py` の 12項目目 `miss_analysis_tag_compliance` の判定ロジック (= 文単位タグ検出 + 10文字未満接続句 cancel) は **変更しない**。粒度ガイドラインは Claude 側の自己点検 (CHECK-2) における「論理的に独立した主張」の解釈基準を明示化するもので、機械検出ロジックそのものは現行通り維持。

##### 既存柱C 4-3 との位置付け

本サブセクションは「タグ付与単位 (主張ごと)」の細則として、原則 (解釈B) + 但し書き4項目 (①〜④) で構成される。既存「タグなし主張は禁止」「良い例 / 悪い例」「[FETCH_FAILED] / [FETCHER:src:proxy] / [INFER] ネスト記法不採用」の各サブセクションとは独立に動作し、競合しない。

#### タグなし主張は禁止

事実主張・推論を含む文末にタグなしの記述があれば **禁止**。検出方法は2系統併用:

- **CHECK-2 自己点検** (Claude 側): 応答送信前 / 記録ファイル書き込み前にタグなし主張がないか目視確認 (`monitoring/check_protocol.md` CHECK-2 と連携)
- **health_check.py 機械検出** (システム側): 新検査項目 `miss_analysis_tag_compliance` が `records/{sport}/*.json` の miss_analysis フィールドを走査し、タグ無し主張を WARN/ALERT 化

#### 良い例 / 悪い例

**悪い例 (Session_61 A038 Shapovalov の miss_analysis 実例)**:

```
Madrid altitude (1500m) で sub-altitude ball change が rhythm を破壊し、
Budkov Kjaer の serve 圧力に対応できなかった。
```

→ 問題点:
- altitude 1500m は記憶ベース ([MEMORY] 必要だが付与なし)
- sub-altitude ball change の影響は WebFetch で検証されていない ([INFER] 必要だが先行 [FETCH] なし)
- serve 圧力の主張も一次ソース未確認 ([SEARCH] 止まり)
- 全体としてタグなしで「確定事実のように」記述 → 一次ソース統制が機能せず R024 implement の根拠として採用された構造的問題

**良い例 (改善後の同パターン)**:

```
Budkov Kjaer は 53分のストレート勝利 [FETCH:https://www.atptour.com/en/scores/2026/madrid/match/r2-budkov-kjaer-shapovalov]。
試合中の Shapovalov の 1st serve in% は 52% (通常 65%) [FETCHER:tennis_serve]。
Madrid は標高 1500m と一般に知られる [MEMORY]。
→ サーブ依存型 player の rhythm が標高で崩れた可能性 [INFER]。
```

→ 各主張ごとにタグが付与され、根拠の信頼性レベル (FETCH > FETCHER > SEARCH > MEMORY > INFER) が読み手に明示される。

#### `[FETCH_FAILED:URL1,URL2,URL3]` タグ詳細仕様

4-2 規定の fetch 失敗時 3回試行で規定件数未達となった場合に付与する。

- **形式**: `[FETCH_FAILED:URL1,URL2,URL3]` (試行した URL をカンマ区切りで列挙)
- **試行回数**: 計3回 (試行1: 同種別代替 / 試行2: 別種別 / 試行3: 別種別)
- **配置**: 当該 miss_analysis テキストの末尾、または該当主張の直後
- **必須セット**: `investigation_status: "investigation_incomplete"` を records エントリに同時付与
- **記述例**:
  ```
  Newcastle の lineup 変更を確認しようとしたが取得失敗
  [FETCH_FAILED:https://example.com/team1,https://example.com/team2,https://espn.com/match]。
  investigation_status: investigation_incomplete として次セッション再試行を pending_actions.md に登録。
  ```

#### `[FETCHER:src:proxy]` タグ仕様 (4-2 補足の実体化)

- `[FETCHER:src]` = 通常の構造化スタッツデータ (一次計算値)
- `[FETCHER:src:proxy]` = proxy / 計算由来の値 (フラグ付きデータ)
- 件数カウントは同等 (WebFetch 1件相当)
- 適用例:
  - `fangraphs` で `wRC_plus_is_proxy=true` のデータ → `[FETCHER:fangraphs:proxy]`
  - `fangraphs` で `FIP_is_computed=true` のデータ → `[FETCHER:fangraphs:proxy]`
  - 通常の Statcast 直接取得値 → `[FETCHER:baseball_savant]` (proxy なし)
- 分析時は proxy データを **副**、一次取得値を **主** の位置付けで使用すること

#### `[INFER]` のネスト記法不採用

`[INFER:[FETCH:url]]` のような入れ子記述は **不採用**。代わりに、同段落内に先行する `[FETCH:url]` または `[FETCHER:src]` または `[SEARCH]` タグを置き、それを根拠として直後に `[INFER]` 主張を続ける運用とする。

例 (再掲):
```
xG は ホーム 2.1 / アウェー 0.7 [FETCHER:understat]。
→ ホーム側のシュート機会優位だが決定力差で接戦化した可能性 [INFER]。
```

→ `[INFER]` の根拠は同段落内の先行タグに依存。段落をまたぐ場合は再掲する。

#### 遡及適用範囲 (新規のみ)

- **対象**: フェーズ4 ステージ3 承認後の **新規** miss_analysis / evidence エントリ / session_logs MISS 分析記述
- **遡及付与なし**: 既存 records/*.json (100件超) / 既存 `rule_pipeline.json` evidence (P001-P033) / 既存 `upset_patterns.json` (A001-A043) への遡及付与は実施しない
- 既存記述に対する CHECK-2 / health_check 検出は **新規付与時点以降のエントリのみ** 対象とする

#### CHECK-2 連携

`monitoring/check_protocol.md` の CHECK-2 (情報精度チェック) に以下のチェック項目を追加して運用する (本フェーズで check_protocol.md 自体は改訂対象外。CHECK-2 適用時に本セクションを参照する運用):

- 新規 miss_analysis / evidence 記述時、各主張に5種タグのいずれかが付与されているか?
- `[FETCH:URL]` / `[FETCHER:src]` の URL/src は実際に取得した一次ソースか?
- `[INFER]` 主張の同段落内に先行 `[FETCH]` / `[FETCHER]` / `[SEARCH]` タグがあるか?
- 4-2 規定の Class 別 fetch 件数 (A=3 / B=2 / C=1) を満たしているか?
- 規定未達なら `[FETCH_FAILED:URL1,URL2,URL3]` + `investigation_status: investigation_incomplete` が付与されているか?

#### health_check.py 連携 (新項目 `miss_analysis_tag_compliance`)

`monitoring/health_check.py` に12番目の検査項目として `miss_analysis_tag_compliance` を実装する:

- `records/{sport}/*.json` を再帰走査し、`miss_analysis` フィールドを持つエントリを抽出
- フェーズ4 ステージ3 承認日 (= 2026-04-27) 以降に追加されたエントリのみ対象 (記録ファイルの `last_updated` または `prediction_hit` の確定日基準)
- 各 miss_analysis テキストを正規表現でスキャンし、5種タグ (`\[FETCH:` / `\[FETCHER:` / `\[SEARCH\]` / `\[MEMORY\]` / `\[INFER\]` / `\[FETCH_FAILED:`) の有無を検出
- タグなし主張 (= タグなしで終わる文) を発見 → WARN 化
- 完全タグなし miss_analysis (タグ 0個) を発見 → ALERT 化

#### セッション固有スクリプト (`_sessionXX_*.py`) 生成時のタグ義務

セッション内の使い捨てスクリプトで records / upset_patterns / rule_pipeline に書き込みを行う場合、書き込まれる miss_analysis / evidence テキストにも本タグ仕様を適用する。スクリプト生成時に以下を遵守:

- スクリプト内で生成する miss_analysis 文字列には主張ごとのタグを含めること
- スクリプト末尾に `# tag_compliance_check: applied` コメントを残し、health_check 側で目印とする (将来の自動検証用)
- 既存 `_session61_writeback.py` / `_session61_rule_feedback.py` / `_session61_phase2_upsets.py` の3本は使い捨て完了済のため改修対象外

---

## 【柱D: 記録対象判断テーブル】Session_62 2026-04-27 制定

> **背景**: Session_61 で scope外UPSET 9件検出時、Bristol-Newcastle (records 未登録) / Northampton-Bath (date 訂正のみ) / Swiatek retire / Bondar-Svitolina / TOR-CLE G4 等の境界事例を Claude 自発判断で「records には未反映・upset_patterns のみ」処理した。判断基準が CLAUDE.md に明文化されておらず、ユーザー側で整合性検証ができない構造だった。本プロトコルは「記録対象 / 参考記録 / 無視可」の3区分判定基準を明文化し、scope 境界の判断を統制する。

### 1. 3区分定義 (record_class)

records エントリ・scope外UPSET 検出試合・新規分析試合のすべてに `record_class` フィールドを必須付与する (新規エントリのみ。既存 records 100件超への遡及付与なし)。

| 区分 | 名称 (record_class 値) | 記録先 | 用途 |
|---|---|---|---|
| **1** | `full_record` | `records/{sport}/*.json` への正式登録 + 該当時 `upset_patterns.json` / `multi_bets.json` | ベット推奨 / 予測精度追跡 / cumulative.json Track 1 + Track 2 両軸集計対象 |
| **2** | `reference_only` | `upset_patterns.json` のみ (records 本体には登録しない) | rule_pipeline.json evidence 蓄積用 / **cumulative.json Track 1 集計対象外、Track 2 では `by_record_class` 別軸集計対象** (Session_62 2026-04-28 フェーズ6 議題7 確定) |
| **3** | `skip_record` | 記録なし | scope 外として明示的に除外 |

#### v3.0 2トラック精度管理整合表 (Session_62 2026-04-28 フェーズ6 議題7 反映)

| Track | 集計対象 | 区分1 (full_record) | 区分2 (reference_only) | 区分3 (skip_record) |
|---|---|---|---|---|
| **Track 1 (ベット推奨収益性)** | tier ∈ {go, upset_pick} の確定エントリのみ | ○ (寄与) | × (集計対象外) | × (記録対象外) |
| **Track 2 (全試合モデル品質)** | 全試合の予測精度追跡 | ○ (`by_record_class` 別軸の `record_class_1_only` + `record_class_1_and_2` 両方に寄与) | **○ (`by_record_class` 別軸の `record_class_1_and_2` のみに寄与)** (議題7) | × (記録対象外) |

- Track 1 = **区分1 のみ寄与** (現行維持・収益性追跡の純度確保)
- Track 2 = **`by_record_class` 別軸集計** (区分1 のみの数値 + 区分1+2 合算の数値を並列追跡)
- cumulative.json への `by_record_class` セクション新設 (`record_class_1_only` / `record_class_1_and_2`) と dashboard.html の表示拡張 (Track 2 の二軸表示) は **4本柱完了後の別タスクで実施** (本フェーズでは柱D サブセクション1 + 本整合表の文言改訂のみ即時反映)
- フェーズ6 第4段階では cumulative.json / dashboard.html への書き込みは禁止 (議題7 別タスク統合扱い)

#### 判定条件 (機械判定可能な形)

| 区分 | 判定条件 |
|---|---|
| **区分1: full_record** | 以下の **すべて** を満たす:<br>(a) 対象スポーツが CLAUDE.md L1 早見表 9種目に含まれる<br>(b) 対象大会が「scope内大会」(下記 4. 大会優先度テーブル参照)<br>(c) 対象 round が「scope内 round」(下記 5. リーグ内 round/week 階層 参照)<br>(d) `match_status == "completed"` (棄権/W-O/中止以外)<br>(e) ユーザー提供データ起点 OR scope外UPSET スキャン (結果反映 STEP 0.5) でユーザー (A) 承認 |
| **区分2: reference_only** | 以下の **いずれか** を満たす:<br>(a) scope外UPSET スキャン (結果反映 STEP 0.5) でユーザー (B) 承認<br>(b) records 既登録試合の関連試合 (例: NBA G4 のみ scope内、G3 は参考)<br>(c) `match_status ∈ {"retired", "walkover"}` だが UPSET 性質を持つ (例: 高 conf fav の retire) |
| **区分3: skip_record** | 以下の **いずれか** を満たす:<br>(a) スポーツが CLAUDE.md L1 早見表 9種目に **含まれない**<br>(b) 対象大会が「scope外大会」(下記 4. 大会優先度テーブル参照)<br>(c) ユーザー (C) 判断で除外<br>(d) `match_status ∈ {"cancelled", "postponed"}` で UPSET 性質も持たない |

### 2. match_status enum 仕様

records エントリの試合状態を 5値の enum で明示する。既存 `void: true` フィールドは後方互換用として維持 (match_status != "completed" なら void=true と整合)。

| match_status | 意味 | 区分 (record_class) | prediction_hit 更新 | miss_class 付与 |
|---|---|---|---|---|
| `completed` | 正規に試合完了 | 区分1 | 必須 | 必須 (false 時) |
| `retired` | 一方が試合中棄権 | 区分1 or 2 (UPSET 性質で判断) | retire 側を「敗北」扱い | 区分1 時のみ |
| `walkover` | 試合前不出場 (W-O) | 区分2 | 不要 | 不要 |
| `cancelled` | 試合中止 (再開予定なし) | 区分3 | 不要 | 不要 |
| `postponed` | 順延 (後日再開) | 区分3 (再開時に新規エントリ) | 不要 | 不要 |

### 3. record_class フィールド付与ルール

- **対象**: フェーズ5 承認後 (= 2026-04-27 以降) の **新規** records / upset_patterns エントリのみ
- **遡及付与なし**: 既存 records/*.json (100件超) / 既存 upset_patterns.json (A001-A043) への遡及付与は実施しない
- **付与タイミング**: 新規エントリ作成時に同時付与 (`record_class` + `match_status` を同時に設定)
- **値**: `record_class` は `"full_record"` / `"reference_only"` / `"skip_record"` の3値必須 / `match_status` は5値必須
- **記述例**:
  ```json
  {
    "match": "...",
    "record_class": "full_record",
    "match_status": "completed",
    "tier": "go",
    "prediction_hit": false,
    "miss_class": "A",
    "miss_analysis": "..."
  }
  ```

### 4. 大会優先度テーブル (scope内 / scope外)

| 種目 | scope内 (区分1 候補) | scope外 (区分3) |
|---|---|---|
| **ATP テニス** | Grand Slam 全 round / Masters 1000 R1〜F / ATP 500 R2〜F / ATP 250 R2〜F | Challenger / Exhibition / Olympic / ATP 500 R1 (区分2) / ATP 250 R1 (区分3) |
| **WTA テニス** | Grand Slam 全 round / WTA 1000 R1〜F / WTA 500 R2〜F / WTA 250 R2〜F | WTA 125K / Exhibition / WTA 500 R1 (区分2) / WTA 250 R1 (区分3) |
| **NHL** | Regular Season 全試合 / Playoffs 全試合 | Preseason / All-Star |
| **NBA** | Regular Season 全試合 / Playoffs 全試合 / Play-In | Preseason / Summer League / All-Star |
| **MLB** | Regular Season 全試合 / Postseason 全試合 | Spring Training / All-Star |
| **NFL** | Regular Season 全試合 / Playoffs 全試合 | Preseason / Pro Bowl |
| **CFL / UFL** | Regular Season 全試合 / Playoffs 全試合 | Preseason |
| **NRL** | Regular Round 1-27 全試合 / Finals 全試合 | Preseason / All-Stars |
| **Super Rugby Pacific** | Regular Round 1-15 / Finals | Preseason |
| **Premiership / Top14 / Pro D2** | League 全試合 / Playoffs / Final | Champions Cup (区分2) / Challenge Cup (区分2) |
| **Super League** | Regular Round / Super 8s / Finals | Challenge Cup (区分2) |
| **AHL** | Regular Season / Calder Cup Playoffs | Preseason |
| **サッカー (5大リーグ)** | League 全試合 | UCL Knockout R16以降 (区分1) / UCL Group Stage (区分2) / UEL 全般 (区分2) / FA Cup R5以降 (区分2) / FA Cup R4以前 (区分3) / 各国カップ全般 (DFB-Pokal / Coupe de France 等) (区分3) |

#### Cup 戦細分化 (詳細)

| Cup 戦 | 区分 | 理由 |
|---|---|---|
| UCL Knockout (R16 以降) | 区分1 | トップクラス対戦・スタッツ十分 |
| UCL Group Stage | 区分2 | ローテーション影響大・サンプル不足 |
| UEL 全般 | 区分2 | リーグ参戦動機差・スタッツ精度低 |
| FA Cup R5 以降 | 区分2 | 上位チーム真剣度向上 |
| FA Cup R4 以前 | 区分3 | giant-killing 多発・予測対象外 |
| DFB-Pokal / Coupe de France / Coppa Italia 等 | 区分3 | データ不十分・ベット対象外 |
| Davis Cup / United Cup / Laver Cup (チーム戦テニス) | **区分3** | ELO 機能せず・形式特殊・ベット対象外 |

### 5. リーグ内 round/week 階層 (CLAUDE.md インライン記述)

各種目の scope_rounds は本セクションでインライン記述する (rules_*.json 改訂は柱A 承認必須のため本フェーズ範囲外)。

| 種目 | scope内 round | scope外 round |
|---|---|---|
| ATP / WTA | Masters R1〜F / GS R1〜F / 500 R2〜F / 250 R2〜F | 500 R1 (区分2) / 250 R1 (区分3) / Q (区分3) |
| NHL / NBA / NFL / MLB / CFL / UFL / AHL | Regular Season + Playoffs (全試合) | Preseason / All-Star / Exhibition |
| NRL / Super Rugby / Super League | Regular Round 1-26/27 + Finals | Preseason / All-Stars / Challenge Cup |
| Premiership / Top14 / Pro D2 | League + Playoffs + Final | Champions Cup / Challenge Cup (= 区分2 分類) |
| サッカー 5大リーグ | League 全試合 (38節) | Cup 戦は上記 4. Cup 戦細分化テーブル参照 |

### 6. 新リーグ追加 SOP (Session_62 2026-04-28 フェーズ6 議題6 改訂)

新規スポーツ・リーグを scope に追加する際のワークフロー。CLAUDE.md 改訂の階層化規定 (柱A サブセクション1-1 で実装済) に基づき、**新リーグ追加 = 柱A 適用対象外 (追記のみ)** / **既存大会の名称変更 = B区分 (承認必須)** に階層化:

#### 6-1. 新リーグ追加ワークフロー (柱A 適用対象外、追記のみ)

新規スポーツ・リーグの scope 追加で 柱D 大会優先度テーブル (本セクション 4) / scope_rounds 階層 (本セクション 5) に行を追加するのみのケース。判定ロジック (rules_*.json 内の大会名照合等) に既存影響を与えないため、柱A 承認制プロトコル適用対象外:

1. 新リーグデータ受領 (ユーザー提供 JSON 起点)
2. CLAUDE.md 柱D「大会優先度テーブル」(本セクション 4) に該当リーグ行を追加 (柱A 適用対象外、追記のみ)
3. scope内 round 範囲の暫定案を提示 → ユーザー承認
4. `core/rules_{newsport}.json` 新規作成 → **柱A 承認必須プロセス** (ルール改訂統制プロトコル適用)
5. 初回 STEP 0.5 (結果反映) で境界事例検出時、本プロトコル 3区分テーブルで判定

#### 6-2. 既存大会の名称変更 (B区分・承認必須)

既存大会の名称を変更するケース (例: `ATP 250 → ATP Tour 250` / `Premiership → Gallagher Premiership` / `Bundesliga → Bundesliga 1` 等):

- 柱A サブセクション1-1 (CLAUDE.md 改訂の階層化規定) に基づき、**B区分 (承認必須)** として扱う
- 理由: 名称変更は判定ロジック (rules_*.json 内の大会名照合 / 大会優先度テーブル参照 / scope_rounds 階層) に **影響する** ため、柱A 承認制プロトコル適用必須
- 名称変更時のワークフロー:
  1. 既存リーグの名称変更を検知 → ユーザーに B区分 改訂提案を提示 (旧名称 / 新名称 / 影響範囲 / 改訂根拠)
  2. ユーザー承認後にのみ CLAUDE.md 柱D 大会優先度テーブル / scope_rounds 階層 / `core/rules_*.json` 内大会名を改訂
  3. 改訂後、影響を受ける既存 records エントリの大会名照合を再検証

#### 6-3. 境界判断 (ケースバイケース対応)

新リーグ追加 / 名称変更の中間ケース (リーグ統合・分割・大会フォーマット変更等) は **ケースバイケース対応** (Claude 自発判断禁止・ユーザー判断必須):

- リーグ統合例: 2つの既存リーグが合併して新名称で運営継続 → 既存判定ロジックへの影響度を Claude が分析し、ユーザーに B区分 / 対象外 のいずれを採用するか判断依頼
- リーグ分割例: 既存リーグが上位 / 下位に分割 → 上位リーグのみ scope 維持 / 下位リーグを新規追加扱いとする等の境界判断
- 大会フォーマット変更例: round 数変更 / 出場枠変更 / 大会期間変更 → 既存 scope_rounds 階層への影響度評価が必要

→ 中間ケースは柱D サブセクション8「境界曖昧リーグ個別判断 SOP」のワークフローと同様、Claude が「該当」を検出してユーザー判断を仰ぐ運用とする。

### 7. 既存柱との整合性

#### 柱A (rule 改訂承認制) との整合

- 区分1 (full_record) の試合 MISS が rule_pipeline.json evidence に積算される → 柱A 承認制プロセス起動
- 区分2 (reference_only) の試合 MISS も同等に evidence 積算可能 (柱B 結果反映 STEP 0.5 SOP と整合)
- 区分3 (skip_record) は records にも upset_patterns にも登録しないため、自然に evidence 積算対象外

#### 柱B (結果反映 STEP 0.5 scope外UPSET スキャン SOP) との整合

scope外UPSET スキャン時のユーザー提示テーブルに「Claude 推奨区分」列を追加 (本フェーズで実装):

- ユーザー回答 (A) records 登録 = 区分1 (full_record)
- ユーザー回答 (B) upset_patterns のみ = 区分2 (reference_only)
- ユーザー回答 (C) 無視 = 区分3 (skip_record)

#### 柱C (一次ソース fetch 義務化) との整合

| 区分 | miss_class 付与 | fetch 件数規定 | タグ義務 |
|---|---|---|---|
| **区分1: full_record** | 必須 (新規 prediction_hit=false 時) | Class 別件数規定適用 (A=3 / B=2 / C=1) | 全タグ義務適用 |
| **区分2: reference_only** | 任意 (UPSET 性質追跡用に "C" 付与可) | C 相当 (1 件以上) | タグ義務適用 (簡略可) |
| **区分3: skip_record** | 付与禁止 | fetch 不要 | **タグ義務対象外** |

#### health_check.py `miss_analysis_tag_compliance` との整合

- 12項目目 `miss_analysis_tag_compliance` の検査ロジックは `record_class == "skip_record"` フィルタを適用 (本フェーズ ステップ3 で実装)
- 区分3 試合は走査対象外として skip
- 区分2 (reference_only) は records/*.json には登録されないため、走査対象は実質 区分1 のみ

### 8. 境界曖昧リーグの個別判断 SOP

#### 境界曖昧リーグ表 (本フェーズ確定 6リーグ + ユーザー追加運用)

| リーグ | 境界曖昧の理由 | 既定推奨区分 |
|---|---|---|
| ATP 500 R1 | seeded player は R1 bye / 上位選手の R2 初戦のみ scope 内が自然 | 区分2 (reference_only) |
| ATP 250 R1 | 上位選手の出場頻度が低く市場 efficiency が低い | 区分3 (skip_record) |
| WTA 125K | scope内大会の閾値ライン上 | 区分3 (skip_record) |
| Pro D2 (フランス2部) | データ取得難・scope内だが粒度低い | 区分1 (full_record) だが confidence_drift 多発予想 |
| Premiership 下位カード | 上位 vs 下位の場合のみ scope 内 | 個別判断 |
| Super League playoffs/PO | seeded chain の date 訂正リスク (CE019 再発リスク) | 個別判断 + 必須 draw sheet 確認 |

ユーザー側で追加リーグを境界曖昧と判定した場合、本表に追記する運用とする。

#### 境界曖昧時のユーザー個別判断ワークフロー

1. Claude が記録対象判断時に「上記境界曖昧リーグ表に該当」を検出
2. 当該試合をユーザーに提示し、3区分のどれを採用するか確認:
   ```
   【記録対象判断 確認】
   試合: XXX vs YYY (リーグ: ATP 500 R1)
   境界曖昧理由: ATP 500 R1 は seeded player bye / 上位選手の R2 初戦のみ scope 内が自然
   Claude 推奨: 区分2 (reference_only)
   ユーザー判断依頼: 区分1 / 区分2 / 区分3 のいずれを採用しますか?
   ```
3. ユーザー回答に基づき記録 (Claude 自発判断は禁止)
4. 同一リーグの今後の試合は前回判断を踏襲 (ユーザー再判断不要)。シーズン跨ぎ等の再判断タイミングは下記「踏襲有効期限」サブセクションで規定 (Session_62 2026-04-28 フェーズ6 議題8 確定)

#### 踏襲有効期限 (Session_62 2026-04-28 フェーズ6 議題8 追加)

境界曖昧リーグの判断踏襲には有効期限を設ける。**案B 原則 (同一フォーマット継続中は踏襲) + シーズン跨ぎ見直し提案 + フォーマット変更時強制再判断** の3層構造で運用する:

##### 案B 原則: 同一フォーマット継続中は前回判断踏襲

- **適用範囲**: 同一シーズン内 + 同一大会フォーマット内
- **運用**: 前回ユーザー判断 (区分1 / 区分2 / 区分3) を踏襲。Claude による再判断 / ユーザー再判断不要
- **判断記録**: 個別判断結果は Claude 内部の判断ログ (= 過去 records / upset_patterns エントリの `record_class` フィールド + 該当境界曖昧リーグ表) を参照

##### シーズン跨ぎ時: Claude Code が見直し提案 (1回)

シーズン跨ぎ (= 当該リーグの新シーズン開幕日経過) 時に Claude Code が **見直し提案を1回** 行う:

- **提案フォーマット**:
  ```
  【記録対象判断 シーズン跨ぎ見直し】
  リーグ: ATP 500 R1 (例)
  前回判断: 区分2 (reference_only) — Session_X (旧シーズン)
  新シーズン: 2026-2027 シーズン (XXXX 開幕)
  ユーザー判断依頼: (1) 踏襲継続 / (2) 区分変更 / (3) 大会フォーマット変更を別議題化
  ```
- **頻度**: 各境界曖昧リーグごとに新シーズン開幕後の **最初の関連試合検出時** に **1回のみ**
- **ユーザー回答が「踏襲継続」の場合**: 当該シーズン中の以降の同リーグ試合は再判断不要
- **ユーザー回答が「区分変更」の場合**: 新シーズン開始時点から新区分を適用 (旧シーズン記録への遡及変更は実施しない)

##### フォーマット変更時: 強制再判断 (Claude 自発判断禁止・ユーザー判断必須)

大会フォーマット変更 (リーグ統合・分割・round 構造変更・出場枠変更等) を Claude が検知した場合、**強制再判断** を発動:

- **検知トリガー**: (a) リーグ公式発表のフォーマット変更 / (b) round 数 / 出場枠の前年比変動 / (c) 主催者・運営団体の変更等
- **強制再判断ワークフロー**:
  1. Claude が「フォーマット変更を検知」とユーザーに通知
  2. 旧フォーマット下の判断 (区分1/2/3) を **無効化** とする旨を明示
  3. 新フォーマット下での記録対象判断をユーザーに依頼 (柱D サブセクション8 ワークフロー再実行)
- **Claude 自発判断による踏襲継続は禁止** (議題8 確定方針)

##### シーズン跨ぎ判定基準 (種目別)

各種目のシーズン境界を以下のテーブルで判定する。Claude は本テーブルに基づき、当該リーグの新シーズン開幕日経過を機械的に判定して見直し提案を発動する:

| 種目 | シーズン跨ぎ判定基準 |
|---|---|
| **ATP / WTA テニス** | ATP/WTA Tour カレンダー (1月〜11月) で年度跨ぎ (毎年 11月→1月の Off-season 切れ目) |
| **NHL / NBA / MLB / NFL (北米プロ)** | 各リーグのレギュラーシーズン開幕日 (NHL=10月 / NBA=10月 / MLB=3-4月 / NFL=9月) |
| **サッカー (5大リーグ)** | ヨーロッパシーズン (8月〜5月) で年度跨ぎ (毎年 5月→8月の Off-season 切れ目) |
| **ラグビー (Premiership / Top14 / Pro D2 / NRL / Super Rugby / Super League)** | 各リーグの公式シーズン開幕日 |
| **CFL / UFL / AHL** | 各リーグのレギュラーシーズン開幕日 (CFL=6月 / UFL=3月 / AHL=10月) |

##### 議題8 確定方針との整合

本サブセクションは Session_62 フェーズ6 第3段階で確定した議題8 方針 (案B 原則 + シーズン跨ぎ見直し提案 + フォーマット変更時強制再判断) を完全反映している。3層構造 (案B 原則 → シーズン跨ぎ → フォーマット変更) により、運用負荷の最小化 (案B 原則の踏襲) と判断精度の確保 (シーズン跨ぎ + フォーマット変更時の見直し) を両立する。

### 9. Session_61 由来 9件 振り分け案 (4本柱完了後の別タスクで実施)

> **本テーブルは 4本柱完了後の遡及判断タスク (A-3 等) で参照する判断材料**。本フェーズでは記録のみで実装は行わない。Session_61 由来 12件 (Modified 8 + Untracked 4) + ready_to_implement 候補 (P020 / P024) は 4本柱完了まで凍結維持。

| # | 試合 | 推奨区分 | match_status | 根拠 |
|---|---|---|---|---|
| 1 | Bristol 52-19 Newcastle Premiership | 区分1 (full_record) | completed | scope内大会 / regular round / 試合成立 / 市場fav 敗戦 (UPSET) |
| 2 | Northampton 41-38 Bath Premiership | 区分1 (full_record) | completed | scope内 / 既 records 登録 (date 訂正のみ必要 4/26→4/25) |
| 3 | Swiatek retire vs Li Madrid R3 | 区分2 (reference_only) | retired | Swiatek (#1 シード) retire は UPSET 性質あり |
| 4 | Bondar d. Svitolina (#7 seed) Madrid R2 | 区分1 (full_record) | completed | scope内 (WTA Masters 相当) / R2 / 試合成立 / #7 seed 敗退 (UPSET) |
| 5 | PHI G4 vs PIT (NHL Playoffs) | 区分1 (full_record) | completed | scope内 / Playoffs / 試合成立 |
| 6 | TOR 93-89 CLE G4 (NBA Playoffs) | 区分1 (full_record) | completed | scope内 / Playoffs / 市場fav CLE 敗戦 (UPSET) |
| 7 | HOU 115-96 LAL G4 (NBA Playoffs) | 区分1 (full_record) | completed | scope内 / Playoffs / 市場fav LAL 敗戦 (UPSET) |
| 8 | Baptiste d. Paolini Madrid R3 | 区分1 (full_record) | completed | scope内 (WTA Masters) / R3 / Paolini fav 敗戦 (UPSET) |
| 9 | Pliskova(PR) d. Mertens(#19) Madrid R3 | 区分1 (full_record) | completed | scope内 / R3 / Mertens (#19) 敗戦 (UPSET) |

**遡及登録時の処理**: 4本柱完了後の別タスクにて、上記推奨区分に基づき records/{sport}/*.json への登録 (区分1) または upset_patterns.json への参考登録 (区分2) を実施する。Session_61 由来 12件 (Modified + Untracked) との統合実施を予定。

**訂正履歴**: 2026-04-28 A-3 サブタスク3 セッション1 ステップ5 で #9 試合表記を `Pliskova(Q)` → `Pliskova(PR)` に訂正 (WebFetch 確認結果反映 / Pliskova はキャリア中の Protected Ranking 利用エントリで Qualifier ではない)。

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
