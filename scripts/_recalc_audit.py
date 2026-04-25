"""Session_59 STEP C+D: 全 records から実測ベースで再集計"""
import json, glob
from pathlib import Path

base = Path(r'C:\Users\ohwada\Desktop\claude_sport\records')
files = sorted(glob.glob(str(base / '**/*.json'), recursive=True))

def walk(obj):
    if isinstance(obj, list):
        for x in obj: yield from walk(x)
    elif isinstance(obj, dict):
        yield obj
        for v in obj.values(): yield from walk(v)

sport_map = {
    'tennis': 'tennis_atp', 'wta': 'tennis_wta', 'nhl': 'nhl', 'nba': 'nba',
    'nrl': 'nrl', 'superrugby': 'superrugby', 'premiership': 'premiership',
    'top14': 'top14', 'prod2': 'prod2', 'ahl': 'ahl', 'superleague': 'super_league',
    'ufl': 'ufl', 'cfl': 'cfl', 'nfl': 'nfl', 'soccer': 'soccer', 'mlb': 'mlb',
}

agg = {sk: {
    'go_total':0, 'go_hit':0, 'go_miss':0, 'go_void':0, 'go_pending':0, 'go_pnl':0.0,
    'q1_total':0, 'q1_confirmed':0, 'q1_hit':0, 'q1_miss':0, 'q1_void':0, 'q1_pnl':0.0,
    'q3_total':0, 'q3_confirmed':0, 'q3_hit':0, 'q3_void':0,
    'q3_mid_total':0, 'q3_mid_confirmed':0, 'q3_mid_hit':0,
    'q4_total':0, 'q4_confirmed':0, 'q4_upset_realized':0, 'q4_fav_hit':0,
    'pred_total':0, 'pred_confirmed':0, 'pred_hit':0, 'pred_miss':0, 'pred_void':0,
} for sk in sport_map.values()}

for fp in files:
    if 'multi_bets' in fp: continue
    sport_dir = Path(fp).parent.name
    sk = sport_map.get(sport_dir)
    if not sk: continue
    try: d = json.load(open(fp, encoding='utf-8-sig'))
    except: continue

    for o in walk(d):
        if not isinstance(o, dict): continue
        tier = o.get('tier')
        if tier in ('archived_duplicate','duplicate_closed','invalid'): continue
        if o.get('archived') is True: continue
        if not o.get('match'): continue
        date_str = str(o.get('date','?'))
        if date_str == '?' or not date_str: continue

        ph = o.get('prediction_hit')
        hit = o.get('hit')
        ev = o.get('actual_ev')
        void = o.get('void') is True
        quad = o.get('quadrant', '')

        if o.get('predicted_winner'):
            agg[sk]['pred_total'] += 1
            if ph is True: agg[sk]['pred_hit'] += 1; agg[sk]['pred_confirmed'] += 1
            elif ph is False: agg[sk]['pred_miss'] += 1; agg[sk]['pred_confirmed'] += 1
            elif void: agg[sk]['pred_void'] += 1

        if tier == 'go':
            agg[sk]['go_total'] += 1
            if void: agg[sk]['go_void'] += 1
            elif hit is True: agg[sk]['go_hit'] += 1; agg[sk]['go_pnl'] += ev or 0
            elif hit is False: agg[sk]['go_miss'] += 1; agg[sk]['go_pnl'] += ev or 0
            else: agg[sk]['go_pending'] += 1

        if quad == 'Q1_go':
            agg[sk]['q1_total'] += 1
            if void: agg[sk]['q1_void'] += 1
            elif hit is True: agg[sk]['q1_hit'] += 1; agg[sk]['q1_confirmed'] += 1; agg[sk]['q1_pnl'] += ev or 0
            elif hit is False: agg[sk]['q1_miss'] += 1; agg[sk]['q1_confirmed'] += 1; agg[sk]['q1_pnl'] += ev or 0
        if quad == 'Q3_output_a':
            agg[sk]['q3_total'] += 1
            if void: agg[sk]['q3_void'] += 1
            elif ph is True: agg[sk]['q3_hit'] += 1; agg[sk]['q3_confirmed'] += 1
            elif ph is False: agg[sk]['q3_confirmed'] += 1
        if quad == 'Q3_mid':
            agg[sk]['q3_mid_total'] += 1
            if ph is True: agg[sk]['q3_mid_hit'] += 1; agg[sk]['q3_mid_confirmed'] += 1
            elif ph is False: agg[sk]['q3_mid_confirmed'] += 1
        if quad == 'Q4_upset_watch':
            agg[sk]['q4_total'] += 1
            if ph is not None:
                agg[sk]['q4_confirmed'] += 1
                if ph is False: agg[sk]['q4_upset_realized'] += 1
                else: agg[sk]['q4_fav_hit'] += 1

print('=== sport別 ===')
print('sport         GO  hit  miss void pend     pnl | PRED  hit miss')
totals = {'go_total':0,'go_hit':0,'go_miss':0,'go_void':0,'go_pending':0,'go_pnl':0.0}
for sk, dd in agg.items():
    if dd['pred_total'] == 0 and dd['go_total'] == 0: continue
    print('%-13s %3d %4d %4d %4d %4d %+7.3f | %4d %4d %4d' % (sk, dd['go_total'], dd['go_hit'], dd['go_miss'], dd['go_void'], dd['go_pending'], dd['go_pnl'], dd['pred_total'], dd['pred_hit'], dd['pred_miss']))
    for k in totals: totals[k] += dd[k]

adv_sports = ['tennis_atp', 'tennis_wta', 'nhl', 'nba', 'nfl']
basic_sports = ['ufl', 'cfl', 'nrl', 'superrugby', 'premiership', 'top14', 'prod2', 'ahl', 'super_league', 'soccer', 'mlb']

adv_totals = {'go_total':0,'go_hit':0,'go_miss':0,'go_void':0,'go_pending':0,'go_pnl':0.0}
basic_totals = {'go_total':0,'go_hit':0,'go_miss':0,'go_void':0,'go_pending':0,'go_pnl':0.0}
for sk, dd in agg.items():
    if sk in adv_sports:
        for k in adv_totals: adv_totals[k] += dd[k]
    elif sk in basic_sports:
        for k in basic_totals: basic_totals[k] += dd[k]

print('\n=== Tier 別 ===')
adv_conf = adv_totals['go_hit']+adv_totals['go_miss']
basic_conf = basic_totals['go_hit']+basic_totals['go_miss']
print('Advanced: %d/%d hit %.1f%% pnl=%+.3f (pending %d void %d)' % (adv_totals['go_hit'], adv_conf, adv_totals['go_hit']/adv_conf*100 if adv_conf else 0, adv_totals['go_pnl'], adv_totals['go_pending'], adv_totals['go_void']))
print('Basic:    %d/%d hit %.1f%% pnl=%+.3f (pending %d void %d)' % (basic_totals['go_hit'], basic_conf, basic_totals['go_hit']/basic_conf*100 if basic_conf else 0, basic_totals['go_pnl'], basic_totals['go_pending'], basic_totals['go_void']))
overall_conf = totals['go_hit']+totals['go_miss']
print('OVERALL:  %d/%d hit %.1f%% pnl=%+.3f' % (totals['go_hit'], overall_conf, totals['go_hit']/overall_conf*100 if overall_conf else 0, totals['go_pnl']))

q1 = {'t':0,'c':0,'h':0,'m':0,'v':0,'pnl':0.0}
q3 = {'t':0,'c':0,'h':0,'v':0}
q3m = {'t':0,'c':0,'h':0}
q4 = {'t':0,'c':0,'u':0,'f':0}
for d in agg.values():
    q1['t']+=d['q1_total']; q1['c']+=d['q1_confirmed']; q1['h']+=d['q1_hit']; q1['m']+=d['q1_miss']; q1['v']+=d['q1_void']; q1['pnl']+=d['q1_pnl']
    q3['t']+=d['q3_total']; q3['c']+=d['q3_confirmed']; q3['h']+=d['q3_hit']; q3['v']+=d['q3_void']
    q3m['t']+=d['q3_mid_total']; q3m['c']+=d['q3_mid_confirmed']; q3m['h']+=d['q3_mid_hit']
    q4['t']+=d['q4_total']; q4['c']+=d['q4_confirmed']; q4['u']+=d['q4_upset_realized']; q4['f']+=d['q4_fav_hit']
print('\n=== 4象限 ===')
print('Q1_go:       total=%d conf=%d hit=%d miss=%d void=%d pnl=%+.3f (%.1f%%)' % (q1['t'],q1['c'],q1['h'],q1['m'],q1['v'],q1['pnl'], q1['h']/q1['c']*100 if q1['c'] else 0))
print('Q3_output_a: total=%d conf=%d hit=%d void=%d (%.1f%%)' % (q3['t'],q3['c'],q3['h'],q3['v'], q3['h']/q3['c']*100 if q3['c'] else 0))
print('Q3_mid:      total=%d conf=%d hit=%d' % (q3m['t'],q3m['c'],q3m['h']))
print('Q4_upset_watch: total=%d conf=%d upset_real=%d fav_hit=%d (detect=%.1f%%)' % (q4['t'],q4['c'],q4['u'],q4['f'], q4['u']/q4['c']*100 if q4['c'] else 0))

out = {sk: dict(v) for sk, v in agg.items()}
out['_overall'] = totals
out['_advanced'] = adv_totals
out['_basic'] = basic_totals
out['_q1_total'] = q1; out['_q3_total'] = q3; out['_q3_mid_total'] = q3m; out['_q4_total'] = q4
Path(r'C:\Users\ohwada\Desktop\claude_sport\stats\_audit_recalc.json').write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding='utf-8')
print('\n=> stats/_audit_recalc.json saved')
