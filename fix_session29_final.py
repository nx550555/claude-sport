#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Session _29 Final Update: multi_bets.json + dashboard.html (Output A x7, Output B top5)"""

import json
import re

# ===== 1. records/multi_bets.json 更新 =====
mb_path = r"C:\Users\ohwada\Desktop\claude_sport\records\multi_bets.json"
with open(mb_path, encoding='utf-8-sig') as f:
    mb = json.load(f)

# session_29 を検索して更新
for s in mb['sessions']:
    if s['session_id'] == '_29':
        # Output A: 7件（確実性高い順）
        s['output_a'] = [
            {
                "rank": 1,
                "match": "Swiatek I. vs Siegemund L.",
                "sport": "WTA",
                "tournament": "Porsche Tennis Grand Prix Stuttgart R2",
                "date": "2026-04-16",
                "recommendation": "Swiatek I.",
                "win_prob": 0.92,
                "odds": 1.02,
                "ev": -0.062,
                "reason": "WTA #1 vs Qualifier. cElo差400pt超。Clay最強格。推定勝率92%。EVはマイナスだが予測確実性は最高位。",
                "result": "pending"
            },
            {
                "rank": 2,
                "match": "Alcaraz C. vs Machac T.",
                "sport": "ATP",
                "tournament": "Barcelona Open R2",
                "date": "2026-04-16",
                "recommendation": "Alcaraz C.",
                "win_prob": 0.88,
                "odds": 1.11,
                "ev": -0.023,
                "reason": "ATP #3 Clay specialist vs 世界66位。cElo差300pt超。Barcelona地元。推定勝率88%。",
                "result": "pending"
            },
            {
                "rank": 3,
                "match": "Columbus Aviators @ Arlington Renegades",
                "sport": "UFL",
                "tournament": "UFL Week 4",
                "date": "2026-04-18",
                "recommendation": "Arlington Renegades",
                "win_prob": 0.85,
                "odds": 1.36,
                "ev": 0.156,
                "reason": "Renegades 3-0 vs Aviators 0-3。DIFF/G差。Austin Reed QB確認済。ホーム優位+4%。Week4閾値80%超。",
                "result": "pending"
            },
            {
                "rank": 4,
                "match": "Houston Gamblers vs Louisville Kings",
                "sport": "UFL",
                "tournament": "UFL Week 4",
                "date": "2026-04-17",
                "recommendation": "Louisville Kings",
                "win_prob": 0.82,
                "odds": 1.65,
                "ev": 0.353,
                "reason": "Louisville 3-0 vs Gamblers 0-3。DIFF/G差8点超。OLine格差。Week4閾値80%超。EV+35.3%。",
                "result": "pending"
            },
            {
                "rank": 5,
                "match": "Moutet C. vs Musetti L.",
                "sport": "ATP",
                "tournament": "Barcelona Open R2",
                "date": "2026-04-16",
                "recommendation": "Musetti L.",
                "win_prob": 0.82,
                "odds": 1.37,
                "ev": 0.123,
                "reason": "cElo差200pt超。Musetti Clay巧者。推定勝率82%。EV+12.3%。両閾値クリア。",
                "result": "pending"
            },
            {
                "rank": 6,
                "match": "Samsonova L. vs Gauff C.",
                "sport": "WTA",
                "tournament": "Porsche Tennis Grand Prix Stuttgart R2",
                "date": "2026-04-16",
                "recommendation": "Gauff C.",
                "win_prob": 0.81,
                "odds": 1.15,
                "ev": -0.067,
                "reason": "WTA #3 vs 世界10位前後。Gauff Clay成績良好。推定勝率81%。EVマイナスだが予測確実性高い。",
                "result": "pending"
            },
            {
                "rank": 7,
                "match": "Sonmez Z. vs Paolini J.",
                "sport": "WTA",
                "tournament": "Porsche Tennis Grand Prix Stuttgart R2",
                "date": "2026-04-15",
                "recommendation": "Paolini J.",
                "win_prob": 0.78,
                "odds": 1.24,
                "ev": 0.054,
                "reason": "cElo差300pt（Paolini 1916 vs Sonmez 1616）。推定勝率78%。EV+5.4%。両閾値クリア。",
                "result": "pending"
            }
        ]

        # Output B: top5 EV+ コンボ
        # EV+試合: Louisville(ev_factor=1.353), Renegades(1.156), Musetti(1.123)
        # EV-試合: Alcaraz(0.977), Paolini(0.967), Swiatek(0.938), Gauff(0.932)
        # 追加するほどEVが下がるため、EV+3試合コアが最高
        s['output_b'] = [
            {
                "rank": 1,
                "label": "Louisville x Renegades x Musetti",
                "matches": ["Louisville Kings", "Arlington Renegades", "Musetti L."],
                "match_details": [
                    "Houston Gamblers vs Louisville Kings (UFL W4)",
                    "Columbus Aviators @ Arlington Renegades (UFL W4)",
                    "Moutet C. vs Musetti L. (Barcelona R2)"
                ],
                "count": 3,
                "total_win_prob": round(0.82 * 0.85 * 0.82, 4),
                "multi_odds": round(1.65 * 1.36 * 1.37, 4),
                "multi_ev": round(0.82 * 0.85 * 0.82 * 1.65 * 1.36 * 1.37 - 1, 4),
                "calc_note": "0.82x0.85x0.82=0.5715 | 1.65x1.36x1.37=3.0743 | EV=0.5715x3.0743-1=+75.8%",
                "result": "pending"
            },
            {
                "rank": 2,
                "label": "Louisville x Renegades x Musetti x Alcaraz",
                "matches": ["Louisville Kings", "Arlington Renegades", "Musetti L.", "Alcaraz C."],
                "match_details": [
                    "Houston Gamblers vs Louisville Kings (UFL W4)",
                    "Columbus Aviators @ Arlington Renegades (UFL W4)",
                    "Moutet C. vs Musetti L. (Barcelona R2)",
                    "Alcaraz C. vs Machac T. (Barcelona R2)"
                ],
                "count": 4,
                "total_win_prob": round(0.82 * 0.85 * 0.82 * 0.88, 4),
                "multi_odds": round(1.65 * 1.36 * 1.37 * 1.11, 4),
                "multi_ev": round(0.82 * 0.85 * 0.82 * 0.88 * 1.65 * 1.36 * 1.37 * 1.11 - 1, 4),
                "calc_note": "prob=0.5030 | odds=3.4124 | EV=0.5030x3.4124-1=+71.6%",
                "result": "pending"
            },
            {
                "rank": 3,
                "label": "Louisville x Renegades x Musetti x Paolini",
                "matches": ["Louisville Kings", "Arlington Renegades", "Musetti L.", "Paolini J."],
                "match_details": [
                    "Houston Gamblers vs Louisville Kings (UFL W4)",
                    "Columbus Aviators @ Arlington Renegades (UFL W4)",
                    "Moutet C. vs Musetti L. (Barcelona R2)",
                    "Sonmez Z. vs Paolini J. (WTA Stuttgart R2)"
                ],
                "count": 4,
                "total_win_prob": round(0.82 * 0.85 * 0.82 * 0.78, 4),
                "multi_odds": round(1.65 * 1.36 * 1.37 * 1.24, 4),
                "multi_ev": round(0.82 * 0.85 * 0.82 * 0.78 * 1.65 * 1.36 * 1.37 * 1.24 - 1, 4),
                "calc_note": "prob=0.4458 | odds=3.8121 | EV=0.4458x3.8121-1=+70.0%",
                "result": "pending"
            },
            {
                "rank": 4,
                "label": "Louisville x Renegades x Musetti x Alcaraz x Paolini",
                "matches": ["Louisville Kings", "Arlington Renegades", "Musetti L.", "Alcaraz C.", "Paolini J."],
                "match_details": [
                    "Houston Gamblers vs Louisville Kings (UFL W4)",
                    "Columbus Aviators @ Arlington Renegades (UFL W4)",
                    "Moutet C. vs Musetti L. (Barcelona R2)",
                    "Alcaraz C. vs Machac T. (Barcelona R2)",
                    "Sonmez Z. vs Paolini J. (WTA Stuttgart R2)"
                ],
                "count": 5,
                "total_win_prob": round(0.82 * 0.85 * 0.82 * 0.88 * 0.78, 4),
                "multi_odds": round(1.65 * 1.36 * 1.37 * 1.11 * 1.24, 4),
                "multi_ev": round(0.82 * 0.85 * 0.82 * 0.88 * 0.78 * 1.65 * 1.36 * 1.37 * 1.11 * 1.24 - 1, 4),
                "calc_note": "prob=0.3923 | odds=4.2311 | EV=0.3923x4.2311-1=+66.0%",
                "result": "pending"
            },
            {
                "rank": 5,
                "label": "Louisville x Renegades x Musetti x Swiatek",
                "matches": ["Louisville Kings", "Arlington Renegades", "Musetti L.", "Swiatek I."],
                "match_details": [
                    "Houston Gamblers vs Louisville Kings (UFL W4)",
                    "Columbus Aviators @ Arlington Renegades (UFL W4)",
                    "Moutet C. vs Musetti L. (Barcelona R2)",
                    "Swiatek I. vs Siegemund L. (WTA Stuttgart R2)"
                ],
                "count": 4,
                "total_win_prob": round(0.82 * 0.85 * 0.82 * 0.92, 4),
                "multi_odds": round(1.65 * 1.36 * 1.37 * 1.02, 4),
                "multi_ev": round(0.82 * 0.85 * 0.82 * 0.92 * 1.65 * 1.36 * 1.37 * 1.02 - 1, 4),
                "calc_note": "prob=0.5258 | odds=3.1358 | EV=0.5258x3.1358-1=+64.9%",
                "result": "pending"
            }
        ]

        s['output_b_calc_note'] = (
            "EV+試合: Louisville(0.82x1.65=1.353) / Renegades(0.85x1.36=1.156) / Musetti(0.82x1.37=1.123). "
            "EV-試合: Alcaraz(0.88x1.11=0.977) / Paolini(0.78x1.24=0.967) / Swiatek(0.92x1.02=0.938) / Gauff(0.81x1.15=0.932). "
            "EV+3試合コア(+75.8%)が最高。以下は追加EV-試合でEV漸減。"
        )
        print("multi_bets.json session_29 updated: Output A x7, Output B top5")
        break

with open(mb_path, 'w', encoding='utf-8') as f:
    json.dump(mb, f, ensure_ascii=False, indent=2)
print("records/multi_bets.json: saved")


# ===== 2. dashboard.html 更新 =====
html_path = r"C:\Users\ohwada\Desktop\claude_sport\dashboard.html"
with open(html_path, encoding='utf-8') as f:
    html = f.read()

# --- highprob-rows の置換 ---
old_highprob = '''        <tbody id="highprob-rows">
          <tr>
            <td style="text-align:center;font-weight:700;color:var(--text);">1</td>
            <td style="font-weight:600;">Columbus Aviators @<br><strong>Arlington Renegades</strong></td>
            <td>UFL W4<br><span style="font-size:10px;color:var(--text2);">2026-04-18</span></td>
            <td><span class="badge badge-go">Renegades</span></td>
            <td style="text-align:center;font-weight:700;color:#4ade80;">85%</td>
            <td style="text-align:center;">@1.36</td>
            <td style="font-size:11px;color:var(--text2);">Renegades 3-0 vs Aviators 0-3。DIFF/G差。Austin Reed QB確認済。ホーム優位+4%。</td>
            <td><span class="badge badge-pending">PENDING</span></td>
          </tr>
          <tr>
            <td style="text-align:center;font-weight:700;color:var(--text);">2</td>
            <td style="font-weight:600;">Sonmez Z. vs<br><strong>Paolini J.(4)</strong></td>
            <td>WTA Stuttgart R2<br><span style="font-size:10px;color:var(--text2);">2026-04-15</span></td>
            <td><span class="badge badge-go">Paolini</span></td>
            <td style="text-align:center;font-weight:700;color:#4ade80;">78%</td>
            <td style="text-align:center;">@1.24</td>
            <td style="font-size:11px;color:var(--text2);">cElo差300pt（Paolini 1916 vs Sonmez 1616）。推定勝率78%。EV+5.4%。</td>
            <td><span class="badge badge-pending">PENDING</span></td>
          </tr>
        </tbody>'''

new_highprob = '''        <tbody id="highprob-rows">
          <tr>
            <td style="text-align:center;font-weight:700;color:var(--text);">1</td>
            <td style="font-weight:600;">Swiatek I. vs<br><strong>Siegemund L.</strong></td>
            <td>WTA Stuttgart R2<br><span style="font-size:10px;color:var(--text2);">2026-04-16</span></td>
            <td><span class="badge badge-go">Swiatek</span></td>
            <td style="text-align:center;font-weight:700;color:#4ade80;">92%</td>
            <td style="text-align:center;">@1.02</td>
            <td style="font-size:11px;color:var(--text2);">WTA #1 vs Qualifier。cElo差400pt超。Clay最強格。予測確実性最高位。</td>
            <td><span class="badge badge-pending">PENDING</span></td>
          </tr>
          <tr>
            <td style="text-align:center;font-weight:700;color:var(--text);">2</td>
            <td style="font-weight:600;">Alcaraz C. vs<br><strong>Machac T.</strong></td>
            <td>ATP Barcelona R2<br><span style="font-size:10px;color:var(--text2);">2026-04-16</span></td>
            <td><span class="badge badge-go">Alcaraz</span></td>
            <td style="text-align:center;font-weight:700;color:#4ade80;">88%</td>
            <td style="text-align:center;">@1.11</td>
            <td style="font-size:11px;color:var(--text2);">ATP #3 Clay specialist vs 世界66位。cElo差300pt超。Barcelona地元。</td>
            <td><span class="badge badge-pending">PENDING</span></td>
          </tr>
          <tr>
            <td style="text-align:center;font-weight:700;color:var(--text);">3</td>
            <td style="font-weight:600;">Columbus Aviators @<br><strong>Arlington Renegades</strong></td>
            <td>UFL W4<br><span style="font-size:10px;color:var(--text2);">2026-04-18</span></td>
            <td><span class="badge badge-go">Renegades</span></td>
            <td style="text-align:center;font-weight:700;color:#4ade80;">85%</td>
            <td style="text-align:center;">@1.36</td>
            <td style="font-size:11px;color:var(--text2);">Renegades 3-0 vs Aviators 0-3。DIFF/G差。Austin Reed QB確認済。ホーム優位+4%。</td>
            <td><span class="badge badge-pending">PENDING</span></td>
          </tr>
          <tr>
            <td style="text-align:center;font-weight:700;color:var(--text);">4</td>
            <td style="font-weight:600;">Houston Gamblers vs<br><strong>Louisville Kings</strong></td>
            <td>UFL W4<br><span style="font-size:10px;color:var(--text2);">2026-04-17</span></td>
            <td><span class="badge badge-go">Louisville</span></td>
            <td style="text-align:center;font-weight:700;color:#4ade80;">82%</td>
            <td style="text-align:center;">@1.65</td>
            <td style="font-size:11px;color:var(--text2);">Louisville 3-0 vs Gamblers 0-3。DIFF/G差8点超。OLine格差。EV+35.3%。</td>
            <td><span class="badge badge-pending">PENDING</span></td>
          </tr>
          <tr>
            <td style="text-align:center;font-weight:700;color:var(--text);">5</td>
            <td style="font-weight:600;">Moutet C. vs<br><strong>Musetti L.</strong></td>
            <td>ATP Barcelona R2<br><span style="font-size:10px;color:var(--text2);">2026-04-16</span></td>
            <td><span class="badge badge-go">Musetti</span></td>
            <td style="text-align:center;font-weight:700;color:#4ade80;">82%</td>
            <td style="text-align:center;">@1.37</td>
            <td style="font-size:11px;color:var(--text2);">cElo差200pt超。Musetti Clay巧者。推定勝率82%。EV+12.3%。</td>
            <td><span class="badge badge-pending">PENDING</span></td>
          </tr>
          <tr>
            <td style="text-align:center;font-weight:700;color:var(--text);">6</td>
            <td style="font-weight:600;">Samsonova L. vs<br><strong>Gauff C.</strong></td>
            <td>WTA Stuttgart R2<br><span style="font-size:10px;color:var(--text2);">2026-04-16</span></td>
            <td><span class="badge badge-go">Gauff</span></td>
            <td style="text-align:center;font-weight:700;color:#4ade80;">81%</td>
            <td style="text-align:center;">@1.15</td>
            <td style="font-size:11px;color:var(--text2);">WTA #3 vs 世界10位前後。Gauff Clay成績良好。推定勝率81%。</td>
            <td><span class="badge badge-pending">PENDING</span></td>
          </tr>
          <tr>
            <td style="text-align:center;font-weight:700;color:var(--text);">7</td>
            <td style="font-weight:600;">Sonmez Z. vs<br><strong>Paolini J.(4)</strong></td>
            <td>WTA Stuttgart R2<br><span style="font-size:10px;color:var(--text2);">2026-04-15</span></td>
            <td><span class="badge badge-go">Paolini</span></td>
            <td style="text-align:center;font-weight:700;color:#4ade80;">78%</td>
            <td style="text-align:center;">@1.24</td>
            <td style="font-size:11px;color:var(--text2);">cElo差300pt（Paolini 1916 vs Sonmez 1616）。推定勝率78%。EV+5.4%。</td>
            <td><span class="badge badge-pending">PENDING</span></td>
          </tr>
        </tbody>'''

if old_highprob in html:
    html = html.replace(old_highprob, new_highprob)
    print("highprob-rows: updated (2->7 rows)")
else:
    print("ERROR: highprob-rows anchor not found")

# --- multi-rows の置換 ---
old_multi = '''    <div id="multi-rows" style="display:flex;flex-direction:column;gap:12px;">
      <div style="background:var(--surface);border:1px solid var(--border);border-radius:8px;padding:16px;">
        <div style="display:flex;align-items:center;gap:8px;margin-bottom:10px;">
          <span style="font-weight:700;font-size:15px;color:var(--text);">&#x1F947; 1位</span>
          <span style="font-size:13px;color:var(--text2);">Renegades &times; Paolini（2試合）</span>
          <span class="badge badge-pending" style="margin-left:auto;">PENDING</span>
        </div>
        <div style="font-size:12px;color:var(--text2);margin-bottom:8px;">
          Columbus Aviators @ <strong>Arlington Renegades</strong> (UFL W4) &times; Sonmez vs <strong>Paolini</strong> (WTA Stuttgart R2)
        </div>
        <div style="display:flex;gap:16px;flex-wrap:wrap;font-size:12px;">
          <span>全体推定勝率: <strong style="color:#4ade80;">66.3%</strong></span>
          <span>マルチオッズ: <strong>1.6864</strong></span>
          <span>マルチEV: <strong style="color:#4ade80;">+11.8%</strong></span>
        </div>
        <div style="font-size:10px;color:var(--text2);margin-top:6px;">
          計算: 0.85 &times; 0.78 = 0.663 &nbsp;|&nbsp; 1.36 &times; 1.24 = 1.686 &nbsp;|&nbsp; EV = 0.663 &times; 1.686 &minus; 1 = +11.8%
        </div>
      </div>
      <div style="font-size:11px;color:var(--text2);text-align:right;">
        Session _29 (2026-04-15) &nbsp;|&nbsp; 出力A: 2試合 &nbsp;|&nbsp; EV+組み合わせ: 1パターン
      </div>
    </div>'''

new_multi = '''    <div id="multi-rows" style="display:flex;flex-direction:column;gap:12px;">
      <div style="background:var(--surface);border:1px solid var(--border);border-radius:8px;padding:16px;">
        <div style="display:flex;align-items:center;gap:8px;margin-bottom:10px;">
          <span style="font-weight:700;font-size:15px;color:var(--text);">&#x1F947; 1位</span>
          <span style="font-size:13px;color:var(--text2);">Louisville &times; Renegades &times; Musetti（3試合）</span>
          <span class="badge badge-pending" style="margin-left:auto;">PENDING</span>
        </div>
        <div style="font-size:12px;color:var(--text2);margin-bottom:8px;">
          Houston vs <strong>Louisville Kings</strong> (UFL W4) &times; Aviators @ <strong>Renegades</strong> (UFL W4) &times; Moutet vs <strong>Musetti</strong> (Barcelona R2)
        </div>
        <div style="display:flex;gap:16px;flex-wrap:wrap;font-size:12px;">
          <span>全体推定勝率: <strong style="color:#4ade80;">57.2%</strong></span>
          <span>マルチオッズ: <strong>3.0743</strong></span>
          <span>マルチEV: <strong style="color:#4ade80;">+75.8%</strong></span>
        </div>
        <div style="font-size:10px;color:var(--text2);margin-top:6px;">
          0.82&times;0.85&times;0.82=0.5715 &nbsp;|&nbsp; 1.65&times;1.36&times;1.37=3.0743 &nbsp;|&nbsp; EV=0.5715&times;3.0743&minus;1=+75.8%
        </div>
      </div>
      <div style="background:var(--surface);border:1px solid var(--border);border-radius:8px;padding:16px;">
        <div style="display:flex;align-items:center;gap:8px;margin-bottom:10px;">
          <span style="font-weight:700;font-size:15px;color:var(--text);">&#x1F948; 2位</span>
          <span style="font-size:13px;color:var(--text2);">Louisville &times; Renegades &times; Musetti &times; Alcaraz（4試合）</span>
          <span class="badge badge-pending" style="margin-left:auto;">PENDING</span>
        </div>
        <div style="font-size:12px;color:var(--text2);margin-bottom:8px;">
          +<strong>Alcaraz</strong> (Barcelona R2) 追加
        </div>
        <div style="display:flex;gap:16px;flex-wrap:wrap;font-size:12px;">
          <span>全体推定勝率: <strong style="color:#4ade80;">50.3%</strong></span>
          <span>マルチオッズ: <strong>3.4124</strong></span>
          <span>マルチEV: <strong style="color:#4ade80;">+71.6%</strong></span>
        </div>
        <div style="font-size:10px;color:var(--text2);margin-top:6px;">
          prob=0.5715&times;0.88=0.5030 &nbsp;|&nbsp; odds=3.0743&times;1.11=3.4124 &nbsp;|&nbsp; EV=+71.6%
        </div>
      </div>
      <div style="background:var(--surface);border:1px solid var(--border);border-radius:8px;padding:16px;">
        <div style="display:flex;align-items:center;gap:8px;margin-bottom:10px;">
          <span style="font-weight:700;font-size:15px;color:var(--text);">&#x1F949; 3位</span>
          <span style="font-size:13px;color:var(--text2);">Louisville &times; Renegades &times; Musetti &times; Paolini（4試合）</span>
          <span class="badge badge-pending" style="margin-left:auto;">PENDING</span>
        </div>
        <div style="font-size:12px;color:var(--text2);margin-bottom:8px;">
          +<strong>Paolini</strong> (WTA Stuttgart R2) 追加
        </div>
        <div style="display:flex;gap:16px;flex-wrap:wrap;font-size:12px;">
          <span>全体推定勝率: <strong style="color:#4ade80;">44.6%</strong></span>
          <span>マルチオッズ: <strong>3.8121</strong></span>
          <span>マルチEV: <strong style="color:#4ade80;">+70.0%</strong></span>
        </div>
        <div style="font-size:10px;color:var(--text2);margin-top:6px;">
          prob=0.5715&times;0.78=0.4458 &nbsp;|&nbsp; odds=3.0743&times;1.24=3.8121 &nbsp;|&nbsp; EV=+70.0%
        </div>
      </div>
      <div style="background:var(--surface);border:1px solid var(--border);border-radius:8px;padding:16px;">
        <div style="display:flex;align-items:center;gap:8px;margin-bottom:10px;">
          <span style="font-weight:700;font-size:15px;color:var(--text);">4位</span>
          <span style="font-size:13px;color:var(--text2);">Louisville &times; Renegades &times; Musetti &times; Alcaraz &times; Paolini（5試合）</span>
          <span class="badge badge-pending" style="margin-left:auto;">PENDING</span>
        </div>
        <div style="font-size:12px;color:var(--text2);margin-bottom:8px;">
          +<strong>Alcaraz</strong> &amp; <strong>Paolini</strong> 追加（5連複）
        </div>
        <div style="display:flex;gap:16px;flex-wrap:wrap;font-size:12px;">
          <span>全体推定勝率: <strong style="color:#4ade80;">39.2%</strong></span>
          <span>マルチオッズ: <strong>4.2311</strong></span>
          <span>マルチEV: <strong style="color:#4ade80;">+66.0%</strong></span>
        </div>
        <div style="font-size:10px;color:var(--text2);margin-top:6px;">
          prob=0.5030&times;0.78=0.3923 &nbsp;|&nbsp; odds=3.4124&times;1.24=4.2314 &nbsp;|&nbsp; EV=+66.0%
        </div>
      </div>
      <div style="background:var(--surface);border:1px solid var(--border);border-radius:8px;padding:16px;">
        <div style="display:flex;align-items:center;gap:8px;margin-bottom:10px;">
          <span style="font-weight:700;font-size:15px;color:var(--text);">5位</span>
          <span style="font-size:13px;color:var(--text2);">Louisville &times; Renegades &times; Musetti &times; Swiatek（4試合）</span>
          <span class="badge badge-pending" style="margin-left:auto;">PENDING</span>
        </div>
        <div style="font-size:12px;color:var(--text2);margin-bottom:8px;">
          +<strong>Swiatek</strong> (WTA Stuttgart R2) 追加
        </div>
        <div style="display:flex;gap:16px;flex-wrap:wrap;font-size:12px;">
          <span>全体推定勝率: <strong style="color:#4ade80;">52.6%</strong></span>
          <span>マルチオッズ: <strong>3.1358</strong></span>
          <span>マルチEV: <strong style="color:#4ade80;">+64.9%</strong></span>
        </div>
        <div style="font-size:10px;color:var(--text2);margin-top:6px;">
          prob=0.5715&times;0.92=0.5258 &nbsp;|&nbsp; odds=3.0743&times;1.02=3.1358 &nbsp;|&nbsp; EV=+64.9%
        </div>
      </div>
      <div style="font-size:11px;color:var(--text2);text-align:right;">
        Session _29 (2026-04-15) &nbsp;|&nbsp; 出力A: 7試合 &nbsp;|&nbsp; EV+組み合わせ: 5パターン
      </div>
    </div>'''

if old_multi in html:
    html = html.replace(old_multi, new_multi)
    print("multi-rows: updated (1->5 combos)")
else:
    print("ERROR: multi-rows anchor not found")

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)
print("dashboard.html: saved")
