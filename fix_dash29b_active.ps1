# Session 29 Dashboard - Part B: Active section full replacement
$path = "C:\Users\ohwada\Desktop\claude_sport\dashboard.html"
$html = [System.IO.File]::ReadAllText($path, [System.Text.Encoding]::UTF8)

$startM = "<!-- ===== " + [char]0x30A2 + [char]0x30AF + [char]0x30C6 + [char]0x30A3 + [char]0x30D6 + [char]0x63A8 + [char]0x5968 + " ===== -->"
$endM   = "<!-- ===== " + [char]0x5168 + [char]0x5C65 + [char]0x6B74 + " ===== -->"

$si = $html.IndexOf($startM)
$ei = $html.IndexOf($endM)

if ($si -lt 0) { Write-Host "START not found"; exit 1 }
if ($ei -lt 0) { Write-Host "END not found"; exit 1 }

$before = $html.Substring(0, $si)
$after  = $html.Substring($ei)

# Build new active section (Japanese via char codes where needed)
$new = @'
<!-- ===== アクティブ推奨 ===== -->
<div class="tab-content" id="content-active">
  <div class="section-title">アクティブ GO 推奨 — 結果待ち（日付・リーグ順）</div>
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

    <!-- ATP Barcelona R1 HIT -->
    <div class="active-card" style="border-color:#23863640;background:linear-gradient(135deg,#23863610,transparent);opacity:.8;">
      <div class="ac-sport">&#x1F3BE; ATP &mdash; Barcelona R1 2026 <span class="badge badge-hit">HIT &#x2713;</span></div>
      <div class="ac-match">2026-04-14 JST / Barcelona Clay R1</div>
      <div class="ac-rec" style="color:#3fb950;">&#x30E0;&#x30BB;&#x30C3;&#x30C6;&#x30A3; 7-5 6-2</div>
      <div class="ac-metrics">
        <div class="acm"><div class="acm-l">&#x30AA;&#x30C3;&#x30BA;</div><div class="acm-v odds">1.27</div></div>
        <div class="acm"><div class="acm-l">&#x4E88;&#x6E2C;EV</div><div class="acm-v ev">+9.7%</div></div>
        <div class="acm"><div class="acm-l">&#x5B9F;&#x7E3E;EV</div><div class="acm-v ev">+0.27u</div></div>
        <div class="acm"><div class="acm-l">&#x78BA;&#x4FE1;&#x5EA6;</div><div class="acm-v">86.4%</div></div>
      </div>
      <div class="ac-note">cElo &#x30E0;&#x30BB;&#x30C3;&#x30C6;&#x30A3; ~2017 / &#x30E9;&#x30F3;&#x30C0;&#x30EB;&#x30FC;&#x30B5; ~1648. conf 86.4% / EV+9.7%</div>
      <div class="ac-date">&#x1F4C5; 2026-04-14 JST &#x2713;&#x78BA;&#x5B9A;</div>
    </div>

    <!-- ATP Munich R1 Cobolli HIT -->
    <div class="active-card" style="border-color:#23863640;background:linear-gradient(135deg,#23863610,transparent);opacity:.8;">
      <div class="ac-sport">&#x1F3BE; ATP &mdash; Munich R1 2026 <span class="badge badge-hit">HIT &#x2713;</span></div>
      <div class="ac-match">2026-04-14 JST / Munich Clay R1</div>
      <div class="ac-rec" style="color:#3fb950;">&#x30B3;&#x30DC;&#x30C3;&#x30EA; 6-4 7-5</div>
      <div class="ac-metrics">
        <div class="acm"><div class="acm-l">&#x30AA;&#x30C3;&#x30BA;</div><div class="acm-v odds">1.21</div></div>
        <div class="acm"><div class="acm-l">&#x4E88;&#x6E2C;EV</div><div class="acm-v ev">+8.7%</div></div>
        <div class="acm"><div class="acm-l">&#x5B9F;&#x7E3E;EV</div><div class="acm-v ev">+0.21u</div></div>
        <div class="acm"><div class="acm-l">&#x78BA;&#x4FE1;&#x5EA6;</div><div class="acm-v">89.8%</div></div>
      </div>
      <div class="ac-note">cElo &#x30B3;&#x30DC;&#x30C3;&#x30EA; 1929 / &#x30C7;&#x30C9;&#x30A5;&#x30E9;=&#x30D1;&#x30EB;&#x30E1;&#x30ED; 1551. conf 89.8% / EV+8.7%</div>
      <div class="ac-date">&#x1F4C5; 2026-04-14 JST &#x2713;&#x78BA;&#x5B9A;</div>
    </div>

    <!-- ATP Munich R1 Kopriva HIT -->
    <div class="active-card" style="border-color:#23863640;background:linear-gradient(135deg,#23863610,transparent);opacity:.8;">
      <div class="ac-sport">&#x1F3BE; ATP &mdash; Munich R1 2026 <span class="badge badge-hit">HIT &#x2713;</span></div>
      <div class="ac-match">2026-04-14 JST / Munich Clay R1</div>
      <div class="ac-rec" style="color:#3fb950;">&#x30B3;&#x30D7;&#x30B8;&#x30D0; 6-3 5-7 6-2</div>
      <div class="ac-metrics">
        <div class="acm"><div class="acm-l">&#x30AA;&#x30C3;&#x30BA;</div><div class="acm-v odds">1.36</div></div>
        <div class="acm"><div class="acm-l">&#x4E88;&#x6E2C;EV</div><div class="acm-v ev">+9.8%</div></div>
        <div class="acm"><div class="acm-l">&#x5B9F;&#x7E3E;EV</div><div class="acm-v ev">+0.36u</div></div>
        <div class="acm"><div class="acm-l">&#x78BA;&#x4FE1;&#x5EA6;</div><div class="acm-v">80.7%</div></div>
      </div>
      <div class="ac-note">cElo &#x30B3;&#x30D7;&#x30B8;&#x30D0; 1699 / &#x30A8;&#x30F3;&#x30B2;&#x30EB; 1388. conf 80.7% / EV+9.8%</div>
      <div class="ac-date">&#x1F4C5; 2026-04-14 JST &#x2713;&#x78BA;&#x5B9A;</div>
    </div>

    <!-- WTA Stuttgart Paolini MISS (data contamination confirmed) -->
    <div class="active-card" style="border-color:#f8514940;background:linear-gradient(135deg,#f8514908,transparent);opacity:.85;">
      <div class="ac-sport">&#x1F3BE; WTA &mdash; Stuttgart R1 2026 <span class="badge badge-miss">MISS &#x2717;</span></div>
      <div class="ac-match">&#x30BD;&#x30F3;&#x30E1;&#x30BA; Z. vs &#x30D1;&#x30AA;&#x30EA;&#x30FC;&#x30CB; J.(4)</div>
      <div class="ac-rec" style="color:#f85149;">&#x7D50;&#x679C;: &#x30BD;&#x30F3;&#x30E1;&#x30BA;&#x52DD;&#x5229; (&#x30D1;&#x30AA;&#x30EA;&#x30FC;&#x30CB;&#x63A8;&#x5968; &rarr; MISS)</div>
      <div class="ac-metrics">
        <div class="acm"><div class="acm-l">&#x30AA;&#x30C3;&#x30BA;</div><div class="acm-v odds">1.24</div></div>
        <div class="acm"><div class="acm-l">&#x4E88;&#x6E2C;EV</div><div class="acm-v ev">+5.4%</div></div>
        <div class="acm"><div class="acm-l">&#x5B9F;&#x7E3E;EV</div><div class="acm-v" style="color:#f85149;">-1.000</div></div>
        <div class="acm"><div class="acm-l">&#x78BA;&#x4FE1;&#x5EA6;</div><div class="acm-v">85%</div></div>
      </div>
      <div class="ac-note">&#x26A0;&#xFE0F; &#x30C7;&#x30FC;&#x30BF;&#x6C5A;&#x67D3;&#x691C;&#x51FA;: 4/15 JSON&#x3067;&#x300Cupcoming&#x300D;&#x8868;&#x793A;&#x3082;4/13&#x30C7;&#x30FC;&#x30BF;&#x3067;&#x65E2;&#x306B;&#x30BD;&#x30F3;&#x30E1;&#x30BA;&#x52DD;&#x5229;&#x78BA;&#x8A8D;&#x3002;cElo&#x5DEE;300pt&#x306E;&#x9AD8;&#x78BA;&#x4FE1;&#x63A8;&#x5968;&#x304C;&#x30A2;&#x30C3;&#x30D7;&#x30BB;&#x30C3;&#x30C8;&#x3002;</div>
      <div class="ac-date">&#x1F4C5; 2026-04-13 &#x78BA;&#x5B9A; &#x2717;</div>
    </div>

    <!-- ATP MC Final SKIP -->
    <div class="active-card" style="border-color:#30363d;background:linear-gradient(135deg,#30363d10,transparent);opacity:.7;">
      <div class="ac-sport">&#x1F3BE; ATP &mdash; MC2026 &#x6C7A;&#x52DD; <span class="badge badge-skip">SKIP&#xFF08;&#x89B3;&#x6226;&#xFF09;</span></div>
      <div class="ac-match">&#x30A2;&#x30EB;&#x30AB;&#x30E9;&#x30B9; C.(1) vs &#x30B7;&#x30CA;&#x30FC; J.(2)</div>
      <div class="ac-rec" style="color:#3fb950;">&#x7D50;&#x679C;: &#x30B7;&#x30CA;&#x30FC; 7-6(5) 6-3 &mdash; &#x4E88;&#x6E2C;&#x306A;&#x3057;&#xFF08;SKIP&#xFF09;</div>
      <div class="ac-metrics">
        <div class="acm"><div class="acm-l">cElo&#x5DEE;</div><div class="acm-v rule">~20pt</div></div>
        <div class="acm"><div class="acm-l">L1&#x5224;&#x5B9A;</div><div class="acm-v" style="color:#f85149;">&#x4E0D;&#x901A;&#x904E;</div></div>
        <div class="acm"><div class="acm-l">&#x4E88;&#x6E2C;</div><div class="acm-v" style="color:#8b949e;">50/50</div></div>
        <div class="acm"><div class="acm-l">bet</div><div class="acm-v rule">&#x306A;&#x3057;</div></div>
      </div>
      <div class="ac-note">SKIP&#x6B63;&#x89E3;&#xFF08;&#x5DEE;&#x306A;&#x3057;&#x3067;&#x5F53;&#x3066;&#x3066;&#x3082;&#x904B;&#xFF09;&#x3002;&#x30B7;&#x30CA;&#x30FC;&#x304C;7-6(5) 6-3&#x3067;&#x512A;&#x52DD;&#x3002;</div>
      <div class="ac-date">&#x1F4C5; 2026-04-13 JST &#x2713;&#x5B8C;&#x4E86;</div>
    </div>

    <!-- UFL Week 3 Dallas HIT -->
    <div class="active-card" style="border-color:#23863640;background:linear-gradient(135deg,#23863610,transparent);opacity:.8;">
      <div class="ac-sport">&#x1F3C8; UFL Week 3 &mdash; &#x30B3;&#x30ED;&#x30F3;&#x30D0;&#x30B9; @ &#x30C0;&#x30E9;&#x30B9; <span class="badge badge-hit">HIT &#x2713;</span></div>
      <div class="ac-match">2026-04-12 JST / Cotton Bowl, Dallas</div>
      <div class="ac-rec" style="color:#3fb950;">&#x30C0;&#x30E9;&#x30B9;&#x30FB;&#x30EC;&#x30CD;&#x30B2;&#x30FC;&#x30BA; 28 &mdash; 23 &#x30B3;&#x30ED;&#x30F3;&#x30D0;&#x30B9;&#x30FB;&#x30A2;&#x30D3;&#x30A8;&#x30A4;&#x30BF;&#x30FC;&#x30BA;</div>
      <div class="ac-metrics">
        <div class="acm"><div class="acm-l">&#x30AA;&#x30C3;&#x30BA;</div><div class="acm-v odds">1.32</div></div>
        <div class="acm"><div class="acm-l">&#x4E88;&#x6E2C;EV</div><div class="acm-v ev">+8.2%</div></div>
        <div class="acm"><div class="acm-l">&#x5B9F;&#x7E3E;EV</div><div class="acm-v ev">+0.32u</div></div>
        <div class="acm"><div class="acm-l">&#x78BA;&#x4FE1;&#x5EA6;</div><div class="acm-v">82%</div></div>
      </div>
      <div class="ac-note">PD&#x5DEE;30pt&#xFF08;&#x30C0;&#x30E9;&#x30B9; +17.5/&#x8A66;&#x5408; vs &#x30B3;&#x30ED;&#x30F3;&#x30D0;&#x30B9; -12.5/&#x8A66;&#x5408;&#xFF09;&#x304C;&#x5730;&#x529B;&#x5DEE;&#x901A;&#x308A;&#x3002;</div>
      <div class="ac-date">&#x1F4C5; 2026-04-12 JST &#x2713;&#x78BA;&#x5B9A;</div>
    </div>

    <!-- NBA Rockets HIT -->
    <div class="active-card" style="border-color:#23863640;background:linear-gradient(135deg,#23863610,transparent);opacity:.8;">
      <div class="ac-sport">&#x1F3C0; NBA &mdash; &#x30B0;&#x30EA;&#x30BA;&#x30EA;&#x30FC;&#x30BA; @ &#x30ED;&#x30B1;&#x30C3;&#x30C8; <span class="badge badge-hit">HIT &#x2713;</span></div>
      <div class="ac-match">2026-04-12 JST / Toyota Center, Houston</div>
      <div class="ac-rec" style="color:#3fb950;">&#x30D2;&#x30E5;&#x30FC;&#x30B9;&#x30C8;&#x30F3;&#x30FB;&#x30ED;&#x30B1;&#x30C3;&#x30C4;&#x30B9; 124 &mdash; 109 &#x30E1;&#x30F3;&#x30D5;&#x30A3;&#x30B9;&#x30FB;&#x30B0;&#x30EA;&#x30BA;&#x30EA;&#x30FC;&#x30BA;</div>
      <div class="ac-metrics">
        <div class="acm"><div class="acm-l">&#x30AA;&#x30C3;&#x30BA;</div><div class="acm-v odds">1.20</div></div>
        <div class="acm"><div class="acm-l">&#x4E88;&#x6E2C;EV</div><div class="acm-v ev">+5.6%</div></div>
        <div class="acm"><div class="acm-l">&#x5B9F;&#x7E3E;EV</div><div class="acm-v ev">+0.20u</div></div>
        <div class="acm"><div class="acm-l">&#x78BA;&#x4FE1;&#x5EA6;</div><div class="acm-v">88%</div></div>
      </div>
      <div class="ac-date">&#x1F4C5; 2026-04-12 JST &#x2713;&#x78BA;&#x5B9A;&#x6E08;</div>
    </div>

    <!-- NBA Wizards SKIP -->
    <div class="active-card" style="border-color:#30363d;background:linear-gradient(135deg,#30363d08,transparent);opacity:.7;">
      <div class="ac-sport">&#x1F3C0; NBA &mdash; &#x30A6;&#x30A3;&#x30B6;&#x30FC;&#x30BA; @ &#x30AD;&#x30E3;&#x30D0;&#x30EA;&#x30A2;&#x30FC;&#x30BA; <span class="badge badge-skip">SKIP</span></div>
      <div class="ac-match">2026-04-12 JST / Cavs 130-126&#xFF08;&#x53C2;&#x8003;&#x8A18;&#x9332;&#xFF09;</div>
      <div class="ac-rec" style="color:#8b949e;">&#x30AA;&#x30C3;&#x30BA;&#x672A;&#x78BA;&#x8A8D;&#x306E;&#x305F;&#x3081;&#x30D9;&#x30C3;&#x30C8;&#x672A;&#x5B9F;&#x884C;</div>
      <div class="ac-metrics">
        <div class="acm"><div class="acm-l">&#x7D50;&#x679C;</div><div class="acm-v" style="color:#3fb950;">Cavs&#x52DD;</div></div>
        <div class="acm"><div class="acm-l">&#x30DF;&#x30C3;&#x30C1;&#x30A7;&#x30EB;</div><div class="acm-v ev">48pts</div></div>
        <div class="acm"><div class="acm-l">&#x30AA;&#x30C3;&#x30BA;</div><div class="acm-v warn">&#x672A;&#x53D6;&#x5F97;</div></div>
        <div class="acm"><div class="acm-l">EV</div><div class="acm-v rule">&#x30AB;&#x30A6;&#x30F3;&#x30C8;&#x5916;</div></div>
      </div>
      <div class="ac-date">&#x1F4C5; 2026-04-12 JST &mdash; &#x7D71;&#x8A08;&#x30CE;&#x30FC;&#x30AB;&#x30A6;&#x30F3;&#x30C8;</div>
    </div>
  </div></div>
</div>

'@

$html = $before + $new + $after
[System.IO.File]::WriteAllText($path, $html, [System.Text.Encoding]::UTF8)
Write-Host "Part B (active section) done."
