"""
Update past-date items:
1. Add WTA Tan vs Bondar GO entry (retroactive) with HIT
2. Update dashboard_stats.json for WTA + overview
"""
import json, sys, datetime
sys.stdout.reconfigure(encoding='utf-8')

base = r"C:\Users\ohwada\Desktop\claude_sport"

# ===== 1. Update WTA JSON: Add Bondar/Tan GO entry =====
with open(f'{base}/records/wta/2026.json', 'r', encoding='utf-8-sig') as f:
    wta = json.load(f)

bondar_entry = {
    "tournament": "WTA Rouen (Open Capfinances Rouen Metropole)",
    "round": "R1",
    "date": "2026-04-15",
    "start_time": "18:30",
    "match": "Tan H. vs Bondar A.",
    "retroactive": True,
    "retroactive_note": "Session 36/37: GO entry added retroactively. Match found in dashboard active section but was missing from JSON records.",
    "celo_note": "Hard cElo source limited. Market+form analysis used. Market implied Bondar 82.6%.",
    "l1_diff": None,
    "l1_pass": None,
    "tier": "go",
    "rec": "Bondar",
    "rec_odds": 1.21,
    "ev_est": 6.5,
    "confidence": 88,
    "ev_calc": "(0.88 x 1.21) - 1 = +6.5%",
    "skip_reason": None,
    "result": "Bondar A.",
    "score": "6-2 4-6 6-0",
    "hit": True,
    "actual_ev": 0.21,
    "predicted_winner": "Bondar A.",
    "prediction_confidence": 88,
    "prediction_hit": True,
    "status": "completed",
    "note": "WTA Rouen indoor hard. Market+form: Bondar 88% conf. EV+6.5% @1.21. RESULT: Bondar d. Tan 6-2 4-6 6-0 (news.de/WTA Official confirmed 2026-04-15). HIT. actual_ev = 1.21-1 = 0.21u.",
    "sources": ["https://www.news.de/sport/859523515/wta-tennis-15-04-2026-in-frankreich-liveticker-harmony-tan-gegen-anna-bondar/1/", "https://www.wtatennis.com/tournaments/2066/rouen/2026/scores/LS028"]
}

# Find WTA Rouen tournament and add entry
for t in wta['tournaments']:
    if 'Rouen' in t.get('name', ''):
        t['predictions'].append(bondar_entry)
        print(f"Added Bondar entry to {t['name']}. Total predictions: {len(t['predictions'])}")
        break

# Update summary
old_total = wta['summary']['total']
old_hit = wta['summary']['hit']
new_total = old_total + 1
new_hit = old_hit + 1
new_hit_rate = round(new_hit / new_total, 3)
new_pnl = round(wta['summary']['ev_total'] + 0.21, 4)
wta['summary']['total'] = new_total
wta['summary']['hit'] = new_hit
wta['summary']['hit_rate'] = new_hit_rate
wta['summary']['ev_total'] = new_pnl
wta['summary']['note'] = f"GOまたはGAMBLE_BET tier推奨のみカウント。GB001 Ostapenko HIT(+0.5375u)。Paolini Stuttgart R1 MISS(-1.0u)。Bondar Rouen R1 HIT(+0.21u)。通算: {new_hit}/{new_total} {round(new_hit_rate*100,1)}% {new_pnl}u"

with open(f'{base}/records/wta/2026.json', 'w', encoding='utf-8') as f:
    json.dump(wta, f, ensure_ascii=False, indent=2)
print(f"WTA JSON updated: {old_total}->{new_total} GO, {old_hit}->{new_hit} HIT, pnl->{new_pnl}")

# ===== 2. Update dashboard_stats.json =====
with open(f'{base}/core/dashboard_stats.json', 'r', encoding='utf-8-sig') as f:
    ds = json.load(f)

# WTA update
ds['sports']['wta']['go_count'] = new_total
ds['sports']['wta']['confirmed_count'] = new_total
ds['sports']['wta']['hit_count'] = new_hit
ds['sports']['wta']['hit_rate'] = new_hit_rate
ds['sports']['wta']['pnl'] = new_pnl
ds['sports']['wta']['pending_count'] = 0

# Overview update
ds['overview']['total_go'] = ds['overview']['total_go'] + 1       # 27->28
ds['overview']['total_confirmed'] = ds['overview']['total_confirmed'] + 1  # 22->23
ds['overview']['total_hits'] = ds['overview']['total_hits'] + 1   # 17->18
total_conf = ds['overview']['total_confirmed']
total_hits = ds['overview']['total_hits']
ds['overview']['hit_rate'] = round(total_hits / total_conf, 3)
ds['overview']['total_pnl'] = round(ds['overview']['total_pnl'] + 0.21, 2)
# Remove ATP x1 + WTA x1 from pending breakdown (already resolved)
ds['overview']['total_pending'] = 5
ds['overview']['pending_breakdown'] = "UFL x2 + NRL x1 + SL x2"

ds['last_updated'] = "2026-04-16"
ds['session'] = "_37"

with open(f'{base}/core/dashboard_stats.json', 'w', encoding='utf-8') as f:
    json.dump(ds, f, ensure_ascii=False, indent=2)
print("dashboard_stats.json updated:")
print(f"  WTA: {new_total} GO, {new_hit} HIT, {round(new_hit_rate*100,1)}% hit rate, pnl={new_pnl}")
print(f"  Overview: total_go={ds['overview']['total_go']}, confirmed={ds['overview']['total_confirmed']}, hits={ds['overview']['total_hits']}, hit_rate={ds['overview']['hit_rate']}, pnl={ds['overview']['total_pnl']}")
