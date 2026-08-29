# -*- coding: utf-8 -*-
"""Measures every real issue title from data.js against every lane's title box.

Why this exists: the lane 3 title size was originally pinned to «חוק הגיוס», the one
title we happened to be showing, and 15 of the other 16 did not fit. Sizes are no
longer guessed — this renders each title in the lane's OWN box, with the lane's own
font, at each rung of that lane's ladder, and keeps the largest rung that fits in two
balanced lines without an unbreakable word overflowing.

Sources are the built artboards, so the geometry measured is the geometry shipped.
Output: title-steps.json, read by build_v4.py.

    python3 explorations/v4/measure_titles.py
"""
import json, pathlib, re, shutil, subprocess, tempfile

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent.parent
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# the ladder per lane. Every rung must stay >= that lane's claim size: a title set
# smaller than the sentence under it is not a title.
LADDERS = {
    "lane1": dict(file="Main.dc.html",     steps=[66, 58, 50, 44, 38, 34, 30], claim=16),
    "lane2": dict(file="NytGames.dc.html", steps=[66, 58, 50, 44, 38, 34],     claim=19),
    "lane3": dict(file="Stickers.dc.html", steps=[58, 50, 44, 38, 34, 30],     claim=20),
}
MAX_LINES = 2

SHIM = """
class DCLogic {}
document.addEventListener('DOMContentLoaded', () => {
  const b = document.createElement('style');
  b.textContent = 'x-dc{display:block}helmet{display:none}';
  document.head.appendChild(b);
  document.querySelectorAll('x-dc > helmet > style').forEach(s => document.head.appendChild(s));
});
"""

MEASURE = """
window.__measure = (titles, steps, maxLines) => {
  const el = document.querySelector('.issue-title');
  const out = {};
  const lineCount = e => {
    const r = document.createRange(); r.selectNodeContents(e);
    const tops = new Set([...r.getClientRects()].map(x => Math.round(x.top)));
    return tops.size || 1;
  };
  const orig = el.textContent, origSize = el.style.fontSize;
  for (const t of titles) {
    el.textContent = t;
    let chosen = null, detail = [];
    for (const fs of steps) {
      el.style.fontSize = fs + 'px';
      const lines = lineCount(el);
      const overflow = el.scrollWidth > el.clientWidth + 1;
      detail.push({fs, lines, overflow});
      if (!overflow && lines <= maxLines) { chosen = fs; break; }
    }
    out[t] = {step: chosen, detail};
  }
  el.textContent = orig; el.style.fontSize = origSize;
  return out;
};
"""

def titles():
    s = (ROOT / "data.js").read_text(encoding="utf-8")
    i = s.index("{")
    d, _ = json.JSONDecoder().raw_decode(s[i:])
    return [v["title"] for v in d["issues"]]

def run():
    ts = titles()
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="v4titles-"))
    (tmp / "support.js").write_text(SHIM, encoding="utf-8")
    result = {}
    try:
        for lane, cfg in LADDERS.items():
            src = (HERE / cfg["file"]).read_text(encoding="utf-8")
            # the title must wrap and balance while being measured, exactly as it will ship
            src = src.replace("</style>",
                ".issue-title{white-space:normal;text-wrap:balance}\n  </style>", 1)
            src = src.replace("</body>", "<script>%s</script>\n"
                "<pre id=\"out\" hidden></pre>\n"
                "<script>document.fonts.ready.then(()=>{"
                "document.getElementById('out').textContent="
                "JSON.stringify(window.__measure(%s,%s,%d));});</script>\n</body>"
                % (MEASURE, json.dumps(ts, ensure_ascii=False),
                   json.dumps(cfg["steps"]), MAX_LINES), 1)
            page = tmp / ("m_" + cfg["file"])
            page.write_text(src, encoding="utf-8")
            dom = subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-sandbox",
                                  "--virtual-time-budget=8000", "--dump-dom", page.as_uri()],
                                 check=True, capture_output=True).stdout.decode("utf-8")
            m = re.search(r'<pre id="out" hidden="">(.*?)</pre>', dom, re.S)
            assert m and m.group(1).strip(), "no measurement came back for " + lane
            data = json.loads(m.group(1))
            for t, v in data.items():
                assert v["step"] is not None, (lane, t, v["detail"])
                assert v["step"] >= cfg["claim"], (lane, t, v["step"], cfg["claim"])
            result[lane] = {t: v["step"] for t, v in data.items()}
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    (HERE / "title-steps.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=1), encoding="utf-8")
    for lane, cfg in LADDERS.items():
        hist = {}
        for t in ts:
            hist[result[lane][t]] = hist.get(result[lane][t], 0) + 1
        print(lane, "claim %dpx" % cfg["claim"], "->",
              " ".join("%dpx:%d" % (k, hist[k]) for k in sorted(hist, reverse=True)))
    return result

if __name__ == "__main__":
    run()
