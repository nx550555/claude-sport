$file = "C:\Users\ohwada\Desktop\claude_sport\dashboard.html"
$lines = Get-Content -Path $file -Encoding UTF8

# ===== 1. Remove stray <tbody> at line 630 (index 629) =====
if ($lines[629] -match '<tbody>') {
    $lines[629] = '        </tr>'
    Write-Host "L630: stray tbody removed"
}

# ===== 2. Main EV chart: add points #19 and #20 (lines 1862-1863, indices 1861-1862) =====
# polygon: ...740,10 740,170 -> ...740,10 752,6 764,2 764,170
if ($lines[1861] -match '740,10 740,170') {
    $lines[1861] = $lines[1861] -replace '740,10 740,170', '740,10 752,6 764,2 764,170'
    Write-Host "L1862 polygon updated"
}
# polyline: ...740,10" -> ...740,10 752,6 764,2"
if ($lines[1862] -match '740,10"') {
    $lines[1862] = $lines[1862] -replace '740,10"', '740,10 752,6 764,2"'
    Write-Host "L1863 polyline updated"
}

# ===== 3. History table: add rows #18/#19/#20 before </tbody> (line 2195, index 2194) =====
$row18 = '        <tr style="background:rgba(46,160,67,.06);"><td>#18</td><td>2026-04-14</td><td><span class="sport-tag" style="color:#79c0ff;">&#x1F3BE; ATP</span></td><td style="font-size:12px;">Barcelona R1 / Musetti</td><td style="color:#3fb950;font-weight:700;">&#x2713; HIT</td><td class="ev-pos">+0.270</td><td class="ev-pos">+3.261</td><td style="color:#3fb950;">77.8%</td></tr>'
$row19 = '        <tr style="background:rgba(46,160,67,.06);"><td>#19</td><td>2026-04-14</td><td><span class="sport-tag" style="color:#79c0ff;">&#x1F3BE; ATP</span></td><td style="font-size:12px;">Munich R1 / Cobolli</td><td style="color:#3fb950;font-weight:700;">&#x2713; HIT</td><td class="ev-pos">+0.210</td><td class="ev-pos">+3.471</td><td style="color:#3fb950;">78.9%</td></tr>'
$row20 = '        <tr style="background:rgba(46,160,67,.06);"><td>#20</td><td>2026-04-14</td><td><span class="sport-tag" style="color:#79c0ff;">&#x1F3BE; ATP</span></td><td style="font-size:12px;">Munich R1 / Kopriva</td><td style="color:#3fb950;font-weight:700;">&#x2713; HIT</td><td class="ev-pos">+0.360</td><td class="ev-pos">+3.831</td><td style="color:#3fb950;">80.0%</td></tr>'

# Insert before the </tbody> at current index 2194
$newLines = $lines[0..2193] + $row18 + $row19 + $row20 + $lines[2194..($lines.Length - 1)]

$newLines | Set-Content -Path $file -Encoding UTF8
Write-Host "Done - total lines: $($newLines.Length)"
