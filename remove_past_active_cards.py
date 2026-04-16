"""
Remove completed (past-date) entries from dashboard active section:
1. ATP Barcelona R2 Musetti (4/16) - completed HIT
2. WTA Rouen Tan vs Bondar (4/15) - completed HIT
3. WTA Stuttgart Sonmez vs Paolini (4/15) - completed MISS
Also update Tennis header count 3->0 and remove if zero.
"""
import sys, re
sys.stdout.reconfigure(encoding='utf-8')

base = r"C:\Users\ohwada\Desktop\claude_sport"

with open(f'{base}/dashboard.html', 'r', encoding='utf-8') as f:
    html = f.read()

original_len = len(html)

# ---- Helper: remove a block between start_marker and end_marker ----
def remove_block(html, start_marker, end_marker):
    start_idx = html.find(start_marker)
    if start_idx == -1:
        print(f"  [WARN] Start marker not found: {start_marker[:60]}")
        return html, False
    end_idx = html.find(end_marker, start_idx)
    if end_idx == -1:
        print(f"  [WARN] End marker not found after start: {end_marker[:60]}")
        return html, False
    end_idx += len(end_marker)
    removed = html[start_idx:end_idx]
    print(f"  [OK] Removed block ({len(removed)} chars): {removed[:80].strip()}...")
    return html[:start_idx] + html[end_idx:], True

# ---- Remove ATP Musetti card ----
html, ok1 = remove_block(
    html,
    '<!-- ATP Barcelona R2: Musetti vs Moutet (4/16) -->',
    '</div>\n\n    <!-- WTA Rouen: Bondar vs Tan (4/15) -->'
)
if ok1:
    # The end marker consumed the WTA comment, need to re-add the next section marker
    # Actually let's check what remains after removal
    pass

# Re-read since remove_block modifies html
# Let me do this differently - find each active-card and remove by key content
def remove_active_card_by_comment(html, comment_text, next_comment_text=None):
    """Remove an active-card div starting at comment_text and ending before next_comment_text."""
    start = html.find(f'<!-- {comment_text}')
    if start == -1:
        # Try partial match
        start = html.find(comment_text)
        if start == -1:
            print(f"  [WARN] Comment not found: {comment_text[:50]}")
            return html, False

    if next_comment_text:
        end = html.find(f'<!-- {next_comment_text}', start + 1)
        if end == -1:
            end = html.find(next_comment_text, start + 1)
        if end == -1:
            print(f"  [WARN] Next comment not found: {next_comment_text[:50]}")
            return html, False
    else:
        # Find end of the active-card div
        div_start = html.find('<div class="active-card"', start)
        if div_start == -1:
            print(f"  [WARN] active-card div not found after comment")
            return html, False
        # Count divs to find the matching close
        depth = 0
        i = div_start
        while i < len(html):
            if html[i:i+4] == '<div':
                depth += 1
                i += 4
            elif html[i:i+6] == '</div>':
                depth -= 1
                if depth == 0:
                    end = i + 6
                    break
                i += 6
            else:
                i += 1
        else:
            print(f"  [WARN] Could not find matching </div>")
            return html, False
        # Include trailing newlines
        while end < len(html) and html[end] in '\n\r':
            end += 1

    removed = html[start:end]
    print(f"  [OK] Removed ({len(removed)} chars): {removed[:100].strip()[:80]}...")
    return html[:start] + html[end:], True

# Reload fresh
with open(f'{base}/dashboard.html', 'r', encoding='utf-8') as f:
    html = f.read()

print("Removing ATP Musetti card (4/16)...")
html, ok1 = remove_active_card_by_comment(
    html,
    'ATP Barcelona R2: Musetti vs Moutet (4/16)',
    'WTA Rouen: Bondar vs Tan (4/15)'
)

print("Removing WTA Bondar card (4/15)...")
html, ok2 = remove_active_card_by_comment(
    html,
    'WTA Rouen: Bondar vs Tan (4/15)',
    'WTA Stuttgart Paolini PENDING'
)

print("Removing WTA Paolini card (Stuttgart 4/15)...")
html, ok3 = remove_active_card_by_comment(
    html,
    'WTA Stuttgart Paolini PENDING',
    'UFL W4 Louisville'
)

print(f"\nResults: ATP={ok1}, Bondar={ok2}, Paolini={ok3}")

# ---- Update Tennis section header count ----
# Was "3件", should become "0件" if all 3 removed, or remove the header entirely
if ok1 and ok2 and ok3:
    # Remove the entire テニス section header (no more active tennis items)
    old_header = '''    <!-- ===== 🎾 テニス ===== -->
    <div class="active-league-hdr">
      <span>&#x1F3BE; テニス <span style="color:var(--text2);font-weight:400;font-size:11px;">ATP / WTA</span></span>
      <span class="alh-count">3件</span>
    </div>

    '''
    if old_header in html:
        html = html.replace(old_header, '    ')
        print("  [OK] Removed tennis league header (3->0, header removed)")
    else:
        # Try finding the header differently
        tennis_hdr_start = html.find('&#x1F3BE; テニス')
        if tennis_hdr_start == -1:
            tennis_hdr_start = html.find('x1F3BE; &#x30C6;&#x30CB;&#x30B9;')
        if tennis_hdr_start != -1:
            # Find the enclosing active-league-hdr div
            div_start = html.rfind('<div class="active-league-hdr"', 0, tennis_hdr_start)
            div_end = html.find('</div>', tennis_hdr_start) + 6
            if div_start != -1:
                # Also skip following blank line
                while div_end < len(html) and html[div_end] in '\n\r ':
                    div_end += 1
                removed = html[div_start:div_end]
                html = html[:div_start] + html[div_end:]
                print(f"  [OK] Removed tennis header: {removed[:80].strip()}")
        else:
            print("  [WARN] Tennis header not found - update count manually")
            # Just update the count
            html = html.replace('<span class="alh-count">3\u4ef6</span>', '<span class="alh-count">0\u4ef6</span>', 1)

# Save
with open(f'{base}/dashboard.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f"\nDashboard HTML updated. Size: {original_len} -> {len(html)} chars ({original_len-len(html)} chars removed)")

# Verify no past-date items remain in active section
content_start = html.find('id="content-active"')
content_end = html.find('id="content-history"')
active_section = html[content_start:content_end]
for keyword in ['2026-04-14', '2026-04-15 JST', '2026-04-16']:
    count = active_section.count(keyword)
    if count > 0:
        print(f"  [WARN] Still found '{keyword}' {count}x in active section!")
    else:
        print(f"  [OK] '{keyword}' not found in active section")
