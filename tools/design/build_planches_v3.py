"""V3 boards: the locked "Maquette" style applied to every page.

Pages: 01 Post (feed splash), 02 Jeu, 03 Carte de fin, 04 Series & classement.
Reuses the V2 Maquette renderer (iso city, pixel glyphs, chrome) unchanged.
Output: G-DESIGN/planches/v3/*.html. Run: python3 tools/design/build_planches_v3.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_planches_v2 as v2  # noqa: E402

ROOT = v2.ROOT
OUT = ROOT / "G-DESIGN" / "planches" / "v3"

COMMON = (v2.COMMON_JS
          .replace("const ORDER=[4,1,2,3];", "const ORDER=window.PAGE_ORDER||[4,1,2,3];")
          .replace("function routePts(){const p=[[0,0]];legs().forEach(g=>{p.push([g.s.x,g.from.y]);p.push([g.s.x,g.s.y]);});return p;}",
                   "function routePts(){const p=[[0,0]];legs().forEach(g=>{p.push([g.s.x,g.from.y]);p.push([g.s.x,g.s.y]);});"
                   "if(window.CLOSED&&ORDER.length){const l=STOPS[ORDER.at(-1)];p.push([0,l.y]);p.push([0,0]);}return p;}"))
ISO_LIB, GAME_JS = v2.A_JS.split("function game(narrow){", 1)
ISO_LIB = ISO_LIB.replace("if(k===last){", "if(k===last&&!window.NO_RING){")
GAME_JS = "function game(narrow){" + GAME_JS

HDR = r"""
function hdr(clock,streak,hi){return `<header class="hd"><span class="brand">${pixSvg('van',18,'#111')}Tournée</span><span class="hs"><b>${clock}</b><i>clock</i></span><span class="hs${hi?' hi':''}"><b>${streak}</b><i>streak</i></span></header>`;}
"""

# ------------------------------------------------------------------ 01 Post (feed splash)
POST_JS = r"""
function game(narrow){
  return `<div class="g ${narrow?'nw':'wd'}">
  ${hdr('--:--','6',false)}
  <p class="lede">Today's round is loaded: six parcels across town. Plan the shortest way round and bring the van home.</p>
  <div class="bd"><div class="field">${isoMap()}</div>
   <div class="panel">
    <div class="log-hd"><span>Round</span><span>Wed 18 Nov</span></div>
    <ol class="log">
     <li class="kv"><span>Parcels</span><b>6</b></li>
     <li class="kv"><span>Van leaves</span><b>06:00</b></li>
     <li class="kv"><span>Drivers today</span><b>1,284</b></li>
     <li class="kv"><span>Your streak</span><b class="acc">6 days</b></li>
    </ol>
    <div class="acts one"><button class="b1"><span>Start the round</span><span class="c">▸</span></button></div>
   </div></div></div>`;}
"""

# ------------------------------------------------------------------ 03 Carte de fin
FIN_JS = r"""
function strip(n,len,today){let s='<span class="strip">';for(let i=0;i<len;i++){const on=i>=len-n;s+=`<i class="${on?'on':''}${i===len-1?' td':''}"></i>`;}return s+'</span>';}
function game(narrow){
  const L=legs(), total=L.at(-1).cum+dist(STOPS[ORDER.at(-1)],DEPOT);
  const back=hhmm(START+total*MIN_PER_BLOCK);
  return `<div class="g ${narrow?'nw':'wd'}">
  ${hdr('00:58','7',true)}
  <p class="lede"><b>Perfect round.</b> All six parcels delivered, van back at the depot at ${back}.</p>
  <div class="bd"><div class="field">${isoMap()}</div>
   <div class="panel">
    <div class="log-hd"><span>Round result</span><span>18 Nov</span></div>
    <div class="score"><b>100<small>%</small></b><span>Shortest possible<br>round found</span></div>
    <ol class="log">
     <li class="kv"><span>Your round</span><b>${total} blocks</b></li>
     <li class="kv"><span>Best possible</span><b>22 blocks</b></li>
     <li class="kv"><span>Yesterday</span><b>88%</b></li>
     <li class="kv"><span>Streak</span>${strip(7,10)}<b class="acc">7</b></li>
     <li class="kv xs"><span>Drivers who found it</span><b>61%</b></li>
    </ol>
    <div class="quote">Tournée · 18 Nov · ${total} blocks · 100% · 00:58</div>
    <div class="acts two"><button class="b1"><span>Comment your round</span><span class="c">▸</span></button><button class="b2">Board</button></div>
    <div class="next"><span>Next round in</span><b>13:18:40</b></div>
   </div></div></div>`;}
"""

# ------------------------------------------------------------------ 04 Series & classement
SER_JS = r"""
const DAYS=[100,92,85,100,-1,94,100, 88,100,96,100,-1,79,100, 100,91,83,100,100,100,100, 100,100,100];
function calendar(){
  let s=`<svg viewBox="-4.4 -1.5 11.6 6.9" class="iso cal" role="img" aria-label="Last four weeks, one tile per day">`;
  const cells=[];for(let r=0;r<4;r++)for(let c=0;c<7;c++)cells.push([c,r]);
  cells.sort((a,b)=>(a[0]+a[1])-(b[0]+b[1]));
  const g=.1;
  cells.forEach(([c,r])=>{const d=r*7+c;const v=DAYS[d];
    if(v===undefined){s+=prism(c+g,r+g,c+1-g,r+1-g,0,'#fafaf7','#fafaf7','#fafaf7','#d3d5cf',.018);return;}
    if(v<0){s+=prism(c+g,r+g,c+1-g,r+1-g,0,'#ffffff','#fff','#fff','#9a9c95',.02).replace('stroke-linejoin','stroke-dasharray=".08 .06" stroke-linejoin');return;}
    const h=v===100?.62:Math.max(.08,(v-70)/30*.42);
    if(v===100) s+=prism(c+g,r+g,c+1-g,r+1-g,h,'#6f95ff',ACC,'#1746c9','#0b2a86',.018);
    else {const t=v>=90?'#e0eaf8':v>=80?'#ece7f8':'#f7eadb';s+=prism(c+g,r+g,c+1-g,r+1-g,h,t,shade(t,.93),shade(t,.86),'#9fa59c',.018);}
  });
  ['M','T','W','T','F','S','S'].forEach((l,c)=>{const p=iso(c+.5,4.35);s+=`<text x="${p[0]}" y="${p[1]+.1}" class="dl">${l}</text>`;});
  const tp=iso(2.5,3.5,.62);const tx=tp[0]+.6, ty=tp[1]-1.1;
  s+=`<line x1="${tp[0]}" y1="${tp[1]}" x2="${tx}" y2="${ty}" stroke="#111" stroke-width=".018"/>`;
  s+=`<rect x="${tx}" y="${ty-.29}" width="3.25" height=".58" fill="#fff" stroke="#111" stroke-width=".02"/><text x="${tx+.14}" y="${ty+.125}" class="tag">TODAY · 100%</text>`;
  const mp=iso(4.5,1.5,0);const mx=mp[0]+1.1,my=mp[1]-1.0;
  s+=`<line x1="${mp[0]}" y1="${mp[1]}" x2="${mx}" y2="${my}" stroke="#111" stroke-width=".018"/>`;
  s+=`<rect x="${mx}" y="${my-.29}" width="2.05" height=".58" fill="#fff" stroke="#111" stroke-width=".02"/><text x="${mx+.14}" y="${my+.125}" class="tag">MISSED</text>`;
  return s+'</svg>';}
function bar(p,acc){const n=Math.round(p/5);let s='<span class="bar">';for(let i=0;i<20;i++)s+=`<i class="${i<n?(acc?'a':'k'):''}"></i>`;return s+'</span>';}
function game(narrow){
  const rows=[[1,'u/quai_ouest','100%','00:31'],[2,'u/vanlight','100%','00:36'],[3,'u/tram_nine','100%','00:41'],[4,'u/leo_parcel','100%','00:44'],[5,'u/roundabout','100%','00:47']];
  const show=narrow?rows.slice(0,3):rows;
  let b=show.map(r=>`<li class="br"><span class="rk">${r[0]}</span><span class="un">${r[1]}</span><span class="sc">${r[2]}</span><span class="tm">${r[3]}</span></li>`).join('');
  b+=`<li class="br gap"><span class="rk">·</span><span class="un">·</span><span></span><span></span></li>`;
  b+=`<li class="br me"><span class="rk">37</span><span class="un">You</span><span class="sc">100%</span><span class="tm">00:58</span></li>`;
  const dist=[['100%',61,true],['90–99',22],['80–89',11],['< 80',6]];
  return `<div class="g ${narrow?'nw':'wd'}">
  ${hdr('00:58','7',true)}
  <p class="lede"><b>7 perfect rounds in a row.</b> Your best run is 9. Today, 1,284 drivers went out.</p>
  <div class="bd"><div class="field"><div class="fl">Last 4 weeks · tile height = score</div>${calendar()}</div>
   <div class="panel">
    <div class="log-hd"><span>Today's board</span><span>score, then clock</span></div>
    <ol class="log board">${b}</ol>
    <div class="log-hd sub"><span>How drivers did</span><span>1,284</span></div>
    <ol class="log dist">${dist.map(d=>`<li class="dr"><span>${d[0]}</span>${bar(d[1],d[2])}<b>${d[1]}%</b></li>`).join('')}</ol>
    <div class="acts one"><button class="b2 full">Back to today's round</button></div>
   </div></div></div>`;}
"""

P_CSS = r"""
.hs.hi b{color:var(--acc)}
.kv{display:flex;align-items:center;gap:10px;height:32px;padding:0 12px;border-bottom:1px solid var(--line);font-size:13px}
.kv span{color:var(--mut);margin-right:auto}.kv b{font:600 13px ui-monospace,Menlo,monospace}.kv b.acc{color:var(--acc)}
.acts.one{grid-template-columns:1fr}.acts.two{grid-template-columns:1fr 84px}
.acts.two .b2{border-right:0!important;border-left:1px solid var(--ink)!important}
.b2.full{border-right:0!important}
.score{display:flex;align-items:center;gap:14px;padding:12px;border-bottom:1px solid var(--line)}
.score b{font:600 44px/1 ui-monospace,Menlo,monospace;color:var(--acc);letter-spacing:-.02em}.score small{font-size:22px}
.score span{font-size:12px;line-height:1.3;color:var(--mut)}
.strip{display:flex;gap:2px}.strip i{width:9px;height:9px;background:#e6e7e2}.strip i.on{background:var(--acc)}.strip i.td{outline:1px solid var(--ink);outline-offset:1px}
.quote{margin:10px 12px;padding:8px 10px;border:1px dashed #b9bbb4;font:500 11.5px ui-monospace,Menlo,monospace;color:#3a3b38;background:#fafaf7}
.next{display:flex;justify-content:space-between;padding:8px 12px;border-top:1px solid var(--line);font-size:11.5px;color:var(--mut)}
.next b{font:600 12px ui-monospace,Menlo,monospace;color:var(--ink)}
.fl{font-size:10px;letter-spacing:.1em;text-transform:uppercase;color:var(--mut);margin:44px 0 0 6px}
.cal{margin-top:-6px}.cal .dl{font:600 .32px ui-monospace,Menlo,monospace;fill:#7b7d78;text-anchor:middle}
.br{display:grid;grid-template-columns:28px 1fr 46px 46px;align-items:center;height:30px;padding:0 12px;border-bottom:1px solid var(--line);font-size:13px}
.br .rk,.br .sc,.br .tm{font:500 12px ui-monospace,Menlo,monospace}.br .rk{color:var(--mut)}.br .sc,.br .tm{text-align:right}
.br.gap{height:18px;color:#b9bbb4}
.br.me{background:#eef3ff}.br.me .un,.br.me .sc{color:var(--acc);font-weight:600}
.log-hd.sub{border-top:1px solid var(--ink)}
.dr{display:grid;grid-template-columns:48px 1fr 36px;align-items:center;gap:8px;height:26px;padding:0 12px;font-size:12px}
.dr span{font-family:ui-monospace,Menlo,monospace;color:var(--mut)}.dr b{font:600 12px ui-monospace,Menlo,monospace;text-align:right}
.bar{display:flex;gap:1.5px}.bar i{flex:1;height:9px;background:#ecece7}.bar i.k{background:#111}.bar i.a{background:var(--acc)}
.nw .kv{height:28px}.nw .score{padding:8px 12px}.nw .score b{font-size:36px}
.nw .quote{margin:8px 12px}.nw .fl{margin:6px 0 0 4px}
.nw .br{height:26px}.nw .kv.xs{display:none}.nw .kv{height:26px}.nw .dr{height:22px}
"""

PAGES = [
    dict(num="01", slug="post", page="POST", name="01 · Post",
         pre="window.PAGE_ORDER=[];window.NO_RING=true;", js=POST_JS,
         intent="Vue dans le feed : la ville du jour en maquette, les six immeubles encore blancs, aucun tracé. Le panneau annonce la tournée (colis, départ, nombre de chauffeurs, ta série) et un seul bouton noir : « Start the round »."),
    dict(num="02", slug="jeu", page="JEU", name="02 · Jeu",
         pre="", js=GAME_JS,
         intent="Page principale validée (V2 · A), reprise à l'identique : 4 arrêts placés sur 6, 10 blocs parcourus, Send route verrouillé jusqu'à 6/6, journal de bord horodaté."),
    dict(num="03", slug="fin", page="CARTE DE FIN", name="03 · Carte de fin",
         pre="window.PAGE_ORDER=[4,1,2,3,5,0];window.CLOSED=true;window.NO_RING=true;", js=FIN_JS,
         intent="La tournée bouclée : les six immeubles en cobalt, la route revenue au dépôt. Le panneau donne le score contre l'optimum, la comparaison avec la veille, la série, la part de chauffeurs qui ont trouvé, et une ligne de commentaire prête à poster sans spoiler l'ordre."),
    dict(num="04", slug="series", page="SÉRIES & CLASSEMENT", name="04 · Séries & classement",
         pre="window.PAGE_ORDER=[];", js=SER_JS,
         intent="La série devient une maquette : quatre semaines, une tuile par jour, sa hauteur suit le score (cobalt = tournée parfaite, pointillé = jour manqué). À côté, le classement du jour (score puis horloge) et la répartition des chauffeurs en barres de pixels."),
]


def build(d):
    body = (v2.BODY.replace("PAGE JEU · PLANCHE V2 / %%NUM%%", f"PAGE {d['page']} · PLANCHE V3 / %%NUM%% · STYLE VERROUILLÉ")
            .replace("%%NUM%%", d["num"]).replace("%%NAME%%", d["name"]).replace("%%INTENT%%", d["intent"]))
    html = f"""<!doctype html>
<html lang="fr"><head><meta charset="utf-8"><title>Tournée · {d['name']}</title>
<meta name="viewport" content="width=1440">
<style>{v2.CHROME_CSS}
/* ---- style Maquette (verrouillé) ---- */
{v2.A_CSS}
{P_CSS}</style></head>
<body data-kind="iso">{body}
<script>{d['pre']}
{COMMON}
{ISO_LIB}
{HDR}
{d['js']}
{v2.MOUNT}</script>
</body></html>
"""
    p = OUT / f"{d['num']}-{d['slug']}.html"
    p.write_text(html, encoding="utf-8")
    print(p.relative_to(ROOT))


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for d in PAGES:
        build(d)
