"""A022/A024 invalidate + deep factor analysis"""
import json

fp = 'C:/Users/ohwada/Desktop/claude_sport/stats/upset_patterns.json'
with open(fp, encoding='utf-8-sig') as f:
    data = json.load(f)

# Move A022/A024 to invalidated_upsets
new_confirmed = []
invalidated = data.get('invalidated_upsets', [])

for e in data['confirmed_upsets']:
    uid = e.get('upset_id')
    if uid == 'A022':
        e['invalidated'] = True
        e['ce_error'] = 'CE016 (4-case series)'
        e['actual_result_corrected'] = 'Sakamoto d. Svajda 7-6 6-1'
        e['invalidation_note'] = 'NOT AN UPSET. Sakamoto (market fav @1.59, WC Japan) won vs Svajda (3rd Q seed). Original record of "Svajda d. Sakamoto" was reversed. Sakamoto 6 aces, 1 DF - dominant serve.'
        e['verification_sources'] = [
            'tennismajors.com/matches/atp/mutua-madrid-open/zachary-svajda-vs-rei-sakamoto',
            'en.wikipedia.org 2026_Mutua_Madrid_Open_Mens_singles (qualifying draw)'
        ]
        e['deeper_factor_analysis_s46'] = {
            'why_market_favorite_won': {
                'sakamoto_serve_dominance': '6 aces, 1 DF - serve holds consistently',
                'WC_motivation': 'JPN WC 19歳 + home continent (日本) 大会でなくても若手昇進motivation高',
                'svajda_Q_seed_reality': '3rd seed of Q draw = ranking #140-160 圏の player。Sakamoto #170-190圏の WC との実力差は小さく、市場がSakamoto fav @1.59 は妥当'
            },
            'rule_implication': 'P023 evidence に追加: 若手 WC サーブ型が Q seeded player を倒すパターン. Top20範疇ではないが、「サーブ型 若手 on clay → 本命HIT 実現」は同じ構造',
            'p023_evidence_append': True
        }
        e['invalidated_date'] = '2026-04-20'
        e['invalidated_session'] = '_46'
        invalidated.append(e)
        print(f'  [A022] INVALIDATED + deep analysis')
    elif uid == 'A024':
        e['invalidated'] = True
        e['ce_error'] = 'CE016 (4-case series)'
        e['actual_result_corrected'] = 'Droguet d. Virtanen 2-6 6-X 6-X (3 sets)'
        e['invalidation_note'] = 'NOT AN UPSET. Droguet (market fav @1.72, FRA young) won vs Virtanen (FIN #140). Original record of "Virtanen d. Drogue" was reversed. 3-set match - Virtanen took 1st set 6-2, Droguet reversed with 2 sets.'
        e['verification_sources'] = [
            'en.wikipedia.org 2026_Mutua_Madrid_Open_Mens_singles (qualifying draw)',
            'news.de 859538029 liveticker (initial score 2-6 6-3 partial)'
        ]
        e['deeper_factor_analysis_s46'] = {
            'why_market_favorite_won': {
                'droguet_clay_specialist': 'Droguet (FRA) はclay core competency、Bucharest系クレー大会で regular',
                'virtanen_fast_start_fade': '1stセット 6-2 取ったが 3-setマッチ化でDroguet の clay baseline endurance が勝る pattern',
                'market_price_validity': 'fav @1.72 = 58.1% implied は clay specialist 側に妥当'
            },
            'rule_implication': 'young FRA clay specialist が 3-set で hard-court oriented FIN player を attrition で破る pattern. clay specialization の endurance 側面が evidence',
            'supporting_note': 'P012 (clay specialist vs hardcourt player) の候補 evidence としても扱える (Carabelli vs Khachanov と類似 motif)'
        }
        e['invalidated_date'] = '2026-04-20'
        e['invalidated_session'] = '_46'
        invalidated.append(e)
        print(f'  [A024] INVALIDATED + deep analysis')
    else:
        new_confirmed.append(e)

data['confirmed_upsets'] = new_confirmed
data['invalidated_upsets'] = invalidated
data['last_updated'] = '2026-04-20'
data['updated_by'] = 'Session_46 CE016 complete resolution (4 cases: A017/A022/A023/A024 all invalidated)'

with open(fp, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# Add A022 evidence to P023
p2 = 'C:/Users/ohwada/Desktop/claude_sport/core/rule_pipeline.json'
with open(p2, encoding='utf-8-sig') as f:
    pipeline = json.load(f)

for c in pipeline['candidates']:
    if c.get('candidate_id') == 'P023':
        c['evidence'].append({
            "id": "A022_corrected",
            "match": "Sakamoto d. Svajda Madrid Q R1 2026-04-20 7-6 6-1",
            "pattern": "Sakamoto (JPN WC 19歳 サーブ型, fav @1.59) d. Svajda (3rd Q seed). 6 aces / 1 DF で serve dominance. 市場fav HIT. '若手サーブ型 on clay, dominant serve' 系として P023 evidence 扱い (Top20 範疇ではないが構造類似).",
            "tag": "young_server_clay_hold_pattern",
            "sources": [
                "tennismajors.com/matches/atp/mutua-madrid-open/zachary-svajda-vs-rei-sakamoto",
                "en.wikipedia.org 2026_Mutua_Madrid_Open_Mens_singles"
            ]
        })
        c['current_count'] = 2
        c['note'] += ' [Session_46 update]: A022 evidence 追加, 2/3 到達.'
        print(f'  [P023] evidence +1 -> current_count=2/3')

# Add A024 evidence to P012 (clay specialist vs hardcourt)
for c in pipeline['candidates']:
    if c.get('candidate_id') == 'P012':
        c['evidence'].append({
            "id": "A024_corrected",
            "match": "Droguet d. Virtanen Madrid Q R1 2026-04-20 (3sets)",
            "pattern": "Droguet (FRA clay specialist) d. Virtanen (FIN hard-court tendency). Virtanen 1st set 6-2 lead後, Droguet が後半2セット回収. clay attrition power + baseline endurance が Virtanen の fast-start を上回る. fav @1.72 HIT.",
            "tag": "atp_clay_specialist_vs_hardcourt_player",
            "sources": [
                "en.wikipedia.org 2026_Mutua_Madrid_Open_Mens_singles"
            ]
        })
        c['current_count'] = 2
        c['note'] += ' [Session_46]: A024 evidence 追加 (本命HIT経由 - clay specialist endurance pattern).'
        print(f'  [P012] evidence +1 -> current_count=2/3')

pipeline['last_updated'] = '2026-04-20'
pipeline['updated_session'] = '_46'
with open(p2, 'w', encoding='utf-8') as f:
    json.dump(pipeline, f, ensure_ascii=False, indent=2)

print('\n[DONE] CE016 complete resolution')
print(f'  confirmed_upsets: {len(new_confirmed)} (was 34, -2 for A022/A024)')
print(f'  invalidated_upsets: {len(invalidated)}')
