# -*- coding: utf-8 -*-
"""Geometry + colour audit of the built artboards, headless and reproducible.

Runs against each .dc.html on its own (one document per frame, exactly how the canvas
renders them), so nothing here depends on a review page or a live browser tab.

    python3 explorations/v4/audit_v4.py
"""
import json, pathlib, re, shutil, subprocess, tempfile

HERE = pathlib.Path(__file__).resolve().parent
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
SHIM = """
class DCLogic {}
document.addEventListener('DOMContentLoaded', () => {
  const b = document.createElement('style');
  b.textContent = 'x-dc{display:block}helmet{display:none}';
  document.head.appendChild(b);
  document.querySelectorAll('x-dc > helmet > style').forEach(s => document.head.appendChild(s));
});
"""

JS = r"""
const SEL = '.art,.art-emoji,.issue-title,.claim-text,.ans-true,.ans-false,.topic-title,' +
            '.coin-num,.coin-glyph,.avatar,.map-btn,.sticker,.doc-stamp,.art-clip';
const st = document.querySelector('.stage');
const R = e => e.getBoundingClientRect();
const gap = (a, b) => +(Math.max(R(a).left, R(b).left) - Math.min(R(a).right, R(b).right)).toFixed(1);
const lum = c => { const v = c.match(/\d+/g).slice(0,3).map(Number).map(x => {
    x /= 255; return x <= .03928 ? x/12.92 : Math.pow((x+.055)/1.055, 2.4); });
  return .2126*v[0] + .7152*v[1] + .0722*v[2]; };
const ratio = (a, b) => { const L = [lum(a), lum(b)].sort((x,y) => y-x);
  return +((L[0]+.05)/(L[1]+.05)).toFixed(2); };
const K = ['backgroundColor','borderTopColor','borderTopWidth','color','boxShadow',
           'borderRadius','fontSize','minHeight','padding'];
const sig = e => { const c = getComputedStyle(e); return K.map(k => c[k]).join('|'); };
const lines = e => {   /* cluster by position: .px-punct boxes sit off the baseline */
  const r = document.createRange(); r.selectNodeContents(e);
  const lh = parseFloat(getComputedStyle(e).lineHeight) ||
             parseFloat(getComputedStyle(e).fontSize) * 1.2;
  const tops = [...r.getClientRects()].map(x => x.top).sort((a,b) => a-b);
  let n = 0, last = -1e9;
  for (const t of tops) { if (t - last > lh * 0.5) { n++; last = t; } }
  return n || 1; };

const cn = e => (e.getAttribute('class') || '').split(' ')[0] || e.tagName;
const els = [...st.querySelectorAll(SEL)].filter(e => {
  const r = R(e); return r.width > 0 && r.height > 0 && getComputedStyle(e).display !== 'none'; });
const hits = [];
for (let i = 0; i < els.length; i++) for (let j = i+1; j < els.length; j++) {
  if (els[i].contains(els[j]) || els[j].contains(els[i])) continue;
  const a = R(els[i]), b = R(els[j]);
  const ox = Math.min(a.right,b.right) - Math.max(a.left,b.left);
  const oy = Math.min(a.bottom,b.bottom) - Math.max(a.top,b.top);
  if (ox > 1 && oy > 1) hits.push(cn(els[i]) + ' x ' + cn(els[j]) +
                                 ' (' + ox.toFixed(0) + 'x' + oy.toFixed(0) + ')');
}
const card = st.querySelector('.card'), an = st.querySelector('.answers');
const T = st.querySelector('.ans-true'), F = st.querySelector('.ans-false');
const ti = st.querySelector('.issue-title'), cl = st.querySelector('.claim-text');
const bs = getComputedStyle(T), ts = getComputedStyle(ti), cls = getComputedStyle(cl);
return JSON.stringify({
  stage: [...st.classList].filter(c => c !== 'stage').join('.'),
  overlaps: hits,
  trueEqualsFalse: sig(T) === sig(F),
  pileCards: st.querySelectorAll('.pile-card').length,
  titlePx: parseFloat(ts.fontSize), titleLines: lines(ti),
  claimPx: parseFloat(cls.fontSize), claimWeight: cls.fontWeight,
  titleNotSmallerThanClaim: parseFloat(ts.fontSize) >= parseFloat(cls.fontSize),
  cardOverflowY: card.scrollHeight - card.clientHeight,
  titleOverflowX: ti.scrollWidth - ti.clientWidth,
  claimContrast: ratio(cls.color, getComputedStyle(card).backgroundColor),
  btnContrast: ratio(bs.color, bs.backgroundColor),
  mapAvatarGap: gap(st.querySelector('.map-btn'), st.querySelector('.avatar')),
  clusterToTopic: gap(st.querySelector('.map-btn'), st.querySelector('.topic-title')),
  cardToButtons: +(R(an).top - R(card).bottom).toFixed(1),
  buttonsW: +R(an).width.toFixed(0),
  minHitH: +Math.min(...[...st.querySelectorAll('.ans,.map-btn')].map(e => R(e).height)).toFixed(0),
  /* the visual box is 40x40; the real target is hit-tested, because the extra 4px
     comes from a ::after bleed that no bounding rect will show */
  iconBoxes: (() => { const m = R(st.querySelector('.map-btn')), a = R(st.querySelector('.avatar'));
    return {map: [Math.round(m.width), Math.round(m.height)],
            avatar: [Math.round(a.width), Math.round(a.height)]}; })(),
  mapHitTarget: (() => {
    const b = st.querySelector('.map-btn'), r = R(b);
    const cx = r.left + r.width/2, cy = r.top + r.height/2;
    const probe = d => { const e = document.elementFromPoint(cx + d[0], cy + d[1]);
      return !!(e && (e === b || b.contains(e))); };
    const ok = [[-21.5,-21.5],[21.5,-21.5],[-21.5,21.5],[21.5,21.5]].every(probe);
    return ok ? 44 : (([[-19.5,-19.5],[19.5,-19.5],[-19.5,19.5],[19.5,19.5]].every(probe)) ? 40 : 0);
  })(),
  /* v4.8 — no progress indicator anywhere; assert that stays true */
  progressElements: st.querySelectorAll('.storybar,.steps,.step,.seg').length,
  claimText: cl.textContent.trim()
});
"""

def audit():
    files = sorted(p.name for p in HERE.glob("*.dc.html"))
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="v4audit-"))
    (tmp / "support.js").write_text(SHIM, encoding="utf-8")
    rows = []
    try:
        for f in files:
            src = (HERE / f).read_text(encoding="utf-8")
            src = src.replace("</body>",
                '<pre id="out" hidden></pre>\n<script>document.fonts.ready.then(()=>{try{'
                'document.getElementById("out").textContent=(function(){%s})();}'
                'catch(e){document.getElementById("out").textContent=JSON.stringify({error:String(e)});}});'
                '</script>\n</body>'
                % JS, 1)
            (tmp / f).write_text(src, encoding="utf-8")
            dom = subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-sandbox",
                                  "--window-size=390,900", "--virtual-time-budget=8000",
                                  "--dump-dom", (tmp / f).as_uri()],
                                 check=True, capture_output=True).stdout.decode("utf-8")
            m = re.search(r'<pre id="out" hidden="">(.*?)</pre>', dom, re.S)
            assert m and m.group(1).strip(), "no audit came back for " + f
            r = json.loads(m.group(1)); r["file"] = f
            rows.append(r)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print(json.dumps(rows, ensure_ascii=False, indent=1))
    return rows

if __name__ == "__main__":
    audit()
