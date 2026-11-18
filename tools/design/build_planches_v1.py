"""Generate the three V1 style boards (main game page) for Tournee.

Output: G-DESIGN/planches/v1/0X-<direction>.html, each one standalone
(CSS + JS inline, no network). Run: python3 tools/design/build_planches_v1.py
Demo data = the real daily round of 2026-11-18 from src/shared/puzzle.ts.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "G-DESIGN" / "planches" / "v1"

# ---------------------------------------------------------------- shared JS
JS = r"""
const P = { depot:{x:0,y:0}, stops:[
  {n:'Post',x:1,y:5},{n:'Florist',x:4,y:0},{n:'Library',x:6,y:1},
  {n:'Atelier',x:4,y:2},{n:'Bakery',x:1,y:0},{n:'School',x:2,y:4}] };
const ORDER = [4,1,2,3];               // Bakery, Florist, Library, Atelier
const KIND = document.body.dataset.kind;
const dist = (a,b) => Math.abs(a.x-b.x)+Math.abs(a.y-b.y);
function legs(){ let cur=P.depot, cum=0; return ORDER.map(i=>{ const s=P.stops[i], l=dist(cur,s); cum+=l; const o={i,s,from:cur,l,cum}; cur=s; return o; }); }
const code = n => n.slice(0,2).toUpperCase();

function marker(st, state, num){
  const {x,y}=st;
  if(KIND==='fold'){
    if(state==='todo') return `<circle class="mk todo" cx="${x}" cy="${y}" r=".26"/>`;
    return (state==='last'?`<circle class="mk ring" cx="${x}" cy="${y}" r=".44"/>`:'')+
      `<circle class="mk on" cx="${x}" cy="${y}" r=".28"/><text class="mk-n" x="${x}" y="${y+.105}">${num}</text>`;
  }
  if(KIND==='calque'){
    const cross=`<line class="mk-x" x1="${x-.38}" y1="${y}" x2="${x+.38}" y2="${y}"/><line class="mk-x" x1="${x}" y1="${y-.38}" x2="${x}" y2="${y+.38}"/>`;
    if(state==='todo') return cross+`<circle class="mk todo" cx="${x}" cy="${y}" r=".2"/>`;
    return cross+(state==='last'?`<circle class="mk ring" cx="${x}" cy="${y}" r=".36"/>`:'')+
      `<circle class="mk on" cx="${x}" cy="${y}" r=".22"/><text class="mk-n" x="${x}" y="${y+.09}">${num}</text>`;
  }
  // night
  if(state==='todo') return `<rect class="mk todo" x="${x-.27}" y="${y-.27}" width=".54" height=".54" rx=".06"/><text class="mk-c" x="${x}" y="${y+.075}">${code(st.n)}</text>`;
  return (state==='last'?`<rect class="mk ring" x="${x-.4}" y="${y-.4}" width=".8" height=".8" rx=".1"/>`:'')+
    `<rect class="mk on" x="${x-.27}" y="${y-.27}" width=".54" height=".54" rx=".06"/><text class="mk-n" x="${x}" y="${y+.1}">${num}</text>`;
}

function depotMk(){
  const d=P.depot;
  if(KIND==='fold') return `<rect class="dp" x="${d.x-.26}" y="${d.y-.26}" width=".52" height=".52" rx=".05"/><text class="dp-t" x="${d.x}" y="${d.y+.1}">D</text>`;
  if(KIND==='calque') return `<rect class="dp" x="${d.x-.24}" y="${d.y-.24}" width=".48" height=".48"/><rect class="dp2" x="${d.x-.13}" y="${d.y-.13}" width=".26" height=".26"/>`;
  return `<rect class="dp" x="${d.x-.3}" y="${d.y-.3}" width=".6" height=".6" rx=".06"/><text class="dp-t" x="${d.x}" y="${d.y+.075}">DP</text>`;
}

function mapSVG(){
  const L=legs();
  let s=`<svg viewBox="-0.8 -0.8 8.6 8.6" class="map-svg" role="img" aria-label="Street map, depot and six stops">`;
  if(KIND==='calque'){
    s+=`<defs><pattern id="hatch" width=".16" height=".16" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2=".16" class="hatch"/></pattern></defs>`;
    for(let k=0;k<=14;k++){ const v=k/2; s+=`<line class="minor" x1="${v}" y1="-.45" x2="${v}" y2="7.45"/><line class="minor" x1="-.45" y1="${v}" x2="7.45" y2="${v}"/>`; }
    s+=`<rect class="park" x="5.12" y="4.12" width=".76" height="1.76"/>`;
    for(let k=0;k<8;k++){ s+=`<line class="st" x1="${k}" y1="-.45" x2="${k}" y2="7.45"/><line class="st" x1="-.45" y1="${k}" x2="7.45" y2="${k}"/>`; }
  } else {
    const g = KIND==='fold' ? .1 : .11, r = KIND==='fold' ? .03 : .07;
    for(let i=0;i<7;i++) for(let j=0;j<7;j++){
      const park = (i===5 && (j===4||j===5));
      s+=`<rect class="blk${park?' park':''}" x="${i+g}" y="${j+g}" width="${1-2*g}" height="${1-2*g}" rx="${r}"/>`;
    }
  }
  let path='M0 0'; L.forEach(g=>{ path+=` H${g.s.x} V${g.s.y}`; });
  if(KIND!=='calque') s+=`<path class="route-case" d="${path}"/>`;
  s+=`<path class="route" d="${path}"/>`;
  if(KIND==='calque') L.forEach(g=>{
    const h=g.from.x!==g.s.x; const mx=h?(g.from.x+g.s.x)/2:g.s.x; const my=h?g.from.y:(g.from.y+g.s.y)/2;
    const dy=h?(g.from.y===0?-.3:.42):0, ox=h?0:.34;
    s+=`<g class="dim"><text x="${mx+ox}" y="${my+dy+.09}">${g.l}</text></g>`;
  });
  s+=depotMk();
  s+=`<text class="lbl" x="${P.depot.x-.36}" y="${P.depot.y-.42}">Depot</text>`;
  P.stops.forEach((st,i)=>{
    const k=ORDER.indexOf(i);
    const state = k<0?'todo':(k===ORDER.length-1?'last':'on');
    s+=marker(st,state,k+1);
    s+=`<text class="lbl${k<0?' lbl-todo':''}" x="${st.x+.36}" y="${st.y+.5}">${KIND==='night'?st.n.toUpperCase():st.n}</text>`;
  });
  return s+'</svg>';
}

function manifest(narrow){
  const L=legs(); let h='<ol class="mf">';
  L.forEach((g,k)=>{ h+=`<li class="mf-row done${k===L.length-1?' last':''}"><span class="mf-n">${k+1}</span><span class="mf-name">${g.s.n}</span><span class="mf-leg">+${g.l}</span><span class="mf-cum">${g.cum}</span></li>`; });
  for(let k=L.length;k<P.stops.length;k++){
    h+=`<li class="mf-row todo${k===L.length?' next':''}"><span class="mf-n">${k+1}</span><span class="mf-name">${k===L.length?(narrow?'Next':'Tap the next stop'):'—'}</span><span class="mf-leg"></span><span class="mf-cum"></span></li>`;
  }
  if(!narrow) h+=`<li class="mf-row back"><span class="mf-n">${KIND==='night'?'RT':'↩'}</span><span class="mf-name">Back to depot</span><span class="mf-leg"></span><span class="mf-cum"></span></li>`;
  return h+'</ol>';
}

function game(narrow){
  const driven=legs().at(-1).cum;
  const head = KIND==='night'
    ? `<header class="g-top"><span class="brand">Tournée</span><span class="stat"><i>Round</i>18.11</span><span class="stat"><i>Shift</i>00:42</span><span class="stat"><i>Streak</i>06</span></header>`
    : `<header class="g-top"><span class="brand">Tournée</span><span class="g-date">Wed 18 Nov</span><span class="g-meta"><span class="clock">00:42</span><span class="streak">Streak <b>6</b></span></span></header>`;
  const cartouche = KIND==='calque' ? `<div class="cart"><div><i>Sheet</i>18.11.2026</div><div><i>Driven</i>${driven} blk</div><div><i>Clock</i>00:42</div><div><i>Streak</i>6</div></div>` : '';
  return `<div class="g ${narrow?'g--narrow':'g--wide'}">${head}
  <p class="g-rule">Visit all 6 stops, then drive back to the depot. <b>Shortest round wins.</b></p>
  <div class="g-body">
    <div class="g-map"><div class="map">${mapSVG()}</div>${cartouche}</div>
    <div class="g-side">
      ${manifest(narrow)}
      <div class="g-total"><span>Driven <b>${driven}</b> blocks</span><span class="g-left">2 stops left</span></div>
      <div class="g-actions"><button class="btn ghost">Undo</button><button class="btn primary" disabled>Send route <span class="cnt">4/6</span></button></div>
    </div>
  </div></div>`;
}

document.querySelectorAll('[data-game]').forEach(el=>{ el.innerHTML = game(el.dataset.game==='narrow'); });
"""

# ---------------------------------------------------------------- chrome
CHROME_CSS = r"""
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1440px;height:900px;overflow:hidden}
body{background:#e4e2dd;color:#1f1f1f;font:13px/1.4 -apple-system,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif}
button{font:inherit;cursor:pointer}
.bd-head{position:absolute;left:40px;top:26px;right:40px;display:flex;align-items:flex-end;gap:28px}
.bd-title{font-size:22px;font-weight:700;letter-spacing:-.01em}
.bd-title small{display:block;font-size:11px;font-weight:600;letter-spacing:.12em;text-transform:uppercase;color:#6d6a63;margin-bottom:4px}
.bd-spec{display:flex;gap:18px;align-items:center;font-size:11.5px;color:#4b4944;margin-left:auto}
.sw{display:inline-flex;align-items:center;gap:6px}
.sw i{width:16px;height:16px;border-radius:3px;display:inline-block;border:1px solid rgba(0,0,0,.12)}
.cap{position:absolute;font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;color:#6d6a63;font-weight:600}
.frame{position:absolute;transform-origin:0 0;overflow:hidden;background:#f3f4f5;box-shadow:0 0 0 1px rgba(0,0,0,.08),0 24px 48px -24px rgba(0,0,0,.35)}
.desk{width:1440px;height:900px;left:40px;top:116px;transform:scale(.62);border-radius:14px}
.mob{width:390px;height:844px;left:1058px;top:74px;transform:scale(.94);border-radius:44px;border:10px solid #1b1b1d}
/* generic feed chrome, intentionally neutral */
.dk-top{height:56px;background:#fff;border-bottom:1px solid #e3e5e8;display:flex;align-items:center;gap:20px;padding:0 24px}
.dk-logo{width:110px;height:22px;border-radius:6px;background:#d9dcdf}
.dk-search{flex:0 0 520px;margin:0 auto;height:38px;border-radius:19px;background:#eef0f2;color:#8a8f95;display:flex;align-items:center;padding:0 18px;font-size:14px}
.dk-user{width:32px;height:32px;border-radius:50%;background:#d9dcdf}
.dk-main{display:flex;gap:24px;padding:20px 24px}
.dk-rail{width:220px;display:flex;flex-direction:column;gap:12px;padding-top:6px}
.dk-rail span{height:14px;border-radius:7px;background:#dfe2e5}
.dk-rail span:nth-child(2n){width:70%}
.dk-feed{width:760px;margin-left:90px}
.dk-aside{width:300px;background:#fff;border-radius:12px;height:240px;padding:18px;display:flex;flex-direction:column;gap:10px}
.dk-aside span{height:12px;border-radius:6px;background:#e5e8ea}.dk-aside span:first-child{width:60%;height:16px;background:#d6d9dc}
.post{background:#fff;border-radius:12px;padding:14px 10px 10px}
.post-hd{display:flex;align-items:center;gap:8px;font-size:12px;color:#62676d;padding:0 6px}
.post-hd .av{width:24px;height:24px;border-radius:50%;background:#c9cdd1}
.post-hd b{color:#1f1f1f}
.post-title{font-size:19px;font-weight:600;padding:8px 6px 12px;letter-spacing:-.005em}
.post-game{border-radius:10px;overflow:hidden}
.post-act{display:flex;gap:8px;padding:10px 4px 0}
.post-act span{height:32px;padding:0 14px;border-radius:16px;background:#eef0f2;display:flex;align-items:center;font-size:12.5px;font-weight:600;color:#3c4043}
.mb-status{height:44px;display:flex;justify-content:space-between;align-items:center;padding:0 26px;font-size:14px;font-weight:600;background:#fff}
.mb-status i{width:60px;height:12px;border-radius:6px;background:#1b1b1d;opacity:.85}
.mb-bar{height:48px;background:#fff;display:flex;align-items:center;gap:12px;padding:0 14px;border-bottom:1px solid #e9ebed}
.mb-bar .a{width:22px;height:22px;border-radius:6px;background:#d9dcdf}.mb-bar .s{flex:1;height:32px;border-radius:16px;background:#eef0f2}
.mob .post{border-radius:0;padding:10px 0 0}
.mob .post-hd{padding:0 12px}.mob .post-title{font-size:16px;padding:6px 12px 8px}
.mob .post-game{border-radius:0}
.mob .post-act{padding:8px 10px}
.notes{position:absolute;left:40px;top:690px;width:893px;display:grid;grid-template-columns:1.35fr 1fr 1fr 1fr;gap:14px}
.note{background:#f4f3f0;border-radius:10px;padding:12px 14px;font-size:11.5px;color:#45433f;line-height:1.45}
.note h4{font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;color:#1f1f1f;margin-bottom:6px}
.note svg{width:30px;height:30px;float:left;margin:0 10px 4px 0}
"""

BODY = r"""
<div class="bd-head">
  <div class="bd-title"><small>Tournée · page Jeu · planche v1 / %%NUM%%</small>%%NAME%%</div>
  <div class="bd-spec">%%SWATCHES%%<span>%%TYPE%%</span></div>
</div>
<div class="cap" style="left:40px;top:96px">Desktop 1440 × 900 · affiché à 62 %</div>
<div class="cap" style="left:1058px;top:56px;display:none">Mobile</div>

<div class="frame desk">
  <div class="dk-top"><div class="dk-logo"></div><div class="dk-search">Search</div><div class="dk-user"></div></div>
  <div class="dk-main">
    <aside class="dk-rail"><span></span><span></span><span></span><span></span><span></span><span></span><span></span></aside>
    <section class="dk-feed"><article class="post">
      <div class="post-hd"><span class="av"></span><b>r/TourneeDaily</b><span>· 3 h</span></div>
      <h2 class="post-title">Today's delivery round · Wed 18 Nov</h2>
      <div class="post-game" data-game="wide"></div>
      <div class="post-act"><span>Vote</span><span>214 comments</span><span>Share</span></div>
    </article></section>
    <aside class="dk-aside"><span></span><span></span><span></span><span></span><span></span></aside>
  </div>
</div>

<div class="frame mob">
  <div class="mb-status"><span>9:41</span><i></i></div>
  <div class="mb-bar"><span class="a"></span><span class="s"></span><span class="a"></span></div>
  <article class="post">
    <div class="post-hd"><span class="av"></span><b>r/TourneeDaily</b><span>· 3 h</span></div>
    <h2 class="post-title">Today's delivery round · Wed 18 Nov</h2>
    <div class="post-game" data-game="narrow"></div>
    <div class="post-act"><span>Vote</span><span>214</span><span>Share</span></div>
  </article>
</div>
<div class="cap" style="left:1058px;top:880px;display:none"></div>

<div class="notes">
  <div class="note"><h4>Intention</h4>%%INTENT%%</div>
  %%NOTES%%
</div>
"""

DIRECTIONS = [
    dict(
        num="01", slug="carte-pliee", kind="fold", name="Carte pliée",
        swatches=[("#f1eada", "carte"), ("#3a6ea5", "route"), ("#c8322b", "arrêt · accent"), ("#23303d", "encre")],
        type="Sans de signalétique + mono pour les horaires",
        intent="La direction de départ, poussée jusqu'au bout : un plan de ville papier, plié en six, avec ses plis visibles. La route se trace en bleu comme au feutre ; le rouge est réservé aux arrêts et au bouton d'envoi.",
        notes=[
            ("Arrêt à livrer", '<svg viewBox="-.5 -.5 1 1"><circle cx="0" cy="0" r=".3" fill="#f6f0e2" stroke="#c8322b" stroke-width=".07"/></svg>Cercle vide, nom en clair à côté. Toute la cible est touchable (44 px).'),
            ("Arrêt placé", '<svg viewBox="-.5 -.5 1 1"><circle cx="0" cy="0" r=".46" fill="none" stroke="#c8322b" stroke-opacity=".35" stroke-width=".05"/><circle cx="0" cy="0" r=".3" fill="#c8322b"/><text x="0" y=".11" font-size=".34" font-weight="800" text-anchor="middle" fill="#fff" font-family="Arial">4</text></svg>Rempli, numéro d\'ordre. Le dernier posé garde un halo : c\'est lui qu\'Undo retire.'),
            ("Envoi verrouillé", "« Send route 4/6 » reste désactivé tant que les 6 arrêts ne sont pas placés : le compteur dit pourquoi."),
        ],
        css=r"""
.g{--paper:#f6f0e2;--map:#f1eada;--blk:#e5dac3;--park:#d8d8bb;--ink:#23303d;--muted:#6f6a5c;--line:#dccfb4;--route:#3a6ea5;--accent:#c8322b;
  background:var(--paper);color:var(--ink);font-family:"Helvetica Neue","Arial Nova",Arial,sans-serif;padding:18px 20px 20px}
.g-top{display:flex;align-items:center;gap:12px}
.brand{background:var(--ink);color:#f6f0e2;font-weight:700;font-size:15px;letter-spacing:.06em;text-transform:uppercase;padding:5px 10px 4px;border-radius:4px;box-shadow:inset 0 0 0 2px var(--ink),inset 0 0 0 3px #f6f0e2}
.g-date{font-size:12px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--muted)}
.g-meta{margin-left:auto;display:flex;gap:14px;align-items:center;font-size:12px;font-weight:700;letter-spacing:.08em;text-transform:uppercase}
.clock{font-family:ui-monospace,"JetBrains Mono",Menlo,monospace;font-size:15px;letter-spacing:0;background:#fff;border:1px solid var(--line);border-radius:4px;padding:3px 7px}
.streak b{color:var(--accent);font-size:15px}
.g-rule{margin:12px 0 14px;font-size:13.5px;color:var(--muted)}.g-rule b{color:var(--ink)}
.g-body{display:grid;grid-template-columns:420px 1fr;gap:22px;align-items:start}
.map{position:relative;background:var(--map);border:1px solid var(--line);border-radius:3px;box-shadow:0 14px 26px -18px rgba(35,48,61,.55)}
.map::after{content:"";position:absolute;inset:0;pointer-events:none;
 background:linear-gradient(90deg,transparent calc(33.33% - 2px),rgba(35,48,61,.13) 33.33%,rgba(255,255,255,.7) calc(33.33% + 1px),transparent calc(33.33% + 3px),transparent calc(66.66% - 2px),rgba(35,48,61,.13) 66.66%,rgba(255,255,255,.7) calc(66.66% + 1px),transparent calc(66.66% + 3px)),
 linear-gradient(180deg,transparent calc(50% - 2px),rgba(35,48,61,.15) 50%,rgba(255,255,255,.7) calc(50% + 1px),transparent calc(50% + 3px)),
 linear-gradient(90deg,rgba(35,48,61,.04) 0 33.33%,transparent 33.33% 66.66%,rgba(35,48,61,.04) 66.66%),
 linear-gradient(180deg,rgba(255,255,255,.18) 0 50%,transparent 50%)}
.map-svg{display:block;width:100%;height:auto}
.blk{fill:var(--blk)}.blk.park{fill:var(--park)}
.route-case{fill:none;stroke:#fffaf0;stroke-width:.27;stroke-linejoin:round;stroke-linecap:round}
.route{fill:none;stroke:var(--route);stroke-width:.14;stroke-linejoin:round;stroke-linecap:round}
.mk.todo{fill:#fffaf0;stroke:var(--accent);stroke-width:.07}.mk.on{fill:var(--accent)}
.mk.ring{fill:none;stroke:var(--accent);stroke-opacity:.35;stroke-width:.05}
.mk-n{font:800 .32px Arial,sans-serif;fill:#fff;text-anchor:middle}
.dp{fill:var(--ink)}.dp-t{font:800 .3px Arial,sans-serif;fill:#f6f0e2;text-anchor:middle}
.lbl{font:700 .27px "Helvetica Neue",Arial,sans-serif;fill:var(--ink);paint-order:stroke;stroke:var(--map);stroke-width:.08}
.lbl-todo{fill:var(--accent)}
.mf{list-style:none;border-top:2px solid var(--ink)}
.mf-row{display:grid;grid-template-columns:26px 1fr 40px 34px;align-items:center;height:38px;border-bottom:1px dashed var(--line);font-size:14px}
.mf-n{font-family:ui-monospace,Menlo,monospace;font-weight:700;color:var(--muted)}
.mf-name{font-weight:700}
.mf-leg{font-family:ui-monospace,Menlo,monospace;color:var(--route);text-align:right}
.mf-cum{font-family:ui-monospace,Menlo,monospace;font-weight:700;text-align:right}
.mf-row.last .mf-n{color:var(--accent)}
.mf-row.todo .mf-name{color:#a59d8a;font-weight:400}
.mf-row.next .mf-name{color:var(--accent);font-weight:700}
.mf-row.back{border-bottom:2px solid var(--ink)}.mf-row.back .mf-name{font-weight:400;color:var(--muted)}
.g-total{display:flex;justify-content:space-between;margin:12px 0 16px;font-size:13px;color:var(--muted)}
.g-total b{font-family:ui-monospace,Menlo,monospace;font-size:20px;color:var(--ink)}
.g-actions{display:flex;gap:10px}
.btn{height:48px;border-radius:6px;font-weight:800;font-size:13px;letter-spacing:.1em;text-transform:uppercase}
.btn.ghost{width:100px;background:transparent;border:2px solid var(--ink);color:var(--ink)}
.btn.primary{flex:1;background:var(--accent);color:#fff;border:0}
.btn.primary[disabled]{background:#e7d9cf;color:#9d6f66;cursor:not-allowed}
.cnt{font-family:ui-monospace,Menlo,monospace;letter-spacing:0;margin-left:6px}
.g--narrow{padding:12px 14px 14px}.g--narrow .g-date{display:none}
.g--narrow .g-rule{margin:8px 0 10px;font-size:12.5px}
.g--narrow .g-body{grid-template-columns:1fr;gap:10px}
.g--narrow .mf{display:grid;grid-template-columns:repeat(3,1fr);column-gap:10px;border-top-width:2px}
.g--narrow .mf-row{grid-template-columns:18px 1fr 28px;height:28px;font-size:12.5px}.g--narrow .mf-cum{display:none}
.g--narrow .g-total{margin:8px 0 10px}.g--narrow .g-total b{font-size:16px}
.g--narrow .btn{height:44px}.g--narrow .btn.ghost{width:86px}
""",
    ),
    dict(
        num="02", slug="calque", kind="calque", name="Calque d'architecte",
        swatches=[("#fbfaf6", "calque"), ("#c8322b", "encre unique"), ("#2a2422", "texte")],
        type="Grotesque fine + mono pour les cotes",
        intent="La tournée comme un relevé technique : un seul trait d'encre rouge au filet, des cotes de distance posées sur chaque tronçon, un cartouche de plan. Le plaisir de l'ordre devient littéral : chaque bloc est mesuré.",
        notes=[
            ("Cotes", "Chaque tronçon tracé affiche sa longueur en blocs, comme une cote d'architecte. On lit la tournée sans ouvrir le manifeste."),
            ("Arrêt placé", '<svg viewBox="-.5 -.5 1 1"><line x1="-.45" y1="0" x2=".45" y2="0" stroke="#c8322b" stroke-width=".02"/><line x1="0" y1="-.45" x2="0" y2=".45" stroke="#c8322b" stroke-width=".02"/><circle cx="0" cy="0" r=".25" fill="#c8322b"/><text x="0" y=".1" font-size=".28" text-anchor="middle" fill="#fbfaf6" font-family="monospace">4</text></svg>Point de repère en croix ; rempli à l\'encre une fois placé.'),
            ("Cartouche", "Le bloc-titre du plan porte date, distance, horloge et série : les infos de partie sortent du chrome et deviennent dessin."),
        ],
        css=r"""
.g{--bg:#fbfaf6;--ink:#c8322b;--text:#2a2422;--muted:#958a83;--hair:rgba(200,50,43,.42);--faint:rgba(200,50,43,.12);
  background:var(--bg);color:var(--text);font-family:"Helvetica Neue","Arial Nova",Arial,sans-serif;font-weight:300;padding:18px 22px 20px;position:relative}
.g::before{content:"";position:absolute;inset:8px;border:1px solid var(--hair);pointer-events:none}
.g-top{display:flex;align-items:baseline;gap:14px;color:var(--ink)}
.brand{font-size:22px;font-weight:300;letter-spacing:-.01em}
.g-date{font-size:11px;letter-spacing:.14em;text-transform:uppercase}
.g-meta{margin-left:auto;display:flex;gap:16px;font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--ink)}
.clock{font-family:ui-monospace,Menlo,monospace;letter-spacing:.04em}
.g-rule{margin:8px 0 14px;font-size:13.5px;color:var(--text)}.g-rule b{font-weight:500;color:var(--ink)}
.g-body{display:grid;grid-template-columns:420px 1fr;gap:26px;align-items:start}
.g-map{position:relative}
.map{border-top:1px solid var(--ink);border-bottom:1px solid var(--ink)}
.map-svg{display:block;width:100%;height:auto}
.minor{stroke:var(--faint);stroke-width:.01}.st{stroke:var(--hair);stroke-width:.018}
.hatch{stroke:var(--hair);stroke-width:.018}.park{fill:url(#hatch);stroke:var(--hair);stroke-width:.015}
.route{fill:none;stroke:var(--ink);stroke-width:.065;stroke-linejoin:miter}
.dim text{font:400 .26px ui-monospace,Menlo,monospace;fill:var(--ink);text-anchor:middle;paint-order:stroke;stroke:var(--bg);stroke-width:.12}
.mk-x{stroke:var(--ink);stroke-width:.015}
.mk.todo{fill:var(--bg);stroke:var(--ink);stroke-width:.03}.mk.on{fill:var(--ink)}
.mk.ring{fill:none;stroke:var(--ink);stroke-width:.015;stroke-dasharray:.05 .05}
.mk-n{font:500 .24px ui-monospace,Menlo,monospace;fill:var(--bg);text-anchor:middle}
.dp{fill:var(--bg);stroke:var(--ink);stroke-width:.03}.dp2{fill:var(--ink)}
.lbl{font:400 .24px "Helvetica Neue",Arial,sans-serif;fill:var(--text);letter-spacing:.01px;paint-order:stroke;stroke:var(--bg);stroke-width:.1}
.lbl-todo{fill:var(--ink)}
.cart{display:grid;grid-template-columns:repeat(4,1fr);border-bottom:1px solid var(--ink);font-family:ui-monospace,Menlo,monospace;font-size:12px;color:var(--text)}
.cart div{padding:6px 8px;border-right:1px solid var(--hair)}.cart div:last-child{border-right:0}
.cart i{display:block;font-style:normal;font-family:"Helvetica Neue",Arial,sans-serif;font-size:9px;letter-spacing:.14em;text-transform:uppercase;color:var(--ink)}
.mf{list-style:none;border-top:1px solid var(--ink)}
.mf-row{display:grid;grid-template-columns:28px 1fr 40px 36px;align-items:center;height:38px;border-bottom:1px solid var(--faint);font-size:14px}
.mf-n,.mf-leg,.mf-cum{font-family:ui-monospace,Menlo,monospace;font-size:12.5px}
.mf-n{color:var(--ink)}.mf-leg{text-align:right;color:var(--muted)}.mf-cum{text-align:right;color:var(--ink)}
.mf-row.last .mf-name{font-weight:500}
.mf-row.todo .mf-name{color:var(--muted)}
.mf-row.next .mf-name{color:var(--ink)}
.mf-row.back{border-bottom:1px solid var(--ink)}.mf-row.back .mf-name{color:var(--muted)}
.g-total{display:flex;justify-content:space-between;align-items:baseline;margin:14px 0 18px;font-size:12px;letter-spacing:.1em;text-transform:uppercase;color:var(--muted)}
.g-total b{font-family:ui-monospace,Menlo,monospace;font-weight:400;font-size:26px;letter-spacing:0;color:var(--ink)}
.g-actions{display:flex;gap:10px}
.btn{height:48px;border-radius:0;font-weight:400;font-size:12px;letter-spacing:.16em;text-transform:uppercase}
.btn.ghost{width:100px;background:transparent;border:1px solid var(--ink);color:var(--ink)}
.btn.primary{flex:1;background:var(--ink);color:var(--bg);border:1px solid var(--ink)}
.btn.primary[disabled]{background:transparent;color:var(--hair);border:1px dashed var(--hair);cursor:not-allowed}
.cnt{font-family:ui-monospace,Menlo,monospace;letter-spacing:0;margin-left:6px}
.g--narrow{padding:14px 16px 16px}.g--narrow::before{inset:6px}
.g--narrow .brand{font-size:19px}.g--narrow .g-date{display:none}
.g--narrow .g-meta .streak{display:none}
.g--narrow .g-rule{margin:6px 0 8px;font-size:12.5px}
.g--narrow .g-body{grid-template-columns:1fr;gap:8px}
.g--narrow .cart{font-size:11px}.g--narrow .cart div{padding:4px 6px}
.g--narrow .mf{display:grid;grid-template-columns:repeat(3,1fr);column-gap:10px}
.g--narrow .mf-row{grid-template-columns:18px 1fr 26px;height:27px;font-size:12.5px}.g--narrow .mf-cum{display:none}
.g--narrow .g-total{display:none}
.g--narrow .g-actions{margin-top:10px}.g--narrow .btn{height:44px}.g--narrow .btn.ghost{width:86px}
""",
    ),
    dict(
        num="03", slug="nuit-dispatch", kind="night", name="Dispatch de nuit (écart)",
        swatches=[("#121417", "asphalte"), ("#1c2025", "îlot"), ("#f2b33d", "sodium · accent"), ("#e8eaed", "texte")],
        type="Sans neutre + mono dominant (console)",
        intent="L'écart assumé : on quitte le papier pour l'outil du répartiteur, dense comme une console. Les îlots sont des tuiles, la tournée s'allume en jaune sodium comme une rue de nuit, chaque arrêt porte un code de deux lettres.",
        notes=[
            ("Arrêt codé", '<svg viewBox="-.5 -.5 1 1"><rect x="-.3" y="-.3" width=".6" height=".6" rx=".07" fill="#121417" stroke="#5d646d" stroke-width=".035"/><text x="0" y=".08" font-size=".22" text-anchor="middle" fill="#c9ced4" font-family="monospace" font-weight="700">SC</text></svg>Deux lettres sur la carte, nom complet dans le manifeste : lisible à 12 px.'),
            ("Manifeste", "Tableau dense façon outil : ordre, arrêt, tronçon, cumul. La hiérarchie vient du poids et de l'accent, pas de la taille."),
            ("Pourquoi l'écart", "Le feed Reddit est clair : un post sombre tranche au défilement, et le jeu « logistique » se sent comme un vrai poste de travail."),
        ],
        css=r"""
.g{--bg:#121417;--tile:#1c2025;--park:#1d2620;--line:#2a2f35;--text:#e8eaed;--muted:#8a919a;--accent:#f2b33d;
  background:var(--bg);color:var(--text);font-family:Inter,"Helvetica Neue",Arial,sans-serif;padding:0 0 18px}
.g-top{display:flex;align-items:stretch;border-bottom:1px solid var(--line);height:42px}
.brand{display:flex;align-items:center;padding:0 16px;font-weight:700;font-size:15px;letter-spacing:.01em;border-right:1px solid var(--line)}
.stat{display:flex;flex-direction:column;justify-content:center;padding:0 14px;border-right:1px solid var(--line);font:600 13px ui-monospace,Menlo,monospace}
.stat i{font-style:normal;font:600 9px Inter,Arial,sans-serif;letter-spacing:.14em;text-transform:uppercase;color:var(--muted)}
.stat:last-child{margin-left:auto;border-right:0;border-left:1px solid var(--line);color:var(--accent)}
.g-rule{margin:12px 16px 12px;font-size:13px;color:var(--muted)}.g-rule b{color:var(--text);font-weight:600}
.g-body{display:grid;grid-template-columns:380px 1fr;gap:18px;align-items:start;padding:0 16px}
.map{background:var(--bg);border:1px solid var(--line);border-radius:6px}
.map-svg{display:block;width:100%;height:auto}
.blk{fill:var(--tile)}.blk.park{fill:var(--park)}
.route-case{fill:none;stroke:rgba(242,179,61,.18);stroke-width:.34;stroke-linejoin:round;stroke-linecap:round}
.route{fill:none;stroke:var(--accent);stroke-width:.11;stroke-linejoin:round;stroke-linecap:round}
.mk.todo{fill:var(--bg);stroke:#5d646d;stroke-width:.03}.mk.on{fill:var(--accent)}
.mk.ring{fill:none;stroke:var(--accent);stroke-width:.025;stroke-dasharray:.08 .06}
.mk-n{font:800 .3px ui-monospace,Menlo,monospace;fill:#121417;text-anchor:middle}
.mk-c{font:700 .2px ui-monospace,Menlo,monospace;fill:#c9ced4;text-anchor:middle}
.dp{fill:var(--text)}.dp-t{font:800 .2px ui-monospace,Menlo,monospace;fill:#121417;text-anchor:middle}
.lbl{font:600 .2px ui-monospace,Menlo,monospace;fill:var(--muted);letter-spacing:.01px;paint-order:stroke;stroke:var(--bg);stroke-width:.08}
.lbl-todo{fill:#c9ced4}
.mf{list-style:none;border:1px solid var(--line);border-radius:6px;overflow:hidden}
.mf::before{content:"#   Stop                 Leg   Cum";display:block;white-space:pre;padding:7px 12px;font:600 9.5px ui-monospace,Menlo,monospace;letter-spacing:.12em;text-transform:uppercase;color:var(--muted);background:#171a1e;border-bottom:1px solid var(--line)}
.mf-row{display:grid;grid-template-columns:26px 1fr 40px 34px;align-items:center;height:36px;padding:0 10px;border-bottom:1px solid var(--line);font:500 13px ui-monospace,Menlo,monospace}
.mf-row:last-child{border-bottom:0}
.mf-n{color:var(--muted)}.mf-name{font-family:Inter,Arial,sans-serif;font-weight:600}
.mf-leg{text-align:right;color:var(--muted)}.mf-cum{text-align:right;font-weight:700}
.mf-row.last{background:rgba(242,179,61,.08)}.mf-row.last .mf-n,.mf-row.last .mf-cum{color:var(--accent)}
.mf-row.todo .mf-name{color:#5d646d;font-weight:400}
.mf-row.next .mf-name{color:var(--text);font-weight:400}.mf-row.next .mf-n{color:var(--accent)}
.mf-row.back .mf-name{color:var(--muted);font-weight:400}
.g-total{display:flex;justify-content:space-between;align-items:baseline;margin:12px 0 14px;font-size:12px;color:var(--muted)}
.g-total b{font:700 22px ui-monospace,Menlo,monospace;color:var(--text)}
.g-actions{display:flex;gap:8px}
.btn{height:46px;border-radius:6px;font-weight:700;font-size:13.5px}
.btn.ghost{width:96px;background:transparent;border:1px solid #3a4047;color:var(--text)}
.btn.primary{flex:1;background:var(--accent);color:#121417;border:0}
.btn.primary[disabled]{background:#22262b;color:#6d747c;cursor:not-allowed}
.cnt{font-family:ui-monospace,Menlo,monospace;margin-left:6px}
.g--narrow .stat{padding:0 10px}.g--narrow .brand{padding:0 12px}
.g--narrow .g-rule{margin:8px 12px;font-size:12.5px}
.g--narrow .g-body{grid-template-columns:1fr;gap:8px;padding:0 12px}
.g--narrow .mf{display:grid;grid-template-columns:repeat(3,1fr)}.g--narrow .mf::before{display:none}
.g--narrow .mf-row{grid-template-columns:16px 1fr 24px;height:30px;padding:0 8px;font-size:11.5px;border-right:1px solid var(--line)}
.g--narrow .mf-row:nth-child(3n){border-right:0}.g--narrow .mf-row:nth-child(n+4){border-bottom:0}
.g--narrow .mf-cum{display:none}.g--narrow .mf-name{font-size:12px}
.g--narrow .g-total{display:none}
.g--narrow .g-actions{margin-top:10px}.g--narrow .btn{height:44px}.g--narrow .btn.ghost{width:84px}
""",
    ),
]


def build(d):
    sw = "".join(f'<span class="sw"><i style="background:{c}"></i>{n} <code>{c}</code></span>' for c, n in d["swatches"])
    notes = "".join(f'<div class="note"><h4>{t}</h4>{b}</div>' for t, b in d["notes"])
    body = (BODY.replace("%%NUM%%", d["num"]).replace("%%NAME%%", d["name"])
            .replace("%%SWATCHES%%", sw).replace("%%TYPE%%", d["type"])
            .replace("%%INTENT%%", d["intent"]).replace("%%NOTES%%", notes))
    html = f"""<!doctype html>
<html lang="fr"><head><meta charset="utf-8">
<title>Tournée · Jeu · {d['num']} {d['name']}</title>
<meta name="viewport" content="width=1440">
<style>{CHROME_CSS}
/* ---- direction {d['num']} : {d['name']} ---- */
{d['css']}</style></head>
<body data-kind="{d['kind']}">{body}
<script>{JS}</script>
</body></html>
"""
    path = OUT / f"{d['num']}-{d['slug']}.html"
    path.write_text(html, encoding="utf-8")
    print(path.relative_to(ROOT))


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for d in DIRECTIONS:
        build(d)
