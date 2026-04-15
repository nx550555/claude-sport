# Session 29 - Part D: Analysis log chip + daily report
$path = "C:\Users\ohwada\Desktop\claude_sport\dashboard.html"
$html = [System.IO.File]::ReadAllText($path, [System.Text.Encoding]::UTF8)

# == 1. Insert Session 29 chip at top of analysis log chips ==
# Anchor: opening of the flex container (unique line)
$chipAnchor = '<div style="display:flex;gap:10px;flex-wrap:wrap;margin-bottom:20px;">'
$chipPos = $html.IndexOf($chipAnchor)
if ($chipPos -ge 0) {
    $insertAt = $chipPos + $chipAnchor.Length
    $newChip = @"

      <div style="background:var(--surface);border:1px solid #3fb95040;border-radius:8px;padding:10px 14px;font-size:12px;min-width:160px;">
        <div style="color:#3fb950;font-size:10px;text-transform:uppercase;margin-bottom:4px;">Session _29 4/15 &#x5168;&#x30B9;&#x30DD;&#x30FC;&#x30C4;&#x30EC;&#x30D3;&#x30E5;&#x30FC;</div>
        <div>ATP R2 <span style="color:#3fb950;">GO 1</span>(Musetti) &nbsp;|&nbsp; WTA Rouen <span style="color:#3fb950;">GO 1</span>(Bondar) &nbsp;|&nbsp; UFL W4 <span style="color:#3fb950;">GO 1</span>(Louisville) &nbsp;|&nbsp; <span style="color:#f85149;">NRL Broncos REVOKED</span> &nbsp;|&nbsp; <span style="color:#d29922;">SL Warrington EV&#x4FEE;&#x6B63; 40.3&#x2192;32.0%</span></div>
      </div>
"@
    $html = $html.Substring(0, $insertAt) + $newChip + $html.Substring($insertAt)
    Write-Host "1. Session 29 chip inserted"
} else {
    Write-Host "1. Chip container anchor NOT FOUND"
}

# == 2. Add session 29 entry to daily report tab ==
# Find the daily report section
$dailyAnchor = 'id="content-dailyreport"'
$dailyPos = $html.IndexOf($dailyAnchor)
if ($dailyPos -ge 0) {
    # Find the first <div class="section"> after the dailyreport tab
    $sectionStart = $html.IndexOf('<div class="section">', $dailyPos)
    if ($sectionStart -ge 0) {
        $insertAt = $sectionStart + '<div class="section">'.Length
        $newEntry = @"

    <!-- Session 29 -->
    <div style="border:1px solid #3fb95040;border-radius:8px;padding:14px;margin-bottom:14px;background:rgba(46,160,67,.04);">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
        <div style="font-size:13px;font-weight:700;">2026-04-15 _29 &#x2014; &#x5168;&#x30B9;&#x30DD;&#x30FC;&#x30C4;&#x30EC;&#x30D3;&#x30E5;&#x30FC; + WTA&#x65B0;&#x8A18;&#x9332;</div>
        <div><span class="badge badge-go" style="font-size:10px;">GO 3</span></div>
      </div>
      <div style="font-size:12px;color:var(--text2);line-height:1.8;">
        &#x30FB; ATP Barcelona R2: Musetti vs Moutet &#x2014; cElo&#x5DEE;271pt, conf 78%(&#x8A0E;&#x50B7;-5%), EV+6.9% @1.37 <span style="color:#3fb950;font-weight:600;">GO</span><br>
        &#x30FB; WTA Rouen: Bondar vs Tan &#x2014; &#x5E02;&#x5834;implied 82.6%+&#x30D5;&#x30A9;&#x30FC;&#x30E0;&#x88DC;&#x6B63;=88%, EV+6.5% @1.21 <span style="color:#3fb950;font-weight:600;">GO</span><br>
        &#x30FB; UFL W4: Louisville Kings vs Houston &#x2014; QB&#x5DEE;+&#x6226;&#x529B;&#x5DEE;, conf 82%, EV+35.3% @1.65 <span style="color:#3fb950;font-weight:600;">GO</span><br>
        &#x30FB; NRL: Broncos <span style="color:#f85149;font-weight:600;">REVOKED</span>&#xFF08;Luai&#x5FA9;&#x5E30;+Carrigan&#x6B20;&#x5834;&#x30FB;&#x5E02;&#x5834;69%Tigers&#x6709;&#x5229;&#xFF09;, Panthers/Rabbitohs SKIP&#xFF08;&#x30AA;&#x30C3;&#x30BA;&#x53F3;&#x7AEF;&#xFF09;<br>
        &#x30FB; SL Warrington: Tanginoa+Yates OUT &#x2192; conf 85&#x2192;80%, EV 40.3&#x2192;32.0%&#xFF08;&#x5F15;&#x304D;&#x7D9A;&#x304D;GO&#xFF09;<br>
        &#x30FB; WTA Stuttgart&#x6C5A;&#x67D3;&#x78BA;&#x8A8D;: 2026-04-15.json&#x306E;6&#x8A66;&#x5408;&#x306F;4/13&#x6E08;&#x307F;&#x3002;Paolini&#x63A8;&#x5968; &#x2192; <span style="color:#f85149;">MISS</span>&#xFF08;Sonmez&#x52DD;&#x5229;&#xFF09;<br>
        &#x30FB; &#x901A;&#x7B97;: 27GO / 21&#x78BA;&#x5B9A; / 16HIT 76.2% / EV+2.831u
      </div>
    </div>
"@
        $html = $html.Substring(0, $insertAt) + $newEntry + $html.Substring($insertAt)
        Write-Host "2. Session 29 daily report entry added"
    } else {
        Write-Host "2. Section div NOT FOUND in daily report"
    }
} else {
    Write-Host "2. Daily report tab NOT FOUND"
}

[System.IO.File]::WriteAllText($path, $html, [System.Text.Encoding]::UTF8)
Write-Host "Part D complete."
