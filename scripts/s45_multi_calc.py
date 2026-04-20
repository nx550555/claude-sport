# Session_45 出力A 18件から全マルチ組み合わせを計算し、総合勝率 top5 + EV最大 top5 を抽出
import json
from pathlib import Path
from itertools import combinations

BASE = Path(r"C:\Users\ohwada\Desktop\claude_sport")
mb = json.load(open(BASE / "records" / "multi_bets.json", encoding="utf-8-sig"))

session_45 = next(s for s in mb["sessions"] if s.get("session_id")=="_45")
cands = session_45["output_a_candidates"]
print(f"出力A候補数: {len(cands)}")

# 各組み合わせのTotal prob / Multi odds / EV を計算
all_combos = []
for size in [2, 3, 4, 5]:
    for combo in combinations(cands, size):
        names = [c["recommendation"] for c in combo]
        matches = [c["match"] for c in combo]
        total_prob = 1.0
        multi_odds = 1.0
        for c in combo:
            total_prob *= c["win_prob"]
            multi_odds *= c["odds"]
        ev = total_prob * multi_odds - 1
        all_combos.append({
            "size": size, "names": names, "matches": matches,
            "total_prob": round(total_prob, 4),
            "multi_odds": round(multi_odds, 4),
            "ev": round(ev, 4)
        })

print(f"総組み合わせ数: {len(all_combos)}")

# 総合勝率 top 5
by_prob = sorted(all_combos, key=lambda x: -x["total_prob"])[:5]
print("\n=== 総合勝率 TOP 5 (高確率) ===")
for i, c in enumerate(by_prob, 1):
    print(f"#{i} size={c['size']} prob={c['total_prob']*100:.1f}% odds={c['multi_odds']:.3f} EV={c['ev']*100:+.1f}%")
    for n in c["names"]:
        print(f"    - {n}")

# EV最大 top 5
by_ev = sorted(all_combos, key=lambda x: -x["ev"])[:5]
print("\n=== EV最大 TOP 5（最もマイナス幅が小さい）===")
for i, c in enumerate(by_ev, 1):
    print(f"#{i} size={c['size']} prob={c['total_prob']*100:.1f}% odds={c['multi_odds']:.3f} EV={c['ev']*100:+.1f}%")
    for n in c["names"]:
        print(f"    - {n}")

# EV+ の有無
ev_plus = [c for c in all_combos if c["ev"] > 0]
print(f"\n=== EV+組み合わせ: {len(ev_plus)}件 ===")
if not ev_plus:
    print("  (なし。market implied×0.95 proxy のため 0.95^n-1 < 0 は数学的必然)")

# multi_bets session_45 に反映
session_45["output_b_top_by_prob"] = [
    {"rank": i+1, "size": c["size"], "matches": c["matches"],
     "names": c["names"], "total_prob": c["total_prob"],
     "multi_odds": c["multi_odds"], "ev": c["ev"],
     "note": "総合勝率順（参考情報・EV負）"}
    for i, c in enumerate(by_prob)
]
session_45["output_b_top_by_ev"] = [
    {"rank": i+1, "size": c["size"], "matches": c["matches"],
     "names": c["names"], "total_prob": c["total_prob"],
     "multi_odds": c["multi_odds"], "ev": c["ev"],
     "note": "EV最大順（参考情報・全てEV負）"}
    for i, c in enumerate(by_ev)
]
session_45["output_b_revision_note"] = "Session_45 初版は『EV+組み合わせなし』のみ記録だったが、ユーザー指摘を受けて『総合勝率順/EV最大順の各TOP5』を参考情報として追記。EV-だが高確率マルチとしての情報価値を担保。CLAUDE.md 仕様の誤解釈（EV+のみ表示→EV-でも上位列挙）を訂正。"

with open(BASE / "records" / "multi_bets.json", "w", encoding="utf-8") as f:
    json.dump(mb, f, ensure_ascii=False, indent=2)
print("\nmulti_bets.json session_45 に output_b_top_by_prob / output_b_top_by_ev 追記完了")
