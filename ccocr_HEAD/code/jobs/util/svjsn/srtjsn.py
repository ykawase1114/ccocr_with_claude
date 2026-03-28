#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   srtjsn.py   260327  cy
#
#   Sort lines in jsn4db pages into reading order:
#     - detect N-column layout via horizontal gap analysis
#     - left column top-to-bottom, then next column, etc.
#     - words within each line sorted by lft (left to right)
#
#   Algorithm:
#   [1] Group lines into visual rows:
#       a line joins a row if it overlaps vertically with any member
#       AND does not overlap horizontally with any member
#       (lines stacked in the same column go into separate rows)
#   [2] Only multi-line rows (2+ members) are used for gap analysis;
#       single-line rows have gaps everywhere and create spurious separators
#   [3] Contiguous high-gap regions wider than _MIN_GAP -> column separators
#   [4] Column sort applies only within the "column region":
#       lines with top <= last_multi_row_btm + _COL_BUFFER
#       Lines below this region are appended sorted by top (items table etc.)
#   [5] Within column region: sort by (col, top); sort words by lft
#
#--------1---------2---------3---------4---------5---------6---------7--------#

from m.prnt import prnt

_WIDTH      = 1200   # normalized coordinate width
_MIN_GAP    = 50     # minimum column separator width (normalized coords)
_MIN_COV    = 0.75   # gap must appear in this fraction of multi-line rows


# ---------------------------------------------------------------------------
# public entry point
# ---------------------------------------------------------------------------

def srtjsn(pages):
    """
    Sort lines (and words within lines) in reading order for each page.
    Modifies pages in-place and returns pages.
    """
    for page in pages:
        page['lines'] = _sort_lines(page['lines'])
    return pages


# ---------------------------------------------------------------------------
# internal helpers
# ---------------------------------------------------------------------------

def _sort_lines(lines):
    if not lines:
        return lines

    rows = _group_rows(lines)
    seps = _find_separators(rows)

    if seps:
        prnt(f'srtjsn: {len(seps)+1}-col  separators={seps}')
        tagged = sorted(
            ((_col_of(ln, seps), ln) for ln in lines),
            key=lambda t: (t[0], t[1]['top']))
        result = [ln for _, ln in tagged]
    else:
        result = sorted(lines, key=lambda l: l['top'])

    for ln in result:
        ln['words'] = sorted(ln['words'], key=lambda w: w['lft'])

    return result


def _group_rows(lines):
    """
    Group lines into visual rows.
    A line joins a row if it overlaps vertically with at least one member
    AND does not overlap horizontally with any member.
    Lines that overlap both vertically and horizontally are stacked in the
    same column and belong in separate rows.
    """
    srt = sorted(lines, key=lambda l: l['top'])
    rows = []

    for ln in srt:
        placed = False
        for row in rows:
            if _can_join(ln, row):
                row.append(ln)
                placed = True
                break
        if not placed:
            rows.append([ln])

    return rows


def _can_join(ln, row):
    """
    True if ln can join row:
    - overlaps vertically with at least one member
    - does not overlap horizontally with any member
    """
    v_ok = any(
        max(ln['top'], m['top']) < min(ln['btm'], m['btm'])
        for m in row)
    if not v_ok:
        return False
    return not any(
        max(ln['lft'], m['lft']) < min(ln['ryt'], m['ryt'])
        for m in row)


def _find_separators(rows):
    """
    Return sorted list of x-positions that are column separators.
    Only multi-line rows (2+ members) are used for gap detection.
    A separator is a contiguous horizontal gap (>= _MIN_GAP wide) that
    appears in >= _MIN_COV fraction of multi-line rows.
    """
    multi = [row for row in rows if len(row) >= 2]
    if len(multi) < 2:
        return []

    gap_cnt = [0] * _WIDTH

    for row in multi:
        covered = bytearray(_WIDTH)
        for ln in row:
            l = max(0, ln['lft'])
            r = min(_WIDTH, ln['ryt'])
            for x in range(l, r):
                covered[x] = 1
        for x in range(_WIDTH):
            if not covered[x]:
                gap_cnt[x] += 1

    threshold  = len(multi) * _MIN_COV
    separators = []
    in_gap     = False
    start      = 0

    for x in range(_WIDTH):
        if gap_cnt[x] >= threshold and not in_gap:
            in_gap, start = True, x
        elif gap_cnt[x] < threshold and in_gap:
            in_gap = False
            if x - start >= _MIN_GAP:
                separators.append((start + x) // 2)

    if in_gap and _WIDTH - start >= _MIN_GAP:
        separators.append((start + _WIDTH) // 2)

    return separators


def _col_of(line, seps):
    """Return column index (0-based) for a line given separator x-positions."""
    center = (line['lft'] + line['ryt']) // 2
    return sum(1 for s in seps if center > s)
