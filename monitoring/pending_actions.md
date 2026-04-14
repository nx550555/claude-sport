# ペンディングアクションキュー

> **Claude Codeへの指示：**
> - タスク完了後に必ずこのファイルを確認し、残PENDINGを報告する
> - PENDING項目はユーザーが「不要」「スキップ」と明示するまで削除しない
> - 新しいタスクが発生したらすぐに追記する
> - 一つの指示に対応した後、他のPENDING項目をユーザーに確認する（機能③の核心）

---

## ステータス凡例
- `PENDING` — 未着手・待機中
- `IN_PROGRESS` — 現在対応中
- `WAITING` — 外部情報待ち（結果・オッズ・データ等）
- `DONE` — 完了（ユーザー確認済みまたは明示的に完了）
- `SKIP` — 不要とユーザーが明示

---

## アクティブキュー（PENDING / WAITING / IN_PROGRESS）

| ID | 種目 | 内容 | ステータス | 優先度 | 期日 |
|---|---|---|---|---|---|
| PA001 | UFL | Week3 Dallas vs Columbus 結果確認・記録（GO Dallas EV+8.2% 信頼度82%） | WAITING | 高 | 4/13 ET試合後 |
| PA002 | ATP | W16 R2 スクリーニング（R1結果確認後・casino data起点） | PENDING | 高 | 4/14〜 |
| PA003 | ATP | Barcelona/Munich GO3件の結果確認（Musetti@1.27/Cobolli@1.21/Kopriva@1.36 4/14開催） | WAITING | 高 | 4/14試合後 |
| PA004 | WTA | Stuttgart R2 スクリーニング（R1結果確認後） | PENDING | 高 | 4/14〜 |
| PA005 | NHL | 4/15 CAUTION2件ゴーリー確認→最終判断（CAR@NYI 1.90 / COL@CGY 1.60） | WAITING | 高 | 本日22〜24時JST |
| PA006 | NHL | PO R1 スクリーニング（RS終了4/16後、ブラケット確定→MoneyPuck xGF%起点） | PENDING | 高 | 4/16〜17 |
| PA007 | NRL | R7 Broncos@Tigers オッズ確認（記録rec_odds 1.46 vs データ 2.50 の不一致を解消） | PENDING | 中 | 試合前 4/18まで |
| PA008 | NRL | R7 GO2件（Warriors 4/18/Broncos 4/18）・CAUTION2件の結果確認 | WAITING | 中 | 4/18〜19試合後 |
| PA009 | NBA | Play-in（4/15-16）・PO R1（4/19〜）全SKIP確認済み。結果モニタリングのみ | WAITING | 低 | 継続 |
| PA010 | MC2026 | F Alcaraz vs Sinner 結果確認（SKIP・観戦のみ） | WAITING | 低 | 4/13試合後 |

---

## 完了キュー（DONE / SKIP）

| ID | 種目 | 内容 | ステータス | 完了日 |
|---|---|---|---|---|
| PA-C001 | ATP | Barcelona/Munich R1 全試合スクリーニング（GO3件: Musetti/Cobolli/Kopriva） | DONE | 2026-04-13 |
| PA-C002 | WTA | Stuttgart R1 全12試合スクリーニング・結果記録（GB001 HIT） | DONE | 2026-04-13 |
| PA-C003 | WTA | Rouen R1 全16試合スクリーニング（全SKIP） | DONE | 2026-04-13 |
| PA-C004 | NHL | RS最終盤 4/15 全9試合スクリーニング（CAUTION2件 → PA005に継続） | DONE | 2026-04-14 |
| PA-C005 | NBA | Play-in/PO R1（8試合）スクリーニング（全SKIP NRtg差<5pt） | DONE | 2026-04-14 |
| PA-C006 | NRL | R7 全8試合スクリーニング（GO2件/CAUTION2件/SKIP4件） | DONE | 2026-04-13 |

---

## ルール：残タスク確認プロトコル

ユーザーから一つの指示が来て完了した後、必ず以下を実行する：

```
【残タスク確認】
上記のほかに以下 X 件が残っています：
・PA00x: [内容] — [ステータス]
・...

不要なものがあれば教えてください。引き続き対応が必要なものはキューに残しておきます。
```
