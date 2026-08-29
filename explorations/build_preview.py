# -*- coding: utf-8 -*-
"""Assembles the artboards into one horizontally-scrolling review page:
explorations/directions.html — same CSS and markup, no canvas runtime."""
import pathlib, re, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import build_v3 as B

OUT = B.OUT
shared = B.SHARED.replace("%FONT%", B.FONT)

styles, stages = [], []
for lane in B.LANES:
    src = (OUT / lane["file"]).read_text(encoding="utf-8")
    css = re.search(r"<style>.*?\n(/\* LANE.*?)\n  </style>", src, re.S).group(1)
    styles.append(css)
    stage = re.search(r'(<div class="stage .*?)\n</x-dc>', src, re.S).group(1)
    stages.append(stage)

logic = "/* v3 artboards are static — the canvas-pixelation technique was replaced by Bibush Chunky */"

page = """<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>כיווני עיצוב · הח״כ ה-121</title>
<style>
%SHARED%
.row{display:flex;flex-direction:row;gap:26px;padding:22px;overflow-x:auto;align-items:flex-start;min-height:100vh}
@supports not (overflow-x: auto){.row{flex-wrap:wrap}}
%LANES%
</style>
</head>
<body>
<div class="row">
%STAGES%
</div>
<script>
%LOGIC%
</script>
</body>
</html>
""".replace("%SHARED%", shared).replace("%LANES%", "\n\n".join(styles)) \
   .replace("%STAGES%", "\n\n".join(stages)).replace("%LOGIC%", logic)

(OUT / "directions.html").write_text(page, encoding="utf-8")
print("directions.html  %.1f KB" % ((OUT / "directions.html").stat().st_size / 1024))
