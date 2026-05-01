# Session Summary - 2026-05-01 (Part 2 / Approach C Stage 1.5)

## 達成した成果

3 つのコミット:

- `d8f8acd`: `core/awaiting_lineup_bet_schema.json` 新規作成(awaiting_lineup tier 登録時の必須フィールド定義、MLB v1.0)
- `51284b2`: `core/drop_reason_thresholds.json` 新規作成(足切り理由分類の閾値設定、MLB v1.0)
- `5940cde`: `CLAUDE.md` MLB セクション書き換え(3 段階パイプライン明文化、+62 行 -9 行)

## 議論した内容(結論が出たもの)

- Approach C Stage 1.5(awaiting_lineup tier の運用基盤整備)を優先する方針で進めた
- 案 D(スポーツに依存しない設計、tier 並存)を採用、Stage 5+ で案 F(tier 統合)への移行を検討
- α(3 段階運用: awaiting_lineup → provisional_go → go)を確定
- bet_schema は MLB のみ対応で開始(NHL 用 expected_goalie は他スポーツ展開フェーズに延期)
- drop_reason 閾値は経験則ベース(SP ERA +0.5 / wOBA -0.020 / delta_ev_abs 1.0pp / delta_win_prob_abs 1pp)で初期化、実運用でチューニング

## 議論したが結論保留・次セッション以降の課題

- scripts/recalc_ev_from_lineup.py 実装(Approach C Stage 2-A)
- scripts/promote_provisional_to_go.py 実装(Approach C Stage 2-B)
- check_upcoming_games.py を `lineup_watch_target` フラグ判定方式に改修
- awaiting_lineup tier への bet 書き込みロジック設計
- lineup_watch.yml の TODO コメント解除と morning job への組み込み
- 既存 provisional_go 定義に `lineup_watch_target: true` を後付け追加
- BACKLOG.md の Stage 5(tier 統合)・Stage 6(他スポーツ展開)の正式登録

## 次セッションで最初にやるべきこと(最重要)

**Claude Code を 2 セッション体制(設計役 ①、実装役 ②)に再構成する。**

背景:
- 直近の運用で「claude.ai と Claude Code の往復」によって設計議論が膨張、4/25 から 5/1 まで 6 日間ベット実行ゼロの状態が続いた
- 引き継ぎ事故(チャット切り替え時に方向性がズレる)が繰り返し発生
- 議論記録が claude.ai 側に残るが、検索性・参照性が低い

提案構成:
Ayumu
├── Claude Code ①(設計役) … 別フォルダ(例: claude_sport_meta/)で起動
│     └── ファイル(議論記録、指示文)を出力
│
└── コピペ(Ayumu が手動)
↓
Claude Code ②(実装役) … 既存の claude_sport/ で起動

具体的な準備タスク(次セッション冒頭で実施):

1. `claude_sport_meta/` フォルダを新規作成
2. 中に `CHARTER.md`(目的・やらないこと・スコープ制約)を作成
3. `conversations/` サブフォルダを作成(設計議論の記録用)
4. `handoffs/` サブフォルダを作成(セッション間引き継ぎ用)
5. claude_sport_meta/ で Claude Code を起動して動作確認

CHARTER.md に最低限書くべき内容:
- 最上位目的(変えてはいけない)
- やらないこと(明示的禁止リスト)
- 議論膨張防止のセルフチェック条件
- 設計役 Claude Code が持つべき判断基準

## 警告(次セッションの Claude / Claude Code が必ず読むべき)

直近のセッションで起きた問題:

- 設計議論が「もっともらしい次の Q」を出し続けることで膨張、Ayumu の判断疲労を引き起こした
- 「Stage 1.5」「Approach C」などの略号を補足なしで多用し、Ayumu との認識ズレを生んだ
- 「将来の○○移行」「sport-agnostic」「責務分離」といった抽象語で議論を膨らませた
- 4/25 以降 6 日間、ベット実行ゼロのままシステム改善議論が続いた(目的と手段のすり替え)

次セッションでの再発防止:

- 略号を使うときは必ず日本語補足を併記する
- 選択肢を 3 つ以上出す前に、2 択にできないか検討する
- 議論が 3 往復続いたら「これは目的に直結しているか?」を Claude 側から問い直す
- 「将来の拡張」「美しい設計」を理由に提案する前に、目的への直結性を確認する

## 関連ファイル

- `core/awaiting_lineup_bet_schema.json`(本セッション新設)
- `core/drop_reason_thresholds.json`(本セッション新設)
- `CLAUDE.md`(MLB セクション書き換え)
- `core/rules_mlb.json`(M012, M013 — 前セッションで追加済み)
