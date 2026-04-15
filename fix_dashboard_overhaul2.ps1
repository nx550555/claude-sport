$base = "C:\Users\ohwada\Desktop\claude_sport"
$file = "$base\dashboard.html"
$content = [System.IO.File]::ReadAllText($file, [System.Text.Encoding]::UTF8)

$old = [System.IO.File]::ReadAllText("$base\dash_header_old.txt", [System.Text.Encoding]::UTF8)
$new = [System.IO.File]::ReadAllText("$base\dash_header_new.txt", [System.Text.Encoding]::UTF8)
if ($content.Contains($old)) {
    $content = $content.Replace($old, $new)
    Write-Host "  OK: header updated"
} else {
    Write-Host "  NG: header not found"
}

[System.IO.File]::WriteAllText($file, $content, [System.Text.Encoding]::UTF8)
Write-Host "Done."
