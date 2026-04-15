#!/usr/bin/env python3
"""
Session_30: ATP R1結果更新 + VGK@WPG NHL note更新
"""
import json, os

BASE = r"C:\Users\ohwada\Desktop\claude_sport"

# ─────────────────────────────────────────────
# 1. ATP 2026-ATP.json 結果更新
# ─────────────────────────────────────────────
atp_path = os.path.join(BASE, "records", "tennis", "2026-ATP.json")
with open(atp_path, "r", encoding="utf-8-sig") as f:
    atp = json.load(f)

# Confirmed R1 results to update
results_map = {
    "Norrie C. vs Wawrinka S.(WC)": {
        "result": "Norrie C.",
        "score": "6-4 6-7(5) 6-4",
        "note": "Norrie defeated Wawrinka (retirement tour) 6-4 6-7(5) 6-4 in 2h33m. Wawrinka made 59 UEs. SKIP (cElo diff below GO threshold)."
    },
    "Borges N. vs Mannarino A.": {
        "result": "Borges N.",
        "score": "6-3 6-4",
        "note": "Borges beat Mannarino 6-3 6-4. Borges 77pts vs 61. SKIP."
    },
    "Nava E. vs Shelton B.(2)": {
        "result": "Shelton B.(2)",
        "score": "7-6(4) 3-6 6-3",
        "note": "Shelton beat Nava 7-6(4) 3-6 6-3 with 14 aces. Munich R1. SKIP."
    },
    "Blockx A. vs Hanfmann Y.": {
        "result": "Blockx A.",
        "score": "7-6(2) 6-2",
        "note": "Blockx beat Hanfmann 7-6(2) 6-2 on his Munich debut. SKIP."
    },
    "Molcan A. vs Bublik A.(3)": {
        "result": "Molcan A.",
        "score": "6-4 6-2",
        "note": "Molcan UPSET Bublik(3) 6-4 6-2. CAUTION rec=null (Bublik conf 65.5% -> SKIP). Molcan upset was flagged as risk."
    }
}

updated = 0
for p in atp["predictions"]:
    match_key = p.get("match", "")
    if match_key in results_map and p.get("result") is None:
        r = results_map[match_key]
        p["result"] = r["result"]
        p["score"] = r["score"]
        # Only update hit for CAUTION with rec
        if p.get("tier") == "caution" and p.get("rec") is not None:
            # rec is Bublik (null in this case), so no hit tracking
            pass
        if "note" not in p or p.get("note") is None:
            p["note"] = r["note"]
        else:
            p["note"] = p["note"] + " | " + r["note"]
        updated += 1
        print(f"  Updated: {match_key} -> {r['result']} {r['score']}")

print(f"[1] ATP: {updated} matches updated")

with open(atp_path, "w", encoding="utf-8") as f:
    json.dump(atp, f, ensure_ascii=False, indent=4)

# ─────────────────────────────────────────────
# 2. NHL VGK@WPG note確認更新
# ─────────────────────────────────────────────
nhl_path = os.path.join(BASE, "records", "nhl", "2025-26.json")
with open(nhl_path, "r", encoding="utf-8-sig") as f:
    nhl = json.load(f)

for g in nhl["games"]:
    if g.get("match") == "Vegas Golden Knights @ Winnipeg Jets":
        if g.get("score") == "6-2" and g.get("result") == "Vegas Golden Knights":
            # Already has correct result; just update the note to confirm
            g["note"] = (
                "retroactive prediction. predicted_winner=null (xGF%未確認のため予測未記録)。"
                "結果: VGK 6-2 WPG確認済。"
                "Stone 1G/Eichel 1G3A/Barbashev 1G1A/Andersson 1G1A/Smith 1G/Dorofeyev 1G。"
                "VGK Pacific Division title争い。"
            )
            print("[2] NHL VGK@WPG note更新済み")
            break

with open(nhl_path, "w", encoding="utf-8-sig") as f:
    json.dump(nhl, f, ensure_ascii=False, indent=2)

print("\n=== ATP+NHL更新完了 ===")
