# ベッティング分析システム — Claude Code 引き継ぎファイル

このファイルはセッション開始時に最初に読み込むエントリポイントです。
細則はすべて `archive/CLAUDE_full_20260430.md` に退避済み。必要時のみ参照すること。

---

## このシステムの価値観

### 目的
市場（オッズ・大衆予想）とは独立して、根拠を持って正しい勝者を予測できるシステムを育てること。

### 予測とベットは別物
- **予測**: 全試合を対象に勝者を予測する。外れても問題ない。外れた理由が検証の源泉になる
- **ベット推奨**: 予測の中で **信頼度≥75% AND EV>+5%** を満たした試合のみ
- **EV閾値はベットするかどうかの基準であり、予測するかどうかの基準ではない**

### MISSの扱い
MISSは損失ではなく学習の機会。`miss_analysis` に「なぜ実際の勝者がモデル予測を上回ったか」を書き、知見を `rules_{sport}.json` に追記する。

---

## 【絶対禁止】架空情報の生成

選手名・チーム名・スコア・オッズ・怪我・出場情報など、架空の具体的情報を生成することは絶対禁止。

- 実際に検索・確認した情報 → そのまま具体的に記載
- サンプル例を示す場合 → 必ず「【サンプル】」と明記し、`[選手名]` 等のプレースホルダーを使う
- 確認していない情報 → 「未確認」と書く
- 不明な情報 → 「不明」と書く

ベット判断に直結するため、架空情報は実害につながる。

---

## セッション開始時の手順

1. `BACKLOG.md` を読み込む（`[~]` 作業中があれば「前回途中」と報告）
2. `monitoring/pending_actions.md` を読み込む（PENDING/WAITING/IN_PROGRESS を一覧報告）
3. 「引き継ぎ完了」と報告して指示を待つ

---

## 各スポーツの作業時に読むファイル

| 種目 | ルールファイル | 記録ファイル |
|---|---|---|
| ATPテニス | `core/rules_tennis.json` | `records/tennis/2026-ATP.json` |
| WTAテニス | `core/rules_wta.json` | `records/wta/2026.json` |
| NHL | `core/rules_nhl.json` | `records/nhl/2025-26.json` |
| NBA | `core/rules_nba.json` | `records/nba/2025-26.json` |
| UFL | `core/rules_ufl.json` | `records/ufl/2026.json` |
| NFL | `core/rules_nfl.json` | `records/nfl/2026-27.json` |
| CFL | `core/rules_cfl.json` | `records/cfl/2026.json` |
| NRL | `core/rules_nrl.json` | `records/nrl/2026.json` |
| Super Rugby | `core/rules_superrugby.json` | `records/superrugby/2026.json` |
| Premiership | `core/rules_premiership.json` | `records/premiership/2026.json` |
| Top 14 | `core/rules_top14.json` | `records/top14/2026.json` |
| Pro D2 | `core/rules_prod2.json` | `records/prod2/2026.json` |
| Super League | (NRLルール準拠) | `records/superleague/2026.json` |
| AHL | `core/rules_ahl.json` | `records/ahl/2025-26.json` |
| サッカー(5大リーグ) | `core/rules_soccer.json` | `records/soccer/2025-26.json` |
| MLB | `core/rules_mlb.json` | `records/mlb/2026.json` |

---

## L1指標 早見表

| リーグ | L1指標 | ソース | 閾値 |
|---|---|---|---|
| ATP | クレーcElo差 | tennisabstract.com | 差100以上 |
| WTA | クレーcElo差 | tennisabstract.com (Women's) | 差80以上 |
| NHL | xGF% | moneypuck.com/teams.htm | 差5pt以上 |
| NBA | NRtg差 | basketball-reference.com | (rules_nba.json参照) |
| UFL | 得失点差/試合 | theufl.com/stats | 差4点以上 |
| NFL | Total DVOA | footballoutsiders.com | 差10%以上 |
| CFL | 得失点差/試合 | cfl.ca/stats | 差5点以上 |
| NRL | 得失点差/試合 | nrl.com/draw | 差6点以上 |
| Super Rugby | 得失点差/試合 | super.rugby/stats | 差7点以上 |
| サッカー | clubelo + xGD/G | clubelo.com / understat.com | Elo差50pt以上 + xGD差0.6以上 |
| MLB | wRC+ + FIP | FanGraphs / Baseball Savant | wRC+差10pt以上 + FIP差0.4以上 |

---

## 4象限フレームワーク

全試合は必ず以下4象限のいずれかに分類して `quadrant` フィールドを付与する。

|  | **EV+ (ベット推奨)** | **EV- (ベットしないが予測)** |
|---|---|---|
| **本命側** | **Q1_go**: conf≥75% AND EV>+5% | **Q3_output_a**: conf≥85% / **Q3_mid**: conf 80-84% (別集計) |
| **アップセット側** | **Q2_upset_pick**: UF≥3 AND div≥15pp | **Q4_upset_watch**: dog odds≥3.0 AND UF≥2 |
| **該当なし** | skip | skip |

**運用ルール:**
- 全試合に `quadrant` フィールド必須
- Q1〜Q4 すべて深掘り対象
- Q1とQ2は同一試合で排他、Q3とQ4は共存可
- Q3_midはQ3_output_aと混在禁止（別バケット管理）

---

## GEN005 衝突解消ルール

L1〜L4でconfidence算出 + UF因子チェックを同時に行い、以下で推奨トラックを決定:

| UF因子 | 市場乖離 | トラック |
|---|---|---|
| 0-1個 | <10pp | GO推奨 (通常) |
| 2個 | 10-15pp | CAUTION (見送り・検証用) |
| 3個以上 | ≥15pp | UPSET_PICK (アンダードッグ推奨) |

GO と UPSET_PICK は同一試合で排他。stakeは両トラック 1u 統一。

---

## 分析フロー

```
① ユーザー提供のJSONデータ(試合一覧・オッズ)を起点にスクリーニング開始
   ※ 自分でOddsPortal等を調べない
② 対象スポーツのL1指標でスクリーニング
③ 候補のみL2〜L4を深掘り
④ 全試合に predicted_winner / prediction_confidence / prediction_basis を記録
   ※ tier=skip でも予測勝者は必ず記入
⑤ 信頼度≥75% AND EV>+5% → GO推奨として出力
   ※ GEN008: rec_odds と opponent_odds の両方を必ず記録 (片側のみは禁止)
⑥ 結果確認後 → records/{sport}/*.json を更新 (prediction_hit も更新)
⑦ MISSがあれば miss_analysis に要因分類(L1/L2/L3/L4/External)を記録
   ※ GEN009 v2: 全確定試合に verification フィールド必須 (class配列+depth+note)
     - class: hit_normal / hit_unexpected / miss / upset_occurred / market_divergence から1〜複数
     - depth: hit_normal のみ→light(note 20字以上) / それ以外含む→deep(note 40字以上、決定要因+市場乖離仮説)
⑧ MISSの知見を rules_{sport}.json に追記
```

---

## 記録更新後のダッシュボード同期

`records/*.json` を更新したら必ず以下を実行:

1. `core/dashboard_stats.json` を更新
2. `python sync_sport_cards.py` を実行
3. `dashboard.html` の「アクティブ推奨」から完了試合を削除
4. `records/multi_bets.json` のセッションエントリを最新化
5. `dashboard.html` の予測精度・成長分析タブの数値を確認

---

## セッション終了時の手順

ユーザーが「会話を終了する」「終わり」「記録して」と言ったら:

1. `session_logs/YYYY-MM-DD_HH.md` に作業ログを保存
2. `BACKLOG.md` の完了項目を `[x]` に更新、未完了を残す
3. `git add -A && git commit -m "Session end YYYY-MM-DD" && git push origin main`
4. 「セッション終了。次回は〇〇から再開します。」と報告

---

## 細則・履歴の参照先

以下が必要になったら `archive/CLAUDE_full_20260430.md` を参照する:

- 柱A: ルール改訂統制プロトコル
- 柱B: scope外UPSETスキャンSOP（結果反映 STEP 0.5）
- 柱C: 一次ソースfetch義務化（5種タグ・Class A/B/C件数規定）
- 柱D: 記録対象判断テーブル（3区分定義・大会優先度）
- 健全性スキャン仕様（health_check.py 各項目）
- 過去のSession議題・確定方針
- Session_61由来9件の振り分け案

---

## 重要な原則

- 記録はJSONファイルに直接書き込む (チャット内で終わらせない)
- ルール更新は必ず `rules_{sport}.json` を上書き保存
- 累積統計は `stats/cumulative.json` に反映
- ダッシュボードは結果更新のたびに再生成
- NRL(リーグ)とSuper Rugby(ユニオン)は別競技・別ルールファイル
