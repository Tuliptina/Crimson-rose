"""
🔪 The Dissection Table — SVG Renderer
Hand-crafted SVGs with SMIL animation for the Anatomy Theatre.
Base64-encoded for reliable Streamlit rendering.

Architecture mirrors cabinet_2d_bottles.py:
  - Mode palettes (gaslight / gothic / clinical)
  - Individual SVG renderers per item
  - Composed table scene
  - UV overlay system
  - Base64 encoding for Streamlit
"""

import base64

# =============================================================================
# MODE PALETTES
# =============================================================================

MODE_PALETTES = {
    "gaslight": {
        "marble":       "#8a7d6b",
        "marble_vein":  "#7a6d5b",
        "marble_light": "#9a8d7b",
        "bg":           "#1a1410",
        "bg_dark":      "#0d0a07",
        "channel":      "#6b5a3e",
        "channel_liquid":"#8b6914",
        "accent":       "#d4a574",
        "accent_dim":   "#8b6914",
        "text":         "#d4c4a8",
        "text_dim":     "#a89070",
        "organ_red":    "#8b4040",
        "organ_pink":   "#a06060",
        "organ_dark":   "#5a2020",
        "bone":         "#c8b898",
        "bone_shadow":  "#a09070",
        "steel":        "#9a9a8a",
        "steel_bright": "#d4d4c4",
        "brass":        "#b8963a",
        "brass_dark":   "#8a6a1a",
        "blood_fresh":  "#8b2020",
        "blood_old":    "#3a1a0a",
        "candle_flame": "#e8a020",
        "candle_glow":  "rgba(232,160,32,0.15)",
        "rose":         "#8b2040",
        "rose_bright":  "#c83060",
        "ink":          "#2a1a10",
        "shadow":       "rgba(0,0,0,0.4)",
        "uv_bg":        "rgba(20,0,60,0.85)",
        "uv_glow":      "#7b68ee",
        "uv_text":      "#9370db",
        "uv_bright":    "#b8a9e8",
    },
    "gothic": {
        "marble":       "#2a1a1a",
        "marble_vein":  "#4a0000",
        "marble_light": "#3a2020",
        "bg":           "#0a0a0a",
        "bg_dark":      "#000000",
        "channel":      "#4a0000",
        "channel_liquid":"#8b0000",
        "accent":       "#cc0000",
        "accent_dim":   "#8b0000",
        "text":         "#e8e0d0",
        "text_dim":     "#a09080",
        "organ_red":    "#aa2020",
        "organ_pink":   "#cc3030",
        "organ_dark":   "#6a0000",
        "bone":         "#c0b0a0",
        "bone_shadow":  "#807060",
        "steel":        "#808080",
        "steel_bright": "#c0c0c0",
        "brass":        "#a08030",
        "brass_dark":   "#604010",
        "blood_fresh":  "#cc0000",
        "blood_old":    "#4a0000",
        "candle_flame": "#cc2020",
        "candle_glow":  "rgba(204,0,0,0.12)",
        "rose":         "#cc0000",
        "rose_bright":  "#ff2040",
        "ink":          "#1a0000",
        "shadow":       "rgba(0,0,0,0.6)",
        "uv_bg":        "rgba(10,0,40,0.9)",
        "uv_glow":      "#6a4aee",
        "uv_text":      "#8060cc",
        "uv_bright":    "#a090e8",
    },
    "clinical": {
        "marble":       "#e8e4dc",
        "marble_vein":  "#d8d4cc",
        "marble_light": "#f5f2ec",
        "bg":           "#f5f5f0",
        "bg_dark":      "#e0e0d8",
        "channel":      "#c0c0b0",
        "channel_liquid":"#d0d0c8",
        "accent":       "#2f4f4f",
        "accent_dim":   "#5f7f7f",
        "text":         "#1a1a1a",
        "text_dim":     "#4a4a4a",
        "organ_red":    "#c06060",
        "organ_pink":   "#d89090",
        "organ_dark":   "#904040",
        "bone":         "#e0d8c8",
        "bone_shadow":  "#c0b8a8",
        "steel":        "#b0b0b0",
        "steel_bright": "#e0e0e0",
        "brass":        "#c0a060",
        "brass_dark":   "#a08040",
        "blood_fresh":  "#c04040",
        "blood_old":    "#804040",
        "candle_flame": "#2f4f4f",
        "candle_glow":  "rgba(47,79,79,0.05)",
        "rose":         "#c04060",
        "rose_bright":  "#e06080",
        "ink":          "#1a1a1a",
        "shadow":       "rgba(0,0,0,0.08)",
        "uv_bg":        "rgba(20,0,60,0.85)",
        "uv_glow":      "#7b68ee",
        "uv_text":      "#9370db",
        "uv_bright":    "#b8a9e8",
    }
}


def get_palette(mode: str) -> dict:
    return MODE_PALETTES.get(mode, MODE_PALETTES["gaslight"])


# =============================================================================
# BASE64 ENCODING
# =============================================================================

def svg_to_base64_img(svg_str: str, width: str = "100%") -> str:
    """Encode an SVG string to a base64 <img> tag for Streamlit rendering."""
    b64 = base64.b64encode(svg_str.encode("utf-8")).decode("utf-8")
    return f'<img src="data:image/svg+xml;base64,{b64}" style="width:{width}; display:block;">'


# =============================================================================
# TABLE BASE — Marble slab with drainage channels
# =============================================================================

def svg_table_base(p: dict, uv: bool = False, intensity: int = 2) -> str:
    """The marble dissection table surface with drainage channels and atmosphere."""
    # Marble veining pattern
    veins = f'''
        <path d="M120,80 Q200,120 180,200 T250,350 Q300,400 350,380 T500,450"
              stroke="{p['marble_vein']}" stroke-width="1.2" fill="none" opacity="0.4"/>
        <path d="M400,70 Q450,150 430,250 T500,300 Q600,320 650,280 T780,350"
              stroke="{p['marble_vein']}" stroke-width="0.8" fill="none" opacity="0.3"/>
        <path d="M200,400 Q300,380 400,420 T600,450 Q700,400 750,440"
              stroke="{p['marble_vein']}" stroke-width="1" fill="none" opacity="0.35"/>
        <path d="M100,250 Q150,230 200,260 T350,240 Q400,250 420,230"
              stroke="{p['marble_vein']}" stroke-width="0.6" fill="none" opacity="0.25"/>
        <path d="M550,100 Q600,130 580,180 T620,280 Q650,320 700,300"
              stroke="{p['marble_vein']}" stroke-width="0.7" fill="none" opacity="0.3"/>
    '''

    # Drainage channels with animated liquid
    liquid_anim_dur = "12s" if intensity <= 3 else "8s"
    channels = f'''
        <!-- Main perimeter channel -->
        <rect x="60" y="60" width="780" height="480" rx="6" ry="6"
              fill="none" stroke="{p['channel']}" stroke-width="4" opacity="0.5"/>
        <!-- Cross channels -->
        <line x1="450" y1="65" x2="450" y2="535" stroke="{p['channel']}" stroke-width="3" opacity="0.35"/>
        <line x1="65" y1="300" x2="835" y2="300" stroke="{p['channel']}" stroke-width="2" opacity="0.25"/>
        <!-- Drainage basin at bottom -->
        <ellipse cx="450" cy="545" rx="40" ry="10" fill="{p['channel']}" opacity="0.4"/>
        <!-- Animated liquid creep in channels -->
        <line x1="60" y1="62" x2="60" y2="540" stroke="{p['channel_liquid']}" stroke-width="2" opacity="0">
            <animate attributeName="opacity" values="0;0.5;0.3;0" dur="{liquid_anim_dur}" repeatCount="indefinite"/>
            <animate attributeName="y2" values="62;540;540;62" dur="{liquid_anim_dur}" repeatCount="indefinite"/>
        </line>
        <line x1="840" y1="540" x2="840" y2="62" stroke="{p['channel_liquid']}" stroke-width="2" opacity="0">
            <animate attributeName="opacity" values="0;0;0.4;0.2;0" dur="{liquid_anim_dur}" begin="3s" repeatCount="indefinite"/>
        </line>
    '''

    # Condensation shimmer
    shimmer = f'''
        <rect x="55" y="55" width="790" height="490" rx="8" fill="url(#shimmer_grad)" opacity="0.08">
            <animate attributeName="opacity" values="0.04;0.1;0.06;0.08;0.04" dur="7s" repeatCount="indefinite"/>
        </rect>
    '''

    # UV overlay elements
    uv_layer = ""
    if uv:
        uv_layer = f'''
        <rect x="50" y="50" width="800" height="500" rx="8" fill="{p['uv_bg']}" opacity="0.88"/>
        <!-- Chemical stains -->
        <circle cx="300" cy="250" r="40" fill="{p['uv_glow']}" opacity="0.08"/>
        <circle cx="550" cy="200" r="30" fill="{p['uv_glow']}" opacity="0.06"/>
        <circle cx="400" cy="400" r="35" fill="{p['uv_glow']}" opacity="0.07"/>
        <!-- Rose symbol burned into center -->
        <g transform="translate(450,300)" opacity="0.25">
            <ellipse cx="0" cy="-8" rx="12" ry="10" fill="none" stroke="{p['uv_bright']}" stroke-width="1"/>
            <ellipse cx="-8" cy="2" rx="10" ry="12" fill="none" stroke="{p['uv_bright']}" stroke-width="1" transform="rotate(-30)"/>
            <ellipse cx="8" cy="2" rx="10" ry="12" fill="none" stroke="{p['uv_bright']}" stroke-width="1" transform="rotate(30)"/>
            <line x1="0" y1="10" x2="0" y2="35" stroke="{p['uv_bright']}" stroke-width="1.5"/>
            <animate attributeName="opacity" values="0.15;0.3;0.15" dur="4s" repeatCount="indefinite"/>
        </g>
        <!-- Hidden text -->
        <text x="450" y="510" text-anchor="middle" fill="{p['uv_text']}" font-size="9"
              font-family="serif" font-style="italic" opacity="0.5">
            THE WARREN PROTOCOL CONTINUES
            <animate attributeName="opacity" values="0.3;0.6;0.3" dur="5s" repeatCount="indefinite"/>
        </text>
        <!-- Fingerprints on table edge -->
        <g opacity="0.2">
            <circle cx="200" cy="540" r="6" fill="none" stroke="{p['uv_glow']}" stroke-width="0.5"/>
            <circle cx="200" cy="540" r="4" fill="none" stroke="{p['uv_glow']}" stroke-width="0.5"/>
            <circle cx="200" cy="540" r="2" fill="none" stroke="{p['uv_glow']}" stroke-width="0.5"/>
            <circle cx="215" cy="538" r="5" fill="none" stroke="{p['uv_glow']}" stroke-width="0.5"/>
        </g>
        '''

    return f'''
    <!-- TABLE BASE -->
    <defs>
        <linearGradient id="shimmer_grad" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0%" stop-color="{p['marble_light']}" stop-opacity="0"/>
            <stop offset="50%" stop-color="{p['marble_light']}" stop-opacity="1"/>
            <stop offset="100%" stop-color="{p['marble_light']}" stop-opacity="0"/>
            <animate attributeName="x1" values="-1;1" dur="6s" repeatCount="indefinite"/>
            <animate attributeName="x2" values="0;2" dur="6s" repeatCount="indefinite"/>
        </linearGradient>
        <radialGradient id="candle_light" cx="0.12" cy="0.15">
            <stop offset="0%" stop-color="{p['candle_flame']}" stop-opacity="0.15"/>
            <stop offset="60%" stop-color="{p['candle_flame']}" stop-opacity="0.03"/>
            <stop offset="100%" stop-color="{p['candle_flame']}" stop-opacity="0"/>
        </radialGradient>
        <filter id="soft_glow">
            <feGaussianBlur stdDeviation="2" result="blur"/>
            <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
        </filter>
        <filter id="uv_glow_filter">
            <feGaussianBlur stdDeviation="3" result="blur"/>
            <feMerge><feMergeNode in="blur"/><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
        </filter>
    </defs>
    <!-- Table shadow -->
    <rect x="56" y="56" width="800" height="500" rx="10" fill="{p['shadow']}" opacity="0.5"/>
    <!-- Main marble slab -->
    <rect x="50" y="50" width="800" height="500" rx="8"
          fill="{p['marble']}" stroke="{p['accent_dim']}" stroke-width="1.5"/>
    <!-- Marble veining -->
    {veins}
    <!-- Candle light cone (gaslight/gothic only) -->
    <rect x="50" y="50" width="800" height="500" rx="8" fill="url(#candle_light)"/>
    <!-- Drainage system -->
    {channels}
    <!-- Condensation -->
    {shimmer}
    <!-- Section divider labels -->
    <text x="225" y="90" text-anchor="middle" fill="{p['text_dim']}" font-size="10"
          font-family="serif" letter-spacing="3" opacity="0.5">ORGANS</text>
    <text x="675" y="90" text-anchor="middle" fill="{p['text_dim']}" font-size="10"
          font-family="serif" letter-spacing="3" opacity="0.5">INSTRUMENTS</text>
    {uv_layer}
    '''


# =============================================================================
# ORGAN SVGs
# =============================================================================

def svg_heart(p: dict, x: int, y: int, uv: bool = False) -> str:
    """Anatomical heart with double-throb SMIL animation."""
    uv_marks = ""
    if uv:
        uv_marks = f'''
            <circle cx="0" cy="-5" r="2" fill="{p['uv_glow']}" opacity="0.8" filter="url(#uv_glow_filter)"/>
            <circle cx="-4" cy="2" r="1.5" fill="{p['uv_glow']}" opacity="0.7" filter="url(#uv_glow_filter)"/>
            <circle cx="5" cy="-2" r="1.8" fill="{p['uv_glow']}" opacity="0.6" filter="url(#uv_glow_filter)"/>
            <text x="0" y="35" text-anchor="middle" fill="{p['uv_text']}" font-size="5" opacity="0.6">INJ. SITES</text>
        '''
    return f'''
    <g transform="translate({x},{y})">
        <!-- Dish -->
        <ellipse cx="0" cy="20" rx="35" ry="8" fill="{p['marble_light']}" stroke="{p['accent_dim']}" stroke-width="0.8" opacity="0.6"/>
        <ellipse cx="0" cy="18" rx="30" ry="5" fill="{p['channel_liquid']}" opacity="0.2"/>
        <!-- Heart with lub-dub animation -->
        <g>
            <animateTransform attributeName="transform" type="scale"
                values="1,1; 1.06,1.04; 1,1; 1.03,1.02; 1,1"
                dur="1.2s" repeatCount="indefinite" additive="sum"/>
            <!-- Main heart shape -->
            <path d="M0,-12 C-6,-22 -22,-20 -22,-8 C-22,4 -8,14 0,22 C8,14 22,4 22,-8 C22,-20 6,-22 0,-12Z"
                  fill="{p['organ_red']}" stroke="{p['organ_dark']}" stroke-width="1"/>
            <!-- Aorta -->
            <path d="M0,-12 C-2,-18 -4,-26 -8,-30 Q-10,-34 -6,-36"
                  fill="none" stroke="{p['organ_dark']}" stroke-width="2.5" stroke-linecap="round"/>
            <path d="M0,-12 C2,-18 6,-24 10,-26 Q14,-28 16,-24"
                  fill="none" stroke="{p['organ_dark']}" stroke-width="2" stroke-linecap="round"/>
            <!-- Surface detail -->
            <path d="M-10,-4 Q-5,0 -2,6" fill="none" stroke="{p['organ_pink']}" stroke-width="0.6" opacity="0.5"/>
            <path d="M8,-2 Q4,4 2,10" fill="none" stroke="{p['organ_pink']}" stroke-width="0.5" opacity="0.4"/>
            <!-- Ventricle line -->
            <path d="M0,-8 L0,16" fill="none" stroke="{p['organ_dark']}" stroke-width="0.5" opacity="0.4"/>
        </g>
        <!-- Trailing vessels -->
        <path d="M-24,-6 Q-34,-4 -38,2" fill="none" stroke="{p['organ_dark']}" stroke-width="1.5" opacity="0.5" stroke-linecap="round"/>
        <path d="M24,-6 Q32,0 36,8" fill="none" stroke="{p['organ_dark']}" stroke-width="1.2" opacity="0.4" stroke-linecap="round"/>
        {uv_marks}
    </g>
    '''


def svg_brain(p: dict, x: int, y: int, uv: bool = False) -> str:
    """Brain from above with electrical pulse SMIL animation."""
    uv_annotations = ""
    if uv:
        uv_annotations = f'''
            <text x="-20" y="-18" fill="{p['uv_text']}" font-size="4" font-style="italic" opacity="0.7">seat of mania?</text>
            <text x="8" y="15" fill="{p['uv_text']}" font-size="4" font-style="italic" opacity="0.6">CUT HERE</text>
            <line x1="5" y1="17" x2="20" y2="12" stroke="{p['uv_glow']}" stroke-width="0.5" opacity="0.5"/>
            <text x="-25" y="8" fill="{p['uv_text']}" font-size="3.5" opacity="0.5">temporal adhesion</text>
        '''
    return f'''
    <g transform="translate({x},{y})">
        <!-- Glass plate -->
        <ellipse cx="0" cy="2" rx="38" ry="28" fill="{p['marble_light']}" stroke="{p['steel']}" stroke-width="0.5" opacity="0.4"/>
        <!-- Brain mass — left hemisphere -->
        <path d="M-2,-20 C-12,-22 -28,-18 -30,-8 C-32,2 -28,14 -18,18 C-10,22 -4,20 -2,15"
              fill="{p['organ_pink']}" stroke="{p['organ_red']}" stroke-width="0.8"/>
        <!-- Brain mass — right hemisphere -->
        <path d="M2,-20 C12,-22 28,-18 30,-8 C32,2 28,14 18,18 C10,22 4,20 2,15"
              fill="{p['organ_pink']}" stroke="{p['organ_red']}" stroke-width="0.8"/>
        <!-- Central fissure -->
        <path d="M0,-22 L0,18" fill="none" stroke="{p['organ_dark']}" stroke-width="1" opacity="0.6"/>
        <!-- Sulci (left) -->
        <path d="M-6,-14 Q-14,-12 -22,-8" fill="none" stroke="{p['organ_dark']}" stroke-width="0.5" opacity="0.4"/>
        <path d="M-4,-6 Q-12,-4 -24,0" fill="none" stroke="{p['organ_dark']}" stroke-width="0.5" opacity="0.4"/>
        <path d="M-4,2 Q-10,6 -20,10" fill="none" stroke="{p['organ_dark']}" stroke-width="0.5" opacity="0.35"/>
        <path d="M-6,10 Q-12,14 -16,16" fill="none" stroke="{p['organ_dark']}" stroke-width="0.5" opacity="0.3"/>
        <!-- Sulci (right) -->
        <path d="M6,-14 Q14,-12 22,-8" fill="none" stroke="{p['organ_dark']}" stroke-width="0.5" opacity="0.4"/>
        <path d="M4,-6 Q12,-4 24,0" fill="none" stroke="{p['organ_dark']}" stroke-width="0.5" opacity="0.4"/>
        <path d="M4,2 Q10,6 20,10" fill="none" stroke="{p['organ_dark']}" stroke-width="0.5" opacity="0.35"/>
        <path d="M6,10 Q12,14 16,16" fill="none" stroke="{p['organ_dark']}" stroke-width="0.5" opacity="0.3"/>
        <!-- Electrical pulse animation along folds -->
        <circle r="2" fill="{p['accent']}" opacity="0" filter="url(#soft_glow)">
            <animateMotion path="M-6,-14 Q-14,-12 -22,-8 Q-24,0 -20,10 Q-12,16 0,18 Q12,16 20,10 Q24,0 22,-8 Q14,-12 6,-14"
                dur="4s" repeatCount="indefinite"/>
            <animate attributeName="opacity" values="0;0.8;0.6;0.8;0" dur="4s" repeatCount="indefinite"/>
        </circle>
        <circle r="1.5" fill="{p['accent']}" opacity="0" filter="url(#soft_glow)">
            <animateMotion path="M-4,-6 Q-12,-4 -24,0 Q-20,10 -6,10 Q0,8 4,2 Q12,-4 24,0"
                dur="3s" begin="1.5s" repeatCount="indefinite"/>
            <animate attributeName="opacity" values="0;0.6;0.4;0" dur="3s" begin="1.5s" repeatCount="indefinite"/>
        </circle>
        {uv_annotations}
    </g>
    '''


def svg_lungs(p: dict, x: int, y: int, mode: str = "gaslight", uv: bool = False) -> str:
    """Lung pair — one healthy, one blackened. Breathing SMIL animation."""
    right_fill = p['organ_pink']  # healthy
    left_fill = p['organ_dark'] if mode != "clinical" else p['organ_pink']  # blackened in gaslight/gothic
    if mode == "gothic":
        right_fill = p['organ_dark']  # both black in gothic

    uv_formula = ""
    if uv:
        uv_formula = f'''
            <text x="-15" y="30" fill="{p['uv_text']}" font-size="4" opacity="0.7">C₁₇H₁₉NO₃</text>
            <text x="-15" y="36" fill="{p['uv_text']}" font-size="3.5" opacity="0.5">+ [UNKNOWN]</text>
            <rect x="-30" y="-20" width="14" height="8" fill="{p['uv_glow']}" opacity="0.1" rx="2">
                <animate attributeName="opacity" values="0.05;0.15;0.05" dur="3s" repeatCount="indefinite"/>
            </rect>
        '''
    return f'''
    <g transform="translate({x},{y})">
        <!-- Waxed paper base -->
        <rect x="-38" y="-25" width="76" height="50" rx="2" fill="{p['marble_light']}" opacity="0.3" stroke="{p['accent_dim']}" stroke-width="0.3"/>
        <!-- Right lung (healthy) with breathing animation -->
        <g>
            <animateTransform attributeName="transform" type="scale"
                values="1,1; 1.03,1.05; 1,1" dur="4s" repeatCount="indefinite" additive="sum"/>
            <path d="M4,-20 C6,-22 18,-20 22,-14 C26,-6 28,4 26,12 C24,18 16,22 8,20 C4,18 2,10 2,0 Z"
                  fill="{right_fill}" stroke="{p['organ_dark']}" stroke-width="0.7"/>
            <!-- Lobe divisions -->
            <path d="M8,-8 Q16,-6 22,-2" fill="none" stroke="{p['organ_dark']}" stroke-width="0.4" opacity="0.4"/>
            <path d="M6,4 Q14,6 24,8" fill="none" stroke="{p['organ_dark']}" stroke-width="0.4" opacity="0.3"/>
        </g>
        <!-- Left lung (blackened) with breathing animation -->
        <g>
            <animateTransform attributeName="transform" type="scale"
                values="1,1; 1.02,1.04; 1,1" dur="4s" begin="0.3s" repeatCount="indefinite" additive="sum"/>
            <path d="M-4,-20 C-6,-22 -18,-20 -22,-14 C-26,-6 -28,4 -26,12 C-24,18 -16,22 -8,20 C-4,18 -2,10 -2,0 Z"
                  fill="{left_fill}" stroke="{p['organ_dark']}" stroke-width="0.7"/>
            <path d="M-8,-8 Q-16,-6 -22,-2" fill="none" stroke="{p['organ_dark']}" stroke-width="0.4" opacity="0.3"/>
            <path d="M-6,4 Q-14,6 -24,8" fill="none" stroke="{p['organ_dark']}" stroke-width="0.4" opacity="0.3"/>
        </g>
        <!-- Trachea stub -->
        <path d="M0,-22 L0,-28" stroke="{p['organ_red']}" stroke-width="3" stroke-linecap="round"/>
        <path d="M0,-22 L-4,-20" stroke="{p['organ_red']}" stroke-width="2" stroke-linecap="round"/>
        <path d="M0,-22 L4,-20" stroke="{p['organ_red']}" stroke-width="2" stroke-linecap="round"/>
        {uv_formula}
    </g>
    '''


def svg_eye(p: dict, x: int, y: int, mode: str = "gaslight", uv: bool = False) -> str:
    """Preserved eye in jar with pupil dilation SMIL animation."""
    # Iris color
    iris_color = "#4a8050" if mode != "gothic" else "#2a4030"
    uv_retina = ""
    if uv:
        iris_color = p['uv_glow']
        uv_retina = f'''
            <text x="0" y="22" text-anchor="middle" fill="{p['uv_text']}" font-size="3.5" opacity="0.6">BELLADONNA</text>
            <circle cx="0" cy="0" r="14" fill="none" stroke="{p['uv_glow']}" stroke-width="0.5" opacity="0.4">
                <animate attributeName="r" values="14;16;14" dur="3s" repeatCount="indefinite"/>
            </circle>
        '''
    return f'''
    <g transform="translate({x},{y})">
        <!-- Jar -->
        <rect x="-14" y="-18" width="28" height="34" rx="4" fill="{p['marble_light']}" opacity="0.2" stroke="{p['steel']}" stroke-width="0.6"/>
        <rect x="-12" y="-20" width="24" height="4" rx="2" fill="{p['brass']}" stroke="{p['brass_dark']}" stroke-width="0.4"/>
        <!-- Fluid -->
        <rect x="-12" y="-16" width="24" height="30" rx="3" fill="{p['channel_liquid']}" opacity="0.15"/>
        <!-- Eyeball -->
        <circle cx="0" cy="0" r="12" fill="#e8e0d0" stroke="{p['organ_red']}" stroke-width="0.5"/>
        <!-- Blood vessels on sclera -->
        <path d="M-10,-3 Q-6,-1 -4,0" fill="none" stroke="{p['organ_red']}" stroke-width="0.3" opacity="0.5"/>
        <path d="M10,2 Q6,0 4,-1" fill="none" stroke="{p['organ_red']}" stroke-width="0.3" opacity="0.4"/>
        <path d="M-8,6 Q-4,4 -2,2" fill="none" stroke="{p['organ_red']}" stroke-width="0.2" opacity="0.3"/>
        <!-- Iris -->
        <circle cx="0" cy="0" r="7" fill="{iris_color}"/>
        <!-- Iris fibers -->
        <g opacity="0.3">
            <line x1="0" y1="-7" x2="0" y2="-3" stroke="#2a3020" stroke-width="0.3"/>
            <line x1="5" y1="-5" x2="2" y2="-2" stroke="#2a3020" stroke-width="0.3"/>
            <line x1="7" y1="0" x2="3" y2="0" stroke="#2a3020" stroke-width="0.3"/>
            <line x1="5" y1="5" x2="2" y2="2" stroke="#2a3020" stroke-width="0.3"/>
            <line x1="0" y1="7" x2="0" y2="3" stroke="#2a3020" stroke-width="0.3"/>
            <line x1="-5" y1="5" x2="-2" y2="2" stroke="#2a3020" stroke-width="0.3"/>
            <line x1="-7" y1="0" x2="-3" y2="0" stroke="#2a3020" stroke-width="0.3"/>
            <line x1="-5" y1="-5" x2="-2" y2="-2" stroke="#2a3020" stroke-width="0.3"/>
        </g>
        <!-- Pupil with dilation animation -->
        <circle cx="0" cy="0" r="3" fill="#0a0a0a">
            <animate attributeName="r" values="2.5;4;2.5;3;2.5" dur="5s" repeatCount="indefinite"/>
        </circle>
        <!-- Specular highlight -->
        <circle cx="-2" cy="-2" r="1.5" fill="white" opacity="0.6"/>
        {uv_retina}
    </g>
    '''


def svg_skeletal_hand(p: dict, x: int, y: int, uv: bool = False) -> str:
    """Articulated skeletal hand with galvanic finger twitch."""
    uv_numbers = ""
    if uv:
        uv_numbers = f'''
            <text x="-12" y="-28" fill="{p['uv_text']}" font-size="3" opacity="0.7">F-23-VII</text>
            <text x="4" y="-30" fill="{p['uv_text']}" font-size="3" opacity="0.6">F-23-XII</text>
            <text x="14" y="-20" fill="{p['uv_text']}" font-size="3" opacity="0.5">F-23-XIX</text>
            <circle cx="-8" cy="4" r="3" fill="none" stroke="{p['uv_glow']}" stroke-width="0.5" opacity="0.4">
                <animate attributeName="opacity" values="0.2;0.5;0.2" dur="2.5s" repeatCount="indefinite"/>
            </circle>
            <text x="-8" y="6" text-anchor="middle" fill="{p['uv_text']}" font-size="2.5" opacity="0.6">🌹</text>
        '''
    return f'''
    <g transform="translate({x},{y})">
        <!-- Cork board base -->
        <rect x="-28" y="-8" width="56" height="20" rx="2" fill="{p['bone_shadow']}" opacity="0.3" stroke="{p['accent_dim']}" stroke-width="0.3"/>
        <!-- Wrist bones (carpals) -->
        <rect x="-8" y="-2" width="16" height="10" rx="3" fill="{p['bone']}" stroke="{p['bone_shadow']}" stroke-width="0.5"/>
        <!-- Metacarpals -->
        <line x1="-6" y1="-2" x2="-10" y2="-14" stroke="{p['bone']}" stroke-width="2.5" stroke-linecap="round"/>
        <line x1="-2" y1="-2" x2="-4" y2="-16" stroke="{p['bone']}" stroke-width="2.5" stroke-linecap="round"/>
        <line x1="2" y1="-2" x2="2" y2="-18" stroke="{p['bone']}" stroke-width="2.5" stroke-linecap="round"/>
        <line x1="6" y1="-2" x2="8" y2="-16" stroke="{p['bone']}" stroke-width="2.5" stroke-linecap="round"/>
        <!-- Thumb -->
        <line x1="-8" y1="2" x2="-16" y2="-4" stroke="{p['bone']}" stroke-width="2.5" stroke-linecap="round"/>
        <line x1="-16" y1="-4" x2="-20" y2="-10" stroke="{p['bone']}" stroke-width="2" stroke-linecap="round"/>
        <!-- Finger tips (phalanges) -->
        <line x1="-10" y1="-14" x2="-12" y2="-22" stroke="{p['bone']}" stroke-width="2" stroke-linecap="round"/>
        <line x1="-12" y1="-22" x2="-14" y2="-28" stroke="{p['bone']}" stroke-width="1.5" stroke-linecap="round"/>
        <line x1="-4" y1="-16" x2="-5" y2="-24" stroke="{p['bone']}" stroke-width="2" stroke-linecap="round"/>
        <line x1="-5" y1="-24" x2="-6" y2="-32" stroke="{p['bone']}" stroke-width="1.5" stroke-linecap="round"/>
        <line x1="2" y1="-18" x2="2" y2="-26" stroke="{p['bone']}" stroke-width="2" stroke-linecap="round"/>
        <line x1="2" y1="-26" x2="2" y2="-34" stroke="{p['bone']}" stroke-width="1.5" stroke-linecap="round"/>
        <!-- Ring finger — MISSING (stump only) -->
        <line x1="8" y1="-16" x2="10" y2="-20" stroke="{p['bone']}" stroke-width="2" stroke-linecap="round"/>
        <circle cx="10" cy="-20" r="1" fill="{p['bone_shadow']}"/>
        <!-- Galvanic twitch on index finger -->
        <g>
            <animateTransform attributeName="transform" type="rotate"
                values="0 -5 -24; -4 -5 -24; 0 -5 -24; 0 -5 -24; 0 -5 -24"
                dur="6s" repeatCount="indefinite"/>
            <!-- Tiny spark at fingertip -->
            <circle cx="-6" cy="-32" r="1" fill="{p['accent']}" opacity="0">
                <animate attributeName="opacity" values="0;0;0.8;0;0;0;0;0;0;0" dur="6s" repeatCount="indefinite"/>
            </circle>
        </g>
        <!-- Wire connectors -->
        <circle cx="-2" cy="-2" r="0.5" fill="{p['steel']}"/>
        <circle cx="2" cy="-2" r="0.5" fill="{p['steel']}"/>
        <circle cx="-6" cy="-2" r="0.5" fill="{p['steel']}"/>
        <circle cx="6" cy="-2" r="0.5" fill="{p['steel']}"/>
        {uv_numbers}
    </g>
    '''


# =============================================================================
# INSTRUMENT SVGs
# =============================================================================

def svg_bone_saw(p: dict, x: int, y: int, uv: bool = False) -> str:
    """Bone saw with steel glint SMIL animation."""
    uv_layer = ""
    if uv:
        uv_layer = f'''
            <text x="30" y="18" fill="{p['uv_text']}" font-size="3.5" opacity="0.7" transform="rotate(-5,30,18)">R.R.S. 1881</text>
            <rect x="28" y="5" width="6" height="3" fill="{p['uv_glow']}" opacity="0.3" rx="1">
                <animate attributeName="opacity" values="0.2;0.4;0.2" dur="2s" repeatCount="indefinite"/>
            </rect>
        '''
    return f'''
    <g transform="translate({x},{y})">
        <!-- Handle -->
        <rect x="28" y="-4" width="22" height="8" rx="3" fill="{p['brass']}" stroke="{p['brass_dark']}" stroke-width="0.5"/>
        <rect x="30" y="-2" width="18" height="4" rx="1" fill="{p['brass_dark']}" opacity="0.3"/>
        <!-- Blade frame -->
        <path d="M-30,-6 L28,-6 L28,-2 L-30,-2 Z" fill="{p['steel']}" stroke="{p['steel_bright']}" stroke-width="0.5"/>
        <!-- Teeth -->
        <path d="M-28,-2 L-26,2 L-24,-2 L-22,2 L-20,-2 L-18,2 L-16,-2 L-14,2 L-12,-2 L-10,2 L-8,-2 L-6,2 L-4,-2 L-2,2 L0,-2 L2,2 L4,-2 L6,2 L8,-2 L10,2 L12,-2 L14,2 L16,-2 L18,2 L20,-2 L22,2 L24,-2 L26,2 L28,-2"
              fill="none" stroke="{p['steel']}" stroke-width="0.8"/>
        <!-- Spine bar -->
        <rect x="-30" y="-8" width="58" height="3" rx="1" fill="{p['steel_bright']}" stroke="{p['steel']}" stroke-width="0.3"/>
        <!-- Steel glint animation -->
        <rect x="-30" y="-8" width="8" height="12" fill="{p['steel_bright']}" opacity="0">
            <animate attributeName="x" values="-30;30;-30" dur="4s" repeatCount="indefinite"/>
            <animate attributeName="opacity" values="0;0.4;0" dur="4s" repeatCount="indefinite"/>
        </rect>
        <!-- Dark fleck on teeth -->
        <circle cx="-8" cy="0" r="1" fill="{p['blood_old']}" opacity="0.6">
            <animate attributeName="opacity" values="0.4;0.7;0.4" dur="3s" repeatCount="indefinite"/>
        </circle>
        <circle cx="4" cy="1" r="0.8" fill="{p['blood_old']}" opacity="0.5"/>
        {uv_layer}
    </g>
    '''


def svg_scalpel(p: dict, x: int, y: int, uv: bool = False) -> str:
    """Scalpel #4 with red edge line animation. Missing #3 noted."""
    uv_layer = ""
    if uv:
        uv_layer = f'''
            <text x="-5" y="10" fill="{p['uv_text']}" font-size="3.5" opacity="0.7">S.C. — I KEPT YOUR PLACE</text>
        '''
    return f'''
    <g transform="translate({x},{y}) rotate(-15)">
        <!-- Handle -->
        <rect x="12" y="-3" width="28" height="6" rx="2" fill="{p['steel']}" stroke="{p['steel_bright']}" stroke-width="0.4"/>
        <rect x="14" y="-1" width="24" height="2" rx="1" fill="{p['steel_bright']}" opacity="0.3"/>
        <!-- Blade -->
        <path d="M12,0 L-18,0 Q-22,0 -24,-2 L-22,0 Q-22,0 -18,0"
              fill="{p['steel_bright']}" stroke="{p['steel']}" stroke-width="0.5"/>
        <path d="M12,-1 L-16,-1 Q-20,-1 -24,-2" fill="none" stroke="{p['steel']}" stroke-width="0.3"/>
        <path d="M12,1 L-16,1 Q-20,1 -22,0" fill="none" stroke="{p['steel']}" stroke-width="0.3"/>
        <!-- Blade shape (triangular) -->
        <path d="M12,-2 L-20,-2 L-26,0 L-20,2 L12,2 Z" fill="{p['steel_bright']}" stroke="{p['steel']}" stroke-width="0.4"/>
        <!-- Red edge line -->
        <line x1="-24" y1="0" x2="10" y2="2" stroke="{p['blood_fresh']}" stroke-width="0.6" opacity="0.5">
            <animate attributeName="opacity" values="0.3;0.7;0.3" dur="3s" repeatCount="indefinite"/>
        </line>
        <!-- Bolster -->
        <rect x="10" y="-3.5" width="3" height="7" rx="0.5" fill="{p['brass']}" stroke="{p['brass_dark']}" stroke-width="0.3"/>
        <!-- Light catch -->
        <line x1="-10" y1="-1.5" x2="8" y2="-1.5" stroke="white" stroke-width="0.3" opacity="0">
            <animate attributeName="opacity" values="0;0.5;0" dur="5s" begin="1s" repeatCount="indefinite"/>
        </line>
        {uv_layer}
    </g>
    '''


def svg_retractors(p: dict, x: int, y: int, uv: bool = False) -> str:
    """Surgical retractors with slow open/close SMIL animation."""
    uv_layer = ""
    if uv:
        uv_layer = f'''
            <text x="0" y="20" text-anchor="middle" fill="{p['uv_text']}" font-size="3.5" opacity="0.6">F-E-034</text>
        '''
    return f'''
    <g transform="translate({x},{y})">
        <!-- Left arm -->
        <g>
            <animateTransform attributeName="transform" type="rotate"
                values="0 0 0; -5 0 0; 0 0 0" dur="8s" repeatCount="indefinite"/>
            <path d="M0,0 L-6,-20 L-10,-22 L-8,-18 L0,0" fill="{p['steel']}" stroke="{p['steel_bright']}" stroke-width="0.5"/>
            <rect x="-12" y="-24" width="6" height="3" rx="1" fill="{p['steel']}" stroke="{p['steel_bright']}" stroke-width="0.3"/>
        </g>
        <!-- Right arm -->
        <g>
            <animateTransform attributeName="transform" type="rotate"
                values="0 0 0; 5 0 0; 0 0 0" dur="8s" repeatCount="indefinite"/>
            <path d="M0,0 L6,-20 L10,-22 L8,-18 L0,0" fill="{p['steel']}" stroke="{p['steel_bright']}" stroke-width="0.5"/>
            <rect x="6" y="-24" width="6" height="3" rx="1" fill="{p['steel']}" stroke="{p['steel_bright']}" stroke-width="0.3"/>
        </g>
        <!-- Central ratchet mechanism -->
        <circle cx="0" cy="0" r="3" fill="{p['steel']}" stroke="{p['steel_bright']}" stroke-width="0.5"/>
        <circle cx="0" cy="0" r="1.5" fill="{p['steel_bright']}"/>
        <!-- Handle -->
        <rect x="-2" y="2" width="4" height="14" rx="1" fill="{p['steel']}" stroke="{p['steel_bright']}" stroke-width="0.3"/>
        <rect x="-4" y="14" width="8" height="3" rx="1" fill="{p['brass']}" stroke="{p['brass_dark']}" stroke-width="0.3"/>
        {uv_layer}
    </g>
    '''


def svg_suture_needle(p: dict, x: int, y: int, uv: bool = False) -> str:
    """Curved suture needle with catgut thread swaying."""
    uv_layer = ""
    if uv:
        uv_layer = f'''
            <text x="5" y="18" fill="{p['uv_text']}" font-size="3.5" opacity="0.6">CONCEALMENT PROTOCOL</text>
        '''
    return f'''
    <g transform="translate({x},{y})">
        <!-- Curved needle -->
        <path d="M-8,-10 Q-14,0 -8,10 Q-4,14 2,12" fill="none" stroke="{p['steel_bright']}" stroke-width="1.2" stroke-linecap="round"/>
        <!-- Needle point -->
        <circle cx="-8" cy="-10" r="0.8" fill="{p['steel_bright']}"/>
        <!-- Catgut thread with sway animation -->
        <path d="M2,12 Q8,14 12,10 Q16,6 14,0 Q12,-6 16,-10 Q20,-14 18,-18" fill="none"
              stroke="{p['bone_shadow']}" stroke-width="0.6" stroke-linecap="round" opacity="0.7">
            <animate attributeName="d"
                values="M2,12 Q8,14 12,10 Q16,6 14,0 Q12,-6 16,-10 Q20,-14 18,-18;
                        M2,12 Q6,16 10,12 Q14,8 12,2 Q10,-4 14,-10 Q18,-16 16,-20;
                        M2,12 Q8,14 12,10 Q16,6 14,0 Q12,-6 16,-10 Q20,-14 18,-18"
                dur="5s" repeatCount="indefinite"/>
        </path>
        <!-- Thread end -->
        <circle cx="18" cy="-18" r="0.5" fill="{p['bone_shadow']}" opacity="0.5">
            <animate attributeName="cy" values="-18;-20;-18" dur="5s" repeatCount="indefinite"/>
        </circle>
        {uv_layer}
    </g>
    '''


def svg_magnifying_lens(p: dict, x: int, y: int, uv: bool = False) -> str:
    """Brass magnifying lens with light refraction sweep."""
    uv_layer = ""
    if uv:
        uv_layer = f'''
            <text x="-8" y="22" fill="{p['uv_text']}" font-size="3" opacity="0.6">21 NAMES</text>
            <text x="-8" y="26" fill="{p['uv_text']}" font-size="2.5" opacity="0.5">3 CROSSED OUT</text>
        '''
    return f'''
    <g transform="translate({x},{y})">
        <!-- Handle -->
        <rect x="14" y="-3" width="24" height="6" rx="2" fill="{p['brass']}" stroke="{p['brass_dark']}" stroke-width="0.5"/>
        <rect x="16" y="-1" width="20" height="2" rx="1" fill="{p['brass_dark']}" opacity="0.3"/>
        <!-- Lens frame -->
        <circle cx="0" cy="0" r="14" fill="none" stroke="{p['brass']}" stroke-width="2.5"/>
        <circle cx="0" cy="0" r="12" fill="none" stroke="{p['brass_dark']}" stroke-width="0.5"/>
        <!-- Lens glass -->
        <circle cx="0" cy="0" r="12" fill="{p['marble_light']}" opacity="0.15"/>
        <!-- Magnified marble grain beneath -->
        <g clip-path="url(#lens_clip)" opacity="0.3">
            <path d="M-8,-6 Q-2,-3 4,-8" fill="none" stroke="{p['marble_vein']}" stroke-width="1.5"/>
            <path d="M-6,2 Q0,5 8,2" fill="none" stroke="{p['marble_vein']}" stroke-width="1"/>
        </g>
        <!-- Crack in lens -->
        <path d="M-4,8 Q-2,4 0,0 Q2,-4 6,-10" fill="none" stroke="{p['steel']}" stroke-width="0.4" opacity="0.5"/>
        <!-- Light refraction sweep -->
        <ellipse cx="-6" cy="-4" rx="3" ry="6" fill="white" opacity="0" transform="rotate(-20)">
            <animate attributeName="opacity" values="0;0.3;0" dur="6s" repeatCount="indefinite"/>
            <animateTransform attributeName="transform" type="rotate"
                values="-20;20;-20" dur="6s" repeatCount="indefinite"/>
        </ellipse>
        <!-- Specular highlight -->
        <ellipse cx="-4" cy="-4" rx="2" ry="4" fill="white" opacity="0.15" transform="rotate(-30)"/>
        {uv_layer}
    </g>
    '''


# =============================================================================
# ATMOSPHERIC DETAIL SVGs
# =============================================================================

def svg_candle(p: dict, x: int, y: int, mode: str = "gaslight", uv: bool = False) -> str:
    """Tallow candle with flickering flame and wax drip."""
    if mode == "clinical":
        # Clinical mode: notation card instead of candle
        return f'''
        <g transform="translate({x},{y})">
            <rect x="-12" y="-15" width="24" height="30" rx="1" fill="{p['marble_light']}" stroke="{p['accent']}" stroke-width="0.5"/>
            <text x="0" y="-5" text-anchor="middle" fill="{p['text_dim']}" font-size="4" font-family="sans-serif">PROCEDURE</text>
            <text x="0" y="0" text-anchor="middle" fill="{p['text_dim']}" font-size="4" font-family="sans-serif">#108</text>
            <text x="0" y="6" text-anchor="middle" fill="{p['text_dim']}" font-size="3" font-family="sans-serif">THORACIC</text>
            <line x1="-8" y1="9" x2="8" y2="9" stroke="{p['accent']}" stroke-width="0.3"/>
            <text x="0" y="13" text-anchor="middle" fill="{p['accent']}" font-size="3" font-family="sans-serif">APPROVED</text>
        </g>
        '''
    uv_layer = ""
    if uv:
        uv_layer = f'''
            <text x="0" y="28" text-anchor="middle" fill="{p['uv_text']}" font-size="3.5" opacity="0.6">🌹 23</text>
        '''
    flame_color = p['candle_flame']
    return f'''
    <g transform="translate({x},{y})">
        <!-- Brass holder -->
        <ellipse cx="0" cy="18" rx="10" ry="4" fill="{p['brass']}" stroke="{p['brass_dark']}" stroke-width="0.5"/>
        <rect x="-4" y="10" width="8" height="8" fill="{p['brass']}" stroke="{p['brass_dark']}" stroke-width="0.3"/>
        <ellipse cx="0" cy="10" rx="6" ry="2.5" fill="{p['brass']}" stroke="{p['brass_dark']}" stroke-width="0.3"/>
        <!-- Candle body -->
        <rect x="-3" y="-10" width="6" height="20" rx="1" fill="#e8e0c8" stroke="#d0c8b0" stroke-width="0.3"/>
        <!-- Wax drip -->
        <path d="M3,0 Q4,-2 5,2 Q5,5 4,8 Q3,10 3,10" fill="#e8e0c8" stroke="#d0c8b0" stroke-width="0.3"/>
        <path d="M-3,4 Q-4,2 -5,6 Q-5,8 -4,12" fill="#e8e0c8" stroke="#d0c8b0" stroke-width="0.2" opacity="0.7"/>
        <!-- Wick -->
        <line x1="0" y1="-10" x2="0" y2="-14" stroke="#2a2a1a" stroke-width="0.8"/>
        <!-- Flame -->
        <g>
            <animateTransform attributeName="transform" type="translate"
                values="0,0; 0.5,-0.5; -0.3,0.2; 0.2,-0.3; 0,0" dur="0.8s" repeatCount="indefinite"/>
            <!-- Outer flame -->
            <path d="M0,-14 Q-3,-18 -1.5,-24 Q0,-28 1.5,-24 Q3,-18 0,-14Z"
                  fill="{flame_color}" opacity="0.6">
                <animate attributeName="d"
                    values="M0,-14 Q-3,-18 -1.5,-24 Q0,-28 1.5,-24 Q3,-18 0,-14Z;
                            M0,-14 Q-2.5,-19 -1,-25 Q0,-29 1,-25 Q2.5,-19 0,-14Z;
                            M0,-14 Q-3,-18 -1.5,-24 Q0,-28 1.5,-24 Q3,-18 0,-14Z"
                    dur="0.6s" repeatCount="indefinite"/>
            </path>
            <!-- Inner flame (bright) -->
            <path d="M0,-14 Q-1.5,-17 -0.5,-21 Q0,-23 0.5,-21 Q1.5,-17 0,-14Z"
                  fill="#ffe8a0" opacity="0.9">
                <animate attributeName="opacity" values="0.8;1;0.7;0.9;0.8" dur="0.4s" repeatCount="indefinite"/>
            </path>
        </g>
        <!-- Wax drip animation -->
        <circle cx="3" cy="0" r="0.8" fill="#e8e0c8" opacity="0">
            <animate attributeName="cy" values="0;8;18" dur="10s" repeatCount="indefinite"/>
            <animate attributeName="opacity" values="0;0.8;0" dur="10s" repeatCount="indefinite"/>
        </circle>
        {uv_layer}
    </g>
    '''


def svg_pocket_watch(p: dict, x: int, y: int, mode: str = "gaslight", uv: bool = False) -> str:
    """Pocket watch — ticks forward normally, backwards in gothic mode."""
    direction = "0;360" if mode != "gothic" else "360;0"
    uv_layer = ""
    if uv:
        uv_layer = f'''
            <text x="0" y="22" text-anchor="middle" fill="{p['uv_text']}" font-size="3" opacity="0.7">FOR A.F. — E.F.</text>
            <text x="0" y="26" text-anchor="middle" fill="{p['uv_text']}" font-size="2.5" opacity="0.5">RESETS: 18 DAYS</text>
        '''
    return f'''
    <g transform="translate({x},{y})">
        <!-- Case -->
        <circle cx="0" cy="0" r="16" fill="{p['brass']}" stroke="{p['brass_dark']}" stroke-width="1"/>
        <circle cx="0" cy="0" r="14" fill="{p['marble_light']}" stroke="{p['brass_dark']}" stroke-width="0.5"/>
        <!-- Crown -->
        <rect x="-2" y="-19" width="4" height="4" rx="1.5" fill="{p['brass']}" stroke="{p['brass_dark']}" stroke-width="0.3"/>
        <!-- Hour markers -->
        <g fill="{p['text']}" font-size="3.5" text-anchor="middle" font-family="serif">
            <text x="0" y="-9">XII</text>
            <text x="10" y="-1">III</text>
            <text x="0" y="11">VI</text>
            <text x="-10" y="-1">IX</text>
        </g>
        <!-- Tick marks -->
        <g stroke="{p['text_dim']}" stroke-width="0.3">
            <line x1="0" y1="-12" x2="0" y2="-11"/>
            <line x1="6" y1="-10.4" x2="5.5" y2="-9.5"/>
            <line x1="10.4" y1="-6" x2="9.5" y2="-5.5"/>
            <line x1="12" y1="0" x2="11" y2="0"/>
            <line x1="10.4" y1="6" x2="9.5" y2="5.5"/>
            <line x1="6" y1="10.4" x2="5.5" y2="9.5"/>
            <line x1="0" y1="12" x2="0" y2="11"/>
            <line x1="-6" y1="10.4" x2="-5.5" y2="9.5"/>
            <line x1="-10.4" y1="6" x2="-9.5" y2="5.5"/>
            <line x1="-12" y1="0" x2="-11" y2="0"/>
            <line x1="-10.4" y1="-6" x2="-9.5" y2="-5.5"/>
            <line x1="-6" y1="-10.4" x2="-5.5" y2="-9.5"/>
        </g>
        <!-- Hour hand -->
        <line x1="0" y1="0" x2="0" y2="-7" stroke="{p['text']}" stroke-width="1" stroke-linecap="round"/>
        <!-- Minute hand -->
        <line x1="0" y1="0" x2="5" y2="-8" stroke="{p['text']}" stroke-width="0.6" stroke-linecap="round"/>
        <!-- Second hand (animated) -->
        <line x1="0" y1="2" x2="0" y2="-10" stroke="{p['blood_fresh']}" stroke-width="0.4" stroke-linecap="round">
            <animateTransform attributeName="transform" type="rotate"
                values="{direction}" dur="60s" repeatCount="indefinite" additive="sum"/>
        </line>
        <!-- Center pin -->
        <circle cx="0" cy="0" r="1" fill="{p['brass']}"/>
        <!-- Chain stub -->
        <path d="M0,-19 Q-4,-22 -2,-26 Q0,-28 2,-26 Q4,-22 0,-19" fill="none" stroke="{p['brass']}" stroke-width="0.8"/>
        {uv_layer}
    </g>
    '''


def svg_handwritten_note(p: dict, x: int, y: int, uv: bool = False) -> str:
    """Torn note with bleeding ink animation."""
    uv_layer = ""
    if uv:
        uv_layer = f'''
            <g opacity="0.8">
                <text x="5" y="-10" fill="{p['uv_bright']}" font-size="3" font-family="serif" font-style="italic">The Warren Protocol must be</text>
                <text x="5" y="-5" fill="{p['uv_bright']}" font-size="3" font-family="serif" font-style="italic">stopped. Subject 23 remained</text>
                <text x="5" y="0" fill="{p['uv_bright']}" font-size="3" font-family="serif" font-style="italic">conscious throughout. She spoke</text>
                <text x="5" y="5" fill="{p['uv_bright']}" font-size="3" font-family="serif" font-style="italic">my name. — A.F.</text>
                <animate attributeName="opacity" values="0.5;0.9;0.5" dur="4s" repeatCount="indefinite"/>
            </g>
        '''
    return f'''
    <g transform="translate({x},{y})">
        <!-- Torn paper -->
        <path d="M-20,-16 L20,-14 Q22,-14 22,-12 L24,16 Q24,18 22,18 L-18,20 Q-20,18 -22,16 L-24,-12 Q-22,-16 -20,-16Z"
              fill="#e8dcc0" stroke="#c8b8a0" stroke-width="0.5" opacity="0.9"/>
        <!-- Torn edge -->
        <path d="M-20,-16 Q-18,-14 -16,-16 Q-14,-13 -12,-15 Q-8,-13 -4,-16 Q0,-13 4,-15 Q8,-14 12,-16 Q16,-13 20,-14"
              fill="none" stroke="#c8b8a0" stroke-width="0.5"/>
        <!-- Handwritten text (visible portions) -->
        <g fill="{p['ink']}" font-size="3.5" font-family="serif" font-style="italic" opacity="0.7">
            <text x="-16" y="-6">...cannot continue this...</text>
            <text x="-16" y="0">...the Warren Protocol must...</text>
            <text x="-16" y="6">...Carlisle was right...</text>
            <text x="-16" y="12">...God forgive me...</text>
        </g>
        <!-- Ink bleeding from corner -->
        <circle cx="20" cy="14" r="3" fill="{p['ink']}" opacity="0.4">
            <animate attributeName="r" values="3;8;12" dur="20s" fill="freeze"/>
            <animate attributeName="opacity" values="0.4;0.2;0.1" dur="20s" fill="freeze"/>
        </circle>
        <circle cx="18" cy="10" r="2" fill="{p['ink']}" opacity="0.3">
            <animate attributeName="r" values="2;5;8" dur="25s" fill="freeze"/>
            <animate attributeName="opacity" values="0.3;0.15;0.08" dur="25s" fill="freeze"/>
        </circle>
        {uv_layer}
    </g>
    '''


def svg_blood_spots(p: dict, x: int, y: int, uv: bool = False) -> str:
    """Blood spots in various oxidation stages with darkening animation."""
    uv_layer = ""
    if uv:
        uv_layer = f'''
            <!-- Rose pattern revealed -->
            <g opacity="0.4">
                <circle cx="0" cy="0" r="18" fill="none" stroke="{p['uv_glow']}" stroke-width="0.5"/>
                <ellipse cx="0" cy="-6" rx="6" ry="5" fill="none" stroke="{p['uv_bright']}" stroke-width="0.5"/>
                <ellipse cx="-5" cy="2" rx="5" ry="6" fill="none" stroke="{p['uv_bright']}" stroke-width="0.5" transform="rotate(-25)"/>
                <ellipse cx="5" cy="2" rx="5" ry="6" fill="none" stroke="{p['uv_bright']}" stroke-width="0.5" transform="rotate(25)"/>
                <animate attributeName="opacity" values="0.3;0.5;0.3" dur="3s" repeatCount="indefinite"/>
            </g>
            <text x="0" y="24" text-anchor="middle" fill="{p['uv_text']}" font-size="3" opacity="0.5">RITUAL PATTERN</text>
        '''
    return f'''
    <g transform="translate({x},{y})">
        <!-- Fresh spot (crimson) -->
        <circle cx="-10" cy="-5" r="4" fill="{p['blood_fresh']}" opacity="0.7"/>
        <circle cx="-8" cy="-3" r="1.5" fill="{p['blood_fresh']}" opacity="0.5"/>
        <!-- Mid-oxidation spots -->
        <circle cx="8" cy="2" r="3.5" fill="{p['blood_old']}" opacity="0.6">
            <animate attributeName="fill" values="{p['blood_fresh']};{p['blood_old']}" dur="30s" fill="freeze"/>
        </circle>
        <circle cx="4" cy="-8" r="2" fill="{p['blood_old']}" opacity="0.5"/>
        <!-- Old spot (near-black) -->
        <circle cx="-3" cy="8" r="5" fill="{p['blood_old']}" opacity="0.8"/>
        <circle cx="12" cy="8" r="2.5" fill="{p['blood_old']}" opacity="0.4"/>
        <!-- Splatter trails -->
        <circle cx="-14" cy="-8" r="0.8" fill="{p['blood_fresh']}" opacity="0.3"/>
        <circle cx="-16" cy="-10" r="0.5" fill="{p['blood_fresh']}" opacity="0.2"/>
        <circle cx="14" cy="4" r="0.6" fill="{p['blood_old']}" opacity="0.3"/>
        {uv_layer}
    </g>
    '''


def svg_red_rose(p: dict, x: int, y: int, uv: bool = False) -> str:
    """Wilting red rose with falling petal animation."""
    uv_layer = ""
    if uv:
        uv_layer = f'''
            <g filter="url(#uv_glow_filter)">
                <circle cx="0" cy="-8" r="10" fill="{p['uv_glow']}" opacity="0.2">
                    <animate attributeName="opacity" values="0.15;0.3;0.15" dur="3s" repeatCount="indefinite"/>
                </circle>
            </g>
            <text x="-12" y="20" fill="{p['uv_text']}" font-size="3.5" opacity="0.6">R. R. S.</text>
            <text x="-12" y="25" fill="{p['uv_text']}" font-size="2.5" opacity="0.4">THE WARREN PROTOCOL</text>
            <text x="-12" y="29" fill="{p['uv_text']}" font-size="2.5" opacity="0.4">CONTINUES</text>
        '''
    return f'''
    <g transform="translate({x},{y})">
        <!-- Stem -->
        <path d="M0,8 Q-2,16 -1,28 Q0,34 2,38" fill="none" stroke="#3a5a2a" stroke-width="1.5"/>
        <!-- Leaves -->
        <path d="M-1,18 Q-8,14 -12,18 Q-8,20 -1,18" fill="#3a5a2a" opacity="0.7"/>
        <path d="M0,26 Q6,22 10,26 Q6,28 0,26" fill="#3a5a2a" opacity="0.6"/>
        <!-- Bloom (layered petals) -->
        <g>
            <!-- Outer petals (wilting) -->
            <path d="M0,-8 Q-10,-14 -14,-8 Q-12,-2 -6,0 Q-2,0 0,-2"
                  fill="{p['rose']}" stroke="{p['rose_bright']}" stroke-width="0.3" opacity="0.8"/>
            <path d="M0,-8 Q10,-14 14,-8 Q12,-2 6,0 Q2,0 0,-2"
                  fill="{p['rose']}" stroke="{p['rose_bright']}" stroke-width="0.3" opacity="0.8"/>
            <path d="M0,0 Q-8,4 -10,0 Q-8,-4 0,-2"
                  fill="{p['rose']}" opacity="0.7"/>
            <path d="M0,0 Q8,4 10,0 Q8,-4 0,-2"
                  fill="{p['rose']}" opacity="0.7"/>
            <!-- Inner petals (curled) -->
            <path d="M0,-6 Q-4,-10 -6,-6 Q-4,-2 0,-4" fill="{p['rose_bright']}" opacity="0.9"/>
            <path d="M0,-6 Q4,-10 6,-6 Q4,-2 0,-4" fill="{p['rose_bright']}" opacity="0.9"/>
            <ellipse cx="0" cy="-5" rx="2" ry="3" fill="{p['rose_bright']}" opacity="0.7"/>
            <!-- Brown edges (wilting) -->
            <path d="M-14,-8 Q-15,-6 -14,-4" fill="none" stroke="#5a3020" stroke-width="0.5" opacity="0.5"/>
            <path d="M14,-8 Q15,-6 14,-4" fill="none" stroke="#5a3020" stroke-width="0.5" opacity="0.5"/>
        </g>
        <!-- Fallen petals on marble -->
        <ellipse cx="-16" cy="6" rx="4" ry="2" fill="{p['rose']}" opacity="0.5" transform="rotate(-20,-16,6)"/>
        <ellipse cx="18" cy="10" rx="3.5" ry="1.8" fill="{p['rose']}" opacity="0.4" transform="rotate(15,18,10)"/>
        <!-- Falling petal animation -->
        <ellipse cx="8" cy="-4" rx="3" ry="1.5" fill="{p['rose']}" opacity="0.6" transform="rotate(30,8,-4)">
            <animate attributeName="cy" values="-4;12" dur="15s" fill="freeze"/>
            <animate attributeName="cx" values="8;14" dur="15s" fill="freeze"/>
            <animate attributeName="opacity" values="0.6;0.4" dur="15s" fill="freeze"/>
            <animateTransform attributeName="transform" type="rotate"
                values="30,8,-4; 80,14,12" dur="15s" fill="freeze"/>
        </ellipse>
        {uv_layer}
    </g>
    '''


# =============================================================================
# MAIN COMPOSITION — Full dissection table scene
# =============================================================================

def render_dissection_table_svg(mode: str = "gaslight", uv: bool = False,
                                 intensity: int = 2, selected_id: str = None) -> str:
    """
    Compose the full 900x600 dissection table SVG.
    Returns a base64-encoded <img> tag for Streamlit rendering.
    """
    p = get_palette(mode)

    # Intensity-based additions
    mist = ""
    if mode == "gothic" and intensity >= 3:
        mist = f'''
        <rect x="50" y="400" width="800" height="150" fill="url(#mist_grad)" opacity="0.3">
            <animate attributeName="y" values="400;380;400" dur="10s" repeatCount="indefinite"/>
            <animate attributeName="opacity" values="0.2;0.4;0.2" dur="10s" repeatCount="indefinite"/>
        </rect>
        '''

    # Highlight ring around selected item
    highlight = ""
    if selected_id:
        pos_map = {
            "heart": (180, 200), "brain": (320, 190), "lungs": (180, 310),
            "eye": (320, 310), "skeletal_hand": (250, 420),
            "bone_saw": (620, 180), "scalpel": (720, 200),
            "retractors": (620, 300), "suture_needle": (720, 310),
            "magnifying_lens": (670, 410),
            "pocket_watch": (450, 480), "handwritten_note": (350, 120),
            "candle": (100, 130), "blood_spots": (450, 300),
            "red_rose": (780, 460),
        }
        if selected_id in pos_map:
            hx, hy = pos_map[selected_id]
            highlight = f'''
            <circle cx="{hx}" cy="{hy}" r="32" fill="none" stroke="{p['accent']}" stroke-width="1.5"
                    stroke-dasharray="4,3" opacity="0.6">
                <animate attributeName="r" values="30;35;30" dur="2s" repeatCount="indefinite"/>
                <animate attributeName="opacity" values="0.4;0.7;0.4" dur="2s" repeatCount="indefinite"/>
            </circle>
            '''

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 600" width="900" height="600">
    <defs>
        <clipPath id="lens_clip"><circle cx="0" cy="0" r="12"/></clipPath>
        <linearGradient id="mist_grad" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stop-color="{p['bg']}" stop-opacity="0"/>
            <stop offset="100%" stop-color="{p['bg']}" stop-opacity="0.8"/>
        </linearGradient>
    </defs>
    <!-- Background -->
    <rect width="900" height="600" fill="{p['bg']}"/>

    {svg_table_base(p, uv, intensity)}

    <!-- ORGANS (left side) -->
    {svg_heart(p, 180, 200, uv)}
    {svg_brain(p, 320, 190, uv)}
    {svg_lungs(p, 180, 310, mode, uv)}
    {svg_eye(p, 320, 310, mode, uv)}
    {svg_skeletal_hand(p, 250, 420, uv)}

    <!-- INSTRUMENTS (right side) -->
    {svg_bone_saw(p, 620, 180, uv)}
    {svg_scalpel(p, 720, 200, uv)}
    {svg_retractors(p, 620, 300, uv)}
    {svg_suture_needle(p, 720, 310, uv)}
    {svg_magnifying_lens(p, 670, 410, uv)}

    <!-- ATMOSPHERIC DETAILS -->
    {svg_candle(p, 100, 130, mode, uv)}
    {svg_pocket_watch(p, 450, 480, mode, uv)}
    {svg_handwritten_note(p, 350, 120, uv)}
    {svg_blood_spots(p, 450, 300, uv)}
    {svg_red_rose(p, 780, 460, uv)}

    <!-- Gothic mist -->
    {mist}

    <!-- Selection highlight -->
    {highlight}

    </svg>'''

    return svg_to_base64_img(svg, width="100%")


# =============================================================================
# DETAIL VIEW — Enlarged item SVG for examination panel
# =============================================================================

def render_item_detail_svg(item_id: str, mode: str = "gaslight", uv: bool = False) -> str:
    """
    Render an enlarged detail SVG for a single item (150x150).
    Used in the examination panel beside the text.
    """
    p = get_palette(mode)

    renderers = {
        "heart":          lambda: svg_heart(p, 75, 80, uv),
        "brain":          lambda: svg_brain(p, 75, 80, uv),
        "lungs":          lambda: svg_lungs(p, 75, 85, mode, uv),
        "eye":            lambda: svg_eye(p, 75, 80, mode, uv),
        "skeletal_hand":  lambda: svg_skeletal_hand(p, 75, 95, uv),
        "bone_saw":       lambda: svg_bone_saw(p, 75, 80, uv),
        "scalpel":        lambda: svg_scalpel(p, 75, 80, uv),
        "retractors":     lambda: svg_retractors(p, 75, 85, uv),
        "suture_needle":  lambda: svg_suture_needle(p, 75, 80, uv),
        "magnifying_lens":lambda: svg_magnifying_lens(p, 75, 80, uv),
        "pocket_watch":   lambda: svg_pocket_watch(p, 75, 80, mode, uv),
        "handwritten_note":lambda: svg_handwritten_note(p, 75, 80, uv),
        "candle":         lambda: svg_candle(p, 75, 85, mode, uv),
        "blood_spots":    lambda: svg_blood_spots(p, 75, 80, uv),
        "red_rose":       lambda: svg_red_rose(p, 75, 75, uv),
    }

    renderer = renderers.get(item_id)
    if not renderer:
        return ""

    item_svg = renderer()

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 150 150" width="150" height="150">
    <defs>
        <filter id="soft_glow"><feGaussianBlur stdDeviation="2" result="blur"/>
            <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
        <filter id="uv_glow_filter"><feGaussianBlur stdDeviation="3" result="blur"/>
            <feMerge><feMergeNode in="blur"/><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
        <clipPath id="lens_clip"><circle cx="0" cy="0" r="12"/></clipPath>
    </defs>
    <rect width="150" height="150" fill="{p['bg']}" rx="4"/>
    <rect x="2" y="2" width="146" height="146" fill="none" stroke="{p['accent_dim']}" stroke-width="0.5" rx="3"/>
    {item_svg}
    </svg>'''

    return svg_to_base64_img(svg, width="150px")
