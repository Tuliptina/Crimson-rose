"""
🎭 The Anatomy Theatre — 3D Experience
An immersive Three.js Victorian anatomy theatre.
"""

def get_theatre_3d(mode: str = "gaslight", intensity: int = 3) -> str:
    """
    Generate the 3D anatomy theatre HTML/JS.
    
    Args:
        mode: Visual mode (gaslight, gothic, clinical)
        intensity: Atmosphere intensity 1-5
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
            "light_color": 0xffaa44,
            "light_intensity": 1.5,
            "fog_color": 0x1a1410,
            "fog_near": 5,
            "fog_far": 50,
            "particle_color": 0xffcc88,
            "text_color": "#d4a574"
        },
        "gothic": {
            "ambient": 0x1a0505,
            "background": 0x0a0a0a,
            "wood": 0x2a1515,
            "wood_dark": 0x1a0a0a,
            "metal": 0x4a4a4a,
            "cloth": 0x8b0000,
            "light_color": 0xff2200,
            "light_intensity": 2.0,
            "fog_color": 0x0a0000,
            "fog_near": 3,
            "fog_far": 35,
            "particle_color": 0xff4444,
            "text_color": "#cc0000"
        },
        "clinical": {
            "ambient": 0x404040,
            "background": 0xf0f0f0,
            "wood": 0xe0e0e0,
            "wood_dark": 0xcccccc,
            "metal": 0xaaaaaa,
            "cloth": 0xffffff,
            "light_color": 0xffffff,
            "light_intensity": 2.5,
            "fog_color": 0xf0f0f0,
            "fog_near": 20,
            "fog_far": 100,
            "particle_color": 0xcccccc,
            "text_color": "#2f4f4f"
        }
    }
    
    c = colors.get(mode, colors["gaslight"])
    
    # Intensity affects fog density and particle count
    fog_multiplier = 1 + (intensity - 1) * 0.2
    particle_count = 100 + intensity * 50
    flicker_intensity = 0.1 + intensity * 0.05
    
    # Convert hex integers to JS hex strings
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
        }}
        canvas {{
            display: block;
            width: 100% !important;
            height: 100% !important;
        }}
        #info {{
            position: absolute;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            color: {c["text_color"]};
            font-size: 14px;
            text-align: center;
            pointer-events: none;
            text-shadow: 0 0 10px rgba(0,0,0,0.8);
            opacity: 0.8;
            z-index: 100;
        }}
        #mode-label {{
            position: absolute;
            top: 20px;
            left: 20px;
            color: {c["text_color"]};
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 3px;
            opacity: 0.6;
            z-index: 100;
        }}
        #loading {{
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            color: {c["text_color"]};
            font-size: 18px;
            z-index: 200;
        }}
        #error {{
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            color: #ff4444;
            font-size: 14px;
            text-align: center;
            max-width: 80%;
            z-index: 200;
            display: none;
        }}
        #quote {{
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            color: {c["text_color"]};
            font-size: 18px;
            font-style: italic;
            text-align: center;
            max-width: 500px;
            opacity: 0;
            transition: opacity 2s;
            pointer-events: none;
            text-shadow: 0 0 20px rgba(0,0,0,0.9);
            z-index: 100;
        }}
        .vignette {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            background: radial-gradient(ellipse at center, transparent 40%, rgba(0,0,0,{0.7 if mode != 'clinical' else 0.2}) 100%);
            z-index: 50;
        }}
    </style>
</head>
<body>
    <div id="container"></div>
    <div class="vignette"></div>
    <div id="mode-label">{mode.upper()} MODE</div>
    <div id="info">Drag to orbit • Scroll to zoom</div>
    <div id="loading">Loading Theatre...</div>
    <div id="error"></div>
    <div id="quote"></div>
    
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script>
    (function() {{
        'use strict';
        
        const loadingEl = document.getElementById('loading');
        const errorEl = document.getElementById('error');
        
        function showError(msg) {{
            loadingEl.style.display = 'none';
            errorEl.style.display = 'block';
            errorEl.textContent = 'Error: ' + msg;
            console.error(msg);
        }}
        
        // Check if Three.js loaded
        if (typeof THREE === 'undefined') {{
            showError('Three.js failed to load. Please refresh the page.');
            return;
        }}
        
        try {{
            // ========================================
            // SCENE SETUP
            // ========================================
            
            const container = document.getElementById('container');
            const width = container.clientWidth || window.innerWidth;
            const height = container.clientHeight || window.innerHeight;
            
            const scene = new THREE.Scene();
            scene.background = new THREE.Color({to_hex(c["background"])});
            scene.fog = new THREE.Fog({to_hex(c["fog_color"])}, {c["fog_near"] / fog_multiplier}, {c["fog_far"] / fog_multiplier});
            
            const camera = new THREE.PerspectiveCamera(60, width / height, 0.1, 1000);
            camera.position.set(15, 10, 15);
            camera.lookAt(0, 2, 0);
            
            const renderer = new THREE.WebGLRenderer({{ antialias: true }});
            renderer.setSize(width, height);
            renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
            renderer.shadowMap.enabled = true;
            renderer.shadowMap.type = THREE.PCFSoftShadowMap;
            container.appendChild(renderer.domElement);
            
            // ========================================
            // MATERIALS
            // ========================================
            
            const woodMaterial = new THREE.MeshLambertMaterial({{
                color: {to_hex(c["wood"])}
            }});
            
            const darkWoodMaterial = new THREE.MeshLambertMaterial({{
                color: {to_hex(c["wood_dark"])}
            }});
            
            const metalMaterial = new THREE.MeshLambertMaterial({{
                color: {to_hex(c["metal"])}
            }});
            
            const clothMaterial = new THREE.MeshLambertMaterial({{
                color: {to_hex(c["cloth"])},
                side: THREE.DoubleSide
            }});
            
            const stoneMaterial = new THREE.MeshLambertMaterial({{
                color: 0x555555
            }});
            
            // ========================================
            // LIGHTING (CRITICAL!)
            // ========================================
            
            // Strong ambient light to ensure visibility
            const ambientLight = new THREE.AmbientLight(0xffffff, 0.4);
            scene.add(ambientLight);
            
            // Hemisphere light for natural fill
            const hemiLight = new THREE.HemisphereLight(0xffffff, {to_hex(c["wood_dark"])}, 0.5);
            scene.add(hemiLight);
            
            // Main directional light
            const dirLight = new THREE.DirectionalLight({to_hex(c["light_color"])}, 1.0);
            dirLight.position.set(10, 20, 10);
            dirLight.castShadow = true;
            scene.add(dirLight);
            
            // Central spotlight on the table
            const spotlight = new THREE.SpotLight({to_hex(c["light_color"])}, {c["light_intensity"]});
            spotlight.position.set(0, 15, 0);
            spotlight.target.position.set(0, 0, 0);
            spotlight.angle = Math.PI / 4;
            spotlight.penumbra = 0.5;
            spotlight.castShadow = true;
            scene.add(spotlight);
            scene.add(spotlight.target);
            
            // ========================================
            // THEATRE STRUCTURE
            // ========================================
            
            // Floor
            const floorGeometry = new THREE.CircleGeometry(20, 64);
            const floor = new THREE.Mesh(floorGeometry, stoneMaterial);
            floor.rotation.x = -Math.PI / 2;
            floor.receiveShadow = true;
            scene.add(floor);
            
            // Central pit floor
            const pitGeometry = new THREE.CircleGeometry(4, 32);
            const pitMaterial = new THREE.MeshLambertMaterial({{ color: 0x333333 }});
            const pit = new THREE.Mesh(pitGeometry, pitMaterial);
            pit.rotation.x = -Math.PI / 2;
            pit.position.y = 0.01;
            pit.receiveShadow = true;
            scene.add(pit);
            
            // Gallery tiers
            const tierCount = 5;
            const tierHeight = 1.2;
            const tierDepth = 2;
            const innerRadius = 5;
            
            for (let i = 0; i < tierCount; i++) {{
                const radius = innerRadius + i * tierDepth;
                const y = i * tierHeight;
                
                // Tier platform (ring)
                const tierShape = new THREE.Shape();
                tierShape.absarc(0, 0, radius + tierDepth - 0.1, 0, Math.PI * 2, false);
                const tierHole = new THREE.Path();
                tierHole.absarc(0, 0, radius, 0, Math.PI * 2, true);
                tierShape.holes.push(tierHole);
                
                const tierGeometry = new THREE.ExtrudeGeometry(tierShape, {{
                    depth: 0.2,
                    bevelEnabled: false
                }});
                const tier = new THREE.Mesh(tierGeometry, woodMaterial);
                tier.rotation.x = -Math.PI / 2;
                tier.position.y = y;
                tier.receiveShadow = true;
                tier.castShadow = true;
                scene.add(tier);
                
                // Railing posts
                const postCount = 16;
                for (let j = 0; j < postCount; j++) {{
                    const angle = (j / postCount) * Math.PI * 2;
                    const postRadius = radius + 0.2;
                    
                    const postGeometry = new THREE.CylinderGeometry(0.05, 0.05, 0.8, 8);
                    const post = new THREE.Mesh(postGeometry, metalMaterial);
                    post.position.x = Math.cos(angle) * postRadius;
                    post.position.z = Math.sin(angle) * postRadius;
                    post.position.y = y + 0.4;
                    scene.add(post);
                }}
                
                // Seats
                const seatCount = 8 + i * 4;
                for (let j = 0; j < seatCount; j++) {{
                    const angle = (j / seatCount) * Math.PI * 2;
                    const seatRadius = radius + tierDepth / 2;
                    
                    const seatGeometry = new THREE.BoxGeometry(0.6, 0.4, 0.5);
                    const seat = new THREE.Mesh(seatGeometry, darkWoodMaterial);
                    seat.position.x = Math.cos(angle) * seatRadius;
                    seat.position.z = Math.sin(angle) * seatRadius;
                    seat.position.y = y + 0.3;
                    seat.rotation.y = -angle + Math.PI / 2;
                    seat.castShadow = true;
                    scene.add(seat);
                }}
            }}
            
            // Back wall
            const wallGeometry = new THREE.CylinderGeometry(
                innerRadius + tierCount * tierDepth + 1,
                innerRadius + tierCount * tierDepth + 1,
                tierCount * tierHeight + 4,
                32, 1, true
            );
            const wallMaterial = new THREE.MeshLambertMaterial({{
                color: {to_hex(c["wood_dark"])},
                side: THREE.BackSide
            }});
            const wall = new THREE.Mesh(wallGeometry, wallMaterial);
            wall.position.y = (tierCount * tierHeight) / 2;
            scene.add(wall);
            
            // ========================================
            // DISSECTION TABLE
            // ========================================
            
            // Table legs
            const legGeometry = new THREE.CylinderGeometry(0.08, 0.08, 0.8, 8);
            const legPositions = [[-0.8, -0.3], [0.8, -0.3], [-0.8, 0.3], [0.8, 0.3]];
            legPositions.forEach(pos => {{
                const leg = new THREE.Mesh(legGeometry, metalMaterial);
                leg.position.set(pos[0], 0.4, pos[1]);
                scene.add(leg);
            }});
            
            // Table top
            const tableTopGeometry = new THREE.BoxGeometry(2.5, 0.1, 1);
            const tableTop = new THREE.Mesh(tableTopGeometry, metalMaterial);
            tableTop.position.y = 0.85;
            tableTop.receiveShadow = true;
            tableTop.castShadow = true;
            scene.add(tableTop);
            
            // The Subject (body shape with cloth)
            const bodyGroup = new THREE.Group();
            
            // Simple body form
            const torsoGeometry = new THREE.BoxGeometry(1.4, 0.25, 0.5);
            const torso = new THREE.Mesh(torsoGeometry, clothMaterial);
            torso.position.y = 1.05;
            bodyGroup.add(torso);
            
            // Head
            const headGeometry = new THREE.SphereGeometry(0.15, 16, 16);
            const head = new THREE.Mesh(headGeometry, clothMaterial);
            head.position.set(-0.85, 1.1, 0);
            bodyGroup.add(head);
            
            // Legs shape
            const legsGeometry = new THREE.BoxGeometry(0.8, 0.15, 0.4);
            const legs = new THREE.Mesh(legsGeometry, clothMaterial);
            legs.position.set(0.5, 1.0, 0);
            bodyGroup.add(legs);
            
            scene.add(bodyGroup);
            
            // Instrument tray
            const trayGeometry = new THREE.BoxGeometry(0.5, 0.03, 0.25);
            const tray = new THREE.Mesh(trayGeometry, metalMaterial);
            tray.position.set(1.6, 0.9, 0);
            scene.add(tray);
            
            // ========================================
            // GASLIGHTS
            // ========================================
            
            const gaslights = [];
            const gaslightCount = 8;
            const glightRadius = innerRadius + tierCount * tierDepth - 0.5;
            
            for (let i = 0; i < gaslightCount; i++) {{
                const angle = (i / gaslightCount) * Math.PI * 2;
                
                // Lamp fixture
                const fixtureGeometry = new THREE.CylinderGeometry(0.15, 0.2, 0.3, 8);
                const fixture = new THREE.Mesh(fixtureGeometry, metalMaterial);
                fixture.position.x = Math.cos(angle) * glightRadius;
                fixture.position.z = Math.sin(angle) * glightRadius;
                fixture.position.y = tierCount * tierHeight;
                scene.add(fixture);
                
                // Light
                const light = new THREE.PointLight({to_hex(c["light_color"])}, {c["light_intensity"] * 0.5}, 12);
                light.position.copy(fixture.position);
                light.position.y -= 0.2;
                scene.add(light);
                gaslights.push(light);
                
                // Glow
                const glowGeometry = new THREE.SphereGeometry(0.1, 8, 8);
                const glowMaterial = new THREE.MeshBasicMaterial({{
                    color: {to_hex(c["light_color"])},
                    transparent: true,
                    opacity: 0.9
                }});
                const glow = new THREE.Mesh(glowGeometry, glowMaterial);
                glow.position.copy(light.position);
                scene.add(glow);
            }}
            
            // ========================================
            // DUST PARTICLES
            // ========================================
            
            const particleCount = {particle_count};
            const particleGeometry = new THREE.BufferGeometry();
            const particlePositions = new Float32Array(particleCount * 3);
            
            for (let i = 0; i < particleCount; i++) {{
                particlePositions[i * 3] = (Math.random() - 0.5) * 25;
                particlePositions[i * 3 + 1] = Math.random() * 12;
                particlePositions[i * 3 + 2] = (Math.random() - 0.5) * 25;
            }}
            
            particleGeometry.setAttribute('position', new THREE.BufferAttribute(particlePositions, 3));
            
            const particleMaterial = new THREE.PointsMaterial({{
                color: {to_hex(c["particle_color"])},
                size: 0.08,
                transparent: true,
                opacity: 0.5
            }});
            
            const particles = new THREE.Points(particleGeometry, particleMaterial);
            scene.add(particles);
            
            // ========================================
            // SPECIMEN CABINETS
            // ========================================
            
            const cabinetPositions = [
                {{ x: -3.5, z: 3.5 }},
                {{ x: 3.5, z: 3.5 }},
                {{ x: -3.5, z: -3.5 }},
                {{ x: 3.5, z: -3.5 }}
            ];
            
            cabinetPositions.forEach(pos => {{
                const cabinetGeometry = new THREE.BoxGeometry(0.8, 1.2, 0.4);
                const cabinet = new THREE.Mesh(cabinetGeometry, darkWoodMaterial);
                cabinet.position.set(pos.x, 0.6, pos.z);
                cabinet.lookAt(0, 0.6, 0);
                cabinet.castShadow = true;
                scene.add(cabinet);
            }});
            
            // ========================================
            // CAMERA CONTROLS
            // ========================================
            
            let isDragging = false;
            let prevMouse = {{ x: 0, y: 0 }};
            let spherical = {{ radius: 20, theta: Math.PI / 4, phi: Math.PI / 3 }};
            
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
                if (!isDragging) return;
                const dx = e.clientX - prevMouse.x;
                const dy = e.clientY - prevMouse.y;
                spherical.theta -= dx * 0.01;
                spherical.phi = Math.max(0.3, Math.min(1.4, spherical.phi + dy * 0.01));
                prevMouse = {{ x: e.clientX, y: e.clientY }};
                updateCamera();
            }});
            
            window.addEventListener('mouseup', () => {{ isDragging = false; }});
            
            renderer.domElement.addEventListener('wheel', e => {{
                e.preventDefault();
                spherical.radius = Math.max(10, Math.min(35, spherical.radius + e.deltaY * 0.05));
                updateCamera();
            }}, {{ passive: false }});
            
            // Touch support
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
                spherical.theta -= dx * 0.01;
                spherical.phi = Math.max(0.3, Math.min(1.4, spherical.phi + dy * 0.01));
                prevMouse = {{ x: e.touches[0].clientX, y: e.touches[0].clientY }};
                updateCamera();
            }});
            
            renderer.domElement.addEventListener('touchend', () => {{ isDragging = false; }});
            
            updateCamera();
            
            // ========================================
            // QUOTES
            // ========================================
            
            const quotes = [
                "The theatre is full tonight...",
                "They have come to see inside the human form.",
                "What secrets does the flesh conceal?",
                "The blade reveals what words cannot.",
                "Every cut is a question.",
                "The Society watches. The Society waits."
            ];
            
            let quoteIndex = 0;
            const quoteEl = document.getElementById('quote');
            
            function showQuote() {{
                quoteEl.textContent = quotes[quoteIndex];
                quoteEl.style.opacity = 1;
                setTimeout(() => {{ quoteEl.style.opacity = 0; }}, 4000);
                quoteIndex = (quoteIndex + 1) % quotes.length;
            }}
            
            setTimeout(showQuote, 3000);
            setInterval(showQuote, 12000);
            
            // ========================================
            // ANIMATION
            // ========================================
            
            const clock = new THREE.Clock();
            
            function animate() {{
                requestAnimationFrame(animate);
                
                const t = clock.getElapsedTime();
                
                // Flicker gaslights
                gaslights.forEach((light, i) => {{
                    const flicker = Math.sin(t * 12 + i * 2) * {flicker_intensity} +
                                   Math.sin(t * 27 + i * 3) * {flicker_intensity * 0.5};
                    light.intensity = {c["light_intensity"] * 0.5} * (1 + flicker);
                }});
                
                // Float particles
                const pos = particles.geometry.attributes.position.array;
                for (let i = 0; i < particleCount; i++) {{
                    pos[i * 3 + 1] += 0.003;
                    if (pos[i * 3 + 1] > 12) pos[i * 3 + 1] = 0;
                }}
                particles.geometry.attributes.position.needsUpdate = true;
                
                // Auto-rotate
                if (!isDragging) {{
                    spherical.theta += 0.001;
                    updateCamera();
                }}
                
                renderer.render(scene, camera);
            }}
            
            // ========================================
            // RESIZE
            // ========================================
            
            window.addEventListener('resize', () => {{
                const w = container.clientWidth || window.innerWidth;
                const h = container.clientHeight || window.innerHeight;
                camera.aspect = w / h;
                camera.updateProjectionMatrix();
                renderer.setSize(w, h);
            }});
            
            // Hide loading, start animation
            loadingEl.style.display = 'none';
            animate();
            
        }} catch (err) {{
            showError(err.message || 'Unknown error occurred');
        }}
    }})();
    </script>
</body>
</html>
'''
    return html
