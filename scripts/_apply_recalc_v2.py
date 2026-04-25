"""Session_59 STEP C/D v2: sync_sport_cards.py が書き出した dashboard_stats.json を真値とする
   (tier='go' + tier='gamble_bet' 両方を bet 対象、confirmed=hit not None で void 含む)
   この単一ロジックに cumulative.json を一致させる
"""
import json
from pathlib import Path

base = Path(r'C:\Users\ohwada\Desktop\claude_sport')
ds = json.load(open(base / 'core' / 'dashboard_stats.json', encoding='utf-8-sig'))
cum_path = base / 'stats' / 'cumulative.json'
cum = json.load(open(cum_path, encoding='utf-8-sig'))
audit = json.load(open(base / 'stats' / '_audit_recalc.json', encoding='utf-8'))

today = '2026-04-25'

# dashboard_stats.json の sports → cumulative
sport_map = {
    'atp': 'tennis_atp', 'wta': 'tennis_wta', 'nhl': 'nhl', 'nba': 'nba',
    'nrl': 'nrl', 'superrugby': 'superrugby', 'superleague': 'super_league',
    'ufl': 'ufl', 'cfl': 'cfl', 'premiership': 'premiership',
    'top14': 'top14', 'prod2': 'prod2', 'ahl': 'ahl',
}

def upsert_sport(cum_key, ds_data, label):
    if cum_key not in cum:
        cum[cum_key] = {}
    cum[cum_key]['total_predictions'] = ds_data.get('go_count', 0)
    cum[cum_key]['confirmed'] = ds_data.get('confirmed_count', 0)
    cum[cum_key]['hits'] = ds_data.get('hit_count', 0)
    cum[cum_key]['hit_rate'] = ds_data.get('hit_rate')
    cum[cum_key]['ev_total'] = round(ds_data.get('pnl', 0), 3)
    cum[cum_key]['pending'] = ds_data.get('pending_count', 0)
    cum[cum_key]['session_59_audit'] = (
        f'Session_59 (2026-04-25) STEP C/D 真値書き換え (sync_sport_cards.py logic 採用): '
        f'GO+GB total={ds_data.get("go_count",0)} confirmed={ds_data.get("confirmed_count",0)} '
        f'hit={ds_data.get("hit_count",0)} ev={ds_data.get("pnl",0):+.3f}u pending={ds_data.get("pending_count",0)}. '
        f'Source: dashboard_stats.json (records 全件再計算).'
    )

for dk, ck in sport_map.items():
    if dk not in ds.get('sports', {}): continue
    upsert_sport(ck, ds['sports'][dk], dk.upper())

# overview
ov = ds['overview']
cum['overall_combined'] = {
    'confirmed': ov.get('total_confirmed', 0),
    'hits': ov.get('total_hits', 0),
    'misses': ov.get('total_confirmed', 0) - ov.get('total_hits', 0),
    'pending': ov.get('total_pending', 0),
    'go_total': ov.get('total_go', 0),
    'hit_rate': ov.get('hit_rate'),
    'ev_total': round(ov.get('total_pnl', 0), 3),
    'session': '_59',
    'last_updated': today,
    'note': 'Session_59 STEP C/D v2 真値書き換え。sync_sport_cards.py logic (tier in {go, gamble_bet}, confirmed=hit not None) で集計。dashboard_stats.json と完全同期。',
}

# by_tier
adv_keys = ['atp', 'wta', 'nhl', 'nba']
basic_keys = ['ufl', 'nrl', 'superrugby', 'premiership', 'top14', 'prod2', 'superleague', 'ahl']
adv_tot = {'go':0, 'conf':0, 'hit':0, 'pnl':0.0, 'pend':0}
basic_tot = {'go':0, 'conf':0, 'hit':0, 'pnl':0.0, 'pend':0}
for k in adv_keys:
    sp = ds.get('sports', {}).get(k, {})
    adv_tot['go'] += sp.get('go_count', 0)
    adv_tot['conf'] += sp.get('confirmed_count', 0)
    adv_tot['hit'] += sp.get('hit_count', 0)
    adv_tot['pnl'] += sp.get('pnl', 0)
    adv_tot['pend'] += sp.get('pending_count', 0)
for k in basic_keys:
    sp = ds.get('sports', {}).get(k, {})
    basic_tot['go'] += sp.get('go_count', 0)
    basic_tot['conf'] += sp.get('confirmed_count', 0)
    basic_tot['hit'] += sp.get('hit_count', 0)
    basic_tot['pnl'] += sp.get('pnl', 0)
    basic_tot['pend'] += sp.get('pending_count', 0)

cum['by_tier']['advanced'] = {
    'total_predictions': adv_tot['go'],
    'confirmed': adv_tot['conf'],
    'hits': adv_tot['hit'],
    'ev_total': round(adv_tot['pnl'], 3),
    'pending': adv_tot['pend'],
    'sports_included': ['tennis_atp','tennis_wta','nhl','nba','nfl'],
    'note': f'Session_59 真値. Advanced GO confirmed={adv_tot["conf"]} hit={adv_tot["hit"]} pnl={adv_tot["pnl"]:+.3f}u',
    'hit_rate': round(adv_tot['hit']/adv_tot['conf'], 3) if adv_tot['conf'] else None,
}
cum['by_tier']['basic'] = {
    'total_predictions': basic_tot['go'],
    'confirmed': basic_tot['conf'],
    'hits': basic_tot['hit'],
    'ev_total': round(basic_tot['pnl'], 3),
    'pending': basic_tot['pend'],
    'sports_included': ['ufl','cfl','nrl','superrugby','premiership','top14','prod2','ahl','super_league','soccer','mlb'],
    'note': f'Session_59 真値. Basic GO confirmed={basic_tot["conf"]} hit={basic_tot["hit"]} pnl={basic_tot["pnl"]:+.3f}u',
    'hit_rate': round(basic_tot['hit']/basic_tot['conf'], 3) if basic_tot['conf'] else None,
}

# by_quadrant (audit から)
q1 = audit['_q1_total']
q3 = audit['_q3_total']
q3m = audit['_q3_mid_total']
q4 = audit['_q4_total']

cum['by_quadrant']['Q1_go'] = {
    'total': ov.get('total_go', 0),
    'confirmed': ov.get('total_confirmed', 0),
    'hit': ov.get('total_hits', 0),
    'miss': ov.get('total_confirmed', 0) - ov.get('total_hits', 0),
    'pending': ov.get('total_pending', 0),
    'hit_rate': ov.get('hit_rate'),
    'ev_total': round(ov.get('total_pnl', 0), 3),
    'note': f'Session_59 真値 (sync_sport_cards.py logic). 全 GO/GB 推奨累計。明示 Q1_go タグ {q1["t"]} 件は q1_explicit_tag に分離記録.',
    'q1_explicit_tag': {
        'total': q1['t'], 'confirmed': q1['c'], 'hit': q1['h'], 'miss': q1['m'], 'void': q1['v'],
        'pnl': round(q1['pnl'], 3),
        'note': '4象限フレームワーク Phase2 以降の明示 Q1_go タグ付き entries のみ集計',
    },
}
cum['by_quadrant']['Q3_output_a'] = {
    'total': q3['t'], 'confirmed': q3['c'], 'hit': q3['h'], 'void_excluded': q3['v'],
    'hit_rate': round(q3['h']/q3['c'], 3) if q3['c'] else None,
    'ev_total': 0,
    'note': 'Session_59 真値. Q3_output_a (conf>=85% 高確率予想) 累計.',
}
cum['by_quadrant']['Q3_mid'] = {
    'total': q3m['t'], 'confirmed': q3m['c'], 'hit': q3m['h'],
    'hit_rate': round(q3m['h']/q3m['c'], 3) if q3m['c'] else None,
    'ev_total': 0,
    '_description': 'Session_56 新設 80%<=conf<85% 中確実性帯。Session_59 真値.',
    'last_updated': today,
}
cum['by_quadrant']['Q4_upset_watch'] = {
    'total': q4['t'], 'confirmed': q4['c'],
    'upset_realized_count': q4['u'], 'fav_hit_count': q4['f'],
    'detection_rate': round(q4['u']/q4['c'], 3) if q4['c'] else None,
    'detection_rate_note': f'Q4_upset_watch detect rate {q4["u"]}/{q4["c"]} = {q4["u"]/q4["c"]*100 if q4["c"] else 0:.1f}%',
    'note': 'Session_59 真値.',
    'last_updated': today,
}
cum['by_quadrant']['last_updated'] = '2026-04-25 Session_59'

cum['last_updated'] = today
cum['last_session'] = '_59'

# schema version (重複追加避け)
versions = cum.setdefault('schema_versions', [])
if not any(v.get('version') == 'v3.2' for v in versions):
    versions.append({
        'version': 'v3.2',
        'date': today,
        'change': 'Session_59 STEP A-E 真値書き換え v2: sync_sport_cards.py logic 採用 (tier in {go, gamble_bet}, confirmed=hit not None)',
    })

cum_path.write_text(json.dumps(cum, ensure_ascii=False, indent=2), encoding='utf-8')
print('cumulative.json updated (v2).')
print(f"Overview: GO={ov.get('total_go')} conf={ov.get('total_confirmed')} hit={ov.get('total_hits')} hit_rate={ov.get('hit_rate')} pnl={ov.get('total_pnl')}")
print(f"Advanced: {adv_tot['hit']}/{adv_tot['conf']} = {adv_tot['hit']/adv_tot['conf']*100 if adv_tot['conf'] else 0:.1f}% pnl={adv_tot['pnl']:+.3f}u (pend {adv_tot['pend']})")
print(f"Basic: {basic_tot['hit']}/{basic_tot['conf']} = {basic_tot['hit']/basic_tot['conf']*100 if basic_tot['conf'] else 0:.1f}% pnl={basic_tot['pnl']:+.3f}u (pend {basic_tot['pend']})")
