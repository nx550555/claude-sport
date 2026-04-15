#!/usr/bin/env python3
"""multi_bets.json Louisville Kings 説明テキスト修正"""
import json, os

BASE = r"C:\Users\ohwada\Desktop\claude_sport"
mb_path = os.path.join(BASE, "records", "multi_bets.json")

with open(mb_path, "r", encoding="utf-8-sig") as f:
    mb = json.load(f)

for s in mb.get("sessions", []):
    for item in s.get("output_a", []):
        if "Louisville Kings" in item.get("recommendation", "") and "Houston" in item.get("match", ""):
            # Fix wrong records description
            if "3-0" in item.get("reason", "") and "0-3" in item.get("reason", ""):
                item["reason"] = (
                    "Houston QB Tagovailoa 171yd 7-45 blowout loss W3 (unstable QB situation)。"
                    "Louisville QB Bean W3 352yd 3TD (Houston戦で好パフォーマンス)。"
                    "PD/G: Louisville -4.7/G vs Houston -18.3/G (Houston W3 45-7大敗でPD悪化)。"
                    "L1 diff 13.6 > threshold 4。conf 82% > Week4 threshold 80%。EV+35.3%。"
                )
                print("Fixed Louisville reason text")

with open(mb_path, "w", encoding="utf-8") as f:
    json.dump(mb, f, ensure_ascii=False, indent=2)
print("multi_bets.json updated")
