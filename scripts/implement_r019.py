"""Session_57 提案#5: R019 clay specialist vs hardcourt bias implement
evidence: A011 (Carabelli d. Khachanov) + A024 (Droguet d. Virtanen) + Tirante d. Paul = 3/3 到達
"""
import json
from pathlib import Path

ROOT = Path("C:/Users/ohwada/Desktop/claude_sport")

# ====== 1. rules_tennis.json に R019 追加 ======
rules_path = ROOT / "core/rules_tennis.json"
with open(rules_path, encoding="utf-8-sig") as f:
    rules = json.load(f)

R019 = {
    "id": "R019",
    "name": "Clay specialist vs hardcourt-bias 実効力補正",
    "type": "L1_adjustment",
    "applies_to": "ATP clay surface matches",
    "condition": {
        "surface": "clay",
        "l1_celo_diff": "<120pt",
        "clay_specialist_side": {
            "nationality": ["ARG", "ESP", "FRA (clay-heavy)", "ITA (clay-heavy)", "URU", "PER", "CHI", "BRA"],
            "recent_clay_record": ">=8 wins in last 12 months on clay OR clay-preference in ATP profile"
        },
        "hardcourt_bias_opponent": {
            "nationality": ["USA", "RUS", "POL (non-clay-specialist)", "CZE (non-clay-specialist)", "AUS"],
            "surface_bias": "hardcourt primary (>50% career wins on hard)"
        }
    },
    "adjustment": "+15pt cElo bonus to clay specialist side (実質 confidence +3〜+5%)",
    "rationale": "clay specialist rally endurance + baseline defense on clay dominates over hardcourt-oriented servers/flat-hitters when cElo gap is marginal. 3 件 evidence 到達で implement.",
    "evidence_base": [
        "A011 Carabelli (ARG) d. Khachanov (RUS) Barcelona 2026 R1 (cElo diff 82pt)",
        "A024 Droguet (FRA clay) d. Virtanen (FIN hardcourt bias) Madrid Q R1 2026 3sets",
        "Tirante (ARG clay) d. Paul T. (USA hardcourt) Madrid R1 2026 6-2 6-4 (Session_57 GO MISS -1.0u)"
    ],
    "implemented_date": "2026-04-24",
    "implemented_session": "_57",
    "collision_rules": [
        "R019 と R001 (cElo base threshold) 同時成立時: R019 を L1 補正として適用後に R001 閾値判定",
        "R019 と R017 (home WC momentum) 同時成立時: R017 優先"
    ]
}
rules["rules"].append(R019)
rules["version"] = "v2.3"
rules["updated"] = "2026-04-24"
rules["last_update_note"] = "Session_57 R019 clay specialist vs hardcourt-bias implement (evidence 3/3 reached via A011+A024+Tirante/Paul)"

with open(rules_path, "w", encoding="utf-8") as f:
    json.dump(rules, f, ensure_ascii=False, indent=2)
print("R019 implemented in rules_tennis.json v2.3")

# ====== 2. rule_pipeline.json の P012 を implemented へ ======
pipeline_path = ROOT / "core/rule_pipeline.json"
with open(pipeline_path, encoding="utf-8-sig") as f:
    pipe = json.load(f)

# P012 candidate 更新
for c in pipe["candidates"]:
    if c["candidate_id"] == "P012":
        c["status"] = "implemented"
        c["current_count"] = 3
        c["implemented_date"] = "2026-04-24"
        c["implemented_in"] = "rules_tennis.json v2.3 R019"
        c["evidence"].append({
            "id": "A034_session57",
            "match": "Tirante T.A. d. Paul T. Madrid 2026 R1 6-2 6-4",
            "pattern": "Tirante (ARG clay specialist, ranking ~100) d. Paul T. (USA hardcourt bias, Top20). GO @1.40 MISS -1.0u. clay endurance + ARG specialist power overcame seed gap. P012 3件目 evidence 到達 (A011+A024+今回) → R019 implement.",
            "tag": "atp_clay_specialist_vs_hardcourt_player",
            "sources": [
                "atptour.com/en/news/madrid-2026-results",
                "dimers.com tirante-paul"
            ]
        })
        c["note"] = c.get("note","") + " 【実装完了 2026-04-24】Session_57 Paul MISS で evidence 3/3 到達 → R019 clay specialist vs hardcourt-bias として rules_tennis.json v2.3 に実装"
        break

# implemented_rules に追加
pipe.setdefault("implemented_rules", []).append({
    "candidate_id": "P012",
    "implemented_date": "2026-04-24",
    "target_rule_file": "core/rules_tennis.json",
    "rule_id": "R019",
    "title": "Clay specialist vs hardcourt-bias 実効力補正 (+15pt cElo)",
    "trigger_event": "A011 Carabelli/Khachanov + A024 Droguet/Virtanen + A034 Tirante/Paul (Session_57 GO MISS -1.0u) = 3件 threshold到達",
    "evidence_count": 3,
    "note": "ATP clay L1 cElo差<120pt + 南米/clay-heavy specialist vs hardcourt-bias → clay specialist 側 +15pt 補正 (confidence +3〜+5%). R017 と同時成立時は R017 優先."
})
pipe["last_updated"] = "2026-04-24"
pipe["updated_session"] = "_57"

with open(pipeline_path, "w", encoding="utf-8") as f:
    json.dump(pipe, f, ensure_ascii=False, indent=2)
print("P012 → implemented in rule_pipeline.json")
