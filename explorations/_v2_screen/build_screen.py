# -*- coding: utf-8 -*-
"""v2 — the claim screen only, skinned 8 ways.
One shared markup skeleton -> 8 .dc.html artboards. Only the lane class and the
lane CSS block differ. Regenerate:  python3 explorations/build_screen.py
The v1 MK reveal card is parked in explorations/_v1_reveal/ for the shortlist.
"""
import base64, json, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT  = ROOT / "explorations"
FONT = base64.b64encode((ROOT / "fonts" / "SimplerPro_HLAR-Black.woff2").read_bytes()).decode()

# ---- verbatim content, issue r1 of data.js + the fixed HUD strings ----------
COINS   = "240"
PROG    = "3/8"
TOPIC   = "דת ומדינה"
LIVE    = "שידור"
TITLE   = "חוק הגיוס"
CLAIM   = "הצעת חוק הגיוס שהקואליציה קידמה ב-2024 מבוססת על מתווה שכתב... בני גנץ."
ANS_T   = "אמת"
ANS_F   = "שקר"
SOURCE  = "ישראל היום"

SHARED = """
@font-face{font-family:'SimplerPro';src:url(data:font/woff2;base64,%FONT%) format('woff2');font-weight:900;font-style:normal;font-display:block}
*{margin:0;padding:0;box-sizing:border-box}
body{background:#9A9A97;font-family:system-ui,"Segoe UI",Arial,sans-serif;font-variant-numeric:tabular-nums;-webkit-font-smoothing:antialiased}
a{color:#1a3acc}
a:hover{color:#0f2894}

/* ---- caption strip: outside the frame, on the grey canvas ---- */
.stage{width:390px;background:#9A9A97;padding-bottom:24px}
.caption{display:flex;flex-wrap:wrap;align-items:baseline;gap:4px 9px;padding:16px 16px 12px;color:#141414}
.cap-num{font-family:'SimplerPro',system-ui,sans-serif;font-weight:900;font-size:27px;line-height:.9}
.cap-he{font-weight:700;font-size:15px;line-height:1.2}
.cap-en{font-size:11.5px;letter-spacing:.05em;text-transform:uppercase;color:#2A2A28}
.cap-font{flex-basis:100%;font-size:10.5px;color:#2A2A28}

/* ---- the frame ---- */
.frame{position:relative;width:390px;min-height:780px;overflow:hidden;isolation:isolate;
  display:flex;flex-direction:column;padding:14px 16px 22px;box-shadow:0 3px 14px rgba(0,0,0,.3)}
.frame-bg{position:absolute;inset:0;z-index:0;pointer-events:none}
.deco{position:absolute;inset:0;width:100%;height:100%;z-index:0;pointer-events:none}
.deco g{display:none}
.sparkles{display:none}

/* ---- HUD ---- */
.hud{position:relative;z-index:3;flex:none;height:46px;display:flex;align-items:center;
  justify-content:space-between;gap:10px}
.hud-coins{display:flex;align-items:center;gap:7px}
.coin-glyph{width:22px;height:22px;flex:none;display:grid;place-items:center;border-radius:50%}
.coin-num{font-family:'SimplerPro',system-ui,sans-serif;font-weight:900;font-size:20px;line-height:1}
.hud-mid{display:flex;align-items:center;gap:8px;min-width:0}
.hud-live{display:none;align-items:center;gap:6px;font-size:10px;font-weight:800;letter-spacing:.16em;
  padding:4px 9px;line-height:1}
.live-dot{width:7px;height:7px;border-radius:50%;background:currentColor;flex:none}
.topic-chip{display:inline-flex;align-items:center;gap:6px;font-size:11.5px;font-weight:700;
  padding:4px 10px;line-height:1.25;white-space:nowrap}
.topic-mark{display:inline-flex;align-items:center;justify-content:center;width:15px;height:15px;flex:none}
.mark-emoji{font-size:12px;line-height:1}
.mark-svg{display:none;width:100%;height:100%;fill:none;stroke:currentColor;stroke-width:1.9;
  stroke-linejoin:round;stroke-linecap:round}
.px-mark{display:none}
.hud-progress{font-family:'SimplerPro',system-ui,sans-serif;font-weight:900;font-size:18px;line-height:1}

/* ---- the deck: hero card over a pile of backs ---- */
.deck{position:relative;z-index:1;flex:1;display:flex;align-items:center;justify-content:center;
  padding:30px 0 4px}
.pile{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;pointer-events:none}
.pile-card{position:absolute;width:340px;height:470px}
.pile-1{transform:translateY(-10px) rotate(-1.9deg)}
.pile-2{transform:translateY(-19px) rotate(3.1deg)}
.pile-3{transform:translateY(-28px) rotate(-4.8deg)}
.card{position:relative;z-index:2;width:340px;height:470px;display:flex;flex-direction:column;
  padding:22px 20px 18px}
.issue-title{margin-top:auto;font-family:'SimplerPro',system-ui,sans-serif;font-weight:900;
  font-size:38px;line-height:1.02}
.px-title{display:none}
.claim-text{font-size:15.5px;line-height:1.6;margin-top:16px}
.claim-echo{display:none}
.hints{margin-top:auto;display:flex;align-items:center;justify-content:space-between;gap:10px}
.hint{display:flex;align-items:center;gap:6px;font-size:12px;font-weight:800;line-height:1}
.hint-true{flex-direction:row-reverse}
.hint-arrow{width:17px;height:17px;flex:none;fill:none;stroke:currentColor;stroke-width:2.4;
  stroke-linecap:round;stroke-linejoin:round}
.hint-false .hint-arrow{transform:scaleX(-1)}
.source{display:flex;align-items:center;gap:7px;font-size:12.5px;line-height:1.3;margin-top:14px}
.ico-link{width:14px;height:14px;flex:none;stroke:currentColor;fill:none;stroke-width:2;stroke-linecap:round}

/* ---- answer buttons ---- */
.answers{position:relative;z-index:3;flex:none;display:flex;gap:12px;margin-top:18px}
.ans{position:relative;flex:1;min-height:56px;appearance:none;cursor:pointer;border:0;background:none;
  color:inherit;font-family:'SimplerPro',system-ui,sans-serif;font-weight:900;font-size:22px;
  line-height:1;padding:16px 8px;display:grid;place-items:center}
.ans:focus-visible{outline:3px solid #0052ff;outline-offset:3px}
.px-ans{display:none}

@media (prefers-reduced-motion: reduce){*{animation:none !important;transition:none !important}}
"""

BODY = """<div class="stage %LANE%">
  <header class="caption" dir="rtl" lang="he">
    <span class="cap-num">%NUM%</span>
    <span class="cap-he">%HE%</span>
    <span class="cap-en" dir="ltr">%EN%</span>
    <span class="cap-font">טקסט: פונט זמני</span>
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
          <span class="topic-mark" aria-hidden="true"><span class="mark-emoji">🕍</span><svg class="mark-svg" viewBox="0 0 24 24"><path d="M3.5 11h17v10.5h-17z"></path><path d="M7 11V7h10v4"></path><path d="M9.5 2.8h5V7h-5z"></path></svg><canvas class="px-mark" width="13" height="13"></canvas></span>
          <span class="topic-label">%TOPIC%</span>
        </span>
      </div>
      <div class="hud-progress">%PROG%</div>
    </header>

    <div class="deck">
      <div class="pile" aria-hidden="true">
        <div class="pile-card pile-3"></div>
        <div class="pile-card pile-2"></div>
        <div class="pile-card pile-1"></div>
      </div>
      <article class="card claim">
        <h2 class="issue-title"><canvas class="px-title" width="140" height="26"></canvas><span class="title-text">%TITLE%</span></h2>
        <p class="claim-text">%CLAIM%</p>
        <p class="claim-echo" aria-hidden="true">%CLAIM%</p>
        <div class="hints" aria-hidden="true">
          <span class="hint hint-true"><span class="hint-word">%ANS_T%</span><svg class="hint-arrow" viewBox="0 0 24 24"><path d="M4 12h15M13 6l6 6-6 6"></path></svg></span>
          <span class="hint hint-false"><span class="hint-word">%ANS_F%</span><svg class="hint-arrow" viewBox="0 0 24 24"><path d="M4 12h15M13 6l6 6-6 6"></path></svg></span>
        </div>
        <p class="source"><svg class="ico-link" viewBox="0 0 24 24" aria-hidden="true"><path d="M10.5 13.5a5 5 0 0 0 7.3.4l2.7-2.7a5 5 0 0 0-7-7l-1.5 1.4"></path><path d="M13.5 10.5a5 5 0 0 0-7.3-.4l-2.7 2.7a5 5 0 0 0 7 7l1.4-1.4"></path></svg><span class="source-name">%SOURCE%</span></p>
      </article>
    </div>

    <div class="answers">
      <button type="button" class="ans ans-true"><canvas class="px-ans" width="46" height="15"></canvas><span class="ans-text">%ANS_T%</span></button>
      <button type="button" class="ans ans-false"><canvas class="px-ans" width="46" height="15"></canvas><span class="ans-text">%ANS_F%</span></button>
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
%LOGIC%
</script>
</body>
</html>
"""

LOGIC_STATIC = "class Component extends DCLogic {\n  renderVals() { return {}; }\n}"

# =========================================================================
LANES = []

# ---------------------------------------------------------------- lane 1
LANES.append(dict(
  n=1, file="Main.dc.html", cls="lane1",
  he="אולפן שידור", en="Stream Overlay",
  tokens="""<!--
  LANE 1 · Stream Overlay
  palette   : base #070D1A · panel #0D1830 · live cyan #37E0FF · rail #16D0EE · gold accent #D4A94E (coin only)
  type      : SimplerPro Black in white; scoreboard tabular numerals; 10px tracked caps for HUD labels
  texture   : one — the AR perspective floor grid, cyan, receding under the deck
  signature : the card as a floating glass panel with a live cyan edge above that grid
-->""",
  css="""/* LANE 1 · Stream Overlay
   palette   : base #070D1A · panel #0D1830 · live cyan #37E0FF · rail #16D0EE · gold #D4A94E (coin only)
   type      : SimplerPro Black white; scoreboard tabular numerals; 10px tracked caps for HUD
   texture   : one — the AR perspective floor grid receding under the deck
   signature : the card as a floating glass panel with a live cyan edge above that grid */
.lane1 .frame{background:#070D1A;color:#E6F4FF}
.lane1 .frame-bg{background:
  radial-gradient(120% 46% at 50% 104%,rgba(55,224,255,.26),transparent 66%),
  linear-gradient(180deg,#070D1A 0%,#091428 62%,#06111F 100%)}
.lane1 .deco .deco-floor{display:block;fill:none;stroke:#37E0FF;stroke-width:1;opacity:.4}
/* HUD: live badge, ticker tag, scoreboard count */
.lane1 .hud-live{display:inline-flex;color:#37E0FF;background:rgba(55,224,255,.1);
  border:1px solid rgba(55,224,255,.5);border-radius:2px}
.lane1 .live-dot{animation:l1live 2s ease-in-out infinite;box-shadow:0 0 8px #37E0FF}
@keyframes l1live{0%,100%{opacity:1}50%{opacity:.3}}
.lane1 .topic-mark{display:none}
.lane1 .topic-chip{background:rgba(13,24,48,.9);border:1px solid rgba(55,224,255,.4);color:#B7E8FA;
  border-radius:2px;letter-spacing:.05em;padding-inline-start:8px}
.lane1 .topic-chip::before{content:"";width:3px;height:13px;background:#37E0FF;flex:none;
  box-shadow:0 0 8px #37E0FF}
.lane1 .coin-glyph{background:radial-gradient(circle at 34% 30%,#E9CE93,#D4A94E 62%,#9C7830)}
.lane1 .coin-num{color:#fff;font-size:22px;text-shadow:0 0 14px rgba(55,224,255,.55)}
.lane1 .hud-progress{color:#7FB4D4;letter-spacing:.02em}
/* the pile: dimmer glass panels behind */
.lane1 .pile-card{background:linear-gradient(180deg,rgba(19,40,76,.9),rgba(8,19,42,.75));
  border:1px solid rgba(55,224,255,.34);border-radius:3px;box-shadow:0 0 20px rgba(55,224,255,.16)}
/* signature: the floating glass panel */
.lane1 .card{background:linear-gradient(180deg,rgba(20,42,80,.82),rgba(9,20,44,.7));
  border:1px solid rgba(120,224,255,.55);border-radius:3px;backdrop-filter:blur(4px);
  box-shadow:0 0 40px rgba(55,224,255,.22),0 24px 40px rgba(0,0,0,.6),
             inset 0 1px 0 rgba(255,255,255,.22)}
.lane1 .card::before{content:"";position:absolute;top:-1px;left:14px;right:14px;height:2px;
  background:linear-gradient(90deg,transparent,#37E0FF,transparent);box-shadow:0 0 12px #37E0FF}
.lane1 .issue-title{color:#fff;letter-spacing:-.015em;text-shadow:0 0 26px rgba(55,224,255,.55)}
.lane1 .claim-text{color:#CFE6F7}
.lane1 .hint{color:#37E0FF;letter-spacing:.08em}
.lane1 .hint-true{text-shadow:0 0 10px rgba(55,224,255,.7)}
.lane1 .hint-false{text-shadow:0 0 10px rgba(55,224,255,.7)}
.lane1 .source{color:#87B6D6;border-top:1px solid rgba(120,224,255,.2);padding-top:11px;letter-spacing:.03em}
.lane1 .ans{background:linear-gradient(180deg,rgba(20,44,84,.9),rgba(9,22,46,.85));
  border:1px solid rgba(120,224,255,.6);border-radius:3px;color:#EAF8FF;letter-spacing:.04em;
  box-shadow:inset 0 1px 0 rgba(255,255,255,.2),0 0 20px rgba(55,224,255,.18),0 4px 0 rgba(15,80,110,.9)}
.lane1 .ans:focus-visible{outline:3px solid #37E0FF;outline-offset:3px}"""))

# ---------------------------------------------------------------- lane 2
LANES.append(dict(
  n=2, file="StateMedal.dc.html", cls="lane2",
  he="מהדורה מוגבלת", en="Collector's Drop",
  tokens="""<!--
  LANE 2 · Collector's Drop
  palette   : ink #16130F · off-white #F4F1E8 · bronze #8C6A3F · light bronze #C9A56E · velvet #27408B
  type      : SimplerPro Black big and tight; 10px tracked caps reserved for micro-labels only
  texture   : one — struck metal, built from layered inset shadows; no wood, no parchment
  signature : the struck medal — HUD coin and the debossed title are the same object language
-->""",
  css="""/* LANE 2 · Collector's Drop
   palette   : ink #16130F · off-white #F4F1E8 · bronze #8C6A3F · light bronze #C9A56E · velvet #27408B
   type      : SimplerPro Black big and tight; tracked caps only on micro-labels
   texture   : one — struck metal from layered inset shadows (no wood, no parchment)
   signature : the struck medal — HUD coin and debossed title are one object language */
.lane2 .frame{background:#16130F;color:#1E1B16}
.lane2 .frame-bg{background:
  radial-gradient(90% 42% at 50% 6%,rgba(201,165,110,.16),transparent 68%),
  linear-gradient(180deg,#16130F,#100E0B)}
/* the medal, twice: HUD coin and the card's one debossed element */
.lane2 .coin-glyph{width:24px;height:24px;
  background:radial-gradient(circle at 33% 27%,#E3C48F,#C9A56E 42%,#8C6A3F 72%,#5F4227);
  box-shadow:inset 0 2px 2px rgba(255,255,255,.6),inset 0 -3px 4px rgba(0,0,0,.55),
             0 2px 0 rgba(0,0,0,.6),0 0 0 1px rgba(201,165,110,.5)}
.lane2 .coin-glyph::after{content:"";width:9px;height:9px;border-radius:50%;
  box-shadow:inset 0 1px 1px rgba(0,0,0,.6),0 1px 0 rgba(255,255,255,.4)}
.lane2 .coin-num{color:#F4F1E8;font-size:21px}
.lane2 .hud-progress{color:#C9A56E}
.lane2 .mark-emoji{display:none}
.lane2 .mark-svg{display:block;color:#C9A56E;filter:drop-shadow(0 1px 0 rgba(0,0,0,.8))}
.lane2 .topic-chip{color:#C9A56E;letter-spacing:.2em;font-size:10px;text-transform:none;
  border:1px solid rgba(201,165,110,.4);border-radius:0;padding:5px 10px}
/* velvet survives only here */
.lane2 .pile-card{background:linear-gradient(180deg,#2E4A99,#27408B 55%,#1C2F68);border-radius:3px;
  box-shadow:inset 0 0 26px rgba(0,0,0,.5),0 2px 0 rgba(0,0,0,.5)}
.lane2 .card{background:#F4F1E8;border-radius:3px;
  box-shadow:0 22px 38px rgba(0,0,0,.55),inset 0 1px 0 rgba(255,255,255,.9),
             inset 0 0 0 1px rgba(140,106,63,.28)}
.lane2 .issue-title{font-size:52px;letter-spacing:-.03em;line-height:.96;color:#26211A;
  text-shadow:0 1px 0 rgba(255,255,255,.95),0 -1px 0 rgba(93,72,42,.45)}
.lane2 .claim-text{color:#2B2721;margin-top:22px}
.lane2 .hint{color:#6E5433;letter-spacing:.18em;font-size:10.5px}
.lane2 .source{color:#6E5433;letter-spacing:.14em;font-size:10.5px;font-weight:700;
  border-top:1px solid rgba(140,106,63,.3);padding-top:12px}
.lane2 .ans{background:linear-gradient(180deg,#FBF9F3,#E3DDCC);color:#1E1B16;border-radius:3px;
  letter-spacing:.06em;
  box-shadow:inset 0 2px 0 rgba(255,255,255,1),inset 0 -2px 0 rgba(140,106,63,.35),
             inset 0 0 0 1px rgba(140,106,63,.55),0 4px 0 #8C6A3F,0 8px 14px rgba(0,0,0,.45)}
.lane2 .ans:focus-visible{outline:3px solid #C9A56E;outline-offset:3px}"""))

# ---------------------------------------------------------------- lane 3
MOTIF = ("url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='38' height='38' "
         "viewBox='0 0 38 38'%3E%3Cg fill='none' stroke='%234F5BFF' stroke-width='1.7' "
         "stroke-linejoin='round'%3E%3Crect x='10' y='16' width='18' height='12'/%3E%3Cpath "
         "d='M13.5 16v-5h11v5'/%3E%3Crect x='17' y='6' width='4.5' height='5.5'/%3E%3C/g%3E%3C/svg%3E\")")

LANES.append(dict(
  n=3, file="Linocut.dc.html", cls="lane3",
  he="לינוקאט אזרחי", en="Linocut Civic Revival",
  tokens="""<!--
  LANE 3 · Linocut Civic Revival
  palette   : ink-blue #4F5BFF · ochre #D9962E · cream #F2E9D8 · ink-black #141414
  type      : SimplerPro Black stacked tight, poster lettering, flat ink fills only
  texture   : one — feTurbulence displacement, on every printed edge (card, buttons, stamps)
  signature : ink-block buttons with a misregistered ochre pull behind them
-->""",
  css="""/* LANE 3 · Linocut Civic Revival
   palette   : ink-blue #4F5BFF · ochre #D9962E · cream #F2E9D8 · ink-black #141414
   type      : SimplerPro Black stacked tight, poster lettering, flat ink fills only
   texture   : one — feTurbulence displacement on every printed edge (card, buttons, stamps)
   signature : ink-block buttons with a misregistered ochre pull behind them */
.lane3 .frame{background:#F2E9D8;color:#141414}
.lane3 .frame-bg{background:#F2E9D8}
.lane3 .coin-glyph{background:#D9962E;box-shadow:inset 0 0 0 2.5px #141414}
.lane3 .coin-num{color:#141414}
.lane3 .hud-progress{color:#4F5BFF}
.lane3 .mark-emoji{display:none}
.lane3 .mark-svg{display:block;color:#141414;stroke-width:2.1}
.lane3 .topic-chip{color:#141414;font-weight:900;letter-spacing:.02em;padding:4px 0}
/* pile: cream stock, one-colour repeated ballot motif */
.lane3 .pile-card{background:#F2E9D8 %MOTIF%;background-size:38px 38px;
  box-shadow:inset 0 0 0 3px #141414;filter:url(#rough)}
.lane3 .card{background:none}
.lane3 .card::before{content:"";position:absolute;inset:0;z-index:-1;background:#fff;
  box-shadow:inset 0 0 0 3px #141414;filter:url(#rough)}
.lane3 .issue-title{color:#4F5BFF;font-size:56px;line-height:.85;letter-spacing:-.03em}
.lane3 .claim-text{font-weight:600;margin-top:20px}
/* stamp grammar carried into the swipe hints */
.lane3 .hint{position:relative;color:#141414;font-weight:900;letter-spacing:.02em;padding:7px 11px;
  isolation:isolate}
.lane3 .hint::before{content:"";position:absolute;inset:0;z-index:-1;background:#D9962E;
  box-shadow:inset 0 0 0 3px #141414;filter:url(#rough);mix-blend-mode:multiply}
.lane3 .hint-true{rotate:-4deg}
.lane3 .hint-false{rotate:4deg}
.lane3 .source{color:#141414;font-weight:700;border-top:3px solid #141414;padding-top:11px;margin-top:16px}
/* signature: ink-block print buttons, misregistered second pull */
.lane3 .ans{background:none;color:#F2E9D8;isolation:isolate;letter-spacing:.03em}
.lane3 .ans::before{content:"";position:absolute;inset:0;z-index:-1;background:#4F5BFF;filter:url(#rough)}
.lane3 .ans::after{content:"";position:absolute;inset:0;z-index:-2;translate:5px 5px;background:#D9962E;
  filter:url(#rough);mix-blend-mode:multiply}
.lane3 .ans:focus-visible{outline:3px solid #141414;outline-offset:5px}""".replace("%MOTIF%", MOTIF)))

# ---------------------------------------------------------------- lane 4
LANES.append(dict(
  n=4, file="Stickers.dc.html", cls="lane4",
  he="תרבות סטיקרים", en="Israeli Sticker Culture",
  tokens="""<!--
  LANE 4 · Israeli Sticker Culture
  palette   : yellow #FFD60A · hot-pink #FF3B6B · teal #2EC4B6 · black #000 · pole-grey #B9B7B0
  type      : SimplerPro Black in slogan chunks; every chunk sits on its own die-cut
  texture   : one — the street pole: grain over pale torn remnants of older stickers
  signature : the claim card as the newest, biggest sticker, one corner peeling
-->""",
  css="""/* LANE 4 · Israeli Sticker Culture
   palette   : yellow #FFD60A · hot-pink #FF3B6B · teal #2EC4B6 · black #000 · pole-grey #B9B7B0
   type      : SimplerPro Black slogan chunks; every chunk on its own die-cut
   texture   : one — the street pole: grain over pale torn remnants of older stickers
   signature : the claim card as the newest, biggest sticker, one corner peeling */
.lane4 .frame{background:#B9B7B0;color:#000}
.lane4 .frame-bg{background:#B9B7B0}
.lane4 .frame-bg::after{content:"";position:absolute;inset:0;opacity:.5;
  background-image:radial-gradient(rgba(0,0,0,.55) .5px,transparent .5px),
    radial-gradient(rgba(255,255,255,.65) .5px,transparent .5px);
  background-size:3px 3px,5px 5px;background-position:0 0,2px 1px}
.lane4 .deco .deco-ghosts{display:block;fill:#CFCDC6;stroke:#fff;stroke-width:3;opacity:.55}
.lane4 .coin-glyph{background:#2EC4B6;border:3px solid #fff;box-shadow:0 2px 0 rgba(0,0,0,.45);
  rotate:-8deg}
.lane4 .coin-num{color:#000}
.lane4 .hud-progress{background:#FFD60A;border:3px solid #fff;padding:3px 9px;rotate:3deg;
  box-shadow:0 2px 0 rgba(0,0,0,.45);font-size:15px}
.lane4 .topic-chip{background:#FF3B6B;color:#000;border:3px solid #fff;border-radius:999px;rotate:-2.5deg;
  box-shadow:0 2px 0 rgba(0,0,0,.45);font-weight:900}
.lane4 .pile-1{background:#FFD60A;border:5px solid #fff;box-shadow:0 4px 0 rgba(0,0,0,.4)}
.lane4 .pile-2{background:#2EC4B6;border:5px solid #fff;box-shadow:0 4px 0 rgba(0,0,0,.4)}
.lane4 .pile-3{background:#FF3B6B;border:5px solid #fff;box-shadow:0 4px 0 rgba(0,0,0,.4)}
/* signature: the newest sticker, peeling at one corner */
.lane4 .card{background:#fff;border:7px solid #fff;rotate:-1.4deg;
  box-shadow:0 7px 0 rgba(0,0,0,.42),0 16px 26px rgba(0,0,0,.28)}
.lane4 .card::after{content:"";position:absolute;left:-7px;bottom:-7px;width:40px;height:40px;
  background:linear-gradient(45deg,#EFEDE7 0 52%,#fff 52%);
  clip-path:polygon(0 100%,100% 100%,0 0);
  box-shadow:5px -5px 9px rgba(0,0,0,.24)}
.lane4 .issue-title{background:#FFD60A;border:5px solid #fff;padding:8px 15px 10px;rotate:1.6deg;
  align-self:flex-start;font-size:40px;box-shadow:0 4px 0 rgba(0,0,0,.45)}
.lane4 .claim-text{font-weight:700;margin-top:22px}
/* half-peeled arrow stickers */
.lane4 .hint{background:#2EC4B6;color:#000;border:4px solid #fff;border-radius:10px;padding:7px 11px;
  font-weight:900;box-shadow:0 3px 0 rgba(0,0,0,.42)}
.lane4 .hint-true{rotate:-6deg}
.lane4 .hint-false{rotate:6deg;background:#FF3B6B}
.lane4 .source{background:#fff;border:4px solid #fff;padding:5px 11px;rotate:-1.6deg;font-weight:800;
  align-self:flex-start;box-shadow:0 3px 0 rgba(0,0,0,.4);margin-top:16px}
.lane4 .ans{border:5px solid #fff;border-radius:16px;box-shadow:0 5px 0 rgba(0,0,0,.48);font-size:24px}
.lane4 .ans-true{background:#FFD60A;color:#000;rotate:-2.2deg}
.lane4 .ans-false{background:#FF3B6B;color:#000;rotate:2.2deg}
.lane4 .ans:focus-visible{outline:4px solid #000;outline-offset:4px}"""))

# ---------------------------------------------------------------- lane 5
LANES.append(dict(
  n=5, file="AcidType.dc.html", cls="lane5",
  he="טיפוגרפי חומצי", en="Acid Typographic",
  tokens="""<!--
  LANE 5 · Acid Typographic
  palette   : acid field #3ECF6E · card acid #4BD97A · black #0A0A0A · white · accent #FF7A00 (coin only)
  type      : the title gigantic and cropped; the claim a strict block at reading size; nothing else
  texture   : one — the title echoed once behind itself at 6% black
  signature : the scale-crop of «חוק הגיוס» running off both card edges
-->""",
  css="""/* LANE 5 · Acid Typographic
   palette   : acid field #3ECF6E · card #4BD97A · black #0A0A0A · white · accent #FF7A00 (coin only)
   type      : title gigantic and cropped; claim a strict block at reading size; nothing else
   texture   : one — the title echoed once behind itself at 6% black
   signature : the scale-crop of «חוק הגיוס» running off both card edges */
.lane5 .frame{background:#3ECF6E;color:#0A0A0A}
.lane5 .frame-bg{background:#3ECF6E}
.lane5 .coin-glyph{background:#FF7A00;border-radius:0}
.lane5 .coin-num{color:#0A0A0A;font-size:21px}
.lane5 .hud-progress{color:#0A0A0A}
.lane5 .topic-mark{display:none}
.lane5 .topic-chip{color:#0A0A0A;font-weight:800;letter-spacing:.2em;font-size:10.5px;padding:4px 0}
.lane5 .pile-card{background:#0A0A0A}
.lane5 .card{background:#4BD97A;box-shadow:inset 0 0 0 3px #0A0A0A,0 16px 0 -6px rgba(10,10,10,.22);
  overflow:hidden;padding:18px 20px 18px}
/* signature: the crop */
.lane5 .issue-title{position:relative;z-index:2;font-size:86px;line-height:.86;letter-spacing:-.045em;
  margin:auto -26px 0;white-space:nowrap;text-align:center}
.lane5 .claim-echo{display:block;position:absolute;z-index:0;top:6px;left:-40px;right:-40px;
  font-family:'SimplerPro',system-ui,sans-serif;font-weight:900;font-size:44px;line-height:.92;
  color:rgba(10,10,10,.05);pointer-events:none;user-select:none}
.lane5 .claim-text{position:relative;z-index:2;font-size:16px;line-height:1.5;font-weight:700;
  margin-top:24px;border-top:3px solid #0A0A0A;border-bottom:3px solid #0A0A0A;padding:14px 0}
.lane5 .hints{position:relative;z-index:2}
.lane5 .hint{color:#0A0A0A;font-weight:900;letter-spacing:.16em;font-size:11px}
.lane5 .source{position:relative;z-index:2;color:#0A0A0A;font-weight:800;letter-spacing:.06em;margin-top:16px}
.lane5 .ans{background:#0A0A0A;color:#fff;letter-spacing:.05em;box-shadow:0 5px 0 rgba(10,10,10,.35)}
.lane5 .ans:focus-visible{outline:3px solid #0A0A0A;outline-offset:4px}"""))

# ---------------------------------------------------------------- lane 6
LANES.append(dict(
  n=6, file="PapersPlease.dc.html", cls="lane6",
  he="ניירת, בבקשה", en="Papers, Please × Reigns",
  tokens="""<!--
  LANE 6 · Papers, Please × Reigns
  palette   : desk #2B2626 · paper #A39A8A · manila #B8A97E · khaki #6E6A54 · off-white #D8D2C4
  type      : SimplerPro Black rasterised to <canvas> at 12px, upscaled 2x nearest-neighbour
  texture   : one — a 4px pixel checker over the desk; hard rules on the document, zero radii
  signature : every display string is pixel type — title, both buttons, the topic marker
-->""",
  css="""/* LANE 6 · Papers, Please x Reigns
   palette   : desk #2B2626 · paper #A39A8A · manila #B8A97E · khaki #6E6A54 · off-white #D8D2C4
   type      : SimplerPro Black rasterised to <canvas> at 12px, upscaled 2x nearest-neighbour
   texture   : one — 4px pixel checker over the desk; hard document rules, zero radii
   signature : every display string is pixel type — title, both buttons, the topic marker */
.lane6 .frame{background:#2B2626;color:#2B2626}
.lane6 .frame-bg{background:#2B2626}
.lane6 .frame-bg::after{content:"";position:absolute;inset:0;opacity:.5;
  background-image:repeating-conic-gradient(rgba(255,255,255,.05) 0 25%,transparent 0 50%);
  background-size:4px 4px}
.lane6 .coin-glyph{background:#6E6A54;border-radius:0;box-shadow:inset 0 0 0 2px #2B2626}
.lane6 .coin-num{color:#D8D2C4}
.lane6 .hud-progress{color:#A39A8A}
.lane6 .mark-emoji{display:none}
.lane6 .px-mark{display:block;image-rendering:pixelated;width:26px;height:26px}
.lane6 .topic-mark{width:26px;height:26px}
.lane6 .topic-chip{background:#6E6A54;color:#D8D2C4;border-radius:0;letter-spacing:.14em;font-size:10px;
  padding:3px 9px;gap:7px}
/* pile: manila folders, tabs showing */
.lane6 .pile-card{background:#B8A97E;border-radius:0;box-shadow:inset 0 0 0 1px #8A7C55,0 2px 0 rgba(0,0,0,.5)}
.lane6 .pile-card::before{content:"";position:absolute;top:-13px;width:96px;height:14px;background:#B8A97E;
  box-shadow:inset 0 0 0 1px #8A7C55}
.lane6 .pile-1::before{right:26px}
.lane6 .pile-2::before{right:132px}
.lane6 .pile-3::before{right:230px}
.lane6 .card{background:#A39A8A;border-radius:0;
  box-shadow:inset 0 0 0 1px #8A8171,0 4px 0 rgba(0,0,0,.55),0 18px 26px rgba(0,0,0,.45)}
.lane6 .px-title{display:block;image-rendering:pixelated;width:280px;height:52px}
.lane6 .title-text{display:none}
.lane6 .issue-title{line-height:1;border-bottom:2px solid #7A7264;padding-bottom:12px}
.lane6 .claim-text{color:#2B2626;font-size:14.5px;line-height:1.55;margin-top:18px}
.lane6 .hint{background:#6E6A54;color:#D8D2C4;padding:6px 10px;letter-spacing:.12em;font-size:10.5px;
  box-shadow:inset 0 0 0 1px #2B2626}
.lane6 .source{color:#3A342B;font-weight:700;letter-spacing:.06em;font-size:11.5px;
  border-top:1px dashed #7A7264;padding-top:11px;margin-top:16px}
.lane6 .px-ans{display:block;image-rendering:pixelated;width:138px;height:45px}
.lane6 .ans-text{display:none}
.lane6 .ans{background:#D8D2C4;border-radius:0;
  box-shadow:inset 0 0 0 2px #2B2626,4px 4px 0 rgba(0,0,0,.5)}
.lane6 .ans:focus-visible{outline:3px solid #D8D2C4;outline-offset:4px}"""))

# ---------------------------------------------------------------- lane 7
LANES.append(dict(
  n=7, file="StateKitsch.dc.html", cls="lane7",
  he="קיטש ממלכתי אפי", en="Epic State Kitsch",
  tokens="""<!--
  LANE 7 · Epic State Kitsch
  palette   : gold #F5C542 · deep gold #C9932B · sky #7EB8E6 · cloud cream #FFF4DC · label brown #5C4008
  type      : SimplerPro Black bevelled by stacked text-shadows; body dark brown on cream
  texture   : one — the cloud bank, painted into the background layer and never above content
  signature : the אמת/שקר buttons as radiant golden tablets over a solid gold Knesset band
-->""",
  css="""/* LANE 7 · Epic State Kitsch
   palette   : gold #F5C542 · deep gold #C9932B · sky #7EB8E6 · cloud cream #FFF4DC · label #5C4008
   type      : SimplerPro Black bevelled by stacked text-shadows; body dark brown on cream
   texture   : one — the cloud bank, painted in the background layer, never above content
   signature : the אמת/שקר buttons as radiant golden tablets over a solid gold Knesset band */
.lane7 .frame{background:#7EB8E6;color:#4A3A12}
.lane7 .frame-bg{background:
  radial-gradient(52px 34px at 14% 20%,rgba(255,255,255,.92),transparent 72%),
  radial-gradient(66px 40px at 84% 13%,rgba(255,255,255,.85),transparent 72%),
  radial-gradient(78px 44px at 22% 47%,rgba(255,255,255,.7),transparent 74%),
  radial-gradient(86px 48px at 90% 55%,rgba(255,255,255,.62),transparent 74%),
  radial-gradient(150% 40% at 50% 100%,rgba(245,197,66,.6),transparent 66%),
  linear-gradient(180deg,#5FA2D8,#7EB8E6 46%,#BFD9F0 100%)}
.lane7 .deco .deco-knesset{display:block;fill:#A87A1E}
.lane7 .sparkles{display:block;position:absolute;inset:0;z-index:2;pointer-events:none;font-size:0}
.lane7 .sparkles>i,.lane7 .sparkles>b{position:absolute;font-style:normal;font-weight:400}
.lane7 .sparkles>i{top:62px;left:28px;font-size:17px;animation:l7tw 3.4s ease-in-out infinite .8s}
.lane7 .sparkles>b{top:150px;right:22px;font-size:21px;animation:l7tw 3.9s ease-in-out infinite 1.6s}
.lane7 .sparkles::after{content:"✨";position:absolute;top:612px;left:24px;font-size:19px;
  animation:l7tw 4.4s ease-in-out infinite}
@keyframes l7tw{0%,100%{opacity:.55;scale:.9}50%{opacity:1;scale:1.12}}
.lane7 .coin-glyph{width:24px;height:24px;
  background:radial-gradient(circle at 33% 27%,#FFF3C8,#F5C542 52%,#C9932B);
  border:2px solid #A87A1E;box-shadow:0 0 14px rgba(245,197,66,.9),inset 0 2px 0 rgba(255,255,255,.85)}
.lane7 .coin-glyph::after{content:"";width:9px;height:9px;border-radius:50%;
  box-shadow:inset 0 1px 1px rgba(138,99,26,.8),0 1px 0 rgba(255,255,255,.7)}
.lane7 .coin-num{color:#FFF3C8;text-shadow:0 1px 0 #C9932B,0 2px 0 #A87A1E,0 3px 5px rgba(74,58,18,.5)}
.lane7 .hud-progress{color:#FFF3C8;text-shadow:0 1px 0 #C9932B,0 2px 4px rgba(74,58,18,.5)}
.lane7 .topic-chip{background:linear-gradient(180deg,#FFF4DC,#FFE9A8);color:#5C4008;border-radius:999px;
  border:1px solid #C9932B;box-shadow:inset 0 1px 0 rgba(255,255,255,.9)}
.lane7 .pile-card{background:linear-gradient(180deg,#FFF9E9,#FFE9BE);border-radius:20px;
  border:2px solid #E7BE6A;box-shadow:0 8px 20px rgba(74,58,18,.3)}
.lane7 .card{background:linear-gradient(180deg,#FFFBF0,#FFEFD2);border-radius:22px;border:2px solid #E7BE6A;
  box-shadow:0 0 0 4px rgba(255,255,255,.6),0 18px 34px rgba(74,58,18,.35),inset 0 2px 0 rgba(255,255,255,.95)}
.lane7 .issue-title{background:linear-gradient(180deg,#59A0D8,#8CC3EB);margin:auto -20px 0;
  padding:20px 20px 22px;border-radius:20px 20px 0 0;box-shadow:inset 0 -3px 0 rgba(255,255,255,.5);
  color:#FFE9A8;font-size:44px;letter-spacing:.005em;
  text-shadow:0 1px 0 #F5C542,0 2px 0 #D9A233,0 3px 0 #C9932B,0 4px 0 #A87A1E,0 6px 10px rgba(74,58,18,.5)}
.lane7 .claim-text{color:#4A3A12;font-weight:600;margin-top:20px;padding:0 0 4px}
.lane7 .hint{color:#8A631A;font-weight:800}
.lane7 .source{color:#5C4A1E;font-weight:700;border-top:1px solid #E7BE6A;padding-top:11px;margin-top:16px}
/* signature: radiant golden tablets */
.lane7 .ans{background:linear-gradient(180deg,#FFF3C8,#F5C542 46%,#C9932B);color:#5C4008;
  border:2px solid #A87A1E;border-radius:20px 20px 26px 26px;letter-spacing:.02em;font-size:23px;
  text-shadow:0 1px 0 rgba(255,255,255,.9);
  box-shadow:0 0 26px rgba(245,197,66,.85),inset 0 2px 0 rgba(255,255,255,.95),
             inset 0 -5px 7px rgba(120,84,14,.3),0 5px 0 #8A631A}
.lane7 .ans:focus-visible{outline:3px solid #5C4008;outline-offset:4px}"""))

# ---------------------------------------------------------------- lane 8
LANES.append(dict(
  n=8, file="Editorial.dc.html", cls="lane8",
  he="עיתונאי מודרני", en="Modern Editorial / Tile-Clean",
  tokens="""<!--
  LANE 8 · Modern Editorial / Tile-Clean
  palette   : paper #FAFAF7 · ink #1A1A1A · rule #DDD9D0 · miss #787C7E · surprise amber #C9A227
  type      : one display size, one body size, generous leading; small caps for every micro-label
  texture   : none — whitespace, a strict grid and hairlines carry the page
  signature : the pile as a stack of paper sheets, and two neutral pre-flip Wordle tiles for the swipe
-->""",
  css="""/* LANE 8 · Modern Editorial / Tile-Clean
   palette   : paper #FAFAF7 · ink #1A1A1A · rule #DDD9D0 · miss #787C7E · surprise amber #C9A227
   type      : one display size, one body size, generous leading, small caps for micro-labels
   texture   : none — whitespace, a strict grid and hairlines carry the page
   signature : the pile as a stack of paper sheets; two neutral pre-flip tiles for the swipe */
.lane8 .frame{background:#EFEEE9;color:#1A1A1A;padding:14px 20px 26px}
.lane8 .frame-bg{background:#EFEEE9}
.lane8 .coin-glyph{background:#FAFAF7;box-shadow:inset 0 0 0 1.5px #1A1A1A}
.lane8 .coin-num{color:#1A1A1A}
.lane8 .hud-progress{color:#5C5C58}
.lane8 .topic-mark{display:none}
.lane8 .topic-chip{color:#5C5C58;font-size:10.5px;font-weight:700;letter-spacing:.19em;
  border:1px solid #D6D2C9;border-radius:999px;padding:5px 13px}
/* signature part 1: a stack of paper sheets */
.lane8 .pile-card{background:#FAFAF7;border-radius:2px;
  box-shadow:0 0 0 1px #D3CFC5,0 3px 8px rgba(0,0,0,.1)}
.lane8 .card{background:#FAFAF7;border-radius:2px;padding:26px 24px 20px;
  box-shadow:0 0 0 1px #DDD9D0,0 10px 26px rgba(0,0,0,.13)}
.lane8 .issue-title{font-size:40px;letter-spacing:-.015em;line-height:1.06}
.lane8 .claim-text{font-size:16.5px;line-height:1.62;margin-top:22px}
/* signature part 2: neutral pre-flip tiles */
.lane8 .hint{background:#FAFAF7;border:2px solid #DDD9D0;border-radius:2px;padding:9px 13px;
  color:#5C5C58;font-size:12.5px;letter-spacing:.06em}
.lane8 .hint .hint-arrow{stroke:#787C7E}
.lane8 .source{margin-top:18px;padding-top:13px;border-top:1px solid #DDD9D0;font-size:14.5px;
  font-weight:700;color:#1A1A1A}
.lane8 .source .ico-link{width:15px;height:15px;color:#787C7E}
.lane8 .source-name{border-bottom:2px solid #C9A227;padding-bottom:1px}
.lane8 .ans{background:#FAFAF7;border:1.5px solid #1A1A1A;border-radius:2px;color:#1A1A1A;font-size:21px;
  letter-spacing:.02em;box-shadow:0 3px 0 #1A1A1A}
.lane8 .ans:focus-visible{outline:3px solid #C9A227;outline-offset:3px}"""))

# ---------------------------------------------------------------- lane 6 logic
LOGIC_L6 = r"""class Component extends DCLogic {
  componentDidMount() {
    this.paint();
    if (document.fonts && document.fonts.ready) { document.fonts.ready.then(() => this.paint()); }
    setTimeout(() => this.paint(), 500);
  }
  renderVals() { return {}; }
  // SimplerPro Black drawn small, then upscaled 2x nearest-neighbour by CSS
  px(cv, text, size, align) {
    const c = cv.getContext('2d');
    c.clearRect(0, 0, cv.width, cv.height);
    c.imageSmoothingEnabled = false;
    c.fillStyle = '#2B2626';
    c.font = '900 ' + size + 'px SimplerPro, system-ui, sans-serif';
    c.textBaseline = 'middle';
    c.textAlign = align;
    if ('direction' in c) { c.direction = 'rtl'; }
    c.fillText(text, align === 'right' ? cv.width - 2 : cv.width / 2, cv.height / 2 + 1);
  }
  paint() {
    const root = document.querySelector('.lane6');
    if (!root) return;
    const t = root.querySelector('.px-title');
    if (t) { this.px(t, 'חוק הגיוס', 17, 'right'); }
    const bt = root.querySelector('.ans-true .px-ans');
    if (bt) { this.px(bt, 'אמת', 11.5, 'center'); }
    const bf = root.querySelector('.ans-false .px-ans');
    if (bf) { this.px(bf, 'שקר', 11.5, 'center'); }
    const m = root.querySelector('.px-mark');
    if (m) {
      const c = m.getContext('2d');
      c.clearRect(0, 0, m.width, m.height);
      c.imageSmoothingEnabled = false;
      c.textBaseline = 'middle';
      c.textAlign = 'center';
      c.font = '11px system-ui, sans-serif';
      c.fillText('🕍', m.width / 2, m.height / 2 + 1);
    }
  }
}"""

# =========================================================================
def build():
    shared = SHARED.replace("%FONT%", FONT)
    for lane in LANES:
        body = (BODY
                .replace("%LANE%", lane["cls"]).replace("%NUM%", str(lane["n"]))
                .replace("%HE%", lane["he"]).replace("%EN%", lane["en"])
                .replace("%COINS%", COINS).replace("%PROG%", PROG).replace("%TOPIC%", TOPIC)
                .replace("%LIVE%", LIVE).replace("%TITLE%", TITLE).replace("%CLAIM%", CLAIM)
                .replace("%ANS_T%", ANS_T).replace("%ANS_F%", ANS_F).replace("%SOURCE%", SOURCE))
        page = (PAGE
                .replace("%TOKENS%", lane["tokens"]).replace("%SHARED%", shared)
                .replace("%LANECSS%", lane["css"]).replace("%BODY%", body)
                .replace("%LOGIC%", LOGIC_L6 if lane["n"] == 6 else LOGIC_STATIC))
        (OUT / lane["file"]).write_text(page, encoding="utf-8")

    manifest = {
        "artboards": [
            {"file": l["file"], "x": (len(LANES) - 1 - i) * 480, "y": 0, "w": 390, "h": 880,
             "title": "%d · %s · %s" % (l["n"], l["he"], l["en"])}
            for i, l in enumerate(LANES)
        ],
        "launch": {"view": "canvas"},
    }
    (OUT / "canvas.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    for l in LANES:
        print("%s  %6.1f KB" % (l["file"].ljust(22), (OUT / l["file"]).stat().st_size / 1024))

if __name__ == "__main__":
    build()
