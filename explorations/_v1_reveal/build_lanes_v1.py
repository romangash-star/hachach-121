# -*- coding: utf-8 -*-
"""Builds the 8 direction artboards for the visual-direction canvas.

One shared markup skeleton -> 8 .dc.html files. Only the lane class and the
lane CSS block differ, which is what the brief's "same markup structure in all
8 frames" contract asks for. Regenerate with:  python3 explorations/build_lanes.py
"""
import base64, json, os, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT  = ROOT / "explorations"
FONT = base64.b64encode((ROOT / "fonts" / "SimplerPro_HLAR-Black.woff2").read_bytes()).decode()

# ---- verbatim content, issue r1 of data.js -------------------------------
TOPIC   = "דת ומדינה 🕍"
TITLE   = "חוק הגיוס 🪖"
CLAIM   = "הצעת חוק הגיוס שהקואליציה קידמה ב-2024 מבוססת על מתווה שכתב... בני גנץ."
ANS_T   = "אמת"
ANS_F   = "שקר"
SOURCE  = "ישראל היום"
MK_NAME = "בני גנץ"
MK_PART = "המחנה הממלכתי"
GUESS   = "בעד"
ACTUAL  = "נגד"
NOTE    = "הצביע נגד המתווה שהוא עצמו כתב — כי לטענתו 7/10 שינה הכל"

SHARED = """
@font-face{font-family:'SimplerPro';src:url(data:font/woff2;base64,%FONT%) format('woff2');font-weight:900;font-style:normal;font-display:block}
*{margin:0;padding:0;box-sizing:border-box}
body{background:#9A9A97;font-family:system-ui,"Segoe UI",Arial,sans-serif;font-variant-numeric:tabular-nums;-webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility}
a{color:#1a3acc}
a:hover{color:#0f2894}

/* ---- caption strip: outside the frame, on the grey canvas ---- */
.stage{width:390px;background:#9A9A97;padding-bottom:26px}
.caption{display:flex;flex-wrap:wrap;align-items:baseline;gap:4px 9px;padding:16px 16px 12px;color:#141414}
.cap-num{font-family:'SimplerPro',system-ui,sans-serif;font-weight:900;font-size:27px;line-height:.9}
.cap-he{font-weight:700;font-size:15px;line-height:1.2}
.cap-en{font-size:11.5px;letter-spacing:.05em;text-transform:uppercase;color:#2A2A28}
.cap-font{flex-basis:100%;font-size:10.5px;color:#2A2A28}

/* ---- the frame ---- */
.frame{position:relative;width:390px;min-height:800px;overflow:hidden;isolation:isolate;
  display:flex;flex-direction:column;gap:14px;padding:18px 16px 22px;box-shadow:0 3px 14px rgba(0,0,0,.3)}
.frame-bg{position:absolute;inset:0;z-index:0;pointer-events:none}
.deco{position:absolute;left:0;right:0;bottom:0;height:0;overflow:hidden;z-index:0;pointer-events:none}
.deco g{display:none}
.sparkles{display:none}

/* ---- cards ---- */
.card{position:relative;z-index:1;display:flex;flex-direction:column;gap:12px;padding:16px}
.claim-head{display:flex;flex-direction:column;align-items:flex-start;gap:8px}
.chip-topic{display:inline-flex;align-items:center;font-size:12px;font-weight:700;padding:5px 11px;line-height:1.25}
.issue-title{font-family:'SimplerPro',system-ui,sans-serif;font-weight:900;font-size:31px;line-height:1.05}
.px-title{display:none}
.claim-text{font-size:15px;line-height:1.55}
.claim-echo{display:none}
.answers{display:flex;gap:10px}
.ans{flex:1;min-height:52px;appearance:none;cursor:pointer;border:0;background:none;color:inherit;
  font-family:'SimplerPro',system-ui,sans-serif;font-weight:900;font-size:21px;line-height:1;padding:14px 8px}
.ans:focus-visible{outline:3px solid #0052ff;outline-offset:3px}
.source{display:flex;align-items:center;gap:7px;font-size:12.5px;line-height:1.3}
.ico-link{width:14px;height:14px;flex:none;stroke:currentColor;fill:none;stroke-width:2;stroke-linecap:round}

/* ---- reveal ---- */
.mk{display:flex;align-items:center;gap:12px}
.portrait{position:relative;width:58px;height:58px;flex:none;display:grid;place-items:center;overflow:hidden}
.silhouette{position:relative;width:100%;height:100%;display:block}
.px-portrait{display:none}
.initials{display:none;font-family:'SimplerPro',system-ui,sans-serif;font-weight:900;font-size:23px;line-height:1}
.mk-id{display:flex;flex-direction:column;gap:3px;min-width:0}
.mk-name{font-family:'SimplerPro',system-ui,sans-serif;font-weight:900;font-size:21px;line-height:1.1}
.mk-party{font-size:12.5px;line-height:1.2}
.tiles{display:flex;align-items:stretch;gap:9px}
.tile{flex:1;display:flex;flex-direction:column;align-items:center;gap:5px;padding:11px 6px}
.tile-label{font-size:11px;line-height:1.2;letter-spacing:.02em}
.tile-val{font-family:'SimplerPro',system-ui,sans-serif;font-weight:900;font-size:23px;line-height:1}
.tile-arrow{align-self:center;font-size:19px;line-height:1;opacity:.8}
.verdict{display:flex;align-items:center;justify-content:center}
.verdict-mark{font-family:'SimplerPro',system-ui,sans-serif;font-weight:900;font-size:36px;line-height:1;display:block}
.note{font-size:13.5px;line-height:1.55}

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
    <svg class="deco" viewBox="0 0 390 200" preserveAspectRatio="xMidYMax slice">
      <defs>
        <filter id="rough" x="-8%" y="-8%" width="116%" height="116%">
          <feTurbulence type="fractalNoise" baseFrequency="0.04 0.07" numOctaves="3" seed="7" result="n"></feTurbulence>
          <feDisplacementMap in="SourceGraphic" in2="n" scale="6" xChannelSelector="R" yChannelSelector="G"></feDisplacementMap>
        </filter>
      </defs>
      <g class="deco-floor">
        <path d="M0 108H390"></path>
        <path d="M195 108-70 200M195 108 55 200M195 108 140 200M195 108 250 200M195 108 335 200M195 108 460 200"></path>
        <path d="M0 130H390M0 158H390M0 200H390"></path>
      </g>
      <g class="deco-knesset">
        <path d="M118 158h154v10H118zM124 118h142v8H124z"></path>
        <path d="M133 126h9v32h-9zM150 126h9v32h-9zM167 126h9v32h-9zM184 126h9v32h-9zM201 126h9v32h-9zM218 126h9v32h-9zM235 126h9v32h-9zM248 126h9v32h-9z"></path>
      </g>
      <g class="deco-doves">
        <path d="M54 62q9-9 18 0q9-9 18 0M300 44q7-7 14 0q7-7 14 0"></path>
      </g>
    </svg>
    <span class="sparkles">✨<i>✨</i><b>✨</b></span>

    <article class="card claim">
      <div class="claim-head">
        <span class="chip-topic">%TOPIC%</span>
        <h2 class="issue-title"><canvas class="px-title" width="132" height="20"></canvas><span class="title-text">%TITLE%</span></h2>
      </div>
      <p class="claim-text">%CLAIM%</p>
      <p class="claim-echo" aria-hidden="true">%CLAIM%</p>
      <div class="answers">
        <button type="button" class="ans ans-true">%ANS_T%</button>
        <button type="button" class="ans ans-false">%ANS_F%</button>
      </div>
      <p class="source"><svg class="ico-link" viewBox="0 0 24 24" aria-hidden="true"><path d="M10.5 13.5a5 5 0 0 0 7.3.4l2.7-2.7a5 5 0 0 0-7-7l-1.5 1.4"></path><path d="M13.5 10.5a5 5 0 0 0-7.3-.4l-2.7 2.7a5 5 0 0 0 7 7l1.4-1.4"></path></svg><span class="source-name">%SOURCE%</span></p>
    </article>

    <article class="card reveal">
      <div class="mk">
        <div class="portrait">
          <svg class="silhouette" viewBox="0 0 64 64" aria-hidden="true"><circle cx="32" cy="24" r="12"></circle><path d="M7 61c0-13.5 11.2-20.5 25-20.5S57 47.5 57 61Z"></path></svg>
          <canvas class="px-portrait" width="16" height="16"></canvas>
          <span class="initials">בג</span>
        </div>
        <div class="mk-id">
          <span class="mk-name">%MK_NAME%</span>
          <span class="mk-party">%MK_PART%</span>
        </div>
      </div>
      <div class="tiles">
        <div class="tile tile-guess"><span class="tile-label">ניחשת</span><span class="tile-val">%GUESS%</span></div>
        <span class="tile-arrow" aria-hidden="true">←</span>
        <div class="tile tile-real"><span class="tile-label">בפועל</span><span class="tile-val">%ACTUAL%</span></div>
      </div>
      <div class="verdict"><span class="verdict-mark">✗</span></div>
      <p class="note">%NOTE%</p>
    </article>
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
<script data-dc-script data-props='{"$preview":{"width":390,"height":900}}'>
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
  he="אולפן בחירות", en="AR Broadcast Studio",
  tokens="""<!--
  LANE 1 · AR Broadcast Studio
  palette   : deep #050E24 · navy #0A1A3C · glow-cyan #4FD2FF · gold #D4A94E · white #FFFFFF
  type      : SimplerPro Black display in white; values in gold, tabular; wide thin caps for labels
  texture   : translucent dark glass — 1px light border, soft outer glow, perspective plaza grid
  signature : the verdict as a results bar rising off the studio floor line
-->""",
  css="""/* LANE 1 · AR Broadcast Studio
   palette   : deep #050E24 · navy #0A1A3C · glow-cyan #4FD2FF · gold #D4A94E · white
   type      : SimplerPro display white; values gold tabular; thin wide caps for labels
   texture   : translucent dark glass, 1px light border + soft outer glow, perspective floor
   signature : verdict as a results bar rising off the studio floor line */
.lane1 .frame{background:#050E24;color:#EAF3FF}
.lane1 .frame-bg{background:
  radial-gradient(120% 62% at 50% 108%,rgba(79,210,255,.20),transparent 62%),
  radial-gradient(90% 50% at 50% -8%,rgba(79,210,255,.16),transparent 70%),
  linear-gradient(180deg,#050E24 0%,#0A1A3C 58%,#071331 100%)}
.lane1 .deco{height:190px;opacity:.55}
.lane1 .deco .deco-floor{display:block;fill:none;stroke:#4FD2FF;stroke-width:1;opacity:.45}
.lane1 .card{background:linear-gradient(180deg,rgba(19,42,86,.72),rgba(8,22,50,.6));
  border:1px solid rgba(160,215,255,.42);border-radius:2px;backdrop-filter:blur(3px);
  box-shadow:0 0 28px rgba(79,210,255,.16),inset 0 1px 0 rgba(255,255,255,.16);padding:18px}
.lane1 .chip-topic{background:rgba(79,210,255,.14);border:1px solid rgba(79,210,255,.5);color:#BFE9FF;
  letter-spacing:.06em;border-radius:1px}
.lane1 .issue-title{color:#fff;letter-spacing:-.01em;text-shadow:0 0 22px rgba(79,210,255,.5)}
.lane1 .claim-text{color:#D5E5F8}
.lane1 .ans{background:linear-gradient(180deg,rgba(212,169,78,.20),rgba(212,169,78,.05));
  border:1px solid rgba(212,169,78,.7);color:#F2DFB0;border-radius:1px;letter-spacing:.04em;
  box-shadow:inset 0 1px 0 rgba(255,255,255,.14),0 0 16px rgba(212,169,78,.14)}
.lane1 .ans:focus-visible{outline:3px solid #4FD2FF;outline-offset:3px}
.lane1 .source{color:#9EC3E4;letter-spacing:.03em;border-top:1px solid rgba(160,215,255,.2);padding-top:11px}
/* lower-third: portrait in a broadcast frame, name on a gold strap */
.lane1 .mk{gap:0;align-items:stretch;border:1px solid rgba(160,215,255,.4);background:rgba(5,14,36,.7)}
.lane1 .portrait{width:62px;height:62px;background:linear-gradient(180deg,#123061,#081937);
  border-inline-end:1px solid rgba(160,215,255,.4)}
.lane1 .silhouette{fill:rgba(79,210,255,.55);width:74%;height:74%}
.lane1 .mk-id{justify-content:center;gap:0;padding:0}
.lane1 .mk-name{color:#fff;padding:6px 12px 5px}
.lane1 .mk-party{color:#08152F;background:#D4A94E;padding:5px 12px;font-weight:700;letter-spacing:.05em}
.lane1 .tile{background:rgba(9,24,54,.75);border:1px solid rgba(160,215,255,.3)}
.lane1 .tile-label{color:#8FB6DA;letter-spacing:.1em}
.lane1 .tile-val{color:#D4A94E;font-size:26px}
.lane1 .tile-arrow{color:#4FD2FF}
.lane1 .verdict{position:relative;height:136px;display:block;margin-top:6px}
.lane1 .verdict::after{content:"";position:absolute;left:-18px;right:-18px;bottom:0;height:2px;
  background:linear-gradient(90deg,transparent,#4FD2FF 18%,#4FD2FF 82%,transparent);
  box-shadow:0 0 14px rgba(79,210,255,.8)}
.lane1 .verdict::before{content:"";position:absolute;bottom:2px;left:50%;translate:-50% 0;width:108px;height:96px;
  background:linear-gradient(0deg,rgba(212,169,78,.06),#D4A94E 72%);
  box-shadow:0 0 34px rgba(212,169,78,.45);animation:l1rise 1.1s cubic-bezier(.2,.9,.3,1) both}
@keyframes l1rise{from{height:0}to{height:96px}}
.lane1 .verdict-mark{position:absolute;bottom:42px;left:50%;translate:-50% 0;font-size:46px;color:#07142F}
.lane1 .note{color:#C5DAF0}"""))

# ---------------------------------------------------------------- lane 2
LANES.append(dict(
  n=2, file="StateMedal.dc.html", cls="lane2",
  he="ממלכתי רטרו", en="State Medal / Retro Institution",
  tokens="""<!--
  LANE 2 · State Medal / Retro Institution
  palette   : bronze #8C6A3F · parchment #EFE6D4 · state-navy #1C2A52 · velvet #27408B · wood #6B4A2F
  type      : SimplerPro Black with wide 60s logo letterspacing; engraved 1px light/dark text shadow
  texture   : layered inset shadows for emboss/deboss; ruled wood grain; velvet inner panel
  signature : the verdict as a struck, embossed bronze medal
-->""",
  css="""/* LANE 2 · State Medal / Retro Institution
   palette   : bronze #8C6A3F · parchment #EFE6D4 · navy #1C2A52 · velvet #27408B · wood #6B4A2F
   type      : SimplerPro Black, wide 60s logo letterspacing, engraved light/dark shadow pair
   texture   : layered inset shadows (emboss/deboss), ruled wood grain, velvet inner panel
   signature : verdict as a struck, embossed bronze medal */
.lane2 .frame{background:#6B4A2F;color:#1C2A52}
.lane2 .frame-bg{background:
  repeating-linear-gradient(96deg,rgba(0,0,0,.14) 0 2px,transparent 2px 7px),
  linear-gradient(180deg,#7A5636,#5A3E27)}
.lane2 .frame-bg::after{content:"";position:absolute;inset:9px;
  background:radial-gradient(120% 62% at 50% 12%,#3653A4,#27408B 46%,#1B2E66 100%);
  box-shadow:inset 0 0 40px rgba(0,0,0,.6),0 0 0 1px rgba(212,190,150,.35)}
.lane2 .frame-bg::before{content:"";position:absolute;inset:9px;z-index:1;opacity:.5;
  background-image:repeating-linear-gradient(74deg,rgba(255,255,255,.09) 0 1px,transparent 1px 3px)}
.lane2 .card{background:#EFE6D4;border-radius:0;padding:19px 18px;
  box-shadow:inset 0 2px 0 rgba(255,255,255,.85),inset 0 -3px 0 rgba(0,0,0,.22),
             inset 0 0 0 1px rgba(140,106,63,.55)}
.lane2 .chip-topic{background:#1C2A52;color:#EFE6D4;letter-spacing:.22em;padding:6px 12px;
  border-radius:0;font-size:11px;box-shadow:inset 0 -2px 0 rgba(0,0,0,.35)}
.lane2 .issue-title{color:#1C2A52;letter-spacing:.1em;font-size:28px;
  text-shadow:0 1px 0 rgba(255,255,255,.9),0 -1px 0 rgba(0,0,0,.25)}
.lane2 .claim-text{color:#2B2F42;border-top:2px solid rgba(140,106,63,.5);
  border-bottom:2px solid rgba(140,106,63,.5);padding:11px 0}
.lane2 .ans{background:linear-gradient(180deg,#F7F1E3,#DBCEB4);color:#1C2A52;border-radius:0;
  letter-spacing:.14em;box-shadow:inset 0 2px 0 rgba(255,255,255,.95),inset 0 -3px 0 rgba(0,0,0,.28),
    inset 0 0 0 1px rgba(140,106,63,.7),0 3px 0 rgba(0,0,0,.3)}
.lane2 .ans:focus-visible{outline:3px solid #27408B;outline-offset:3px}
.lane2 .source{color:#5C4526;letter-spacing:.08em;font-weight:700}
.lane2 .portrait{width:66px;height:66px;border-radius:50%;
  background:radial-gradient(circle at 34% 28%,#CBA771,#8C6A3F 62%,#65472A);
  box-shadow:inset 0 3px 4px rgba(255,255,255,.5),inset 0 -4px 7px rgba(0,0,0,.5),0 3px 0 rgba(0,0,0,.35);
  border:2px solid rgba(255,255,255,.22)}
.lane2 .silhouette{width:70%;height:70%;fill:#6B4A2F;
  filter:drop-shadow(0 1px 0 rgba(255,255,255,.45)) drop-shadow(0 -1px 0 rgba(0,0,0,.35))}
.lane2 .mk-name{color:#1C2A52;letter-spacing:.06em;text-shadow:0 1px 0 rgba(255,255,255,.8)}
.lane2 .mk-party{color:#5C4526;letter-spacing:.1em;font-weight:700}
.lane2 .tile{background:#E4D9C2;border-radius:0;
  box-shadow:inset 0 2px 3px rgba(0,0,0,.3),inset 0 -1px 0 rgba(255,255,255,.7)}
.lane2 .tile-label{color:#5C4526;letter-spacing:.14em}
.lane2 .tile-val{color:#1C2A52;text-shadow:0 1px 0 rgba(255,255,255,.8)}
.lane2 .tile-arrow{color:#8C6A3F}
.lane2 .verdict{margin:6px 0 2px}
.lane2 .verdict-mark{width:112px;height:112px;border-radius:50%;display:grid;place-items:center;font-size:48px;
  color:#5B4126;background:radial-gradient(circle at 32% 26%,#D2AE77,#8C6A3F 58%,#5F4227);
  box-shadow:inset 0 4px 5px rgba(255,255,255,.55),inset 0 -5px 8px rgba(0,0,0,.5),
    0 0 0 4px rgba(239,230,212,.85),0 0 0 6px rgba(140,106,63,.8),0 5px 0 rgba(0,0,0,.35);
  text-shadow:0 1px 0 rgba(255,255,255,.55),0 -1px 1px rgba(0,0,0,.55)}
.lane2 .note{color:#2B2F42}"""))

# ---------------------------------------------------------------- lane 3
LANES.append(dict(
  n=3, file="Linocut.dc.html", cls="lane3",
  he="לינוקאט אזרחי", en="Linocut Civic Revival",
  tokens="""<!--
  LANE 3 · Linocut Civic Revival
  palette   : ink-blue #4F5BFF · ochre #D9962E · cream #F2E9D8 · ink-black #141414
  type      : SimplerPro Black stacked tight (line-height .84), poster lettering, flat ink fills
  texture   : feTurbulence + feDisplacementMap on card edges and portrait halo — rough print edge
  signature : the portrait — linocut ink head on an offset cream halo, sticker-cut
-->""",
  css="""/* LANE 3 · Linocut Civic Revival
   palette   : ink-blue #4F5BFF · ochre #D9962E · cream #F2E9D8 · ink-black #141414
   type      : SimplerPro Black stacked tight (.84), poster lettering, flat ink fills
   texture   : feTurbulence + feDisplacementMap on card edges + portrait halo (rough print edge)
   signature : the portrait — linocut ink head on an offset cream halo, sticker-cut */
.lane3 .frame{background:#F2E9D8;color:#141414}
.lane3 .frame-bg{background:#F2E9D8}
.lane3 .card{background:none;padding:20px 18px;gap:14px}
.lane3 .card::before{content:"";position:absolute;inset:0;z-index:-1;background:#fff;
  box-shadow:inset 0 0 0 3px #141414;filter:url(#rough)}
.lane3 .chip-topic{background:#D9962E;color:#141414;border-radius:0;font-weight:900;letter-spacing:.02em;
  box-shadow:3px 3px 0 #141414}
.lane3 .issue-title{color:#4F5BFF;font-size:43px;line-height:.86;letter-spacing:-.02em}
.lane3 .claim-text{color:#141414;font-weight:600}
.lane3 .ans{background:#4F5BFF;color:#F2E9D8;border-radius:0;box-shadow:4px 4px 0 #141414;letter-spacing:.03em}
.lane3 .ans-false{background:#141414;color:#F2E9D8}
.lane3 .ans:focus-visible{outline:3px solid #D9962E;outline-offset:4px}
.lane3 .source{color:#141414;font-weight:700}
/* signature: ink portrait, offset cream halo, rough sticker cut */
.lane3 .portrait{width:76px;height:76px;overflow:visible;margin-inline-start:4px}
.lane3 .portrait::before{content:"";position:absolute;inset:-7px -7px -7px -11px;background:#F2E9D8;
  border-radius:50%;box-shadow:0 0 0 3px #141414;filter:url(#rough)}
.lane3 .portrait::after{content:"";position:absolute;inset:0;background:#4F5BFF;border-radius:50%;filter:url(#rough)}
.lane3 .silhouette{width:78%;height:78%;fill:#F2E9D8;z-index:1}
.lane3 .mk-name{font-size:24px;color:#141414}
.lane3 .mk-party{color:#3A3A3A;font-weight:700}
.lane3 .tile{background:#F2E9D8;box-shadow:inset 0 0 0 3px #141414;border-radius:0}
.lane3 .tile-label{color:#3A3A3A;font-weight:700}
.lane3 .tile-val{color:#141414}
.lane3 .tile-arrow{color:#4F5BFF}
.lane3 .verdict{position:relative;height:82px;margin:2px 0}
.lane3 .verdict::before{content:"";position:absolute;top:8px;left:50%;translate:-50% 0;rotate:-7deg;
  width:132px;height:64px;background:#D9962E;box-shadow:inset 0 0 0 4px #141414;
  mix-blend-mode:multiply;filter:url(#rough)}
.lane3 .verdict-mark{position:relative;rotate:-7deg;font-size:40px;color:#141414;margin-top:8px}
.lane3 .note{color:#141414;border-top:3px solid #141414;padding-top:11px}"""))

# ---------------------------------------------------------------- lane 4
LANES.append(dict(
  n=4, file="Stickers.dc.html", cls="lane4",
  he="תרבות סטיקרים", en="Israeli Sticker Culture",
  tokens="""<!--
  LANE 4 · Israeli Sticker Culture
  palette   : sticker-yellow #FFD60A · hot-pink #FF3B6B · teal #2EC4B6 · black #000 · pole-grey #C9C9C4
  type      : SimplerPro Black in slogan chunks, tight, every chunk on its own die-cut
  texture   : white die-cut strokes + drop shadows, hard tilt rotations, grainy pole-grey backdrop
  signature : the verdict slapped on at an angle, overlapping the card edge
-->""",
  css="""/* LANE 4 · Israeli Sticker Culture
   palette   : yellow #FFD60A · hot-pink #FF3B6B · teal #2EC4B6 · black #000 · pole-grey #C9C9C4
   type      : SimplerPro Black slogan chunks, tight, each chunk on its own die-cut
   texture   : white die-cut strokes + drop shadow, hard tilt rotations, grain over pole-grey
   signature : the verdict slapped on at an angle, overlapping the card edge */
.lane4 .frame{background:#C9C9C4;color:#000;gap:22px;padding:22px 16px 30px}
.lane4 .frame-bg{background:#C9C9C4}
.lane4 .frame-bg::after{content:"";position:absolute;inset:0;opacity:.35;
  background-image:radial-gradient(rgba(0,0,0,.5) .5px,transparent .5px),radial-gradient(rgba(255,255,255,.6) .5px,transparent .5px);
  background-size:4px 4px,7px 7px;background-position:0 0,2px 3px}
.lane4 .card{background:none;padding:0;gap:14px;align-items:flex-start}
.lane4 .chip-topic{background:#2EC4B6;color:#000;border:4px solid #fff;border-radius:999px;padding:7px 15px;
  rotate:-3.5deg;font-weight:900;font-size:13px;box-shadow:0 3px 0 rgba(0,0,0,.45)}
.lane4 .issue-title{background:#FFD60A;color:#000;border:5px solid #fff;padding:8px 16px 10px;rotate:1.8deg;
  font-size:34px;box-shadow:0 4px 0 rgba(0,0,0,.5);align-self:flex-start}
.lane4 .claim-text{background:#fff;border:5px solid #fff;padding:13px 15px;
  rotate:-1.2deg;font-weight:700;box-shadow:0 4px 0 rgba(0,0,0,.4);color:#000}
.lane4 .answers{width:100%;gap:12px}
.lane4 .ans{border:5px solid #fff;border-radius:14px;box-shadow:0 4px 0 rgba(0,0,0,.5);font-size:23px}
.lane4 .ans-true{background:#FFD60A;color:#000;rotate:-2.5deg}
.lane4 .ans-false{background:#FF3B6B;color:#000;rotate:2.5deg}
.lane4 .ans:focus-visible{outline:4px solid #000;outline-offset:3px}
.lane4 .source{background:#fff;border:4px solid #fff;padding:6px 12px;rotate:-2deg;font-weight:800;
  box-shadow:0 3px 0 rgba(0,0,0,.4);color:#000;align-self:flex-start}
.lane4 .reveal{position:relative;overflow:visible;background:#fff;border:6px solid #fff;padding:16px;
  rotate:.9deg;box-shadow:0 5px 0 rgba(0,0,0,.45);gap:14px;align-items:stretch}
.lane4 .portrait{width:70px;height:70px;background:#2EC4B6;border-radius:50%;border:5px solid #fff;
  box-shadow:0 3px 0 rgba(0,0,0,.45);rotate:-6deg}
.lane4 .silhouette{width:76%;height:76%;fill:#000}
.lane4 .mk-name{font-size:24px}
.lane4 .mk-party{font-weight:700;color:#1a1a1a}
.lane4 .tile{background:#C9C9C4;border:4px solid #fff;border-radius:12px;box-shadow:0 3px 0 rgba(0,0,0,.4)}
.lane4 .tile-guess{rotate:-2deg}
.lane4 .tile-real{rotate:2deg}
.lane4 .tile-label{font-weight:800;color:#1a1a1a}
.lane4 .tile-val{color:#000}
.lane4 .verdict{position:absolute;bottom:-22px;left:-12px;z-index:4;margin:0}
.lane4 .verdict-mark{background:#FF3B6B;color:#000;border:6px solid #fff;border-radius:50%;
  width:86px;height:86px;display:grid;place-items:center;font-size:40px;rotate:-13deg;
  box-shadow:0 5px 0 rgba(0,0,0,.5)}
.lane4 .note{font-weight:700;color:#000;padding-left:78px;min-height:66px}"""))

# ---------------------------------------------------------------- lane 5
LANES.append(dict(
  n=5, file="AcidType.dc.html", cls="lane5",
  he="טיפוגרפי חומצי", en="Acid Typographic",
  tokens="""<!--
  LANE 5 · Acid Typographic
  palette   : acid-green field #3ECF6E · black #0A0A0A · white #FFFFFF · warm accent #FF7A00 (used once)
  type      : SimplerPro Black at 41px doing all the work; body type small, black, unstyled
  texture   : the claim repeated once at 7% black behind itself — repetition IS the texture
  signature : the scale-crop — the claim runs off both frame edges
-->""",
  css="""/* LANE 5 · Acid Typographic
   palette   : acid field #3ECF6E · black #0A0A0A · white · warm accent #FF7A00 (used exactly once)
   type      : SimplerPro Black at 41px doing all the work; body small, black, unstyled
   texture   : the claim repeated once at 7% black behind itself — repetition IS the texture
   signature : the scale-crop — the claim runs off both frame edges */
.lane5 .frame{background:#3ECF6E;color:#0A0A0A;gap:0;padding:20px 0 22px;justify-content:flex-start}
.lane5 .frame-bg{background:#3ECF6E}
.lane5 .card{background:none;padding:0;gap:0}
.lane5 .claim{position:relative;padding-bottom:26px}
.lane5 .claim-head{padding:0 18px;gap:4px}
.lane5 .chip-topic{background:none;padding:0;color:#0A0A0A;font-weight:800;letter-spacing:.16em;
  text-transform:none;font-size:11.5px}
.lane5 .issue-title{font-size:20px;letter-spacing:.02em}
.lane5 .claim-text{position:relative;z-index:2;font-family:'SimplerPro',system-ui,sans-serif;font-weight:900;
  font-size:39px;line-height:.94;letter-spacing:-.025em;color:#0A0A0A;
  margin:16px -20px 0;padding:0 8px}
.lane5 .claim-echo{display:block;position:absolute;z-index:0;top:96px;right:-64px;left:-64px;
  font-family:'SimplerPro',system-ui,sans-serif;font-weight:900;font-size:60px;line-height:.9;
  color:rgba(10,10,10,.07);pointer-events:none;user-select:none}
.lane5 .answers{margin-top:26px;padding:0 18px;gap:26px;justify-content:flex-start}
.lane5 .ans{flex:0 0 auto;padding:0;min-height:44px;font-size:27px;color:#0A0A0A;background:none;
  text-decoration:underline;text-decoration-thickness:5px;text-underline-offset:7px}
.lane5 .ans:focus-visible{outline:3px solid #0A0A0A;outline-offset:5px}
.lane5 .source{margin-top:20px;padding:0 18px;color:#0A0A0A;font-weight:800;letter-spacing:.04em}
.lane5 .reveal{margin-top:28px;padding:22px 18px 0;border-top:5px solid #0A0A0A;gap:16px}
.lane5 .portrait{width:60px;height:60px;background:#0A0A0A;border-radius:0}
.lane5 .silhouette{width:78%;height:78%;fill:#3ECF6E}
.lane5 .mk-name{font-size:23px}
.lane5 .mk-party{font-weight:700;color:#0A0A0A}
.lane5 .tiles{gap:0;border-top:2px solid #0A0A0A;border-bottom:2px solid #0A0A0A}
.lane5 .tile{padding:12px 6px;align-items:flex-start;gap:3px}
.lane5 .tile-label{font-weight:800;letter-spacing:.14em;color:#0A0A0A}
.lane5 .tile-val{font-size:27px;color:#0A0A0A}
.lane5 .tile-arrow{font-size:22px;opacity:1}
.lane5 .verdict{justify-content:flex-start}
.lane5 .verdict-mark{font-size:78px;line-height:.8;color:#FF7A00}
.lane5 .note{font-weight:700;color:#0A0A0A;max-width:31ch}"""))

# ---------------------------------------------------------------- lane 6
LANES.append(dict(
  n=6, file="PapersPlease.dc.html", cls="lane6",
  he="ניירת, בבקשה", en="Papers, Please × Reigns",
  tokens="""<!--
  LANE 6 · Papers, Please × Reigns
  palette   : grey-brown #2B2626 · paper #A39A8A · muted-red #7C1F1F · khaki #6E6A54 · off-white #D8D2C4
  type      : SimplerPro Black rasterised to a <canvas> at 11px, upscaled 2x nearest-neighbour
  texture   : 1px pixel checker over the desk, hard document rules, no radii anywhere
  signature : the verdict as an angled rubber stamp bleeding off the document's corner
-->""",
  css="""/* LANE 6 · Papers, Please x Reigns
   palette   : grey-brown #2B2626 · paper #A39A8A · muted-red #7C1F1F · khaki #6E6A54 · off-white #D8D2C4
   type      : SimplerPro Black rasterised to <canvas> at 11px, upscaled 2x nearest-neighbour
   texture   : 1px pixel checker over the desk, hard document rules, zero radii
   signature : the verdict as an angled rubber stamp bleeding off the document corner */
.lane6 .frame{background:#2B2626;color:#2B2626;gap:16px;padding:20px 16px 26px}
.lane6 .frame-bg{background:#2B2626}
.lane6 .frame-bg::after{content:"";position:absolute;inset:0;opacity:.55;
  background-image:repeating-conic-gradient(rgba(255,255,255,.045) 0 25%,transparent 0 50%);
  background-size:4px 4px}
.lane6 .card{background:#A39A8A;border-radius:0;padding:16px 15px;
  box-shadow:inset 0 0 0 1px #8A8171,0 2px 0 rgba(0,0,0,.5)}
.lane6 .claim-head{width:100%;gap:10px;border-bottom:2px solid #7A7264;padding-bottom:10px}
.lane6 .chip-topic{background:#6E6A54;color:#D8D2C4;border-radius:0;letter-spacing:.16em;font-size:10.5px;
  padding:4px 9px;font-weight:700}
.lane6 .px-title{display:block;image-rendering:pixelated;width:264px;height:40px}
.lane6 .title-text{display:none}
.lane6 .issue-title{line-height:1}
.lane6 .claim-text{color:#2B2626;font-size:14px;line-height:1.5;
  border-bottom:1px dashed #7A7264;padding-bottom:12px}
.lane6 .answers{gap:9px}
.lane6 .ans{background:#D8D2C4;color:#2B2626;border-radius:0;letter-spacing:.12em;font-size:19px;
  box-shadow:inset 0 0 0 2px #2B2626,3px 3px 0 rgba(0,0,0,.45)}
.lane6 .ans:focus-visible{outline:3px solid #7C1F1F;outline-offset:3px}
.lane6 .source{color:#3A342B;font-weight:700;letter-spacing:.06em;font-size:11.5px}
.lane6 .reveal{position:relative;overflow:visible}
.lane6 .portrait{width:58px;height:58px;background:#6E6A54;border-radius:0;
  box-shadow:inset 0 0 0 2px #2B2626,0 0 0 1px #8A8171}
.lane6 .silhouette{display:none}
.lane6 .px-portrait{display:block;image-rendering:pixelated;width:52px;height:52px}
.lane6 .mk-name{font-size:19px;letter-spacing:.02em}
.lane6 .mk-party{color:#3A342B;font-weight:700;letter-spacing:.05em}
.lane6 .tiles{gap:0;border:1px solid #7A7264;background:#9A9182}
.lane6 .tile{padding:10px 6px;align-items:flex-start}
.lane6 .tile-guess{border-inline-end:1px dashed #7A7264}
.lane6 .tile-real{border-inline-start:1px dashed #7A7264}
.lane6 .tile-label{color:#3A342B;letter-spacing:.16em;font-weight:700;font-size:10px}
.lane6 .tile-val{color:#2B2626;font-size:21px}
.lane6 .tile-arrow{color:#3A342B;padding:0 8px}
.lane6 .verdict{position:absolute;bottom:6px;left:12px;z-index:5;margin:0}
.lane6 .verdict-mark{width:96px;height:96px;border-radius:50%;display:grid;place-items:center;font-size:44px;
  color:#7C1F1F;rotate:-13deg;opacity:.82;mix-blend-mode:multiply;
  box-shadow:inset 0 0 0 5px #7C1F1F,inset 0 0 0 9px transparent,inset 0 0 0 11px #7C1F1F}
.lane6 .note{color:#2B2626;font-size:13px;padding-left:96px;min-height:74px;
  border-top:1px solid #7A7264;padding-top:10px}"""))

# ---------------------------------------------------------------- lane 7
LANES.append(dict(
  n=7, file="StateKitsch.dc.html", cls="lane7",
  he="קיטש ממלכתי אפי", en="Epic State Kitsch",
  tokens="""<!--
  LANE 7 · Epic State Kitsch
  palette   : gold #F5C542 · deep-gold #C9932B · sky #7EB8E6 · cloud-cream #FFF4DC · sunset-pink #F2A7C3
  type      : SimplerPro Black bevelled by five stacked text-shadows; body on cloud-cream, dark brown
  texture   : radial cloud puffs, conic sunburst, glow; exactly three sparkles
  signature : the אמת/שקר buttons as radiant golden tablets resting in cloud
-->""",
  css="""/* LANE 7 · Epic State Kitsch
   palette   : gold #F5C542 · deep-gold #C9932B · sky #7EB8E6 · cloud-cream #FFF4DC · pink #F2A7C3
   type      : SimplerPro Black bevelled by five stacked text-shadows; body dark brown on cream
   texture   : radial cloud puffs, conic sunburst, glow; exactly three sparkles
   signature : the אמת/שקר buttons as radiant golden tablets resting in cloud */
.lane7 .frame{background:#7EB8E6;color:#4A3A12;gap:16px}
.lane7 .frame-bg{background:
  radial-gradient(58% 30% at 50% 96%,rgba(255,244,220,.95),transparent 70%),
  radial-gradient(38% 22% at 12% 78%,rgba(255,255,255,.85),transparent 70%),
  radial-gradient(42% 24% at 88% 66%,rgba(255,255,255,.8),transparent 70%),
  radial-gradient(46% 26% at 20% 22%,rgba(255,255,255,.7),transparent 70%),
  conic-gradient(from 200deg at 50% 116%,rgba(245,197,66,.55),rgba(242,167,195,.35),rgba(245,197,66,.55),rgba(242,167,195,.35),rgba(245,197,66,.55)),
  linear-gradient(180deg,#5FA2D8,#7EB8E6 42%,#F2A7C3 100%)}
.lane7 .deco{height:200px;opacity:.5}
.lane7 .deco .deco-knesset{display:block;fill:#4A6E92;opacity:.55}
/* exactly three sparkles; the container is font-size:0 so the bare glyph stays hidden */
.lane7 .sparkles{display:block;position:absolute;inset:0;z-index:3;pointer-events:none;font-size:0;line-height:1}
.lane7 .sparkles>i,.lane7 .sparkles>b{position:absolute;font-style:normal;font-weight:400}
.lane7 .sparkles>i{top:104px;left:24px;font-size:18px;animation:l7tw 3.4s ease-in-out infinite .8s}
.lane7 .sparkles>b{top:296px;right:20px;font-size:23px;animation:l7tw 3.9s ease-in-out infinite 1.6s}
.lane7 .sparkles::after{content:"✨";position:absolute;top:474px;left:20px;font-size:20px;
  animation:l7tw 4.4s ease-in-out infinite}
@keyframes l7tw{0%,100%{opacity:.55;scale:.9}50%{opacity:1;scale:1.12}}
.lane7 .card{background:linear-gradient(180deg,rgba(255,244,220,.97),rgba(255,236,196,.94));
  border-radius:22px;border:2px solid #E7BE6A;padding:18px;
  box-shadow:0 0 0 4px rgba(255,255,255,.55),0 10px 26px rgba(74,58,18,.28),inset 0 2px 0 rgba(255,255,255,.9)}
.lane7 .claim-head{background:linear-gradient(180deg,#59A0D8,#8CC3EB);margin:-18px -18px 6px;
  padding:16px 18px 18px;border-radius:20px 20px 0 0;gap:11px;
  box-shadow:inset 0 -3px 0 rgba(255,255,255,.5)}
.lane7 .chip-topic{background:linear-gradient(180deg,#FFE9A8,#F5C542);color:#4A3A12;border-radius:999px;
  border:1px solid #C9932B;padding:5px 13px;box-shadow:inset 0 1px 0 rgba(255,255,255,.9)}
.lane7 .issue-title{color:#FFE9A8;font-size:34px;letter-spacing:.01em;
  text-shadow:0 1px 0 #F5C542,0 2px 0 #D9A233,0 3px 0 #C9932B,0 4px 0 #A87A1E,0 6px 10px rgba(74,58,18,.5)}
.lane7 .claim-text{color:#4A3A12;font-weight:600}
/* signature: radiant golden tablets in cloud */
.lane7 .answers{position:relative;margin:12px 0 6px;padding-bottom:16px;gap:12px}
.lane7 .answers::before{content:"";position:absolute;inset:-26px -14px -14px;z-index:0;border-radius:50%;
  background:radial-gradient(closest-side,rgba(255,233,168,.95),rgba(245,197,66,.35),transparent 78%)}
.lane7 .answers::after{content:"";position:absolute;left:-6px;right:-6px;bottom:-8px;height:38px;z-index:2;
  background:
    radial-gradient(19px 16px at 11% 42%,#fff 99%,transparent 100%),
    radial-gradient(25px 20px at 30% 60%,#fff 99%,transparent 100%),
    radial-gradient(21px 17px at 50% 41%,#fff 99%,transparent 100%),
    radial-gradient(26px 21px at 70% 61%,#fff 99%,transparent 100%),
    radial-gradient(20px 16px at 89% 43%,#fff 99%,transparent 100%),
    linear-gradient(#fff,#fff) 0 22px/100% 16px no-repeat;
  filter:drop-shadow(0 3px 3px rgba(74,58,18,.24))}
.lane7 .ans{position:relative;z-index:1;background:linear-gradient(180deg,#FFF3C8,#F5C542 46%,#C9932B);
  color:#4A3A12;border:2px solid #A87A1E;border-radius:20px 20px 26px 26px;font-size:23px;letter-spacing:.02em;
  text-shadow:0 1px 0 rgba(255,255,255,.85);
  box-shadow:0 0 26px rgba(245,197,66,.85),inset 0 2px 0 rgba(255,255,255,.9),inset 0 -5px 7px rgba(120,84,14,.35),0 5px 0 #8A631A}
.lane7 .ans:focus-visible{outline:3px solid #4A3A12;outline-offset:4px}
.lane7 .source{color:#5C4A1E;font-weight:700}
.lane7 .portrait{width:66px;height:66px;border-radius:50%;
  background:radial-gradient(circle at 34% 28%,#FFF3C8,#F5C542 55%,#C9932B);
  border:2px solid #A87A1E;box-shadow:0 0 20px rgba(245,197,66,.8),inset 0 2px 0 rgba(255,255,255,.85)}
.lane7 .silhouette{display:none}
.lane7 .initials{display:block;color:#4A3A12;font-size:26px;text-shadow:0 1px 0 rgba(255,255,255,.85)}
.lane7 .mk-name{color:#4A3A12;font-size:22px;text-shadow:0 1px 0 rgba(255,255,255,.8)}
.lane7 .mk-party{color:#5C4A1E;font-weight:700}
.lane7 .tile{background:rgba(255,255,255,.62);border:1px solid #E7BE6A;border-radius:16px}
.lane7 .tile-label{color:#5C4A1E;font-weight:700}
.lane7 .tile-val{color:#4A3A12}
.lane7 .tile-arrow{color:#C9932B}
.lane7 .verdict-mark{color:#8A631A;font-size:52px;
  text-shadow:0 -1px 0 #FFE9A8,0 1px 0 #C9932B,0 2px 0 #A87A1E,0 4px 9px rgba(74,58,18,.4)}
.lane7 .note{color:#4A3A12;font-weight:600}"""))

# ---------------------------------------------------------------- lane 8
LANES.append(dict(
  n=8, file="Editorial.dc.html", cls="lane8",
  he="עיתונאי מודרני", en="Modern Editorial / Tile-Clean",
  tokens="""<!--
  LANE 8 · Modern Editorial / Tile-Clean
  palette   : paper #FAFAF7 · ink #1A1A1A · correct #6AAA64 · miss #787C7E · surprise #C9A227 · rule #DDD9D0
  type      : one SimplerPro display size, one body size, generous leading, hairline rules only
  texture   : none — whitespace and a strict left-edge grid carry the page
  signature : guess vs reality as two flat Wordle tiles; the fill, not the word, carries the verdict
-->""",
  css="""/* LANE 8 · Modern Editorial / Tile-Clean
   palette   : paper #FAFAF7 · ink #1A1A1A · correct #6AAA64 · miss #787C7E · surprise #C9A227 · rule #DDD9D0
   type      : one SimplerPro display size, one body size, generous leading, hairline rules only
   texture   : none — whitespace and a strict grid carry the page
   signature : guess vs reality as two flat Wordle tiles; the fill carries the verdict */
.lane8 .frame{background:#FAFAF7;color:#1A1A1A;gap:0;padding:30px 24px 34px}
.lane8 .frame-bg{background:#FAFAF7}
.lane8 .card{background:none;padding:0;gap:0}
.lane8 .claim-head{gap:14px}
.lane8 .chip-topic{background:none;padding:0;color:#5C5C58;font-weight:700;font-size:11.5px;
  letter-spacing:.18em;text-transform:none}
.lane8 .issue-title{font-size:33px;letter-spacing:-.01em;line-height:1.08}
.lane8 .claim-text{margin-top:22px;font-size:16.5px;line-height:1.62;color:#1A1A1A;max-width:30ch}
.lane8 .answers{margin-top:26px;gap:12px}
.lane8 .ans{background:none;border:1px solid #1A1A1A;border-radius:2px;color:#1A1A1A;font-size:20px;
  letter-spacing:.02em}
.lane8 .ans:focus-visible{outline:3px solid #C9A227;outline-offset:3px}
.lane8 .source{margin-top:26px;padding-top:13px;border-top:1px solid #DDD9D0;color:#1A1A1A;
  font-size:14.5px;font-weight:700;letter-spacing:.01em}
.lane8 .source .ico-link{width:15px;height:15px;color:#787C7E}
.lane8 .source-name{border-bottom:2px solid #C9A227;padding-bottom:1px}
.lane8 .reveal{margin-top:34px;padding-top:26px;border-top:3px solid #1A1A1A;gap:0}
.lane8 .portrait{width:52px;height:52px;border-radius:50%;background:#FAFAF7;
  box-shadow:inset 0 0 0 1px #DDD9D0}
.lane8 .silhouette{width:66%;height:66%;fill:#C4C0B6}
.lane8 .mk-name{font-size:22px}
.lane8 .mk-party{color:#5C5C58}
/* signature: Wordle tiles — equal type, the fill does the talking */
.lane8 .tiles{margin-top:24px;gap:12px;align-items:flex-end}
.lane8 .tile{padding:0;gap:8px}
.lane8 .tile-label{color:#5C5C58;font-size:11.5px;letter-spacing:.16em;font-weight:700}
.lane8 .tile-val{width:100%;padding:22px 0;text-align:center;font-size:26px;color:#1A1A1A;border-radius:2px}
.lane8 .tile-guess .tile-val{background:#787C7E}
.lane8 .tile-real .tile-val{background:#C9A227}
.lane8 .tile-arrow{color:#787C7E;padding-bottom:26px}
.lane8 .verdict{margin-top:22px}
.lane8 .verdict-mark{font-size:28px;color:#787C7E}
.lane8 .note{margin-top:16px;font-size:15px;line-height:1.6;color:#1A1A1A;max-width:32ch}"""))

# ---------------------------------------------------------------- lane 6 logic
LOGIC_L6 = r"""class Component extends DCLogic {
  componentDidMount() {
    this.paint();
    if (document.fonts && document.fonts.ready) { document.fonts.ready.then(() => this.paint()); }
    setTimeout(() => this.paint(), 500);
  }
  renderVals() { return {}; }
  paint() {
    const root = document.querySelector('.lane6');
    if (!root) return;
    // display type: SimplerPro Black drawn at 12px, upscaled 2x nearest-neighbour by CSS
    const t = root.querySelector('.px-title');
    if (t) {
      const c = t.getContext('2d');
      c.clearRect(0, 0, t.width, t.height);
      c.imageSmoothingEnabled = false;
      c.fillStyle = '#2B2626';
      c.font = '900 12px SimplerPro, system-ui, sans-serif';
      c.textBaseline = 'alphabetic';
      c.textAlign = 'right';
      if ('direction' in c) { c.direction = 'rtl'; }
      c.fillText('חוק הגיוס 🪖', t.width - 2, 15);
    }
    // booth photo: 16x16 silhouette, upscaled the same way
    const p = root.querySelector('.px-portrait');
    if (p) {
      const c = p.getContext('2d');
      c.imageSmoothingEnabled = false;
      c.clearRect(0, 0, 16, 16);
      c.fillStyle = '#6E6A54';
      c.fillRect(0, 0, 16, 16);
      c.fillStyle = '#2B2626';
      c.fillRect(6, 2, 4, 1);
      c.fillRect(5, 3, 6, 4);
      c.fillRect(6, 7, 4, 2);
      c.fillRect(4, 9, 8, 2);
      c.fillRect(3, 11, 10, 5);
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
                .replace("%TOPIC%", TOPIC).replace("%TITLE%", TITLE).replace("%CLAIM%", CLAIM)
                .replace("%ANS_T%", ANS_T).replace("%ANS_F%", ANS_F).replace("%SOURCE%", SOURCE)
                .replace("%MK_NAME%", MK_NAME).replace("%MK_PART%", MK_PART)
                .replace("%GUESS%", GUESS).replace("%ACTUAL%", ACTUAL).replace("%NOTE%", NOTE))
        page = (PAGE
                .replace("%TOKENS%", lane["tokens"])
                .replace("%SHARED%", shared)
                .replace("%LANECSS%", lane["css"])
                .replace("%BODY%", body)
                .replace("%LOGIC%", LOGIC_L6 if lane["n"] == 6 else LOGIC_STATIC))
        (OUT / lane["file"]).write_text(page, encoding="utf-8")

    manifest = {
        "artboards": [
            {"file": l["file"], "x": (len(LANES) - 1 - i) * 480, "y": 0, "w": 390, "h": 900,
             "title": "%d · %s · %s" % (l["n"], l["he"], l["en"])}
            for i, l in enumerate(LANES)
        ],
        "launch": {"view": "canvas"},
    }
    (OUT / "canvas.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    for l in LANES:
        print("%s  %6.1f KB" % (l["file"].ljust(22), (OUT / l["file"]).stat().st_size / 1024))
    print("canvas.json written")

if __name__ == "__main__":
    build()
