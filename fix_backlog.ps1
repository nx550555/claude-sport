$path = "C:\Users\ohwada\Desktop\claude_sport\BACKLOG.md"
$content = Get-Content $path -Encoding UTF8
$content = $content -replace '\[ \] UFL Week3 Dallas vs Columbus', '[x] UFL Week3 Dallas vs Columbus'
$content = $content -replace '\[ \] MC2026 F Alcaraz vs Sinner', '[x] MC2026 F Alcaraz vs Sinner'
Set-Content $path $content -Encoding UTF8
Write-Host "BACKLOG updated."
