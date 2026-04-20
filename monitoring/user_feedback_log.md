# ユーザー指摘・意見・質問ログ

> **Claude Codeへの指示：**
> - ユーザーから指摘・意見・質問があったら即座にこのファイルに追記する
> - ステータスは OPEN（未解決）/ RESOLVED（解決済み）/ ONGOING（継続対応中）
> - RESOLVEDにするのはユーザーが明示的に確認した場合のみ。自己判断でRESOLVEDにしない
> - セッション開始時に必ず読み込み、OPENの項目を報告する

---

## ステータス凡例
- `OPEN` — 未解決（優先対応）
- `ONGOING` — 継続対応中（ルール化・仕組み改善として継続監視）
- `RESOLVED` — 解決済み（ユーザー確認済み）

---

## ログ

| ID | 日付 | 種別 | 内容 | ステータス | 対応内容 |
|---|---|---|---|---|---|
| FB001 | 2026-04-14 | 指摘 | 「4-14のファイルを見なかったのでは？」→ 実際は両ファイルを同時読込していたが説明が不明確だった | RESOLVED | 両ファイル同時読込を確認・説明。4/13=NRL/NHL-4/14データ、4/14=NHL-4/15データと整理 |
| FB002 | 2026-04-14 | 指摘 | 「スクリーニングするという意味で返答が来ている」→ 保留（CAUTION）で終わらせてはいけない | RESOLVED | MoneyPuck xGF%を自分でWebFetch取得して即スクリーニング実施 |
| FB003 | 2026-04-14 | 指摘 | 「データを持ち込んでもらえればは私が提供するものではない」→ xGF%等の統計データはClaudeが自分で取得すべき | ONGOING | 対応済み。今後もユーザーに統計取得を求めない。MoneyPuck/Basketball-Reference等を自分でWebFetch |
| FB004 | 2026-04-14 | 質問 | 「スクリーニングしたデータは4/13に存在しなかったデータか？」→ 新データの確認 | RESOLVED | 4/15 NHL試合は4/14ファイルにのみ存在することを確認・報告 |
| FB005 | 2026-04-14 | 意見 | 日本時間（JST）でデータが提供されているため時刻解釈に注意が必要 | ONGOING | 常にJSTベースで解釈。4/15 08:00 JST = 4/14 7PM ET等の変換を意識する |
| FB006 | 2026-04-17 | 指摘 | [59] Fonseca vs Shelton は「今日」。私がCE011としてinvalid化したが、QFで対戦するため組合せとしては正しかった | RESOLVED | [59]を R2→QF に修正・invalid解除。[58] Cobolli vs Kopriva も同様にQFで対戦することを確認し修正。Munich QF残り2試合(Zverev/Cerundolo, Shapovalov/Molcan)も新規登録。CE011の記述を「R2ラベル誤りだがQF組合せと偶然一致」に格下げ |
| FB007 | 2026-04-20 | 要望 | フランスのTop14などラグビーユニオンは怪我人の関係によるローテーションメンバーなのかどうかが勝敗に影響する可能性を考慮に追加して欲しい | RESOLVED | 4ラグビーユニオンルール (top14/prod2/premiership/superrugby) に injury_rotation 補正ルール追加 (T006/D006/P006/SR006)。欠場数別補正(-3/-7/-12%)、key positions (fly-half/scrum-half/captain/front row)、rotation triggers (欧州杯/Test window/プレーオフ/back-to-back/long-term復帰)、team sheet 試合前48h確認必須化 |
| FB008 | 2026-04-20 | 要望 | 土砂降りレベルの雨だとパスやランのチームが得意なパターンを作れずに負けるケースがある・FWで強いチームは勝ちやすい | RESOLVED | 4ラグビーユニオンルールに weather_style_matchup 補正ルール追加 (T007/D007/P007/SR007)。大雨×パスラン型チーム -7%信頼度 / FW型+5%。天候カテゴリ3段階(heavy rain/moderate/extreme heat)。team style 分類ガイド・天候予報確認ソース (weather.com/meteofrance.fr/metservice.com) 明記 |
