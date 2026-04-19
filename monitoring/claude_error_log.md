# Claude自身のエラー記録ログ

> **Claude Codeへの指示：**
> - このファイルはClaudeが犯したミス・間違いを記録するためのファイル
> - セッション開始時に必ず読み込み、同種のミスを繰り返さないよう注意する
> - ミスが発覚した時点で即座に追記する（対応完了を待たない）
> - カテゴリ別にパターンを把握して、応答前の自己チェックに活用する

---

## ステータス凡例
- `ACTIVE` — 再発リスクあり（常に注意）
- `MITIGATED` — ルール/仕組みで対策済み（ただし念のため意識を維持）
- `RESOLVED` — 完全解決・再発なし

---

## カテゴリ分類
| カテゴリ | 説明 |
|---|---|
| DATA_ERROR | スコア・スタッツ・数値の誤り |
| INCOMPLETE | 作業未完了なのに完了と報告 |
| ENCODING | ファイルのエンコーディング問題 |
| FABRICATION | 未確認情報を確認済みとして記述 |
| ANALYSIS | 分析ロジック・判断の誤り |
| PROCESS | 手順の省略・順序ミス |

---

## エラーログ

| ID | 日付 | カテゴリ | 概要 | ステータス |
|---|---|---|---|---|
| CE001 | 2026-04-15 | DATA_ERROR | Cerundolo vs Machac スコア誤記 | MITIGATED |
| CE002 | 2026-04-15 | DATA_ERROR | Louisville Kings 勝敗記述逆転 | MITIGATED |
| CE003 | 2026-04-15 | INCOMPLETE | miss_analysis 空のまま「完了」報告 | MITIGATED |
| CE004 | 2026-04-15 | ENCODING | Windows JSON のutf-8-sig未対応 | MITIGATED |
| CE005 | 2026-04-13〜 | FABRICATION | 推論値を「確認済み」として記述 | ACTIVE |
| CE006 | 2026-04-16 | DATA_ERROR | WTA Stuttgart Korpatsch/Shnaider 結果誤入力（実: Shnaider勝利） | MITIGATED |
| CE007 | 2026-04-16 | DATA_ERROR | ATP Munich Nagal/Cerundolo 結果誤入力（実: Cerundolo勝利） | MITIGATED |
| CE008 | 2026-04-16 | DATA_ERROR | WTA Stuttgart screening_log結果誤入力2件（Samsonova勝利→Ruzic誤記 / Zhang/Noskova未完了→Zhang WIN誤記） | MITIGATED |
| CE009 | 2026-04-16 | DATA_ERROR | WTA Stuttgart Eala/Fernandez 結果誤入力（実: Fernandez Q 6-1 6-4 勝利） | MITIGATED |
| CE011 | 2026-04-17 | PROCESS | Munich QF予測をR2ラベルで誤登録（組合せ自体はQF対戦として偶然正しかった）。ラベル修正で対応 | MITIGATED |
| CE012 | 2026-04-17 | ANALYSIS | Norrie vs Quinn R2 の predicted_winner=Quinn は明確な誤記（実際はNorrie GS決勝経験者が本命） | ACTIVE |
| CE013 | 2026-04-18 | DATA_ERROR | UFL Week4 Renegades vs Aviators の勝敗を真逆に報告（実: Aviators 28-14 勝利）。Week3スコアをWeek4と誤認 + WebSearch snippet依存 + 一次ソース未確認 | MITIGATED |
| CE014 | 2026-04-18 | DATA_ERROR | 【遡及発覚】GB001 Ostapenko vs Andreeva Stuttgart R1 (2026-04-13) を HIT として記録していたが、実際は Andreeva 5-7 6-2 6-4 で Ostapenko 敗北 (MISS -0.25u)。約1週間誤データでダッシュボード表示 | MITIGATED |
| CE015 | 2026-04-18 | DATA_ERROR | 【遡及発覚】MC2026 SF Alcaraz vs de Minaur と記録していたが、de Minaur は QF で Vacherot に敗退。実際の SF は Alcaraz vs Vacherot 6-4 6-4。対戦相手記載誤り + スコア"確認中"のまま未検証 | MITIGATED |

---

## 詳細記録

### CE001 — Cerundolo vs Machac スコア誤記
**日付:** 2026-04-15（Session_30）  
**カテゴリ:** DATA_ERROR  
**ステータス:** MITIGATED  

**何を間違えたか:**  
2026-ATP.jsonに Cerundolo vs Machac のスコアを「6-2 7-6(3)」と記録したが、正しいスコアは「7-6(2) 6-3」（セット順も点数も両方誤り）。

**どう発覚したか:**  
miss_analysis深掘り調査のためWebSearch実施時に、puntodebreak/ATP公式記事の記述と記録値が食い違うことで判明。

**なぜ発生したか:**  
スコアを一次ソースで確認せず、セッション内の会話記憶または推定で記録した。

**再発防止ルール:**  
→ スコア・数値を records JSON に書き込む前に必ずATP Tour公式サイト/Flashscore等の一次ソースで確認する。  
→ 「たぶんこのスコアだったはず」という記録は絶対にしない。未確認なら「result: null」のまま残す。

---

### CE002 — Louisville Kings 勝敗記述逆転
**日付:** 2026-04-15（Session_30）  
**カテゴリ:** DATA_ERROR  
**ステータス:** MITIGATED  

**何を間違えたか:**  
multi_bets.jsonの推薦理由テキストに「Louisville 3-0 vs Gamblers 0-3」と記述したが、実際はLouisville 0-3でGamblers 1-2（勝敗記録が逆転していた）。

**どう発覚したか:**  
ユーザーがmulti_bets.jsonを確認した際に指摘。

**なぜ発生したか:**  
推奨理由の文章を records JSONから直接引用せず、記憶で記述した。

**再発防止ルール:**  
→ チームの勝敗記録・順位・スタッツは必ず records JSON または一次ソースから直接引用する。  
→ 文章中に「X-Y」形式の数値を書くときは、直前に元データを参照していることを確認する。

---

### CE003 — miss_analysis 空のまま「完了」報告
**日付:** 2026-04-15（Session_30）  
**カテゴリ:** INCOMPLETE  
**ステータス:** MITIGATED  

**何を間違えたか:**  
ATP GO MISS 3件（Medvedev/Berrettini、Cerundolo/Machac、Berrettini/Fonseca）について、miss_analysisフィールドが空のまま「外れ分析済み」として報告した。ユーザーに「外れたものの分析は終わっていますか？」と確認されて発覚。

**どう発覚したか:**  
ユーザーから明示的に確認を求められ、records JSONを実際に読んだ時点でフィールドが空であることが判明。

**なぜ発生したか:**  
「分析内容を考えた/方針を決めた」という認知を「records JSONに書き込んだ」と混同した。実際の書き込み確認をせず完了宣言した。

**再発防止ルール:**  
→ 「分析完了」「記録完了」と報告する前に、必ず対象フィールドがJSON内に存在することをコードで確認する（python -c で読み込んでprintする）。  
→ 「考えた」と「書いた」は別。書いた事実を確認してから完了報告する。

---

### CE004 — Windows JSON の utf-8-sig 未対応
**日付:** 2026-04-15（Session_30）  
**カテゴリ:** ENCODING  
**ステータス:** MITIGATED  

**何を間違えたか:**  
NHLなど複数のJSONファイルを `encoding="utf-8"` で読み込もうとして `json.decoder.JSONDecodeError: Unexpected UTF-8 BOM` エラーが発生。

**どう発覚したか:**  
スクリプト実行時のエラーメッセージで即座に判明。

**なぜ発生したか:**  
このプロジェクトのJSONファイルはWindowsのメモ帳等で作成されたものがあり、UTF-8 BOM付きで保存されている。`utf-8`では読めない。

**再発防止ルール:**  
→ このプロジェクト内の全JSONファイルの読み込みは `encoding="utf-8-sig"` を使う（BOMありでもなしでも対応可）。  
→ 書き込みは `encoding="utf-8"`（BOMなしで統一）。  
→ 新しいスクリプトを書くときは冒頭に必ず `utf-8-sig` を指定する。

---

### CE005 — 推論値・未確認情報を「確認済み」として記述
**日付:** 2026-04-13〜（複数セッション）  
**カテゴリ:** FABRICATION  
**ステータス:** ACTIVE（継続注意）  

**何を間違えたか:**  
選手の出場状況・試合スタッツ・チーム成績等について、WebSearch/WebFetchで確認していないにもかかわらず「確認済み」「〜が出場」「スコアは〜」と具体的な記述をした。ユーザーから「推測した数字は使わず、データとして存在しているものを正しく利用してください」と複数回指摘を受けた。

**どう発覚したか:**  
ユーザーからの指摘（「繰り返しですが推測した数字は使わず」という表現から、複数回発生していたことが明確）。

**なぜ発生したか:**  
知識カットオフ内の情報を「知っている」と判断して検索を省略した。または、文脈から推定できると判断して実際の確認を省いた。

**再発防止ルール:**  
→ 選手名・スコア・スタッツ・出場情報・怪我情報は**必ずWebSearch/WebFetchで確認してから**記述する。  
→ 「知ってる気がする」は「知らない」と同義。必ず検索する。  
→ 確認できなかった情報は `"未確認"` / `null` / `「[要確認]」` と明記する。  
→ 「例として」「イメージとして」という理由での具体値生成は絶対禁止。

---

## 自己チェックチェックリスト（応答前に必ず確認）

このリストはCE001〜CE005の再発防止を念頭に置いたチェック項目。

- [ ] **スコア・数値を記録する場合**: 一次ソース（ATP Tour/Flashscore/ESPN等）で確認済みか？
- [ ] **「〜が完了した」と報告する場合**: 実際にファイル内のフィールドをコードで確認したか？
- [ ] **JSON読み込みスクリプトを書く場合**: `encoding="utf-8-sig"` を使っているか？
- [ ] **チームの成績・勝敗を書く場合**: records JSONまたは一次ソースから直接参照しているか？
- [ ] **試合関連の具体的情報**: WebSearch/WebFetchで今セッション内に確認した情報のみを使っているか？
---

### CE006 — WTA Stuttgart R1 Korpatsch/Shnaider 結果誤入力
**日付:** 2026-04-16（Session_31）  
**カテゴリ:** DATA_ERROR  
**ステータス:** MITIGATED  

**何を間違えたか:**  
WTA Stuttgart R1 Shnaider vs Korpatsch の結果を「Korpatsch d. Shnaider (UPSET 4.70)」と記録したが、実際はShnaider（本命1.16/1.19）が6-3 6-1で勝利。WTA公式「Shnaider outduels home favorite Korpatsch」が正しい。アップセットは発生していなかった。

**どう発覚したか:**  
Type A アップセット分析フレームワーク構築後に、過去スクリーニング済み試合を全点検。WebSearch（WTA公式URL）で一次確認して誤入力が判明。

**なぜ発生したか:**  
結果を一次ソース確認せず、セッション内のデータや記憶から記録した。Korpatsch(4.70)という高オッズを見て「これが勝ったはず」と誤認したか、または別試合の結果と混同した可能性。

**修正内容:**  
→ records/wta/2026.json: Shnaider d. Korpatsch 6-3 6-1 に修正  
→ r1_upset_analysis.upsets_by_odds: 2 → 1  
→ stats/upset_patterns.json: notable_upsets からKorpatsch削除、key_insight修正  

**再発防止:**  
→ スコア・結果記録前に必ず一次ソース（WTA公式/Flashscore等）確認。高オッズ選手の勝利はより慎重に確認する。

---

### CE007 — ATP Munich R1 Nagal/Cerundolo 結果誤入力
**日付:** 2026-04-16（Session_31）  
**カテゴリ:** DATA_ERROR  
**ステータス:** MITIGATED  

**何を間違えたか:**  
ATP Munich R1 Cerundolo(5) vs Nagal(LL) の結果を「Nagal d. Cerundolo(5) HUGE UPSET @9.4」と記録したが、実際はCerundolo（本命1.05）が6-2 6-2で80分の快勝。Indian Tennis Daily「Cerundolo Cruises Past Nagal」、ATP Tour公式で確認。

**どう発覚したか:**  
Type A アップセット分析時にWebSearchで確認。Cerundolo勝利が明確に判明した。

**なぜ発生したか:**  
結果を一次ソース確認せず記録した（CE005のパターンと同種）。Nagalのオッズ9.4という高倍率が目に入り「アップセットが起きた」と誤認したか、または異なる試合の結果と混同。

**修正内容:**  
→ records/tennis/2026-ATP.json: Cerundolo F. 6-2 6-2 に修正  
→ outcome_note更新（「HUGE UPSET」削除）

**再発防止:**  
→ 結果記録時は必ずWebSearch実施。オッズだけ見て結果を推定することは絶対禁止。CE005の指示を徹底。
---

### CE008 — WTA Stuttgart R1 screening_log 結果誤入力2件
**日付:** 2026-04-16（Session_31）  
**カテゴリ:** DATA_ERROR  
**ステータス:** MITIGATED  

**何を間違えたか:**  
1. `Samsonova vs Ruzic`: screening_logに「Ruzic WIN(UPSET 2.95)」と記録。実際はSamsonova 6-0 6-4で圧勝（predictions予測エントリは正しかった）。  
2. `Zhang vs Noskova`: screening_logに「Zhang WIN(UPSET 5.20)」と記録。試合はまだサスペンド中（4/16時点: Zhang 7-5 / Noskova 6-4 / 第3セット中断）。まだ結果が出ていない。

**なぜ発生したか:**  
同セッション内で結果バッチ更新した際、一次確認なしに記録した。Ruzicは「アップセット候補」と思い込んでいたか、他試合と混同。Zhang/Noskovaは試合途中の進捗情報を「最終結果」として誤記録した。

**修正内容:**  
→ Samsonova/Ruzic: 「Samsonova WIN 6-0 6-4 (SKIP正解)」に修正  
→ Zhang/Noskova: 「SUSPENDED 未完了」に修正（試合完了後に再更新要）
---

### CE009 — WTA Stuttgart Eala/Fernandez 結果誤入力
**日付:** 2026-04-16（Session_31）  
**カテゴリ:** DATA_ERROR  
**ステータス:** MITIGATED  

**何を間違えたか:**  
WTA Stuttgart R1 Fernandez(Q) vs Eala の結果を「Eala d. Fernandez (UPSET 2.39)」と記録。実際はFernandez（本命1.54/1.66、Q）が6-1 6-4で圧勝（WTA公式・ESPN・TSN・Rappler等複数ソース確認）。アップセットではなく予測通りの結果だった。

**どう発覚したか:**  
Type A アップセット分析フレームワークで過去記録を全点検。WTA公式WebFetch + WebSearchで複数ソース確認。

**修正内容:**  
→ predictions entry: Fernandez d. Eala 6-1 6-4 に修正  
→ r1_upset_analysis.upset_list: Eala → Lys/Badosa に差し替え  
→ upset_patterns.json: Eala エントリ削除  

**Stuttgart R1 真の状況（修正後）:**  
確認済みアップセット = 1件のみ（Lys d. Badosa 2-6 7-5 6-4）。残り全試合は本命勝利または誤入力だった。

---

### CE010 — ATP Munich Bublik vs Hurkacz phantom entry（casino data誤り）
**日付:** 2026-04-16（Session_35）  
**カテゴリ:** DATA_ERROR  
**ステータス:** MITIGATED  

**何を間違えたか:**  
Casino dataに「Bublik A.(3) vs Hurkacz H.」というMunich R1エントリーが存在したため、そのままrecordsに記録した。しかし実際にはHurkaczが棄権（またはdraw変更）しており、この試合は開催されなかった。  
実際のBublikのMunich R1相手はMolcan A.（6-4 6-2でMolcan勝利）で、別エントリー「Molcan A. vs Bublik A.(3)」が正しく存在している。  

**どう発覚したか:**  
Type A調査フェーズで「Bublik vs Hurkaczの結果が記録されていない」ことを調査中、puntodebreak.com「Molcan surprises Bublik in his ATP Munich debut」記事＋WebSearch結果から実際の対戦相手がMolcanであることを確認。  

**修正内容:**  
→ 「Bublik A.(3) vs Hurkacz H.」entry: tier="invalid", ce_error="CE010", invalidation_note追加  
→ 「Molcan A. vs Bublik A.(3)」entry: predicted_winner/prediction_confidence/prediction_hit/type_a_upset_id(A012)追加  
→ upset_patterns.json: A012(Molcan d. Bublik 6-4 6-2, CAUTION verdict correct)追加  

**再発防止策:**  
Casino dataのエントリーが実際の試合と一致するか、大会ドローと照合するステップを設ける。特にseededプレイヤーの対戦相手は変更（棄権・LL置き換え等）が起こりやすい。

### CE011 — R2予測エントリ作成時のドロー構造未照合（Munich R2）
**日付:** 2026-04-17（Session_39）
**カテゴリ:** PROCESS / DATA_ERROR
**ステータス:** MITIGATED

**何を間違えたか:**
Munich QF予測エントリを誤って "R2" ラベルで登録した。
- [58] "Cobolli F. vs Kopriva V." — 実際のR2は Cobolli d. Bergs / Kopriva d. Darderi。**QFで対戦組合せと偶然一致**（4/17 QF: Cobolli vs Kopriva）。
- [59] "Fonseca J. vs Shelton B." — 実際のR2は Fonseca d. Rinderknech / Shelton d. Blockx。**QFで対戦組合せと偶然一致**（4/17 QF: Fonseca vs Shelton）。

つまり組合せ自体は将来QFで実現した正しい対戦だったが、ラウンドラベルを誤っていた。完全な誤組合せではなく "ラウンド齟齬"。

**どう発覚したか:**
Session_39 で「結果が出た試合の分析」中、WebSearchでMunich R2結果を取得した際に、記録した対戦カードと実際のR2マッチアップが一致しないことが判明。ATPドロー構造を照合して正誤を特定。

**なぜ発生したか:**
R2予測を「R1の両勝者候補を掛け合わせて推定」した。実際にはATPドローのセクション構造（上半分・下半分・クォーター区分）により、R1勝者の対戦相手は固定されている。ドロー未照合で組合せを仮定したのが根本原因。

**修正内容:**
- [58][59] をinvalid化→ユーザー指摘で再検証→**QF組合せと偶然一致していたため、round="R2"→"QF"に修正、tier="pending_screening"で復活**
- [58] Cobolli vs Kopriva / [59] Fonseca vs Shelton をQFエントリとして活用
- 真のR2 5試合をretroactiveエントリとして別途追加（Cobolli/Bergs, Fonseca/Rinderknech, Shelton/Blockx, Cerundolo/VdZ, Darderi/Kopriva）
- Munich QF 残り2試合 (Zverev/Cerundolo, Shapovalov/Molcan) を新規登録・スクリーニング実施

**再発防止ルール:**
→ 次ラウンド予測エントリを作成する前に、**必ずATPドロー/WTAドロー公式で対戦組合せと該当ラウンドを照合する**
→ ラウンドラベル（R1/R2/R3/R16/QF/SF/F）を確定するため、ドロー構造（上半分/下半分/クォーター区分）を確認
→ ドロー未確定のラウンドについて予測エントリを作成する場合は、対戦組合せが「本当にそのラウンドで成立するか」を必ず検証
→ 万が一ラベル誤りが発見された場合、組合せ自体が別ラウンドで偶然正しい可能性もあるため、invalidate前に再検証する

### CE012 — Norrie vs Quinn R2 の predicted_winner 誤記
**日付:** 2026-04-17（Session_39）
**カテゴリ:** ANALYSIS
**ステータス:** ACTIVE（再発防止ルール必要）

**何を間違えたか:**
Barcelona R2 Norrie vs Quinn の predicted_winner を "Quinn E." と記録。実際はNorrieが6-3 4-6 6-4で勝利。
- Norrie: #54、ATP Masters 1000 Indian Wells champ (2022)、Roland Garros 4R (2022)、GS決勝経験（US Open SF）
- Quinn: #120台、クオリファイアー、ATP実績少
- cElo差・実績・クレー経験すべてNorrie圧倒的優位

**どう発覚したか:**
MISS深掘り調査中（WebSearch）、Norrieの実績・ランキングがQuinn予測と不整合と判明。

**なぜ発生したか (推定):**
- スクリーニング時の predicted_winner 記入ミス
- またはR1 Norrie-Wawrinka 3セット消耗情報に引きずられ、Quinn (fresh) を過大視
- または記憶違い / data 転写ミス

**修正内容:**
- miss_analysis に誤記原因と正しい評価を記録
- miss_layer = PREDICTION_LOGIC_ERROR

**再発防止ルール（新規）:**
→ **predicted_winner 記入前self-check**: (1) 両者のATPランキング確認 (2) クレー直近勝率確認 (3) cElo差の方向性確認 (4) 記入した predicted_winner がL1優位側と一致するか検証
→ SKIP予測であっても predicted_winner の選択は L1 cElo評価に忠実に従う
→ 「R1消耗」を理由に本命を外す場合は、明確な根拠 (セット数・試合時間・怪我情報) を prediction_basis に明記する
→ 一致しない場合は prediction_basis に「逆選択理由」を書く義務（例: "cElo優位のNorrieではなくQuinn予測の理由: R1消耗 + XXX"）

**今後の記入時チェックリスト (self-check):**
- [ ] predicted_winner は cElo/ランキング優位側か？
- [ ] 優位側を選ばない場合、prediction_basis に明確な理由を記載したか？
- [ ] L1指標値 (cElo差) を prediction_basis に含めたか？

---

### CE013 — UFL Week4 Renegades vs Aviators 勝敗真逆報告
**日付:** 2026-04-18（Session_42）
**カテゴリ:** DATA_ERROR（CE005 FABRICATION系の再発）
**ステータス:** MITIGATED

**何を間違えたか:**
UFL Week4 Columbus Aviators @ Arlington Renegades (4/17 開催) の結果について、最初のWebSearch snippetに「Dallas (3-0) edged Columbus (0-3) 28-23」という記述があったため、それをWeek 4の結果と誤認してユーザーに「Renegades 28-23 Aviators HIT」と報告した。実際はそれはWeek 3のスコアで、Week 4は**Aviators 28-14 Renegades**（expansion チームのUPSET勝利）が正しい結果。Renegades GO @1.36 は **MISS -1.0u** が真実。

**どう発覚したか:**
ユーザーから「外しているはず」と指摘され、再確認のためESPN scoreboard をWebFetchしたところ「Aviators (1-3) 28, Renegades (3-1) 14」と明確に表示され、勝敗が真逆だったことが判明。

**なぜ発生したか:**
1. **一次ソースを最初に当たらなかった**: ESPN scoreboard / UFL公式 / 大会 boxscore を最初から参照せず、WebSearch のAI要約snippetで済ませた
2. **Week3とWeek4の混同**: 同じ対戦カードのWeek3結果(28-23)をWeek4のものと読み違えた
3. **通算成績との論理整合性チェックを怠った**: 「Renegades 3-1 / Aviators 1-3」という通算勝敗が出ていれば、Week4でRenegadesが敗れたことは自明だった
4. **複数ソースでの相互検証なし**: 1つのsnippet情報だけで確定扱いした

**重大性:**
勝敗情報の真逆報告は、ベット判断システムにおいて最悪クラスの誤り。ユーザーの信頼・累積統計・EV計算・ルール追加判断の全てに波及する。CE005（FABRICATION）の再発パターンとして深刻。

**再発防止ルール（最重要・即時発効）:**

**【勝敗・スコア確認 新プロトコル】**
records/{sport}/*.json に結果を書き込む前に、以下を必ず実施する：

1. **一次ソースを最低2つ参照**
   - 優先順位: ①大会公式サイト（NHL.com gamecenter / ATP Tour / WTA.com / nrl.com / theufl.com / NBA.com 等） ②ESPN scoreboard or boxscore ③Flashscore or sofascore
   - WebSearch snippet **だけ** での勝敗確定は禁止。必ず WebFetch で具体ページを開いて「X 28, Y 14」のような明示スコアを確認する

2. **日付・ラウンド・週番号の一致確認**
   - 参照しているスコアが「問い合わせ試合日」と合致していることを確認
   - 特に連戦・リマッチ試合では「Week 3 結果」と「Week 4 結果」を混同しないよう週番号を必ず照合
   - 「Live Score」「Preview」「Recap」などページ種別も確認（試合前プレビュー記事を結果と誤認しない）

3. **通算成績との論理整合性チェック**
   - 勝敗記録（3-0→3-1 / 0-3→1-3 等）は試合結果の論理的証拠
   - 通算勝敗が更新されていれば、どちらが直近勝ったかが逆算できる
   - snippet内の通算記録と「勝利者」の主張が矛盾する場合は必ず再検証

4. **「defeated」「edged」「held off」等の表現と具体スコアの対応を厳密に読む**
   - 「A defeated B, score 28-14」を「A 28, B 14」と解釈するのはOK
   - ただし記事が複数試合を報告している場合、どの試合のスコアか必ず明示されていることを確認
   - 疑わしい場合は WebFetch で直接 boxscore を取得

5. **自己疑義の発動**
   - 「アップセット濃厚だった試合で本命が勝った」「高オッズ側が勝った」といった驚きの結果は特に慎重に確認
   - ユーザーが「本当にそう？」と疑問を呈した時点で、推測せず即座に一次ソース再確認

**再発防止：自己チェック追加項目（応答前必須）:**
- [ ] 勝敗を記述する前に、一次ソース2つ以上で確認したか？
- [ ] WebFetch で boxscore/gamecenter を開き、明示スコアを確認したか？
- [ ] 参照記事の試合日・週番号が対象試合と一致するか？
- [ ] 通算勝敗記録と「誰が勝ったか」の論理整合性が取れているか？

---

### CE014 — GB001 Ostapenko HIT → 実は MISS（遡及発覚）
**日付:** 2026-04-18 発覚（元データ入力: 2026-04-13）
**カテゴリ:** DATA_ERROR（CE013 と同じ勝敗真逆パターン）
**ステータス:** MITIGATED

**何を間違えたか:**
WTA Stuttgart R1 (2026-04-13) GB001 Ostapenko vs Andreeva について、"Ostapenko d. Andreeva" として記録、hit=true、actual_ev=+0.5375u で約1週間ダッシュボード表示されていた。実際は **Andreeva 5-7 6-2 6-4 で Ostapenko 敗北**。Andreeva が defending champion Ostapenko を dethrone した試合。

**どう発覚したか:**
CE013 訂正後、Session_42 で全確定 GO エントリを再検証していた際、WebSearch で Stuttgart R1 結果を確認したところ「Andreeva dethrones defending champ Ostapenko」の複数ソース記事を発見。records の "Ostapenko d. Andreeva" と矛盾。

**なぜ発生したか:**
- 試合結果をセッション内推定で記録し、一次ソース確認を省略（CE005と同根本原因）
- GAMBLE_BET 枠の特殊推奨だったため、「Ostapenko 側をプレイした = Ostapenko 勝利」と無意識に混同？
- 約1週間チェックされず残存

**修正内容:**
- records/wta/2026.json GB001 entry: hit=false, result=Andreeva d. Ostapenko, score=5-7 6-2 6-4, actual_ev=-0.25
- summary: hit 2→1, hit_rate 0.667→0.333, ev_total -0.2525→-1.04
- 検証ソース記録: WTA Official + Sofascore + Tennis Tonic 複数
- cumulative.json WTA 再計算 (追加更新要)

**重大性:**
- 約1週間、システム統計が誤表示されていた (正答率を過大評価)
- CE013 と同一パターン (結果の真逆記録) が発覚 → 過去分全件再検証の必要性が確定

---

### CE015 — MC2026 SF 対戦相手誤記（de Minaur → Vacherot）
**日付:** 2026-04-18 発覚（元データ入力: 2026-04-11）
**カテゴリ:** DATA_ERROR（対戦組合せ未検証）
**ステータス:** MITIGATED

**何を間違えたか:**
MC2026 SF で "Alcaraz C.(1) vs de Minaur A.(5)" として記録し、スコアは "確認中"（未検証）のまま hit=true として累計統計に入っていた。実際は de Minaur は QF で Vacherot(WC) に敗退しており、SF対戦相手は **Vacherot**。Alcaraz 6-4 6-4 Vacherot（84分）。

**どう発覚したか:**
Session_42 CE013/CE014 後の過去エントリ再検証中、WebSearch で「Alcaraz de Minaur MC2026 SF」検索に対して「de Minaur は Vacherot に QF で敗退」という複数情報源の記述を発見。records の QF entry (line 303-309) でも "de Minaur(5) vs Vacherot(WC) Vacherot V. 6-4 3-6 6-3" が記録されており、論理矛盾が明白だった。

**なぜ発生したか:**
- SF対戦組合せを draw sheet で確認せず、シード通り (#1 vs #5) と仮定して記録
- スコア "確認中" のまま修正を怠った（CE003 "未完了を完了と報告" の類型）
- QF の Vacherot 勝利情報は記録されていたが、SF の組合せ生成時に参照していなかった

**修正内容:**
- records/tennis/2026-ATP.json SF entry: match="Alcaraz C.(1) vs Vacherot V.(WC)"、score="6-4 6-4"、verification_sources 追加
- hit=true は維持（Alcaraz は予測通り勝利）

**再発防止ルール:**
→ トーナメント各ラウンドの対戦組合せは draw sheet / 前ラウンド結果から必ず確認する
→ スコア "確認中" "TBD" "未確認" のままのエントリを定期的に scan して解消する（grep自動化検討）
→ 前ラウンドの結果を参照するとトーナメント logical consistency が validation 可能
