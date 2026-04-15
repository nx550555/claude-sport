$file = "C:\Users\ohwada\Desktop\claude_sport\dashboard.html"
$lines = Get-Content -Path $file -Encoding UTF8

# Line 239: 17件 -> 20件 (index 238)
$lines[238] = $lines[238] -replace '17件', '20件'
Write-Host "L239: $($lines[238].Trim())"

# Line 244: 13HIT / 17試合 -> 16HIT / 20試合 (index 243)
$lines[243] = $lines[243] -replace '13HIT', '16HIT' -replace '17試合', '20試合'
Write-Host "L244: $($lines[243].Trim())"

# Line 2876: 76.5% -> 80.0% and 13 / 17 -> 16 / 20 (index 2875)
$lines[2875] = $lines[2875] -replace '76\.5%', '80.0%' -replace '13 / 17', '16 / 20'
Write-Host "L2876: $($lines[2875].Trim())"

# Line 2138: update history summary (index 2137)
$lines[2137] = $lines[2137] -replace 'UFL確定後 13/17 \(76\.5%\)', 'W16 ATP後 16/20 (80.0%)'
Write-Host "L2138: $($lines[2137].Trim())"

# Line 2139: update EV (index 2138)
$lines[2138] = $lines[2138] -replace '\+2\.991u', '+3.831u'
Write-Host "L2139: $($lines[2138].Trim())"

# Line 1650: 76.5% (13/17) -> 80.0% (16/20) (index 1649)
$lines[1649] = $lines[1649] -replace '76\.5% \(13/17\)', '80.0% (16/20)'
Write-Host "L1650: $($lines[1649].Trim())"

$lines | Set-Content -Path $file -Encoding UTF8
Write-Host "Done"
