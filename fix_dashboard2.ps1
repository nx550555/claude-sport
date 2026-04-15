# fix_dashboard2.ps1
$f = 'C:\Users\ohwada\Desktop\claude_sport\dashboard.html'
$enc = [System.Text.Encoding]::UTF8
$content = [System.IO.File]::ReadAllText($f, $enc)

# 1. ヘッダー: GO 19件/待機 4件 → GO 21件/待機 6件
$ken = [char]0x4EF6
$kakutei = [char]0x78BA + [char]0x5B9A
$taiki = [char]0x5F85 + [char]0x6A5F
$content = $content.Replace('GO 19' + $ken + ' / ' + $kakutei + ' 15' + $ken + ' / ' + $taiki + ' 4' + $ken, 'GO 21' + $ken + ' / ' + $kakutei + ' 15' + $ken + ' / ' + $taiki + ' 6' + $ken)

# 2. 待機中サブテキスト
$old2 = '<div class="bs-sub">UFL Dallas + ATP 4/14 x3</div>'
$new2 = '<div class="bs-sub">UFL+ATP 4/14 x3 + NRL 4/18 x2</div>'
$content = $content.Replace($old2, $new2)

# 3. NRL カード GO回数: 1 → 3
$gokaisu = 'GO' + [char]0x56DE + [char]0x6570
$old3 = '<div class="sm-label">' + $gokaisu + '</div><div class="sm-val">1</div></div>' + [char]0x0A + '          <div class="sm"><div class="sm-label">' + [char]0x7D50 + [char]0x679C + [char]0x6E08
$new3 = '<div class="sm-label">' + $gokaisu + '</div><div class="sm-val">3</div></div>' + [char]0x0A + '          <div class="sm"><div class="sm-label">' + [char]0x7D50 + [char]0x679C + [char]0x6E08

# NRL block is identified by the -1.000 EV value which is unique
$old3b = '<div class="sm-val" style="color:#f85149;">-1.000</div></div>' + [char]0x0A + '          <div class="sm"><div class="sm-label">' + [char]0x5F85 + [char]0x6A5F + [char]0x4E2D + '</div><div class="sm-val" style="color:#8b949e;">0</div>'
$new3b = '<div class="sm-val" style="color:#f85149;">-1.000</div></div>' + [char]0x0A + '          <div class="sm"><div class="sm-label">' + [char]0x5F85 + [char]0x6A5F + [char]0x4E2D + '</div><div class="sm-val" style="color:#e3b341;">2</div>'
$content = $content.Replace($old3b, $new3b)

$bytes = $enc.GetBytes($content)
[System.IO.File]::WriteAllBytes($f, $bytes)
Write-Output "Done"
