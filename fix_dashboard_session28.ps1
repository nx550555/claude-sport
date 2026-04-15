$file = "C:\Users\ohwada\Desktop\claude_sport\dashboard.html"
$content = Get-Content -Raw -Encoding UTF8 $file

# ---- Main stats: confirmed count ----
$content = $content -replace '<div class="bs-sub">&#x7D50;&#x679C;&#x78BA;&#x5B9A;: 17&#x4EF6;</div>', '<div class="bs-sub">&#x7D50;&#x679C;&#x78BA;&#x5B9A;: 20&#x4EF6;</div>'
# Also try ASCII version
$content = $content.Replace("BS-sub" + ">" + "17", "")  # no-op

# Direct text replacements (main stats area)
$content = $content.Replace('<div class="bs-sub">&#x7D50;&#x679C;&#x78BA;&#x5B9A;: 17&#x4EF6;</div>', '<div class="bs-sub">&#x7D50;&#x679C;&#x78BA;&#x5B9A;: 20&#x4EF6;</div>')

# hit rate 76.5%
$content = $content.Replace('<div class="bs-val" style="color:#3fb950;">76.5%</div>', '<div class="bs-val" style="color:#3fb950;">80.0%</div>')

# 13HIT / 17
$content = $content.Replace('<div class="bs-sub">13HIT / 17&#x8A66;&#x5408;</div>', '<div class="bs-sub">16HIT / 20&#x8A66;&#x5408;</div>')

# EV total +2.991 -> +3.831 (main stat)
$content = $content.Replace('<div class="bs-val" style="color:#3fb950;">+2.991</div>', '<div class="bs-val" style="color:#3fb950;">+3.831</div>')

# ---- Prediction accuracy panel ----
$content = $content.Replace('<span class="pred-pct" style="color:#3fb950;">76.5%</span><span class="pred-count">13 / 17 &#x78BA;&#x5B9A;</span>', '<span class="pred-pct" style="color:#3fb950;">80.0%</span><span class="pred-count">16 / 20 &#x78BA;&#x5B9A;</span>')

# ATP row in prediction panel: 7/10 70.0% -> 10/13 76.9%
$content = $content.Replace('<span>ATP</span><span>7 / 10</span><span style="color:#3fb950;">70.0%</span>', '<span>ATP</span><span>10 / 13</span><span style="color:#3fb950;">76.9%</span>')

# ---- Mini chart: extend polyline with 3 new points ----
# Old last 3 points: ...207,31 218,22
# New points: 229,15 240,9 251,2 (extended at ~EV +3.261, +3.471, +3.831)
$oldPoly17 = 'points="44,126 55,152 66,136 77,162 88,147 99,133 110,121 121,111 132,105 143,95 154,78 165,38 176,24 187,50 198,45 207,31 218,22"'
$newPoly20 = 'points="44,126 55,152 66,136 77,162 88,147 99,133 110,121 121,111 132,105 143,95 154,78 165,38 176,24 187,50 198,45 207,31 218,22 229,15 240,9 251,2"'
$content = $content.Replace($oldPoly17, $newPoly20)

# Polygon (adds closing vertices)
$oldPolygon17 = 'points="44,126 55,152 66,136 77,162 88,147 99,133 110,121 121,111 132,105 143,95 154,78 165,38 176,24 187,50 198,45 207,31 218,22 218,100 44,100"'
$newPolygon20 = 'points="44,126 55,152 66,136 77,162 88,147 99,133 110,121 121,111 132,105 143,95 154,78 165,38 176,24 187,50 198,45 207,31 218,22 229,15 240,9 251,2 251,100 44,100"'
$content = $content.Replace($oldPolygon17, $newPolygon20)

# Update last highlighted circle & label
$content = $content.Replace('<circle cx="218" cy="22"  r="4"   fill="#3fb950" stroke="#0d1117" stroke-width="1.5"/>', '<circle cx="218" cy="22"  r="2.5" fill="#3fb950" opacity="0.9"/><circle cx="229" cy="15"  r="2.5" fill="#3fb950" opacity="0.9"/><circle cx="240" cy="9"   r="2.5" fill="#3fb950" opacity="0.9"/><circle cx="251" cy="2"   r="4"   fill="#3fb950" stroke="#0d1117" stroke-width="1.5"/>')

# Update chart label +2.991 -> +3.831 and position
$content = $content.Replace('<rect x="155" y="10" width="54" height="16" rx="3" fill="#0f2c1a" stroke="#3fb950" stroke-width="1"/>', '<rect x="198" y="0" width="54" height="16" rx="3" fill="#0f2c1a" stroke="#3fb950" stroke-width="1"/>')
$content = $content.Replace('<text x="182" y="21" text-anchor="middle" fill="#3fb950" font-size="10" font-weight="700">+2.991</text>', '<text x="225" y="11" text-anchor="middle" fill="#3fb950" font-size="10" font-weight="700">+3.831</text>')

# ---- Main EV chart: extend polyline ----
$oldMainPoly = 'points="60,170 106,170 152,118 198,131 244,108 290,93 336,82 382,73 428,67 474,62 520,57 566,54 612,51 658,59 704,56"'
$newMainPoly = 'points="60,170 106,170 152,118 198,131 244,108 290,93 336,82 382,73 428,67 474,62 520,57 566,54 612,51 658,59 704,56 716,45 728,34 740,10"'
$content = $content.Replace($oldMainPoly, $newMainPoly)

$oldMainPolygon = 'points="60,170 106,170 152,118 198,131 244,108 290,93 336,82 382,73 428,67 474,62 520,57 566,54 612,51 658,59 704,56 704,170"'
$newMainPolygon = 'points="60,170 106,170 152,118 198,131 244,108 290,93 336,82 382,73 428,67 474,62 520,57 566,54 612,51 658,59 704,56 716,45 728,34 740,10 740,170"'
$content = $content.Replace($oldMainPolygon, $newMainPolygon)

# ---- cumEV comment update ----
$content = $content.Replace('<!-- cumEV: -1.0,-2.0,-1.37,-2.37,-1.8,-1.267,-0.817,-0.437,-0.187,+0.213,+0.863,+2.393,+2.933,+1.933,+2.133,+2.671,+2.991 -->', '<!-- cumEV: -1.0,-2.0,-1.37,-2.37,-1.8,-1.267,-0.817,-0.437,-0.187,+0.213,+0.863,+2.393,+2.933,+1.933,+2.133,+2.671,+2.991,+3.261,+3.471,+3.831 -->')

# ---- History table: add 3 rows after #17 ----
$row17 = '<tr style="background:rgba(46,160,67,.06);"><td>#17</td><td>2026-04-12</td><td><span class="sport-tag" style="color:#fca5a5;">&#x1F3C8; UFL</span></td><td style="font-size:12px;">Columbus Aviators @ Dallas Renegades</td><td style="color:#3fb950;font-weight:700;">&#x2713; HIT</td><td class="ev-pos">+0.320</td><td class="ev-pos">+2.991</td><td style="color:#3fb950;">76.5%</td></tr>'
$row17new = '<tr style="background:rgba(46,160,67,.06);"><td>#17</td><td>2026-04-12</td><td><span class="sport-tag" style="color:#fca5a5;">&#x1F3C8; UFL</span></td><td style="font-size:12px;">Columbus Aviators @ Dallas Renegades</td><td style="color:#3fb950;font-weight:700;">&#x2713; HIT</td><td class="ev-pos">+0.320</td><td class="ev-pos">+2.991</td><td style="color:#3fb950;">76.5%</td></tr>
        <tr style="background:rgba(46,160,67,.06);"><td>#18</td><td>2026-04-14</td><td><span class="sport-tag" style="color:#79c0ff;">&#x1F3BE; Tennis</span></td><td style="font-size:12px;">Musetti L. vs Landaluce M. (Barcelona R1)</td><td style="color:#3fb950;font-weight:700;">&#x2713; HIT</td><td class="ev-pos">+0.270</td><td class="ev-pos">+3.261</td><td style="color:#3fb950;">77.8%</td></tr>
        <tr style="background:rgba(46,160,67,.06);"><td>#19</td><td>2026-04-14</td><td><span class="sport-tag" style="color:#79c0ff;">&#x1F3BE; Tennis</span></td><td style="font-size:12px;">Cobolli F. vs Dedura-Palmero D. (Munich R1)</td><td style="color:#3fb950;font-weight:700;">&#x2713; HIT</td><td class="ev-pos">+0.210</td><td class="ev-pos">+3.471</td><td style="color:#3fb950;">78.9%</td></tr>
        <tr style="background:rgba(46,160,67,.06);"><td>#20</td><td>2026-04-14</td><td><span class="sport-tag" style="color:#79c0ff;">&#x1F3BE; Tennis</span></td><td style="font-size:12px;">Kopriva V. vs Engel J. (Munich R1)</td><td style="color:#3fb950;font-weight:700;">&#x2713; HIT</td><td class="ev-pos">+0.360</td><td class="ev-pos">+3.831</td><td style="color:#3fb950;">80.0%</td></tr>'

$content = $content.Replace($row17, $row17new)

# ---- Write file ----
$content | Set-Content -Path $file -Encoding UTF8 -NoNewline
Write-Host "Dashboard updated successfully"
