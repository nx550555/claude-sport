"""Session_49 cumulative.json + dashboard_stats.json 同期"""
import json
from pathlib import Path

ROOT = Path("C:/Users/ohwada/Desktop/claude_sport")

def load(p):
    with open(p, encoding="utf-8-sig") as f:
        return json.load(f)
def save(p, d):
    with open(p, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)

# ===== cumulative.json =====
cp = ROOT / "stats/cumulative.json"
c = load(cp)

# WTA: Galfi GO HIT +0.54u
wta = c["tennis_wta"]
wta["total_predictions"] = 4   # was 3
wta["confirmed"] = 4
wta["hits"] = 2                # was 1
wta["hit_rate"] = round(2/4, 3)
wta["ev_total"] = round(-1.04 + 0.54, 3)  # -0.50
wta["pending"] = 0
wta["status"] = "Galfi Madrid Q Final HIT (Session_49)"
wta["note"] = (wta["note"] +
               " | Session_49 update: Galfi D. d. Vidmanova D. 7-5 6-3 GO HIT +0.54u (Madrid Q Final). "
               "Sonmez Q3 output_a HIT (Madrid R1 d. Martinez Cires 7-5 6-2). 通算 2/4 50% -0.50u")
# Append Madrid tournament
wta_tourns = wta.setdefault("tournaments", [])
wta_tourns.append({
    "id": "2026-Madrid-Q",
    "name": "Mutua Madrid Open 2026 Qualifying",
    "predictions": 1,
    "confirmed": 1,
    "hits": 1,
    "hit_rate": 1.0,
    "ev_total": 0.54,
    "status": "q_final_complete",
    "note": "Galfi D. d. Vidmanova D. 7-5 6-3 GO @1.54 HIT +0.54u (Session_49)."
})

# NHL: bet影響なし、prediction精度のみ更新
nhl = c["nhl"]
nhl["note"] = (nhl.get("note", "") +
               " | Session_49: G2 7/8 closed (EDM-ANA pending). prediction G2: BOS HIT (BOS 4-2 BUF), TBL HIT (TBL 3-2 MTL OT), CAR HIT (CAR 3-2 OTT 2OT), PHI HIT (PHI 3-0 PIT), COL HIT (COL 2-1 LAK OT, both [38][48]). "
               "MISS: predicted_winner 不一致 [45][46][47][50][52]では prediction_winner 設定/不設定混在. 全 SKIP/CAUTION no-bet (P&L 0).")
nhl["status"] = "PO R1 G2 7/8 closed (EDM-ANA pending). 4 series 2-0, 4 series 1-1."

# NBA: bet影響なし、prediction精度のみ
nba = c["nba"]
nba["note"] = (nba.get("note", "") +
               " | Session_49: G2 7/8 closed (OKC-PHX pending). Q3 output_a: BOS G2 MISS (PHI 111-97), SAS G2 MISS (POR 106-103), Sonmez WTA HIT, OKC G2 pending. "
               "BOS-PHI tied, SAS-POR tied, ATL-NYK tied, MIN-DEN tied. LAL-HOU 2-0, CLE-TOR 2-0, ORL-DET tied (Pistons G2 HIT 98-83).")
nba["status"] = "PO R1 G2 7/8 closed (OKC-PHX pending)."

# ===== by_tier (advanced) =====
adv = c["by_tier"]["advanced"]
adv["total_predictions"] = 22  # +1 Galfi GO
adv["confirmed"] = 22
adv["hits"] = 16  # +1 Galfi
adv["pending"] = 0
adv["ev_total"] = round(2.763 + 0.54, 3)  # 3.303
adv["hit_rate"] = round(16/22, 3)
adv["note"] = adv["note"] + " | Session_49: Galfi WTA Madrid Q HIT +0.54u 反映. 16/22 72.7% +3.303u."

# overall_combined
oc = c["overall_combined"]
oc["total_predictions"] = 30
oc["confirmed"] = 30
oc["hits"] = 21
oc["pending"] = 0
oc["ev_total"] = round(1.733 + 0.54, 3)  # 2.273
oc["hit_rate"] = round(21/30, 4)
oc["note"] = oc["note"] + " | Session_49: Galfi WTA Madrid Q HIT +0.54u. 21/30 70.0% +2.273u (Adv 16/22 72.7% +3.303u / Basic 5/8 62.5% -1.03u)."

# Q1_go quadrant
q1 = c["by_quadrant"]["Q1_go"]
q1["total"] = 30
q1["confirmed"] = 30
q1["hit"] = 21
q1["hit_rate"] = round(21/30, 3)
q1["ev_total"] = round(1.7 + 0.54, 3)  # 2.24
q1["note"] = q1["note"] + " | Session_49: Galfi GO HIT +0.54u 反映"

# Q3_output_a quadrant
q3 = c["by_quadrant"]["Q3_output_a"]
# Sonmez HIT, BOS G2 MISS, SAS G2 MISS, OKC G2 still pending → confirmed 7→10, hit 7→8
q3["confirmed"] = 10
q3["hit"] = 8
q3["hit_rate"] = round(8/10, 3)  # 0.8
q3["note"] = q3["note"] + " | Session_49: Sonmez HIT, BOS G2 MISS (PHI 111-97), SAS G2 MISS (POR 106-103). OKC G2 pending. 8/10 80.0%."

c["last_updated"] = "2026-04-23"
c.setdefault("schema_versions", []).append({
    "version": "v3.1.1",
    "date": "2026-04-23",
    "change": "Session_49: Galfi GO HIT +0.54u + NHL G2 7/8 + NBA G2 7/8 + Q3 output_a 3/4 closed反映"
})

save(cp, c)
print(f"cumulative.json updated. Overall: {oc['hits']}/{oc['confirmed']} {oc['hit_rate']*100:.1f}% {oc['ev_total']:+.3f}u")

# ===== dashboard_stats.json =====
dp = ROOT / "core/dashboard_stats.json"
d = load(dp)

# WTA
d["sports"]["wta"] = {
    "go_count": 4,
    "confirmed_count": 4,
    "hit_count": 2,
    "hit_rate": round(2/4, 3),
    "pnl": round(-1.04 + 0.54, 3),  # -0.50
    "pending_count": 0
}

# Overview
ov = d["overview"]
ov["total_go"] = 31  # was 30
ov["total_confirmed"] = 30  # was 29
ov["total_hits"] = 22  # was 21
ov["hit_rate"] = round(22/30, 3)
ov["total_pnl"] = round(1.9 + 0.54, 3)  # 2.44
ov["total_pending"] = 0  # Galfi closed
ov["pending_breakdown"] = "なし (Galfi closed Session_49)"

# by_tier advanced
adv_d = d["by_tier"]["advanced"]
adv_d["go_count"] = 22
adv_d["confirmed_count"] = 22
adv_d["hit_count"] = 17  # 16 -> 17? Wait. 16+1=17. But WTA had 1, +1 Galfi = 2 hits (already counted in adv_d hits). Let me recount:
# advanced sports: ATP(11), WTA(2 after Galfi), NHL(2), NBA(2) = 17 hits. confirmed: 14+4+2+2 = 22
adv_d["hit_count"] = 17
adv_d["pnl"] = round(1.74 + (-0.50) + 1.863 + 0.38, 3)  # ATP+WTA+NHL+NBA = 3.483
adv_d["pending_count"] = 0
adv_d["hit_rate"] = round(17/22, 3)
adv_d["note"] = adv_d["note"] + " | Session_49: Galfi HIT 反映, 17/22 77.3% +3.483u."

d["last_updated"] = "2026-04-23"
d["session"] = "_49"
d.setdefault("session_49_notes", {
    "result_reflection": "Galfi WTA Madrid Q Final HIT +0.54u + NHL G2 7/8 + NBA G2 7/8 closed. Q3 output_a 3/4: Sonmez HIT, BOS G2 MISS, SAS G2 MISS, OKC G2 pending. EDM-ANA NHL G2 + OKC-PHX NBA G2 pending.",
    "key_metrics": f"GO bet: {ov['total_hits']}/{ov['total_confirmed']} {ov['hit_rate']*100:.1f}% {ov['total_pnl']:+.3f}u (+0.54u from Session_48)"
})

save(dp, d)
print(f"dashboard_stats.json updated. Overview: {ov['total_hits']}/{ov['total_confirmed']} {ov['hit_rate']*100:.1f}% {ov['total_pnl']:+.3f}u")

print("\n=== Sync DONE ===")
