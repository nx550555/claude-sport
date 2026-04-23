# スポーツ予想分析システム — 情報ソース要件と運用フロー

> **用途**: Claude チャットへ現行システムの仕組み・必要情報・スポーツ追加可否を相談するための説明資料

---

## 1. システムの基本構造 (4層モデル)

全スポーツ共通の分析レイヤー構造:

| 層 | 役割 | 補正幅 | 必要な情報種別 |
|---|---|---|---|
| **L1** | 地力評価 (ベースレート) | — | 定量的・集計的指標 |
| **L2** | 直近フォーム品質 | ±3% | 対戦相手調整済み勝率 |
| **L3** | スタッツ補正 | ±5〜8% | 戦術・マッチアップ指標 |
| **L4** | 外部要因 | ±10〜15% | 怪我・天候・ホーム・モチベ |

---

## 2. 正しく分析するために必要な情報ソース

### 【絶対必須】L1 指標 (これが無いと構造上スクリーニング不能)

各スポーツで「独立したレーティング」または「対戦相手調整済みの得失点指標」が必要。

| 指標タイプ | 品質 | 例 | Tier |
|---|---|---|---|
| Bayesian Elo (surface/situation 調整) | ★★★★★ | tennis cElo, soccer club Elo | Advanced |
| Expected stats (xG, xGF%, possession 調整) | ★★★★★ | NHL xGF%, Soccer xG | Advanced |
| Efficiency rating (possession 調整) | ★★★★☆ | NBA Net Rating, NFL DVOA | Advanced |
| 単純得失点差 (PD/G) | ★★☆☆☆ | NRL, UFL, Rugby Union | Basic |
| 勝率のみ | ★☆☆☆☆ | 低層リーグ | 運用不可 |

**Advanced Tier (conf≥75% + EV>+5%)** と **Basic Tier (conf≥78% + EV>+7%)** の2段階で閾値を使い分けている理由はここにあります。

### 【絶対必須】オッズソース
- 試合ごとの複数ブック・安定した提供 (ユーザー手動データ起点 or OddsPortal 同等)
- 試合前 vig-抜き implied probability が計算できる精度が必要

### 【重要】L4 補正のための周辺情報

| 情報 | 取得難易度 | 影響度 |
|---|---|---|
| 怪我・欠場情報 | 要リアルタイム | ★★★★★ |
| ゴーリー先発確認 (NHL) | 試合当日 | ★★★★★ |
| ホームコート / 移動疲労 | 固定情報 | ★★★☆☆ |
| 天候 (屋外スポーツ) | 試合当日 | ★★★★☆ (ラグビー・MLB等) |
| モチベーション (消化試合・PO進出確定・プレーオフ) | 文脈理解 | ★★★★☆ |
| 連戦 (Back-to-back) | スケジュール | ★★★☆☆ |

### 【蓄積必須】履歴データ
- アップセット事例 (Type A/B) を継続記録できる ID 空間
- ルール昇格のための evidence accumulation

---

## 3. 現在の運用フロー (全7ステップ)

### STEP 0: 健全性スキャン
- `health_check.py` v6 で 12項目検証 (MISS 補填欠損・CE 同根パターン・スタッツフィード鮮度)

### STEP 0.5: 外部スタッツフィード自動取得 (GEN006)
- GitHub Actions で毎日 2回 (09:00 / 21:00 JST) 8つの fetcher を自動実行
- 対象: NHL (MoneyPuck xGF% + players + injuries), NBA (Basketball-Reference + injuries), Tennis (cElo + serve/return last52), Rugby/Football 8リーグ standings

### STEP 1: 必読ファイル読み込み
- BACKLOG / pending_actions / claude_error_log / rule_pipeline / framework / user_feedback_log

### STEP 2: データ受領
- ユーザーが **手動試合データ JSON** を提供 (オッズ + 試合リスト)
- Claude 側ではオッズを自分で探さない (役割分離)

### STEP 3: GEN004 照合 (既分析 vs 新規)
- オッズ変化 ±0.01 以上 → EV 再計算
- 新規試合 → 次ステップへ

### STEP 4: L1 スクリーニング
- 外部スタッツフィード + WebSearch で L1 指標取得
- 閾値超え → 深掘り / 未達 → SKIP

### STEP 5: L2-L4 深掘り (L1 通過のみ)
- WebSearch で怪我・先発・天候・モチベ・連戦確認
- 各層の補正を適用 → 最終 confidence 算出

### STEP 6: 4象限分類 + UF walkthrough
- Q1_go (EV+ 本命) / Q2_upset_pick (UF≥3 + div≥15pp) / Q3_output_a (conf≥85%) / Q4_upset_watch (UF≥2 + market乖離)
- UF 因子 UF01〜UFA06 の全件 walkthrough 必須 (PA-PERM03)

### STEP 7: 記録 + 同期
- records に predicted_winner・confidence・basis・tier・quadrant 記入
- 5ステップ同期 (cumulative → dashboard_stats → multi_bets → sync_dashboard → sport_cards)

### 事後: MISS 分析 → ルール昇格
- MISS 発生時は miss_analysis + miss_layer + rule_linked の3点セット必須
- upset_patterns.json に Type A/B 登録
- rule_pipeline で evidence 3件到達 → rules_{sport}.json へ昇格

---

## 4. 新スポーツ追加可否の判定基準

以下を全て満たせる必要があります:

### ✅ 追加可能なスポーツの条件
1. **L1 指標が公開されている**
   - 最低限: 得失点差/試合 (PD/G) や勝率基準の順位表
   - 理想: Elo/xG/効率指標など
2. **オッズ市場が流動的**
   - 試合前に安定したオッズが付いている (主要ブックで提供)
3. **選手・チーム情報が英語 or 主要メディアで取得可能**
   - WebSearch で怪我・出場情報・前試合結果が確認できる
4. **試合数が年間数十試合以上**
   - Type A/B 蓄積にサンプルが必要
5. **文化的・ルール的理解が可能**
   - ホームアドバンテージ・連戦疲労・PO形式の仕組みが明文化されている

### ❌ 追加困難なスポーツ (構造的障壁)
1. **公開統計が存在しない / ペイウォール**
   - 一次データが取れない → L1 成立不能
2. **オッズが付かない / 市場が薄すぎる**
   - EV計算の相手 = 市場が機能しない
3. **選手個人要因が勝敗の 80%+ を支配**
   - 例: 個人競技の一発勝負系 (ボクシング単発試合など)
4. **多人数の突発的ラインナップ変更が頻発**
   - AHL (NHLのコールアップで直前で主力変動) は元々除外 → 2026-04 で Basic Tier 復活
5. **シーズン外 / ランダム試合形式**
   - 招待試合・エキシビションは文脈不明で予測困難

---

## 5. 現在稼働中のスポーツ (参考比較)

### Advanced Tier (5種目)
高度な調整指標あり、GO閾値 conf≥75% + EV>+5%

| スポーツ | L1指標 | ソース |
|---|---|---|
| **ATP Tennis** | cElo (surface-specific) | tennisabstract.com |
| **WTA Tennis** | cElo Women's | tennisabstract.com |
| **NHL** | xGF% (5v5 all-situation) | moneypuck.com |
| **NBA** | Net Rating (possession 調整) | basketball-reference.com |
| **NFL** | Total DVOA (予定・9月開幕) | footballoutsiders.com |

### Basic Tier (9種目)
PD/G などcounting stats のみ、GO閾値 conf≥78% + EV>+7%

UFL / CFL / NRL / Super Rugby Pacific / Super League / Premiership / Top 14 / Pro D2 / AHL

### 除外・未対応
- **サッカー** (全リーグ): 未対応。L1 成立可能 (Club Elo / xG 利用可) だが未導入
- **MLB** (野球): 未対応。統計豊富 (wRC+/FIP/xwOBA) だが未導入
- **MLS / Bundesliga / Premier League** 等: 未対応
- **格闘技 (UFC/Boxing)**: L1 難あり
- **F1 / MotoGP**: ランキング点制で EV フレーム成立しにくい
- **ゴルフ**: 複数選手フィールド競技で L1 設計が特殊

---

## 6. Claude チャットに相談する時のポイント

以下の観点で検討すると「追加可能か否か」が判定しやすいです。

### 追加検討リストの作り方
各スポーツについて以下を調べてもらう:
1. **公開されている L1 相当の指標は何があるか?** (Elo / 効率指標 / 得失点差)
2. **その指標の提供サイト** (API? 静的HTML? ペイウォール?)
3. **オッズが付いているか** (OddsPortal等で試合前odds存在)
4. **怪我情報源の有無** (公式サイト / ESPN / 専門サイト)
5. **年間試合数・シーズン形式**

### 優先検討推奨スポーツ (推測順)
1. **サッカー主要リーグ** (Premier League/Bundesliga/La Liga/Serie A/J1) — L1 (Club Elo/FiveThirtyEight SPI/xG) + 豊富なオッズ + 怪我情報 → **Advanced Tier 可能性大**
2. **MLB** — sabermetrics 界の宝庫 (wRC+/FIP/xFIP) + 毎日試合でサンプル豊富 → **Advanced Tier 可能**
3. **KHL / SHL** (欧州アイスホッケー) — NHL類似だが xGF% 公開状況が弱い → **Basic Tier**
4. **EuroLeague / CBA** (欧州・中国バスケ) — NBA類似だが Net Rating 取得難 → **Basic Tier**
5. **クリケット / ラグビーWC** — ワールド大会は試合数限定で L1 蓄積困難
6. **K-League / MLS** — Basic Tier 相当か

### 情報提供者(ユーザー)側に依存する要素
- **オッズデータ提供**: ユーザーが手動で JSON 形式で渡す前提の運用
- **スポーツ文脈の初期教示**: 新リーグの PO 形式・特殊ルール・チーム構成等

---

## 相談テンプレート例

> Claude に相談する際の雛形:

```
現在 14 スポーツを対象に予想分析システムを運用しています。
(Advanced Tier 5種目: ATP/WTA/NHL/NBA/NFL、Basic Tier 9種目: UFL/CFL/NRL/Super Rugby/Super League/Premiership/Top14/Pro D2/AHL)

新しく「[スポーツ名]」を追加することを検討しています。
以下を調べてください:

1. 使用できる L1 指標 (Elo / 効率指標 / PD/G等) と提供サイト
2. オッズ市場の有無 (主要ブックでの提供状況)
3. 怪我・欠場情報のソース
4. 年間試合数とシーズン構造
5. 特殊ルール (ホーム、連戦、PO形式など)

上記を踏まえ Advanced/Basic どちらの Tier で運用可能か、または追加困難かを判定してください。
```

---

*作成日: 2026-04-23 / Session_53*
*System Version: v3.0 (Phase 2: UPSET_PICK 運用中)*
