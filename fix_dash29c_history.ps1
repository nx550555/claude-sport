# Session 29 - Part C: History table updates (IndexOf approach, CRLF-safe)
$path = "C:\Users\ohwada\Desktop\claude_sport\dashboard.html"
$html = [System.IO.File]::ReadAllText($path, [System.Text.Encoding]::UTF8)

function ReplaceAfter($html, $anchor, $oldStr, $newStr) {
    $pos = $html.IndexOf($anchor)
    if ($pos -lt 0) { Write-Host "ANCHOR NOT FOUND: $anchor"; return $html }
    $searchFrom = $pos
    $idx = $html.IndexOf($oldStr, $searchFrom)
    if ($idx -lt 0 -or $idx - $pos -gt 800) { Write-Host "TARGET NOT FOUND after anchor: $anchor"; return $html }
    return $html.Substring(0, $idx) + $newStr + $html.Substring($idx + $oldStr.Length)
}

function InsertAfter($html, $anchor, $insertStr) {
    $pos = $html.IndexOf($anchor)
    if ($pos -lt 0) { Write-Host "ANCHOR NOT FOUND: $anchor"; return $html }
    $insertAt = $pos + $anchor.Length
    return $html.Substring(0, $insertAt) + $insertStr + $html.Substring($insertAt)
}

$PENDING = '<span class="badge badge-pending">PENDING</span>'
$REVOKED = '<span class="badge badge-skip">REVOKED</span>'
$SKIP    = '<span class="badge badge-skip">SKIP</span>'
$GO_BADGE = '<span class="badge badge-go">GO</span>'

# == 1. Broncos: PENDING -> REVOKED ==
$html = ReplaceAfter $html "Wests Tigers vs Brisbane Broncos" $PENDING $REVOKED
# Also gray out the recommendation text
$html = ReplaceAfter $html "Wests Tigers vs Brisbane Broncos" 'color:#3fb950;font-weight:600;">Broncos' 'color:#8b949e;font-weight:600;">Broncos'
# Change row background from green to gray
$broncoRowStart = $html.IndexOf("Wests Tigers vs Brisbane Broncos") - 300
$broncoRowBg = $html.IndexOf('background:rgba(46,160,67,.06)', [Math]::Max(0,$broncoRowStart))
if ($broncoRowBg -ge 0 -and $broncoRowBg - ($html.IndexOf("Wests Tigers vs Brisbane Broncos")) -lt 0) {
    $html = $html.Substring(0, $broncoRowBg) + 'background:rgba(48,54,61,.3);opacity:.7' + $html.Substring($broncoRowBg + 'background:rgba(46,160,67,.06)'.Length)
}
Write-Host "1. Broncos: REVOKED done"

# == 2. Panthers: PENDING -> SKIP ==
$html = ReplaceAfter $html "Penrith Panthers vs Dolphins" $PENDING $SKIP
$html = ReplaceAfter $html "Penrith Panthers vs Dolphins" 'color:#d29922;font-weight:600;">Panthers' 'color:#8b949e;font-weight:600;">Panthers'
Write-Host "2. Panthers: SKIP done"

# == 3. Rabbitohs vs Dragons: PENDING -> SKIP ==
$html = ReplaceAfter $html "South Sydney Rabbitohs vs St George Illawarra Dragons" $PENDING $SKIP
$html = ReplaceAfter $html "South Sydney Rabbitohs vs St George Illawarra Dragons" 'color:#d29922;font-weight:600;">Rabbitohs' 'color:#8b949e;font-weight:600;">Rabbitohs'
Write-Host "3. Rabbitohs vs Dragons: SKIP done"

# == 4. Insert new rows after Warriors row ==
# Find the end of Warriors row: the unique ">Warriors</td>" cell followed by 1.22
# Use the closing </tr> after the Warriors PENDING cell
# Anchor = the last &#x2014;</td>\n        </tr> after Warriors context
$warriorsAnchor = "NZ Warriors vs Gold Coast Titans"
$warriorsPos = $html.IndexOf($warriorsAnchor)
if ($warriorsPos -ge 0) {
    # Find the next </tr> after Warriors row
    $trEnd = $html.IndexOf("</tr>", $warriorsPos + $warriorsAnchor.Length)
    if ($trEnd -ge 0) {
        $insertAt = $trEnd + "</tr>".Length
        $newRows = @"

        <tr style="background:rgba(46,160,67,.06);">
          <td>2026-04-19</td>
          <td><span class="sport-tag" style="color:#bfdbfe;">&#x1F3C9; SL</span></td>
          <td style="font-size:12px;">Super League R8</td>
          <td class="match-cell">Catalans Dragons vs Warrington Wolves</td>
          <td><span class="badge badge-go">GO</span></td>
          <td style="color:#3fb950;font-weight:600;">Warrington</td>
          <td style="color:#e3b341;">1.65</td>
          <td class="ev-pos">+32.0%</td>
          <td>80%</td>
          <td><span class="badge badge-pending">PENDING</span></td>
          <td style="color:#8b949e;">&#x2014;</td>
          <td style="color:#8b949e;">&#x2014;</td>
        </tr>
        <tr style="background:rgba(46,160,67,.06);">
          <td>2026-04-18</td>
          <td><span class="sport-tag" style="color:#bfdbfe;">&#x1F3C9; SL</span></td>
          <td style="font-size:12px;">Super League R8</td>
          <td class="match-cell">Huddersfield Giants vs Leeds Rhinos</td>
          <td><span class="badge badge-go">GO</span></td>
          <td style="color:#3fb950;font-weight:600;">Leeds Rhinos</td>
          <td style="color:#e3b341;">1.32</td>
          <td class="ev-pos">+14.8%</td>
          <td>87%</td>
          <td><span class="badge badge-pending">PENDING</span></td>
          <td style="color:#8b949e;">&#x2014;</td>
          <td style="color:#8b949e;">&#x2014;</td>
        </tr>
        <tr style="background:rgba(46,160,67,.06);">
          <td>2026-04-17</td>
          <td><span class="sport-tag" style="color:#fca5a5;">&#x1F3C8; UFL</span></td>
          <td style="font-size:12px;">UFL 2026 Week 4</td>
          <td class="match-cell">Houston Gamblers vs Louisville Kings</td>
          <td><span class="badge badge-go">GO</span></td>
          <td style="color:#3fb950;font-weight:600;">Louisville Kings</td>
          <td style="color:#e3b341;">1.65</td>
          <td class="ev-pos">+35.3%</td>
          <td>82%</td>
          <td><span class="badge badge-pending">PENDING</span></td>
          <td style="color:#8b949e;">&#x2014;</td>
          <td style="color:#8b949e;">&#x2014;</td>
        </tr>
        <tr style="background:rgba(46,160,67,.06);">
          <td>2026-04-16</td>
          <td><span class="sport-tag" style="color:#79c0ff;">&#x1F3BE; ATP</span></td>
          <td style="font-size:12px;">Barcelona R2 2026</td>
          <td class="match-cell">Moutet C. vs Musetti L.(2)</td>
          <td><span class="badge badge-go">GO</span></td>
          <td style="color:#3fb950;font-weight:600;">Musetti</td>
          <td style="color:#e3b341;">1.37</td>
          <td class="ev-pos">+6.9%</td>
          <td>78%</td>
          <td><span class="badge badge-pending">PENDING</span></td>
          <td style="color:#8b949e;">&#x2014;</td>
          <td style="color:#8b949e;">&#x2014;</td>
        </tr>
        <tr style="background:rgba(46,160,67,.06);">
          <td>2026-04-15</td>
          <td><span class="sport-tag" style="color:#f9a8d4;">&#x1F3BE; WTA</span></td>
          <td style="font-size:12px;">WTA Rouen R1</td>
          <td class="match-cell">Tan H. vs Bondar A.</td>
          <td><span class="badge badge-go">GO</span></td>
          <td style="color:#3fb950;font-weight:600;">Bondar</td>
          <td style="color:#e3b341;">1.21</td>
          <td class="ev-pos">+6.5%</td>
          <td>88%</td>
          <td><span class="badge badge-pending">PENDING</span></td>
          <td style="color:#8b949e;">&#x2014;</td>
          <td style="color:#8b949e;">&#x2014;</td>
        </tr>
        <tr style="background:rgba(248,81,73,.04);">
          <td>2026-04-15</td>
          <td><span class="sport-tag" style="color:#f9a8d4;">&#x1F3BE; WTA</span></td>
          <td style="font-size:12px;">Stuttgart R1 2026</td>
          <td class="match-cell">Paolini J.(4) vs Sonmez Z.</td>
          <td><span class="badge badge-go">GO</span></td>
          <td style="color:#f85149;font-weight:600;">Paolini</td>
          <td style="color:#e3b341;">1.24</td>
          <td class="ev-pos">+5.4%</td>
          <td>85%</td>
          <td><span class="badge badge-miss">&#x2717; MISS</span></td>
          <td style="color:#f85149;">Sonmez win</td>
          <td class="ev-neg">-1.000</td>
        </tr>
"@
        $html = $html.Substring(0, $insertAt) + $newRows + $html.Substring($insertAt)
        Write-Host "4. New rows inserted after Warriors"
    }
} else {
    Write-Host "4. Warriors anchor NOT FOUND"
}

# == 5. Small screening table: Paolini PENDING -> MISS ==
$html = $html.Replace("PENDING 4/15 21:30 JST</strong>", "MISS &#x2014; Sonmez win (data contamination confirmed)</strong>")
Write-Host "5. Paolini small table: done"

[System.IO.File]::WriteAllText($path, $html, [System.Text.Encoding]::UTF8)
Write-Host "Part C complete."
