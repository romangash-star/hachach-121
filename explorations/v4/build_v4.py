# -*- coding: utf-8 -*-
"""v4.2 — Final Three. 3 lanes x 2 topic-colour frames = 6 artboards.
Published as its OWN canvas (final-three-121.html); the six-lane v3 board
at visual-directions-121.html is untouched.
Regenerate:  python3 explorations/v4/build_v4.py
"""
import base64, json, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
OUT  = ROOT / "explorations" / "v4"
OUT.mkdir(exist_ok=True)
# v4.4 — title sizes are MEASURED, not chosen. measure_titles.py renders every issue
# title from data.js in each lane's own box and records the largest ladder rung that
# fits in two balanced lines; build_v4.py just reads the answer. Regenerate with
#   python3 explorations/v4/measure_titles.py
def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def bibush_title(t):
    """Lane 1's title, set in Bibush Chunky, which has no - and no / .
    Both are drawn as CSS boxes on the font's own stroke (.px-punct), the same
    mechanism the caption strip demonstrates — the font files are never touched.
    A digit/digit run is wrapped dir=ltr: with the real slash gone the two numbers
    become separate runs and the bidi algorithm would otherwise reorder them
    («7/10» coming out as «10 7»). 4 of the 16 real titles need this."""
    # Both passes emit markup whose own class names contain "-", so the source hyphens
    # are parked on a sentinel first and swapped in last. Substituting them in place
    # rewrote «px-punct px-slash» into nested tags — silently, and only in the four
    # titles that carry punctuation.
    SENT = "\x01"
    t = esc(t).replace("-", SENT)
    t = re.sub(r"(\d+)/(\d+)",
               r'<span dir="ltr">\1<i class="px-punct px-slash"></i>\2</span>', t)
    # <wbr> after the box gives back the line-break opportunity a real hyphen carries:
    # the boxes are elements, not characters, so the line breaker sees nothing there.
    # None inside the digit run — «7/10» should never be split across lines.
    return t.replace(SENT, '<i class="px-punct px-hyphen"></i><wbr>')

TITLE_STEPS = json.loads((pathlib.Path(__file__).resolve().parent / "title-steps.json")
                         .read_text(encoding="utf-8"))
# v4.5 — three rungs, not six. A headline that is 66px one round and 34px two rounds
# later changes the card's character as you play; steadiness beats the extra loudness
# on short titles. The top rung is where r1 already sat and does not move; the bottom
# rung is the floor the six-rung measurement found, so nothing falls below its claim.
LADDER = {"lane1": [66, 50, 34],
          "lane2": [66, 50, 38],
          "lane3": [58, 44, 34]}

FONT   = base64.b64encode((ROOT / "fonts" / "SimplerPro_HLAR-Black.woff2").read_bytes()).decode()
BIBUSH = base64.b64encode((ROOT / "fonts" / "BibushChunky.v1.0.otf").read_bytes()).decode()

# ---- verbatim r1 content ---------------------------------------------------
COINS   = "240"
TITLE   = "חוק הגיוס"
CLAIM_A = "הצעת חוק הגיוס שהקואליציה קידמה ב-2024 מבוססת על "
CLAIM_B = "מתווה שכתב... בני גנץ"
ANS_T   = "אמת"
ANS_F   = "שקר"
# v4.3 CHANGE 1 — the source chip is GONE from the claim card.
# Sources belong to the reveal beat, not the guess beat: the round arc is
# claim -> own vote -> neutral context (bill_title + bill_date) -> MK cascade ->
# full reveal (tf_explain + tally + resolution + SOURCES). A named outlet shown
# before the player answers is also a partisan cue - a player who knows the
# outlet's lean can read the masthead as a hint about how the claim resolves.
# SOURCE = "ישראל היום"   # returns on the reveal card, not here.
BILLDATE = "11 ביוני 2024"   # data.js  issues[r1].bill_date — the sticker's date stamp
ART     = "🪖"
MAP     = "מפה"
LONGTITLE = "מדינה פלסטינית: התנגדות עקרונית"   # data.js issues[m2].title — the longest of the 16
LONGNOTE  = " · מקרה קצה: הכותרת הארוכה ביותר"
PUNCTTITLE = "ועדת חקירה ל-7/10"   # data.js issues[a1].title — the only one with both - and /
PUNCTNOTE  = " · מקרה קצה: פיסוק שחסר ב-Bibush, מצויר בקופסאות CSS"

# v4.3 CHANGE 1, optional half — OFF. See the .verified block in SHARED.
# True renders a bare check glyph (no outlet, no words) where the source chip was.
VERIFY_MARK = False
VERIFY_HTML = ('          <p class="verified"><svg class="ico-check" viewBox="0 0 24 24" '
               'aria-hidden="true"><path d="M4 12.7l5.4 5.3L20 6.9"></path></svg></p>\n')
TOPICS  = {"religion": "דת ומדינה", "branches": "מי מחליט פה?"}

SHARED = """
@font-face{font-family:'SimplerPro';src:url(data:font/woff2;base64,%FONT%) format('woff2');font-weight:900;font-style:normal;font-display:block}
*{margin:0;padding:0;box-sizing:border-box}
body{background:#9A9A97;font-family:system-ui,"Segoe UI",Arial,sans-serif;font-variant-numeric:tabular-nums;-webkit-font-smoothing:antialiased}
a{color:#1a3acc}
a:hover{color:#0f2894}

/* ---- caption strip: annotation space, outside the frame ---- */
.stage{width:390px;background:#9A9A97;padding-bottom:24px}
.caption{display:flex;flex-wrap:wrap;align-items:baseline;gap:4px 9px;padding:16px 16px 12px;color:#141414}
.cap-num{font-family:'SimplerPro',system-ui,sans-serif;font-weight:900;font-size:26px;line-height:.9}
.cap-he{font-weight:700;font-size:15px;line-height:1.2}
.cap-en{font-size:11.5px;letter-spacing:.05em;text-transform:uppercase;color:#2A2A28}
.cap-meta{flex-basis:100%;font-size:10.5px;color:#2A2A28}
.cap-spec{display:none;flex-basis:100%;margin-top:6px;padding:7px 10px;background:#EFEDE6;
  color:#1A1714;border:1px solid #7E7C74}
.cap-spec b{display:block;font-size:9.5px;font-weight:700;letter-spacing:.12em;color:#4A4740;
  margin-bottom:3px}

/* ---- the frame ---- */
.frame{position:relative;width:390px;min-height:780px;overflow:hidden;isolation:isolate;
  display:flex;flex-direction:column;padding:12px 16px 20px;box-shadow:0 3px 14px rgba(0,0,0,.3)}
.frame-bg{position:absolute;inset:0;z-index:0;pointer-events:none}
.deco{position:absolute;inset:0;width:100%;height:100%;z-index:0;pointer-events:none}
.deco g{display:none}

/* ---- HUD v3: [coins] .......... [topic + steps] .......... [map][avatar] ---- */
.hud{position:relative;z-index:4;flex:none;min-height:46px;display:flex;align-items:center;
  justify-content:space-between;gap:8px}
.hud-coins{display:flex;align-items:center;gap:7px;flex:none}
.coin-glyph{width:22px;height:22px;flex:none;display:grid;place-items:center;border-radius:50%}
.coin-num{font-family:'SimplerPro',system-ui,sans-serif;font-weight:900;font-size:20px;line-height:1}
.hud-mid{display:flex;flex-direction:column;align-items:center;gap:6px;min-width:0}
.topic-title{font-size:12.5px;font-weight:700;line-height:1.2;white-space:nowrap;padding:3px 0}
/* three step dots = the three beats of the round; the pile behind the card is those same three */
.steps{display:flex;align-items:center;gap:5px}
.step{width:7px;height:7px;border-radius:50%;background:currentColor;opacity:.32;display:block}
.step-on{opacity:1;width:17px;border-radius:4px}
.hud-you{display:flex;align-items:center;gap:6px;flex:none}
.map-btn{width:44px;height:44px;flex:none;border:0;background:none;color:inherit;cursor:pointer;
  display:grid;place-items:center;padding:0;border-radius:50%}
.map-icon{width:21px;height:21px;fill:none;stroke:currentColor;stroke-width:1.9;stroke-linejoin:round;
  stroke-linecap:round}
.map-btn:focus-visible{outline:3px solid #0052ff;outline-offset:2px}
.avatar{position:relative;width:40px;height:40px;flex:none;border-radius:50%;overflow:hidden;
  display:grid;place-items:center}
.avatar-sil{width:76%;height:76%;display:block}

/* ---- deck: card + its attached buttons, over exactly three beat-card backs ---- */
.deck{position:relative;z-index:1;flex:1;display:flex;flex-direction:column;align-items:center;
  justify-content:center;padding-top:24px}
.stack{position:relative;width:340px;height:470px;flex:none}
.pile{position:absolute;inset:0;pointer-events:none}
.pile-card{position:absolute;inset:0}
.pile-1{transform:translateY(-10px) rotate(-1.9deg)}
.pile-2{transform:translateY(-19px) rotate(3.1deg)}
.pile-3{transform:translateY(-28px) rotate(-4.8deg)}
.card{position:relative;z-index:2;width:100%;height:100%;display:flex;flex-direction:column;
  padding:16px 20px 16px}
.art{position:relative;flex:1;min-height:130px;display:flex;align-items:center;justify-content:center}
.art-emoji{font-size:96px;line-height:1;display:block}
.art-clip{display:none;position:absolute;width:26px;height:58px;fill:none;stroke:currentColor;
  stroke-width:3.4;stroke-linecap:round}
.sticker{display:none}
/* v4.4 — a title may take two lines, balanced. The size that keeps it to two comes
   from the per-lane .ts-* rung the stage carries; see TITLE_STEPS. */
.issue-title{margin-top:4px;font-family:'SimplerPro',system-ui,sans-serif;font-weight:900;
  font-size:36px;line-height:1.04;text-wrap:balance}
.claim-text{margin-top:10px;font-size:16px;line-height:1.5;font-weight:700;text-wrap:balance}
.hl{background:none;color:inherit}
/* v4.2 FIX 3 — the in-card swipe hints are gone. The buttons ARE the affordance;
   the direction now lives on the arrow inside each button (.ans-arrow). */
/* ---- OPTIONAL, OFF BY DEFAULT: set VERIFY_MARK = True to render ----------
   data.js carries verification:"verified" on this issue. A bare check in the
   source chip's old slot signals "documented record" without naming an outlet.
   Ships only if review accepts it; it needs a Hebrew aria-label first, and that
   is a copy decision, not a build one - no copy is invented here.          */
.verified{margin-top:auto;padding-top:12px;display:flex}
.ico-check{width:20px;height:20px;flex:none;fill:none;stroke:currentColor;stroke-width:2.8;
  stroke-linecap:round;stroke-linejoin:round;opacity:.6}

/* buttons ride with the card: same width, 8px gap, one object */
.answers{position:relative;z-index:3;flex:none;width:340px;display:flex;gap:10px;margin-top:8px}
.ans{position:relative;flex:1;min-height:56px;appearance:none;cursor:pointer;border:0;background:none;
  color:inherit;font-family:'SimplerPro',system-ui,sans-serif;font-weight:900;font-size:22px;
  line-height:1;padding:16px 10px;display:flex;align-items:center;justify-content:center;gap:9px}
/* the two surfaces stay identical; only the arrow differs, and only in direction.
   RTL row-reverse puts אמת's arrow on the right edge pointing right; שקר's on the
   left pointing left — the same mapping the removed .hint pair carried. */
.ans-true{flex-direction:row-reverse}
.ans-arrow{width:20px;height:20px;flex:none;fill:none;stroke:currentColor;stroke-width:2.6;
  stroke-linecap:round;stroke-linejoin:round}
.ans-false .ans-arrow{transform:scaleX(-1)}
.ans:focus-visible{outline:3px solid #0052ff;outline-offset:3px}

@media (prefers-reduced-motion: reduce){*{animation:none !important;transition:none !important}}
"""

BODY = """<div class="stage %LANE% topic-%TOPICID%%VARCLS%">
  <header class="caption" dir="rtl" lang="he">
    <span class="cap-num">%NUM%</span>
    <span class="cap-he">%HE%</span>
    <span class="cap-en" dir="ltr">%EN%</span>
    <span class="cap-meta">טקסט: פונט זמני · נושא: %TOPIC%%DISPNOTE%</span>
    <span class="cap-spec"><b>BIBUSH CHUNKY · פיסוק חסר, מוחלף בקופסאות CSS</b><span class="spec-line">ועדת חקירה ל<i class="px-punct px-hyphen"></i><span dir="ltr">7<i class="px-punct px-slash"></i>10</span></span></span>
  </header>

  <div class="frame" dir="rtl" lang="he">
    <div class="frame-bg"></div>
    <svg class="deco" viewBox="0 0 390 800" preserveAspectRatio="xMidYMid slice" aria-hidden="true">
      <defs>
        <filter id="dc-%LANE%-%TOPICID%" x="-35%" y="-35%" width="170%" height="170%" color-interpolation-filters="sRGB" filterUnits="objectBoundingBox" primitiveUnits="userSpaceOnUse">
          <feMorphology in="SourceAlpha" operator="dilate" radius="15" result="r2"></feMorphology>
          <feOffset in="r2" dx="5" dy="8" result="r2o"></feOffset>
          <feFlood class="dc-tint" result="f2"></feFlood>
          <feComposite in="f2" in2="r2o" operator="in" result="tint"></feComposite>
          <feMorphology in="SourceAlpha" operator="dilate" radius="9" result="r1"></feMorphology>
          <feFlood class="dc-cut" result="f1"></feFlood>
          <feComposite in="f1" in2="r1" operator="in" result="cut"></feComposite>
          <feMerge><feMergeNode in="tint"></feMergeNode><feMergeNode in="cut"></feMergeNode><feMergeNode in="SourceGraphic"></feMergeNode></feMerge>
        </filter>
        <filter id="co-%LANE%-%TOPICID%" x="-35%" y="-35%" width="170%" height="170%" color-interpolation-filters="sRGB" filterUnits="objectBoundingBox" primitiveUnits="userSpaceOnUse">
          <feMorphology in="SourceAlpha" operator="dilate" radius="7" result="grown"></feMorphology>
          <feTurbulence type="fractalNoise" baseFrequency="0.22" numOctaves="2" seed="7" result="noise"></feTurbulence>
          <feDisplacementMap in="grown" in2="noise" scale="5" xChannelSelector="R" yChannelSelector="G" result="deckle"></feDisplacementMap>
          <feFlood class="co-stock" result="stock"></feFlood>
          <feComposite in="stock" in2="deckle" operator="in" result="paper"></feComposite>
          <feMerge><feMergeNode in="paper"></feMergeNode><feMergeNode in="SourceGraphic"></feMergeNode></feMerge>
        </filter>
      </defs>
      <g class="deco-ghosts">
        <rect x="16" y="86" width="126" height="54" rx="9" transform="rotate(-7 79 113)"></rect>
        <rect x="238" y="176" width="138" height="46" rx="4" transform="rotate(5 307 199)"></rect>
        <ellipse cx="76" cy="404" rx="74" ry="34" transform="rotate(-11 76 404)"></ellipse>
        <rect x="216" y="546" width="152" height="62" rx="11" transform="rotate(-4 292 577)"></rect>
        <rect x="18" y="648" width="120" height="44" rx="6" transform="rotate(6 78 670)"></rect>
        <ellipse cx="302" cy="62" rx="58" ry="25" transform="rotate(8 302 62)"></ellipse>
        <path d="M156 730l124-9 5 24-6 22-31 5-26-7-31 8-25-5-9-16z" transform="rotate(-3 215 751)"></path>
      </g>
    </svg>

    <header class="hud">
      <div class="hud-coins">
        <span class="coin-glyph" aria-hidden="true"></span>
        <span class="coin-num">%COINS%</span>
      </div>
      <div class="hud-mid">
        <span class="topic-title">%TOPIC%</span>
        <span class="steps" aria-hidden="true"><i class="step step-on"></i><i class="step"></i><i class="step"></i></span>
      </div>
      <div class="hud-you">
        <button type="button" class="map-btn" aria-label="%MAP%">
          <svg class="map-icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M3 6.6 9 4l6 2.6L21 4v13.4L15 20l-6-2.6L3 20z"></path><path d="M9 4v13.4M15 6.6V20"></path></svg>
        </button>
        <div class="avatar" aria-hidden="true">
          <svg class="avatar-sil" viewBox="0 0 64 64"><circle cx="32" cy="25" r="12"></circle><path d="M8 60c0-13 10.8-19.5 24-19.5S56 47 56 60Z"></path></svg>
        </div>
      </div>
    </header>

    <div class="deck">
      <div class="stack">
        <div class="pile" aria-hidden="true">
          <div class="pile-card pile-3"></div>
          <div class="pile-card pile-2"></div>
          <div class="pile-card pile-1"></div>
        </div>
        <article class="card claim">
          <span class="sticker">%BILLDATE%</span>
          <div class="art" aria-hidden="true">
            <span class="art-emoji">%ART%</span>
            <svg class="art-clip" viewBox="0 0 28 60"><path d="M18 18v28a6.5 6.5 0 0 1-13 0V15a10 10 0 0 1 20 0v34"></path></svg>
          </div>
          <h2 class="issue-title">%TITLE%</h2>
          <p class="claim-text">%CLAIM_A%<mark class="hl">%CLAIM_B%</mark>.</p>
%VERIFY%        </article>
      </div>
      <div class="answers">
        <button type="button" class="ans ans-true"><span class="ans-word">%ANS_T%</span><svg class="ans-arrow" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 12h15M13 6l6 6-6 6"></path></svg></button>
        <button type="button" class="ans ans-false"><span class="ans-word">%ANS_F%</span><svg class="ans-arrow" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 12h15M13 6l6 6-6 6"></path></svg></button>
      </div>
    </div>
  </div>
</div>"""

PAGE = """<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <script src="./support.js"></script>
</head>
<body>
%TOKENS%
<x-dc>
<helmet>
  <style>%SHARED%
%LANECSS%
  </style>
</helmet>
%BODY%
</x-dc>
<script data-dc-script data-props='{"$preview":{"width":390,"height":880}}'>
class Component extends DCLogic {
  renderVals() { return {}; }
}
</script>
</body>
</html>
"""

# =========================================================================
LANES = []

# ---------------------------------------------------------------- lane 1
LANES.append(dict(
  n="1", file="Main.dc.html", cls="lane1",
  dispnote=" · תצוגה: Bibush Chunky · מדבקה כחולה + מרקר זהב במסגרת אחת",
  # v4.3 CHANGE 3 — lane 1 renders ONE frame, not two: the branches sticker and the
  # religion highlighter in a single sample.
  frames=[dict(file="Main.dc.html", label=TOPICS["religion"]),
          dict(file="MainLongTitle.dc.html", label=TOPICS["religion"],
               title=LONGTITLE, note=LONGNOTE, row=1),
          # the punctuation worst case, and the only frame where .px-punct is visible
          # inside a title rather than in the caption specimen
          dict(file="MainPunct.dc.html", label=TOPICS["religion"],
               title=PUNCTTITLE, note=PUNCTNOTE, row=2)],
  he="טופס מודבק", en="Defaced Paperwork",
  tokens="""<!--
  LANE 1 · Defaced Paperwork
  palette   : desk #241F1A · manila card #D9D2C0 · ink #1A1714 · photo stock #EFE9DA
              · mixed file backs: cream #E4DCC4 / lavender #D3C4CE / pale blue #B8C3D2
              · accents, one use each: muted red clip #A8443C · muted teal tab #2F7D74
  type      : Bibush Chunky display (title, אמת/שקר, coins); stand-in system face for body
  texture   : one — office document: hard rules, file tabs, a binder margin, zero radii
  BOLDNESS  : the Bibush Chunky title at 66px — it takes a third of the card on its own
  ARTIFACTS : four, counted — paperclip · tape · highlighter · two punched filing holes
  TOPIC     : religion #ffd23f/#ffb800 -> #F2C230/#8A6A18   (highlighter gold, deep manila)
              branches #2b4cff/#1a3acc -> #4A6BD6/#25376B   (mimeograph blue, carbon deep)
              rendered as ONE merged frame: blue sticker + gold highlighter
-->""",
  css="""/* LANE 1 · Defaced Paperwork
   palette   : desk #241F1A · manila card #D9D2C0 · ink #1A1714 · photo stock #EFE9DA
               · mixed file backs: cream #E4DCC4 / lavender #D3C4CE / pale blue #B8C3D2
               · accents, one use each: muted red clip #A8443C · muted teal tab #2F7D74
   type      : Bibush Chunky display (title, אמת/שקר, coins); stand-in face for body
   texture   : one — office document: hard rules, file tabs, a binder margin, zero radii
   BOLDNESS  : the Bibush Chunky title at 66px, taking a third of the card on its own
   ARTIFACTS : four, counted — paperclip · tape · highlighter · two punched filing holes
   TOPIC old->new : religion #ffd23f/#ffb800 -> #F2C230/#8A6A18 (highlighter gold, deep manila)
                    branches #2b4cff/#1a3acc -> #4A6BD6/#25376B (mimeograph blue, carbon deep)

   v4.3 CHANGE 3 — the per-topic mechanism below is INTACT and unchanged; lane 1 simply
   renders one frame instead of two. .topic-religion and .topic-branches are still here,
   still correct, and still what a religion or a branches round would use: switch
   frames= in the lane dict back to both topics and the two frames return as they were.
   .topic-merged is the sample only — the branches sticker (--t1 mimeograph blue) with
   the religion highlighter (--hl gold), so one frame shows both tokens at once. It is a
   specimen, not a reachable game state. */
.lane1.topic-religion{--t1:#F2C230;--t2:#8A6A18;--hl:#F7DC7A;--on-t1:#1A1714}
.lane1.topic-branches{--t1:#4A6BD6;--t2:#25376B;--hl:#AEC4F2;--on-t1:#FFFFFF}
.lane1.topic-merged{--t1:#4A6BD6;--t2:#25376B;--hl:#F7DC7A;--on-t1:#FFFFFF}

/* Bibush Chunky's cmap, read directly off the file: 47 glyphs. It HAS . : and digits;
   it lacks - / " ׳ ״ . (The other cut is the mirror image — it has - and lacks : .)
   Checked against data.js: 4 of the 16 real titles break, and only on - and / :
   ועדת חקירה ל-7/10 · המס על כלים חד-פעמיים · חוק המשטרה של בן-גביר ·
   מדינה פלסטינית: הכרה חד-צדדית. The brief's suggested U+0022 fallback is absent too,
   so punctuation is drawn as CSS boxes on Bibush's stroke (.px-punct below); the font
   files themselves are never modified. The demo sits in the caption strip.
   NOT YET WIRED INTO THE TITLE ITSELF — so the measured ladder rung for those four
   titles is taken with the browser's fallback glyph and is approximate until it is. */
@font-face{font-family:'BibushChunky';src:url(data:font/ttf;base64,%BIBUSHFONT%) format('truetype');
  font-weight:400;font-style:normal;font-display:block}
.lane1 .cap-spec{display:block}
.lane1 .spec-line{font-family:'BibushChunky',system-ui,sans-serif;font-size:29px;line-height:1.15;
  display:block}
.px-punct{display:inline-block;background:none;color:currentColor}
/* pixel hyphen: one bar on Bibush's stroke weight */
.px-hyphen{width:.40em;height:.115em;background:currentColor;vertical-align:.30em;margin:0 .06em}
/* pixel solidus: a stair of stroke-sized blocks, same weight as the hyphen */
.px-slash{position:relative;width:.42em;height:.74em;vertical-align:-.05em;margin:0 .05em}
.px-slash::before{content:"";position:absolute;left:0;bottom:0;width:.115em;height:.115em;
  background:currentColor;
  box-shadow:.105em -.115em 0 currentColor,.105em -.23em 0 currentColor,
             .21em -.345em 0 currentColor,.21em -.46em 0 currentColor,
             .315em -.575em 0 currentColor,.315em -.69em 0 currentColor}

.lane1 .frame{background:#241F1A;color:#1A1714}
.lane1 .frame-bg{background:#241F1A}
.lane1 .frame-bg::after{content:"";position:absolute;inset:0;opacity:.45;
  background-image:repeating-conic-gradient(rgba(255,255,255,.05) 0 25%,transparent 0 50%);
  background-size:4px 4px}
.lane1 .coin-glyph{background:var(--t2);border-radius:0;box-shadow:inset 0 0 0 2px #1A1714}
.lane1 .coin-num{color:#D9D2C0;font-family:'BibushChunky',system-ui,sans-serif;font-size:23px}
.lane1 .topic-title{color:#C0B393;letter-spacing:.14em;font-size:11px;text-transform:none}
.lane1 .steps{color:#C0B393}
.lane1 .map-btn{color:#D9D2C0;border-radius:0;background:#3A332B;
  box-shadow:inset 0 0 0 2px #1A1714}
.lane1 .map-btn:focus-visible{outline:3px solid #D9D2C0;outline-offset:3px}
.lane1 .avatar{border-radius:0;background:#C0B393;box-shadow:inset 0 0 0 2px #1A1714}
.lane1 .avatar-sil{fill:#1A1714}
/* file-tab pile — v4.4 CHANGE B. Three sheets of the same manila read as one thick
   sheet, not as a case file. Papers, Please is differently tinted papers on a brown
   desk, so each back gets its own document colour and its own edge: cream, the pale
   lavender-pink of a fingerprint hand-out, the pale blue of an ID record. The front
   card stays neutral manila — the colour is around and behind it, never on it. */
.lane1 .pile-card{box-shadow:inset 0 0 0 1px #8E8264,0 2px 0 rgba(0,0,0,.55)}
.lane1 .pile-card::before{content:"";position:absolute;top:-13px;width:96px;height:14px;
  background:inherit;box-shadow:inset 0 0 0 1px #8E8264}
.lane1 .pile-1{background:#E4DCC4}
.lane1 .pile-1::before{right:26px}
.lane1 .pile-2{background:#D3C4CE}
.lane1 .pile-2::before{right:132px}
/* v4.6 — the shift back. #9FB0C6 existed only to separate this back from the
   #BFC9D6 photo plate; the plate is gone, so the reason is gone and the lighter
   ID-record blue returns. Nothing on the card is that colour any more. */
.lane1 .pile-3{background:#B8C3D2}
.lane1 .pile-3::before{right:230px}
/* the second saturated accent, used once: one folder in the file is tabbed muted teal.
   A coloured tab is document furniture, it sits behind the card so it can never touch
   content, and it belongs to no topic and no verdict. */
.lane1 .pile-2::before{background:#2F7D74;box-shadow:inset 0 0 0 1px #215A54}
.lane1 .card{background:#D9D2C0;padding-right:36px;
  box-shadow:inset 0 0 0 1px #A79C81,0 4px 0 rgba(0,0,0,.6),0 20px 30px rgba(0,0,0,.5)}
/* INTERVENTION 1 — one slapped die-cut sticker, carrying the topic colour.
   v4.2 FIX 1(a): it now carries document furniture — the bill's own date stamp,
   data.js issues[r1].bill_date. Ink flips to --on-t1 so the stamp clears AA on
   both topic frames (gold 10.7:1 on ink, blue 4.8:1 on white). */
.lane1 .sticker{display:flex;align-items:center;justify-content:center;position:absolute;
  top:-17px;left:-16px;z-index:6;min-width:96px;height:38px;padding:0 13px;
  border-radius:999px;background:var(--t1);color:var(--on-t1);border:4px solid #fff;rotate:-13deg;
  box-shadow:0 3px 0 rgba(0,0,0,.45);
  font-size:12px;font-weight:800;letter-spacing:.02em;line-height:1;white-space:nowrap}
/* INTERVENTION 3 — one strip of tape across the opposite corner */
.lane1 .card::before{content:"";position:absolute;top:-13px;right:-24px;width:104px;height:29px;
  rotate:36deg;background:linear-gradient(96deg,rgba(238,238,228,.52),rgba(214,216,204,.66));
  box-shadow:inset 0 0 0 1px rgba(255,255,255,.4);z-index:5}
/* INTERVENTION 4 — v4.3 CHANGE 3: two punched filing holes down the binder margin.
   Chosen over the staple, the torn corner, the coffee ring and the fold crease because
   it is the only candidate that proves the card is a physical sheet LYING ON the desk:
   the desk colour is what you see through the holes, so the artifact reads as depth
   rather than as another mark added on top. It is also the only one that cannot touch
   content — a punch lives in the margin by definition, which is why the card grew a
   36px binder margin on its leading (right, RTL) edge to hold it. Neutral, document
   native, nothing defaced, nothing crossed out. Two holes, one counted artifact. */
.lane1 .card::after{content:"";position:absolute;right:8px;top:161px;width:20px;height:147px;
  z-index:6;pointer-events:none;background-repeat:no-repeat;background-size:20px 20px;
  /* two holes, 147px apart on the standard two-hole pitch. Each is a dark disc (the desk,
     seen through the sheet) sat on a slightly offset pale disc, so the lit bottom-right
     lip of the cut paper shows — that lip is what makes it read as punched rather than
     printed. Layers paint front to back: hole, lip, hole, lip. */
  background-position:50% 0,50% 0,50% 100%,50% 100%;
  background-image:
    radial-gradient(circle at 50% 47%,#241F1A 0 45%,transparent 46%),
    radial-gradient(circle at 54% 58%,#F0EBDD 0 50%,transparent 51%),
    radial-gradient(circle at 50% 47%,#241F1A 0 45%,transparent 46%),
    radial-gradient(circle at 54% 58%,#F0EBDD 0 50%,transparent 51%)}

/* v4.6 CHANGE C — the framed photo plate is gone. The helmet is now a printed photo
   trimmed to its own outline and laid on the manila.

   It must NOT converge on lane 3's die-cut sticker, so every cue is a different word
   for the same physicality:
     lane 3  9px of hard bright white  · smooth cut · hard offset colour rim ·
             flat black knock-out · 216px · a hard 5px shadow
     lane 1  6px of cream photo stock  · DECKLED   · no rim ·
             a grey photo with midtones · 186px · a soft diffuse shadow
   The deckle is the detail that separates a cut photograph from a vinyl sticker, and
   it is cheap: feTurbulence displaces the dilated alpha before it is flooded, so the
   paper margin comes out ragged the way scissors and a guillotine leave it.
   The contrast is deliberately down from contrast(9) to 1.7 — a photo has midtones; a
   sticker is flat. The clip crosses the photo's edge, so the object reads as placed on
   the document rather than printed into it. mix-blend-mode is gone with the plate:
   there is no rectangle left to multiply into. */
.lane1 .co-stock{flood-color:#EFE9DA;flood-opacity:1}
.lane1 .art{flex:1;min-height:244px;margin-top:10px}
.lane1 .art-emoji{font-size:186px;rotate:-2.5deg;
  filter:grayscale(1) contrast(1.7) brightness(1.02)
         drop-shadow(2px 5px 6px rgba(26,23,20,.42))}
.lane1.topic-merged .art-emoji{filter:grayscale(1) contrast(1.7) brightness(1.02)
  url(#co-lane1-merged) drop-shadow(2px 5px 6px rgba(26,23,20,.42))}
/* the one saturated accent, used on one thin stroke: a coated-wire clip in muted red.
   It belongs to the document world, never to a topic and never to a verdict.
   It now sits ON the photo's edge — it is what holds the cut-out down. */
.lane1 .art-clip{display:block;color:#A8443C;top:34px;left:88px;rotate:14deg;z-index:3}
.lane1 .issue-title{font-family:'BibushChunky',system-ui,sans-serif;font-weight:400;font-size:66px;
  line-height:.98;margin-top:12px;color:#1A1714}
.lane1 .claim-text{color:#1A1714;margin-top:10px;line-height:1.5}
/* INTERVENTION 2 — one highlighter swipe, in the topic colour */
.lane1 .hl{background:linear-gradient(104deg,rgba(0,0,0,0) 0,var(--hl) 1.5%,var(--hl) 98%,rgba(0,0,0,0) 100%);
  opacity:.999;box-decoration-break:clone;-webkit-box-decoration-break:clone;padding:1px 2px;
  mix-blend-mode:multiply}
%TITLESTEPS%
.lane1 .ans{background:#EDE8DA;color:#1A1714;border-radius:0;
  font-family:'BibushChunky',system-ui,sans-serif;font-weight:400;font-size:27px;
  box-shadow:inset 0 0 0 2px #1A1714,4px 4px 0 rgba(0,0,0,.55)}
.lane1 .ans:focus-visible{outline:3px solid #EDE8DA;outline-offset:4px}"""))

# ---------------------------------------------------------------- lane 2
LANES.append(dict(
  n="2", file="NytGames.dc.html", cls="lane2", dispnote="",
  he="משחקי עיתון", en="NYT Games",
  # v4.4 CHANGE A — one frame, mixed pile; plus the longest real title as a stress frame
  frames=[dict(file="NytGames.dc.html", tid="branches", label=TOPICS["branches"]),
          dict(file="NytGamesLongTitle.dc.html", tid="branches", label=TOPICS["branches"],
               title=LONGTITLE, note=LONGNOTE, row=1)],
  tokens="""<!--
  LANE 2 · NYT Games
  palette   : warm grey #E8E6E1 · paper #FDFDFB · ink #1A1A1A · rule #DDD9D0 · neutral back #CFCBC2
  type      : the boldness lives here — title 52px, claim 17.5px/700, small caps micro-labels
  texture   : none — flat games-family colour and a strict grid; green banned lane-wide
  BOLDNESS  : type scale. The title is a poster headline, not a form label
  TOPIC     : religion #ffd23f/#ffb800 -> #EE9F3C/#C7701D  (pushed to warm orange so the
                                                            #C9A227 surprise amber stays distinct)
              branches #2b4cff/#1a3acc -> #6AA9E0/#4A6FB5  (games sky, deep sky)
-->""",
  css="""/* LANE 2 · NYT Games
   palette   : warm grey #E8E6E1 · paper #FDFDFB · ink #1A1A1A · rule #DDD9D0 · neutral #CFCBC2
   type      : the boldness lives here — title 52px, claim 17.5px/700, small caps micro-labels
   texture   : none — flat games-family colour and a strict grid; green banned lane-wide
   BOLDNESS  : type scale. The title is a poster headline, not a form label
   TOPIC old->new : religion #ffd23f/#ffb800 -> #EE9F3C/#C7701D  (warm orange, pushed off the
                      #C9A227 surprise amber so the verdict colour stays unmistakable)
                    branches #2b4cff/#1a3acc -> #6AA9E0/#4A6FB5  (games sky, deep sky) */
/* v4.4 CHANGE A — the pile stops carrying the topic and becomes one fixed mixed set.
   THE TOPIC TOKEN NOW LIVES ON EXACTLY ONE PROPERTY IN THE CARD REGION:
       background on .card, via --card.
   Everything else in the card region that the topic used to tint (the pile backs, the
   art disc) is now a lane constant, so 8 topics x 2 rounds still differ round to round
   without the whole frame recolouring. --t1/--t2 stay defined and stay correct: they
   are what the HUD topic chip, coin and avatar ring read. --tint is retained but
   unused, so the old per-topic disc can be restored in one line. */
.lane2.topic-religion{--t1:#EE9F3C;--t2:#C7701D;--tint:#F7DEC2;--card:#FDF4E6}
.lane2.topic-branches{--t1:#6AA9E0;--t2:#4A6FB5;--tint:#CFE1F3;--card:#EFF4FB}
.lane2 .frame{background:#E8E6E1;color:#1A1A1A;padding:12px 20px 24px}
.lane2 .frame-bg{background:#E8E6E1}
.lane2 .coin-glyph{background:#FDFDFB;box-shadow:inset 0 0 0 1.5px #1A1A1A}
.lane2 .coin-num{color:#1A1A1A}
.lane2 .topic-title{color:#4A4A46;font-size:10.5px;letter-spacing:.19em;padding:4px 0}
.lane2 .steps{color:var(--t2)}
.lane2 .map-btn{color:#1A1A1A;background:#FDFDFB;box-shadow:inset 0 0 0 1.5px #1A1A1A}
.lane2 .map-btn:focus-visible{outline:3px solid #C9A227;outline-offset:2px}
.lane2 .avatar{background:#FDFDFB;box-shadow:inset 0 0 0 1.5px #1A1A1A}
.lane2 .avatar-sil{fill:#B9B5AC}
/* pile: two from the topic family + one neutral */
.lane2 .pile-card{border-radius:6px;box-shadow:0 3px 10px rgba(0,0,0,.15)}
/* the merged pile: the two topic families the board was comparing, plus the neutral
   that was already there. Chosen over inventing a new palette because a deck of
   different-coloured puzzle backs IS the NYT Games idiom, and warm / cool / neutral in
   rotation reads as three different puzzles rather than three copies of one. Fixed —
   identical in every round. */
.lane2 .pile-1{background:#EE9F3C}
.lane2 .pile-2{background:#6AA9E0}
.lane2 .pile-3{background:#CFCBC2}
.lane2 .card{background:var(--card);border-radius:6px;padding:14px 22px 16px;
  box-shadow:0 0 0 1px #DDD9D0,0 12px 28px rgba(0,0,0,.16)}
.lane2 .art{min-height:96px}
.lane2 .art::before{content:"";position:absolute;width:172px;height:172px;border-radius:50%;
  background:#E7E3DA}   /* lane constant now: the topic lives on --card */
.lane2 .art-emoji{position:relative;font-size:100px;filter:grayscale(1) brightness(0)}
/* BOLDNESS: poster type.
   v4.2 FIX 3 — lane 2's freed space went to TYPE, which is where this lane's
   boldness lives: title 52 -> 66px, claim 17.5 -> 19px. .art stays flex:1 and
   takes what is left over, so the disc grows a little with it. */
.lane2 .issue-title{font-size:66px;letter-spacing:-.03em;line-height:.94;margin-top:10px}
.lane2 .claim-text{margin-top:14px;font-size:19px;line-height:1.42}
%TITLESTEPS%
.lane2 .ans{background:#FDFDFB;border:1.5px solid #1A1A1A;border-radius:3px;color:#1A1A1A;font-size:21px;
  letter-spacing:.02em;box-shadow:0 3px 0 #1A1A1A}
.lane2 .ans:focus-visible{outline:3px solid #C9A227;outline-offset:3px}"""))

# ---------------------------------------------------------------- lane 3
LANES.append(dict(
  n="3", file="Stickers.dc.html", cls="lane3", dispnote="",
  he="תרבות סטיקרים", en="Israeli Sticker Culture",
  rung_trim=dict(keep_above=58, chrome=38, inner=290,
                 css="border-width:3px;padding:4px 8px 6px"),
  # v4.4 CHANGE A — one frame, mixed pile; plus the longest real title as a stress frame
  frames=[dict(file="Stickers.dc.html", tid="religion", label=TOPICS["religion"]),
          dict(file="StickersLongTitle.dc.html", tid="religion", label=TOPICS["religion"],
               title=LONGTITLE, note=LONGNOTE, row=1)],
  # a three-line comparison frame lived here; three lines was ruled out — at 36px, the
  # only size that is genuinely three lines and still fits, it bought 2px of headline
  # over the two-line setting and cost a line.
  tokens="""<!--
  LANE 3 · Israeli Sticker Culture
  palette   : pole grey #B3B1A9 · white die-cut · black #000 · fixed pink #FF3B6B + topic colours
  type      : SimplerPro Black in slogan chunks; the HUD is a flat band, not a sticker sheet
  texture   : one — the pole: two-scale grain over pale ghost remnants of older stickers
  BOLDNESS  : a 216px die-cut sticker cut to the helmet's own silhouette, stuck on
              the card and breaking out over its top edge
  FIXED     : אמת/שקר buttons #2EC4B6 — one lane constant, identical on both buttons and
              both topic frames, never topic-tinted; direction is the arrow alone.
              #FF3B6B survives only as one card in the pile (v4.2: the swipe hints are gone)
  TOPIC     : religion #ffd23f/#ffb800 -> #FFD60A/#FF8A00  (sticker yellow, sticker orange)
              branches #2b4cff/#1a3acc -> #3D5BFF/#1E36B8  (electric blue, deep blue)
-->""",
  css="""/* LANE 3 · Israeli Sticker Culture
   palette   : pole grey #B3B1A9 · white die-cut · black #000 · fixed pink #FF3B6B + topic colours
   type      : SimplerPro Black slogan chunks; the HUD is a flat band, not a sticker sheet
   texture   : one — the pole: two-scale grain over pale ghost remnants of older stickers
   BOLDNESS  : a 216px die-cut sticker cut to the helmet's own silhouette, stuck on
              the card and breaking out over its top edge
   TOPIC old->new : religion #ffd23f/#ffb800 -> #FFD60A/#FF8A00 (sticker yellow, sticker orange)
                    branches #2b4cff/#1a3acc -> #3D5BFF/#1E36B8 (electric blue, deep blue) */
/* v4.4 CHANGE A — as in lane 2: the pile is a fixed mixed set and
   THE TOPIC TOKEN LIVES ON EXACTLY ONE PROPERTY IN THE CARD REGION:
       background on .card, via --card.
   The die-cut sticker's registration rim, which carried the topic in v4.3, becomes a
   lane constant (--rim) so the card region has one topic-keyed surface, not two. */
.lane3.topic-religion{--t1:#FFD60A;--t2:#FF8A00;--on-t1:#000;--card:#FFF3CE}
.lane3.topic-branches{--t1:#3D5BFF;--t2:#1E36B8;--on-t1:#fff;--card:#E6EDFF}
.lane3{--rim:#3D5BFF}
.lane3 .frame{background:#B3B1A9;color:#000}
.lane3 .frame-bg{background:#B3B1A9}
/* the pole: ghost remnants sit under two grains at different scales */
.lane3 .frame-bg::after{content:"";position:absolute;inset:0;
  background-image:
    radial-gradient(rgba(0,0,0,.5) .5px,transparent .6px),
    radial-gradient(rgba(255,255,255,.55) .5px,transparent .6px),
    repeating-linear-gradient(89deg,rgba(0,0,0,.05) 0 1px,transparent 1px 4px);
  background-size:3px 3px,7px 7px,100% 100%;background-position:0 0,2px 3px,0 0}
/* v4.2 FIX 2 — the "ghost rectangle" under the buttons was one of these: a peeled-sticker
   remnant from the pole texture. At .75 opacity with a crisp 3px light outline and rx:8
   geometry, parked directly beneath the verdict buttons, it read as an empty UI panel.
   Kept as texture, not deleted: outline dropped, opacity halved, and the shape that sits
   in the button zone redrawn as a torn edge so nothing down there has control geometry. */
.lane3 .deco .deco-ghosts{display:block;fill:#C6C4BC;stroke:none;opacity:.34}
/* HUD: a flat band, one sticker accent only (the topic title).
   v4.2 FIX 4 — the solid black bar read as browser chrome. It is now a bleached strip of
   the pole itself: same grain, same colour family, lightened, with a hairline bottom rule
   so it still reads as a band. Opaque rather than translucent so the card can never show
   through it. Content flips to near-black (11.0:1 on #C9C7C1, down from 15.4:1). Still flat, still one
   sticker accent, plain avatar circle, plain step dots. */
.lane3 .hud{background:#C9C7C1;margin:-12px -16px 0;padding:10px 16px;min-height:60px;
  overflow:hidden;box-shadow:inset 0 -1.5px 0 rgba(0,0,0,.22)}
.lane3 .hud::before{content:"";position:absolute;inset:0;z-index:-1;pointer-events:none;
  background-image:
    radial-gradient(rgba(0,0,0,.5) .5px,transparent .6px),
    radial-gradient(rgba(255,255,255,.55) .5px,transparent .6px),
    repeating-linear-gradient(89deg,rgba(0,0,0,.05) 0 1px,transparent 1px 4px);
  background-size:3px 3px,7px 7px,100% 100%;background-position:0 0,2px 3px,0 0}
.lane3 .coin-glyph{background:var(--t1);box-shadow:inset 0 0 0 2px #000}
.lane3 .coin-num{color:#131310}
.lane3 .topic-title{background:var(--t1);color:var(--on-t1);border:3px solid #fff;border-radius:999px;
  padding:4px 13px;rotate:-2.5deg;font-weight:900;
  box-shadow:0 0 0 1.5px rgba(0,0,0,.3),0 3px 0 rgba(0,0,0,.42)}
.lane3 .steps{color:#131310}
.lane3 .map-btn{color:#131310;background:none}
.lane3 .map-btn:focus-visible{outline:3px solid #131310;outline-offset:2px}
.lane3 .avatar{background:#2E2C26;box-shadow:0 0 0 3px var(--t1)}
.lane3 .avatar-sil{fill:#CFCDC4}
.lane3 .pile-card{border:5px solid #fff;box-shadow:0 4px 0 rgba(0,0,0,.42)}
/* the merged pile: warm red + warm orange against the lane's electric blue. Fixed —
   identical in every round. Sticker yellow is deliberately NOT in the pile: the front
   card is now pale warm yellow, and a yellow back behind it would flatten the stack. */
.lane3 .pile-1{background:#FF3B6B;transform:translateY(-11px) rotate(-3.4deg)}
.lane3 .pile-2{background:#3D5BFF;transform:translateY(-20px) rotate(4.6deg)}
.lane3 .pile-3{background:#FF8A00;transform:translateY(-29px) rotate(-7deg)}
.lane3 .card{background:var(--card);border:7px solid #fff;rotate:-1.4deg;overflow:visible;
  padding:0 18px 16px;box-shadow:0 7px 0 rgba(0,0,0,.42),0 16px 26px rgba(0,0,0,.28)}
/* BOLDNESS — v4.3 CHANGE 2: the helmet is a die-cut sticker stuck ON the card.
   The coloured rounded square is gone. The white cut edge now follows the HELMET'S
   OWN SILHOUETTE, which no border can do, so it is built in the filter that every
   artboard carries in its <defs> (inert in lanes 1 and 2):
     feMorphology dilate 15 on SourceAlpha, offset 5/8, flooded var(--t1)  -> the
       colour registration rim, the frame's topic-colour carrier inside the card;
     feMorphology dilate 9  on SourceAlpha, flooded #fff                   -> the cut;
     SourceGraphic (the flat black helmet) on top.
   A CSS drop-shadow underneath lifts it off the white card. Nothing here is
   verdict-capable: the topic colour touches the sticker rim and nothing else. */
.lane3 .dc-tint{flood-color:var(--rim);flood-opacity:1}
.lane3 .dc-cut{flood-color:#fff;flood-opacity:1}
.lane3 .art{flex:none;height:214px;margin-top:-48px;overflow:visible;z-index:4}
.lane3 .art-emoji{display:block;font-size:0;rotate:-7deg}
.lane3 .art-emoji::before{content:"🪖";display:block;font-size:216px;line-height:1;
  filter:grayscale(1) brightness(0) drop-shadow(0 11px 13px rgba(0,0,0,.3))}
.lane3.topic-religion .art-emoji::before{filter:grayscale(1) brightness(0)
  url(#dc-lane3-religion) drop-shadow(0 11px 13px rgba(0,0,0,.3))}
.lane3.topic-branches .art-emoji::before{filter:grayscale(1) brightness(0)
  url(#dc-lane3-branches) drop-shadow(0 11px 13px rgba(0,0,0,.3))}
/* the title + claim block is centred in what the sticker leaves, and both grow into
   the space the source chip freed: title 46 -> 58px, claim 17 -> 19px.
   58px is the ceiling for one line: «חוק הגיוס» measures 244px of the 252px the box
   can hold, and 60px overflows it to 252.4px and wraps. A wrapped title stretches the
   black box to the full card width and stops reading as a slogan chunk, so the size
   is pinned to the one-line fit and the remainder went to the sticker (196 -> 216px). */
.lane3 .issue-title{background:#000;color:#fff;border:5px solid #fff;padding:6px 14px 9px;rotate:1.4deg;
  align-self:flex-start;font-size:58px;box-shadow:0 4px 0 rgba(0,0,0,.45);margin-top:auto}
.lane3 .claim-text{margin-top:18px;margin-bottom:auto;font-size:20px;line-height:1.45;
  max-width:27ch;text-wrap:balance}
/* fixed lane colour — never the topic colour: this is the אמת/שקר surface */
/* v4.4 CHANGE A, approved — full-saturation teal was competing with the sticker for
   the loudest thing on the frame. The fill goes white and the teal moves out to a
   die-cut edge, which is the sticker's own construction, so the card reads as one
   system. Dark teal label on white: 12.3:1. Both buttons identical, no topic token,
   direction carried by the arrow alone. */
%TITLESTEPS%
.lane3 .ans{background:#FFFFFF;color:#0B3B36;border:5px solid #2EC4B6;border-radius:16px;
  box-shadow:0 5px 0 rgba(0,0,0,.48);font-size:24px}
.lane3 .ans-true{rotate:-1.8deg}
.lane3 .ans-false{rotate:1.8deg}
.lane3 .ans:focus-visible{outline:4px solid #000;outline-offset:4px}"""))

# =========================================================================
def frames_of(lane):
    """Every frame a lane renders, as dicts: tid, label, file, var, note.
    v4.4 CHANGE A — all three lanes now render ONE frame each, so a frame names its
    own file rather than deriving it from a topic. `var` is an extra stage class for
    a side-by-side variant (lane 3's button options); `note` annotates the caption."""
    out = []
    for f in lane["frames"]:
        d = dict(tid=f.get("tid", "merged"), label=f.get("label", TOPICS["religion"]),
                 file=f["file"], var=f.get("var", ""), note=f.get("note", ""),
                 title=f.get("title", TITLE), row=f.get("row", 0))
        out.append(d)
    return out

def build():
    shared = SHARED.replace("%FONT%", FONT)
    boards = []
    for lane in LANES:
        for fr in frames_of(lane):
            tid, tlabel, fname = fr["tid"], fr["label"], fr["file"]
            # a frame must render a topic the lane actually defines tokens for: an
            # undefined --card silently drops .card's background and the pile shows
            # through. Caught once the hard way; asserted from now on.
            assert ".%s.topic-%s{" % (lane["cls"], tid) in lane["css"], (lane["cls"], tid)
            # the rung this title was measured into; the stage carries it so the
            # markup skeleton stays identical frame to frame
            step = TITLE_STEPS[lane["cls"]][fr["title"]]
            classes = " ".join(x for x in ("ts-%d" % step, fr["var"]) if x)
            body = (BODY
                    .replace("%LANE%", lane["cls"]).replace("%TOPICID%", tid)
                    .replace("%VARCLS%", " " + classes)
                    .replace("%NUM%", lane["n"]).replace("%HE%", lane["he"]).replace("%EN%", lane["en"])
                    .replace("%DISPNOTE%", lane["dispnote"] + fr["note"])
                    .replace("%COINS%", COINS).replace("%TOPIC%", tlabel)
                    .replace("%TITLE%", bibush_title(fr["title"])
                                          if lane["cls"] == "lane1" else esc(fr["title"]))
                    .replace("%CLAIM_A%", CLAIM_A).replace("%CLAIM_B%", CLAIM_B)
                    .replace("%ANS_T%", ANS_T).replace("%ANS_F%", ANS_F)
                    .replace("%VERIFY%", VERIFY_HTML if VERIFY_MARK else "")
                    .replace("%ART%", ART).replace("%MAP%", MAP)
                    .replace("%BILLDATE%", BILLDATE))
            cls = lane["cls"]
            rungs = "/* v4.5 — measured title ladder for this lane; see measure_titles.py */\n" + \
                    "\n".join(".%s.ts-%d .issue-title{font-size:%dpx}" % (cls, f, f)
                               for f in LADDER[cls])
            trim = lane.get("rung_trim")
            if trim:
                low = [f for f in LADDER[cls] if f < trim["keep_above"]]
                rungs += ("\n/* the box itself gives ground at the low rungs. The top rung keeps the\n"
                          "   approved proportions exactly; below it the border and padding come in so\n"
                          "   the long titles are not paying %dpx of chrome out of %dpx of card. */\n"
                          % (trim["chrome"], trim["inner"])) + \
                         ".%s:is(%s) .issue-title{%s}" % (
                             cls, ",".join(".ts-%d" % f for f in low), trim["css"])
            page = (PAGE.replace("%TOKENS%", lane["tokens"]).replace("%SHARED%", shared)
                    .replace("%LANECSS%", lane["css"].replace("%BIBUSHFONT%", BIBUSH)
                                                     .replace("%TITLESTEPS%", rungs))
                    .replace("%BODY%", body))
            (OUT / fname).write_text(page, encoding="utf-8")
            boards.append((fname, lane, fr))

    # v4.4 — top row: the r1 round. Bottom row: the same lane with the longest real
    # title in data.js, so the worst case is visible next to the normal one.
    arts = []
    for fname, lane, fr in boards:
        col = LANES.index(lane)
        arts.append({"file": fname, "x": (len(LANES) - 1 - col) * 480,
                     "y": fr["row"] * 1010, "w": 390, "h": 930,
                     "title": "%s · %s · %s%s" % (lane["n"], lane["he"], lane["en"],
                                                  fr["note"] or " — " + fr["label"])})
    (OUT / "canvas.json").write_text(
        json.dumps({"artboards": arts, "launch": {"view": "canvas"}}, ensure_ascii=False, indent=2),
        encoding="utf-8")
    for f, *_ in boards:
        print("%s  %6.1f KB" % (f.ljust(28), (OUT / f).stat().st_size / 1024))

if __name__ == "__main__":
    build()
