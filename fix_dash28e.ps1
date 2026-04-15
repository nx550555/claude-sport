$file = "C:\Users\ohwada\Desktop\claude_sport\dashboard.html"
$lines = Get-Content -Path $file -Encoding UTF8

# ===== 1. Sport Card ATP (lines 264-268, indices 263-267) =====
# L264 (index 263): 10 -> 13
$lines[263] = $lines[263] -replace '>10<', '>13<'
Write-Host "L264: $($lines[263].Trim())"

# L265 (index 264): 7 -> 10
$lines[264] = $lines[264] -replace '>7<', '>10<'
Write-Host "L265: $($lines[264].Trim())"

# L266 (index 265): 70.0% -> 76.9%
$lines[265] = $lines[265] -replace '70\.0%', '76.9%'
Write-Host "L266: $($lines[265].Trim())"

# L267 (index 266): +0.530 -> +1.370
$lines[266] = $lines[266] -replace '\+0\.530', '+1.370'
Write-Host "L267: $($lines[266].Trim())"

# L268 (index 267): 3(4/14) orange -> 0 grey
$lines[267] = $lines[267] -replace 'color:#e3b341;">[^<]+<', 'color:#8b949e;">0<'
Write-Host "L268: $($lines[267].Trim())"

# ===== 2. ATP Active Cards -> HIT (indices 378-418) =====

$newMusetti = @(
    '    <div class="active-card" style="border-color:#23863640;background:linear-gradient(135deg,#23863610,transparent);opacity:.8;">',
    '      <div class="ac-sport">&#x1F3BE; ATP &#x2014; Barcelona R1 2026 <span class="badge badge-hit">HIT &#x2713;</span></div>',
    '      <div class="ac-match">2026-04-14 JST / Barcelona Clay R1</div>',
    '      <div class="ac-rec" style="color:#3fb950;">&#x30E0;&#x30BB;&#x30C3;&#x30C6;&#x30A3; 7-5 6-2</div>',
    '      <div class="ac-metrics">',
    '        <div class="acm"><div class="acm-l">&#x30AA;&#x30C3;&#x30BA;</div><div class="acm-v odds">1.27</div></div>',
    '        <div class="acm"><div class="acm-l">&#x4E88;&#x6E2C;EV</div><div class="acm-v ev">+9.7%</div></div>',
    '        <div class="acm"><div class="acm-l">&#x5B9F;&#x7E3E;EV</div><div class="acm-v ev">+0.27u</div></div>',
    '        <div class="acm"><div class="acm-l">&#x78BA;&#x4FE1;&#x5EA6;</div><div class="acm-v">86.4%</div></div>',
    '      </div>',
    '      <div class="ac-note">cElo &#x30E0;&#x30BB;&#x30C3;&#x30C6;&#x30A3; 1841 / &#x30E9;&#x30F3;&#x30C0;&#x30EB;&#x30FC;&#x30B5; 1471. conf 86.4% / EV+9.7%</div>',
    '      <div class="ac-date">&#x1F4C5; 2026-04-14 JST &#x2713;&#x78BA;&#x5B9A;</div>',
    '    </div>'
)

$newCobolli = @(
    '    <div class="active-card" style="border-color:#23863640;background:linear-gradient(135deg,#23863610,transparent);opacity:.8;">',
    '      <div class="ac-sport">&#x1F3BE; ATP &#x2014; Munich R1 2026 <span class="badge badge-hit">HIT &#x2713;</span></div>',
    '      <div class="ac-match">2026-04-14 JST / Munich Clay R1</div>',
    '      <div class="ac-rec" style="color:#3fb950;">&#x30B3;&#x30DC;&#x30C3;&#x30EA; 6-4 7-5</div>',
    '      <div class="ac-metrics">',
    '        <div class="acm"><div class="acm-l">&#x30AA;&#x30C3;&#x30BA;</div><div class="acm-v odds">1.21</div></div>',
    '        <div class="acm"><div class="acm-l">&#x4E88;&#x6E2C;EV</div><div class="acm-v ev">+8.7%</div></div>',
    '        <div class="acm"><div class="acm-l">&#x5B9F;&#x7E3E;EV</div><div class="acm-v ev">+0.21u</div></div>',
    '        <div class="acm"><div class="acm-l">&#x78BA;&#x4FE1;&#x5EA6;</div><div class="acm-v">89.8%</div></div>',
    '      </div>',
    '      <div class="ac-note">cElo &#x30B3;&#x30DC;&#x30C3;&#x30EA; 1929 / &#x30C7;&#x30C9;&#x30A5;&#x30E9;=&#x30D1;&#x30EB;&#x30E1;&#x30ED; 1551. conf 89.8% / EV+8.7%</div>',
    '      <div class="ac-date">&#x1F4C5; 2026-04-14 JST &#x2713;&#x78BA;&#x5B9A;</div>',
    '    </div>'
)

$newKopriva = @(
    '    <div class="active-card" style="border-color:#23863640;background:linear-gradient(135deg,#23863610,transparent);opacity:.8;">',
    '      <div class="ac-sport">&#x1F3BE; ATP &#x2014; Munich R1 2026 <span class="badge badge-hit">HIT &#x2713;</span></div>',
    '      <div class="ac-match">2026-04-14 JST / Munich Clay R1</div>',
    '      <div class="ac-rec" style="color:#3fb950;">&#x30B3;&#x30D7;&#x30B8;&#x30D0; 6-3 5-7 6-2</div>',
    '      <div class="ac-metrics">',
    '        <div class="acm"><div class="acm-l">&#x30AA;&#x30C3;&#x30BA;</div><div class="acm-v odds">1.36</div></div>',
    '        <div class="acm"><div class="acm-l">&#x4E88;&#x6E2C;EV</div><div class="acm-v ev">+9.8%</div></div>',
    '        <div class="acm"><div class="acm-l">&#x5B9F;&#x7E3E;EV</div><div class="acm-v ev">+0.36u</div></div>',
    '        <div class="acm"><div class="acm-l">&#x78BA;&#x4FE1;&#x5EA6;</div><div class="acm-v">80.7%</div></div>',
    '      </div>',
    '      <div class="ac-note">cElo &#x30B3;&#x30D7;&#x30B8;&#x30D0; 1699 / &#x30A8;&#x30F3;&#x30B2;&#x30EB; 1388. conf 80.7% / EV+9.8%</div>',
    '      <div class="ac-date">&#x1F4C5; 2026-04-14 JST &#x2713;&#x78BA;&#x5B9A;</div>',
    '    </div>'
)

# Splice: keep [0..377], new Musetti, keep [391], new Cobolli, keep [405], new Kopriva, keep [419..]
$newLines = $lines[0..377] + $newMusetti + $lines[391..391] + $newCobolli + $lines[405..405] + $newKopriva + $lines[419..($lines.Length - 1)]

$newLines | Set-Content -Path $file -Encoding UTF8
Write-Host "Done - total lines: $($newLines.Length)"
