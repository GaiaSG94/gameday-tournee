"""V2 style boards for the Tournee game page, rebuilt from scratch.

Three directions, each grounded in a reference mechanic:
  A  Maquette  - Baseten: isometric pastel tile field, extruded blocks carrying data
  B  Salle     - PART: the post is a wire-drawn room, the city lies on its floor
  C  Feuilleton- narrative first: flat pixel-tile city + the shift told as a story
Output: G-DESIGN/planches/v2/*.html (standalone, no network).
Run: python3 tools/design/build_planches_v2.py
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "G-DESIGN" / "planches" / "v2"

# --------------------------------------------------------------------- data + helpers
COMMON_JS = r"""
const DEPOT={n:'Depot',x:0,y:0,ic:'house'};
const STOPS=[
 {n:'Post',x:1,y:5,ic:'mail',tint:'#dde8fb',tag:[-1,1]},
 {n:'Florist',x:4,y:0,ic:'flower',tint:'#f9dfe9',tag:[1,-1]},
 {n:'Library',x:6,y:1,ic:'book',tint:'#e6e0fa',tag:[1,-1]},
 {n:'Atelier',x:4,y:2,ic:'needle',tint:'#fbe7d3',tag:[1,-1]},
 {n:'Bakery',x:1,y:0,ic:'bread',tint:'#f5eccc',tag:[1,-1]},
 {n:'School',x:2,y:4,ic:'bell',tint:'#d9f0dc',tag:[-1,-1]}];
const ORDER=[4,1,2,3];
const KIND=document.body.dataset.kind;
const dist=(a,b)=>Math.abs(a.x-b.x)+Math.abs(a.y-b.y);
const hhmm=m=>String(Math.floor(m/60)).padStart(2,'0')+':'+String(m%60).padStart(2,'0');
const MIN_PER_BLOCK=3, START=6*60;
function legs(){let cur=DEPOT,cum=0;return ORDER.map(i=>{const s=STOPS[i],l=dist(cur,s);cum+=l;const o={i,s,from:cur,l,cum,t:hhmm(START+cum*MIN_PER_BLOCK)};cur=s;return o;});}
function routePts(){const p=[[0,0]];legs().forEach(g=>{p.push([g.s.x,g.from.y]);p.push([g.s.x,g.s.y]);});return p;}
// 5x5 pixel glyphs
const PIX={
 house:'00100 01110 11111 01010 01110', bread:'00000 01110 11111 10101 11111',
 flower:'01010 11111 01010 00100 01110', book:'11011 10101 10101 10101 11011',
 needle:'10001 01010 00100 01010 11011', mail:'11111 11011 10101 10001 11111',
 bell:'00100 01110 01110 11111 00100', van:'11100 10110 11111 11111 01010'};
function pix(name,x,y,u,fill){let s='';PIX[name].split(' ').forEach((row,r)=>[...row].forEach((c,k)=>{if(c==='1')s+=`<rect x="${(x+k*u).toFixed(3)}" y="${(y+r*u).toFixed(3)}" width="${u}" height="${u}" fill="${fill}"/>`;}));return s;}
function pixSvg(name,size,fill){return `<svg class="px" width="${size}" height="${size}" viewBox="0 0 5 5" shape-rendering="crispEdges">${pix(name,0,0,1,fill)}</svg>`;}
// constructed stroke type (own design: orthogonal + 45deg strokes on a 4x6 grid)
const GLY={
 T:[[[0,0],[4,0]],[[2,0],[2,6]]], O:[[[1,0],[3,0],[4,1],[4,5],[3,6],[1,6],[0,5],[0,1],[1,0]]],
 U:[[[0,0],[0,5],[1,6],[3,6],[4,5],[4,0]]], R:[[[0,6],[0,0],[3,0],[4,1],[4,2],[3,3],[0,3]],[[2,3],[4,6]]],
 N:[[[0,6],[0,0],[4,6],[4,0]]], E:[[[4,0],[0,0],[0,6],[4,6]],[[0,3],[3,3]]],
 'É':[[[4,0],[0,0],[0,6],[4,6]],[[0,3],[3,3]],[[1.5,-1],[3,-2.2]]],
 '0':[[[1,0],[3,0],[4,1],[4,5],[3,6],[1,6],[0,5],[0,1],[1,0]]],
 '1':[[[1,1],[2,0],[2,6]],[[1,6],[3,6]]], '2':[[[0,1],[1,0],[3,0],[4,1],[4,2],[0,6],[4,6]]],
 '3':[[[0,0],[4,0],[2,2.5],[3,2.5],[4,3.5],[4,5],[3,6],[1,6],[0,5]]], '4':[[[3,6],[3,0],[0,4],[4,4]]],
 '5':[[[4,0],[0,0],[0,2.5],[3,2.5],[4,3.5],[4,5],[3,6],[0,6]]],
 '6':[[[3,0],[1,0],[0,1],[0,5],[1,6],[3,6],[4,5],[4,3.5],[3,2.5],[0,2.5]]], '7':[[[0,0],[4,0],[1.5,6]]],
 '8':[[[1,3],[0,2],[0,1],[1,0],[3,0],[4,1],[4,2],[3,3],[1,3],[0,4],[0,5],[1,6],[3,6],[4,5],[4,4],[3,3]]],
 '9':[[[4,3.5],[1,3.5],[0,2.5],[0,1],[1,0],[3,0],[4,1],[4,5],[3,6],[1,6]]],
 ':':[[[2,1.5],[2,2]],[[2,4.5],[2,5]]], '/':[[[0,6],[4,0]]], ' ':[]};
function stroke(str,x,y,h,cls){const k=h/6;let s=`<g class="${cls||'ct'}" transform="translate(${x} ${y}) skewX(-14) scale(${k})">`;let cx=0;
 [...str].forEach(ch=>{(GLY[ch]||[]).forEach(pl=>{s+=`<polyline points="${pl.map(p=>(p[0]+cx)+','+p[1]).join(' ')}"/>`;});cx+=ch===' '?3.5:6;});
 return s+'</g>';}
function strokeW(str,h){return [...str].reduce((w,ch)=>w+(ch===' '?3.5:6),0)*h/6-h/6*2;}
"""

# --------------------------------------------------------------------- A : Maquette (iso)
A_JS = r"""
const ACC='#1f5cff';
const iso=(x,y,z=0)=>[(x-y),(x+y)*.5-z];
const P=(pts)=>pts.map(p=>p.map(v=>v.toFixed(3)).join(',')).join(' ');
function shade(hex,f){const n=parseInt(hex.slice(1),16);const c=[n>>16,(n>>8)&255,n&255].map(v=>Math.round(v*f));return '#'+c.map(v=>v.toString(16).padStart(2,'0')).join('');}
function prism(x0,y0,x1,y1,h,top,left,right,stroke,sw){
  const A=iso(x0,y0),B=iso(x1,y0),C=iso(x1,y1),D=iso(x0,y1);
  const up=p=>[p[0],p[1]-h];
  let s='';
  if(h>0){s+=`<polygon points="${P([D,C,up(C),up(D)])}" fill="${left}" stroke="${stroke}" stroke-width="${sw}" stroke-linejoin="round"/>`;
          s+=`<polygon points="${P([C,B,up(B),up(C)])}" fill="${right}" stroke="${stroke}" stroke-width="${sw}" stroke-linejoin="round"/>`;}
  s+=`<polygon points="${P([up(A),up(B),up(C),up(D)])}" fill="${top}" stroke="${stroke}" stroke-width="${sw}" stroke-linejoin="round"/>`;
  return s;}
const TINTS=['#e4f2df','#ece7f8','#e0eaf8','#f7eadb','#f1f1ec','#f1f1ec','#e4f2df'];
function hash(i,j){return ((i*73856093)^(j*19349663))>>>0;}
function isoMap(){
  let s=`<svg viewBox="-7.7 -1.9 16.1 9.3" class="iso" role="img" aria-label="Isometric city with depot and six stops">`;
  const g=.13;
  const cells=[];for(let i=0;i<7;i++)for(let j=0;j<7;j++)cells.push([i,j]);
  cells.sort((a,b)=>(a[0]+a[1])-(b[0]+b[1]));
  cells.forEach(([i,j])=>{const hv=hash(i,j);const t=TINTS[hv%TINTS.length];const h=[0,0,.12,.22,.36][hv%5];
    s+=prism(i+g,j+g,i+1-g,j+1-g,h,t,shade(t,.93),shade(t,.86),'#c5cbc2',.018);});
  const rp=routePts().map(p=>iso(p[0],p[1]));
  s+=`<polyline points="${P(rp)}" fill="none" stroke="#fff" stroke-width=".3" stroke-linejoin="round" stroke-linecap="round"/>`;
  s+=`<polyline points="${P(rp)}" fill="none" stroke="${ACC}" stroke-width=".14" stroke-linejoin="round" stroke-linecap="round"/>`;
  // next-leg hint: dashed from last stop
  const items=[{st:DEPOT,k:-2}].concat(STOPS.map((st,i)=>({st,k:ORDER.indexOf(i)})));
  items.sort((a,b)=>(a.st.x+a.st.y)-(b.st.x+b.st.y));
  const last=ORDER.length-1;
  items.forEach(({st,k})=>{
    const r=.24,{x,y}=st;
    if(k===last){const ring=[iso(x-.55,y-.55),iso(x+.55,y-.55),iso(x+.55,y+.55),iso(x-.55,y+.55)];s+=`<polygon points="${P(ring)}" fill="none" stroke="${ACC}" stroke-width=".035" stroke-dasharray=".12 .08"/>`;}
    if(k===-2) s+=prism(x-.3,y-.3,x+.3,y+.3,.55,'#2b2b2b','#111','#1d1d1d','#111',.02);
    else if(k<0) s+=prism(x-r,y-r,x+r,y+r,1.05,'#ffffff','#f0f0ec','#e0e0da','#111',.025);
    else s+=prism(x-r,y-r,x+r,y+r,1.05,'#6f95ff',ACC,'#1746c9','#0b2a86',.02);
    const C=iso(x+r,y+r), B=iso(x+r,y-r);
    if(k>=0){const mx=(C[0]+B[0])/2, my=(C[1]+B[1])/2-.55;
      s+=`<text x="${mx}" y="${my+.14}" transform="rotate(0)" class="face" style="transform-box:fill-box;transform-origin:center;transform:skewY(-26.565deg)">${k+1}</text>`;}
    // tag
    const top=iso(x,y,k===-2?.55:1.05);
    const side=k===-2?-1:st.tag[0], vy=k===-2?-1:st.tag[1];
    const tx=top[0]+side*.55, ty=top[1]+(vy<0?-.55:.9);
    const label=(k===-2?'Depot':st.n).toUpperCase();
    const w=.72+label.length*.255;
    const rx=side>0?tx:tx-w;
    s+=`<line x1="${top[0]}" y1="${top[1]}" x2="${side>0?rx:rx+w}" y2="${ty}" stroke="#111" stroke-width=".018"/>`;
    s+=`<rect x="${rx}" y="${ty-.29}" width="${w}" height=".58" fill="${k>=0||k===-2?'#fff':'#fff'}" stroke="#111" stroke-width=".02"/>`;
    s+=pix(k===-2?'house':st.ic,rx+.1,ty-.19,.075,k>=0?ACC:'#111');
    s+=`<text x="${rx+.6}" y="${ty+.125}" class="tag${k<0&&k!==-2?' todo':''}">${label}</text>`;
  });
  return s+'</svg>';}
function game(narrow){
  const L=legs();
  let log=`<div class="log-hd"><span>Shift log</span><span>18 Nov</span></div><ol class="log">`;
  if(!narrow) log+=`<li class="lr dp"><span class="t">06:00</span><span class="ic">${pixSvg('house',15,'#111')}</span><span class="n">Depot</span><span class="d">van out</span></li>`;
  L.forEach((g,k)=>{log+=`<li class="lr done${k===L.length-1?' last':''}"><span class="t">${g.t}</span><span class="ic" style="background:${g.s.tint}">${pixSvg(g.s.ic,15,'#111')}</span><span class="n">${g.s.n}</span><span class="d">+${g.l}</span></li>`;});
  log+=`<li class="lr next"><span class="t">--:--</span><span class="ic"></span><span class="n">Tap your next stop</span><span class="d">▸</span></li>`;
  log+=`<li class="lr todo"><span class="t">--:--</span><span class="ic"></span><span class="n">1 more parcel</span><span class="d"></span></li></ol>`;
  return `<div class="g ${narrow?'nw':'wd'}">
  <header class="hd"><span class="brand">${pixSvg('van',18,'#111')}Tournée</span><span class="hs"><b>00:42</b><i>clock</i></span><span class="hs"><b>6</b><i>streak</i></span></header>
  <p class="lede">Six parcels, one van. Tap the stops in the order you'll drive them. Shortest round home wins.</p>
  <div class="bd"><div class="field">${isoMap()}</div>
   <div class="panel">${log}
    <div class="sum"><span><b>${L.at(-1).cum}</b> blocks driven</span><span>2 parcels left</span></div>
    <div class="acts"><button class="b2">Undo</button><button class="b1" disabled><span>Send route</span><span class="c">4/6 ▸</span></button></div>
   </div></div></div>`;}
"""

A_CSS = r"""
.g{--ink:#111;--mut:#7b7d78;--acc:#1f5cff;--line:#d6d8d2;background:#fafaf7;background-image:radial-gradient(#d9dad4 1px,transparent 1.2px);background-size:9px 9px;color:var(--ink);font-family:"Helvetica Neue",Arial,sans-serif;padding:16px 18px 18px}
.hd{display:flex;align-items:center;gap:0;background:#fff;border:1px solid var(--ink)}
.brand{display:flex;align-items:center;gap:10px;font-weight:600;font-size:17px;letter-spacing:-.01em;padding:8px 12px;margin-right:auto}
.hs{display:flex;flex-direction:column;align-items:flex-end;padding:5px 12px;border-left:1px solid var(--ink);line-height:1.05}
.hs b{font:600 16px ui-monospace,Menlo,monospace}.hs i{font-style:normal;font-size:9.5px;letter-spacing:.08em;text-transform:uppercase;color:var(--mut)}
.lede{background:#fff;border:1px solid var(--ink);border-top:0;padding:8px 12px;font-size:13px;line-height:1.35;max-width:62%}
.bd{display:grid;grid-template-columns:1fr 252px;gap:0;align-items:start;margin-top:-8px}
.iso{display:block;width:100%;height:auto}
.iso .face{font:700 .5px ui-monospace,Menlo,monospace;fill:#fff;text-anchor:middle}
.iso .tag{font:600 .36px "Helvetica Neue",Arial,sans-serif;letter-spacing:.02px;fill:#111}
.iso .tag.todo{fill:#111}
.panel{background:#fff;border:1px solid var(--ink);margin-top:42px}
.log-hd{display:flex;justify-content:space-between;padding:8px 12px;border-bottom:1px solid var(--ink);font-size:10px;letter-spacing:.1em;text-transform:uppercase;color:var(--mut)}
.log{list-style:none}
.lr{display:grid;grid-template-columns:44px 22px 1fr 34px;align-items:center;gap:8px;height:32px;padding:0 12px;border-bottom:1px solid var(--line);font-size:13px}
.lr .t{font:500 12px ui-monospace,Menlo,monospace;color:var(--mut)}
.lr .ic{width:22px;height:22px;display:flex;align-items:center;justify-content:center;border:1px solid rgba(0,0,0,.08)}
.lr .ic:empty{border:1px dashed #b9bbb4}
.lr .d{font:500 12px ui-monospace,Menlo,monospace;text-align:right;color:var(--mut)}
.lr.done .n{font-weight:600}.lr.last .d,.lr.last .t{color:var(--acc)}
.lr.dp .n{font-weight:600}.lr.dp .d{font-family:inherit;font-size:11px}
.lr.next{background:#eef3ff}.lr.next .n{color:var(--acc);font-weight:600}.lr.next .d{color:var(--acc)}
.lr.todo .n{color:#a3a59e}
.sum{display:flex;justify-content:space-between;align-items:baseline;padding:10px 12px;font-size:11.5px;color:var(--mut)}
.sum b{font:600 22px ui-monospace,Menlo,monospace;color:var(--ink);margin-right:4px}
.acts{display:grid;grid-template-columns:84px 1fr;border-top:1px solid var(--ink)}
.acts button{height:44px;border:0;font-size:13px;font-weight:600;text-align:left;padding:0 12px}
.b2{background:#fff;border-right:1px solid var(--ink)!important;color:var(--ink)}
.b1{background:var(--ink);color:#fff;display:flex;justify-content:space-between;align-items:center}
.b1[disabled]{background:#ecece7;color:#9b9d96;cursor:not-allowed}
.b1 .c{font-family:ui-monospace,Menlo,monospace}
.nw{padding:10px 12px 12px}
.nw .lede{max-width:none;font-size:12.5px}
.nw .bd{grid-template-columns:1fr;margin-top:0}
.nw .field{margin:2px -6px -6px}
.nw .panel{margin-top:0}
.nw .lr{height:27px;font-size:12.5px;grid-template-columns:40px 20px 1fr 30px}
.nw .lr .ic{width:20px;height:20px}
.nw .sum{padding:6px 12px}.nw .sum b{font-size:18px}
"""

# --------------------------------------------------------------------- B : Salle (PART)
B_JS = r"""
function room(W,H,cfg){
  const {bx0,bx1,by0,by1,floorY}=cfg; // back wall rect; floor front edge y
  let s=`<svg viewBox="0 0 ${W} ${H}" class="room" role="img" aria-label="Wire room, city map on the floor">`;
  const fl=floorY;
  // frame + room edges
  s+=`<rect x=".5" y=".5" width="${W-1}" height="${fl-1}" class="hl"/>`;
  s+=`<rect x="${bx0}" y="${by0}" width="${bx1-bx0}" height="${by1-by0}" class="hl"/>`;
  [[0,0,bx0,by0],[W,0,bx1,by0],[0,fl,bx0,by1],[W,fl,bx1,by1]].forEach(([a,b,c,d])=>s+=`<line x1="${a}" y1="${b}" x2="${c}" y2="${d}" class="hl"/>`);
  // ceiling hatch (dense, converging)
  const n=46;for(let i=1;i<n;i++){const t=i/n;s+=`<line x1="${W*t}" y1="0" x2="${bx0+(bx1-bx0)*t}" y2="${by0}" class="hf"/>`;}
  for(let i=1;i<7;i++){const t=i/7;const y0=by0*t;s+=`<line x1="${bx0*t}" y1="${y0}" x2="${W-(W-bx1)*t}" y2="${y0}" class="hf"/>`;}
  // side walls: verticals converging
  for(let i=1;i<6;i++){const t=i/6;const x=bx0*t;const yt=by0*t,yb=fl-(fl-by1)*t;s+=`<line x1="${x}" y1="${yt}" x2="${x}" y2="${yb}" class="hf"/>`;
    const xr=W-(W-bx1)*t;s+=`<line x1="${xr}" y1="${yt}" x2="${xr}" y2="${yb}" class="hf"/>`;}
  // floor projection
  const Zb=(W)/(bx1-bx0), Zf=1; // depth ratio
  const proj=(x,y)=>{ // x,y lattice 0..7 ; margin inside floor
    const m=.55, u=(x+m)/(7+2*m), t=(y+m)/(7+2*m);
    const Z=Zb+(Zf-Zb)*t; const inv=(1/Z-1/Zb)/(1/Zf-1/Zb);
    const Y=by1+(fl-by1)*inv; const xl=bx0*(1-inv), xr=bx1+(W-bx1)*inv;
    return [xl+(xr-xl)*u, Y];};
  for(let k=0;k<8;k++){const a=proj(k,-.55),b=proj(k,7.55);s+=`<line x1="${a[0]}" y1="${a[1]}" x2="${b[0]}" y2="${b[1]}" class="st"/>`;
    const c=proj(-.55,k),d=proj(7.55,k);s+=`<line x1="${c[0]}" y1="${c[1]}" x2="${d[0]}" y2="${d[1]}" class="st"/>`;}
  // park, hatched
  const pk=[proj(5.15,4.15),proj(5.85,4.15),proj(5.85,5.85),proj(5.15,5.85)];
  s+=`<polygon points="${pk.map(p=>p.join(',')).join(' ')}" class="pk"/>`;
  // route
  s+=`<polyline points="${routePts().map(p=>proj(p[0],p[1]).join(',')).join(' ')}" class="rt"/>`;
  // stops
  const dp=proj(0,0);s+=`<rect x="${dp[0]-6}" y="${dp[1]-6}" width="12" height="12" class="dp"/><rect x="${dp[0]-2.5}" y="${dp[1]-2.5}" width="5" height="5" class="dpi"/>`;
  s+=`<text x="${dp[0]-10}" y="${dp[1]-9}" class="lb" text-anchor="end">depot</text>`;
  STOPS.forEach((st,i)=>{const k=ORDER.indexOf(i);const p=proj(st.x,st.y);const sc=.75+.35*((st.y+.5)/8);
    if(k===ORDER.length-1) s+=`<circle cx="${p[0]}" cy="${p[1]}" r="${15*sc}" class="ring"/>`;
    if(k<0) s+=`<circle cx="${p[0]}" cy="${p[1]}" r="${6*sc}" class="so"/><line x1="${p[0]-11*sc}" y1="${p[1]}" x2="${p[0]+11*sc}" y2="${p[1]}" class="hl"/><line x1="${p[0]}" y1="${p[1]-11*sc}" x2="${p[0]}" y2="${p[1]+11*sc}" class="hl"/>`;
    else s+=`<circle cx="${p[0]}" cy="${p[1]}" r="${9*sc}" class="sf"/><text x="${p[0]}" y="${p[1]+3.6*sc}" class="sn" style="font-size:${10*sc}px">${k+1}</text>`;
    s+=`<text x="${p[0]+12*sc}" y="${p[1]-8*sc}" class="lb${k<0?' lt':''}" style="font-size:${10.5*sc}px">${st.n.toLowerCase()}</text>`;});
  return {s,proj};}

function game(narrow){
  const L=legs(), driven=L.at(-1).cum;
  const W=narrow?390:740, H=narrow?592:540;
  const cfg=narrow?{bx0:54,bx1:336,by0:56,by1:228,floorY:526}:{bx0:178,bx1:562,by0:52,by1:214,floorY:478};
  const R=room(W,H,cfg); let s=R.s;
  const {bx0,bx1,by0,by1,floorY}=cfg;
  // back wall content : constructed title + narrative + running sentence + big number
  const th=narrow?17:19;
  s+=stroke('TOURNÉE',bx0+14,by0+16,th,'ct');
  const para=narrow
    ? ['Six parcels wait at the depot.','Drive them all and bring the van','home by the shortest round.']
    : ['Six parcels wait at the depot. Drive them all','and bring the van home by the shortest round.'];
  para.forEach((ln,i)=>s+=`<text x="${bx0+14}" y="${by0+(narrow?58:56)+i*14}" class="pp">${ln}</text>`);
  const seq='depot · '+L.map(g=>g.s.n.toLowerCase()+' '+g.l).join(' · ')+' · ?';
  const words=['depot · bakery 1 · florist 3','library 3 · atelier 3 · ?'];
  words.forEach((w,i)=>s+=`<text x="${bx0+14}" y="${by1-(narrow?44:30)+i*13}" class="mo">${w}</text>`);
  const num=String(driven);const nh=narrow?30:40;
  s+=stroke(num,bx1-14-strokeW(num,nh),by1-(narrow?30:14)-nh,nh,'ct big');
  s+=`<text x="${bx1-14}" y="${by1-(narrow?14:2)}" class="mo" text-anchor="end" dy="${narrow?0:-2}">blocks</text>`;
  // side walls: vertical labels
  const lx=bx0/2+4, rx=W-(W-bx1)/2-4;
  const vl=(x,y,t,rot)=>`<text x="${x}" y="${y}" class="vt" transform="rotate(${rot} ${x} ${y})" text-anchor="middle">${t}</text>`;
  const mid=(by0+floorY)/2;
  s+=vl(lx,mid-70,'round 18.11',-90)+vl(lx,mid+60,'6 stops',-90);
  s+=vl(rx,mid-70,'clock 00:42',90)+vl(rx,mid+60,'streak 6',90);
  // actions
  const ay=floorY+(narrow?20:24);
  s+=`<text x="16" y="${ay+18}" class="ac">undo</text><line x1="16" y1="${ay+24}" x2="52" y2="${ay+24}" class="hl"/>`;
  const bw=narrow?220:260;
  s+=`<rect x="${W-16-bw}" y="${ay}" width="${bw}" height="34" class="cta"/>`;
  s+=`<text x="${W-16-bw+14}" y="${ay+22}" class="ac dim">send route</text><text x="${W-30}" y="${ay+22}" class="ac dim" text-anchor="end">4/6 →</text>`;
  s+=`<text x="${W/2-(narrow?20:40)}" y="${ay+22}" class="mo" text-anchor="middle">${narrow?'':'two parcels left'}</text>`;
  return `<div class="g">${s.replace('<svg',`<svg`)}</svg></div>`.replace('</svg></svg>','</svg>');}
"""

B_CSS = r"""
.g{--ink:#e2432e;background:#fff;color:var(--ink);font-family:"Helvetica Neue",Arial,sans-serif}
.room{display:block;width:100%;height:auto}
.hl{fill:none;stroke:var(--ink);stroke-width:1}
.hf{stroke:var(--ink);stroke-width:.5;opacity:.55}
.st{stroke:var(--ink);stroke-width:.7;opacity:.75}
.pk{fill:rgba(226,67,46,.14);stroke:var(--ink);stroke-width:.6}
.rt{fill:none;stroke:var(--ink);stroke-width:3.2;stroke-linejoin:miter}
.dp{fill:#fff;stroke:var(--ink);stroke-width:1.4}.dpi{fill:var(--ink)}
.so{fill:#fff;stroke:var(--ink);stroke-width:1.2}
.sf{fill:var(--ink)}
.sn{fill:#fff;font:600 10px "Helvetica Neue",Arial,sans-serif;text-anchor:middle}
.ring{fill:none;stroke:var(--ink);stroke-width:.8;stroke-dasharray:3 2.5}
.lb{fill:var(--ink);font:500 10.5px "Helvetica Neue",Arial,sans-serif;paint-order:stroke;stroke:#fff;stroke-width:3px}
.lb.lt{font-weight:400}
.ct polyline{fill:none;stroke:var(--ink);stroke-width:.62;stroke-linecap:square;stroke-linejoin:miter}
.ct.big polyline{stroke-width:.5}
.pp{fill:var(--ink);font:500 11.5px "Helvetica Neue",Arial,sans-serif}
.mo{fill:var(--ink);font:400 9.5px ui-monospace,Menlo,monospace;letter-spacing:.02em}
.vt{fill:var(--ink);font:400 10.5px "Helvetica Neue",Arial,sans-serif;letter-spacing:.02em}
.ac{fill:var(--ink);font:500 13px "Helvetica Neue",Arial,sans-serif}
.ac.dim{opacity:.45}
.cta{fill:#fff;stroke:var(--ink);stroke-width:1;stroke-dasharray:4 3;opacity:.7}
"""

# --------------------------------------------------------------------- C : Feuilleton (pixel tiles + story)
C_JS = r"""
function tileMap(){
  const N=15;let s=`<svg viewBox="-1.25 -1.25 ${N+1.5} ${N+1.5}" class="tm" role="img" aria-label="Tile city, depot and six stops" shape-rendering="crispEdges">`;
  const route=new Set();const rp=routePts();
  for(let k=1;k<rp.length;k++){const [x0,y0]=rp[k-1],[x1,y1]=rp[k];
    for(let x=Math.min(x0,x1)*2;x<=Math.max(x0,x1)*2;x++)for(let y=Math.min(y0,y1)*2;y<=Math.max(y0,y1)*2;y++)route.add(x+','+y);}
  const G=.06;s+=`<rect x="-.08" y="-.08" width="${N+.16}" height="${N+.16}" fill="#d9dbd5"/>`;
  for(let r=0;r<N;r++)for(let c=0;c<N;c++){
    const street=(r%2===0)||(c%2===0);
    let f;
    if(!street){const hv=((c*31)^(r*17))%9; f=['#e9eee6','#efece6','#e7ebf2','#ecebe6','#ece8f1','#e9eee6','#f0ede4','#e8ebe8','#d9ead8'][hv];}
    else f=route.has(c+','+r)?'#111':'#ffffff';
    s+=`<rect x="${c+G}" y="${r+G}" width="${1-2*G}" height="${1-2*G}" fill="${f}"/>`;}
  // stops as pixel chips
  const chip=(st,k)=>{const cx=st.x*2, cy=st.y*2;const big=.32;
    let o=`<rect x="${cx-big}" y="${cy-big}" width="${1+2*big}" height="${1+2*big}" fill="${k===-2?'#111':st.tint}" stroke="#111" stroke-width="${k>=0||k===-2?.09:.05}" shape-rendering="geometricPrecision"/>`;
    o+=pix(k===-2?'house':st.ic,cx-big+.24,cy-big+.24,.25*(1+2*big-.48)/1.25,k===-2?'#fff':'#111');
    if(k>=0) o+=`<rect x="${cx+.55}" y="${cy-.95}" width=".72" height=".72" fill="#111"/><text x="${cx+.91}" y="${cy-.4}" class="bn">${k+1}</text>`;
    if(k===ORDER.length-1) o+=`<rect x="${cx-.62}" y="${cy-.62}" width="2.24" height="2.24" fill="none" stroke="#111" stroke-width=".05" stroke-dasharray=".18 .14" shape-rendering="geometricPrecision"/>`;
    return o;};
  s+=chip(DEPOT,-2);
  STOPS.forEach((st,i)=>s+=chip(st,ORDER.indexOf(i)));
  return s+'</svg>';}
function game(narrow){
  const L=legs();
  const lines=[`<li class="ev"><span class="t">06:00</span><p>The van leaves the <b>depot</b>, six parcels in the back.</p></li>`];
  L.forEach((g,k)=>lines.push(`<li class="ev${k===L.length-1?' last':''}"><span class="t">${g.t}</span><p><span class="chip" style="background:${g.s.tint}">${pixSvg(g.s.ic,12,'#111')}</span><b>${g.s.n}</b>, ${g.l} block${g.l>1?'s':''} on.</p></li>`));
  lines.push(`<li class="ev q"><span class="t">06:30</span><p>Two parcels left: <b>School</b> or <b>Post</b> first?</p></li>`);
  const shown=narrow?lines.slice(-3):lines;
  return `<div class="g ${narrow?'nw':'wd'}">
   <header class="hd"><div class="ttl">${pixSvg('van',20,'#111')}<span>Tournée</span></div><div class="meta"><span>Wed 18 Nov</span><span class="m">00:42</span><span>Streak <b>6</b></span></div></header>
   <div class="bd"><div class="mapw">${tileMap()}</div>
    <div class="story"><div class="ch">Wed 18 Nov · the morning round</div><ol class="evs">${shown.join('')}</ol>
     <div class="acts"><button class="b2">Undo</button><button class="b1" disabled>Send route <span>4/6</span></button></div></div>
   </div></div>`;}
"""

C_CSS = r"""
.g{--ink:#111;--mut:#80827c;background:#f7f6f2;color:var(--ink);font-family:"Helvetica Neue",Arial,sans-serif;padding:18px 20px 20px}
.hd{display:flex;align-items:flex-end;justify-content:space-between;border-bottom:2px solid var(--ink);padding-bottom:10px}
.ttl{display:flex;align-items:center;gap:10px;font-size:30px;font-weight:700;letter-spacing:-.03em;line-height:1}
.meta{display:flex;gap:14px;font-size:12px;color:var(--mut);align-items:baseline}
.meta .m{font:600 15px ui-monospace,Menlo,monospace;color:var(--ink)}.meta b{color:var(--ink)}
.bd{display:grid;grid-template-columns:372px 1fr;gap:22px;margin-top:16px;align-items:start}
.tm{display:block;width:100%;height:auto}
.tm .bn{font:700 .5px ui-monospace,Menlo,monospace;fill:#fff;text-anchor:middle}
.ch{font-size:10.5px;letter-spacing:.12em;text-transform:uppercase;color:var(--mut);margin-bottom:6px}
.evs{list-style:none}
.ev{display:grid;grid-template-columns:46px 1fr;gap:6px;padding:7px 0;border-top:1px solid #e1e0da;font-size:14.5px;line-height:1.3}
.ev .t{font:500 12px ui-monospace,Menlo,monospace;color:var(--mut);padding-top:2px}
.ev p{margin:0}
.ev .chip{display:inline-flex;width:18px;height:18px;align-items:center;justify-content:center;border:1px solid var(--ink);vertical-align:-3px;margin-right:6px}
.ev.last .t{color:var(--ink);font-weight:700}
.ev.q{border-top:2px solid var(--ink)}.ev.q p{font-size:16px;font-weight:500}
.acts{display:grid;grid-template-columns:90px 1fr;gap:8px;margin-top:14px}
.acts button{height:46px;font-size:14px;font-weight:600;border:2px solid var(--ink)}
.b2{background:transparent;color:var(--ink)}
.b1{background:var(--ink);color:#fff;display:flex;justify-content:space-between;align-items:center;padding:0 14px}
.b1 span{font-family:ui-monospace,Menlo,monospace}
.b1[disabled]{background:transparent;color:#a3a59f;border-color:#c9cac4;cursor:not-allowed}
.nw{padding:12px 14px 14px}
.nw .ttl{font-size:24px}.nw .meta span:first-child{display:none}
.nw .bd{grid-template-columns:1fr;gap:10px;margin-top:10px}
.nw .ev{padding:5px 0;font-size:13px}.nw .ev.q p{font-size:14px}
.nw .ch{display:none}
.nw .acts{margin-top:8px}.nw .acts button{height:44px}
"""

# --------------------------------------------------------------------- board + feed chrome
CHROME_CSS = r"""
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1440px;height:900px;overflow:hidden}
body{background:#ebeae6;color:#222;font:13px/1.4 -apple-system,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif}
button{font:inherit}
.bh{position:absolute;left:40px;top:30px;width:880px}
.bh .k{font:500 11px ui-monospace,Menlo,monospace;letter-spacing:.06em;color:#76746e}
.bh h1{font-size:26px;font-weight:600;letter-spacing:-.02em;margin:6px 0 6px}
.bh p{font-size:13.5px;color:#4a4843;max-width:760px}
.frame{position:absolute;transform-origin:0 0;overflow:hidden;background:#f3f4f5;box-shadow:0 0 0 1px rgba(0,0,0,.08),0 24px 48px -24px rgba(0,0,0,.3)}
.desk{width:1440px;height:900px;left:40px;top:150px;transform:scale(.62);border-radius:14px}
.mob{width:390px;height:844px;left:1012px;top:30px;border-radius:44px;border:10px solid #1b1b1d}
.dk-top{height:56px;background:#fff;border-bottom:1px solid #e3e5e8;display:flex;align-items:center;gap:20px;padding:0 24px}
.dk-logo{width:110px;height:22px;border-radius:6px;background:#dcdfe2}
.dk-search{flex:0 0 520px;margin:0 auto;height:38px;border-radius:19px;background:#eef0f2;color:#8a8f95;display:flex;align-items:center;padding:0 18px;font-size:14px}
.dk-user{width:32px;height:32px;border-radius:50%;background:#dcdfe2}
.dk-main{display:flex;gap:24px;padding:20px 24px}
.dk-rail{width:220px;display:flex;flex-direction:column;gap:12px;padding-top:6px}
.dk-rail span{height:14px;border-radius:7px;background:#e1e4e7}.dk-rail span:nth-child(2n){width:70%}
.dk-feed{width:760px;margin-left:90px}
.dk-aside{width:300px;background:#fff;border-radius:12px;height:220px;padding:18px;display:flex;flex-direction:column;gap:10px}
.dk-aside span{height:12px;border-radius:6px;background:#e7e9eb}
.post{background:#fff;border-radius:12px;padding:14px 10px 10px}
.post-hd{display:flex;align-items:center;gap:8px;font-size:12px;color:#62676d;padding:0 6px}
.post-hd .av{width:24px;height:24px;border-radius:50%;background:#cfd3d7}.post-hd b{color:#1f1f1f}
.post-title{font-size:19px;font-weight:600;padding:8px 6px 12px}
.post-game{border-radius:8px;overflow:hidden;border:1px solid #e6e7e9}
.post-act{display:flex;gap:8px;padding:10px 4px 0}
.post-act span{height:32px;padding:0 14px;border-radius:16px;background:#eef0f2;display:flex;align-items:center;font-size:12.5px;font-weight:600;color:#3c4043}
.mb-status{height:44px;display:flex;justify-content:space-between;align-items:center;padding:0 26px;font-size:14px;font-weight:600;background:#fff}
.mb-status i{width:60px;height:12px;border-radius:6px;background:#1b1b1d;opacity:.85}
.mb-bar{height:48px;background:#fff;display:flex;align-items:center;gap:12px;padding:0 14px;border-bottom:1px solid #e9ebed}
.mb-bar .a{width:22px;height:22px;border-radius:6px;background:#dcdfe2}.mb-bar .s{flex:1;height:32px;border-radius:16px;background:#eef0f2}
.mob .post{border-radius:0;padding:10px 0 0}.mob .post-hd{padding:0 12px}.mob .post-title{font-size:16px;padding:6px 12px 8px}
.mob .post-game{border-radius:0;border-left:0;border-right:0}.mob .post-act{padding:8px 10px}
.cap{position:absolute;font:500 10.5px ui-monospace,Menlo,monospace;color:#8a8882;letter-spacing:.04em}
"""

BODY = r"""
<div class="bh"><div class="k">TOURNÉE · PAGE JEU · PLANCHE V2 / %%NUM%%</div><h1>%%NAME%%</h1><p>%%INTENT%%</p></div>
<div class="cap" style="left:40px;top:722px">desktop 1440 × 900 · 62 %</div>
<div class="cap" style="left:1012px;top:880px">mobile 390 × 844 · 100 %</div>
<div class="frame desk">
  <div class="dk-top"><div class="dk-logo"></div><div class="dk-search">Search</div><div class="dk-user"></div></div>
  <div class="dk-main"><aside class="dk-rail"><span></span><span></span><span></span><span></span><span></span><span></span></aside>
    <section class="dk-feed"><article class="post"><div class="post-hd"><span class="av"></span><b>r/TourneeDaily</b><span>· 3 h</span></div>
      <h2 class="post-title">Today's delivery round · Wed 18 Nov</h2><div class="post-game" data-game="wide"></div>
      <div class="post-act"><span>Vote</span><span>214 comments</span><span>Share</span></div></article></section>
    <aside class="dk-aside"><span></span><span></span><span></span><span></span></aside></div>
</div>
<div class="frame mob">
  <div class="mb-status"><span>9:41</span><i></i></div>
  <div class="mb-bar"><span class="a"></span><span class="s"></span><span class="a"></span></div>
  <article class="post"><div class="post-hd"><span class="av"></span><b>r/TourneeDaily</b><span>· 3 h</span></div>
    <h2 class="post-title">Today's delivery round · Wed 18 Nov</h2><div class="post-game" data-game="narrow"></div>
    <div class="post-act"><span>Vote</span><span>214</span><span>Share</span></div></article>
</div>
"""

MOUNT = "document.querySelectorAll('[data-game]').forEach(el=>{el.innerHTML=game(el.dataset.game==='narrow');});"

DIRS = [
    dict(num="A", slug="maquette", kind="iso", name="A · Maquette",
         intent="Baseten : un champ de tuiles isométriques pastel d'où sortent des blocs porteurs de données. "
                "Chaque arrêt est un petit immeuble ; une fois livré il passe au cobalt et porte son numéro sur sa face. "
                "Le journal de bord se lit comme un horaire : 06:03 Bakery, 06:12 Florist…",
         js=A_JS, css=A_CSS),
    dict(num="B", slug="salle", kind="room", name="B · Salle",
         intent="PART : le post devient une pièce dessinée au filet rouge. La ville est posée au sol en perspective, "
                "le mur du fond porte le titre en lettres construites, le récit et les blocs parcourus ; "
                "les infos de partie sont écrites à la verticale sur les murs latéraux. La route et les lettres sont faites du même trait.",
         js=B_JS, css=B_CSS),
    dict(num="C", slug="feuilleton", kind="tiles", name="C · Feuilleton",
         intent="Le récit d'abord : une ville en tuiles plates, vue de haut ; la tournée s'imprime case par case en noir. "
                "À côté, la matinée s'écrit comme une histoire, une ligne par livraison, et la question du moment est posée en clair : "
                "« School or Post first? ». Pastels et pixels de Baseten, sobriété noire.",
         js=C_JS, css=C_CSS),
]


def build(d):
    body = BODY.replace("%%NUM%%", d["num"]).replace("%%NAME%%", d["name"]).replace("%%INTENT%%", d["intent"])
    html = f"""<!doctype html>
<html lang="fr"><head><meta charset="utf-8"><title>Tournée · Jeu · V2 {d['name']}</title>
<meta name="viewport" content="width=1440">
<style>{CHROME_CSS}
/* ---- direction {d['name']} ---- */
{d['css']}</style></head>
<body data-kind="{d['kind']}">{body}
<script>{COMMON_JS}
{d['js']}
{MOUNT}</script>
</body></html>
"""
    p = OUT / f"{d['num']}-{d['slug']}.html"
    p.write_text(html, encoding="utf-8")
    print(p.relative_to(ROOT))


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for d in DIRS:
        build(d)
