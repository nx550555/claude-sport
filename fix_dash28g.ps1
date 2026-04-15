$file = "C:\Users\ohwada\Desktop\claude_sport\dashboard.html"
$lines = Get-Content -Path $file -Encoding UTF8

# Funnel summary: L1 box ~41 -> ~46
if ($lines[1623] -match '~41') {
    $lines[1623] = $lines[1623] -replace '~41', '~46'
    Write-Host "L1624 OK"
}

# Funnel summary: HIT box 13 -> 16
if ($lines[1640] -match '>13<') {
    $lines[1640] = $lines[1640] -replace '>13<', '>16<'
    Write-Host "L1641 OK"
}

# Funnel summary: /17 -> /20 (HIT row)
if ($lines[1641] -match '>17<') {
    $lines[1641] = $lines[1641] -replace '>17<', '>20<'
    Write-Host "L1642 OK"
}

# Funnel summary: /17 -> /20 (MISS row)
if ($lines[1646] -match '>17<') {
    $lines[1646] = $lines[1646] -replace '>17<', '>20<'
    Write-Host "L1647 OK"
}

# Funnel summary note: 40.6% (41/101) -> 45.5% (46/101)
if ($lines[1649] -match '40\.6%') {
    $lines[1649] = $lines[1649] -replace '40\.6% \(41/101\)', '45.5% (46/101)'
    Write-Host "L1650 OK"
}

# W16 R1 row: confirmed 0 -> 3
if ($lines[1689] -match 'text-align:right;">0<') {
    $lines[1689] = $lines[1689] -replace 'text-align:right;">0<', 'text-align:right;">3<'
    Write-Host "L1690 OK"
}

# W16 R1 row: HIT em-dash -> 3 green
if ($lines[1690] -match '&#x2014;') {
    $lines[1690] = '          <td style="text-align:right;color:#3fb950;font-weight:600;">3</td>'
    Write-Host "L1691 OK"
}

# W16 R1 row: MISS em-dash -> 0
if ($lines[1691] -match '&#x2014;') {
    $lines[1691] = '          <td style="text-align:right;color:var(--text2);">0</td>'
    Write-Host "L1692 OK"
}

# W16 R1 row: pending 3 orange -> 0 grey
if ($lines[1692] -match 'color:#d29922;">3<') {
    $lines[1692] = $lines[1692] -replace 'color:#d29922;">3<', 'color:var(--text2);">0<'
    Write-Host "L1693 OK"
}

$lines | Set-Content -Path $file -Encoding UTF8
Write-Host "Done"
