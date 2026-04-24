"""Session_57 提案#4: Q4_upset_watch 検知精度自動集計
各スポーツ records の quadrant=Q4_upset_watch を走査し、
upset_realized (prediction_hit=False かつ market_favorite 側予測) 率を算出
cumulative.json の by_quadrant.Q4_upset_watch.detection_accuracy に記録
"""
import json
from pathlib import Path

ROOT = Path("C:/Users/ohwada/Desktop/claude_sport")

RECORDS = [
    "records/tennis/2026-ATP.json", "records/wta/2026.json",
    "records/nhl/2025-26.json", "records/nba/2025-26.json",
    "records/ufl/2026.json", "records/nrl/2026.json",
    "records/superrugby/2026.json", "records/premiership/2026.json",
    "records/top14/2026.json", "records/prod2/2026.json",
    "records/superleague/2026.json", "records/ahl/2025-26.json",
]

def iter_preds(d):
    if "games" in d: return d["games"]
    if "predictions" in d: return d["predictions"]
    if "tournaments" in d:
        out = []
        for t in d["tournaments"]:
            out.extend(t.get("predictions", []))
        return out
    return []

q4_total = 0
q4_confirmed = 0  # prediction_hit に値が入っている件数
q4_upset_realized = 0  # prediction_hit=False → UPSET 実現 (Q4 が当たった)
q4_fav_hit = 0  # prediction_hit=True → UPSET 不発 (Q4 警告は外れた)
q4_details = []

for rel in RECORDS:
    path = ROOT / rel
    if not path.exists():
        continue
    with open(path, encoding="utf-8-sig") as f:
        d = json.load(f)
    for p in iter_preds(d):
        if p.get("void") or p.get("tier") in ("invalid", "duplicate_closed"):
            continue
        q = p.get("quadrant", "")
        if q != "Q4_upset_watch":
            continue
        q4_total += 1
        ph = p.get("prediction_hit")
        if ph is not None:
            q4_confirmed += 1
            if ph is False:  # predicted fav 外れ = UPSET 実現
                q4_upset_realized += 1
                q4_details.append(f"UPSET_realized: {rel.split('/')[-1]}:{p.get('match',p.get('name',''))[:40]}")
            else:  # predicted fav HIT = Q4 警告外れ (upset 不発)
                q4_fav_hit += 1

detection_rate = round(q4_upset_realized / q4_confirmed, 3) if q4_confirmed else None

print(f"Q4_upset_watch total: {q4_total}")
print(f"  pending: {q4_total - q4_confirmed}")
print(f"  confirmed: {q4_confirmed}")
print(f"  UPSET realized (Q4 detection HIT): {q4_upset_realized}")
print(f"  Fav HIT (Q4 detection MISS, upset 不発): {q4_fav_hit}")
print(f"  detection_rate: {detection_rate}")
for det in q4_details[:10]:
    print(f"    {det}")

# ====== cumulative.json 更新 ======
cumulative_path = ROOT / "stats/cumulative.json"
with open(cumulative_path, encoding="utf-8-sig") as f:
    cum = json.load(f)

cum.setdefault("by_quadrant", {}).setdefault("Q4_upset_watch", {})
q4c = cum["by_quadrant"]["Q4_upset_watch"]
q4c["total_tagged"] = q4_total
q4c["confirmed"] = q4_confirmed
q4c["pending"] = q4_total - q4_confirmed
q4c["upset_realized_count"] = q4_upset_realized
q4c["fav_hit_count"] = q4_fav_hit
q4c["detection_rate"] = detection_rate
q4c["detection_rate_note"] = f"Q4_upset_watch が事前警告した試合で実際に UPSET が実現した率。{q4_upset_realized}/{q4_confirmed} = {(detection_rate*100 if detection_rate else 0):.1f}%. 43% 程度が初期ベースライン想定 (Session_57 提案#4 instituted)."
q4c["interpretation_rule"] = "Q4 はベット対象外 (no-bet watch)。detection_rate ≥50% で GEN005 閾値再調整の検討材料となる。Session_57 時点ではサンプル不足のため参考値。"
q4c["last_updated"] = "2026-04-24"

cum["last_updated"] = "2026-04-24"
with open(cumulative_path, "w", encoding="utf-8") as f:
    json.dump(cum, f, ensure_ascii=False, indent=2)
print(f"\ncumulative.json.by_quadrant.Q4_upset_watch 更新完了")
