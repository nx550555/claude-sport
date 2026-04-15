#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sport-cards セクション全体を dashboard_stats.json から完全に再生成する。
fix_sc_final.py による構造破損（SCアンカー二重挿入・余分な</div>）を修正。
SCアンカーは使わず、sport-card-headerのユニーク色で sport-metrics を直接置換する方式に切り替える。
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

# ──────────────────────────────────────────────────
# ヘルパー
# ──────────────────────────────────────────────────
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
        if val is None or str(val) in ("\u2014", "", "None"): return ' style="color:#8b949e;"'
        try:
            pct = float(str(val).replace("%",""))
        except ValueError:
            return ' style="color:#8b949e;"'
        if pct >= 75:   return ' style="color:#3fb950;"'
        elif pct >= 60: return ' style="color:#e3b341;"'
        else:           return ' style="color:#f85149;"'
    if label == "\u7d2f\u7a4d\u0045\u0056":
        if val is None or str(val) in ("\u2014", "", "None"): return ' style="color:#8b949e;"'
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

def build_metrics_html(data, label1):
    rows = [
        sm_row(label1, data.get("go_count", 0)),
        sm_row("\u7d50\u679c\u6e08", data.get("confirmed_count", 0)),
        sm_row("\u7684\u4e2d", data.get("hit_count", 0)),
        sm_row("\u6b63\u7b54\u7387", fmt_rate(data.get("hit_rate"))),
        sm_row("\u7d2f\u7a4d\u0045\u0056", fmt_ev(data.get("ev_total", 0))),
        sm_row("\u5f85\u6a5f\u4e2d", str(data.get("pending_count", 0))),
    ]
    return "\n".join(rows)

# ──────────────────────────────────────────────────
# sport-card ブロック特定（色でユニークに識別）
# ──────────────────────────────────────────────────
SPORT_CARDS = [
    {"key": "ATP",  "data_key": "atp",         "label1": "GO\u56de\u6570", "color": "#79c0ff"},
    {"key": "WTA",  "data_key": "wta",         "label1": "GB\u63a8\u5968", "color": "#f9a8d4"},
    {"key": "NHL",  "data_key": "nhl",         "label1": "GO\u56de\u6570", "color": "#a5f3fc"},
    {"key": "UFL",  "data_key": "ufl",         "label1": "GO\u56de\u6570", "color": "#fca5a5", "extra": "UFL"},
    {"key": "NRL",  "data_key": "nrl",         "label1": "GO\u56de\u6570", "color": "#86efac"},
    {"key": "SRP",  "data_key": "superrugby",  "label1": "GO\u56de\u6570", "color": "#c4b5fd"},
    {"key": "NBA",  "data_key": "nba",         "label1": "GO\u56de\u6570", "color": "#fca5a5", "extra": "NBA"},
    {"key": "SL",   "data_key": "superleague", "label1": "GO\u56de\u6570", "color": "#bfdbfe"},
]

sport_data = stats.get("sports", {})

# ──────────────────────────────────────────────────
# sport-cards コンテナを取得・再構築
# ──────────────────────────────────────────────────

# sport-cards div の開始と終了を探す
SC_OPEN  = '<div class="sport-cards">'
# preseason-card の最初の出現の前の行を終端とする
PRESEASON = '<div class="preseason-card">'

sc_start = content.find(SC_OPEN)
if sc_start < 0:
    print("ERROR: sport-cards div not found")
    exit(1)

# preseason-card の前に sport-cards の閉じが来るはず
preseason_pos = content.find(PRESEASON, sc_start)
if preseason_pos < 0:
    print("ERROR: preseason-card not found")
    exit(1)

# sport-cards の終端は preseason-card の手前 → 正しい </div> を探す
# 現在の HTML で sport-cards の閉じを特定：
# 元の正しい構造では sport-cards が全 sport-card を包んでいるので、
# preseason-card の前の行に </div> がある
# → preseason-card の前の最後の </div> の後の位置を終端とする
before_preseason = content[sc_start:preseason_pos]

# sport-cards コンテナ全体を再生成する
# 元のHTMLから sport-card-header の HTML を取得して sport-metrics だけ差し替える

# アプローチ：元の sport-card ブロックを色で特定し、sport-metrics を差し替えて再構築
# まず各 sport-card の正しい HTML（sport-card-header + sport-metrics）を構築

def build_sport_card(card, metrics_html):
    """sport-card div 全体を生成"""
    # header は元のHTMLから取得する
    # 色とキーで sport-card-header を特定
    color = card["color"]
    extra = card.get("extra", "")

    # header テキストを元のHTMLから取得
    # sport-card-header div を色で探す
    header_pattern = f'style="color:{color};"'
    if extra:
        # UFL と NBA は同じ色なので extra text で区別
        header_search = f'{header_pattern}'
    else:
        header_search = header_pattern

    # sport-card-header div のコンテンツを元 HTML から取得
    # content の中から <div class="sport-card-header" style="color:{color};">...</div> を探す
    hdr_tag = f'<div class="sport-card-header" style="color:{color};">'

    all_positions = []
    pos = 0
    while True:
        idx = content.find(hdr_tag, pos)
        if idx < 0: break
        all_positions.append(idx)
        pos = idx + len(hdr_tag)

    if not all_positions:
        print(f"  [WARN] header not found for {card['key']}")
        return None

    # extra text で絞り込み
    target_pos = None
    if extra:
        for p in all_positions:
            line_end = content.find('\n', p)
            line = content[p:line_end]
            if extra in line:
                target_pos = p
                break
    else:
        target_pos = all_positions[0]

    if target_pos is None:
        print(f"  [WARN] header match not found for {card['key']} (extra={extra!r})")
        return None

    # header div の終わりを探す（この行の</div>）
    hdr_end = content.find('</div>', target_pos) + len('</div>')
    header_html = '        ' + content[target_pos:hdr_end]

    # sport-card 全体を組み立て
    sm_open  = '        <div class="sport-metrics">'
    sm_close = '        </div>'
    sport_card_html = (
        f'      <div class="sport-card">\n'
        f'{header_html}\n'
        f'{sm_open}\n'
        f'{metrics_html}\n'
        f'{sm_close}\n'
        f'      </div>'
    )
    return sport_card_html


# 新しい sport-cards セクション HTML を構築
new_sport_cards_lines = ['      <!-- sport-cards: rebuilt by fix_sport_cards_rebuild.py -->']
for card in SPORT_CARDS:
    dk = card["data_key"]
    if dk not in sport_data:
        print(f"  [SKIP] data not found: {dk}")
        continue

    metrics_html = build_metrics_html(sport_data[dk], card["label1"])
    card_html = build_sport_card(card, metrics_html)
    if card_html is None:
        print(f"  [ERROR] could not build card for {card['key']}")
        continue

    print(f"  [OK] built: {card['key']}")
    new_sport_cards_lines.append(card_html)

new_sport_cards_content = '\n'.join(new_sport_cards_lines)

# sport-cards コンテナ全体（SC_OPEN から preseason の直前まで）を置換
# preseason_pos の直前のスペース/改行を保持
sc_end = preseason_pos  # preseason_pos の手前まで

# sc_start から sc_end の内容を新しいものに置換
new_sc_block = (
    f'{SC_OPEN}\n'
    f'{new_sport_cards_content}\n'
    f'    </div>\n'
    f'    '  # preseason-card の前のインデント
)

content = content[:sc_start] + new_sc_block + content[sc_end:]

# ──────────────────────────────────────────────────
# SC アンカーコメントを全削除（残留防止）
# ──────────────────────────────────────────────────
content = re.sub(r'\s*<!-- (?:SC|/SC):[A-Z]+ -->', '', content)
print("  [OK] SC anchors removed")

with open(DASH_PATH, "w", encoding="utf-8") as f:
    f.write(content)
print("\ndashboard.html saved.")

# ──────────────────────────────────────────────────
# 検証
# ──────────────────────────────────────────────────
with open(DASH_PATH, encoding="utf-8") as f:
    c2 = f.read()

masked = re.sub(r'<style[\s\S]*?</style>',
    lambda m: m.group().replace('<div','<XXX').replace('</div>','</XXX'), c2)
masked = re.sub(r'<script[\s\S]*?</script>',
    lambda m: m.group().replace('<div','<XXX').replace('</div>','</XXX'), masked)

total_opens  = masked.count('<div')
total_closes = masked.count('</div>')
diff = total_opens - total_closes
print(f"Div balance (style+script masked): <div={total_opens}, </div={total_closes}, diff={diff}")

# sport-cards コンテナ確認
sc_pos = c2.find(SC_OPEN)
pre_pos = c2.find(PRESEASON, sc_pos)
sc_section = c2[sc_pos:pre_pos]
o = sc_section.count('<div')
cl = sc_section.count('</div>')
print(f"sport-cards section: o={o}, c={cl}, diff={o-cl}")
