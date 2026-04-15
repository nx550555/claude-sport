#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sync_sport_cards.py
===================
core/dashboard_stats.json を読んで dashboard.html の種目別カードを自動更新する。

【使い方】
  python sync_sport_cards.py

【いつ実行するか】
  - records/*.json に GO/CAUTION 追記後
  - 試合結果(HIT/MISS)を確定させた後
  - 必ず git commit の前に実行してから dashboard.html をコミットする

【動作原理】
  各 sport card の開始を <!-- SC:xxx --> アンカーコメントで検出し、
  その中の sm-val を正規表現で置換する。
  アンカーが存在しない場合は自動でアンカーを挿入する（初回のみ）。
"""

import json, re, sys
from pathlib import Path

BASE = Path(__file__).parent
STATS_PATH   = BASE / "core" / "dashboard_stats.json"
DASH_PATH    = BASE / "dashboard.html"

# ─────────────────────────────────────
# スポーツカード定義
# ─────────────────────────────────────
# anchor_key  : SC:xxx コメントの xxx 部分
# header_match: HTML 内でカードを特定するための固有文字列
SPORT_CARDS = [
    {"key": "ATP",   "header": "\U0001f3be ATP Tennis",       "data_key": "atp",        "label1": "GO\u56de\u6570"},
    {"key": "WTA",   "header": "\U0001f3be WTA Tennis",       "data_key": "wta",        "label1": "GB\u63a8\u5968"},
    {"key": "NHL",   "header": "\U0001f3d2 NHL",               "data_key": "nhl",        "label1": "GO\u56de\u6570"},
    {"key": "UFL",   "header": "\U0001f3c8 UFL",               "data_key": "ufl",        "label1": "GO\u56de\u6570"},
    {"key": "NRL",   "header": "\U0001f3c9 NRL",               "data_key": "nrl",        "label1": "GO\u56de\u6570"},
    {"key": "SRP",   "header": "Super Rugby Pacific",          "data_key": "superrugby", "label1": "GO\u56de\u6570"},
    {"key": "NBA",   "header": "\U0001f3c0 NBA",               "data_key": "nba",        "label1": "GO\u56de\u6570"},
    {"key": "SL",    "header": "Super League",                 "data_key": "superleague","label1": "GO\u56de\u6570"},
]

# ─────────────────────────────────────
# HTML 生成ヘルパー
# ─────────────────────────────────────
def color_for(label, val):
    """ラベルと値に応じた style 属性を返す"""
    if label in ("\u7684\u4e2d", "GO\u56de\u6570", "\u7d50\u679c\u6e08", "GB\u63a8\u5968"):
        return ""
    if label == "\u6b63\u7b54\u7387":
        if val is None or str(val) in ("\u2014", "", "None"):
            return ' style="color:#8b949e;"'
        try:
            pct = float(str(val).replace("%",""))
        except ValueError:
            return ' style="color:#8b949e;"'
        if pct >= 75:
            return ' style="color:#3fb950;"'
        elif pct >= 60:
            return ' style="color:#e3b341;"'
        else:
            return ' style="color:#f85149;"'
    if label == "\u7d2f\u7a4d\u0045\u0056":
        if val is None or str(val) in ("\u2014", "", "None"):
            return ' style="color:#8b949e;"'
        try:
            n = float(str(val).replace("+",""))
        except ValueError:
            return ' style="color:#8b949e;"'
        if n > 0:
            return ' style="color:#3fb950;"'
        elif n < 0:
            return ' style="color:#f85149;"'
        else:
            return ' style="color:#8b949e;"'
    if label == "\u5f85\u6a5f\u4e2d":
        n = int(val)
        if n > 0:
            return ' style="color:#d29922;"'
        else:
            return ' style="color:#8b949e;"'
    return ""

def sm_row(label, val):
    c = color_for(label, val)
    return f'          <div class="sm"><div class="sm-label">{label}</div><div class="sm-val"{c}>{val}</div></div>'

def fmt_rate(rate):
    if rate is None:
        return "\u2014"
    return f"{rate*100:.1f}%"

def fmt_ev(ev):
    if ev is None:
        return "\u2014"
    return f"+{ev:.3f}" if ev >= 0 else f"{ev:.3f}"

def build_sport_metrics(data, label1):
    """sport card の <div class="sport-metrics">...</div> 内側 HTML を生成"""
    go_count    = data.get("go_count", 0)
    confirmed   = data.get("confirmed_count", 0)
    hits        = data.get("hit_count", 0)
    hit_rate    = data.get("hit_rate")
    ev_total    = data.get("ev_total", 0)
    pending     = data.get("pending_count", 0)

    rate_str    = fmt_rate(hit_rate)
    ev_str      = fmt_ev(ev_total)
    pending_str = str(pending)

    rows = [
        sm_row(label1, go_count),
        sm_row("\u7d50\u679c\u6e08", confirmed),
        sm_row("\u7684\u4e2d", hits),
        sm_row("\u6b63\u7b54\u7387", rate_str),
        sm_row("\u7d2f\u7a4d\u0045\u0056", ev_str),
        sm_row("\u5f85\u6a5f\u4e2d", pending_str),
    ]
    return "\n".join(rows)

# ─────────────────────────────────────
# アンカー挿入（初回のみ）
# ─────────────────────────────────────
def ensure_anchors(content):
    """SC:xxx アンカーがない場合は各 sport card の前後に挿入する"""
    for card in SPORT_CARDS:
        key = card["key"]
        if f"<!-- SC:{key} -->" in content:
            continue  # 既存
        # sport-card-header で検索
        h = card["header"]
        # sport-card div の開始を探す
        pattern = r'(<div class="sport-card">[\s\S]{0,20}?<div class="sport-card-header"[^>]*>' + re.escape(h) + r')'
        m = re.search(pattern, content)
        if not m:
            print(f"  [WARN] アンカー挿入失敗: {key} (header not found: {h!r})")
            continue
        start = m.start()
        # <div class="sport-card"> の開始位置を見つける
        card_start = content.rfind('<div class="sport-card">', 0, start)
        if card_start < 0:
            print(f"  [WARN] sport-card div not found for {key}")
            continue
        # </div>を2つ進めて card の終了を探す（メトリクスdiv + sport-cardiv）
        # sport-card は </div>\n      </div> で終わる
        # 簡易: card_start から次の sport-card-header か preseason-card まで
        search_from = m.end()
        next_card = re.search(r'</div>\s*</div>\s*\n\s*<div class="(?:sport-card|preseason-card)', content[search_from:])
        if not next_card:
            print(f"  [WARN] カード終端が見つからない: {key}")
            continue
        card_end = search_from + next_card.start() + next_card.end() - len(next_card.group().split('\n')[-1]) - 1

        # </div></div>の最後の位置を探す
        card_end_tag_match = re.search(r'</div>\s*\n\s*</div>', content[search_from:search_from+500])
        if card_end_tag_match:
            card_end = search_from + card_end_tag_match.end()
        else:
            print(f"  [WARN] カード終端tag未検出: {key}")
            continue

        old_block = content[card_start:card_end]
        new_block = f"<!-- SC:{key} -->\n{old_block}\n<!-- /SC:{key} -->"
        content = content[:card_start] + new_block + content[card_end:]
        print(f"  [INFO] アンカー挿入: SC:{key}")
    return content

# ─────────────────────────────────────
# sport-metrics 部分のみを置換
# ─────────────────────────────────────
def update_sport_card(content, card, data):
    key    = card["key"]
    label1 = card.get("label1", "GO\u56de\u6570")

    anchor_start = f"<!-- SC:{key} -->"
    anchor_end   = f"<!-- /SC:{key} -->"

    if anchor_start not in content:
        print(f"  [SKIP] アンカーなし: {key}")
        return content

    idx_s = content.index(anchor_start)
    idx_e = content.index(anchor_end, idx_s) + len(anchor_end)
    block = content[idx_s:idx_e]

    new_metrics = build_sport_metrics(data, label1)

    # sport-metrics 内側を置換
    new_block = re.sub(
        r'(<div class="sport-metrics">)\s*[\s\S]*?\s*(</div>)',
        lambda m: m.group(1) + "\n" + new_metrics + "\n        " + m.group(2),
        block,
        count=1,
    )

    if new_block == block:
        print(f"  [WARN] 変更なし: {key}")
    else:
        print(f"  [OK] 更新: {key}")

    return content[:idx_s] + new_block + content[idx_e:]

# ─────────────────────────────────────
# 概要 big-stat の更新
# ─────────────────────────────────────
def update_overview(content, overview):
    """累積EV合計・待機中・内訳の big-stat を更新する"""
    # 累積EV合計
    ev = overview.get("total_ev", 0)
    ev_str = f"+{ev:.3f}" if ev >= 0 else f"{ev:.3f}"
    content = re.sub(
        r'(<div class="bs-label">\u7d2f\u7a4d\u0045\u0056\u5408\u8a08</div>\s*<div class="bs-val"[^>]*>)[^<]*(</div>)',
        lambda m: m.group(1) + ev_str + m.group(2),
        content,
    )

    # 待機中合計
    pending = overview.get("total_pending", 0)
    content = re.sub(
        r'(<div class="bs-label">\u5f85\u6a5f\u4e2d</div>\s*<div class="bs-val"[^>]*>)[^<]*(</div>)',
        lambda m: m.group(1) + str(pending) + m.group(2),
        content,
    )

    # 待機中内訳
    breakdown = overview.get("pending_breakdown", "")
    if breakdown:
        content = re.sub(
            r'(<div class="bs-sub">)(?:ATP|WTA|NRL|SL|UFL|NHL|NBA)[^<]*(</div>)',
            lambda m: m.group(1) + breakdown + m.group(2),
            content,
        )

    return content

# ─────────────────────────────────────
# メイン
# ─────────────────────────────────────
def main():
    print("=== sync_sport_cards.py ===")

    # JSON 読み込み
    with open(STATS_PATH, encoding="utf-8") as f:
        stats = json.load(f)
    print(f"Stats loaded: {STATS_PATH.name}, session={stats.get('session')}, updated={stats.get('last_updated')}")

    # dashboard.html 読み込み
    with open(DASH_PATH, encoding="utf-8") as f:
        content = f.read()

    # アンカー確認・挿入
    content = ensure_anchors(content)

    # 各 sport card を更新
    sport_data = stats.get("sports", {})
    for card in SPORT_CARDS:
        dk = card["data_key"]
        if dk in sport_data:
            content = update_sport_card(content, card, sport_data[dk])
        else:
            print(f"  [SKIP] data not found: {dk}")

    # 概要 big-stat 更新
    overview = stats.get("overview", {})
    if overview:
        content = update_overview(content, overview)
        print("  [OK] 概要 big-stat 更新")

    # 保存
    with open(DASH_PATH, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"dashboard.html saved.")

    # 使い方リマインダー
    print()
    print("次のステップ:")
    print("  git add dashboard.html core/dashboard_stats.json")
    print("  git commit -m 'Sync: sport cards updated'")

if __name__ == "__main__":
    main()
