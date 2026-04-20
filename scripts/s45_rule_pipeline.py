# Session_45: rule_pipeline.json に P017 候補追加 + records screening_log 統一追記
import json
from pathlib import Path

BASE = Path(r"C:\Users\ohwada\Desktop\claude_sport")

rp_path = BASE / "core" / "rule_pipeline.json"
rp = json.load(open(rp_path, encoding="utf-8-sig"))

# P017 candidate: veteran Q-round motivation
p017 = {
    "candidate_id": "P017",
    "status": "watching",
    "target_rule_file": "core/rules_tennis.json",
    "proposed_rule_id": "R022",
    "title": "ベテラン Top100 選手の Masters Qualifying R1 モチベ危機補正",
    "description": "Top100のATPベテラン選手がMasters 1000 Qualifying R1で低ランク・無名選手と対戦する場合、『本戦出場権のみの副次大会』というステージでの相対的モチベ低下により、-5%〜-7%補正が妥当な可能性。Bonzi(Top100 vet) vs Darwin (unknown) で先に発生 (A025)。",
    "trigger_threshold": 3,
    "current_count": 1,
    "evidence": [
        {
            "id": "A025",
            "match": "Darwin B. d. Bonzi B. Madrid Open Qualifying R1",
            "pattern": "Bonzi Top100 vet が fav @1.61 で負ける。低ランク無名選手 Darwin 勝利 @2.22。market divergence 12pp。",
            "tag": "atp_veteran_qualifying_motivation_dip"
        }
    ],
    "tag_matches": ["atp_veteran_qualifying_motivation_dip","wta_veteran_qualifying_motivation_dip"],
    "note": "3件揃ったら R022 として『Top100 vet の Masters Q R1 での-5%補正』を実装。ATP Madrid Q・Rome Q・Cincinnati Q 等の各大会で継続観察。"
}

# Add new procedure note to instructions
rp.setdefault("instructions_for_claude", [])
new_instruction = "(Session_45 2026-04-20 追加) GEN005 UF因子チェックは、L1-L4確信度算出直後の**必須手順**。UF因子を機械的に全件 walkthrough (UF01〜UFA06) し、該当数と市場乖離を記録。UPSET_PICK条件未達でも UF因子数>=2 であれば CAUTION 格下げを検討。"
if new_instruction not in rp["instructions_for_claude"]:
    rp["instructions_for_claude"].append(new_instruction)

# Insert P017 before implemented_rules
candidates = rp.setdefault("candidates", [])
existing_ids = {c.get("candidate_id") for c in candidates}
if "P017" not in existing_ids:
    candidates.append(p017)
    print("P017 added.")
else:
    print("P017 already exists, skipping.")

rp["last_updated"] = "2026-04-20"
rp["updated_session"] = "_45"

with open(rp_path, 'w', encoding='utf-8') as f:
    json.dump(rp, f, ensure_ascii=False, indent=2)

# === Each records: screening_log entry ===
screening_entry = {
    "date": "2026-04-20",
    "session": "_45",
    "scope": "Session_45 case-C full screening with new procedure (L1-L4 + UF factor walkthrough + output-A tag)",
    "note": "2026-04-20.json + 114 upcoming matches screened. See records/multi_bets.json session_45 for output-A (18) and UPSET_PICK checks (11, none triggered)."
}

# Load screening summary
scr = json.load(open(BASE / "scripts" / "s45_screening_summary.json", encoding="utf-8-sig"))

# Sports map
sport_files = {
    "nba": BASE / "records" / "nba" / "2025-26.json",
    "nhl": BASE / "records" / "nhl" / "2025-26.json",
    "nrl": BASE / "records" / "nrl" / "2026.json",
    "top14": BASE / "records" / "top14" / "2026.json",
    "superrugby": BASE / "records" / "superrugby" / "2026.json",
    "wta": BASE / "records" / "wta" / "2026.json"
}

# Aggregate per-sport list of upcoming
def match_to_sport(x):
    tn = x["tournament"]
    sp = x["sport"]
    if "NBA" in tn: return "nba"
    if "NHL" in tn or "ホッケー" in tn or "ice_hockey" == sp: return "nhl"
    if "NRL" in tn: return "nrl"
    if "トップ14" in tn or "top14" in tn.lower(): return "top14"
    if "スーパーラグビー" in tn: return "superrugby"
    if "WTA" in tn: return "wta"
    return None

updated_files = 0
for sport_key, fp in sport_files.items():
    if not fp.exists():
        continue
    d = json.load(open(fp, encoding="utf-8-sig"))
    matches_for_sport = [x for x in scr if match_to_sport(x) == sport_key]
    if not matches_for_sport:
        continue
    sport_entry = dict(screening_entry)
    sport_entry["matches_screened_this_sport"] = len(matches_for_sport)
    sport_entry["output_a_candidates_this_sport"] = sum(1 for x in matches_for_sport if x["tag"]=="OUTPUT_A_CANDIDATE")
    sport_entry["go_candidates_this_sport"] = sum(1 for x in matches_for_sport if x["tag"]=="GO_CANDIDATE")
    sport_entry["upset_pick_checks_this_sport"] = sum(1 for x in matches_for_sport if x["tag"]=="UPSET_PICK_CHECK")
    sport_entry["screening_note"] = "All GO_CANDIDATE entries are market-only classification; L1 depth required to confirm EV+ -> GO. Output-A candidates captured for first time via new procedure."

    sl = d.setdefault("screening_log", [])
    sl.append(sport_entry)
    with open(fp, 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
    updated_files += 1
    print(f"  {sport_key}: +1 screening_log entry ({len(matches_for_sport)} matches)")

print(f"\nScreening log added to {updated_files} files.")
print(f"rule_pipeline.json: last_updated={rp['last_updated']}")
