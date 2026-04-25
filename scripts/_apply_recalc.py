"""Session_59 STEP C/D: 実測ベースで cumulative.json を真値書き換え"""
import json
from pathlib import Path

base = Path(r'C:\Users\ohwada\Desktop\claude_sport')
audit = json.load(open(base / 'stats' / '_audit_recalc.json', encoding='utf-8'))
cum_path = base / 'stats' / 'cumulative.json'
cum = json.load(open(cum_path, encoding='utf-8-sig'))

today = '2026-04-25'

# 各 sport の confirmed/hits/ev_total を実測 GO ベースで書き換え
def set_sport(key, dd, label, tier_label):
    if key not in cum:
        cum[key] = {}
    confirmed = dd['go_hit'] + dd['go_miss']
    cum[key]['total_predictions'] = dd['go_total']
    cum[key]['confirmed'] = confirmed
    cum[key]['hits'] = dd['go_hit']
    cum[key]['hit_rate'] = round(dd['go_hit']/confirmed, 3) if confirmed else None
    cum[key]['ev_total'] = round(dd['go_pnl'], 3)
    cum[key]['pending'] = dd['go_pending']
    cum[key]['void'] = dd['go_void']
    cum[key].setdefault('tier', tier_label)
    cum[key]['session_59_audit'] = (
        f'Session_59 (2026-04-25) STEP C/D 真値書き換え: '
        f'GO total={dd["go_total"]} confirmed={confirmed} hit={dd["go_hit"]} miss={dd["go_miss"]} '
        f'void={dd["go_void"]} pending={dd["go_pending"]} pnl={dd["go_pnl"]:+.3f}u. '
        f'PRED total={dd["pred_total"]} hit={dd["pred_hit"]} miss={dd["pred_miss"]}. '
        f'Source: stats/_audit_recalc.json (records 全件 walk + archived/duplicate 除外).'
    )

set_sport('tennis_atp', audit['tennis_atp'], 'ATP', 'advanced')
set_sport('tennis_wta', audit['tennis_wta'], 'WTA', 'advanced')
set_sport('nhl', audit['nhl'], 'NHL', 'advanced')
set_sport('nba', audit['nba'], 'NBA', 'advanced')
set_sport('nrl', audit['nrl'], 'NRL', 'basic')
set_sport('superrugby', audit['superrugby'], 'SuperRugby', 'basic')
set_sport('super_league', audit['super_league'], 'SuperLeague', 'basic')
set_sport('ufl', audit['ufl'], 'UFL', 'basic')
# nfl/cfl/premiership/top14/prod2/ahl は 0 件のため confirmed=0 を保持

# by_tier 再計算
adv = audit['_advanced']
basic = audit['_basic']
adv_conf = adv['go_hit'] + adv['go_miss']
basic_conf = basic['go_hit'] + basic['go_miss']
cum['by_tier']['advanced'] = {
    'total_predictions': adv['go_total'],
    'confirmed': adv_conf,
    'hits': adv['go_hit'],
    'ev_total': round(adv['go_pnl'], 3),
    'pending': adv['go_pending'],
    'void': adv['go_void'],
    'sports_included': ['tennis_atp','tennis_wta','nhl','nba','nfl'],
    'note': f'Session_59 (2026-04-25) 真値書き換え。Advanced GO confirmed={adv_conf} hit={adv["go_hit"]} pnl={adv["go_pnl"]:+.3f}u. Source: stats/_audit_recalc.json',
    'hit_rate': round(adv['go_hit']/adv_conf, 3) if adv_conf else None,
}
cum['by_tier']['basic'] = {
    'total_predictions': basic['go_total'],
    'confirmed': basic_conf,
    'hits': basic['go_hit'],
    'ev_total': round(basic['go_pnl'], 3),
    'pending': basic['go_pending'],
    'void': basic['go_void'],
    'sports_included': ['ufl','cfl','nrl','superrugby','premiership','top14','prod2','ahl','super_league','soccer','mlb'],
    'note': f'Session_59 (2026-04-25) 真値書き換え。Basic GO confirmed={basic_conf} hit={basic["go_hit"]} pnl={basic["go_pnl"]:+.3f}u',
    'hit_rate': round(basic['go_hit']/basic_conf, 3) if basic_conf else None,
}

# overall_combined 再計算
ov = audit['_overall']
ov_conf = ov['go_hit'] + ov['go_miss']
cum['overall_combined'] = {
    'confirmed': ov_conf,
    'hits': ov['go_hit'],
    'misses': ov['go_miss'],
    'void': ov['go_void'],
    'pending': ov['go_pending'],
    'go_total': ov['go_total'],
    'hit_rate': round(ov['go_hit']/ov_conf, 3) if ov_conf else None,
    'ev_total': round(ov['go_pnl'], 3),
    'session': '_59',
    'last_updated': today,
    'note': f'Session_59 真値書き換え (STEP C/D). Source: stats/_audit_recalc.json (records 全件 walk).',
}

# by_quadrant 再計算
q1 = audit['_q1_total']
q3 = audit['_q3_total']
q3m = audit['_q3_mid_total']
q4 = audit['_q4_total']

cum['by_quadrant']['Q1_go'] = {
    'total': ov['go_total'],
    'confirmed': ov_conf,
    'hit': ov['go_hit'],
    'miss': ov['go_miss'],
    'void': ov['go_void'],
    'pending': ov['go_pending'],
    'hit_rate': round(ov['go_hit']/ov_conf, 3) if ov_conf else None,
    'ev_total': round(ov['go_pnl'], 3),
    'note': f'Session_59 (2026-04-25) 真値書き換え: 全 GO 推奨累計 (Q1 明示タグ {q1["t"]} 件 + 旧 quadrant 未タグ legacy GO の合算)。実測 records 全件 walk。',
    'q1_explicit_tag': {
        'total': q1['t'], 'confirmed': q1['c'], 'hit': q1['h'], 'miss': q1['m'], 'void': q1['v'],
        'pnl': round(q1['pnl'], 3),
        'note': '4象限フレームワーク Phase2 以降の明示 Q1_go タグ付き entries のみ集計',
    },
}
cum['by_quadrant']['Q3_output_a'] = {
    'total': q3['t'],
    'confirmed': q3['c'],
    'hit': q3['h'],
    'void_excluded': q3['v'],
    'hit_rate': round(q3['h']/q3['c'], 3) if q3['c'] else None,
    'ev_total': 0,
    'note': f'Session_59 真値書き換え。Q3_output_a (conf>=85% 高確率予想) 累計。',
}
cum['by_quadrant']['Q3_mid'] = {
    'total': q3m['t'],
    'confirmed': q3m['c'],
    'hit': q3m['h'],
    'hit_rate': round(q3m['h']/q3m['c'], 3) if q3m['c'] else None,
    'ev_total': 0,
    '_description': 'Session_56 新設 80%<=conf<85% 中確実性帯。Session_59 真値書き換え。',
    'last_updated': today,
}
cum['by_quadrant']['Q4_upset_watch'] = {
    'total': q4['t'],
    'confirmed': q4['c'],
    'upset_realized_count': q4['u'],
    'fav_hit_count': q4['f'],
    'detection_rate': round(q4['u']/q4['c'], 3) if q4['c'] else None,
    'detection_rate_note': f'Q4_upset_watch が事前警告した試合で実際に UPSET が実現した率。{q4["u"]}/{q4["c"]} = {q4["u"]/q4["c"]*100 if q4["c"] else 0:.1f}%.',
    'interpretation_rule': 'Q4 はベット対象外 (no-bet watch)。detection_rate >=50% で GEN005 閾値再調整の検討材料.',
    'note': f'Session_59 真値書き換え。',
    'last_updated': today,
}
cum['by_quadrant']['last_updated'] = f'2026-04-25 Session_59 STEP C/D'

# overall (Session_58 segment) も last_session 更新
cum['last_updated'] = today
cum['last_session'] = '_59'
cum.setdefault('schema_versions', []).append({
    'version': 'v3.2',
    'date': today,
    'change': 'Session_59 STEP A-D 真値書き換え: MC 二重ファイル archived 化 + WTA 重複統合 + cumulative 全種目 sport/tier/quadrant 実測再集計',
})

cum_path.write_text(json.dumps(cum, ensure_ascii=False, indent=2), encoding='utf-8')
print('cumulative.json updated successfully.')
print(f'Overall: {ov["go_hit"]}/{ov_conf} = {ov["go_hit"]/ov_conf*100 if ov_conf else 0:.1f}% pnl={ov["go_pnl"]:+.3f}u (pending {ov["go_pending"]})')
print(f'Advanced: {adv["go_hit"]}/{adv_conf} = {adv["go_hit"]/adv_conf*100 if adv_conf else 0:.1f}% pnl={adv["go_pnl"]:+.3f}u')
print(f'Basic: {basic["go_hit"]}/{basic_conf} = {basic["go_hit"]/basic_conf*100 if basic_conf else 0:.1f}% pnl={basic["go_pnl"]:+.3f}u')
