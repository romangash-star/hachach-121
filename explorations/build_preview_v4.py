# -*- coding: utf-8 -*-
"""Assembles the six v4 artboards into one review page: explorations/v4/final-three.html"""
import pathlib, re, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import build_v4 as B

OUT = B.OUT
shared = B.SHARED.replace("%FONT%", B.FONT)
styles, stages, seen = [], [], set()
order = []
for lane in B.LANES:
    for tid in ("religion", "branches"):
        f = lane["file"] if tid == "religion" else lane["file"].replace(".dc.html", "Branches.dc.html")
        order.append((f, lane, tid))
for f, lane, tid in order:
    src = (OUT / f).read_text(encoding="utf-8")
    if lane["cls"] not in seen:
        styles.append(re.search(r"<style>.*?\n(/\* LANE.*?)\n  </style>", src, re.S).group(1))
        seen.add(lane["cls"])
    stages.append(re.search(r'(<div class="stage .*?)\n</x-dc>', src, re.S).group(1))

rows = [stages[0], stages[2], stages[4]], [stages[1], stages[3], stages[5]]
page = """<!DOCTYPE html>
<html lang="he" dir="rtl">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>שלושת הכיוונים · הח״כ ה-121</title>
<style>
%SHARED%
.row{display:flex;flex-direction:row;gap:26px;padding:22px;align-items:flex-start}
%LANES%
</style></head>
<body>
<div class="row">%R1%</div>
<div class="row">%R2%</div>
</body></html>
""".replace("%SHARED%", shared).replace("%LANES%", "\n\n".join(styles)) \
   .replace("%R1%", "\n".join(rows[0])).replace("%R2%", "\n".join(rows[1]))
(OUT / "final-three.html").write_text(page, encoding="utf-8")
print("final-three.html  %.1f KB" % ((OUT / "final-three.html").stat().st_size / 1024))
