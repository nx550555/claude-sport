$file = "C:\Users\ohwada\Desktop\claude_sport\dashboard.html"
$lines = Get-Content -Path $file -Encoding UTF8

# Line 239 (index 238): change 17 to 20 in the confirmation count line
if ($lines[238] -match 'bs-sub.*17') {
    $lines[238] = $lines[238] -replace '17([^H])', '20$1'
    Write-Host "L239 updated"
}

# Line 244 (index 243): change 13HIT/17 to 16HIT/20
if ($lines[243] -match '13HIT') {
    $lines[243] = $lines[243] -replace '13HIT', '16HIT'
    $lines[243] = $lines[243] -replace '/ 17', '/ 20'
    Write-Host "L244 updated"
}

# Line 2876 (index 2875): pred panel stats
if ($lines[2875] -match '76\.5%') {
    $lines[2875] = $lines[2875] -replace '76\.5%', '80.0%'
    $lines[2875] = $lines[2875] -replace '13 / 17', '16 / 20'
    Write-Host "L2876 updated"
}

# Line 2138 (index 2137): history tab summary - UFL to W16ATP
if ($lines[2137] -match '13/17') {
    $lines[2137] = $lines[2137] -replace '13/17 \(76\.5%\)', '16/20 (80.0%)'
    $lines[2137] = $lines[2137] -replace 'UFL.*?13/17', 'W16 ATP 16/20'
    Write-Host "L2138 updated"
}

# Line 2139 (index 2138): EV total
if ($lines[2138] -match '2\.991u') {
    $lines[2138] = $lines[2138] -replace '2\.991u', '3.831u'
    Write-Host "L2139 updated"
}

# Line 1650 (index 1649): prediction accuracy text
if ($lines[1649] -match '76\.5%') {
    $lines[1649] = $lines[1649] -replace '76\.5% \(13/17\)', '80.0% (16/20)'
    Write-Host "L1650 updated"
}

$lines | Set-Content -Path $file -Encoding UTF8
Write-Host "Done"
