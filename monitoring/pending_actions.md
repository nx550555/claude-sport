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
| PA001 | UFL | Week3 Dallas vs Columbus 結果確認・記録（GO Dallas EV+8.2% 信頼度82%） | DONE | 高 | 完了 4/14 |
| PA016 | 全スポーツ | Type Aアップセット分析 品質補完（A001-A013 ニュース/ブログ/SNS多ソース検証 + rule_pipeline候補を rules_*.json に実装） | DONE | 最高 | 完了 2026-04-16 |
| PA002 | ATP | W16 R2 スクリーニング（Barcelona R2 4件 + Munich R2 5件 完了） | DONE | 高 | 完了 2026-04-16 |
| PA003 | ATP | Barcelona/Munich GO3件の結果確認（Musetti@1.27/Cobolli@1.21/Kopriva@1.36 4/14開催） | DONE | 高 | 完了 4/15 全HIT |
| PA004 | WTA | Stuttgart R2 + Rouen R2 スクリーニング完了（全試合SKIP/EV負） | DONE | 高 | 完了 2026-04-16 |
| PA005 | NHL | 4/15 CAUTION2件ゴーリー確認完了: CAR@NYI=Andersen確認(N006解消)試合進行中 / COL@CGY=Blackwood起用→N016発動→SKIP推奨 | DONE | 高 | 完了 4/15 |
| PA006 | NHL | PO R1 スクリーニング（RS終了4/16後、ブラケット確定→MoneyPuck xGF%起点） | DONE | 高 | 完了 4/16 |
| PA014 | NHL | PO R1 TBL vs MTL CAUTION→GO確認（G1=4/18。TBL: Vasilevskiy確認済4-2 2.19GAA .912sv%。MTL: Dobes(29-10-4 2.78GAA .901sv%)。オッズ確認+min 1.38要） | PENDING | 高 | 4/18試合当日 |
| PA015 | NHL | PO R1 COL vs LAK CAUTION（G1=4/18。Manson OUT(上半身)/Bednar返答済→playoff復帰見込。Kadri復帰見込。Blackwood 22-10-2 2.55GAA .901sv%。オッズ確認要） | PENDING | 中 | 4/18試合当日 |
| PA017 | NBA | PO R1 SAS vs POR GO @1.18 結果確認（G1=4/20 JST。Wembanyama ACTIVE確認済。Lillard OUT全季。EV+5.6%） | WAITING | 高 | 4/20試合後 |
| PA007 | NRL | R7 Broncos@Tigers オッズ確認（REVOKED済→odds discrepancy無効） | SKIP | 中 | Broncos REVOKED済 |
| PA008 | NRL | R7 GO2件（Warriors 4/18/Broncos 4/18）・CAUTION2件の結果確認 | WAITING | 中 | 4/18〜19試合後 |
| PA009 | NBA | Play-in（4/15-16）・PO R1（4/19〜）全SKIP確認済み。結果モニタリングのみ | WAITING | 低 | 継続 |
| PA010 | MC2026 | F Alcaraz vs Sinner 結果確認（SKIP・観戦のみ） | DONE | 低 | 完了 4/14 Sinner 7-6(5) 6-3 |
| PA011 | システム | 【フェーズ移行T3発動】実装済みルール3件達成→Phase2移行可否をユーザーに確認 | PENDING | 中 | 確認待ち |
| PA012 | WTA | Stuttgart Zhang vs Noskova R1 結果確認 | DONE | 高 | 完了 4/16 Noskova d. Zhang 5-7 6-1 6-4 (予測HIT/SKIP nobet) |
| PA013 | ATP | Barcelona R2 Musetti vs Moutet GO @1.37 結果確認 | DONE | 高 | 完了 4/17 Musetti d. Moutet 6-3 6-4 (GO HIT +0.37u) |
| PA018 | UFL | W4 Louisville vs Houston GO @1.65 結果確認 | DONE | 高 | 完了 4/17 Louisville 24-22 OT (HIT +0.65u) |
| PA019 | WTA | Stuttgart R2 全6試合結果確認 (Swiatek/Gauff/Muchova/Rybakina HIT, Alexandrova/Andreeva/Fernandez R2一部未確認) | IN_PROGRESS | 中 | 4/17 |
| PA020 | ATP | Alcaraz Barcelona R2棄権 (右手首負傷) → 出力A #2/マルチ rank 2&4 VOID対応 | DONE | 高 | 完了 4/17 |
| PA021 | UFL | W4 Renegades @1.36 GO 結果確認 (4/18 Columbus @ Arlington) | WAITING | 高 | 4/18試合後 |
| PA022 | NHL | PA014 TBL vs MTL: Lightning series -275 ≈ML1.36でmin 1.38未達の可能性 → G1オッズ精査必要 | IN_PROGRESS | 高 | 4/18試合当日 |
| PA023 | ATP | Munich QF 4試合(4/17)結果確認 — 全SKIP予測(Cobolli/Zverev/Fonseca/Shapovalov)。特に Shapovalov vs Molcan は P013/P014 候補関連 | WAITING | 高 | 4/17試合後 |
| PA024 | ATP | Barcelona QF 4試合(4/17)結果確認 — 全SKIP予測(Medjedovic/Rublev/Musetti/Jodar)。Jódar P010 候補関連 | WAITING | 高 | 4/17試合後 |
| PA025 | WTA | Rouen QF 結果確認: 手動データ(2026-04-17.json)でPodrez d. Boulter(upset 2.55)報告あり。WebSearchインデックス遅延→次セッションで一次確認後に記録 | WAITING | 高 | 次セッション |
| PA026 | ATP | Munich QF 手動データ(2026-04-17.json)完了分報告: Fonseca d. Shelton / Shapovalov d. Molcan。WebSearchインデックス遅延→次セッションで一次確認後に記録 | WAITING | 高 | 次セッション |
| PA027 | WTA | Stuttgart QF 手動データ(2026-04-17.json)完了分報告: Swiatek d. Andreeva / Rybakina d. Fernandez。WebSearchインデックス遅延→次セッションで一次確認後に記録 | WAITING | 高 | 次セッション |
| PA028 | Premiership | Exeter-Northampton/Sale-Saracens 2試合のPD/G完全取得→L1スクリーニング | PENDING | 中 | 4/18試合前 |
| PA029 | Top 14 | Bayonne-Pau/Castres-Toulouse/Racing-StadeFrancais 3試合のPD/G完全取得→L1スクリーニング | PENDING | 中 | 4/18-20試合前 |
| PA030 | Pro D2 | Stade Montois-Dax/Nevers-Valence/Beziers-Provence/Grenoble-Oyonnax 4試合のPD/G完全取得→L1スクリーニング | PENDING | 中 | 4/18試合前 |
| PA031 | NHL | TBL vs MTL G1: min odds 1.38 PASSED (now 1.53). 信頼度76%/EV+16.28%→goalie confirmed次第でCAUTION→GO昇格候補。dailyfaceoff 4/18 morning確認要 | IN_PROGRESS | 最高 | 4/18試合当日 |

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

---
**Session_30 更新 (2026-04-15):**
- NHL CAR@NYI 2-1 HIT / COL@CGY 3-1 HIT (両CAUTION/SKIP・ベットなし・予測HIT) → pending_games cleared
- UFL DC vs STL CAUTION: Ta'amu確認済・L1データ追加 (DC+16.7/G vs STL-2.0/G、conf78%、EV+12.3%)
- NRL Warriors/Titans GO維持 (Capewell復帰確認) / Broncos REVOKED確認 (Luai+May復帰・Carrigan/Walsh/Paix全欠場)
- ATP W16 R1 全5試合結果記録済
- WTA Paolini vs Sonmez: 2ndセット中断中・未完了 (Sonmez 6-2 lead, 2nd set suspended)
- WTA Zhang vs Noskova: 1stセット中断・未完了
- P003 Stuttgart R1 trigger: 未達 (Paolini/Sonmez + Zhang/Noskova の2試合がまだ未完了)

---
**Session_31 更新 (2026-04-16):**
- Type A/B アップセット分析フレームワーク深掘り実施
- CE006-CE009: Stuttgart R1 データ誤入力4件修正 (Korpatsch/Shnaider・Eala/Fernandez・Samsonova/Ruzic・Zhang/Noskova SL)
- 真のType A確認済みアップセット: Lys/Badosa 2-6 7-5 6-4 → A001として upset_patterns.json に追記
- PA007: NRL Broncos REVOKED済のため odds discrepancy は無効 → SKIP推奨
- Zhang/Noskova Stuttgart R1: まだサスペンド中 (Zhang 7-5/Noskova 6-4/3rd set in progress) → PA012追加
- ATP Barcelona R2 Musetti@1.37 GO (4/16 18:00) 結果確認要 → PA013追加

---
**Session_33 更新 (2026-04-16) GEN003チェック:**
- PA012 DONE: Noskova d. Zhang 5-7 6-1 6-4 (WTA公式動画確認)。予測HIT・SKIPノーベット。
- PA013 DONE: Musetti HIT vs Moutet (ATP Tour公式「Alcaraz, Musetti advance」確認)。actual_ev +0.37u。スコア要確認。
- PA014更新: TBL Vasilevskiy確認(4-2 2.19GAA .912sv%) / MTL Dobes確認(29-10-4 2.78GAA .901sv%)。G1=4/18。
- PA015更新: COL Manson OUT(上半身) / Bednar playoff復帰見込 / Kadri復帰見込。Blackwood 22-10-2 .901sv%。
- NRL R7: Luai+May(Tigers)復帰確認=Broncos REVOKED維持正解。Adam Reynolds(Broncos)復帰・Carrigan依然停止。
- NRL Warriors GO維持: Capewell返答済・Titans変更なし。
- UFL W4: Renegades特定怪我情報なし。Louisville OL軽傷あり(Watson/Tunstill out, 試合前確認要)。

---
**Session_32 更新 (2026-04-16):**
- MoneyPuck統計: 5v5 All Season xGF%を確認。最高精度指標でPO R1スクリーニング実施
- NHL PO R1 全8シリーズL1スクリーニング完了 (PA006 DONE)
  - L1通過: TBL vs MTL (diff 6.11pp) → CAUTION (goalie+odds確認待ち, min odds 1.38)
  - L1近傍CAUTION: COL vs LAK (raw 4.70pp / score-adj 5.73pp) → CAUTION
  - SKIP 6シリーズ: BUF/BOS・CAR/OTT・PIT/PHI・DAL/MIN・VGK/UTA・EDM/ANA
  - 注目: MIN(C3)がDAL(C2)より5v5 xGF%高い / ANA(P3)がEDM(P2)より微小上回る
  - PA014(TBL G1確認) / PA015(COL G1確認) 追加
- PA013 Musetti vs Moutet: 14:00 UTC試合・結果未確認 (WAITING継続)
- PA012 Zhang/Noskova: WTA公式でSet2=6-1表示 (記録の6-4と差異)。試合完了後に要確認
---
**Session_39 追加 (2026-04-17 CE011再判定):**
- FB006記録・対応完了: [58][59]をinvalid→QF記録に格上げ
- CE011 再分類: 「R2組合せ誤り」→「ラウンドラベル誤り（QF組合せと偶然一致）」に格下げ
- Munich QF 4試合スクリーニング完了: 全SKIP (Cobolli 68%/Zverev 71%/Fonseca 62%/Shapovalov 58%)
- Barcelona QF 4試合スクリーニング完了: 全SKIP (Medjedovic 63%/Rublev 64%/Musetti 66%/Jodar 68%)
- rule_pipeline P013 新候補追加 (R1 upsetter R2モメンタム): Molcan/Kopriva 2件・残1件で実装
- rule_pipeline P014 新候補追加 (R1 upset winner R2 reversion): Shapovalov/Marozsan 1件
- rule_pipeline P007 evidence +1 (Paolini R2 MISS): current_count 1→2、残1件で実装

---
**Session_39 更新 (2026-04-17):**
- PA013 DONE: Musetti d. Moutet 6-3 6-4 (ATP Tour公式・puntodebreak複数ソース確認)。GO @1.37 HIT +0.37u。
- PA018 追加→DONE: UFL W4 Louisville 24-22 OT Houston (Kings初勝利・Bean 17/34 192yd・OT 2pt conv成功)。GO @1.65 HIT +0.65u。
- PA019 追加: WTA Stuttgart R2 Swiatek/Gauff/Muchova/Rybakina HIT確認。Alexandrova vs Noskova / Andreeva vs Parks / Fernandez vs Sonmez (4/17) は追加確認要。
- PA020 追加→DONE: Alcaraz Barcelona R2棄権 (右手首負傷4/16判明)。出力A #2 VOID / マルチ rank 2/4 のAlcarazレッグはブックで再評価。Madrid/Rome・Roland Garros出場リスク報道。
- PA021 追加: Renegades @1.36 GO 4/18開催 WAITING。
- PA022 追加: TBL vs MTL series price -275 ≈ ML1.36、min odds 1.38要件未達の可能性大 → 4/18当日G1オッズ再精査。
- 出力A結果: HIT=4 (Swiatek/Louisville/Gauff/Musetti) / MISS=1 (Paolini) / VOID=1 (Alcaraz) / PENDING=1 (Renegades)
- 出力B結果: LOSE=2 (rank3/4 Paolini MISS) / PENDING=3 (rank1/2/5 Renegades待ち、うちrank2はAlcaraz VOIDで再評価)
- dashboard_stats.json 更新: ATP 11/14 78.6% +1.74u / UFL 2/2 100% +0.97u / Overall 19/24 79.2% +4.06u
- dashboard.html: Musetti/Louisvilleアクティブカード削除 + 出力A結果列反映 + マルチベットタブ leg-status行追加

---
**Session_38 更新 (2026-04-16):**
- PA002 DONE: ATP Barcelona R2(4件) + Munich R2(5件) スクリーニング完了 (全SKIP/EV負)
- PA004 DONE: WTA Stuttgart R2(6件) + Rouen R2(6件) スクリーニング完了 (全SKIP/EV負)
- NBA-003 追加: SAS vs POR GO @1.18 (EV+5.6%, Wembanyama ACTIVE, Lillard OUT) → PA017追加
- NRL Warriors vs Titans: オッズ @1.22→@1.25更新 (EV 10.7%→13.4%)
- NHL RS最終日6試合: 全SKIP (xGF%取得不可 + 主力温存リスク)
- dashboard_stats.json更新: GO=29, confirmed=22, hit=17, P&L=+3.0u
- PA013 DONE誤判定修正: 「Alcaraz, Musetti advance」=R1ハイライト（アルカラスはR2前に手首負傷ウォークオーバー）。Musetti vs Moutet R2は4/16 14:00 UTC開始予定。WAITINGに戻す。cumulative.json ATPも修正。
