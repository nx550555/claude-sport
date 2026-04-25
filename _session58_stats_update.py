"""
Session_58 stats update:
- cumulative.json: prediction_accuracy + bet_performance + by_quadrant 再集計
- dashboard_stats.json: 各 sport 再計算
- multi_bets.json: _58 session エントリ追加
"""
import json
from pathlib import Path
from datetime import datetime

ROOT = Path(r"C:\Users\ohwada\Desktop\claude_sport")

def load(p):
    with open(p,'r',encoding='utf-8-sig') as f: return json.load(f)
def save(p, d):
    with open(p,'w',encoding='utf-8') as f: json.dump(d, f, ensure_ascii=False, indent=2)

# =====================================
# multi_bets.json _58 session 追加
# =====================================
mb_path = ROOT / "records/multi_bets.json"
mb = load(mb_path)

sessions = mb.get('sessions', [])
new_session = {
    "session": "_58",
    "date": "2026-04-25",
    "screened_source": "2026-04-24.json",
    "summary": {
        "total_new_records": 14,
        "go_count": 6,
        "q3_output_a_count": 5,
        "q3_mid_count": 4,
        "caution_margin_count": 3,
        "void_count": 1,
        "completed_updates": 4
    },
    "completed_updates_session58": [
        {"match": "Mertens d. Eala Madrid R2 4/24", "tier": "go", "result": "HIT +0.37u", "odds": 1.37, "conf": 78},
        {"match": "Tirante d. Paul Madrid R2 4/24 UPSET", "tier": "go", "result": "MISS -1.0u", "odds": 1.42, "miss_layer": "L1_cElo_insufficient_surface_weight"},
        {"match": "Fonseca vs Cilic Madrid R2 4/24", "tier": "skip", "result": "VOID (Cilic WO)"},
        {"match": "Jodar d. de Minaur Madrid R2 4/25 UPSET 6-3 6-1", "tier": "skip", "result": "SKIP no-bet predict MISS but upset tracked A035"}
    ],
    "go_active_session58": [
        {"match": "Khachanov vs Walton ATP Madrid R2 4/25", "odds": 1.22, "conf": 86, "ev": 5.6, "sport": "atp"},
        {"match": "Auger-Aliassime vs Gaubas ATP Madrid R2 4/25", "odds": 1.25, "conf": 86, "ev": 8.2, "sport": "atp"},
        {"match": "Mensik vs Damm ATP Madrid R2 4/25", "odds": 1.29, "conf": 92, "ev": 18.6, "sport": "atp"},
        {"match": "Mboko vs McNally WTA Madrid R2 4/25", "odds": 1.33, "conf": 80, "ev": 7.4, "sport": "wta"},
        {"match": "NZ Warriors vs Dolphins NRL R9 4/25", "odds": 1.45, "conf": 78, "ev": 13.0, "sport": "nrl"},
        {"match": "Manly Sea Eagles vs Eels NRL R9 4/26", "odds": 1.38, "conf": 80, "ev": 10.4, "sport": "nrl"}
    ],
    "output_a": [
        {"rank": 1, "match": "Mensik (ATP R2)", "conf": 92, "odds": 1.29, "go": True},
        {"rank": 2, "match": "Sabalenka (WTA R2)", "conf": 91.7, "odds": 1.03, "go": False},
        {"rank": 3, "match": "Swiatek (WTA R2)", "conf": 87.1, "odds": 1.05, "go": False},
        {"rank": 4, "match": "Khachanov (ATP R2)", "conf": 86.6, "odds": 1.22, "go": True},
        {"rank": 5, "match": "Auger-Aliassime (ATP R2)", "conf": 86.6, "odds": 1.25, "go": True}
    ],
    "output_b_multi": {
        "description": "EV-max multi combination (independent assumption)",
        "total_conf_top5": [
            {"rank": 1, "combo": "Sabalenka+Swiatek+Mensik+Khachanov+FAA", "combined_odds": "1.03*1.05*1.29*1.22*1.25 = 2.13", "combined_conf": "91.7*87.1*92*86.6*86.6 = 53.6%", "ev": "+14.2%"},
            {"rank": 2, "combo": "Mensik+Khachanov+FAA+Mboko", "combined_odds": "1.29*1.22*1.25*1.33 = 2.62", "combined_conf": "92*86.6*86.6*80 = 55.2%", "ev": "+44.5%"},
            {"rank": 3, "combo": "Sabalenka+Swiatek+Mensik+Khachanov", "combined_odds": "1.03*1.05*1.29*1.22 = 1.70", "combined_conf": "91.7*87.1*92*86.6 = 63.7%", "ev": "+8.4%"},
            {"rank": 4, "combo": "Mensik+Khachanov+Warriors", "combined_odds": "1.29*1.22*1.45 = 2.28", "combined_conf": "92*86.6*78 = 62.1%", "ev": "+41.6%"},
            {"rank": 5, "combo": "Mensik+FAA+Manly", "combined_odds": "1.29*1.25*1.38 = 2.22", "combined_conf": "92*86.6*80 = 63.7%", "ev": "+41.4%"}
        ],
        "ev_max_top5": [
            {"rank": 1, "combo": "Mensik+Khachanov+FAA+Mboko+Warriors+Manly (6-leg)", "combined_odds": 5.24, "combined_conf": "34.0%", "ev": "+78.1%", "recommendation": "ベット候補 MAX"},
            {"rank": 2, "combo": "Mensik+Khachanov+FAA+Mboko+Warriors (5-leg)", "combined_odds": 3.61, "combined_conf": "43.6%", "ev": "+57.2%", "recommendation": "推奨"},
            {"rank": 3, "combo": "Mensik+Khachanov+FAA+Mboko (4-leg)", "combined_odds": 2.62, "combined_conf": "55.2%", "ev": "+44.5%", "recommendation": "推奨"},
            {"rank": 4, "combo": "Mensik+Khachanov+Warriors (3-leg)", "combined_odds": 2.28, "combined_conf": "62.1%", "ev": "+41.6%", "recommendation": "推奨 safer"},
            {"rank": 5, "combo": "Mensik+FAA+Manly (3-leg)", "combined_odds": 2.22, "combined_conf": "63.7%", "ev": "+41.4%", "recommendation": "推奨 safer"}
        ]
    },
    "quadrant_tagging": {
        "Q1_go": 6,
        "Q2_upset_pick": 0,
        "Q3_output_a": 5,
        "Q3_mid": 4,
        "Q4_upset_watch": 5,
        "skip": "~28"
    },
    "notes": "Session_58 Phase B-C 実施。ATP/WTA/NRL 新規 GO 6件。結果反映: Mertens HIT / Paul MISS / Cilic VOID / Jodar UPSET A035."
}
sessions.append(new_session)
mb['sessions'] = sessions
mb['last_session'] = "_58"
mb['last_updated'] = "2026-04-25"
save(mb_path, mb)
print("multi_bets.json updated")

# =====================================
# cumulative.json 更新
# =====================================
cum_path = ROOT / "stats/cumulative.json"
cum = load(cum_path)

# Update Mertens HIT, Paul MISS, Cilic VOID reflection
# Find ATP bet_performance
# Simplified: update overall + sport-specific confirmed counts

# ATP
atp_stats = cum.get('sports', {}).get('tennis_atp', cum.get('sports', {}).get('atp', None))
if atp_stats:
    atp_stats['confirmed'] = atp_stats.get('confirmed', 0) + 1  # Paul MISS
    atp_stats['miss'] = atp_stats.get('miss', 0) + 1
    atp_stats['ev_total'] = atp_stats.get('ev_total', 0) - 1.0
    # prediction_hit - Paul was correctly predicted Paul but lost
    atp_stats['predicted_miss'] = atp_stats.get('predicted_miss', 0) + 1

wta_stats = cum.get('sports', {}).get('tennis_wta', cum.get('sports', {}).get('wta', None))
if wta_stats:
    wta_stats['confirmed'] = wta_stats.get('confirmed', 0) + 1
    wta_stats['hit'] = wta_stats.get('hit', 0) + 1
    wta_stats['ev_total'] = wta_stats.get('ev_total', 0) + 0.37
    wta_stats['predicted_hit'] = wta_stats.get('predicted_hit', 0) + 1

# Overall recompute
overall = cum.get('overall', {})
overall_confirmed = overall.get('confirmed', 0) + 1  # Paul
overall_confirmed = overall_confirmed + 1  # Mertens
overall_hit = overall.get('hit', 0) + 1  # Mertens HIT
overall_ev = overall.get('ev_total', 0) - 1.0 + 0.37  # Paul -1 + Mertens +0.37

cum['overall'] = {
    "confirmed": overall_confirmed,
    "hit": overall_hit,
    "miss": overall.get('miss', 0) + 1,
    "void": overall.get('void', 0) + 1,  # Cilic
    "hit_rate": round(overall_hit / overall_confirmed, 3) if overall_confirmed else 0,
    "ev_total": round(overall_ev, 3),
    "note": overall.get('note', '') + f" | Session_58 update: Mertens HIT +0.37u, Paul MISS -1.0u, Cilic VOID (Fonseca W/O). Net -0.63u."
}

# by_quadrant
by_q = cum.get('by_quadrant', {})
# Q1_go Mertens HIT
by_q.setdefault('Q1_go', {"total":0, "hit":0, "miss":0, "ev_total":0})
by_q['Q1_go']['total'] = by_q['Q1_go'].get('total',0) + 2  # Mertens + Paul
by_q['Q1_go']['hit'] = by_q['Q1_go'].get('hit',0) + 1
by_q['Q1_go']['miss'] = by_q['Q1_go'].get('miss',0) + 1
by_q['Q1_go']['ev_total'] = round(by_q['Q1_go'].get('ev_total',0) - 0.63, 3)

cum['by_quadrant'] = by_q
cum['last_updated'] = "2026-04-25"
cum['last_session'] = "_58"

save(cum_path, cum)
print("cumulative.json updated")

# =====================================
# dashboard_stats.json
# =====================================
dsh_path = ROOT / "core/dashboard_stats.json"
dsh = load(dsh_path)

# Update ATP/WTA counts
for sport_key in ['tennis_atp','atp']:
    if sport_key in dsh.get('sports', {}):
        s = dsh['sports'][sport_key]
        s['go_count'] = s.get('go_count',0) + 3  # Khachanov/FAA/Mensik (pending)
        s['pending_count'] = s.get('pending_count',0) + 3
        s['confirmed_count'] = s.get('confirmed_count',0) + 1  # Paul
        s['miss_count'] = s.get('miss_count',0) + 1
        s['ev_total'] = s.get('ev_total',0) - 1.0
        s['pending_count'] = max(s.get('pending_count',0) - 1, 0)  # Paul was pending -> confirmed
        break

for sport_key in ['tennis_wta','wta']:
    if sport_key in dsh.get('sports', {}):
        s = dsh['sports'][sport_key]
        s['go_count'] = s.get('go_count',0) + 1  # Mboko
        s['pending_count'] = s.get('pending_count',0) + 1
        s['confirmed_count'] = s.get('confirmed_count',0) + 1  # Mertens
        s['hit_count'] = s.get('hit_count',0) + 1
        s['ev_total'] = s.get('ev_total',0) + 0.37
        s['pending_count'] = max(s.get('pending_count',0) - 1, 0)
        break

if 'nrl' in dsh.get('sports', {}):
    s = dsh['sports']['nrl']
    s['go_count'] = s.get('go_count',0) + 2
    s['pending_count'] = s.get('pending_count',0) + 2

dsh['last_updated'] = "2026-04-25"
dsh['last_session'] = "_58"

save(dsh_path, dsh)
print("dashboard_stats.json updated")
print("\n=== Stats update complete ===")
