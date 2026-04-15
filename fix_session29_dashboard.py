#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session _29 dashboard update script
- Update highprob-rows with Output A (2 entries)
- Update multi-rows with Output B (1 combination)
"""
enc = 'utf-8'

dash_path = r"C:\Users\ohwada\Desktop\claude_sport\dashboard.html"
with open(dash_path, encoding=enc) as f:
    dash = f.read()

# ============================================================
# 1. Update highprob-rows (Output A table)
# ============================================================
old_highprob = '''        <tbody id="highprob-rows">
          <tr>
            <td colspan="8" style="text-align:center;color:var(--text2);padding:40px;font-size:13px;">
              次回の分析セッションから記録開始
            </td>
          </tr>
        </tbody>'''

new_highprob = '''        <tbody id="highprob-rows">
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

if old_highprob in dash:
    dash = dash.replace(old_highprob, new_highprob)
    print("highprob-rows: updated")
else:
    print("WARNING: highprob-rows anchor not found!")

# ============================================================
# 2. Update multi-rows (Output B cards)
# ============================================================
old_multi = '''    <div id="multi-rows" style="display:flex;flex-direction:column;gap:12px;">
      <div style="text-align:center;color:var(--text2);padding:40px;font-size:13px;background:var(--surface);border:1px solid var(--border);border-radius:8px;">
        次回の分析セッションから記録開始。出力Aが2件以上の場合に表示。
      </div>
    </div>'''

new_multi = '''    <div id="multi-rows" style="display:flex;flex-direction:column;gap:12px;">
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

if old_multi in dash:
    dash = dash.replace(old_multi, new_multi)
    print("multi-rows: updated")
else:
    print("WARNING: multi-rows anchor not found!")

with open(dash_path, 'w', encoding=enc) as f:
    f.write(dash)
print("dashboard.html: OK")
