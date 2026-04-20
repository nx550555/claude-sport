# Session_45: A014-A020本体登録漏れ補填 + ATP Madrid Q R1 UPSET 4件 + 遡及分析
import json

path = r"C:\Users\ohwada\Desktop\claude_sport\stats\upset_patterns.json"
d = json.load(open(path, encoding="utf-8-sig"))
cu = d.setdefault("confirmed_upsets", [])

new_upsets = [
    {
        "upset_id": "A014",
        "date": "2026-04-17",
        "sport": "tennis_atp",
        "tournament": "BMW Open Munich",
        "round": "R2",
        "match": "Kopriva V. vs Darderi L.",
        "market_favorite": "Darderi L.",
        "fav_odds": 1.37,
        "dog_odds": 3.0,
        "result": "Kopriva d. Darderi (come-from-behind, R1 upset then R2 win)",
        "uf_count": 3,
        "uf_factors": {
            "UF02": "Kopriva R1 for Engel(WC) momentum (R1 upset winner)",
            "UF05": "Darderi clay fav but rally stamina limits (Kopriva Rio SF grade clay rally experience)",
            "UFA03": "mental reset after 2 set down win"
        },
        "market_divergence_pp": 20,
        "upset_pick_feasibility": "UF3 + 20pp > 15pp -> UPSET_PICK condition met. R020 (R1 upsetter R2 momentum) not yet implemented at time of match.",
        "rule_linked": "R020"
    },
    {
        "upset_id": "A015",
        "date": "2026-04-17",
        "sport": "tennis_atp",
        "tournament": "BMW Open Munich",
        "round": "R2",
        "match": "Shapovalov D.(4) vs Marozsan F.",
        "market_favorite": "Marozsan F.",
        "fav_odds": 1.73,
        "dog_odds": 2.1,
        "result": "Shapovalov d. Marozsan 7-6(7) 6-2",
        "uf_count": 2,
        "uf_factors": {
            "UFA02": "Shapovalov R1 3-set drain (Griekspoor) fatigue residue",
            "UF05": "Marozsan R1 upset winner (Tsitsipas) R2 reversion pattern"
        },
        "market_divergence_pp": 10,
        "upset_pick_feasibility": "UF2 + 10pp < 15pp. UPSET_PICK not met. CAUTION (no bet) would have been appropriate.",
        "rule_linked": "P014 (R021 candidate)"
    },
    {
        "upset_id": "A016",
        "date": "2026-04-17",
        "sport": "ufl",
        "tournament": "UFL Week 4",
        "round": "RS",
        "match": "Columbus Aviators at Arlington Renegades",
        "market_favorite": "Arlington Renegades",
        "fav_odds": 1.36,
        "dog_odds": 3.0,
        "result": "Aviators 28-14 Renegades UPSET",
        "uf_count": 4,
        "uf_factors": {
            "UF01": "Aviators (expansion 0-3) first home game desire",
            "UF02": "Renegades QB Reed 13/27 48% big drop from season avg",
            "UF03": "Aviators 202 rushing yds (2x of Renegades 97)",
            "UF04": "TOP 36:38 vs 23:22 time control dominance"
        },
        "market_divergence_pp": 25,
        "upset_pick_feasibility": "UF4 + 25pp - UPSET_PICK condition FULLY MET. Week3 narrow loss to home rematch is P015 textbook case. Should have been UPSET_PICK at 3.0 instead of fav GO at 1.36. This is the CRITICAL screening miss.",
        "rule_linked": "P015 / U008_modified",
        "critical_note": "This is the paradigm case of UF factor check being skipped. Resulted in -1.0u loss. Root cause: screening did not run UF factor walkthrough after L1-L4."
    },
    {
        "upset_id": "A017",
        "date": "2026-04-17",
        "sport": "tennis_atp",
        "tournament": "BMW Open Munich",
        "round": "QF",
        "match": "Fonseca J. vs Shelton B.",
        "market_favorite": "Shelton B.",
        "fav_odds": 1.44,
        "dog_odds": 2.8,
        "result": "Fonseca d. Shelton",
        "uf_count": 2,
        "uf_factors": {
            "UF02": "Fonseca 19yo breakout + MC2026 momentum",
            "UFA04": "Shelton clay weakness (hard/grass type)"
        },
        "market_divergence_pp": 15,
        "upset_pick_feasibility": "UF2 + 15pp - borderline. CAUTION no-bet would have been right.",
        "rule_linked": None
    },
    {
        "upset_id": "A018",
        "date": "2026-04-17",
        "sport": "tennis_atp",
        "tournament": "BMW Open Munich",
        "round": "QF",
        "match": "Molcan A.(Q) vs Shapovalov D.(4)",
        "market_favorite": "Shapovalov D.",
        "fav_odds": 1.58,
        "dog_odds": 2.4,
        "result": "Molcan d. Shapovalov (QF 3 straight fav takedown)",
        "uf_count": 4,
        "uf_factors": {
            "UF02": "Molcan 3 straight fav takedown momentum (Bublik then Altmaier then Shapovalov)",
            "UF05": "Shapovalov R1 Griekspoor 3-set drain fatigue residue",
            "UFA03": "Molcan 84% 1stSrvPts vs Altmaier high form data",
            "UF06": "Shapovalov 4-match winstreak mental peak past"
        },
        "market_divergence_pp": 16,
        "upset_pick_feasibility": "UF4 + 16pp - UPSET_PICK met. Molcan momentum (P013=R020 source) recognized but not extracted as UPSET_PICK.",
        "rule_linked": "R020"
    },
    {
        "upset_id": "A019",
        "date": "2026-04-17",
        "sport": "tennis_atp",
        "tournament": "Barcelona Open",
        "round": "QF",
        "match": "Jodar R.(WC) vs Norrie C.",
        "market_favorite": "Norrie C.",
        "fav_odds": 1.53,
        "dog_odds": 2.5,
        "result": "Jodar d. Norrie (19yo first ATP500 SF)",
        "uf_count": 3,
        "uf_factors": {
            "UF02": "Jodar(WC Spain 19yo) consecutive round momentum",
            "UF01": "Barcelona home crowd advantage",
            "UFA02": "Norrie R1 Wawrinka 3-set drain residue"
        },
        "market_divergence_pp": 13,
        "upset_pick_feasibility": "UF3 + 13pp < 15pp - borderline below. CAUTION with contrarian lean. R017 (P010) source.",
        "rule_linked": "R017"
    },
    {
        "upset_id": "A020",
        "date": "2026-04-19",
        "sport": "super_league",
        "tournament": "Super League R8",
        "round": "RS",
        "match": "Warrington Wolves at Catalans Dragons",
        "market_favorite": "Warrington Wolves",
        "fav_odds": 1.64,
        "dog_odds": 2.3,
        "result": "Catalans 38-22 Warrington (Dodd hat-trick)",
        "uf_count": 3,
        "uf_factors": {
            "UF01": "Catalans France home + home crowd (away-to-France travel)",
            "UF02": "Dodd individual explosion (hat-trick)",
            "UFA04": "Warrington travel fatigue away to France"
        },
        "market_divergence_pp": 10,
        "upset_pick_feasibility": "UF3 + 10pp < 15pp - below. Catalans home correction -5% to -7/-10% would have dropped to CAUTION (P016 candidate).",
        "rule_linked": "P016"
    },
    # Madrid Q R1 UPSETs
    {
        "upset_id": "A022", "date": "2026-04-20", "sport": "tennis_atp",
        "tournament": "Madrid Open Qualifying", "round": "Q R1",
        "match": "Svajda Z. vs Sakamoto R.",
        "market_favorite": "Sakamoto R.", "fav_odds": 1.59, "dog_odds": 2.27,
        "result": "Svajda d. Sakamoto",
        "uf_count": 1,
        "uf_factors": {"UFA05": "Svajda(US) vs Sakamoto(JPN jr) - market misprice, Svajda likely had edge"},
        "market_divergence_pp": 13,
        "upset_pick_feasibility": "UF1 + 13pp - not met. L1=market_implied limitation example.",
        "rule_linked": None
    },
    {
        "upset_id": "A023", "date": "2026-04-20", "sport": "tennis_atp",
        "tournament": "Madrid Open Qualifying", "round": "Q R1",
        "match": "Gea A. vs Gaubas V.",
        "market_favorite": "Gaubas V.", "fav_odds": 1.72, "dog_odds": 2.05,
        "result": "Gea d. Gaubas",
        "uf_count": 0,
        "uf_factors": {"_note": "near pick-em (8pp); UF details unknown"},
        "market_divergence_pp": 8,
        "upset_pick_feasibility": "UF0 + 8pp - noise range. Not UPSET_PICK.",
        "rule_linked": None
    },
    {
        "upset_id": "A024", "date": "2026-04-20", "sport": "tennis_atp",
        "tournament": "Madrid Open Qualifying", "round": "Q R1",
        "match": "Virtanen O. vs Drogue T.",
        "market_favorite": "Drogue T.", "fav_odds": 1.72, "dog_odds": 2.05,
        "result": "Virtanen d. Drogue",
        "uf_count": 1,
        "uf_factors": {"UFA05": "Virtanen(FIN ATP tour #140) vs Drogue(FRA jr unknown) - market underpriced Virtanen"},
        "market_divergence_pp": 8,
        "upset_pick_feasibility": "UF1 + 8pp - below UPSET_PICK. cElo lookup could have flipped fav via L1.",
        "rule_linked": None
    },
    {
        "upset_id": "A025", "date": "2026-04-20", "sport": "tennis_atp",
        "tournament": "Madrid Open Qualifying", "round": "Q R1",
        "match": "Darwin B. vs Bonzi B.",
        "market_favorite": "Bonzi B.", "fav_odds": 1.61, "dog_odds": 2.22,
        "result": "Darwin d. Bonzi",
        "uf_count": 1,
        "uf_factors": {"UFA06": "Bonzi Top 100 ATP vet lost to unknown Darwin - veteran Q-round motivation risk (deep dive needed)"},
        "market_divergence_pp": 12,
        "upset_pick_feasibility": "UF1 + 12pp - below UPSET_PICK. Possibly Top100 Q-match motivation crisis rule worth tracking (P017 candidate).",
        "rule_linked": "P017-candidate"
    }
]

existing_ids = {u.get("upset_id") for u in cu}
added = 0
for nu in new_upsets:
    if nu["upset_id"] not in existing_ids:
        cu.append(nu)
        added += 1

# rule_improvement_candidates
ric = d.setdefault("rule_improvement_candidates", [])
ric.append({
    "session_added": "_45",
    "date": "2026-04-20",
    "title": "Session_30-43 SKIP match UF factor retro",
    "method": "Re-evaluate A014-A025 UF factor count + market divergence vs UPSET_PICK condition (UF>=3 AND divergence>=15pp)",
    "findings": {
        "total_reviewed": 12,
        "condition_met_in_hindsight": ["A014 UF3+20pp", "A016 UF4+25pp CRITICAL", "A018 UF4+16pp"],
        "borderline": ["A017 UF2+15pp", "A019 UF3+13pp", "A020 UF3+10pp"],
        "not_applicable": ["A015", "A022", "A023", "A024", "A025"],
        "critical_miss": "A016 Aviators vs Renegades UF4+25pp textbook case. Fav GO @1.36 MISS -1.0u. Should have been UPSET_PICK @3.0. Screening skipped UF walkthrough."
    },
    "rule_proposals": [
        {
            "id": "P017_candidate",
            "title": "Veteran ATP Q-round motivation crisis adjustment",
            "desc": "Top100 player in Masters Qualifying R1 vs unknown: -5% motivation correction (A025 Bonzi MISS trigger)",
            "evidence": 1,
            "threshold": 3
        }
    ],
    "new_procedure": {
        "before": "L1-L4 then conf/EV then GO/SKIP",
        "after": "L1-L4 fav conf then UF factor FULL WALKTHROUGH then GEN005 table match then GO/CAUTION/UPSET_PICK/SKIP. Output-A tag by separate axis (certainty >= 85%).",
        "integration": "From 2026-04-20 Session_45 onward, mandatory screening process"
    }
})

d["last_updated"] = "2026-04-20"
d["updated_by"] = "Session_45 case-C retro + Madrid Q R1 upsets"

with open(path, 'w', encoding='utf-8') as f:
    json.dump(d, f, ensure_ascii=False, indent=2)

print(f"Added: {added} / total confirmed_upsets: {len(cu)}")
print(f"rule_improvement_candidates count: {len(ric)}")
