# Session_45: 2026-04-20.json upcoming matches - bulk screening with new procedure
# Steps: Market-implied prob + output-A candidate tag + UPSET_PICK candidate flag
import json
from pathlib import Path

BASE = Path(r"C:\Users\ohwada\Desktop\claude_sport")
src = json.load(open(BASE / "手動試合データ" / "2026-04-20.json", encoding="utf-8-sig"))

# Parse upcoming matches across all tournaments
def get_team_side(m, key):
    return m.get(key) or m.get(f"team{key[-1]}" if "team" in key else f"player{key[-1]}")

def implied(odds):
    return round(100/odds)

def margin_adj(odds, margin=0.05):
    return round(100/odds * (1-margin))

# Bucket matches
summary = []

for t in src.get("tournaments", []):
    tname = t.get("tournament","")
    sport = t.get("sport","")
    upcoming = t.get("matches",{}).get("upcoming",[])
    for m in upcoming:
        p1 = m.get("player1") or m.get("team1")
        p2 = m.get("player2") or m.get("team2")
        odds = m.get("odds",{})
        o1 = odds.get("player1") or odds.get("team1")
        o2 = odds.get("player2") or odds.get("team2")
        if not (p1 and p2 and o1 and o2):
            continue
        if o1 <= o2:
            fav, fav_o, dog, dog_o = p1, o1, p2, o2
        else:
            fav, fav_o, dog, dog_o = p2, o2, p1, o1
        fav_imp = implied(fav_o)
        fav_conf = margin_adj(fav_o)
        divergence_pp = fav_imp - implied(dog_o)
        date = m.get("date","")
        stime = m.get("start_time","")
        # tier categorization
        if fav_conf >= 85:
            tag = "OUTPUT_A_CANDIDATE"
        elif fav_conf >= 75 and fav_o >= 1.05:
            tag = "GO_CANDIDATE"
        elif dog_o >= 3.0 and divergence_pp >= 40:
            tag = "UPSET_PICK_CHECK"  # check UF factors
        elif 45 <= fav_conf <= 55:
            tag = "PICK_EM"
        else:
            tag = "SKIP_MARKET"
        summary.append({
            "tournament": tname,
            "sport": sport,
            "date": date,
            "time": stime,
            "match": f"{p1} vs {p2}",
            "fav": fav,
            "fav_odds": fav_o,
            "fav_conf": fav_conf,
            "dog": dog,
            "dog_odds": dog_o,
            "divergence_pp": divergence_pp,
            "tag": tag
        })

# Print per tag
from collections import Counter
tag_count = Counter(x["tag"] for x in summary)
print(f"Total upcoming matches: {len(summary)}")
print(f"Tag distribution: {dict(tag_count)}")

print("\n=== OUTPUT_A_CANDIDATE (fav_conf >= 85%) ===")
for x in [x for x in summary if x["tag"]=="OUTPUT_A_CANDIDATE"]:
    print(f"  {x['date']} {x['sport']}/{x['tournament'][:30]} | {x['fav']}({x['fav_odds']}, {x['fav_conf']}%) vs {x['dog']}({x['dog_odds']})")

print("\n=== GO_CANDIDATE (conf 75-84%) ===")
for x in [x for x in summary if x["tag"]=="GO_CANDIDATE"]:
    print(f"  {x['date']} {x['sport']}/{x['tournament'][:30]} | {x['fav']}({x['fav_odds']}, {x['fav_conf']}%) vs {x['dog']}({x['dog_odds']})")

print("\n=== UPSET_PICK_CHECK (dog>=3.0, div>=40pp) ===")
for x in [x for x in summary if x["tag"]=="UPSET_PICK_CHECK"]:
    print(f"  {x['date']} {x['sport']}/{x['tournament'][:30]} | {x['fav']}({x['fav_odds']}) vs {x['dog']}({x['dog_odds']})")

print("\n=== PICK_EM (45-55% confidence) ===")
for x in [x for x in summary if x["tag"]=="PICK_EM"]:
    print(f"  {x['date']} {x['sport']}/{x['tournament'][:30]} | {x['fav']}({x['fav_odds']}) vs {x['dog']}({x['dog_odds']})")

# Save to scratch
with open(BASE / "scripts" / "s45_screening_summary.json", "w", encoding="utf-8") as f:
    json.dump(summary, f, ensure_ascii=False, indent=2)

print(f"\nSaved to scripts/s45_screening_summary.json")
