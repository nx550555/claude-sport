# -*- coding: utf-8 -*-
import json
from pathlib import Path
p = Path(r'C:\Users\ohwada\Desktop\claude_sport\core\rule_pipeline.json')
d = json.loads(p.read_text(encoding='utf-8-sig'))

cands = d.get('candidates', [])
added_evidence = 0

for c in cands:
    cid = c.get('candidate_id')
    # P018: NHL PO G1 underdog young core activation — add A027 PHI evidence
    if cid == 'P018':
        # Already has A021 MTL. Add A027 PHI young energy
        existing_ids = {e.get('id') for e in c.get('evidence', [])}
        if 'A027' not in existing_ids:
            c['evidence'].append({
                'id': 'A027',
                'match': 'Philadelphia Flyers d. Pittsburgh Penguins PO R1 G1 2026-04-18',
                'pattern': 'PHI young energy (Drysdale/Martone 各1G, Vladar G) vs PIT veteran (Crosby 0pt). home favorite @1.67 MISS. P018/P019 重複適合。',
                'tag': 'nhl_po_g1_young_core_activation',
                'sources': [
                    'ESPN gameId 401869717',
                    'PensBurgh Recap'
                ]
            })
            c['current_count'] = len(c['evidence'])
            added_evidence += 1
            print(f'P018 evidence +1 -> {c["current_count"]}/{c["trigger_threshold"]}')

    # P019: NHL PO G1 rivalry + home favorite late-season fade — enrich A027 entry
    if cid == 'P019':
        # evidence[0] is already A027 entry but may need factor detail update
        for e in c.get('evidence', []):
            if e.get('id') == 'A027':
                e['pattern'] = 'PIT @1.67 home M2 favorite, Crosby veteran-heavy + PIT RS late 20G xGF 下降トレンド。PHI young energy (Drysdale/Martone 各1G) + rivalry Metro div motivation。PHI 3-2 PIT。UF 3個 (veteran fade + young energy + rivalry)。'
                print('P019 A027 evidence detail updated')

    # P022: NBA PO G1 playoff experience gap — enrich A026 entry
    if cid == 'P022':
        for e in c.get('evidence', []):
            if e.get('id') == 'A026':
                e['pattern'] = 'DET @1.22 home #1 seed (Cunningham 24yo young core, PO inexperience) vs ORL (prior 2024 R1 PO experience). Banchero 23/9 breakout. 112-101 ORL. Only road G1 win of the night.'
                print('P022 A026 evidence detail updated')

# Add new candidate P024: NBA PO star scorer absence
existing_cids = {c.get('candidate_id') for c in cands}
if 'P024' not in existing_cids:
    cands.append({
        'candidate_id': 'P024',
        'status': 'watching',
        'target_rule_file': 'core/rules_nba.json',
        'proposed_rule_id': 'N_NBA_new2',
        'title': 'NBA PO G1 star scorer (>25ppg RS) 欠場時の L4 下方補正',
        'description': 'star scorer (RS 25ppg+) が G1 game-time decision → ruled out になった場合、star-heavy チーム側信頼度を -8〜-10% 補正。Durant (26ppg) HOU 欠場のように実質 NRtg 1-4pt 下方修正相当。L1 NRtg は RS 全体平均で star ON ベース → star OFF では NRtg proxy が破綻。',
        'trigger_threshold': 3,
        'current_count': 1,
        'evidence': [
            {
                'id': 'A029',
                'match': 'LAL d. HOU PO R1 G1 2026-04-18 107-98',
                'pattern': 'Kevin Durant (HOU RS 26.0ppg) G1 欠場 (patellar tendon contusion)。pre-game warmup 後 ruled out。Luke Kennard 27pts career-high で short-handed LAL が HOU を突破。市場 HOU @1.43 fav、予測 HOU MISS。',
                'tag': 'nba_po_g1_star_scorer_absence',
                'sources': [
                    'ESPN gameId 401869190',
                    'ESPN rockets kevin-durant-g1-vs-lakers-knee-contusion',
                    'NBA.com rockets-lakers-2026-playoffs-game-1-takeaways'
                ]
            }
        ],
        'tag_matches': [
            'nba_po_g1_star_scorer_absence',
            'nhl_po_g1_key_player_absence'
        ],
        'note': '3件揃ったら N_NBA_new2 として実装。pre-game injury report scraping (NBA.com injury / dailyfaceoff NHL) を screening protocol に組込検討。星級選手欠場 = L4 -8〜-10% 自動補正。'
    })
    print('P024 NEW candidate added')

# Add new candidate P025: NHL PO G1 xGF% priority over seed (from A028)
if 'P025' not in existing_cids:
    cands.append({
        'candidate_id': 'P025',
        'status': 'watching',
        'target_rule_file': 'core/rules_nhl.json',
        'proposed_rule_id': 'N021',
        'title': 'NHL PO G1 predicted_winner 選択ルール: xGF% higher team 優先',
        'description': 'records PO_R1_W2/W4 で type_a_watch として事前に警告されていた "lower seed xGF% higher" パターンで MIN/ANA が higher xGF% を有した。MIN 6-1 DAL UPSET で実証 (A028)。今後 type_a_watch 発動時は seed より xGF% higher team を predicted_winner に自動設定する。ANA/EDM では EDM 勝利だが僅差で ANA の方がxGFわずか上位 → 継続観察。',
        'trigger_threshold': 3,
        'current_count': 1,
        'evidence': [
            {
                'id': 'A028',
                'match': 'Minnesota Wild d. Dallas Stars PO R1 G1 2026-04-18 6-1',
                'pattern': 'MIN xGF% 51.50 > DAL 50.79 (lower seed process advantage)。type_a_watch 事前警告 PASS → MIN が BLOWOUT UPSET で実証。predicted_winner DAL (home seed) は L1 シグナルと矛盾。xGF% higher team を優先すべき教訓。',
                'tag': 'nhl_po_xgf_priority_over_seed',
                'sources': [
                    'ESPN gameId 401869716',
                    'NHL.com wild minnesota-wild-dallas-stars-game-1-recap'
                ]
            }
        ],
        'tag_matches': [
            'nhl_po_xgf_priority_over_seed',
            'nhl_type_a_watch_realized'
        ],
        'note': '3件揃ったら N021 として実装。predicted_winner 選択アルゴリズムの改定: type_a_watch (lower seed xGF higher) 発動 → xGF higher team を予測。ANA-EDM G2 以降で実地確認継続。'
    })
    print('P025 NEW candidate added')

# Add new candidate P026: PHI/PIT-type veteran vs young NHL pattern reinforcement
# (same as P019 partially) → skip to avoid duplication

d['candidates'] = cands
d['last_updated'] = '2026-04-21'
d['updated_session'] = '_47'

p.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding='utf-8')
print('\n[OK] rule_pipeline saved. candidates =', len(cands), 'added evidence count =', added_evidence)
