# Fix: content-active has 1 unclosed div - add missing </div> before history section
$path = "C:\Users\ohwada\Desktop\claude_sport\dashboard.html"
$html = [System.IO.File]::ReadAllText($path, [System.Text.Encoding]::UTF8)

# Verify the problem
$activeStart = $html.IndexOf('id="content-active"')
$historyStart = $html.IndexOf('id="content-history"')
$section = $html.Substring($activeStart, $historyStart - $activeStart)
$opens = ([regex]::Matches($section, '<div')).Count
$closes = ([regex]::Matches($section, '</div>')).Count
Write-Host "Before: open=$opens close=$closes diff=$($opens-$closes)"

# Find the history section marker (ASCII anchor: "content-history")
$anchor = 'id="content-history"'
$pos = $html.IndexOf($anchor)

# Go back to find the <div class="tab-content" that starts content-history
$tabContentBefore = $html.LastIndexOf('<div class="tab-content"', $pos)
Write-Host "Tab-content before pos: $tabContentBefore"

# Insert </div> right before that <div
$html = $html.Substring(0, $tabContentBefore) + '</div>' + [System.Environment]::NewLine + $html.Substring($tabContentBefore)

# Verify fix
$html2 = $html
$activeStart2 = $html2.IndexOf('id="content-active"')
$historyStart2 = $html2.IndexOf('id="content-history"')
$section2 = $html2.Substring($activeStart2, $historyStart2 - $activeStart2)
$opens2 = ([regex]::Matches($section2, '<div')).Count
$closes2 = ([regex]::Matches($section2, '</div>')).Count
Write-Host "After: open=$opens2 close=$closes2 diff=$($opens2-$closes2)"

[System.IO.File]::WriteAllText($path, $html, [System.Text.Encoding]::UTF8)
Write-Host "Fix applied and saved."
