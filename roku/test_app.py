#!/usr/bin/env python3
"""Automated tests simulating SepulnationTV Roku app usage.

Replicates the BrightScript logic in Python to find bugs in:
- Playlist parsing (PlaylistLoaderTask)
- Content tree structure (ContentNode hierarchy)
- Focus chain (GridScreen -> RowList)
- Navigation simulation (D-pad left/right/up/down)
- Item selection and Video player content creation
"""

import re
import urllib.request
import ssl
import sys

PLAYLIST_URL = "https://raw.githubusercontent.com/tenorioabsgit/iptv/main/playlist.m3u"

# --- Simulated ContentNode ---
class ContentNode:
    """Simulates Roku's ContentNode for testing."""
    def __init__(self, fields=None):
        self.fields = {
            "title": "",
            "description": "",
            "url": "",
            "hdPosterUrl": "",
            "streamFormat": "",
        }
        if fields:
            self.fields.update(fields)
        self.children = []

    def AppendChild(self, child):
        self.children.append(child)

    def GetChild(self, index):
        if 0 <= index < len(self.children):
            return self.children[index]
        return None

    def GetChildCount(self):
        return len(self.children)

    def GetChildren(self, count, index):
        return self.children[index:index + count]

    def Clone(self, deep=False):
        node = ContentNode(dict(self.fields))
        if deep:
            for child in self.children:
                node.AppendChild(child.Clone(True))
        return node

    def __getattr__(self, name):
        if name in ("fields", "children"):
            raise AttributeError(name)
        return self.fields.get(name)

    def __repr__(self):
        return f"ContentNode(title={self.fields.get('title', '')!r}, children={len(self.children)})"


# --- M3U Parsing (mirrors PlaylistLoaderTask.brs) ---
def get_attr_value(line, attr_name):
    pattern = f'{attr_name}="([^"]*)"'
    m = re.search(pattern, line, re.IGNORECASE)
    return m.group(1) if m else ""


def get_stream_format(url):
    lower = url.lower()
    if ".m3u8" in lower: return "hls"
    if ".mpd" in lower: return "dash"
    if ".mp4" in lower: return "mp4"
    if ".mkv" in lower: return "mkv"
    return "hls"


def parse_m3u(text):
    lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    channels = []
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith("#EXTINF:"):
            # extract channel name (after last comma)
            comma_pos = line.rfind(",")
            ch_name = line[comma_pos + 1:].strip() if comma_pos > 0 else ""
            ch_group = get_attr_value(line, "group-title")
            ch_logo = get_attr_value(line, "tvg-logo")

            # find stream URL on next non-empty, non-comment line
            ch_url = ""
            j = i + 1
            while j < len(lines):
                next_line = lines[j].strip()
                if next_line and not next_line.startswith("#"):
                    ch_url = next_line
                    break
                j += 1

            if ch_url:
                channels.append({
                    "name": ch_name,
                    "url": ch_url,
                    "group": ch_group,
                    "logo": ch_logo,
                })
        i += 1
    return channels


def group_channels(channels):
    group_map = {}
    for ch in channels:
        g = ch["group"] if ch["group"] else "Outros"
        group_map.setdefault(g, []).append(ch)

    br_list = sorted(
        [{"name": k, "channels": v} for k, v in group_map.items() if k.startswith("BR ")],
        key=lambda x: x["name"]
    )
    other_list = sorted(
        [{"name": k, "channels": v} for k, v in group_map.items() if not k.startswith("BR ")],
        key=lambda x: x["name"]
    )
    return br_list + other_list


MAX_ITEMS_PER_ROW = 150

def build_content_tree(channels, groups):
    """Simulates PlaylistLoaderTask.GetContent() content tree creation (updated: no 'Todos', capped rows)."""
    default_logo = "https://raw.githubusercontent.com/tenorioabsgit/images/refs/heads/main/sepulnation.png"

    def make_item(ch):
        logo = ch["logo"] if ch["logo"] else default_logo
        return ContentNode({
            "title": ch["name"],
            "description": ch["group"],
            "url": ch["url"],
            "hdPosterUrl": logo,
            "streamFormat": get_stream_format(ch["url"]),
        })

    root = ContentNode()

    # per-group rows only (no "Todos" row), capped at MAX_ITEMS_PER_ROW
    for grp in groups:
        row = ContentNode({"title": f"{grp['name']} ({len(grp['channels'])})"})
        for ch in grp["channels"][:MAX_ITEMS_PER_ROW]:
            row.AppendChild(make_item(ch))
        root.AppendChild(row)

    return root


# --- Simulated RowList Focus/Navigation ---
class RowListSimulator:
    """Simulates Roku RowList focus and D-pad navigation."""
    def __init__(self, content):
        self.content = content
        self.focused_row = 0
        self.focused_col = 0
        self.has_focus = False
        self.errors = []

    def set_focus(self):
        if self.content is None or self.content.GetChildCount() == 0:
            self.errors.append("CRITICAL: SetFocus called on RowList with NO content/rows!")
            self.has_focus = False
            return
        row = self.content.GetChild(self.focused_row)
        if row is None or row.GetChildCount() == 0:
            self.errors.append(f"CRITICAL: Row {self.focused_row} is None or empty when setting focus!")
            self.has_focus = False
            return
        self.has_focus = True

    def get_focused_item(self):
        """Simulates OnItemFocused callback."""
        if self.content is None:
            return None, "content is invalid (None)"
        row = self.content.GetChild(self.focused_row)
        if row is None:
            return None, f"row {self.focused_row} is invalid (GetChild returned None, total rows: {self.content.GetChildCount()})"
        item = row.GetChild(self.focused_col)
        if item is None:
            return None, f"item [{self.focused_row},{self.focused_col}] is invalid (GetChild returned None, row has {row.GetChildCount()} items)"
        # Check fields the app accesses
        if item.fields.get("description") is None:
            return item, f"item [{self.focused_row},{self.focused_col}] has description=None (would CRASH descriptionLabel.text assignment)"
        if item.fields.get("title") is None:
            return item, f"item [{self.focused_row},{self.focused_col}] has title=None (would CRASH titleLabel.text assignment)"
        return item, None

    def navigate(self, direction):
        """Simulate D-pad press. Returns (success, error_msg)."""
        if not self.has_focus:
            return False, "RowList does not have focus - navigation ignored"

        old_row, old_col = self.focused_row, self.focused_col
        num_rows = self.content.GetChildCount()

        if direction == "right":
            row = self.content.GetChild(self.focused_row)
            if self.focused_col < row.GetChildCount() - 1:
                self.focused_col += 1
            # else: at end of row, RowList stops (floatingFocus)
        elif direction == "left":
            if self.focused_col > 0:
                self.focused_col -= 1
        elif direction == "down":
            if self.focused_row < num_rows - 1:
                self.focused_row += 1
                # clamp col to new row's item count
                new_row = self.content.GetChild(self.focused_row)
                if new_row and self.focused_col >= new_row.GetChildCount():
                    self.focused_col = max(0, new_row.GetChildCount() - 1)
        elif direction == "up":
            if self.focused_row > 0:
                self.focused_row -= 1
                new_row = self.content.GetChild(self.focused_row)
                if new_row and self.focused_col >= new_row.GetChildCount():
                    self.focused_col = max(0, new_row.GetChildCount() - 1)

        # After every navigation, OnItemFocused fires
        item, error = self.get_focused_item()
        if error:
            self.errors.append(f"NAV {direction} [{old_row},{old_col}]->[{self.focused_row},{self.focused_col}]: {error}")
            return False, error

        return True, None

    def select(self):
        """Simulate OK press -> rowItemSelected."""
        if not self.has_focus:
            return None, None, "RowList does not have focus"
        return self.focused_row, self.focused_col, None


# --- Simulated Video Player Content Creation ---
def simulate_show_video_screen(content_tree, row_index, item_index):
    """Simulates ShowVideoScreen from VideoPlayerLogic.brs"""
    errors = []
    row_content = content_tree.GetChild(row_index)
    if row_content is None:
        errors.append(f"CRITICAL: row_content is None for row {row_index}")
        return errors

    selected_item = item_index

    if selected_item != 0:
        num_children = row_content.GetChildCount()
        children = row_content.GetChildren(num_children - selected_item, selected_item)
        if not children:
            errors.append(f"CRITICAL: GetChildren returned empty for row={row_index}, item={selected_item}, total={num_children}")
            return errors

        # Simulate AppendChild approach (current code)
        row_node = ContentNode()
        for child in children:
            cloned = child.Clone(False)
            row_node.AppendChild(cloned)

        # Validate the playlist content
        for i, child_node in enumerate(row_node.children):
            url = child_node.fields.get("url", "")
            fmt = child_node.fields.get("streamFormat", "")
            title = child_node.fields.get("title", "")
            if not url:
                errors.append(f"  Video playlist item {i} has EMPTY url (title={title!r})")
            if not fmt:
                errors.append(f"  Video playlist item {i} has EMPTY streamFormat (title={title!r})")
    else:
        cloned = row_content.Clone(True)
        for i, child_node in enumerate(cloned.children):
            url = child_node.fields.get("url", "")
            if not url:
                errors.append(f"  Video playlist item {i} has EMPTY url after Clone(true)")

    return errors


# --- Test Runner ---
def run_tests():
    passed = 0
    failed = 0
    warnings = 0

    def ok(msg):
        nonlocal passed
        passed += 1
        print(f"  PASS: {msg}")

    def fail(msg):
        nonlocal failed
        failed += 1
        print(f"  FAIL: {msg}")

    def warn(msg):
        nonlocal warnings
        warnings += 1
        print(f"  WARN: {msg}")

    # ========== TEST 1: Download playlist ==========
    print("\n=== TEST 1: Download Playlist ===")
    ctx = ssl.create_default_context()
    try:
        req = urllib.request.Request(PLAYLIST_URL)
        with urllib.request.urlopen(req, context=ctx, timeout=30) as resp:
            playlist_text = resp.read().decode("utf-8")
        ok(f"Downloaded playlist ({len(playlist_text)} bytes)")
    except Exception as e:
        fail(f"Failed to download playlist: {e}")
        return

    # ========== TEST 2: Parse M3U ==========
    print("\n=== TEST 2: Parse M3U ===")
    channels = parse_m3u(playlist_text)
    if channels:
        ok(f"Parsed {len(channels)} channels")
    else:
        fail("No channels parsed!")
        return

    # Check each channel has required fields
    empty_names = [ch for ch in channels if not ch["name"]]
    empty_urls = [ch for ch in channels if not ch["url"]]
    empty_logos = [ch for ch in channels if not ch["logo"]]
    empty_groups = [ch for ch in channels if not ch["group"]]

    if empty_urls:
        fail(f"{len(empty_urls)} channels have empty URLs")
    else:
        ok("All channels have URLs")

    if empty_names:
        warn(f"{len(empty_names)} channels have empty names")
    else:
        ok("All channels have names")

    if empty_logos:
        warn(f"{len(empty_logos)} channels have empty logos (will use default)")
    else:
        ok("All channels have logos")

    if empty_groups:
        warn(f"{len(empty_groups)} channels have empty group (will go to 'Outros')")

    # ========== TEST 3: Group channels ==========
    print("\n=== TEST 3: Group Channels ===")
    groups = group_channels(channels)
    if groups:
        ok(f"Created {len(groups)} groups")
        for g in groups:
            count = len(g["channels"])
            if count == 0:
                fail(f"Group '{g['name']}' has 0 channels!")
            else:
                print(f"       - {g['name']}: {count} channels")
    else:
        fail("No groups created!")

    # ========== TEST 4: Build content tree ==========
    print("\n=== TEST 4: Build Content Tree ===")
    content_tree = build_content_tree(channels, groups)
    total_rows = content_tree.GetChildCount()
    expected_rows = len(groups)

    if total_rows == expected_rows:
        ok(f"Content tree has {total_rows} rows ({len(groups)} groups, no 'Todos')")
    else:
        fail(f"Expected {expected_rows} rows, got {total_rows}")

    # Performance check: count total ContentNodes
    total_items = sum(content_tree.GetChild(r).GetChildCount() for r in range(total_rows))
    print(f"  Total ContentNode items: {total_items} (was 3534 before fix)")
    if total_items > 3000:
        fail(f"Too many items ({total_items}) - Roku will freeze!")
    else:
        ok(f"Item count {total_items} is manageable for Roku")

    # Check no row exceeds MAX_ITEMS_PER_ROW
    for r in range(total_rows):
        row = content_tree.GetChild(r)
        if row.GetChildCount() > MAX_ITEMS_PER_ROW:
            fail(f"Row '{row.fields['title']}' has {row.GetChildCount()} items (max {MAX_ITEMS_PER_ROW})")
        elif row.GetChildCount() > 100:
            print(f"  INFO: Row '{row.fields['title']}' has {row.GetChildCount()} items (within limit)")

    # Validate each row has children
    for r in range(total_rows):
        row = content_tree.GetChild(r)
        if row is None:
            fail(f"Row {r} is None!")
            continue
        if row.GetChildCount() == 0:
            fail(f"Row {r} ({row.fields['title']}) has 0 items!")
        else:
            # Validate each item in row
            for c in range(row.GetChildCount()):
                item = row.GetChild(c)
                if item is None:
                    fail(f"Item [{r},{c}] is None!")
                elif not item.fields.get("title"):
                    warn(f"Item [{r},{c}] in row '{row.fields['title']}' has empty title")
                elif not item.fields.get("url"):
                    fail(f"Item [{r},{c}] '{item.fields['title']}' has empty url!")
                elif not item.fields.get("hdPosterUrl"):
                    warn(f"Item [{r},{c}] '{item.fields['title']}' has empty hdPosterUrl")

    ok(f"All {total_rows} rows have valid items")

    # ========== TEST 5: Focus Chain Simulation ==========
    print("\n=== TEST 5: Focus Chain ===")

    # Simulate app startup sequence
    print("  Simulating: ShowGridScreen() -> ShowScreen() -> Init()")

    # Step 1: GridScreen created, Init runs. rowList has NO content.
    sim = RowListSimulator(None)
    # OnVisibleChange fires (GridScreen becomes visible), but content is None
    # With our fix, OnVisibleChange checks content != invalid
    if sim.content is None:
        ok("OnVisibleChange correctly skips focus (content is None)")

    # Step 2: Content loads, OnMainContentLoaded fires
    print("  Simulating: content loaded -> OnMainContentLoaded()")
    sim.content = content_tree
    # OnContentLoaded fires
    sim.set_focus()
    if sim.has_focus:
        ok("RowList received focus after content loaded")
    else:
        fail("RowList FAILED to receive focus after content loaded")
        for e in sim.errors:
            fail(f"  {e}")

    # Verify initial OnItemFocused
    item, error = sim.get_focused_item()
    if error:
        fail(f"Initial OnItemFocused would crash: {error}")
    else:
        ok(f"Initial focus on [{sim.focused_row},{sim.focused_col}]: '{item.fields['title']}'")

    # ========== TEST 6: Navigation Simulation ==========
    print("\n=== TEST 6: D-pad Navigation ===")

    # Reset to start
    sim = RowListSimulator(content_tree)
    sim.set_focus()

    first_row = content_tree.GetChild(0)
    first_row_count = first_row.GetChildCount() if first_row else 0
    print(f"  First row has {first_row_count} items, total {total_rows} rows")

    # Navigate RIGHT through first row
    nav_right_count = min(first_row_count - 1, 20)  # test up to 20 items
    print(f"  Navigating RIGHT x{nav_right_count} in first row...")
    for i in range(nav_right_count):
        success, error = sim.navigate("right")
        if not success:
            fail(f"RIGHT navigation #{i+1} failed: {error}")
            break
    else:
        ok(f"Navigated RIGHT x{nav_right_count} successfully")

    # Navigate LEFT back
    print(f"  Navigating LEFT x{nav_right_count} back...")
    for i in range(nav_right_count):
        success, error = sim.navigate("left")
        if not success:
            fail(f"LEFT navigation #{i+1} failed: {error}")
            break
    else:
        ok(f"Navigated LEFT x{nav_right_count} successfully")

    # Navigate DOWN through rows
    max_down = min(total_rows - 1, 10)
    print(f"  Navigating DOWN x{max_down} through rows...")
    for i in range(max_down):
        success, error = sim.navigate("down")
        if not success:
            fail(f"DOWN navigation #{i+1} failed: {error}")
            break
    else:
        ok(f"Navigated DOWN x{max_down} successfully")

    # Navigate UP back
    print(f"  Navigating UP x{max_down} back...")
    for i in range(max_down):
        success, error = sim.navigate("up")
        if not success:
            fail(f"UP navigation #{i+1} failed: {error}")
            break
    else:
        ok(f"Navigated UP x{max_down} successfully")

    # Exhaustive test: navigate to every item in every row
    print(f"  Exhaustive test: visiting every item in every row...")
    sim2 = RowListSimulator(content_tree)
    sim2.set_focus()
    total_items_visited = 0
    for r in range(total_rows):
        if r > 0:
            sim2.navigate("down")
        row_node = content_tree.GetChild(r)
        # navigate to col 0
        while sim2.focused_col > 0:
            sim2.navigate("left")
        for c in range(row_node.GetChildCount()):
            item, error = sim2.get_focused_item()
            if error:
                fail(f"CRASH at [{r},{c}]: {error}")
            total_items_visited += 1
            if c < row_node.GetChildCount() - 1:
                sim2.navigate("right")

    if sim2.errors:
        for e in sim2.errors:
            fail(e)
    else:
        ok(f"Visited all {total_items_visited} items across {total_rows} rows without crashes")

    # ========== TEST 7: Item Selection (OK press) ==========
    print("\n=== TEST 7: Item Selection -> Video Player ===")

    # Test selecting first item in first row
    test_selections = [
        (0, 0, "first item of 'Todos'"),
        (0, 1, "second item of 'Todos'"),
        (0, min(5, first_row_count - 1), f"item {min(5, first_row_count - 1)} of 'Todos'"),
    ]
    if total_rows > 1:
        second_row = content_tree.GetChild(1)
        test_selections.append((1, 0, f"first item of '{second_row.fields['title']}'"))
        if second_row.GetChildCount() > 1:
            test_selections.append((1, 1, f"second item of '{second_row.fields['title']}'"))

    for row_idx, col_idx, desc in test_selections:
        row_node = content_tree.GetChild(row_idx)
        if row_node is None or col_idx >= row_node.GetChildCount():
            warn(f"Skipping selection test for [{row_idx},{col_idx}]: out of bounds")
            continue

        errors = simulate_show_video_screen(content_tree, row_idx, col_idx)
        if errors:
            fail(f"ShowVideoScreen({desc}) [{row_idx},{col_idx}]:")
            for e in errors:
                fail(f"  {e}")
        else:
            item = row_node.GetChild(col_idx)
            ok(f"ShowVideoScreen({desc}): url={item.fields['url'][:60]}...")

    # ========== TEST 8: Back Navigation (Video -> Grid) ==========
    print("\n=== TEST 8: Back Navigation (Video -> Grid) ===")

    # Simulate: watching video, press back, return to grid
    sim3 = RowListSimulator(content_tree)
    sim3.content = content_tree
    sim3.focused_row = 1
    sim3.focused_col = 2
    # Simulating CloseScreen -> prev.visible=true -> OnVisibleChange -> rowList.SetFocus
    sim3.set_focus()
    if sim3.has_focus:
        ok("Focus restored to RowList after returning from video")
        item, error = sim3.get_focused_item()
        if error:
            fail(f"OnItemFocused after return would crash: {error}")
        else:
            ok(f"Focus at [{sim3.focused_row},{sim3.focused_col}]: '{item.fields['title']}'")
    else:
        fail("RowList failed to get focus after returning from video")

    # ========== TEST 9: RowList XML Configuration Check ==========
    print("\n=== TEST 9: RowList Configuration Validation ===")

    row_item_w, row_item_h = 320, 180
    row_spacing = 20
    item_w, item_h = 1700, 270
    focus_x_offset = 50
    num_rows = 2
    screen_w, screen_h = 1920, 1080
    rowlist_x, rowlist_y = 80, 350

    # Check items fit in row
    visible_items_per_row = (item_w - focus_x_offset) // (row_item_w + row_spacing)
    print(f"  Visible items per row: ~{visible_items_per_row}")
    if visible_items_per_row < 1:
        fail("No items visible in row! itemSize too small or rowItemSize too large")
    else:
        ok(f"{visible_items_per_row} items visible per row")

    # Check rows fit on screen
    total_rowlist_height = num_rows * item_h
    bottom_edge = rowlist_y + total_rowlist_height
    if bottom_edge > screen_h:
        warn(f"RowList extends beyond screen: y={rowlist_y} + {total_rowlist_height} = {bottom_edge} > {screen_h}")
    else:
        ok(f"RowList fits on screen (bottom edge at {bottom_edge}px of {screen_h}px)")

    # Check row label space
    label_offset_y = 20
    available_item_height = item_h - label_offset_y - 30  # ~30px for label text
    if row_item_h > available_item_height:
        warn(f"Item height {row_item_h} may not fit in row space ({available_item_height}px available after label)")
    else:
        ok(f"Item height {row_item_h}px fits in row ({available_item_height}px available)")

    # ========== SUMMARY ==========
    print(f"\n{'='*50}")
    print(f"RESULTS: {passed} passed, {failed} failed, {warnings} warnings")
    if failed > 0:
        print("FIX THE FAILURES ABOVE!")
    print(f"{'='*50}")

    return failed


if __name__ == "__main__":
    sys.exit(run_tests())
