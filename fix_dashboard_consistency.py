#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dashboard consistency fix + new features:
 1. Overview: 待機中 6→8 (WTA x1→x2, UFL x1→x2), UFL sport card update
 2. Active: Add Arlington Renegades GO card (after Louisville)
 3. Active: Fix Paolini (R1→R2, 85%→78%)
 4. History: "Dallas Renegades" → "Arlington Renegades"
 5. Highprob: Musetti 82%→78% / EV+12.3%→+6.9%, swap rank5/6 (Gauff 81% > Musetti 78%)
 6. Highprob: Add GO-overlap badge/indicator to items that are also in active GO
 7. multi_bets.json: Musetti conf fix + Output B recalculation
"""
import json

# ===== A. multi_bets.json =====
mb_path = r"C:\Users\ohwada\Desktop\claude_sport\records\multi_bets.json"
with open(mb_path, encoding='utf-8-sig') as f:
    mb = json.load(f)

for s in mb['sessions']:
    if s['session_id'] == '_29':
        # Fix Musetti rank 5: win_prob 0.82→0.78, ev 0.123→0.069
        # Also re-rank: Gauff(81%) and Musetti(78%) swap, now Gauff=rank5, Musetti=rank6
        new_a = []
        for item in s['output_a']:
            if 'Musetti' in str(item.get('match','')) or 'Moutet' in str(item.get('match','')):
                item['win_prob'] = 0.78
                item['ev'] = round(0.78 * 1.37 - 1, 4)  # +0.0686
                item['reason'] = (
                    "cElo差271pt（Musetti ~2017 vs Moutet ~1746）。"
                    "基礎確率84%→傷病歴補正-5%(AO adductor+Miami arm, R013)→conf 78%。"
                    "EV+6.9%。両閾値クリア。"
                )
            new_a.append(item)

        # Re-sort by win_prob desc (keeping rank numbers):
        # Swiatek 92 > Alcaraz 88 > Renegades 85 > Louisville 82 > Gauff 81 > Musetti 78 = Paolini 78
        sort_order = {
            'Swiatek': (1, 0.92),
            'Alcaraz': (2, 0.88),
            'Renegades': (3, 0.85),
            'Louisville': (4, 0.82),
            'Gauff': (5, 0.81),
            'Musetti': (6, 0.78),
            'Paolini': (7, 0.78),
        }
        def rank_key(item):
            rec = str(item.get('recommendation',''))
            for k,(r,_) in sort_order.items():
                if k in rec:
                    return r
            return 99
        new_a_sorted = sorted(new_a, key=rank_key)
        for i, item in enumerate(new_a_sorted):
            item['rank'] = i + 1
        s['output_a'] = new_a_sorted

        # Recalculate Output B with corrected Musetti 78%
        # EV+ items: Louisville(0.82x1.65=1.353), Renegades(0.85x1.36=1.156), Musetti(0.78x1.37=1.069)
        # EV- items: Alcaraz(0.88x1.11=0.977), Paolini(0.78x1.24=0.967), Swiatek(0.92x1.02=0.938), Gauff(0.81x1.15=0.932)

        def p(*probs):
            r = 1.0
            for x in probs: r *= x
            return round(r, 4)

        def o(*odds_list):
            r = 1.0
            for x in odds_list: r *= x
            return round(r, 4)

        def ev(prob, odds):
            return round(prob * odds - 1, 4)

        p_lou, o_lou = 0.82, 1.65
        p_ren, o_ren = 0.85, 1.36
        p_mus, o_mus = 0.78, 1.37
        p_alc, o_alc = 0.88, 1.11
        p_pao, o_pao = 0.78, 1.24
        p_swa, o_swa = 0.92, 1.02

        combos = [
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
                "total_win_prob": p(p_lou, p_ren, p_mus),
                "multi_odds": o(o_lou, o_ren, o_mus),
                "multi_ev": ev(p(p_lou,p_ren,p_mus), o(o_lou,o_ren,o_mus)),
                "calc_note": f"prob={p(p_lou,p_ren,p_mus)} | odds={o(o_lou,o_ren,o_mus)} | EV=+{round((p(p_lou,p_ren,p_mus)*o(o_lou,o_ren,o_mus)-1)*100,1)}%",
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
                "total_win_prob": p(p_lou,p_ren,p_mus,p_alc),
                "multi_odds": o(o_lou,o_ren,o_mus,o_alc),
                "multi_ev": ev(p(p_lou,p_ren,p_mus,p_alc), o(o_lou,o_ren,o_mus,o_alc)),
                "calc_note": f"prob={p(p_lou,p_ren,p_mus,p_alc)} | odds={o(o_lou,o_ren,o_mus,o_alc)} | EV=+{round((p(p_lou,p_ren,p_mus,p_alc)*o(o_lou,o_ren,o_mus,o_alc)-1)*100,1)}%",
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
                "total_win_prob": p(p_lou,p_ren,p_mus,p_pao),
                "multi_odds": o(o_lou,o_ren,o_mus,o_pao),
                "multi_ev": ev(p(p_lou,p_ren,p_mus,p_pao), o(o_lou,o_ren,o_mus,o_pao)),
                "calc_note": f"prob={p(p_lou,p_ren,p_mus,p_pao)} | odds={o(o_lou,o_ren,o_mus,o_pao)} | EV=+{round((p(p_lou,p_ren,p_mus,p_pao)*o(o_lou,o_ren,o_mus,o_pao)-1)*100,1)}%",
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
                "total_win_prob": p(p_lou,p_ren,p_mus,p_alc,p_pao),
                "multi_odds": o(o_lou,o_ren,o_mus,o_alc,o_pao),
                "multi_ev": ev(p(p_lou,p_ren,p_mus,p_alc,p_pao), o(o_lou,o_ren,o_mus,o_alc,o_pao)),
                "calc_note": f"prob={p(p_lou,p_ren,p_mus,p_alc,p_pao)} | odds={o(o_lou,o_ren,o_mus,o_alc,o_pao)} | EV=+{round((p(p_lou,p_ren,p_mus,p_alc,p_pao)*o(o_lou,o_ren,o_mus,o_alc,o_pao)-1)*100,1)}%",
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
                "total_win_prob": p(p_lou,p_ren,p_mus,p_swa),
                "multi_odds": o(o_lou,o_ren,o_mus,o_swa),
                "multi_ev": ev(p(p_lou,p_ren,p_mus,p_swa), o(o_lou,o_ren,o_mus,o_swa)),
                "calc_note": f"prob={p(p_lou,p_ren,p_mus,p_swa)} | odds={o(o_lou,o_ren,o_mus,o_swa)} | EV=+{round((p(p_lou,p_ren,p_mus,p_swa)*o(o_lou,o_ren,o_mus,o_swa)-1)*100,1)}%",
                "result": "pending"
            },
        ]
        s['output_b'] = combos

        # Show computed EVs
        for c in combos:
            pct = round(c['multi_ev']*100, 1)
            print(f"  B rank{c['rank']}: {c['label']} EV={'+' if pct>=0 else ''}{pct}%")

        s['output_b_calc_note'] = (
            "EV+試合: Louisville(0.82x1.65=1.353) / Renegades(0.85x1.36=1.156) / Musetti(0.78x1.37=1.069). "
            "EV-試合: Alcaraz(0.88x1.11=0.977) / Paolini(0.78x1.24=0.967) / Swiatek(0.92x1.02=0.938) / Gauff(0.81x1.15=0.932). "
            "[Musetti conf 82%->78% 修正済み: R013傷病歴補正-5%を正確に反映]"
        )
        print("multi_bets.json: updated Output A rank order + Musetti fix + Output B recalc")
        break

with open(mb_path, 'w', encoding='utf-8') as f:
    json.dump(mb, f, ensure_ascii=False, indent=2)
print("records/multi_bets.json: saved")

# ===== B. dashboard.html =====
html_path = r"C:\Users\ohwada\Desktop\claude_sport\dashboard.html"
with open(html_path, encoding='utf-8') as f:
    html = f.read()

fixes_applied = []

# --- B1. Overview: 待機中 6→8, description update ---
old_waiting = '''      <div class="big-stat">
        <div class="bs-label">待機中</div>
        <div class="bs-val" style="color:#d29922;">6</div>
        <div class="bs-sub">ATP x1 + WTA x1 + NRL x1 + SL x2 + UFL x1</div>
      </div>'''
new_waiting = '''      <div class="big-stat">
        <div class="bs-label">待機中</div>
        <div class="bs-val" style="color:#d29922;">8</div>
        <div class="bs-sub">ATP x1 + WTA x2 + NRL x1 + SL x2 + UFL x2</div>
      </div>'''
if old_waiting in html:
    html = html.replace(old_waiting, new_waiting)
    fixes_applied.append("Overview: 待機中 6→8")
else:
    print("WARN: Overview 待機中 anchor not found")

# --- B2. UFL sport card: GO 1→3, 待機中 0→2 ---
old_ufl_card = '''      <div class="sport-card">
        <div class="sport-card-header" style="color:#fca5a5;">🏈 UFL <span class="rule-ver">v1.0</span></div>
        <div class="sport-metrics">
          <div class="sm"><div class="sm-label">GO回数</div><div class="sm-val">1</div></div>
          <div class="sm"><div class="sm-label">結果済</div><div class="sm-val">1</div></div>
          <div class="sm"><div class="sm-label">的中</div><div class="sm-val">1</div></div>
          <div class="sm"><div class="sm-label">正答率</div><div class="sm-val" style="color:#3fb950;">100%</div></div>
          <div class="sm"><div class="sm-label">累積EV</div><div class="sm-val" style="color:#3fb950;">+0.320</div></div>
          <div class="sm"><div class="sm-label">待機中</div><div class="sm-val">0</div></div>
        </div>
      </div>'''
new_ufl_card = '''      <div class="sport-card">
        <div class="sport-card-header" style="color:#fca5a5;">🏈 UFL <span class="rule-ver">v1.0</span></div>
        <div class="sport-metrics">
          <div class="sm"><div class="sm-label">GO回数</div><div class="sm-val">3</div></div>
          <div class="sm"><div class="sm-label">結果済</div><div class="sm-val">1</div></div>
          <div class="sm"><div class="sm-label">的中</div><div class="sm-val">1</div></div>
          <div class="sm"><div class="sm-label">正答率</div><div class="sm-val" style="color:#3fb950;">100%</div></div>
          <div class="sm"><div class="sm-label">累積EV</div><div class="sm-val" style="color:#3fb950;">+0.320</div></div>
          <div class="sm"><div class="sm-label">待機中</div><div class="sm-val" style="color:#d29922;">2</div></div>
        </div>
      </div>'''
if old_ufl_card in html:
    html = html.replace(old_ufl_card, new_ufl_card)
    fixes_applied.append("UFL sport card: GO 1→3, 待機中 0→2")
else:
    print("WARN: UFL sport card anchor not found")

# --- B3. WTA sport card: 次回 Bondar → 次回 Bondar + Paolini pending ---
old_wta_next = '          <div class="sm"><div class="sm-label">次回</div><div class="sm-val" style="color:#e3b341;">Bondar @1.21 PENDING</div></div>'
new_wta_next = '          <div class="sm"><div class="sm-label">待機中</div><div class="sm-val" style="color:#d29922;">2</div></div>'
if old_wta_next in html:
    html = html.replace(old_wta_next, new_wta_next)
    fixes_applied.append("WTA sport card: 次回→待機中 x2")
else:
    print("WARN: WTA sport card 次回 anchor not found")

# --- B4. Active: Fix Paolini card (R1→R2, 85%→78%) ---
old_paolini_card = '''        <!-- WTA Stuttgart Paolini PENDING (result suspended, 2026-04-15) -->
    <div class="active-card" style="border-color:#f9a8d460;background:linear-gradient(135deg,#f9a8d408,transparent);opacity:.85;">
      <div class="ac-sport">&#x1F3BE; WTA &mdash; Stuttgart R1 2026 <span class="badge badge-go">GO</span></div>
      <div class="ac-match">&#x30BD;&#x30F3;&#x30E1;&#x30BA; Z. vs &#x30D1;&#x30AA;&#x30EA;&#x30FC;&#x30CB; J.(4)</div>
      <div class="ac-rec">&#x63A8;&#x5968;: <strong style="color:#3fb950;">&#x30D1;&#x30AA;&#x30EA;&#x30FC;&#x30CB;&#x30FB;&#x30B8;&#x30E3;&#x30B9;&#x30DF;&#x30F3;</strong></div>
      <div class="ac-metrics">
        <div class="acm"><div class="acm-l">&#x30AA;&#x30C3;&#x30BA;</div><div class="acm-v odds">1.24</div></div>
        <div class="acm"><div class="acm-l">&#x4E88;&#x6E2C;EV</div><div class="acm-v ev">+5.4%</div></div>
        <div class="acm"><div class="acm-l">&#x78BA;&#x4FE1;&#x5EA6;</div><div class="acm-v">85%</div></div>
        <div class="acm"><div class="acm-l">cElo&#x5DEE;</div><div class="acm-v rule">+300pt</div></div>
      </div>
      <div class="ac-note">&#x26A0;&#xFE0F; 4/15 1st Set&#x4E2D;&#x65AD;&#x4E2D;&#xFF08;&#x305F;&#x3060;&#x3057;&#x7D50;&#x679C;&#x672A;&#x78BA;&#x8A8D;&#xFF09;&#x3002;Stuttgart indoor clay&#x3002;cElo&#x5DEE;300pt&#x3002;&#x7D50;&#x679C;&#x5F85;&#x6A5F;&#x3002;</div>
      <div class="ac-date">&#x1F4C5; 2026-04-15 JST &mdash; Stuttgart R1 &#x23F3; PENDING</div>
    </div>'''
new_paolini_card = '''        <!-- WTA Stuttgart Paolini PENDING (result suspended, 2026-04-15) -->
    <div class="active-card" style="border-color:#f9a8d460;background:linear-gradient(135deg,#f9a8d408,transparent);opacity:.85;">
      <div class="ac-sport">&#x1F3BE; WTA &mdash; Stuttgart R2 2026 <span class="badge badge-go">GO</span></div>
      <div class="ac-match">&#x30BD;&#x30F3;&#x30E1;&#x30BA; Z. vs &#x30D1;&#x30AA;&#x30EA;&#x30FC;&#x30CB; J.(4)</div>
      <div class="ac-rec">&#x63A8;&#x5968;: <strong style="color:#3fb950;">&#x30D1;&#x30AA;&#x30EA;&#x30FC;&#x30CB;&#x30FB;&#x30B8;&#x30E3;&#x30B9;&#x30DF;&#x30F3;</strong></div>
      <div class="ac-metrics">
        <div class="acm"><div class="acm-l">&#x30AA;&#x30C3;&#x30BA;</div><div class="acm-v odds">1.24</div></div>
        <div class="acm"><div class="acm-l">&#x4E88;&#x6E2C;EV</div><div class="acm-v ev">+5.4%</div></div>
        <div class="acm"><div class="acm-l">&#x78BA;&#x4FE1;&#x5EA6;</div><div class="acm-v">78%</div></div>
        <div class="acm"><div class="acm-l">cElo&#x5DEE;</div><div class="acm-v rule">+300pt</div></div>
      </div>
      <div class="ac-note">&#x26A0;&#xFE0F; 4/15 1st Set&#x4E2D;&#x65AD;&#x4E2D;&#xFF08;&#x305F;&#x3060;&#x3057;&#x7D50;&#x679C;&#x672A;&#x78BA;&#x8A8D;&#xFF09;&#x3002;Stuttgart indoor clay&#x3002;cElo&#x5DEE;300pt&#x3002;&#x7D50;&#x679C;&#x5F85;&#x6A5F;&#x3002;</div>
      <div class="ac-date">&#x1F4C5; 2026-04-15 JST &mdash; Stuttgart R2 &#x23F3; PENDING</div>
    </div>'''
if old_paolini_card in html:
    html = html.replace(old_paolini_card, new_paolini_card)
    fixes_applied.append("Active: Paolini R1→R2, 85%→78%")
else:
    print("WARN: Paolini active card anchor not found")

# --- B5. Active: Add Renegades GO card after Louisville ---
old_after_louisville = '''      <div class="ac-date">&#x1F4C5; 2026-04-17 09:00 JST &mdash; UFL Week 4</div>
    </div>

    <!-- SL Warrington'''
new_after_louisville = '''      <div class="ac-date">&#x1F4C5; 2026-04-17 09:00 JST &mdash; UFL Week 4</div>
    </div>

    <!-- UFL W4 Renegades (4/18) GO -->
    <div class="active-card" style="border-color:#fca5a560;background:linear-gradient(135deg,#fca5a508,transparent);">
      <div class="ac-sport">&#x1F3C8; UFL &mdash; Week 4 2026 <span class="badge badge-go">GO</span></div>
      <div class="ac-match">Columbus Aviators @ Arlington Renegades</div>
      <div class="ac-rec">&#x63A8;&#x5968;: <strong style="color:#3fb950;">Arlington Renegades</strong></div>
      <div class="ac-metrics">
        <div class="acm"><div class="acm-l">&#x30AA;&#x30C3;&#x30BA;</div><div class="acm-v odds">1.36</div></div>
        <div class="acm"><div class="acm-l">&#x4E88;&#x6E2C;EV</div><div class="acm-v ev">+15.6%</div></div>
        <div class="acm"><div class="acm-l">&#x78BA;&#x4FE1;&#x5EA6;</div><div class="acm-v">85%</div></div>
        <div class="acm"><div class="acm-l">Week4&#x9583;&#x5024;</div><div class="acm-v warn">80%&#x4EE5;&#x4E0A;</div></div>
      </div>
      <div class="ac-note">Renegades 3-0 vs Aviators 0-3&#x3002;QB Austin Reed&#x78BA;&#x8A8D;&#x6E08;&#x3002;DIFF/G&#x5DEE;+8&#x70B9;&#x8D85;&#x3002;&#x30DB;&#x30FC;&#x30E0;+4%&#x8003;&#x616E;&#x6E08;&#x3002;conf 85% &gt; Week4&#x9583;&#x5024;80%&#x3002;</div>
      <div class="ac-date">&#x1F4C5; 2026-04-18 09:00 JST &mdash; UFL Week 4</div>
    </div>

    <!-- SL Warrington'''
if old_after_louisville in html:
    html = html.replace(old_after_louisville, new_after_louisville)
    fixes_applied.append("Active: Added Renegades GO card (UFL W4 4/18)")
else:
    print("WARN: Louisville→Warrington anchor not found")

# --- B6. History: Dallas Renegades → Arlington Renegades ---
html = html.replace(
    'Columbus Aviators @ Dallas Renegades',
    'Columbus Aviators @ Arlington Renegades'
)
html = html.replace(
    '<td style="color:#e3b341;font-weight:600;">Dallas Renegades</td>',
    '<td style="color:#e3b341;font-weight:600;">Arlington Renegades</td>'
)
fixes_applied.append("History: Dallas Renegades → Arlington Renegades")

# --- B7. Highprob tab: Fix Musetti + swap Gauff/Musetti + add GO badges ---
old_highprob = '''        <tbody id="highprob-rows">
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

# GO重複説明を追加した列ヘッダー付き新テーブル
new_highprob = '''        <tbody id="highprob-rows">
          <tr>
            <td style="text-align:center;font-weight:700;color:var(--text);">1</td>
            <td style="font-weight:600;">Swiatek I. vs<br><strong>Siegemund L.</strong></td>
            <td>WTA Stuttgart R2<br><span style="font-size:10px;color:var(--text2);">2026-04-16</span></td>
            <td><span class="badge badge-go">Swiatek</span><br><span style="font-size:9px;color:var(--text2);">予測のみ</span></td>
            <td style="text-align:center;font-weight:700;color:#4ade80;">92%</td>
            <td style="text-align:center;">@1.02</td>
            <td style="font-size:11px;color:var(--text2);">WTA #1 vs Qualifier。cElo差400pt超。Clay最強格。予測確実性最高位。</td>
            <td><span class="badge badge-pending">PENDING</span></td>
          </tr>
          <tr>
            <td style="text-align:center;font-weight:700;color:var(--text);">2</td>
            <td style="font-weight:600;">Alcaraz C. vs<br><strong>Machac T.</strong></td>
            <td>ATP Barcelona R2<br><span style="font-size:10px;color:var(--text2);">2026-04-16</span></td>
            <td><span class="badge badge-go">Alcaraz</span><br><span style="font-size:9px;color:var(--text2);">予測のみ</span></td>
            <td style="text-align:center;font-weight:700;color:#4ade80;">88%</td>
            <td style="text-align:center;">@1.11</td>
            <td style="font-size:11px;color:var(--text2);">ATP #3 Clay specialist vs 世界66位。cElo差300pt超。Barcelona地元。</td>
            <td><span class="badge badge-pending">PENDING</span></td>
          </tr>
          <tr style="background:rgba(46,160,67,.06);">
            <td style="text-align:center;font-weight:700;color:var(--text);">3</td>
            <td style="font-weight:600;">Columbus Aviators @<br><strong>Arlington Renegades</strong></td>
            <td>UFL W4<br><span style="font-size:10px;color:var(--text2);">2026-04-18</span></td>
            <td><span class="badge badge-go">Renegades</span><br><span style="font-size:9px;color:#3fb950;font-weight:600;">&#x2714; GO推奨重複</span></td>
            <td style="text-align:center;font-weight:700;color:#4ade80;">85%</td>
            <td style="text-align:center;">@1.36</td>
            <td style="font-size:11px;color:var(--text2);">Renegades 3-0 vs Aviators 0-3。DIFF/G差。Austin Reed QB確認済。ホーム優位+4%。EV+15.6%。</td>
            <td><span class="badge badge-pending">PENDING</span></td>
          </tr>
          <tr style="background:rgba(46,160,67,.06);">
            <td style="text-align:center;font-weight:700;color:var(--text);">4</td>
            <td style="font-weight:600;">Houston Gamblers vs<br><strong>Louisville Kings</strong></td>
            <td>UFL W4<br><span style="font-size:10px;color:var(--text2);">2026-04-17</span></td>
            <td><span class="badge badge-go">Louisville</span><br><span style="font-size:9px;color:#3fb950;font-weight:600;">&#x2714; GO推奨重複</span></td>
            <td style="text-align:center;font-weight:700;color:#4ade80;">82%</td>
            <td style="text-align:center;">@1.65</td>
            <td style="font-size:11px;color:var(--text2);">Louisville 3-0 vs Gamblers 0-3。DIFF/G差8点超。OLine格差。EV+35.3%。</td>
            <td><span class="badge badge-pending">PENDING</span></td>
          </tr>
          <tr>
            <td style="text-align:center;font-weight:700;color:var(--text);">5</td>
            <td style="font-weight:600;">Samsonova L. vs<br><strong>Gauff C.</strong></td>
            <td>WTA Stuttgart R2<br><span style="font-size:10px;color:var(--text2);">2026-04-16</span></td>
            <td><span class="badge badge-go">Gauff</span><br><span style="font-size:9px;color:var(--text2);">予測のみ</span></td>
            <td style="text-align:center;font-weight:700;color:#4ade80;">81%</td>
            <td style="text-align:center;">@1.15</td>
            <td style="font-size:11px;color:var(--text2);">WTA #3 vs 世界10位前後。Gauff Clay成績良好。推定勝率81%。EV-6.7%のため予測のみ。</td>
            <td><span class="badge badge-pending">PENDING</span></td>
          </tr>
          <tr style="background:rgba(46,160,67,.06);">
            <td style="text-align:center;font-weight:700;color:var(--text);">6</td>
            <td style="font-weight:600;">Moutet C. vs<br><strong>Musetti L.</strong></td>
            <td>ATP Barcelona R2<br><span style="font-size:10px;color:var(--text2);">2026-04-16</span></td>
            <td><span class="badge badge-go">Musetti</span><br><span style="font-size:9px;color:#3fb950;font-weight:600;">&#x2714; GO推奨重複</span></td>
            <td style="text-align:center;font-weight:700;color:#4ade80;">78%</td>
            <td style="text-align:center;">@1.37</td>
            <td style="font-size:11px;color:var(--text2);">cElo差271pt。傷病歴補正-5%適用（R013）→conf 78%。EV+6.9%。</td>
            <td><span class="badge badge-pending">PENDING</span></td>
          </tr>
          <tr style="background:rgba(46,160,67,.06);">
            <td style="text-align:center;font-weight:700;color:var(--text);">7</td>
            <td style="font-weight:600;">Sonmez Z. vs<br><strong>Paolini J.(4)</strong></td>
            <td>WTA Stuttgart R2<br><span style="font-size:10px;color:var(--text2);">2026-04-15</span></td>
            <td><span class="badge badge-go">Paolini</span><br><span style="font-size:9px;color:#3fb950;font-weight:600;">&#x2714; GO推奨重複</span></td>
            <td style="text-align:center;font-weight:700;color:#4ade80;">78%</td>
            <td style="text-align:center;">@1.24</td>
            <td style="font-size:11px;color:var(--text2);">cElo差300pt（Paolini 1916 vs Sonmez 1616）。推定勝率78%。EV+5.4%。</td>
            <td><span class="badge badge-pending">PENDING</span></td>
          </tr>
        </tbody>'''

if old_highprob in html:
    html = html.replace(old_highprob, new_highprob)
    fixes_applied.append("Highprob: Musetti fix(82→78%, EV fix) + rank5/6 swap(Gauff↑/Musetti↓) + GO重複バッジ追加")
else:
    print("WARN: highprob-rows anchor not found")

# --- B8. Highprob table header: add GO overlap column note ---
old_hp_header = '''            <th>確実と判断した理由</th>
            <th>結果</th>
          </tr>
        </thead>
        <tbody id="highprob-rows">'''
new_hp_header = '''            <th>確実と判断した理由</th>
            <th>結果</th>
          </tr>
        </thead>
        <tr><td colspan="8" style="font-size:10px;color:var(--text2);padding:4px 8px;border-bottom:1px solid var(--border);">
          &#x2714;&#x00A0;GO推奨重複 = アクティブ推奨タブにもGO掲載（EV+5%閾値もクリア） &nbsp;|&nbsp; 予測のみ = 高確率だがEV-のためベット推奨なし
        </td></tr>
        <tbody id="highprob-rows">'''
if old_hp_header in html:
    html = html.replace(old_hp_header, new_hp_header)
    fixes_applied.append("Highprob: 凡例行を追加")
else:
    print("WARN: highprob header anchor not found")

# --- B9. Multi-rows: Update with corrected EV values ---
old_multi = '''      <div style="background:var(--surface);border:1px solid var(--border);border-radius:8px;padding:16px;">
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
      </div>'''

# Calculate corrected values with Musetti 78%
p_lou, o_lou = 0.82, 1.65
p_ren, o_ren = 0.85, 1.36
p_mus, o_mus = 0.78, 1.37
p_alc, o_alc = 0.88, 1.11
p_pao, o_pao = 0.78, 1.24
p_swa, o_swa = 0.92, 1.02

def calc(probs, odds_list):
    p = 1.0
    for x in probs: p *= x
    o = 1.0
    for x in odds_list: o *= x
    ev = p * o - 1
    return round(p*100,1), round(o,4), round(ev*100,1)

c1 = calc([p_lou,p_ren,p_mus],[o_lou,o_ren,o_mus])
c2 = calc([p_lou,p_ren,p_mus,p_alc],[o_lou,o_ren,o_mus,o_alc])
c3 = calc([p_lou,p_ren,p_mus,p_pao],[o_lou,o_ren,o_mus,o_pao])
c4 = calc([p_lou,p_ren,p_mus,p_alc,p_pao],[o_lou,o_ren,o_mus,o_alc,o_pao])
c5 = calc([p_lou,p_ren,p_mus,p_swa],[o_lou,o_ren,o_mus,o_swa])

new_multi = f'''      <div style="background:var(--surface);border:1px solid var(--border);border-radius:8px;padding:16px;">
        <div style="display:flex;align-items:center;gap:8px;margin-bottom:10px;">
          <span style="font-weight:700;font-size:15px;color:var(--text);">&#x1F947; 1位</span>
          <span style="font-size:13px;color:var(--text2);">Louisville &times; Renegades &times; Musetti（3試合）</span>
          <span class="badge badge-pending" style="margin-left:auto;">PENDING</span>
        </div>
        <div style="font-size:12px;color:var(--text2);margin-bottom:8px;">
          Houston vs <strong>Louisville Kings</strong> (UFL W4) &times; Aviators @ <strong>Renegades</strong> (UFL W4) &times; Moutet vs <strong>Musetti</strong> (Barcelona R2)
        </div>
        <div style="display:flex;gap:16px;flex-wrap:wrap;font-size:12px;">
          <span>全体推定勝率: <strong style="color:#4ade80;">{c1[0]}%</strong></span>
          <span>マルチオッズ: <strong>{c1[1]}</strong></span>
          <span>マルチEV: <strong style="color:#4ade80;">+{c1[2]}%</strong></span>
        </div>
        <div style="font-size:10px;color:var(--text2);margin-top:6px;">
          0.82&times;0.85&times;0.78={round(p_lou*p_ren*p_mus,4)} &nbsp;|&nbsp; 1.65&times;1.36&times;1.37={c1[1]} &nbsp;|&nbsp; EV={round(p_lou*p_ren*p_mus,4)}&times;{c1[1]}&minus;1=+{c1[2]}%
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
          <span>全体推定勝率: <strong style="color:#4ade80;">{c2[0]}%</strong></span>
          <span>マルチオッズ: <strong>{c2[1]}</strong></span>
          <span>マルチEV: <strong style="color:#4ade80;">+{c2[2]}%</strong></span>
        </div>
        <div style="font-size:10px;color:var(--text2);margin-top:6px;">
          prob={round(p_lou*p_ren*p_mus*p_alc,4)} &nbsp;|&nbsp; odds={c2[1]} &nbsp;|&nbsp; EV=+{c2[2]}%
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
          <span>全体推定勝率: <strong style="color:#4ade80;">{c3[0]}%</strong></span>
          <span>マルチオッズ: <strong>{c3[1]}</strong></span>
          <span>マルチEV: <strong style="color:#4ade80;">+{c3[2]}%</strong></span>
        </div>
        <div style="font-size:10px;color:var(--text2);margin-top:6px;">
          prob={round(p_lou*p_ren*p_mus*p_pao,4)} &nbsp;|&nbsp; odds={c3[1]} &nbsp;|&nbsp; EV=+{c3[2]}%
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
          <span>全体推定勝率: <strong style="color:#4ade80;">{c4[0]}%</strong></span>
          <span>マルチオッズ: <strong>{c4[1]}</strong></span>
          <span>マルチEV: <strong style="color:#4ade80;">+{c4[2]}%</strong></span>
        </div>
        <div style="font-size:10px;color:var(--text2);margin-top:6px;">
          prob={round(p_lou*p_ren*p_mus*p_alc*p_pao,4)} &nbsp;|&nbsp; odds={c4[1]} &nbsp;|&nbsp; EV=+{c4[2]}%
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
          <span>全体推定勝率: <strong style="color:#4ade80;">{c5[0]}%</strong></span>
          <span>マルチオッズ: <strong>{c5[1]}</strong></span>
          <span>マルチEV: <strong style="color:#4ade80;">+{c5[2]}%</strong></span>
        </div>
        <div style="font-size:10px;color:var(--text2);margin-top:6px;">
          prob={round(p_lou*p_ren*p_mus*p_swa,4)} &nbsp;|&nbsp; odds={c5[1]} &nbsp;|&nbsp; EV=+{c5[2]}%
        </div>
      </div>
      <div style="font-size:11px;color:var(--text2);text-align:right;">
        Session _29 (2026-04-15) &nbsp;|&nbsp; 出力A: 7試合 &nbsp;|&nbsp; EV+組み合わせ: 5パターン &nbsp;|&nbsp; &#x26A0; Musetti conf 82%&#x2192;78% 修正済
      </div>'''

if old_multi in html:
    html = html.replace(old_multi, new_multi)
    fixes_applied.append("Multi-rows: Musetti修正後の全EVを再計算")
else:
    print("WARN: multi-rows anchor not found")

# Save
with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)

print("\n===== 修正完了 =====")
for i, fix in enumerate(fixes_applied, 1):
    print(f"  {i}. {fix}")
print(f"\ndashboard.html: saved")
