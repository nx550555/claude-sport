$file = "C:\Users\ohwada\Desktop\claude_sport\dashboard.html"
$lines = Get-Content -Path $file -Encoding UTF8

# Line 1642 (index 1641): / 17 -> / 20 (HIT confirmed label)
if ($lines[1641] -match '/ 17') {
    $lines[1641] = $lines[1641] -replace '/ 17', '/ 20'
    Write-Host "L1642 OK: $($lines[1641].Trim())"
}

# Line 1647 (index 1646): / 17 -> / 20 (MISS confirmed label)
if ($lines[1646] -match '/ 17') {
    $lines[1646] = $lines[1646] -replace '/ 17', '/ 20'
    Write-Host "L1647 OK: $($lines[1646].Trim())"
}

$lines | Set-Content -Path $file -Encoding UTF8
Write-Host "Done"
