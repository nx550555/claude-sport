$file = "C:\Users\ohwada\Desktop\claude_sport\BACKLOG.md"
$lines = Get-Content -Path $file -Encoding UTF8
# Update line 86 (index 85)
if ($lines[85] -match '^\- \[ \] ATP GO3') {
    $lines[85] = $lines[85] -replace '^\- \[ \]', '- [x]'
    Write-Host "Updated line 86"
}
$lines | Set-Content -Path $file -Encoding UTF8
Write-Host "Done"
