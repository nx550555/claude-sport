"""Session_57 Part 2: 追加 WTA + SL 結果反映"""
import json
from pathlib import Path

ROOT = Path("C:/Users/ohwada/Desktop/claude_sport")

def load_json(p):
    with open(p, encoding="utf-8-sig") as f:
        return json.load(f)

def save_json(p, d):
    with open(p, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)

# ============ WTA Madrid 追加反映 ============
wta_path = ROOT / "records/wta/2026.json"
wta = load_json(wta_path)

madrid_idx = None
for i, t in enumerate(wta["tournaments"]):
    if "Madrid" in t.get("name", ""):
        madrid_idx = i
        break

madrid_preds = wta["tournaments"][madrid_idx]["predictions"]

wta_updates = {
    4: {  # Svitolina vs Bondar → Bondar UPSET
        "result": "Bondar d. Svitolina",
        "score": "6-3 6-4",
        "prediction_hit": False,
        "outcome_note": "UPSET realized (skip tier, no-bet). Bondar first career top-10 win. 6 aces / 6/6 BP saved. Svitolina MISS.",
        "miss_layer": "L1_elo_underestimate",
        "miss_analysis": "Bondar HUN clay specialist + Svitolina post-surgery return form dip. 27 winners / 9 unforced errors from Bondar 示す overwhelming performance. P009 (injury comeback overrated) の逆方向: Svitolina が過大評価され Bondar が正当評価に戻った。",
        "rule_linked": "P009_reverse_candidate",
        "verification_sources": ["tennistonic.com Bondar surprises Svitolina", "skysports.com Bondar vs Svitolina Madrid Highlights", "yournews.com Bondar upends Svitolina"],
    },
    5: {  # Starodubtseva vs Cristian → Cristian HIT
        "result": "Cristian d. Starodubtseva",
        "score": "6-3 6-7(5) 6-4",
        "prediction_hit": True,
        "outcome_note": "Cristian HIT (skip tier, no-bet). Starodubtseva LL squandered 3 match points in Set 2 TB. dramatic 3 sets.",
        "verification_sources": ["news.de Starodubtseva vs Cristian", "mezha.net Starodubtseva lost to Cristian"],
    },
    7: {  # Wang X. vs Samson L. → Wang HIT (Samson retired)
        "result": "Wang d. Samson (Samson RET Set 3)",
        "score": "6-2 3-6 0-5 RET",
        "prediction_hit": True,
        "hit": None,
        "actual_ev": 0.0,
        "outcome_note": "Q4_upset_watch caution_margin - UPSET not realized initially but Samson retired in 3rd set. Wang HIT via retirement. L4_External: Samson injury.",
        "verification_sources": ["wtatennis.com Wang vs Samson Round of 64", "tennismajors.com Xinyu Wang vs Laura Samsonova"],
    },
    8: {  # Shnaider vs Bouzas → Shnaider HIT
        "result": "Shnaider d. Bouzas Maneiro",
        "score": "3-6 7-5 6-1",
        "prediction_hit": True,
        "outcome_note": "Shnaider HIT (skip tier). 1st career H2H. Bouzas took set 1, Shnaider dominated sets 2-3.",
        "verification_sources": ["tennistonic.com Shnaider Bouzas Maneiro prediction", "wtatennis.com Shnaider Bouzas R64"],
    },
    12: {  # Bouzkova vs Kalinina → Kalinina HIT (winner confirmed via Osaka R3 opponent)
        "result": "Kalinina d. Bouzkova",
        "score": "確認中 (indirect confirmation via Osaka R3 opponent)",
        "prediction_hit": True,
        "outcome_note": "skip tier, no-bet. Kalinina HIT confirmed indirectly (Osaka R3 vs Kalinina). score unverified - needs direct confirmation next session.",
        "verification_status": "WINNER_CONFIRMED_SCORE_PENDING",
        "verification_sources": ["tennisworldusa.org Osaka to face qualifier in 3R (Kalinina)", "tennistonic.com Osaka ousts Osorio (Kalinina next)"],
    },
    13: {  # Ann Li vs Parks → Li HIT
        "result": "Li d. Parks",
        "score": "6-2 6-7(5) 6-3",
        "prediction_hit": True,
        "hit": None,
        "actual_ev": 0.0,
        "outcome_note": "Q4_upset_watch caution_margin UPSET not realized. Li HIT in 3 sets all-American match. Li best Madrid result tied.",
        "verification_sources": ["tennistonic.com Ann Li wins against Parks", "thestatszone.com Parks vs Li Preview"],
    },
    15: {  # Jovic vs Linette → Jovic HIT
        "result": "Jovic d. Linette",
        "score": "6-4 6-1",
        "prediction_hit": True,
        "outcome_note": "Jovic HIT (skip tier). 15-seed 16-ranked American dominant 69min. H2H 2-0 Jovic.",
        "verification_sources": ["profootballnetwork.com Jovic vs Linette preview", "en.tennistemple.com Jovic defeats Linette Madrid R2"],
    },
}

for idx, upd in wta_updates.items():
    p = madrid_preds[idx]
    for k, v in upd.items():
        p[k] = v

wta["last_updated"] = "2026-04-24"
save_json(wta_path, wta)
print(f"WTA Madrid updated (part2): {len(wta_updates)} entries")

# ============ Super League 反映 ============
sl_path = ROOT / "records/superleague/2026.json"
sl = load_json(sl_path)
sl_key = "games" if "games" in sl else "predictions"

sl_updates = {
    2: {  # York vs Toulouse 4/23
        "result": "York 38-14 Toulouse",
        "score": "38-14",
        "winner": "York Knights",
        "prediction_hit": True,
        "outcome_note": "York HIT (skip tier, no-bet). Scott Galeano hat-trick. dominance at LNER Community Stadium.",
        "verification_sources": ["skysports.com Galeano hat-trick York beat Toulouse"],
    },
    3: {  # Leigh vs Huddersfield 4/23
        "result": "Leigh 30-16 Huddersfield",
        "score": "30-16",
        "winner": "Leigh Leopards",
        "prediction_hit": True,
        "outcome_note": "Leigh HIT (skip tier). Josh Charnley 400th appearance + 2 tries. AJ Towse 2 tries + Senior 1 + Lam penalty try.",
        "verification_sources": ["skysports.com Super League Leigh win Huddersfield"],
    },
}

for idx, upd in sl_updates.items():
    g = sl[sl_key][idx]
    for k, v in upd.items():
        g[k] = v

sl["last_updated"] = "2026-04-24"
save_json(sl_path, sl)
print(f"SL updated: {len(sl_updates)} entries")
