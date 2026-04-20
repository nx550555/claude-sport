"""
Session_45 4象限 quadrant field 一括適用
既存 records に quadrant field を付与 + stats/cumulative.json に by_quadrant 集計セクション追加
"""
import json
from pathlib import Path

BASE = Path(r"C:\Users\ohwada\Desktop\claude_sport")

def classify_quadrant(conf, ev, uf_count, div_pp, dog_odds):
    """4象限分類ロジック。conf=%(0-100), ev=fraction(-0.05=-5%), uf_count=int, div_pp=int, dog_odds=float"""
    # Q2_upset_pick: UF>=3 + div>=15pp
    if uf_count >= 3 and div_pp >= 15:
        return "Q2_upset_pick"
    # Q1_go: conf>=75% + EV>+5%
    if conf >= 75 and ev is not None and ev > 0.05:
        return "Q1_go"
    # Q3_output_a: conf>=85% (EV問わず)
    if conf >= 85:
        return "Q3_output_a"
    # Q4_upset_watch: dog>=3.0 + UF>=2
    if dog_odds and dog_odds >= 3.0 and uf_count >= 2:
        return "Q4_upset_watch"
    return "skip"

# ---- (A) records/tennis/2026-ATP.json: Madrid Q R1 24件 ----
atp_path = BASE / "records" / "tennis" / "2026-ATP.json"
atp = json.load(open(atp_path, encoding="utf-8-sig"))
updated = 0
for p in atp.get("predictions", []):
    if p.get("tournament") == "Mutua Madrid Open Qualifying" and "quadrant" not in p:
        conf = p.get("prediction_confidence", 0)
        l1 = p.get("l1_data","")
        # Q3判定：conf>=85
        # skip判定：conf<85
        # UF は市場ベースのため 0
        fav_odds_str = l1.split(" / ")[0] if " / " in l1 else ""
        try:
            dog_odds = float(l1.split("@")[-1].strip()) if "@" in l1 else None
        except:
            dog_odds = None
        q = classify_quadrant(conf, None, 0, 0, dog_odds)
        p["quadrant"] = q
        updated += 1
print(f"ATP Madrid Q R1: {updated} entries got quadrant field")

with open(atp_path, 'w', encoding='utf-8') as f:
    json.dump(atp, f, ensure_ascii=False, indent=2)

# ---- (B) records/nba/2025-26.json: Session_45 G1 results ----
nba_path = BASE / "records" / "nba" / "2025-26.json"
nba = json.load(open(nba_path, encoding="utf-8-sig"))
updated_nba = 0
# Session_45 新規追加分 (G1 8件)
for g in nba.get("games", []):
    if g.get("source","").startswith("Session_45") and "quadrant" not in g:
        tier_cat = g.get("tier","")
        conf = g.get("prediction_confidence", 0)
        fav_odds = g.get("fav_odds", 0)
        dog_odds = g.get("dog_odds", 0)
        # EV計算: 本命 conf × odds - 1
        ev = (conf/100 * fav_odds - 1) if fav_odds else None
        if "output_a" in tier_cat:
            q = "Q3_output_a"
        elif tier_cat == "go_active_PA017":
            q = "Q1_go"  # 従来のGO推奨
        elif "UPSET" in tier_cat:
            q = "Q4_upset_watch"  # 結果的にupsetだったが事前は market分類
        else:
            q = classify_quadrant(conf, ev, 0, 0, dog_odds)
        g["quadrant"] = q
        updated_nba += 1
print(f"NBA Session_45 G1: {updated_nba} entries got quadrant field")
with open(nba_path, 'w', encoding='utf-8') as f:
    json.dump(nba, f, ensure_ascii=False, indent=2)

# ---- (C) records/nhl/2025-26.json: Session_45 G1 results ----
nhl_path = BASE / "records" / "nhl" / "2025-26.json"
nhl = json.load(open(nhl_path, encoding="utf-8-sig"))
updated_nhl = 0
for g in nhl.get("games", []):
    if g.get("source","").startswith("Session_45") and "quadrant" not in g:
        tier_cat = g.get("tier","")
        conf = g.get("prediction_confidence", 0)
        fav_odds = g.get("fav_odds", 0)
        dog_odds = g.get("dog_odds", 0)
        ev = (conf/100 * fav_odds - 1) if fav_odds else None
        if "UPSET" in tier_cat:
            q = "Q4_upset_watch"
        else:
            q = classify_quadrant(conf, ev, 0, 0, dog_odds)
        g["quadrant"] = q
        updated_nhl += 1
print(f"NHL Session_45 G1: {updated_nhl} entries got quadrant field")
with open(nhl_path, 'w', encoding='utf-8') as f:
    json.dump(nhl, f, ensure_ascii=False, indent=2)

# ---- (D) stats/cumulative.json: by_quadrant セクション新設 ----
cum_path = BASE / "stats" / "cumulative.json"
cum = json.load(open(cum_path, encoding="utf-8-sig"))

by_quadrant = {
    "_description": "Session_45 (2026-04-20) 新設。4象限別の予測精度・ベット成績を追跡",
    "_formula": "hit_rate = hits / confirmed / ev_total = sum of actual_ev for GO-tier only",
    "_frame": "Q1_go=GO推奨(conf>=75 AND EV>+5) / Q2_upset_pick=UPSET_PICK(UF>=3 AND div>=15pp) / Q3_output_a=高確率予想(conf>=85 EV問わず) / Q4_upset_watch=アップセット観察(dog>=3.0 AND UF>=2)",
    "Q1_go": {
        "total": 29,
        "confirmed": 28,
        "hit": 20,
        "hit_rate": 0.714,
        "ev_total": 1.7,
        "note": "既存GO推奨累計。Session_30-43のGO+Session_44遡及4件+過去全件"
    },
    "Q2_upset_pick": {
        "total": 0,
        "confirmed": 0,
        "hit": 0,
        "hit_rate": None,
        "ev_total": 0,
        "note": "Phase2移行(2026-04-18)以降発動0件。閾値UF>=3+div>=15ppは実運用で極めて稀"
    },
    "Q3_output_a": {
        "total": 18,
        "confirmed": 3,
        "hit": 3,
        "hit_rate": 1.0,
        "ev_total": None,
        "note": "Session_45で正式運用開始。NBA G1 3/3 HIT (BOS blowout / SAS Wemby record / OKC 119-84). 残15件は4/21-27決着待ち。EVは計算しない（EV負でも確実性抽出が目的）"
    },
    "Q4_upset_watch": {
        "total": 11,
        "confirmed": 0,
        "hit": 0,
        "hit_rate": None,
        "ev_total": None,
        "note": "Session_45 UPSET_PICK_CHECK 候補11件。全件UF walkthrough後 Q2昇格なし。観察対象として継続追跡"
    },
    "skip": {
        "total": "N/A (既存 tier=skip records数)",
        "note": "L1差なし・UF因子なし・確実性低。予測精度追跡は prediction_hit ベース"
    },
    "last_updated": "2026-04-20 Session_45"
}
cum["by_quadrant"] = by_quadrant
cum["last_updated"] = "2026-04-20"
cum.setdefault("schema_versions", []).append({
    "version": "v3.1",
    "date": "2026-04-20",
    "change": "4象限フレームワーク正式運用開始。全予測に quadrant field 必須。cumulative.by_quadrant セクション新設"
})
with open(cum_path, 'w', encoding='utf-8') as f:
    json.dump(cum, f, ensure_ascii=False, indent=2)
print("stats/cumulative.json: by_quadrant セクション新設完了")

print("\n=== Summary ===")
print(f"  ATP Madrid Q: +{updated} quadrant")
print(f"  NBA Session_45 G1: +{updated_nba} quadrant")
print(f"  NHL Session_45 G1: +{updated_nhl} quadrant")
print(f"  cumulative.json: by_quadrant 新設")
