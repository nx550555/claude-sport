#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
アクティブ推奨タブ:
1. セクションタイトル文字化け修正
2. アクティブグリッドをリーグ別グループ（テニス/UFL/ラグビー）に再配置
3. UFL チーム名を日本語化
4. CSS にリーグヘッダースタイル追加
"""

html_path = r"C:\Users\ohwada\Desktop\claude_sport\dashboard.html"
with open(html_path, encoding='utf-8') as f:
    html = f.read()

# ===== 1. CSS にリーグヘッダースタイル追加 =====
old_css_anchor = '.active-card{background:var(--surface);border:1px solid var(--border);border-radius:10px;padding:16px;}'
new_css = (
    '.active-card{background:var(--surface);border:1px solid var(--border);border-radius:10px;padding:16px;}\n'
    '.active-league-hdr{grid-column:1/-1;display:flex;align-items:center;gap:10px;'
    'border-bottom:2px solid var(--border);padding:10px 4px 6px;margin-top:6px;'
    'font-size:13px;font-weight:700;color:var(--text);letter-spacing:.02em;}'
    '.active-league-hdr:first-child{margin-top:0;}'
    '.alh-count{font-size:11px;font-weight:400;color:var(--text2);'
    'background:var(--surface2);border-radius:10px;padding:1px 8px;margin-left:auto;}'
)
if old_css_anchor in html:
    html = html.replace(old_css_anchor, new_css)
    print("CSS: リーグヘッダースタイル追加")
else:
    print("WARN: CSS anchor not found")

# ===== 2. アクティブセクション全体を置換 =====
# 置換前: 現在の全体（タイトル〜/div></div></div>\n</div>）
old_active_section = '''<div class="tab-content" id="content-active">
  <div class="section-title">繧｢繧ｯ繝・ぅ繝・GO 謗ｨ螂ｨ 窶・邨先棡蠕・■・域律莉倥・繝ｪ繝ｼ繧ｰ鬆・ｼ・/div>
  <div class="section"><div class="active-grid">

    <!-- WTA Rouen: Bondar vs Tan (4/15) NEW -->
    <div class="active-card" style="border-color:#f9a8d460;background:linear-gradient(135deg,#f9a8d408,transparent);">
      <div class="ac-sport">&#x1F3BE; WTA &mdash; Rouen R1 2026 <span class="badge badge-go">GO</span></div>
      <div class="ac-match">&#x30BF;&#x30F3; H. vs &#x30DC;&#x30F3;&#x30C0;&#x30EB; A.</div>
      <div class="ac-rec">&#x63A8;&#x5968;: <strong style="color:#3fb950;">&#x30DC;&#x30F3;&#x30C0;&#x30EB;&#x30FB;&#x30A2;&#x30F3;&#x30CA;</strong></div>
      <div class="ac-metrics">
        <div class="acm"><div class="acm-l">&#x30AA;&#x30C3;&#x30BA;</div><div class="acm-v odds">1.21</div></div>
        <div class="acm"><div class="acm-l">&#x4E88;&#x6E2C;EV</div><div class="acm-v ev">+6.5%</div></div>
        <div class="acm"><div class="acm-l">&#x78BA;&#x4FE1;&#x5EA6;</div><div class="acm-v">88%</div></div>
        <div class="acm"><div class="acm-l">&#x5E02;&#x5834;implied</div><div class="acm-v rule">82.6%</div></div>
      </div>
      <div class="ac-note">WTA Rouen Hard(indoor). &#x30CF;&#x30FC;&#x30C9;cElo&#x4E00;&#x6B21;&#x30BD;&#x30FC;&#x30B9;&#x5236;&#x9650;&#x3002;&#x5E02;&#x5834;+&#x30D5;&#x30A9;&#x30FC;&#x30E0;&#x5206;&#x6790;&#x3067;&#x63A8;&#x5B9A;88%&#x3002;EV+6.5% @1.21&#x3002;&#x5168;&#x30BD;&#x30FC;&#x30B9;&#x78BA;&#x8A8D;&#x6E08;&#x3002;</div>
      <div class="ac-date">&#x1F4C5; 2026-04-15 18:30 JST &mdash; WTA Rouen R1</div>
    </div>

    <!-- ATP Barcelona R2: Musetti vs Moutet (4/16) NEW -->
    <div class="active-card" style="border-color:#79c0ff60;background:linear-gradient(135deg,#79c0ff08,transparent);">
      <div class="ac-sport">&#x1F3BE; ATP &mdash; Barcelona R2 2026 <span class="badge badge-go">GO</span></div>
      <div class="ac-match">&#x30E0;&#x30C6; C. vs &#x30E0;&#x30BB;&#x30C3;&#x30C6;&#x30A3; L.(2)</div>
      <div class="ac-rec">&#x63A8;&#x5968;: <strong style="color:#3fb950;">&#x30E0;&#x30BB;&#x30C3;&#x30C6;&#x30A3;&#x30FB;&#x30ED;&#x30EC;&#x30F3;&#x30C4;&#x30A9;</strong></div>
      <div class="ac-metrics">
        <div class="acm"><div class="acm-l">&#x30AA;&#x30C3;&#x30BA;</div><div class="acm-v odds">1.37</div></div>
        <div class="acm"><div class="acm-l">&#x4E88;&#x6E2C;EV</div><div class="acm-v ev">+6.9%</div></div>
        <div class="acm"><div class="acm-l">&#x78BA;&#x4FE1;&#x5EA6;</div><div class="acm-v">78%</div></div>
        <div class="acm"><div class="acm-l">cElo&#x5DEE;</div><div class="acm-v rule">+271pt</div></div>
      </div>
      <div class="ac-cond">&#x26A0; PR&#x88DC;&#x6B63; -5%: AO2026 adductor + Miami2026 arm &#x8907;&#x6570;&#x8CA0;&#x50B7; (R013&#x9069;&#x7528;: &#x904E;&#x5927;&#x88DC;&#x6B63;&#x56DE;&#x907F;)</div>
      <div class="ac-note">&#x30E0;&#x30BB;&#x30C3;&#x30C6;&#x30A3; cElo~2017 / &#x30E0;&#x30C6; ~1746&#x3002;&#x5DEE;271pt &gt; 130pt GO&#x9583;&#x5024;&#x3002;&#x57FA;&#x672C;84% &rarr; PR&#x88DC;&#x6B63; -5% &rarr; conf 78%&#x3002;&#x5168;&#x30BD;&#x30FC;&#x30B9;&#x78BA;&#x8A8D;&#x6E08;&#x3002;</div>
      <div class="ac-date">&#x1F4C5; 2026-04-16 18:00 JST &mdash; Barcelona Clay(outdoor) R2</div>
    </div>

    <!-- NRL Warriors (4/18) existing GO -->
    <div class="active-card" style="border-color:#23863640;background:linear-gradient(135deg,#23863610,transparent);">
      <div class="ac-sport">&#x1F3C9; NRL &mdash; Round 7 2026</div>
      <div class="ac-match">NZ&#x30A6;&#x30A9;&#x30EA;&#x30A2;&#x30FC;&#x30BA; vs &#x30B4;&#x30FC;&#x30EB;&#x30C9;&#x30B3;&#x30FC;&#x30B9;&#x30C8;&#x30FB;&#x30BF;&#x30A4;&#x30BF;&#x30F3;&#x30BA; <span class="badge badge-go">GO</span></div>
      <div class="ac-rec">&#x63A8;&#x5968;: <strong style="color:#3fb950;">NZ&#x30A6;&#x30A9;&#x30EA;&#x30A2;&#x30FC;&#x30BA;</strong></div>
      <div class="ac-metrics">
        <div class="acm"><div class="acm-l">&#x30AA;&#x30C3;&#x30BA;</div><div class="acm-v odds">1.22</div></div>
        <div class="acm"><div class="acm-l">&#x4E88;&#x6E2C;EV</div><div class="acm-v ev">+10.7%</div></div>
        <div class="acm"><div class="acm-l">&#x78BA;&#x4FE1;&#x5EA6;</div><div class="acm-v">90.7%</div></div>
        <div class="acm"><div class="acm-l">PD/G&#x5DEE;</div><div class="acm-v rule">+16.7pt</div></div>
      </div>
      <div class="ac-note">&#x30A6;&#x30A9;&#x30EA;&#x30A2;&#x30FC;&#x30BA; PD/G +8.7 / &#x30BF;&#x30A4;&#x30BF;&#x30F3;&#x30BA; PD/G -8.0 &rarr; &#x5DEE;+16.7pt&#x3002;&#x9583;&#x5024;12pt&#x8D85;&#x3002;conf 90.7% / EV+10.7%</div>
      <div class="ac-date">&#x1F4C5; 2026-04-18 JST &mdash; NRL R7</div>
    </div>

    <!-- SL Leeds (4/18) existing GO -->
    <div class="active-card" style="border-color:#bfdbfe60;background:linear-gradient(135deg,#bfdbfe08,transparent);">
      <div class="ac-sport">&#x1F3C9; Super League &mdash; Round 8 2026</div>
      <div class="ac-match">&#x30CF;&#x30C0;&#x30FC;&#x30BA;&#x30D5;&#x30A3;&#x30FC;&#x30EB;&#x30C9;&#x30FB;&#x30B8;&#x30E3;&#x30A4;&#x30A2;&#x30F3;&#x30C4; vs &#x30EA;&#x30FC;&#x30BA;&#x30FB;&#x30E9;&#x30A4;&#x30CE;&#x30BA; <span class="badge badge-go">GO</span></div>
      <div class="ac-rec">&#x63A8;&#x5968;: <strong style="color:#3fb950;">&#x30EA;&#x30FC;&#x30BA;&#x30FB;&#x30E9;&#x30A4;&#x30CE;&#x30BA;</strong></div>
      <div class="ac-metrics">
        <div class="acm"><div class="acm-l">&#x30AA;&#x30C3;&#x30BA;</div><div class="acm-v odds">1.32</div></div>
        <div class="acm"><div class="acm-l">&#x4E88;&#x6E2C;EV</div><div class="acm-v ev">+14.8%</div></div>
        <div class="acm"><div class="acm-l">&#x78BA;&#x4FE1;&#x5EA6;</div><div class="acm-v">87%</div></div>
        <div class="acm"><div class="acm-l">PD/G&#x5DEE;</div><div class="acm-v rule">+20.3pt</div></div>
      </div>
      <div class="ac-note">&#x30EA;&#x30FC;&#x30BA; PD/G +14.00(2&#x4F4D;) / &#x30CF;&#x30C0;&#x30FC;&#x30BA;&#x30D5;&#x30A3;&#x30FC;&#x30EB;&#x30C9; -6.29(11&#x4F4D;) &rarr; &#x5DEE;+20.3pt&#x3002;&#x65E9;&#x671F;&#x9583;&#x5024;12pt&#x8D85;&#x3002;conf 87% / EV+14.8%</div>
      <div class="ac-date">&#x1F4C5; 2026-04-18 JST &mdash; Super League R8</div>
    </div>

    <!-- UFL W4 Louisville (4/17) NEW GO -->
    <div class="active-card" style="border-color:#fca5a560;background:linear-gradient(135deg,#fca5a508,transparent);">
      <div class="ac-sport">&#x1F3C8; UFL &mdash; Week 4 2026 <span class="badge badge-go">GO</span></div>
      <div class="ac-match">Houston Gamblers vs Louisville Kings</div>
      <div class="ac-rec">&#x63A8;&#x5968;: <strong style="color:#3fb950;">Louisville Kings</strong></div>
      <div class="ac-metrics">
        <div class="acm"><div class="acm-l">&#x30AA;&#x30C3;&#x30BA;</div><div class="acm-v odds">1.65</div></div>
        <div class="acm"><div class="acm-l">&#x4E88;&#x6E2C;EV</div><div class="acm-v ev">+35.3%</div></div>
        <div class="acm"><div class="acm-l">&#x78BA;&#x4FE1;&#x5EA6;</div><div class="acm-v">82%</div></div>
        <div class="acm"><div class="acm-l">Week4&#x9583;&#x5024;</div><div class="acm-v warn">80%&#x4EE5;&#x4E0A;</div></div>
      </div>
      <div class="ac-note">Houston QB: Dekkers(&#x80A9;W1&#x8CA0;&#x50B7;)&rarr;Tagovailoa&#x5148;&#x767A;(W3 21/40 171yd 7-45&#x5927;&#x6557;)&#x3002;Louisville QB Bean&#x7D76;&#x597D;&#x8ABF;(W3 352yd 3TD)&#x3002;conf 82% &gt; Week4&#x9583;&#x5024;80%&#x3002;</div>
      <div class="ac-date">&#x1F4C5; 2026-04-17 09:00 JST &mdash; UFL Week 4</div>
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

    <!-- SL Warrington (4/19) UPDATED EV+32% conf80% -->
    <div class="active-card" style="border-color:#bfdbfe60;background:linear-gradient(135deg,#bfdbfe08,transparent);">
      <div class="ac-sport">&#x1F3C9; Super League &mdash; Round 8 2026</div>
      <div class="ac-match">&#x30AB;&#x30BF;&#x30EB;&#x30FC;&#x30CB;&#x30E3;&#x30FB;&#x30C9;&#x30E9;&#x30B4;&#x30F3;&#x30BA; vs &#x30A6;&#x30A9;&#x30EA;&#x30F3;&#x30C8;&#x30F3;&#x30FB;&#x30A6;&#x30EB;&#x30D6;&#x30BA; <span class="badge badge-go">GO</span></div>
      <div class="ac-rec">&#x63A8;&#x5968;: <strong style="color:#3fb950;">&#x30A6;&#x30A9;&#x30EA;&#x30F3;&#x30C8;&#x30F3;&#x30FB;&#x30A6;&#x30EB;&#x30D6;&#x30BA;</strong></div>
      <div class="ac-metrics">
        <div class="acm"><div class="acm-l">&#x30AA;&#x30C3;&#x30BA;</div><div class="acm-v odds">1.65</div></div>
        <div class="acm"><div class="acm-l">&#x4E88;&#x6E2C;EV</div><div class="acm-v ev">+32.0%</div></div>
        <div class="acm"><div class="acm-l">&#x78BA;&#x4FE1;&#x5EA6;</div><div class="acm-v">80%</div></div>
        <div class="acm"><div class="acm-l">PD/G&#x5DEE;</div><div class="acm-v rule">+23.9pt</div></div>
      </div>
      <div class="ac-cond">&#x26A0; &#x6016;&#x6211;: Tanginoa OUT + Luke Yates OUT (&#x30D0;&#x30C3;&#x30AF;&#x30ED;&#x30FC;2&#x540D;&#x96E2;&#x8131;&#x78BA;&#x8A8D;) &rarr; &#x4FE1;&#x983C;&#x5EA6; 85%&rarr;80%&#x4FEE;&#x6B63;</div>
      <div class="ac-note">&#x30A6;&#x30A9;&#x30EA;&#x30F3;&#x30C8;&#x30F3; PD/G +21.17(1&#x4F4D;) / &#x30AB;&#x30BF;&#x30EB;&#x30FC;&#x30CB;&#x30E3; -2.71(6&#x4F4D;) &rarr; &#x5DEE;+23.9pt&#x3002;&#x4ED4;&#x56FD;&#x30DB;&#x30FC;&#x30E0;-5%&#x8003;&#x616E;&#x6E08;&#x3002;conf 80% / EV+32.0%</div>
      <div class="ac-date">&#x1F4C5; 2026-04-19 JST &mdash; Super League R8 (Perpignan, France)</div>
    </div>

        <!-- WTA Stuttgart Paolini PENDING (result suspended, 2026-04-15) -->
    <div class="active-card" style="border-color:#f9a8d460;background:linear-gradient(135deg,#f9a8d408,transparent);opacity:.85;">
      <div class="ac-sport">&#x1F3BE; WTA &mdash; Stuttgart R2 2026 <span class="badge badge-go">GO</span></div>
      <div class="ac-match">&#x30BD;&#x30F3;&#x30E1;&#x30BA; Z. vs &#x30D1;&#x30AA;&#x30EA;&#x30FC;&#x30CB; J.(4)</div>
      <div class="ac-rec">&#x63A8;&#x5968;: <strong style="color:#3fb950;">&#x30D1;&#x30AA;&#x30EA;&#x30FC;&#x30CB;&#x30FB;&#x30B8;&#x30A1;&#x30B9;&#x30DF;&#x30F3;</strong></div>
      <div class="ac-metrics">
        <div class="acm"><div class="acm-l">&#x30AA;&#x30C3;&#x30BA;</div><div class="acm-v odds">1.24</div></div>
        <div class="acm"><div class="acm-l">&#x4E88;&#x6E2C;EV</div><div class="acm-v ev">+5.4%</div></div>
        <div class="acm"><div class="acm-l">&#x78BA;&#x4FE1;&#x5EA6;</div><div class="acm-v">78%</div></div>
        <div class="acm"><div class="acm-l">cElo&#x5DEE;</div><div class="acm-v rule">+300pt</div></div>
      </div>
      <div class="ac-note">&#x26A0;&#xFE0F; 4/15 1st Set&#x4E2D;&#x65AD;&#x4E2D;&#xFF08;&#x305F;&#x3060;&#x3057;&#x7D50;&#x679C;&#x672A;&#x78BA;&#x8A8D;&#xFF09;&#x3002;Stuttgart indoor clay&#x3002;cElo&#x5DEE;300pt&#x3002;&#x7D50;&#x679C;&#x5F85;&#x6A5F;&#x3002;</div>
      <div class="ac-date">&#x1F4C5; 2026-04-15 JST &mdash; Stuttgart R2 &#x23F3; PENDING</div>
    </div>
  </div></div>
</div>'''

# ===== 新レイアウト: リーグ別グループ =====
new_active_section = '''<div class="tab-content" id="content-active">
  <div class="section-title">アクティブ GO 推奨 — PENDING のみ（結果確定後は全履歴タブへ移動）</div>
  <div class="section"><div class="active-grid">

    <!-- ===== 🎾 テニス ===== -->
    <div class="active-league-hdr">
      <span>&#x1F3BE; テニス <span style="color:var(--text2);font-weight:400;font-size:11px;">ATP / WTA</span></span>
      <span class="alh-count">3件</span>
    </div>

    <!-- ATP Barcelona R2: Musetti vs Moutet (4/16) -->
    <div class="active-card" style="border-color:#79c0ff60;background:linear-gradient(135deg,#79c0ff08,transparent);">
      <div class="ac-sport">&#x1F3BE; ATP &mdash; バルセロナ R2 2026 <span class="badge badge-go">GO</span></div>
      <div class="ac-match">&#x30E0;&#x30C6; C. vs &#x30E0;&#x30BB;&#x30C3;&#x30C6;&#x30A3; L.(2)</div>
      <div class="ac-rec">&#x63A8;&#x5968;: <strong style="color:#3fb950;">&#x30E0;&#x30BB;&#x30C3;&#x30C6;&#x30A3;&#x30FB;&#x30ED;&#x30EC;&#x30F3;&#x30C4;&#x30A9;</strong></div>
      <div class="ac-metrics">
        <div class="acm"><div class="acm-l">&#x30AA;&#x30C3;&#x30BA;</div><div class="acm-v odds">1.37</div></div>
        <div class="acm"><div class="acm-l">&#x4E88;&#x6E2C;EV</div><div class="acm-v ev">+6.9%</div></div>
        <div class="acm"><div class="acm-l">&#x78BA;&#x4FE1;&#x5EA6;</div><div class="acm-v">78%</div></div>
        <div class="acm"><div class="acm-l">cElo&#x5DEE;</div><div class="acm-v rule">+271pt</div></div>
      </div>
      <div class="ac-cond">&#x26A0; PR&#x88DC;&#x6B63; -5%: AO2026 adductor + Miami2026 arm &#x8907;&#x6570;&#x8CA0;&#x50B7; (R013&#x9069;&#x7528;: &#x904E;&#x5927;&#x88DC;&#x6B63;&#x56DE;&#x907F;)</div>
      <div class="ac-note">&#x30E0;&#x30BB;&#x30C3;&#x30C6;&#x30A3; cElo~2017 / &#x30E0;&#x30C6; ~1746&#x3002;&#x5DEE;271pt &gt; 130pt GO&#x9583;&#x5024;&#x3002;&#x57FA;&#x672C;84% &rarr; PR&#x88DC;&#x6B63; -5% &rarr; conf 78%&#x3002;&#x5168;&#x30BD;&#x30FC;&#x30B9;&#x78BA;&#x8A8D;&#x6E08;&#x3002;</div>
      <div class="ac-date">&#x1F4C5; 2026-04-16 18:00 JST &mdash; バルセロナ Clay R2</div>
    </div>

    <!-- WTA Rouen: Bondar vs Tan (4/15) -->
    <div class="active-card" style="border-color:#f9a8d460;background:linear-gradient(135deg,#f9a8d408,transparent);">
      <div class="ac-sport">&#x1F3BE; WTA &mdash; ルーアン R1 2026 <span class="badge badge-go">GO</span></div>
      <div class="ac-match">&#x30BF;&#x30F3; H. vs &#x30DC;&#x30F3;&#x30C0;&#x30EB; A.</div>
      <div class="ac-rec">&#x63A8;&#x5968;: <strong style="color:#3fb950;">&#x30DC;&#x30F3;&#x30C0;&#x30EB;&#x30FB;&#x30A2;&#x30F3;&#x30CA;</strong></div>
      <div class="ac-metrics">
        <div class="acm"><div class="acm-l">&#x30AA;&#x30C3;&#x30BA;</div><div class="acm-v odds">1.21</div></div>
        <div class="acm"><div class="acm-l">&#x4E88;&#x6E2C;EV</div><div class="acm-v ev">+6.5%</div></div>
        <div class="acm"><div class="acm-l">&#x78BA;&#x4FE1;&#x5EA6;</div><div class="acm-v">88%</div></div>
        <div class="acm"><div class="acm-l">&#x5E02;&#x5834;implied</div><div class="acm-v rule">82.6%</div></div>
      </div>
      <div class="ac-note">WTA ルーアン ハード(室内)&#x3002;&#x30CF;&#x30FC;&#x30C9;cElo&#x4E00;&#x6B21;&#x30BD;&#x30FC;&#x30B9;&#x5236;&#x9650;&#x3002;&#x5E02;&#x5834;+&#x30D5;&#x30A9;&#x30FC;&#x30E0;&#x5206;&#x6790;&#x3067;&#x63A8;&#x5B9A;88%&#x3002;EV+6.5% @1.21&#x3002;&#x5168;&#x30BD;&#x30FC;&#x30B9;&#x78BA;&#x8A8D;&#x6E08;&#x3002;</div>
      <div class="ac-date">&#x1F4C5; 2026-04-15 18:30 JST &mdash; WTA ルーアン R1</div>
    </div>

    <!-- WTA Stuttgart Paolini PENDING (result suspended, 2026-04-15) -->
    <div class="active-card" style="border-color:#f9a8d460;background:linear-gradient(135deg,#f9a8d408,transparent);opacity:.85;">
      <div class="ac-sport">&#x1F3BE; WTA &mdash; シュトゥットガルト R2 2026 <span class="badge badge-go">GO</span></div>
      <div class="ac-match">&#x30BD;&#x30F3;&#x30E1;&#x30BA; Z. vs &#x30D1;&#x30AA;&#x30EA;&#x30FC;&#x30CB; J.(4)</div>
      <div class="ac-rec">&#x63A8;&#x5968;: <strong style="color:#3fb950;">&#x30D1;&#x30AA;&#x30EA;&#x30FC;&#x30CB;&#x30FB;&#x30B8;&#x30E3;&#x30B9;&#x30DF;&#x30F3;</strong></div>
      <div class="ac-metrics">
        <div class="acm"><div class="acm-l">&#x30AA;&#x30C3;&#x30BA;</div><div class="acm-v odds">1.24</div></div>
        <div class="acm"><div class="acm-l">&#x4E88;&#x6E2C;EV</div><div class="acm-v ev">+5.4%</div></div>
        <div class="acm"><div class="acm-l">&#x78BA;&#x4FE1;&#x5EA6;</div><div class="acm-v">78%</div></div>
        <div class="acm"><div class="acm-l">cElo&#x5DEE;</div><div class="acm-v rule">+300pt</div></div>
      </div>
      <div class="ac-note">&#x26A0;&#xFE0F; 4/15 1st Set&#x4E2D;&#x65AD;&#x4E2D;&#xFF08;&#x305F;&#x3060;&#x3057;&#x7D50;&#x679C;&#x672A;&#x78BA;&#x8A8D;&#xFF09;&#x3002;&#x30B7;&#x30E5;&#x30C8;&#x30A5;&#x30C3;&#x30C8;&#x30AC;&#x30EB;&#x30C8; indoor clay&#x3002;cElo&#x5DEE;300pt&#x3002;&#x7D50;&#x679C;&#x5F85;&#x6A5F;&#x3002;</div>
      <div class="ac-date">&#x1F4C5; 2026-04-15 JST &mdash; シュトゥットガルト R2 &#x23F3; PENDING</div>
    </div>

    <!-- ===== 🏈 アメフト ===== -->
    <div class="active-league-hdr">
      <span>&#x1F3C8; アメリカンフットボール <span style="color:var(--text2);font-weight:400;font-size:11px;">UFL</span></span>
      <span class="alh-count">2件</span>
    </div>

    <!-- UFL W4 Louisville (4/17) -->
    <div class="active-card" style="border-color:#fca5a560;background:linear-gradient(135deg,#fca5a508,transparent);">
      <div class="ac-sport">&#x1F3C8; UFL &mdash; Week 4 2026 <span class="badge badge-go">GO</span></div>
      <div class="ac-match">&#x30D2;&#x30E5;&#x30FC;&#x30B9;&#x30C8;&#x30F3;&#x30FB;&#x30AE;&#x30E3;&#x30F3;&#x30D6;&#x30E9;&#x30FC;&#x30BA; vs &#x30EB;&#x30A4;&#x30D3;&#x30EB;&#x30FB;&#x30AD;&#x30F3;&#x30B0;&#x30B9;</div>
      <div class="ac-rec">&#x63A8;&#x5968;: <strong style="color:#3fb950;">&#x30EB;&#x30A4;&#x30D3;&#x30EB;&#x30FB;&#x30AD;&#x30F3;&#x30B0;&#x30B9;</strong></div>
      <div class="ac-metrics">
        <div class="acm"><div class="acm-l">&#x30AA;&#x30C3;&#x30BA;</div><div class="acm-v odds">1.65</div></div>
        <div class="acm"><div class="acm-l">&#x4E88;&#x6E2C;EV</div><div class="acm-v ev">+35.3%</div></div>
        <div class="acm"><div class="acm-l">&#x78BA;&#x4FE1;&#x5EA6;</div><div class="acm-v">82%</div></div>
        <div class="acm"><div class="acm-l">Week4&#x9583;&#x5024;</div><div class="acm-v warn">80%&#x4EE5;&#x4E0A;</div></div>
      </div>
      <div class="ac-note">&#x30D2;&#x30E5;&#x30FC;&#x30B9;&#x30C8;&#x30F3; QB: Dekkers(&#x80A9;W1&#x8CA0;&#x50B7;)&rarr;Tagovailoa&#x5148;&#x767A;(W3 21/40 171yd 7-45&#x5927;&#x6557;)&#x3002;&#x30EB;&#x30A4;&#x30D3;&#x30EB; QB Bean&#x7D76;&#x597D;&#x8ABF;(W3 352yd 3TD)&#x3002;conf 82% &gt; Week4&#x9583;&#x5024;80%&#x3002;</div>
      <div class="ac-date">&#x1F4C5; 2026-04-17 09:00 JST &mdash; UFL Week 4</div>
    </div>

    <!-- UFL W4 Renegades (4/18) -->
    <div class="active-card" style="border-color:#fca5a560;background:linear-gradient(135deg,#fca5a508,transparent);">
      <div class="ac-sport">&#x1F3C8; UFL &mdash; Week 4 2026 <span class="badge badge-go">GO</span></div>
      <div class="ac-match">&#x30B3;&#x30ED;&#x30F3;&#x30D0;&#x30B9;&#x30FB;&#x30A2;&#x30D3;&#x30A8;&#x30A4;&#x30BF;&#x30FC;&#x30BA; @ &#x30A2;&#x30FC;&#x30EA;&#x30F3;&#x30C8;&#x30F3;&#x30FB;&#x30EC;&#x30CD;&#x30B2;&#x30FC;&#x30BA;</div>
      <div class="ac-rec">&#x63A8;&#x5968;: <strong style="color:#3fb950;">&#x30A2;&#x30FC;&#x30EA;&#x30F3;&#x30C8;&#x30F3;&#x30FB;&#x30EC;&#x30CD;&#x30B2;&#x30FC;&#x30BA;</strong></div>
      <div class="ac-metrics">
        <div class="acm"><div class="acm-l">&#x30AA;&#x30C3;&#x30BA;</div><div class="acm-v odds">1.36</div></div>
        <div class="acm"><div class="acm-l">&#x4E88;&#x6E2C;EV</div><div class="acm-v ev">+15.6%</div></div>
        <div class="acm"><div class="acm-l">&#x78BA;&#x4FE1;&#x5EA6;</div><div class="acm-v">85%</div></div>
        <div class="acm"><div class="acm-l">Week4&#x9583;&#x5024;</div><div class="acm-v warn">80%&#x4EE5;&#x4E0A;</div></div>
      </div>
      <div class="ac-note">&#x30EC;&#x30CD;&#x30B2;&#x30FC;&#x30BA; 3-0 vs &#x30A2;&#x30D3;&#x30A8;&#x30A4;&#x30BF;&#x30FC;&#x30BA; 0-3&#x3002;QB Austin Reed&#x78BA;&#x8A8D;&#x6E08;&#x3002;DIFF/G&#x5DEE;+8&#x70B9;&#x8D85;&#x3002;&#x30DB;&#x30FC;&#x30E0;+4%&#x8003;&#x616E;&#x6E08;&#x3002;conf 85% &gt; Week4&#x9583;&#x5024;80%&#x3002;</div>
      <div class="ac-date">&#x1F4C5; 2026-04-18 09:00 JST &mdash; UFL Week 4</div>
    </div>

    <!-- ===== 🏉 ラグビー ===== -->
    <div class="active-league-hdr">
      <span>&#x1F3C9; ラグビー <span style="color:var(--text2);font-weight:400;font-size:11px;">NRL / Super League</span></span>
      <span class="alh-count">3件</span>
    </div>

    <!-- NRL Warriors (4/18) -->
    <div class="active-card" style="border-color:#23863640;background:linear-gradient(135deg,#23863610,transparent);">
      <div class="ac-sport">&#x1F3C9; NRL &mdash; Round 7 2026</div>
      <div class="ac-match">NZ&#x30A6;&#x30A9;&#x30EA;&#x30A2;&#x30FC;&#x30BA; vs &#x30B4;&#x30FC;&#x30EB;&#x30C9;&#x30B3;&#x30FC;&#x30B9;&#x30C8;&#x30FB;&#x30BF;&#x30A4;&#x30BF;&#x30F3;&#x30BA; <span class="badge badge-go">GO</span></div>
      <div class="ac-rec">&#x63A8;&#x5968;: <strong style="color:#3fb950;">NZ&#x30A6;&#x30A9;&#x30EA;&#x30A2;&#x30FC;&#x30BA;</strong></div>
      <div class="ac-metrics">
        <div class="acm"><div class="acm-l">&#x30AA;&#x30C3;&#x30BA;</div><div class="acm-v odds">1.22</div></div>
        <div class="acm"><div class="acm-l">&#x4E88;&#x6E2C;EV</div><div class="acm-v ev">+10.7%</div></div>
        <div class="acm"><div class="acm-l">&#x78BA;&#x4FE1;&#x5EA6;</div><div class="acm-v">90.7%</div></div>
        <div class="acm"><div class="acm-l">PD/G&#x5DEE;</div><div class="acm-v rule">+16.7pt</div></div>
      </div>
      <div class="ac-note">&#x30A6;&#x30A9;&#x30EA;&#x30A2;&#x30FC;&#x30BA; PD/G +8.7 / &#x30BF;&#x30A4;&#x30BF;&#x30F3;&#x30BA; PD/G -8.0 &rarr; &#x5DEE;+16.7pt&#x3002;&#x9583;&#x5024;12pt&#x8D85;&#x3002;conf 90.7% / EV+10.7%</div>
      <div class="ac-date">&#x1F4C5; 2026-04-18 JST &mdash; NRL R7</div>
    </div>

    <!-- SL Leeds (4/18) -->
    <div class="active-card" style="border-color:#bfdbfe60;background:linear-gradient(135deg,#bfdbfe08,transparent);">
      <div class="ac-sport">&#x1F3C9; Super League &mdash; Round 8 2026</div>
      <div class="ac-match">&#x30CF;&#x30C0;&#x30FC;&#x30BA;&#x30D5;&#x30A3;&#x30FC;&#x30EB;&#x30C9;&#x30FB;&#x30B8;&#x30E3;&#x30A4;&#x30A2;&#x30F3;&#x30C4; vs &#x30EA;&#x30FC;&#x30BA;&#x30FB;&#x30E9;&#x30A4;&#x30CE;&#x30BA; <span class="badge badge-go">GO</span></div>
      <div class="ac-rec">&#x63A8;&#x5968;: <strong style="color:#3fb950;">&#x30EA;&#x30FC;&#x30BA;&#x30FB;&#x30E9;&#x30A4;&#x30CE;&#x30BA;</strong></div>
      <div class="ac-metrics">
        <div class="acm"><div class="acm-l">&#x30AA;&#x30C3;&#x30BA;</div><div class="acm-v odds">1.32</div></div>
        <div class="acm"><div class="acm-l">&#x4E88;&#x6E2C;EV</div><div class="acm-v ev">+14.8%</div></div>
        <div class="acm"><div class="acm-l">&#x78BA;&#x4FE1;&#x5EA6;</div><div class="acm-v">87%</div></div>
        <div class="acm"><div class="acm-l">PD/G&#x5DEE;</div><div class="acm-v rule">+20.3pt</div></div>
      </div>
      <div class="ac-note">&#x30EA;&#x30FC;&#x30BA; PD/G +14.00(2&#x4F4D;) / &#x30CF;&#x30C0;&#x30FC;&#x30BA;&#x30D5;&#x30A3;&#x30FC;&#x30EB;&#x30C9; -6.29(11&#x4F4D;) &rarr; &#x5DEE;+20.3pt&#x3002;&#x65E9;&#x671F;&#x9583;&#x5024;12pt&#x8D85;&#x3002;conf 87% / EV+14.8%</div>
      <div class="ac-date">&#x1F4C5; 2026-04-18 JST &mdash; Super League R8</div>
    </div>

    <!-- SL Warrington (4/19) -->
    <div class="active-card" style="border-color:#bfdbfe60;background:linear-gradient(135deg,#bfdbfe08,transparent);">
      <div class="ac-sport">&#x1F3C9; Super League &mdash; Round 8 2026</div>
      <div class="ac-match">&#x30AB;&#x30BF;&#x30EB;&#x30FC;&#x30CB;&#x30E3;&#x30FB;&#x30C9;&#x30E9;&#x30B4;&#x30F3;&#x30BA; vs &#x30A6;&#x30A9;&#x30EA;&#x30F3;&#x30C8;&#x30F3;&#x30FB;&#x30A6;&#x30EB;&#x30D6;&#x30BA; <span class="badge badge-go">GO</span></div>
      <div class="ac-rec">&#x63A8;&#x5968;: <strong style="color:#3fb950;">&#x30A6;&#x30A9;&#x30EA;&#x30F3;&#x30C8;&#x30F3;&#x30FB;&#x30A6;&#x30EB;&#x30D6;&#x30BA;</strong></div>
      <div class="ac-metrics">
        <div class="acm"><div class="acm-l">&#x30AA;&#x30C3;&#x30BA;</div><div class="acm-v odds">1.65</div></div>
        <div class="acm"><div class="acm-l">&#x4E88;&#x6E2C;EV</div><div class="acm-v ev">+32.0%</div></div>
        <div class="acm"><div class="acm-l">&#x78BA;&#x4FE1;&#x5EA6;</div><div class="acm-v">80%</div></div>
        <div class="acm"><div class="acm-l">PD/G&#x5DEE;</div><div class="acm-v rule">+23.9pt</div></div>
      </div>
      <div class="ac-cond">&#x26A0; &#x6016;&#x6211;: Tanginoa OUT + Luke Yates OUT (&#x30D0;&#x30C3;&#x30AF;&#x30ED;&#x30FC;2&#x540D;&#x96E2;&#x8131;&#x78BA;&#x8A8D;) &rarr; &#x4FE1;&#x983C;&#x5EA6; 85%&rarr;80%&#x4FEE;&#x6B63;</div>
      <div class="ac-note">&#x30A6;&#x30A9;&#x30EA;&#x30F3;&#x30C8;&#x30F3; PD/G +21.17(1&#x4F4D;) / &#x30AB;&#x30BF;&#x30EB;&#x30FC;&#x30CB;&#x30E3; -2.71(6&#x4F4D;) &rarr; &#x5DEE;+23.9pt&#x3002;&#x4ED4;&#x56FD;&#x30DB;&#x30FC;&#x30E0;-5%&#x8003;&#x616E;&#x6E08;&#x3002;conf 80% / EV+32.0%</div>
      <div class="ac-date">&#x1F4C5; 2026-04-19 JST &mdash; Super League R8 (Perpignan, France)</div>
    </div>

  </div></div>
</div>'''

if old_active_section in html:
    html = html.replace(old_active_section, new_active_section)
    print("アクティブセクション: リーグ別再配置完了")
else:
    print("ERROR: old_active_section anchor not found")
    # デバッグ: 最初の200文字を確認
    start = html.find('<div class="tab-content" id="content-active">')
    print(f"  DEBUG start: {repr(html[start:start+200])}")

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)
print("dashboard.html: saved")
