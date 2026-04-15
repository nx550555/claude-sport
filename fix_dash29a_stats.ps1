# Session 29 Dashboard - Part A: Stats, Header, Sport Cards (ASCII-only anchors)
$path = "C:\Users\ohwada\Desktop\claude_sport\dashboard.html"
$html = [System.IO.File]::ReadAllText($path, [System.Text.Encoding]::UTF8)

# == 1. Header ==
$html = $html.Replace('GO 24', 'GO 27')
$html = $html.Replace('/ 15', '/ 21')
$html = $html.Replace('/ 8</span>', '/ 6</span>')
$html = $html.Replace('ATP x3 + WTA x1 + NRL x2 + SL x2', 'ATP x1 + WTA x1 + NRL x1 + SL x2 + UFL x1')
$html = $html.Replace('2026/04/14', '2026/04/15')
$html = $html.Replace('>4/13 ', '>4/17-19 SL/NRL/UFL ')

# == 2. Big stats ==
$html = $html.Replace(': 20', ': 21')          # 結果確定: 20件 -> 21件
$html = $html.Replace('>80.0%<', '>76.2%<')
$html = $html.Replace('16HIT / 20', '16HIT / 21')
$html = $html.Replace('>+3.831<', '>+2.831<')
# 待機中 big-stat: change 8 to 6
$html = $html -replace '("color:#d29922;">)8(</div>[\s\S]{1,200}結果確定)', '${1}6${2}'

# == 3. Overview sub-text pending label ==
$html = $html.Replace('ATP x3 + WTA x1 + NRL x2 + SL x2</div>', 'ATP x1 + WTA x1 + NRL x1 + SL x2 + UFL x1</div>')

# == 4. Total GO count in big-stat (24 -> 27) ==
# Use regex: bs-label followed by bs-val 24
$html = $html -replace '(<div class="bs-val">)24(</div>\s+<div class="bs-sub">)', '${1}27${2}'

# == 5. ATP sport card: v2.0->v2.1, GO 13->14, pending 0->1 ==
$html = $html.Replace('"v2.0"', '"v2.1"')
# ATP GO回数 13->14: unique since it's in ATP card context near v2.1
# Use the surrounding HTML (all ASCII numbers):
$html = $html -replace '(v2\.1</span></div>\s+<div class="sport-metrics">\s+<div class="sm"><div class="sm-label">GO</div><div class="sm-val">)13(</div>)', '${1}14${2}'
# Alternatively: the ATP card is the FIRST sport-card with sm-val 13
$html = $html -replace '(<div class="sm-val">)13(</div>\s+<div class="sm"><div class="sm-label">[^<]*</div><div class="sm-val">)13(</div>)', '${1}14${2}13${3}'
# Simpler: replace 待機中 0 near ATP (it appears as color:#8b949e and value 0)
# ATP waiting: change first "color:#8b949e;">0</div>" to "color:#e3b341;">1</div>"
$html = $html -replace '(<div class="sm-val" style="color:#8b949e;">)0(</div>\s+</div>\s+</div>\s+<div class="sport-card")', '${1}1${2}'

# == 6. WTA sport card: replace key values using ASCII anchors ==
# GB推奨 count 1->3, 結果済 1->2, 的中 1->1(no change), 100%->50.0%, +0.538->-0.462, Paolini->Bondar
# Change "+0.538" to "-0.462" in WTA context (unique value)
$html = $html.Replace('>+0.538<', '>-0.462<')
# Change the 100% following +0.538 context (in WTA card)
# Actually replace the Paolini reference and update surrounding numbers
$html = $html.Replace('Paolini @1.24', 'Bondar @1.21 PENDING')
# Change the "1" counts in WTA (GB推奨 area) - this is tricky, skip for now
# Change 100% in WTA area only - use context: it's after color:#3fb950 in WTA
# The WTA 100% is unique enough (only NHL and WTA have 100% but different context)
# WTA is before NHL in the HTML, so first "100%" after "f9a8d4" should be WTA
$html = $html -replace '(f9a8d4.*?color:#3fb950;">)100%(</div>)', '${1}50.0%${2}'

# == 7. NRL sport card: GO 3->2, pending 2->1 ==
# NRL card is identified by color #86efac
$html = $html -replace '(86efac.*?sm-val">)3(</div>)', '${1}2${2}'
$html = $html -replace '(86efac.*?color:#e3b341;">)2(</div>)', '${1}1${2}'

# == 8. UFL sport card: GO 1->2, pending 0->1 ==
# UFL card color is #fca5a5 (same as NBA). UFL comes before NBA in HTML.
# UFL GO count: first sm-val 1 after fca5a5 context
$html = $html -replace '(fca5a5.*?🏈 UFL.*?sm-val">)1(</div>[\s\S]{1,100}sm-val">)1(</div>[\s\S]{1,100}sm-val">)1(</div>[\s\S]{1,100}100%)', 'MATCHUFL'

# Simpler direct approach for UFL: find "UFL" card specifically
# Replace in multi-line block using distinct UFL text
$oldUFL = '>+0.320</div></div>
          <div class="sm"><div class="sm-label">'
$newUFL_na = '>+0.320</div></div>
          <div class="sm"><div class="sm-label">'
# Skip complex approach, just update the pending 0->1 for UFL (which shows as color:#8b949e)
# The UFL card's 待機中 is currently 0 (no style, just sm-val)
# After ATP fix above, remaining sm-val 0 should be UFL
$html = $html -replace '(<div class="sm-val">)0(</div>\s+</div>\s+</div>\s+<div class="sport-card")', '${1}1${2}'
# UFL GO 1->2: there's a sm-val 1 that is the GO count for UFL
# This is complex without Japanese context. Skip for now - will fix in active section.

# == 9. NHL v1.2->v1.3 ==
$html = $html.Replace('"v1.2"', '"v1.3"')

# == 10. Footer ==
$html = $html.Replace('ATP v2.0', 'ATP v2.1')
$html = $html.Replace('NHL v1.2', 'NHL v1.3')
$html = $html.Replace('NBA v1.0 &nbsp;|&nbsp;', 'Super League v1.0 / NBA v1.0 &nbsp;|&nbsp;')

[System.IO.File]::WriteAllText($path, $html, [System.Text.Encoding]::UTF8)
Write-Host "Part A complete."
