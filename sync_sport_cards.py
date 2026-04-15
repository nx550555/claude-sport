#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sync_sport_cards.py
===================
core/dashboard_stats.json を読んで dashboard.html の種目別カードと概要big-statを自動更新する。

【使い方】
  python sync_sport_cards.py

【いつ実行するか】
  - records/*.json に GO 追記後
  - 試合結果(HIT/MISS)を確定させた後
  - 必ず git commit の前に実行してから dashboard.html をコミットする

【動作原理】
  sport-card-header の CSS色でカードをユニークに識別し、
  sport-cards セクション全体を再構築する（SCアンカー不使用）。
"""

import json, re
from pathlib import Path

BASE       = Path(__file__).parent
STATS_PATH = BASE / "core" / "dashboard_stats.json"
DASH_PATH  = BASE / "dashboard.html"

# ─────────────────────────────────────
# スポーツカード定義（color で sport-card-header をユニーク識別）
# UFL と NBA は同色なので extra テキストで区別
# ─────────────────────────────────────
SPORT_CARDS = [
    {"key": "ATP", "data_key": "atp",         "label1": "GO回数",  "color": "#79c0ff"},
    {"key": "WTA", "data_key": "wta",         "label1": "GB推奨",  "color": "#f9a8d4"},
    {"key": "NHL", "data_key": "nhl",         "label1": "GO回数",  "color": "#a5f3fc"},
    {"key": "UFL", "data_key": "ufl",         "label1": "GO回数",  "color": "#fca5a5", "extra": "UFL"},
    {"key": "NRL", "data_key": "nrl",         "label1": "GO回数",  "color": "#86efac"},
    {"key": "SRP", "data_key": "superrugby",  "label1": "GO回数",  "color": "#c4b5fd"},
    {"key": "NBA", "data_key": "nba",         "label1": "GO回数",  "color": "#fca5a5", "extra": "NBA"},
    {"key": "SL",  "data_key": "superleague", "label1": "GO回数",  "color": "#bfdbfe"},
]

# ─────────────────────────────────────
# HTML 生成ヘルパー
# ─────────────────────────────────────
def fmt_rate(rate):
    if rate is None:
        return "—"
    return f"{rate*100:.1f}%"

def fmt_ev(ev):
    if ev is None:
        return "—"
    return f"+{ev:.3f}" if ev >= 0 else f"{ev:.3f}"

def color_for(label, val):
    if label in ("的中", "GO回数", "結果済", "GB推奨"):
        return ""
    if label == "正答率":
        if val is None or str(val) in ("—", "", "None"):
            return ' style="color:#8b949e;"'
        try:
            pct = float(str(val).replace("%", ""))
        except ValueError:
            return ' style="color:#8b949e;"'
        if pct >= 75:
            return ' style="color:#3fb950;"'
        elif pct >= 60:
            return ' style="color:#e3b341;"'
        else:
            return ' style="color:#f85149;"'
    if label == "累積EV":
        if val is None or str(val) in ("—", "", "None"):
            return ' style="color:#8b949e;"'
        try:
            n = float(str(val).replace("+", ""))
        except ValueError:
            return ' style="color:#8b949e;"'
        if n > 0:
            return ' style="color:#3fb950;"'
        elif n < 0:
            return ' style="color:#f85149;"'
        else:
            return ' style="color:#8b949e;"'
    if label == "待機中":
        try:
            n = int(val)
        except (ValueError, TypeError):
            return ' style="color:#8b949e;"'
        return ' style="color:#d29922;"' if n > 0 else ' style="color:#8b949e;"'
    return ""

def sm_row(label, val):
    c = color_for(label, val)
    return (f'          <div class="sm">'
            f'<div class="sm-label">{label}</div>'
            f'<div class="sm-val"{c}>{val}</div>'
            f'</div>')

def build_metrics_html(data, label1):
    rows = [
        sm_row(label1,   data.get("go_count", 0)),
        sm_row("結果済", data.get("confirmed_count", 0)),
        sm_row("的中",   data.get("hit_count", 0)),
        sm_row("正答率", fmt_rate(data.get("hit_rate"))),
        sm_row("累積EV", fmt_ev(data.get("ev_total", 0))),
        sm_row("待機中", str(data.get("pending_count", 0))),
    ]
    return "\n".join(rows)

# ─────────────────────────────────────
# sport-card HTML 構築（color で header を特定）
# ─────────────────────────────────────
def build_sport_card(card, metrics_html, content):
    color = card["color"]
    extra = card.get("extra", "")
    hdr_tag = f'<div class="sport-card-header" style="color:{color};">'

    # 全出現位置を収集
    positions = []
    pos = 0
    while True:
        idx = content.find(hdr_tag, pos)
        if idx < 0:
            break
        positions.append(idx)
        pos = idx + len(hdr_tag)

    if not positions:
        print(f"  [WARN] header not found: {card['key']}")
        return None

    # extra テキストで絞り込み（UFL / NBA の同色区別）
    target = None
    if extra:
        for p in positions:
            line_end = content.find('\n', p)
            if extra in content[p:line_end]:
                target = p
                break
    else:
        target = positions[0]

    if target is None:
        print(f"  [WARN] header match not found: {card['key']} (extra={extra!r})")
        return None

    # header div の終わりを取得
    hdr_end = content.find('</div>', target) + len('</div>')
    header_html = '        ' + content[target:hdr_end]

    return (
        f'      <div class="sport-card">\n'
        f'{header_html}\n'
        f'        <div class="sport-metrics">\n'
        f'{metrics_html}\n'
        f'        </div>\n'
        f'      </div>'
    )

# ─────────────────────────────────────
# sport-cards セクションを再構築
# ─────────────────────────────────────
def rebuild_sport_cards(content, sport_data):
    SC_OPEN   = '<div class="sport-cards">'
    PRESEASON = '<div class="preseason-card">'

    sc_start = content.find(SC_OPEN)
    if sc_start < 0:
        print("  [ERROR] sport-cards div not found")
        return content

    preseason_pos = content.find(PRESEASON, sc_start)
    if preseason_pos < 0:
        print("  [ERROR] preseason-card not found")
        return content

    lines = ['      <!-- sport-cards: rebuilt by sync_sport_cards.py -->']
    for card in SPORT_CARDS:
        dk = card["data_key"]
        if dk not in sport_data:
            print(f"  [SKIP] data not found: {dk}")
            continue
        metrics_html = build_metrics_html(sport_data[dk], card["label1"])
        card_html = build_sport_card(card, metrics_html, content)
        if card_html is None:
            print(f"  [ERROR] could not build: {card['key']}")
            continue
        print(f"  [OK] {card['key']}")
        lines.append(card_html)

    new_sc_block = (
        f'{SC_OPEN}\n'
        + '\n'.join(lines) + '\n'
        + '    </div>\n'
        + '    '
    )
    content = content[:sc_start] + new_sc_block + content[preseason_pos:]

    # 残留 SC アンカーコメントを削除
    content = re.sub(r'\s*<!-- (?:SC|/SC):[A-Z]+ -->', '', content)
    return content

# ─────────────────────────────────────
# 概要 big-stat を更新
# ─────────────────────────────────────
def update_overview(content, overview):
    total_go        = overview.get("total_go", 0)
    total_confirmed = overview.get("total_confirmed", 0)
    total_hits      = overview.get("total_hits", 0)
    hit_rate        = overview.get("hit_rate")
    total_ev        = overview.get("total_ev", 0)
    total_pending   = overview.get("total_pending", 0)
    breakdown       = overview.get("pending_breakdown", "")

    rate_str = f"{hit_rate*100:.1f}%" if hit_rate is not None else "—"
    ev_str   = f"+{total_ev:.3f}" if total_ev >= 0 else f"{total_ev:.3f}"
    ev_color = "#3fb950" if total_ev > 0 else ("#f85149" if total_ev < 0 else "#8b949e")
    rate_color = "#3fb950" if (hit_rate or 0) >= 0.75 else ("#e3b341" if (hit_rate or 0) >= 0.6 else "#f85149")

    # 総GO回数
    content = re.sub(
        r'(<div class="bs-label">総GO回数</div>\s*<div class="bs-val"[^>]*>)\d+(</div>\s*<div class="bs-sub">結果確定:) \d+件(</div>)',
        lambda m: f'{m.group(1)}{total_go}{m.group(2)} {total_confirmed}件{m.group(3)}',
        content
    )

    # 通算正答率
    content = re.sub(
        r'(<div class="bs-label">通算正答率</div>\s*<div class="bs-val"[^>]*>)[^<]+(</div>\s*<div class="bs-sub">)\d+HIT / \d+試合(</div>)',
        lambda m: f'<div class="bs-label">通算正答率</div>\n        <div class="bs-val" style="color:{rate_color};">{rate_str}{m.group(2)}{total_hits}HIT / {total_confirmed}試合{m.group(3)}',
        content
    )

    # 累積EV合計
    content = re.sub(
        r'(<div class="bs-label">累積EV合計</div>\s*<div class="bs-val"[^>]*>)[^<]+(</div>)',
        lambda m: f'<div class="bs-label">累積EV合計</div>\n        <div class="bs-val" style="color:{ev_color};">{ev_str}{m.group(2)}',
        content
    )

    # 待機中 (数値)
    content = re.sub(
        r'(<div class="bs-label">待機中</div>\s*<div class="bs-val"[^>]*>)\d+(</div>)',
        lambda m: f'{m.group(1)}{total_pending}{m.group(2)}',
        content
    )

    # 待機中 内訳
    if breakdown:
        content = re.sub(
            r'(<div class="bs-sub">)(ATP[^<]*)(</div>(?:\s*</div>){0,1}\s*</div>\s*</div>\s*</div>)',
            lambda m: f'{m.group(1)}{breakdown}{m.group(3)}',
            content,
            count=1
        )

    return content

# ─────────────────────────────────────
# メイン
# ─────────────────────────────────────
def main():
    print("=== sync_sport_cards.py ===")

    with open(STATS_PATH, encoding="utf-8-sig") as f:
        stats = json.load(f)
    print(f"Loaded: {STATS_PATH.name}, session={stats.get('session')}, updated={stats.get('last_updated')}")

    with open(DASH_PATH, encoding="utf-8") as f:
        content = f.read()

    sport_data = stats.get("sports", {})

    # ① overview を sports から自動計算して更新
    total_go        = sum(s.get("go_count", 0)        for s in sport_data.values())
    total_confirmed = sum(s.get("confirmed_count", 0)  for s in sport_data.values())
    total_hits      = sum(s.get("hit_count", 0)        for s in sport_data.values())
    total_ev        = sum(s.get("ev_total", 0)         for s in sport_data.values())
    total_pending   = sum(s.get("pending_count", 0)    for s in sport_data.values())
    hit_rate        = total_hits / total_confirmed if total_confirmed > 0 else None

    # pending 内訳
    breakdown_parts = []
    key_label = {"atp":"ATP","wta":"WTA","nhl":"NHL","ufl":"UFL","nrl":"NRL",
                 "superrugby":"SRP","nba":"NBA","superleague":"SL"}
    for dk, label in key_label.items():
        p = sport_data.get(dk, {}).get("pending_count", 0)
        if p > 0:
            breakdown_parts.append(f"{label} x{p}")
    breakdown = " + ".join(breakdown_parts)

    overview = {
        "total_go": total_go,
        "total_confirmed": total_confirmed,
        "total_hits": total_hits,
        "hit_rate": round(hit_rate, 3) if hit_rate is not None else None,
        "total_ev": round(total_ev, 3),
        "total_pending": total_pending,
        "pending_breakdown": breakdown,
    }
    stats["overview"] = overview

    # overview を dashboard_stats.json にも保存
    with open(STATS_PATH, "w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)
    print(f"  overview: GO={total_go}, confirmed={total_confirmed}, hit={total_hits}, "
          f"rate={f'{hit_rate*100:.1f}%' if hit_rate else 'N/A'}, ev={total_ev:.3f}, pending={total_pending}")

    # ② sport-cards セクション再構築
    print("--- sport-cards rebuild ---")
    content = rebuild_sport_cards(content, sport_data)

    # ③ 概要 big-stat 更新
    content = update_overview(content, overview)
    print("  [OK] big-stat updated")

    # ④ 保存
    with open(DASH_PATH, "w", encoding="utf-8") as f:
        f.write(content)
    print("dashboard.html saved.")

    # ⑤ div balance 検証
    masked = re.sub(r'<style[\s\S]*?</style>',
                    lambda m: m.group().replace('<div', '<XXX').replace('</div>', '</XXX'), content)
    masked = re.sub(r'<script[\s\S]*?</script>',
                    lambda m: m.group().replace('<div', '<XXX').replace('</div>', '</XXX'), masked)
    o  = masked.count('<div')
    cl = masked.count('</div>')
    diff = o - cl
    status = "OK" if diff == 0 else f"PROBLEM(diff={diff})"
    print(f"Div balance: <div={o}, </div={cl}, diff={diff} → {status}")

    print()
    print("次のステップ:")
    print("  git add dashboard.html core/dashboard_stats.json")
    print("  git commit -m 'Sync: sport cards updated'")

if __name__ == "__main__":
    main()
