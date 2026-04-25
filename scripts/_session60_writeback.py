"""Session_60 records write-back: soccer + mlb + nrl 新規スクリーニング結果を records に反映"""
import json
from pathlib import Path
from datetime import datetime

BASE = Path(__file__).parent.parent
TODAY = "2026-04-25"

# date 訂正: 提供データの 2024-04-25 → 2026-04-25, 2024-04-26 → 2026-04-26 など
def fix_date(d):
    if d and d.startswith("2024-"): return "2026-" + d[5:]
    if d and d.startswith("2025-"): return "2026-" + d[5:]
    return d

def get_quadrant(tier, conf, ev):
    """4象限分類"""
    if tier in ("provisional_go","caution_waiting_sp"):
        return "Q1_go"
    if tier == "caution_margin":
        if conf and conf >= 85: return "Q3_output_a"
        if conf and conf >= 80: return "Q3_mid"
        return "Q1_go"  # caution_margin treated as bet-track watch
    return "skip"

def make_entry(r, sport_tier, l1_metric_name):
    """records 用 entry 生成"""
    tier = r["tier"]
    conf = r.get("conf")
    ev = r.get("ev")
    quadrant = get_quadrant(tier, conf, ev)

    # Determine market_favorite
    o1, o2 = r["home_odds"], r["away_odds"]
    market_fav = "home" if (o1 and o2 and o1 < o2) else ("away" if (o1 and o2) else None)

    return {
        "match": r["match_en"],
        "date": fix_date(r["date"]),
        "league": r["league"],
        "tier": tier,
        "tier_class": sport_tier,
        "quadrant": quadrant,
        "home_odds": r["home_odds"],
        "draw_odds": r.get("draw_odds"),
        "away_odds": r["away_odds"],
        "rec_odds": (r["home_odds"] if r["predicted_winner"] and r["predicted_winner"] in r["match_en"].split(" vs ")[0] else r["away_odds"]),
        "predicted_winner": r["predicted_winner"],
        "prediction_confidence": conf,
        "prediction_basis": f"L1 ({l1_metric_name}): {r['note']}",
        "ev": ev,
        "market_favorite": market_fav,
        "screening_session": "_60",
        "screening_date": TODAY,
        "step45_required": tier == "provisional_go",
        "step45_status": "PENDING",
        "result": None,
        "score": None,
        "prediction_hit": None,
        "actual_ev": None,
        "notify_sent": False
    }

def append_to_records(file_path, entries, sport_label):
    """既存 records に append + screening_log 追加"""
    if file_path.exists():
        d = json.load(open(file_path, encoding="utf-8-sig"))
    else:
        d = {"sport": sport_label, "version": "1.0", "season": "2026", "games": [], "predictions": [], "screening_log": []}

    # games or predictions
    games_key = "games" if "games" in d else ("predictions" if "predictions" in d else "games")
    d.setdefault(games_key, [])
    d.setdefault("screening_log", [])

    # dedup: 同 match + date のものは skip
    existing = {(g.get("match"), g.get("date")) for g in d[games_key]}
    appended = 0
    for e in entries:
        if (e["match"], e["date"]) in existing: continue
        d[games_key].append(e)
        appended += 1

    # screening_log
    d["screening_log"].append({
        "session": "_60",
        "date": TODAY,
        "added": appended,
        "skipped_existing": len(entries) - appended,
        "summary": f"{sport_label}: {appended} entries added (Session_60 一括スクリーニング)"
    })

    d["last_updated"] = TODAY
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
    return appended

# === Soccer ===
soc = json.load(open(BASE / "stats/_screening_soccer_2026-04-25.json", encoding="utf-8-sig"))
soc_entries = [make_entry(r, "advanced", "Elo+xGD/G") for r in soc]
n = append_to_records(BASE / "records/soccer/2025-26.json", soc_entries, "soccer")
print(f"[Soccer] {n}/{len(soc_entries)} appended")

# === MLB === (新規ファイル)
mlb = json.load(open(BASE / "stats/_screening_mlb_2026-04-25.json", encoding="utf-8-sig"))
mlb_entries = [make_entry(r, "advanced", "wRC+/FIP (proxy)") for r in mlb]
mlb_path = BASE / "records/mlb/2026.json"
mlb_path.parent.mkdir(exist_ok=True)
n = append_to_records(mlb_path, mlb_entries, "mlb")
print(f"[MLB] {n}/{len(mlb_entries)} appended")

# === NRL ===
nrl = json.load(open(BASE / "stats/_screening_nrl_2026-04-25.json", encoding="utf-8-sig"))
nrl_entries = [make_entry(r, "basic", "PD/G") for r in nrl]
n = append_to_records(BASE / "records/nrl/2026.json", nrl_entries, "nrl")
print(f"[NRL]  {n}/{len(nrl_entries)} appended")

# === multi_bets.json: Session_60 entry 追加 ===
mb_path = BASE / "records/multi_bets.json"
mb = json.load(open(mb_path, encoding="utf-8-sig"))

# Session_60 GO/CAUTION/Q3 候補
q1_go = []
caution_margin = []
q3_output_a = []
q3_mid = []

for entry_list, sport in [(soc_entries, "soccer"), (mlb_entries, "mlb"), (nrl_entries, "nrl")]:
    for e in entry_list:
        if e["tier"] == "provisional_go":
            q1_go.append({
                "match": e["match"], "sport": sport, "rec": e["predicted_winner"],
                "rec_odds": e["rec_odds"], "conf": e["prediction_confidence"], "ev": e["ev"],
                "date": e["date"], "step45": "PENDING"
            })
        elif e["tier"] == "caution_margin":
            caution_margin.append({
                "match": e["match"], "sport": sport, "rec": e["predicted_winner"],
                "conf": e["prediction_confidence"], "ev": e["ev"], "date": e["date"]
            })
        elif e["tier"] == "caution_waiting_sp":
            caution_margin.append({
                "match": e["match"], "sport": sport, "rec": e["predicted_winner"],
                "conf": e["prediction_confidence"], "ev": e["ev"], "date": e["date"],
                "note": "MLB先発SP未確定→GO禁止 (M002)"
            })
        if e["quadrant"] == "Q3_output_a":
            q3_output_a.append({"match": e["match"], "sport": sport, "conf": e["prediction_confidence"]})
        elif e["quadrant"] == "Q3_mid":
            q3_mid.append({"match": e["match"], "sport": sport, "conf": e["prediction_confidence"]})

session_entry = {
    "session_id": "_60",
    "date": TODAY,
    "scope": "soccer 5大リーグ + MLB + NRL R9 (2026-04-25.json 新規分一括スクリーニング)",
    "totals": {
        "screened_total": len(soc_entries) + len(mlb_entries) + len(nrl_entries),
        "provisional_go": len(q1_go),
        "caution_margin": len(caution_margin),
        "skip": sum(1 for e in soc_entries+mlb_entries+nrl_entries if e["tier"] in ("skip","skip_data_missing"))
    },
    "q1_go_provisional": q1_go,
    "caution_margin": caution_margin,
    "output_a": {"candidates": q3_output_a, "count": len(q3_output_a)},
    "output_a_additions": [],
    "q3_mid": q3_mid,
    "note": "STEP 4.5 (スタメン確認) 未実施。Soccer/MLB/NRL 全 provisional_go は STEP 4.5 後に GO 昇格 or caution_waiting 格下げ判定。MLB 全件は M002 (先発SP未確定→GO禁止) で waiting。"
}
mb["sessions"].append(session_entry)
mb["last_session"] = "_60"
mb["last_updated"] = TODAY
with open(mb_path, "w", encoding="utf-8") as f:
    json.dump(mb, f, ensure_ascii=False, indent=2)
print(f"\n[multi_bets] Session_60 entry 追加 (provisional_go {len(q1_go)} / caution_margin {len(caution_margin)})")

print("\n=== Session_60 スクリーニング サマリー ===")
print(f"  Provisional GO ({len(q1_go)}):")
for g in q1_go: print(f"    {g['sport']}: {g['match']} | {g['rec']} @{g['rec_odds']} conf {g['conf']}% EV {g['ev']:+.1%}")
print(f"\n  CAUTION_MARGIN ({len(caution_margin)}):")
for c in caution_margin: print(f"    {c['sport']}: {c['match']} | conf {c['conf']}% EV {c['ev']:+.1%}{(' ['+c.get('note','')+']') if c.get('note') else ''}")
print(f"\n  Q3_output_a candidates: {len(q3_output_a)} | Q3_mid: {len(q3_mid)}")
