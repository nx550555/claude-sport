# -*- coding: utf-8 -*-
import json
from pathlib import Path
p = Path(r'C:\Users\ohwada\Desktop\claude_sport\stats\upset_patterns.json')
d = json.loads(p.read_text(encoding='utf-8-sig'))

ID_MAP = {
    22: 'A014', 23: 'A015', 24: 'A016', 25: 'A018', 26: 'A019',
    27: 'A020', 28: 'A025', 29: 'A026', 30: 'A027', 31: 'A028',
}

for i, u in enumerate(d.get('confirmed_upsets', [])):
    if i in ID_MAP and u.get('id') in (None, 'NONE', ''):
        u['id'] = ID_MAP[i]
        print(f'[{i}] id -> {ID_MAP[i]}')

for u in d.get('confirmed_upsets', []):
    uid = u.get('id')
    if uid == 'A026':
        u.setdefault('date', '2026-04-19')
        u.setdefault('round', 'PO R1 G1')
        u.setdefault('result_score', 'ORL 112-101 DET')
        u.setdefault('actual_winner', 'Orlando Magic')
        u.setdefault('favorite_market', 'Detroit Pistons @1.22 (home #1 seed E)')
        u.setdefault('underdog_market', 'Orlando Magic @4.60')
        u.setdefault('upset_factors', ['UF02', 'UF06', 'UFA03'])
        u.setdefault('factor_notes', {
            'UF02': 'Banchero 23/9 breakout (P022 evidence). Wagner efficient scoring.',
            'UF06': 'DET young core (Cunningham 24yo) PO inexperience vs ORL prior R1 PO (2024) experience.',
            'UFA03': 'Only road G1 win across NBA 4/19 slate - isolated game situation.'
        })
        u.setdefault('rule_linked', 'P022 NBA PO G1 playoff experience gap')
        u.setdefault('sources', [
            'NBA.com live-updates playoffs R1',
            'Tucson.com winners-losers Magic stun top-seeded'
        ])
        u.setdefault('miss_layer', 'L4_External')
        print('A026 enriched')

    if uid == 'A027':
        u['date'] = '2026-04-19'
        u['round'] = 'PO R1 G1'
        u['result_score'] = 'PHI 3-2 PIT'
        u['actual_winner'] = 'Philadelphia Flyers'
        u['favorite_market'] = 'Pittsburgh Penguins @1.67 (home M2)'
        u['underdog_market'] = 'Philadelphia Flyers @2.17'
        u['upset_factors'] = ['UF02', 'UF06', 'UFH01']
        u['factor_notes'] = {
            'UF02': 'PHI young energy (Drysdale 1G, Martone 1G) + Vladar G work vs PIT veteran core (Crosby 0pt, Malkin 1G).',
            'UF06': 'PIT RS late 20G xGF down-trend + Crosby/Malkin veteran-heavy fatigue。PHI rivalry momentum + road PO first game energy。',
            'UFH01': 'Rivalry PO G1 where home favorite veteran core historically fades (Metropolitan div).'
        }
        u['rule_linked'] = 'P019 NHL PO G1 rivalry + home favorite late-season fade'
        u['sources'] = [
            'ESPN gameId 401869717 Flyers 3-2 Penguins',
            'PensBurgh Penguins/Flyers Game 1 Recap',
            'Broad Street Hockey takeaways'
        ]
        u['miss_layer'] = 'L4_External'
        print('A027 enriched')

    if uid == 'A028':
        u['date'] = '2026-04-19'
        u['round'] = 'PO R1 G1'
        u['result_score'] = 'MIN 6-1 DAL'
        u['actual_winner'] = 'Minnesota Wild'
        u['favorite_market'] = 'Dallas Stars @1.82 (home C2)'
        u['underdog_market'] = 'Minnesota Wild @1.96'
        u['upset_factors'] = ['UF01', 'UF02', 'UFH02']
        u['factor_notes'] = {
            'UF01': 'MIN xGF% 51.50 > DAL 50.79 (lower seed process advantage - type_a_watch 事前警告 adequate).',
            'UF02': 'Kaprizov+Boldy 40G teammates explosion + Eriksson Ek 2G PP + Hartman 1G + Zuccarello 3A。2nd P 6.5min で 4-0。',
            'UFH02': 'DAL home が MIN 特殊攻勢構造 (PP強 + forward depth) に崩壊。Wallstedt PO debut 27sv 完敗。'
        }
        u['rule_linked'] = 'N001 xGF% L1 signal type_a_watch 警告の有効性確認'
        u['sources'] = [
            'ESPN gameId 401869716 Wild 6-1 Stars',
            'NHL.com wild minnesota-wild-dallas-stars-game-1-recap',
            'The Hockey Writers 3-takeaways-from-stars-stunning-6-1-loss'
        ]
        u['miss_layer'] = 'L1_xGF'
        u['type_a_insight'] = 'seed順位より xGF% 順位を優先すべし。type_a_watch 事前警告が正しかった - predicted_winner 選択時のルール改善が必要 (下記 rule_candidate)。'
        u['rule_candidate'] = 'N_new_xgf_priority: L1 xGF% higher team > seed ranking。type_a_watch 発動時は higher xGF% team を predicted_winner に自動設定。'
        print('A028 enriched')

# Check A029 not already present
ids_existing = {u.get('id') for u in d.get('confirmed_upsets', [])}
if 'A029' not in ids_existing:
    a029 = {
        'id': 'A029',
        'type': 'type_a',
        'type_note': 'Type A: SKIP no-bet のアップセット。star選手G1欠場がL1/L4に反映されず MISS。',
        'date': '2026-04-18',
        'sport': 'nba',
        'round': 'PO R1 G1',
        'our_verdict': 'SKIP (conf 56% / EV -5.93% / 予測 HOU)',
        'favorite_market': 'Houston Rockets @1.43 (home W2, Durant RS 26.0ppg)',
        'underdog_market': 'Los Angeles Lakers @2.75 (W7)',
        'result_score': 'LAL 107-98 HOU',
        'actual_winner': 'Los Angeles Lakers',
        'upset_factors': ['UF05', 'UFA02', 'UFA04'],
        'factor_notes': {
            'UF05': 'Kevin Durant (HOU star RS 26.0ppg) G1 欠場 (right knee patellar tendon contusion, 火曜練習負傷)。pre-game warmup 後 ruled out。',
            'UFA02': 'Luke Kennard playoff career-high 27pts 爆発で short-handed LAL でも十分。',
            'UFA04': 'L1 NRtg 3.5pt diff は Durant 前提値 → 欠場で実質 -3〜-4pt 下方修正 → coin flip に変化。'
        },
        'screening_decision_review': 'SKIP 判断 OK (EV-5.93%) だが predicted_winner を HOU にしたのが誤り。Durant 欠場情報は NBA injury report / ESPN で game-day 取得可能だった。',
        'rule_candidate': 'N_NBA_new2: NBA PO G1 star scorer (>25ppg RS) 欠場時、star-heavy チーム信頼度 -8〜-10% 補正。Durant級欠場は実質 NRtg 1-4pt 下方修正。',
        'miss_layer': 'L4_External',
        'sources': [
            'ESPN gameId 401869190 Lakers 107-98 Rockets',
            'ESPN rockets kevin-durant-g1-vs-lakers-knee-contusion',
            'NBA.com rockets-lakers-2026-playoffs-game-1-takeaways',
            'CBS Sports kevin-durant-injury-rockets-lakers-analysis'
        ],
        'rule_linked': 'P024 NEW (NBA PO star scorer absence L4 correction)'
    }
    d.setdefault('confirmed_upsets', []).append(a029)
    print('A029 added')

d['confirmed_count'] = len(d['confirmed_upsets'])
d['last_updated'] = '2026-04-21'
d['updated_session'] = '_47'

sb = {}
for u in d['confirmed_upsets']:
    s = u.get('sport', 'unknown')
    sb[s] = sb.get(s, 0) + 1
d['sport_breakdown'] = sb
print('sport_breakdown:', sb)

p.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding='utf-8')
print('\n[OK] saved. total confirmed =', d['confirmed_count'])
