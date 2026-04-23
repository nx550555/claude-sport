"""Session_49 結果反映スクリプト
Galfi GO HIT + Q3 output_a 4件 (Sonmez HIT / BOS G2 MISS / SAS G2 MISS / OKC G2 pending)
+ NHL G2 7/8試合 + NBA G2 7/8試合
"""
import json
from pathlib import Path

ROOT = Path("C:/Users/ohwada/Desktop/claude_sport")

def load(p):
    with open(p, encoding="utf-8-sig") as f:
        return json.load(f)

def save(p, d):
    with open(p, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)

# ===== WTA =====
wp = ROOT / "records/wta/2026.json"
wta = load(wp)
md = wta["tournaments"][2]  # Madrid Open
# [0] Galfi vs Vidmanova GO HIT
g = md["predictions"][0]
g["result"] = "Galfi d. Vidmanova 7-5 6-3"
g["score"] = "7-5 6-3"
g["prediction_hit"] = True
g["hit"] = True
g["actual_ev"] = 0.54  # @1.54 - 1
g["verification_sources"] = ["wtatennis.com Galfi vs Vidmanova RS023", "WTA Madrid Q draw PDF", "puntodebreak.com"]
g["closed_session"] = "_49"
# [1] Sonmez vs Martinez Cires Q3 output_a HIT
s = md["predictions"][1]
s["result"] = "Sonmez d. Martinez Cires 7-5 6-2"
s["score"] = "7-5 6-2"
s["prediction_hit"] = True
s["verification_sources"] = ["puntodebreak.com Sonmez ends Carlota Martinez dream", "anews.com.tr", "skysports.com highlights"]
s["closed_session"] = "_49"

# Update WTA summary
ws = wta["summary"]
ws["total"] = ws.get("total", 3) + 1  # +1 Galfi GO
ws["hit"] = ws.get("hit", 1) + 1
ws["hit_rate"] = round(ws["hit"] / ws["total"], 3)
ws["ev_total"] = round(ws.get("ev_total", -1.04) + 0.54, 3)
ws["note"] = (ws.get("note", "") +
              " | Session_49 update: Galfi Madrid Q Final GO HIT +0.54u (d. Vidmanova 7-5 6-3). "
              "Sonmez Madrid R1 Q3 output_a HIT (d. Martinez Cires 7-5 6-2). "
              f"通算 {ws['hit']}/{ws['total']} {round(ws['hit_rate']*100,1)}% {ws['ev_total']:+.3f}u")
save(wp, wta)
print(f"WTA updated: Galfi HIT +0.54u, Sonmez prediction HIT. Total bet={ws['hit']}/{ws['total']} EV={ws['ev_total']:+.3f}u")

# ===== NHL =====
np_ = ROOT / "records/nhl/2025-26.json"
nhl = load(np_)

# NHL G2 results map
nhl_g2_results = {
    # idx: (result_str, score, predicted_winner_team_name_check, true_winner_team_name)
    38: ("Colorado Avalanche 2-1 Los Angeles Kings (OT)", "2-1 OT", "COL", "Colorado Avalanche"),
    45: ("Tampa Bay Lightning 3-2 Montreal Canadiens (OT)", "3-2 OT", None, "Tampa Bay Lightning"),
    46: ("Boston Bruins 4-2 Buffalo Sabres", "4-2", None, "Boston Bruins"),
    47: ("Utah Mammoth 3-2 Vegas Golden Knights", "3-2", None, "Utah Mammoth"),
    48: ("Colorado Avalanche 2-1 Los Angeles Kings (OT)", "2-1 OT", "Colorado Avalanche", "Colorado Avalanche"),
    49: ("Philadelphia Flyers 3-0 Pittsburgh Penguins", "3-0", None, "Philadelphia Flyers"),
    50: ("Dallas Stars 4-2 Minnesota Wild", "4-2", None, "Dallas Stars"),
    52: ("Carolina Hurricanes 3-2 Ottawa Senators (2OT)", "3-2 2OT", None, "Carolina Hurricanes"),
}

prediction_hits = 0
prediction_total = 0
for idx, (res, sc, expected_pred, true_winner) in nhl_g2_results.items():
    g = nhl["games"][idx]
    g["result"] = res
    g["score"] = sc
    pred = g.get("predicted_winner", "")
    # Determine if prediction hit
    if pred:
        # match team name fuzzy
        pred_l = pred.lower()
        tw_l = true_winner.lower()
        # short codes COL/LAK/PHI etc.
        team_codes = {"COL": "colorado", "LAK": "los angeles kings", "TBL": "tampa bay",
                      "MTL": "montreal", "BOS": "boston", "BUF": "buffalo", "UTA": "utah",
                      "VGK": "vegas", "PHI": "philadelphia", "PIT": "pittsburgh",
                      "DAL": "dallas", "MIN": "minnesota", "CAR": "carolina", "OTT": "ottawa",
                      "EDM": "edmonton", "ANA": "anaheim"}
        pred_full = team_codes.get(pred, pred_l)
        is_hit = pred_full.lower() in tw_l or pred_l in tw_l
        g["prediction_hit"] = is_hit
        prediction_total += 1
        if is_hit:
            prediction_hits += 1
    g["closed_session"] = "_49"
    g["verification_sources"] = ["NHL.com game recap", "ESPN game recap"]
    if "tier" in g and g["tier"] == "caution":
        # CAUTION no-bet, hit stays None for bet, but prediction_hit set above
        pass

# EDM-ANA G2 [51] left pending (in progress at session time)
nhl["games"][51]["note"] = (nhl["games"][51].get("note", "") +
                            " | Session_49: 4/22 試合進行中 (1stP 1-1)、結果未確定。次セッション確認。")

# Update NHL summary
ns = nhl["summary"]
ns["prediction_total"] = ns.get("prediction_total", 17) + prediction_total
ns["prediction_hit"] = ns.get("prediction_hit", 7) + prediction_hits
ns["prediction_pending"] = max(0, ns.get("prediction_pending", 7) - prediction_total)
ns["prediction_hit_rate"] = round(ns["prediction_hit"] / ns["prediction_total"], 3)
ns["note"] = (ns.get("note", "") +
              f" | Session_49: G2 {prediction_total}/8 closed ({prediction_hits} prediction HIT). "
              "EDM-ANA G2 pending. all CAUTION/SKIP no-bet (P&L 0).")
ns["last_updated"] = "2026-04-23 Session_49"
save(np_, nhl)
print(f"NHL updated: G2 {prediction_total}/8 closed, prediction {prediction_hits}/{prediction_total} HIT")
print(f"  cum prediction: {ns['prediction_hit']}/{ns['prediction_total']} = {ns['prediction_hit_rate']*100:.1f}%")

# ===== NBA =====
bp = ROOT / "records/nba/2025-26.json"
nba = load(bp)

# NBA G2 results map
nba_g2_results = {
    25: ("Philadelphia 76ers 111-97 Boston Celtics", "111-97", "Boston Celtics", "Philadelphia 76ers"),
    26: ("Portland Trail Blazers 106-103 San Antonio Spurs", "106-103", "San Antonio Spurs", "Portland Trail Blazers"),
    27: ("Los Angeles Lakers 101-94 Houston Rockets", "101-94", "Houston Rockets", "Los Angeles Lakers"),
    28: ("Detroit Pistons 98-83 Orlando Magic", "98-83", "Detroit Pistons", "Detroit Pistons"),
    # 30-32: registered as G1 but actually G2 (label mismatch from Session_48 import)
    30: ("Atlanta Hawks d. New York Knicks (G2)", "ATL W", "New York Knicks", "Atlanta Hawks"),
    31: ("Cleveland Cavaliers 115-105 Toronto Raptors", "115-105", "Cleveland Cavaliers", "Cleveland Cavaliers"),
    32: ("Minnesota Timberwolves 119-114 Denver Nuggets", "119-114", "Denver Nuggets", "Minnesota Timberwolves"),
}

nba_pred_hits = 0
nba_pred_total = 0
for idx, (res, sc, pred_team, true_winner) in nba_g2_results.items():
    g = nba["games"][idx]
    g["result"] = res
    g["score"] = sc
    pred = g.get("predicted_winner", "") or ""
    is_hit = pred.lower() in true_winner.lower() if pred else None
    g["prediction_hit"] = is_hit
    nba_pred_total += 1
    if is_hit:
        nba_pred_hits += 1
    g["closed_session"] = "_49"
    g["verification_sources"] = ["NBA.com game recap", "ESPN game recap"]
    # For idx 30-32, fix round label G1 → G2
    if idx in (30, 31, 32):
        g["round"] = "Playoffs R1 G2"
        if "G1" in g.get("match", ""):
            g["match"] = g["match"].replace("G1", "G2")
        g["round_label_corrected"] = "Session_49: import時に G1 ラベル誤付与, 実際は G2"

# OKC-PHX G2 [29] still pending
nba["games"][29]["note"] = (nba["games"][29].get("note", "") +
                            " | Session_49: 4/22 21:30 ET 進行中、結果未確定。次セッション確認。")

# Update NBA summary
bs = nba["summary"]
# Add prediction tracking if not present
bs["prediction_total"] = bs.get("prediction_total", 0) + nba_pred_total
bs["prediction_hit"] = bs.get("prediction_hit", 0) + nba_pred_hits
bs["prediction_pending"] = max(0, bs.get("prediction_pending", 1) - nba_pred_total)
if bs["prediction_total"] > 0:
    bs["prediction_hit_rate"] = round(bs["prediction_hit"] / bs["prediction_total"], 3)
bs["note"] = (bs.get("note", "") +
              f" | Session_49: G2 {nba_pred_total}/8 closed ({nba_pred_hits} prediction HIT). "
              "OKC-PHX G2 pending. Q3 output_a: BOS G2 MISS / SAS G2 MISS / Sonmez WTA HIT. "
              "[30][31][32] round label G1→G2 訂正 (Session_48 import error).")
bs["last_updated"] = "2026-04-23 Session_49"
save(bp, nba)
print(f"NBA updated: G2 {nba_pred_total}/8 closed, prediction {nba_pred_hits}/{nba_pred_total} HIT")

print("\n=== Session_49 update DONE ===")
