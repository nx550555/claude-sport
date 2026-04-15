# Session 29 - Part E: Fix cumulative table (#20 + add #21 Paolini MISS)
$path = "C:\Users\ohwada\Desktop\claude_sport\dashboard.html"
$html = [System.IO.File]::ReadAllText($path, [System.Text.Encoding]::UTF8)

# Fix #20 Kopriva: cumulative should be +3.831 (before Paolini), hit rate 80%
# Anchor: unique "#20" in the cumulative table context
$anchor20 = '#20</td><td>2026-04-14</td>'
$pos20 = $html.IndexOf($anchor20)
if ($pos20 -ge 0) {
    # In that row: fix "+2.831" -> "+3.831"
    $idx = $html.IndexOf('+2.831</td>', $pos20)
    if ($idx -ge 0 -and $idx - $pos20 -lt 400) {
        $html = $html.Substring(0, $idx) + '+3.831</td>' + $html.Substring($idx + '+2.831</td>'.Length)
        Write-Host "20a. #20 cumulative +3.831 done"
    } else {
        Write-Host "20a. cumulative anchor not found after #20"
    }
    # Fix hit rate: "76.2%" -> "80.0%"
    $pos20b = $html.IndexOf($anchor20)
    $idx2 = $html.IndexOf('76.2%</td>', $pos20b)
    if ($idx2 -ge 0 -and $idx2 - $pos20b -lt 400) {
        $html = $html.Substring(0, $idx2) + '80.0%</td>' + $html.Substring($idx2 + '76.2%</td>'.Length)
        Write-Host "20b. #20 hit rate 80.0% done"
    }
    # Also fix color from f85149 to 3fb950 (positive rate)
} else {
    Write-Host "#20 anchor not found"
}

# Add #21 Paolini MISS row after #20 Kopriva row
# Anchor: the </tr> after the Kopriva row
$koprivaEnd = '#20</td><td>2026-04-14</td>'
$pos20c = $html.IndexOf($koprivaEnd)
if ($pos20c -ge 0) {
    $trEnd = $html.IndexOf('</tr>', $pos20c)
    if ($trEnd -ge 0) {
        $insertAt = $trEnd + '</tr>'.Length
        $newRow = @"

        <tr style="background:rgba(248,81,73,.04);"><td>#21</td><td>2026-04-15</td><td><span class="sport-tag" style="color:#f9a8d4;">&#x1F3BE; WTA</span></td><td style="font-size:12px;">Paolini J.(4) vs Sonmez Z. (Stuttgart R1)</td><td style="color:#f85149;font-weight:700;">&#x2717; MISS</td><td class="ev-neg">-1.000</td><td class="ev-pos">+2.831</td><td style="color:#e3b341;">76.2%</td></tr>
"@
        $html = $html.Substring(0, $insertAt) + $newRow + $html.Substring($insertAt)
        Write-Host "21. #21 Paolini MISS row added"
    }
} else {
    Write-Host "#20 row end not found"
}

[System.IO.File]::WriteAllText($path, $html, [System.Text.Encoding]::UTF8)
Write-Host "Part E (funnel fix) complete."
