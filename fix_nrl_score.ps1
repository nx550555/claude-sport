$file = "C:\Users\ohwada\Desktop\claude_sport\dashboard.html"
$content = [System.IO.File]::ReadAllText($file, [System.Text.Encoding]::UTF8)

# Line 1837: Raiders 22-30 MISS -> Raiders 36-34 MISS
$content = $content.Replace("Raiders 22-30 MISS", "Raiders 36-34 MISS")

# Line 1936: Raiders 30-22 (ASCII anchor, Japanese follows)
$content = $content.Replace("Raiders 30-22", "Raiders 36-34")

# Line 2292: 30-22</span> (unique in span tag context)
$content = $content.Replace(">30-22</span>", ">36-34</span>")

[System.IO.File]::WriteAllText($file, $content, [System.Text.Encoding]::UTF8)
Write-Host "Done"
