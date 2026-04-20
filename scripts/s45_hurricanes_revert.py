"""
Session_45: Hurricanes試合の誤追加を revert
理由: ユーザーが指摘していたのは Warrington Wolves(SuperLeague) であり、
Hurricanes(Super Rugby) は当初から対象外だった。提供JSONに含まれない試合を
追加したのは過剰対応。
"""
import json
from pathlib import Path

BASE = Path(r"C:\Users\ohwada\Desktop\claude_sport")
sr_path = BASE / "records" / "superrugby" / "2026.json"
d = json.load(open(sr_path, encoding="utf-8-sig"))

# games から Chiefs vs Hurricanes エントリ削除
games = d.get("games", [])
new_games = [g for g in games if not (
    g.get("match","") == "Chiefs vs Hurricanes" and g.get("date","") == "2026-04-18"
)]
removed = len(games) - len(new_games)
d["games"] = new_games

# screening_log の _45_supplement / _45_supplement_corrected エントリ削除
sl = d.get("screening_log", [])
new_sl = [s for s in sl if not (
    isinstance(s, dict) and str(s.get("session","")).startswith("_45_supplement")
)]
sl_removed = len(sl) - len(new_sl)
d["screening_log"] = new_sl

# 正しい screening_log エントリを追加（Session_45 の誤追加を記録として残す）
new_sl.append({
    "date": "2026-04-20",
    "session": "_45_scope_correction",
    "note": (
        "Session_45末尾でユーザー発言『ウェリントンの負け分析』を Hurricanes (Super Rugby) と誤解。"
        "提供JSON対象外の Chiefs vs Hurricanes (4/18 R10) を自動追加してしまった → "
        "ユーザー再指摘『調べる必要もなかった試合では？』で誤認識発覚 → revert (本エントリ)。"
        "真の指摘対象は Warrington Wolves (Super League R8) であり Session_42 で既に完全分析済 (A020/P016)。"
    ),
    "lesson_hardened": (
        "ユーザーから『XXは分析した？』と聞かれた際、"
        "(1) チーム名の正確な特定 (略称・別名をユーザーに確認) "
        "(2) 提供JSONにあるか確認 "
        "(3) なければ追加分析するかユーザーに確認 — の順で対応する。"
        "勝手に自動追加しない。"
    )
})
d["screening_log"] = new_sl
d["last_updated"] = "2026-04-20"

with open(sr_path, 'w', encoding='utf-8') as f:
    json.dump(d, f, ensure_ascii=False, indent=2)
print(f"games 削除: {removed}件 / screening_log 旧補遺削除: {sl_removed}件")
print(f"games: {len(new_games)} / screening_log: {len(new_sl)}")
