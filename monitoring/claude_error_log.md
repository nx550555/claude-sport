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
