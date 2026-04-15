# Session 29 - Part G: Final corrections
$path = "C:\Users\ohwada\Desktop\claude_sport\dashboard.html"
$html = [System.IO.File]::ReadAllText($path, [System.Text.Encoding]::UTF8)

# == 1. Header: "GO 27件 / 確定 15件 / 待機 8件" -> correct values ==
$html = $html.Replace('GO 27' + [char]0x4EF6 + ' / ' + [char]0x78BA + [char]0x5B9A + ' 15' + [char]0x4EF6 + ' / ' + [char]0x5F85 + [char]0x6A5F + ' 8' + [char]0x4EF6, 'PLACEHOLDER_HDR')
# Use IndexOf for Japanese-safe approach
$hdrAnchor = '/  ' + [char]0x78BA + [char]0x5B9A + ' 15'  # Won't work either

# Let's use the ASCII-only approach: the span containing "件 / 確定"
# The unique ASCII part in the header span: "GO 27"
$pos = $html.IndexOf('GO 27')
if ($pos -ge 0) {
    # Find the containing span end
    $spanEnd = $html.IndexOf('</span>', $pos)
    if ($spanEnd -ge 0 -and $spanEnd - $pos -lt 60) {
        $oldSpanContent = $html.Substring($pos, $spanEnd - $pos)
        Write-Host "Found header content: $oldSpanContent"
        # Replace this entire span content
        $newContent = 'GO 27' + [char]0x4EF6 + ' / ' + [char]0x78BA + [char]0x5B9A + ' 21' + [char]0x4EF6 + ' / ' + [char]0x5F85 + [char]0x6A5F + ' 6' + [char]0x4EF6
        $html = $html.Substring(0, $pos) + $newContent + $html.Substring($spanEnd)
        Write-Host "1. Header fixed"
    }
} else {
    Write-Host "1. GO 27 not found in header"
}

# == 2. Pred tracking: "16 / 20 確定" -> "16 / 21 確定" ==
$html = $html.Replace('16 / 20 ' + [char]0x78BA + [char]0x5B9A, '16 / 21 ' + [char]0x78BA + [char]0x5B9A)
Write-Host "2. Pred tracking: 16/21 done"

# == 3. WTA pred row: "1 / 1" -> "1 / 2" (Paolini MISS added, 1 HIT / 2 confirmed) ==
# But wait - GB001 Ostapenko was the 1 WTA HIT; Paolini is now a MISS. So WTA = 1 HIT / 2 confirmed = 50%
# Check current WTA row
$wtaPos = $html.IndexOf('>WTA<')
if ($wtaPos -ge 0) {
    $wtaEnd = $html.IndexOf('</div>', $wtaPos)
    $wtaSnippet = $html.Substring($wtaPos, [Math]::Min(200, $wtaEnd - $wtaPos))
    Write-Host "WTA pred row: $wtaSnippet"
}

# == 4. Chart label: verify current state ==
$chartLabel = $html.IndexOf('+2.831</text>')
Write-Host "4. Chart label at: $chartLabel"

[System.IO.File]::WriteAllText($path, $html, [System.Text.Encoding]::UTF8)
Write-Host "Part G complete."
