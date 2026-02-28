"""
🧪 The Specimen Cabinet — Victorian Medical Collection
An interactive curiosity cabinet from Dr. Alistair Fitzroy's private collection.
Features 3D bottle display with 2D detail inspection.
"""

def get_cabinet_3d(mode: str = "gaslight", intensity: int = 3) -> str:
    """
    Generate the interactive medical cabinet.
    
    Args:
        mode: Visual mode (gaslight, gothic, clinical)
        intensity: Atmosphere intensity 1-5
    """
    
    colors = {
        "gaslight": {
            "background": 0x1a1410,
            "wood": 0x4a3520,
            "wood_dark": 0x2c1810,
            "metal": 0xb8860b,
            "light_color": 0xffaa44,
            "text_color": "#d4a574",
            "glass_tint": "0xffffee",
            "ambient": 0.4
        },
        "gothic": {
            "background": 0x0a0505,
            "wood": 0x2a1515,
            "wood_dark": 0x1a0808,
            "metal": 0x4a4a4a,
            "light_color": 0xff4422,
            "text_color": "#cc0000",
            "glass_tint": "0xffcccc",
            "ambient": 0.25
        },
        "clinical": {
            "background": 0xf5f5f5,
            "wood": 0xe8e0d8,
            "wood_dark": 0xd0c8c0,
            "metal": 0xcccccc,
            "light_color": 0xffffff,
            "text_color": "#2f4f4f",
            "glass_tint": "0xffffff",
            "ambient": 0.6
        }
    }
    
    c = colors.get(mode, colors["gaslight"])
    creep = intensity / 5.0
    
    def to_hex(val):
        return f"0x{val:06x}"
    
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
            opacity: 0.7;
            text-shadow: 0 0 20px rgba(0,0,0,0.8);
        }}
        
        #subtitle {{
            top: 48px;
            left: 50%;
            transform: translateX(-50%);
            font-style: italic;
            font-size: 13px;
            opacity: 0.5;
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
            font-style: italic;
            font-size: 14px;
            opacity: 0;
            transition: opacity 0.5s;
        }}
        
        /* Detail Panel */
        #detail-panel {{
            position: absolute;
            top: 0; left: 0;
            width: 100%; height: 100%;
            background: rgba(0,0,0,0.95);
            display: none;
            z-index: 200;
            opacity: 0;
            transition: opacity 0.4s;
        }}
        
        #detail-panel.visible {{
            display: flex;
            opacity: 1;
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
            position: relative;
        }}
        
        #bottle-canvas {{
            max-width: 100%;
            max-height: 100%;
        }}
        
        #bottle-info {{
            flex: 1;
            display: flex;
            flex-direction: column;
            justify-content: center;
            padding: 20px;
            max-width: 450px;
        }}
        
        #bottle-name {{
            font-family: 'Cinzel', serif;
            font-size: 28px;
            margin-bottom: 8px;
            color: {c["text_color"]};
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
            margin-bottom: 24px;
        }}
        
        #bottle-contents {{
            font-size: 14px;
            opacity: 0.8;
            margin-bottom: 24px;
            padding: 16px;
            background: rgba(255,255,255,0.03);
            border-left: 3px solid {c["text_color"]}44;
        }}
        
        #bottle-secret {{
            font-style: italic;
            font-size: 15px;
            color: {'#cc0000' if mode == 'gothic' else '#8b0000'};
            margin-top: 16px;
            padding-top: 16px;
            border-top: 1px solid {c["text_color"]}22;
            opacity: 0;
            transition: opacity 1s;
        }}
        
        #bottle-secret.revealed {{
            opacity: 1;
        }}
        
        #bottle-warning {{
            display: inline-block;
            padding: 4px 12px;
            background: {'#440000' if mode == 'gothic' else '#4a3520'};
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 2px;
            margin-top: 20px;
            opacity: 0.8;
        }}
        
        #close-detail {{
            position: absolute;
            top: 30px;
            right: 30px;
            font-size: 32px;
            cursor: pointer;
            opacity: 0.5;
            transition: opacity 0.3s;
            pointer-events: auto;
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
            border: 1px solid {c["text_color"]}44;
            color: {c["text_color"]};
            font-family: 'EB Garamond', serif;
            font-size: 14px;
            cursor: pointer;
            transition: all 0.3s;
            pointer-events: auto;
        }}
        
        .detail-btn:hover {{
            background: {c["text_color"]}22;
            border-color: {c["text_color"]};
        }}
        
        /* Whisper text */
        #whisper {{
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-style: italic;
            font-size: 16px;
            opacity: 0;
            transition: opacity 1.5s;
            pointer-events: none;
            text-align: center;
            z-index: 150;
        }}
        
        /* Vignette */
        .vignette {{
            position: absolute;
            top: 0; left: 0;
            width: 100%; height: 100%;
            pointer-events: none;
            background: radial-gradient(ellipse at center, 
                transparent 40%, 
                rgba(0,0,0,{0.6 if mode != 'clinical' else 0.2}) 100%);
            z-index: 50;
        }}
        
        /* Secret found flash */
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
            text-shadow: 0 0 20px rgba(139,0,0,0.8);
        }}
        
        /* Leech animation */
        @keyframes leech-squirm {{
            0%, 100% {{ transform: scaleX(1) scaleY(1); }}
            50% {{ transform: scaleX(0.9) scaleY(1.1); }}
        }}
        
        /* Liquid swirl */
        @keyframes swirl {{
            0% {{ filter: hue-rotate(0deg); }}
            100% {{ filter: hue-rotate(360deg); }}
        }}
    </style>
</head>
<body>
    <div id="container"></div>
    <div class="vignette"></div>
    
    <div id="title" class="ui-overlay">The Fitzroy Collection</div>
    <div id="subtitle" class="ui-overlay">Private Medical Cabinet — St. Bartholomew's Hospital, 1889</div>
    <div id="info" class="ui-overlay">Drag to rotate • Scroll to zoom • Click bottles to examine</div>
    <div id="secrets-count" class="ui-overlay">Secrets: <span id="secret-num">0</span>/8</div>
    <div id="bottle-hint" class="ui-overlay"></div>
    <div id="whisper" class="ui-overlay"></div>
    <div id="secret-flash">Secret Discovered</div>
    
    <!-- Detail Panel -->
    <div id="detail-panel">
        <div id="close-detail">×</div>
        <div id="detail-content">
            <div id="bottle-view">
                <canvas id="bottle-canvas" width="400" height="500"></canvas>
            </div>
            <div id="bottle-info">
                <div id="bottle-name"></div>
                <div id="bottle-subtitle"></div>
                <div id="bottle-description"></div>
                <div id="bottle-contents"></div>
                <div id="bottle-warning"></div>
                <div id="bottle-secret"></div>
                <div id="detail-actions">
                    <button class="detail-btn" id="btn-rotate">Rotate</button>
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
            // Shelf 1: "Medicines"
            {{
                id: 'laudanum',
                name: 'Laudanum',
                subtitle: 'Tincture of Opium',
                shape: 'rectangular',
                color: 0xcc8844,
                opacity: 0.7,
                liquidColor: 0x442200,
                liquidLevel: 0.6,
                position: {{ shelf: 0, slot: 0 }},
                description: 'A powerful preparation of opium dissolved in alcohol. Prescribed liberally for pain, coughs, insomnia, and "women\'s complaints." Highly addictive.',
                contents: 'Opium, alcohol, and various "proprietary" additives. This bottle is nearly half empty.',
                warning: 'HIGHLY ADDICTIVE',
                secret: 'Margin note in Fitzroy\'s hand: "Mrs. Harrison — increase to 40 drops. She asks too many questions."',
                secretId: 'laudanum_note',
                hasSecret: true
            }},
            {{
                id: 'chloroform',
                name: 'Chloroform',
                subtitle: 'Anesthetic Compound',
                shape: 'hexagonal',
                color: 0x4466aa,
                opacity: 0.5,
                liquidColor: 0xeeeeff,
                liquidLevel: 0.3,
                position: {{ shelf: 0, slot: 1 }},
                description: 'A volatile anesthetic. Revolutionized surgery—and enabled darker purposes. The skull embossed on the glass serves as warning.',
                contents: 'Trichloromethane. The bottle is nearly empty. Recently used.',
                warning: 'POISON — HANDLE WITH CARE',
                secret: 'Fingerprints in the dust suggest frequent, recent use. But Fitzroy has had no surgeries scheduled this month.',
                secretId: 'chloroform_use',
                hasSecret: INTENSITY >= 3
            }},
            {{
                id: 'soothing_syrup',
                name: 'Mrs. Winslow\\'s Soothing Syrup',
                subtitle: 'For Teething Infants',
                shape: 'round',
                color: 0xeeddcc,
                opacity: 0.8,
                liquidColor: 0x886644,
                liquidLevel: 0.8,
                position: {{ shelf: 0, slot: 2 }},
                description: 'A "soothing" preparation for fussy infants. The cheerful label depicts a peaceful, sleeping baby.',
                contents: 'Morphine sulphate and alcohol. One drop will quiet any child. Some never wake.',
                warning: 'FOR EXTERNAL USE ONLY',
                secret: 'The label is different from commercial versions. This was compounded specially. The dosage instructions are ten times the normal amount.',
                secretId: 'syrup_dosage',
                hasSecret: INTENSITY >= 2
            }},
            {{
                id: 'mercury',
                name: 'Mercury Bichloride',
                subtitle: 'Blue Mass Pills',
                shape: 'round',
                color: 0x223344,
                opacity: 0.6,
                liquidColor: 0x889999,
                liquidLevel: 0.5,
                position: {{ shelf: 0, slot: 3 }},
                description: 'The standard treatment for syphilis. Also causes madness, tooth loss, and death. But the alternative was considered worse.',
                contents: 'Mercuric chloride in suspension. The liquid has a silver shimmer.',
                warning: 'TOXIC — PHYSICIAN USE ONLY',
                secret: 'A list of names is tucked behind the label. Society members? Or patients who knew too much?',
                secretId: 'mercury_names',
                hasSecret: INTENSITY >= 4
            }},
            {{
                id: 'arsenic',
                name: 'Dr. Rose\\'s Arsenic Wafers',
                subtitle: 'Complexion Beautifier',
                shape: 'oval',
                color: 0x99aa88,
                opacity: 0.6,
                liquidColor: 0xddffdd,
                liquidLevel: 0.7,
                position: {{ shelf: 0, slot: 4 }},
                description: 'For achieving that fashionable pale, ethereal complexion. Women consumed these daily, slowly poisoning themselves for beauty.',
                contents: 'Arsenic trioxide in a sugar base. Sweet-tasting death.',
                warning: 'TAKE AS DIRECTED',
                secret: 'Why does a male anatomist keep complexion wafers? Unless they serve another purpose entirely...',
                secretId: 'arsenic_purpose',
                hasSecret: INTENSITY >= 3
            }},
            
            // Shelf 2: Surgical
            {{
                id: 'ether',
                name: 'Diethyl Ether',
                subtitle: 'Surgical Anesthetic',
                shape: 'ribbed',
                color: 0x664422,
                opacity: 0.5,
                liquidColor: 0xffeedd,
                liquidLevel: 0.4,
                position: {{ shelf: 1, slot: 0 }},
                description: 'The miracle of modern surgery—patients who sleep through the knife. But ether is unpredictable. Sometimes they wake during.',
                contents: 'Pure diethyl ether. Highly flammable. The rubber stopper is degraded.',
                warning: 'FLAMMABLE — NO OPEN FLAME',
                secret: 'There are scratches on the inside of the lid. As if someone tried to open it from within.',
                secretId: 'ether_scratches',
                hasSecret: INTENSITY >= 5
            }},
            {{
                id: 'cocaine',
                name: 'Cocaine Solution 4%',
                subtitle: 'Local Anesthetic',
                shape: 'dropper',
                color: 0xeeeeff,
                opacity: 0.3,
                liquidColor: 0xffffff,
                liquidLevel: 0.15,
                position: {{ shelf: 1, slot: 1 }},
                description: 'Revolutionary local anesthetic for eye and dental surgery. Also remarkably effective at improving the surgeon\\'s confidence.',
                contents: 'Cocaine hydrochloride solution. Nearly empty. Someone has been using this.',
                warning: 'MEDICINAL USE ONLY',
                secret: 'This is Fitzroy\\'s personal supply. The consumption rate suggests daily use. His hands never shake during demonstrations.',
                secretId: 'cocaine_addiction',
                hasSecret: true
            }},
            {{
                id: 'strychnine',
                name: 'Strychnine Tonic',
                subtitle: 'Nerve Stimulant',
                shape: 'hexagonal',
                color: 0xcc2222,
                opacity: 0.6,
                liquidColor: 0xffdddd,
                liquidLevel: 0.5,
                position: {{ shelf: 1, slot: 2 }},
                description: 'A "tonic" that stimulates the nerves. In small doses, a stimulant. In larger doses, death by violent convulsions.',
                contents: 'Strychnine in alcohol solution. The bright red label serves as warning.',
                warning: 'POISON — MEASURED DOSES ONLY',
                secret: 'The dosage guidelines have been scratched out and rewritten. The new dose would be lethal.',
                secretId: 'strychnine_dose',
                hasSecret: INTENSITY >= 4
            }},
            {{
                id: 'carbolic',
                name: 'Carbolic Acid',
                subtitle: 'Antiseptic Solution',
                shape: 'hexagonal',
                color: 0x4444aa,
                opacity: 0.5,
                liquidColor: 0xffffee,
                liquidLevel: 0.7,
                position: {{ shelf: 1, slot: 3 }},
                description: 'Lister\\'s miracle—the solution that kills infection. Also useful for destroying evidence.',
                contents: 'Phenol solution 5%. Burns organic matter on contact.',
                warning: 'CORROSIVE — DILUTE BEFORE USE',
                secret: 'There are traces of blood on the bottle cap. And hair. Human hair.',
                secretId: 'carbolic_evidence',
                hasSecret: INTENSITY >= 4
            }},
            {{
                id: 'embalming',
                name: 'Embalming Fluid',
                subtitle: 'Preservation Solution',
                shape: 'large_round',
                color: 0x888866,
                opacity: 0.4,
                liquidColor: 0xddddaa,
                liquidLevel: 0.9,
                position: {{ shelf: 1, slot: 4 }},
                description: 'Formaldehyde solution for preserving specimens. An anatomist\\'s essential tool.',
                contents: 'Formaldehyde, methanol, and proprietary additives. This is an unusually large supply.',
                warning: 'TOXIC FUMES — VENTILATE',
                secret: 'Why does Fitzroy need this much? The hospital provides preservation fluid. Unless specimens are being prepared elsewhere...',
                secretId: 'embalming_quantity',
                hasSecret: INTENSITY >= 3
            }},
            
            // Shelf 3: The Society's Collection
            {{
                id: 'vita_aeterna',
                name: 'Vita Aeterna',
                subtitle: 'The Eternal Essence',
                shape: 'teardrop',
                color: 0x880022,
                opacity: 0.8,
                liquidColor: 0xaa0000,
                liquidLevel: 0.6,
                position: {{ shelf: 2, slot: 0 }},
                special: 'swirl',
                description: 'The Society\\'s communion wine. Passed among members during their secret gatherings. The liquid seems to move of its own accord.',
                contents: 'Unknown. The color is too deep for wine. Too red. It swirls without being touched.',
                warning: 'FOR MEMBERS ONLY',
                secret: '"Sanguis innocentum" — Blood of the innocent. The label is written in Fitzroy\\'s hand. This is not wine.',
                secretId: 'vita_truth',
                hasSecret: true
            }},
            {{
                id: 'unmarked',
                name: 'Unmarked Bottle #7',
                subtitle: 'Contents Unknown',
                shape: 'hexagonal',
                color: 0x666666,
                opacity: 0.4,
                liquidColor: 0xffffff,
                liquidLevel: 0.5,
                position: {{ shelf: 2, slot: 1 }},
                description: 'No label. No markings. The liquid is cloudy white. There is a faint smell of almonds.',
                contents: 'Unknown. But that smell... bitter almonds indicate hydrogen cyanide.',
                warning: 'DO NOT OPEN',
                secret: 'This is potassium cyanide. Enough to kill a hundred people. Why does Fitzroy keep this?',
                secretId: 'cyanide',
                hasSecret: INTENSITY >= 3
            }},
            {{
                id: 'unwilling',
                name: '"For the Unwilling"',
                subtitle: 'Special Preparation',
                shape: 'rectangular',
                color: 0x111111,
                opacity: 0.9,
                liquidColor: 0x332244,
                liquidLevel: 0.7,
                position: {{ shelf: 2, slot: 2 }},
                description: 'Black glass. No commercial label. Only those handwritten words. The Society uses this when subjects do not come willingly.',
                contents: 'Chloral hydrate, morphine, and something else. One dose brings immediate unconsciousness.',
                warning: 'SOCIETY USE ONLY',
                secret: 'The procurement ledger shows 12 "donations" this year. Not one was voluntary. This bottle made them all... compliant.',
                secretId: 'unwilling_purpose',
                hasSecret: true
            }},
            {{
                id: 'final_mercy',
                name: '"Final Mercy"',
                subtitle: 'Terminal Preparation',
                shape: 'tiny_vial',
                color: 0xaa0000,
                opacity: 0.7,
                liquidColor: 0x220000,
                liquidLevel: 0.9,
                position: {{ shelf: 2, slot: 3 }},
                description: 'A tiny vial with a red skull. When demonstrations go wrong—when subjects suffer too long—this ends it quickly.',
                contents: 'Concentrated morphine and potassium chloride. Death within seconds.',
                warning: 'EMERGENCY USE',
                secret: 'Three doses are missing since January. Three subjects whose hearts "simply gave out" during demonstration.',
                secretId: 'mercy_used',
                hasSecret: INTENSITY >= 4
            }},
            {{
                id: 'blood_sc',
                name: 'Preserved Blood — S.C.',
                subtitle: 'Sample Collection',
                shape: 'test_tube',
                color: 0xeeeeee,
                opacity: 0.3,
                liquidColor: 0x660000,
                liquidLevel: 0.6,
                position: {{ shelf: 2, slot: 4 }},
                description: 'A corked test tube containing preserved blood. The initials S.C. are written on the label in Fitzroy\\'s hand.',
                contents: 'Human blood, preserved in citrate solution. Still viable for testing.',
                warning: 'SPECIMEN — DO NOT DISCARD',
                secret: 'S.C. — Sebastian Carlisle. Fitzroy\\'s star pupil. Why is his blood being kept? What tests are being run?',
                secretId: 'sebastian_blood',
                hasSecret: true
            }},
            
            // Shelf 4: Curiosities
            {{
                id: 'teeth',
                name: 'Dental Collection',
                subtitle: 'Human Teeth in Spirits',
                shape: 'wide_jar',
                color: 0xffffee,
                opacity: 0.4,
                liquidColor: 0xffffdd,
                liquidLevel: 0.8,
                hasParticles: true,
                position: {{ shelf: 3, slot: 0 }},
                description: 'A wide-mouth jar filled with human teeth suspended in alcohol. They shift and settle as you watch.',
                contents: 'Forty-seven teeth. From how many patients? The variety suggests at least a dozen sources.',
                warning: 'ANATOMICAL SPECIMEN',
                secret: 'Some teeth show signs of being extracted from the living. Tool marks. Fractures. These were not collected from corpses.',
                secretId: 'teeth_source',
                hasSecret: INTENSITY >= 3
            }},
            {{
                id: 'leeches',
                name: 'Medicinal Leeches',
                subtitle: 'Hirudo medicinalis',
                shape: 'leech_jar',
                color: 0xeeffee,
                opacity: 0.3,
                liquidColor: 0xccddcc,
                liquidLevel: 0.7,
                special: 'leeches',
                position: {{ shelf: 3, slot: 1 }},
                description: 'Living leeches for bloodletting. They move behind the glass, sensing warmth. Sensing you.',
                contents: 'A dozen medicinal leeches. They are hungry. They press against the glass when you come near.',
                warning: 'LIVE SPECIMENS',
                secret: 'Why are these leeches so large? What have they been feeding on? The hospital stopped using leeches years ago.',
                secretId: 'leech_feeding',
                hasSecret: INTENSITY >= 2
            }},
            {{
                id: 'essence',
                name: '"Essence of Youth"',
                subtitle: 'Rejuvenation Compound',
                shape: 'ceramic_pot',
                color: 0xddccbb,
                opacity: 1.0,
                liquidColor: 0xffffee,
                liquidLevel: 0.6,
                position: {{ shelf: 3, slot: 2 }},
                description: 'A ceramic pot with a hand-written label. The contents are waxy, pale yellow. A faint smell of rendered fat.',
                contents: 'Unknown fatty substance. Solid at room temperature. Applied to the skin, it softens wrinkles.',
                warning: 'EXTERNAL USE ONLY',
                secret: 'This is human fat. Rendered from surgical "waste." The Society sells this to wealthy patrons. Made from the poor. Bought by the rich.',
                secretId: 'fat_source',
                hasSecret: INTENSITY >= 4
            }},
            {{
                id: 'tapeworm',
                name: 'Sanitized Tapeworm',
                subtitle: 'Diet Aid',
                shape: 'round',
                color: 0xeeeedd,
                opacity: 0.4,
                liquidColor: 0xffffee,
                liquidLevel: 0.7,
                hasParticles: true,
                position: {{ shelf: 3, slot: 3 }},
                description: 'Segments of beef tapeworm in preservation fluid. Victorians swallowed these intentionally to lose weight.',
                contents: 'Taenia saginata segments. Marketed as a "natural" weight loss solution. The worms consume food in the intestines.',
                warning: 'NOT FOR CONSUMPTION',
                secret: 'This jar contains far more segments than a single tapeworm produces. Someone is farming these. For sale?',
                secretId: 'tapeworm_farm',
                hasSecret: INTENSITY >= 3
            }},
            {{
                id: 'brain_tonic',
                name: 'Dr. Hammond\\'s Nerve Food',
                subtitle: 'For Weakness of Mind',
                shape: 'ornate_jar',
                color: 0xbbaa99,
                opacity: 0.6,
                liquidColor: 0xddccbb,
                liquidLevel: 0.5,
                position: {{ shelf: 3, slot: 4 }},
                description: 'An ornate jar promising to restore mental acuity. The contents are gray and fibrous. Floating in yellowed fluid.',
                contents: 'Preserved brain tissue suspended in alcohol. The label claims this "transfers mental energy" when consumed.',
                warning: 'TAKE TWICE DAILY',
                secret: '"Brain matter from subjects displaying superior intellect." This is human tissue. Marketed as medicine. Cannibalism dressed as cure.',
                secretId: 'brain_cannibalism',
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
        scene.background = new THREE.Color({to_hex(c["background"])});
        scene.fog = new THREE.FogExp2({to_hex(c["background"])}, 0.015);
        
        const camera = new THREE.PerspectiveCamera(50, width / height, 0.1, 1000);
        camera.position.set(0, 1.5, 5);
        camera.lookAt(0, 1, 0);
        
        const renderer = new THREE.WebGLRenderer({{ antialias: true }});
        renderer.setSize(width, height);
        renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        renderer.shadowMap.enabled = true;
        container.appendChild(renderer.domElement);
        
        const raycaster = new THREE.Raycaster();
        const mouse = new THREE.Vector2();
        
        // Lighting
        scene.add(new THREE.AmbientLight(0xffffff, {c["ambient"]}));
        
        const keyLight = new THREE.SpotLight({to_hex(c["light_color"])}, 1.2);
        keyLight.position.set(2, 4, 3);
        keyLight.angle = Math.PI / 4;
        keyLight.penumbra = 0.5;
        keyLight.castShadow = true;
        scene.add(keyLight);
        
        const fillLight = new THREE.PointLight({to_hex(c["light_color"])}, 0.4);
        fillLight.position.set(-2, 2, 2);
        scene.add(fillLight);
        
        const backLight = new THREE.PointLight({to_hex(c["light_color"])}, 0.3);
        backLight.position.set(0, 2, -3);
        scene.add(backLight);
        
        // ==========================================
        // CABINET CONSTRUCTION
        // ==========================================
        
        const cabinetGroup = new THREE.Group();
        
        const woodMat = new THREE.MeshLambertMaterial({{ color: {to_hex(c["wood"])} }});
        const darkWoodMat = new THREE.MeshLambertMaterial({{ color: {to_hex(c["wood_dark"])} }});
        const metalMat = new THREE.MeshLambertMaterial({{ color: {to_hex(c["metal"])} }});
        
        // Cabinet frame
        const cabinetWidth = 3.5;
        const cabinetHeight = 3;
        const cabinetDepth = 0.6;
        const shelfCount = 4;
        const shelfHeight = cabinetHeight / shelfCount;
        
        // Back panel
        const backPanel = new THREE.Mesh(
            new THREE.BoxGeometry(cabinetWidth, cabinetHeight, 0.05),
            darkWoodMat
        );
        backPanel.position.z = -cabinetDepth / 2;
        backPanel.position.y = cabinetHeight / 2;
        cabinetGroup.add(backPanel);
        
        // Side panels
        [-1, 1].forEach(side => {{
            const sidePanel = new THREE.Mesh(
                new THREE.BoxGeometry(0.08, cabinetHeight, cabinetDepth),
                woodMat
            );
            sidePanel.position.x = side * (cabinetWidth / 2);
            sidePanel.position.y = cabinetHeight / 2;
            sidePanel.castShadow = true;
            cabinetGroup.add(sidePanel);
        }});
        
        // Top panel
        const topPanel = new THREE.Mesh(
            new THREE.BoxGeometry(cabinetWidth + 0.1, 0.08, cabinetDepth + 0.1),
            woodMat
        );
        topPanel.position.y = cabinetHeight + 0.04;
        topPanel.castShadow = true;
        cabinetGroup.add(topPanel);
        
        // Crown molding
        const crownGeo = new THREE.BoxGeometry(cabinetWidth + 0.2, 0.15, 0.15);
        const crown = new THREE.Mesh(crownGeo, woodMat);
        crown.position.y = cabinetHeight + 0.12;
        crown.position.z = cabinetDepth / 2 - 0.05;
        cabinetGroup.add(crown);
        
        // Shelves
        for (let i = 0; i <= shelfCount; i++) {{
            const shelf = new THREE.Mesh(
                new THREE.BoxGeometry(cabinetWidth - 0.1, 0.04, cabinetDepth - 0.05),
                woodMat
            );
            shelf.position.y = i * shelfHeight;
            shelf.receiveShadow = true;
            cabinetGroup.add(shelf);
        }}
        
        // Decorative columns
        [-1, 1].forEach(side => {{
            const column = new THREE.Mesh(
                new THREE.CylinderGeometry(0.04, 0.05, cabinetHeight, 8),
                metalMat
            );
            column.position.x = side * (cabinetWidth / 2 - 0.15);
            column.position.y = cabinetHeight / 2;
            column.position.z = cabinetDepth / 2 - 0.1;
            cabinetGroup.add(column);
        }});
        
        scene.add(cabinetGroup);
        
        // ==========================================
        // BOTTLE CREATION
        // ==========================================
        
        const bottleObjects = [];
        const bottleMeshMap = new Map();
        
        function createBottleGeometry(shape) {{
            switch(shape) {{
                case 'rectangular':
                    return new THREE.BoxGeometry(0.15, 0.35, 0.08);
                case 'hexagonal':
                    return new THREE.CylinderGeometry(0.07, 0.07, 0.32, 6);
                case 'round':
                    return new THREE.CylinderGeometry(0.08, 0.08, 0.28, 16);
                case 'oval':
                    return new THREE.CapsuleGeometry(0.06, 0.15, 8, 16);
                case 'ribbed':
                    return new THREE.CylinderGeometry(0.07, 0.08, 0.3, 12);
                case 'teardrop':
                    return new THREE.SphereGeometry(0.1, 16, 12);
                case 'dropper':
                    return new THREE.CylinderGeometry(0.04, 0.06, 0.25, 12);
                case 'large_round':
                    return new THREE.CylinderGeometry(0.12, 0.12, 0.35, 16);
                case 'tiny_vial':
                    return new THREE.CylinderGeometry(0.025, 0.025, 0.12, 8);
                case 'test_tube':
                    return new THREE.CapsuleGeometry(0.025, 0.12, 4, 12);
                case 'wide_jar':
                    return new THREE.CylinderGeometry(0.12, 0.11, 0.22, 16);
                case 'leech_jar':
                    return new THREE.CylinderGeometry(0.1, 0.1, 0.25, 16);
                case 'ceramic_pot':
                    return new THREE.CylinderGeometry(0.09, 0.11, 0.18, 12);
                case 'ornate_jar':
                    return new THREE.CylinderGeometry(0.1, 0.08, 0.25, 8);
                default:
                    return new THREE.CylinderGeometry(0.07, 0.07, 0.28, 12);
            }}
        }}
        
        function getSlotPosition(shelf, slot) {{
            const startX = -cabinetWidth / 2 + 0.35;
            const spacing = (cabinetWidth - 0.7) / 4;
            const x = startX + slot * spacing;
            const y = shelf * shelfHeight + 0.15;
            const z = 0;
            return {{ x, y, z }};
        }}
        
        BOTTLES.forEach(bottleData => {{
            const group = new THREE.Group();
            
            // Glass bottle
            const glassGeo = createBottleGeometry(bottleData.shape);
            const glassMat = new THREE.MeshPhysicalMaterial({{
                color: bottleData.color,
                transparent: true,
                opacity: bottleData.opacity,
                roughness: 0.1,
                metalness: 0.1,
                transmission: 0.3
            }});
            const glass = new THREE.Mesh(glassGeo, glassMat);
            group.add(glass);
            
            // Liquid inside
            const liquidScale = 0.85;
            const liquidGeo = createBottleGeometry(bottleData.shape);
            liquidGeo.scale(liquidScale, bottleData.liquidLevel * liquidScale, liquidScale);
            const liquidMat = new THREE.MeshLambertMaterial({{
                color: bottleData.liquidColor,
                transparent: true,
                opacity: 0.8
            }});
            const liquid = new THREE.Mesh(liquidGeo, liquidMat);
            liquid.position.y = -((1 - bottleData.liquidLevel) * 0.15);
            group.add(liquid);
            
            // Cork/stopper
            const corkGeo = new THREE.CylinderGeometry(0.03, 0.035, 0.05, 8);
            const corkMat = new THREE.MeshLambertMaterial({{ color: 0x8b7355 }});
            const cork = new THREE.Mesh(corkGeo, corkMat);
            cork.position.y = glassGeo.parameters.height ? glassGeo.parameters.height / 2 + 0.02 : 0.16;
            group.add(cork);
            
            // Label (simple plane)
            const labelGeo = new THREE.PlaneGeometry(0.1, 0.08);
            const labelMat = new THREE.MeshLambertMaterial({{ 
                color: 0xffffee,
                side: THREE.DoubleSide
            }});
            const label = new THREE.Mesh(labelGeo, labelMat);
            label.position.z = 0.08;
            label.position.y = -0.02;
            group.add(label);
            
            // Position on shelf
            const pos = getSlotPosition(bottleData.position.shelf, bottleData.position.slot);
            group.position.set(pos.x, pos.y, pos.z);
            
            // Store data reference
            group.userData = bottleData;
            
            cabinetGroup.add(group);
            bottleObjects.push(group);
            bottleMeshMap.set(bottleData.id, group);
        }});
        
        // ==========================================
        // DUST PARTICLES
        // ==========================================
        
        const dustCount = 100;
        const dustGeo = new THREE.BufferGeometry();
        const dustPos = new Float32Array(dustCount * 3);
        
        for (let i = 0; i < dustCount; i++) {{
            dustPos[i * 3] = (Math.random() - 0.5) * 4;
            dustPos[i * 3 + 1] = Math.random() * 3.5;
            dustPos[i * 3 + 2] = (Math.random() - 0.5) * 2;
        }}
        
        dustGeo.setAttribute('position', new THREE.BufferAttribute(dustPos, 3));
        const dust = new THREE.Points(dustGeo, new THREE.PointsMaterial({{
            color: {to_hex(c["light_color"])},
            size: 0.015,
            transparent: true,
            opacity: 0.4
        }}));
        scene.add(dust);
        
        // ==========================================
        // CAMERA CONTROLS
        // ==========================================
        
        let isDragging = false;
        let prevMouse = {{ x: 0, y: 0 }};
        let cameraAngle = {{ theta: 0, phi: Math.PI / 2 - 0.3 }};
        let cameraDistance = 5;
        let cameraTarget = new THREE.Vector3(0, 1.5, 0);
        
        function updateCamera() {{
            camera.position.x = cameraTarget.x + cameraDistance * Math.sin(cameraAngle.phi) * Math.sin(cameraAngle.theta);
            camera.position.y = cameraTarget.y + cameraDistance * Math.cos(cameraAngle.phi);
            camera.position.z = cameraTarget.z + cameraDistance * Math.sin(cameraAngle.phi) * Math.cos(cameraAngle.theta);
            camera.lookAt(cameraTarget);
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
                cameraAngle.theta += dx * 0.005;
                cameraAngle.phi = Math.max(0.5, Math.min(1.3, cameraAngle.phi + dy * 0.005));
                prevMouse = {{ x: e.clientX, y: e.clientY }};
                updateCamera();
            }}
        }});
        
        window.addEventListener('mouseup', () => {{ isDragging = false; }});
        
        renderer.domElement.addEventListener('wheel', e => {{
            e.preventDefault();
            cameraDistance = Math.max(3, Math.min(8, cameraDistance + e.deltaY * 0.005));
            updateCamera();
        }}, {{ passive: false }});
        
        // Touch controls
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
                cameraAngle.theta += dx * 0.005;
                cameraAngle.phi = Math.max(0.5, Math.min(1.3, cameraAngle.phi + dy * 0.005));
                prevMouse = {{ x: e.touches[0].clientX, y: e.touches[0].clientY }};
                updateCamera();
            }}
        }});
        
        renderer.domElement.addEventListener('touchend', () => {{ isDragging = false; }});
        
        updateCamera();
        
        // ==========================================
        // CLICK INTERACTIONS
        // ==========================================
        
        let selectedBottle = null;
        
        const detailPanel = document.getElementById('detail-panel');
        const bottleName = document.getElementById('bottle-name');
        const bottleSubtitle = document.getElementById('bottle-subtitle');
        const bottleDescription = document.getElementById('bottle-description');
        const bottleContents = document.getElementById('bottle-contents');
        const bottleWarning = document.getElementById('bottle-warning');
        const bottleSecret = document.getElementById('bottle-secret');
        const secretFlash = document.getElementById('secret-flash');
        
        function showBottleDetail(bottleData) {{
            selectedBottle = bottleData;
            
            bottleName.textContent = bottleData.name;
            bottleSubtitle.textContent = bottleData.subtitle;
            bottleDescription.textContent = bottleData.description;
            bottleContents.textContent = '📋 ' + bottleData.contents;
            bottleWarning.textContent = '⚠ ' + bottleData.warning;
            
            // Secret
            bottleSecret.classList.remove('revealed');
            if (bottleData.hasSecret && bottleData.secret) {{
                bottleSecret.textContent = '🔍 ' + bottleData.secret;
                setTimeout(() => {{
                    bottleSecret.classList.add('revealed');
                    
                    // Track secret discovery
                    if (!foundSecrets.has(bottleData.secretId)) {{
                        foundSecrets.add(bottleData.secretId);
                        secretsFound++;
                        document.getElementById('secret-num').textContent = secretsFound;
                        
                        secretFlash.style.opacity = 1;
                        setTimeout(() => {{ secretFlash.style.opacity = 0; }}, 2000);
                    }}
                }}, 1500);
            }} else {{
                bottleSecret.textContent = '';
            }}
            
            detailPanel.classList.add('visible');
            drawBottle2D(bottleData);
        }}
        
        document.getElementById('close-detail').addEventListener('click', () => {{
            detailPanel.classList.remove('visible');
            selectedBottle = null;
        }});
        
        renderer.domElement.addEventListener('click', e => {{
            if (isDragging) return;
            
            const clickMouse = new THREE.Vector2(
                (e.clientX / window.innerWidth) * 2 - 1,
                -(e.clientY / window.innerHeight) * 2 + 1
            );
            
            raycaster.setFromCamera(clickMouse, camera);
            const intersects = raycaster.intersectObjects(bottleObjects, true);
            
            if (intersects.length > 0) {{
                let obj = intersects[0].object;
                while (obj && !obj.userData.id) obj = obj.parent;
                
                if (obj && obj.userData.id) {{
                    showBottleDetail(obj.userData);
                }}
            }}
        }});
        
        // ==========================================
        // 2D BOTTLE RENDERING
        // ==========================================
        
        const canvas2D = document.getElementById('bottle-canvas');
        const ctx = canvas2D.getContext('2d');
        let bottleRotation = 0;
        let isShaking = false;
        let liquidOffset = 0;
        
        function drawBottle2D(bottle) {{
            const w = canvas2D.width;
            const h = canvas2D.height;
            const cx = w / 2;
            const cy = h / 2;
            
            ctx.clearRect(0, 0, w, h);
            
            // Bottle body
            ctx.save();
            ctx.translate(cx, cy);
            ctx.rotate(Math.sin(bottleRotation) * 0.1);
            
            // Glass
            const bottleWidth = 80;
            const bottleHeight = 200;
            
            ctx.fillStyle = '#' + bottle.color.toString(16).padStart(6, '0') + '88';
            ctx.strokeStyle = '#' + bottle.color.toString(16).padStart(6, '0');
            ctx.lineWidth = 2;
            
            // Bottle shape
            ctx.beginPath();
            ctx.roundRect(-bottleWidth/2, -bottleHeight/2, bottleWidth, bottleHeight, 8);
            ctx.fill();
            ctx.stroke();
            
            // Liquid
            const liquidHeight = bottleHeight * bottle.liquidLevel * 0.85;
            const liquidY = bottleHeight/2 - liquidHeight - 10;
            
            ctx.fillStyle = '#' + bottle.liquidColor.toString(16).padStart(6, '0') + 'cc';
            ctx.beginPath();
            
            // Wavy top for liquid
            ctx.moveTo(-bottleWidth/2 + 8, liquidY + Math.sin(liquidOffset) * 3);
            for (let x = -bottleWidth/2 + 8; x <= bottleWidth/2 - 8; x += 5) {{
                ctx.lineTo(x, liquidY + Math.sin(liquidOffset + x * 0.1) * 3);
            }}
            ctx.lineTo(bottleWidth/2 - 8, bottleHeight/2 - 10);
            ctx.lineTo(-bottleWidth/2 + 8, bottleHeight/2 - 10);
            ctx.closePath();
            ctx.fill();
            
            // Cork
            ctx.fillStyle = '#8b7355';
            ctx.fillRect(-15, -bottleHeight/2 - 20, 30, 25);
            
            // Label
            ctx.fillStyle = '#ffffee';
            ctx.fillRect(-35, -20, 70, 50);
            ctx.strokeStyle = '#8b7355';
            ctx.lineWidth = 1;
            ctx.strokeRect(-35, -20, 70, 50);
            
            // Label text
            ctx.fillStyle = '#333';
            ctx.font = '10px Georgia';
            ctx.textAlign = 'center';
            ctx.fillText(bottle.name, 0, 0);
            ctx.font = '7px Georgia';
            ctx.fillText(bottle.subtitle, 0, 15);
            
            // Special effects
            if (bottle.special === 'leeches' && INTENSITY >= 2) {{
                // Draw leeches
                ctx.fillStyle = '#2a3a2a';
                for (let i = 0; i < 5; i++) {{
                    const lx = Math.sin(liquidOffset * 0.5 + i * 2) * 25;
                    const ly = liquidY + 30 + Math.cos(liquidOffset * 0.3 + i * 3) * 20;
                    ctx.beginPath();
                    ctx.ellipse(lx, ly, 8, 4, Math.sin(liquidOffset + i) * 0.5, 0, Math.PI * 2);
                    ctx.fill();
                }}
            }}
            
            if (bottle.special === 'swirl') {{
                // Swirling effect
                ctx.strokeStyle = '#ff000044';
                ctx.lineWidth = 2;
                for (let i = 0; i < 3; i++) {{
                    ctx.beginPath();
                    ctx.arc(
                        Math.sin(liquidOffset + i) * 15,
                        liquidY + 40 + i * 20,
                        10 + i * 5,
                        liquidOffset + i,
                        liquidOffset + i + Math.PI
                    );
                    ctx.stroke();
                }}
            }}
            
            ctx.restore();
            
            // Intensity 5: Face in the glass
            if (INTENSITY >= 5 && Math.random() > 0.95) {{
                ctx.fillStyle = 'rgba(0,0,0,0.3)';
                ctx.beginPath();
                ctx.arc(cx + 20, cy - 30, 15, 0, Math.PI * 2);
                ctx.fill();
                ctx.fillStyle = 'rgba(255,255,255,0.5)';
                ctx.beginPath();
                ctx.arc(cx + 15, cy - 35, 3, 0, Math.PI * 2);
                ctx.arc(cx + 25, cy - 35, 3, 0, Math.PI * 2);
                ctx.fill();
            }}
        }}
        
        // Button handlers
        document.getElementById('btn-rotate').addEventListener('click', () => {{
            bottleRotation += Math.PI / 2;
        }});
        
        document.getElementById('btn-shake').addEventListener('click', () => {{
            isShaking = true;
            setTimeout(() => {{ isShaking = false; }}, 1000);
        }});
        
        document.getElementById('btn-open').addEventListener('click', () => {{
            if (selectedBottle) {{
                const scents = {{
                    'laudanum': 'A bitter, medicinal smell mixed with alcohol...',
                    'chloroform': 'Sweet, almost pleasant. Dangerously so.',
                    'cocaine': 'Slight chemical odor. Your nose tingles.',
                    'unmarked': 'Bitter almonds. You pull back immediately.',
                    'vita_aeterna': 'Iron. Salt. Something ancient.',
                    'embalming': 'Sharp formaldehyde burns your nostrils.',
                    'leeches': 'Stagnant water and something organic...'
                }};
                
                const hint = document.getElementById('bottle-hint');
                hint.textContent = scents[selectedBottle.id] || 'A faint chemical odor...';
                hint.style.opacity = 1;
                setTimeout(() => {{ hint.style.opacity = 0; }}, 3000);
            }}
        }});
        
        // ==========================================
        // WHISPERS
        // ==========================================
        
        const whispers = [
            '*Glass clinks softly in the silence...*',
            '*Something shifts on a shelf...*',
            '*The liquid seems to move...*',
            '*You hear breathing. Your own?*',
            '*A label peels slightly at the corner...*',
            '*The leeches press against the glass...*',
            '*Someone was here recently. The dust is disturbed...*'
        ];
        
        if (INTENSITY >= 4) {{
            whispers.push('*A face. In the glass. Behind you.*');
            whispers.push('*The bottles are watching.*');
            whispers.push('*"Take one," a voice suggests.*');
        }}
        
        const whisperEl = document.getElementById('whisper');
        let whisperIdx = 0;
        
        function showWhisper() {{
            whisperEl.textContent = whispers[whisperIdx];
            whisperEl.style.opacity = 0.7;
            setTimeout(() => {{ whisperEl.style.opacity = 0; }}, 4000);
            whisperIdx = (whisperIdx + 1) % whispers.length;
        }}
        
        setTimeout(showWhisper, 5000);
        setInterval(showWhisper, 12000 - INTENSITY * 1500);
        
        // ==========================================
        // ANIMATION
        // ==========================================
        
        const clock = new THREE.Clock();
        
        function animate() {{
            requestAnimationFrame(animate);
            const t = clock.getElapsedTime();
            
            // Dust particles
            const dustPositions = dust.geometry.attributes.position.array;
            for (let i = 0; i < dustCount; i++) {{
                dustPositions[i * 3 + 1] += 0.002;
                dustPositions[i * 3] += Math.sin(t + i) * 0.001;
                if (dustPositions[i * 3 + 1] > 3.5) dustPositions[i * 3 + 1] = 0;
            }}
            dust.geometry.attributes.position.needsUpdate = true;
            
            // Light flicker
            keyLight.intensity = 1.2 + Math.sin(t * 8) * 0.1 * CREEP;
            
            // Bottle hover highlight
            raycaster.setFromCamera(mouse, camera);
            const intersects = raycaster.intersectObjects(bottleObjects, true);
            
            bottleObjects.forEach(b => {{
                b.children[0].material.emissive = new THREE.Color(0x000000);
            }});
            
            if (intersects.length > 0) {{
                let obj = intersects[0].object;
                while (obj && !obj.userData.id) obj = obj.parent;
                if (obj) {{
                    obj.children[0].material.emissive = new THREE.Color({to_hex(c["light_color"])});
                    obj.children[0].material.emissiveIntensity = 0.15;
                    
                    // Show hint
                    const hint = document.getElementById('bottle-hint');
                    hint.textContent = obj.userData.name;
                    hint.style.opacity = 0.7;
                }}
            }} else {{
                document.getElementById('bottle-hint').style.opacity = 0;
            }}
            
            // Special bottle animations
            bottleObjects.forEach(b => {{
                if (b.userData.special === 'swirl') {{
                    // Vita Aeterna swirls
                    b.children[1].rotation.y = t * 0.5;
                }}
                if (b.userData.special === 'leeches') {{
                    // Leeches pulse
                    b.children[1].scale.y = 1 + Math.sin(t * 2) * 0.05;
                }}
            }});
            
            // 2D bottle animation
            if (selectedBottle) {{
                liquidOffset += isShaking ? 0.5 : 0.03;
                if (isShaking) bottleRotation += 0.3;
                drawBottle2D(selectedBottle);
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
