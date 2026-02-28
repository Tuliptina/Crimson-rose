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
            "ambient": "0x2a1a0a",
            "background": "0x1a1410",
            "wood": "0x4a3520",
            "wood_dark": "0x2c1810",
            "metal": "0xb8860b",
            "cloth": "0xf5f5dc",
            "light_color": "0xffaa44",
            "light_intensity": 1.5,
            "fog_color": "0x1a1410",
            "fog_near": 5,
            "fog_far": 50,
            "particle_color": "0xffcc88"
        },
        "gothic": {
            "ambient": "0x1a0505",
            "background": "0x0a0a0a",
            "wood": "0x2a1515",
            "wood_dark": "0x1a0a0a",
            "metal": "0x4a4a4a",
            "cloth": "0x8b0000",
            "light_color": "0xff2200",
            "light_intensity": 2.0,
            "fog_color": "0x0a0000",
            "fog_near": 3,
            "fog_far": 35,
            "particle_color": "0xff4444"
        },
        "clinical": {
            "ambient": "0x404040",
            "background": "0xf0f0f0",
            "wood": "0xe0e0e0",
            "wood_dark": "0xcccccc",
            "metal": "0xaaaaaa",
            "cloth": "0xffffff",
            "light_color": "0xffffff",
            "light_intensity": 2.5,
            "fog_color": "0xf0f0f0",
            "fog_near": 20,
            "fog_far": 100,
            "particle_color": "0xcccccc"
        }
    }
    
    c = colors.get(mode, colors["gaslight"])
    
    # Intensity affects fog density and particle count
    fog_multiplier = 1 + (intensity - 1) * 0.2
    particle_count = 100 + intensity * 50
    flicker_intensity = 0.1 + intensity * 0.05
    
    html = f'''
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            overflow: hidden; 
            background: #{c["background"][2:]};
            font-family: 'Georgia', serif;
        }}
        #container {{ 
            width: 100%; 
            height: 100vh; 
            position: relative;
        }}
        #info {{
            position: absolute;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            color: {'#d4a574' if mode == 'gaslight' else '#cc0000' if mode == 'gothic' else '#2f4f4f'};
            font-size: 14px;
            text-align: center;
            pointer-events: none;
            text-shadow: 0 0 10px rgba(0,0,0,0.8);
            opacity: 0.8;
        }}
        #mode-label {{
            position: absolute;
            top: 20px;
            left: 20px;
            color: {'#d4a574' if mode == 'gaslight' else '#cc0000' if mode == 'gothic' else '#2f4f4f'};
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 3px;
            opacity: 0.6;
        }}
        #quote {{
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            color: {'#d4a574' if mode == 'gaslight' else '#cc0000' if mode == 'gothic' else '#2f4f4f'};
            font-size: 18px;
            font-style: italic;
            text-align: center;
            max-width: 500px;
            opacity: 0;
            transition: opacity 2s;
            pointer-events: none;
            text-shadow: 0 0 20px rgba(0,0,0,0.9);
        }}
        .vignette {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            background: radial-gradient(ellipse at center, transparent 40%, rgba(0,0,0,{'0.7' if mode != 'clinical' else '0.2'}) 100%);
        }}
    </style>
</head>
<body>
    <div id="container"></div>
    <div class="vignette"></div>
    <div id="mode-label">{mode.upper()} MODE</div>
    <div id="info">🖱️ Drag to orbit • Scroll to zoom • Click objects to examine</div>
    <div id="quote"></div>
    
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script>
        // ========================================
        // SCENE SETUP
        // ========================================
        
        const container = document.getElementById('container');
        const scene = new THREE.Scene();
        scene.background = new THREE.Color({c["background"]});
        scene.fog = new THREE.Fog({c["fog_color"]}, {c["fog_near"] / fog_multiplier}, {c["fog_far"] / fog_multiplier});
        
        const camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 1000);
        camera.position.set(12, 8, 12);
        camera.lookAt(0, 2, 0);
        
        const renderer = new THREE.WebGLRenderer({{ antialias: true, alpha: true }});
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        renderer.shadowMap.enabled = true;
        renderer.shadowMap.type = THREE.PCFSoftShadowMap;
        container.appendChild(renderer.domElement);
        
        // ========================================
        // MATERIALS
        // ========================================
        
        const woodMaterial = new THREE.MeshStandardMaterial({{
            color: {c["wood"]},
            roughness: 0.8,
            metalness: 0.1
        }});
        
        const darkWoodMaterial = new THREE.MeshStandardMaterial({{
            color: {c["wood_dark"]},
            roughness: 0.9,
            metalness: 0.05
        }});
        
        const metalMaterial = new THREE.MeshStandardMaterial({{
            color: {c["metal"]},
            roughness: 0.3,
            metalness: 0.8
        }});
        
        const clothMaterial = new THREE.MeshStandardMaterial({{
            color: {c["cloth"]},
            roughness: 0.95,
            metalness: 0,
            side: THREE.DoubleSide
        }});
        
        const stoneMaterial = new THREE.MeshStandardMaterial({{
            color: 0x555555,
            roughness: 0.95,
            metalness: 0
        }});
        
        // ========================================
        // THEATRE STRUCTURE
        // ========================================
        
        // Floor
        const floorGeometry = new THREE.CircleGeometry(20, 64);
        const floor = new THREE.Mesh(floorGeometry, stoneMaterial);
        floor.rotation.x = -Math.PI / 2;
        floor.receiveShadow = true;
        scene.add(floor);
        
        // Central pit floor (slightly lower)
        const pitGeometry = new THREE.CircleGeometry(4, 32);
        const pitMaterial = new THREE.MeshStandardMaterial({{
            color: 0x333333,
            roughness: 1
        }});
        const pit = new THREE.Mesh(pitGeometry, pitMaterial);
        pit.rotation.x = -Math.PI / 2;
        pit.position.y = -0.05;
        pit.receiveShadow = true;
        scene.add(pit);
        
        // Gallery tiers (5 levels)
        const tierCount = 5;
        const tierHeight = 1.2;
        const tierDepth = 2;
        const innerRadius = 5;
        
        for (let i = 0; i < tierCount; i++) {{
            const radius = innerRadius + i * tierDepth;
            const y = i * tierHeight;
            
            // Tier platform
            const tierGeometry = new THREE.RingGeometry(radius, radius + tierDepth - 0.1, 32, 1);
            const tier = new THREE.Mesh(tierGeometry, woodMaterial);
            tier.rotation.x = -Math.PI / 2;
            tier.position.y = y;
            tier.receiveShadow = true;
            tier.castShadow = true;
            scene.add(tier);
            
            // Tier front (vertical face)
            const frontGeometry = new THREE.CylinderGeometry(radius + tierDepth, radius + tierDepth, tierHeight, 32, 1, true);
            const front = new THREE.Mesh(frontGeometry, darkWoodMaterial);
            front.position.y = y - tierHeight / 2;
            scene.add(front);
            
            // Railing
            const railGeometry = new THREE.TorusGeometry(radius + 0.1, 0.05, 8, 64);
            const rail = new THREE.Mesh(railGeometry, metalMaterial);
            rail.rotation.x = Math.PI / 2;
            rail.position.y = y + 0.8;
            scene.add(rail);
            
            // Seats (simplified as boxes)
            const seatCount = 12 + i * 4;
            for (let j = 0; j < seatCount; j++) {{
                const angle = (j / seatCount) * Math.PI * 2;
                const seatRadius = radius + tierDepth / 2;
                
                const seatGeometry = new THREE.BoxGeometry(0.5, 0.4, 0.4);
                const seat = new THREE.Mesh(seatGeometry, darkWoodMaterial);
                seat.position.x = Math.cos(angle) * seatRadius;
                seat.position.z = Math.sin(angle) * seatRadius;
                seat.position.y = y + 0.2;
                seat.rotation.y = -angle + Math.PI / 2;
                seat.castShadow = true;
                scene.add(seat);
            }}
        }}
        
        // Back wall (dome suggestion)
        const wallGeometry = new THREE.CylinderGeometry(innerRadius + tierCount * tierDepth + 1, innerRadius + tierCount * tierDepth + 1, tierCount * tierHeight + 4, 32, 1, true);
        const wallMaterial = new THREE.MeshStandardMaterial({{
            color: {c["wood_dark"]},
            roughness: 0.95,
            side: THREE.BackSide
        }});
        const wall = new THREE.Mesh(wallGeometry, wallMaterial);
        wall.position.y = (tierCount * tierHeight) / 2;
        scene.add(wall);
        
        // Dome ceiling
        const domeGeometry = new THREE.SphereGeometry(innerRadius + tierCount * tierDepth + 1, 32, 16, 0, Math.PI * 2, 0, Math.PI / 2);
        const dome = new THREE.Mesh(domeGeometry, wallMaterial);
        dome.position.y = tierCount * tierHeight + 2;
        scene.add(dome);
        
        // ========================================
        // DISSECTION TABLE
        // ========================================
        
        // Table base
        const tableBaseGeometry = new THREE.BoxGeometry(1, 0.8, 0.6);
        const tableBase = new THREE.Mesh(tableBaseGeometry, metalMaterial);
        tableBase.position.y = 0.4;
        tableBase.castShadow = true;
        scene.add(tableBase);
        
        // Table top
        const tableTopGeometry = new THREE.BoxGeometry(2.5, 0.1, 1);
        const tableTop = new THREE.Mesh(tableTopGeometry, metalMaterial);
        tableTop.position.y = 0.85;
        tableTop.receiveShadow = true;
        tableTop.castShadow = true;
        scene.add(tableTop);
        
        // Drainage channels
        const channelGeometry = new THREE.BoxGeometry(2.6, 0.02, 0.05);
        const channel1 = new THREE.Mesh(channelGeometry, metalMaterial);
        channel1.position.set(0, 0.86, 0.3);
        scene.add(channel1);
        const channel2 = new THREE.Mesh(channelGeometry, metalMaterial);
        channel2.position.set(0, 0.86, -0.3);
        scene.add(channel2);
        
        // The Subject (draped cloth over body shape)
        const bodyGroup = new THREE.Group();
        
        // Body form underneath
        const torsoGeometry = new THREE.CapsuleGeometry(0.25, 1.2, 8, 16);
        const torso = new THREE.Mesh(torsoGeometry, clothMaterial);
        torso.rotation.z = Math.PI / 2;
        torso.position.y = 1.1;
        bodyGroup.add(torso);
        
        // Head
        const headGeometry = new THREE.SphereGeometry(0.18, 16, 16);
        const head = new THREE.Mesh(headGeometry, clothMaterial);
        head.position.set(-0.9, 1.15, 0);
        bodyGroup.add(head);
        
        // Draping cloth
        const clothGeometry = new THREE.PlaneGeometry(2.2, 1.2, 20, 20);
        // Deform cloth vertices for draping effect
        const clothVertices = clothGeometry.attributes.position.array;
        for (let i = 0; i < clothVertices.length; i += 3) {{
            const x = clothVertices[i];
            const z = clothVertices[i + 1];
            // Create body-shaped bump
            const distFromCenter = Math.sqrt(x * x + z * z * 4);
            clothVertices[i + 2] = Math.max(0, 0.3 - distFromCenter * 0.3) + Math.sin(x * 5) * 0.02;
        }}
        clothGeometry.computeVertexNormals();
        
        const cloth = new THREE.Mesh(clothGeometry, clothMaterial);
        cloth.rotation.x = -Math.PI / 2;
        cloth.position.y = 1.0;
        cloth.castShadow = true;
        cloth.receiveShadow = true;
        bodyGroup.add(cloth);
        
        scene.add(bodyGroup);
        
        // Instrument tray
        const trayGeometry = new THREE.BoxGeometry(0.6, 0.05, 0.3);
        const tray = new THREE.Mesh(trayGeometry, metalMaterial);
        tray.position.set(1.5, 1.0, 0);
        scene.add(tray);
        
        // Instruments (simplified)
        const instrumentGeometry = new THREE.CylinderGeometry(0.01, 0.01, 0.2, 8);
        for (let i = 0; i < 5; i++) {{
            const instrument = new THREE.Mesh(instrumentGeometry, metalMaterial);
            instrument.position.set(1.35 + i * 0.08, 1.05, 0);
            instrument.rotation.z = Math.PI / 2 + (Math.random() - 0.5) * 0.2;
            scene.add(instrument);
        }}
        
        // ========================================
        // GASLIGHTS
        // ========================================
        
        const gaslights = [];
        const gaslightCount = 8;
        
        for (let i = 0; i < gaslightCount; i++) {{
            const angle = (i / gaslightCount) * Math.PI * 2;
            const radius = innerRadius + tierCount * tierDepth - 0.5;
            
            // Lamp bracket
            const bracketGeometry = new THREE.BoxGeometry(0.1, 0.5, 0.1);
            const bracket = new THREE.Mesh(bracketGeometry, metalMaterial);
            bracket.position.x = Math.cos(angle) * radius;
            bracket.position.z = Math.sin(angle) * radius;
            bracket.position.y = tierCount * tierHeight + 1;
            scene.add(bracket);
            
            // Lamp housing
            const housingGeometry = new THREE.CylinderGeometry(0.15, 0.2, 0.3, 8);
            const housing = new THREE.Mesh(housingGeometry, metalMaterial);
            housing.position.x = Math.cos(angle) * radius;
            housing.position.z = Math.sin(angle) * radius;
            housing.position.y = tierCount * tierHeight + 0.6;
            scene.add(housing);
            
            // Light source
            const light = new THREE.PointLight({c["light_color"]}, {c["light_intensity"]}, 15, 2);
            light.position.x = Math.cos(angle) * radius;
            light.position.z = Math.sin(angle) * radius;
            light.position.y = tierCount * tierHeight + 0.5;
            light.castShadow = true;
            light.shadow.mapSize.width = 512;
            light.shadow.mapSize.height = 512;
            scene.add(light);
            gaslights.push(light);
            
            // Glow sphere
            const glowGeometry = new THREE.SphereGeometry(0.08, 16, 16);
            const glowMaterial = new THREE.MeshBasicMaterial({{
                color: {c["light_color"]},
                transparent: true,
                opacity: 0.8
            }});
            const glow = new THREE.Mesh(glowGeometry, glowMaterial);
            glow.position.copy(light.position);
            scene.add(glow);
        }}
        
        // Central overhead light
        const mainLight = new THREE.SpotLight({c["light_color"]}, {c["light_intensity"] * 1.5}, 20, Math.PI / 4, 0.5, 2);
        mainLight.position.set(0, tierCount * tierHeight + 3, 0);
        mainLight.target.position.set(0, 1, 0);
        mainLight.castShadow = true;
        mainLight.shadow.mapSize.width = 1024;
        mainLight.shadow.mapSize.height = 1024;
        scene.add(mainLight);
        scene.add(mainLight.target);
        gaslights.push(mainLight);
        
        // Ambient light
        const ambientLight = new THREE.AmbientLight({c["ambient"]}, 0.3);
        scene.add(ambientLight);
        
        // ========================================
        // DUST PARTICLES
        // ========================================
        
        const particleCount = {particle_count};
        const particleGeometry = new THREE.BufferGeometry();
        const particlePositions = new Float32Array(particleCount * 3);
        const particleSizes = new Float32Array(particleCount);
        
        for (let i = 0; i < particleCount; i++) {{
            particlePositions[i * 3] = (Math.random() - 0.5) * 30;
            particlePositions[i * 3 + 1] = Math.random() * 15;
            particlePositions[i * 3 + 2] = (Math.random() - 0.5) * 30;
            particleSizes[i] = Math.random() * 0.05 + 0.02;
        }}
        
        particleGeometry.setAttribute('position', new THREE.BufferAttribute(particlePositions, 3));
        particleGeometry.setAttribute('size', new THREE.BufferAttribute(particleSizes, 1));
        
        const particleMaterial = new THREE.PointsMaterial({{
            color: {c["particle_color"]},
            size: 0.05,
            transparent: true,
            opacity: 0.4,
            sizeAttenuation: true
        }});
        
        const particles = new THREE.Points(particleGeometry, particleMaterial);
        scene.add(particles);
        
        // ========================================
        // SPECIMEN CABINETS
        // ========================================
        
        const cabinetPositions = [
            {{ x: -3, z: 3, rot: Math.PI / 4 }},
            {{ x: 3, z: 3, rot: -Math.PI / 4 }},
            {{ x: -3, z: -3, rot: -Math.PI / 4 + Math.PI }},
            {{ x: 3, z: -3, rot: Math.PI / 4 + Math.PI }}
        ];
        
        cabinetPositions.forEach(pos => {{
            // Cabinet body
            const cabinetGeometry = new THREE.BoxGeometry(1, 1.5, 0.4);
            const cabinet = new THREE.Mesh(cabinetGeometry, darkWoodMaterial);
            cabinet.position.set(pos.x, 0.75, pos.z);
            cabinet.rotation.y = pos.rot;
            cabinet.castShadow = true;
            scene.add(cabinet);
            
            // Glass front (simplified)
            const glassGeometry = new THREE.PlaneGeometry(0.8, 1.2);
            const glassMaterial = new THREE.MeshStandardMaterial({{
                color: 0x88ccff,
                transparent: true,
                opacity: 0.2,
                roughness: 0.1,
                metalness: 0.9
            }});
            const glass = new THREE.Mesh(glassGeometry, glassMaterial);
            glass.position.set(pos.x + Math.sin(pos.rot) * 0.21, 0.75, pos.z + Math.cos(pos.rot) * 0.21);
            glass.rotation.y = pos.rot;
            scene.add(glass);
            
            // Specimen jars (glowing slightly)
            for (let j = 0; j < 3; j++) {{
                const jarGeometry = new THREE.CylinderGeometry(0.08, 0.08, 0.2, 16);
                const jarMaterial = new THREE.MeshStandardMaterial({{
                    color: {'0x44ff44' if mode == 'gothic' else '0xffffcc'},
                    transparent: true,
                    opacity: 0.5,
                    emissive: {'0x002200' if mode == 'gothic' else '0x111100'},
                    emissiveIntensity: 0.3
                }});
                const jar = new THREE.Mesh(jarGeometry, jarMaterial);
                const offsetX = (j - 1) * 0.25;
                jar.position.set(
                    pos.x + Math.sin(pos.rot) * 0.1 + Math.cos(pos.rot) * offsetX,
                    0.75,
                    pos.z + Math.cos(pos.rot) * 0.1 - Math.sin(pos.rot) * offsetX
                );
                scene.add(jar);
            }}
        }});
        
        // ========================================
        // ORBIT CONTROLS (Manual Implementation)
        // ========================================
        
        let isDragging = false;
        let previousMousePosition = {{ x: 0, y: 0 }};
        let spherical = {{ radius: 18, theta: Math.PI / 4, phi: Math.PI / 3 }};
        
        function updateCamera() {{
            camera.position.x = spherical.radius * Math.sin(spherical.phi) * Math.cos(spherical.theta);
            camera.position.y = spherical.radius * Math.cos(spherical.phi);
            camera.position.z = spherical.radius * Math.sin(spherical.phi) * Math.sin(spherical.theta);
            camera.lookAt(0, 2, 0);
        }}
        
        renderer.domElement.addEventListener('mousedown', (e) => {{
            isDragging = true;
            previousMousePosition = {{ x: e.clientX, y: e.clientY }};
        }});
        
        renderer.domElement.addEventListener('mousemove', (e) => {{
            if (!isDragging) return;
            
            const deltaX = e.clientX - previousMousePosition.x;
            const deltaY = e.clientY - previousMousePosition.y;
            
            spherical.theta -= deltaX * 0.005;
            spherical.phi = Math.max(0.3, Math.min(Math.PI / 2 - 0.1, spherical.phi + deltaY * 0.005));
            
            previousMousePosition = {{ x: e.clientX, y: e.clientY }};
            updateCamera();
        }});
        
        renderer.domElement.addEventListener('mouseup', () => {{ isDragging = false; }});
        renderer.domElement.addEventListener('mouseleave', () => {{ isDragging = false; }});
        
        renderer.domElement.addEventListener('wheel', (e) => {{
            spherical.radius = Math.max(8, Math.min(30, spherical.radius + e.deltaY * 0.02));
            updateCamera();
        }});
        
        // Touch support
        renderer.domElement.addEventListener('touchstart', (e) => {{
            if (e.touches.length === 1) {{
                isDragging = true;
                previousMousePosition = {{ x: e.touches[0].clientX, y: e.touches[0].clientY }};
            }}
        }});
        
        renderer.domElement.addEventListener('touchmove', (e) => {{
            if (!isDragging || e.touches.length !== 1) return;
            
            const deltaX = e.touches[0].clientX - previousMousePosition.x;
            const deltaY = e.touches[0].clientY - previousMousePosition.y;
            
            spherical.theta -= deltaX * 0.005;
            spherical.phi = Math.max(0.3, Math.min(Math.PI / 2 - 0.1, spherical.phi + deltaY * 0.005));
            
            previousMousePosition = {{ x: e.touches[0].clientX, y: e.touches[0].clientY }};
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
            "We are all meat, in the end.",
            "The dead have so much to teach us.",
            "Every cut is a question. Every organ, an answer.",
            "The Society watches. The Society waits."
        ];
        
        let currentQuote = 0;
        const quoteElement = document.getElementById('quote');
        
        function showQuote() {{
            quoteElement.textContent = quotes[currentQuote];
            quoteElement.style.opacity = 1;
            
            setTimeout(() => {{
                quoteElement.style.opacity = 0;
            }}, 4000);
            
            currentQuote = (currentQuote + 1) % quotes.length;
        }}
        
        // Show first quote after 3 seconds
        setTimeout(showQuote, 3000);
        // Then every 15 seconds
        setInterval(showQuote, 15000);
        
        // ========================================
        // ANIMATION LOOP
        // ========================================
        
        const clock = new THREE.Clock();
        
        function animate() {{
            requestAnimationFrame(animate);
            
            const time = clock.getElapsedTime();
            
            // Flickering gaslights
            gaslights.forEach((light, i) => {{
                const flicker = Math.sin(time * 10 + i * 2) * {flicker_intensity} + 
                               Math.sin(time * 23 + i * 3) * {flicker_intensity * 0.5} +
                               Math.sin(time * 37 + i * 5) * {flicker_intensity * 0.25};
                light.intensity = {c["light_intensity"]} * (1 + flicker);
            }});
            
            // Floating dust particles
            const positions = particles.geometry.attributes.position.array;
            for (let i = 0; i < particleCount; i++) {{
                positions[i * 3 + 1] += Math.sin(time + i) * 0.001;
                positions[i * 3] += Math.cos(time * 0.5 + i) * 0.0005;
                
                // Reset particles that float too high
                if (positions[i * 3 + 1] > 15) {{
                    positions[i * 3 + 1] = 0;
                }}
            }}
            particles.geometry.attributes.position.needsUpdate = true;
            
            // Subtle cloth movement (breathing?)
            if (cloth && {'true' if mode == 'gothic' else 'false'}) {{
                const clothVerts = cloth.geometry.attributes.position.array;
                for (let i = 2; i < clothVerts.length; i += 3) {{
                    clothVerts[i] += Math.sin(time * 2 + i * 0.1) * 0.0003;
                }}
                cloth.geometry.attributes.position.needsUpdate = true;
            }}
            
            // Auto-rotate when not dragging
            if (!isDragging) {{
                spherical.theta += 0.0005;
                updateCamera();
            }}
            
            renderer.render(scene, camera);
        }}
        
        // ========================================
        // RESIZE HANDLER
        // ========================================
        
        window.addEventListener('resize', () => {{
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        }});
        
        // Start animation
        animate();
        
    </script>
</body>
</html>
'''
    return html
