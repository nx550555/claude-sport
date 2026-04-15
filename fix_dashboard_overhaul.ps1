$base = "C:\Users\ohwada\Desktop\claude_sport"
$file = "$base\dashboard.html"
$content = [System.IO.File]::ReadAllText($file, [System.Text.Encoding]::UTF8)

# ========== 1. アクティブ推奨セクション全体置換 ==========
$activeStart = [System.IO.File]::ReadAllText("$base\dash_active_anchor_start.txt", [System.Text.Encoding]::UTF8)
$historyStart = [System.IO.File]::ReadAllText("$base\dash_history_anchor_start.txt", [System.Text.Encoding]::UTF8)
$newActive = [System.IO.File]::ReadAllText("$base\dash_new_active_section.txt", [System.Text.Encoding]::UTF8)

$startIdx = $content.IndexOf($activeStart)
$endIdx = $content.IndexOf($historyStart)

if ($startIdx -ge 0 -and $endIdx -gt $startIdx) {
    $content = $content.Substring(0, $startIdx) + $newActive + "`n`n" + $content.Substring($endIdx)
    Write-Host "  OK: active section replaced"
} else {
    Write-Host "  NG: active anchors not found ($startIdx, $endIdx)"
}

# ========== 2. ファネルタブボタン追加 (分析ログの後) ==========
$analysisTabAnchor = [System.IO.File]::ReadAllText("$base\dash_analysislog_anchor.txt", [System.Text.Encoding]::UTF8)
$funnelTabBtn = "onclick=`"showTab('analysislog')`">&#x1F50D; &#x5206;&#x6790;&#x30ED;&#x30B0;</div>`n  <div class=`"tab`" id=`"tab-funnel`" onclick=`"showTab('funnel')`">&#x1F52C; &#x30D5;&#x30A1;&#x30CD;&#x30EB;&#x5206;&#x6790;</div>"

if ($content.Contains($analysisTabAnchor)) {
    $content = $content.Replace($analysisTabAnchor, $funnelTabBtn)
    Write-Host "  OK: funnel tab button added"
} else {
    Write-Host "  NG: analysislog tab anchor not found"
}

# ========== 3. ファネルタブコンテンツ追加 (成長分析の前) ==========
$timelineAnchor = [System.IO.File]::ReadAllText("$base\dash_analysislog_content_anchor.txt", [System.Text.Encoding]::UTF8)
$funnelContent = [System.IO.File]::ReadAllText("$base\dash_funnel_content.txt", [System.Text.Encoding]::UTF8)

if ($content.Contains($timelineAnchor)) {
    $content = $content.Replace($timelineAnchor, $funnelContent + "`n" + $timelineAnchor)
    Write-Host "  OK: funnel content inserted"
} else {
    Write-Host "  NG: timeline anchor not found"
}

# ========== 4. 日報セクション置換 ==========
$dailyStart = [System.IO.File]::ReadAllText("$base\dash_dailyreport_anchor.txt", [System.Text.Encoding]::UTF8)
$rulesStart = [System.IO.File]::ReadAllText("$base\dash_rules_anchor.txt", [System.Text.Encoding]::UTF8)
$newDailyReport = [System.IO.File]::ReadAllText("$base\dash_new_dailyreport.txt", [System.Text.Encoding]::UTF8)

$dailyIdx = $content.IndexOf($dailyStart)
$rulesIdx = $content.IndexOf($rulesStart)

if ($dailyIdx -ge 0 -and $rulesIdx -gt $dailyIdx) {
    $content = $content.Substring(0, $dailyIdx) + $newDailyReport + "`n`n" + $content.Substring($rulesIdx)
    Write-Host "  OK: daily report replaced"
} else {
    Write-Host "  NG: daily report anchors not found ($dailyIdx, $rulesIdx)"
}

# ========== 5. 待機中 bs-val 5→8, bs-sub更新 ==========
$oldBsVal = '<div class="bs-val" style="color:#d29922;">5</div>'
$newBsVal = '<div class="bs-val" style="color:#d29922;">8</div>'
if ($content.Contains($oldBsVal)) {
    $content = $content.Replace($oldBsVal, $newBsVal)
    Write-Host "  OK: bs-val 5->8"
} else {
    Write-Host "  NG: bs-val not found"
}

$oldBsSub = '<div class="bs-sub">ATP W16 x3 + NRL R7 x2</div>'
$newBsSub = '<div class="bs-sub">ATP x3 + WTA x1 + NRL x2 + SL x2</div>'
if ($content.Contains($oldBsSub)) {
    $content = $content.Replace($oldBsSub, $newBsSub)
    Write-Host "  OK: bs-sub updated"
} else {
    Write-Host "  NG: bs-sub not found"
}

# ========== 6. showTab JS function: add 'funnel' case ==========
$oldShowTab = "function showTab(id){"
$newShowTab = "function showTab(id){
  document.querySelectorAll('.tab-content').forEach(el=>el.classList.remove('active'));
  document.querySelectorAll('.tab').forEach(el=>el.classList.remove('active'));
  var c=document.getElementById('content-'+id);
  var t=document.getElementById('tab-'+id);
  if(c)c.classList.add('active');
  if(t)t.classList.add('active');"
# Only patch if it has the old simple version
# Skip this - showTab should already work generically

[System.IO.File]::WriteAllText($file, $content, [System.Text.Encoding]::UTF8)
Write-Host "Done."
