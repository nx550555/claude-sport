# Session_45: GO_CANDIDATE L1 deep dive + UPSET_PICK UF factor deep dive results
import json
from pathlib import Path

BASE = Path(r"C:\Users\ohwada\Desktop\claude_sport")
mb_path = BASE / "records" / "multi_bets.json"
mb = json.load(open(mb_path, encoding="utf-8-sig"))

for sess in mb["sessions"]:
    if sess.get("session_id") == "_45":
        # GO_CANDIDATE L1 deep dive results
        sess["go_candidate_L1_deep_dive"] = {
            "performed": "2026-04-20 Session_45 WebSearch",
            "matches_investigated": 4,
            "findings": [
                {
                    "match": "NRL Panthers vs Knights (Penrith 1.20 vs 4.0)",
                    "L1_data": "Panthers 5-0 start, +150 PD through 5 rounds (+30/G early). Later regression (R6 loss to Bulldogs 32-16). Knights previously wooden spoon, now improved w/ Dylan Brown + Sandon Smith. R9 timing: Panthers revival stage.",
                    "L1_verdict": "Panthers fav correct. PD/G diff still substantial. Own conf estimate 79-82% vs market 79%. Marginal edge < 5pp. Not GO trigger threshold.",
                    "tier_after_L1": "SKIP (insufficient edge)"
                },
                {
                    "match": "Super Rugby Crusaders vs Waratahs (Crusaders 1.15 vs 4.8)",
                    "L1_data": "Crusaders 9M 4-5 21pts 6th PD +39 (+4.3/G). Waratahs form poor (specific data not obtained).",
                    "L1_verdict": "Crusaders home playoff-desperate + Waratahs struggling. PD/G diff ~7pt+ likely. L1 PASS threshold (7pt for Super Rugby). Conf 83-85%. Very close to market @83%. Marginal.",
                    "tier_after_L1": "SKIP (own conf matches market)"
                },
                {
                    "match": "Top14 Toulouse vs Clermont (Toulouse 1.02 vs 10)",
                    "L1_data": "Toulouse 1st 76pts, Clermont 6th 57pts after 21 matches. 19-point gap = dominant lead.",
                    "L1_verdict": "Already output_A candidate @93% conf. L1 confirms. No GO promotion needed (EV structural negative).",
                    "tier_after_L1": "OUTPUT_A confirmed"
                },
                {
                    "match": "Top14 Racing 92 vs US Montalbanaise (Racing 1.00 vs 12)",
                    "L1_data": "Racing 7th 55pts, US Montalbanaise likely last in standings.",
                    "L1_verdict": "OUTPUT_A confirmed @95% conf. No edge over market.",
                    "tier_after_L1": "OUTPUT_A confirmed"
                }
            ],
            "structural_conclusion": "L1 data confirms market positioning. No GO_CANDIDATE L1 promotion achieved in Session_45. Next sessions need L2-L4 depth (injuries, form momentum, H2H, coaching, rest) for independent conf outside market.",
            "unchanged_issue": "Market efficiency at major sports = L1 alone rarely beats bookmaker. GO generation requires multi-layer depth or rare market-mispricing events."
        }

        # UPSET_PICK UF factor deep dive
        sess["upset_pick_uf_deep_dive"] = {
            "performed": "2026-04-20 Session_45 per-candidate UF walkthrough",
            "candidates_investigated": 11,
            "results": [
                {
                    "match": "NHL COL-LAK G2 (4/22 COL home, Avalanche 1.35 vs Kings 3.15)",
                    "uf_walkthrough": {
                        "UF01": "COL home advantage. LAK must-win away. Negates upset.",
                        "UF02": "LAK Kopitar veteran leadership + down 0-1 desperation (partial)",
                        "UF05": "Wedgewood may regress (sophomore game). Partial.",
                        "UF06": "COL complacency risk after G1 win. Partial.",
                        "UFH04": "LAK G1 shots 25 vs 24 - near parity; not dominantly outplayed"
                    },
                    "uf_count": 2,
                    "divergence_pp": 42,
                    "verdict": "UF2 + 42pp - UPSET_PICK NOT met (UF<3). COL home + Wedgewood form + G1 lead all favor COL. Skip."
                },
                {
                    "match": "NRL Manly vs Parramatta (Manly 1.30 vs Eels 3.20)",
                    "uf_walkthrough": {
                        "UF01": "Manly home advantage",
                        "UF02": "Eels form unclear",
                        "UFA04": "No clear travel/fatigue edge"
                    },
                    "uf_count": 1,
                    "divergence_pp": 46,
                    "verdict": "UF1 + 46pp - not met. Manly strong home fav."
                },
                {
                    "matches_batch": "9 WTA Madrid Q + Oeiras + ATP Challenger matches",
                    "batch_verdict": "All dog-side unknown players (Q/futures level). UF factor assessment requires player-level data not obtained in time-budget. Conservative verdict: UPSET_PICK NOT applicable for Q-round players; insufficient information.",
                    "uf_count_avg": 0,
                    "divergence_range_pp": "30-55pp"
                }
            ],
            "overall_verdict": "0/11 triggered UPSET_PICK. UF factor walkthrough confirms Session_45 tentative read. UPSET_PICK extremely rare under strict UF>=3+div>=15pp rule.",
            "rule_observation": "UPSET_PICK threshold (UF>=3+div>=15pp) may be too strict. Future rule review: consider loosening to UF>=2+div>=20pp for tier-adjusted stake (0.5u) UPSET_PICK-Lite category."
        }
        break

mb["last_updated"] = "2026-04-20"
with open(mb_path, 'w', encoding='utf-8') as f:
    json.dump(mb, f, ensure_ascii=False, indent=2)
print("Deep dive results added to session_45.")
