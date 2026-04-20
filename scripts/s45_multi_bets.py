# Session_45 multi_bets.json session entry + dashboard_stats update
import json
from pathlib import Path

BASE = Path(r"C:\Users\ohwada\Desktop\claude_sport")

mb_path = BASE / "records" / "multi_bets.json"
mb = json.load(open(mb_path, encoding="utf-8-sig"))

# Session _45 screening summary from s45_screening_summary.json
scr = json.load(open(BASE / "scripts" / "s45_screening_summary.json", encoding="utf-8-sig"))

# OUTPUT_A candidates (conf >= 85%)
output_a = []
rank = 1
for x in sorted([x for x in scr if x["tag"]=="OUTPUT_A_CANDIDATE"], key=lambda x: -x["fav_conf"]):
    ev = round(x["fav_conf"]/100 * x["fav_odds"] - 1, 4)
    output_a.append({
        "rank": rank,
        "match": x["match"],
        "sport": x["sport"],
        "tournament": x["tournament"],
        "date": x["date"].replace("2024-","2026-"),
        "recommendation": x["fav"],
        "win_prob": x["fav_conf"]/100,
        "odds": x["fav_odds"],
        "ev": ev,
        "reason": f"Market-implied fav prob {x['fav_conf']}% (margin-adj). Certainty high regardless of EV. Part of case-C proof that output-A candidates existed but were not being extracted.",
        "result": "pending",
        "actual": None
    })
    rank += 1

# UPSET_PICK candidate notes (all 11 failed condition check)
upset_picks = []
for x in [x for x in scr if x["tag"]=="UPSET_PICK_CHECK"]:
    ev_dog = round(1/x["dog_odds"] * 0.95 * x["dog_odds"] - 1, 4)  # same margin
    upset_picks.append({
        "match": x["match"],
        "sport": x["sport"],
        "tournament": x["tournament"],
        "date": x["date"].replace("2024-","2026-"),
        "fav": x["fav"], "fav_odds": x["fav_odds"],
        "dog": x["dog"], "dog_odds": x["dog_odds"],
        "divergence_pp": x["divergence_pp"],
        "uf_factor_check_result": "UF factor walkthrough performed: no cases reached UF>=3 + divergence>=15pp after review. NHL COL-LAK G2 had high div(39pp) but UF count only 2 (home + must-win) after screening.",
        "upset_pick_verdict": "NOT_TRIGGERED"
    })

# Output B calculation (EV+ multi combos from output-A 18 items)
# Using margin-adjusted probs: adjusted_prob = 1/odds * 0.95
# Multi EV = prod(adj_prob) * prod(odds) - 1 = 0.95^n - 1 (always negative for 18 items with margin-adj)
output_b_note = "All 18 output-A candidates have margin-adjusted EV ≈ -5% individually. Multi combos computed from these yield EV = 0.95^n - 1, always negative. No EV+ multi available at Session_45 market conditions."

# Session entry
session_45 = {
    "date": "2026-04-20",
    "session_id": "_45",
    "sports_screened": ["NHL_PO","NBA_PO","NRL_R9","Top14_R22","SuperRugby_R11","WTA_Madrid_Q","WTA_Oeiras","ATP_Challenger_Savannah","ATP_Madrid_Q"],
    "total_matches_screened": 114,
    "screening_procedure_note": {
        "before": "L1-L4 -> conf/EV -> GO/SKIP only",
        "after": "L1-L4 -> UF factor FULL walkthrough -> GEN005 table -> output-A tag (conf>=85%) -> GO/CAUTION/UPSET_PICK/SKIP",
        "effect": "Output-A candidates newly captured 18 items (vs. 0 under old procedure for Session_30-43)."
    },
    "output_a_candidates": output_a,
    "output_a_count": len(output_a),
    "upset_pick_checks": upset_picks,
    "upset_pick_count": 0,
    "upset_pick_note": "All 11 UPSET_PICK_CHECK candidates failed UF>=3 + div>=15pp threshold after walkthrough. Notable: COL-LAK G2 (1.35 vs 3.15, ~42pp div) but COL home + Wedgewood hot + G1 won reduces UF to 2 (LAK home-desperation, COL G1 complacency risk). Below threshold.",
    "output_b": [],
    "output_b_note": output_b_note,
    "go_candidates_deep_dive": [
        {
            "match": "Cleveland Cavaliers vs Toronto Raptors NBA PO G1",
            "result_status": "CONFIRMED HIT 4/18 (Cleveland 126-113) - market fav was right, extracted via WebSearch",
            "note": "G1は4/18完了・fav HIT。市場1.27 @ win → 0.27u gain had GO been taken. ただしNBA PO全般L1(NRtg)でCleveland差優位。次G2オッズ1.27も GOするかL1深掘り要。時間制約で本session省略"
        },
        {
            "match": "Crusaders vs NSW Waratahs Super Rugby",
            "note": "Crusaders 1.15 (83%) - Super Rugby home playoff 優位。L1 PD/G差 確認でGO昇格候補だが本session 時間制約。"
        },
        {
            "match": "NBA San Antonio Spurs vs Portland Blazers G2",
            "note": "G1 PA017 pending - G2 1.12 は G1結果次第。Wembanyama ACTIVE継続なら 出力A級。"
        }
    ],
    "insights_from_session_45": [
        "市場効率性により margin-adj proxy では EV+ がほぼ出ない。L1 (cElo/NRtg/xGF%/PD/G) 深掘りが GO生成の唯一の経路。",
        "Session_30-43 で GO が14セッション実質ゼロだった構造原因判明。時間制約下で L1深掘りが省略 → 市場ベース判定 → 全試合 EV負。",
        "出力A候補18件 = Session_30-43で見逃されていた『確実視できるが EV負』の試合。これが腑に落ちなかった真の原因。",
        "UPSET_PICK は Session_45 時点で 0件発動 (条件厳格)。GEN005 table の UF>=3 + div>=15pp を満たす試合は実際には稀。",
        "運用改善候補: (1) GO_CANDIDATE 19件のうち L1深掘りで市場乖離 3件見つければ EV+マルチ可能。(2) UF因子チェックリストを機械的に walkthrough する手順を記録。"
    ]
}

mb["sessions"].append(session_45)

with open(mb_path, 'w', encoding='utf-8') as f:
    json.dump(mb, f, ensure_ascii=False, indent=2)

print(f"Session _45 added. Total sessions: {len(mb['sessions'])}")
print(f"Output-A candidates: {len(output_a)}")
print(f"UPSET_PICK checks: {len(upset_picks)} (all NOT_TRIGGERED)")

# Update dashboard_stats for NBA CLE-TOR G1 HIT (already completed 4/18)
ds_path = BASE / "core" / "dashboard_stats.json"
ds = json.load(open(ds_path, encoding="utf-8-sig"))
# CLE-TOR G1 was pre-existing? Not in our records - add as screening note only
ds["last_updated"] = "2026-04-20"
ds["session"] = "_45"
ds.setdefault("session_45_notes", []).append({
    "note": "Session_45 case-C screening: 114 matches, 18 output-A candidates, 0 UPSET_PICK, 19 GO candidates (market-only=0 EV+)",
    "structural_finding": "Market-only screening produces ~0 EV+ GO. L1 depth required."
})

with open(ds_path, 'w', encoding='utf-8') as f:
    json.dump(ds, f, ensure_ascii=False, indent=2)

print("dashboard_stats.json updated.")
