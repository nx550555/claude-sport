"""Session_57: VOID schema 導入
- records 全体を走査し、outcome_note に "VOID"/"withdrew"/"retired before match" パターンがあれば void=true を追加
- regenerate_dashboard_stats / cumulative 集計スクリプトは void=true をスキップする仕様に変更
- 既存 records の void 状態監査
"""
import json
from pathlib import Path

ROOT = Path("C:/Users/ohwada/Desktop/claude_sport")

RECORDS = [
    "records/tennis/2026-ATP.json",
    "records/wta/2026.json",
    "records/nhl/2025-26.json",
    "records/ufl/2026.json",
    "records/nrl/2026.json",
    "records/nba/2025-26.json",
    "records/superrugby/2026.json",
    "records/premiership/2026.json",
    "records/top14/2026.json",
    "records/prod2/2026.json",
    "records/superleague/2026.json",
    "records/ahl/2025-26.json",
    "records/soccer/2025-26.json",
    "records/mlb/2026.json",
]

def iter_preds_ref(d):
    if "games" in d:
        return d["games"]
    if "predictions" in d:
        return d["predictions"]
    if "tournaments" in d:
        out = []
        for t in d["tournaments"]:
            out.extend(t.get("predictions", []))
        return out
    return []

void_added = 0
for rel in RECORDS:
    path = ROOT / rel
    if not path.exists():
        continue
    with open(path, encoding="utf-8-sig") as f:
        d = json.load(f)
    items = iter_preds_ref(d)
    modified = False
    for p in items:
        on = (p.get("outcome_note", "") or "").lower()
        score = (p.get("score", "") or "").lower()
        result = (p.get("result", "") or "").lower()
        is_void = (
            ("void" in on and "(keys" in on or "withdrew" in on or "withdrawal" in on or "w/o" in on or "w/o" in score or "walkover" in on)
            or score.strip() == "w/o"
        )
        if is_void and not p.get("void"):
            p["void"] = True
            p["void_reason"] = p.get("void_reason") or "withdrawal/walkover before match start - bet refunded"
            void_added += 1
            modified = True
    if modified:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(d, f, ensure_ascii=False, indent=2)

print(f"VOID flags applied to {void_added} records")

# 既存 void 状態の監査
print("\n=== 現在 void=true の試合一覧 ===")
total_void = 0
for rel in RECORDS:
    path = ROOT / rel
    if not path.exists():
        continue
    with open(path, encoding="utf-8-sig") as f:
        d = json.load(f)
    for p in iter_preds_ref(d):
        if p.get("void"):
            total_void += 1
            print(f"  {rel.split('/')[-1]}: {p.get('match',p.get('name',''))[:60]} | date={p.get('date','?')} | reason={p.get('void_reason','N/A')[:50]}")
print(f"Total void: {total_void}")
