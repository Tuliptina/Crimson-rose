"""
🧪 The Specimen Cabinet — ULTIMATE Edition
Victorian medical cabinet with ALL features:
- Drawer system with hidden items
- Zoom mode for bottle inspection
- Sound descriptions
- Advanced bottle animations
- Hidden compartment behind back panel
- Blacklight mode (UV reveals secrets)
- Combination lock puzzle
- Bottle mixing system
- Full nightmare mode at Intensity 5
"""

def get_cabinet_3d(mode: str = "gaslight", intensity: int = 3) -> str:
    """Generate the ultimate interactive medical cabinet."""
    
    if mode == "gothic":
        bg = "0x0a0505"; wood = "0x3a1818"; wood_dark = "0x1a0808"
        metal = "0x5a5a5a"; light = "0xff4422"; text = "#cc0000"
        ambient = 0.35; uv_color = "#ff00ff"
    elif mode == "clinical":
        bg = "0xe8e8e8"; wood = "0xd8d0c8"; wood_dark = "0xc0b8b0"
        metal = "0xbbbbbb"; light = "0xffffff"; text = "#2f4f4f"
        ambient = 0.7; uv_color = "#9900ff"
    else:
        bg = "0x1a1410"; wood = "0x5a4530"; wood_dark = "0x3c2818"
        metal = "0xc8a030"; light = "0xffbb55"; text = "#d4a574"
        ambient = 0.5; uv_color = "#cc00ff"
    
    creep = intensity / 5.0
    nightmare = "true" if intensity >= 5 else "false"
    
    html = f'''<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ width:100%; height:100vh; overflow:hidden; background:#111; font-family:Georgia,serif; color:{text}; }}
#container {{ width:100%; height:100%; cursor:grab; }}
#container:active {{ cursor:grabbing; }}

.ui {{ position:absolute; pointer-events:none; z-index:100; }}
#title {{ top:15px; left:50%; transform:translateX(-50%); font-size:16px; letter-spacing:3px; opacity:0.8; }}
#info {{ bottom:15px; left:50%; transform:translateX(-50%); font-size:11px; opacity:0.5; }}
#hint {{ bottom:50px; left:50%; transform:translateX(-50%); font-size:14px; background:rgba(0,0,0,0.85); padding:8px 16px; border-radius:4px; opacity:0; transition:opacity 0.3s; }}
#secrets {{ top:15px; right:15px; font-size:12px; opacity:0.7; }}
#sounds {{ bottom:90px; left:50%; transform:translateX(-50%); font-style:italic; font-size:13px; opacity:0; transition:opacity 1s; }}
#nightmare-text {{ position:absolute; top:50%; left:50%; transform:translate(-50%,-50%); font-size:20px; color:#880000; opacity:0; transition:opacity 2s; pointer-events:none; z-index:300; text-shadow:0 0 20px #ff0000; }}

/* Controls */
#controls {{ position:absolute; top:60px; right:15px; display:flex; flex-direction:column; gap:8px; z-index:150; }}
#controls button {{ padding:8px 14px; background:rgba(0,0,0,0.7); border:1px solid {text}44; color:{text}; font-family:Georgia; font-size:11px; cursor:pointer; pointer-events:auto; transition:all 0.3s; }}
#controls button:hover {{ background:{text}22; }}
#controls button.active {{ background:{text}33; border-color:{text}; }}

/* Vignette */
.vignette {{ position:absolute; top:0; left:0; width:100%; height:100%; background:radial-gradient(ellipse at center, transparent 40%, rgba(0,0,0,0.6) 100%); pointer-events:none; z-index:50; }}

/* UV Overlay */
#uv-overlay {{ position:absolute; top:0; left:0; width:100%; height:100%; background:rgba(80,0,120,0.15); pointer-events:none; z-index:45; opacity:0; transition:opacity 0.5s; }}
#uv-overlay.active {{ opacity:1; }}

/* Zoom Panel */
#zoom-panel {{ position:absolute; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.97); display:none; z-index:200; }}
#zoom-panel.show {{ display:flex; }}
#zoom-left {{ flex:1.2; display:flex; align-items:center; justify-content:center; position:relative; }}
#zoom-canvas {{ border:1px solid {text}22; }}
#zoom-right {{ flex:1; max-width:380px; padding:40px; display:flex; flex-direction:column; justify-content:center; }}
#zoom-name {{ font-size:26px; margin-bottom:8px; }}
#zoom-sub {{ font-size:13px; opacity:0.5; font-style:italic; margin-bottom:20px; border-bottom:1px solid {text}22; padding-bottom:15px; }}
#zoom-desc {{ font-size:15px; line-height:1.7; margin-bottom:15px; }}
#zoom-contents {{ font-size:13px; opacity:0.8; padding:12px; background:rgba(255,255,255,0.03); border-left:3px solid {text}33; margin-bottom:15px; }}
#zoom-warn {{ display:inline-block; padding:5px 12px; background:#331100; font-size:10px; letter-spacing:2px; }}
#zoom-secret {{ color:#bb3333; font-style:italic; margin-top:18px; opacity:0; transition:opacity 1.5s; }}
#zoom-secret.show {{ opacity:1; }}
#zoom-uv {{ color:{uv_color}; font-style:italic; margin-top:12px; opacity:0; transition:opacity 0.5s; display:none; }}
#zoom-uv.show {{ opacity:1; display:block; }}
#zoom-close {{ position:absolute; top:25px; right:30px; font-size:32px; cursor:pointer; opacity:0.5; z-index:210; }}
#zoom-close:hover {{ opacity:1; }}
#zoom-btns {{ display:flex; gap:10px; margin-top:20px; flex-wrap:wrap; }}
#zoom-btns button {{ padding:8px 16px; background:transparent; border:1px solid {text}44; color:{text}; font-family:Georgia; font-size:12px; cursor:pointer; }}
#zoom-btns button:hover {{ background:{text}22; }}

/* Drawer Panel */
#drawer-panel {{ position:absolute; bottom:0; left:50%; transform:translateX(-50%); width:80%; max-width:700px; background:rgba(20,15,10,0.97); border:1px solid {text}33; border-bottom:none; padding:20px; display:none; z-index:180; border-radius:8px 8px 0 0; }}
#drawer-panel.show {{ display:block; }}
#drawer-title {{ font-size:14px; letter-spacing:2px; margin-bottom:15px; opacity:0.8; }}
#drawer-items {{ display:flex; gap:15px; flex-wrap:wrap; }}
.drawer-item {{ padding:12px 18px; background:rgba(0,0,0,0.4); border:1px solid {text}22; cursor:pointer; font-size:13px; transition:all 0.3s; }}
.drawer-item:hover {{ background:{text}22; border-color:{text}55; }}
.drawer-item.locked {{ opacity:0.4; cursor:not-allowed; }}
#drawer-close {{ position:absolute; top:10px; right:15px; font-size:20px; cursor:pointer; opacity:0.5; }}

/* Combination Lock */
#lock-panel {{ position:absolute; top:50%; left:50%; transform:translate(-50%,-50%); background:rgba(15,10,8,0.98); border:2px solid {text}44; padding:30px; display:none; z-index:250; text-align:center; border-radius:8px; }}
#lock-panel.show {{ display:block; }}
#lock-title {{ font-size:14px; letter-spacing:2px; margin-bottom:20px; }}
#lock-dials {{ display:flex; gap:10px; justify-content:center; margin-bottom:20px; }}
.dial {{ width:50px; height:60px; background:#222; border:2px solid {text}55; display:flex; align-items:center; justify-content:center; font-size:28px; font-family:monospace; cursor:pointer; user-select:none; }}
.dial:hover {{ border-color:{text}; }}
#lock-submit {{ padding:10px 25px; background:transparent; border:1px solid {text}55; color:{text}; font-family:Georgia; cursor:pointer; }}
#lock-hint {{ font-size:11px; opacity:0.5; margin-top:15px; font-style:italic; }}
#lock-close {{ position:absolute; top:10px; right:15px; font-size:20px; cursor:pointer; opacity:0.5; }}

/* Mixing Panel */
#mix-panel {{ position:absolute; top:50%; left:50%; transform:translate(-50%,-50%); background:rgba(15,10,8,0.98); border:2px solid {text}44; padding:30px; display:none; z-index:250; border-radius:8px; min-width:350px; }}
#mix-panel.show {{ display:block; }}
#mix-title {{ font-size:14px; letter-spacing:2px; margin-bottom:20px; text-align:center; }}
#mix-slots {{ display:flex; gap:15px; justify-content:center; margin-bottom:20px; }}
.mix-slot {{ width:70px; height:90px; background:#1a1510; border:2px dashed {text}33; display:flex; align-items:center; justify-content:center; font-size:11px; opacity:0.6; cursor:pointer; }}
.mix-slot.filled {{ border-style:solid; opacity:1; border-color:{text}66; }}
#mix-result {{ text-align:center; min-height:60px; padding:15px; background:rgba(0,0,0,0.3); margin-bottom:15px; font-style:italic; }}
#mix-buttons {{ display:flex; gap:10px; justify-content:center; }}
#mix-buttons button {{ padding:8px 18px; background:transparent; border:1px solid {text}44; color:{text}; font-family:Georgia; cursor:pointer; }}
#mix-close {{ position:absolute; top:10px; right:15px; font-size:20px; cursor:pointer; opacity:0.5; }}

/* Hidden Panel Flash */
#hidden-flash {{ position:absolute; top:50%; left:50%; transform:translate(-50%,-50%); font-size:16px; letter-spacing:3px; color:#aa0000; opacity:0; transition:opacity 0.5s; z-index:160; text-shadow:0 0 15px #ff0000; }}
</style>
</head>
<body>
<div id="container"></div>
<div class="vignette"></div>
<div id="uv-overlay"></div>

<div id="title" class="ui">THE FITZROY COLLECTION</div>
<div id="info" class="ui">Drag to rotate • Scroll to zoom • Click bottles to examine</div>
<div id="hint" class="ui"></div>
<div id="secrets" class="ui">Secrets: <span id="snum">0</span>/12</div>
<div id="sounds" class="ui"></div>
<div id="nightmare-text"></div>
<div id="hidden-flash">SECRET COMPARTMENT FOUND</div>

<div id="controls">
    <button id="btn-uv">🔦 UV Light</button>
    <button id="btn-drawer">🗄️ Drawers</button>
    <button id="btn-mix">⚗️ Mix</button>
</div>

<!-- Zoom Panel -->
<div id="zoom-panel">
    <div id="zoom-close">×</div>
    <div id="zoom-left"><canvas id="zoom-canvas" width="380" height="480"></canvas></div>
    <div id="zoom-right">
        <div id="zoom-name"></div>
        <div id="zoom-sub"></div>
        <div id="zoom-desc"></div>
        <div id="zoom-contents"></div>
        <div id="zoom-warn"></div>
        <div id="zoom-secret"></div>
        <div id="zoom-uv"></div>
        <div id="zoom-btns">
            <button id="z-shake">Shake</button>
            <button id="z-smell">Smell</button>
            <button id="z-pour">Pour Drop</button>
            <button id="z-addmix">Add to Mix</button>
        </div>
    </div>
</div>

<!-- Drawer Panel -->
<div id="drawer-panel">
    <div id="drawer-close">×</div>
    <div id="drawer-title">LOWER DRAWERS</div>
    <div id="drawer-items"></div>
</div>

<!-- Lock Panel -->
<div id="lock-panel">
    <div id="lock-close">×</div>
    <div id="lock-title">🔒 SOCIETY DRAWER</div>
    <div id="lock-dials">
        <div class="dial" data-i="0">0</div>
        <div class="dial" data-i="1">0</div>
        <div class="dial" data-i="2">0</div>
    </div>
    <button id="lock-submit">UNLOCK</button>
    <div id="lock-hint">"The year the Society was founded..."</div>
</div>

<!-- Mix Panel -->
<div id="mix-panel">
    <div id="mix-close">×</div>
    <div id="mix-title">⚗️ MIXING CHAMBER</div>
    <div id="mix-slots">
        <div class="mix-slot" data-slot="0">Empty</div>
        <div class="mix-slot" data-slot="1">Empty</div>
    </div>
    <div id="mix-result">Add two bottles to combine...</div>
    <div id="mix-buttons">
        <button id="mix-combine">Combine</button>
        <button id="mix-clear">Clear</button>
    </div>
</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script>
(function() {{
const INTENSITY = {intensity};
const NIGHTMARE = {nightmare};
const CREEP = {creep};

let secrets = 0, uvMode = false, hiddenFound = false;
const found = new Set();
const mixSlots = [null, null];

// Sound descriptions
const SOUNDS = [
    '*Wood creaks as you lean closer...*',
    '*Glass clinks softly...*',
    '*Liquid sloshes against its container...*',
    '*A cork shifts slightly...*',
    '*Something settles on a shelf...*',
    '*You hear your own breathing...*',
    '*Dust motes drift in the light...*'
];
const NIGHTMARE_SOUNDS = [
    '*Something taps from inside a jar...*',
    '*A wet sound. Behind you.*',
    '*Whispers. Too faint to understand.*',
    '*The leeches are excited.*',
    '*A face. In the reflection. Gone now.*',
    '*"Open me..." Was that a voice?*'
];

// Drawer items
const DRAWER_ITEMS = [
    {{ id:'scalpel', name:'Surgical Scalpel', desc:'Initials A.F. on handle. Dried blood.', locked:false }},
    {{ id:'letters', name:'Correspondence', desc:'Letters from T.B. Blackmail?', locked:false }},
    {{ id:'journal', name:'Private Journal', desc:'Fitzroy\\'s notes. Encoded.', locked:false }},
    {{ id:'society', name:'🔒 Society Drawer', desc:'Locked. Requires combination.', locked:true }},
    {{ id:'blackbook', name:'The Black Book', desc:'Ledger of procured subjects.', locked:true }},
    {{ id:'mask', name:'Ceremonial Mask', desc:'Worn for "special procedures."', locked:true }}
];

// Bottle data with UV secrets and mix properties
const BOTTLES = [
    {{ id:'laudanum', name:'Laudanum', sub:'Tincture of Opium', color:0xcc8844, liquid:0x553311, level:0.6, row:0, slot:0, desc:'Opium in alcohol. For everything.', contents:'Half empty.', warn:'ADDICTIVE', secret:'Note: "Mrs. Harrison — 40 drops."', uv:'Hidden text: "SILENCE HER"', hasSecret:true, mixType:'sedative', anim:'bubble' }},
    {{ id:'chloroform', name:'Chloroform', sub:'Anesthetic', color:0x4466bb, liquid:0xccddff, level:0.25, row:0, slot:1, desc:'Volatile anesthetic.', contents:'Recently used.', warn:'POISON', secret:'Used without surgeries scheduled.', uv:'Bloodstain under label', hasSecret:INTENSITY>=3, mixType:'knockout', anim:'swirl' }},
    {{ id:'soothing', name:"Winslow's Syrup", sub:'For Infants', color:0xeeddbb, liquid:0x997755, level:0.75, row:0, slot:2, desc:'Soothing syrup for babies.', contents:'Morphine and alcohol.', warn:'EXTERNAL USE', secret:'Dosage 10x normal.', uv:'Infant names listed', hasSecret:INTENSITY>=2, mixType:'sedative', anim:'none' }},
    {{ id:'mercury', name:'Mercury', sub:'Blue Mass', color:0x334455, liquid:0x99aaaa, level:0.5, row:0, slot:3, desc:'Treatment. Causes madness.', contents:'Silver shimmer.', warn:'TOXIC', secret:'Names behind label.', uv:'Society symbol', hasSecret:INTENSITY>=4, mixType:'poison', anim:'shimmer' }},
    {{ id:'arsenic', name:'Arsenic', sub:'Complexion', color:0x88aa77, liquid:0xcceecc, level:0.65, row:0, slot:4, desc:'For pale beauty.', contents:'Sweet poison.', warn:'AS DIRECTED', secret:'Why does he keep these?', uv:'"For V.H. — final dose"', hasSecret:INTENSITY>=3, mixType:'poison', anim:'none' }},
    
    {{ id:'ether', name:'Ether', sub:'Anesthetic', color:0x775533, liquid:0xffeedd, level:0.35, row:1, slot:0, desc:'Patients sleep. Usually.', contents:'Flammable.', warn:'NO FLAME', secret:'Scratches inside lid.', uv:'Claw marks visible', hasSecret:INTENSITY>=5, mixType:'knockout', anim:'bubble' }},
    {{ id:'cocaine', name:'Cocaine 4%', sub:'Local', color:0xeeeeff, liquid:0xffffff, level:0.12, row:1, slot:1, desc:'Anesthetic. Confidence.', contents:'Nearly empty.', warn:'MEDICINAL', secret:"Fitzroy's daily supply.", uv:'Usage log: every 3 hours', hasSecret:true, mixType:'stimulant', anim:'sparkle' }},
    {{ id:'strychnine', name:'Strychnine', sub:'Nerve Tonic', color:0xdd3333, liquid:0xffcccc, level:0.5, row:1, slot:2, desc:'Stimulant or death.', contents:'Red warning.', warn:'POISON', secret:'Lethal dosage noted.', uv:'"For the weak ones"', hasSecret:INTENSITY>=4, mixType:'poison', anim:'pulse' }},
    {{ id:'carbolic', name:'Carbolic Acid', sub:'Antiseptic', color:0x4455aa, liquid:0xeeeedd, level:0.7, row:1, slot:3, desc:'Kills infection. And evidence.', contents:'Burns organic matter.', warn:'CORROSIVE', secret:'Blood and hair on cap.', uv:'Fingerprints revealed', hasSecret:INTENSITY>=4, mixType:'acid', anim:'none' }},
    {{ id:'embalming', name:'Embalming', sub:'Preservation', color:0x888866, liquid:0xccccaa, level:0.85, row:1, slot:4, desc:'For specimens.', contents:'Large supply.', warn:'TOXIC FUMES', secret:'Why so much?', uv:'Off-site address', hasSecret:INTENSITY>=3, mixType:'preserve', anim:'none' }},
    
    {{ id:'vita', name:'Vita Aeterna', sub:'Eternal Essence', color:0x880022, liquid:0xaa0000, level:0.55, row:2, slot:0, desc:'Society communion. Swirls alone.', contents:'Too red for wine.', warn:'MEMBERS ONLY', secret:'"Sanguis innocentum"', uv:'BLOOD OF 7 INFANTS', hasSecret:true, mixType:'blood', anim:'swirl', special:'swirl' }},
    {{ id:'unmarked', name:'Bottle #7', sub:'Unmarked', color:0x666666, liquid:0xeeeeee, level:0.5, row:2, slot:1, desc:'No label. Almonds.', contents:'Cyanide.', warn:'DO NOT OPEN', secret:'Enough to kill 100.', uv:'Batch number: 1847', hasSecret:INTENSITY>=3, mixType:'poison', anim:'none' }},
    {{ id:'unwilling', name:'"Unwilling"', sub:'Special', color:0x222222, liquid:0x332244, level:0.7, row:2, slot:2, desc:'For resistant subjects.', contents:'Instant knockout.', warn:'SOCIETY', secret:'12 "donations" — none willing.', uv:'Map to procurement sites', hasSecret:true, mixType:'knockout', anim:'pulse' }},
    {{ id:'mercy', name:'"Final Mercy"', sub:'Terminal', color:0xaa0000, liquid:0x220000, level:0.9, row:2, slot:3, desc:'Ends suffering.', contents:'Death in seconds.', warn:'EMERGENCY', secret:'3 doses missing.', uv:'"THANK YOU" scratched inside', hasSecret:INTENSITY>=4, mixType:'lethal', anim:'pulse' }},
    {{ id:'blood_sc', name:'Blood—S.C.', sub:'Specimen', color:0xdddddd, liquid:0x660000, level:0.6, row:2, slot:4, desc:'Initials S.C.', contents:'Still viable.', warn:'DO NOT DISCARD', secret:'Sebastian Carlisle. Why?', uv:'TEST RESULTS: Compatible', hasSecret:true, mixType:'blood', anim:'none' }},
    
    {{ id:'teeth', name:'Teeth', sub:'Collection', color:0xffffdd, liquid:0xffffcc, level:0.8, row:3, slot:0, desc:'47 teeth in alcohol.', contents:'12+ sources.', warn:'SPECIMEN', secret:'Some from the living.', uv:'Names on each tooth', hasSecret:INTENSITY>=3, mixType:'none', anim:'float' }},
    {{ id:'leeches', name:'Leeches', sub:'Live', color:0xccffcc, liquid:0xaaddaa, level:0.7, row:3, slot:1, desc:'They sense you.', contents:'Hungry.', warn:'LIVE', secret:'Why so large?', uv:'Feeding log: weekly', hasSecret:INTENSITY>=2, mixType:'none', anim:'leeches', special:'leeches' }},
    {{ id:'essence', name:'"Youth"', sub:'Rejuvenation', color:0xddccbb, liquid:0xffffdd, level:0.6, row:3, slot:2, desc:'Smells of fat.', contents:'Softens wrinkles.', warn:'EXTERNAL', secret:'Human fat. From poor.', uv:'Supplier: Resurrection Men', hasSecret:INTENSITY>=4, mixType:'none', anim:'none' }},
    {{ id:'tapeworm', name:'Tapeworm', sub:'Diet', color:0xeeeedd, liquid:0xffffee, level:0.7, row:3, slot:3, desc:'Diet aid.', contents:'Weight loss.', warn:'DO NOT EAT', secret:'Being farmed.', uv:'Breeding instructions', hasSecret:INTENSITY>=3, mixType:'none', anim:'float' }},
    {{ id:'brain', name:'Nerve Food', sub:'For Mind', color:0xbbaa88, liquid:0xccbbaa, level:0.5, row:3, slot:4, desc:'Gray matter.', contents:'Transfers mental energy.', warn:'TWICE DAILY', secret:'Human brain. Cannibalism.', uv:'"GENIUS DONOR"', hasSecret:true, mixType:'none', anim:'pulse' }}
];

// Mix combinations
const MIX_RESULTS = {{
    'sedative+sedative': {{ result:'Lethal Overdose', effect:'A dose no one wakes from.', color:'#880000' }},
    'sedative+knockout': {{ result:'Deep Sleep', effect:'Hours of unconsciousness.', color:'#666688' }},
    'sedative+stimulant': {{ result:'Confusion Tonic', effect:'Disorientation and compliance.', color:'#888866' }},
    'knockout+knockout': {{ result:'Instant Blackout', effect:'Seconds to unconsciousness.', color:'#444466' }},
    'poison+poison': {{ result:'Certain Death', effect:'No antidote exists.', color:'#880000' }},
    'poison+blood': {{ result:'Tainted Blood', effect:'For the communion...', color:'#aa0022' }},
    'blood+blood': {{ result:'Vita Renewed', effect:'The Society\\'s sacrament.', color:'#cc0000' }},
    'stimulant+stimulant': {{ result:'Heart Attack', effect:'Too much. The heart cannot take it.', color:'#ff4444' }},
    'stimulant+poison': {{ result:'Painful End', effect:'Alert and dying.', color:'#cc4400' }},
    'acid+blood': {{ result:'Evidence Destroyed', effect:'Nothing remains to identify.', color:'#555555' }},
    'preserve+blood': {{ result:'Eternal Specimen', effect:'Preserved forever. Still aware?', color:'#668866' }},
    'lethal+blood': {{ result:'Mercy Communion', effect:'The final sacrament.', color:'#440000' }}
}};

// Three.js setup
const container = document.getElementById('container');
const scene = new THREE.Scene();
scene.background = new THREE.Color({bg});

const camera = new THREE.PerspectiveCamera(50, window.innerWidth/window.innerHeight, 0.1, 100);
camera.position.set(0, 1.5, 6);
camera.lookAt(0, 1.2, 0);

const renderer = new THREE.WebGLRenderer({{ antialias:true }});
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
container.appendChild(renderer.domElement);

const raycaster = new THREE.Raycaster();
const mouse = new THREE.Vector2();

// Lights
scene.add(new THREE.AmbientLight(0xffffff, {ambient}));
scene.add(new THREE.HemisphereLight(0xffffff, {wood_dark}, 0.4));
const dir = new THREE.DirectionalLight({light}, 1.0);
dir.position.set(3, 5, 4);
scene.add(dir);
scene.add(new THREE.PointLight({light}, 0.6, 20).position.set(-3, 3, 3));

// UV Light (for blacklight mode)
const uvLight = new THREE.PointLight(0x8800ff, 0, 15);
uvLight.position.set(0, 2, 3);
scene.add(uvLight);

// Materials
const woodMat = new THREE.MeshLambertMaterial({{ color: {wood} }});
const darkMat = new THREE.MeshLambertMaterial({{ color: {wood_dark} }});
const metalMat = new THREE.MeshLambertMaterial({{ color: {metal} }});

// Cabinet
const W = 4, H = 3.2, D = 0.7, ROWS = 4, SH = H/ROWS;

// Back (clickable for hidden compartment)
const backGeo = new THREE.BoxGeometry(W, H, 0.05);
const back = new THREE.Mesh(backGeo, darkMat);
back.position.set(0, H/2, -D/2);
back.userData = {{ isBack: true }};
scene.add(back);

// Sides
[-1,1].forEach(s => {{
    const side = new THREE.Mesh(new THREE.BoxGeometry(0.08, H, D), woodMat);
    side.position.set(s*W/2, H/2, 0);
    scene.add(side);
}});

// Top
const top = new THREE.Mesh(new THREE.BoxGeometry(W+0.1, 0.1, D+0.1), woodMat);
top.position.set(0, H+0.05, 0);
scene.add(top);

// Shelves
for (let i=0; i<=ROWS; i++) {{
    const shelf = new THREE.Mesh(new THREE.BoxGeometry(W-0.1, 0.04, D-0.08), woodMat);
    shelf.position.set(0, i*SH, 0);
    scene.add(shelf);
}}

// Drawers at bottom
const drawerGeo = new THREE.BoxGeometry(W-0.15, 0.25, D-0.1);
const drawer = new THREE.Mesh(drawerGeo, darkMat);
drawer.position.set(0, -0.15, 0.05);
drawer.userData = {{ isDrawer: true }};
scene.add(drawer);

// Drawer handles
[-0.8, 0, 0.8].forEach(x => {{
    const handle = new THREE.Mesh(new THREE.BoxGeometry(0.15, 0.03, 0.05), metalMat);
    handle.position.set(x, -0.15, D/2);
    scene.add(handle);
}});

// Bottles
const bottles = [];
function slotPos(row, slot) {{
    const startX = -W/2 + 0.45;
    const spacing = (W - 0.9) / 4;
    return {{ x: startX + slot*spacing, y: row*SH + 0.18, z: 0 }};
}}

BOTTLES.forEach(b => {{
    const g = new THREE.Group();
    
    const glass = new THREE.Mesh(
        new THREE.CylinderGeometry(0.08, 0.09, 0.32, 12),
        new THREE.MeshLambertMaterial({{ color:b.color, transparent:true, opacity:0.6 }})
    );
    g.add(glass);
    
    const lh = 0.28 * b.level;
    const liq = new THREE.Mesh(
        new THREE.CylinderGeometry(0.065, 0.075, lh, 12),
        new THREE.MeshLambertMaterial({{ color:b.liquid, transparent:true, opacity:0.85 }})
    );
    liq.position.y = -0.14 + lh/2 + 0.02;
    liq.userData = {{ isLiquid: true }};
    g.add(liq);
    
    const cork = new THREE.Mesh(
        new THREE.CylinderGeometry(0.035, 0.04, 0.05, 8),
        new THREE.MeshLambertMaterial({{ color: 0x8b7355 }})
    );
    cork.position.y = 0.18;
    g.add(cork);
    
    const label = new THREE.Mesh(
        new THREE.PlaneGeometry(0.1, 0.08),
        new THREE.MeshLambertMaterial({{ color: 0xffffee, side: THREE.DoubleSide }})
    );
    label.position.set(0, 0, 0.09);
    g.add(label);
    
    const p = slotPos(b.row, b.slot);
    g.position.set(p.x, p.y, p.z);
    g.userData = b;
    
    scene.add(g);
    bottles.push(g);
}});

// Camera controls
let drag=false, px=0, py=0, theta=0, phi=1.2, dist=6;
const target = new THREE.Vector3(0, 1.3, 0);

function updateCam() {{
    camera.position.x = target.x + dist*Math.sin(phi)*Math.sin(theta);
    camera.position.y = target.y + dist*Math.cos(phi);
    camera.position.z = target.z + dist*Math.sin(phi)*Math.cos(theta);
    camera.lookAt(target);
}}

renderer.domElement.onmousedown = e => {{ drag=true; px=e.clientX; py=e.clientY; }};
window.onmouseup = () => drag=false;
renderer.domElement.onmousemove = e => {{
    mouse.x = (e.clientX/window.innerWidth)*2-1;
    mouse.y = -(e.clientY/window.innerHeight)*2+1;
    if(drag) {{
        theta += (e.clientX-px)*0.005;
        phi = Math.max(0.5, Math.min(1.5, phi+(e.clientY-py)*0.005));
        px=e.clientX; py=e.clientY;
        updateCam();
    }}
}};
renderer.domElement.onwheel = e => {{
    e.preventDefault();
    dist = Math.max(3.5, Math.min(10, dist+e.deltaY*0.005));
    updateCam();
}};
updateCam();

// Sounds
const soundEl = document.getElementById('sounds');
let soundIdx = 0;
function showSound() {{
    const pool = NIGHTMARE ? [...SOUNDS, ...NIGHTMARE_SOUNDS] : SOUNDS;
    soundEl.textContent = pool[soundIdx % pool.length];
    soundEl.style.opacity = 0.7;
    setTimeout(() => soundEl.style.opacity = 0, 3500);
    soundIdx++;
}}
setInterval(showSound, 8000 - INTENSITY*1000);
setTimeout(showSound, 3000);

// Nightmare text
const nightmareEl = document.getElementById('nightmare-text');
const NIGHTMARE_TEXTS = [
    'IT SEES YOU',
    'OPEN THE RED ONE',
    'WE ARE WAITING',
    'JOIN US',
    'YOUR BLOOD NEXT',
    'THEY NEVER LEFT'
];
if (NIGHTMARE) {{
    setInterval(() => {{
        nightmareEl.textContent = NIGHTMARE_TEXTS[Math.floor(Math.random()*NIGHTMARE_TEXTS.length)];
        nightmareEl.style.opacity = 0.8;
        setTimeout(() => nightmareEl.style.opacity = 0, 2000);
    }}, 15000);
}}

// UV Mode
document.getElementById('btn-uv').onclick = () => {{
    uvMode = !uvMode;
    document.getElementById('btn-uv').classList.toggle('active', uvMode);
    document.getElementById('uv-overlay').classList.toggle('active', uvMode);
    uvLight.intensity = uvMode ? 2 : 0;
    dir.intensity = uvMode ? 0.3 : 1.0;
}};

// Drawer panel
document.getElementById('btn-drawer').onclick = () => {{
    const panel = document.getElementById('drawer-panel');
    panel.classList.toggle('show');
    if (panel.classList.contains('show')) {{
        const items = document.getElementById('drawer-items');
        items.innerHTML = '';
        DRAWER_ITEMS.forEach(item => {{
            const div = document.createElement('div');
            div.className = 'drawer-item' + (item.locked ? ' locked' : '');
            div.textContent = item.name;
            div.onclick = () => {{
                if (item.locked && item.id === 'society') {{
                    document.getElementById('lock-panel').classList.add('show');
                }} else if (!item.locked) {{
                    alert(item.name + '\\n\\n' + item.desc);
                    if (!found.has('drawer_'+item.id)) {{
                        found.add('drawer_'+item.id);
                        secrets++;
                        document.getElementById('snum').textContent = secrets;
                    }}
                }}
            }};
            items.appendChild(div);
        }});
    }}
}};
document.getElementById('drawer-close').onclick = () => document.getElementById('drawer-panel').classList.remove('show');

// Lock panel
const dials = document.querySelectorAll('.dial');
dials.forEach(d => {{
    d.onclick = () => {{
        let v = parseInt(d.textContent);
        d.textContent = (v + 1) % 10;
    }};
}});
document.getElementById('lock-submit').onclick = () => {{
    const code = Array.from(dials).map(d => d.textContent).join('');
    if (code === '847') {{ // 1847 - Society founded
        document.getElementById('lock-panel').classList.remove('show');
        DRAWER_ITEMS.forEach(item => item.locked = false);
        document.getElementById('btn-drawer').click();
        document.getElementById('btn-drawer').click();
        if (!found.has('lock_solved')) {{
            found.add('lock_solved');
            secrets++;
            document.getElementById('snum').textContent = secrets;
        }}
    }} else {{
        document.getElementById('lock-hint').textContent = 'Incorrect. The Society was founded in 18__...';
    }}
}};
document.getElementById('lock-close').onclick = () => document.getElementById('lock-panel').classList.remove('show');

// Mix panel
document.getElementById('btn-mix').onclick = () => document.getElementById('mix-panel').classList.toggle('show');
document.getElementById('mix-close').onclick = () => document.getElementById('mix-panel').classList.remove('show');
document.getElementById('mix-clear').onclick = () => {{
    mixSlots[0] = mixSlots[1] = null;
    document.querySelectorAll('.mix-slot').forEach(s => {{
        s.textContent = 'Empty';
        s.classList.remove('filled');
    }});
    document.getElementById('mix-result').innerHTML = 'Add two bottles to combine...';
}};
document.getElementById('mix-combine').onclick = () => {{
    if (!mixSlots[0] || !mixSlots[1]) return;
    const t1 = mixSlots[0].mixType, t2 = mixSlots[1].mixType;
    const key1 = t1+'+'+t2, key2 = t2+'+'+t1;
    const result = MIX_RESULTS[key1] || MIX_RESULTS[key2];
    if (result) {{
        document.getElementById('mix-result').innerHTML = 
            '<span style="color:'+result.color+';font-weight:bold;">'+result.result+'</span><br><br>'+result.effect;
        if (!found.has('mix_'+key1)) {{
            found.add('mix_'+key1);
            secrets++;
            document.getElementById('snum').textContent = secrets;
        }}
    }} else {{
        document.getElementById('mix-result').innerHTML = 'No reaction. These substances do not combine meaningfully.';
    }}
}};

// Zoom panel
let sel = null, wave = 0, shaking = false;
const zoomPanel = document.getElementById('zoom-panel');
const zCanvas = document.getElementById('zoom-canvas');
const zCtx = zCanvas.getContext('2d');

function showZoom(b) {{
    sel = b;
    document.getElementById('zoom-name').textContent = b.name;
    document.getElementById('zoom-sub').textContent = b.sub;
    document.getElementById('zoom-desc').textContent = b.desc;
    document.getElementById('zoom-contents').textContent = b.contents;
    document.getElementById('zoom-warn').textContent = '⚠ ' + b.warn;
    
    const sec = document.getElementById('zoom-secret');
    sec.classList.remove('show');
    if (b.hasSecret) {{
        sec.textContent = '🔍 ' + b.secret;
        setTimeout(() => {{
            sec.classList.add('show');
            if (!found.has(b.id)) {{
                found.add(b.id);
                secrets++;
                document.getElementById('snum').textContent = secrets;
            }}
        }}, 1200);
    }} else sec.textContent = '';
    
    const uvEl = document.getElementById('zoom-uv');
    uvEl.textContent = '☢ UV REVEALS: ' + b.uv;
    uvEl.classList.toggle('show', uvMode);
    
    zoomPanel.classList.add('show');
}}

document.getElementById('zoom-close').onclick = () => {{ zoomPanel.classList.remove('show'); sel = null; }};
document.getElementById('z-shake').onclick = () => {{ shaking = true; setTimeout(() => shaking = false, 800); }};
document.getElementById('z-smell').onclick = () => {{
    const smells = {{ laudanum:'Bitter opium...', chloroform:'Sickly sweet.', vita:'Iron and copper.', leeches:'Stagnant water.', unmarked:'BITTER ALMONDS!', brain:'Formaldehyde.' }};
    const hint = document.getElementById('hint');
    hint.textContent = smells[sel?.id] || 'Chemical odor...';
    hint.style.opacity = 1;
    setTimeout(() => hint.style.opacity = 0, 2500);
}};
document.getElementById('z-pour').onclick = () => {{
    if (sel) {{
        sel.level = Math.max(0.05, sel.level - 0.1);
        document.getElementById('hint').textContent = '*A drop falls...*';
        document.getElementById('hint').style.opacity = 1;
        setTimeout(() => document.getElementById('hint').style.opacity = 0, 2000);
    }}
}};
document.getElementById('z-addmix').onclick = () => {{
    if (!sel || sel.mixType === 'none') return;
    const slot = mixSlots[0] === null ? 0 : (mixSlots[1] === null ? 1 : -1);
    if (slot >= 0) {{
        mixSlots[slot] = sel;
        const slotEl = document.querySelector('.mix-slot[data-slot="'+slot+'"]');
        slotEl.textContent = sel.name;
        slotEl.classList.add('filled');
        document.getElementById('hint').textContent = 'Added to mixing chamber.';
        document.getElementById('hint').style.opacity = 1;
        setTimeout(() => document.getElementById('hint').style.opacity = 0, 1500);
    }}
}};

// 2D bottle rendering
function draw2d(b) {{
    const w=zCanvas.width, h=zCanvas.height;
    zCtx.clearRect(0,0,w,h);
    zCtx.save();
    zCtx.translate(w/2, h/2);
    if(shaking) zCtx.rotate(Math.sin(wave*3)*0.1);
    
    const bW=100, bH=250;
    
    // Glass
    zCtx.fillStyle = '#'+b.color.toString(16).padStart(6,'0')+'99';
    zCtx.strokeStyle = '#'+b.color.toString(16).padStart(6,'0');
    zCtx.lineWidth = 3;
    zCtx.beginPath();
    zCtx.roundRect(-bW/2, -bH/2, bW, bH, 12);
    zCtx.fill(); zCtx.stroke();
    
    // Liquid
    const lh = bH * b.level * 0.85;
    const ly = bH/2 - lh - 15;
    zCtx.fillStyle = '#'+b.liquid.toString(16).padStart(6,'0')+'dd';
    zCtx.beginPath();
    zCtx.moveTo(-bW/2+12, ly+Math.sin(wave)*5);
    for(let x=-bW/2+12; x<=bW/2-12; x+=8) zCtx.lineTo(x, ly+Math.sin(wave+x*0.08)*5);
    zCtx.lineTo(bW/2-12, bH/2-15);
    zCtx.lineTo(-bW/2+12, bH/2-15);
    zCtx.closePath(); zCtx.fill();
    
    // Animations
    if(b.anim==='bubble' || b.anim==='swirl') {{
        for(let i=0; i<5; i++) {{
            const bx = Math.sin(wave*0.5+i*2)*(bW/3);
            const by = ly+20+((wave*20+i*30)%(lh-20));
            zCtx.beginPath();
            zCtx.arc(bx, by, 3+Math.sin(wave+i)*2, 0, Math.PI*2);
            zCtx.fillStyle = 'rgba(255,255,255,0.3)';
            zCtx.fill();
        }}
    }}
    if(b.anim==='pulse') {{
        zCtx.fillStyle = 'rgba(255,100,100,'+(0.1+Math.sin(wave)*0.1)+')';
        zCtx.fillRect(-bW/2+5, ly+5, bW-10, lh);
    }}
    if(b.anim==='shimmer') {{
        for(let i=0; i<8; i++) {{
            const sx = Math.sin(wave+i)*bW/3;
            const sy = ly+10+i*20;
            zCtx.beginPath();
            zCtx.arc(sx, sy, 2, 0, Math.PI*2);
            zCtx.fillStyle = 'rgba(200,200,220,0.5)';
            zCtx.fill();
        }}
    }}
    if(b.anim==='sparkle') {{
        for(let i=0; i<6; i++) {{
            if(Math.sin(wave*2+i)>0.7) {{
                const sx = (Math.random()-0.5)*bW*0.6;
                const sy = ly+20+Math.random()*lh*0.8;
                zCtx.beginPath();
                zCtx.arc(sx, sy, 2, 0, Math.PI*2);
                zCtx.fillStyle = 'rgba(255,255,255,0.8)';
                zCtx.fill();
            }}
        }}
    }}
    if(b.special==='leeches') {{
        zCtx.fillStyle = '#2a3a2a';
        for(let i=0; i<5; i++) {{
            const lx = Math.sin(wave*0.4+i*2)*30;
            const leechY = ly+30+i*25+Math.cos(wave*0.3+i)*10;
            zCtx.beginPath();
            zCtx.ellipse(lx, leechY, 12, 6, Math.sin(wave+i)*0.4, 0, Math.PI*2);
            zCtx.fill();
            // Eye
            zCtx.fillStyle = '#ff0000';
            zCtx.beginPath();
            zCtx.arc(lx+8, leechY-2, 2, 0, Math.PI*2);
            zCtx.fill();
            zCtx.fillStyle = '#2a3a2a';
        }}
    }}
    if(b.special==='swirl') {{
        zCtx.strokeStyle = 'rgba(200,50,50,0.5)';
        zCtx.lineWidth = 3;
        for(let i=0; i<4; i++) {{
            zCtx.beginPath();
            zCtx.arc(Math.sin(wave+i)*18, ly+50+i*25, 12+i*5, wave+i, wave+i+Math.PI);
            zCtx.stroke();
        }}
    }}
    if(b.anim==='float') {{
        zCtx.fillStyle = 'rgba(200,200,180,0.7)';
        for(let i=0; i<7; i++) {{
            const fx = (Math.sin(wave*0.3+i*1.5)-0.5)*bW*0.6;
            const fy = ly+15+((wave*8+i*20)%(lh-15));
            zCtx.beginPath();
            zCtx.ellipse(fx, fy, 4, 3, wave+i, 0, Math.PI*2);
            zCtx.fill();
        }}
    }}
    
    // NIGHTMARE: Face in liquid
    if(NIGHTMARE && Math.random()>0.97) {{
        zCtx.fillStyle = 'rgba(0,0,0,0.4)';
        zCtx.beginPath();
        zCtx.arc(0, ly+lh/2, 20, 0, Math.PI*2);
        zCtx.fill();
        zCtx.fillStyle = 'rgba(255,255,255,0.6)';
        zCtx.beginPath();
        zCtx.arc(-7, ly+lh/2-5, 4, 0, Math.PI*2);
        zCtx.arc(7, ly+lh/2-5, 4, 0, Math.PI*2);
        zCtx.fill();
        zCtx.strokeStyle = 'rgba(255,255,255,0.4)';
        zCtx.beginPath();
        zCtx.arc(0, ly+lh/2+8, 8, 0.2, Math.PI-0.2);
        zCtx.stroke();
    }}
    
    // Cork
    zCtx.fillStyle = '#8b7355';
    zCtx.fillRect(-22, -bH/2-28, 44, 32);
    
    // Label
    zCtx.fillStyle = uvMode ? '#220033' : '#ffffee';
    zCtx.fillRect(-40, -30, 80, 60);
    zCtx.strokeStyle = '#8b7355'; zCtx.lineWidth = 1;
    zCtx.strokeRect(-40, -30, 80, 60);
    zCtx.fillStyle = uvMode ? '{uv_color}' : '#333';
    zCtx.font = '13px Georgia';
    zCtx.textAlign = 'center';
    zCtx.fillText(b.name, 0, -5);
    zCtx.font = '10px Georgia';
    zCtx.fillText(b.sub, 0, 12);
    
    // UV mode extra text
    if(uvMode && b.uv) {{
        zCtx.fillStyle = '{uv_color}';
        zCtx.font = 'italic 9px Georgia';
        zCtx.fillText('UV:', 0, 28);
    }}
    
    zCtx.restore();
    
    // NIGHTMARE: Reaching hand
    if(NIGHTMARE && Math.random()>0.99) {{
        zCtx.fillStyle = 'rgba(100,80,70,0.7)';
        zCtx.beginPath();
        zCtx.moveTo(w-30, h);
        zCtx.lineTo(w-50, h-60);
        zCtx.lineTo(w-35, h-80);
        zCtx.lineTo(w-25, h-65);
        zCtx.lineTo(w-15, h-85);
        zCtx.lineTo(w-10, h-60);
        zCtx.lineTo(w, h);
        zCtx.fill();
    }}
}}

// Hidden compartment (click back 3 times)
let backClicks = 0;
function checkHidden() {{
    raycaster.setFromCamera(mouse, camera);
    const hits = raycaster.intersectObject(back);
    if(hits.length > 0) {{
        backClicks++;
        if(backClicks >= 3 && !hiddenFound) {{
            hiddenFound = true;
            document.getElementById('hidden-flash').style.opacity = 1;
            setTimeout(() => document.getElementById('hidden-flash').style.opacity = 0, 2500);
            if(!found.has('hidden_compartment')) {{
                found.add('hidden_compartment');
                secrets++;
                document.getElementById('snum').textContent = secrets;
            }}
            // Add secret bottle
            const secretBottle = {{
                id:'elixir', name:'THE ELIXIR', sub:'Unknown Origin', color:0x000000, liquid:0x110011,
                level:0.95, row:2, slot:2, desc:'Found behind false panel. Ancient. Terrible.',
                contents:'Older than Fitzroy. Older than the Society.', warn:'DO NOT DRINK',
                secret:'This is what they worship.', uv:'ANNO DOMINI 1666', hasSecret:true,
                mixType:'blood', anim:'swirl', special:'swirl'
            }};
            const g = new THREE.Group();
            const glass = new THREE.Mesh(
                new THREE.CylinderGeometry(0.1, 0.11, 0.38, 12),
                new THREE.MeshLambertMaterial({{ color:0x111111, transparent:true, opacity:0.8 }})
            );
            g.add(glass);
            const liq = new THREE.Mesh(
                new THREE.CylinderGeometry(0.08, 0.09, 0.32, 12),
                new THREE.MeshLambertMaterial({{ color:0x220011, transparent:true, opacity:0.9 }})
            );
            liq.position.y = -0.02;
            g.add(liq);
            g.position.set(0, 1.6, 0.3);
            g.userData = secretBottle;
            scene.add(g);
            bottles.push(g);
        }}
    }}
}}

// Click handler
renderer.domElement.onclick = e => {{
    if(drag) return;
    const cm = new THREE.Vector2((e.clientX/window.innerWidth)*2-1, -(e.clientY/window.innerHeight)*2+1);
    raycaster.setFromCamera(cm, camera);
    
    // Check back panel
    const backHit = raycaster.intersectObject(back);
    if(backHit.length > 0) {{ checkHidden(); return; }}
    
    // Check bottles
    const hits = raycaster.intersectObjects(bottles, true);
    if(hits.length) {{
        let o = hits[0].object;
        while(o && !o.userData.id) o = o.parent;
        if(o) showZoom(o.userData);
    }}
}};

// Animation
const clock = new THREE.Clock();
function animate() {{
    requestAnimationFrame(animate);
    const t = clock.getElapsedTime();
    
    // Hover
    raycaster.setFromCamera(mouse, camera);
    const hits = raycaster.intersectObjects(bottles, true);
    bottles.forEach(b => b.children[0].material.emissive = new THREE.Color(0));
    
    const hint = document.getElementById('hint');
    if(hits.length && !zoomPanel.classList.contains('show')) {{
        let o = hits[0].object;
        while(o && !o.userData.id) o = o.parent;
        if(o) {{
            o.children[0].material.emissive = new THREE.Color({light});
            o.children[0].material.emissiveIntensity = uvMode ? 0.4 : 0.2;
            hint.textContent = o.userData.name;
            hint.style.opacity = 1;
        }}
    }} else if(!zoomPanel.classList.contains('show')) hint.style.opacity = 0;
    
    // Bottle animations (3D)
    bottles.forEach(b => {{
        if(b.userData.special === 'swirl') {{
            b.children[1].rotation.y = t * 0.5;
        }}
        if(b.userData.special === 'leeches') {{
            b.children[1].scale.y = 1 + Math.sin(t*2)*0.05;
        }}
        if(b.userData.anim === 'pulse') {{
            b.children[0].material.opacity = 0.5 + Math.sin(t*3)*0.15;
        }}
        // UV glow
        if(uvMode && b.userData.uv) {{
            b.children[0].material.emissive = new THREE.Color(0x440066);
            b.children[0].material.emissiveIntensity = 0.3 + Math.sin(t*4)*0.1;
        }}
    }});
    
    // 2D animation
    wave += shaking ? 0.4 : 0.03;
    if(sel) draw2d(sel);
    
    // UV flicker
    if(uvMode) uvLight.intensity = 2 + Math.sin(t*10)*0.3;
    
    // NIGHTMARE: Random bottle shake
    if(NIGHTMARE && Math.random() > 0.998) {{
        const randBottle = bottles[Math.floor(Math.random()*bottles.length)];
        randBottle.rotation.z = 0.1;
        setTimeout(() => randBottle.rotation.z = 0, 200);
    }}
    
    renderer.render(scene, camera);
}}

window.onresize = () => {{
    camera.aspect = window.innerWidth/window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
}};

animate();
}})();
</script>
</body>
</html>'''
    return html
