"""Session_57 final: outcome_note "upset" 表記完全除去 + Opelka/Keys 補填"""
import json
from pathlib import Path

ROOT = Path("C:/Users/ohwada/Desktop/claude_sport")

def load_json(p):
    with open(p, encoding="utf-8-sig") as f:
        return json.load(f)

def save_json(p, d):
    with open(p, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)

# ============ ATP ============
atp_path = ROOT / "records/tennis/2026-ATP.json"
atp = load_json(atp_path)

# Opelka MISS rule_linked 補填 (index 115)
atp["predictions"][115]["rule_linked"] = "L4_External_retirement"

save_json(atp_path, atp)
print("ATP Opelka補填完了")

# ============ WTA ============
wta_path = ROOT / "records/wta/2026.json"
wta = load_json(wta_path)

for t in wta["tournaments"]:
    if "Madrid" not in t.get("name", ""):
        continue
    preds = t["predictions"]
    # outcome_note の "upset" 表記を除去/置換
    preds[7]["outcome_note"] = "Q4 watchlist caution_margin - not an underdog win (Samson retired Set 3). Wang fav_HIT via retirement. L4_External: Samson injury."
    preds[11]["outcome_note"] = "Paolini comeback win 3 sets (lost 1st set). Q4 watchlist fav_confirmed (Paolini HIT)."
    preds[13]["outcome_note"] = "Q4 watchlist caution_margin fav_confirmed. Li fav_HIT in 3 sets all-American match. Li best Madrid result tied."
    preds[18]["outcome_note"] = "Osaka 2026 first clay win. Q4 watchlist fav_confirmed, fav Osaka HIT. Osaka advances to R3 vs Kalinina."

    # Keys VOID 明示マーキング
    # index 31 Keys M. vs Zhang Sh.
    for i, p in enumerate(preds):
        if "Keys M." in p.get("match","") and p.get("date") == "2026-04-24":
            p["void"] = True
            p["void_reason"] = "Keys withdrew 30 min before match due to illness"
            p["miss_analysis"] = "N/A - VOID (no match played, bet refunded)"
            p["miss_layer"] = "N/A_VOID"
            p["rule_linked"] = "N/A_VOID"
            break
    break

save_json(wta_path, wta)
print("WTA fixes完了")

# ============ NHL ============
# OTT vs CAR: outcome_note に "sweep brink" は upset 含まず OK
# BOS vs BUF: "UPSET" 含む → 修正
nhl_path = ROOT / "records/nhl/2025-26.json"
nhl = load_json(nhl_path)

# [53] BOS vs BUF G3 MISS: outcome_note から UPSET 除去
nhl["games"][53]["outcome_note"] = "SKIP no-bet / 予測MISS. BUF took 2-1 series lead at TD Garden. Byram/Tuch/Ostlund(EN) scored. Lyon 24 saves in first start. Jeannot sole Bruins goal. BOS G2 rebound success after G1 away loss, then G3 loss continues series volatility."

save_json(nhl_path, nhl)
print("NHL fix完了")
