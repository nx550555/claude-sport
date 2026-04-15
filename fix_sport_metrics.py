#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SCアンカーブロック内の sport-metrics を完全に再構築する。
sync_sport_cards.py の regex ミスで古いデータが残留している問題を修正。
sport-metrics の正しい閉じ </div> から sport-card の閉じ </div> までを正確に置換する。
"""
import json, re
from pathlib import Path

BASE = Path(__file__).parent
STATS_PATH = BASE / "core" / "dashboard_stats.json"
DASH_PATH  = BASE / "dashboard.html"

with open(STATS_PATH, encoding="utf-8") as f:
    stats = json.load(f)

with open(DASH_PATH, encoding="utf-8") as f:
    content = f.read()

SPORT_CARDS = [
    {"key": "ATP",  "data_key": "atp",         "label1": "GO\u56de\u6570"},
    {"key": "WTA",  "data_key": "wta",         "label1": "GB\u63a8\u5968"},
    {"key": "NHL",  "data_key": "nhl",         "label1": "GO\u56de\u6570"},
    {"key": "UFL",  "data_key": "ufl",         "label1": "GO\u56de\u6570"},
    {"key": "NRL",  "data_key": "nrl",         "label1": "GO\u56de\u6570"},
    {"key": "SRP",  "data_key": "superrugby",  "label1": "GO\u56de\u6570"},
    {"key": "NBA",  "data_key": "nba",         "label1": "GO\u56de\u6570"},
    {"key": "SL",   "data_key": "superleague", "label1": "GO\u56de\u6570"},
]

def fmt_rate(rate):
    if rate is None: return "\u2014"
    return f"{rate*100:.1f}%"

def fmt_ev(ev):
    if ev is None: return "\u2014"
    return f"+{ev:.3f}" if ev >= 0 else f"{ev:.3f}"

def color_for(label, val):
    if label in ("\u7684\u4e2d", "GO\u56de\u6570", "\u7d50\u679c\u6e08", "GB\u63a8\u5968"):
        return ""
    if label == "\u6b63\u7b54\u7387":
        if val is None or str(val) in ("\u2014", "", "None"):
            return ' style="color:#8b949e;"'
        try:
            pct = float(str(val).replace("%",""))
        except ValueError:
            return ' style="color:#8b949e;"'
        if pct >= 75:   return ' style="color:#3fb950;"'
        elif pct >= 60: return ' style="color:#e3b341;"'
        else:           return ' style="color:#f85149;"'
    if label == "\u7d2f\u7a4d\u0045\u0056":
        if val is None or str(val) in ("\u2014", "", "None"):
            return ' style="color:#8b949e;"'
        try:
            n = float(str(val).replace("+",""))
        except ValueError:
            return ' style="color:#8b949e;"'
        if n > 0:   return ' style="color:#3fb950;"'
        elif n < 0: return ' style="color:#f85149;"'
        else:       return ' style="color:#8b949e;"'
    if label == "\u5f85\u6a5f\u4e2d":
        n = int(val)
        return ' style="color:#d29922;"' if n > 0 else ' style="color:#8b949e;"'
    return ""

def sm_row(label, val):
    c = color_for(label, val)
    return f'          <div class="sm"><div class="sm-label">{label}</div><div class="sm-val"{c}>{val}</div></div>'

def build_metrics(data, label1):
    rows = [
        sm_row(label1, data.get("go_count", 0)),
        sm_row("\u7d50\u679c\u6e08", data.get("confirmed_count", 0)),
        sm_row("\u7684\u4e2d", data.get("hit_count", 0)),
        sm_row("\u6b63\u7b54\u7387", fmt_rate(data.get("hit_rate"))),
        sm_row("\u7d2f\u7a4d\u0045\u0056", fmt_ev(data.get("ev_total", 0))),
        sm_row("\u5f85\u6a5f\u4e2d", str(data.get("pending_count", 0))),
    ]
    return "\n".join(rows)


def find_div_end(text, start_after_open):
    """
    <div> が開かれた直後の位置 start_after_open から始めて、
    対応する </div> の終わり位置を返す。
    """
    depth = 1
    pos = start_after_open
    while depth > 0 and pos < len(text):
        next_open  = text.find('<div', pos)
        next_close = text.find('</div>', pos)
        if next_close < 0:
            break
        if next_open >= 0 and next_open < next_close:
            depth += 1
            pos = next_open + 4
        else:
            depth -= 1
            pos = next_close + 6
    return pos  # 対応する </div> の次の文字位置


sport_data = stats.get("sports", {})

for card in SPORT_CARDS:
    key    = card["key"]
    dk     = card["data_key"]
    label1 = card["label1"]

    if dk not in sport_data:
        print(f"  [SKIP] data not found: {dk}")
        continue

    anchor_s = f"<!-- SC:{key} -->"
    anchor_e = f"<!-- /SC:{key} -->"

    if anchor_s not in content:
        print(f"  [SKIP] anchor not found: {key}")
        continue

    idx_s = content.index(anchor_s)
    idx_e = content.index(anchor_e, idx_s) + len(anchor_e)
    block = content[idx_s:idx_e]

    SM_TAG = '<div class="sport-metrics">'
    sm_start = block.find(SM_TAG)
    if sm_start < 0:
        print(f"  [WARN] sport-metrics not found: {key}")
        continue

    # sport-metrics の正しい閉じ </div> の位置
    sm_content_start = sm_start + len(SM_TAG)
    sm_end = find_div_end(block, sm_content_start)

    # sm_end 以降で sport-card の閉じ </div> の直前にある不要なデータを確認
    after_sm = block[sm_end:]
    # 不要なデータ: </div> と <!-- /SC:KEY --> の間にあるもの
    # sport-card の閉じ </div> を探す（最初の </div> の直前まで削除）
    # ここでは after_sm が "</div>\n      <!-- /SC:KEY -->" で始まるべきところ
    # 不要なデータがある場合は最後の </div> を sport-card の閉じとして使う

    # 正しい構造: sm_end → </div> (sport-card閉じ) → <!-- /SC:KEY -->
    # 壊れた構造: sm_end → 残留データ... → </div> (sport-card閉じ) → <!-- /SC:KEY -->
    # なので、<!-- /SC:KEY --> の直前の </div> から後を保持する

    anchor_e_in_block = anchor_e
    anchor_pos_in_after = after_sm.find(anchor_e_in_block)
    if anchor_pos_in_after < 0:
        print(f"  [WARN] end anchor not found in after_sm: {key}")
        continue

    # anchor の直前の </div> を探す
    before_anchor = after_sm[:anchor_pos_in_after]
    last_close = before_anchor.rfind('</div>')
    if last_close < 0:
        print(f"  [WARN] no </div> before end anchor: {key}")
        continue

    # 正しい残り部分: </div> (sport-card閉じ) + anchor_e
    suffix = before_anchor[last_close:] + after_sm[anchor_pos_in_after:]

    # 新しいブロックを構築
    new_metrics_inner = build_metrics(sport_data[dk], label1)
    new_sm = f'{SM_TAG}\n{new_metrics_inner}\n        </div>'

    new_block = block[:sm_start] + new_sm + suffix

    if new_block == block:
        print(f"  [SAME] no change: {key}")
    else:
        lines_old = len(block.split('\n'))
        lines_new = len(new_block.split('\n'))
        print(f"  [OK] fixed: {key} ({lines_old} -> {lines_new} lines)")

    content = content[:idx_s] + new_block + content[idx_e:]

with open(DASH_PATH, "w", encoding="utf-8") as f:
    f.write(content)
print("\ndashboard.html saved.")

# 検証
with open(DASH_PATH, encoding="utf-8") as f:
    c2 = f.read()

import re as _re
no_style = _re.sub(r'<style[\s\S]*?</style>',
    lambda m: m.group().replace('<div','<XXX').replace('</div>','</XXX'), c2)

total_opens  = no_style.count('<div')
total_closes = no_style.count('</div>')
diff = total_opens - total_closes
status = "OK" if diff == 0 else f"PROBLEM({diff})"
print(f"Div balance (style masked): <div={total_opens}, </div={total_closes}, diff={diff} -> {status}")
