# -*- coding: utf-8 -*-
"""Builds the stakeholder deck: explorations/v4/presentation.html

Two outputs from one source, because they have different jobs:
  presentation.html           standalone, openable from disk
  presentation.artifact.html  body-only, for publishing (the host supplies the skeleton)

The three frames are embedded as 2x PNGs rendered from the PUBLISHED document's own
files, not re-hosted as live CSS. Three reasons: the deck then shows exactly the frames
that were signed off; no lane CSS can leak into the deck's own chrome, which the brief
asks for explicitly; and it keeps a second copy of the licence-unknown Bibush font out
of a published artifact.

    python3 explorations/v4/build_deck.py
"""
import base64, html, json, pathlib, shutil, subprocess, tempfile

HERE = pathlib.Path(__file__).resolve().parent
PAGE = HERE / "final-three-121.html"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
W, H, SCALE = 390, 780, 2

FRAMES = [("VintageKnesset.dc.html", "lane1"), ("NytGames.dc.html", "lane2"),
          ("Stickers.dc.html", "lane3")]

SHIM = """
class DCLogic {}
document.addEventListener('DOMContentLoaded', () => {
  const b = document.createElement('style');
  b.textContent = 'x-dc{display:block}helmet{display:none}';
  document.head.appendChild(b);
  document.querySelectorAll('x-dc > helmet > style').forEach(s => document.head.appendChild(s));
  const crop = document.createElement('style');
  crop.textContent = 'html,body{margin:0;padding:0;background:#9A9A97}' +
                     '.caption{display:none!important}' +
                     '.stage{padding:0!important;width:390px!important}' +
                     '.frame{box-shadow:none!important}';
  document.head.appendChild(crop);
});
"""

def render_frames():
    doc = json.loads(PAGE.read_text(encoding="utf-8")
                     .split('<script type="application/json" id="appifact-doc">')[1]
                     .split("</script>")[0])
    files = doc["content"]["files"]
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="v4deck-"))
    (tmp / "support.js").write_text(SHIM, encoding="utf-8")
    out = {}
    try:
        for src, lane in FRAMES:
            (tmp / src).write_text(files[src], encoding="utf-8")
            png = tmp / (lane + ".png")
            subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-sandbox",
                            "--hide-scrollbars", "--force-device-scale-factor=%d" % SCALE,
                            "--window-size=%d,%d" % (W, H), "--virtual-time-budget=6000",
                            "--screenshot=%s" % png, (tmp / src).as_uri()],
                           check=True, capture_output=True)
            out[lane] = base64.b64encode(png.read_bytes()).decode()
            print("  %s  %6.1f KB @%dx" % (lane, png.stat().st_size / 1024, SCALE))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return out

# ---------------------------------------------------------------- content
# The deck's prose is English. Two things stay Hebrew because they are names, not copy:
# the style titles, and everything inside the screens themselves.
DIRECTIONS = [
 dict(lane="lane1", n="1", he="כנסת של פעם", en="Vintage Knesset", blocks=[
  ("What it is",
   "The screen is a paper case file on a desk. The claim sits on a manila card inside a "
   "folder of differently tinted sheets, over a faintly printed colonnade ground, with a "
   "ruled margin down its binder edge and the uneven toning of a sheet that has been "
   "around a while. The issue image is a period photograph trimmed to its own outline "
   "and held down with a bulldog clip. Someone has been over the page with a highlighter "
   "and a strip of tape, and the bill's own date is stuck to the corner on a faded "
   "label."),
  ("Why it fits",
   "The game's material is real Knesset records — bill texts, dates, votes. This "
   "direction makes the record itself the visual material, so the interface is the "
   "evidence rather than a frame around it. To someone voting for the first time the "
   "Knesset tends to sound abstract; a document you can see has been handled makes it "
   "concrete."),
  ("References",
   "Papers, Please (Lucas Pope, 2013) — its document world, and the brown desk with "
   "differently tinted papers on it. The display face is Bibush, a Hebrew pixel "
   "typeface, used for the headline and the date label. The repeating background is a "
   "plain portico, drawn on purpose rather than borrowed: the Knesset's own emblem is a "
   "trademark, and a real official mark printed across the page would claim an "
   "authenticity this game does not have."),
  ("The risk",
   "The most expensive direction to produce: every round needs an image treated as a "
   "cut-out and an artifact layer repositioned for it. Bibush is also missing the "
   "hyphen and the slash — solved here with CSS boxes, but 4 of the 16 existing titles "
   "need them and any new title with punctuation will too. And the font's licence is "
   "unknown, so it cannot ship as it stands."),
 ]),
 dict(lane="lane2", n="2", he="משחקי עיתון", en="NYT Games", blocks=[
  ("What it is",
   "A quiet white card, one very large headline, a small illustrative disc, and two "
   "outlined buttons. The deck of coloured card backs behind it is the only colour on "
   "screen."),
  ("Why it fits",
   "This audience already plays Wordle and Connections, so the visual grammar is "
   "familiar and the cost of learning the game is low. The restraint suits content that "
   "is factual and sometimes uncomfortable — nothing in the styling takes a position. "
   "It also holds up best across 16 rounds: it keeps the headline at 66px for 8 of the "
   "16 real titles, more than either other direction."),
  ("References",
   "NYT Games — the typographic confidence of one headline carrying the whole screen, "
   "the flat tile palette, and the outlined-button pattern."),
  ("The risk",
   "The least exciting at first glance. On a phone home screen, beside other apps, it "
   "does not announce itself. Against that, it is the most durable of the three: the "
   "least likely to feel repetitive or shouty by round ten."),
 ]),
 dict(lane="lane3", n="3", he="תרבות סטיקרים", en="Israeli Sticker Culture", blocks=[
  ("What it is",
   "A sticker on a pole: a glossy photograph die-cut to its own silhouette with a thick "
   "white margin, a headline in a black slogan box, and a deck of mixed-colour backs "
   "behind it."),
  ("Why it fits",
   "It borrows an Israeli street language this audience meets daily — stickers on "
   "bumpers, on poles, at bus stops. It makes a civic subject feel local rather than "
   "institutional, without softening the content itself."),
  ("References",
   "Israeli sticker and bumper-sticker culture, which is a documented political genre "
   "in its own right: «שירת הסטיקר» (HaDag Nahash, lyrics by David Grossman, 2004) is "
   "built entirely out of bumper-sticker slogans."),
  ("The risk",
   "Since the frames were merged the palette no longer varies by topic — the deck of "
   "backs is fixed and only the front card's fill changes, so across 16 rounds this "
   "direction varies less than it was meant to. It is also the loudest of the three, "
   "and so the most likely to read as a game about politics rather than a record of "
   "it. Its black headline box is expensive in width, which is why its headline drops "
   "to 34px where direction 2 still holds 38px."),
 ]),
]

OPEN = [
 ("Screens are current",
  "Each screen here is a direct capture of the board as it stands, not a mock-up of it. "
  "Where a direction had competing variants — two clip treatments, two palettes for "
  "direction 3, a louder pass at direction 1 — those have been decided and the losing "
  "versions removed, so what is shown is the only version that exists."),
 ("Bibush typeface",
  "Licence unknown. Sketch use only — it cannot go to production as it stands."),
 ("Unverified reference",
  "The brief named «טיפוגרפיית העטיפה של הרדיקל» as a possible touchstone for direction "
  "3. I have no basis for verifying what it refers to, so it is not in the references "
  "above. If it is relevant, someone who knows it should add that line."),
]

# ---------------------------------------------------------------- page
HEAD = """<title>בחירת כיוון · הח״כ ה-121</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Assistant:wght@400;600;700&family=Frank+Ruhl+Libre:wght@700&display=swap">
<style>
/* The deck's own world is deliberately none of the three it presents: a cool-biased
   neutral where lane 1 is warm khaki, lane 3 is pole grey and lane 2 near-white; and a
   serif for the names, which no lane uses. It cannot be mistaken for a fourth
   direction. Frank Ruhl Libre carries Hebrew and Latin, so the Hebrew style names and
   the English prose share one voice. */
:root{
  --ground:#FBFBFC; --surface:#F1F2F5; --bed:#E7E9ED;
  --ink:#17181B; --soft:#5B5F68; --rule:#DEE0E5; --accent:#3C4A63;
  --serif:"Frank Ruhl Libre",Georgia,"Times New Roman",serif;
  --sans:"Assistant","Segoe UI",system-ui,-apple-system,Arial,sans-serif;
}
@media (prefers-color-scheme: dark){
  :root:not([data-theme="light"]){
    --ground:#131417; --surface:#1A1C21; --bed:#101115;
    --ink:#ECEDF0; --soft:#9EA3AD; --rule:#2C2F36; --accent:#9DB0D0;
  }
}
:root[data-theme="dark"]{
  --ground:#131417; --surface:#1A1C21; --bed:#101115;
  --ink:#ECEDF0; --soft:#9EA3AD; --rule:#2C2F36; --accent:#9DB0D0;
}
*{box-sizing:border-box}
body{margin:0;background:var(--ground);color:var(--ink);font-family:var(--sans);
  direction:ltr;font-size:15px;line-height:1.65;font-variant-numeric:tabular-nums;
  -webkit-font-smoothing:antialiased}
.wrap{max-width:1420px;margin:0 auto;padding:56px 32px 72px;display:flex;
  flex-direction:column;gap:44px}

.masthead{display:flex;flex-direction:column;gap:10px;padding-bottom:26px;
  border-bottom:1px solid var(--rule)}
.eyebrow{align-self:flex-start;font-size:12px;font-weight:700;letter-spacing:.14em;
  color:var(--accent)}
h1{margin:0;font-family:var(--serif);font-weight:700;font-size:34px;line-height:1.25;
  letter-spacing:-.01em;text-wrap:balance}
.standfirst{margin:0;max-width:68ch;color:var(--soft);font-size:16px}

.grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:40px;align-items:start}
.dir{display:flex;flex-direction:column;gap:20px;min-width:0}
.dir-head{display:flex;flex-direction:column;gap:3px}
.dir-num{font-size:11.5px;font-weight:700;letter-spacing:.16em;color:var(--accent);
  text-transform:uppercase}
/* the style name is a name, so it stays Hebrew and gets its own direction */
.dir-name{align-self:flex-start;margin:0;font-family:var(--serif);font-weight:700;
  font-size:27px;line-height:1.2}
.dir-en{font-size:11.5px;font-weight:600;letter-spacing:.13em;color:var(--soft);
  text-transform:uppercase}
.shot{margin:0;background:var(--bed);border:1px solid var(--rule);border-radius:3px;
  padding:20px;display:flex;justify-content:center}
.shot img{display:block;width:100%;max-width:390px;height:auto}
.case{display:flex;flex-direction:column;gap:16px}
.block{display:flex;flex-direction:column;gap:5px;padding-top:16px;
  border-top:1px solid var(--rule)}
.block:first-child{padding-top:0;border-top:0}
.block h3{margin:0;font-size:11px;font-weight:700;letter-spacing:.14em;color:var(--accent);
  text-transform:uppercase}
.block p{margin:0;font-size:14.5px;line-height:1.7}
.risk h3{color:var(--ink)}
.risk p{color:var(--soft)}
.he{font-family:var(--sans);font-weight:600}

.open{background:var(--surface);border:1px solid var(--rule);border-radius:3px;
  padding:28px 30px;display:flex;flex-direction:column;gap:18px}
.open > h2{margin:0;font-family:var(--serif);font-weight:700;font-size:20px}
.open dl{margin:0;display:grid;grid-template-columns:minmax(180px,240px) 1fr;
  gap:14px 26px;align-items:baseline}
.open dt{font-size:12px;font-weight:700;letter-spacing:.05em;color:var(--accent)}
.open dd{margin:0;font-size:14.5px;color:var(--soft);max-width:82ch}

.colophon{display:flex;flex-wrap:wrap;gap:8px 24px;padding-top:22px;
  border-top:1px solid var(--rule);font-size:13px;color:var(--soft)}
.colophon a{color:var(--accent);text-decoration-thickness:1px;text-underline-offset:3px}
.colophon a:focus-visible{outline:2px solid var(--accent);outline-offset:3px;border-radius:2px}

@media (max-width:1180px){
  .grid{grid-template-columns:1fr;gap:56px}
  .open dl{grid-template-columns:1fr;gap:4px 0}
  .open dd{padding-bottom:12px}
  .wrap{padding:40px 22px 56px}
}
</style>"""

def esc(t):
    return html.escape(t, quote=False)

def he(t):
    """Hebrew inside English prose needs its own direction or the punctuation drifts."""
    return '<span class="he" dir="rtl" lang="he">%s</span>' % esc(t)

def body(shots):
    cols = []
    for d in DIRECTIONS:
        blocks = []
        for lbl, txt in d["blocks"]:
            t = esc(txt)
            for h in ("שירת הסטיקר", "טיפוגרפיית העטיפה של הרדיקל"):
                t = t.replace(esc(h), he(h))
            blocks.append('        <div class="block%s">\n          <h3>%s</h3>\n'
                          '          <p>%s</p>\n        </div>'
                          % (" risk" if lbl == "The risk" else "", esc(lbl), t))
        cols.append("""    <section class="dir">
      <header class="dir-head">
        <span class="dir-num">Direction %s</span>
        <h2 class="dir-name" dir="rtl" lang="he">%s</h2>
        <span class="dir-en">%s</span>
      </header>
      <figure class="shot"><img src="data:image/png;base64,%s" width="390" height="780" alt="The round screen in the %s direction"></figure>
      <div class="case">
%s
      </div>
    </section>""" % (esc(d["n"]), esc(d["he"]), esc(d["en"]), shots[d["lane"]],
                     esc(d["en"]), "\n".join(blocks)))

    items = []
    for t, b in OPEN:
        bb = esc(b)
        for h in ("טיפוגרפיית העטיפה של הרדיקל",):
            bb = bb.replace(esc(h), he(h))
        items.append('        <dt>%s</dt>\n        <dd>%s</dd>' % (esc(t), bb))

    return """<div class="wrap">
  <header class="masthead">
    <span class="eyebrow" dir="rtl" lang="he">הח״כ ה-121</span>
    <h1>Three directions for the round screen</h1>
    <p class="standfirst">Each direction is shown as one screen — the %s round — with what it is, why it fits, the references it draws on, and one real risk. The screens are direct captures of what was built, unaltered.</p>
  </header>

  <div class="grid">
%s
  </div>

  <section class="open">
    <h2>Still open</h2>
    <dl>
%s
    </dl>
  </section>

  <footer class="colophon">
    <span>Screens are 390px wide. Round r1 from data.js, wording verbatim.</span>
    <span>Interactive board with every frame: <a href="https://claude.ai/code/artifact/33df1ff5-dede-4dcd-8979-38d9adff560e">שלושת הכיוונים</a></span>
  </footer>
</div>""" % (he("חוק הגיוס"), "\n".join(cols), "\n".join(items))

def build():
    print("rendering frames at %dx…" % SCALE)
    shots = render_frames()
    b = body(shots)
    (HERE / "presentation.artifact.html").write_text(HEAD + "\n" + b + "\n", encoding="utf-8")
    (HERE / "presentation.html").write_text(
        '<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        + HEAD + "\n</head>\n<body>\n" + b + "\n</body>\n</html>\n", encoding="utf-8")
    for f in ("presentation.html", "presentation.artifact.html"):
        print("%-30s %7.1f KB" % (f, (HERE / f).stat().st_size / 1024))

if __name__ == "__main__":
    build()
