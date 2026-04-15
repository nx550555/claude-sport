# Session 29 - Part F: Add Paolini MISS point to cumulative EV chart
$path = "C:\Users\ohwada\Desktop\claude_sport\dashboard.html"
$html = [System.IO.File]::ReadAllText($path, [System.Text.Encoding]::UTF8)

# Current last point (Kopriva #20): x=251 cy=2 (represents +3.831)
# New point (Paolini #21 MISS): x=262 cy=26 (represents +2.831; y=100-2.831*26=26.4~26)

# 1. Update polygon: add x=262,26 before closing "251,100 44,100"
$oldPolygon = '251,2 251,100 44,100'
$newPolygon = '251,2 262,26 262,100 44,100'
$html = $html.Replace($oldPolygon, $newPolygon)
Write-Host "1. Polygon updated"

# 2. Update polyline: add 262,26 at end
$oldPolyline = '240,9 251,2" fill="none"'
$newPolyline = '240,9 251,2 262,26" fill="none"'
$html = $html.Replace($oldPolyline, $newPolyline)
Write-Host "2. Polyline updated"

# 3. Change last circle (Kopriva at cx=251 cy=2) back to normal HIT
# And add Paolini MISS circle at cx=262 cy=26 with red
# The current last circle: <circle cx="251" cy="2"   r="4"   fill="#3fb950" ...>
$oldLastCircle = '<circle cx="251" cy="2"   r="4"   fill="#3fb950" stroke="#0d1117" stroke-width="1.5"/>'
$newLastCircle = '<circle cx="251" cy="2"   r="2.5" fill="#3fb950" opacity="0.9"/><circle cx="262" cy="26"  r="4"   fill="#f85149" stroke="#0d1117" stroke-width="1.5"/>'
$html = $html.Replace($oldLastCircle, $newLastCircle)
Write-Host "3. Circles updated"

# 4. Move the current value label to x=262+27=289 area... or keep at current position
# Current label is at x=198..225 for +2.831 label. Update to reflect it's now the end of chart.
# Actually just move label to be near the new last point (cx=262)
$oldLabel = '<rect x="198" y="0" width="54" height="16" rx="3" fill="#0f2c1a" stroke="#3fb950" stroke-width="1"/>
        <text x="225" y="11" text-anchor="middle" fill="#3fb950" font-size="10" font-weight="700">+2.831</text>'
$newLabel = '<rect x="218" y="28" width="54" height="16" rx="3" fill="#170d0d" stroke="#f85149" stroke-width="1"/>
        <text x="245" y="39" text-anchor="middle" fill="#f85149" font-size="10" font-weight="700">+2.831</text>'
$html = $html.Replace($oldLabel, $newLabel)
Write-Host "4. Label repositioned"

# 5. Update chart comment
$oldComment = '<!-- cumEV: -1.0,-2.0,-1.37,-2.37,-1.8,-1.267,-0.817,-0.437,-0.187,+0.213,+0.863,+2.393,+2.933,+1.933,+2.133,+2.671,+2.991,+3.261,+3.471,+3.831 -->'
$newComment = '<!-- cumEV: -1.0,-2.0,-1.37,-2.37,-1.8,-1.267,-0.817,-0.437,-0.187,+0.213,+0.863,+2.393,+2.933,+1.933,+2.133,+2.671,+2.991,+3.261,+3.471,+3.831,+2.831 (#21 Paolini MISS -1.0) -->'
$html = $html.Replace($oldComment, $newComment)
Write-Host "5. Chart comment updated"

[System.IO.File]::WriteAllText($path, $html, [System.Text.Encoding]::UTF8)
Write-Host "Part F (chart) complete."
