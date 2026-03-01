"""
🧪 The Specimen Cabinet — Victorian Medical Collection
Minimal working version with proper hex formatting.
"""

def get_cabinet_3d(mode: str = "gaslight", intensity: int = 3) -> str:
    """Generate the interactive medical cabinet."""
    
    # Mode-based colors (as hex strings for direct JS use)
    if mode == "gothic":
        bg_color = "0x0a0505"
        wood_color = "0x3a1818"
        wood_dark = "0x1a0808"
        metal_color = "0x5a5a5a"
        light_color = "0xff4422"
        text_color = "#cc0000"
        ambient = 0.35
    elif mode == "clinical":
        bg_color = "0xe8e8e8"
        wood_color = "0xd8d0c8"
        wood_dark = "0xc0b8b0"
        metal_color = "0xbbbbbb"
        light_color = "0xffffff"
        text_color = "#2f4f4f"
        ambient = 0.7
    else:  # gaslight
        bg_color = "0x1a1410"
        wood_color = "0x5a4530"
        wood_dark = "0x3c2818"
        metal_color = "0xc8a030"
        light_color = "0xffbb55"
        text_color = "#d4a574"
        ambient = 0.5
    
    creep = intensity / 5.0
    
    html = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            width: 100%; height: 100vh;
            overflow: hidden; 
            background: #1a1410;
            font-family: Georgia, serif;
            color: {text_color};
        }}
        #container {{ width: 100%; height: 100%; }}
        #title {{
            position: absolute;
            top: 20px; left: 50%;
            transform: translateX(-50%);
            font-size: 18px;
            letter-spacing: 3px;
            opacity: 0.8;
            z-index: 100;
            pointer-events: none;
        }}
        #info {{
            position: absolute;
            bottom: 20px; left: 50%;
            transform: translateX(-50%);
            font-size: 12px;
            opacity: 0.6;
            z-index: 100;
            pointer-events: none;
        }}
        #hint {{
            position: absolute;
            bottom: 60px; left: 50%;
            transform: translateX(-50%);
            font-size: 14px;
            background: rgba(0,0,0,0.8);
            padding: 8px 16px;
            border-radius: 4px;
            opacity: 0;
            transition: opacity 0.3s;
            z-index: 100;
            pointer-events: none;
        }}
        #secrets {{
            position: absolute;
            top: 20px; right: 20px;
            font-size: 13px;
            opacity: 0.7;
            z-index: 100;
            pointer-events: none;
        }}
        .vignette {{
            position: absolute;
            top: 0; left: 0;
            width: 100%; height: 100%;
            background: radial-gradient(ellipse at center, transparent 50%, rgba(0,0,0,0.5) 100%);
            pointer-events: none;
            z-index: 50;
        }}
        #detail {{
            position: absolute;
            top: 0; left: 0;
            width: 100%; height: 100%;
            background: rgba(0,0,0,0.95);
            display: none;
            z-index: 200;
            padding: 50px;
        }}
        #detail.show {{ display: flex; }}
        #detail-left {{ flex: 1; display: flex; align-items: center; justify-content: center; }}
        #detail-right {{ flex: 1; max-width: 400px; display: flex; flex-direction: column; justify-content: center; }}
        #detail h2 {{ font-size: 28px; margin-bottom: 10px; }}
        #detail h3 {{ font-size: 14px; opacity: 0.6; margin-bottom: 20px; font-weight: normal; font-style: italic; }}
        #detail p {{ font-size: 15px; line-height: 1.7; margin-bottom: 15px; }}
        #detail .warn {{ background: #442200; padding: 8px 14px; font-size: 11px; letter-spacing: 2px; display: inline-block; }}
        #detail .secret {{ color: #cc4444; font-style: italic; margin-top: 20px; opacity: 0; transition: opacity 1s; }}
        #detail .secret.show {{ opacity: 1; }}
        #close {{ position: absolute; top: 30px; right: 40px; font-size: 36px; cursor: pointer; opacity: 0.6; }}
        #close:hover {{ opacity: 1; }}
        #btns {{ margin-top: 25px; display: flex; gap: 12px; }}
        #btns button {{ 
            padding: 10px 20px; 
            background: transparent; 
            border: 1px solid {text_color}55; 
            color: {text_color}; 
            font-family: Georgia; 
            cursor: pointer; 
        }}
        #btns button:hover {{ background: rgba(255,255,255,0.1); }}
        canvas#bottle2d {{ border: 1px solid {text_color}33; }}
    </style>
</head>
<body>
    <div id="container"></div>
    <div class="vignette"></div>
    <div id="title">THE FITZROY COLLECTION</div>
    <div id="info">Drag to rotate • Scroll to zoom • Click bottles</div>
    <div id="hint"></div>
    <div id="secrets">Secrets: <span id="snum">0</span>/8</div>
    
    <div id="detail">
        <div id="close">×</div>
        <div id="detail-left"><canvas id="bottle2d" width="300" height="400"></canvas></div>
        <div id="detail-right">
            <h2 id="d-name"></h2>
            <h3 id="d-sub"></h3>
            <p id="d-desc"></p>
            <p id="d-contents"></p>
            <div class="warn" id="d-warn"></div>
            <p class="secret" id="d-secret"></p>
            <div id="btns">
                <button id="btn-shake">Shake</button>
                <button id="btn-smell">Smell</button>
            </div>
        </div>
    </div>
    
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script>
    (function() {{
        const INTENSITY = {intensity};
        let secrets = 0;
        const found = new Set();
        
        // Bottle data
        const BOTTLES = [
            {{ id:'laudanum', name:'Laudanum', sub:'Tincture of Opium', color:0xcc8844, liquid:0x553311, level:0.6, row:0, slot:0, desc:'Opium dissolved in alcohol. Prescribed for everything.', contents:'Nearly half empty.', warn:'ADDICTIVE', secret:'Note: "Mrs. Harrison — 40 drops. She asks too many questions."', hasSecret:true }},
            {{ id:'chloroform', name:'Chloroform', sub:'Anesthetic', color:0x4466bb, liquid:0xccddff, level:0.25, row:0, slot:1, desc:'Volatile anesthetic. Revolutionary—and dangerous.', contents:'Recently used.', warn:'POISON', secret:'Fingerprints in dust. No surgeries scheduled.', hasSecret:INTENSITY>=3 }},
            {{ id:'soothing', name:"Mrs. Winslow's Syrup", sub:'For Infants', color:0xeeddbb, liquid:0x997755, level:0.75, row:0, slot:2, desc:'Soothing syrup for babies. Cheerful label.', contents:'Morphine and alcohol.', warn:'EXTERNAL USE', secret:'Dosage is 10x normal. Compounded specially.', hasSecret:INTENSITY>=2 }},
            {{ id:'mercury', name:'Mercury Bichloride', sub:'Blue Mass', color:0x334455, liquid:0x99aaaa, level:0.5, row:0, slot:3, desc:'Treatment for syphilis. Causes madness.', contents:'Silver shimmer.', warn:'TOXIC', secret:'Names hidden behind label.', hasSecret:INTENSITY>=4 }},
            {{ id:'arsenic', name:'Arsenic Wafers', sub:'Complexion', color:0x88aa77, liquid:0xcceecc, level:0.65, row:0, slot:4, desc:'For pale complexion. Women ate these.', contents:'Sweet-tasting poison.', warn:'AS DIRECTED', secret:'Why does an anatomist keep these?', hasSecret:INTENSITY>=3 }},
            
            {{ id:'ether', name:'Diethyl Ether', sub:'Anesthetic', color:0x775533, liquid:0xffeedd, level:0.35, row:1, slot:0, desc:'Patients sleep through surgery. Usually.', contents:'Highly flammable.', warn:'NO FLAME', secret:'Scratches inside the lid.', hasSecret:INTENSITY>=5 }},
            {{ id:'cocaine', name:'Cocaine Solution', sub:'4% Local', color:0xeeeeff, liquid:0xffffff, level:0.12, row:1, slot:1, desc:'Local anesthetic. Improves confidence.', contents:'Nearly empty.', warn:'MEDICINAL', secret:"Fitzroy's personal supply. Daily use.", hasSecret:true }},
            {{ id:'strychnine', name:'Strychnine', sub:'Nerve Tonic', color:0xdd3333, liquid:0xffcccc, level:0.5, row:1, slot:2, desc:'Stimulant in small doses. Death in larger.', contents:'Bright red warning.', warn:'POISON', secret:'New dosage would be lethal.', hasSecret:INTENSITY>=4 }},
            {{ id:'carbolic', name:'Carbolic Acid', sub:'Antiseptic', color:0x4455aa, liquid:0xeeeedd, level:0.7, row:1, slot:3, desc:"Lister's miracle. Also destroys evidence.", contents:'Burns organic matter.', warn:'CORROSIVE', secret:'Blood and hair on cap.', hasSecret:INTENSITY>=4 }},
            {{ id:'embalming', name:'Embalming Fluid', sub:'Preservation', color:0x888866, liquid:0xccccaa, level:0.85, row:1, slot:4, desc:'For preserving specimens.', contents:'Unusually large supply.', warn:'TOXIC FUMES', secret:'Why so much? Hospital provides this.', hasSecret:INTENSITY>=3 }},
            
            {{ id:'vita', name:'Vita Aeterna', sub:'Eternal Essence', color:0x880022, liquid:0xaa0000, level:0.55, row:2, slot:0, desc:"Society's communion. Swirls on its own.", contents:'Too red for wine.', warn:'MEMBERS ONLY', secret:'"Sanguis innocentum" — Blood of innocents.', hasSecret:true, special:'swirl' }},
            {{ id:'unmarked', name:'Bottle #7', sub:'Unmarked', color:0x666666, liquid:0xeeeeee, level:0.5, row:2, slot:1, desc:'No label. Smells of almonds.', contents:'Cyanide.', warn:'DO NOT OPEN', secret:'Enough to kill a hundred.', hasSecret:INTENSITY>=3 }},
            {{ id:'unwilling', name:'"For the Unwilling"', sub:'Special', color:0x222222, liquid:0x332244, level:0.7, row:2, slot:2, desc:'Black glass. Society uses for subjects.', contents:'Immediate unconsciousness.', warn:'SOCIETY ONLY', secret:'12 "donations" this year. None voluntary.', hasSecret:true }},
            {{ id:'mercy', name:'"Final Mercy"', sub:'Terminal', color:0xaa0000, liquid:0x220000, level:0.9, row:2, slot:3, desc:'Tiny vial. Red skull. Ends suffering.', contents:'Death in seconds.', warn:'EMERGENCY', secret:'3 doses missing. 3 hearts "gave out."', hasSecret:INTENSITY>=4 }},
            {{ id:'blood_sc', name:'Blood — S.C.', sub:'Specimen', color:0xdddddd, liquid:0x660000, level:0.6, row:2, slot:4, desc:'Test tube. Initials S.C.', contents:'Still viable.', warn:'DO NOT DISCARD', secret:'Sebastian Carlisle. Why keep his blood?', hasSecret:true }},
            
            {{ id:'teeth', name:'Dental Collection', sub:'Human Teeth', color:0xffffdd, liquid:0xffffcc, level:0.8, row:3, slot:0, desc:'47 teeth in alcohol.', contents:'From at least 12 sources.', warn:'SPECIMEN', secret:'Some extracted from the living.', hasSecret:INTENSITY>=3 }},
            {{ id:'leeches', name:'Leeches', sub:'Live', color:0xccffcc, liquid:0xaaddaa, level:0.7, row:3, slot:1, desc:'They press against glass, sensing you.', contents:'A dozen. Hungry.', warn:'LIVE', secret:'Why so large? Hospital stopped using these.', hasSecret:INTENSITY>=2, special:'leeches' }},
            {{ id:'essence', name:'"Essence of Youth"', sub:'Rejuvenation', color:0xddccbb, liquid:0xffffdd, level:0.6, row:3, slot:2, desc:'Waxy substance. Smells of fat.', contents:'Softens wrinkles.', warn:'EXTERNAL', secret:'Human fat. Made from poor. Sold to rich.', hasSecret:INTENSITY>=4 }},
            {{ id:'tapeworm', name:'Tapeworm', sub:'Diet Aid', color:0xeeeedd, liquid:0xffffee, level:0.7, row:3, slot:3, desc:'Victorians swallowed these.', contents:'"Natural" weight loss.', warn:'NOT FOR EATING', secret:'Someone is farming these.', hasSecret:INTENSITY>=3 }},
            {{ id:'brain', name:'Nerve Food', sub:'For Weakness', color:0xbbaa88, liquid:0xccbbaa, level:0.5, row:3, slot:4, desc:'Gray matter in fluid.', contents:'"Transfers mental energy."', warn:'TWICE DAILY', secret:'Human brain. Cannibalism as medicine.', hasSecret:true }}
        ];
        
        // Scene
        const container = document.getElementById('container');
        const scene = new THREE.Scene();
        scene.background = new THREE.Color({bg_color});
        
        const camera = new THREE.PerspectiveCamera(50, window.innerWidth/window.innerHeight, 0.1, 100);
        camera.position.set(0, 1.5, 6);
        camera.lookAt(0, 1.2, 0);
        
        const renderer = new THREE.WebGLRenderer({{ antialias: true }});
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        container.appendChild(renderer.domElement);
        
        // Lights
        scene.add(new THREE.AmbientLight(0xffffff, {ambient}));
        scene.add(new THREE.HemisphereLight(0xffffff, {wood_dark}, 0.4));
        
        const dir = new THREE.DirectionalLight({light_color}, 1.0);
        dir.position.set(3, 5, 4);
        scene.add(dir);
        
        const fill = new THREE.PointLight({light_color}, 0.6);
        fill.position.set(-3, 3, 3);
        scene.add(fill);
        
        // Materials
        const woodMat = new THREE.MeshLambertMaterial({{ color: {wood_color} }});
        const darkMat = new THREE.MeshLambertMaterial({{ color: {wood_dark} }});
        const metalMat = new THREE.MeshLambertMaterial({{ color: {metal_color} }});
        
        // Cabinet
        const W = 4, H = 3.2, D = 0.7, ROWS = 4;
        const SH = H / ROWS;
        
        // Back
        const back = new THREE.Mesh(new THREE.BoxGeometry(W, H, 0.05), darkMat);
        back.position.set(0, H/2, -D/2);
        scene.add(back);
        
        // Sides
        [-1, 1].forEach(s => {{
            const side = new THREE.Mesh(new THREE.BoxGeometry(0.08, H, D), woodMat);
            side.position.set(s * W/2, H/2, 0);
            scene.add(side);
        }});
        
        // Top
        const top = new THREE.Mesh(new THREE.BoxGeometry(W + 0.1, 0.1, D + 0.1), woodMat);
        top.position.set(0, H + 0.05, 0);
        scene.add(top);
        
        // Shelves
        for (let i = 0; i <= ROWS; i++) {{
            const shelf = new THREE.Mesh(new THREE.BoxGeometry(W - 0.1, 0.04, D - 0.08), woodMat);
            shelf.position.set(0, i * SH, 0);
            scene.add(shelf);
        }}
        
        // Bottles
        const bottles = [];
        const raycaster = new THREE.Raycaster();
        const mouse = new THREE.Vector2();
        
        function slotPos(row, slot) {{
            const startX = -W/2 + 0.45;
            const spacing = (W - 0.9) / 4;
            return {{ x: startX + slot * spacing, y: row * SH + 0.18, z: 0 }};
        }}
        
        BOTTLES.forEach(b => {{
            const g = new THREE.Group();
            
            // Glass
            const glass = new THREE.Mesh(
                new THREE.CylinderGeometry(0.08, 0.09, 0.32, 12),
                new THREE.MeshLambertMaterial({{ color: b.color, transparent: true, opacity: 0.6 }})
            );
            g.add(glass);
            
            // Liquid
            const lh = 0.28 * b.level;
            const liq = new THREE.Mesh(
                new THREE.CylinderGeometry(0.065, 0.075, lh, 12),
                new THREE.MeshLambertMaterial({{ color: b.liquid, transparent: true, opacity: 0.85 }})
            );
            liq.position.y = -0.14 + lh/2 + 0.02;
            g.add(liq);
            
            // Cork
            const cork = new THREE.Mesh(
                new THREE.CylinderGeometry(0.035, 0.04, 0.05, 8),
                new THREE.MeshLambertMaterial({{ color: 0x8b7355 }})
            );
            cork.position.y = 0.18;
            g.add(cork);
            
            // Label
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
        let drag = false, px = 0, py = 0;
        let theta = 0, phi = 1.2, dist = 6;
        const target = new THREE.Vector3(0, 1.3, 0);
        
        function updateCam() {{
            camera.position.x = target.x + dist * Math.sin(phi) * Math.sin(theta);
            camera.position.y = target.y + dist * Math.cos(phi);
            camera.position.z = target.z + dist * Math.sin(phi) * Math.cos(theta);
            camera.lookAt(target);
        }}
        
        renderer.domElement.onmousedown = e => {{ drag = true; px = e.clientX; py = e.clientY; }};
        window.onmouseup = () => drag = false;
        renderer.domElement.onmousemove = e => {{
            mouse.x = (e.clientX / window.innerWidth) * 2 - 1;
            mouse.y = -(e.clientY / window.innerHeight) * 2 + 1;
            if (drag) {{
                theta += (e.clientX - px) * 0.005;
                phi = Math.max(0.5, Math.min(1.4, phi + (e.clientY - py) * 0.005));
                px = e.clientX; py = e.clientY;
                updateCam();
            }}
        }};
        renderer.domElement.onwheel = e => {{
            e.preventDefault();
            dist = Math.max(3.5, Math.min(10, dist + e.deltaY * 0.005));
            updateCam();
        }};
        updateCam();
        
        // Detail panel
        let sel = null, wave = 0, shaking = false;
        const detail = document.getElementById('detail');
        const canvas2d = document.getElementById('bottle2d');
        const ctx = canvas2d.getContext('2d');
        
        function showDetail(b) {{
            sel = b;
            document.getElementById('d-name').textContent = b.name;
            document.getElementById('d-sub').textContent = b.sub;
            document.getElementById('d-desc').textContent = b.desc;
            document.getElementById('d-contents').textContent = b.contents;
            document.getElementById('d-warn').textContent = '⚠ ' + b.warn;
            
            const sec = document.getElementById('d-secret');
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
            
            detail.classList.add('show');
        }}
        
        document.getElementById('close').onclick = () => {{ detail.classList.remove('show'); sel = null; }};
        
        renderer.domElement.onclick = e => {{
            if (drag) return;
            const cm = new THREE.Vector2(
                (e.clientX / window.innerWidth) * 2 - 1,
                -(e.clientY / window.innerHeight) * 2 + 1
            );
            raycaster.setFromCamera(cm, camera);
            const hits = raycaster.intersectObjects(bottles, true);
            if (hits.length) {{
                let o = hits[0].object;
                while (o && !o.userData.id) o = o.parent;
                if (o) showDetail(o.userData);
            }}
        }};
        
        // 2D render
        function draw2d(b) {{
            const w = canvas2d.width, h = canvas2d.height;
            ctx.clearRect(0, 0, w, h);
            ctx.save();
            ctx.translate(w/2, h/2);
            if (shaking) ctx.rotate(Math.sin(wave * 3) * 0.1);
            
            // Glass
            ctx.fillStyle = '#' + b.color.toString(16).padStart(6, '0') + '99';
            ctx.strokeStyle = '#' + b.color.toString(16).padStart(6, '0');
            ctx.lineWidth = 3;
            ctx.beginPath();
            ctx.roundRect(-45, -110, 90, 220, 10);
            ctx.fill(); ctx.stroke();
            
            // Liquid
            const lh = 180 * b.level;
            const ly = 110 - lh - 15;
            ctx.fillStyle = '#' + b.liquid.toString(16).padStart(6, '0') + 'dd';
            ctx.beginPath();
            ctx.moveTo(-35, ly + Math.sin(wave) * 4);
            for (let x = -35; x <= 35; x += 8) ctx.lineTo(x, ly + Math.sin(wave + x * 0.1) * 4);
            ctx.lineTo(35, 95); ctx.lineTo(-35, 95);
            ctx.closePath(); ctx.fill();
            
            // Leeches
            if (b.special === 'leeches') {{
                ctx.fillStyle = '#2a3a2a';
                for (let i = 0; i < 4; i++) {{
                    ctx.beginPath();
                    ctx.ellipse(Math.sin(wave*0.5+i*2)*25, ly+40+i*20, 10, 5, Math.sin(wave+i)*0.4, 0, Math.PI*2);
                    ctx.fill();
                }}
            }}
            
            // Swirl
            if (b.special === 'swirl') {{
                ctx.strokeStyle = 'rgba(255,50,50,0.5)';
                ctx.lineWidth = 3;
                for (let i = 0; i < 3; i++) {{
                    ctx.beginPath();
                    ctx.arc(Math.sin(wave+i)*15, ly+50+i*20, 10+i*5, wave+i, wave+i+Math.PI);
                    ctx.stroke();
                }}
            }}
            
            // Cork
            ctx.fillStyle = '#8b7355';
            ctx.fillRect(-18, -135, 36, 28);
            
            // Label
            ctx.fillStyle = '#ffffee';
            ctx.fillRect(-35, -25, 70, 50);
            ctx.strokeStyle = '#8b7355'; ctx.lineWidth = 1;
            ctx.strokeRect(-35, -25, 70, 50);
            ctx.fillStyle = '#333';
            ctx.font = '11px Georgia';
            ctx.textAlign = 'center';
            ctx.fillText(b.name, 0, -2);
            ctx.font = '9px Georgia';
            ctx.fillText(b.sub, 0, 12);
            
            ctx.restore();
        }}
        
        document.getElementById('btn-shake').onclick = () => {{ shaking = true; setTimeout(() => shaking = false, 800); }};
        document.getElementById('btn-smell').onclick = () => {{
            const smells = {{ laudanum:'Bitter medicine...', chloroform:'Sweet, dangerous.', vita:'Iron and salt.', leeches:'Stagnant water.', unmarked:'Bitter almonds!' }};
            const hint = document.getElementById('hint');
            hint.textContent = smells[sel?.id] || 'Chemical odor...';
            hint.style.opacity = 1;
            setTimeout(() => hint.style.opacity = 0, 2500);
        }};
        
        // Animation
        function animate() {{
            requestAnimationFrame(animate);
            
            // Hover
            raycaster.setFromCamera(mouse, camera);
            const hits = raycaster.intersectObjects(bottles, true);
            bottles.forEach(b => b.children[0].material.emissive = new THREE.Color(0));
            
            const hint = document.getElementById('hint');
            if (hits.length && !detail.classList.contains('show')) {{
                let o = hits[0].object;
                while (o && !o.userData.id) o = o.parent;
                if (o) {{
                    o.children[0].material.emissive = new THREE.Color({light_color});
                    o.children[0].material.emissiveIntensity = 0.2;
                    hint.textContent = o.userData.name;
                    hint.style.opacity = 1;
                }}
            }} else if (!detail.classList.contains('show')) hint.style.opacity = 0;
            
            // 2D
            wave += shaking ? 0.4 : 0.03;
            if (sel) draw2d(sel);
            
            renderer.render(scene, camera);
        }}
        
        window.onresize = () => {{
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        }};
        
        animate();
    }})();
    </script>
</body>
</html>'''
    return html
