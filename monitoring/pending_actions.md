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
| PA014 | NHL | PO R1 TBL vs MTL G1 (4/19 5:45pm ET) 結果確認 - 手動データで live 2-2 2ndブレイク進行中確認。次セッションで最終スコア一次確認必須 | WAITING | 高 | 4/20 JST朝 |
| PA015 | NHL | PO R1 COL vs LAK G1 (4/19 3pm ET) **DONE Session_43**: COL 2-1 LAK (Wedgewood 24 saves debut). CAUTION no bet. 予測HIT | DONE | 中 | 完了 2026-04-19 |
| PA017 | NBA | PO R1 SAS vs POR GO @1.18 結果確認（G1=4/20 JST 10:00）Session_43時点で試合未確定。次セッションで結果確認 | WAITING | 高 | 4/20試合後 |
| PA007 | NRL | R7 Broncos@Tigers オッズ確認（REVOKED済→odds discrepancy無効） | SKIP | 中 | Broncos REVOKED済 |
| PA008 | NRL | R7 GO2件（Warriors 4/18/Broncos 4/18）・CAUTION2件の結果確認 | WAITING | 中 | 4/18〜19試合後 |
| PA009 | NBA | Play-in（4/15-16）・PO R1（4/19〜）全SKIP確認済み。結果モニタリングのみ | WAITING | 低 | 継続 |
| PA010 | MC2026 | F Alcaraz vs Sinner 結果確認（SKIP・観戦のみ） | DONE | 低 | 完了 4/14 Sinner 7-6(5) 6-3 |
| PA011 | システム | 【完了 2026-04-18】Phase1→Phase2 移行実施。UPSET_PICK命名（旧GAMBLE_BET）+ stake 1u統一 + GEN005衝突解消ルール制定 | DONE | 中 | 完了 2026-04-18 |
| PA012 | WTA | Stuttgart Zhang vs Noskova R1 結果確認 | DONE | 高 | 完了 4/16 Noskova d. Zhang 5-7 6-1 6-4 (予測HIT/SKIP nobet) |
| PA013 | ATP | Barcelona R2 Musetti vs Moutet GO @1.37 結果確認 | DONE | 高 | 完了 4/17 Musetti d. Moutet 6-3 6-4 (GO HIT +0.37u) |
| PA018 | UFL | W4 Louisville vs Houston GO @1.65 結果確認 | DONE | 高 | 完了 4/17 Louisville 24-22 OT (HIT +0.65u) |
| PA019 | WTA | Stuttgart R2 全6試合結果確認 (Swiatek/Gauff/Muchova/Rybakina HIT, Alexandrova/Andreeva/Fernandez R2一部未確認) | IN_PROGRESS | 中 | 4/17 |
| PA020 | ATP | Alcaraz Barcelona R2棄権 (右手首負傷) → 出力A #2/マルチ rank 2&4 VOID対応 | DONE | 高 | 完了 4/17 |
| PA021 | UFL | W4 Renegades @1.34 GO 結果確認 — **DONE 4/17 Aviators 28-14 Renegades UPSET MISS -1.0u** (CE013発生で勝敗報告ミス→訂正済) | DONE | 高 | 完了 2026-04-17 |
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
| PA032 | AHL | 初回スクリーニング完了 (27試合 RS最終週4/18-19 全SKIP)。Basic Tier厳格閾値 + AHL固有補正で全試合conf<78%/EV<+7%。プレーオフ(4/22〜)で再評価 | DONE | 中 | 完了 2026-04-17 |
| PA033 | AHL | Calder Cup Playoffs R1 (4/22〜) スクリーニング - best-of-3シリーズ。ラインナップ安定期でGO/CAUTION候補期待 | PENDING | 中 | 4/22以降 |
| PA034 | SL | R8 Leeds vs Huddersfield @1.23 GO 結果確認 — **DONE 4/17 Leeds 56-22 HIT +0.23u** (10 tries, Brodie Croft 4 tries, Brad Arthur 50th match celebration) | DONE | 高 | 完了 2026-04-17 |
| PA035 | SL | R8 Warrington @Catalans **DONE Session_43** — Catalans 38-22 Warrington UPSET (Dodd hat-trick). GO @1.64 MISS -1.0u. P016候補 (Catalans仏国ホーム補正-5%→-7/-10%検討) 記録 | DONE | 高 | 完了 2026-04-19 |
| PA037 | ATP | Barcelona/Munich QF 8試合結果確認 **DONE Session_43**: Barcelona (Rublev/Medjedovic/Fils/Jodar HIT 3/4, Musetti MISS SKIP) / Munich (Cobolli/Zverev HIT 2/4, Fonseca/Shapovalov MISS SKIP). 予測精度 5/8. P013+1 P010+1 evidence | DONE | 高 | 完了 2026-04-20 |
| PA038 | WTA | Stuttgart QF+R2残3 / Rouen QF+R2 結果確認 **DONE Session_43**: Stuttgart QF (Rybakina/Svitolina HIT 2/4), Rouen QF (Cirstea/Kostyuk HIT 2/4). Stuttgart R2残 Noskova/Fernandez HIT. Output A 4/7 HIT確定 (Swiatek/Gauff/Paolini MISS + Alcaraz VOID + Renegades MISS). | DONE | 高 | 完了 2026-04-20 |
| PA039 | Tennis | 2026-MC.json CE015波及訂正 **DONE Session_43**: SF Alcaraz vs de Minaur → Alcaraz vs Vacherot (6-4 6-4) 訂正 / Marozsan vs Hurkacz スコア 6-2 6-3 確認 / QF draw_structure/screening_log 訂正 | DONE | 高 | 完了 2026-04-20 |
| PA040 | スクリーニング | 2026-04-19.json スクリーニング **DONE Session_43**: NHL PO G1残5+G2 全SKIP / NBA PO G1残7 全SKIP / NRL R9 全SKIP / Top14 R22 全SKIP / WTA Oeiras+Madrid Q + ATP Challenger (out-of-scope, cElo取得不可) ログのみ | DONE | 中 | 完了 2026-04-20 |
| PA041 | NHL | PO R1 G1 全8試合 結果反映 **DONE Session_47**: BUF/CAR/VGK/EDM HIT, TBL/PIT/DAL MISS(A021/A027/A028), COL HIT(Session_46). 5/8 62.5% all SKIP/CAUTION no-bet | DONE | 中 | 完了 2026-04-21 |
| PA042 | P013実装判断 | Molcan/Shapovalov(MISS) + Kopriva/Darderi + Molcan/Altmaier で evidence 3件到達 → R020 「R1 upsetter R2 momentum +5%」実装判断 | PENDING | 中 | 次セッション |
| PA043 | P010実装判断 | Jodar d. Norrie (A019候補) 追加で evidence 2件到達 → R017 「WC home + 連続ラウンドモメンタム +5%」実装判断 | PENDING | 中 | 次セッション |
| PA036 | NRL | R7 Warriors @1.23 GO 結果確認 — **DONE 4/18 Warriors 28-20 Titans HIT +0.23u** (HT 22pt lead, Titans後半猛追も Warriors が最終ラインで止めて8点差逃げ切り) | DONE | 中 | 完了 2026-04-18 |
| PA-PERM01 | 常設 | **毎セッション終了時に multi_bets.json の最新 session date が本日か確認し、古ければ session エントリを追記する**（全SKIPでも「候補なし」として記録）— 2026-04-20 Session_44 運用改善で追加 | PENDING | 最高 | 毎セッション末尾 |
| PA-PERM02 | 常設 | **毎セッション終了時に dashboard.html の予測精度タブ・成長分析タブの数値を dashboard_stats.json と突き合わせる** — Session_44 で Session_42/43 の訂正が未反映と発覚したため追加 | PENDING | 最高 | 毎セッション末尾 |
| PA-PERM03 | 常設 | **スクリーニング時に UF因子（UF01〜UFA06）全件 walkthrough を必須実施**し、該当数+市場乖離を記録。UF≥3+div≥15pp で UPSET_PICK 候補化。CAUTION/SKIPでもUF≥2 なら注意記録 — Session_45 GEN005 運用改善 | PENDING | 最高 | 各試合スクリーニング時 |
| PA-PERM04 | 常設 | **出力A候補（fav conf≥85%）は EV負でも独立タグ付けで抽出し multi_bets.json に記録**。GO推奨とは別軸で管理（CLAUDE.md指示通り） — Session_45 case-C で運用漏れ発覚 | PENDING | 最高 | 各セッション末尾 |
| PA048 | GO候補深掘り | Session_45 GO_CANDIDATE 19件のうち L1深掘り（cElo/NRtg/xGF%/PD/G）で市場乖離3件以上特定 → アクティブ GO推奨化を次セッション試行 | PENDING | 高 | 次セッション |
| PA049 | P017監視 | ATP Masters Q R1 で Top100 vet 対 無名選手のupsetを継続収集。evidence 3件到達で R022 実装 | PENDING | 中 | 継続 |
| PA050 | UPSET_PICK監視 | GEN005 衝突解消テーブルの UF≥3+div≥15pp を満たす試合を継続観察。2026-04-20 Session_45 時点で発動 0件 | PENDING | 中 | 継続 |
| PA051 | 🚨最優先 | **upset_patterns 全件③→④反映監査 DONE Session_46 2026-04-20**。結果: 36→32件confirmed + 4件 invalidated(CE016 A017/A022/A023/A024)、rule_linked率 19.4%→100%、新規候補 5件追加 (P018/P019/P020/P022/P023)。Deep factor analysis 完了 (A017/A023: 4ソース検証, A022/A024: Wikipedia+TennisMajors 再検証で CE016 系確定) | DONE | 最高 | 完了 2026-04-20 |
| PA052 | CE016再発防止 | **データ取込時 winner vs market_favorite 整合性自動チェック** DONE Session_46: health_check.py v3 項目9 追加 | DONE | 最高 | 完了 2026-04-20 |
| PA053 | rule_pipeline | P023 (Top20サーブ型 vs 若手クレーモメンタム停止) evidence 3件目収集 (現在 2/3) で implement 判断 | PENDING | 中 | 継続 |
| PA054 | rule_pipeline | P012 (clay specialist vs hardcourt) evidence 3件目収集 (現在 2/3) で R019 implement 判断 | PENDING | 中 | 継続 |
| PA055 | upset_patterns 反映 | **DONE Session_47**: A021/A026/A027/A028 全件 records 反映 + factor_notes 強化 + rule_linked 付与完了。A014-A028 の id割当修正済(NONE→A0xx). | DONE | 高 | 完了 2026-04-21 |
| PA056 | NEW 新規候補 P024 | NBA PO G1 star scorer (>25ppg RS) 欠場時の -8〜-10% 信頼度補正 (A029 LAL-HOU KD欠場で発足 1/3). evidence 収集継続 | PENDING | 中 | 継続 |
| PA057 | NEW 新規候補 P025 | NHL PO type_a_watch 発動時 xGF% higher team を predicted_winner に優先設定 (A028 MIN/DAL で実証 1/3). evidence 収集継続 | PENDING | 中 | 継続 |
| PA058 | NEW Session_47 | NBA PO R1 G1 全8試合結果反映 DONE. LAL-HOU UPSET(A029)登録・KD欠場系ルール候補P024発足 | DONE | 高 | 完了 2026-04-21 |
| PA059 | NEW P018実装判断 | NHL PO G1 underdog young core activation (A021 MTL + A027 PHI) evidence 2/3 到達. あと1件で N019 実装判断 | PENDING | 中 | 継続 |
| PA060 | NEW NHL PO G2 | **DONE Session_49** 4/21-22 G2 7/8試合結果確認: BOS 4-2 BUF / TBL 3-2 MTL OT / CAR 3-2 OTT 2OT / PHI 3-0 PIT / COL 2-1 LAK OT / DAL 4-2 MIN / UTA 3-2 VGK. EDM-ANA G2 のみ pending (4/22 進行中) | DONE | 高 | 完了 2026-04-23 |
| PA061 | NEW NBA PO G2 | **DONE Session_49** 4/21-22 G2 7/8試合結果確認: PHI 111-97 BOS / POR 106-103 SAS / LAL 101-94 HOU / DET 98-83 ORL / ATL d. NYK / CLE 115-105 TOR / MIN 119-114 DEN. OKC-PHX G2 のみ pending (4/22 進行中) | DONE | 高 | 完了 2026-04-23 |
| PA062 | Madrid 本戦 R1 | 2026-04-21.json 受領済. ATP 24試合 + WTA 19試合 本戦R1 (4/22〜) スクリーニング **Session_48 で完了** | DONE | 高 | 完了 2026-04-22 |
| PA063 | Galfi GO 結果 | **DONE Session_49**: Galfi D. d. Vidmanova D. 7-5 6-3 GO @1.54 HIT +0.54u (Madrid Q Final 4/21) | DONE | 最高 | 完了 2026-04-23 |
| PA064 | Q3 output_a 4件 | **DONE Session_50**: Sonmez HIT / BOS G2 MISS / SAS G2 MISS / OKC G2 HIT (OKC 120-107 PHX SGA 37pts)。Q3 通算 9/11 81.8% | DONE | 高 | 完了 2026-04-23 |
| PA065 | EDM-ANA G2 | **DONE Session_50**: ANA 6-4 EDM UPSET (Gauthier 決勝点 残り4:52)。予測MISS。SKIP no-bet (P&L 0)。type_a_watch 的中で P025 evidence 2/3 到達 | DONE | 高 | 完了 2026-04-23 |
| PA066 | OKC-PHX G2 | **DONE Session_50**: OKC 120-107 PHX HIT (SGA 37pts/9ast)。シリーズ 2-0 OKC。Q3 output_a HIT | DONE | 高 | 完了 2026-04-23 |
| PA067 | NBA records dedup | [10][17] CLE-TOR G1 / [11][21][30] NYK-ATL / [12][20][32] DEN-MIN / [13][18] BOS-PHI G1 / [14][24] LAL-HOU / [15][23] OKC-PHX / [16][22] DET-ORL G1 等 重複登録の整理 (Session_48 import + 既存命名のずれ) | PENDING | 中 | 次セッション |
| PA068 | Madrid GO 5件 結果 | Session_50 新規 → **Session_52 GEN003 で Tsitsipas / Musetti を CAUTION 降格**。残 GO 3件: Paul @1.40 (4/24) / Keys @1.23 (4/24) / Mertens @1.37 (**4/23 date 訂正**) 結果確認 | WAITING | 最高 | 4/23-25 |
| PA076 | GEN003 Session_52 downgrade 追跡 | Tsitsipas CAUTION_MARGIN (@1.35 conf 72 / 今日 4/23) / Musetti CAUTION_WAITING (@1.42 conf 71 / 4/24 arm injury 初戦) 結果確認。CAUTION 予測精度として記録 (bet-off)。試合前に Musetti practice 状況で WAITING→SKIP 再判定検討 | WAITING | 高 | 4/23-24 |
| PA077 | UFL W5 スクリーニング | **Session_52 で W5 schedule 確認のみ** (4/24-26 4試合 Louisville/Birmingham・StL/Orlando・Columbus/Houston・日曜夕方4試合目要確認)。PD/G 取得が未実施 → 次セッションで ESPN/FOX stats 取得後に L1 スクリーニング 4試合 | PENDING | 高 | 4/23-25 |
| PA069 | Q3 output_a 7件 結果 | Session_50: Sinner/Bencic/Swiatek/Sabalenka/Andreeva/Gauff/Rybakina 予測精度追跡 | WAITING | 高 | 4/23-24 |
| PA070 | Q4 upset_watch 13件 | Session_50: Osaka-Osorio UPSET濃厚 + Popyrin/Opelka/Rinderknech/Shelton/Diallo/Grant/Samsonova 等観察 | WAITING | 中 | 4/23-24 |
| PA071 | 🚨 既存 MISS miss_analysis 欠損 全件補填 | **DONE Session_51 2026-04-23**: 健全性スキャン 58件→47件→18件→**0件**完全補填達成。内訳: NBA 8件 + NHL 13件 + ATP 16件 + MC 1件 + WTA 14件 = 計52件補填 (Phase 1: 11件 / Phase 2: 24件 / Phase 3: 18件 ph=null/VOID/WALKOVER/重複閉鎖/WTA旧分含む)。CE017 (Madrid Q records 4件勝敗逆転) を波及発見・訂正。 | DONE | 最高 | 完了 2026-04-23 |
| PA074 | CE017 波及対応 | **DONE Session_51 2026-04-23**: dashboard.html 予測精度タブに ATP 全試合 43/59 (72.9%) + WTA 全試合 23/37 (62.2%) 行を追加 + Q3 注記に CE017 訂正反映を明記。health_check v6 に「outcome_note 表記 vs prediction_hit / market_favorite 論理整合性自動検証」追加 → CE006/CE007/CE009 訂正済 outcome_note 残骸 3件 (Cerundolo/Shnaider/Fernandez) を発見・クリーンアップ。CE013-017 同根パターン未検知状態達成。 | DONE | 最高 | 完了 2026-04-23 |
| PA075 | NBA records 重複閉鎖整理 | **DONE Session_51 2026-04-23**: PA067 で挙げられた重複登録ペア 6件を整理。tier=duplicate_closed に正式化 + dedup_partner_index ポインタ追加 + 旧 tier を old_tier_before_dedup に保存。命名規約 (フル名+G_R1 形式を正規) を screening_log に明文化。NHL records は LAK@COL を Session_51 Phase3 で既補填済。閉鎖エントリ: [13]/[15]/[17]/[20]/[21]/[24]。 | DONE | 中 | 完了 2026-04-23 |
| PA072 | NEW 新規候補 P027 N_NHL_new1 監視 | Session_51 新設。NHL PO G1 underdog UPSET 後の G2 fav home rebound 補正。evidence 2/3 到達 (BOS G2 / DAL G2)。3件目候補は EDM-ANA G3 / TBL-MTL G3 等の G1 UPSET 系シリーズの G2 結果から抽出。 | PENDING | 中 | 継続 |
| PA073 | NEW NBA G2 詳細スタッツ補填 | **DONE Session_52 2026-04-23**: [30] ATL 107-106 NYK G2 → McCollum 32pts / ATL 4Q 72% / NYK 4Q 5-22 collapse → P028 新候補 (G1 home fav win 後 G2 home 4Q execution collapse) 1/3 evidence / [32] MIN 119-114 DEN G2 → Gobert vs Jokic 1-of-8 / MIN +17 2nd-chance → P029 新候補 (DPOY vs MVP center matchup) 1/3 evidence. 両 entry date 4/24→4/20 訂正. | DONE | 中 | 完了 2026-04-23 |
| PA-PERM05 | 常設 | **結果反映時は miss_analysis + miss_layer + rule_linked を必ず同時記入**（Session_50 feedback loop 改善プロトコル）。health_check v5 で毎セッション STEP 0 に自動検知 | PENDING | 最高 | 毎 MISS 発生時 |
| PA-PERM06 | 常設 | **GEN007 システム改善提案の常時義務** (Session_54 2026-04-23 制定)。データ取得失敗・MISS反復・ルール肥大化・自動化余地などを検知したら Claude 側から能動的に改善案を提案する継続契約。遠慮して提案しないことがルール違反。毎セッション冒頭に GEN007 意識を確認 | PENDING | 最高 | 毎セッション冒頭+検知時 |
| PA078 | NHL | PO G3 結果追跡 (8試合) 4/24-26: BOS/OTT/LAK/MTL/UTA/ANA/MIN/PHI home各. CAUTION_MARGIN OTT-CAR, Q4_upset_watch ANA-EDM 注目 | WAITING | 高 | 4/24-26 |
| PA079 | UFL | W6 結果追跡 (4試合) 4/24-27: Stallions/ORL/HOU/REN home. 全SKIP予測精度追跡 | WAITING | 中 | 4/24-27 |
| PA080 | Super League | R9 結果追跡 (7試合): Leeds vs Catalans Q3_output_a, St Helens vs Wakefield Q4_upset_watch. Bradford-HKR odds data error未解消 | WAITING | 中 | 4/23-26 |
| PA081 | Premiership | R14 結果追跡 (5試合): Newcastle-Bristol Q3_output_a (BRI conf 88%), Harlequins-Sale / Northampton-Bath Q4_upset_watch | WAITING | 中 | 4/24-26 |
| PA082 | Top14 | R23 Toulouse vs Clermont (4/27) Q3_output_a 予測精度追跡 | WAITING | 中 | 4/27 |
| PA083 | AHL | Calder Cup PO 8試合結果追跡。全 Basic Tier SKIP 予測精度。PA033 partial 完了 | WAITING | 低 | 4/24-26 |
| PA084 | CE018 発見 | Top14 RCT Toulon vs Stade Toulousain 表記混同。Session_53 訂正済. 将来の France rugby 取込時に類似 RCT/Stade Toulousain 区別チェックを入れる | PENDING | 中 | 次フランスデータ受領時 |
| PA085 | GEN007 Understat 修復 | **DONE Session_56 2026-04-23**: 旧 `teamsData` JS 変数は完全消失 → Playwright で完全レンダリング後の HTML `<table>` を直接 HTML パースする方式に fetcher 書き直し。5リーグ 96 teams 取得成功 (EPL 20 / La Liga 20 / Bundesliga 18 / Serie A 20 / Ligue 1 18)。stats_feed_reader 変更不要（team_id→team_slug フィールド拡張のみ） | DONE | 中 | 完了 2026-04-23 |
| PA086 | GEN007 FanGraphs 修復 | **DONE Session_56 2026-04-23**: Cloudflare challenge は Playwright headless でも突破不可と確認 → 公式 MLB StatsAPI (`statsapi.mlb.com/api/v1/teams/stats`) に切替で Cloudflare 完全回避。wRC+ は OPS+ proxy (100 × team_OPS / lgOPS) / FIP は (13×HR + 3×(BB+HBP) - 2×K)/IP + cFIP で生スタッツから計算。30 teams 取得 (lgOPS=0.708 / lgERA=4.13 / cFIP=3.13 現実的値)。wRC_plus_is_proxy / FIP_is_computed フラグで推定値を明示 | DONE | 中 | 完了 2026-04-23 |
| PA087 | Session_55 修復 DONE | fetch_baseball_savant.py URL 修正 (batter-team/pitcher-team) で 30 teams 取得。fetch_lineups.py 全面書き直しで NBA 6/MLB 18/soccer 14 取得。fetch_understat.py curl shortcut 修正 (teamsData 検査)。health_check v7 parse=0 空フィード検知追加 | DONE | 最高 | 完了 2026-04-23 |
| PA088 | Session_56 GEN007 #2 Q3_mid 新設 DONE | Q3_output_a 閾値 85% は維持しつつ、80-84% 帯を Q3_mid として別バケット追跡開始。framework.json quadrant_framework セクション追加・CLAUDE.md 4象限テーブル更新・cumulative.json Q3_mid bucket 追加。統合禁止・分離表示必須。| DONE | 高 | 完了 2026-04-23 |
| PA089 | Session_56 GEN007 #3 UCL 拡張 DONE | rules_soccer.json に UCL/UEL target_leagues + ucl_uel_adjustments セクション追加。5大リーグ所属クラブ同士のみ対象。records/soccer/2025-26.json に SOC-001 PSG-Bayern (4/29) + SOC-002 Atletico-Arsenal (4/30) 初回登録。PSG-Bayern は SKIP、Atletico-Arsenal は CAUTION_MARGIN (conf 49.4% EV+28.3%)。両試合 STEP 4.5 必須 | DONE | 高 | 完了 2026-04-23 |
| PA090 | Session_56 GEN007 #1 保留: conf キャリブレーション | soccer records 50試合到達時に再提案。現状は仮係数 (logistic divisor=400 / xGD_bonus=0.015 / conf上限=0.92) で運用。understat の過去 backtest data を使うか、自前 records 蓄積を待つかは再提案時に決定。ユーザー判断: 保留 (2026-04-23) | PENDING | 中 | soccer 50試合到達時 |
| PA091 | Session_56 Q3_mid sync_dashboard.py 拡張 | sync_dashboard.py / dashboard_stats.json に Q3_mid バケットを表示する分離セクションを追加する必要あり。現状 cumulative.json は更新済だがダッシュボード可視化未対応 | PENDING | 中 | 次セッション以降 |
| PA092 | Session_56 UCL SF STEP 4.5 | PSG-Bayern (4/29 04:00 JST) と Atletico-Arsenal (4/30 04:00 JST) のキックオフ75分前に fetch_lineups.py --sport soccer で team sheet 取得必須。GK/主力FW/CB/キャプテン確認で EV 再計算。Arsenal の Saliba/Saka/Odegaard 出場可否が最重要 | PENDING | 最高 | 4/29-30 キックオフ75分前 |
| PA044 | NHL | PA014 TBL-MTL G1 **MTL 4-3 OT 予測MISS 記録 DONE Session_44** (Slafkovsky hat trick + OT 1:22 PP). Type A A021 upset登録。CAUTION no-bet のため P&L影響なし | DONE | 高 | 完了 2026-04-20 |
| PA045 | Rule Pipeline | **R020/R017 実装 DONE Session_44** (rules_tennis.json v2.2). P013/P010 implemented_rulesへ移動。GEN005衝突解消: R017 vs R020 同時成立時はR017優先 | DONE | 中 | 完了 2026-04-20 |
| PA046 | 出力A/B | **Session_30-43 新規GO遡及追加 DONE Session_44** (multi_bets.json + dashboard同期). Leeds/Warriors/Warrington/SAS を追加。累計 11件・6HIT・3MISS・1VOID・1PENDING | DONE | 最高 | 完了 2026-04-20 |
| PA047 | upset_patterns | **A014-A020 upset_patterns.json 本体への登録漏れ補填**。BACKLOG/records には記録されているが confirmed_upsets 配列に未入力（A021 は Session_44 で追加済）| PENDING | 中 | 次セッション |

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
**Session_41 更新 (2026-04-17 GEN003実行):**
- PA014/PA015: NHL PO G1 両試合 **日付修正 4/18 → 4/19** (公式NHLスケジュール確認)
- PA035 新規: SL Warrington **Tanginoa 復帰確認** (Yahoo Sports + seriousaboutrl) → confidence 80→83, EV +32→+36.1%, records/superleague/2026.json 更新済
- PA036 新規: NRL Warriors — Titans Brimson(第二子出産)+ Randall(calf) 欠場。Titans更に弱体化。Warriors予測強化方向。
- PA034 新規: SL Leeds vs Huddersfield 試合時刻確認 (UK 4/17 19:00 = JST 4/18 04:00)
- UFL Renegades: 怪我情報なし、推奨維持
- NBA SAS: Wembanyama 100%近い、推奨維持
- ダッシュボード更新: 予測精度タブ (19/24 79.2% / Tier分離表示)、ルール変更インパクト表 (R013/U008拡張/GEN004/Tier分類/AHL復活の5行追加)、アクティブ推奨 Warringtonカード (83%/+36.1%)、AHL sport-card pending 0→27 更新

---
**Session_43 更新 (2026-04-20):**
- 過去分スコア未検証訂正: 2026-MC.json の Marozsan vs Hurkacz 「未確認」→「6-2 6-3」、SF 対戦相手 de Minaur→Vacherot (CE015波及)、QF draw_structure 訂正
- 結果確認完了: NHL COL-LAK G1 HIT / SL Warrington MISS / ATP Barcelona+Munich QF 8件 / WTA Stuttgart QF+R2残3 + Rouen QF+R2 結果反映
- 2026-04-19.json 全試合スクリーニング: NHL PO G1残+G2 全SKIP / NBA PO G1残 全SKIP / NRL R9 全SKIP / Top14 R22 全SKIP / WTA 125K+Q・ATP Challenger out-of-scope
- Rule pipeline evidence 増加: P013 3/3到達 (R020実装判断要), P010 2/2到達 (R017実装判断要), P014 1/3, P007 2/3
- SL P016候補記録: Catalans仏国ホーム補正-5%→-7%〜-10%強化検討 (evidence A020)
- cumulative/dashboard_stats/dashboard.html 全同期完了: 通算 20/28 71.4% +1.733u (Advanced 15/20 75.0% / Basic 5/8 62.5%)
- 未解決: PA014 TBL-MTL G1 (live 2-2進行中) / PA017 SAS-POR G1 (未開始) / PA041 NHL PO G1残5+G2 結果 / PA042 P013実装判断 / PA043 P010実装判断

---
**Session_42 更新 (2026-04-18 CE013発生・訂正・全体整合性検証):**
- **CE013 発生**: UFL Week4 Renegades vs Aviators の勝敗を真逆に誤報（WebSearch snippet のWeek3スコアをWeek4と誤認）。ユーザー指摘で発覚。一次ソース確認で Aviators 28-14 Renegades UPSET が正しいことを確定。
- 再発防止: feedback_result_verification.md 新規作成（memory自動ロード）。claude_error_log.md CE013詳細追記。新プロトコル: 一次ソース最低2つ+WebFetch具体boxscore確認+週番号照合+通算勝敗整合性チェック。
- PA021 DONE: Aviators 28-14 Renegades → GO MISS -1.0u (CE013訂正後)
- PA034 DONE: Leeds 56-22 Huddersfield → GO HIT +0.23u
- PA036 DONE: Warriors 28-20 Titans → GO HIT +0.23u
- P015 新規追加 rule_pipeline.json: UFL expansion team home rematch after narrow road loss パターン (A016として evidence 1件記録)
- records/ufl・nrl・superleague、cumulative.json、dashboard_stats.json 全更新
- dashboard.html: sync_sport_cards.py 実行で sport cards 再生成、overview big-stat 自動更新、アクティブ推奨から完了3件削除、履歴テーブル3件 PENDING→HIT/MISS更新、stale PENDING 4件 (Louisville/Musetti R2/Tan-Bondar) も訂正、高確率予想 rank3 Renegades MISS反映、マルチベット 全5コンボ LOSE確定 (P&L -5.0u)
- Tan/Bondar note typo修正: cumulative.json で "Tan d. Bondar" → "Bondar d. Tan 6-2 4-6 6-0"
- 通算: 21/27 (77.8%) +3.52u (Phase2移行直後の初期値更新)

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
