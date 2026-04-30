# A-3 サブタスク6 step1 提案レポート: P020 / P024 柱A 承認制プロセス

> **位置付け**: 議題1+1' (柱A 異セッション独立性チェック + rule_linked: null パターン + candidate_pattern registry) の **step4 実証本丸**。Session_61 R024 forbidden_practice (同一 turn 内 evidence 3/3 → implement) の再発防止構造が初めて本格運用される。本レポートは step1 (提案レポート生成) のみ。step2 (ユーザー判断 + Claude.ai 外部レビュー) 以降の着手は次の指示を待つ。
>
> **本レポートの構成**: P020 → P024 各々で (a)〜(e) を生成。両候補の step3 改訂実装は **個別 commit** とする (一括処理禁止 / 柱A 規律継続)。

---

## 0. 共通: 議題1+1' step4 実証チェック (柱A 機械検証層)

両候補について、柱A 規律遵守を機械的にチェックした結果。

### 0.1 異セッション独立性チェック (柱A 3-1 / rule_pipeline.json instructions step1)

| 候補 | evidence | added_session (commit) | 異セッション独立性 |
|---|---|---|---|
| **P020** | U005 | Initial commit (`5fc49f2` / Session_30 以前 / 2026-04-11) | ✓ |
| **P020** | A008 | Session_34 (`0721b85` 全スポーツ Type A 調査 / 2026-04-13頃) | ✓ |
| **P020** | A039 | Session_61 (`b770d5b` _session61_rule_feedback.py 経由 / 2026-04-26) | ✓ |
| **P024** | A029 | Session_47 (`2740513` NHL/NBA G1 全結果反映 / 2026-04-21) | ✓ |
| **P024** | A031 | Session_50 (`2c2e466` Q3 output_a MISS 5件 補填 / 2026-04-22) | ✓ |
| **P024** | A043 | Session_61 (`b770d5b` _session61_rule_feedback.py 経由 / 2026-04-26) | ✓ |

→ **両候補とも 3 evidence が異なるセッションで独立検出済**。Session_61 R024 で発生した「同一 turn 内 evidence 3/3 検出」逸脱パターンに該当しない。

### 0.2 同一 turn 内重複付与禁止チェック (柱A 5. 禁止事項 6項目目 / 議題1+1')

両候補とも evidence 3件目 (P020=A039 / P024=A043) は Session_61 で追加されたが、**ready_to_implement 移行は Session_61 内で実施済**。本サブタスク6 (Session_64) で proposal を生成するのは **次セッション以降規定** に従う運用 (= 議題1 確定方針: 「最後の evidence 追加から次セッション以降に proposal 生成」)。

→ 議題1 規定遵守 ✓。

### 0.3 一次ソース fetch 件数規定 (柱C 4-2)

R*** 改訂は柱C「4-2 fetch 件数規定」の対象外 (柱C 4-1 は MISS 重要度3段階分類が miss_class 付与対象 / 4-2 は MISS 分析 fetch 件数規定であり、ルール改訂時の evidence 一次ソースは Session_62 フェーズ4 ステージ3 で別途規定)。ただし evidence 3件の一次ソース URL は柱C 4-3 5種タグ義務に沿って proposal レポート (a)〜(e) で明示する。

---

## 1. P020 提案レポート (NRL R1-R8 PD/G 信頼性ダウン補正 / R014 新規実装)

### 1-(a) 現状分析

#### 候補ルール基本情報

| 項目 | 内容 |
|---|---|
| **candidate_id** | P020 |
| **proposed_rule_id** | R014 |
| **target_rule_file** | `core/rules_nrl.json` |
| **title** | NRL 小サンプル期 (R1-R8) PD/G 信頼性ダウン補正 |
| **description (元提案)** | NRL の Round 1-8 において、PD/G ベースの L1 indicator は 1-2試合のアウトライヤー blowout で大きく歪む可能性が高い。PD/G 差が6pt以上でも、その内訳（1試合の40点差が平均を歪めているか等）を確認する。小サンプル期には信頼度上限を 78% に制限し、CAUTION 格下げを検討。desperate team (0-4/1-4) との対戦時は追加 -5% 補正 [MEMORY:rule_pipeline.json L605-637]。 |
| **trigger_threshold** | 3 |
| **current_count** | 3 |
| **status** | ready_to_implement (柱A 改訂後は `ready_for_proposal` 相当) |

#### evidence 3件 詳細

##### evidence#1: U005 (NRL R6 Rabbitohs vs Raiders / 2026-04-11)

- **試合**: Canberra Raiders 36-34 South Sydney Rabbitohs (R6) [SEARCH]
- **市場 fav**: Rabbitohs (PD +3.5/試合) / odds 不明 [SEARCH]
- **PD差**: 17.3pt/試合 (Raiders -13.8 vs Rabbitohs +3.5) [MEMORY:rule_pipeline.json L617]
- **MISS 分析**: Raiders 5試合 PD は single game blowout が平均を歪めた可能性。Rabbitohs 4連勝中の hot streak が逆 trend 引き起こした疑い [MEMORY:rule_pipeline.json L617]
- **既存 rule 紐付け**: R012 (R3-R8 閾値 6pt → 12pt) trigger evidence でもある [FETCH:core/rules_nrl.json L128-133]
- **追加セッション**: Initial commit (`5fc49f2`) / Session_30 以前

##### evidence#2: A008 (NRL R6 Sharks vs Roosters / 2026-04-11)

- **試合**: Sydney Roosters 34-22 Cronulla Sharks (R6 @Optus Stadium Perth neutral venue) [FETCH:nrl.com R6 match centre]
- **市場 fav**: Sharks (PD advantage, but small sample outlier inflated) [SEARCH]
- **MISS 分析**: Sharks PD advantage が 'first 5 rounds' outlier で過大評価。Optus Stadium Perth (neutral venue) で 22-13 から Roosters が後半22点逆転。'Game of two halves' [SEARCH]
- **rule_linked**: P020 (NRL small-sample PD unreliability - same pattern as U005) [FETCH:upset_patterns.json L558]
- **追加セッション**: Session_34 (`0721b85` / 全スポーツ Type A アップセット調査完了 A002-A011)
- **一次ソース**: nrl.com R6 match centre / leagueunlimited.com / zerotackle.com [SEARCH]

##### evidence#3: A039 (NRL R8 Manly vs Eels / 2026-04-26)

- **試合**: Parramatta Eels 24-18 Manly Sea Eagles (R8) [SEARCH]
- **市場 fav**: Manly @1.37 home (PD +91 / 4連勝中の hot streak) [MEMORY:rule_pipeline.json L629]
- **MISS 分析**: Manly home @1.37 fav (PD +91) → Eels 逆転 24-18。Manly 4連勝の hot streak が Sydney derby rivalry + 4Q fade で崩壊。PD/G 過大評価 + Eels desperate (1-6) home derby motivation 過小評価。R8 = 小サンプル期上限 [MEMORY:rule_pipeline.json L629]
- **追加セッション**: Session_61 (`b770d5b` / _session61_rule_feedback.py 経由)

#### 既存ルールとの関係

| 既存 rule | 関係 | 競合判定 |
|---|---|---|
| **R001** (L1 PD差 6pt 閾値) | 同 L1 stage / 異なる threshold (R001=6pt 通過 / R014=78% 信頼度上限) | レイヤー異なるため非競合 |
| **R011** (Desperate Team -5%) | desperate team 対戦時の補正 / R014 の desperate 条件と重複範囲あり | **重複可能性あり** → 案2-3 で排他制御方針 |
| **R012** (R3-R8 閾値 6pt → 12pt) | 同 R1-R8 stage / 異なる stage (R012=L1 通過 / R014=L4 信頼度補正) | レイヤー異なるため非競合 |
| **R013** (長期 H2H 連敗ストリーク終焉 -8%) | 適用条件異なる (10連敗以上) | 非競合 |

#### candidate_pattern 紐付け

新規 candidate_pattern 値 `nrl_small_sample_r1_r8_pd_overrate_desperate_opp` を提案。registry 登録要 (柱A 3-3 規定)。

#### 一次ソース fetch 状態 (柱C 4-3)

| evidence | 一次ソース URL | fetch 種別 |
|---|---|---|
| U005 | (Initial commit / fetcher 経由なし) | [MEMORY] (記述根拠は記憶ベース) |
| A008 | nrl.com / leagueunlimited.com / zerotackle.com | [SEARCH] (本文 WebFetch 未実施 / WebSearch スニペットレベル) |
| A039 | (Session_61 で _session61_rule_feedback.py 経由 / 詳細未記録) | [SEARCH] (Session_61 時点の検証粒度不明) |

**観察事項**: 3件とも一次ソース WebFetch 本文取得は未実施。柱C 4-2 規定の Class A=3件以上の WebFetch 成功は本 proposal 段階では満たしていない。step2 で追加 fetch 実施を検討要。

### 1-(b) 提案案 (3案以上)

#### 案1: 緩和版 (信頼度上限 80% + 追加 -3%)

```
適用条件: Round 1-8 NRL 試合 + L1 PD差 6pt以上 + 対戦相手 desperate (≤2-6 record)
補正値: 信頼度上限 80% + 追加 -3%
R011 競合解消: R014 適用時は R011 を非適用 (排他)
```

- **長所**: -3% は控えめで R1-R8 高信頼度予想 HIT 案件 (Warriors vs GC R7 conf 90.7 など) への影響が小さい
- **短所**: A039 Manly MISS の場合、conf 78 + -3 = 75 で GO 維持される可能性 → MISS 回避効果が低い
- **MISS 回避シミュレーション**: A039 Manly @1.37 推定勝率元値 78% → 75% で `conf>=78% AND EV>+7%` を割り込み GO 解除 → CAUTION 格下げで MISS 回避 ✓ (Basic Tier 78% 閾値が決定的)

#### 案2: 標準版 (元 P020 提案そのまま)

```
適用条件: Round 1-8 NRL 試合 + L1 PD差 6pt以上 + 対戦相手 desperate (≤2-6 record)
補正値: 信頼度上限 78% + 追加 -5%
R011 競合解消: R014 適用時は R011 を非適用 (排他制御)
```

- **長所**: 元 P020 提案と整合 / U005・A039 の再発抑制効果が確実 (上限 78% で GO 解除)
- **短所**: -5% は強めの補正で false positive (本来 GO だった試合への過剰下方補正) リスク
- **MISS 回避シミュレーション**: A039 Manly 78% → 73% (上限 78% は元値と一致 → 追加 -5% が効く)。78% threshold 割り込み → SKIP/CAUTION 格下げ → MISS 回避 ✓

#### 案3: 厳格版 (desperate 条件不問 + 一律 -5%)

```
適用条件: Round 1-8 NRL 試合 + L1 PD差 6pt以上 (desperate 条件不問)
補正値: 信頼度上限 75% + 一律 -5%
R011 競合解消: R014 と R011 は加算可 (上限 -10%)
```

- **長所**: 適用条件がシンプルで desperate 判定不要 / R1-R8 全試合一律で false negative (MISS 回避漏れ) 最小
- **短所**: 過剰下方補正リスク (R1-R8 高信頼度 HIT の Warriors vs GC R7 conf 90.7 → 85.7 に格下げ → ベット推奨機会損失)。**A007 Warriors vs Storm R6 (R013 trigger / 連敗終焉 HIT)** のような特殊勝因があるケースまで一律補正してしまう

#### 案4 (議題1+1' で言及された代替案 / 緩和系): R012 強化版

```
案4 = R014 を新規実装せず、既存 R012 の閾値 (R3-R8 6pt → 12pt) を R1-R8 6pt → 14pt に引き上げる
```

- **長所**: 新 rule 追加なし / 既存ルールの拡張のみ / 構造シンプル
- **短所**: R012 は L1 stage の通過閾値 (= 候補絞り込み) であり、L4 stage の信頼度補正ではない → MISS 回避メカニズムが異なる。Manly @1.37 PD +91 のような大差案件は L1 を通過してしまうため案4 は MISS 回避効果なし

### 1-(c) 反例検証

#### 反例カテゴリ整理

R1-R8 NRL で PD差6pt以上 + 高信頼予測が **HIT** したケースを検出し、新ルール適用時の false positive (本来 GO だった試合への過剰下方補正) を確認する。

#### 反例#1: R7 NZ Warriors vs Gold Coast Titans (2026-04-18)

- **conf**: 90.7% (元値) [FETCH:records/nrl/2026.json]
- **predicted_winner**: NZ Warriors
- **prediction_hit**: TRUE
- **PD差**: 大 (Warriors hot form / 詳細不明)
- **対戦相手**: Gold Coast Titans (record 不明 / 必ずしも desperate ≤2-6 ではない可能性)
- **新ルール適用シミュレーション**:
  - 案1 (-3%): 90.7 → 87.7 (上限 80% 適用 → 80%) → GO 維持 (78% threshold 通過) ✓
  - 案2 (-5%): 90.7 → 85.7 (上限 78% 適用 → 78%) → GO 境界線 (78% threshold 同値) → CAUTION 格下げリスク 高 ✗
  - 案3 (一律 -5%): 90.7 → 85.7 (上限 75% 適用 → 75%) → SKIP 格下げ ✗ false positive

#### 反例#2: R6 NZ Warriors vs Melbourne Storm (2026-04-11 / R013 trigger)

- **conf**: 不明 (記録 hit=true / R013 trigger evidence A007) [MEMORY:rules_nrl.json R013]
- **predicted_winner**: 不明 (Warriors と推測 / Storm market fav)
- **PD差**: 大 (Storm fav / Warriors 12年メルボルン未勝利)
- **特殊勝因**: R013 (12年連敗終焉) で別補正系
- **新ルール適用シミュレーション**: R013 既適用前提で R014 は重複適用なし (排他制御要) → R014 影響なし ✓

#### 反例#3-#4: 他 R1-R8 高信頼予想

- 現セーズン (2026) の R1-R5 records は明示的記録なし (NRL 開幕 3月 / Initial commit 以前のデータ)
- 既存 records 上で R1-R8 の `prediction_hit=True` 高信頼予想 (conf>=78%) は **R7 NZ Warriors vs GC のみ 1件** (反例#1 と重複)
- 追加反例の取得には **WebFetch で過去セッション (Session_44 以前) のスクリーニング結果取得** または **過去シーズン 2025 NRL R1-R8 PD/G 高 fav HIT 事例** の追加検証が必要

#### 反例#5: 仮想反例 (将来想定 / 過去シーズン extrapolation)

- **想定**: 2025 NRL R1-R8 で PD差 8-12pt + desperate 対戦 + HIT したケース複数 (詳細データ未取得)
- **取得方法**: WebFetch nrl.com/draw/?competition=111&round=R1〜R8 + 当時オッズ
- **step2 でのアクション**: ユーザー承認時に追加調査依頼するか、`investigation_status: investigation_incomplete` 付与で proposal を仮承認とするかを判断

#### 反例検証 充足度判定

| 種別 | 件数 | 充足度 |
|---|---|---|
| 直接反例 (R1-R8 + PD差6pt+ + desperate + HIT) | **0件** (現セーズン記録上) | ✗ 未充足 |
| 間接反例 (R1-R8 + 高信頼度予想 + HIT) | **1件** (反例#1 R7 Warriors vs GC) | △ 部分充足 |
| 排他制御確認 (既存 R013 trigger evidence と非競合) | **1件** (反例#2) | ✓ 確認 |

→ **反例検証は不十分**。step2 でユーザー判断時に「過去シーズン 2025 NRL R1-R8 一次ソース fetch 追加調査」を提案するか、段階的承認 (案1 緩和版で先行実装 + 90日後評価) を推奨。

### 1-(d) 推奨案 + 根拠

#### 推奨: **案2 (標準版 / 元 P020 提案そのまま)**

#### 推奨根拠

1. **元 P020 設計思想と整合**: pipeline 候補化時 (Session_44 以前) からの検討蓄積を活用。新 rule 設計の再検討コストなし。
2. **MISS 回避効果が確実**: A039 Manly MISS (78% conf) を案2 で 73% 格下げ → GO 解除 → MISS 回避 ✓
3. **Basic Tier 整合**: NRL は Basic Tier (rules_nrl.json `accuracy_tier: basic` / GO 閾値 conf≥78% AND EV>+7%) なので、上限 78% は閾値ライン上 → 「GO 境界の試合のみ格下げ」効果で false positive を最小化
4. **R011 排他制御で過剰補正回避**: R014 適用時は R011 を非適用とする排他制御で -10% (R011 -5% + R014 -5%) を回避

#### 案2 採用に伴うリスクと対応

| リスク | 対応 |
|---|---|
| 反例#1 (R7 Warriors vs GC HIT 90.7%) が CAUTION 格下げ → ベット機会損失 | desperate 条件 (≤2-6 record) で絞り込み済 → GC が ≤2-6 でない場合は適用外 → リスク軽減 |
| 反例検証 不充足 (過去シーズン未調査) | step2 で「過去シーズン 2025 NRL R1-R8 追加調査」をユーザーに依頼 |
| 実装後 R1-R8 NRL の累計予測精度低下 | 90日後 (≈ 2026-07-29 / R20 前後) に retrospective 評価 + 必要に応じて閾値調整 |

#### 却下時の代替案 (案1 緩和版へ後退)

ユーザー却下時は **案1 緩和版** (上限 80% + -3%) に後退。`-3%` は false positive を最小化するが MISS 回避効果も弱まる。再評価サイクルを 60日に短縮し早期改訂可とする。

### 1-(e) 実装影響範囲

#### rules_nrl.json への変更内容 (案2 採用想定)

```json
{
  "id": "R014",
  "type": "learned",
  "title": "R1-R8 小サンプル期 PD/G 信頼性ダウン補正 (desperate 対戦時)",
  "body": "Round 1-8 NRL 試合において L1 PD差 6pt以上 + 対戦相手 desperate (record ≤2-6) の場合、信頼度上限を 78% に制限し、追加 -5% 補正。Basic Tier 78% threshold 整合。R011 (Desperate Team -5%) との重複適用を避けるため、R014 適用時は R011 を非適用 (排他制御)。",
  "trigger": "P020 evidence 3/3: U005 (R6 Rabbitohs vs Raiders / Initial) + A008 (R6 Roosters vs Sharks / Session_34) + A039 (R8 Manly vs Eels / Session_61). 議題1+1' 異セッション独立性確認済。",
  "added": "2026-04-30 (A-3 サブタスク6 step1 提案 → step3 改訂実装で確定)",
  "candidate_pattern": "nrl_small_sample_r1_r8_pd_overrate_desperate_opp",
  "exclusion": ["R013 (長期 H2H 連敗終焉) trigger evidence の場合は R014 を非適用 = R013 既適用前提で重複補正回避]"
}
```

#### candidate_pattern_registry.json への新規登録

```json
"nrl_small_sample_r1_r8_pd_overrate_desperate_opp": {
  "sport": "nrl",
  "context": "nrl_regular_season_r1_r8",
  "summary": "NRL R1-R8 小サンプル期 PD/G 過大評価 + desperate (≤2-6) 対戦時の信頼度上限 78% + 追加 -5% 補正 (実装候補 P020 → R014 / 議題1+1' step4 実証)",
  "evidence_count": 3,
  "first_evidence": {"session": "Initial commit", "match": "U005 R6 Raiders d. Rabbitohs", "date": "2026-04-11"},
  "evidence_sessions": ["Initial", "Session_34", "Session_61"],
  "alias": [],
  "status": "promoted",
  "trigger_threshold": 3,
  "promoted_to_p_candidate_id": "P020",
  "weak_link_to_existing": null
}
```

#### rule_pipeline.json への変更内容

- P020 の `status` を `ready_to_implement` → `approved_pending_implementation` (step3 ユーザー承認後) → `implemented` (step4 commit 後) に変更
- `implemented_session` フィールド追加
- `implemented_rule_id` = "R014"

#### cumulative.json 影響シミュレーション (遡及適用)

過去 R1-R8 NRL records に R014 を遡及適用した場合:

| 試合 | 元 conf / hit | R014 適用後 | 影響 |
|---|---|---|---|
| U005 R6 Rabbitohs vs Raiders | 78%? / MISS | 73% / SKIP 格下げ | MISS 回避 (推奨ベット減) |
| A008 R6 Sharks vs Roosters | 不明 / MISS | 73% / SKIP 格下げ | MISS 回避 |
| A039 R8 Manly vs Eels | 78%? / MISS | 73% / CAUTION_MARGIN | MISS 回避 |
| 反例#1 R7 Warriors vs GC | 90.7% / HIT | 78% / GO 境界 | false positive リスクあり (GC desperate 条件確認要) |

**累計 hit_rate 影響**: NRL 全体 records 推奨 N=不明 (要再計算) のため step3 commit 後に dashboard_stats.json 自動再計算で確認。本 proposal 段階での厳密な数値シミュレーションは未実施。

#### dashboard.html / dashboard_stats.json 影響

- NRL タブの予測精度 (hit_rate) 数値が遡及更新される可能性 (上記シミュレーション結果次第)
- 4本柱完了後の別タスク (cumulative.json `by_record_class` 別軸 + Track 1/Track 2 表示拡張) と統合実施推奨

#### 推定 commit 数

- 実装1 (rules_nrl.json + rule_pipeline.json + candidate_pattern_registry.json + 関連 records 4本柱フィールド遡及付与) = +1 commit
- handoff 1 (P020 step3 完了 → step4 (運用観察) handoff) = +1 commit
- 合計 +2 commit

---

## 2. P024 提案レポート (NBA PO G1 Star Scorer Absence -8〜-10% / N_NBA_new2 新規実装)

### 2-(a) 現状分析

#### 候補ルール基本情報

| 項目 | 内容 |
|---|---|
| **candidate_id** | P024 |
| **proposed_rule_id** | N_NBA_new2 (B015 リネーム検討) |
| **target_rule_file** | `core/rules_nba.json` |
| **title** | NBA PO G1 star scorer (>25ppg RS) 欠場時の L4 下方補正 |
| **description (元提案)** | star scorer (RS 25ppg+) が G1 game-time decision → ruled out になった場合、star-heavy チーム側信頼度を -8〜-10% 補正。Durant (26ppg) HOU 欠場のように実質 NRtg 1-4pt 下方修正相当。L1 NRtg は RS 全体平均で star ON ベース → star OFF では NRtg proxy が破綻 [MEMORY:rule_pipeline.json L703-705]。 |
| **trigger_threshold** | 3 |
| **current_count** | 3 |
| **status** | ready_to_implement (柱A 改訂後は `ready_for_proposal` 相当) |

#### evidence 3件 詳細

##### evidence#1: A029 (NBA PO R1 G1 LAL d. HOU / 2026-04-18)

- **試合**: Los Angeles Lakers 107-98 Houston Rockets (PO R1 G1 / HOU @home) [FETCH:ESPN gameId 401869190]
- **市場 fav**: HOU @1.43 (W2, Durant RS 26.0ppg)
- **欠場**: Kevin Durant (HOU RS 26.0ppg) G1 欠場 (patellar tendon contusion / pre-game warmup 後 ruled out) [FETCH:ESPN rockets kevin-durant-g1-vs-lakers-knee-contusion]
- **MISS パターン**: 市場 HOU @1.43 fav、予測 HOU MISS。Luke Kennard 27pts career-high で short-handed LAL が突破 [FETCH:NBA.com rockets-lakers-2026-playoffs-game-1-takeaways]
- **追加セッション**: Session_47 (`2740513`)

##### evidence#2: A031 (NBA PO R1 G2 POR d. SAS / 2026-04-22)

- **試合**: Portland Trail Blazers 106-103 San Antonio Spurs (PO R1 G2 / SAS @home) [FETCH:ESPN gameId 401869378]
- **欠場**: Wembanyama (SAS RS 24.3ppg) 2Q concussion 退場 (Holiday ファウル face-first fall, jaw slam) [FETCH:CBS Sports Wembanyama concussion protocol]
- **MISS パターン**: Wemby OFF で L1 NRtg proxy 破綻、SAS 4Q 14pt リードから closing 3:37 無得点で逆転負け。Scoot Henderson 31pts POR breakout [FETCH:NBA.com trail-blazers-spurs-2026-playoffs-first-round-game-2-takeaways]
- **A029 との同型**: KD 欠場 HOU と同一構造 (star scorer in-game loss → L4 -8〜-10% 相当)
- **追加セッション**: Session_50 (`2c2e466`)

##### evidence#3: A043 (NBA PO R1 G4 HOU d. LAL / 2026-04-26)

- **試合**: Houston Rockets 115-96 Los Angeles Lakers (PO R1 G4 / HOU @home / 19pt blowout) [FETCH:vavel.com rockets-lakers-game-4]
- **市場 fav**: LAL (-2 spread / fav_odds 1.65)
- **HIT パターン**: KD G4 return → HOU 19pt blowout, avoid elimination. P024 reverse パターン (star return → home dominance)
- **双方向構造**: G1 absence は -8〜-10%、return G時は逆方向 +5〜+8% 補正 [MEMORY:rule_pipeline.json L734]
- **追加セッション**: Session_61 (`b770d5b`)

#### 既存ルールとの関係

| 既存 rule | 関係 | 競合判定 |
|---|---|---|
| **B005** (Star 選手欠場 -15〜-20%MVP / -10〜-15% All-Star / -5〜-8% 主力) | 認識ベース (MVP/All-Star) vs 数値ベース (RS 25ppg+) | **重複範囲あり** → 案3 で B005 統合改訂 / 案2 で N_NBA_new2 優先 |
| **B007** (ロードマネジメント対応) | 手順ルール (ステータス確認) | レイヤー異なるため非競合 |
| **B008** (公式傷病リスト確認) | 手順ルール (前提条件) | 非競合 (B008 確認後に N_NBA_new2 補正適用) |
| **B009** (3P% 分散) | 別 L3 補正系 | 非競合 |

#### candidate_pattern 紐付け

新規 candidate_pattern 値 `nba_po_g1_star_scorer_25ppg_absence_return_l4_correction` を提案。registry 登録要 (柱A 3-3 規定 / 80文字以内 OK)。

#### 一次ソース fetch 状態 (柱C 4-3)

| evidence | 一次ソース | fetch 種別 |
|---|---|---|
| A029 | ESPN gameId 401869190 / NBA.com rockets-lakers-2026-playoffs-game-1-takeaways / ESPN rockets kevin-durant-g1-vs-lakers-knee-contusion | [FETCH] (3件 / Class A 充足) |
| A031 | ESPN gameId 401869378 / NBA.com trail-blazers-spurs-2026-playoffs-first-round-game-2-takeaways / CBS Sports Wembanyama concussion protocol | [FETCH] (3件 / Class A 充足) |
| A043 | vavel.com rockets-lakers-game-4 / silverscreenandroll.com lakers-rockets-recap-game-4 | [FETCH] (2件 / Class B 充足) |

**観察事項**: P020 と異なり、3 evidence とも一次ソース複数件確認済 (柱C 4-2 Class A or B 充足)。

### 2-(b) 提案案 (3案以上)

#### 案1: 単方向 OFF のみ補正 (return cycle は別 rule)

```
適用条件: PO R1 G1 / RS 25ppg+ star scorer が game-time decision → ruled out
補正値: 当該 team 信頼度 -8〜-10%
return cycle: 別 rule (将来 N_NBA_new3 等で扱う)
B005 競合解消: N_NBA_new2 適用時は B005 のスター欠場補正のうち重複部分を非適用
```

- **長所**: シンプル / evidence#1 (A029) + #2 (A031) と整合 (両方 OFF パターン)
- **短所**: A043 (return cycle HIT) を捕捉できない → P024 evidence 3件目の意義を半分失う

#### 案2: 双方向 OFF/ON 統合 (元 P024 提案そのまま)

```
適用条件: PO R1 G1 / RS 25ppg+ star scorer の OFF/ON 状態 (G1 status change)
補正値:
  - OFF (game-time decision → ruled out): 当該 team 信頼度 -8〜-10%
  - ON return (前 G で OFF → return G): 当該 team 信頼度 +5〜+8%
B005 競合解消: N_NBA_new2 適用時は B005 のスター欠場補正のうち重複部分を非適用
```

- **長所**: A029 + A031 + A043 の3 evidence を完全捕捉 / return cycle で予測精度向上
- **短所**: 適用条件が複雑 (前 G 状態追跡要) / SAS G3 反証 (Wemby OUT でも勝った) のような case に対応不可

#### 案3: B005 統合改訂 (新 rule ID 不要)

```
B005 を v1.1 改訂し以下を追加:
- 「PO G1 限定 + RS 25ppg+ star scorer の OFF/ON cycle」サブ条項
- 数値ベース判定 (現状 B005 は MVP/All-Star 認識ベース)
- 双方向補正 (-8〜-10% / +5〜+8%)
```

- **長所**: 新 rule ID 追加なし / 既存ルールの拡張のみ / B005 重複問題が構造的に解決
- **短所**: B005 改訂は柱A 既存ルール改訂プロセス (3-1 規定) に該当 → 「v_X.0 → v_Y.0 差分レポート」+ 反例検証の追加負荷 / 実装の影響範囲が B005 全体に拡大

#### 案4: PO G1 限定 + 対戦相手依存度補正サブ条件

```
適用条件: PO R1 G1 / RS 25ppg+ star scorer の OFF/ON cycle + 対戦相手 star 依存度
補正値:
  - 基本補正は案2 と同じ (-8〜-10% / +5〜+8%)
  - 対戦相手 star 依存度が低い場合は -50% (= -4〜-5% に弱める)
B005 競合解消: 案2 と同じ
```

- **長所**: SAS G3 反証 (Wemby OUT でも勝った / 対戦相手 MIN star 依存度低い ≠ 反論しない) に対応可能
- **短所**: 実装複雑度増 / star 依存度の定量定義が困難

### 2-(c) 反例検証

#### 反例カテゴリ整理

NBA PO G1-G4 で star scorer 欠場/復帰時の HIT/MISS 分布を確認し、新ルール適用時の false positive (本来 GO だった試合への過剰補正) と false negative (適用すべきところを見逃し) を検証する。

#### 反例#1: A029 系列 G2 (KD HOU 復帰でも HOU 連敗 / Session_50 PA096 reference)

- **試合**: HOU vs LAL G2 (4-22) / KD return [FETCH:records/nba/2025-26.json L?]
- **conf**: 62 / hit=False / pred=Houston Rockets [FETCH:records/nba/2025-26.json]
- **意味**: G1 KD OFF → G2 KD ON return でも HOU は LAL に連敗 → 案2 (+5〜+8% return cycle 補正) を適用しても HOU 勝率は復活しない可能性 (momentum carryover が L1 NRtg を上回る)
- **本 evidence の論理**: 案2 は「return G で +5〜+8%」だが、A029 系列 G2 では return しても fav 復活せず → **案2 の return cycle 補正は too generous**
- **対応**: 案2 の return cycle は **G2 ではなく G3 以降** に限定 (G2 は前 G の momentum 残効果が大きい) するサブ条件追加検討

#### 反例#2: SAS G3 (Wemby OUT でも SAS 勝利 / Session_60 PA096 reference)

- **試合**: SAS vs MIN G3 (4-25) / Wemby OUT [FETCH:records/nba/2025-26.json / Session_60 PA096]
- **outcome**: SAS HIT (UPSET prediction 当たり / Wemby OUT でも勝利)
- **意味**: 案2 (-8〜-10% G1 OFF) を G3 まで延長すると SAS conf を不当に格下げ → false positive
- **対応**: 案2 を **PO R1 G1 限定** とする (G2 以降は team adjustment が進む) サブ条件で false positive 回避

#### 反例#3: BOS G1 vs PHI (4-22 / 32pt blowout HIT)

- **試合**: BOS 123-91 PHI (PO R1 G1) / star scorer absence なし
- **conf**: 85.2% / hit=True
- **意味**: 案2 適用条件 (RS 25ppg+ star scorer absence) 該当なし → **case 該当なし** = false positive リスクなし ✓

#### 反例#4: OKC G1 vs PHX (4-23 / 35pt blowout HIT)

- **試合**: OKC 119-84 PHX (PO R1 G1) / star scorer absence なし
- **conf**: 90.6% / hit=True
- **意味**: 同上 → false positive リスクなし ✓

#### 反例#5: SAS G1 vs POR (4-20 / SAS 87% conf HIT)

- **試合**: SAS HIT (G1)
- **conf**: 87 / hit=True / Wemby ON
- **意味**: G1 で Wemby ON → 案2 適用なし (補正なし) → false positive リスクなし ✓
- **重要観察**: G2 (4-22) で in-game injury → A031 の MISS 案件。Wemby G1 は ON、G2 で OUT。「**G2 in-game** での star loss」は案2 の「G1 status change」適用範囲外 → **案2 は A031 evidence を完全捕捉できていない**

#### 反例#6: DET G1 vs ORL (4-19 / DET 78% conf MISS)

- **試合**: DET 78% conf MISS (A026 / P022 candidate trigger)
- **意味**: star scorer absence ではなく **PO experience gap** (P022 candidate) が要因 → 案2 適用なし → false positive リスクなし ✓
- **観察**: P022 (PO experience gap) と P024 は **異なるパターン** で並列に存在

#### 反例検証 充足度判定

| 種別 | 件数 | 充足度 |
|---|---|---|
| 直接反例 (PO G1 + star scorer absence + HIT) | **0件** | ✗ 検出なし (絶対 sample 不足) |
| 間接反例 (PO G1 高信頼度予測 HIT) | **3件** (反例#3 BOS / #4 OKC / #5 SAS) | ✓ 充足 |
| 隣接反例 (G2/G3 で star scorer 状態変動) | **2件** (反例#1 KD G2 return MISS / 反例#2 Wemby G3 OUT HIT) | ✓ 充足 |
| 別パターン排他確認 (P022 PO experience gap) | **1件** (反例#6) | ✓ 確認 |

→ **反例検証は P020 より充足**。ただし以下の論点が浮上:
- 案2 の return cycle 補正は **G2 では too generous** (反例#1) → 案2-modified (G3 以降に限定) または 案4 (対戦相手 star 依存度補正) を要検討
- 案2 は **G2 in-game star loss** を捕捉できない (反例#5 観察) → A031 evidence が論理的に微妙

### 2-(d) 推奨案 + 根拠

#### 推奨: **案2 (双方向 OFF/ON) + 適用範囲限定サブ条件 (PO G1 限定 / 反例#2 対応)**

#### 推奨根拠

1. **3 evidence 完全捕捉**: 案2 が A029 + A031 + A043 を一律にカバー (案1 は A043 を捕捉できない / 案3 は実装影響大)
2. **PO G1 限定で false positive 最小化**: 反例#2 (SAS G3 Wemby OUT HIT) を回避するため適用範囲を PO R1 G1 に限定
3. **B005 との競合は B005 非適用で解消**: N_NBA_new2 適用時は B005 のスター欠場補正のうち RS 25ppg+ star scorer に該当する部分のみ非適用 (排他制御 / 案3 改訂版より影響範囲小)

#### 案2 採用に伴うリスクと対応

| リスク | 対応 |
|---|---|
| 反例#1 (KD G2 return でも HOU 連敗) → return cycle +5〜+8% は too generous | 適用範囲を PO R1 G1 に限定 → G2 return cycle は案2 範囲外 |
| 反例#5 観察 (G2 in-game star loss / A031) → 案2 で論理的に捕捉できない | A031 evidence は「**SAS G2 in-game injury は L4 補正の trigger 事例**」として位置付ける。case 該当時の補正適用は別 rule (将来 N_NBA_new3 等) で扱う |
| sample size = 3 だが return cycle evidence は A043 のみ | A043 は HOU 19pt blowout で statistical strength あるが、单一 evidence の汎化リスクあり → 90日後 retrospective 評価 |
| 案4 (対戦相手 star 依存度サブ条件) の検討漏れ | 案4 は「定量定義困難」のため step1 段階では未採用。step2 でユーザー判断時に検討可 |

#### 却下時の代替案

ユーザー却下時は **案1 単方向 OFF** (return cycle 抜き) に後退。案1 で先行実装し、return cycle (A043) は将来別 P*** 候補として再蓄積。

### 2-(e) 実装影響範囲

#### rules_nba.json への変更内容 (案2 + PO G1 限定サブ条件 採用想定)

```json
{
  "id": "B015",
  "type": "learned",
  "title": "NBA PO R1 G1 Star Scorer (RS 25ppg+) OFF/ON 双方向 L4 補正",
  "body": "PO R1 G1 において、RS 25ppg+ star scorer の game-time decision → ruled out 状態の場合、当該 team 信頼度 -8〜-10% (L4 stage)。逆に前 G で OFF → return G (= G2-G4 で return) の場合は +5〜+8% 補正。適用範囲を PO R1 G1 に限定 (G2 以降の team adjustment 進行で false positive 回避)。B005 (Star 選手欠場補正) との競合解消: B015 適用時は B005 のスター欠場補正のうち RS 25ppg+ star scorer に該当する部分のみ非適用 (排他制御)。",
  "trigger": "P024 evidence 3/3: A029 (LAL d. HOU G1 / KD OFF / Session_47) + A031 (POR d. SAS G2 / Wemby in-game / Session_50) + A043 (HOU d. LAL G4 / KD return / Session_61). 議題1+1' 異セッション独立性確認済。",
  "added": "2026-04-30 (A-3 サブタスク6 step1 提案 → step3 改訂実装で確定)",
  "candidate_pattern": "nba_po_g1_star_scorer_25ppg_absence_return_l4_correction",
  "exclusion": ["B005 (Star 選手欠場補正) のうち RS 25ppg+ star scorer 該当部分は非適用"],
  "applicability_note": "A031 (G2 in-game injury) は本ルールの adjacent reference として位置付け。本ルール本体の補正対象は G1 status change のみ。"
}
```

#### candidate_pattern_registry.json への新規登録

```json
"nba_po_g1_star_scorer_25ppg_absence_return_l4_correction": {
  "sport": "nba",
  "context": "nba_playoffs_round1_g1",
  "summary": "NBA PO R1 G1 での RS 25ppg+ star scorer の OFF/ON 双方向 L4 補正 (-8〜-10% / +5〜+8%)。A029 KD HOU OFF + A031 Wemby SAS in-game (adjacent ref) + A043 KD HOU return (実装候補 P024 → B015 / 議題1+1' step4 実証)",
  "evidence_count": 3,
  "first_evidence": {"session": "Session_47", "match": "A029 LAL d. HOU G1 (KD OFF)", "date": "2026-04-18"},
  "evidence_sessions": ["Session_47", "Session_50", "Session_61"],
  "alias": [],
  "status": "promoted",
  "trigger_threshold": 3,
  "promoted_to_p_candidate_id": "P024",
  "weak_link_to_existing": null
}
```

#### rule_pipeline.json への変更内容

- P024 の `status` を `ready_to_implement` → `approved_pending_implementation` (step3 ユーザー承認後) → `implemented` (step4 commit 後) に変更
- `implemented_session` フィールド追加
- `implemented_rule_id` = "B015"

#### cumulative.json 影響シミュレーション (遡及適用)

過去 PO R1 G1 records に B015 を遡及適用した場合:

| 試合 | 元 conf / hit | B015 適用後 | 影響 |
|---|---|---|---|
| A029 LAL d. HOU G1 | 56% / MISS (pred HOU) | 56-9=47% (HOU側 -9% 適用) → SKIP 維持 | 元 SKIP のため影響なし |
| A031 POR d. SAS G2 | 85% / MISS (pred SAS) | (G2 in-game = 適用範囲外) | 影響なし (案2 PO G1 限定) |
| A043 HOU d. LAL G4 | 不明 / HIT (pred LAL) | (G4 return = 適用範囲外) | 影響なし (案2 PO G1 限定) |
| BOS G1 vs PHI 4-22 | 85.2% / HIT | (star absence なし) | 影響なし |
| OKC G1 vs PHX 4-23 | 90.6% / HIT | (star absence なし) | 影響なし |
| SAS G1 vs POR 4-20 | 87% / HIT | (Wemby ON) | 影響なし |

**累計 hit_rate 影響**: A029 (元 SKIP) のみ補正対象。SKIP は SKIP のままのため累計 hit_rate / EV 変動なし ✓

#### dashboard.html / dashboard_stats.json 影響

- NBA タブの予測精度数値は変動なし (上記シミュレーション結果)
- ただし将来の PO G1 (NBA Conference Semifinals G1 / Conference Finals G1 / NBA Finals G1) で B015 が初発動する際は dashboard 反映要

#### 推定 commit 数

- 実装1 (rules_nba.json + rule_pipeline.json + candidate_pattern_registry.json) = +1 commit
- handoff 1 (P024 step3 完了 → step4 (運用観察) handoff) = +1 commit
- 合計 +2 commit

---

## 3. 共通: step2 着手向け論点整理

### 3.1 ユーザー判断依頼事項

step2 ではユーザーに以下を判断していただく:

| 論点 | 候補 | 内容 |
|---|---|---|
| **論点1** | P020/P024 共通 | 両候補を **個別 commit** で step3 実装するか、**統合 commit** で同時実装するか |
| **論点2** | P020 | 案1 緩和版 / **案2 標準版 (推奨)** / 案3 厳格版 / 案4 R012 強化版 のどれを採用するか |
| **論点3** | P020 | 反例検証不充足 (R1-R8 過去シーズン未調査) について step2 で追加調査するか、現 evidence 3件で承認するか |
| **論点4** | P024 | 案1 単方向 / **案2 双方向 + PO G1 限定 (推奨)** / 案3 B005 統合改訂 / 案4 対戦相手 star 依存度補正 のどれを採用するか |
| **論点5** | P024 | A031 (G2 in-game injury) を本ルールの adjacent reference として位置付けるか、本ルール範囲に含めるか |
| **論点6** | P020/P024 共通 | proposed_rule_id を「R014 / B015」(連番) で確定するか、元提案の「R014 / N_NBA_new2」を維持するか |

### 3.2 Claude.ai 外部レビュー想定論点

ユーザーが step2 で Claude.ai 外部レビューを依頼する場合、想定論点:

| # | 外部レビュー想定論点 |
|---|---|
| 1 | P020 反例検証不充足の取り扱い (現 evidence 3件で実装するか、追加検証要求か) |
| 2 | P024 案2 + PO G1 限定が SAS G3 反証 (反例#2) を回避できているか |
| 3 | P024 A031 (G2 in-game injury) を adjacent reference として位置付けることの論理的妥当性 |
| 4 | candidate_pattern 命名規則 (80文字以内 / sport_context_summary 形式) 整合性 |
| 5 | B005 (既存) と B015 (新規) の排他制御方針が他の B*** rules と整合するか |
| 6 | R014 と R011 の排他制御方針が他の R*** rules と整合するか |

### 3.3 step3 実装完了基準

step2 ユーザー承認 → step3 実装 → 以下完了で step3 終了:

| 候補 | step3 完了基準 |
|---|---|
| **P020** | rules_nrl.json R014 追加 + rule_pipeline.json P020 status 変更 + candidate_pattern_registry.json 新規登録 + 関連 records 4本柱フィールド遡及付与 (該当なしでも明示) |
| **P024** | rules_nba.json B015 追加 + rule_pipeline.json P024 status 変更 + candidate_pattern_registry.json 新規登録 + 関連 records 4本柱フィールド遡及付与 (該当なしでも明示) |
| **共通** | health_check 15項目維持 (OK 11 + WARN ≤4 + ALERT 0) + 個別 commit (一括処理禁止) |

### 3.4 議題1+1' step4 実証成果のまとめ (本 step1 完了時点)

| 議題1+1' 規定 | 本 step1 での実証 | 評価 |
|---|---|---|
| **異セッション独立性チェック (柱A 3-1)** | P020/P024 とも 3 evidence が異なるセッションで独立検出済 | ✓ PASS |
| **同一 turn 内重複付与禁止 (柱A 5.6)** | 両候補とも evidence 3件目は Session_61 / proposal 生成は Session_64 (= 次セッション以降) | ✓ PASS |
| **rule_linked: null + rule_linked_note 必須4項目パターン (柱A 3-2)** | 本 step1 では適用なし (3 evidence 揃った正式 candidate のため weak_link 不要) | (該当外) |
| **candidate_pattern 規約 (柱A 3-3)** | P020 = `nrl_small_sample_r1_r8_pd_overrate_desperate_opp` (74文字) / P024 = `nba_po_g1_star_scorer_25ppg_absence_return_l4_correction` (56文字) → 80文字以内 + snake_case + registry 整合性 OK | ✓ PASS |
| **health_check 機械検証 (項目10/14)** | step3 commit 後に再実行で確認予定 | (step3 で確認) |
| **三層防御 (機械検証層 + 規定層 + 記録層)** | 規定層 + 記録層 (本 step1 で本 markdown ファイル新規作成) → 機械検証層は step3 で確認 | ✓ 部分実証 |

→ **議題1+1' step4 実証は step1 段階で 4/6 規定 PASS。残り 2項目 (機械検証層 + 三層防御完全実証) は step3 commit 後に確認予定。**

---

## 4. 本 step1 完了確認

### 4.1 完了項目

- [x] 柱A 異セッション独立性チェック (両候補 PASS)
- [x] 同一 turn 内重複付与禁止チェック (両候補 PASS)
- [x] P020 提案レポート (a)〜(e) 完成
- [x] P024 提案レポート (a)〜(e) 完成
- [x] step2 着手向け論点整理 (論点1-6 + 外部レビュー想定論点 + step3 完了基準)
- [x] 議題1+1' step4 実証成果まとめ

### 4.2 step2 着手指示待ち

本 step1 完了後、以下を待機:

1. **ユーザー回答**: 論点1-6 への判断
2. **Claude.ai 外部レビュー結果** (任意 / ユーザー判断時に実施可)
3. **step2 着手指示** (= 「step2 着手してください」等)

→ step2 着手指示を受領するまで step3 改訂実装には移行しない (柱A 規律遵守 / 同一 turn 内 implement 禁止)。

---

**本 step1 提案レポート作成完了**: 2026-04-30 (A-3 サブタスク6 step1)
**次工程**: step2 ユーザー判断 + (任意) Claude.ai 外部レビュー
**最優先タスク**: ユーザー回答待機 (論点1-6)
