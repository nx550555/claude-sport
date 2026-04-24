"""Session_57: cumulative.json 更新 (ATP/WTA パート反映)"""
import json
from pathlib import Path

ROOT = Path("C:/Users/ohwada/Desktop/claude_sport")
cpath = ROOT / "stats/cumulative.json"
with open(cpath, encoding="utf-8-sig") as f:
    d = json.load(f)

# ============ ATP ============
# 新規 Paul MISS -1.0u 反映: 11 hits / 14 conf → 11 / 15, ev 1.74 → 0.74
atp = d["tennis_atp"]
atp["confirmed"] = 15
atp["hits"] = 11
atp["hit_rate"] = round(11/15, 3)
atp["ev_total"] = round(0.74, 3)
atp["pending"] = 0  # Mertens は WTA、ATP GO pending なし (4/24 夜試合は ATP だが Paul 除き Musetti/Tsitsipas CAUTION なので GO でなし)
atp.setdefault("tournaments", []).append({
    "id": "2026-Madrid-MS",
    "name": "Mutua Madrid Open 2026 (ATP)",
    "predictions": 1,
    "confirmed": 1,
    "hits": 0,
    "hit_rate": 0.0,
    "ev_total": -1.0,
    "status": "r1_partial",
    "note": "Paul @1.40 GO MISS (Tirante 6-2 6-4 UPSET, clay specialist pattern). Tsitsipas/Musetti CAUTION no-bet both HIT (R1 完了). P012 R019 implement 判断候補 (evidence 3件目)."
})
atp["session_57_note"] = "Session_57 (2026-04-24): Paul Madrid R1 GO MISS -1.0u (Tirante UPSET). Tsitsipas/Musetti CAUTION no-bet 両者本命HIT. 通算 11/15 73.3% +0.74u."

# ============ WTA ============
wta = d["tennis_wta"]
# Keys VOID (棄権) は bet_perf 影響なし / Mertens pending
wta["confirmed"] = 3
wta["hits"] = 2
wta["hit_rate"] = round(2/3, 3)
wta["ev_total"] = round(-0.25, 3)
wta["pending"] = 2  # Keys VOID + Mertens pending
wta.setdefault("tournaments", []).append({
    "id": "2026-Madrid-WTA",
    "name": "Mutua Madrid Open 2026 (WTA)",
    "predictions": 2,
    "confirmed": 0,
    "hits": 0,
    "hit_rate": None,
    "ev_total": 0.0,
    "status": "r1_r2_pending",
    "note": "Keys @1.23 GO → VOID (illness withdrawal 30 min before). Mertens @1.37 GO date 訂正 4/23→4/24 (CE019), R2 vs Eala pending. bet_perf 影響なし."
})
wta["session_57_note"] = "Session_57 (2026-04-24): Keys VOID (棄権), Mertens R2 pending. CE019 (Mertens date) + CE020 (Bencic opponent) 訂正. Q3 output_a 反映: Andreeva/Sabalenka/Swiatek/Bencic 4件HIT (4/23). Q4: Bondar UPSET / Galfi UPSET / Paolini HIT comeback / Osaka HIT / Li HIT / Wang HIT RET."

# ============ NHL ============
nhl = d.get("nhl", {})
nhl["confirmed"] = nhl.get("confirmed", 2)  # GO 変化なし
nhl["hits"] = nhl.get("hits", 2)
nhl["ev_total"] = nhl.get("ev_total", 1.863)
nhl["session_57_note"] = "Session_57 (2026-04-24): G3 5試合反映. BUF UPSET BOS (UF3 road continuation). CAR HIT OTT (3-0 sweep brink). COL HIT LAK (sweep brink). DAL HIT MIN 2OT + PHI HIT PIT (両方 date 4/26→4/23 訂正 CE021/CE022). P018 evidence 3件目候補 (PHI G3 → N019 implement 判断). P027 evidence 強化 (BOS G2 + DAL G2 + DAL G3 = G1 UPSET 後 fav rebound)."

# ============ SL ============
sl = d.get("super_league", d.get("superleague", {}))
sl_key = "super_league"
sl_existing = d.get(sl_key, {})
sl_existing["confirmed"] = sl_existing.get("confirmed", 2) + 2  # York + Leigh HIT predictions (skip tier, bet_perf影響なし)
sl_existing["pred_confirmed_session57"] = 2
sl_existing["pred_hits_session57"] = 2
sl_existing["session_57_note"] = "Session_57 (2026-04-24): R9 York d. Toulouse 38-14 + Leigh d. Huddersfield 30-16 2件 predicted HIT (skip tier). Leeds-Catalans R9 4/24 pending."
d[sl_key] = sl_existing

# ============ overall_combined ============
# 再計算: all sports
sports_keys = ["tennis_atp", "tennis_wta", "nhl", "ufl", "nrl", "superrugby", "nba", "premiership", "top14", "prod2", "ahl", "super_league"]
tot_conf, tot_hits, tot_ev = 0, 0, 0.0
for k in sports_keys:
    s = d.get(k, {})
    c = s.get("confirmed") or 0
    h = s.get("hits") or 0
    e = s.get("ev_total") or 0
    if isinstance(c, int): tot_conf += c
    if isinstance(h, int): tot_hits += h
    if isinstance(e, (int,float)): tot_ev += e

d["overall_combined"] = {
    "confirmed": tot_conf,
    "hits": tot_hits,
    "hit_rate": round(tot_hits/tot_conf, 3) if tot_conf else None,
    "ev_total": round(tot_ev, 3),
    "session": "_57",
    "last_updated": "2026-04-24",
    "note": "auto-calculated Session_57. includes GO-only bet_performance."
}

d["last_updated"] = "2026-04-24"
d["updated"] = "2026-04-24"

with open(cpath, "w", encoding="utf-8") as f:
    json.dump(d, f, ensure_ascii=False, indent=2)
print(f"cumulative updated. Overall: {tot_hits}/{tot_conf} ({100*tot_hits/tot_conf:.1f}%) EV {tot_ev:+.3f}u")
