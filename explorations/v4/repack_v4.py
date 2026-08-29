# -*- coding: utf-8 -*-
"""Swaps the freshly built v4 artboards into the published board in place.

explorations/v4/final-three-121.html is a published design canvas: the whole
editable document (the six .dc.html sources + canvas.json + the title) lives in
the JSON script block with id "appifact-doc"; the rest of the file is the canvas
editor bundle. This rewrites only that block, byte-for-byte compatible with how
the canvas serialises it, so the page stays the same document at the same URL —
opening it and hitting Save republishes it.

Run after build_v4.py:  python3 explorations/v4/repack_v4.py
"""
import json, pathlib

OUT  = pathlib.Path(__file__).resolve().parent
PAGE = OUT / "final-three-121.html"
TAG  = '<script type="application/json" id="appifact-doc">'
# v4.4 CHANGE A — one frame per lane, plus lane 3's second button option.
FILES = ["Main.dc.html", "NytGames.dc.html", "Stickers.dc.html",
         "StickersAltButtons.dc.html", "canvas.json"]

def dump(doc):
    # the canvas writes compact JSON, non-ASCII literal, and escapes only "<"
    # so the payload can never terminate its own <script> element
    return "\n" + json.dumps(doc, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c") + "\n"

def repack():
    page = PAGE.read_text(encoding="utf-8")
    i = page.index(TAG) + len(TAG)
    j = page.index("</script>", i)
    doc = json.loads(page[i:j])

    stale = [f for f in doc["content"]["files"] if f not in FILES]
    for f in stale:
        del doc["content"]["files"][f]
    missing = [f for f in FILES if not (OUT / f).exists()]
    assert not missing, missing
    changed = []
    for f in FILES:
        new = (OUT / f).read_text(encoding="utf-8")
        if doc["content"]["files"].get(f) != new:
            changed.append(f)
            doc["content"]["files"][f] = new

    PAGE.write_text(page[:i] + dump(doc) + page[j:], encoding="utf-8")
    print("final-three-121.html  %.1f KB  ·  %d/%d artboard files updated"
          % (PAGE.stat().st_size / 1024, len(changed), len(FILES)))
    for f in changed:
        print("   ", f)
    for f in stale:
        print("    removed", f)

if __name__ == "__main__":
    repack()
