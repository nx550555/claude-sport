$file = "C:\Users\ohwada\Desktop\claude_sport\BACKLOG.md"
$lines = Get-Content -Path $file -Encoding UTF8
# Line 62 (index 61) and line 86 (index 85)
for ($i = 0; $i -lt $lines.Length; $i++) {
    if ($lines[$i] -match '^\- \[ \] ATP Munich GO3') {
        $lines[$i] = $lines[$i] -replace '^\- \[ \]', '- [x]'
        Write-Host "Updated line $($i+1): $($lines[$i])"
    }
    if ($lines[$i] -match '^\- \[ \] ATP GO3.*Musetti.*進行中') {
        $lines[$i] = $lines[$i] -replace '^\- \[ \]', '- [x]'
        Write-Host "Updated line $($i+1): $($lines[$i])"
    }
}
$lines | Set-Content -Path $file -Encoding UTF8
Write-Host "BACKLOG updated"
