"""Session_59: NBA PO R1 G3 完了試合 4件を records に追加"""
import json

fp = 'records/nba/2025-26.json'
with open(fp, encoding='utf-8-sig') as f:
    d = json.load(f)
games = d['games']

new_entries = [
    {
        'date': '2026-04-24',
        'tier': 'skip',
        'caution_type': None,
        'quadrant': 'skip',
        'match': 'Philadelphia 76ers vs Boston Celtics (G3 R1)',
        'home': 'Philadelphia 76ers',
        'away': 'Boston Celtics',
        'l1_metric': 'NRtg diff',
        'l1_data': 'NRtg gap ~6pt fav BOS',
        'predicted_winner': 'Boston Celtics',
        'prediction_confidence': 65,
        'prediction_basis': 'BOS NRtg edge + Tatum return form / PHI G2 home momentum spent',
        'rec': None, 'rec_odds': None, 'ev': None,
        'result': 'Boston Celtics 108-100 Philadelphia 76ers',
        'score': '108-100',
        'prediction_hit': True,
        'hit': None,
        'actual_ev': 0.0,
        'outcome_note': 'BOS 108-100 PHI G3 (Tatum 25 / Brown 25 / Pritchard 15 5x3P bench. Maxey 31 PHI). Q4 clutch BOS 19-12. BOS series 2-1 lead. predicted BOS HIT.',
        'verification_sources': [
            'NBC Sports Boston Celtics-Sixers recap clutch Game 3',
            'NBA.com Boston Celtics vs Philadelphia 76ers Apr 24 2026 Summary 0042500113',
            'CBS Sports gametracker NBA_20260424_BOS@PHI'
        ],
        'session': '_59'
    },
    {
        'date': '2026-04-24',
        'tier': 'skip',
        'caution_type': None,
        'quadrant': 'Q4_upset_watch',
        'match': 'Houston Rockets vs Los Angeles Lakers (G3 R1)',
        'home': 'Houston Rockets',
        'away': 'Los Angeles Lakers',
        'l1_metric': 'NRtg diff',
        'l1_data': 'HOU NRtg edge + home / LAL @3.70 road UPSET watch',
        'predicted_winner': 'Houston Rockets',
        'prediction_confidence': 60,
        'prediction_basis': 'HOU home + KD return / LAL road sweep attempt 2-0',
        'rec': None, 'rec_odds': None, 'ev': None,
        'result': 'Los Angeles Lakers 112-108 Houston Rockets (OT)',
        'score': '112-108 OT',
        'prediction_hit': False,
        'hit': None,
        'actual_ev': 0.0,
        'outcome_note': 'LAL 112-108 OT HOU G3 (LeBron tied <20s + LAL OT clutch). LAL series 3-0 sweep imminent UPSET. Q4_upset_watch HIT (LAL @3.70 actualized). predicted HOU MISS. KD returned but LAL prevailed - P024 boundary case.',
        'verification_sources': [
            'VAVEL USA Rockets vs Lakers G3 highlights 04/24/2026',
            'NBA.com Lakers vs Rockets Apr 24 Summary 0042500173'
        ],
        'miss_layer': 'L4_External',
        'miss_analysis': 'KD returned G3 but HOU L1 NRtg edge was reversed by LAL veteran clutch + OT 4Q execution. Q4 UPSET series 3-0 sweep imminent MOMENTUM exceeded NRtg gap. A036 candidate.',
        'rule_linked_candidate': 'A036 candidate / P024 boundary case for evaluation',
        'session': '_59'
    },
    {
        'date': '2026-04-24',
        'tier': 'skip',
        'caution_type': None,
        'quadrant': 'Q4_upset_watch',
        'match': 'Portland Trail Blazers vs San Antonio Spurs (G3 R1)',
        'home': 'Portland Trail Blazers',
        'away': 'San Antonio Spurs',
        'l1_metric': 'NRtg diff',
        'l1_data': 'POR home + Wemby OUT (Wembanyama concussion protocol)',
        'predicted_winner': 'Portland Trail Blazers',
        'prediction_confidence': 62,
        'prediction_basis': 'POR home + Wemby OUT (SAS NRtg star-OFF -4pt estimate) / Q4 watch SAS road @1.70',
        'rec': None, 'rec_odds': None, 'ev': None,
        'result': 'San Antonio Spurs 120-108 Portland Trail Blazers',
        'score': '120-108',
        'prediction_hit': False,
        'hit': None,
        'actual_ev': 0.0,
        'outcome_note': 'SAS 120-108 POR G3 (Dylan Harper rookie 27pts, 2H 22pts surge - Q3 12pts + Q4 10pts). POR 1H 65pts double-digit lead -> 2H collapse. SAS series 2-1 lead. predicted POR MISS. Q4_upset_watch (SAS @1.70 road) HIT. P024 counter-evidence: even with Wemby OUT, SAS won via rookie depth.',
        'verification_sources': [
            'NBA.com Trail Blazers Spurs 2026 Playoffs G3 takeaways Dylan Harper',
            'ESPN Spurs 120-108 Trail Blazers Apr 24 Final',
            'Blazers Edge POR ascended then plunged G3'
        ],
        'miss_layer': 'L4_External',
        'miss_analysis': 'Wemby concussion OUT L4 -8 to -10% adjustment justified POR pick, but SAS rookie Dylan Harper (No.2 pick) 27pts career night exceeded the L4 buffer. star scorer absence offset by bench breakout = P024 simple -8/-10% adjustment limit exposed. depth/draft pedigree factor needed.',
        'rule_linked_candidate': 'P024 counter-evidence: simple star OFF -10% adjustment insufficient, replacement quality factor required',
        'session': '_59'
    },
    {
        'date': '2026-04-23',
        'tier': 'skip',
        'caution_type': None,
        'quadrant': 'skip',
        'match': 'New York Knicks vs Atlanta Hawks (G3 R1)',
        'home': 'New York Knicks',
        'away': 'Atlanta Hawks',
        'l1_metric': 'NRtg diff',
        'l1_data': 'NYK NRtg edge + home / ATL series 1-1 momentum',
        'predicted_winner': 'New York Knicks',
        'prediction_confidence': 58,
        'prediction_basis': 'NYK home + L1 NRtg fav. ATL G2 4Q breakout (P028 candidate) tied series 1-1.',
        'rec': None, 'rec_odds': None, 'ev': None,
        'result': 'Atlanta Hawks 109-108 New York Knicks',
        'score': '109-108',
        'prediction_hit': False,
        'hit': None,
        'actual_ev': 0.0,
        'outcome_note': 'ATL 109-108 NYK G3 (McCollum fadeaway 12.5s remaining GWG / McCollum 23 + J.Johnson 24. NYK Anunoby 29 / Brunson 26 / KAT 21). ATL G2 reverse home 18pt early lead -> NYK rally 108-105 with 1:03 left -> McCollum decisive shot. ATL series 2-1 lead. predicted NYK MISS. P028 evidence 2/3 reached.',
        'verification_sources': [
            'NBA.com Knicks-Hawks G3 takeaways CJ McCollum',
            'ABC7 NY NBA Playoffs Knicks lose G3 109-108',
            'Basketball-Reference 202604230ATL.html'
        ],
        'miss_layer': 'L4_External',
        'miss_analysis': 'NYK 4Q execution wavered again (G2 5-22 -> G3 lost lead with 12.5s on McCollum game-winner). McCollum individual outburst + ATL closing experience exceeded NYK home edge. P028 (G2 4Q collapse) extension: home fav 4Q execution decline trend confirmed in G3.',
        'rule_linked_candidate': 'P028 evidence 2/3 reached: G1 home win -> G2 home 4Q collapse -> G3 road clutch. 3rd evidence triggers N_NBA_new4 implementation.',
        'session': '_59'
    }
]

existing_matches = {(g.get('match', ''), g.get('date', '')) for g in games}
added = 0
for ne in new_entries:
    key = (ne['match'], ne['date'])
    if key not in existing_matches:
        games.append(ne)
        added += 1
        print(f'  + ADD: [{ne["date"]}] {ne["match"]} -> {ne["result"]}')
    else:
        print(f'  - SKIP duplicate: {ne["match"]}')

s = d.get('summary', {})
hit_count = sum(1 for ne in new_entries if ne.get('prediction_hit') is True)
miss_count = sum(1 for ne in new_entries if ne.get('prediction_hit') is False)
s['prediction_total'] = s.get('prediction_total', 0) + added
s['prediction_hit'] = s.get('prediction_hit', 0) + hit_count
d['summary'] = s
d['last_updated'] = '2026-04-25'

with open(fp, 'w', encoding='utf-8') as f:
    json.dump(d, f, ensure_ascii=False, indent=2)
print(f'NBA G3 {added} entries added. HIT={hit_count} MISS={miss_count}')
print('summary:', {k: s.get(k) for k in ['prediction_total', 'prediction_hit', 'total', 'hit', 'ev_total']})
