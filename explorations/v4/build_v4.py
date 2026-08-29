# -*- coding: utf-8 -*-
"""v4.2 — Final Three. 3 lanes x 2 topic-colour frames = 6 artboards.
Published as its OWN canvas (final-three-121.html); the six-lane v3 board
at visual-directions-121.html is untouched.
Regenerate:  python3 explorations/v4/build_v4.py
"""
import base64, json, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
OUT  = ROOT / "explorations" / "v4"
OUT.mkdir(exist_ok=True)
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
.issue-title{margin-top:4px;font-family:'SimplerPro',system-ui,sans-serif;font-weight:900;
  font-size:36px;line-height:1.04}
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

BODY = """<div class="stage %LANE% topic-%TOPICID%">
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
  n="1", file="Main.dc.html", cls="lane1", dispnote=" · תצוגה: Bibush Chunky",
  he="טופס מודבק", en="Defaced Paperwork",
  tokens="""<!--
  LANE 1 · Defaced Paperwork
  palette   : desk #241F1A · paper #D9D2C0 · ink #1A1714 · manila #C0B393 · ochre stamp #B07A1E
  type      : Bibush Chunky display (title, אמת/שקר, coins); stand-in system face for body
  texture   : one — office document: hard rules, dashed rules, file tabs, zero radii
  BOLDNESS  : the Bibush Chunky title at 60px — it takes a third of the card on its own
  TOPIC     : religion #ffd23f/#ffb800 -> #F2C230/#8A6A18   (highlighter gold, deep manila)
              branches #2b4cff/#1a3acc -> #4A6BD6/#25376B   (mimeograph blue, carbon deep)
-->""",
  css="""/* LANE 1 · Defaced Paperwork
   palette   : desk #241F1A · paper #D9D2C0 · ink #1A1714 · manila #C0B393 · ochre #B07A1E
   type      : Bibush Chunky display (title, אמת/שקר, coins); stand-in face for body
   texture   : one — office document: hard rules, dashed rules, file tabs, zero radii
   BOLDNESS  : the Bibush Chunky title at 60px, taking a third of the card on its own
   TOPIC old->new : religion #ffd23f/#ffb800 -> #F2C230/#8A6A18 (highlighter gold, deep manila)
                    branches #2b4cff/#1a3acc -> #4A6BD6/#25376B (mimeograph blue, carbon deep) */
.lane1.topic-religion{--t1:#F2C230;--t2:#8A6A18;--hl:#F7DC7A;--on-t1:#1A1714}
.lane1.topic-branches{--t1:#4A6BD6;--t2:#25376B;--hl:#AEC4F2;--on-t1:#FFFFFF}

/* Bibush Chunky covers Hebrew letters + digits only. Missing: - / " ׳ ״ .
   Checked against data.js: 4 of the 16 real issue titles break, and ONLY on - and / .
   The brief's suggested U+0022 fallback is absent from the font too, so punctuation is
   drawn as CSS boxes matched to Bibush's stroke (.px-punct below) — the font files
   themselves are never modified. Demo of «ועדת חקירה ל-7/10» sits in the caption strip. */
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
/* file-tab pile */
.lane1 .pile-card{background:#C0B393;box-shadow:inset 0 0 0 1px #8E8264,0 2px 0 rgba(0,0,0,.55)}
.lane1 .pile-card::before{content:"";position:absolute;top:-13px;width:96px;height:14px;background:#C0B393;
  box-shadow:inset 0 0 0 1px #8E8264}
.lane1 .pile-1::before{right:26px}
.lane1 .pile-2::before{right:132px}
.lane1 .pile-3::before{right:230px}
.lane1 .card{background:#D9D2C0;
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
/* art: high-contrast duotone document photo, paperclipped.
   v4.2 FIX 3 — the space the swipe hints used to hold goes here: the plate grows
   126 -> 244px and the duotone with it. Lane 1's freed space went to ART. */
/* v4.3 CHANGE 1 — the source chip's 49px goes to the photo plate, not to a gap */
.lane1 .art{flex:1;min-height:244px;background:#C0B393;
  box-shadow:inset 0 0 0 2px #1A1714;margin-top:10px}
.lane1 .art-emoji{font-size:136px;filter:grayscale(1) brightness(1.08) contrast(9);
  mix-blend-mode:multiply}
.lane1 .art-clip{display:block;color:#3A332B;top:-10px;left:64px;rotate:9deg}
.lane1 .issue-title{font-family:'BibushChunky',system-ui,sans-serif;font-weight:400;font-size:66px;
  line-height:.98;margin-top:12px;color:#1A1714}
.lane1 .claim-text{color:#1A1714;margin-top:10px;line-height:1.5}
/* INTERVENTION 2 — one highlighter swipe, in the topic colour */
.lane1 .hl{background:linear-gradient(104deg,rgba(0,0,0,0) 0,var(--hl) 1.5%,var(--hl) 98%,rgba(0,0,0,0) 100%);
  opacity:.999;box-decoration-break:clone;-webkit-box-decoration-break:clone;padding:1px 2px;
  mix-blend-mode:multiply}
.lane1 .ans{background:#EDE8DA;color:#1A1714;border-radius:0;
  font-family:'BibushChunky',system-ui,sans-serif;font-weight:400;font-size:27px;
  box-shadow:inset 0 0 0 2px #1A1714,4px 4px 0 rgba(0,0,0,.55)}
.lane1 .ans:focus-visible{outline:3px solid #EDE8DA;outline-offset:4px}"""))

# ---------------------------------------------------------------- lane 2
LANES.append(dict(
  n="2", file="NytGames.dc.html", cls="lane2", dispnote="",
  he="משחקי עיתון", en="NYT Games",
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
.lane2.topic-religion{--t1:#EE9F3C;--t2:#C7701D;--tint:#F7DEC2}
.lane2.topic-branches{--t1:#6AA9E0;--t2:#4A6FB5;--tint:#CFE1F3}
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
.lane2 .pile-1{background:var(--t1)}
.lane2 .pile-2{background:#CFCBC2}
.lane2 .pile-3{background:var(--t2)}
.lane2 .card{background:#FDFDFB;border-radius:6px;padding:14px 22px 16px;
  box-shadow:0 0 0 1px #DDD9D0,0 12px 28px rgba(0,0,0,.16)}
.lane2 .art{min-height:96px}
.lane2 .art::before{content:"";position:absolute;width:172px;height:172px;border-radius:50%;
  background:var(--tint)}
.lane2 .art-emoji{position:relative;font-size:100px;filter:grayscale(1) brightness(0)}
/* BOLDNESS: poster type.
   v4.2 FIX 3 — lane 2's freed space went to TYPE, which is where this lane's
   boldness lives: title 52 -> 66px, claim 17.5 -> 19px. .art stays flex:1 and
   takes what is left over, so the disc grows a little with it. */
.lane2 .issue-title{font-size:66px;letter-spacing:-.03em;line-height:.94;margin-top:10px}
.lane2 .claim-text{margin-top:14px;font-size:19px;line-height:1.42}
.lane2 .ans{background:#FDFDFB;border:1.5px solid #1A1A1A;border-radius:3px;color:#1A1A1A;font-size:21px;
  letter-spacing:.02em;box-shadow:0 3px 0 #1A1A1A}
.lane2 .ans:focus-visible{outline:3px solid #C9A227;outline-offset:3px}"""))

# ---------------------------------------------------------------- lane 3
LANES.append(dict(
  n="3", file="Stickers.dc.html", cls="lane3", dispnote="",
  he="תרבות סטיקרים", en="Israeli Sticker Culture",
  tokens="""<!--
  LANE 3 · Israeli Sticker Culture
  palette   : pole grey #B3B1A9 · white die-cut · black #000 · fixed pink #FF3B6B + topic colours
  type      : SimplerPro Black in slogan chunks; the HUD is a flat band, not a sticker sheet
  texture   : one — the pole: two-scale grain over pale ghost remnants of older stickers
  BOLDNESS  : the art sticker at 196px, breaking clean out over the card's top edge
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
   BOLDNESS  : the art sticker at 196px, breaking clean out over the card's top edge
   TOPIC old->new : religion #ffd23f/#ffb800 -> #FFD60A/#FF8A00 (sticker yellow, sticker orange)
                    branches #2b4cff/#1a3acc -> #3D5BFF/#1E36B8 (electric blue, deep blue) */
.lane3.topic-religion{--t1:#FFD60A;--t2:#FF8A00;--on-t1:#000}
.lane3.topic-branches{--t1:#3D5BFF;--t2:#1E36B8;--on-t1:#fff}
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
.lane3 .pile-1{background:var(--t1);transform:translateY(-11px) rotate(-3.4deg)}
.lane3 .pile-2{background:#FF3B6B;transform:translateY(-20px) rotate(4.6deg)}
.lane3 .pile-3{background:var(--t2);transform:translateY(-29px) rotate(-7deg)}
.lane3 .card{background:#fff;border:7px solid #fff;rotate:-1.4deg;overflow:visible;
  padding:0 18px 16px;box-shadow:0 7px 0 rgba(0,0,0,.42),0 16px 26px rgba(0,0,0,.28)}
/* BOLDNESS: the art sticker breaks out over the card's top edge.
   v4.2 FIX 3 — lane 3's freed space went to ART: the breakout sticker 196 -> 268px,
   which is this lane's stated boldness element. The title takes 2px of it. */
/* v4.3 CHANGE 1 — the source chip's 49px goes into the sticker, not to a gap */
.lane3 .art{flex:1;min-height:252px;margin-top:-44px;overflow:visible;z-index:4}
.lane3 .art-emoji{width:292px;height:292px;display:grid;place-items:center;font-size:0;
  background:var(--t1);border:8px solid #fff;border-radius:44px;rotate:-5deg;
  box-shadow:0 7px 0 rgba(0,0,0,.45),0 14px 22px rgba(0,0,0,.3)}
.lane3 .art-emoji::before{content:"🪖";font-size:186px;line-height:1;
  filter:grayscale(1) brightness(0) invert(1) drop-shadow(0 3px 0 rgba(0,0,0,.4))}
.lane3 .issue-title{background:#000;color:#fff;border:5px solid #fff;padding:6px 14px 9px;rotate:1.4deg;
  align-self:flex-start;font-size:46px;box-shadow:0 4px 0 rgba(0,0,0,.45);margin-top:16px}
.lane3 .claim-text{margin-top:18px;font-size:17px;line-height:1.5;max-width:27ch;text-wrap:balance}
/* fixed lane colour — never the topic colour: this is the אמת/שקר surface */
.lane3 .ans{background:#2EC4B6;color:#000;border:5px solid #fff;border-radius:16px;
  box-shadow:0 5px 0 rgba(0,0,0,.48);font-size:24px}
.lane3 .ans-true{rotate:-1.8deg}
.lane3 .ans-false{rotate:1.8deg}
.lane3 .ans:focus-visible{outline:4px solid #000;outline-offset:4px}"""))

# =========================================================================
def build():
    shared = SHARED.replace("%FONT%", FONT)
    boards = []
    for lane in LANES:
        for tid, tlabel in TOPICS.items():
            fname = lane["file"] if tid == "religion" else lane["file"].replace(".dc.html", "Branches.dc.html")
            body = (BODY
                    .replace("%LANE%", lane["cls"]).replace("%TOPICID%", tid)
                    .replace("%NUM%", lane["n"]).replace("%HE%", lane["he"]).replace("%EN%", lane["en"])
                    .replace("%DISPNOTE%", lane["dispnote"])
                    .replace("%COINS%", COINS).replace("%TOPIC%", tlabel).replace("%TITLE%", TITLE)
                    .replace("%CLAIM_A%", CLAIM_A).replace("%CLAIM_B%", CLAIM_B)
                    .replace("%ANS_T%", ANS_T).replace("%ANS_F%", ANS_F)
                    .replace("%VERIFY%", VERIFY_HTML if VERIFY_MARK else "")
                    .replace("%ART%", ART).replace("%MAP%", MAP)
                    .replace("%BILLDATE%", BILLDATE))
            page = (PAGE.replace("%TOKENS%", lane["tokens"]).replace("%SHARED%", shared)
                    .replace("%LANECSS%", lane["css"].replace("%BIBUSHFONT%", BIBUSH))
                    .replace("%BODY%", body))
            (OUT / fname).write_text(page, encoding="utf-8")
            boards.append((fname, lane, tid, tlabel))

    # religion row on top, branches row below; lane 1 on the right (RTL reading)
    arts = []
    for fname, lane, tid, tlabel in boards:
        col = LANES.index(lane)
        arts.append({"file": fname, "x": (len(LANES) - 1 - col) * 480,
                     "y": 0 if tid == "religion" else 1010, "w": 390, "h": 930,
                     "title": "%s · %s · %s — %s" % (lane["n"], lane["he"], lane["en"], tlabel)})
    (OUT / "canvas.json").write_text(
        json.dumps({"artboards": arts, "launch": {"view": "canvas"}}, ensure_ascii=False, indent=2),
        encoding="utf-8")
    for f, *_ in boards:
        print("%s  %6.1f KB" % (f.ljust(26), (OUT / f).stat().st_size / 1024))

if __name__ == "__main__":
    build()
