"""
🧪 The Specimen Cabinet — Victorian Medical Collection
Fixed version with proper lighting and hex colors.
"""

def get_cabinet_3d(mode: str = "gaslight", intensity: int = 3) -> str:
    """
    Generate the interactive medical cabinet.
    """
    
    colors = {
        "gaslight": {
            "background": 0x1a1410,
            "wood": 0x5a4530,
            "wood_dark": 0x3c2818,
            "metal": 0xc8a030,
            "light_color": 0xffbb55,
            "text_color": "#d4a574",
            "ambient_intensity": 0.5
        },
        "gothic": {
            "background": 0x0a0505,
            "wood": 0x3a1818,
            "wood_dark": 0x1a0808,
            "metal": 0x5a5a5a,
            "light_color": 0xff4422,
            "text_color": "#cc0000",
            "ambient_intensity": 0.35
        },
        "clinical": {
            "background": 0xe8e8e8,
            "wood": 0xd8d0c8,
            "wood_dark": 0xc0b8b0,
            "metal": 0xbbbbbb,
            "light_color": 0xffffff,
            "text_color": "#2f4f4f",
            "ambient_intensity": 0.7
        }
    }
    
    c = colors.get(mode, colors["gaslight"])
    creep = intensity / 5.0
    
    html = f'''
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,600;1,400&family=Cinzel:wght@400;600&display=swap');
        
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        html, body {{ 
            width: 100%; height: 100%;
            overflow: hidden; 
            background: #{c["background"]:06x};
            font-family: 'EB Garamond', Georgia, serif;
            color: {c["text_color"]};
        }}
        
        #container {{ 
            width: 100%; height: 100%; 
            position: relative;
            cursor: grab;
        }}
        #container:active {{ cursor: grabbing; }}
        
        .ui-overlay {{
            position: absolute;
            pointer-events: none;
            z-index: 100;
        }}
        
        #title {{
            top: 20px;
            left: 50%;
            transform: translateX(-50%);
            font-family: 'Cinzel', serif;
            font-size: 18px;
            letter-spacing: 4px;
            text-transform: uppercase;
            opacity: 0.8;
            text-shadow: 0 2px 10px rgba(0,0,0,0.8);
        }}
        
        #subtitle {{
            top: 48px;
            left: 50%;
            transform: translateX(-50%);
            font-style: italic;
            font-size: 13px;
            opacity: 0.6;
        }}
        
        #info {{
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            font-size: 12px;
            opacity: 0.6;
        }}
        
        #secrets-count {{
            top: 20px;
            right: 20px;
            font-size: 13px;
            opacity: 0.7;
        }}
        
        #bottle-hint {{
            bottom: 60px;
            left: 50%;
            transform: translateX(-50%);
            font-size: 15px;
            opacity: 0;
            transition: opacity 0.3s;
            background: rgba(0,0,0,0.7);
            padding: 8px 16px;
            border-radius: 4px;
        }}
        
        /* Detail Panel */
        #detail-panel {{
            position: absolute;
            top: 0; left: 0;
            width: 100%; height: 100%;
            background: rgba(0,0,0,0.95);
            display: none;
            z-index: 200;
        }}
        
        #detail-panel.visible {{
            display: flex;
        }}
        
        #detail-content {{
            display: flex;
            width: 100%;
            height: 100%;
            padding: 40px;
            gap: 40px;
        }}
        
        #bottle-view {{
            flex: 1;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        
        #bottle-canvas {{
            border: 1px solid {c["text_color"]}33;
        }}
        
        #bottle-info {{
            flex: 1;
            display: flex;
            flex-direction: column;
            justify-content: center;
            max-width: 450px;
        }}
        
        #bottle-name {{
            font-family: 'Cinzel', serif;
            font-size: 28px;
            margin-bottom: 8px;
        }}
        
        #bottle-subtitle {{
            font-style: italic;
            font-size: 14px;
            opacity: 0.6;
            margin-bottom: 24px;
            padding-bottom: 16px;
            border-bottom: 1px solid {c["text_color"]}33;
        }}
        
        #bottle-description {{
            font-size: 16px;
            line-height: 1.7;
            margin-bottom: 20px;
        }}
        
        #bottle-contents {{
            font-size: 14px;
            opacity: 0.85;
            margin-bottom: 20px;
            padding: 14px;
            background: rgba(255,255,255,0.05);
            border-left: 3px solid {c["text_color"]}44;
        }}
        
        #bottle-warning {{
            display: inline-block;
            padding: 6px 14px;
            background: #442200;
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 2px;
        }}
        
        #bottle-secret {{
            font-style: italic;
            font-size: 15px;
            color: #cc4444;
            margin-top: 20px;
            padding-top: 16px;
            border-top: 1px solid {c["text_color"]}22;
            opacity: 0;
            transition: opacity 1.5s;
        }}
        
        #bottle-secret.revealed {{ opacity: 1; }}
        
        #close-detail {{
            position: absolute;
            top: 25px; right: 30px;
            font-size: 36px;
            cursor: pointer;
            opacity: 0.6;
            transition: opacity 0.3s;
            z-index: 210;
        }}
        #close-detail:hover {{ opacity: 1; }}
        
        #detail-actions {{
            display: flex;
            gap: 12px;
            margin-top: 24px;
        }}
        
        .detail-btn {{
            padding: 10px 20px;
            background: transparent;
            border: 1px solid {c["text_color"]}55;
            color: {c["text_color"]};
            font-family: 'EB Garamond', serif;
            font-size: 14px;
            cursor: pointer;
            transition: all 0.3s;
        }}
        .detail-btn:hover {{
            background: {c["text_color"]}22;
        }}
        
        #whisper {{
            position: absolute;
            top: 50%; left: 50%;
            transform: translate(-50%, -50%);
            font-style: italic;
            font-size: 16px;
            opacity: 0;
            transition: opacity 1.5s;
            pointer-events: none;
            text-align: center;
            z-index: 150;
        }}
        
        .vignette {{
            position: absolute;
            top: 0; left: 0;
            width: 100%; height: 100%;
            pointer-events: none;
            background: radial-gradient(ellipse at center, 
                transparent 50%, 
                rgba(0,0,0,{0.5 if mode != 'clinical' else 0.15}) 100%);
            z-index: 50;
        }}
        
        #secret-flash {{
            position: absolute;
            top: 50%; left: 50%;
            transform: translate(-50%, -50%);
            font-family: 'Cinzel', serif;
            font-size: 14px;
            text-transform: uppercase;
            letter-spacing: 4px;
            color: #cc0000;
            opacity: 0;
            transition: opacity 0.5s;
            z-index: 250;
            text-shadow: 0 0 20px rgba(200,0,0,0.8);
        }}
    </style>
</head>
<body>
    <div id="container"></div>
    <div class="vignette"></div>
    
    <div id="title" class="ui-overlay">The Fitzroy Collection</div>
    <div id="subtitle" class="ui-overlay">Private Medical Cabinet — St. Bartholomew's, 1889</div>
    <div id="info" class="ui-overlay">Drag to rotate | Scroll to zoom | Click bottles to examine</div>
    <div id="secrets-count" class="ui-overlay">Secrets: <span id="secret-num">0</span>/8</div>
    <div id="bottle-hint" class="ui-overlay"></div>
    <div id="whisper" class="ui-overlay"></div>
    <div id="secret-flash">Secret Discovered</div>
    
    <!-- Detail Panel -->
    <div id="detail-panel">
        <div id="close-detail">×</div>
        <div id="detail-content">
            <div id="bottle-view">
                <canvas id="bottle-canvas" width="350" height="450"></canvas>
            </div>
            <div id="bottle-info">
                <div id="bottle-name"></div>
                <div id="bottle-subtitle"></div>
                <div id="bottle-description"></div>
                <div id="bottle-contents"></div>
                <div id="bottle-warning"></div>
                <div id="bottle-secret"></div>
                <div id="detail-actions">
                    <button class="detail-btn" id="btn-shake">Shake</button>
                    <button class="detail-btn" id="btn-open">Open</button>
                </div>
            </div>
        </div>
    </div>
    
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script>
    (function() {{
        'use strict';
        
        const MODE = '{mode}';
        const INTENSITY = {intensity};
        const CREEP = {creep};
        
        let secretsFound = 0;
        const foundSecrets = new Set();
        
        // ==========================================
        // BOTTLE DATA
        // ==========================================
        
        const BOTTLES = [
            // Row 0: Medicines
            {{
                id: 'laudanum', name: 'Laudanum', subtitle: 'Tincture of Opium',
                color: 0xcc8844, liquidColor: 0x553311, liquidLevel: 0.6, row: 0, slot: 0,
                description: 'A powerful preparation of opium dissolved in alcohol. Prescribed for pain, coughs, and "women\'s complaints."',
                contents: 'Opium and alcohol. This bottle is nearly half empty.',
                warning: 'HIGHLY ADDICTIVE',
                secret: 'Margin note: "Mrs. Harrison — increase to 40 drops. She asks too many questions."',
                hasSecret: true
            }},
            {{
                id: 'chloroform', name: 'Chloroform', subtitle: 'Anesthetic',
                color: 0x4466bb, liquidColor: 0xccddff, liquidLevel: 0.25, row: 0, slot: 1,
                description: 'A volatile anesthetic that revolutionized surgery—and enabled darker purposes.',
                contents: 'Trichloromethane. Nearly empty. Recently used.',
                warning: 'POISON — HANDLE WITH CARE',
                secret: 'Fingerprints in dust suggest frequent use. But no surgeries are scheduled.',
                hasSecret: INTENSITY >= 3
            }},
            {{
                id: 'soothing_syrup', name: 'Mrs. Winslow\\'s Soothing Syrup', subtitle: 'For Infants',
                color: 0xeeddbb, liquidColor: 0x997755, liquidLevel: 0.75, row: 0, slot: 2,
                description: 'A "soothing" syrup for fussy babies. The cheerful label shows a sleeping infant.',
                contents: 'Morphine sulphate and alcohol. Some children never woke.',
                warning: 'EXTERNAL USE ONLY',
                secret: 'The dosage is TEN TIMES the normal amount. This was compounded specially.',
                hasSecret: INTENSITY >= 2
            }},
            {{
                id: 'mercury', name: 'Mercury Bichloride', subtitle: 'Blue Mass',
                color: 0x334455, liquidColor: 0x99aaaa, liquidLevel: 0.5, row: 0, slot: 3,
                description: 'Standard treatment for syphilis. Also causes madness and death.',
                contents: 'Mercuric chloride. The liquid has a silver shimmer.',
                warning: 'TOXIC — PHYSICIAN ONLY',
                secret: 'A list of names tucked behind the label. Society members? Victims?',
                hasSecret: INTENSITY >= 4
            }},
            {{
                id: 'arsenic', name: 'Arsenic Complexion Wafers', subtitle: 'Beautifier',
                color: 0x88aa77, liquidColor: 0xcceecc, liquidLevel: 0.65, row: 0, slot: 4,
                description: 'For that fashionable pale complexion. Women ate these daily.',
                contents: 'Arsenic trioxide in sugar. Sweet-tasting death.',
                warning: 'TAKE AS DIRECTED',
                secret: 'Why does a male anatomist keep these? Unless they serve another purpose...',
                hasSecret: INTENSITY >= 3
            }},
            
            // Row 1: Surgical
            {{
                id: 'ether', name: 'Diethyl Ether', subtitle: 'Surgical Anesthetic',
                color: 0x775533, liquidColor: 0xffeedd, liquidLevel: 0.35, row: 1, slot: 0,
                description: 'Patients sleep through the knife. But sometimes they wake during.',
                contents: 'Pure ether. Highly flammable.',
                warning: 'FLAMMABLE — NO OPEN FLAME',
                secret: 'Scratches on the inside of the lid. As if someone tried to open it from within.',
                hasSecret: INTENSITY >= 5
            }},
            {{
                id: 'cocaine', name: 'Cocaine Solution 4%', subtitle: 'Local Anesthetic',
                color: 0xeeeeff, liquidColor: 0xffffff, liquidLevel: 0.12, row: 1, slot: 1,
                description: 'Revolutionary anesthetic. Also improves the surgeon\\'s confidence.',
                contents: 'Nearly empty. Someone has been using this frequently.',
                warning: 'MEDICINAL USE ONLY',
                secret: 'Fitzroy\\'s personal supply. Daily use. His hands never shake during demonstrations.',
                hasSecret: true
            }},
            {{
                id: 'strychnine', name: 'Strychnine Tonic', subtitle: 'Nerve Stimulant',
                color: 0xdd3333, liquidColor: 0xffcccc, liquidLevel: 0.5, row: 1, slot: 2,
                description: 'A "tonic" that stimulates nerves. In larger doses: death by convulsions.',
                contents: 'Strychnine in alcohol. The red label serves as warning.',
                warning: 'POISON — MEASURED DOSES',
                secret: 'Dosage guidelines scratched out. The new dose would be lethal.',
                hasSecret: INTENSITY >= 4
            }},
            {{
                id: 'carbolic', name: 'Carbolic Acid', subtitle: 'Antiseptic',
                color: 0x4455aa, liquidColor: 0xeeeedd, liquidLevel: 0.7, row: 1, slot: 3,
                description: 'Lister\\'s miracle—kills infection. Also destroys evidence.',
                contents: 'Phenol solution. Burns organic matter on contact.',
                warning: 'CORROSIVE',
                secret: 'Blood on the cap. And hair. Human hair.',
                hasSecret: INTENSITY >= 4
            }},
            {{
                id: 'embalming', name: 'Embalming Fluid', subtitle: 'Preservation',
                color: 0x888866, liquidColor: 0xccccaa, liquidLevel: 0.85, row: 1, slot: 4,
                description: 'Formaldehyde for preserving specimens. An anatomist\\'s tool.',
                contents: 'An unusually large supply.',
                warning: 'TOXIC FUMES',
                secret: 'Why so much? The hospital provides this. Unless specimens are prepared elsewhere...',
                hasSecret: INTENSITY >= 3
            }},
            
            // Row 2: Society Collection
            {{
                id: 'vita_aeterna', name: 'Vita Aeterna', subtitle: 'The Eternal Essence',
                color: 0x880022, liquidColor: 0xaa0000, liquidLevel: 0.55, row: 2, slot: 0,
                special: 'swirl',
                description: 'The Society\\'s communion wine. It swirls without being touched.',
                contents: 'Unknown. Too red for wine. It moves on its own.',
                warning: 'FOR MEMBERS ONLY',
                secret: '"Sanguis innocentum" — Blood of the innocent. This is not wine.',
                hasSecret: true
            }},
            {{
                id: 'unmarked', name: 'Bottle #7', subtitle: 'Unmarked',
                color: 0x666666, liquidColor: 0xeeeeee, liquidLevel: 0.5, row: 2, slot: 1,
                description: 'No label. Cloudy white liquid. Faint smell of almonds.',
                contents: 'Unknown. But bitter almonds indicate... cyanide.',
                warning: 'DO NOT OPEN',
                secret: 'Potassium cyanide. Enough to kill a hundred people.',
                hasSecret: INTENSITY >= 3
            }},
            {{
                id: 'unwilling', name: '"For the Unwilling"', subtitle: 'Special Preparation',
                color: 0x111111, liquidColor: 0x332244, liquidLevel: 0.7, row: 2, slot: 2,
                description: 'Black glass. Handwritten label. The Society uses this when subjects resist.',
                contents: 'Chloral hydrate and morphine. Immediate unconsciousness.',
                warning: 'SOCIETY USE ONLY',
                secret: '12 "donations" this year. Not one voluntary. This made them compliant.',
                hasSecret: true
            }},
            {{
                id: 'final_mercy', name: '"Final Mercy"', subtitle: 'Terminal',
                color: 0xaa0000, liquidColor: 0x220000, liquidLevel: 0.9, row: 2, slot: 3,
                description: 'A tiny vial with red skull. For when subjects suffer too long.',
                contents: 'Concentrated morphine and potassium chloride. Death in seconds.',
                warning: 'EMERGENCY USE',
                secret: 'Three doses missing since January. Three hearts that "simply gave out."',
                hasSecret: INTENSITY >= 4
            }},
            {{
                id: 'blood_sc', name: 'Blood Sample — S.C.', subtitle: 'Specimen',
                color: 0xdddddd, liquidColor: 0x660000, liquidLevel: 0.6, row: 2, slot: 4,
                description: 'A test tube with preserved blood. Initials: S.C.',
                contents: 'Human blood in citrate solution. Still viable.',
                warning: 'DO NOT DISCARD',
                secret: 'S.C. — Sebastian Carlisle. Why is Fitzroy keeping his protégé\\'s blood?',
                hasSecret: true
            }},
            
            // Row 3: Curiosities
            {{
                id: 'teeth', name: 'Dental Collection', subtitle: 'Human Teeth',
                color: 0xffffdd, liquidColor: 0xffffcc, liquidLevel: 0.8, row: 3, slot: 0,
                hasParticles: true,
                description: 'A wide jar of teeth in alcohol. 47 teeth. From how many patients?',
                contents: 'The variety suggests at least a dozen sources.',
                warning: 'ANATOMICAL SPECIMEN',
                secret: 'Some show extraction marks from the living. These weren\\'t from corpses.',
                hasSecret: INTENSITY >= 3
            }},
            {{
                id: 'leeches', name: 'Medicinal Leeches', subtitle: 'Live Specimens',
                color: 0xccffcc, liquidColor: 0xaaddaa, liquidLevel: 0.7, row: 3, slot: 1,
                special: 'leeches',
                description: 'Living leeches for bloodletting. They press against the glass, sensing you.',
                contents: 'A dozen hungry leeches. They follow your movement.',
                warning: 'LIVE SPECIMENS',
                secret: 'Why so large? What have they been feeding on? The hospital stopped using leeches years ago.',
                hasSecret: INTENSITY >= 2
            }},
            {{
                id: 'essence', name: '"Essence of Youth"', subtitle: 'Rejuvenation',
                color: 0xddccbb, liquidColor: 0xffffdd, liquidLevel: 0.6, row: 3, slot: 2,
                description: 'A ceramic pot. Waxy, pale substance. Smells of rendered fat.',
                contents: 'Unknown fatty compound. Applied to skin, softens wrinkles.',
                warning: 'EXTERNAL USE ONLY',
                secret: 'Human fat. Rendered from surgical "waste." Made from the poor. Sold to the rich.',
                hasSecret: INTENSITY >= 4
            }},
            {{
                id: 'tapeworm', name: 'Sanitized Tapeworm', subtitle: 'Diet Aid',
                color: 0xeeeedd, liquidColor: 0xffffee, liquidLevel: 0.7, row: 3, slot: 3,
                hasParticles: true,
                description: 'Tapeworm segments. Victorians swallowed these to lose weight.',
                contents: 'Taenia segments. A "natural" weight loss solution.',
                warning: 'NOT FOR CONSUMPTION',
                secret: 'Far more segments than one worm produces. Someone is farming these.',
                hasSecret: INTENSITY >= 3
            }},
            {{
                id: 'brain_tonic', name: 'Dr. Hammond\\'s Nerve Food', subtitle: 'For Weakness of Mind',
                color: 0xbbaa88, liquidColor: 0xccbbaa, liquidLevel: 0.5, row: 3, slot: 4,
                description: 'Gray fibrous matter floating in yellowed fluid. Promises mental restoration.',
                contents: 'Preserved brain tissue. "Transfers mental energy when consumed."',
                warning: 'TAKE TWICE DAILY',
                secret: '"Brain matter from subjects of superior intellect." Cannibalism dressed as cure.',
                hasSecret: true
            }}
        ];
        
        // ==========================================
        // THREE.JS SETUP
        // ==========================================
        
        const container = document.getElementById('container');
        const width = container.clientWidth || window.innerWidth;
        const height = container.clientHeight || window.innerHeight;
        
        const scene = new THREE.Scene();
        scene.background = new THREE.Color({c["background"]});
        
        const camera = new THREE.PerspectiveCamera(50, width / height, 0.1, 100);
        camera.position.set(0, 1.5, 6);
        camera.lookAt(0, 1.2, 0);
        
        const renderer = new THREE.WebGLRenderer({{ antialias: true }});
        renderer.setSize(width, height);
        renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        renderer.shadowMap.enabled = true;
        container.appendChild(renderer.domElement);
        
        const raycaster = new THREE.Raycaster();
        const mouse = new THREE.Vector2();
        
        // ==========================================
        // STRONG LIGHTING
        // ==========================================
        
        // Ambient
        const ambient = new THREE.AmbientLight(0xffffff, {c["ambient_intensity"]});
        scene.add(ambient);
        
        // Hemisphere
        const hemi = new THREE.HemisphereLight(0xffffff, {c["wood_dark"]}, 0.4);
        scene.add(hemi);
        
        // Key light
        const keyLight = new THREE.DirectionalLight({c["light_color"]}, 1.0);
        keyLight.position.set(3, 5, 4);
        keyLight.castShadow = true;
        scene.add(keyLight);
        
        // Fill light
        const fillLight = new THREE.PointLight({c["light_color"]}, 0.6);
        fillLight.position.set(-3, 3, 3);
        scene.add(fillLight);
        
        // Back light
        const backLight = new THREE.PointLight({c["light_color"]}, 0.3);
        backLight.position.set(0, 2, -3);
        scene.add(backLight);
        
        // ==========================================
        // MATERIALS
        // ==========================================
        
        const woodMat = new THREE.MeshLambertMaterial({{ color: {c["wood"]} }});
        const darkWoodMat = new THREE.MeshLambertMaterial({{ color: {c["wood_dark"]} }});
        const metalMat = new THREE.MeshLambertMaterial({{ color: {c["metal"]} }});
        
        // ==========================================
        // CABINET
        // ==========================================
        
        const cabinet = new THREE.Group();
        
        const W = 4, H = 3.2, D = 0.7;
        const SHELVES = 4;
        const SHELF_H = H / SHELVES;
        
        // Back
        const back = new THREE.Mesh(
            new THREE.BoxGeometry(W, H, 0.05),
            darkWoodMat
        );
        back.position.set(0, H/2, -D/2);
        cabinet.add(back);
        
        // Sides
        [-1, 1].forEach(s => {{
            const side = new THREE.Mesh(
                new THREE.BoxGeometry(0.08, H, D),
                woodMat
            );
            side.position.set(s * W/2, H/2, 0);
            cabinet.add(side);
        }});
        
        // Top
        const top = new THREE.Mesh(
            new THREE.BoxGeometry(W + 0.1, 0.1, D + 0.1),
            woodMat
        );
        top.position.set(0, H + 0.05, 0);
        cabinet.add(top);
        
        // Crown
        const crown = new THREE.Mesh(
            new THREE.BoxGeometry(W + 0.15, 0.12, 0.12),
            woodMat
        );
        crown.position.set(0, H + 0.12, D/2 - 0.05);
        cabinet.add(crown);
        
        // Shelves
        for (let i = 0; i <= SHELVES; i++) {{
            const shelf = new THREE.Mesh(
                new THREE.BoxGeometry(W - 0.1, 0.04, D - 0.08),
                woodMat
            );
            shelf.position.set(0, i * SHELF_H, 0);
            shelf.receiveShadow = true;
            cabinet.add(shelf);
        }}
        
        // Columns
        [-1, 1].forEach(s => {{
            const col = new THREE.Mesh(
                new THREE.CylinderGeometry(0.04, 0.05, H, 8),
                metalMat
            );
            col.position.set(s * (W/2 - 0.12), H/2, D/2 - 0.08);
            cabinet.add(col);
        }});
        
        scene.add(cabinet);
        
        // ==========================================
        // BOTTLES
        // ==========================================
        
        const bottleObjects = [];
        
        function getSlotPos(row, slot) {{
            const startX = -W/2 + 0.45;
            const spacing = (W - 0.9) / 4;
            return {{
                x: startX + slot * spacing,
                y: row * SHELF_H + 0.18,
                z: 0
            }};
        }}
        
        BOTTLES.forEach(b => {{
            const group = new THREE.Group();
            
            // Glass bottle
            const glassGeo = new THREE.CylinderGeometry(0.08, 0.09, 0.32, 12);
            const glassMat = new THREE.MeshLambertMaterial({{
                color: b.color,
                transparent: true,
                opacity: 0.65
            }});
            const glass = new THREE.Mesh(glassGeo, glassMat);
            group.add(glass);
            
            // Liquid
            const liqH = 0.28 * b.liquidLevel;
            const liqGeo = new THREE.CylinderGeometry(0.065, 0.075, liqH, 12);
            const liqMat = new THREE.MeshLambertMaterial({{
                color: b.liquidColor,
                transparent: true,
                opacity: 0.85
            }});
            const liquid = new THREE.Mesh(liqGeo, liqMat);
            liquid.position.y = -0.14 + liqH/2 + 0.02;
            group.add(liquid);
            
            // Cork
            const cork = new THREE.Mesh(
                new THREE.CylinderGeometry(0.035, 0.04, 0.05, 8),
                new THREE.MeshLambertMaterial({{ color: 0x8b7355 }})
            );
            cork.position.y = 0.18;
            group.add(cork);
            
            // Label
            const label = new THREE.Mesh(
                new THREE.PlaneGeometry(0.1, 0.08),
                new THREE.MeshLambertMaterial({{ color: 0xffffee, side: THREE.DoubleSide }})
            );
            label.position.set(0, 0, 0.085);
            group.add(label);
            
            // Position
            const pos = getSlotPos(b.row, b.slot);
            group.position.set(pos.x, pos.y, pos.z);
            
            group.userData = b;
            cabinet.add(group);
            bottleObjects.push(group);
        }});
        
        // ==========================================
        // DUST PARTICLES
        // ==========================================
        
        const dustCount = 80;
        const dustGeo = new THREE.BufferGeometry();
        const dustPos = new Float32Array(dustCount * 3);
        
        for (let i = 0; i < dustCount; i++) {{
            dustPos[i*3] = (Math.random() - 0.5) * 5;
            dustPos[i*3+1] = Math.random() * 3.5;
            dustPos[i*3+2] = (Math.random() - 0.5) * 2;
        }}
        
        dustGeo.setAttribute('position', new THREE.BufferAttribute(dustPos, 3));
        const dust = new THREE.Points(dustGeo, new THREE.PointsMaterial({{
            color: {c["light_color"]},
            size: 0.02,
            transparent: true,
            opacity: 0.5
        }}));
        scene.add(dust);
        
        // ==========================================
        // CAMERA CONTROLS
        // ==========================================
        
        let isDragging = false;
        let prevMouse = {{ x: 0, y: 0 }};
        let camAngle = {{ theta: 0, phi: 1.2 }};
        let camDist = 6;
        const camTarget = new THREE.Vector3(0, 1.3, 0);
        
        function updateCam() {{
            camera.position.x = camTarget.x + camDist * Math.sin(camAngle.phi) * Math.sin(camAngle.theta);
            camera.position.y = camTarget.y + camDist * Math.cos(camAngle.phi);
            camera.position.z = camTarget.z + camDist * Math.sin(camAngle.phi) * Math.cos(camAngle.theta);
            camera.lookAt(camTarget);
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
                camAngle.theta += dx * 0.005;
                camAngle.phi = Math.max(0.5, Math.min(1.4, camAngle.phi + dy * 0.005));
                prevMouse = {{ x: e.clientX, y: e.clientY }};
                updateCam();
            }}
        }});
        
        window.addEventListener('mouseup', () => isDragging = false);
        
        renderer.domElement.addEventListener('wheel', e => {{
            e.preventDefault();
            camDist = Math.max(3.5, Math.min(10, camDist + e.deltaY * 0.005));
            updateCam();
        }}, {{ passive: false }});
        
        // Touch
        renderer.domElement.addEventListener('touchstart', e => {{
            if (e.touches.length === 1) {{
                isDragging = true;
                prevMouse = {{ x: e.touches[0].clientX, y: e.touches[0].clientY }};
            }}
        }});
        renderer.domElement.addEventListener('touchmove', e => {{
            if (isDragging && e.touches.length === 1) {{
                const dx = e.touches[0].clientX - prevMouse.x;
                const dy = e.touches[0].clientY - prevMouse.y;
                camAngle.theta += dx * 0.005;
                camAngle.phi = Math.max(0.5, Math.min(1.4, camAngle.phi + dy * 0.005));
                prevMouse = {{ x: e.touches[0].clientX, y: e.touches[0].clientY }};
                updateCam();
            }}
        }});
        renderer.domElement.addEventListener('touchend', () => isDragging = false);
        
        updateCam();
        
        // ==========================================
        // CLICK / DETAIL PANEL
        // ==========================================
        
        let selectedBottle = null;
        const detailPanel = document.getElementById('detail-panel');
        
        function showDetail(b) {{
            selectedBottle = b;
            document.getElementById('bottle-name').textContent = b.name;
            document.getElementById('bottle-subtitle').textContent = b.subtitle;
            document.getElementById('bottle-description').textContent = b.description;
            document.getElementById('bottle-contents').textContent = b.contents;
            document.getElementById('bottle-warning').textContent = '⚠ ' + b.warning;
            
            const secretEl = document.getElementById('bottle-secret');
            secretEl.classList.remove('revealed');
            
            if (b.hasSecret && b.secret) {{
                secretEl.textContent = '🔍 ' + b.secret;
                setTimeout(() => {{
                    secretEl.classList.add('revealed');
                    if (!foundSecrets.has(b.id)) {{
                        foundSecrets.add(b.id);
                        secretsFound++;
                        document.getElementById('secret-num').textContent = secretsFound;
                        document.getElementById('secret-flash').style.opacity = 1;
                        setTimeout(() => document.getElementById('secret-flash').style.opacity = 0, 2000);
                    }}
                }}, 1200);
            }} else {{
                secretEl.textContent = '';
            }}
            
            detailPanel.classList.add('visible');
            draw2D(b);
        }}
        
        document.getElementById('close-detail').onclick = () => {{
            detailPanel.classList.remove('visible');
            selectedBottle = null;
        }};
        
        renderer.domElement.addEventListener('click', e => {{
            if (isDragging) return;
            
            const clickMouse = new THREE.Vector2(
                (e.clientX / window.innerWidth) * 2 - 1,
                -(e.clientY / window.innerHeight) * 2 + 1
            );
            
            raycaster.setFromCamera(clickMouse, camera);
            const hits = raycaster.intersectObjects(bottleObjects, true);
            
            if (hits.length > 0) {{
                let obj = hits[0].object;
                while (obj && !obj.userData.id) obj = obj.parent;
                if (obj && obj.userData.id) showDetail(obj.userData);
            }}
        }});
        
        // ==========================================
        // 2D BOTTLE VIEW
        // ==========================================
        
        const canvas2D = document.getElementById('bottle-canvas');
        const ctx = canvas2D.getContext('2d');
        let liquidWave = 0;
        let isShaking = false;
        
        function draw2D(b) {{
            const w = canvas2D.width, h = canvas2D.height;
            const cx = w/2, cy = h/2;
            
            ctx.clearRect(0, 0, w, h);
            
            ctx.save();
            ctx.translate(cx, cy);
            if (isShaking) ctx.rotate(Math.sin(liquidWave * 3) * 0.1);
            
            const bW = 90, bH = 220;
            
            // Glass
            ctx.fillStyle = '#' + b.color.toString(16).padStart(6, '0') + '99';
            ctx.strokeStyle = '#' + b.color.toString(16).padStart(6, '0');
            ctx.lineWidth = 3;
            ctx.beginPath();
            ctx.roundRect(-bW/2, -bH/2, bW, bH, 10);
            ctx.fill();
            ctx.stroke();
            
            // Liquid
            const liqH = bH * b.liquidLevel * 0.85;
            const liqY = bH/2 - liqH - 12;
            
            ctx.fillStyle = '#' + b.liquidColor.toString(16).padStart(6, '0') + 'dd';
            ctx.beginPath();
            ctx.moveTo(-bW/2 + 10, liqY + Math.sin(liquidWave) * 4);
            for (let x = -bW/2 + 10; x <= bW/2 - 10; x += 6) {{
                ctx.lineTo(x, liqY + Math.sin(liquidWave + x * 0.08) * 4);
            }}
            ctx.lineTo(bW/2 - 10, bH/2 - 12);
            ctx.lineTo(-bW/2 + 10, bH/2 - 12);
            ctx.closePath();
            ctx.fill();
            
            // Leeches
            if (b.special === 'leeches') {{
                ctx.fillStyle = '#2a3a2a';
                for (let i = 0; i < 5; i++) {{
                    const lx = Math.sin(liquidWave * 0.5 + i * 2) * 28;
                    const ly = liqY + 35 + Math.cos(liquidWave * 0.3 + i * 3) * 25;
                    ctx.beginPath();
                    ctx.ellipse(lx, ly, 10, 5, Math.sin(liquidWave + i) * 0.5, 0, Math.PI * 2);
                    ctx.fill();
                }}
            }}
            
            // Swirl
            if (b.special === 'swirl') {{
                ctx.strokeStyle = 'rgba(255,50,50,0.4)';
                ctx.lineWidth = 3;
                for (let i = 0; i < 3; i++) {{
                    ctx.beginPath();
                    ctx.arc(
                        Math.sin(liquidWave + i) * 18,
                        liqY + 50 + i * 22,
                        12 + i * 6,
                        liquidWave + i,
                        liquidWave + i + Math.PI
                    );
                    ctx.stroke();
                }}
            }}
            
            // Cork
            ctx.fillStyle = '#8b7355';
            ctx.fillRect(-18, -bH/2 - 24, 36, 28);
            
            // Label
            ctx.fillStyle = '#ffffee';
            ctx.fillRect(-38, -25, 76, 55);
            ctx.strokeStyle = '#8b7355';
            ctx.lineWidth = 1;
            ctx.strokeRect(-38, -25, 76, 55);
            
            ctx.fillStyle = '#333';
            ctx.font = '12px Georgia';
            ctx.textAlign = 'center';
            ctx.fillText(b.name, 0, 0);
            ctx.font = '9px Georgia';
            ctx.fillText(b.subtitle, 0, 16);
            
            ctx.restore();
        }}
        
        // Button handlers
        document.getElementById('btn-shake').onclick = () => {{
            isShaking = true;
            setTimeout(() => isShaking = false, 1000);
        }};
        
        document.getElementById('btn-open').onclick = () => {{
            if (!selectedBottle) return;
            const scents = {{
                'laudanum': 'Bitter medicine and alcohol...',
                'chloroform': 'Sweet, almost pleasant. Dangerously so.',
                'cocaine': 'Slight chemical tingle.',
                'unmarked': 'Bitter almonds. Step back.',
                'vita_aeterna': 'Iron. Salt. Something ancient.',
                'embalming': 'Sharp formaldehyde burns your nostrils.',
                'leeches': 'Stagnant water and organic decay.',
                'brain_tonic': 'Formaldehyde and something worse.'
            }};
            const hint = document.getElementById('bottle-hint');
            hint.textContent = scents[selectedBottle.id] || 'A faint chemical odor...';
            hint.style.opacity = 1;
            setTimeout(() => hint.style.opacity = 0, 3000);
        }};
        
        // ==========================================
        // WHISPERS
        // ==========================================
        
        const whispers = [
            '*Glass clinks softly...*',
            '*Something shifts on a shelf...*',
            '*The liquid seems to move...*',
            '*You hear breathing.*',
            '*A label peels at the corner...*',
            '*The leeches press against glass...*'
        ];
        if (INTENSITY >= 4) {{
            whispers.push('*A face in the reflection...*');
            whispers.push('*"Take one," a voice suggests.*');
        }}
        
        const whisperEl = document.getElementById('whisper');
        let wIdx = 0;
        
        function showWhisper() {{
            whisperEl.textContent = whispers[wIdx];
            whisperEl.style.opacity = 0.8;
            setTimeout(() => whisperEl.style.opacity = 0, 4000);
            wIdx = (wIdx + 1) % whispers.length;
        }}
        
        setTimeout(showWhisper, 5000);
        setInterval(showWhisper, 12000);
        
        // ==========================================
        // ANIMATION
        // ==========================================
        
        const clock = new THREE.Clock();
        
        function animate() {{
            requestAnimationFrame(animate);
            const t = clock.getElapsedTime();
            
            // Dust
            const dPos = dust.geometry.attributes.position.array;
            for (let i = 0; i < dustCount; i++) {{
                dPos[i*3+1] += 0.002;
                dPos[i*3] += Math.sin(t + i) * 0.0008;
                if (dPos[i*3+1] > 3.5) dPos[i*3+1] = 0;
            }}
            dust.geometry.attributes.position.needsUpdate = true;
            
            // Light flicker
            keyLight.intensity = 1.0 + Math.sin(t * 8) * 0.08;
            
            // Bottle hover
            raycaster.setFromCamera(mouse, camera);
            const hits = raycaster.intersectObjects(bottleObjects, true);
            
            bottleObjects.forEach(b => {{
                b.children[0].material.emissive = new THREE.Color(0x000000);
            }});
            
            const hint = document.getElementById('bottle-hint');
            if (hits.length > 0 && !detailPanel.classList.contains('visible')) {{
                let obj = hits[0].object;
                while (obj && !obj.userData.id) obj = obj.parent;
                if (obj) {{
                    obj.children[0].material.emissive = new THREE.Color({c["light_color"]});
                    obj.children[0].material.emissiveIntensity = 0.2;
                    hint.textContent = obj.userData.name;
                    hint.style.opacity = 1;
                }}
            }} else if (!detailPanel.classList.contains('visible')) {{
                hint.style.opacity = 0;
            }}
            
            // 2D animation
            liquidWave += isShaking ? 0.4 : 0.025;
            if (selectedBottle) draw2D(selectedBottle);
            
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
