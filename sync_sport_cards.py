#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sync_sport_cards.py
===================
records/*.json を直接読んで統計を再計算し、dashboard.html を更新する。

【使い方】
  python sync_sport_cards.py

【いつ実行するか】
  - records/*.json に GO 追記後
  - 試合結果(HIT/MISS)を確定させた後
  - 必ず git commit の前に実行してから dashboard.html をコミットする

【計算ルール】
  - カウント対象: tier='go' または tier='gamble_bet'
  - 通算損益: 1単位ベット想定、HIT=+1u / MISS=-1u
  - WTA は gamble_bet が主推奨なので go + gamble_bet を両方カウント
"""

import json, re
from pathlib import Path

BASE       = Path(__file__).parent
STATS_PATH = BASE / "core" / "dashboard_stats.json"
DASH_PATH  = BASE / "dashboard.html"

# ─────────────────────────────────────
# records パス定義
# ─────────────────────────────────────
RECORDS = {
    "atp":         BASE / "records/tennis/2026-ATP.json",
    "wta":         BASE / "records/wta/2026.json",
    "nhl":         BASE / "records/nhl/2025-26.json",
    "ufl":         BASE / "records/ufl/2026.json",
    "nrl":         BASE / "records/nrl/2026.json",
    "superrugby":  BASE / "records/superrugby/2026.json",
    "nba":         BASE / "records/nba/2025-26.json",
    "superleague": BASE / "records/superleague/2026.json",
}

# ─────────────────────────────────────
# スポーツカード定義
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
# 統計再計算
# ─────────────────────────────────────
GO_TIERS = {"go", "gamble_bet"}

def load_json(path):
    try:
        with open(path, encoding="utf-8-sig") as f:
            return json.load(f)
    except Exception as e:
        print(f"  [WARN] load failed: {path.name}: {e}")
        return None

def get_go_entries(data):
    """GO/GB推奨エントリを全構造から収集（go + gamble_bet）"""
    entries = []
    # top-level predictions[] (ATP)
    for e in data.get("predictions", []):
        if e.get("tier") in GO_TIERS:
            entries.append(e)
    # top-level games[] + pending_games[] (NHL/UFL/NRL/NBA/SL/SRP)
    for e in data.get("games", []) + data.get("pending_games", []):
        if e.get("tier") in GO_TIERS:
            entries.append(e)
    # tournaments[].predictions[] (WTA)
    for t in data.get("tournaments", []):
        for e in t.get("predictions", []):
            if e.get("tier") in GO_TIERS:
                entries.append(e)
    return entries

def calc_stats(data):
    go_entries      = get_go_entries(data)
    go_count        = len(go_entries)
    confirmed       = [e for e in go_entries if e.get("hit") is not None]
    confirmed_count = len(confirmed)
    hit_count       = sum(1 for e in confirmed if e.get("hit") is True)
    hit_rate        = hit_count / confirmed_count if confirmed_count > 0 else None
    # 実現損益: actual_ev を使用（hit=True: rec_odds-1, hit=False: -1.0）
    pnl             = sum((e.get("actual_ev") or 0) for e in confirmed)
    pending_count   = go_count - confirmed_count
    return {
        "go_count":        go_count,
        "confirmed_count": confirmed_count,
        "hit_count":       hit_count,
        "hit_rate":        round(hit_rate, 3) if hit_rate is not None else None,
        "pnl":             pnl,          # realized P&L in units (±1 per bet)
        "pending_count":   pending_count,
    }

def recalc_all_stats():
    """全スポーツを records から再計算して dashboard_stats.json に保存"""
    sports = {}
    for key, path in RECORDS.items():
        data = load_json(path)
        if data is None:
            sports[key] = {"go_count":0,"confirmed_count":0,"hit_count":0,
                           "hit_rate":None,"pnl":0.0,"pending_count":0}
            continue
        s = calc_stats(data)
        sports[key] = s
        rate_str = f"{s['hit_rate']*100:.1f}%" if s["hit_rate"] else "N/A"
        pnl_str  = f"+{s['pnl']:.1f}u" if s["pnl"] >= 0 else f"{s['pnl']:.1f}u"
        print(f"  {key:12s}: GO={s['go_count']}, confirmed={s['confirmed_count']}, "
              f"hit={s['hit_count']}, rate={rate_str}, P&L={pnl_str}, pending={s['pending_count']}")

    # overview 合計
    total_go        = sum(s["go_count"]        for s in sports.values())
    total_confirmed = sum(s["confirmed_count"] for s in sports.values())
    total_hits      = sum(s["hit_count"]       for s in sports.values())
    total_pnl       = sum(s["pnl"]            for s in sports.values())
    total_pending   = sum(s["pending_count"]   for s in sports.values())
    hit_rate        = total_hits / total_confirmed if total_confirmed > 0 else None

    key_label = {"atp":"ATP","wta":"WTA","nhl":"NHL","ufl":"UFL","nrl":"NRL",
                 "superrugby":"SRP","nba":"NBA","superleague":"SL"}
    breakdown_parts = [f"{lbl} x{sports[k]['pending_count']}"
                       for k, lbl in key_label.items()
                       if sports.get(k, {}).get("pending_count", 0) > 0]
    breakdown = " + ".join(breakdown_parts)

    overview = {
        "total_go":        total_go,
        "total_confirmed": total_confirmed,
        "total_hits":      total_hits,
        "hit_rate":        round(hit_rate, 3) if hit_rate is not None else None,
        "total_pnl":       round(total_pnl, 1),
        "total_pending":   total_pending,
        "pending_breakdown": breakdown,
    }

    # dashboard_stats.json に保存
    try:
        with open(STATS_PATH, encoding="utf-8-sig") as f:
            stats = json.load(f)
    except Exception:
        stats = {}
    stats["sports"]  = sports
    stats["overview"] = overview
    import datetime
    stats["last_updated"] = datetime.date.today().isoformat()

    with open(STATS_PATH, "w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)

    pnl_str = f"+{total_pnl:.1f}u" if total_pnl >= 0 else f"{total_pnl:.1f}u"
    print(f"  {'TOTAL':12s}: GO={total_go}, confirmed={total_confirmed}, "
          f"hit={total_hits}, rate={f'{hit_rate*100:.1f}%' if hit_rate else 'N/A'}, "
          f"P&L={pnl_str}, pending={total_pending}")
    return stats

# ─────────────────────────────────────
# HTML 生成ヘルパー
# ─────────────────────────────────────
def fmt_rate(rate):
    if rate is None: return "—"
    return f"{rate*100:.1f}%"

def fmt_pnl(pnl):
    if pnl is None: return "—"
    return f"+{pnl:.1f}u" if pnl >= 0 else f"{pnl:.1f}u"

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
        if pct >= 75:   return ' style="color:#3fb950;"'
        elif pct >= 60: return ' style="color:#e3b341;"'
        else:           return ' style="color:#f85149;"'
    if label == "通算損益":
        if val is None or str(val) in ("—", "", "None"):
            return ' style="color:#8b949e;"'
        try:
            n = float(str(val).replace("+","").replace("u",""))
        except ValueError:
            return ' style="color:#8b949e;"'
        if n > 0:   return ' style="color:#3fb950;"'
        elif n < 0: return ' style="color:#f85149;"'
        else:       return ' style="color:#8b949e;"'
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
        sm_row("通算損益", fmt_pnl(data.get("pnl", 0.0))),
        sm_row("待機中", str(data.get("pending_count", 0))),
    ]
    return "\n".join(rows)

# ─────────────────────────────────────
# sport-card HTML 構築
# ─────────────────────────────────────
def build_sport_card(card, metrics_html, content):
    color = card["color"]
    extra = card.get("extra", "")
    hdr_tag = f'<div class="sport-card-header" style="color:{color};">'

    positions = []
    pos = 0
    while True:
        idx = content.find(hdr_tag, pos)
        if idx < 0: break
        positions.append(idx)
        pos = idx + len(hdr_tag)

    if not positions:
        print(f"  [WARN] header not found: {card['key']}")
        return None

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
        print(f"  [WARN] header match not found: {card['key']}")
        return None

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
# sport-cards セクション再構築
# ─────────────────────────────────────
def rebuild_sport_cards(content, sport_data):
    SC_OPEN   = '<div class="sport-cards">'
    PRESEASON = '<div class="preseason-card">'

    sc_start = content.find(SC_OPEN)
    if sc_start < 0:
        print("  [ERROR] sport-cards div not found"); return content

    preseason_pos = content.find(PRESEASON, sc_start)
    if preseason_pos < 0:
        print("  [ERROR] preseason-card not found"); return content

    lines = ['      <!-- sport-cards: rebuilt by sync_sport_cards.py -->']
    for card in SPORT_CARDS:
        dk = card["data_key"]
        if dk not in sport_data:
            print(f"  [SKIP] {dk}"); continue
        metrics_html = build_metrics_html(sport_data[dk], card["label1"])
        card_html = build_sport_card(card, metrics_html, content)
        if card_html is None:
            print(f"  [ERROR] {card['key']}"); continue
        print(f"  [OK] {card['key']}")
        lines.append(card_html)

    new_sc_block = (SC_OPEN + '\n'
                    + '\n'.join(lines) + '\n'
                    + '    </div>\n    ')
    content = content[:sc_start] + new_sc_block + content[preseason_pos:]
    content = re.sub(r'\s*<!-- (?:SC|/SC):[A-Z]+ -->', '', content)
    return content

# ─────────────────────────────────────
# 概要 big-stat 更新
# ─────────────────────────────────────
def update_overview(content, overview):
    total_go        = overview.get("total_go", 0)
    total_confirmed = overview.get("total_confirmed", 0)
    total_hits      = overview.get("total_hits", 0)
    hit_rate        = overview.get("hit_rate")
    total_pnl       = overview.get("total_pnl", 0.0)
    total_pending   = overview.get("total_pending", 0)
    breakdown       = overview.get("pending_breakdown", "")

    rate_str  = f"{hit_rate*100:.1f}%" if hit_rate is not None else "—"
    pnl_str   = f"+{total_pnl:.1f}u" if total_pnl >= 0 else f"{total_pnl:.1f}u"
    pnl_color = "#3fb950" if total_pnl > 0 else ("#f85149" if total_pnl < 0 else "#8b949e")
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
        lambda m: (f'<div class="bs-label">通算正答率</div>\n'
                   f'        <div class="bs-val" style="color:{rate_color};">{rate_str}'
                   f'{m.group(2)}{total_hits}HIT / {total_confirmed}試合{m.group(3)}'),
        content
    )
    # 通算損益（旧: 累積EV合計）
    content = re.sub(
        r'<div class="bs-label">(?:累積EV合計|通算損益)</div>\s*<div class="bs-val"[^>]*>[^<]*(</div>)',
        f'<div class="bs-label">通算損益</div>\n        <div class="bs-val" style="color:{pnl_color};">{pnl_str}\\1',
        content
    )
    # bs-sub: 単位説明
    content = re.sub(
        r'(<div class="bs-sub">単位:)[^<]*(</div>)',
        r'\g<1> (オッズ-1)u / MISS=-1u（1単位ベット）\2',
        content
    )
    # 待機中（数値）
    content = re.sub(
        r'(<div class="bs-label">待機中</div>\s*<div class="bs-val"[^>]*>)\d+(</div>)',
        lambda m: f'{m.group(1)}{total_pending}{m.group(2)}',
        content
    )
    # 待機中内訳（bs-sub直前のbs-valが待機中数値の場合のみ更新）
    if breakdown:
        content = re.sub(
            r'(<div class="bs-label">待機中</div>.*?<div class="bs-sub">)[^<]*(</div>\s*</div>)',
            lambda m: f'{m.group(1)}{breakdown}{m.group(2)}',
            content, count=1, flags=re.DOTALL
        )
    return content

# ─────────────────────────────────────
# メイン
# ─────────────────────────────────────
def main():
    print("=== sync_sport_cards.py ===")

    # ① records から統計再計算
    print("--- recalculate from records ---")
    stats = recalc_all_stats()
    sport_data = stats["sports"]
    overview   = stats["overview"]

    # ② dashboard.html 更新
    with open(DASH_PATH, encoding="utf-8") as f:
        content = f.read()

    print("--- sport-cards rebuild ---")
    content = rebuild_sport_cards(content, sport_data)

    content = update_overview(content, overview)
    print("  [OK] big-stat updated")

    with open(DASH_PATH, "w", encoding="utf-8") as f:
        f.write(content)
    print("dashboard.html saved.")

    # ③ div balance 検証
    masked = re.sub(r'<style[\s\S]*?</style>',
                    lambda m: m.group().replace('<div','<XXX').replace('</div>','</XXX'), content)
    masked = re.sub(r'<script[\s\S]*?</script>',
                    lambda m: m.group().replace('<div','<XXX').replace('</div>','</XXX'), masked)
    o  = masked.count('<div')
    cl = masked.count('</div>')
    diff = o - cl
    print(f"Div balance: <div={o}, </div={cl}, diff={diff} -> {'OK' if diff==0 else 'PROBLEM'}")

    print()
    print("次のステップ:")
    print("  git add dashboard.html core/dashboard_stats.json records/")
    print("  git commit -m 'Sync: sport cards + stats recalculated'")

if __name__ == "__main__":
    main()
