"""
🎭 The Anatomy Theatre
An immersive, atmospheric exploration of a Victorian anatomy theatre.
Tied to the world of The Crimson Rose series.

BUG FIXES IMPLEMENTED:
- Secret evaluation deferred to end of script execution to capture tab widget states
- Secrets rendered globally via top-level placeholder container
- Session state lists updated via strict reassignment
- UI controls mapped to native session state keys
"""

import streamlit as st
import random
from content import (
    get_opening, get_ambient_sound, get_ambient_observation,
    get_anatomy_text, get_random_epigraph, get_specimens_by_category,
    get_dissection_table_items, check_secret_condition,
    ANATOMY_REGIONS, SPECIMENS, SECRETS, DISSECTION_TABLE_ITEMS
)
from theatre_3d import get_theatre_3d


# =============================================================================
# PAGE CONFIG
# =============================================================================

st.set_page_config(
    page_title="The Anatomy Theatre",
    page_icon="🎭",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =============================================================================
# CSS THEMES
# =============================================================================

GASLIGHT_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,600;1,400&family=Playfair+Display:wght@700&display=swap');

:root {
    --bg-primary: #1a1410;
    --bg-secondary: #2c1810;
    --bg-tertiary: #3d2317;
    --text-primary: #d4c4a8;
    --text-secondary: #a89070;
    --accent: #d4a574;
    --accent-dim: #8b6914;
    --danger: #8b4513;
}

.stApp {
    background: linear-gradient(180deg, var(--bg-primary) 0%, var(--bg-secondary) 100%);
}

.main-title {
    font-family: 'Playfair Display', serif;
    color: var(--accent);
    text-align: center;
    font-size: 3.5rem;
    text-shadow: 0 0 30px rgba(212, 165, 116, 0.3);
    letter-spacing: 0.15em;
    margin-bottom: 0;
}

.subtitle {
    font-family: 'EB Garamond', serif;
    color: var(--text-secondary);
    text-align: center;
    font-size: 1.2rem;
    font-style: italic;
    margin-top: 0.5rem;
}

.epigraph {
    font-family: 'EB Garamond', serif;
    color: var(--text-secondary);
    font-style: italic;
    text-align: center;
    padding: 2rem;
    border-left: 3px solid var(--accent-dim);
    border-right: 3px solid var(--accent-dim);
    margin: 2rem auto;
    max-width: 700px;
    background: rgba(44, 24, 16, 0.5);
}

.narration {
    font-family: 'EB Garamond', serif;
    color: var(--text-primary);
    font-size: 1.15rem;
    line-height: 1.9;
    padding: 2rem;
    background: linear-gradient(135deg, rgba(44, 24, 16, 0.8) 0%, rgba(26, 20, 16, 0.9) 100%);
    border-radius: 4px;
    border: 1px solid var(--accent-dim);
    box-shadow: inset 0 0 50px rgba(0,0,0,0.3);
}

.ambient-sound {
    font-family: 'EB Garamond', serif;
    color: var(--accent);
    font-style: italic;
    text-align: center;
    padding: 1rem;
    opacity: 0.9;
}

.pov-label {
    font-family: 'Playfair Display', serif;
    color: var(--accent);
    font-size: 1.5rem;
    text-transform: uppercase;
    letter-spacing: 0.3em;
    text-align: center;
    margin-bottom: 1rem;
}

.specimen-card {
    background: rgba(44, 24, 16, 0.9);
    border: 1px solid var(--accent-dim);
    border-radius: 4px;
    padding: 1.5rem;
    margin: 1rem 0;
    transition: all 0.3s ease;
}

.specimen-card:hover {
    border-color: var(--accent);
    box-shadow: 0 0 20px rgba(212, 165, 116, 0.2);
}

.specimen-title {
    font-family: 'Playfair Display', serif;
    color: var(--accent);
    font-size: 1.2rem;
    margin-bottom: 0.5rem;
}

.specimen-text {
    font-family: 'EB Garamond', serif;
    color: var(--text-primary);
    font-size: 1rem;
    line-height: 1.7;
}

.secret-reveal {
    background: linear-gradient(135deg, rgba(139, 69, 19, 0.3) 0%, rgba(44, 24, 16, 0.9) 100%);
    border: 1px solid var(--danger);
    padding: 1.5rem;
    margin-top: 1rem;
    border-radius: 4px;
    animation: fadeIn 0.5s ease;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(-10px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes flicker {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.8; }
    75% { opacity: 0.9; }
}

.flickering {
    animation: flicker 3s infinite;
}

/* Streamlit overrides */
.stSelectbox label, .stSlider label, .stRadio label {
    font-family: 'EB Garamond', serif !important;
    color: var(--text-secondary) !important;
}

.stButton > button {
    font-family: 'EB Garamond', serif !important;
    background: var(--bg-tertiary) !important;
    color: var(--text-primary) !important;
    border: 1px solid var(--accent-dim) !important;
    transition: all 0.3s ease !important;
}

.stButton > button:hover {
    border-color: var(--accent) !important;
    box-shadow: 0 0 15px rgba(212, 165, 116, 0.3) !important;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 2px;
    background: var(--bg-secondary);
}

.stTabs [data-baseweb="tab"] {
    font-family: 'EB Garamond', serif !important;
    color: var(--text-secondary) !important;
    background: var(--bg-tertiary) !important;
}

.stTabs [aria-selected="true"] {
    color: var(--accent) !important;
    border-bottom: 2px solid var(--accent) !important;
}

.stExpander {
    background: var(--bg-secondary) !important;
    border: 1px solid var(--accent-dim) !important;
}

hr {
    border-color: var(--accent-dim) !important;
}
</style>
"""

GOTHIC_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Cormorant+Garamond:ital,wght@0,400;0,600;1,400&display=swap');

:root {
    --bg-primary: #0a0a0a;
    --bg-secondary: #1a0a0a;
    --bg-tertiary: #2a1515;
    --text-primary: #e8e0d0;
    --text-secondary: #a09080;
    --accent: #8b0000;
    --accent-bright: #cc0000;
    --silver: #c0c0c0;
}

.stApp {
    background: radial-gradient(ellipse at center, var(--bg-secondary) 0%, var(--bg-primary) 70%);
}

.main-title {
    font-family: 'Cinzel', serif;
    color: var(--accent-bright);
    text-align: center;
    font-size: 4rem;
    text-shadow: 0 0 40px rgba(139, 0, 0, 0.6), 0 0 80px rgba(139, 0, 0, 0.3);
    letter-spacing: 0.2em;
    margin-bottom: 0;
    animation: pulse 4s infinite;
}

@keyframes pulse {
    0%, 100% { text-shadow: 0 0 40px rgba(139, 0, 0, 0.6), 0 0 80px rgba(139, 0, 0, 0.3); }
    50% { text-shadow: 0 0 60px rgba(139, 0, 0, 0.8), 0 0 100px rgba(139, 0, 0, 0.5); }
}

.subtitle {
    font-family: 'Cormorant Garamond', serif;
    color: var(--silver);
    text-align: center;
    font-size: 1.3rem;
    font-style: italic;
    letter-spacing: 0.1em;
}

.epigraph {
    font-family: 'Cormorant Garamond', serif;
    color: var(--silver);
    font-style: italic;
    text-align: center;
    padding: 2rem;
    border-top: 1px solid var(--accent);
    border-bottom: 1px solid var(--accent);
    margin: 2rem auto;
    max-width: 700px;
    background: rgba(26, 10, 10, 0.7);
}

.narration {
    font-family: 'Cormorant Garamond', serif;
    color: var(--text-primary);
    font-size: 1.2rem;
    line-height: 2;
    padding: 2.5rem;
    background: linear-gradient(180deg, rgba(26, 10, 10, 0.9) 0%, rgba(10, 10, 10, 0.95) 100%);
    border-left: 3px solid var(--accent);
    box-shadow: -5px 0 30px rgba(139, 0, 0, 0.2);
}

.ambient-sound {
    font-family: 'Cormorant Garamond', serif;
    color: var(--accent-bright);
    font-style: italic;
    text-align: center;
    padding: 1.5rem;
    text-shadow: 0 0 10px rgba(139, 0, 0, 0.5);
    animation: flicker 2s infinite;
}

@keyframes flicker {
    0%, 100% { opacity: 1; }
    92% { opacity: 1; }
    93% { opacity: 0.6; }
    94% { opacity: 1; }
    96% { opacity: 0.7; }
    97% { opacity: 1; }
}

.pov-label {
    font-family: 'Cinzel', serif;
    color: var(--accent-bright);
    font-size: 1.8rem;
    text-transform: uppercase;
    letter-spacing: 0.4em;
    text-align: center;
    margin-bottom: 1.5rem;
    text-shadow: 0 0 20px rgba(139, 0, 0, 0.5);
}

.specimen-card {
    background: rgba(26, 10, 10, 0.9);
    border: 1px solid var(--accent);
    border-radius: 0;
    padding: 1.5rem;
    margin: 1rem 0;
    transition: all 0.3s ease;
    position: relative;
}

.specimen-card:hover {
    border-color: var(--accent-bright);
    box-shadow: 0 0 30px rgba(139, 0, 0, 0.4);
}

.specimen-title {
    font-family: 'Cinzel', serif;
    color: var(--accent-bright);
    font-size: 1.3rem;
    margin-bottom: 0.5rem;
}

.specimen-text {
    font-family: 'Cormorant Garamond', serif;
    color: var(--text-primary);
    font-size: 1.05rem;
    line-height: 1.8;
}

.secret-reveal {
    background: linear-gradient(135deg, rgba(139, 0, 0, 0.2) 0%, rgba(10, 10, 10, 0.95) 100%);
    border: 1px solid var(--accent-bright);
    padding: 1.5rem;
    margin-top: 1rem;
    animation: bloodReveal 0.8s ease;
}

@keyframes bloodReveal {
    from { opacity: 0; border-color: transparent; box-shadow: none; }
    to { opacity: 1; border-color: var(--accent-bright); box-shadow: 0 0 20px rgba(139, 0, 0, 0.5); }
}

/* Streamlit overrides */
.stSelectbox label, .stSlider label, .stRadio label {
    font-family: 'Cormorant Garamond', serif !important;
    color: var(--text-secondary) !important;
}

.stButton > button {
    font-family: 'Cinzel', serif !important;
    background: var(--bg-tertiary) !important;
    color: var(--text-primary) !important;
    border: 1px solid var(--accent) !important;
    transition: all 0.3s ease !important;
}

.stButton > button:hover {
    background: var(--accent) !important;
    color: var(--text-primary) !important;
    box-shadow: 0 0 25px rgba(139, 0, 0, 0.6) !important;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 0;
    background: var(--bg-secondary);
    border-bottom: 1px solid var(--accent);
}

.stTabs [data-baseweb="tab"] {
    font-family: 'Cinzel', serif !important;
    color: var(--text-secondary) !important;
    background: transparent !important;
}

.stTabs [aria-selected="true"] {
    color: var(--accent-bright) !important;
    background: rgba(139, 0, 0, 0.1) !important;
}

.stExpander {
    background: var(--bg-secondary) !important;
    border: 1px solid var(--accent) !important;
}

hr {
    border-color: var(--accent) !important;
}
</style>
"""

CLINICAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=Source+Serif+Pro:ital@0;1&display=swap');

:root {
    --bg-primary: #f5f5f0;
    --bg-secondary: #ffffff;
    --bg-tertiary: #e8e8e3;
    --text-primary: #1a1a1a;
    --text-secondary: #4a4a4a;
    --accent: #2f4f4f;
    --accent-light: #5f7f7f;
    --surgical: #3d6b6b;
    --bone: #e8e4dc;
}

.stApp {
    background: var(--bg-primary);
}

.main-title {
    font-family: 'Inter', sans-serif;
    color: var(--text-primary);
    text-align: center;
    font-size: 2.5rem;
    font-weight: 300;
    letter-spacing: 0.3em;
    text-transform: uppercase;
    margin-bottom: 0;
    border-bottom: 1px solid var(--accent);
    padding-bottom: 1rem;
}

.subtitle {
    font-family: 'Inter', sans-serif;
    color: var(--text-secondary);
    text-align: center;
    font-size: 0.9rem;
    font-weight: 400;
    letter-spacing: 0.15em;
    text-transform: uppercase;
}

.epigraph {
    font-family: 'Source Serif Pro', serif;
    color: var(--text-secondary);
    font-style: italic;
    text-align: left;
    padding: 1.5rem;
    border-left: 4px solid var(--accent);
    margin: 2rem auto;
    max-width: 700px;
    background: var(--bg-secondary);
}

.narration {
    font-family: 'Inter', sans-serif;
    color: var(--text-primary);
    font-size: 1rem;
    line-height: 1.8;
    font-weight: 300;
    padding: 2rem;
    background: var(--bg-secondary);
    border: 1px solid var(--bg-tertiary);
    border-radius: 2px;
}

.ambient-sound {
    font-family: 'Inter', sans-serif;
    color: var(--accent);
    font-style: normal;
    font-weight: 500;
    text-align: left;
    padding: 0.75rem 1rem;
    background: var(--bone);
    border-left: 3px solid var(--surgical);
    margin: 0.5rem 0;
    font-size: 0.9rem;
}

.pov-label {
    font-family: 'Inter', sans-serif;
    color: var(--accent);
    font-size: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 0.25em;
    font-weight: 600;
    text-align: left;
    margin-bottom: 0.5rem;
    padding: 0.5rem;
    background: var(--bone);
    display: inline-block;
}

.specimen-card {
    background: var(--bg-secondary);
    border: 1px solid var(--bg-tertiary);
    border-radius: 2px;
    padding: 1.5rem;
    margin: 0.75rem 0;
    transition: all 0.2s ease;
}

.specimen-card:hover {
    border-color: var(--accent);
}

.specimen-title {
    font-family: 'Inter', sans-serif;
    color: var(--accent);
    font-size: 0.9rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 0.5rem;
}

.specimen-text {
    font-family: 'Inter', sans-serif;
    color: var(--text-primary);
    font-size: 0.95rem;
    line-height: 1.7;
    font-weight: 300;
}

.secret-reveal {
    background: var(--bone);
    border-left: 4px solid var(--surgical);
    padding: 1.5rem;
    margin-top: 1rem;
}

/* Streamlit overrides */
.stSelectbox label, .stSlider label, .stRadio label {
    font-family: 'Inter', sans-serif !important;
    color: var(--text-secondary) !important;
    font-weight: 500 !important;
    text-transform: uppercase !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.1em !important;
}

.stButton > button {
    font-family: 'Inter', sans-serif !important;
    font-weight: 500 !important;
    background: var(--bg-secondary) !important;
    color: var(--text-primary) !important;
    border: 1px solid var(--accent) !important;
    border-radius: 2px !important;
    text-transform: uppercase !important;
    letter-spacing: 0.1em !important;
    font-size: 0.8rem !important;
}

.stButton > button:hover {
    background: var(--accent) !important;
    color: var(--bg-secondary) !important;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 0;
    background: var(--bg-tertiary);
}

.stTabs [data-baseweb="tab"] {
    font-family: 'Inter', sans-serif !important;
    color: var(--text-secondary) !important;
    font-weight: 500 !important;
    text-transform: uppercase !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.1em !important;
}

.stTabs [aria-selected="true"] {
    color: var(--accent) !important;
    border-bottom: 2px solid var(--accent) !important;
}

.stExpander {
    background: var(--bg-secondary) !important;
    border: 1px solid var(--bg-tertiary) !important;
}

hr {
    border-color: var(--bg-tertiary) !important;
}
</style>
"""

THEMES = {
    "gaslight": GASLIGHT_CSS,
    "gothic": GOTHIC_CSS,
    "clinical": CLINICAL_CSS
}


# =============================================================================
# INTENSITY EFFECTS
# =============================================================================

INTENSITY_NAMES = {
    1: "Candlelit",
    2: "Uneasy",
    3: "Tense",
    4: "Dread",
    5: "Visceral"
}

def get_intensity_css(intensity: int) -> str:
    if intensity <= 2:
        return ""
    effects = []
    if intensity >= 3:
        effects.append("""
        .narration { animation: subtle-shift 8s infinite; }
        @keyframes subtle-shift { 0%, 100% { filter: brightness(1); } 50% { filter: brightness(0.95); } }
        """)
    if intensity >= 4:
        effects.append("""
        .ambient-sound { animation: unease 3s infinite; }
        @keyframes unease { 0%, 100% { transform: translateX(0); } 25% { transform: translateX(1px); } 75% { transform: translateX(-1px); } }
        """)
    if intensity >= 5:
        effects.append("""
        .main-title { animation: glitch 0.5s infinite; }
        @keyframes glitch {
            0%, 100% { text-shadow: inherit; }
            25% { text-shadow: -2px 0 #ff0000, 2px 0 #00ff00; }
            50% { text-shadow: 2px 0 #ff0000, -2px 0 #00ff00; }
            75% { text-shadow: 0 -1px #ff0000, 0 1px #00ff00; }
        }
        .narration { animation: static 0.1s infinite; }
        @keyframes static { 0%, 100% { opacity: 1; } 50% { opacity: 0.98; } }
        """)
    return f"<style>{''.join(effects)}</style>"


# =============================================================================
# SESSION STATE INITIALIZATION
# =============================================================================

def init_session_state():
    defaults = {
        "pov": None,
        "mode": "gaslight",
        "intensity": 2,
        "visit_count": 0,
        "discovered_secrets": [],
        "examined_regions": [],
        "examined_specimens": [],
        "examined_table_items": [],
        "selected_table_item": None,
        "uv_active": False,
        "current_region": None,
        "show_intro": True,
        "random_seed": random.randint(0, 10000)
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


# =============================================================================
# HELPER: add to list without duplicates (BUG FIX: Strict Array Reassignment)
# =============================================================================

def add_to_list(state_key: str, item) -> None:
    """Safely append an item to a session state list via reassignment."""
    if item not in st.session_state[state_key]:
        st.session_state[state_key] = st.session_state[state_key] + [item]


# =============================================================================
# HELPER: check and reveal secrets
# =============================================================================

def try_reveal_secrets():
    """Check all secrets against current state and reveal any that match."""
    pov = st.session_state.pov
    mode = st.session_state.mode
    intensity = st.session_state.intensity
    regions = st.session_state.examined_regions
    specimens = st.session_state.examined_specimens
    visits = st.session_state.visit_count
    revealed = []

    for secret in SECRETS:
        sid = secret["id"]
        if sid in st.session_state.discovered_secrets:
            continue
        if check_secret_condition(secret, pov, mode, intensity, regions, specimens, visits):
            add_to_list("discovered_secrets", sid)
            revealed.append(secret)

    return revealed


# =============================================================================
# MAIN APPLICATION
# =============================================================================

def render_intro():
    st.markdown('<h1 class="main-title">The Anatomy Theatre</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">An Immersive Experience</p>', unsafe_allow_html=True)

    epigraph = get_random_epigraph()
    st.markdown(f'<div class="epigraph">{epigraph}</div>', unsafe_allow_html=True)

    st.markdown("---")

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown("### Choose Your Perspective")

        pov_descriptions = {
            "The Observer": "Watch from the gallery. See what others miss.",
            "The Anatomist": "Wield the blade. Feel the power of revelation.",
            "The Investigator": "Search for truth among the secrets.",
            "The Subject": "Experience the table. Know the cold."
        }

        pov_choice = st.radio(
            "Who are you tonight?",
            list(pov_descriptions.keys()),
            format_func=lambda x: f"{x}",
            label_visibility="collapsed"
        )

        st.caption(pov_descriptions[pov_choice])

        st.markdown("---")

        intensity = st.slider(
            "Intensity",
            min_value=1,
            max_value=5,
            value=st.session_state.intensity,
            help="How deep do you wish to go?"
        )
        st.caption(f"*{INTENSITY_NAMES[intensity]}*")

        st.markdown("---")

        if st.button("Enter the Theatre", use_container_width=True, type="primary"):
            pov_map = {
                "The Observer": "observer",
                "The Anatomist": "anatomist",
                "The Investigator": "investigator",
                "The Subject": "subject"
            }
            st.session_state.pov = pov_map[pov_choice]
            st.session_state.intensity = intensity
            st.session_state.show_intro = False
            st.session_state.visit_count += 1
            st.rerun()


def render_theatre():
    pov = st.session_state.pov
    mode = st.session_state.mode
    intensity = st.session_state.intensity

    random.seed(st.session_state.random_seed + st.session_state.visit_count)

    pov_titles = {
        "observer": "THE OBSERVER",
        "anatomist": "THE ANATOMIST",
        "investigator": "THE INVESTIGATOR",
        "subject": "THE SUBJECT"
    }

    st.markdown(f'<div class="pov-label">{pov_titles[pov]}</div>', unsafe_allow_html=True)

    with st.expander("⚙️ Theatre Controls", expanded=False):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.selectbox(
                "Visual Mode",
                ["gaslight", "gothic", "clinical"],
                key="mode",
                format_func=lambda x: x.title()
            )
        with col2:
            st.slider(
                "Intensity",
                1, 5,
                key="intensity",
                help=INTENSITY_NAMES[st.session_state.intensity]
            )
        with col3:
            if st.button("Change Perspective"):
                st.session_state.show_intro = True
                st.rerun()

    st.markdown("---")
    
    # Global placeholder to render newly discovered secrets above the tabs
    secret_placeholder = st.container()

    tab1, tab2, tab3 = st.tabs(["🎭 3D Theatre", "📜 The Scene", "🔪 Dissection Table"])

    with tab1:
        render_3d_theatre(mode, intensity)
    with tab2:
        render_scene(pov, mode, intensity)
    with tab3:
        render_dissection_table(pov, mode, intensity)

    # BUG FIX: Evaluate secrets after the tabs have rendered to catch any widget interactions, 
    # but render the results back up into the secret_placeholder at the top of the UI.
    revealed = try_reveal_secrets()
    if revealed:
        with secret_placeholder:
            for secret in revealed:
                st.markdown(
                    f'<div class="secret-reveal" style="margin-bottom: 2rem;">'
                    f'<strong>Something catches your attention...</strong><br><br>{secret["content"]}</div>',
                    unsafe_allow_html=True
                )


def render_scene(pov: str, mode: str, intensity: int):
    opening = get_opening(pov, mode)
    st.markdown(f'<div class="narration">{opening}</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    num_sounds = min(intensity, 3)
    for _ in range(num_sounds):
        sound = get_ambient_sound(intensity)
        st.markdown(f'<div class="ambient-sound">{sound}</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    observation = get_ambient_observation(pov)
    st.markdown(f'<div class="narration" style="font-style: italic;">{observation}</div>',
                unsafe_allow_html=True)


def render_dissection_table(pov: str, mode: str, intensity: int):
    """Render the immersive dissection table — SVG + examination panel."""
    st.markdown("### The Dissection Table")
    st.markdown("*Marble slab. Drainage channels. The instruments of revelation arranged with surgical precision.*")
    st.markdown("---")

    # UV toggle
    col_uv, col_spacer = st.columns([1, 3])
    with col_uv:
        uv_on = st.toggle("🔮 UV Lamp", value=st.session_state.uv_active, key="uv_toggle")
        st.session_state.uv_active = uv_on

    # ── SVG Table (will be rendered by theatre_2d_svg.py in next phase) ──
    # For now, placeholder that proves the tab works and state flows correctly
    import streamlit.components.v1 as components

    # Collect items for the table
    table_items = get_dissection_table_items()

    # Item categories for the selection panel
    organs = [i for i in table_items if i["category"] == "organ"]
    instruments = [i for i in table_items if i["category"] == "instrument"]
    details = [i for i in table_items if i["category"] == "detail"]

    # ── Layout: SVG left, examination panel right ──
    col_table, col_exam = st.columns([3, 2])

    with col_table:
        # PLACEHOLDER: This will become the full interactive SVG
        # rendered via components.html() from theatre_2d_svg.py
        mode_colors = {
            "gaslight": {"bg": "#2c1810", "marble": "#8a7d6b", "accent": "#d4a574", "channel": "#6b5a3e"},
            "gothic": {"bg": "#1a0a0a", "marble": "#2a1a1a", "accent": "#8b0000", "channel": "#4a0000"},
            "clinical": {"bg": "#f5f5f0", "marble": "#e8e4dc", "accent": "#2f4f4f", "channel": "#c0c0c0"},
        }
        c = mode_colors.get(mode, mode_colors["gaslight"])
        uv_filter = ""
        if uv_on:
            uv_filter = f'''
                <rect width="900" height="600" fill="rgba(20,0,60,0.85)" />
                <text x="450" y="300" text-anchor="middle" fill="#7b68ee"
                      font-size="18" font-family="serif" opacity="0.7">
                    UV ACTIVE — Hidden marks revealed
                </text>
                <text x="450" y="340" text-anchor="middle" fill="#9370db"
                      font-size="12" font-family="serif" font-style="italic" opacity="0.5">
                    THE WARREN PROTOCOL CONTINUES
                </text>
            '''

        placeholder_svg = f'''
        <svg viewBox="0 0 900 600" xmlns="http://www.w3.org/2000/svg"
             style="width:100%; background:{c['bg']}; border-radius:4px;">
            <!-- Table surface -->
            <rect x="50" y="50" width="800" height="500" rx="8"
                  fill="{c['marble']}" stroke="{c['accent']}" stroke-width="2" opacity="0.9"/>
            <!-- Drainage channels -->
            <line x1="150" y1="60" x2="150" y2="540" stroke="{c['channel']}" stroke-width="3" opacity="0.6"/>
            <line x1="450" y1="60" x2="450" y2="540" stroke="{c['channel']}" stroke-width="3" opacity="0.6"/>
            <line x1="750" y1="60" x2="750" y2="540" stroke="{c['channel']}" stroke-width="3" opacity="0.6"/>
            <line x1="60" y1="300" x2="840" y2="300" stroke="{c['channel']}" stroke-width="2" opacity="0.4"/>
            <!-- Region labels -->
            <text x="250" y="180" text-anchor="middle" fill="{c['accent']}" font-size="14"
                  font-family="serif" opacity="0.8">— ORGANS —</text>
            <text x="650" y="180" text-anchor="middle" fill="{c['accent']}" font-size="14"
                  font-family="serif" opacity="0.8">— INSTRUMENTS —</text>
            <text x="450" y="450" text-anchor="middle" fill="{c['accent']}" font-size="14"
                  font-family="serif" opacity="0.8">— PERSONAL EFFECTS —</text>
            <!-- Organ placeholders -->
            <text x="200" y="240" text-anchor="middle" fill="{c['accent']}" font-size="20" opacity="0.6">🫀</text>
            <text x="300" y="240" text-anchor="middle" fill="{c['accent']}" font-size="20" opacity="0.6">🧠</text>
            <text x="200" y="310" text-anchor="middle" fill="{c['accent']}" font-size="20" opacity="0.6">🫁</text>
            <text x="300" y="310" text-anchor="middle" fill="{c['accent']}" font-size="20" opacity="0.6">👁️</text>
            <text x="250" y="380" text-anchor="middle" fill="{c['accent']}" font-size="20" opacity="0.6">🦴</text>
            <!-- Instrument placeholders -->
            <text x="600" y="240" text-anchor="middle" fill="{c['accent']}" font-size="18" opacity="0.6">🪚</text>
            <text x="700" y="240" text-anchor="middle" fill="{c['accent']}" font-size="18" opacity="0.6">🔪</text>
            <text x="600" y="310" text-anchor="middle" fill="{c['accent']}" font-size="18" opacity="0.6">🪡</text>
            <text x="700" y="310" text-anchor="middle" fill="{c['accent']}" font-size="18" opacity="0.6">🔍</text>
            <!-- Detail placeholders -->
            <text x="350" y="500" text-anchor="middle" fill="{c['accent']}" font-size="18" opacity="0.6">🕯️</text>
            <text x="450" y="500" text-anchor="middle" fill="{c['accent']}" font-size="18" opacity="0.6">⌚</text>
            <text x="550" y="500" text-anchor="middle" fill="{c['accent']}" font-size="18" opacity="0.6">🌹</text>
            <!-- Waiting text -->
            <text x="450" y="40" text-anchor="middle" fill="{c['accent']}" font-size="11"
                  font-family="serif" font-style="italic" opacity="0.5">
                Select an item below to examine — full SVG rendering coming soon
            </text>
            {uv_filter}
        </svg>
        '''
        st.markdown(placeholder_svg, unsafe_allow_html=True)

    with col_exam:
        st.markdown("#### Examination")

        # Build selection list from all table items
        item_names = {item["id"]: item["name"] for item in table_items}
        item_labels = {item["id"]: f'{item["icon"]} {item["name"]}' for item in table_items}

        selected_id = st.selectbox(
            "Select item to examine:",
            list(item_names.keys()),
            format_func=lambda x: item_labels.get(x, x),
            key="table_item_selector"
        )

        if selected_id:
            st.session_state.selected_table_item = selected_id
            add_to_list("examined_table_items", selected_id)

            # Also track as examined_regions/specimens for secret triggers
            selected_item = next((i for i in table_items if i["id"] == selected_id), None)
            if selected_item:
                # Map organs to examined_regions for secret compatibility
                if selected_item["category"] == "organ":
                    region_key = selected_item.get("region_key")
                    if region_key:
                        add_to_list("examined_regions", region_key)

                # Map items to examined_specimens for secret compatibility
                specimen_key = selected_item.get("specimen_key")
                if specimen_key:
                    add_to_list("examined_specimens", specimen_key)

                # ── Render examination card ──
                layer_tabs = st.tabs(["📋 Medical", "🔒 Hidden", "💭 Personal"])

                with layer_tabs[0]:
                    medical_text = selected_item.get("medical", "No medical notes available.")
                    st.markdown(
                        f'<div class="specimen-text">{medical_text}</div>',
                        unsafe_allow_html=True
                    )

                with layer_tabs[1]:
                    lore_text = selected_item.get("lore", "Nothing hidden... yet.")
                    # Only show if intensity >= 3
                    if intensity >= 3:
                        st.markdown(
                            f'<div class="specimen-text" style="font-style: italic;">{lore_text}</div>',
                            unsafe_allow_html=True
                        )
                    else:
                        st.markdown(
                            f'<div class="specimen-text" style="opacity:0.5;">'
                            f'<em>Increase intensity to reveal hidden details...</em></div>',
                            unsafe_allow_html=True
                        )

                with layer_tabs[2]:
                    emotional_data = selected_item.get("emotional", {})
                    if isinstance(emotional_data, dict):
                        emotional_text = emotional_data.get(pov, emotional_data.get("observer", ""))
                    else:
                        emotional_text = emotional_data
                    st.markdown(
                        f'<div class="specimen-text">{emotional_text}</div>',
                        unsafe_allow_html=True
                    )

                # UV reveal
                if uv_on:
                    uv_text = selected_item.get("uv_text", "")
                    if uv_text:
                        st.markdown(
                            f'<div class="secret-reveal" style="border-color: #7b68ee; '
                            f'background: linear-gradient(135deg, rgba(75,0,130,0.3), rgba(20,0,40,0.9));">'
                            f'<strong style="color:#9370db;">🔮 UV Reveals:</strong><br><br>'
                            f'<span style="color:#b8a9e8;">{uv_text}</span></div>',
                            unsafe_allow_html=True
                        )


def render_3d_theatre(mode: str, intensity: int):
    st.markdown("### Enter the Theatre")
    st.markdown("*An immersive view of the anatomical demonstration space.*")
    theatre_html = get_theatre_3d(mode, intensity)
    import streamlit.components.v1 as components
    components.html(theatre_html, height=600, scrolling=False)


# =============================================================================
# MAIN ENTRY POINT
# =============================================================================

def main():
    init_session_state()
    mode = st.session_state.mode
    st.markdown(THEMES.get(mode, GASLIGHT_CSS), unsafe_allow_html=True)
    intensity = st.session_state.intensity
    st.markdown(get_intensity_css(intensity), unsafe_allow_html=True)

    if st.session_state.show_intro or st.session_state.pov is None:
        render_intro()
    else:
        render_theatre()

    st.markdown("---")
    discovered = len(st.session_state.discovered_secrets)
    total = len(SECRETS)
    st.markdown(
        f'<p style="text-align: center; opacity: 0.5; font-size: 0.8rem;">'
        f'The Anatomy Theatre • A Crimson Rose Experience • 🌹 '
        f'• Secrets discovered: {discovered}/{total}'
        f'</p>',
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
