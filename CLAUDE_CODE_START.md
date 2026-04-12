# ベッティング分析システム — Claude Code 引き継ぎファイル
# このファイルをClaude Codeセッションの最初に読ませてください

---

## あなたへの指示

このファイルを読んだら、以下を実行してください：

**【毎回必須】最初に必ず読む：**
1. `C:\Users\ohwada\Desktop\claude_sport\BACKLOG.md` を読み込む
   - `[~]` 作業中の項目があれば「前回途中になっています」と報告する
   - `[ ]` 未着手の項目があれば一覧を表示する

**【毎回必須】抜け漏れチェック（②の要件）：**
以下を確認して「現状チェック」として報告する：
- hit:null の未確認試合が records/ にないか
- BACKLOG.md の [ ] 未着手項目で対応できるものはないか
- 前回の分析ログ（daily_reports/）と今回の状況に乖離がないか
- 今日・明日に試合がある種目でスクリーニングが必要なものはないか

**【会話終了時】セッション終了手順（③の要件）：**
ユーザーが「会話を終了する」「終わり」「終了」などと言ったら：
1. このセッションで行った作業を `session_logs/YYYY-MM-DD_HH.md` に保存する
2. BACKLOG.md の完了項目を [x] に更新する
3. 次回への申し送り事項を BACKLOG.md の「未完了」欄に追記する
4. `git add -A && git commit -m "Session end YYYY-MM-DD" && git push origin main` を実行する
5. 「セッション終了。次回は〇〇から再開します。」と報告する

**テニス（ATP）の作業をするとき：**
1. `C:\Users\ohwada\Desktop\claude_sport\core\rules_tennis.json` を読み込む
2. `C:\Users\ohwada\Desktop\claude_sport\records\tennis\2026-ATP.json` を読み込む
3. OddsPortalで「今週オッズが付いているATP試合」を確認してからスクリーニングを開始する
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
└── dashboard/
    └── index.html              ← 閲覧用ダッシュボード
```

---

## 現在の状況（2026-04-10時点）

### ATP テニス（MC2026）
- R32：完了（1/5的中、EV -3.37u）
- R16：完了（1/2的中、EV -0.43u）
- QF：**本日進行中**（Zverev的中確定、Alcaraz・Sinner結果待ち）
- SF：4/11 / F：4/12

### WTA テニス
- 稼働開始（Stuttgart Porsche Tennis Grand Prix 4月下旬〜）
- 次にやること：Stuttgart開幕時にオッズ・cElo確認→分析

### NHL
- レギュラーシーズン終盤。プレーオフ直前。
- 記録：COL勝利確定（1/1）、OTT@NYI（4/11）結果待ち
- 次にやること：OTT@NYI結果確認＋プレーオフ開始後に分析継続

### UFL（Week3）
- Dallas vs Columbus（4/13）結果待ち
- Louisville vs Orlando（4/11）スキップ済み
- 次にやること：4/13結果確認→Week4分析

### NFL
- オフシーズン（2026年9月開幕予定）
- ドラフト・トレードのニュースは記録不要。開幕前にDepth Chartを確認。

### CFL
- オフシーズン（2026年6月開幕予定）
- 開幕1〜2週前にrules_cfl.jsonを読み込み分析開始

### NRL（Round6）
- South Sydney vs Canberra（4/11）結果待ち（推奨：Rabbitohs 1.55）
- 次にやること：4/11結果確認→Round7分析

### Super Rugby Pacific
- 稼働開始（2026-04-10）
- 次にやること：今週のラウンドのオッズ・得失点差確認→初回分析

---

## 分析フロー（種目共通）

```
① OddsPortalで本日の試合一覧を取得
② 対象スポーツのL1指標でスクリーニング
③ 候補のみL2〜L4を深掘り
④ 信頼度≥75% AND EV>+5% → 推奨として出力
⑤ 結果確認後 → records/{sport}/{year}.json を更新
⑥ 新しい外れがあれば rules_{sport}.json にルール追加して上書き保存
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
