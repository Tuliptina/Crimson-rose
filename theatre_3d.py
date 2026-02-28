"""
🎭 The Anatomy Theatre — Ultimate 3D Experience
Fully immersive Three.js Victorian anatomy theatre with:
- Animated spectators and anatomist
- Interactive clickable objects
- Atmospheric effects (fog, shadows, rain)
- Story elements (Red Rose secrets, hidden lore)
- Intensity-scaled creepiness
"""

def get_theatre_3d(mode: str = "gaslight", intensity: int = 3) -> str:
    """
    Generate the ultimate 3D anatomy theatre.
    
    Args:
        mode: Visual mode (gaslight, gothic, clinical)
        intensity: Atmosphere intensity 1-5 (scales creepiness)
    """
    
    # Color schemes per mode
    colors = {
        "gaslight": {
            "ambient": 0x2a1a0a,
            "background": 0x1a1410,
            "wood": 0x4a3520,
            "wood_dark": 0x2c1810,
            "metal": 0xb8860b,
            "cloth": 0xf5f5dc,
            "skin": 0xdcbfa0,
            "light_color": 0xffaa44,
            "light_intensity": 1.5,
            "fog_color": 0x1a1410,
            "fog_near": 5,
            "fog_far": 50,
            "particle_color": 0xffcc88,
            "text_color": "#d4a574",
            "rose_color": 0x8b0000,
            "spectator_color": 0x1a1a1a
        },
        "gothic": {
            "ambient": 0x1a0505,
            "background": 0x0a0a0a,
            "wood": 0x2a1515,
            "wood_dark": 0x1a0a0a,
            "metal": 0x4a4a4a,
            "cloth": 0x8b0000,
            "skin": 0x998877,
            "light_color": 0xff2200,
            "light_intensity": 2.0,
            "fog_color": 0x0a0000,
            "fog_near": 3,
            "fog_far": 35,
            "particle_color": 0xff4444,
            "text_color": "#cc0000",
            "rose_color": 0xff0000,
            "spectator_color": 0x0a0a0a
        },
        "clinical": {
            "ambient": 0x404040,
            "background": 0xf0f0f0,
            "wood": 0xe0e0e0,
            "wood_dark": 0xcccccc,
            "metal": 0xaaaaaa,
            "cloth": 0xffffff,
            "skin": 0xeeddcc,
            "light_color": 0xffffff,
            "light_intensity": 2.5,
            "fog_color": 0xf0f0f0,
            "fog_near": 20,
            "fog_far": 100,
            "particle_color": 0xcccccc,
            "text_color": "#2f4f4f",
            "rose_color": 0xcc0000,
            "spectator_color": 0x333333
        }
    }
    
    c = colors.get(mode, colors["gaslight"])
    
    # Intensity scaling
    fog_density = 1 + (intensity - 1) * 0.3
    particle_count = 80 + intensity * 40
    spectator_count = 5 + intensity * 3
    flicker_intensity = 0.05 + intensity * 0.04
    creep_factor = intensity / 5.0
    
    def to_hex(val):
        return f"0x{val:06x}"
    
    html = f'''
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        html, body {{ 
            width: 100%;
            height: 100%;
            overflow: hidden; 
            background: #{c["background"]:06x};
            font-family: 'Georgia', serif;
        }}
        #container {{ 
            width: 100%; 
            height: 100%; 
            position: relative;
            cursor: grab;
        }}
        #container:active {{ cursor: grabbing; }}
        canvas {{
            display: block;
            width: 100% !important;
            height: 100% !important;
        }}
        .ui-overlay {{
            position: absolute;
            pointer-events: none;
            z-index: 100;
        }}
        #info {{
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            color: {c["text_color"]};
            font-size: 13px;
            text-align: center;
            text-shadow: 0 0 10px rgba(0,0,0,0.9);
            opacity: 0.7;
        }}
        #mode-label {{
            top: 20px;
            left: 20px;
            color: {c["text_color"]};
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 3px;
            opacity: 0.5;
        }}
        #intensity-label {{
            top: 20px;
            right: 20px;
            color: {c["text_color"]};
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 2px;
            opacity: 0.5;
        }}
        #discovery-count {{
            top: 45px;
            right: 20px;
            color: {c["text_color"]};
            font-size: 12px;
            opacity: 0.6;
        }}
        #tooltip {{
            position: absolute;
            background: rgba(0,0,0,0.9);
            color: {c["text_color"]};
            padding: 12px 16px;
            border-radius: 4px;
            font-size: 13px;
            max-width: 280px;
            line-height: 1.5;
            pointer-events: none;
            opacity: 0;
            transition: opacity 0.3s;
            z-index: 200;
            border: 1px solid {c["text_color"]}44;
        }}
        #tooltip.visible {{ opacity: 1; }}
        #tooltip .title {{
            font-weight: bold;
            margin-bottom: 6px;
            color: {'#cc0000' if mode == 'gothic' else c["text_color"]};
        }}
        #tooltip .lore {{
            font-style: italic;
            font-size: 12px;
            margin-top: 8px;
            opacity: 0.8;
            border-top: 1px solid {c["text_color"]}33;
            padding-top: 8px;
        }}
        #quote {{
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            color: {c["text_color"]};
            font-size: 20px;
            font-style: italic;
            text-align: center;
            max-width: 500px;
            opacity: 0;
            transition: opacity 2s;
            pointer-events: none;
            text-shadow: 0 0 30px rgba(0,0,0,0.95);
            z-index: 100;
        }}
        #whisper {{
            position: absolute;
            bottom: 80px;
            left: 50%;
            transform: translateX(-50%);
            color: {c["text_color"]};
            font-size: 14px;
            font-style: italic;
            opacity: 0;
            transition: opacity 1s;
            pointer-events: none;
            text-shadow: 0 0 15px rgba(0,0,0,0.9);
            z-index: 100;
        }}
        .vignette {{
            position: absolute;
            top: 0; left: 0;
            width: 100%; height: 100%;
            pointer-events: none;
            background: radial-gradient(ellipse at center, 
                transparent 30%, 
                rgba(0,0,0,{0.5 + creep_factor * 0.3 if mode != 'clinical' else 0.1}) 100%);
            z-index: 50;
        }}
        #lightning {{
            position: absolute;
            top: 0; left: 0;
            width: 100%; height: 100%;
            background: white;
            opacity: 0;
            pointer-events: none;
            z-index: 60;
        }}
        #blood-overlay {{
            position: absolute;
            top: 0; left: 0;
            width: 100%; height: 100%;
            background: radial-gradient(ellipse at center, transparent 60%, rgba(139,0,0,0.3) 100%);
            opacity: 0;
            pointer-events: none;
            z-index: 55;
            transition: opacity 0.5s;
        }}
        .secret-found {{
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            color: #cc0000;
            font-size: 16px;
            text-transform: uppercase;
            letter-spacing: 4px;
            opacity: 0;
            pointer-events: none;
            z-index: 150;
            text-shadow: 0 0 20px rgba(139,0,0,0.8);
            transition: opacity 0.5s;
        }}
    </style>
</head>
<body>
    <div id="container"></div>
    <div class="vignette"></div>
    <div id="lightning"></div>
    <div id="blood-overlay"></div>
    
    <div id="mode-label" class="ui-overlay">{mode.upper()}</div>
    <div id="intensity-label" class="ui-overlay">INTENSITY {intensity}</div>
    <div id="discovery-count" class="ui-overlay">Secrets: <span id="rose-count">0</span>/5</div>
    <div id="info" class="ui-overlay">Drag to orbit | Scroll to zoom | Click to examine</div>
    <div id="tooltip"><div class="title"></div><div class="desc"></div><div class="lore"></div></div>
    <div id="quote"></div>
    <div id="whisper"></div>
    <div class="secret-found" id="secret-msg">SECRET DISCOVERED</div>
    
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script>
    (function() {{
        'use strict';
        
        const MODE = '{mode}';
        const INTENSITY = {intensity};
        const CREEP = {creep_factor};
        
        let secretsFound = 0;
        const foundSecrets = new Set();
        const clickableObjects = [];
        
        // Scene
        const container = document.getElementById('container');
        const width = container.clientWidth || window.innerWidth;
        const height = container.clientHeight || window.innerHeight;
        
        const scene = new THREE.Scene();
        scene.background = new THREE.Color({to_hex(c["background"])});
        scene.fog = new THREE.FogExp2({to_hex(c["fog_color"])}, {0.012 * fog_density});
        
        const camera = new THREE.PerspectiveCamera(55, width / height, 0.1, 1000);
        camera.position.set(18, 12, 18);
        camera.lookAt(0, 2, 0);
        
        const renderer = new THREE.WebGLRenderer({{ antialias: true }});
        renderer.setSize(width, height);
        renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        renderer.shadowMap.enabled = true;
        renderer.shadowMap.type = THREE.PCFSoftShadowMap;
        container.appendChild(renderer.domElement);
        
        const raycaster = new THREE.Raycaster();
        const mouse = new THREE.Vector2();
        
        // Materials
        const woodMat = new THREE.MeshLambertMaterial({{ color: {to_hex(c["wood"])} }});
        const darkWoodMat = new THREE.MeshLambertMaterial({{ color: {to_hex(c["wood_dark"])} }});
        const metalMat = new THREE.MeshLambertMaterial({{ color: {to_hex(c["metal"])} }});
        const clothMat = new THREE.MeshLambertMaterial({{ color: {to_hex(c["cloth"])}, side: THREE.DoubleSide }});
        const skinMat = new THREE.MeshLambertMaterial({{ color: {to_hex(c["skin"])} }});
        const stoneMat = new THREE.MeshLambertMaterial({{ color: 0x444444 }});
        const spectatorMat = new THREE.MeshLambertMaterial({{ color: {to_hex(c["spectator_color"])} }});
        const roseMat = new THREE.MeshBasicMaterial({{ color: {to_hex(c["rose_color"])}, transparent: true, opacity: 0.9 }});
        
        // Lighting
        scene.add(new THREE.AmbientLight(0xffffff, 0.3));
        scene.add(new THREE.HemisphereLight(0xffffff, {to_hex(c["wood_dark"])}, 0.4));
        
        const dirLight = new THREE.DirectionalLight({to_hex(c["light_color"])}, 0.8);
        dirLight.position.set(10, 25, 10);
        dirLight.castShadow = true;
        dirLight.shadow.mapSize.width = 1024;
        dirLight.shadow.mapSize.height = 1024;
        scene.add(dirLight);
        
        const spotlight = new THREE.SpotLight({to_hex(c["light_color"])}, {c["light_intensity"] * 1.2});
        spotlight.position.set(0, 12, 0);
        spotlight.angle = Math.PI / 5;
        spotlight.penumbra = 0.4;
        spotlight.castShadow = true;
        scene.add(spotlight);
        
        // Floor
        const floor = new THREE.Mesh(
            new THREE.CircleGeometry(22, 64),
            stoneMat
        );
        floor.rotation.x = -Math.PI / 2;
        floor.receiveShadow = true;
        scene.add(floor);
        
        // Central pit
        const pit = new THREE.Mesh(
            new THREE.CircleGeometry(4.5, 32),
            new THREE.MeshLambertMaterial({{ color: 0x222222 }})
        );
        pit.rotation.x = -Math.PI / 2;
        pit.position.y = 0.01;
        scene.add(pit);
        
        // Gallery tiers
        const tierCount = 5;
        const tierHeight = 1.3;
        const tierDepth = 2.2;
        const innerRadius = 5.5;
        
        for (let i = 0; i < tierCount; i++) {{
            const radius = innerRadius + i * tierDepth;
            const y = i * tierHeight;
            
            // Platform ring
            const shape = new THREE.Shape();
            shape.absarc(0, 0, radius + tierDepth - 0.15, 0, Math.PI * 2, false);
            const hole = new THREE.Path();
            hole.absarc(0, 0, radius, 0, Math.PI * 2, true);
            shape.holes.push(hole);
            
            const tier = new THREE.Mesh(
                new THREE.ExtrudeGeometry(shape, {{ depth: 0.25, bevelEnabled: false }}),
                woodMat
            );
            tier.rotation.x = -Math.PI / 2;
            tier.position.y = y;
            tier.receiveShadow = true;
            scene.add(tier);
            
            // Railing
            const rail = new THREE.Mesh(
                new THREE.TorusGeometry(radius + 0.15, 0.04, 6, 48),
                metalMat
            );
            rail.rotation.x = Math.PI / 2;
            rail.position.y = y + 0.9;
            scene.add(rail);
        }}
        
        // Back wall
        const wall = new THREE.Mesh(
            new THREE.CylinderGeometry(
                innerRadius + tierCount * tierDepth + 1.5,
                innerRadius + tierCount * tierDepth + 1.5,
                tierCount * tierHeight + 5,
                48, 1, true
            ),
            new THREE.MeshLambertMaterial({{ color: {to_hex(c["wood_dark"])}, side: THREE.BackSide }})
        );
        wall.position.y = (tierCount * tierHeight) / 2;
        scene.add(wall);
        
        // Dissection Table
        const tableGroup = new THREE.Group();
        tableGroup.userData = {{
            type: 'table',
            title: 'The Dissection Table',
            desc: 'Cold metal. Drainage channels. The subject waits.',
            lore: 'How many have lain here before?'
        }};
        
        const tableTop = new THREE.Mesh(new THREE.BoxGeometry(2.8, 0.08, 1.1), metalMat);
        tableTop.position.y = 0.9;
        tableTop.castShadow = true;
        tableGroup.add(tableTop);
        
        [[-0.9, -0.35], [0.9, -0.35], [-0.9, 0.35], [0.9, 0.35]].forEach(p => {{
            const leg = new THREE.Mesh(new THREE.CylinderGeometry(0.06, 0.08, 0.85, 8), metalMat);
            leg.position.set(p[0], 0.425, p[1]);
            tableGroup.add(leg);
        }});
        
        scene.add(tableGroup);
        clickableObjects.push(tableGroup);
        
        // The Subject
        const subjectGroup = new THREE.Group();
        subjectGroup.userData = {{
            type: 'subject',
            title: 'The Subject',
            desc: 'A shape beneath white cloth. Still. Silent.',
            lore: INTENSITY >= 4 ? 'The locket... is that Sarah?' : 'Identity unknown.'
        }};
        
        const body = new THREE.Mesh(new THREE.BoxGeometry(1.5, 0.22, 0.45), clothMat);
        body.position.y = 1.08;
        subjectGroup.add(body);
        
        const head = new THREE.Mesh(new THREE.SphereGeometry(0.14, 16, 12), clothMat);
        head.position.set(-0.9, 1.12, 0);
        subjectGroup.add(head);
        
        const chest = new THREE.Mesh(
            new THREE.SphereGeometry(0.18, 12, 8, 0, Math.PI * 2, 0, Math.PI / 2),
            clothMat
        );
        chest.rotation.x = Math.PI;
        chest.position.set(-0.2, 1.12, 0);
        chest.userData.isChest = true;
        subjectGroup.add(chest);
        
        scene.add(subjectGroup);
        clickableObjects.push(subjectGroup);
        
        // The Anatomist
        const anatomist = new THREE.Group();
        anatomist.userData = {{
            type: 'anatomist',
            title: 'The Anatomist',
            desc: 'A figure of authority. Steady hands. Cold eyes.',
            lore: 'Is that Fitzroy? The stance. The precision.'
        }};
        
        const anatBody = new THREE.Mesh(
            new THREE.CylinderGeometry(0.2, 0.25, 1.4, 8),
            new THREE.MeshLambertMaterial({{ color: 0x1a1a1a }})
        );
        anatBody.position.y = 0.7;
        anatomist.add(anatBody);
        
        const anatHead = new THREE.Mesh(new THREE.SphereGeometry(0.15, 12, 10), skinMat);
        anatHead.position.y = 1.55;
        anatomist.add(anatHead);
        
        const armGeo = new THREE.CylinderGeometry(0.05, 0.05, 0.6, 6);
        const armMat = new THREE.MeshLambertMaterial({{ color: 0x1a1a1a }});
        
        const leftArm = new THREE.Mesh(armGeo, armMat);
        leftArm.position.set(-0.3, 1.0, 0.2);
        leftArm.rotation.set(Math.PI/4, 0, Math.PI/6);
        anatomist.add(leftArm);
        
        const rightArm = new THREE.Mesh(armGeo.clone(), armMat);
        rightArm.position.set(0.3, 1.0, 0.2);
        rightArm.rotation.set(Math.PI/4, 0, -Math.PI/6);
        rightArm.userData.isScalpelHand = true;
        anatomist.add(rightArm);
        
        const scalpel = new THREE.Mesh(
            new THREE.CylinderGeometry(0.01, 0.01, 0.18, 4),
            metalMat
        );
        scalpel.position.set(0.35, 0.65, 0.4);
        scalpel.rotation.x = Math.PI / 3;
        anatomist.add(scalpel);
        
        anatomist.position.set(0, 0, -1.3);
        scene.add(anatomist);
        clickableObjects.push(anatomist);
        
        // Spectators
        const spectators = [];
        const spectatorData = [
            {{ tier: 0, angle: 0.5, desc: 'A medical student. Pale. Sweating.' }},
            {{ tier: 0, angle: 2.1, desc: 'A gentleman with a RED ROSE pinned to his lapel.', hasRose: true }},
            {{ tier: 1, angle: 1.2, desc: 'A woman in mourning. She should not be here.' }},
            {{ tier: 1, angle: 3.8, desc: 'Someone taking frantic notes.' }},
            {{ tier: 2, angle: 0.8, desc: 'A figure who has not moved. Not once.' }},
            {{ tier: 2, angle: 4.2, desc: 'An older man. His hands shake.' }},
            {{ tier: 3, angle: 2.5, desc: 'Empty eyes. Watching YOU, not the table.' }},
            {{ tier: 3, angle: 5.5, desc: 'The sketch artist. What is he drawing?' }},
            {{ tier: 4, angle: 1.0, desc: 'A shadow in the back. Familiar somehow.' }},
            {{ tier: 4, angle: 3.2, desc: 'Another RED ROSE. Definitely Society.', hasRose: true }},
        ];
        
        const numSpectators = Math.min({spectator_count}, spectatorData.length);
        
        for (let i = 0; i < numSpectators; i++) {{
            const data = spectatorData[i];
            const radius = innerRadius + data.tier * tierDepth + tierDepth / 2;
            const y = data.tier * tierHeight + 0.7;
            
            const spectator = new THREE.Group();
            
            const sBody = new THREE.Mesh(
                new THREE.CylinderGeometry(0.15, 0.18, 0.9, 6),
                spectatorMat
            );
            sBody.position.y = 0.45;
            spectator.add(sBody);
            
            const sHead = new THREE.Mesh(
                new THREE.SphereGeometry(0.12, 8, 6),
                spectatorMat
            );
            sHead.position.y = 1.05;
            sHead.userData.isHead = true;
            spectator.add(sHead);
            
            // Add rose pin to some
            if (data.hasRose) {{
                const rose = new THREE.Mesh(
                    new THREE.SphereGeometry(0.04, 6, 4),
                    roseMat
                );
                rose.position.set(0.12, 0.7, 0.1);
                spectator.add(rose);
            }}
            
            spectator.position.set(
                Math.cos(data.angle) * radius,
                y,
                Math.sin(data.angle) * radius
            );
            spectator.lookAt(0, y, 0);
            
            spectator.userData = {{
                type: 'spectator',
                title: 'A Spectator',
                desc: data.desc,
                lore: data.hasRose ? 'The Society has eyes everywhere.' : ''
            }};
            
            scene.add(spectator);
            spectators.push(spectator);
            clickableObjects.push(spectator);
        }}
        
        // Gaslights
        const gaslights = [];
        const glowMeshes = [];
        const gaslightRadius = innerRadius + tierCount * tierDepth;
        
        for (let i = 0; i < 10; i++) {{
            const angle = (i / 10) * Math.PI * 2;
            
            const fixture = new THREE.Mesh(
                new THREE.CylinderGeometry(0.12, 0.18, 0.35, 8),
                metalMat
            );
            fixture.position.set(
                Math.cos(angle) * gaslightRadius,
                tierCount * tierHeight + 0.5,
                Math.sin(angle) * gaslightRadius
            );
            scene.add(fixture);
            
            const light = new THREE.PointLight({to_hex(c["light_color"])}, {c["light_intensity"] * 0.4}, 14);
            light.position.copy(fixture.position);
            light.position.y -= 0.25;
            scene.add(light);
            gaslights.push(light);
            
            const glow = new THREE.Mesh(
                new THREE.SphereGeometry(0.08, 8, 6),
                new THREE.MeshBasicMaterial({{
                    color: {to_hex(c["light_color"])},
                    transparent: true,
                    opacity: 0.85
                }})
            );
            glow.position.copy(light.position);
            scene.add(glow);
            glowMeshes.push(glow);
        }}
        
        // Specimen Cabinets
        const cabinetData = [
            {{ x: -3.8, z: 3.8, contents: 'A heart in a jar. Label: "Subject 23."' }},
            {{ x: 3.8, z: 3.8, contents: 'Infant bones on velvet. A receipt beneath.' }},
            {{ x: -3.8, z: -3.8, contents: 'A brain in spirits. Shrinking.' }},
            {{ x: 3.8, z: -3.8, contents: 'Documents. Black Book fragments.' }}
        ];
        
        cabinetData.forEach((data, idx) => {{
            const cabinet = new THREE.Group();
            
            const cabBody = new THREE.Mesh(
                new THREE.BoxGeometry(0.9, 1.4, 0.45),
                darkWoodMat
            );
            cabBody.position.y = 0.7;
            cabinet.add(cabBody);
            
            const glass = new THREE.Mesh(
                new THREE.PlaneGeometry(0.7, 1.1),
                new THREE.MeshBasicMaterial({{
                    color: 0x88aacc,
                    transparent: true,
                    opacity: 0.15,
                    side: THREE.DoubleSide
                }})
            );
            glass.position.set(0, 0.7, 0.23);
            cabinet.add(glass);
            
            // Jars
            for (let j = 0; j < 3; j++) {{
                const jar = new THREE.Mesh(
                    new THREE.CylinderGeometry(0.06, 0.06, 0.18, 12),
                    new THREE.MeshLambertMaterial({{
                        color: MODE === 'gothic' ? 0x44ff44 : 0xeeffaa,
                        transparent: true,
                        opacity: 0.6,
                        emissive: MODE === 'gothic' ? 0x003300 : 0x111100,
                        emissiveIntensity: 0.4
                    }})
                );
                jar.position.set((j - 1) * 0.22, 0.75, 0.1);
                cabinet.add(jar);
            }}
            
            cabinet.position.set(data.x, 0, data.z);
            cabinet.lookAt(0, 0, 0);
            
            cabinet.userData = {{
                type: 'cabinet',
                title: 'Specimen Cabinet',
                desc: data.contents,
                lore: 'Property of the Anatomy Club.'
            }};
            
            scene.add(cabinet);
            clickableObjects.push(cabinet);
        }});
        
        // Hidden Red Roses (Secrets)
        const roses = [];
        const rosePositions = [
            {{ x: -1.5, y: 0.95, z: 0.5 }},
            {{ x: 0, y: tierCount * tierHeight + 0.2, z: gaslightRadius - 0.8 }},
            {{ x: -6, y: 4.0, z: 2.5 }},
            {{ x: 3.2, y: 0.35, z: -3.8 }},
            {{ x: 5.5, y: 2.6, z: -4.5 }}
        ];
        
        rosePositions.forEach((pos, idx) => {{
            const rose = new THREE.Group();
            
            const petal = new THREE.Mesh(
                new THREE.SphereGeometry(0.05, 8, 6),
                roseMat
            );
            rose.add(petal);
            
            const stem = new THREE.Mesh(
                new THREE.CylinderGeometry(0.008, 0.008, 0.1, 4),
                new THREE.MeshBasicMaterial({{ color: 0x1a4a1a }})
            );
            stem.position.y = -0.07;
            rose.add(stem);
            
            rose.position.set(pos.x, pos.y, pos.z);
            rose.visible = INTENSITY >= 3 || idx < 2;
            
            rose.userData = {{
                type: 'rose',
                title: 'Red Rose',
                desc: 'The symbol of the Society.',
                lore: 'They are everywhere. Watching. Waiting.',
                secretId: 'rose_' + idx,
                isSecret: true
            }};
            
            scene.add(rose);
            roses.push(rose);
            clickableObjects.push(rose);
        }});
        
        // Instrument Tray
        const tray = new THREE.Group();
        const trayMesh = new THREE.Mesh(new THREE.BoxGeometry(0.55, 0.03, 0.28), metalMat);
        tray.add(trayMesh);
        
        for (let i = 0; i < 5; i++) {{
            const inst = new THREE.Mesh(
                new THREE.CylinderGeometry(0.012, 0.008, 0.18, 4),
                metalMat
            );
            inst.position.set(-0.18 + i * 0.09, 0.04, 0);
            inst.rotation.z = Math.PI / 2 + (Math.random() - 0.5) * 0.3;
            tray.add(inst);
        }}
        
        tray.position.set(1.7, 0.92, 0);
        tray.userData = {{
            type: 'tray',
            title: 'Surgical Instruments',
            desc: 'Scalpels, forceps, bone saws. All sharp.',
            lore: 'The blade reveals what words cannot.'
        }};
        scene.add(tray);
        clickableObjects.push(tray);
        
        // Podium
        const podium = new THREE.Group();
        const podBase = new THREE.Mesh(
            new THREE.CylinderGeometry(0.3, 0.35, 1.1, 8),
            darkWoodMat
        );
        podBase.position.y = 0.55;
        podium.add(podBase);
        
        const podTop = new THREE.Mesh(
            new THREE.BoxGeometry(0.5, 0.05, 0.35),
            darkWoodMat
        );
        podTop.position.y = 1.15;
        podTop.rotation.x = -0.2;
        podium.add(podTop);
        
        const notes = new THREE.Mesh(
            new THREE.BoxGeometry(0.3, 0.01, 0.22),
            new THREE.MeshLambertMaterial({{ color: 0xffffee }})
        );
        notes.position.set(0, 1.2, 0);
        notes.rotation.x = -0.2;
        podium.add(notes);
        
        podium.position.set(2.5, 0, -2);
        podium.rotation.y = -Math.PI / 4;
        podium.userData = {{
            type: 'podium',
            title: 'Lecturer\\'s Podium',
            desc: 'Notes in precise handwriting.',
            lore: INTENSITY >= 4 ? '"Fitzroy Protocol, Appendix C..."' : 'Illegible from here.'
        }};
        scene.add(podium);
        clickableObjects.push(podium);
        
        // Particles
        const particleCount = {particle_count};
        const particleGeo = new THREE.BufferGeometry();
        const particlePos = new Float32Array(particleCount * 3);
        const particleVel = [];
        
        for (let i = 0; i < particleCount; i++) {{
            particlePos[i * 3] = (Math.random() - 0.5) * 28;
            particlePos[i * 3 + 1] = Math.random() * 14;
            particlePos[i * 3 + 2] = (Math.random() - 0.5) * 28;
            particleVel.push(0.002 + Math.random() * 0.004);
        }}
        
        particleGeo.setAttribute('position', new THREE.BufferAttribute(particlePos, 3));
        
        const particles = new THREE.Points(particleGeo, new THREE.PointsMaterial({{
            color: {to_hex(c["particle_color"])},
            size: 0.06,
            transparent: true,
            opacity: 0.45
        }}));
        scene.add(particles);
        
        // Ground Fog
        const fogPlanes = [];
        if (MODE !== 'clinical') {{
            for (let i = 0; i < 4; i++) {{
                const fogPlane = new THREE.Mesh(
                    new THREE.PlaneGeometry(30, 30),
                    new THREE.MeshBasicMaterial({{
                        color: {to_hex(c["fog_color"])},
                        transparent: true,
                        opacity: 0.06 + i * 0.02,
                        side: THREE.DoubleSide,
                        depthWrite: false
                    }})
                );
                fogPlane.rotation.x = -Math.PI / 2;
                fogPlane.position.y = 0.1 + i * 0.12;
                scene.add(fogPlane);
                fogPlanes.push(fogPlane);
            }}
        }}
        
        // Camera Controls
        let isDragging = false;
        let prevMouse = {{ x: 0, y: 0 }};
        let spherical = {{ radius: 22, theta: Math.PI / 4, phi: Math.PI / 3 }};
        
        function updateCamera() {{
            camera.position.x = spherical.radius * Math.sin(spherical.phi) * Math.cos(spherical.theta);
            camera.position.y = spherical.radius * Math.cos(spherical.phi);
            camera.position.z = spherical.radius * Math.sin(spherical.phi) * Math.sin(spherical.theta);
            camera.lookAt(0, 2, 0);
        }}
        
        renderer.domElement.addEventListener('mousedown', e => {{
            isDragging = true;
            prevMouse = {{ x: e.clientX, y: e.clientY }};
        }});
        
        renderer.domElement.addEventListener('mousemove', e => {{
            mouse.x = (e.clientX / window.innerWidth) * 2 - 1;
            mouse.y = -(e.clientY / window.innerHeight) * 2 + 1;
            
            if (isDragging) {{
                const dx = e.clientX - prevMouse.x;
                const dy = e.clientY - prevMouse.y;
                spherical.theta -= dx * 0.008;
                spherical.phi = Math.max(0.3, Math.min(1.5, spherical.phi + dy * 0.008));
                prevMouse = {{ x: e.clientX, y: e.clientY }};
                updateCamera();
            }}
        }});
        
        window.addEventListener('mouseup', () => {{ isDragging = false; }});
        
        renderer.domElement.addEventListener('wheel', e => {{
            e.preventDefault();
            spherical.radius = Math.max(12, Math.min(40, spherical.radius + e.deltaY * 0.04));
            updateCamera();
        }}, {{ passive: false }});
        
        // Touch
        renderer.domElement.addEventListener('touchstart', e => {{
            if (e.touches.length === 1) {{
                isDragging = true;
                prevMouse = {{ x: e.touches[0].clientX, y: e.touches[0].clientY }};
            }}
        }});
        
        renderer.domElement.addEventListener('touchmove', e => {{
            if (!isDragging || e.touches.length !== 1) return;
            const dx = e.touches[0].clientX - prevMouse.x;
            const dy = e.touches[0].clientY - prevMouse.y;
            spherical.theta -= dx * 0.008;
            spherical.phi = Math.max(0.3, Math.min(1.5, spherical.phi + dy * 0.008));
            prevMouse = {{ x: e.touches[0].clientX, y: e.touches[0].clientY }};
            updateCamera();
        }});
        
        renderer.domElement.addEventListener('touchend', () => {{ isDragging = false; }});
        
        updateCamera();
        
        // Click Interaction
        const tooltip = document.getElementById('tooltip');
        
        function showTooltip(obj, x, y) {{
            const data = obj.userData;
            tooltip.querySelector('.title').textContent = data.title || '';
            tooltip.querySelector('.desc').textContent = data.desc || '';
            tooltip.querySelector('.lore').textContent = data.lore || '';
            tooltip.querySelector('.lore').style.display = data.lore ? 'block' : 'none';
            tooltip.style.left = Math.min(x + 15, window.innerWidth - 300) + 'px';
            tooltip.style.top = Math.min(y + 15, window.innerHeight - 150) + 'px';
            tooltip.classList.add('visible');
        }}
        
        function hideTooltip() {{
            tooltip.classList.remove('visible');
        }}
        
        renderer.domElement.addEventListener('click', e => {{
            const clickMouse = new THREE.Vector2(
                (e.clientX / window.innerWidth) * 2 - 1,
                -(e.clientY / window.innerHeight) * 2 + 1
            );
            
            raycaster.setFromCamera(clickMouse, camera);
            const intersects = raycaster.intersectObjects(scene.children, true);
            
            for (const hit of intersects) {{
                let obj = hit.object;
                while (obj && !obj.userData.type) obj = obj.parent;
                
                if (obj && obj.userData.type) {{
                    showTooltip(obj, e.clientX, e.clientY);
                    
                    if (obj.userData.isSecret && !foundSecrets.has(obj.userData.secretId)) {{
                        foundSecrets.add(obj.userData.secretId);
                        secretsFound++;
                        document.getElementById('rose-count').textContent = secretsFound;
                        
                        const msg = document.getElementById('secret-msg');
                        msg.style.opacity = 1;
                        setTimeout(() => {{ msg.style.opacity = 0; }}, 2000);
                        
                        const blood = document.getElementById('blood-overlay');
                        blood.style.opacity = 0.4;
                        setTimeout(() => {{ blood.style.opacity = 0; }}, 800);
                    }}
                    return;
                }}
            }}
            hideTooltip();
        }});
        
        // Quotes & Whispers
        const quotes = [
            "The theatre is full tonight...",
            "They have come to witness truth laid bare.",
            "What secrets does the flesh conceal?",
            "The blade reveals what words cannot.",
            "Every cut is a question.",
            "The Society watches. Always.",
            "We are all meat, in the end.",
            "Progress demands sacrifice."
        ];
        
        const whispers = [
            "*The scratch of chalk on slate...*",
            "*A cough echoes in the gallery...*",
            "*Someone breathes too loudly...*",
            "*The gaslights flicker...*",
            "*A woman weeps. Or laughs...*",
            "*You feel eyes upon you...*",
            "*The blade catches the light...*",
            "*Something drips below...*"
        ];
        
        if (INTENSITY >= 4) {{
            whispers.push("*Someone whispered your name...*");
            whispers.push("*The subject's hand twitches...*");
            whispers.push("*'You're next...'*");
        }}
        
        const quoteEl = document.getElementById('quote');
        const whisperEl = document.getElementById('whisper');
        let qIdx = 0, wIdx = 0;
        
        function showQuote() {{
            quoteEl.textContent = '"' + quotes[qIdx] + '"';
            quoteEl.style.opacity = 1;
            setTimeout(() => {{ quoteEl.style.opacity = 0; }}, 5000);
            qIdx = (qIdx + 1) % quotes.length;
        }}
        
        function showWhisper() {{
            whisperEl.textContent = whispers[wIdx];
            whisperEl.style.opacity = 0.8;
            setTimeout(() => {{ whisperEl.style.opacity = 0; }}, 3000);
            wIdx = (wIdx + 1) % whispers.length;
        }}
        
        setTimeout(showQuote, 4000);
        setInterval(showQuote, 18000);
        setTimeout(showWhisper, 8000);
        setInterval(showWhisper, 10000 - INTENSITY * 1000);
        
        // Lightning (Gothic high intensity)
        const lightningEl = document.getElementById('lightning');
        function flash() {{
            if (MODE === 'gothic' && INTENSITY >= 4) {{
                lightningEl.style.opacity = 0.6;
                setTimeout(() => {{ lightningEl.style.opacity = 0; }}, 80);
                setTimeout(() => {{
                    lightningEl.style.opacity = 0.3;
                    setTimeout(() => {{ lightningEl.style.opacity = 0; }}, 50);
                }}, 130);
            }}
        }}
        if (MODE === 'gothic' && INTENSITY >= 4) {{
            setInterval(flash, 12000 + Math.random() * 18000);
        }}
        
        // Animation
        const clock = new THREE.Clock();
        
        function animate() {{
            requestAnimationFrame(animate);
            const t = clock.getElapsedTime();
            
            // Flicker lights
            gaslights.forEach((light, i) => {{
                const f = Math.sin(t * 15 + i * 2.5) * {flicker_intensity} +
                         Math.sin(t * 31 + i * 4) * {flicker_intensity * 0.5};
                light.intensity = {c["light_intensity"] * 0.4} * (1 + f);
                if (glowMeshes[i]) glowMeshes[i].material.opacity = 0.7 + f * 0.3;
            }});
            
            // Particles
            const pos = particles.geometry.attributes.position.array;
            for (let i = 0; i < particleCount; i++) {{
                pos[i * 3 + 1] += particleVel[i];
                pos[i * 3] += Math.sin(t + i) * 0.001;
                if (pos[i * 3 + 1] > 14) pos[i * 3 + 1] = 0;
            }}
            particles.geometry.attributes.position.needsUpdate = true;
            
            // Fog drift
            fogPlanes.forEach((fog, i) => {{
                fog.position.x = Math.sin(t * 0.1 + i) * 2;
                fog.position.z = Math.cos(t * 0.08 + i) * 2;
            }});
            
            // Subject breathing
            if (INTENSITY >= 3) {{
                subjectGroup.children.forEach(child => {{
                    if (child.userData.isChest) {{
                        child.scale.y = 1 + Math.sin(t * 0.8) * 0.025 * CREEP;
                    }}
                }});
            }}
            
            // Anatomist movement
            anatomist.rotation.y = Math.sin(t * 0.3) * 0.04;
            anatomist.children.forEach(child => {{
                if (child.userData.isScalpelHand) {{
                    child.rotation.x = Math.PI/4 + Math.sin(t * 0.5) * 0.08;
                }}
            }});
            
            // Spectators turn heads (creepy)
            if (INTENSITY >= 3) {{
                spectators.forEach((spec, i) => {{
                    const shouldTurn = Math.sin(t * 0.2 + i * 1.5) > 0.7;
                    spec.children.forEach(child => {{
                        if (child.userData.isHead) {{
                            if (shouldTurn && INTENSITY >= 4) {{
                                const targetAngle = Math.atan2(
                                    camera.position.x - spec.position.x,
                                    camera.position.z - spec.position.z
                                ) - spec.rotation.y;
                                child.rotation.y += (targetAngle * 0.4 - child.rotation.y) * 0.02;
                            }} else {{
                                child.rotation.y *= 0.98;
                            }}
                        }}
                    }});
                }});
            }}
            
            // Roses pulse
            roses.forEach((rose, i) => {{
                if (rose.visible) {{
                    rose.children[0].material.opacity = 0.7 + Math.sin(t * 2 + i) * 0.2;
                    rose.rotation.y = t * 0.5 + i;
                }}
            }});
            
            // Auto-rotate
            if (!isDragging) {{
                spherical.theta += 0.0006;
                updateCamera();
            }}
            
            renderer.render(scene, camera);
        }}
        
        // Resize
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
</html>
'''
    return html
