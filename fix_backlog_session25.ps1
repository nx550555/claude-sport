$base = "C:\Users\ohwada\Desktop\claude_sport"
$file = "$base\BACKLOG.md"
$content = [System.IO.File]::ReadAllText($file, [System.Text.Encoding]::UTF8)

# 1. UPSET 5/12 -> 2/10
$old1 = "UPSET 5/12"
$new1 = "UPSET 2/10"
if ($content.Contains($old1)) {
    $content = $content.Replace($old1, $new1)
    Write-Host "  REPLACED: UPSET count"
} else {
    Write-Host "  NOTE: UPSET count not found"
}

# 2. Insert new section
$anchor = [System.IO.File]::ReadAllText("$base\backlog_anchor.txt", [System.Text.Encoding]::UTF8)
$insertContent = [System.IO.File]::ReadAllText("$base\backlog_insert.txt", [System.Text.Encoding]::UTF8)
if ($content.Contains($anchor)) {
    $content = $content.Replace($anchor, $insertContent + $anchor)
    Write-Host "  INSERTED: new session section"
} else {
    Write-Host "  NOT FOUND: anchor"
}

[System.IO.File]::WriteAllText($file, $content, [System.Text.Encoding]::UTF8)
Write-Host "All done."
