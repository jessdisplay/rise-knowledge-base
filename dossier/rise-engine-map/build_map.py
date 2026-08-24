#!/usr/bin/env python3
"""Bake the compliance-engine constellation for the dossier.

Reads the seed graph (rise-ndis-package/rise-nodes-and-edges.json, the source of
truth) and the suite mirror on disk, runs a deterministic force layout, and
writes index.html beside this script with the positions baked in. No physics
runs in the browser; regenerate by running this script from the repo root or
this directory. Layout is seeded, so the same inputs give the same picture.
"""
import json, math, os, random, re, collections

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..'))

graph = json.load(open(os.path.join(REPO, 'rise-ndis-package', 'rise-nodes-and-edges.json')))
nodes, edges = graph['nodes'], graph['edges']

# real documentation pages: doc id -> suite path (relative to dossier/)
suite = {}
for root, _, files in os.walk(os.path.join(REPO, 'dossier', 'suite')):
    for f in files:
        if f.endswith('.html') and not f.startswith('00-'):
            suite[f.split('_')[0].upper()] = os.path.relpath(os.path.join(root, f), os.path.join(REPO, 'dossier'))

def community(n):
    i, t = n['id'], n['node_type']
    if t == 'Document':
        return 'D:' + i.split('-')[1]
    if t == 'Standard':
        return 'S:' + re.match(r'([A-Z0-9]+)', i).group(1)
    if t == 'Instrument':
        return 'LAW'
    return 'MODEL'  # Module / Framework

idx = {n['id']: k for k, n in enumerate(nodes)}
coms = sorted({community(n) for n in nodes})
rng = random.Random(2026)

# community centroids on a golden-angle spiral
cent = {}
GA = math.pi * (3 - math.sqrt(5))
for k, c in enumerate(coms):
    r = 340 * math.sqrt((k + 0.6) / len(coms))
    a = k * GA
    cent[c] = (r * math.cos(a), r * math.sin(a))

pos = []
for n in nodes:
    cx, cy = cent[community(n)]
    pos.append([cx + rng.uniform(-28, 28), cy + rng.uniform(-28, 28)])

E = [(idx[e['source']], idx[e['target']]) for e in edges]
deg = collections.Counter()
for a, b in E:
    deg[a] += 1; deg[b] += 1

# force sim: springs on edges, short-range repulsion, pull to community centroid
for it in range(320):
    heat = 0.9 * (1 - it / 320) + 0.05
    disp = [[0.0, 0.0] for _ in nodes]
    # repulsion via coarse grid buckets
    grid = collections.defaultdict(list)
    CELL = 46
    for i, (x, y) in enumerate(pos):
        grid[(int(x // CELL), int(y // CELL))].append(i)
    for (gx, gy), members in grid.items():
        near = []
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                near += grid.get((gx + dx, gy + dy), [])
        for i in members:
            xi, yi = pos[i]
            for j in near:
                if j <= i: continue
                dx, dy = xi - pos[j][0], yi - pos[j][1]
                d2 = dx * dx + dy * dy + 0.01
                if d2 < 42 * 42:
                    f = 620.0 / d2
                    dl = math.sqrt(d2)
                    disp[i][0] += f * dx / dl; disp[i][1] += f * dy / dl
                    disp[j][0] -= f * dx / dl; disp[j][1] -= f * dy / dl
    for a, b in E:
        dx, dy = pos[a][0] - pos[b][0], pos[a][1] - pos[b][1]
        d = math.sqrt(dx * dx + dy * dy) + 0.01
        f = (d - 42) * 0.020
        disp[a][0] -= f * dx / d; disp[a][1] -= f * dy / d
        disp[b][0] += f * dx / d; disp[b][1] += f * dy / d
    for i, n in enumerate(nodes):
        cx, cy = cent[community(n)]
        disp[i][0] += (cx - pos[i][0]) * 0.012
        disp[i][1] += (cy - pos[i][1]) * 0.012
        dl = math.sqrt(disp[i][0] ** 2 + disp[i][1] ** 2) + 1e-9
        step = min(dl, 14 * heat)
        pos[i][0] += disp[i][0] / dl * step
        pos[i][1] += disp[i][1] / dl * step

# palette: class hue + per-community variation
CLASS_BASE = {'Instrument': 262, 'Standard': 168, 'Document': 34, 'Module': 208, 'Framework': 208}
com_list = sorted(coms)
def color(n):
    base = CLASS_BASE[n['node_type']]
    k = com_list.index(community(n))
    h = (base + (k * 9) % 26 - 13) % 360
    return h

out_nodes = []
for i, n in enumerate(nodes):
    out_nodes.append({
        'id': n['id'], 'title': n['title'], 'nt': n['node_type'], 'kind': n.get('kind', ''),
        'ver': n.get('verification', ''), 'note': n.get('note', ''),
        'x': round(pos[i][0], 1), 'y': round(pos[i][1], 1),
        'c': community(n), 'h': color(n),
        'r': round(2.4 + math.sqrt(deg[i]) * 1.15, 1),
        'doc': suite.get(n['id'].upper()),
    })
out_edges = [[idx[e['source']], idx[e['target']], e['type']] for e in edges]
com_counts = collections.Counter(community(n) for n in nodes)
COM_LABEL = {'LAW': 'Law, rules and framework', 'MODEL': 'Modules and framework'}
out_coms = [{'id': c, 'label': COM_LABEL.get(c, c.split(':', 1)[-1]), 'n': com_counts[c]} for c in com_list]

DATA = json.dumps({'nodes': out_nodes, 'edges': out_edges, 'coms': out_coms}, separators=(',', ':'))

HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>The compliance engine — the real graph</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@500;600;700;800&family=Space+Grotesk:wght@400;500;600&family=IBM+Plex+Mono:wght@400;600&display=swap" rel="stylesheet">
<style>
:root{--bg:#17160F;--panel:#201F17;--ink:#F3EAD3;--mut:#B8AE93;--rule:#3A3728;--amber:#F7AC28;--ok:#5ECFB4}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--bg);color:var(--ink);font:15px/1.55 "Space Grotesk",system-ui,sans-serif;height:100vh;display:flex;flex-direction:column;overflow:hidden}
header{display:flex;flex-wrap:wrap;align-items:center;gap:10px 18px;padding:12px 18px;border-bottom:1px solid var(--rule);background:var(--bg);z-index:5}
header a.back{color:var(--mut);text-decoration:none;font:600 12.5px Archivo;letter-spacing:.04em}
header a.back:hover{color:var(--amber)}
h1{font:800 19px/1.2 Archivo;letter-spacing:-.01em}
h1 em{font-style:normal;color:var(--amber)}
.stats{font:600 12px "IBM Plex Mono";color:var(--mut);letter-spacing:.04em}
#q{flex:1 1 220px;max-width:340px;background:var(--panel);border:1px solid var(--rule);border-radius:8px;color:var(--ink);padding:8px 12px;font:500 14px "Space Grotesk"}
#q:focus-visible{outline:2px solid var(--amber)}
main{flex:1;display:flex;min-height:0}
#stage{flex:1;position:relative;min-width:0}
canvas{position:absolute;inset:0;width:100%;height:100%;cursor:grab;touch-action:none}
canvas.dragging{cursor:grabbing}
#tip{position:absolute;pointer-events:none;background:#000c;border:1px solid var(--rule);border-radius:6px;padding:5px 9px;font:600 12px "Space Grotesk";color:var(--ink);display:none;max-width:300px;z-index:4}
aside{width:min(430px,44vw);border-left:1px solid var(--rule);background:var(--panel);display:flex;flex-direction:column;min-width:0}
aside .pad{padding:16px 18px;overflow-y:auto}
aside h2{font:700 16px/1.3 Archivo;margin-bottom:4px}
aside .meta{font:600 11px "IBM Plex Mono";color:var(--mut);letter-spacing:.06em;text-transform:uppercase;margin-bottom:8px}
aside .note{color:var(--mut);font-size:13.5px;margin:8px 0}
.tagv{display:inline-block;font:600 10.5px "IBM Plex Mono";letter-spacing:.06em;border:1px solid var(--rule);border-radius:999px;padding:2px 8px;color:var(--ok);margin-right:6px}
.links{margin:10px 0;font-size:13px}
.links li{list-style:none;margin:4px 0;color:var(--mut)}
.links b{color:var(--ink);font-weight:600}
.links .rel{color:var(--amber);font:600 10.5px "IBM Plex Mono"}
a.opendoc{display:inline-block;background:var(--amber);color:#17160F;font:700 13px Archivo;padding:8px 14px;border-radius:8px;text-decoration:none;margin:8px 8px 8px 0}
a.openext{color:var(--amber);font:600 12.5px Archivo;text-decoration:none}
a.openext:hover,a.opendoc:hover{filter:brightness(1.1)}
#docframe{flex:1;border:0;border-top:1px solid var(--rule);background:#fff;display:none;min-height:0}
#legend{position:absolute;left:12px;bottom:12px;background:#000a;border:1px solid var(--rule);border-radius:10px;padding:10px 12px;max-height:44vh;overflow-y:auto;max-width:240px;z-index:3}
#legend h3{font:700 11px "IBM Plex Mono";letter-spacing:.1em;color:var(--mut);text-transform:uppercase;margin-bottom:6px}
#legend button{display:flex;align-items:center;gap:7px;width:100%;background:none;border:0;color:var(--ink);font:500 12.5px "Space Grotesk";padding:2px 0;cursor:pointer;text-align:left}
#legend button .dot{width:8px;height:8px;border-radius:50%;flex:none}
#legend button .n{margin-left:auto;color:var(--mut);font:600 11px "IBM Plex Mono"}
#legend button[aria-pressed="true"]{color:var(--amber)}
.zoombtns{position:absolute;right:12px;top:12px;display:flex;gap:6px;z-index:3}
.zoombtns button{background:#000a;border:1px solid var(--rule);color:var(--ink);border-radius:8px;width:34px;height:34px;font:700 16px Archivo;cursor:pointer}
.zoombtns button:focus-visible,#legend button:focus-visible{outline:2px solid var(--amber)}
.hint{position:absolute;right:12px;bottom:12px;color:var(--mut);font:500 11.5px "Space Grotesk";background:#000a;border:1px solid var(--rule);border-radius:8px;padding:6px 10px;z-index:3}
#results{position:absolute;left:18px;top:0;background:var(--panel);border:1px solid var(--rule);border-radius:0 0 10px 10px;z-index:6;max-height:300px;overflow-y:auto;display:none;min-width:320px}
#results button{display:block;width:100%;text-align:left;background:none;border:0;color:var(--ink);padding:7px 12px;font:500 13px "Space Grotesk";cursor:pointer}
#results button:hover,#results button.sel{background:#2A2820}
#results .id{font:600 11px "IBM Plex Mono";color:var(--amber);margin-right:8px}
@media (max-width:860px){aside{position:absolute;inset:auto 0 0 0;height:60vh;width:100%;border-left:0;border-top:1px solid var(--rule);z-index:7}}
</style>
</head>
<body>
<header>
  <a class="back" href="../index.html">&#8592; The dossier</a>
  <h1>The compliance engine &#183; <em>the real graph</em></h1>
  <span class="stats" id="stats"></span>
  <input id="q" type="search" placeholder="Find anything&#8230; (CORE-2.6, POL-INC-01, medication)" aria-label="Search nodes">
</header>
<main>
  <div id="stage">
    <canvas id="cv" aria-label="Compliance graph. Use the search box to find and select nodes."></canvas>
    <div id="tip" role="status"></div>
    <div id="legend"><h3>Communities</h3><div id="legendlist"></div></div>
    <div class="zoombtns"><button id="zin" aria-label="Zoom in">+</button><button id="zout" aria-label="Zoom out">&#8722;</button><button id="zfit" aria-label="Reset view" style="font-size:11px;width:auto;padding:0 10px">Fit</button></div>
    <div class="hint">drag to move &#183; scroll to zoom &#183; click a node for the real document</div>
    <div id="results" role="listbox"></div>
  </div>
  <aside id="panel" aria-live="polite">
    <div class="pad" id="info">
      <h2>Click any node</h2>
      <p class="note">Every dot is real: 224 nodes, 528 typed edges from the seed graph. Documents open the actual page from the 123-document suite, right here. The same graph runs on <a class="openext" href="https://jessdisplay.github.io/rw/compliance-graph/" target="_blank" rel="noopener">the Rise website</a>.</p>
    </div>
    <iframe id="docframe" title="The selected document"></iframe>
  </aside>
</main>
<script id="data" type="application/json">__DATA__</script>
<script>
const D=JSON.parse(document.getElementById('data').textContent);
const N=D.nodes, E=D.edges, COMS=D.coms;
document.getElementById('stats').textContent=N.length+' nodes \\u00b7 '+E.length+' edges \\u00b7 '+COMS.length+' communities';
const adj=N.map(()=>[]);
E.forEach(([a,b,t],i)=>{adj[a].push([b,t,'\\u2192']);adj[b].push([a,t,'\\u2190']);});
const cv=document.getElementById('cv'), ctx=cv.getContext('2d');
let W=0,H=0,DPR=1, cam={x:0,y:0,k:1}, sel=-1, hov=-1, comFilter=null;
function resize(){DPR=devicePixelRatio||1;W=cv.clientWidth;H=cv.clientHeight;cv.width=W*DPR;cv.height=H*DPR;draw();}
function fit(){const xs=N.map(n=>n.x),ys=N.map(n=>n.y);const mx=[Math.min(...xs),Math.max(...xs)],my=[Math.min(...ys),Math.max(...ys)];
 cam.k=Math.min(W/(mx[1]-mx[0]+140),H/(my[1]-my[0]+140));cam.x=(mx[0]+mx[1])/2;cam.y=(my[0]+my[1])/2;draw();}
function sx(x){return (x-cam.x)*cam.k+W/2} function sy(y){return (y-cam.y)*cam.k+H/2}
function nodeCol(n,a){return 'hsla('+n.h+',68%,'+(n.nt==='Document'?66:60)+'%,'+a+')'}
function draw(){ctx.setTransform(DPR,0,0,DPR,0,0);ctx.clearRect(0,0,W,H);ctx.fillStyle='#17160F';ctx.fillRect(0,0,W,H);
 const focus=sel>=0?sel:hov;
 const lit=new Set(); if(focus>=0){lit.add(focus);adj[focus].forEach(([j])=>lit.add(j));}
 ctx.lineWidth=Math.max(.4,.6*cam.k);
 for(const [a,b] of E){const dim=(focus>=0&&!(lit.has(a)&&lit.has(b)))||(comFilter&&N[a].c!==comFilter&&N[b].c!==comFilter);
  ctx.strokeStyle=dim?'rgba(200,190,160,.05)':(focus>=0?'rgba(247,172,40,.45)':'rgba(200,190,160,.14)');
  ctx.beginPath();ctx.moveTo(sx(N[a].x),sy(N[a].y));ctx.lineTo(sx(N[b].x),sy(N[b].y));ctx.stroke();}
 for(let i=0;i<N.length;i++){const n=N[i];const x=sx(n.x),y=sy(n.y);if(x<-20||y<-20||x>W+20||y>H+20)continue;
  const dim=(focus>=0&&!lit.has(i))||(comFilter&&n.c!==comFilter);
  const r=Math.max(1.6,n.r*cam.k*.55)*(i===focus?1.6:1);
  ctx.beginPath();ctx.arc(x,y,r,0,7);ctx.fillStyle=nodeCol(n,dim?.14:.95);ctx.fill();
  if(i===focus){ctx.strokeStyle='#F7AC28';ctx.lineWidth=1.6;ctx.stroke();}
  if(cam.k>2.4&&!dim){ctx.fillStyle='rgba(243,234,211,.8)';ctx.font='600 '+Math.min(11,4.2*cam.k)+'px "IBM Plex Mono"';ctx.fillText(n.id,x+r+3,y+3);}}
}
function pick(mx,my){let best=-1,bd=144;for(let i=0;i<N.length;i++){const dx=sx(N[i].x)-mx,dy=sy(N[i].y)-my;const d=dx*dx+dy*dy;if(d<bd){bd=d;best=i;}}return best;}
const tip=document.getElementById('tip');
let drag=null;
cv.addEventListener('pointerdown',e=>{drag={x:e.clientX,y:e.clientY,cx:cam.x,cy:cam.y,moved:false};cv.setPointerCapture(e.pointerId);cv.classList.add('dragging');});
cv.addEventListener('pointermove',e=>{const r=cv.getBoundingClientRect();
 if(drag){const dx=e.clientX-drag.x,dy=e.clientY-drag.y;if(Math.abs(dx)+Math.abs(dy)>4)drag.moved=true;
  cam.x=drag.cx-dx/cam.k;cam.y=drag.cy-dy/cam.k;draw();return;}
 const i=pick(e.clientX-r.left,e.clientY-r.top);
 if(i!==hov){hov=i;draw();}
 if(i>=0){tip.style.display='block';tip.style.left=(e.clientX-r.left+14)+'px';tip.style.top=(e.clientY-r.top+10)+'px';tip.textContent=N[i].id+' \\u00b7 '+N[i].title;}
 else tip.style.display='none';});
cv.addEventListener('pointerup',e=>{cv.classList.remove('dragging');const r=cv.getBoundingClientRect();
 if(drag&&!drag.moved){const i=pick(e.clientX-r.left,e.clientY-r.top);select(i);}drag=null;});
cv.addEventListener('wheel',e=>{e.preventDefault();const f=Math.exp(-e.deltaY*.0016);cam.k=Math.min(14,Math.max(.2,cam.k*f));draw();},{passive:false});
document.getElementById('zin').onclick=()=>{cam.k=Math.min(14,cam.k*1.35);draw();};
document.getElementById('zout').onclick=()=>{cam.k=Math.max(.2,cam.k/1.35);draw();};
document.getElementById('zfit').onclick=()=>{sel=-1;comFilter=null;syncLegend();fit();info(-1);};
const infoEl=document.getElementById('info'), frame=document.getElementById('docframe');
function esc(s){return s.replace(/&/g,'&amp;').replace(/</g,'&lt;')}
function info(i){
 if(i<0){infoEl.innerHTML='<h2>Click any node</h2><p class="note">Every dot is real: '+N.length+' nodes, '+E.length+' typed edges from the seed graph. Documents open the actual page from the 123-document suite, right here.</p>';frame.style.display='none';return;}
 const n=N[i];
 let h='<div class="meta">'+esc(n.nt)+(n.kind?' \\u00b7 '+esc(n.kind):'')+' \\u00b7 '+esc(n.c.split(":").pop())+'</div><h2>'+esc(n.id)+' \\u00b7 '+esc(n.title)+'</h2>';
 if(n.ver)h+='<span class="tagv">verification '+esc(n.ver)+'</span>';
 if(n.note)h+='<p class="note">'+esc(n.note)+'</p>';
 if(n.doc)h+='<a class="opendoc" id="readbtn" href="../'+n.doc+'" target="_blank" rel="noopener">Open the real document \\u2197</a>';
 else if(n.nt==='Standard')h+='<a class="opendoc" href="../../standards.html" target="_blank" rel="noopener">See it in the standards index \\u2197</a>';
 const rel=adj[i].slice(0,14).map(([j,t,dir])=>'<li><span class="rel">'+esc(t)+' '+dir+'</span> <b>'+esc(N[j].id)+'</b> '+esc(N[j].title)+'</li>').join('');
 if(rel)h+='<ul class="links"><div class="meta" style="margin:10px 0 4px">connections ('+adj[i].length+')</div>'+rel+(adj[i].length>14?'<li>\\u2026 and '+(adj[i].length-14)+' more</li>':'')+'</ul>';
 infoEl.innerHTML=h;
 if(n.doc){frame.src='../'+n.doc;frame.style.display='block';}else{frame.style.display='none';frame.removeAttribute('src');}
}
function select(i){sel=i;info(i);draw();if(i>=0)history.replaceState(null,'','#focus='+encodeURIComponent(N[i].id));}
const legendList=document.getElementById('legendlist');
function syncLegend(){[...legendList.children].forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.c===comFilter)));}
COMS.forEach(c=>{const first=N.find(n=>n.c===c.id);
 const b=document.createElement('button');b.dataset.c=c.id;b.setAttribute('aria-pressed','false');
 b.innerHTML='<span class="dot" style="background:'+nodeCol(first,1)+'"></span>'+esc(c.label)+'<span class="n">'+c.n+'</span>';
 b.onclick=()=>{comFilter=comFilter===c.id?null:c.id;syncLegend();draw();};legendList.appendChild(b);});
const q=document.getElementById('q'), results=document.getElementById('results');
q.addEventListener('input',()=>{const v=q.value.trim().toLowerCase();if(!v){results.style.display='none';return;}
 const hits=[];for(let i=0;i<N.length&&hits.length<12;i++){const n=N[i];
  if(n.id.toLowerCase().includes(v)||n.title.toLowerCase().includes(v))hits.push(i);}
 results.innerHTML=hits.map(i=>'<button data-i="'+i+'"><span class="id">'+esc(N[i].id)+'</span>'+esc(N[i].title)+'</button>').join('')||'<button disabled>No match</button>';
 results.style.display='block';
 [...results.querySelectorAll('button[data-i]')].forEach(b=>b.onclick=()=>{const i=+b.dataset.i;results.style.display='none';q.value=N[i].id;
  cam.x=N[i].x;cam.y=N[i].y;cam.k=Math.max(cam.k,3.4);select(i);});});
q.addEventListener('keydown',e=>{if(e.key==='Enter'){const b=results.querySelector('button[data-i]');if(b)b.click();}});
document.addEventListener('click',e=>{if(!results.contains(e.target)&&e.target!==q)results.style.display='none';});
addEventListener('resize',resize);
resize();fit();
const m=location.hash.match(/focus=([^&]+)/);
if(m){const id=decodeURIComponent(m[1]).toUpperCase();const i=N.findIndex(n=>n.id.toUpperCase()===id);
 if(i>=0){cam.x=N[i].x;cam.y=N[i].y;cam.k=3.4;select(i);}}
</script>
</body>
</html>
"""

out = HTML.replace('__DATA__', DATA)
open(os.path.join(HERE, 'index.html'), 'w').write(out)
print('wrote index.html', len(out), 'bytes;', len(out_nodes), 'nodes,', len(out_edges), 'edges,', len(out_coms), 'communities')
