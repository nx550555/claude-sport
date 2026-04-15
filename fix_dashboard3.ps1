# fix_dashboard3.ps1 — NRL R7 全ダッシュボード更新
$f = 'C:\Users\ohwada\Desktop\claude_sport\dashboard.html'
$enc = [System.Text.Encoding]::UTF8
$raw = [System.IO.File]::ReadAllBytes($f)
$content = $enc.GetString($raw)

# 改行コードをLFに正規化
$content = $content.Replace("`r`n", "`n")

# ──────────────────────────────────────────
function ReplaceFirst([string]$text, [string]$old, [string]$new) {
    $idx = $text.IndexOf($old, [System.StringComparison]::Ordinal)
    if ($idx -lt 0) { Write-Warning "NOT FOUND: [$($old.Substring(0, [Math]::Min(60,$old.Length)))]"; return $text }
    return $text.Substring(0, $idx) + $new + $text.Substring($idx + $old.Length)
}
function InsertBefore([string]$text, [string]$anchor, [string]$ins) {
    $idx = $text.IndexOf($anchor, [System.StringComparison]::Ordinal)
    if ($idx -lt 0) { Write-Warning "ANCHOR NOT FOUND: [$($anchor.Substring(0, [Math]::Min(60,$anchor.Length)))]"; return $text }
    return $text.Substring(0, $idx) + $ins + $text.Substring($idx)
}

# ══════════════════════════════════════════
# 1. 待機中サブテキスト修正
# ══════════════════════════════════════════
$content = ReplaceFirst $content `
    '<div class="bs-sub">UFL Dallas + ATP 4/14 x3</div>' `
    '<div class="bs-sub">UFL+ATP 4/14 x3 + NRL 4/18 x2</div>'
Write-Output "1. subtitle done"

# ══════════════════════════════════════════
# 2. NRL GO回数 1→3
# ══════════════════════════════════════════
$gokaisu = "GO" + [char]0x56DE + [char]0x6570
$nrlGoOld = '<div class="sm"><div class="sm-label">' + $gokaisu + '</div><div class="sm-val">1</div></div>'
$nrlGoNew = '<div class="sm"><div class="sm-label">' + $gokaisu + '</div><div class="sm-val">3</div></div>'
$content = ReplaceFirst $content $nrlGoOld $nrlGoNew
Write-Output "2. NRL GO count done"

# ══════════════════════════════════════════
# 3. NRL アクティブカード4枚挿入
# アンカー: アクティブグリッド閉じタグ
# ══════════════════════════════════════════
$nrlCards = @"

    <div class="active-card" style="border-color:#23863640;background:linear-gradient(135deg,#23863610,transparent);">
      <div class="ac-sport">&#x1F3C9; NRL &#x2014; Round 7 2026</div>
      <div class="ac-match">Wests Tigers vs Brisbane Broncos <span class="badge badge-go">GO</span></div>
      <div class="ac-rec">&#x63A8;&#x5968;: <strong style="color:#3fb950;">Brisbane Broncos</strong></div>
      <div class="ac-metrics">
        <div class="acm"><div class="acm-l">&#x30AA;&#x30C3;&#x30BA;</div><div class="acm-v odds">1.46</div></div>
        <div class="acm"><div class="acm-l">&#x4E88;&#x6E2C;EV</div><div class="acm-v ev">+27.9%</div></div>
        <div class="acm"><div class="acm-l">&#x78BA;&#x4FE1;&#x5EA6;</div><div class="acm-v">87.6%</div></div>
        <div class="acm"><div class="acm-l">PD/G&#x5DEE;</div><div class="acm-v rule">+14.1pt</div></div>
      </div>
      <div class="ac-note">Broncos PD/G +10.0 / Tigers PD/G -4.1 &#x2192; diff +14.1pt&#x3002;R7&#x65E9;&#x671F;&#x9583;&#x5024;12pt&#x8D85;&#x3002;conf 87.6% / EV+27.9%</div>
      <div class="ac-date">&#x1F4C5; 2026-04-18 NRL R7</div>
    </div>

    <div class="active-card" style="border-color:#23863640;background:linear-gradient(135deg,#23863610,transparent);">
      <div class="ac-sport">&#x1F3C9; NRL &#x2014; Round 7 2026</div>
      <div class="ac-match">NZ Warriors vs Gold Coast Titans <span class="badge badge-go">GO</span></div>
      <div class="ac-rec">&#x63A8;&#x5968;: <strong style="color:#3fb950;">NZ Warriors</strong></div>
      <div class="ac-metrics">
        <div class="acm"><div class="acm-l">&#x30AA;&#x30C3;&#x30BA;</div><div class="acm-v odds">1.22</div></div>
        <div class="acm"><div class="acm-l">&#x4E88;&#x6E2C;EV</div><div class="acm-v ev">+10.7%</div></div>
        <div class="acm"><div class="acm-l">&#x78BA;&#x4FE1;&#x5EA6;</div><div class="acm-v">90.7%</div></div>
        <div class="acm"><div class="acm-l">PD/G&#x5DEE;</div><div class="acm-v rule">+16.7pt</div></div>
      </div>
      <div class="ac-note">Warriors PD/G +8.7 / Titans PD/G -8.0 &#x2192; diff +16.7pt&#x3002;&#x9583;&#x5024;12pt&#x8D85;&#x3002;conf 90.7% / EV+10.7%</div>
      <div class="ac-date">&#x1F4C5; 2026-04-18 NRL R7</div>
    </div>

    <div class="active-card" style="border-color:#d2992230;background:linear-gradient(135deg,#d2992208,transparent);">
      <div class="ac-sport">&#x1F3C9; NRL &#x2014; Round 7 2026</div>
      <div class="ac-match">Penrith Panthers vs Dolphins <span class="badge badge-caution">CAUTION</span></div>
      <div class="ac-rec">&#x63A8;&#x5968;: <strong style="color:#d29922;">Penrith Panthers</strong></div>
      <div class="ac-metrics">
        <div class="acm"><div class="acm-l">&#x30AA;&#x30C3;&#x30BA;</div><div class="acm-v odds">1.14</div></div>
        <div class="acm"><div class="acm-l">&#x4E88;&#x6E2C;EV</div><div class="acm-v ev">+9.2%</div></div>
        <div class="acm"><div class="acm-l">&#x78BA;&#x4FE1;&#x5EA6;</div><div class="acm-v">95.8%</div></div>
        <div class="acm"><div class="acm-l">PD/G&#x5DEE;</div><div class="acm-v rule">+24.0pt</div></div>
      </div>
      <div class="ac-note">Panthers&#x5727;&#x5012;&#x7684;&#x512A;&#x4F4D;(PD/G +16.0 vs Dolphins -8.0 &#x2192; diff +24.0pt)&#x3002;&#x30AA;&#x30C3;&#x30BA;&#x77ED;&#x3059;&#x304E;(1.14)&#x3067;&#x30EA;&#x30BF;&#x30FC;&#x30F3;&#x8584;&#x3002;CAUTION&#x63A8;&#x5968;&#x3002;</div>
      <div class="ac-date">&#x1F4C5; 2026-04-17 NRL R7</div>
    </div>

    <div class="active-card" style="border-color:#d2992230;background:linear-gradient(135deg,#d2992208,transparent);">
      <div class="ac-sport">&#x1F3C9; NRL &#x2014; Round 7 2026</div>
      <div class="ac-match">South Sydney Rabbitohs vs St George Illawarra Dragons <span class="badge badge-caution">CAUTION</span></div>
      <div class="ac-rec">&#x63A8;&#x5968;: <strong style="color:#d29922;">South Sydney Rabbitohs</strong></div>
      <div class="ac-metrics">
        <div class="acm"><div class="acm-l">&#x30AA;&#x30C3;&#x30BA;</div><div class="acm-v odds">1.18</div></div>
        <div class="acm"><div class="acm-l">&#x4E88;&#x6E2C;EV</div><div class="acm-v ev">+6.8%</div></div>
        <div class="acm"><div class="acm-l">&#x78BA;&#x4FE1;&#x5EA6;</div><div class="acm-v">88.3%</div></div>
        <div class="acm"><div class="acm-l">PD/G&#x5DEE;</div><div class="acm-v rule">+13.5pt</div></div>
      </div>
      <div class="ac-note">Rabbitohs PD/G +7.0 / Dragons PD/G -6.5 &#x2192; diff +13.5pt&#x3002;&#x9583;&#x5024;12pt&#x8D85;&#x3002;&#x30AA;&#x30C3;&#x30BA;1.18&#x3067;EV+6.8%&#x3002;CAUTION&#x63A8;&#x5968;&#x3002;</div>
      <div class="ac-date">&#x1F4C5; 2026-04-18 NRL R7</div>
    </div>

"@

$anchor3 = "  </div></div>`n</div>`n`n<!-- ====="
$content = InsertBefore $content $anchor3 $nrlCards
Write-Output "3. NRL active cards done"

# ══════════════════════════════════════════
# 4. NRL 履歴行 (history tbody 先頭)
# ══════════════════════════════════════════
$nrlRows = @"
        <tr style="background:rgba(46,160,67,.06);">
          <td>2026-04-18</td>
          <td><span class="sport-tag" style="color:#86efac;">&#x1F3C9; NRL</span></td>
          <td style="font-size:12px;">R7 2026</td>
          <td class="match-cell">Wests Tigers vs Brisbane Broncos</td>
          <td><span class="badge badge-go">GO</span></td>
          <td style="color:#3fb950;font-weight:600;">Broncos</td>
          <td style="color:#e3b341;">1.46</td>
          <td class="ev-pos">+27.9%</td>
          <td>87.6%</td>
          <td><span class="badge badge-pending">PENDING</span></td>
          <td style="color:#8b949e;">&#x2014;</td>
          <td style="color:#8b949e;">&#x2014;</td>
        </tr>
        <tr style="background:rgba(46,160,67,.06);">
          <td>2026-04-18</td>
          <td><span class="sport-tag" style="color:#86efac;">&#x1F3C9; NRL</span></td>
          <td style="font-size:12px;">R7 2026</td>
          <td class="match-cell">NZ Warriors vs Gold Coast Titans</td>
          <td><span class="badge badge-go">GO</span></td>
          <td style="color:#3fb950;font-weight:600;">Warriors</td>
          <td style="color:#e3b341;">1.22</td>
          <td class="ev-pos">+10.7%</td>
          <td>90.7%</td>
          <td><span class="badge badge-pending">PENDING</span></td>
          <td style="color:#8b949e;">&#x2014;</td>
          <td style="color:#8b949e;">&#x2014;</td>
        </tr>
        <tr style="background:rgba(210,153,34,.06);">
          <td>2026-04-18</td>
          <td><span class="sport-tag" style="color:#86efac;">&#x1F3C9; NRL</span></td>
          <td style="font-size:12px;">R7 2026</td>
          <td class="match-cell">South Sydney Rabbitohs vs St George Illawarra Dragons</td>
          <td><span class="badge badge-caution">CAUTION</span></td>
          <td style="color:#d29922;font-weight:600;">Rabbitohs</td>
          <td style="color:#e3b341;">1.18</td>
          <td class="ev-pos">+6.8%</td>
          <td>88.3%</td>
          <td><span class="badge badge-pending">PENDING</span></td>
          <td style="color:#8b949e;">&#x2014;</td>
          <td style="color:#8b949e;">&#x2014;</td>
        </tr>
        <tr style="background:rgba(210,153,34,.06);">
          <td>2026-04-17</td>
          <td><span class="sport-tag" style="color:#86efac;">&#x1F3C9; NRL</span></td>
          <td style="font-size:12px;">R7 2026</td>
          <td class="match-cell">Penrith Panthers vs Dolphins</td>
          <td><span class="badge badge-caution">CAUTION</span></td>
          <td style="color:#d29922;font-weight:600;">Panthers</td>
          <td style="color:#e3b341;">1.14</td>
          <td class="ev-pos">+9.2%</td>
          <td>95.8%</td>
          <td><span class="badge badge-pending">PENDING</span></td>
          <td style="color:#8b949e;">&#x2014;</td>
          <td style="color:#8b949e;">&#x2014;</td>
        </tr>
"@

$anchor4 = "        <tbody>`n        <tr style=`"background:rgba(46,160,67,.06);`">`n          <td>2026-04-14</td>"
$content = InsertBefore $content $anchor4 $nrlRows
Write-Output "4. NRL history rows done"

# ══════════════════════════════════════════
# 5. 分析ログ — セッション集計ボックス3個を先頭に追加
# ══════════════════════════════════════════
$newBoxes = @"
      <div style="background:var(--surface);border:1px solid #3fb95040;border-radius:8px;padding:10px 14px;font-size:12px;min-width:160px;">
        <div style="color:#3fb950;font-size:10px;text-transform:uppercase;margin-bottom:4px;">NRL R7 4/13&#x30B9;&#x30AF;&#x30EA;&#x30FC;&#x30CB;&#x30F3;&#x30B0;</div>
        <div>&#x5206;&#x6790; <b>8</b> &#x8A66;&#x5408; &nbsp;|&nbsp; <span style="color:#3fb950;">GO 2</span> &nbsp;|&nbsp; <span style="color:#d29922;">CAUTION 2</span> &nbsp;|&nbsp; <span style="color:#8b949e;">SKIP 4</span></div>
      </div>
      <div style="background:var(--surface);border:1px solid var(--border);border-radius:8px;padding:10px 14px;font-size:12px;min-width:160px;">
        <div style="color:var(--text2);font-size:10px;text-transform:uppercase;margin-bottom:4px;">NBA Play-In 4/13&#x30B9;&#x30AF;&#x30EA;&#x30FC;&#x30CB;&#x30F3;&#x30B0;</div>
        <div>&#x5206;&#x6790; <b>8</b> &#x8A66;&#x5408; &nbsp;|&nbsp; <span style="color:#3fb950;">GO 0</span> &nbsp;|&nbsp; <span style="color:#8b949e;">SKIP 8&#xFF08;&#x5168;&#x8A66;&#x5408;NRtg&#x5DEE;&lt;5pt&#xFF09;</span></div>
      </div>
      <div style="background:var(--surface);border:1px solid var(--border);border-radius:8px;padding:10px 14px;font-size:12px;min-width:160px;">
        <div style="color:var(--text2);font-size:10px;text-transform:uppercase;margin-bottom:4px;">NHL 4/13&#x30B9;&#x30AF;&#x30EA;&#x30FC;&#x30CB;&#x30F3;&#x30B0;</div>
        <div>&#x5206;&#x6790; <b>9</b> &#x8A66;&#x5408; &nbsp;|&nbsp; <span style="color:#3fb950;">GO 0</span> &nbsp;|&nbsp; <span style="color:#8b949e;">SKIP 9&#xFF08;xGF%&#x5DEE;&#x57FA;&#x6E96;&#x8D85;&#x3067;&#x3082;EV&#x8CA0;&#xFF09;</span></div>
      </div>
"@

$anchor5 = "    <div style=`"display:flex;gap:10px;flex-wrap:wrap;margin-bottom:20px;`">`n"
$content = ReplaceFirst $content $anchor5 ($anchor5 + $newBoxes)
Write-Output "5. analysis log boxes done"

# ══════════════════════════════════════════
# 書き出し (LF維持)
# ══════════════════════════════════════════
$bytes = $enc.GetBytes($content)
[System.IO.File]::WriteAllBytes($f, $bytes)
Write-Output "=== ALL DONE ==="
