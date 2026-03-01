"""
🧪 The Fitzroy Collection — Enhanced 3D Apothecary Cabinet
Victorian medical cabinet with interactive bottles and rich atmospheric props.

NEW ELEMENTS:
- Human skull (memento mori) on top
- Dripping candle with animated flame
- Stack of leather-bound books
- Brass balance scales
- Mortar and pestle
- Victorian syringe (brass & glass)
- Magnifying glass
- Cobwebs between bottles
- Dust particles in candlelight
- Dried herbs hanging from top
- Mouse peeking out at intensity 2+
- Pocket watch draped over shelf
- Wax seal stamps
- Chemical stains on wood
"""

def get_cabinet_3d(mode: str = "gaslight", intensity: int = 3) -> str:
    colors = {
        "gaslight": {
            "bg": 0x1a1410, "wood": 0x5a3d25, "wood_dark": 0x3a2515,
            "metal": 0xb8860b, "glass": 0xeeffaa, "cloth": 0x8b7355,
            "light": 0xffaa44, "text": "#d4a574", "glow": 0xffcc88,
            "bone": 0xe8dcc8, "paper": 0xf5f0e0, "leather": 0x3a2010,
            "wax": 0x8b1a1a, "herb": 0x2a4a1a, "cobweb": 0xccccbb,
            "stain_dark": 0x2a1a0a, "stain_red": 0x4a1010,
        },
        "gothic": {
            "bg": 0x0a0a0a, "wood": 0x2a1515, "wood_dark": 0x1a0a0a,
            "metal": 0x4a4a4a, "glass": 0x44ff44, "cloth": 0x1a1a1a,
            "light": 0xff2200, "text": "#cc0000", "glow": 0xff4444,
            "bone": 0xccbbaa, "paper": 0xddccbb, "leather": 0x1a0a05,
            "wax": 0x660000, "herb": 0x1a2a0a, "cobweb": 0x555544,
            "stain_dark": 0x1a0505, "stain_red": 0x440000,
        },
        "clinical": {
            "bg": 0xf0f0f0, "wood": 0xd0c8b8, "wood_dark": 0xb8b0a0,
            "metal": 0xaaaaaa, "glass": 0xccddff, "cloth": 0xffffff,
            "light": 0xffffff, "text": "#2f4f4f", "glow": 0xeeeeee,
            "bone": 0xf5f0e8, "paper": 0xffffff, "leather": 0x554433,
            "wax": 0x993333, "herb": 0x557755, "cobweb": 0xdddddd,
            "stain_dark": 0xaa9988, "stain_red": 0xbb8888,
        }
    }
    c = colors.get(mode, colors["gaslight"])
    creep = intensity / 5.0

    def hx(v):
        return f"0x{v:06x}"

    html = f'''
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
*{{margin:0;padding:0;box-sizing:border-box;}}
html,body{{width:100%;height:100%;overflow:hidden;background:#{c["bg"]:06x};font-family:Georgia,serif;}}
#container{{width:100%;height:100%;position:relative;cursor:grab;}}
#container:active{{cursor:grabbing;}}
canvas{{display:block;width:100%!important;height:100%!important;}}
#info{{position:absolute;bottom:15px;left:50%;transform:translateX(-50%);color:{c["text"]};font-size:12px;opacity:0.6;text-shadow:0 0 8px rgba(0,0,0,0.9);z-index:100;pointer-events:none;text-align:center;}}
#mode-label{{position:absolute;top:15px;left:15px;color:{c["text"]};font-size:10px;text-transform:uppercase;letter-spacing:3px;opacity:0.4;z-index:100;pointer-events:none;}}
#tooltip{{position:absolute;background:rgba(0,0,0,0.92);color:{c["text"]};padding:12px 16px;border-radius:4px;font-size:13px;max-width:260px;line-height:1.5;pointer-events:none;opacity:0;transition:opacity 0.3s;z-index:200;border:1px solid {c["text"]}44;}}
#tooltip.visible{{opacity:1;}}
#tooltip .title{{font-weight:bold;margin-bottom:4px;}}
#tooltip .lore{{font-style:italic;font-size:11px;margin-top:6px;opacity:0.7;border-top:1px solid {c["text"]}33;padding-top:6px;}}
.vignette{{position:absolute;top:0;left:0;width:100%;height:100%;pointer-events:none;background:radial-gradient(ellipse at center,transparent 40%,rgba(0,0,0,{0.4+creep*0.25 if mode!='clinical' else 0.05}) 100%);z-index:50;}}
#uv-overlay{{position:absolute;top:0;left:0;width:100%;height:100%;background:rgba(30,0,80,0.0);pointer-events:none;z-index:55;transition:background 0.5s;}}
#uv-btn{{position:absolute;top:15px;right:15px;background:rgba(0,0,0,0.7);color:{c["text"]};border:1px solid {c["text"]}66;padding:8px 14px;font-family:Georgia,serif;font-size:12px;cursor:pointer;z-index:200;border-radius:3px;transition:all 0.3s;}}
#uv-btn:hover{{border-color:{c["text"]};background:rgba(0,0,0,0.9);}}
#uv-btn.active{{background:rgba(60,0,120,0.8);border-color:#9944ff;color:#bb88ff;}}

/* Detail Panel */
#detail-overlay{{position:absolute;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.7);z-index:300;opacity:0;pointer-events:none;transition:opacity 0.4s ease;}}
#detail-overlay.active{{opacity:1;pointer-events:auto;}}

#detail-panel{{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%) scale(0.9);width:440px;max-width:92%;max-height:85%;background:{'rgba(26,20,16,0.97)' if mode=='gaslight' else 'rgba(10,5,5,0.97)' if mode=='gothic' else 'rgba(250,250,248,0.97)'};border:1px solid {c["text"]}66;border-radius:6px;z-index:310;opacity:0;transition:all 0.4s ease;overflow-y:auto;box-shadow:0 0 60px rgba(0,0,0,0.6);}}
#detail-overlay.active #detail-panel{{opacity:1;transform:translate(-50%,-50%) scale(1);}}

#detail-panel .dp-header{{padding:16px 20px 12px;border-bottom:1px solid {c["text"]}33;display:flex;justify-content:space-between;align-items:center;}}
#detail-panel .dp-title{{font-family:Georgia,serif;font-size:18px;font-weight:bold;color:{c["text"]};letter-spacing:1px;}}
#detail-panel .dp-close{{background:none;border:1px solid {c["text"]}44;color:{c["text"]};width:30px;height:30px;border-radius:50%;cursor:pointer;font-size:16px;display:flex;align-items:center;justify-content:center;transition:all 0.2s;}}
#detail-panel .dp-close:hover{{border-color:{c["text"]};background:{'rgba(139,0,0,0.3)' if mode=='gothic' else 'rgba(255,255,255,0.1)'};}}

#detail-panel .dp-canvas-wrap{{display:flex;justify-content:center;padding:20px;background:{'rgba(0,0,0,0.2)' if mode!='clinical' else 'rgba(0,0,0,0.05)'};}}
#detail-canvas{{border-radius:4px;}}

#detail-panel .dp-body{{padding:16px 20px;}}
#detail-panel .dp-desc{{font-family:Georgia,serif;color:{c["text"]};font-size:13px;line-height:1.7;margin-bottom:12px;}}
#detail-panel .dp-lore{{font-family:Georgia,serif;color:{c["text"]};font-size:12px;font-style:italic;line-height:1.6;opacity:0.75;padding:10px 14px;border-left:3px solid {'#8b0000' if mode=='gothic' else c["text"]}66;margin-bottom:14px;background:{'rgba(139,0,0,0.08)' if mode=='gothic' else 'rgba(255,255,255,0.03)'};}}
#detail-panel .dp-warning{{font-family:Georgia,serif;font-size:11px;color:{'#cc4444' if mode!='clinical' else '#993333'};padding:8px 12px;border:1px solid {'#cc444433' if mode!='clinical' else '#99333333'};border-radius:3px;margin-bottom:14px;}}

#detail-panel .dp-actions{{display:flex;gap:10px;padding:0 20px 16px;}}
#detail-panel .dp-btn{{flex:1;padding:10px;font-family:Georgia,serif;font-size:13px;cursor:pointer;border-radius:3px;transition:all 0.3s;text-align:center;}}
#detail-panel .dp-btn-shake{{background:{'rgba(139,69,19,0.3)' if mode=='gaslight' else 'rgba(139,0,0,0.3)' if mode=='gothic' else 'rgba(47,79,79,0.15)'};border:1px solid {c["text"]}44;color:{c["text"]};}}
#detail-panel .dp-btn-shake:hover{{border-color:{c["text"]};background:{'rgba(139,69,19,0.5)' if mode=='gaslight' else 'rgba(139,0,0,0.5)' if mode=='gothic' else 'rgba(47,79,79,0.25)'};}}
#detail-panel .dp-btn-shake.shaking{{animation:btnPulse 0.6s ease;}}

@keyframes btnPulse{{0%{{transform:scale(1);}}50%{{transform:scale(0.95);}}100%{{transform:scale(1);}}}}
@keyframes bottleShake{{0%,100%{{transform:translate(0,0) rotate(0deg);}}10%{{transform:translate(-8px,2px) rotate(-4deg);}}20%{{transform:translate(6px,-2px) rotate(3deg);}}30%{{transform:translate(-6px,1px) rotate(-3deg);}}40%{{transform:translate(5px,-1px) rotate(2deg);}}50%{{transform:translate(-4px,1px) rotate(-2deg);}}60%{{transform:translate(3px,0) rotate(1deg);}}70%{{transform:translate(-2px,0) rotate(-1deg);}}80%{{transform:translate(1px,0) rotate(0.5deg);}}90%{{transform:translate(-1px,0) rotate(0deg);}}}}
#detail-canvas.shaking{{animation:bottleShake 0.7s ease;}}
</style>
</head>
<body>
<div id="container"></div>
<div class="vignette"></div>
<div id="uv-overlay"></div>
<div id="mode-label">{mode.upper()} · INTENSITY {intensity}</div>
<div id="info">Drag to orbit · Scroll to zoom · Click objects to examine</div>
<button id="uv-btn" onclick="toggleUV()">🔦 UV Light</button>
<div id="tooltip"><div class="title"></div><div class="desc"></div><div class="lore"></div></div>

<div id="detail-overlay" onclick="if(event.target===this)closeDetail()">
  <div id="detail-panel">
    <div class="dp-header">
      <div class="dp-title" id="dp-title"></div>
      <button class="dp-close" onclick="closeDetail()">✕</button>
    </div>
    <div class="dp-canvas-wrap">
      <canvas id="detail-canvas" width="240" height="320"></canvas>
    </div>
    <div class="dp-body">
      <div class="dp-desc" id="dp-desc"></div>
      <div class="dp-warning" id="dp-warning"></div>
      <div class="dp-lore" id="dp-lore"></div>
    </div>
    <div class="dp-actions">
      <button class="dp-btn dp-btn-shake" onclick="shakeBottle()">🫗 Shake Bottle</button>
    </div>
  </div>
</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script>
(function(){{
'use strict';

const MODE = '{mode}';
const INTENSITY = {intensity};
const CREEP = {creep};
let uvMode = false;

const container = document.getElementById('container');
const W = container.clientWidth||window.innerWidth;
const H = container.clientHeight||window.innerHeight;

const scene = new THREE.Scene();
scene.background = new THREE.Color({hx(c["bg"])});
if (MODE !== 'clinical') scene.fog = new THREE.FogExp2({hx(c["bg"])}, 0.04);

const camera = new THREE.PerspectiveCamera(50, W/H, 0.1, 100);
camera.position.set(0, 1.5, 4);
camera.lookAt(0, 1, 0);

const renderer = new THREE.WebGLRenderer({{ antialias:true }});
renderer.setSize(W, H);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
container.appendChild(renderer.domElement);

const raycaster = new THREE.Raycaster();
const clickable = [];

// Materials
const woodMat = new THREE.MeshLambertMaterial({{ color:{hx(c["wood"])} }});
const darkWoodMat = new THREE.MeshLambertMaterial({{ color:{hx(c["wood_dark"])} }});
const metalMat = new THREE.MeshLambertMaterial({{ color:{hx(c["metal"])} }});
const boneMat = new THREE.MeshLambertMaterial({{ color:{hx(c["bone"])} }});
const paperMat = new THREE.MeshLambertMaterial({{ color:{hx(c["paper"])} }});
const leatherMat = new THREE.MeshLambertMaterial({{ color:{hx(c["leather"])} }});
const glassMat = new THREE.MeshLambertMaterial({{ color:{hx(c["glass"])}, transparent:true, opacity:0.5 }});
const waxMat = new THREE.MeshLambertMaterial({{ color:{hx(c["wax"])} }});
const herbMat = new THREE.MeshLambertMaterial({{ color:{hx(c["herb"])} }});
const cobwebMat = new THREE.MeshBasicMaterial({{ color:{hx(c["cobweb"])}, transparent:true, opacity:0.15, side:THREE.DoubleSide }});

// Lights
scene.add(new THREE.AmbientLight(0xffffff, 0.25));
scene.add(new THREE.HemisphereLight(0xffffff, {hx(c["wood_dark"])}, 0.3));

// Main candle light
const candleLight = new THREE.PointLight({hx(c["light"])}, 1.2, 8);
candleLight.position.set(-0.9, 2.4, 0.3);
candleLight.castShadow = true;
scene.add(candleLight);

// Fill lights
const fillLight = new THREE.DirectionalLight({hx(c["light"])}, 0.5);
fillLight.position.set(3, 5, 4);
scene.add(fillLight);

// UV light (hidden initially)
const uvLight = new THREE.PointLight(0x6600cc, 0, 10);
uvLight.position.set(0, 3, 2);
scene.add(uvLight);

// UV hidden elements group
const uvElements = new THREE.Group();
uvElements.visible = false;
scene.add(uvElements);

// ============ CABINET BODY ============
const cabinet = new THREE.Group();

// Main body
const back = new THREE.Mesh(new THREE.BoxGeometry(3.2, 3.0, 0.08), darkWoodMat);
back.position.set(0, 1.5, -0.45);
back.receiveShadow = true;
cabinet.add(back);

// Sides
[-1.6, 1.6].forEach(x => {{
    const side = new THREE.Mesh(new THREE.BoxGeometry(0.08, 3.0, 0.95), woodMat);
    side.position.set(x, 1.5, 0);
    side.castShadow = true;
    cabinet.add(side);
}});

// Top
const top = new THREE.Mesh(new THREE.BoxGeometry(3.4, 0.1, 1.05), woodMat);
top.position.set(0, 3.05, 0);
cabinet.add(top);

// Bottom
const bottom = new THREE.Mesh(new THREE.BoxGeometry(3.2, 0.12, 0.95), woodMat);
bottom.position.set(0, 0.06, 0);
cabinet.add(bottom);

// Crown molding
const crown = new THREE.Mesh(new THREE.BoxGeometry(3.5, 0.08, 0.15), woodMat);
crown.position.set(0, 3.12, 0.42);
cabinet.add(crown);

// Shelves (4 shelves)
const shelfYs = [0.65, 1.3, 1.95, 2.55];
shelfYs.forEach(y => {{
    const shelf = new THREE.Mesh(new THREE.BoxGeometry(3.1, 0.06, 0.88), woodMat);
    shelf.position.set(0, y, 0);
    shelf.receiveShadow = true;
    cabinet.add(shelf);
}});

// ============ STAINS ON WOOD ============
const stainPositions = [
    {{ x:-0.5, y:0.68, type:'ring' }}, {{ x:0.8, y:1.33, type:'ring' }},
    {{ x:-0.3, y:1.98, type:'spill' }}, {{ x:1.1, y:0.68, type:'dark' }}
];
stainPositions.forEach(s => {{
    const stainColor = s.type === 'dark' ? {hx(c["stain_red"])} : {hx(c["stain_dark"])};
    const stain = new THREE.Mesh(
        new THREE.CircleGeometry(s.type === 'ring' ? 0.08 : 0.12, 12),
        new THREE.MeshBasicMaterial({{ color: stainColor, transparent: true, opacity: 0.3 }})
    );
    stain.rotation.x = -Math.PI / 2;
    stain.position.set(s.x, s.y + 0.035, 0.1);
    cabinet.add(stain);
    // Ring stain: hollow center
    if (s.type === 'ring') {{
        const inner = new THREE.Mesh(
            new THREE.CircleGeometry(0.05, 12),
            new THREE.MeshBasicMaterial({{ color: {hx(c["wood"])}, transparent: true, opacity: 0.4 }})
        );
        inner.rotation.x = -Math.PI / 2;
        inner.position.set(s.x, s.y + 0.036, 0.1);
        cabinet.add(inner);
    }}
}});

scene.add(cabinet);

// ============ BOTTLES ============
const bottleData = [
    // Shelf 1 (bottom)
    {{ x:-1.0, y:0.68, h:0.35, r:0.06, color:0xaa4444, label:'Laudanum', desc:'Tincture of opium dissolved in alcohol. Approximately 10% opium by weight. Prescribed for pain, insomnia, and hysteria.', lore:'Half empty. Someone has been dosing regularly. The neck shows fingerprints — hurried, frantic grabs.', warning:'Highly addictive. Withdrawal may prove fatal.' }},
    {{ x:-0.5, y:0.68, h:0.28, r:0.07, color:0x44aa44, label:'Strychnine', desc:'Poison in large doses, stimulant in minute quantities. Extracted from the seeds of Strychnos nux-vomica.', lore:'Fitzroy kept this close. Always. The seal has been broken and resealed multiple times.', warning:'LETHAL. Even small miscalculations in dosage are fatal.' }},
    {{ x:0.0, y:0.68, h:0.4, r:0.05, color:0x4444aa, label:'Mercury Chloride', desc:'Antiseptic and disinfectant. Used in treatment of syphilis. Corrosive to organic tissue.', lore:'The standard treatment. The standard death. Three patients this month alone.', warning:'Corrosive poison. Causes organ failure with prolonged use.' }},
    {{ x:0.5, y:0.68, h:0.3, r:0.065, color:0xaa8844, label:'Chloroform', desc:'Anaesthetic compound. Sweet-smelling volatile liquid used to render patients unconscious.', lore:'How many were silenced with this? The cloth beside it is still damp.', warning:'Overdose causes cardiac arrest. Handle in ventilated area.' }},
    // Shelf 2
    {{ x:-0.8, y:1.33, h:0.32, r:0.055, color:0x884488, label:'Belladonna', desc:'Extract of deadly nightshade. Dilates pupils, reduces secretions. Used in eye examinations.', lore:'"Beautiful lady." The irony is not lost. Women took this to appear attractive — and died for it.', warning:'Toxic alkaloid. Hallucinations precede death.' }},
    {{ x:-0.2, y:1.33, h:0.38, r:0.06, color:0xcc8833, label:'Vita Aeterna', desc:'The label is handwritten in careful script. The liquid glows faintly amber, as if lit from within.', lore:'Protocol Seven. The key ingredient. No known pharmaceutical formula matches this compound.', warning:'UNKNOWN SUBSTANCE. No dosage guidelines exist.' }},
    {{ x:0.5, y:1.33, h:0.25, r:0.07, color:0x448888, label:'Ether', desc:'Volatile anaesthetic compound. Inhaled to produce unconsciousness. Highly flammable.', lore:'The smell of progress. And forgetting. How convenient.', warning:'Extremely flammable. Explosive when concentrated.' }},
    {{ x:1.1, y:1.33, h:0.35, r:0.05, color:0x888844, label:'Arsenic', desc:'The king of poisons. White powder, nearly tasteless. Used in pesticides and, historically, murder.', lore:'Three deaths this quarter. Same symptoms. Same ward. Coincidence?', warning:'LETHAL. Symptoms mimic natural illness — the perfect poison.' }},
    // Shelf 3
    {{ x:-1.0, y:1.98, h:0.3, r:0.06, color:0xaa2222, label:'Blood Sample', desc:'Dark, almost black fluid in a sealed vessel. Viscosity is unusual — thicker than expected for human blood.', lore:'Label reads: "S.C." Sebastian Carlisle. Why is his blood being preserved?', warning:'Biohazard. Unknown pathogenic properties.' }},
    {{ x:-0.3, y:1.98, h:0.35, r:0.055, color:0x66aa66, label:'Digitalis', desc:'Extract of foxglove. Strengthens and regulates heartbeat. Critical cardiac medicine.', lore:'The difference between medicine and murder is dosage. Fitzroy knew this well.', warning:'Narrow therapeutic window. Overdose causes fatal arrhythmia.' }},
    {{ x:0.4, y:1.98, h:0.28, r:0.065, color:0xdddd44, label:'Phosphorus', desc:'Luminescent element. Glows pale green in darkness. Burns spontaneously on contact with air.', lore:'Used in the development process. Details redacted from all official records.', warning:'INCENDIARY. Contact with skin causes deep chemical burns.' }},
    {{ x:1.0, y:1.98, h:0.32, r:0.06, color:0x222222, label:'[UNMARKED]', desc:'No label. No markings. The glass is warm to the touch despite the cold room. The liquid inside is perfectly still.', lore:'DO NOT OPEN. DO NOT OPEN. DO NOT OPEN.', warning:'CONTENTS UNKNOWN. Do not handle without authorization.' }},
    // Shelf 4 (top)
    {{ x:-0.6, y:2.58, h:0.22, r:0.05, color:0xcc4444, label:'Morphine', desc:'Distilled mercy. Extracted from opium. The most powerful analgesic known to medicine.', lore:'Requisitioned in bulk — 40 vials this month. For what? The ward only holds twelve patients.', warning:'Profoundly addictive. Respiratory depression at high doses.' }},
    {{ x:0.1, y:2.58, h:0.3, r:0.06, color:0x8888cc, label:'Formaldehyde', desc:'Preservation fluid. Prevents decomposition of organic tissue. Sharp, penetrating odour.', lore:'The dead must be kept fresh for study. But some of these specimens predate the hospital.', warning:'Toxic vapours. Suspected carcinogen.' }},
    {{ x:0.8, y:2.58, h:0.26, r:0.055, color:0xccaa88, label:'Quinine', desc:'Antimalarial derived from cinchona bark. Bitter crystalline compound dissolved in tonic water.', lore:'Imported. Expensive. Who pays for a workhouse hospital to stock luxury medicines?', warning:'Cardiac toxicity at high doses. Causes cinchonism.' }},
];

const bottles = [];
bottleData.forEach((b, idx) => {{
    const bottle = new THREE.Group();

    // Body
    const body = new THREE.Mesh(
        new THREE.CylinderGeometry(b.r, b.r * 0.9, b.h, 12),
        new THREE.MeshLambertMaterial({{
            color: b.color, transparent: true, opacity: 0.65,
            emissive: b.color, emissiveIntensity: MODE === 'gothic' ? 0.15 : 0.05
        }})
    );
    body.position.y = b.h / 2;
    body.castShadow = true;
    bottle.add(body);

    // Neck
    const neck = new THREE.Mesh(
        new THREE.CylinderGeometry(b.r * 0.4, b.r * 0.6, b.h * 0.25, 8),
        new THREE.MeshLambertMaterial({{ color: b.color, transparent: true, opacity: 0.5 }})
    );
    neck.position.y = b.h + b.h * 0.12;
    bottle.add(neck);

    // Cork
    const cork = new THREE.Mesh(
        new THREE.CylinderGeometry(b.r * 0.42, b.r * 0.38, 0.06, 8),
        new THREE.MeshLambertMaterial({{ color: 0x8b7355 }})
    );
    cork.position.y = b.h + b.h * 0.27;
    bottle.add(cork);

    // Liquid inside
    const liquid = new THREE.Mesh(
        new THREE.CylinderGeometry(b.r * 0.85, b.r * 0.82, b.h * 0.6, 10),
        new THREE.MeshBasicMaterial({{ color: b.color, transparent: true, opacity: 0.35 }})
    );
    liquid.position.y = b.h * 0.32;
    bottle.add(liquid);

    // Label
    const label = new THREE.Mesh(
        new THREE.PlaneGeometry(b.r * 1.8, b.h * 0.35),
        new THREE.MeshLambertMaterial({{ color: {hx(c["paper"])}, side: THREE.DoubleSide }})
    );
    label.position.set(0, b.h * 0.45, b.r + 0.005);
    bottle.add(label);

    bottle.position.set(b.x, b.y, 0.05);
    const hexColor = '#' + b.color.toString(16).padStart(6, '0');
    bottle.userData = {{ type: 'bottle', title: b.label, desc: b.desc, lore: INTENSITY >= 2 ? b.lore : '', color: hexColor, warning: b.warning || '' }};

    scene.add(bottle);
    bottles.push(bottle);
    clickable.push(bottle);

    // UV hidden text for select bottles
    if (idx === 5 || idx === 11) {{ // Vita Aeterna, Unmarked
        const uvText = new THREE.Mesh(
            new THREE.PlaneGeometry(b.r * 2, b.h * 0.25),
            new THREE.MeshBasicMaterial({{ color: 0xaa00ff, transparent: true, opacity: 0.8, side: THREE.DoubleSide }})
        );
        uvText.position.set(b.x, b.y + b.h * 0.7, b.r + 0.02);
        uvElements.add(uvText);
    }}
}});

// ============ COBWEBS ============
const cobwebPositions = [
    {{ x: -1.4, y: 2.8, z: -0.2 }}, {{ x: 1.4, y: 2.65, z: -0.1 }},
    {{ x: -0.7, y: 1.85, z: 0.15 }}, {{ x: 1.3, y: 1.2, z: 0.1 }},
];
cobwebPositions.forEach(pos => {{
    const web = new THREE.Mesh(
        new THREE.PlaneGeometry(0.35, 0.3),
        cobwebMat
    );
    web.position.set(pos.x, pos.y, pos.z);
    web.rotation.y = Math.random() * 0.5;
    web.rotation.z = Math.random() * 0.3;
    scene.add(web);

    // Thread lines
    for (let i = 0; i < 3; i++) {{
        const thread = new THREE.Mesh(
            new THREE.CylinderGeometry(0.001, 0.001, 0.2 + Math.random() * 0.15, 3),
            cobwebMat
        );
        thread.position.set(pos.x + (Math.random() - 0.5) * 0.2, pos.y - 0.1, pos.z + 0.02);
        thread.rotation.z = Math.random() * Math.PI;
        scene.add(thread);
    }}
}});

// ============ SKULL (MEMENTO MORI) ============
const skull = new THREE.Group();
skull.userData = {{ type: 'skull', title: 'Human Skull', desc: 'Memento mori. A reminder of what awaits.', lore: INTENSITY >= 3 ? 'The jaw is wired shut. What was it trying to say?' : 'Teaching specimen. Probably.' }};

// Cranium
const cranium = new THREE.Mesh(
    new THREE.SphereGeometry(0.16, 16, 12),
    boneMat
);
cranium.scale.set(1, 1.1, 1.2);
cranium.position.y = 0.16;
skull.add(cranium);

// Eye sockets
[-0.05, 0.05].forEach(x => {{
    const socket = new THREE.Mesh(
        new THREE.SphereGeometry(0.04, 8, 6),
        new THREE.MeshBasicMaterial({{ color: 0x111111 }})
    );
    socket.position.set(x, 0.15, 0.14);
    skull.add(socket);

    // Eerie glow in gothic
    if (MODE === 'gothic' && INTENSITY >= 4) {{
        const eyeGlow = new THREE.Mesh(
            new THREE.SphereGeometry(0.02, 6, 4),
            new THREE.MeshBasicMaterial({{ color: 0xff2200, transparent: true, opacity: 0.6 }})
        );
        eyeGlow.position.set(x, 0.15, 0.13);
        skull.add(eyeGlow);
    }}
}});

// Nose
const nose = new THREE.Mesh(
    new THREE.SphereGeometry(0.018, 6, 4),
    new THREE.MeshBasicMaterial({{ color: 0x111111 }})
);
nose.position.set(0, 0.1, 0.15);
skull.add(nose);

// Jaw
const jaw = new THREE.Mesh(
    new THREE.BoxGeometry(0.14, 0.04, 0.08),
    boneMat
);
jaw.position.set(0, 0.04, 0.1);
skull.add(jaw);

// Teeth
for (let i = 0; i < 6; i++) {{
    const tooth = new THREE.Mesh(
        new THREE.BoxGeometry(0.015, 0.02, 0.01),
        new THREE.MeshLambertMaterial({{ color: 0xddddbb }})
    );
    tooth.position.set(-0.04 + i * 0.016, 0.065, 0.13);
    skull.add(tooth);
}}

skull.position.set(1.1, 3.12, 0.15);
skull.rotation.y = -0.3;
scene.add(skull);
clickable.push(skull);

// ============ CANDLE WITH DRIPPING WAX ============
const candleGroup = new THREE.Group();
candleGroup.userData = {{ type: 'candle', title: 'Tallow Candle', desc: 'The sole light source. Wax pools at the base.', lore: 'It burns lower every time you look away.' }};

// Holder
const candleHolder = new THREE.Mesh(
    new THREE.CylinderGeometry(0.1, 0.12, 0.04, 12),
    metalMat
);
candleGroup.add(candleHolder);

// Handle
const handle = new THREE.Mesh(
    new THREE.TorusGeometry(0.08, 0.012, 6, 12, Math.PI),
    metalMat
);
handle.rotation.y = Math.PI / 2;
handle.position.set(0.08, 0.02, 0);
candleGroup.add(handle);

// Candle body
const candleBody = new THREE.Mesh(
    new THREE.CylinderGeometry(0.035, 0.04, 0.25, 8),
    new THREE.MeshLambertMaterial({{ color: 0xfffff0 }})
);
candleBody.position.y = 0.145;
candleGroup.add(candleBody);

// Flame
const flame = new THREE.Mesh(
    new THREE.SphereGeometry(0.025, 6, 4),
    new THREE.MeshBasicMaterial({{ color: {hx(c["light"])}, transparent: true, opacity: 0.95 }})
);
flame.scale.set(0.7, 1.4, 0.7);
flame.position.y = 0.3;
candleGroup.add(flame);

// Flame inner
const flameInner = new THREE.Mesh(
    new THREE.SphereGeometry(0.012, 4, 3),
    new THREE.MeshBasicMaterial({{ color: 0xffffff, transparent: true, opacity: 0.9 }})
);
flameInner.position.y = 0.29;
candleGroup.add(flameInner);

// Wax drips
const drips = [
    {{ x: 0.03, h: 0.06 }}, {{ x: -0.02, h: 0.08 }}, {{ x: 0.01, h: 0.04 }}
];
drips.forEach(d => {{
    const drip = new THREE.Mesh(
        new THREE.CylinderGeometry(0.008, 0.005, d.h, 6),
        new THREE.MeshLambertMaterial({{ color: 0xfffff0 }})
    );
    drip.position.set(d.x, 0.04 + d.h / 2, 0.035);
    candleGroup.add(drip);
}});

// Wax pool
const waxPool = new THREE.Mesh(
    new THREE.CircleGeometry(0.08, 12),
    new THREE.MeshLambertMaterial({{ color: 0xfffff0, transparent: true, opacity: 0.6 }})
);
waxPool.rotation.x = -Math.PI / 2;
waxPool.position.y = 0.005;
candleGroup.add(waxPool);

candleGroup.position.set(-0.9, 3.12, 0.3);
scene.add(candleGroup);
clickable.push(candleGroup);

// ============ LEATHER-BOUND BOOKS ============
const books = new THREE.Group();
books.userData = {{ type: 'books', title: 'Medical Texts', desc: 'Gray\\'s Anatomy. Fitzroy\\'s Compendium. One unmarked volume.', lore: INTENSITY >= 3 ? 'The unmarked book falls open to a page about preserving consciousness during vivisection.' : 'Standard reference material.' }};

const bookColors = [0x2a1510, 0x1a2a1a, 0x1a1a2a, 0x3a2515];
bookColors.forEach((bc, i) => {{
    const book = new THREE.Mesh(
        new THREE.BoxGeometry(0.18, 0.28, 0.04 + i * 0.008),
        new THREE.MeshLambertMaterial({{ color: bc }})
    );
    book.position.set(0, i * 0.045, 0);
    book.rotation.y = (Math.random() - 0.5) * 0.15;

    // Gold detail on spine
    const spine = new THREE.Mesh(
        new THREE.PlaneGeometry(0.02, 0.25),
        new THREE.MeshBasicMaterial({{ color: {hx(c["metal"])}, transparent: true, opacity: 0.5 }})
    );
    spine.position.set(-0.091, 0, 0);
    spine.rotation.y = -Math.PI / 2;
    book.add(spine);

    books.add(book);
}});

// One book pulled out
const pulledBook = new THREE.Mesh(
    new THREE.BoxGeometry(0.18, 0.28, 0.035),
    leatherMat
);
pulledBook.position.set(0.06, 0.18, 0.05);
pulledBook.rotation.y = 0.2;
books.add(pulledBook);

books.position.set(-1.1, 3.14, -0.1);
scene.add(books);
clickable.push(books);

// ============ BRASS BALANCE SCALES ============
const scales = new THREE.Group();
scales.userData = {{ type: 'scales', title: 'Apothecary Scales', desc: 'Brass balance. One pan lower than the other.', lore: INTENSITY >= 3 ? 'The lower pan holds a residue. Reddish. Organic.' : 'For measuring precise doses.' }};

// Pillar
const pillar = new THREE.Mesh(new THREE.CylinderGeometry(0.015, 0.02, 0.35, 8), metalMat);
pillar.position.y = 0.175;
scales.add(pillar);

// Base
const sBase = new THREE.Mesh(new THREE.CylinderGeometry(0.08, 0.1, 0.02, 12), metalMat);
scales.add(sBase);

// Beam
const beam = new THREE.Mesh(new THREE.BoxGeometry(0.35, 0.01, 0.015), metalMat);
beam.position.y = 0.36;
beam.rotation.z = 0.08; // tilted
scales.add(beam);

// Pans
[-0.16, 0.16].forEach((x, i) => {{
    const panY = 0.3 + (i === 0 ? -0.02 : 0.02);
    const pan = new THREE.Mesh(new THREE.CylinderGeometry(0.06, 0.06, 0.008, 12), metalMat);
    pan.position.set(x, panY, 0);
    scales.add(pan);
    // Chains
    for (let c = 0; c < 3; c++) {{
        const chain = new THREE.Mesh(new THREE.CylinderGeometry(0.002, 0.002, 0.06, 4), metalMat);
        const a = (c / 3) * Math.PI * 2;
        chain.position.set(x + Math.cos(a) * 0.04, panY + 0.035, Math.sin(a) * 0.04);
        scales.add(chain);
    }}
}});

scales.position.set(0.7, 2.58, 0.2);
scene.add(scales);
clickable.push(scales);

// ============ MORTAR AND PESTLE ============
const mortar = new THREE.Group();
mortar.userData = {{ type: 'mortar', title: 'Mortar & Pestle', desc: 'Stone. Well-used. Stained with unknown compounds.', lore: 'The residue matches no known pharmaceutical.' }};

// Mortar bowl
const mortarBowl = new THREE.Mesh(
    new THREE.CylinderGeometry(0.07, 0.05, 0.08, 12),
    new THREE.MeshLambertMaterial({{ color: 0x666655 }})
);
mortarBowl.position.y = 0.04;
mortar.add(mortarBowl);

// Pestle
const pestle = new THREE.Mesh(
    new THREE.CylinderGeometry(0.012, 0.025, 0.16, 8),
    new THREE.MeshLambertMaterial({{ color: 0x777766 }})
);
pestle.position.set(0.03, 0.1, 0.02);
pestle.rotation.z = 0.5;
pestle.rotation.x = -0.3;
mortar.add(pestle);

mortar.position.set(-0.3, 2.58, 0.25);
scene.add(mortar);
clickable.push(mortar);

// ============ VICTORIAN SYRINGE ============
const syringe = new THREE.Group();
syringe.userData = {{ type: 'syringe', title: 'Hypodermic Syringe', desc: 'Brass and glass. Victorian medical instrument.', lore: INTENSITY >= 3 ? 'Residue inside: laudanum and something else. Something unknown.' : 'Standard issue.' }};

// Barrel (glass)
const barrel = new THREE.Mesh(
    new THREE.CylinderGeometry(0.015, 0.015, 0.18, 8),
    new THREE.MeshLambertMaterial({{ color: 0xccddee, transparent: true, opacity: 0.5 }})
);
barrel.rotation.z = Math.PI / 2;
syringe.add(barrel);

// Plunger handle
const plunger = new THREE.Mesh(
    new THREE.CylinderGeometry(0.02, 0.02, 0.03, 6),
    metalMat
);
plunger.position.set(-0.1, 0, 0);
plunger.rotation.z = Math.PI / 2;
syringe.add(plunger);

// Needle
const needle = new THREE.Mesh(
    new THREE.CylinderGeometry(0.002, 0.001, 0.06, 4),
    new THREE.MeshLambertMaterial({{ color: 0xcccccc }})
);
needle.position.set(0.12, 0, 0);
needle.rotation.z = Math.PI / 2;
syringe.add(needle);

// Finger rings
const ring = new THREE.Mesh(new THREE.TorusGeometry(0.025, 0.004, 4, 8), metalMat);
ring.position.set(-0.09, 0, 0);
ring.rotation.x = Math.PI / 2;
syringe.add(ring);

syringe.position.set(0.2, 1.35, 0.35);
syringe.rotation.y = 0.3;
scene.add(syringe);
clickable.push(syringe);

// ============ MAGNIFYING GLASS ============
const magGlass = new THREE.Group();
magGlass.userData = {{ type: 'magnifier', title: 'Magnifying Glass', desc: 'Brass frame. The lens distorts what lies beneath.', lore: 'Under magnification, the labels reveal a second language.' }};

// Lens
const lens = new THREE.Mesh(
    new THREE.CircleGeometry(0.06, 16),
    new THREE.MeshLambertMaterial({{ color: 0xccddff, transparent: true, opacity: 0.3, side: THREE.DoubleSide }})
);
magGlass.add(lens);

// Frame
const frame = new THREE.Mesh(
    new THREE.TorusGeometry(0.06, 0.006, 6, 16),
    metalMat
);
magGlass.add(frame);

// Handle
const mgHandle = new THREE.Mesh(
    new THREE.CylinderGeometry(0.008, 0.01, 0.15, 6),
    metalMat
);
mgHandle.position.set(0, -0.12, 0);
magGlass.add(mgHandle);

magGlass.position.set(1.1, 1.35, 0.3);
magGlass.rotation.z = -0.4;
magGlass.rotation.x = -0.2;
scene.add(magGlass);
clickable.push(magGlass);

// ============ POCKET WATCH ============
const watch = new THREE.Group();
watch.userData = {{ type: 'watch', title: 'Pocket Watch', desc: 'Gold case. The hands have stopped at 11:47.', lore: INTENSITY >= 3 ? 'Time of death? Or time of the next appointment?' : 'Engraved: A.F.' }};

const watchCase = new THREE.Mesh(new THREE.CylinderGeometry(0.04, 0.04, 0.01, 16), metalMat);
watch.add(watchCase);
const watchFace = new THREE.Mesh(
    new THREE.CircleGeometry(0.035, 16),
    new THREE.MeshLambertMaterial({{ color: 0xfffff0 }})
);
watchFace.position.z = 0.006;
watch.add(watchFace);

// Chain
for (let i = 0; i < 8; i++) {{
    const link = new THREE.Mesh(
        new THREE.TorusGeometry(0.008, 0.002, 4, 6),
        metalMat
    );
    link.position.set(0.04 + i * 0.015, 0.01 * Math.sin(i), 0);
    link.rotation.y = Math.PI / 2;
    watch.add(link);
}}

watch.position.set(-0.6, 1.35, 0.4);
watch.rotation.x = -Math.PI / 2.5;
scene.add(watch);
clickable.push(watch);

// ============ WAX SEAL STAMPS ============
const waxGroup = new THREE.Group();
waxGroup.userData = {{ type: 'wax', title: 'Sealing Wax & Stamp', desc: 'Red wax. A seal bearing a rose motif.', lore: 'The Red Rose Society\\'s official correspondence seal.' }};

// Wax stick
const waxStick = new THREE.Mesh(
    new THREE.CylinderGeometry(0.012, 0.012, 0.12, 6),
    waxMat
);
waxStick.rotation.z = Math.PI / 2;
waxStick.position.y = 0.012;
waxGroup.add(waxStick);

// Stamp
const stamp = new THREE.Mesh(new THREE.CylinderGeometry(0.025, 0.015, 0.08, 8), darkWoodMat);
stamp.position.set(0.08, 0.04, 0);
waxGroup.add(stamp);

// Wax blob
const blob = new THREE.Mesh(
    new THREE.SphereGeometry(0.02, 8, 6),
    waxMat
);
blob.scale.set(1.5, 0.4, 1.5);
blob.position.set(-0.05, 0.005, 0.03);
waxGroup.add(blob);

waxGroup.position.set(0.5, 0.68, 0.35);
scene.add(waxGroup);
clickable.push(waxGroup);

// ============ DRIED HERBS ============
const herbBundles = [];
const herbPositions = [
    {{ x: -0.8, desc: 'Dried lavender. For calm. Or concealment.' }},
    {{ x: -0.3, desc: 'Hemlock sprigs. Beautiful. Deadly.' }},
    {{ x: 0.2, desc: 'Wormwood. The base of absinthe.' }},
    {{ x: 0.7, desc: 'Belladonna leaves. Dried but still potent.' }},
];
herbPositions.forEach((h, i) => {{
    const herb = new THREE.Group();
    herb.userData = {{ type: 'herb', title: 'Dried Herbs', desc: h.desc, lore: '' }};

    // Bundle
    for (let s = 0; s < 4; s++) {{
        const stem = new THREE.Mesh(
            new THREE.CylinderGeometry(0.003, 0.003, 0.18 + Math.random() * 0.08, 4),
            herbMat
        );
        stem.position.set((Math.random() - 0.5) * 0.02, -0.06, (Math.random() - 0.5) * 0.02);
        herb.add(stem);

        // Leaves
        const leaf = new THREE.Mesh(
            new THREE.PlaneGeometry(0.03, 0.02),
            new THREE.MeshLambertMaterial({{ color: {hx(c["herb"])}, side: THREE.DoubleSide }})
        );
        leaf.position.set(stem.position.x, -0.12 - Math.random() * 0.04, stem.position.z + 0.01);
        leaf.rotation.z = Math.random() * 0.5;
        herb.add(leaf);
    }}

    // Twine
    const twine = new THREE.Mesh(
        new THREE.TorusGeometry(0.015, 0.003, 4, 8),
        new THREE.MeshLambertMaterial({{ color: 0x8b7355 }})
    );
    twine.position.y = 0.02;
    herb.add(twine);

    herb.position.set(h.x, 3.0, 0.15);
    herb.rotation.x = Math.PI;
    scene.add(herb);
    herbBundles.push(herb);
    clickable.push(herb);
}});

// ============ MOUSE (Intensity 2+) ============
let mouseGroup = null;
if (INTENSITY >= 2) {{
    mouseGroup = new THREE.Group();
    mouseGroup.userData = {{ type: 'mouse', title: 'A Mouse', desc: 'Small. Quick. Watching you with black eyes.', lore: INTENSITY >= 4 ? 'It\\'s been gnawing on something. Something pink.' : 'A common visitor.' }};

    const mouseBody = new THREE.Mesh(
        new THREE.SphereGeometry(0.03, 8, 6),
        new THREE.MeshLambertMaterial({{ color: 0x6a5a4a }})
    );
    mouseBody.scale.set(1, 0.8, 1.5);
    mouseGroup.add(mouseBody);

    const mouseHead = new THREE.Mesh(
        new THREE.SphereGeometry(0.018, 6, 5),
        new THREE.MeshLambertMaterial({{ color: 0x6a5a4a }})
    );
    mouseHead.position.set(0, 0.01, 0.035);
    mouseGroup.add(mouseHead);

    // Ears
    [-0.01, 0.01].forEach(x => {{
        const ear = new THREE.Mesh(
            new THREE.SphereGeometry(0.008, 4, 4),
            new THREE.MeshLambertMaterial({{ color: 0x997788 }})
        );
        ear.position.set(x, 0.025, 0.03);
        mouseGroup.add(ear);
    }});

    // Eyes
    [-0.007, 0.007].forEach(x => {{
        const eye = new THREE.Mesh(
            new THREE.SphereGeometry(0.004, 4, 4),
            new THREE.MeshBasicMaterial({{ color: 0x111111 }})
        );
        eye.position.set(x, 0.018, 0.05);
        mouseGroup.add(eye);
    }});

    // Tail
    const tail = new THREE.Mesh(
        new THREE.CylinderGeometry(0.002, 0.001, 0.08, 4),
        new THREE.MeshLambertMaterial({{ color: 0x997788 }})
    );
    tail.position.set(0, 0, -0.05);
    tail.rotation.x = 0.5;
    mouseGroup.add(tail);

    mouseGroup.position.set(0.9, 0.72, 0.3);
    mouseGroup.rotation.y = -0.8;
    scene.add(mouseGroup);
    clickable.push(mouseGroup);
}}

// ============ DRAWERS ============
const drawers = [];
for (let i = 0; i < 4; i++) {{
    const drawer = new THREE.Group();
    const dBody = new THREE.Mesh(new THREE.BoxGeometry(0.65, 0.3, 0.05), woodMat);
    drawer.add(dBody);

    const dHandle = new THREE.Mesh(new THREE.SphereGeometry(0.02, 6, 4), metalMat);
    dHandle.position.z = 0.035;
    drawer.add(dHandle);

    // Label plate
    const plate = new THREE.Mesh(
        new THREE.PlaneGeometry(0.12, 0.04),
        metalMat
    );
    plate.position.set(0, 0.06, 0.03);
    drawer.add(plate);

    const drawerLabels = ['Tinctures', 'Compounds', 'Specimens', 'Private'];
    const drawerLore = [
        'Standard medicines.', 'Experimental mixtures.',
        'Organic material. Handle with care.',
        INTENSITY >= 4 ? 'LOCKED. Scratches on the INSIDE.' : 'Locked.'
    ];

    drawer.position.set(-1.6 + i * 1.05 + 0.5, 0.3, 0.45);
    drawer.userData = {{ type: 'drawer', title: drawerLabels[i], desc: 'A labelled drawer.', lore: drawerLore[i] }};
    scene.add(drawer);
    drawers.push(drawer);
    clickable.push(drawer);
}}

// ============ UV BACK WALL MESSAGE ============
const uvMessage = new THREE.Mesh(
    new THREE.PlaneGeometry(2.5, 0.4),
    new THREE.MeshBasicMaterial({{ color: 0x9900ff, transparent: true, opacity: 0.7, side: THREE.DoubleSide }})
);
uvMessage.position.set(0, 1.8, -0.38);
uvElements.add(uvMessage);

// ============ DUST PARTICLES ============
const dustCount = 120 + INTENSITY * 30;
const dustGeo = new THREE.BufferGeometry();
const dustPos = new Float32Array(dustCount * 3);
const dustVel = [];
for (let i = 0; i < dustCount; i++) {{
    dustPos[i * 3] = (Math.random() - 0.5) * 3.5;
    dustPos[i * 3 + 1] = Math.random() * 3.5;
    dustPos[i * 3 + 2] = (Math.random() - 0.5) * 1.5;
    dustVel.push({{ y: 0.0005 + Math.random() * 0.001, x: (Math.random() - 0.5) * 0.0005 }});
}}
dustGeo.setAttribute('position', new THREE.BufferAttribute(dustPos, 3));
const dustParticles = new THREE.Points(dustGeo, new THREE.PointsMaterial({{
    color: {hx(c["glow"])}, size: 0.02, transparent: true, opacity: 0.4
}}));
scene.add(dustParticles);

// ============ CAMERA CONTROLS ============
let isDragging = false;
let prevMouse = {{ x: 0, y: 0 }};
let camAngle = 0, camHeight = 1.5, camDist = 4;

function updateCam() {{
    camera.position.x = Math.sin(camAngle) * camDist;
    camera.position.y = camHeight;
    camera.position.z = Math.cos(camAngle) * camDist;
    camera.lookAt(0, 1.3, 0);
}}

renderer.domElement.addEventListener('mousedown', e => {{ isDragging = true; prevMouse = {{ x: e.clientX, y: e.clientY }}; }});
renderer.domElement.addEventListener('mousemove', e => {{
    if (!isDragging) return;
    camAngle -= (e.clientX - prevMouse.x) * 0.008;
    camHeight = Math.max(0.5, Math.min(3.5, camHeight + (e.clientY - prevMouse.y) * 0.008));
    prevMouse = {{ x: e.clientX, y: e.clientY }};
    updateCam();
}});
window.addEventListener('mouseup', () => {{ isDragging = false; }});
renderer.domElement.addEventListener('wheel', e => {{
    e.preventDefault();
    camDist = Math.max(2, Math.min(7, camDist + e.deltaY * 0.01));
    updateCam();
}}, {{ passive: false }});

// Touch
renderer.domElement.addEventListener('touchstart', e => {{ if (e.touches.length === 1) {{ isDragging = true; prevMouse = {{ x: e.touches[0].clientX, y: e.touches[0].clientY }}; }} }});
renderer.domElement.addEventListener('touchmove', e => {{
    if (!isDragging || e.touches.length !== 1) return;
    camAngle -= (e.touches[0].clientX - prevMouse.x) * 0.008;
    camHeight = Math.max(0.5, Math.min(3.5, camHeight + (e.touches[0].clientY - prevMouse.y) * 0.008));
    prevMouse = {{ x: e.touches[0].clientX, y: e.touches[0].clientY }};
    updateCam();
}});
renderer.domElement.addEventListener('touchend', () => {{ isDragging = false; }});
updateCam();

// ============ CLICK INTERACTION ============
const tooltip = document.getElementById('tooltip');
const detailOverlay = document.getElementById('detail-overlay');
let currentBottleData = null;
let shakeTimer = null;
let liquidOffset = 0;
let liquidAnimFrame = null;

// 2D bottle renderer
function drawBottle2D(bottleData, shakeOffset) {{
    const canvas = document.getElementById('detail-canvas');
    const ctx = canvas.getContext('2d');
    const W = canvas.width, H = canvas.height;
    ctx.clearRect(0, 0, W, H);

    const cx = W / 2 + (shakeOffset || 0);
    const bW = 70, bH = 160;
    const neckW = 28, neckH = 40;
    const corkW = 32, corkH = 18;
    const bottomY = H * 0.78;
    const topY = bottomY - bH;
    const color = bottleData.color || '#aa4444';

    ctx.save();

    // Shadow
    ctx.fillStyle = 'rgba(0,0,0,0.2)';
    ctx.beginPath();
    ctx.ellipse(cx + 4, bottomY + 6, bW / 2 + 5, 8, 0, 0, Math.PI * 2);
    ctx.fill();

    // Bottle body
    const bodyGrad = ctx.createLinearGradient(cx - bW / 2, 0, cx + bW / 2, 0);
    bodyGrad.addColorStop(0, shadeColor(color, -30));
    bodyGrad.addColorStop(0.3, shadeColor(color, 20));
    bodyGrad.addColorStop(0.7, color);
    bodyGrad.addColorStop(1, shadeColor(color, -40));

    ctx.fillStyle = bodyGrad;
    ctx.beginPath();
    ctx.moveTo(cx - bW / 2, bottomY);
    ctx.lineTo(cx - bW / 2 + 3, topY + 10);
    ctx.quadraticCurveTo(cx - bW / 2 + 3, topY, cx - neckW / 2, topY);
    ctx.lineTo(cx - neckW / 2, topY - neckH);
    ctx.lineTo(cx + neckW / 2, topY - neckH);
    ctx.lineTo(cx + neckW / 2, topY);
    ctx.quadraticCurveTo(cx + bW / 2 - 3, topY, cx + bW / 2 - 3, topY + 10);
    ctx.lineTo(cx + bW / 2, bottomY);
    ctx.closePath();
    ctx.fill();

    // Glass outline
    ctx.strokeStyle = shadeColor(color, 40);
    ctx.lineWidth = 1.5;
    ctx.stroke();

    // Liquid inside
    const fillLevel = 0.55 + Math.sin(liquidOffset) * 0.03;
    const liquidTop = bottomY - bH * fillLevel;
    const liquidGrad = ctx.createLinearGradient(0, liquidTop, 0, bottomY);
    liquidGrad.addColorStop(0, shadeColor(color, -10) + 'cc');
    liquidGrad.addColorStop(1, shadeColor(color, -40) + 'ee');

    ctx.save();
    ctx.beginPath();
    ctx.moveTo(cx - bW / 2 + 4, bottomY);
    ctx.lineTo(cx - bW / 2 + 5, topY + 12);
    ctx.quadraticCurveTo(cx - bW / 2 + 5, topY + 4, cx - neckW / 2 + 2, topY + 4);
    ctx.lineTo(cx + neckW / 2 - 2, topY + 4);
    ctx.quadraticCurveTo(cx + bW / 2 - 5, topY + 4, cx + bW / 2 - 5, topY + 12);
    ctx.lineTo(cx + bW / 2 - 4, bottomY);
    ctx.closePath();
    ctx.clip();

    ctx.fillStyle = liquidGrad;
    // Wavy liquid surface
    ctx.beginPath();
    ctx.moveTo(cx - bW / 2, bottomY);
    ctx.lineTo(cx - bW / 2, liquidTop);
    for (let x = cx - bW / 2; x <= cx + bW / 2; x += 4) {{
        const wave = Math.sin((x - cx) * 0.08 + liquidOffset * 3) * 3;
        ctx.lineTo(x, liquidTop + wave);
    }}
    ctx.lineTo(cx + bW / 2, bottomY);
    ctx.closePath();
    ctx.fill();

    // Bubbles
    const bubbleCount = Math.floor(3 + Math.sin(liquidOffset * 2) * 2);
    for (let i = 0; i < bubbleCount; i++) {{
        const bx = cx - bW / 3 + Math.sin(liquidOffset + i * 2.5) * (bW / 3);
        const by = bottomY - 20 - (((liquidOffset * 30 + i * 40) % (bH * fillLevel - 20)));
        const br = 2 + Math.sin(i + liquidOffset) * 1.5;
        if (by > liquidTop + 5) {{
            ctx.fillStyle = 'rgba(255,255,255,0.15)';
            ctx.beginPath();
            ctx.arc(bx, by, br, 0, Math.PI * 2);
            ctx.fill();
        }}
    }}
    ctx.restore();

    // Glass highlight
    ctx.fillStyle = 'rgba(255,255,255,0.08)';
    ctx.beginPath();
    ctx.ellipse(cx - bW / 4, topY + bH / 3, 8, bH / 3, -0.15, 0, Math.PI * 2);
    ctx.fill();

    // Cork
    const corkGrad = ctx.createLinearGradient(cx - corkW / 2, 0, cx + corkW / 2, 0);
    corkGrad.addColorStop(0, '#6b5440');
    corkGrad.addColorStop(0.4, '#9b8370');
    corkGrad.addColorStop(0.8, '#8b7355');
    corkGrad.addColorStop(1, '#5b4430');
    ctx.fillStyle = corkGrad;
    ctx.fillRect(cx - corkW / 2, topY - neckH - corkH, corkW, corkH);
    ctx.strokeStyle = '#5b4430';
    ctx.lineWidth = 1;
    ctx.strokeRect(cx - corkW / 2, topY - neckH - corkH, corkW, corkH);

    // Cork texture lines
    ctx.strokeStyle = 'rgba(90,60,40,0.3)';
    ctx.lineWidth = 0.5;
    for (let i = 0; i < 4; i++) {{
        const ly = topY - neckH - corkH + 4 + i * 4;
        ctx.beginPath();
        ctx.moveTo(cx - corkW / 2 + 3, ly);
        ctx.lineTo(cx + corkW / 2 - 3, ly);
        ctx.stroke();
    }}

    // Wax seal on top
    ctx.fillStyle = '{c["text"]}';
    ctx.beginPath();
    ctx.arc(cx, topY - neckH - corkH - 2, corkW / 2 + 3, Math.PI, 0);
    ctx.fill();

    // Label
    const labelW = 64, labelH = 48;
    const labelY = topY + bH * 0.3;
    const labelGrad = ctx.createLinearGradient(0, labelY, 0, labelY + labelH);
    labelGrad.addColorStop(0, '{c["text"]}11');
    labelGrad.addColorStop(0.5, '#ffffee');
    labelGrad.addColorStop(1, '#eee8d0');
    ctx.fillStyle = labelGrad;
    ctx.fillRect(cx - labelW / 2, labelY, labelW, labelH);
    ctx.strokeStyle = '#8b7355';
    ctx.lineWidth = 0.8;
    ctx.strokeRect(cx - labelW / 2, labelY, labelW, labelH);

    // Label text
    ctx.fillStyle = '#333';
    ctx.font = 'bold 11px Georgia';
    ctx.textAlign = 'center';
    const name = bottleData.title || 'Unknown';
    if (name.length > 12) {{
        ctx.font = 'bold 9px Georgia';
    }}
    ctx.fillText(name, cx, labelY + labelH / 2 + 4);

    // Decorative line on label
    ctx.strokeStyle = '#8b735555';
    ctx.lineWidth = 0.5;
    ctx.beginPath();
    ctx.moveTo(cx - labelW / 3, labelY + 8);
    ctx.lineTo(cx + labelW / 3, labelY + 8);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(cx - labelW / 3, labelY + labelH - 8);
    ctx.lineTo(cx + labelW / 3, labelY + labelH - 8);
    ctx.stroke();

    ctx.restore();
}}

function shadeColor(hex, amt) {{
    // Convert color name or hex to darker/lighter
    let r, g, b;
    if (hex.startsWith('#')) {{
        const num = parseInt(hex.slice(1), 16);
        r = (num >> 16) & 0xff;
        g = (num >> 8) & 0xff;
        b = num & 0xff;
    }} else {{
        r = 170; g = 68; b = 68; // fallback
    }}
    r = Math.max(0, Math.min(255, r + amt));
    g = Math.max(0, Math.min(255, g + amt));
    b = Math.max(0, Math.min(255, b + amt));
    return '#' + ((1 << 24) + (r << 16) + (g << 8) + b).toString(16).slice(1);
}}

function showDetail(data) {{
    currentBottleData = data;
    document.getElementById('dp-title').textContent = data.title || 'Unknown Substance';
    document.getElementById('dp-desc').innerHTML = '<strong>Contents:</strong> ' + (data.desc || 'No description available.');

    const warningEl = document.getElementById('dp-warning');
    if (data.warning) {{
        warningEl.textContent = '⚠ ' + data.warning;
        warningEl.style.display = 'block';
    }} else {{
        warningEl.style.display = 'none';
    }}

    const loreEl = document.getElementById('dp-lore');
    if (data.lore && INTENSITY >= 2) {{
        loreEl.innerHTML = '🕵 <em>' + data.lore + '</em>';
        loreEl.style.display = 'block';
    }} else {{
        loreEl.style.display = 'none';
    }}

    detailOverlay.classList.add('active');
    liquidOffset = 0;
    drawBottle2D(data);
    startLiquidAnim();
}}

function closeDetail() {{
    detailOverlay.classList.remove('active');
    currentBottleData = null;
    if (liquidAnimFrame) cancelAnimationFrame(liquidAnimFrame);
}}

function startLiquidAnim() {{
    function tick() {{
        liquidOffset += 0.02;
        if (currentBottleData) {{
            drawBottle2D(currentBottleData);
            liquidAnimFrame = requestAnimationFrame(tick);
        }}
    }}
    tick();
}}

window.shakeBottle = function() {{
    const canvas = document.getElementById('detail-canvas');
    const btn = document.querySelector('.dp-btn-shake');
    canvas.classList.remove('shaking');
    btn.classList.remove('shaking');
    void canvas.offsetWidth; // force reflow
    canvas.classList.add('shaking');
    btn.classList.add('shaking');

    // Agitate liquid faster during shake
    let shakeFrames = 0;
    const origOffset = liquidOffset;
    function shakeAnim() {{
        shakeFrames++;
        liquidOffset += 0.15;
        if (currentBottleData) drawBottle2D(currentBottleData);
        if (shakeFrames < 25) requestAnimationFrame(shakeAnim);
    }}
    shakeAnim();

    setTimeout(() => {{
        canvas.classList.remove('shaking');
        btn.classList.remove('shaking');
    }}, 750);
}};

// Click: bottles open detail panel, other objects show tooltip
renderer.domElement.addEventListener('click', e => {{
    const cm = new THREE.Vector2((e.clientX / window.innerWidth) * 2 - 1, -(e.clientY / window.innerHeight) * 2 + 1);
    raycaster.setFromCamera(cm, camera);
    const intersects = raycaster.intersectObjects(scene.children, true);
    for (const hit of intersects) {{
        let obj = hit.object;
        while (obj && !obj.userData.type) obj = obj.parent;
        if (obj && obj.userData.type) {{
            if (obj.userData.type === 'bottle') {{
                // Open detail panel for bottles
                tooltip.classList.remove('visible');
                showDetail(obj.userData);
            }} else {{
                // Tooltip for everything else
                tooltip.querySelector('.title').textContent = obj.userData.title || '';
                tooltip.querySelector('.desc').textContent = obj.userData.desc || '';
                tooltip.querySelector('.lore').textContent = obj.userData.lore || '';
                tooltip.querySelector('.lore').style.display = obj.userData.lore ? 'block' : 'none';
                tooltip.style.left = Math.min(e.clientX + 15, window.innerWidth - 280) + 'px';
                tooltip.style.top = Math.min(e.clientY + 15, window.innerHeight - 130) + 'px';
                tooltip.classList.add('visible');
            }}
            return;
        }}
    }}
    tooltip.classList.remove('visible');
}});

// ============ UV TOGGLE ============
window.toggleUV = function() {{
    uvMode = !uvMode;
    document.getElementById('uv-btn').classList.toggle('active', uvMode);
    document.getElementById('uv-overlay').style.background = uvMode ? 'rgba(30,0,80,0.25)' : 'rgba(30,0,80,0)';
    uvLight.intensity = uvMode ? 2.5 : 0;
    uvElements.visible = uvMode;
    candleLight.intensity = uvMode ? 0.2 : 1.2;
}};

// ============ ANIMATION ============
const clock = new THREE.Clock();

function animate() {{
    requestAnimationFrame(animate);
    const t = clock.getElapsedTime();

    // Candle flicker
    candleLight.intensity = (uvMode ? 0.2 : 1.2) + Math.sin(t * 18) * 0.15 + Math.sin(t * 37) * 0.08;
    flame.scale.y = 1.4 + Math.sin(t * 12) * 0.2;
    flame.position.x = Math.sin(t * 7) * 0.003;
    flameInner.scale.y = 1 + Math.sin(t * 15) * 0.15;

    // Dust particles
    const dPos = dustParticles.geometry.attributes.position.array;
    for (let i = 0; i < dustCount; i++) {{
        dPos[i * 3] += dustVel[i].x + Math.sin(t + i) * 0.0002;
        dPos[i * 3 + 1] += dustVel[i].y;
        if (dPos[i * 3 + 1] > 3.5) dPos[i * 3 + 1] = 0;
    }}
    dustParticles.geometry.attributes.position.needsUpdate = true;

    // Herbs sway
    herbBundles.forEach((h, i) => {{
        h.rotation.z = Math.PI + Math.sin(t * 0.8 + i) * 0.05;
    }});

    // Mouse animation
    if (mouseGroup) {{
        const mCycle = Math.sin(t * 2);
        if (mCycle > 0.8) {{
            // Peek out
            mouseGroup.position.z = 0.3 + Math.sin(t * 4) * 0.02;
        }} else {{
            // Hide
            mouseGroup.position.z = 0.25;
        }}
        mouseGroup.rotation.y = -0.8 + Math.sin(t * 0.5) * 0.3;
    }}

    // Scales slight sway
    if (scales) {{
        scales.children.forEach(child => {{
            if (child.position.y > 0.25 && child.position.y < 0.35) {{
                // This affects the beam
            }}
        }});
    }}

    // Bottle liquid shimmer
    bottles.forEach((b, i) => {{
        if (b.children[3]) {{
            b.children[3].material.opacity = 0.3 + Math.sin(t * 1.5 + i) * 0.08;
        }}
    }});

    // UV glow pulse
    if (uvMode) {{
        uvElements.children.forEach((el, i) => {{
            el.material.opacity = 0.5 + Math.sin(t * 3 + i) * 0.3;
        }});
    }}

    // Skull eye glow (gothic high intensity)
    if (MODE === 'gothic' && INTENSITY >= 4) {{
        skull.children.forEach(child => {{
            if (child.material && child.material.color && child.material.color.r > 0.5) {{
                child.material.opacity = 0.4 + Math.sin(t * 2) * 0.3;
            }}
        }});
    }}

    // Auto orbit
    if (!isDragging) {{
        camAngle += 0.001;
        updateCam();
    }}

    renderer.render(scene, camera);
}}

window.addEventListener('resize', () => {{
    const w = container.clientWidth || window.innerWidth;
    const h = container.clientHeight || window.innerHeight;
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
    renderer.setSize(w, h);
}});

animate();
}})();
</script>
</body>
</html>'''
    return html
