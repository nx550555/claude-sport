"""Session_59 STEP E: dashboard_stats.json も実測ベースで真値書き換え"""
import json
from pathlib import Path

base = Path(r'C:\Users\ohwada\Desktop\claude_sport')
audit = json.load(open(base / 'stats' / '_audit_recalc.json', encoding='utf-8'))
ds_path = base / 'core' / 'dashboard_stats.json'
ds = json.load(open(ds_path, encoding='utf-8-sig'))

today = '2026-04-25'

# sport key map
sport_to_dashkey = {
    'tennis_atp': 'atp', 'tennis_wta': 'wta', 'nhl': 'nhl', 'nba': 'nba',
    'nrl': 'nrl', 'superrugby': 'superrugby', 'super_league': 'superleague',
    'ufl': 'ufl', 'cfl': 'cfl', 'premiership': 'premiership',
    'top14': 'top14', 'prod2': 'prod2', 'ahl': 'ahl', 'soccer': 'soccer',
    'mlb': 'mlb', 'nfl': 'nfl',
}

for sk, dk in sport_to_dashkey.items():
    if sk not in audit: continue
    dd = audit[sk]
    confirmed = dd['go_hit'] + dd['go_miss']
    if dk not in ds['sports']:
        ds['sports'][dk] = {}
    ds['sports'][dk] = {
        'go_count': dd['go_total'],
        'confirmed_count': confirmed,
        'hit_count': dd['go_hit'],
        'hit_rate': round(dd['go_hit']/confirmed, 3) if confirmed else None,
        'pnl': round(dd['go_pnl'], 3),
        'pending_count': dd['go_pending'],
        'void_count': dd['go_void'],
    }

# overview
ov = audit['_overall']
ov_conf = ov['go_hit'] + ov['go_miss']
ds['overview'] = {
    'total_go': ov['go_total'],
    'total_confirmed': ov_conf,
    'total_hits': ov['go_hit'],
    'total_misses': ov['go_miss'],
    'total_void': ov['go_void'],
    'hit_rate': round(ov['go_hit']/ov_conf, 3) if ov_conf else None,
    'total_pnl': round(ov['go_pnl'], 3),
    'total_pending': ov['go_pending'],
    'session_59_note': f'Session_59 (2026-04-25) STEP E 真値書き換え: records 全件 walk + archived 除外。GO confirmed={ov_conf} hit={ov["go_hit"]} pnl={ov["go_pnl"]:+.3f}u',
}

adv = audit['_advanced']
basic = audit['_basic']
adv_conf = adv['go_hit'] + adv['go_miss']
basic_conf = basic['go_hit'] + basic['go_miss']
ds['by_tier']['advanced'] = {
    'go_count': adv['go_total'],
    'confirmed_count': adv_conf,
    'hit_count': adv['go_hit'],
    'pnl': round(adv['go_pnl'], 3),
    'pending_count': adv['go_pending'],
    'void_count': adv['go_void'],
    'sports': ['atp', 'wta', 'nhl', 'nba', 'nfl', 'soccer', 'mlb'],
    'hit_rate': round(adv['go_hit']/adv_conf, 3) if adv_conf else None,
}
ds['by_tier']['basic'] = {
    'go_count': basic['go_total'],
    'confirmed_count': basic_conf,
    'hit_count': basic['go_hit'],
    'pnl': round(basic['go_pnl'], 3),
    'pending_count': basic['go_pending'],
    'void_count': basic['go_void'],
    'sports': ['ufl', 'cfl', 'nrl', 'superrugby', 'premiership', 'top14', 'prod2', 'superleague', 'ahl'],
    'hit_rate': round(basic['go_hit']/basic_conf, 3) if basic_conf else None,
}

# Session_59 audit notes 追加
ds['session_59_notes'] = {
    'audit_action': 'STEP A-E 全実行: MC 二重ファイル archived 化 + WTA Tan/Bondar 重複統合 + cumulative.json/dashboard_stats.json 全種目 sport/tier/quadrant 実測再集計',
    'data_changes': {
        'before_audit': 'cumulative_total_go=38 / hit_rate=71.9% / pnl=+1.80u (古い + MC 重複疑い)',
        'after_audit': f'GO total={ov["go_total"]} / hit_rate={ov["go_hit"]/ov_conf*100 if ov_conf else 0:.1f}% / pnl={ov["go_pnl"]:+.3f}u (実測)',
    },
    'detected_issues': [
        '2026-MC.json と 2026-ATP.json で MC 10件 GO 完全二重計上 (Session_59 archived 化)',
        'wta/2026.json と tennis/2026-WTA.json で Tan vs Bondar 重複 (Session_59 archived 化)',
        'cumulative.tennis_wta が古い: Galfi(+0.54) と Mertens(+0.37) HIT 未反映',
        'cumulative.super_league confirmed=4 が誤計上 (実測 2)',
        'cumulative.superrugby confirmed=0 vs 実測 1',
        'Q1_go quadrant タグは Phase2 以降の 11 件のみ (旧 GO は legacy 扱いで quadrant 未付与)',
    ],
    'fixes_applied': [
        'records/tennis/2026-MC.json: 14 archived',
        'records/tennis/2026-WTA.json: 1 archived',
        'stats/cumulative.json: 全種目+by_tier+by_quadrant+overall_combined 真値再計算',
        'core/dashboard_stats.json: 全種目+overview+by_tier 真値再計算',
        'monitoring/health_check.py: void/ph=null を MISS 判定から除外 (CE19 由来)',
        'records/tennis/2026-ATP.json: de Minaur vs Jodar miss_analysis 補填',
    ],
    'next_step_proposal': 'STEP F: stats/cumulative_history.json 新設 (各セッション snapshot 保存) → ダッシュボード成長分析タブで時系列推移を可視化',
}

ds['last_updated'] = today
ds['session'] = '_59'
ds['last_session'] = '_59'

ds_path.write_text(json.dumps(ds, ensure_ascii=False, indent=2), encoding='utf-8')
print('dashboard_stats.json updated.')
print(f'Overview: GO={ov["go_total"]} confirmed={ov_conf} hit={ov["go_hit"]} hit_rate={ov["go_hit"]/ov_conf*100 if ov_conf else 0:.1f}% pnl={ov["go_pnl"]:+.3f}u')
