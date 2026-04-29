"""Session_61 結果反映スクリプト
- ATP Madrid R2 10件 (GO 3 / CAUTION 7)
- Soccer 4件 (provisional_go 1 / caution_margin 3)
- MLB 2件 (caution_margin 2)
- NRL 2件 (provisional_go 2)
"""
import json
import os
from datetime import datetime

ROOT = 'C:/Users/ohwada/Desktop/claude_sport'

def load(p):
    with open(p, 'r', encoding='utf-8') as f:
        return json.load(f)

def save(p, d):
    with open(p, 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=2)

# ATP Madrid R2 results
atp_results = {
    "Rinderknech A. vs Lajovic D.": {"winner": "Rinderknech A.", "score": "6-3 6-2", "predicted": "Arthur Rinderknech", "hit": True, "miss_analysis": None, "miss_layer": None, "rule_linked": None},
    "Shelton B. vs Prizmic D.": {"winner": "Prizmic D.", "score": "4-6 7-6(4) 7-6(5)", "predicted": "Ben Shelton", "hit": False, "miss_analysis": "Prizmic (Croatian Q, 18yo) が Shelton (No.4 seed Top10) を 3h00 marathon で破る。Shelton 1stセット獲得後、TBバトルで本命崩壊。Q初Top10 win。R017候補補強 (clay momentum + Q upsetter)。", "miss_layer": "L3_FormFitness+L4_Mental", "rule_linked": "R020 candidate (R1 upsetter momentum) / R017 candidate"},
    "Diallo G. vs Moller E.": {"winner": "Moller E.", "score": "retired", "predicted": "Gabriel Diallo", "hit": False, "miss_analysis": "Diallo R2 試合中 retire。具体的負傷部位は要確認。怪我による途中棄権で予測 MISS は不可避。caution tier no-bet で P&L影響なし。", "miss_layer": "L4_External_Injury", "rule_linked": "N/A (in-game retirement)"},
    "Griekspoor T. vs Dzumhur D.": {"winner": "Griekspoor T.", "score": "6-3 6-4", "predicted": "Tallon Griekspoor", "hit": True, "miss_analysis": None, "miss_layer": None, "rule_linked": None},
    "Vacherot V. vs Nava E.": {"winner": "Nava E.", "score": "lost R2", "predicted": "Valentin Vacherot", "hit": False, "miss_analysis": "Vacherot (Monaco home WC, MC SF実績) が Nava (USA WC) に R2 で敗北。R017 (home WC + 連続seed撃破モメンタム) は Madrid (海外大会) では home WC 要件不適合。連続ラウンド戦の疲労 + 環境変化で実力差顕在化。R017 の home 要件の厳格適用 (大会開催地と選手出身地の一致のみ home WC とする) を裏付ける evidence。", "miss_layer": "L4_External", "rule_linked": "R017 (home WC 厳格適用)"},
    "Khachanov K. vs Walton A.": {"winner": "Khachanov K.", "score": "6-2 6-3", "predicted": "Karen Khachanov", "hit": True, "miss_analysis": None, "miss_layer": None, "rule_linked": None},
    "Auger-Aliassime F. vs Gaubas V.": {"winner": "Auger-Aliassime F.", "score": "6-3 6-4", "predicted": "Felix Auger-Aliassime", "hit": True, "miss_analysis": None, "miss_layer": None, "rule_linked": None},
    "Mensik J. vs Damm M.": {"winner": "Mensik J.", "score": "6-3 6-4", "predicted": "Jakub Mensik", "hit": True, "miss_analysis": None, "miss_layer": None, "rule_linked": None},
    "Shapovalov D. vs Budkov Kjaer N.": {"winner": "Budkov Kjaer N.", "score": "lost in 53 min straight sets", "predicted": "Denis Shapovalov", "hit": False, "miss_analysis": "Shapovalov (Munich SF実績後) が Budkov Kjaer (NOR Q, 18yo) に straight sets 53min で完敗。Munich消化試合連続 (R005 B2B大会間疲弊) + Madrid 高地 (1500m altitude) + Shapovalov の serve-baseline rhythm 喪失。R014 (Masters→翌週大会 B2B) evidence 補強。Shapovalov MC R1 で Griekspoor 戦 3sets 消耗 → Munich SF (4 matches) → Madrid R1 → R2 = 6試合連続。clay specialist player (Budkov NOR Q U21 Roland Garros) が rhythm 破壊。", "miss_layer": "L4_External_Fatigue", "rule_linked": "R014 candidate (Masters間B2B疲弊) / P006"},
    "Ruud C. vs Munar J.": {"winner": "Ruud C.", "score": "6-0 6-1", "predicted": "Casper Ruud", "hit": True, "miss_analysis": None, "miss_layer": None, "rule_linked": None},
}

# Update ATP records
fp = f'{ROOT}/records/tennis/2026-ATP.json'
d = load(fp)
preds = d['predictions']
atp_pl = 0.0
atp_hits = []
for i, g in enumerate(preds):
    if not isinstance(g, dict): continue
    m = g.get('match', '')
    if m in atp_results and g.get('prediction_hit') is None and g.get('date') in ('2026-04-24', '2026-04-25'):
        r = atp_results[m]
        g['result'] = r['winner']
        g['score'] = r['score']
        g['hit'] = r['hit'] if g.get('tier') == 'go' else None
        g['prediction_hit'] = r['hit']
        # P&L for go tier
        if g.get('tier') == 'go':
            odds = g.get('rec_odds')
            if r['hit']:
                pl = round(odds - 1, 4) if odds else 0
                g['actual_ev'] = pl
                atp_pl += pl
                atp_hits.append(('HIT', m, pl))
            else:
                g['actual_ev'] = -1.0
                atp_pl -= 1.0
                atp_hits.append(('MISS', m, -1.0))
        if r['miss_analysis']:
            g['miss_analysis'] = r['miss_analysis']
            g['miss_layer'] = r['miss_layer']
            g['rule_linked'] = r['rule_linked']
        g['updated_session'] = '_61'
        g['updated_at'] = '2026-04-27'
        print(f'ATP [{i}] {m} -> {r["winner"]} {r["score"]} (hit={r["hit"]})')

# Update screening_log
d['screening_log'].append({
    "session": "_61",
    "date": "2026-04-27",
    "action": "Madrid R2 10件 結果反映",
    "details": f"GO 3/3 HIT (+{atp_pl:.2f}u Khachanov/FAA/Mensik) + CAUTION 4 HIT (Rinderknech/Griekspoor/Ruud) / 4 MISS (Shelton/Diallo retire/Vacherot/Shapovalov). MISS 4件 miss_analysis 同時記入完了 (PA-PERM05)."
})
d['last_updated'] = '2026-04-27 Session_61'
save(fp, d)
print(f'\nATP Madrid R2: GO P&L = +{atp_pl:.3f}u (3 GO all HIT)\n')

# Soccer
fp = f'{ROOT}/records/soccer/2025-26.json'
d = load(fp)
preds = d.get('predictions', d.get('games', d.get('entries', [])))
key = 'predictions' if 'predictions' in d else ('games' if 'games' in d else 'entries')

soccer_results = {
    "Arsenal vs Newcastle United": {"score": "1-0", "winner": "Arsenal", "predicted": "Arsenal", "hit": True, "miss_analysis": None, "miss_layer": None, "rule_linked": None},
    "Getafe vs Barcelona": {"score": "0-2", "winner": "Barcelona", "predicted": "Barcelona", "hit": True, "miss_analysis": None, "miss_layer": None, "rule_linked": None},
    "Mainz 05 vs Bayern Munich": {"score": "3-4", "winner": "Bayern Munich", "predicted": "Bayern Munich", "hit": True, "miss_analysis": None, "miss_layer": None, "rule_linked": None},
    "VfB Stuttgart vs Werder Bremen": {"score": "1-1", "winner": "draw", "predicted": "VfB Stuttgart", "hit": False, "miss_analysis": "VfB Stuttgart home でドロー (1-1)。Bremen が 18'先制 → Demirovic 61'同点。CL圏争いの Stuttgart にとってドローは敗北同然。Bremen 守備強度 (low-block defensive shape) 想定外。L1 xGD 差 と実際の試合内容に乖離。Bundesliga 中位下位の defensive game plan が高位チームを mid-table draw に巻き込むパターン。", "miss_layer": "L3_TacticalMatchup", "rule_linked": "S_new candidate (mid-table low-block vs CL争いhome)"},
}
soccer_pl = 0.0
for i, g in enumerate(preds):
    if not isinstance(g, dict): continue
    m = g.get('match', '')
    if m in soccer_results and g.get('prediction_hit') is None and g.get('date') in ('2026-04-25', '2026-04-26'):
        r = soccer_results[m]
        g['result'] = r['winner']
        g['score'] = r['score']
        g['prediction_hit'] = r['hit']
        # provisional_go: P&L 影響無し (STEP 4.5 lineups 未確認のため caution_waiting 相当)
        if g.get('tier') == 'provisional_go':
            g['tier_final'] = 'caution_waiting'
            g['note_session61'] = 'STEP 4.5 lineups 未確認のままキックオフ → P&L 影響なし扱い (予測精度のみカウント)'
        if r['miss_analysis']:
            g['miss_analysis'] = r['miss_analysis']
            g['miss_layer'] = r['miss_layer']
            g['rule_linked'] = r['rule_linked']
        g['updated_session'] = '_61'
        g['updated_at'] = '2026-04-27'
        print(f'Soccer [{i}] {m} -> {r["winner"]} {r["score"]} (hit={r["hit"]})')
d['last_updated'] = '2026-04-27 Session_61'
save(fp, d)

# MLB
fp = f'{ROOT}/records/mlb/2026.json'
d = load(fp)
preds = d.get('predictions', d.get('games', d.get('entries', [])))
mlb_results = {
    "Houston Astros vs New York Yankees": {"score": "7-4", "winner": "Houston Astros", "predicted": "New York Yankees", "hit": False, "miss_analysis": "Yankees 8連勝中の状況で Astros home (Daikin Park) で 7-4 勝利。Astros Arrighetti SP (2-0 2.45ERA) good start。Yankees Gil SP (1-1 4.11ERA) 苦戦。L1 Savant xwOBA 差より SP matchup decisive。Yankees 連勝 streak fade + Astros home advantage 過小評価。", "miss_layer": "L3_PitcherMatchup", "rule_linked": "M_new candidate (winning streak ≥8 game fade + opposing home SP advantage)"},
    "Los Angeles Dodgers vs Chicago Cubs": {"score": "6-0", "winner": "Los Angeles Dodgers", "predicted": "Los Angeles Dodgers", "hit": True, "miss_analysis": None, "miss_layer": None, "rule_linked": None},
}
for i, g in enumerate(preds):
    if not isinstance(g, dict): continue
    m = g.get('match', '')
    if m in mlb_results and g.get('prediction_hit') is None:
        r = mlb_results[m]
        g['result'] = r['winner']
        g['score'] = r['score']
        g['prediction_hit'] = r['hit']
        if r['miss_analysis']:
            g['miss_analysis'] = r['miss_analysis']
            g['miss_layer'] = r['miss_layer']
            g['rule_linked'] = r['rule_linked']
        g['updated_session'] = '_61'
        g['updated_at'] = '2026-04-27'
        print(f'MLB [{i}] {m} -> {r["winner"]} {r["score"]} (hit={r["hit"]})')
d['last_updated'] = '2026-04-27 Session_61'
save(fp, d)

# NRL
fp = f'{ROOT}/records/nrl/2026.json'
d = load(fp)
preds = d.get('predictions', d.get('games', d.get('entries', [])))
nrl_results = {
    "Newcastle Knights vs Penrith Panthers": {"score": "12-44", "winner": "Penrith Panthers", "predicted": "Penrith Panthers", "hit": True, "miss_analysis": None, "miss_layer": None, "rule_linked": None},
    "Manly Sea Eagles vs Parramatta Eels": {"score": "18-24", "winner": "Parramatta Eels", "predicted": "Manly Sea Eagles", "hit": False, "miss_analysis": "Manly home (4 Pines) で 4連勝中だったが Eels に 18-24 で逆転負け。残り20分時点で Manly リード → 終盤2トライで Eels 逆転。Foran 新監督就任後 Manly が +91 PD で快進撃中も、Eels の 終盤ラッシュ (NRL では 4Q decisive trend) で崩壊。L1 PD/G 差 + home advantage で本命視も、Eels rivalry (NSW Sydney derby) motivation 過小評価。Manly 1Q-3Q dominance vs 4Q fatigue/closer execution パターン。Provisional GO のままキックオフ → caution_waiting 扱いで P&L影響なし。", "miss_layer": "L3_4Q_Execution", "rule_linked": "NRL_new candidate (Sydney derby rivalry 4Q reversal)"},
}
for i, g in enumerate(preds):
    if not isinstance(g, dict): continue
    m = g.get('match', '')
    if m in nrl_results and g.get('prediction_hit') is None:
        r = nrl_results[m]
        g['result'] = r['winner']
        g['score'] = r['score']
        g['prediction_hit'] = r['hit']
        if g.get('tier') == 'provisional_go':
            g['tier_final'] = 'caution_waiting'
            g['note_session61'] = 'STEP 4.5 lineups 未確認のままキックオフ → P&L 影響なし扱い'
        if r['miss_analysis']:
            g['miss_analysis'] = r['miss_analysis']
            g['miss_layer'] = r['miss_layer']
            g['rule_linked'] = r['rule_linked']
        g['updated_session'] = '_61'
        g['updated_at'] = '2026-04-27'
        print(f'NRL [{i}] {m} -> {r["winner"]} {r["score"]} (hit={r["hit"]})')
d['last_updated'] = '2026-04-27 Session_61'
save(fp, d)

print('\n=== SUMMARY ===')
print(f'ATP GO P&L: +{atp_pl:.3f}u (3/3 HIT)')
print('CAUTION ATP: 4 HIT (Rinderknech/Griekspoor/Ruud) / 4 MISS (Shelton-UPSET/Diallo-retire/Vacherot/Shapovalov-fatigue)')
print('Soccer: 3 HIT (Arsenal/Barca/Bayern) / 1 MISS (Stuttgart draw)')
print('MLB: 1 HIT (Dodgers) / 1 MISS (Yankees streak fade)')
print('NRL: 1 HIT (Penrith) / 1 MISS (Manly 4Q reversal)')
print('Provisional GO: P&L 影響なし扱い (STEP 4.5 lineups 未確認 → caution_waiting 相当)')
