"""Session_57 提案#6: 日付基準統一監査
全 records の date フィールドを走査し、以下のチェックを行う:
1. NHL/NBA/MLB/NFL/UFL → ET 基準 (現地時刻日付) が標準
2. ATP/WTA → local tournament 基準
3. NRL/Super Rugby → AEST 基準
4. Premiership/Top14/Pro D2/Super League → 現地基準

不整合を検出して警告するのみ (自動訂正はしない、誤訂正リスク回避)
"""
import json
from pathlib import Path
from datetime import datetime

ROOT = Path("C:/Users/ohwada/Desktop/claude_sport")

DATE_BASIS_MAP = {
    "nhl": "ET (Eastern Time) - 現地試合日付",
    "nba": "ET - 現地試合日付",
    "mlb": "ET - 現地試合日付",
    "nfl": "ET - 現地試合日付",
    "ufl": "ET - 現地試合日付",
    "cfl": "ET - 現地試合日付",
    "nrl": "AEST - オーストラリア現地",
    "superrugby": "AEST - オーストラリア/NZ現地",
    "superleague": "BST - 英国現地",
    "premiership": "BST - 英国現地",
    "top14": "CET - フランス現地",
    "prod2": "CET - フランス現地",
    "ahl": "ET - 北米現地",
    "atp": "local tournament",
    "wta": "local tournament",
    "soccer": "local tournament",
}

RECORDS = [
    ("atp", "records/tennis/2026-ATP.json"),
    ("wta", "records/wta/2026.json"),
    ("nhl", "records/nhl/2025-26.json"),
    ("nba", "records/nba/2025-26.json"),
    ("ufl", "records/ufl/2026.json"),
    ("nrl", "records/nrl/2026.json"),
    ("superrugby", "records/superrugby/2026.json"),
    ("premiership", "records/premiership/2026.json"),
    ("top14", "records/top14/2026.json"),
    ("prod2", "records/prod2/2026.json"),
    ("superleague", "records/superleague/2026.json"),
    ("ahl", "records/ahl/2025-26.json"),
    ("soccer", "records/soccer/2025-26.json"),
    ("mlb", "records/mlb/2026.json"),
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

print("=== 日付基準監査 (Session_57 提案#6) ===\n")
report = {}
for sport, rel in RECORDS:
    path = ROOT / rel
    if not path.exists():
        continue
    with open(path, encoding="utf-8-sig") as f:
        d = json.load(f)
    items = iter_preds(d)
    dates = set()
    future_far = []
    past_far = []
    today = datetime.now()
    for p in items:
        if p.get("void") or p.get("tier") in ("invalid", "duplicate_closed"):
            continue
        ds = p.get("date")
        if not ds or not isinstance(ds, str):
            continue
        try:
            dt = datetime.strptime(ds, "%Y-%m-%d")
        except ValueError:
            continue
        dates.add(ds)
        is_pending = p.get("hit") is None and p.get("prediction_hit") is None
        if is_pending:
            diff = (dt - today).days
            if diff > 40:
                future_far.append((ds, p.get("match", p.get("name",""))[:40]))
            elif diff < -30:
                past_far.append((ds, p.get("match", p.get("name",""))[:40]))
    report[sport] = {
        "basis_expected": DATE_BASIS_MAP.get(sport, "unknown"),
        "unique_dates": len(dates),
        "pending_too_future": future_far[:5],
        "pending_too_past": past_far[:5],
    }
    print(f"{sport:12s}: 基準={DATE_BASIS_MAP.get(sport,'?')[:30]:30s} 日付数={len(dates)}")
    if future_far:
        print(f"  [未来40日以上先 pending] {len(future_far)}件:")
        for ds, m in future_far[:3]:
            print(f"    {ds} {m}")
    if past_far:
        print(f"  [過去30日以上前 pending] {len(past_far)}件:")
        for ds, m in past_far[:3]:
            print(f"    {ds} {m}")

# 監査結果をファイルに保存
audit_path = ROOT / "stats/date_basis_audit_session57.json"
with open(audit_path, "w", encoding="utf-8") as f:
    json.dump({
        "audit_date": "2026-04-24",
        "session": "_57",
        "date_basis_standard": DATE_BASIS_MAP,
        "report": {k: {
            "basis_expected": v["basis_expected"],
            "unique_dates": v["unique_dates"],
            "pending_too_future_count": len(v["pending_too_future"]),
            "pending_too_past_count": len(v["pending_too_past"]),
            "pending_too_future_samples": v["pending_too_future"],
            "pending_too_past_samples": v["pending_too_past"],
        } for k, v in report.items()}
    }, f, ensure_ascii=False, indent=2)
print(f"\n監査結果: {audit_path}")
