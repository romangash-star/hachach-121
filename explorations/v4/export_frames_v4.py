# -*- coding: utf-8 -*-
"""Exports the six v4.2 frames as 1x PNGs, 390x780 each.

Sources are read out of the PUBLISHED document's own serialisation block
(v4/final-three-121.html -> script#appifact-doc -> content.files), not from the
build outputs, so the PNGs are evidence of what that document actually contains.

The canvas runtime's support.js only exists on the published origin, so a small
shim stands in for it: the artboards are static (Component.renderVals() returns
{}), it just needs DCLogic to exist and the <helmet> styles hoisted.

    python3 explorations/v4/export_frames_v4.py
"""
import json, pathlib, shutil, subprocess, tempfile

HERE = pathlib.Path(__file__).resolve().parent
PAGE = HERE / "final-three-121.html"
DEST = HERE / "frames-1x"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
W, H = 390, 780

NAMES = {
    "Main.dc.html":              "lane1-defaced-paperwork",
    "NytGames.dc.html":          "lane2-nyt-games",
    "Stickers.dc.html":          "lane3-stickers-buttons-a",
    "StickersAltButtons.dc.html": "lane3-stickers-buttons-b",
}

SHIM = """
/* stand-in for the canvas runtime's support.js — render-only */
class DCLogic {}
document.addEventListener('DOMContentLoaded', () => {
  const base = document.createElement('style');
  base.textContent = 'x-dc{display:block}helmet{display:none}';
  document.head.appendChild(base);
  document.querySelectorAll('x-dc > helmet > style').forEach(s => document.head.appendChild(s));
  const crop = document.createElement('style');   /* frame only, no caption strip */
  crop.textContent = 'html,body{margin:0;padding:0;background:#9A9A97}' +
                     '.caption{display:none!important}' +
                     '.stage{padding:0!important;width:390px!important}' +
                     '.frame{box-shadow:none!important}';
  document.head.appendChild(crop);
});
"""

def export():
    doc = json.loads(PAGE.read_text(encoding="utf-8")
                     .split('<script type="application/json" id="appifact-doc">')[1]
                     .split("</script>")[0])
    files = doc["content"]["files"]
    assert set(NAMES) <= set(files), sorted(files)

    DEST.mkdir(exist_ok=True)
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="v4frames-"))
    (tmp / "support.js").write_text(SHIM, encoding="utf-8")
    try:
        for src, out in NAMES.items():
            (tmp / src).write_text(files[src], encoding="utf-8")
            png = DEST / (out + ".png")
            subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-sandbox",
                            "--hide-scrollbars", "--force-device-scale-factor=1",
                            "--window-size=%d,%d" % (W, H), "--virtual-time-budget=5000",
                            "--screenshot=%s" % png, (tmp / src).as_uri()],
                           check=True, capture_output=True)
            print(out.ljust(36), "%6.1f KB" % (png.stat().st_size / 1024))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print("->", DEST)

if __name__ == "__main__":
    export()
