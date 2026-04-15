#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""マルチベット をベットスリップ形式に変更（シンプル版）"""

path = r"C:\Users\ohwada\Desktop\claude_sport\dashboard.html"
with open(path, encoding='utf-8') as f:
    content = f.read()

# multi-rows の開始
START = '<div id="multi-rows" style="display:flex;flex-direction:column;gap:12px;">'
# multi-rows の終了（セッション注記の後の閉じタグ）
# 末尾のパターン: \n    </div>\n  </div>\n</div>
# これを見つけるため、セッション注記を含むパターンを使う
END_MARKER = 'Session _29 (2026-04-15)'

idx_start = content.find(START)
if idx_start < 0:
    print("ERROR: multi-rows start not found")
    exit()

idx_session = content.find(END_MARKER, idx_start)
if idx_session < 0:
    print("ERROR: session note not found")
    exit()

# セッション注記の後の </div>\n    </div> を探す
after_session = content[idx_session:]
import re
end_match = re.search(r'</div>\s*\n\s*</div>', after_session)
if not end_match:
    print("ERROR: end tags not found")
    exit()

idx_end = idx_session + end_match.end()
old_block = content[idx_start:idx_end]

print(f"Found block: start={idx_start}, end={idx_end}, length={len(old_block)}")

# ── ベットスリップ HTML 生成 ──────────────────────────────
def dual(ja, en):
    return f'<span class="name-ja">{ja}</span><span class="name-en">{en}</span>'

# レッグHTML生成
def leg_html(emoji, sport_label, match_ja, match_en, rec_ja, rec_en, odds, conf, ev_plus, date, is_addition=False):
    add_badge = '<span style="font-size:9px;background:#0d1f16;color:#3fb950;border:1px solid #238636;border-radius:3px;padding:1px 5px;margin-right:4px;">+追加</span>' if is_addition else ''
    ev_badge = '<span style="font-size:9px;color:#3fb950;font-weight:600;margin-left:3px;">EV+</span>' if ev_plus else '<span style="font-size:9px;color:#8b949e;margin-left:3px;">予測のみ</span>'
    indent = '      '
    return (
        f'{indent}  <div class="ml-card"{"  style=\"opacity:.9;\"" if is_addition else ""}>\n'
        f'{indent}    <span class="ml-sport">{emoji} {sport_label}</span>'
        f'{add_badge}'
        f'<span class="ml-date">{date}</span>\n'
        f'{indent}    <div class="ml-match">{dual(match_ja, match_en)}</div>\n'
        f'{indent}    <div class="ml-rec">\u2192 <strong style="color:#3fb950;">{dual(rec_ja, rec_en)}</strong>'
        f'<span class="ml-odds"> @{odds}</span><span class="ml-conf"> ({conf}%)</span>{ev_badge}</div>\n'
        f'{indent}  </div>'
    )

# 5つのコンボ定義
combos = [
    {
        "rank": "\U0001f947 1\u4f4d", "n_legs": 3,
        "prob": "54.4", "odds": "3.0743", "ev": "+67.1", "ev_pos": True,
        "formula": "0.82\u00d70.85\u00d70.78=0.5437 \u00a0|\u00a0 1.65\u00d71.36\u00d71.37=3.0743 \u00a0|\u00a0 EV=+67.1%",
        "legs": [
            ("\U0001f3c8","UFL Week4","\u30d2\u30e5\u30fc\u30b9\u30c8\u30f3\u30fb\u30ae\u30e3\u30f3\u30d6\u30e9\u30fc\u30ba vs \u30eb\u30a4\u30d3\u30eb\u30fb\u30ad\u30f3\u30b0\u30b9","Houston Gamblers vs Louisville Kings","\u30eb\u30a4\u30d3\u30eb\u30fb\u30ad\u30f3\u30b0\u30b9","Louisville Kings",1.65,82,True,"4/17",False),
            ("\U0001f3c8","UFL Week4","\u30b3\u30ed\u30f3\u30d0\u30b9\u30fb\u30a2\u30d3\u30a8\u30a4\u30bf\u30fc\u30ba @ \u30a2\u30fc\u30ea\u30f3\u30c8\u30f3\u30fb\u30ec\u30cd\u30b2\u30fc\u30ba","Columbus Aviators @ Arlington Renegades","\u30a2\u30fc\u30ea\u30f3\u30c8\u30f3\u30fb\u30ec\u30cd\u30b2\u30fc\u30ba","Arlington Renegades",1.36,85,True,"4/18",False),
            ("\U0001f3be","ATP Barcelona R2","\u30e0\u30c6 C. vs \u30e0\u30bb\u30c3\u30c6\u30a3 L.(2)","Moutet C. vs Musetti L.(2)","\u30e0\u30bb\u30c3\u30c6\u30a3 L.","Musetti L.",1.37,78,True,"4/16",False),
        ],
    },
    {
        "rank": "\U0001f948 2\u4f4d", "n_legs": 4,
        "prob": "47.8", "odds": "3.4124", "ev": "+63.2", "ev_pos": True,
        "formula": "prob=0.4785 \u00a0|\u00a0 odds=3.4124 \u00a0|\u00a0 EV=+63.2%",
        "legs": [
            ("\U0001f3c8","UFL Week4","\u30d2\u30e5\u30fc\u30b9\u30c8\u30f3\u30fb\u30ae\u30e3\u30f3\u30d6\u30e9\u30fc\u30ba vs \u30eb\u30a4\u30d3\u30eb\u30fb\u30ad\u30f3\u30b0\u30b9","Houston Gamblers vs Louisville Kings","\u30eb\u30a4\u30d3\u30eb\u30fb\u30ad\u30f3\u30b0\u30b9","Louisville Kings",1.65,82,True,"4/17",False),
            ("\U0001f3c8","UFL Week4","\u30b3\u30ed\u30f3\u30d0\u30b9\u30fb\u30a2\u30d3\u30a8\u30a4\u30bf\u30fc\u30ba @ \u30a2\u30fc\u30ea\u30f3\u30c8\u30f3\u30fb\u30ec\u30cd\u30b2\u30fc\u30ba","Columbus Aviators @ Arlington Renegades","\u30a2\u30fc\u30ea\u30f3\u30c8\u30f3\u30fb\u30ec\u30cd\u30b2\u30fc\u30ba","Arlington Renegades",1.36,85,True,"4/18",False),
            ("\U0001f3be","ATP Barcelona R2","\u30e0\u30c6 C. vs \u30e0\u30bb\u30c3\u30c6\u30a3 L.(2)","Moutet C. vs Musetti L.(2)","\u30e0\u30bb\u30c3\u30c6\u30a3 L.","Musetti L.",1.37,78,True,"4/16",False),
            ("\U0001f3be","ATP Barcelona R2","\u30a2\u30eb\u30ab\u30e9\u30b9 C. vs \u30de\u30cf\u30c3\u30c1 T.","Alcaraz C. vs Machac T.","\u30a2\u30eb\u30ab\u30e9\u30b9 C.","Alcaraz C.",1.11,88,False,"4/16",True),
        ],
    },
    {
        "rank": "\U0001f949 3\u4f4d", "n_legs": 4,
        "prob": "42.4", "odds": "3.8121", "ev": "+61.7", "ev_pos": True,
        "formula": "prob=0.4241 \u00a0|\u00a0 odds=3.8121 \u00a0|\u00a0 EV=+61.7%",
        "legs": [
            ("\U0001f3c8","UFL Week4","\u30d2\u30e5\u30fc\u30b9\u30c8\u30f3\u30fb\u30ae\u30e3\u30f3\u30d6\u30e9\u30fc\u30ba vs \u30eb\u30a4\u30d3\u30eb\u30fb\u30ad\u30f3\u30b0\u30b9","Houston Gamblers vs Louisville Kings","\u30eb\u30a4\u30d3\u30eb\u30fb\u30ad\u30f3\u30b0\u30b9","Louisville Kings",1.65,82,True,"4/17",False),
            ("\U0001f3c8","UFL Week4","\u30b3\u30ed\u30f3\u30d0\u30b9\u30fb\u30a2\u30d3\u30a8\u30a4\u30bf\u30fc\u30ba @ \u30a2\u30fc\u30ea\u30f3\u30c8\u30f3\u30fb\u30ec\u30cd\u30b2\u30fc\u30ba","Columbus Aviators @ Arlington Renegades","\u30a2\u30fc\u30ea\u30f3\u30c8\u30f3\u30fb\u30ec\u30cd\u30b2\u30fc\u30ba","Arlington Renegades",1.36,85,True,"4/18",False),
            ("\U0001f3be","ATP Barcelona R2","\u30e0\u30c6 C. vs \u30e0\u30bb\u30c3\u30c6\u30a3 L.(2)","Moutet C. vs Musetti L.(2)","\u30e0\u30bb\u30c3\u30c6\u30a3 L.","Musetti L.",1.37,78,True,"4/16",False),
            ("\U0001f3be","WTA Stuttgart R2","\u30bd\u30f3\u30e1\u30ba Z. vs \u30d1\u30aa\u30ea\u30fc\u30cb J.(4)","Sonmez Z. vs Paolini J.(4)","\u30d1\u30aa\u30ea\u30fc\u30cb J.","Paolini J.",1.24,78,True,"4/15",True),
        ],
    },
    {
        "rank": "4\u4f4d", "n_legs": 5,
        "prob": "37.3", "odds": "4.2314", "ev": "+57.9", "ev_pos": True,
        "formula": "prob=0.3732 \u00a0|\u00a0 odds=4.2314 \u00a0|\u00a0 EV=+57.9%",
        "legs": [
            ("\U0001f3c8","UFL Week4","\u30d2\u30e5\u30fc\u30b9\u30c8\u30f3\u30fb\u30ae\u30e3\u30f3\u30d6\u30e9\u30fc\u30ba vs \u30eb\u30a4\u30d3\u30eb\u30fb\u30ad\u30f3\u30b0\u30b9","Houston Gamblers vs Louisville Kings","\u30eb\u30a4\u30d3\u30eb\u30fb\u30ad\u30f3\u30b0\u30b9","Louisville Kings",1.65,82,True,"4/17",False),
            ("\U0001f3c8","UFL Week4","\u30b3\u30ed\u30f3\u30d0\u30b9\u30fb\u30a2\u30d3\u30a8\u30a4\u30bf\u30fc\u30ba @ \u30a2\u30fc\u30ea\u30f3\u30c8\u30f3\u30fb\u30ec\u30cd\u30b2\u30fc\u30ba","Columbus Aviators @ Arlington Renegades","\u30a2\u30fc\u30ea\u30f3\u30c8\u30f3\u30fb\u30ec\u30cd\u30b2\u30fc\u30ba","Arlington Renegades",1.36,85,True,"4/18",False),
            ("\U0001f3be","ATP Barcelona R2","\u30e0\u30c6 C. vs \u30e0\u30bb\u30c3\u30c6\u30a3 L.(2)","Moutet C. vs Musetti L.(2)","\u30e0\u30bb\u30c3\u30c6\u30a3 L.","Musetti L.",1.37,78,True,"4/16",False),
            ("\U0001f3be","ATP Barcelona R2","\u30a2\u30eb\u30ab\u30e9\u30b9 C. vs \u30de\u30cf\u30c3\u30c1 T.","Alcaraz C. vs Machac T.","\u30a2\u30eb\u30ab\u30e9\u30b9 C.","Alcaraz C.",1.11,88,False,"4/16",True),
            ("\U0001f3be","WTA Stuttgart R2","\u30bd\u30f3\u30e1\u30ba Z. vs \u30d1\u30aa\u30ea\u30fc\u30cb J.(4)","Sonmez Z. vs Paolini J.(4)","\u30d1\u30aa\u30ea\u30fc\u30cb J.","Paolini J.",1.24,78,True,"4/15",True),
        ],
    },
    {
        "rank": "5\u4f4d", "n_legs": 4,
        "prob": "50.0", "odds": "3.1358", "ev": "+56.8", "ev_pos": True,
        "formula": "prob=0.5002 \u00a0|\u00a0 odds=3.1358 \u00a0|\u00a0 EV=+56.8%",
        "legs": [
            ("\U0001f3c8","UFL Week4","\u30d2\u30e5\u30fc\u30b9\u30c8\u30f3\u30fb\u30ae\u30e3\u30f3\u30d6\u30e9\u30fc\u30ba vs \u30eb\u30a4\u30d3\u30eb\u30fb\u30ad\u30f3\u30b0\u30b9","Houston Gamblers vs Louisville Kings","\u30eb\u30a4\u30d3\u30eb\u30fb\u30ad\u30f3\u30b0\u30b9","Louisville Kings",1.65,82,True,"4/17",False),
            ("\U0001f3c8","UFL Week4","\u30b3\u30ed\u30f3\u30d0\u30b9\u30fb\u30a2\u30d3\u30a8\u30a4\u30bf\u30fc\u30ba @ \u30a2\u30fc\u30ea\u30f3\u30c8\u30f3\u30fb\u30ec\u30cd\u30b2\u30fc\u30ba","Columbus Aviators @ Arlington Renegades","\u30a2\u30fc\u30ea\u30f3\u30c8\u30f3\u30fb\u30ec\u30cd\u30b2\u30fc\u30ba","Arlington Renegades",1.36,85,True,"4/18",False),
            ("\U0001f3be","ATP Barcelona R2","\u30e0\u30c6 C. vs \u30e0\u30bb\u30c3\u30c6\u30a3 L.(2)","Moutet C. vs Musetti L.(2)","\u30e0\u30bb\u30c3\u30c6\u30a3 L.","Musetti L.",1.37,78,True,"4/16",False),
            ("\U0001f3be","WTA Stuttgart R2","\u30b7\u30d5\u30a3\u30a2\u30c6\u30af I. vs \u30b8\u30fc\u30b2\u30e0\u30f3\u30c8 L.","Swiatek I. vs Siegemund L.","\u30b7\u30d5\u30a3\u30a2\u30c6\u30af I.","Swiatek I.",1.02,92,False,"4/16",True),
        ],
    },
]

def combo_html(c):
    ev_col = "#4ade80" if c["ev_pos"] else "#f85149"
    legs_html = "\n".join([leg_html(*l) for l in c["legs"]])
    return (
        f'      <div class="multi-combo">\n'
        f'        <div class="mc-header">\n'
        f'          <span class="mc-rank">{c["rank"]}</span>\n'
        f'          <span class="mc-legs-count">{c["n_legs"]}\u9023\u8907</span>\n'
        f'          <span class="mc-ev" style="color:{ev_col};">EV <strong>{c["ev"]}%</strong></span>\n'
        f'          <span class="mc-odds">\u30de\u30eb\u30c1\u30aa\u30c3\u30ba: <strong>{c["odds"]}</strong></span>\n'
        f'          <span class="mc-prob">\u5168\u4f53\u52dd\u7387: <strong style="color:{ev_col};">{c["prob"]}%</strong></span>\n'
        f'          <span class="badge badge-pending" style="margin-left:auto;">PENDING</span>\n'
        f'        </div>\n'
        f'        <div class="mc-legs">\n'
        f'{legs_html}\n'
        f'        </div>\n'
        f'        <div class="mc-formula">{c["formula"]}</div>\n'
        f'      </div>'
    )

session_note = (
    '      <div style="font-size:11px;color:var(--text2);text-align:right;padding:4px 2px;">\n'
    '        Session _29 (2026-04-15) &nbsp;|&nbsp; \u51fa\u529bA: 7\u8a66\u5408 &nbsp;|&nbsp; '
    'EV+\u7d44\u307f\u5408\u308f\u305b: 5\u30d1\u30bf\u30fc\u30f3 &nbsp;|&nbsp; '
    '&#x26A0; Musetti conf 82%&#x2192;78% \u4fee\u6b63\u6e08\n'
    '      </div>\n'
    '    </div>'
)

new_rows = "\n".join([combo_html(c) for c in combos]) + "\n" + session_note

# ── CSS 追加 ──────────────────────────────────
css = """
/* ── multi betslip layout ── */
.multi-combo{background:var(--surface);border:1px solid var(--border);border-radius:8px;overflow:hidden;}
.mc-header{display:flex;align-items:center;gap:8px;flex-wrap:wrap;padding:10px 14px;border-bottom:1px solid var(--border);}
.mc-rank{font-weight:700;font-size:14px;color:var(--text);}
.mc-legs-count{font-size:11px;font-weight:600;background:var(--surface2);border:1px solid var(--border);border-radius:10px;padding:1px 8px;color:var(--text2);}
.mc-ev{font-size:13px;}
.mc-odds,.mc-prob{font-size:11px;color:var(--text2);}
.mc-legs{display:flex;flex-direction:column;}
.ml-card{padding:8px 14px;border-bottom:1px solid var(--border);font-size:12px;}
.ml-card:last-child{border-bottom:none;}
.ml-sport{font-size:9px;font-weight:700;text-transform:uppercase;letter-spacing:.06em;color:var(--text2);background:var(--surface2);border-radius:3px;padding:1px 5px;margin-right:4px;}
.ml-date{font-size:9px;color:var(--text2);background:var(--surface2);border-radius:3px;padding:1px 5px;}
.ml-match{color:var(--text2);margin:2px 0 1px;}
.ml-rec{color:var(--text);}
.ml-odds{font-size:11px;color:#e3b341;}
.ml-conf{font-size:10px;color:var(--text2);}
.mc-formula{font-size:10px;color:var(--text2);padding:5px 14px;background:var(--surface2);border-top:1px solid var(--border);}
"""

if '.multi-combo' not in content:
    content = content.replace('</style>', css + '\n</style>', 1)
    print("OK: betslip CSS added")
else:
    print("SKIP: CSS already exists")

# 置換
new_block = START + '\n' + new_rows
content = content[:idx_start] + new_block + content[idx_end:]
print("OK: multi-rows replaced with betslip format")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("dashboard.html saved.")
