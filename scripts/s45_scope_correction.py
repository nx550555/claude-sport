"""
Session_45 認識訂正: Hurricanes試合の screening_log メモを修正
"""
import json
from pathlib import Path

BASE = Path(r"C:\Users\ohwada\Desktop\claude_sport")
sr_path = BASE / "records" / "superrugby" / "2026.json"
d = json.load(open(sr_path, encoding="utf-8-sig"))

# screening_log の最後のエントリ (4/20 Session_45_supplement) を修正
sl = d.get("screening_log", [])
for entry in sl:
    if isinstance(entry, dict) and entry.get("session") == "_45_supplement":
        entry["issue_corrected"] = (
            "初期認識: JSON提供期間外の完了試合が「記録漏れ」と誤認識 → "
            "訂正認識: 提供JSONに含まれない試合はスコープ外。ユーザーの ⓪試合場提供 の役割範囲外。"
        )
        entry["action_corrected"] = (
            "ユーザー明示指摘による例外的記録として残す。games[] に残存。"
            "一般的な運用ルールは変更しない (提供JSON起点を維持)。"
        )
        entry["improvement_withdrawn"] = (
            "撤回: health_check.py v2 への「不在ラウンド WebSearch スキャン」追加提案は撤回。"
            "全世界試合の自動追跡はスコープ爆発・ユーザー役割侵食になるため不採用。"
        )
        entry["lesson"] = (
            "今後ユーザーから「XXは分析した？」と聞かれた際、"
            "まず「提供データに含まれるか」を確認。含まれていなければ「提供データ外のため未分析」と返答し、"
            "追加分析するかユーザーに確認してから進める。"
        )
        break

d["last_updated"] = "2026-04-20"
with open(sr_path, 'w', encoding='utf-8') as f:
    json.dump(d, f, ensure_ascii=False, indent=2)
print("screening_log 認識訂正メモ追記完了")
