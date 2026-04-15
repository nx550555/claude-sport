#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
マルチベットセクションをベットスリップ形式に刷新
「どの試合・どの予想・どのオッズで賭けるのか」が一目でわかるレイアウトに変更
"""

path = r"C:\Users\ohwada\Desktop\claude_sport\dashboard.html"
with open(path, encoding='utf-8') as f:
    content = f.read()

# ベースとなる3試合レッグ定義
BASE_LEGS = [
    {
        "sport_emoji": "\U0001f3c8",
        "sport_label": "UFL W4",
        "match_ja": "\u30d2\u30e5\u30fc\u30b9\u30c8\u30f3\u30fb\u30ae\u30e3\u30f3\u30d6\u30e9\u30fc\u30ba vs \u30eb\u30a4\u30d3\u30eb\u30fb\u30ad\u30f3\u30b0\u30b9",
        "match_en": "Houston Gamblers vs Louisville Kings",
        "rec_ja": "\u30eb\u30a4\u30d3\u30eb\u30fb\u30ad\u30f3\u30b0\u30b9",
        "rec_en": "Louisville Kings",
        "odds": 1.65,
        "conf": 82,
        "ev_flag": True,   # EV+
        "date": "4/17",
        "key": "louisville",
    },
    {
        "sport_emoji": "\U0001f3c8",
        "sport_label": "UFL W4",
        "match_ja": "\u30b3\u30ed\u30f3\u30d0\u30b9\u30fb\u30a2\u30d3\u30a8\u30a4\u30bf\u30fc\u30ba @ \u30a2\u30fc\u30ea\u30f3\u30c8\u30f3\u30fb\u30ec\u30cd\u30b2\u30fc\u30ba",
        "match_en": "Columbus Aviators @ Arlington Renegades",
        "rec_ja": "\u30a2\u30fc\u30ea\u30f3\u30c8\u30f3\u30fb\u30ec\u30cd\u30b2\u30fc\u30ba",
        "rec_en": "Arlington Renegades",
        "odds": 1.36,
        "conf": 85,
        "ev_flag": True,
        "date": "4/18",
        "key": "renegades",
    },
    {
        "sport_emoji": "\U0001f3be",
        "sport_label": "ATP Barcelona R2",
        "match_ja": "\u30e0\u30c6 C. vs \u30e0\u30bb\u30c3\u30c6\u30a3 L.(2)",
        "match_en": "Moutet C. vs Musetti L.(2)",
        "rec_ja": "\u30e0\u30bb\u30c3\u30c6\u30a3 L.",
        "rec_en": "Musetti L.",
        "odds": 1.37,
        "conf": 78,
        "ev_flag": True,
        "date": "4/16",
        "key": "musetti",
    },
]

ADD_LEGS = {
    "alcaraz": {
        "sport_emoji": "\U0001f3be",
        "sport_label": "ATP Barcelona R2",
        "match_ja": "\u30a2\u30eb\u30ab\u30e9\u30b9 C. vs \u30de\u30cf\u30c3\u30c1 T.",
        "match_en": "Alcaraz C. vs Machac T.",
        "rec_ja": "\u30a2\u30eb\u30ab\u30e9\u30b9 C.",
        "rec_en": "Alcaraz C.",
        "odds": 1.11,
        "conf": 88,
        "ev_flag": False,
        "date": "4/16",
    },
    "paolini": {
        "sport_emoji": "\U0001f3be",
        "sport_label": "WTA Stuttgart R2",
        "match_ja": "\u30bd\u30f3\u30e1\u30ba Z. vs \u30d1\u30aa\u30ea\u30fc\u30cb J.(4)",
        "match_en": "Sonmez Z. vs Paolini J.(4)",
        "rec_ja": "\u30d1\u30aa\u30ea\u30fc\u30cb J.",
        "rec_en": "Paolini J.",
        "odds": 1.24,
        "conf": 78,
        "ev_flag": True,
        "date": "4/15",
    },
    "swiatek": {
        "sport_emoji": "\U0001f3be",
        "sport_label": "WTA Stuttgart R2",
        "match_ja": "\u30b7\u30d5\u30a3\u30a2\u30c6\u30af I. vs \u30b8\u30fc\u30b2\u30e0\u30f3\u30c8 L.",
        "match_en": "Swiatek I. vs Siegemund L.",
        "rec_ja": "\u30b7\u30d5\u30a3\u30a2\u30c6\u30af I.",
        "rec_en": "Swiatek I.",
        "odds": 1.02,
        "conf": 92,
        "ev_flag": False,
        "date": "4/16",
    },
}

# 5つの組み合わせ定義
COMBOS = [
    {
        "rank": 1, "medal": "\U0001f947",
        "legs": BASE_LEGS,
        "additions": [],
        "prob": 0.5437, "multi_odds": 3.0743, "multi_ev": 67.1,
        "formula": "0.82\u00d70.85\u00d70.78=0.5437 | 1.65\u00d71.36\u00d71.37=3.0743 | EV=+67.1%",
    },
    {
        "rank": 2, "medal": "\U0001f948",
        "legs": BASE_LEGS,
        "additions": [ADD_LEGS["alcaraz"]],
        "prob": 0.4785, "multi_odds": 3.4124, "multi_ev": 63.2,
        "formula": "prob=0.4785 | odds=3.4124 | EV=+63.2%",
    },
    {
        "rank": 3, "medal": "\U0001f949",
        "legs": BASE_LEGS,
        "additions": [ADD_LEGS["paolini"]],
        "prob": 0.4241, "multi_odds": 3.8121, "multi_ev": 61.7,
        "formula": "prob=0.4241 | odds=3.8121 | EV=+61.7%",
    },
    {
        "rank": 4, "medal": "4\u4f4d",
        "legs": BASE_LEGS,
        "additions": [ADD_LEGS["alcaraz"], ADD_LEGS["paolini"]],
        "prob": 0.3732, "multi_odds": 4.2314, "multi_ev": 57.9,
        "formula": "prob=0.3732 | odds=4.2314 | EV=+57.9%",
    },
    {
        "rank": 5, "medal": "5\u4f4d",
        "legs": BASE_LEGS,
        "additions": [ADD_LEGS["swiatek"]],
        "prob": 0.5002, "multi_odds": 3.1358, "multi_ev": 56.8,
        "formula": "prob=0.5002 | odds=3.1358 | EV=+56.8%",
    },
]

def leg_html(leg, is_addition=False):
    add_mark = '<span style="font-size:10px;background:#1c2d1e;color:#3fb950;border-radius:3px;padding:1px 5px;margin-right:4px;">+追加</span>' if is_addition else ''
    # EV バッジ
    ev_badge = '<span style="font-size:9px;color:#3fb950;margin-left:4px;">EV+</span>' if leg.get("ev_flag") else '<span style="font-size:9px;color:#8b949e;margin-left:4px;">EV-</span>'
    opacity = '' if not is_addition else ' style="opacity:.85;"'
    return f'''\
        <div class="multi-leg"{opacity}>
          <span class="ml-sport">{leg["sport_emoji"]} {leg["sport_label"]}</span>
          {add_mark}
          <span class="ml-date">{leg["date"]}</span>
          <div class="ml-match">
            <span class="name-ja">{leg["match_ja"]}</span><span class="name-en">{leg["match_en"]}</span>
          </div>
          <div class="ml-rec">
            \u2192 <strong style="color:#3fb950;">
              <span class="name-ja">{leg["rec_ja"]}</span><span class="name-en">{leg["rec_en"]}</span>
            </strong>
            <span class="ml-odds">@{leg["odds"]}</span>
            <span class="ml-conf">({leg["conf"]}%)</span>
            {ev_badge}
          </div>
        </div>'''

def combo_html(c):
    all_legs = c["legs"] + c["additions"]
    n_legs = len(all_legs)
    ev_col = "#4ade80" if c["multi_ev"] > 0 else "#f85149"
    legs_html = "\n".join([leg_html(l, is_addition=False) for l in c["legs"]] +
                           [leg_html(l, is_addition=True) for l in c["additions"]])
    return f'''\
      <div class="multi-combo">
        <div class="mc-header">
          <span class="mc-rank">{c["medal"]}</span>
          <span class="mc-legs-count">{n_legs}\u9023\u8907</span>
          <span class="mc-ev" style="color:{ev_col};">EV <strong>{c["multi_ev"]:+.1f}%</strong></span>
          <span class="mc-odds">\u30de\u30eb\u30c1\u30aa\u30c3\u30ba: <strong>{c["multi_odds"]:.4f}</strong></span>
          <span class="mc-prob">\u5168\u4f53\u52dd\u7387: <strong style="color:{ev_col};">{c["prob"]*100:.1f}%</strong></span>
          <span class="badge badge-pending" style="margin-left:auto;">PENDING</span>
        </div>
        <div class="mc-legs">
{legs_html}
        </div>
        <div class="mc-formula">{c["formula"]}</div>
      </div>'''

# CSS 追加
new_css = """
/* ── multi-bet betslip ── */
.multi-combo{background:var(--surface);border:1px solid var(--border);border-radius:8px;overflow:hidden;}
.mc-header{display:flex;align-items:center;gap:8px;flex-wrap:wrap;padding:10px 14px;border-bottom:1px solid var(--border);}
.mc-rank{font-weight:700;font-size:15px;color:var(--text);min-width:24px;}
.mc-legs-count{font-size:11px;font-weight:700;background:var(--surface2);border:1px solid var(--border);border-radius:10px;padding:1px 8px;color:var(--text2);}
.mc-ev{font-size:13px;}
.mc-odds,.mc-prob{font-size:12px;color:var(--text2);}
.mc-legs{display:flex;flex-direction:column;gap:0;}
.multi-leg{padding:8px 14px;border-bottom:1px solid var(--border);font-size:12px;}
.multi-leg:last-child{border-bottom:none;}
.ml-sport{font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.05em;color:var(--text2);margin-right:6px;}
.ml-date{font-size:10px;color:var(--text2);background:var(--surface2);border-radius:4px;padding:1px 5px;}
.ml-match{color:var(--text2);margin-top:2px;}
.ml-rec{margin-top:2px;}
.ml-odds{font-size:11px;color:#e3b341;margin-left:4px;}
.ml-conf{font-size:10px;color:var(--text2);}
.mc-formula{font-size:10px;color:var(--text2);padding:6px 14px;background:var(--surface2);}
"""

# multi-rows div の内容を置換
new_multi_rows = '\n'.join([combo_html(c) for c in COMBOS])
new_multi_rows += '''
      <div style="font-size:11px;color:var(--text2);text-align:right;padding:4px 0;">
        Session _29 (2026-04-15) &nbsp;|&nbsp; \u51fa\u529bA: 7\u8a66\u5408 &nbsp;|&nbsp; EV+\u7d44\u307f\u5408\u308f\u305b: 5\u30d1\u30bf\u30fc\u30f3 &nbsp;|&nbsp; &#x26A0; Musetti conf 82%&#x2192;78% \u4fee\u6b63\u6e08
      </div>'''

# CSS を追加 (lang toggle CSS の後)
content = content.replace('.mc-rank', '.mc-rank-PLACEHOLDER', 1)  # 重複防止チェック
if '.mc-rank-PLACEHOLDER' in content:
    content = content.replace('.mc-rank-PLACEHOLDER', '.mc-rank')
    print("SKIP: CSS already exists")
else:
    content = content.replace('</style>', new_css + '\n</style>', 1)
    print("OK: CSS added")

# multi-rows div の内容を置換
import re
content, n = re.subn(
    r'(<div id="multi-rows"[^>]*>)[\s\S]+?(</div>\n</div>\n</div>)',
    lambda m: m.group(1) + '\n' + new_multi_rows + '\n    ' + m.group(2),
    content,
    count=1
)
if n == 1:
    print("OK: multi-rows replaced")
else:
    print(f"MISS: multi-rows not replaced (n={n})")
    # フォールバック
    old_marker = '<div id="multi-rows"'
    if old_marker in content:
        idx = content.index(old_marker)
        print(f"  multi-rows found at idx={idx}")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("dashboard.html saved.")
