# -*- coding: utf-8 -*-
"""v3 — the claim screen, 6 lanes. One shared markup skeleton -> 6 .dc.html
artboards; only the lane class and the lane CSS block differ.
Regenerate:  python3 explorations/build_v3.py
v1 reveal card -> _v1_reveal/ ; v2 eight-lane screen -> _v2_screen/
"""
import base64, json, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT  = ROOT / "explorations"
FONT   = base64.b64encode((ROOT / "fonts" / "SimplerPro_HLAR-Black.woff2").read_bytes()).decode()
# Brief said explorations/fonts/; the files are actually in the repo's fonts/.
# Read-only, inlined into lane D only — nothing is copied anywhere.
BIBUSH = base64.b64encode((ROOT / "fonts" / "BibushChunky.v1.0.otf").read_bytes()).decode()

# ---- verbatim r1 content + the fixed HUD strings ---------------------------
COINS  = "240"
PROG   = "3/8"
TOPIC  = "דת ומדינה"
LIVE   = "שידור"
TITLE  = "חוק הגיוס"
CLAIM_A = "הצעת חוק הגיוס שהקואליציה קידמה ב-2024 מבוססת על "   # + marked phrase + "."
CLAIM_B = "מתווה שכתב... בני גנץ"
ANS_T  = "אמת"
ANS_F  = "שקר"
SOURCE = "ישראל היום"
ART    = "🪖"
MAP    = "מפה"

SHARED = """
@font-face{font-family:'SimplerPro';src:url(data:font/woff2;base64,%FONT%) format('woff2');font-weight:900;font-style:normal;font-display:block}
*{margin:0;padding:0;box-sizing:border-box}
body{background:#9A9A97;font-family:system-ui,"Segoe UI",Arial,sans-serif;font-variant-numeric:tabular-nums;-webkit-font-smoothing:antialiased}
a{color:#1a3acc}
a:hover{color:#0f2894}

/* ---- caption strip: outside the frame, on the grey canvas ---- */
.stage{width:390px;background:#9A9A97;padding-bottom:24px}
.caption{display:flex;flex-wrap:wrap;align-items:baseline;gap:4px 9px;padding:16px 16px 12px;color:#141414}
.cap-num{font-family:'SimplerPro',system-ui,sans-serif;font-weight:900;font-size:26px;line-height:.9}
.cap-he{font-weight:700;font-size:15px;line-height:1.2}
.cap-en{font-size:11.5px;letter-spacing:.05em;text-transform:uppercase;color:#2A2A28}
.cap-font{flex-basis:100%;font-size:10.5px;color:#2A2A28}

/* ---- the frame ---- */
.frame{position:relative;width:390px;min-height:780px;overflow:hidden;isolation:isolate;
  display:flex;flex-direction:column;padding:12px 16px 22px;box-shadow:0 3px 14px rgba(0,0,0,.3)}
.frame-bg{position:absolute;inset:0;z-index:0;pointer-events:none}
.deco{position:absolute;inset:0;width:100%;height:100%;z-index:0;pointer-events:none}
.deco g{display:none}
.sparkles{display:none}

/* ---- HUD: avatar far left · topic + steps centre · coins far right ---- */
.hud{position:relative;z-index:3;flex:none;min-height:48px;display:flex;align-items:center;
  justify-content:space-between;gap:8px}
.hud-coins{display:flex;align-items:center;gap:7px;flex:none}
.coin-glyph{width:22px;height:22px;flex:none;display:grid;place-items:center;border-radius:50%}
.coin-num{font-family:'SimplerPro',system-ui,sans-serif;font-weight:900;font-size:20px;line-height:1}
.hud-mid{display:flex;flex-direction:column;align-items:center;gap:5px;min-width:0}
.hud-live{display:none;align-items:center;gap:6px;font-size:10px;font-weight:800;letter-spacing:.16em;
  padding:3px 8px;line-height:1}
.live-dot{width:7px;height:7px;border-radius:50%;background:currentColor;flex:none}
.topic-chip{display:inline-flex;align-items:center;gap:7px;font-size:11.5px;font-weight:700;
  padding:4px 11px;line-height:1.25;white-space:nowrap}
.topic-mark{display:inline-flex;align-items:center;justify-content:center;width:14px;height:14px;flex:none}
.mark-emoji{font-size:12px;line-height:1}
.topic-prog{font-family:'SimplerPro',system-ui,sans-serif;font-weight:900;font-size:12px;opacity:.85}
/* three step dots = the three beats of the round; the pile behind the card is the same three */
.steps{display:flex;align-items:center;gap:5px}
.step{width:7px;height:7px;border-radius:50%;background:currentColor;opacity:.3;display:block}
.step-on{opacity:1;width:16px;border-radius:4px}
.avatar{position:relative;width:38px;height:38px;flex:none;border-radius:50%;overflow:hidden;
  display:grid;place-items:center}
.avatar-sil{width:78%;height:78%;display:block}

/* ---- the deck: hero card over exactly three beat-card backs ---- */
.deck{position:relative;z-index:1;flex:1;display:flex;align-items:center;justify-content:center;
  padding:22px 0 4px}
.pile{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;pointer-events:none}
.pile-card{position:absolute;width:340px;height:470px}
.pile-1{transform:translateY(-10px) rotate(-1.9deg)}
.pile-2{transform:translateY(-19px) rotate(3.1deg)}
.pile-3{transform:translateY(-28px) rotate(-4.8deg)}
.card{position:relative;z-index:2;width:340px;height:470px;display:flex;flex-direction:column;
  padding:16px 20px 16px}
/* card art slot — the issue emoji, lane-treated, upper half */
.art{position:relative;flex:1;min-height:152px;display:flex;align-items:center;justify-content:center}
.art-emoji{font-size:98px;line-height:1;display:block}
.art-clip{display:none;position:absolute;width:26px;height:58px;fill:none;stroke:currentColor;
  stroke-width:3.4;stroke-linecap:round}
.issue-title{margin-top:4px;font-family:'SimplerPro',system-ui,sans-serif;font-weight:900;
  font-size:34px;line-height:1.04}
.claim-text{margin-top:10px;font-size:16px;line-height:1.5;font-weight:700}
.hl{background:none;color:inherit}
.claim-echo{display:none}
.hints{margin-top:auto;padding-top:18px;display:flex;align-items:center;justify-content:space-between;gap:10px}
.hint{display:flex;align-items:center;gap:6px;font-size:12px;font-weight:800;line-height:1}
.hint-true{flex-direction:row-reverse}
.hint-arrow{width:17px;height:17px;flex:none;fill:none;stroke:currentColor;stroke-width:2.4;
  stroke-linecap:round;stroke-linejoin:round}
.hint-false .hint-arrow{transform:scaleX(-1)}
.source{display:flex;align-items:center;gap:7px;font-size:12.5px;line-height:1.3;margin-top:12px}
.ico-link{width:14px;height:14px;flex:none;stroke:currentColor;fill:none;stroke-width:2;stroke-linecap:round}

/* ---- FAB back to the map: bottom-left, clear of the buttons ---- */
.fab{position:absolute;left:16px;bottom:94px;z-index:4;width:48px;height:48px;border-radius:50%;
  border:0;background:none;color:inherit;cursor:pointer;display:grid;place-items:center;padding:0}
.fab-icon{width:23px;height:23px;fill:none;stroke:currentColor;stroke-width:1.9;stroke-linejoin:round;
  stroke-linecap:round}
.fab:focus-visible{outline:3px solid #0052ff;outline-offset:3px}

/* ---- answer buttons ---- */
.answers{position:relative;z-index:3;flex:none;display:flex;gap:12px;margin-top:16px}
.ans{position:relative;flex:1;min-height:56px;appearance:none;cursor:pointer;border:0;background:none;
  color:inherit;font-family:'SimplerPro',system-ui,sans-serif;font-weight:900;font-size:22px;
  line-height:1;padding:16px 8px;display:grid;place-items:center}
.ans:focus-visible{outline:3px solid #0052ff;outline-offset:3px}

@media (prefers-reduced-motion: reduce){*{animation:none !important;transition:none !important}}
"""

BODY = """<div class="stage %LANE%">
  <header class="caption" dir="rtl" lang="he">
    <span class="cap-num">%NUM%</span>
    <span class="cap-he">%HE%</span>
    <span class="cap-en" dir="ltr">%EN%</span>
    <span class="cap-font">%FONTNOTE%</span>
  </header>

  <div class="frame" dir="rtl" lang="he">
    <div class="frame-bg"></div>
    <svg class="deco" viewBox="0 0 390 800" preserveAspectRatio="xMidYMid slice" aria-hidden="true">
      <defs>
        <filter id="rough" x="-8%" y="-8%" width="116%" height="116%">
          <feTurbulence type="fractalNoise" baseFrequency="0.04 0.07" numOctaves="3" seed="7" result="n"></feTurbulence>
          <feDisplacementMap in="SourceGraphic" in2="n" scale="6" xChannelSelector="R" yChannelSelector="G"></feDisplacementMap>
        </filter>
      </defs>
      <g class="deco-floor">
        <path d="M0 556H390"></path>
        <path d="M195 556-130 800M195 556 5 800M195 556 118 800M195 556 272 800M195 556 385 800M195 556 520 800"></path>
        <path d="M0 598H390M0 650H390M0 716H390"></path>
      </g>
      <g class="deco-knesset">
        <path d="M104 690h182v11H104zM112 636h166v10H112z"></path>
        <path d="M122 646h12v44h-12zM142 646h12v44h-12zM162 646h12v44h-12zM182 646h12v44h-12zM202 646h12v44h-12zM222 646h12v44h-12zM242 646h12v44h-12zM262 646h12v44h-12z"></path>
      </g>
      <g class="deco-ghosts">
        <rect x="16" y="86" width="126" height="54" rx="9" transform="rotate(-7 79 113)"></rect>
        <rect x="238" y="182" width="138" height="46" rx="4" transform="rotate(5 307 205)"></rect>
        <ellipse cx="84" cy="452" rx="74" ry="34" transform="rotate(-11 84 452)"></ellipse>
        <rect x="212" y="558" width="152" height="62" rx="11" transform="rotate(-4 288 589)"></rect>
        <rect x="26" y="646" width="120" height="44" rx="6" transform="rotate(6 86 668)"></rect>
        <ellipse cx="302" cy="66" rx="58" ry="25" transform="rotate(8 302 66)"></ellipse>
      </g>
    </svg>
    <span class="sparkles" aria-hidden="true">✨<i>✨</i><b>✨</b></span>

    <header class="hud">
      <div class="hud-coins">
        <span class="coin-glyph" aria-hidden="true"></span>
        <span class="coin-num">%COINS%</span>
      </div>
      <div class="hud-mid">
        <span class="hud-live"><span class="live-dot"></span>%LIVE%</span>
        <span class="topic-chip">
          <span class="topic-mark" aria-hidden="true"><span class="mark-emoji">🕍</span></span>
          <span class="topic-label">%TOPIC%</span>
          <span class="topic-prog">%PROG%</span>
        </span>
        <span class="steps" aria-hidden="true"><i class="step step-on"></i><i class="step"></i><i class="step"></i></span>
      </div>
      <div class="avatar" aria-hidden="true">
        <svg class="avatar-sil" viewBox="0 0 64 64"><circle cx="32" cy="25" r="12"></circle><path d="M8 60c0-13 10.8-19.5 24-19.5S56 47 56 60Z"></path></svg>
      </div>
    </header>

    <div class="deck">
      <div class="pile" aria-hidden="true">
        <div class="pile-card pile-3"></div>
        <div class="pile-card pile-2"></div>
        <div class="pile-card pile-1"></div>
      </div>
      <article class="card claim">
        <div class="art" aria-hidden="true">
          <span class="art-emoji">%ART%</span>
          <svg class="art-clip" viewBox="0 0 28 60"><path d="M18 18v28a6.5 6.5 0 0 1-13 0V15a10 10 0 0 1 20 0v34"></path></svg>
        </div>
        <h2 class="issue-title">%TITLE%</h2>
        <p class="claim-text">%CLAIM_A%<mark class="hl">%CLAIM_B%</mark>.</p>
        <p class="claim-echo" aria-hidden="true">%CLAIM_A%%CLAIM_B%.</p>
        <div class="hints" aria-hidden="true">
          <span class="hint hint-true"><span class="hint-word">%ANS_T%</span><svg class="hint-arrow" viewBox="0 0 24 24"><path d="M4 12h15M13 6l6 6-6 6"></path></svg></span>
          <span class="hint hint-false"><span class="hint-word">%ANS_F%</span><svg class="hint-arrow" viewBox="0 0 24 24"><path d="M4 12h15M13 6l6 6-6 6"></path></svg></span>
        </div>
        <p class="source"><svg class="ico-link" viewBox="0 0 24 24" aria-hidden="true"><path d="M10.5 13.5a5 5 0 0 0 7.3.4l2.7-2.7a5 5 0 0 0-7-7l-1.5 1.4"></path><path d="M13.5 10.5a5 5 0 0 0-7.3-.4l-2.7 2.7a5 5 0 0 0 7 7l1.4-1.4"></path></svg><span class="source-name">%SOURCE%</span></p>
      </article>
    </div>

    <button type="button" class="fab" aria-label="%MAP%">
      <svg class="fab-icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M3 6.6 9 4l6 2.6L21 4v13.4L15 20l-6-2.6L3 20z"></path><path d="M9 4v13.4M15 6.6V20"></path></svg>
    </button>

    <div class="answers">
      <button type="button" class="ans ans-true">%ANS_T%</button>
      <button type="button" class="ans ans-false">%ANS_F%</button>
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

FONTNOTE_STD = "טקסט: פונט זמני"
FONTNOTE_D   = "טקסט: פונט זמני · תצוגה: Bibush Chunky"
LANES = []

# ---------------------------------------------------------------- lane A
LANES.append(dict(
  n="A", file="Main.dc.html", cls="laneA", note=FONTNOTE_STD,
  he="שידור", en="CRT × Twitch",
  tokens="""<!--
  LANE A · CRT x Twitch
  palette   : near-black blue #070D1A · panel #0D1830 · electric cyan #37E0FF · phosphor #DFF7FF
  type      : SimplerPro Black in phosphor white with a cyan bloom; OSD tabular numerals
  texture   : one — CRT: curved glass corners, 3.5% scanlines, vignette, over the AR floor grid
  signature : the whole frame is a television; the card is the stream's glass panel inside it
-->""",
  css="""/* LANE A · CRT x Twitch
   palette   : near-black blue #070D1A · panel #0D1830 · cyan #37E0FF · phosphor #DFF7FF
   type      : SimplerPro Black in phosphor white with a cyan bloom; OSD tabular numerals
   texture   : one — CRT: curved glass corners, 3.5% scanlines, vignette, over the AR floor grid
   signature : the whole frame is a television; the card is the stream's glass panel inside it */
.laneA .frame{background:#070D1A;color:#DFF7FF;border-radius:30px/22px}
.laneA .frame-bg{background:
  radial-gradient(120% 46% at 50% 104%,rgba(55,224,255,.24),transparent 66%),
  linear-gradient(180deg,#070D1A 0%,#091428 62%,#06111F 100%);border-radius:30px/22px}
/* the CRT itself — scanlines + vignette ride above everything, at 3.5% */
.laneA .frame::after{content:"";position:absolute;inset:0;z-index:9;pointer-events:none;
  border-radius:30px/22px;
  background:repeating-linear-gradient(rgba(0,0,0,.035) 0 1px,transparent 1px 3px),
    radial-gradient(120% 96% at 50% 50%,transparent 56%,rgba(0,0,0,.42) 100%);
  box-shadow:inset 0 0 26px rgba(0,0,0,.7),inset 0 0 2px rgba(223,247,255,.35)}
.laneA .deco .deco-floor{display:block;fill:none;stroke:#37E0FF;stroke-width:1;opacity:.4}
.laneA .hud-live{display:inline-flex;color:#37E0FF;background:rgba(55,224,255,.1);
  border:1px solid rgba(55,224,255,.5);border-radius:2px}
.laneA .live-dot{animation:aLive 2s ease-in-out infinite;box-shadow:0 0 8px #37E0FF}
@keyframes aLive{0%,100%{opacity:1}50%{opacity:.28}}
.laneA .mark-emoji{display:none}
.laneA .topic-chip{background:rgba(13,24,48,.9);border:1px solid rgba(55,224,255,.4);color:#B7E8FA;
  border-radius:2px;letter-spacing:.05em;padding-inline-start:8px}
.laneA .topic-mark{width:3px;height:13px;background:#37E0FF;box-shadow:0 0 8px #37E0FF}
.laneA .topic-prog{color:#DFF7FF}
.laneA .steps{color:#37E0FF}
/* OSD numerals, like a TV volume overlay */
.laneA .coin-glyph{border-radius:2px;background:rgba(13,24,48,.9);
  box-shadow:inset 0 0 0 1.5px #37E0FF,0 0 10px rgba(55,224,255,.35)}
.laneA .coin-num{color:#DFF7FF;font-size:22px;letter-spacing:.04em;
  text-shadow:0 0 12px rgba(55,224,255,.75)}
.laneA .avatar{background:#0D1830;box-shadow:inset 0 0 0 1.5px rgba(55,224,255,.6),
  inset 0 0 14px rgba(0,0,0,.9),0 0 12px rgba(55,224,255,.25)}
.laneA .avatar-sil{fill:rgba(55,224,255,.55)}
.laneA .pile-card{background:linear-gradient(180deg,rgba(19,40,76,.9),rgba(8,19,42,.75));
  border:1px solid rgba(55,224,255,.34);border-radius:3px;box-shadow:0 0 20px rgba(55,224,255,.16)}
.laneA .card{background:linear-gradient(180deg,rgba(20,42,80,.82),rgba(9,20,44,.7));
  border:1px solid rgba(120,224,255,.55);border-radius:3px;backdrop-filter:blur(4px);
  box-shadow:0 0 40px rgba(55,224,255,.22),0 24px 40px rgba(0,0,0,.6),inset 0 1px 0 rgba(255,255,255,.22)}
.laneA .card::before{content:"";position:absolute;top:-1px;left:14px;right:14px;height:2px;
  background:linear-gradient(90deg,transparent,#37E0FF,transparent);box-shadow:0 0 12px #37E0FF}
/* art slot: glowing emblem, 1px RGB split */
.laneA .art::before{content:"";position:absolute;width:170px;height:170px;border-radius:50%;
  background:radial-gradient(closest-side,rgba(55,224,255,.34),transparent 72%)}
.laneA .art-emoji{position:relative;filter:drop-shadow(0 0 16px rgba(55,224,255,.7));
  text-shadow:-1px 0 0 rgba(255,40,90,.85),1px 0 0 rgba(0,225,255,.85)}
.laneA .issue-title{color:#fff;letter-spacing:-.015em;text-shadow:0 0 24px rgba(55,224,255,.55)}
.laneA .claim-text{color:#D6EAF9}
.laneA .hint{color:#37E0FF;letter-spacing:.08em;text-shadow:0 0 10px rgba(55,224,255,.7)}
.laneA .source{color:#8FBEDD;border-top:1px solid rgba(120,224,255,.2);padding-top:10px;letter-spacing:.03em}
.laneA .fab{background:rgba(13,24,48,.92);color:#37E0FF;
  box-shadow:inset 0 0 0 1.5px rgba(55,224,255,.65),0 0 18px rgba(55,224,255,.3),0 6px 14px rgba(0,0,0,.6)}
.laneA .fab:focus-visible{outline:3px solid #37E0FF;outline-offset:3px}
.laneA .ans{background:linear-gradient(180deg,rgba(20,44,84,.9),rgba(9,22,46,.85));
  border:1px solid rgba(120,224,255,.6);border-radius:3px;color:#EAF8FF;letter-spacing:.04em;
  box-shadow:inset 0 1px 0 rgba(255,255,255,.2),0 0 20px rgba(55,224,255,.18),0 4px 0 rgba(15,80,110,.9)}
.laneA .ans:focus-visible{outline:3px solid #37E0FF;outline-offset:3px}"""))

# ---------------------------------------------------------------- lane B
LANES.append(dict(
  n="B", file="Stickers.dc.html", cls="laneB", note=FONTNOTE_STD,
  he="תרבות סטיקרים", en="Israeli Sticker Culture",
  tokens="""<!--
  LANE B · Israeli Sticker Culture
  palette   : yellow #FFD60A · hot-pink #FF3B6B · teal #2EC4B6 · black #000 · pole-grey #B9B7B0
  type      : SimplerPro Black in slogan chunks; every chunk gets its own die-cut
  texture   : one — the street pole: grain over pale torn remnants of older stickers
  signature : the card is the newest, biggest sticker; the art slot is the one on top of it
-->""",
  css="""/* LANE B · Israeli Sticker Culture
   palette   : yellow #FFD60A · hot-pink #FF3B6B · teal #2EC4B6 · black #000 · pole-grey #B9B7B0
   type      : SimplerPro Black slogan chunks; every chunk gets its own die-cut
   texture   : one — the street pole: grain over pale torn remnants of older stickers
   signature : the card is the newest, biggest sticker; the art slot is the one stuck on top */
.laneB .frame{background:#B9B7B0;color:#000}
.laneB .frame-bg{background:#B9B7B0}
.laneB .frame-bg::after{content:"";position:absolute;inset:0;opacity:.5;
  background-image:radial-gradient(rgba(0,0,0,.55) .5px,transparent .5px),
    radial-gradient(rgba(255,255,255,.65) .5px,transparent .5px);
  background-size:3px 3px,5px 5px;background-position:0 0,2px 1px}
.laneB .deco .deco-ghosts{display:block;fill:#CFCDC6;stroke:#fff;stroke-width:3;opacity:.55}
.laneB .coin-glyph{background:#2EC4B6;border:3px solid #fff;box-shadow:0 2px 0 rgba(0,0,0,.45);rotate:-8deg}
.laneB .coin-num{color:#000}
.laneB .topic-chip{background:#FF3B6B;color:#000;border:3px solid #fff;border-radius:999px;rotate:-2.5deg;
  box-shadow:0 2px 0 rgba(0,0,0,.45);font-weight:900}
.laneB .topic-prog{color:#000}
.laneB .steps{color:#000}
.laneB .avatar{background:#FFD60A;border:3px solid #fff;box-shadow:0 2px 0 rgba(0,0,0,.45);rotate:5deg}
.laneB .avatar-sil{fill:#000}
.laneB .pile-1{background:#FFD60A;border:5px solid #fff;box-shadow:0 4px 0 rgba(0,0,0,.4)}
.laneB .pile-2{background:#2EC4B6;border:5px solid #fff;box-shadow:0 4px 0 rgba(0,0,0,.4)}
.laneB .pile-3{background:#FF3B6B;border:5px solid #fff;box-shadow:0 4px 0 rgba(0,0,0,.4)}
.laneB .card{background:#fff;border:7px solid #fff;rotate:-1.4deg;
  box-shadow:0 7px 0 rgba(0,0,0,.42),0 16px 26px rgba(0,0,0,.28)}
.laneB .card::after{content:"";position:absolute;left:-7px;bottom:-7px;width:40px;height:40px;
  background:linear-gradient(45deg,#EFEDE7 0 52%,#fff 52%);clip-path:polygon(0 100%,100% 100%,0 0);
  box-shadow:5px -5px 9px rgba(0,0,0,.24)}
/* art slot: the biggest die-cut on the card */
.laneB .art{min-height:110px}
.laneB .art-emoji{background:#FFD60A;border:6px solid #fff;border-radius:26px;padding:8px 15px 12px;
  font-size:82px;rotate:-4deg;box-shadow:0 5px 0 rgba(0,0,0,.45)}
.laneB .issue-title{background:#2EC4B6;border:5px solid #fff;padding:6px 14px 8px;rotate:1.6deg;
  align-self:flex-start;font-size:34px;box-shadow:0 4px 0 rgba(0,0,0,.45);margin-top:8px}
.laneB .claim-text{margin-top:14px}
.laneB .hint{background:#2EC4B6;color:#000;border:4px solid #fff;border-radius:10px;padding:7px 11px;
  font-weight:900;box-shadow:0 3px 0 rgba(0,0,0,.42)}
.laneB .hint-true{rotate:-6deg}
.laneB .hint-false{rotate:6deg;background:#FF3B6B}
.laneB .source{background:#fff;border:4px solid #fff;padding:5px 11px;rotate:-1.6deg;font-weight:800;
  align-self:flex-start;box-shadow:0 3px 0 rgba(0,0,0,.4)}
.laneB .fab{background:#FFD60A;color:#000;border:5px solid #fff;rotate:-7deg;
  box-shadow:0 4px 0 rgba(0,0,0,.45)}
.laneB .fab:focus-visible{outline:4px solid #000;outline-offset:4px}
.laneB .ans{border:5px solid #fff;border-radius:16px;box-shadow:0 5px 0 rgba(0,0,0,.48);font-size:24px}
.laneB .ans-true{background:#FFD60A;color:#000;rotate:-2.2deg}
.laneB .ans-false{background:#FF3B6B;color:#000;rotate:2.2deg}
.laneB .ans:focus-visible{outline:4px solid #000;outline-offset:4px}"""))

# ---------------------------------------------------------------- lane C
LANES.append(dict(
  n="C", file="AcidType.dc.html", cls="laneC", note=FONTNOTE_STD,
  he="טיפוגרפי חומצי", en="Acid Typographic",
  tokens="""<!--
  LANE C · Acid Typographic
  palette   : acid field #3ECF6E · card #4BD97A · black #0A0A0A · white · accent #FF7A00 (coin only)
  type      : the v2 claim block unchanged — 16px/700 between two 3px rules; title 44px
  texture   : one — the claim echoed once behind itself at 5% black
  signature : the art slot as a huge flat black ideogram (the data emoji, filtered to solid black)
-->""",
  css="""/* LANE C · Acid Typographic
   palette   : acid field #3ECF6E · card #4BD97A · black #0A0A0A · white · accent #FF7A00 (coin)
   type      : the v2 claim block unchanged — 16px/700 between two 3px rules; title 44px
   texture   : one — the claim echoed once behind itself at 5% black
   signature : the art slot as a huge flat black ideogram (the data emoji, filtered solid black) */
.laneC .frame{background:#3ECF6E;color:#0A0A0A}
.laneC .frame-bg{background:#3ECF6E}
.laneC .coin-glyph{background:#FF7A00;border-radius:0}
.laneC .coin-num{color:#0A0A0A;font-size:21px}
.laneC .topic-mark{display:none}
.laneC .topic-chip{color:#0A0A0A;font-weight:800;letter-spacing:.18em;font-size:10.5px;padding:4px 0;gap:10px}
.laneC .topic-prog{letter-spacing:0}
.laneC .steps{color:#0A0A0A}
.laneC .avatar{border-radius:0;background:#0A0A0A}
.laneC .avatar-sil{fill:#3ECF6E}
.laneC .pile-card{background:#0A0A0A}
.laneC .card{background:#4BD97A;box-shadow:inset 0 0 0 3px #0A0A0A;overflow:hidden}
/* signature: emoji filtered to a flat black ideogram */
.laneC .art{min-height:150px}
.laneC .art-emoji{position:relative;z-index:2;font-size:118px;
  filter:grayscale(1) brightness(0) contrast(2)}
.laneC .claim-echo{display:block;position:absolute;z-index:0;top:196px;left:-40px;right:-40px;
  font-family:'SimplerPro',system-ui,sans-serif;font-weight:900;font-size:44px;line-height:.92;
  color:rgba(10,10,10,.04);pointer-events:none;user-select:none}
.laneC .issue-title{position:relative;z-index:2;font-size:44px;letter-spacing:-.03em;margin-top:2px}
/* the benchmark block — unchanged from v2 */
.laneC .claim-text{position:relative;z-index:2;font-size:16px;line-height:1.5;font-weight:700;
  margin-top:14px;border-top:3px solid #0A0A0A;border-bottom:3px solid #0A0A0A;padding:12px 0}
.laneC .hints{position:relative;z-index:2}
.laneC .hint{color:#0A0A0A;font-weight:900;letter-spacing:.16em;font-size:11px}
.laneC .source{position:relative;z-index:2;color:#0A0A0A;font-weight:800;letter-spacing:.06em}
.laneC .fab{background:#0A0A0A;color:#3ECF6E;border-radius:0;box-shadow:0 5px 0 rgba(10,10,10,.35)}
.laneC .fab:focus-visible{outline:3px solid #0A0A0A;outline-offset:4px}
.laneC .ans{background:#0A0A0A;color:#fff;letter-spacing:.05em;box-shadow:0 5px 0 rgba(10,10,10,.35)}
.laneC .ans:focus-visible{outline:3px solid #0A0A0A;outline-offset:4px}"""))

# ---------------------------------------------------------------- lane D
LANES.append(dict(
  n="D", file="DefacedPaperwork.dc.html", cls="laneD", note=FONTNOTE_D,
  he="טופס מודבק", en="Defaced Paperwork",
  tokens="""<!--
  LANE D · Defaced Paperwork
  palette   : paper #A39A8A · ink #2B2626 · manila #B8A97E · ochre stamp #C08A2E · acid pink #FF3B6B
  type      : Bibush Chunky for display (title, אמת/שקר); stand-in system face for body
  texture   : one — office document: hard rules, dashed rules, file tabs, zero radii
  signature : exactly three teenage interventions on a neutral form — sticker, highlighter, tape
-->""",
  css="""/* LANE D · Defaced Paperwork
   palette   : paper #A39A8A · ink #2B2626 · manila #B8A97E · ochre stamp #C08A2E · acid pink #FF3B6B
   type      : Bibush Chunky for display (title, אמת/שקר); stand-in system face for body
   texture   : one — office document: hard rules, dashed rules, file tabs, zero radii
   signature : exactly three teenage interventions on a neutral form — sticker, highlighter, tape
   (the ochre stamps are the DOCUMENT's own grammar, not an intervention — they carry the
    verdict stamp later; the three interventions are counted below and marked INTERVENTION) */

/* Bibush Chunky — Hebrew letters + digits only. NO gershayim U+05F4 and NO geresh U+05F3.
   Checked: the brief's suggested fallback U+0022 (") is ALSO absent from both cuts, so a
   substitute cannot be set in Bibush at all — .gershayim below renders it in the stand-in
   face, optically matched. Nothing on this screen contains ח״כ, but the app title does. */
@font-face{font-family:'BibushChunky';src:url(data:font/ttf;base64,%BIBUSH%) format('truetype');
  font-weight:400;font-style:normal;font-display:block}
.laneD .gershayim{font-family:system-ui,"Segoe UI",Arial,sans-serif;font-weight:700;
  font-size:.72em;vertical-align:.28em;letter-spacing:0;margin:0 .02em}

.laneD .frame{background:#2B2626;color:#2B2626}
.laneD .frame-bg{background:#2B2626}
.laneD .frame-bg::after{content:"";position:absolute;inset:0;opacity:.5;
  background-image:repeating-conic-gradient(rgba(255,255,255,.05) 0 25%,transparent 0 50%);
  background-size:4px 4px}
.laneD .coin-glyph{background:#6E6A54;border-radius:0;box-shadow:inset 0 0 0 2px #2B2626}
.laneD .coin-num{color:#D8D2C4;font-family:'BibushChunky',system-ui,sans-serif;font-size:23px}
/* INTERVENTION 1 — the slapped sticker, standing in for the topic chip */
.laneD .topic-chip{background:#FF3B6B;color:#2B2626;border:3px solid #fff;border-radius:999px;
  rotate:-4deg;font-weight:900;box-shadow:0 3px 0 rgba(0,0,0,.5)}
/* Bibush Chunky covers Hebrew letters + digits only — it has no "/" either, so 3/8 would set
   half in Bibush and half in the fallback. The progress reading stays in the stand-in face. */
.laneD .topic-prog{color:#2B2626;font-size:12px}
.laneD .steps{color:#A39A8A}
.laneD .avatar{border-radius:0;background:#6E6A54;box-shadow:inset 0 0 0 2px #2B2626}
.laneD .avatar-sil{fill:#2B2626}
/* file-tab pile */
.laneD .pile-card{background:#B8A97E;border-radius:0;box-shadow:inset 0 0 0 1px #8A7C55,0 2px 0 rgba(0,0,0,.5)}
.laneD .pile-card::before{content:"";position:absolute;top:-13px;width:96px;height:14px;background:#B8A97E;
  box-shadow:inset 0 0 0 1px #8A7C55}
.laneD .pile-1::before{right:26px}
.laneD .pile-2::before{right:132px}
.laneD .pile-3::before{right:230px}
.laneD .card{background:#A39A8A;border-radius:0;
  box-shadow:inset 0 0 0 1px #8A8171,0 4px 0 rgba(0,0,0,.55),0 18px 26px rgba(0,0,0,.45)}
/* INTERVENTION 3 — one strip of tape holding the top-left corner */
.laneD .card::before{content:"";position:absolute;top:-14px;left:-22px;width:104px;height:30px;
  rotate:-38deg;background:linear-gradient(96deg,rgba(226,226,214,.5),rgba(206,208,196,.62));
  box-shadow:inset 0 0 0 1px rgba(255,255,255,.35);z-index:5}
/* art slot: booth photo, paperclipped */
.laneD .art{min-height:126px}
.laneD .art-emoji{background:#6E6A54;box-shadow:inset 0 0 0 2px #2B2626,0 0 0 1px #8A8171;
  padding:12px 24px 16px;font-size:82px}
.laneD .art-clip{display:block;color:#4B4740;top:-14px;left:96px;rotate:9deg}
.laneD .issue-title{font-family:'BibushChunky',system-ui,sans-serif;font-weight:400;font-size:42px;
  line-height:1.1;margin-top:10px;border-bottom:2px solid #7A7264;padding-bottom:8px}
.laneD .claim-text{color:#2B2626;margin-top:12px;line-height:1.55}
/* INTERVENTION 2 — one highlighter swipe across the claim's punchline */
.laneD .hl{background:linear-gradient(104deg,rgba(62,207,110,0) 0,rgba(62,207,110,.62) 1.5%,
  rgba(62,207,110,.62) 98%,rgba(62,207,110,0) 100%);
  box-decoration-break:clone;-webkit-box-decoration-break:clone;padding:1px 2px}
/* the document's own rubber-stamp grammar */
.laneD .hint{color:#C08A2E;font-weight:900;letter-spacing:.1em;font-size:11px;padding:5px 9px;
  box-shadow:inset 0 0 0 2.5px #C08A2E}
.laneD .hint-true{rotate:-4deg}
.laneD .hint-false{rotate:4deg}
.laneD .source{color:#3A342B;font-weight:700;letter-spacing:.05em;font-size:11.5px;
  border-top:1px dashed #7A7264;padding-top:10px}
.laneD .fab{background:#D8D2C4;color:#2B2626;border-radius:0;
  box-shadow:inset 0 0 0 2px #2B2626,4px 4px 0 rgba(0,0,0,.5)}
.laneD .fab:focus-visible{outline:3px solid #D8D2C4;outline-offset:4px}
.laneD .ans{background:#D8D2C4;color:#2B2626;border-radius:0;font-family:'BibushChunky',system-ui,sans-serif;
  font-weight:400;font-size:26px;box-shadow:inset 0 0 0 2px #2B2626,4px 4px 0 rgba(0,0,0,.5)}
.laneD .ans:focus-visible{outline:3px solid #D8D2C4;outline-offset:4px}""".replace("%BIBUSH%", "%BIBUSHFONT%")))

# ---------------------------------------------------------------- lane E
LANES.append(dict(
  n="E", file="StateKitsch.dc.html", cls="laneE", note=FONTNOTE_STD,
  he="קיטש ממלכתי אפי", en="Epic State Kitsch",
  tokens="""<!--
  LANE E · Epic State Kitsch
  palette   : gold #F5C542 · deep gold #C9932B · sky #7EB8E6 · cloud cream #FFF4DC · label #5C4008
  type      : SimplerPro Black bevelled by stacked text-shadows; body dark brown on cream
  texture   : one — the cloud bank, painted in the background layer, never above content
  signature : the art slot radiant on a sky band, over a solid gold colonnade in the gap
-->""",
  css="""/* LANE E · Epic State Kitsch
   palette   : gold #F5C542 · deep gold #C9932B · sky #7EB8E6 · cloud cream #FFF4DC · label #5C4008
   type      : SimplerPro Black bevelled by stacked text-shadows; body dark brown on cream
   texture   : one — the cloud bank, painted in the background layer, never above content
   signature : the art slot radiant on a sky band, over a solid gold colonnade in the gap */
.laneE .frame{background:#7EB8E6;color:#4A3A12}
.laneE .frame-bg{background:
  radial-gradient(52px 34px at 14% 20%,rgba(255,255,255,.92),transparent 72%),
  radial-gradient(66px 40px at 84% 13%,rgba(255,255,255,.85),transparent 72%),
  radial-gradient(78px 44px at 22% 47%,rgba(255,255,255,.7),transparent 74%),
  radial-gradient(86px 48px at 90% 55%,rgba(255,255,255,.62),transparent 74%),
  radial-gradient(150% 40% at 50% 100%,rgba(245,197,66,.6),transparent 66%),
  linear-gradient(180deg,#5FA2D8,#7EB8E6 46%,#BFD9F0 100%)}
.laneE .deco .deco-knesset{display:block;fill:#A87A1E}
.laneE .sparkles{display:block;position:absolute;inset:0;z-index:2;pointer-events:none;font-size:0}
.laneE .sparkles>i,.laneE .sparkles>b{position:absolute;font-style:normal;font-weight:400}
.laneE .sparkles>i{top:78px;left:26px;font-size:17px;animation:eTw 3.4s ease-in-out infinite .8s}
.laneE .sparkles>b{top:250px;right:24px;font-size:21px;animation:eTw 3.9s ease-in-out infinite 1.6s}
.laneE .sparkles::after{content:"✨";position:absolute;top:614px;left:96px;font-size:19px;
  animation:eTw 4.4s ease-in-out infinite}
@keyframes eTw{0%,100%{opacity:.55;scale:.9}50%{opacity:1;scale:1.12}}
/* the monogram-coin grammar, reused for the avatar frame */
.laneE .coin-glyph{width:24px;height:24px;background:radial-gradient(circle at 33% 27%,#FFF3C8,#F5C542 52%,#C9932B);
  border:2px solid #A87A1E;box-shadow:0 0 14px rgba(245,197,66,.9),inset 0 2px 0 rgba(255,255,255,.85)}
.laneE .coin-glyph::after{content:"";width:9px;height:9px;border-radius:50%;
  box-shadow:inset 0 1px 1px rgba(138,99,26,.8),0 1px 0 rgba(255,255,255,.7)}
.laneE .coin-num{color:#FFF3C8;text-shadow:0 1px 0 #C9932B,0 2px 0 #A87A1E,0 3px 5px rgba(74,58,18,.5)}
.laneE .topic-chip{background:linear-gradient(180deg,#FFF4DC,#FFE9A8);color:#5C4008;border-radius:999px;
  border:1px solid #C9932B;box-shadow:inset 0 1px 0 rgba(255,255,255,.9)}
.laneE .topic-prog{color:#5C4008}
.laneE .steps{color:#FFF3C8}
.laneE .avatar{width:40px;height:40px;background:radial-gradient(circle at 33% 27%,#FFF3C8,#F5C542 52%,#C9932B);
  border:2px solid #A87A1E;box-shadow:0 0 16px rgba(245,197,66,.85),inset 0 2px 0 rgba(255,255,255,.85)}
.laneE .avatar-sil{fill:#8A631A}
.laneE .pile-card{background:linear-gradient(180deg,#FFF9E9,#FFE9BE);border-radius:20px;
  border:2px solid #E7BE6A;box-shadow:0 8px 20px rgba(74,58,18,.3)}
.laneE .card{background:linear-gradient(180deg,#FFFBF0,#FFEFD2);border-radius:22px;border:2px solid #E7BE6A;
  box-shadow:0 0 0 4px rgba(255,255,255,.6),0 18px 34px rgba(74,58,18,.35),inset 0 2px 0 rgba(255,255,255,.95)}
/* art slot + title share one sky band, so the gold reads */
.laneE .art{min-height:172px;margin:-16px -20px 0;padding-top:10px;border-radius:20px 20px 0 0;
  background:linear-gradient(180deg,#59A0D8,#86BFE8)}
.laneE .art::before{content:"";position:absolute;width:176px;height:176px;border-radius:50%;
  background:radial-gradient(closest-side,rgba(255,243,200,.95),rgba(245,197,66,.4),transparent 76%)}
.laneE .art-emoji{position:relative;filter:drop-shadow(0 3px 0 #A87A1E) drop-shadow(0 0 20px rgba(255,233,168,.95))}
.laneE .issue-title{margin:0 -20px;padding:0 20px 16px;background:#86BFE8;color:#FFE9A8;font-size:40px;
  text-shadow:0 1px 0 #F5C542,0 2px 0 #D9A233,0 3px 0 #C9932B,0 4px 0 #A87A1E,0 6px 10px rgba(74,58,18,.5)}
.laneE .claim-text{color:#4A3A12;margin-top:14px}
.laneE .hint{color:#8A631A;font-weight:800}
.laneE .source{color:#5C4A1E;font-weight:700;border-top:1px solid #E7BE6A;padding-top:10px}
.laneE .fab{background:linear-gradient(180deg,#FFF3C8,#F5C542 46%,#C9932B);color:#5C4008;
  border:2px solid #A87A1E;box-shadow:0 0 20px rgba(245,197,66,.8),inset 0 2px 0 rgba(255,255,255,.9),0 4px 0 #8A631A}
.laneE .fab:focus-visible{outline:3px solid #5C4008;outline-offset:4px}
.laneE .ans{background:linear-gradient(180deg,#FFF3C8,#F5C542 46%,#C9932B);color:#5C4008;
  border:2px solid #A87A1E;border-radius:20px 20px 26px 26px;letter-spacing:.02em;font-size:23px;
  text-shadow:0 1px 0 rgba(255,255,255,.9);
  box-shadow:0 0 26px rgba(245,197,66,.85),inset 0 2px 0 rgba(255,255,255,.95),
             inset 0 -5px 7px rgba(120,84,14,.3),0 5px 0 #8A631A}
.laneE .ans:focus-visible{outline:3px solid #5C4008;outline-offset:4px}"""))

# ---------------------------------------------------------------- lane F
LANES.append(dict(
  n="F", file="NytGames.dc.html", cls="laneF", note=FONTNOTE_STD,
  he="משחקי עיתון", en="NYT Games",
  tokens="""<!--
  LANE F · NYT Games
  palette   : warm grey #E8E6E1 · paper #FDFDFB · ink #1A1A1A · violet #7B61C4 · yellow #E6B93F · sky #6AA9E0
  type      : one display size, one body size at 16/700, small caps for micro-labels; amber = surprise
  texture   : none — flat brand-family colour and a strict grid do the work; green banned in this lane
  signature : three differently-coloured game-tile card backs behind one paper-white hero card
-->""",
  css="""/* LANE F · NYT Games
   palette   : warm grey #E8E6E1 · paper #FDFDFB · ink #1A1A1A · violet #7B61C4 · yellow #E6B93F · sky #6AA9E0
   type      : one display size, one body size at 16/700, small caps for micro-labels
   texture   : none — flat brand-family colour and a strict grid; green is banned in this lane
   signature : three differently-coloured game-tile card backs behind one paper-white hero */
.laneF .frame{background:#E8E6E1;color:#1A1A1A;padding:12px 20px 26px}
.laneF .frame-bg{background:#E8E6E1}
.laneF .coin-glyph{background:#FDFDFB;box-shadow:inset 0 0 0 1.5px #1A1A1A}
.laneF .coin-num{color:#1A1A1A}
.laneF .topic-mark{display:none}
.laneF .topic-chip{color:#4A4A46;font-size:10.5px;font-weight:700;letter-spacing:.17em;
  padding:4px 0;gap:10px}
.laneF .topic-prog{color:#1A1A1A;letter-spacing:0}
.laneF .steps{color:#7B61C4}
.laneF .avatar{background:#FDFDFB;box-shadow:inset 0 0 0 1.5px #1A1A1A}
.laneF .avatar-sil{fill:#B9B5AC}
/* signature: the games-family card backs */
.laneF .pile-card{border-radius:6px;box-shadow:0 3px 10px rgba(0,0,0,.14)}
.laneF .pile-1{background:#6AA9E0}
.laneF .pile-2{background:#E6B93F}
.laneF .pile-3{background:#7B61C4}
.laneF .card{background:#FDFDFB;border-radius:6px;padding:18px 22px 18px;
  box-shadow:0 0 0 1px #DDD9D0,0 12px 28px rgba(0,0,0,.16)}
/* art slot: games-icon style — flat emoji on a soft tile-coloured disc */
.laneF .art{min-height:158px}
.laneF .art::before{content:"";position:absolute;width:148px;height:148px;border-radius:50%;
  background:#D6C9F0}
.laneF .art-emoji{position:relative;font-size:88px}
.laneF .issue-title{font-size:38px;letter-spacing:-.015em;line-height:1.06;margin-top:6px}
.laneF .claim-text{margin-top:14px;line-height:1.55}
/* the pre-flip tile pair, unchanged from v2 */
.laneF .hint{background:#FDFDFB;border:2px solid #DDD9D0;border-radius:3px;padding:9px 13px;
  color:#4A4A46;font-size:12.5px;letter-spacing:.06em}
.laneF .hint .hint-arrow{stroke:#787C7E}
.laneF .source{margin-top:14px;padding-top:12px;border-top:1px solid #DDD9D0;font-size:14.5px;
  font-weight:700;color:#1A1A1A}
.laneF .source .ico-link{width:15px;height:15px;color:#787C7E}
.laneF .source-name{border-bottom:2px solid #C9A227;padding-bottom:1px}
.laneF .fab{background:#FDFDFB;color:#1A1A1A;box-shadow:inset 0 0 0 1.5px #1A1A1A,0 3px 0 #1A1A1A}
.laneF .fab:focus-visible{outline:3px solid #C9A227;outline-offset:3px}
.laneF .ans{background:#FDFDFB;border:1.5px solid #1A1A1A;border-radius:3px;color:#1A1A1A;font-size:21px;
  letter-spacing:.02em;box-shadow:0 3px 0 #1A1A1A}
.laneF .ans:focus-visible{outline:3px solid #C9A227;outline-offset:3px}"""))

# =========================================================================
def build():
    shared = SHARED.replace("%FONT%", FONT)
    for lane in LANES:
        body = (BODY
                .replace("%LANE%", lane["cls"]).replace("%NUM%", lane["n"])
                .replace("%HE%", lane["he"]).replace("%EN%", lane["en"])
                .replace("%FONTNOTE%", lane["note"])
                .replace("%COINS%", COINS).replace("%PROG%", PROG).replace("%TOPIC%", TOPIC)
                .replace("%LIVE%", LIVE).replace("%TITLE%", TITLE)
                .replace("%CLAIM_A%", CLAIM_A).replace("%CLAIM_B%", CLAIM_B)
                .replace("%ANS_T%", ANS_T).replace("%ANS_F%", ANS_F).replace("%SOURCE%", SOURCE)
                .replace("%ART%", ART).replace("%MAP%", MAP))
        page = (PAGE
                .replace("%TOKENS%", lane["tokens"]).replace("%SHARED%", shared)
                .replace("%LANECSS%", lane["css"].replace("%BIBUSHFONT%", BIBUSH))
                .replace("%BODY%", body))
        (OUT / lane["file"]).write_text(page, encoding="utf-8")

    manifest = {
        "artboards": [
            {"file": l["file"], "x": (len(LANES) - 1 - i) * 480, "y": 0, "w": 390, "h": 880,
             "title": "%s · %s · %s" % (l["n"], l["he"], l["en"])}
            for i, l in enumerate(LANES)
        ],
        "launch": {"view": "canvas"},
    }
    (OUT / "canvas.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    for l in LANES:
        print("%s  %6.1f KB" % (l["file"].ljust(24), (OUT / l["file"]).stat().st_size / 1024))

if __name__ == "__main__":
    build()
