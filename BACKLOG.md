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

- [x] MC2026 F予測・実施（4/12 Alcaraz vs Zverev）← Alcaraz go 信頼度82% EV+18.9% 記録済
- [ ] MC2026 F 結果確認・記録（4/12試合後）
- [x] NRL Round 6 Rabbitohs vs Raiders 結果確認・記録 ← Raiders 30-22勝利 → MISS（cumulative更新済）
- [x] Super Rugby R9 Reds vs Crusaders 再評価 ← ラインナップ確認→GO（Crusaders 1.54 EV+17%）記録済
- [x] Super Rugby R9 結果確認・記録（Crusaders 32-12 Reds HIT / Hurricanes 52-14 Blues 予測なし）
- [x] NHL OTT @ NYI 結果確認・記録（Ottawa Senators 3-2 NYI HIT +1.53）
- [ ] UFL Week3 Dallas vs Columbus 結果確認・記録（4/13試合後）
- [x] NBA 4/12最終日 分析完了 ← Rockets CONDITIONAL GO（-500/1.20 EV+5.6%）B008確認後確定。Cavaliers PENDING_ODDS（オッズ-500以内+Mitchell ACTIVEでGO候補）
- [ ] MC2026 F 結果確認・記録（4/12試合後）
- [~] WTA Stuttgart ドロー確認・分析（開幕4/13）← ドロー4/11公開。cElo差80pt以上のマッチアップ抽出要

---

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
