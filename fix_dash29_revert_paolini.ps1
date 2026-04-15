# Revert Paolini MISS -> PENDING (match not confirmed: 1st Set Suspended as of 2026-04-15)
$path = "C:\Users\ohwada\Desktop\claude_sport\dashboard.html"
$html = [System.IO.File]::ReadAllText($path, [System.Text.Encoding]::UTF8)

# == 1. Big stats: 76.2% -> 80.0%, 16HIT/21 -> 16HIT/20, +2.831 -> +3.831 ==
$html = $html.Replace('>76.2%<', '>80.0%<')
$html = $html.Replace('16HIT / 21', '16HIT / 20')
# +2.831 appears in: big-stat div, cumulative #21 (will be removed), chart SVG label
# Replace all instances of ">+2.831<" back to ">+3.831<"
$html = $html.Replace('>+2.831<', '>+3.831<')
Write-Host "1. Big stats reverted"

# == 2. Header: 確定 21件 -> 20件, 待機 6件 -> 7件 ==
$html = $html.Replace('/ ' + [char]0x78BA + [char]0x5B9A + ' 21' + [char]0x4EF6, '/ ' + [char]0x78BA + [char]0x5B9A + ' 20' + [char]0x4EF6)
$html = $html.Replace('/ ' + [char]0x5F85 + [char]0x6A5F + ' 6' + [char]0x4EF6, '/ ' + [char]0x5F85 + [char]0x6A5F + ' 7' + [char]0x4EF6)
Write-Host "2. Header reverted"

# == 3. WTA sport card: -0.462 -> +0.538, 50.0% -> 100% ==
$html = $html.Replace('>-0.462<', '>+0.538<')
# 50.0% -> 100% in WTA card context: use the f9a8d4 color anchor
$html = $html -replace '(f9a8d4.*?color:#3fb950;">)50\.0%(</div>)', '${1}100%${2}'
Write-Host "3. WTA sport card reverted"

# == 4. WTA pred tracking: 1/2 50% -> 1/1 100% ==
$html = $html.Replace('<span>WTA</span><span>1 / 2</span><span style="color:#e3b341;">50%</span>', '<span>WTA</span><span>1 / 1</span><span style="color:#3fb950;">100%</span>')
Write-Host "4. WTA pred tracking reverted"

# == 5. Pred tracking overall: 16/21 -> 16/20 ==
$html = $html.Replace('16 / 21 ' + [char]0x78BA + [char]0x5B9A, '16 / 20 ' + [char]0x78BA + [char]0x5B9A)
Write-Host "5. Pred tracking count reverted"

# == 6. Active section: Paolini MISS card -> PENDING card ==
# Use comment anchor
$missCardStart = $html.IndexOf('<!-- WTA Stuttgart Paolini MISS')
$nextCardStart = $html.IndexOf('<!-- ATP MC Final SKIP -->', $missCardStart)
if ($missCardStart -ge 0 -and $nextCardStart -ge 0) {
    $pendingCard = @"
    <!-- WTA Stuttgart Paolini PENDING (result suspended, 2026-04-15) -->
    <div class="active-card" style="border-color:#f9a8d460;background:linear-gradient(135deg,#f9a8d408,transparent);opacity:.85;">
      <div class="ac-sport">&#x1F3BE; WTA &mdash; Stuttgart R1 2026 <span class="badge badge-go">GO</span></div>
      <div class="ac-match">&#x30BD;&#x30F3;&#x30E1;&#x30BA; Z. vs &#x30D1;&#x30AA;&#x30EA;&#x30FC;&#x30CB; J.(4)</div>
      <div class="ac-rec">&#x63A8;&#x5968;: <strong style="color:#3fb950;">&#x30D1;&#x30AA;&#x30EA;&#x30FC;&#x30CB;&#x30FB;&#x30B8;&#x30A1;&#x30B9;&#x30DF;&#x30F3;</strong></div>
      <div class="ac-metrics">
        <div class="acm"><div class="acm-l">&#x30AA;&#x30C3;&#x30BA;</div><div class="acm-v odds">1.24</div></div>
        <div class="acm"><div class="acm-l">&#x4E88;&#x6E2C;EV</div><div class="acm-v ev">+5.4%</div></div>
        <div class="acm"><div class="acm-l">&#x78BA;&#x4FE1;&#x5EA6;</div><div class="acm-v">85%</div></div>
        <div class="acm"><div class="acm-l">cElo&#x5DEE;</div><div class="acm-v rule">+300pt</div></div>
      </div>
      <div class="ac-note">&#x26A0;&#xFE0F; 4/15 1st Set&#x4E2D;&#x65AD;&#x4E2D;&#xFF08;&#x305F;&#x3060;&#x3057;&#x7D50;&#x679C;&#x672A;&#x78BA;&#x8A8D;&#xFF09;&#x3002;Stuttgart indoor clay&#x3002;cElo&#x5DEE;300pt&#x3002;&#x7D50;&#x679C;&#x5F85;&#x6A5F;&#x3002;</div>
      <div class="ac-date">&#x1F4C5; 2026-04-15 JST &mdash; Stuttgart R1 &#x23F3; PENDING</div>
    </div>

"@
    $html = $html.Substring(0, $missCardStart) + $pendingCard + $html.Substring($nextCardStart)
    Write-Host "6. Paolini active card: MISS -> PENDING"
} else {
    Write-Host "6. Paolini MISS card anchor not found"
}

# == 7. Main history table: Paolini MISS row -> PENDING ==
# Anchor: "Stuttgart R1 2026" + "Paolini J.(4) vs Sonmez Z."
$paoPos = $html.IndexOf('Stuttgart R1 2026</td>')
if ($paoPos -ge 0) {
    # Find badge-miss near this position
    $missIdx = $html.IndexOf('badge-miss">&#x2717; MISS</span>', $paoPos)
    if ($missIdx -ge 0 -and $missIdx - $paoPos -lt 500) {
        $html = $html.Substring(0, $missIdx) + 'badge-pending">PENDING</span>' + $html.Substring($missIdx + 'badge-miss">&#x2717; MISS</span>'.Length)
        Write-Host "7a. Main history Paolini badge: MISS -> PENDING"
    }
    # Change result cell: "Sonmez win" -> "--"
    $sonmezWin = $html.IndexOf('>Sonmez win<', $paoPos)
    if ($sonmezWin -ge 0 -and $sonmezWin - $paoPos -lt 600) {
        $html = $html.Substring(0, $sonmezWin) + '>&#x2014;<' + $html.Substring($sonmezWin + '>Sonmez win<'.Length)
        Write-Host "7b. Main history result: Sonmez win -> --"
    }
    # Change actual EV cell: -1.000 -> -- (but only the one near Paolini)
    $evNegPos = $html.IndexOf('ev-neg">-1.000</td>', $paoPos)
    if ($evNegPos -ge 0 -and $evNegPos - $paoPos -lt 700) {
        $html = $html.Substring(0, $evNegPos) + 'color:#8b949e;">&#x2014;</td>' + $html.Substring($evNegPos + 'ev-neg">-1.000</td>'.Length)
        Write-Host "7c. Main history EV: -1.000 -> --"
    }
    # Change row background from red to green
    $rowBg = $html.LastIndexOf('background:rgba(248,81,73,.04)', $paoPos)
    if ($rowBg -ge 0 -and $paoPos - $rowBg -lt 200) {
        $html = $html.Substring(0, $rowBg) + 'background:rgba(46,160,67,.06)' + $html.Substring($rowBg + 'background:rgba(248,81,73,.04)'.Length)
        Write-Host "7d. Main history row color: red -> green"
    }
    # Change red Paolini text to green
    $redPao = $html.IndexOf('color:#f85149;font-weight:600;">Paolini</td>', $paoPos)
    if ($redPao -ge 0 -and $redPao - $paoPos -lt 400) {
        $html = $html.Substring(0, $redPao) + 'color:#3fb950;font-weight:600;">Paolini</td>' + $html.Substring($redPao + 'color:#f85149;font-weight:600;">Paolini</td>'.Length)
        Write-Host "7e. Main history Paolini color: red -> green"
    }
} else {
    Write-Host "7. Stuttgart R1 anchor not found"
}

# == 8. Cumulative table #21: remove Paolini MISS row ==
$row21 = '<tr style="background:rgba(248,81,73,.04);"><td>#21</td><td>2026-04-15</td>'
$row21End = $html.IndexOf('</tr>', $html.IndexOf($row21))
if ($html.IndexOf($row21) -ge 0 -and $row21End -ge 0) {
    $startIdx = $html.IndexOf($row21)
    $endIdx = $row21End + '</tr>'.Length
    $html = $html.Substring(0, $startIdx) + $html.Substring($endIdx)
    Write-Host "8. Cumulative #21 row removed"
} else {
    Write-Host "8. #21 row not found"
}

# == 9. Chart: revert polygon/polyline to remove Paolini point ==
# Revert polygon: "251,2 262,26 262,100 44,100" -> "251,2 251,100 44,100"
$html = $html.Replace('251,2 262,26 262,100 44,100', '251,2 251,100 44,100')
# Revert polyline: remove "262,26" from end
$html = $html.Replace('240,9 251,2 262,26" fill="none"', '240,9 251,2" fill="none"')
# Revert circles: remove Paolini circle, restore Kopriva as last big circle
$html = $html.Replace('<circle cx="251" cy="2"   r="2.5" fill="#3fb950" opacity="0.9"/><circle cx="262" cy="26"  r="4"   fill="#f85149" stroke="#0d1117" stroke-width="1.5"/>', '<circle cx="251" cy="2"   r="4"   fill="#3fb950" stroke="#0d1117" stroke-width="1.5"/>')
# Revert chart label (was repositioned to red/262 position but failed, so just fix text)
# The label still shows +2.831 (now changed to +3.831 by step 1 above)
Write-Host "9. Chart reverted"

# == 10. Chart comment: remove Paolini point ==
$html = $html.Replace(',+2.831 (#21 Paolini MISS -1.0) -->', ' -->')
Write-Host "10. Chart comment reverted"

# == 11. Screening sub-table: revert MISS -> PENDING ==
$html = $html.Replace('MISS &#x2014; Sonmez win (data contamination confirmed)</strong>', 'PENDING 4/15 &#x2014; 1st Set&#x4E2D;&#x65AD;&#x4E2D;&#xFF08;&#x7D50;&#x679C;&#x672A;&#x78BA;&#x8A8D;&#xFF09;</strong>')
Write-Host "11. Screening sub-table reverted"

# == 12. Daily report: fix Paolini line ==
$html = $html.Replace('WTAデータ汚染確認: 2026-04-15.jsonの6試合は4/13済み。Paolini推奨 → MISSPlaceholder', 'PLACEHOLDER')
# Use ASCII-only anchor: the specific HTML entity sequence in that line
$paoliniDailyOld = 'Paolini&#x63A8;&#x5968; &#x2192; <span style="color:#f85149;">MISS</span>&#xFF08;Sonmez&#x52DD;&#x5229;&#xFF09;<br>'
$paoliniDailyNew = 'Paolini&#x63A8;&#x5968; &#x2192; <span style="color:#e3b341;">PENDING</span>&#xFF08;4/15 1st Set&#x4E2D;&#x65AD;&#x4E2D;&#x3001;&#x7D50;&#x679C;&#x672A;&#x78BA;&#x8A8D;&#xFF09;<br>'
$html = $html.Replace($paoliniDailyOld, $paoliniDailyNew)
Write-Host "12. Daily report Paolini line reverted"

[System.IO.File]::WriteAllText($path, $html, [System.Text.Encoding]::UTF8)
Write-Host "Paolini revert complete."
