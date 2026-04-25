"""Session_59 STEP F: cumulative_history.json 新設 + Session ごとの snapshot 保存
   将来 dashboard 成長分析タブで時系列推移を可視化するためのインフラ"""
import json
from pathlib import Path
from datetime import datetime

base = Path(r'C:\Users\ohwada\Desktop\claude_sport')
ds = json.load(open(base / 'core' / 'dashboard_stats.json', encoding='utf-8-sig'))
audit = json.load(open(base / 'stats' / '_audit_recalc.json', encoding='utf-8'))
hist_path = base / 'stats' / 'cumulative_history.json'

# 既存 history 読み込み or 新規
if hist_path.exists():
    hist = json.load(open(hist_path, encoding='utf-8-sig'))
else:
    hist = {
        '_description': 'セッションごとの累積統計スナップショット。dashboard 成長分析タブで時系列推移を表示する真値ソース。',
        '_created': '2026-04-25 Session_59',
        '_format': '各エントリは {session, date, overall, advanced, basic, by_quadrant, sports} を含む完全スナップショット',
        '_update_rule': 'セッション終了時に必ず追記する (CLAUDE.md セッション終了手順に追加予定)',
        'snapshots': []
    }

ov = ds['overview']
adv = ds['by_tier']['advanced']
basic = ds['by_tier']['basic']

# 新規 snapshot 構築
snapshot = {
    'session': '_59',
    'date': '2026-04-25',
    'timestamp': datetime.now().isoformat(timespec='seconds'),
    'overall': {
        'go_total': ov.get('total_go'),
        'confirmed': ov.get('total_confirmed'),
        'hits': ov.get('total_hits'),
        'misses': ov.get('total_confirmed', 0) - ov.get('total_hits', 0),
        'pending': ov.get('total_pending'),
        'hit_rate': ov.get('hit_rate'),
        'pnl': ov.get('total_pnl'),
    },
    'by_tier': {
        'advanced': {
            'go': adv.get('go_count'),
            'confirmed': adv.get('confirmed_count'),
            'hit': adv.get('hit_count'),
            'pnl': adv.get('pnl'),
            'pending': adv.get('pending_count'),
            'hit_rate': adv.get('hit_rate'),
        },
        'basic': {
            'go': basic.get('go_count'),
            'confirmed': basic.get('confirmed_count'),
            'hit': basic.get('hit_count'),
            'pnl': basic.get('pnl'),
            'pending': basic.get('pending_count'),
            'hit_rate': basic.get('hit_rate'),
        },
    },
    'by_quadrant': {
        'Q1_go': {
            'total': ov.get('total_go'),
            'confirmed': ov.get('total_confirmed'),
            'hit': ov.get('total_hits'),
            'pnl': ov.get('total_pnl'),
        },
        'Q3_output_a': {
            'total': audit['_q3_total']['t'],
            'confirmed': audit['_q3_total']['c'],
            'hit': audit['_q3_total']['h'],
            'hit_rate': round(audit['_q3_total']['h']/audit['_q3_total']['c'], 3) if audit['_q3_total']['c'] else None,
        },
        'Q3_mid': {
            'total': audit['_q3_mid_total']['t'],
            'confirmed': audit['_q3_mid_total']['c'],
            'hit': audit['_q3_mid_total']['h'],
        },
        'Q4_upset_watch': {
            'total': audit['_q4_total']['t'],
            'confirmed': audit['_q4_total']['c'],
            'upset_realized': audit['_q4_total']['u'],
            'fav_hit': audit['_q4_total']['f'],
            'detect_rate': round(audit['_q4_total']['u']/audit['_q4_total']['c'], 3) if audit['_q4_total']['c'] else None,
        },
    },
    'sports': {k: {
        'go': v.get('go_count'),
        'confirmed': v.get('confirmed_count'),
        'hit': v.get('hit_count'),
        'hit_rate': v.get('hit_rate'),
        'pnl': v.get('pnl'),
        'pending': v.get('pending_count'),
    } for k, v in ds.get('sports', {}).items()},
    'session_summary': 'Session_59 STEP A-E 真値再計算完了。MC 二重ファイル archived 化 + WTA 重複統合 + cumulative/dashboard_stats 全種目実測再集計。STEP F (本 history) 開始。',
}

# 同 session 重複防止
hist['snapshots'] = [s for s in hist.get('snapshots', []) if s.get('session') != '_59']
hist['snapshots'].append(snapshot)
hist['_last_updated'] = '2026-04-25'
hist['_last_session'] = '_59'

# 過去 session の snapshot を BACKLOG / cumulative.session_*_note から遡及作成 (現在値のみ)
# Session_43 / 47 / 48 / 49 / 50 / 56 / 57 / 58 の主要 metrics を BACKLOG ベースで補填
legacy = [
    {'session': '_43', 'date': '2026-04-20', 'overall': {'confirmed': 28, 'hits': 20, 'hit_rate': 0.714, 'pnl': 1.733}, 'note': 'BACKLOG/CLAUDE.md より遡及補填'},
    {'session': '_47', 'date': '2026-04-21', 'overall': {'confirmed': 29, 'hits': 21, 'hit_rate': 0.724, 'pnl': 1.90}, 'note': 'BACKLOG より遡及補填'},
    {'session': '_48', 'date': '2026-04-22', 'overall': {'confirmed': 29, 'hits': 21, 'hit_rate': 0.724, 'pnl': 1.90, 'pending': 1}, 'note': 'BACKLOG (Galfi pending)'},
    {'session': '_49', 'date': '2026-04-23', 'overall': {'confirmed': 30, 'hits': 22, 'hit_rate': 0.733, 'pnl': 2.453}, 'note': 'BACKLOG (Galfi HIT 反映)'},
    {'session': '_50', 'date': '2026-04-23', 'overall': {'confirmed': 30, 'hits': 22, 'hit_rate': 0.733, 'pnl': 2.453}, 'note': 'BACKLOG (G2 SKIP のため変化なし)'},
    {'session': '_57', 'date': '2026-04-24', 'overall': {'confirmed': 32, 'hits': 23, 'hit_rate': 0.719, 'pnl': 1.473, 'pending': 1}, 'note': 'BACKLOG (Paul MISS / Mertens pending)'},
    {'session': '_58', 'date': '2026-04-25', 'overall': {'confirmed': 32, 'hits': 23, 'hit_rate': 0.719, 'pnl': 1.80, 'pending': 6}, 'note': 'CLAUDE.md / cumulative session_58_update'},
]
existing_sessions = {s['session'] for s in hist['snapshots']}
for leg in legacy:
    if leg['session'] not in existing_sessions:
        hist['snapshots'].append(leg)
hist['snapshots'].sort(key=lambda s: s.get('session', ''))

hist_path.write_text(json.dumps(hist, ensure_ascii=False, indent=2), encoding='utf-8')
print(f'cumulative_history.json saved with {len(hist["snapshots"])} snapshots.')
for s in hist['snapshots']:
    o = s.get('overall', {})
    print(f"  {s['session']:5} {s['date']}: {o.get('hits','?')}/{o.get('confirmed','?')} = {o.get('hit_rate','?')} pnl={o.get('pnl','?')}")
