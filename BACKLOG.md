# BACKLOG — 依頼・要望トラッキング

> **Claude Codeへの指示：**
> - セッション開始時に必ずこのファイルを読む
> - 依頼を受けたら実行前にここに書き込む
> - 完了したら `[ ]` → `[x]` に更新する
> - 「作業中」の項目は前回セッションで途中になったもの

---

## ステータス凡例
- `[ ]` 未着手
- `[~]` 作業中（前回セッションで途切れた可能性あり）
- `[x]` 完了
- `[-]` 保留・キャンセル

---

## 未完了・作業中（次回セッション最優先）

- [ ] UFL Week3 Dallas vs Columbus 結果確認・記録（4/13 正午ET試合後）← Dallas GO EV+8.2% 信頼度82%
- [ ] MC2026 F Alcaraz vs Sinner 結果確認（4/13試合後）← SKIP（ベットなし・観戦のみ）
- [~] WTA Stuttgart 初回分析（開幕4/13）← Shnaider vs Korpatsch・Andreeva vs Ostapenko を tennisabstract cElo確認後GO判断
- [ ] NHL 4/12-4/13 ゲーム確認・スクリーニング（プレーオフ準備期間の可能性）

---

## 直近完了（4/12 自動分析 10:36 JST実行）

- [x] STEP1: BACKLOG読込・pending ゲーム特定（UFL Dallas, MC F SKIP, WTA Stuttgart）
- [x] STEP2-A: 結果検証（4/13前なので pending のまま）
- [x] STEP5: 次24時間ゲーム検索（NHL/UFL/WTA確認済）
- [x] STEP6: L1スクリーニング（4/13朝実施予定）
- [x] STEP7: ダッシュボード時刻更新（10:36 JST / 次回 22:36 JST）
- [x] STEP8: BACKLOG更新

## 直近完了（4/12 手動自動分析代替）

- [x] MC2026 SF誤記録修正: Sinner vs Zverev → Sinner HIT 6-1 6-4（MISS→HIT, +1.65u delta）
- [x] MC2026 F対戦更新: Alcaraz vs Sinner（4/13）SKIP（cElo差~20pt L1未達）
- [x] NBA 4/12: Rockets 124-109 HIT(+0.20u) / Cavaliers 130-126 SKIP
- [x] upset_patterns.json U004削除（誤記録: SFはSinner HIT、upset未発生）
- [x] cumulative.json更新（通算73.3% 11/15、累積EV+2.133u）
- [x] WTA Stuttgart スクリーニング記録（Shnaider/Andreeva等 cElo確認要）
- [x] dashboard.html全数値更新

## 直近完了（4/11 夜間自動分析）

- [x] NHL OTT @ NYI 結果確認・記録（Ottawa 3-2 HIT / Tkachuk残り13秒決勝点）
- [x] Super Rugby R9 Reds vs Crusaders 結果確認（Crusaders 32-12 HIT / ホームSF確定）
- [x] cumulative.json・dashboard.html更新（通算64.3% 9/14、累積EV+0.283）
- [x] 日次レポート出力（2026-04-11.md）

## 直近完了（4/11 本日）

- [x] MC2026 SF 結果確認・記録（Alcaraz HIT +0.50 / Zverev over Sinner MISS -1.00）
- [x] ダッシュボード全数値更新（通算63.6% 7/11、EV -0.787）
- [x] upset_patterns.json 新設（全8種目対応、U001〜U004記録済）
- [x] ダッシュボードに「🎯 アップセット分析」タブ追加
- [x] 3段階フレームワーク定義（Phase1→2→3）・メモリ保存
- [x] ダッシュボードモバイル対応CSS強化

---

## 今後の予定（時期が決まっているもの）

- [ ] WTA Stuttgart 開幕（2026-04-13）
- [ ] UFL Week3 結果（2026-04-13以降）
- [ ] NHL プレーオフ開始後の分析継続
- [ ] CFL 2026シーズン開幕対応（2026年6月）
- [ ] NFL 2026-27シーズン開幕対応（2026年9月）

---

## 設計方針メモ（次回Claude Codeへ）

- **3段階フレームワーク**: Phase1（強い側確認）→ Phase2（逆転条件特定）→ Phase3（勝者予測）
- **MISSが出たら必ず** `stats/upset_patterns.json` にU00x IDで追記（UF分類）
- **GAMBLE_BET枠**: 実力差ボーダー＋UF2つ以上＋高オッズで別stake発動（通常の1/3以下）
- **R001閾値見直し検討中**: cElo差＜130pt → CAUTION格下げ（U002・U003・U004の3件が根拠）

---

*このファイルはClaude Codeセッションをまたぐ「引き継ぎノート」です。*
*依頼が途切れた場合も、次のセッションで未完了項目から再開できます。*
