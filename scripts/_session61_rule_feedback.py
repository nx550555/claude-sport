"""Session_61 rule_pipeline + upset_patterns フィードバック反映
今回MISS 4件 (Shelton/Vacherot/Shapovalov/Manly) + Stuttgart draw + HOU streak fade
を該当候補ルールの evidence に加算 + 新規 upset を upset_patterns に登録。
"""
import json

ROOT = 'C:/Users/ohwada/Desktop/claude_sport'

def load(p):
    with open(p,'r',encoding='utf-8') as f: return json.load(f)
def save(p,d):
    with open(p,'w',encoding='utf-8') as f: json.dump(d,f,ensure_ascii=False,indent=2)

# === 1. upset_patterns.json: 新規 UPSET 登録 (A036-A039) ===
fp = f'{ROOT}/stats/upset_patterns.json'
up = load(fp)
new_upsets = [
    {
        "id": "A036",
        "match": "Prizmic D. d. Shelton B. Madrid 2026 R2 4-6 7-6(4) 7-6(5)",
        "date": "2026-04-24",
        "tour": "ATP",
        "tournament": "Mutua Madrid Open 2026",
        "round": "R2",
        "winner": "Prizmic D.",
        "loser": "Shelton B.",
        "market_favorite": "Shelton B.",
        "fav_odds": 1.30,
        "underdog_odds": 3.50,
        "div_pp": 23.0,
        "uf_factors": ["UF02 Q hot streak", "UF04 Shelton 連戦疲労 (Munich SF)", "UFT01 clay specialist matchup"],
        "uf_count": 3,
        "factor_notes": [
            "Prizmic (CRO Q, 18yo) Madrid 本戦進出後初Top10勝利、3h00 marathon",
            "Shelton (No.4 seed Top10) Munich SF 4試合消耗→Madrid R1 Q+R2 = 6試合連続",
            "若手 clay specialist が Top10 サーブ型を 3rd-set TB で崩す",
            "P023 (Top20 サーブ型 vs 若手clay) の 反例 → P023 boundary 明確化に活用"
        ],
        "rule_linked": "R014 candidate (Masters interB2B) / P006 evidence",
        "type": "type_a_underdog_realized",
        "added_session": "_61"
    },
    {
        "id": "A037",
        "match": "Nava E. d. Vacherot V. Madrid 2026 R2",
        "date": "2026-04-24",
        "tour": "ATP",
        "tournament": "Mutua Madrid Open 2026",
        "round": "R2",
        "winner": "Nava E.",
        "loser": "Vacherot V.",
        "market_favorite": "Vacherot V.",
        "fav_odds": 1.55,
        "underdog_odds": 2.40,
        "div_pp": 18.0,
        "uf_factors": ["UF06 home WC効果消失 (海外大会)", "UF04 MC SF 連戦疲労継続"],
        "uf_count": 2,
        "factor_notes": [
            "Vacherot (Monaco home WC, MC SF実績) が Madrid (海外) WC 同士で Nava (USA) に敗北",
            "R017 (home WC + 連続seed撃破モメンタム) は home要件厳格適用が必要",
            "Monaco出身 vs Madrid開催地 不一致 → home要件不成立",
            "MC R32-SF 4試合 → Madrid R1 + R2 = 連戦6試合の疲労蓄積"
        ],
        "rule_linked": "R017 (home要件 strict-define refinement)",
        "type": "type_a_underdog_realized",
        "added_session": "_61"
    },
    {
        "id": "A038",
        "match": "Budkov Kjaer N. d. Shapovalov D. Madrid 2026 R2 (53min straight)",
        "date": "2026-04-25",
        "tour": "ATP",
        "tournament": "Mutua Madrid Open 2026",
        "round": "R2",
        "winner": "Budkov Kjaer N.",
        "loser": "Shapovalov D.",
        "market_favorite": "Shapovalov D.",
        "fav_odds": 1.55,
        "underdog_odds": 2.40,
        "div_pp": 18.0,
        "uf_factors": ["UF04 Munich SF後 連戦疲労", "UF02 18yo Q hot streak", "UF01 Madrid altitude (1500m) ball変化"],
        "uf_count": 3,
        "factor_notes": [
            "Shapovalov: Munich Griekspoor R1 3sets → Munich R2/QF/SF (4勝) → Madrid R1 + R2 = 6試合連続",
            "Budkov Kjaer (NOR Q, 18yo) Roland Garros U21 実績の clay specialist",
            "Madrid 高地 (1500m) で sub-altitude ball change が Shapovalov serve-baseline rhythm 破壊",
            "53分 straight sets = Shapovalov の体力枯渇明白",
            "P006 (Masters→翌週大会 B2B疲弊) decisive evidence 2件目"
        ],
        "rule_linked": "P006 → R014 candidate evidence 2/3",
        "type": "type_a_underdog_realized",
        "added_session": "_61"
    },
    {
        "id": "A039",
        "match": "Parramatta Eels d. Manly Sea Eagles NRL R8 2026 24-18",
        "date": "2026-04-26",
        "tour": "NRL",
        "tournament": "NRL Premiership 2026 Round 8",
        "round": "R8",
        "winner": "Parramatta Eels",
        "loser": "Manly Sea Eagles",
        "market_favorite": "Manly Sea Eagles",
        "fav_odds": 1.37,
        "underdog_odds": 3.10,
        "div_pp": 14.0,
        "uf_factors": ["UF06 Sydney derby rivalry motivation", "UF04 Manly 4Q fade pattern"],
        "uf_count": 2,
        "factor_notes": [
            "Manly Foran新監督就任後 4連勝中 → Eels に終盤逆転負け",
            "残り20分時点 Manly リード → 終盤2トライで Eels 逆転",
            "Sydney NSW derby motivation を L3 で過小評価",
            "1Q-3Q dominance vs 4Q execution の典型パターン",
            "L1 PD/G + home advantage で本命視も 4Q decisive trend を反映できず"
        ],
        "rule_linked": "P020 evidence 3/3 候補 (NRL 小サンプル期 PD/G信頼性ダウン)",
        "type": "type_a_underdog_realized",
        "added_session": "_61"
    },
]
up['confirmed_upsets'].extend(new_upsets)
up['updated'] = '2026-04-27'
up['session'] = '_61'
save(fp, up)
print(f'upset_patterns.json: A036-A039 4件追加 (total={len(up["confirmed_upsets"])})')

# === 2. rule_pipeline.json: evidence 加算 ===
fp = f'{ROOT}/core/rule_pipeline.json'
rp = load(fp)
for c in rp['candidates']:
    cid = c['candidate_id']
    # P006 (Masters→翌週大会 B2B疲弊) +1: Shapovalov A038
    if cid == 'P006':
        c['current_count'] = 2
        c['evidence'].append({
            "id": "A038",
            "match": "Budkov Kjaer N. d. Shapovalov D. Madrid 2026 R2",
            "pattern": "Shapovalov Munich SF (4 matches消耗) → Madrid R1+R2 = 6試合連続。Madrid altitude効果も加わり 53min straight loss。CAUTION予測 MISS。-3% では明確に不足、-7〜-10% 必要。",
            "tag": "atp_b2b_inter_tournament",
            "sources": ["records/tennis/2026-ATP.json [136]", "stats/upset_patterns.json A038"]
        })
        c['note'] += " | [Session_61 2026-04-27] A038 Shapovalov Madrid R2 -> evidence 2/3 到達。次evidence で R014 implement (-7〜-10% 補正)。"
    # P017 (Top100 vet Masters Q R1 motivation) - 今回 evidence 該当なし(本戦)
    # P020 (NRL小サンプル期 PD/G) +1: Manly A039
    if cid == 'P020':
        c['current_count'] = 3
        c['evidence'].append({
            "id": "A039",
            "match": "Parramatta Eels d. Manly Sea Eagles R8 2026-04-26",
            "pattern": "R8 Manly home @1.37 fav (PD +91) -> Eels 逆転 24-18。Manly 4連勝の hot streak が Sydney derby rivalry + 4Q fade で崩壊。PD/G 過大評価 + Eels desperate (1-6) home derby motivation 過小評価。 R8 = 小サンプル期上限。",
            "tag": "nrl_small_sample_pd_unreliable"
        })
        c['note'] += " | [Session_61 2026-04-27] A039 Manly MISS で evidence 3/3 到達 → R014 implement 判断: R1-R8 NRL + PD差6pt以上 + 対戦相手 desperate (≤2-6 record) → 信頼度上限78% + 追加-5%。"
        c['status'] = 'ready_to_implement'
    # P010 already implemented as R017 - need refinement note
    if cid == 'P010':
        c['note'] += " | [Session_61 2026-04-27] A037 Vacherot Madrid R2 MISS で R017 home要件 strict-define が必要と判明。R017 の home要件は『大会開催地と選手出身地の正確一致』のみとし、隣接国・地域は home扱いしない。Vacherot (Monaco) は MC のみ home、Madrid/Rome等では home扱いしない。R017 v2 として rules_tennis.json に注記追加。"

# 新規候補 P030: Madrid 高地 (altitude) compound fatigue 補正
new_candidate_p030 = {
    "candidate_id": "P030",
    "status": "watching",
    "target_rule_file": "core/rules_tennis.json",
    "proposed_rule_id": "R024",
    "title": "Madrid altitude (1500m) + Masters interB2B 重複ペナルティ",
    "description": "Madrid Masters は 1500m 高地でボール飛距離増・サーブ威力増・ラリー長期化。Munich/Estoril 等 sea-level 大会から直行する選手は altitude adaptation 24-48時間必要。Masters interB2B (R005疲労) と altitude effect が重なると本命崩壊リスク顕著。Munich SF以上経験後の Madrid R1/R2: 信頼度 -5〜-8% 補正検討。",
    "trigger_threshold": 3,
    "current_count": 1,
    "evidence": [{
        "id": "A038",
        "match": "Budkov Kjaer d. Shapovalov Madrid 2026 R2 53min straight",
        "pattern": "Shapovalov Munich SF (4 wins) -> Madrid R2 53min straight loss。altitude + interB2B 同時適用で本命崩壊。",
        "tag": "atp_madrid_altitude_b2b_compound"
    }],
    "tag_matches": ["atp_madrid_altitude_b2b_compound", "atp_b2b_inter_tournament"],
    "note": "Madrid Masters 期間中の Munich/Estoril/Marrakech 大会通過選手で2件目を観察。Indian Wells (700m) 同様の altitude 影響大会群と統合可能。"
}
# 新規候補 P031: Bundesliga mid-table low-block draw 巻き込み
new_candidate_p031 = {
    "candidate_id": "P031",
    "status": "watching",
    "target_rule_file": "core/rules_soccer.json",
    "proposed_rule_id": "S_new1",
    "title": "Bundesliga mid-table low-block チームの home draw 巻き込み補正",
    "description": "CL争いするチームが mid-table 下位 (15-17位圏) low-block 守備戦術相手と home対戦する場合、xGD 差で本命視しても 1-1 等のドローに巻き込まれるパターン。home pressure過多 + low-block defensive solidity の組合せ。CAUTION_MARGIN 信頼度 -3〜-5% 補正。Bundesliga 特化 (リーグ性質: 下位チームの守備規律高い)。",
    "trigger_threshold": 3,
    "current_count": 1,
    "evidence": [{
        "id": "Stuttgart_Bremen_draw",
        "match": "VfB Stuttgart 1-1 Werder Bremen Bundesliga MD31 2026-04-26",
        "pattern": "Stuttgart CL争い home @1.55 fav -> Bremen low-block ドロー巻込。Bremen 18'先制 -> Stuttgart 61' 同点で push する形に。Stuttgart home pressure 過多 + Bremen defensive shape の典型ドロー。",
        "tag": "bundesliga_mid_table_low_block_draw"
    }],
    "tag_matches": ["bundesliga_mid_table_low_block_draw", "soccer_home_pressure_excess"],
    "note": "Bundesliga 特有パターン (下位チームの守備規律 + Premier League/La Liga と異なる home advantage 計算)。3件で実装。"
}
# 新規候補 P032: MLB winning streak fade
new_candidate_p032 = {
    "candidate_id": "P032",
    "status": "watching",
    "target_rule_file": "core/rules_mlb.json",
    "proposed_rule_id": "M_new1",
    "title": "MLB 連勝 8試合以上 streak の終戦 fade 補正",
    "description": "MLB チーム連勝が 8試合以上に達した翌試合で、相手 home + 相手 SP 良好(<3.00 ERA) の場合、streak fade による 信頼度 -4〜-6% 補正。L1 Savant xwOBA 差より SP matchup × streak fatigue が decisive となる。",
    "trigger_threshold": 3,
    "current_count": 1,
    "evidence": [{
        "id": "HOU_NYY_4_26",
        "match": "Houston Astros 7-4 New York Yankees 2026-04-26",
        "pattern": "Yankees 8連勝中 → Astros home (Daikin Park) で 7-4 敗戦。Astros Arrighetti SP (2-0 2.45ERA) 好投。streak fade + opposing home SP advantage パターン。CAUTION_MARGIN 予測 MISS。",
        "tag": "mlb_winning_streak_fade"
    }],
    "tag_matches": ["mlb_winning_streak_fade", "mlb_streak_8_plus_regression"],
    "note": "MLB 6-7試合 streak の fade率 (歴史的 ~50%) より長期streakの方が fade率高い特徴。3件で実装。"
}
# 新規候補 P033: NRL Sydney derby 4Q reversal
new_candidate_p033 = {
    "candidate_id": "P033",
    "status": "watching",
    "target_rule_file": "core/rules_nrl.json",
    "proposed_rule_id": "R015",
    "title": "NRL Sydney derby + desperate underdog の 4Q reversal 補正",
    "description": "NRL の Sydney NSW derby (Manly/Parramatta/Roosters/Rabbitohs/Bulldogs/Tigers 等の同地域対決) で、underdog が 1-5/2-5 等 desperate record の場合、終盤4Q (60分以降) の execution edge で逆転するパターン。L3 ステージで -3〜-5% home fav 信頼度補正。Manly @1.37 fav -> Eels 24-18 逆転は典型例。",
    "trigger_threshold": 3,
    "current_count": 1,
    "evidence": [{
        "id": "A039",
        "match": "Parramatta Eels 24-18 Manly Sea Eagles R8 2026-04-26",
        "pattern": "Sydney derby + Eels desperate record + Manly 4連勝 hot streak の3条件揃う。残り20分時点 Manly リード → 終盤2トライで Eels 逆転。",
        "tag": "nrl_sydney_derby_4q_reversal"
    }],
    "tag_matches": ["nrl_sydney_derby_4q_reversal", "nrl_desperate_underdog_late_game"],
    "note": "NSW derby 特有パターン。3件で R015 実装: Sydney derby + desperate record (≤2-6) + late-game home fav fade -> -5%補正。"
}
rp['candidates'].extend([new_candidate_p030, new_candidate_p031, new_candidate_p032, new_candidate_p033])
rp['last_updated'] = '2026-04-27'
rp['updated_session'] = '_61'
save(fp, rp)
print('rule_pipeline.json: P006/P020 evidence更新, P010 note強化, 新規 P030/P031/P032/P033 4件追加')
print(f'  P006 -> 2/3 (Shapovalov A038)')
print(f'  P020 -> 3/3 (Manly A039) ready_to_implement')
print(f'  P030 NEW: Madrid altitude+B2B compound (1/3)')
print(f'  P031 NEW: Bundesliga mid-table low-block draw (1/3)')
print(f'  P032 NEW: MLB 8+streak fade (1/3)')
print(f'  P033 NEW: NRL Sydney derby 4Q reversal (1/3)')
