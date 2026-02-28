# 🎭 The Anatomy Theatre

An immersive, atmospheric interactive experience set in a Victorian anatomy theatre. Explore from multiple perspectives, uncover dark secrets, and experience the world of **The Crimson Rose** series.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.54+-red)
![Three.js](https://img.shields.io/badge/Three.js-r128-green)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 🌹 About

Step into a gaslit world of medical ambition, secret societies, and moral corruption. The Anatomy Theatre is an interactive companion piece to *The Crimson Rose* historical fiction thriller series.

### 🎮 NEW: Immersive 3D Theatre

Experience a fully realized Victorian anatomy theatre in 3D:
- **Circular tiered gallery** with seating for spectators
- **Central dissection table** with draped subject
- **Flickering gaslights** that respond to your chosen mode
- **Floating dust particles** for atmospheric depth
- **Specimen cabinets** with glowing jars
- **Orbit camera controls** — drag to rotate, scroll to zoom
- **Auto-rotating view** with haunting quotes
- **Three visual modes** that completely transform the lighting

**Experience the theatre from four perspectives:**

| Perspective | Experience |
|-------------|------------|
| 🪑 **The Observer** | Watch from the gallery. Notice what others miss. |
| 🔪 **The Anatomist** | Wield the blade. Feel the cold precision of discovery. |
| 🔍 **The Investigator** | Search for evidence. Expose the Society's crimes. |
| 💀 **The Subject** | Know the cold. Experience dissolution. |

**Three visual modes:**

- 🕯️ **Gaslight** — Warm sepia tones, elegant serif typography, historical immersion
- 🩸 **Gothic** — Crimson and shadow, dramatic horror, theatrical dread  
- 🔬 **Clinical** — Stark white, clean sans-serif, unsettling detachment

**Five intensity levels:**

1. *Candlelit* — Calm, atmospheric
2. *Uneasy* — Subtle wrongness
3. *Tense* — Intrusive thoughts, hidden content appears
4. *Dread* — Fragmented prose, time distortion
5. *Visceral* — Full horror, text effects, sensory overload

---

## ✨ Features

- **🎮 Immersive 3D Theatre** — Full Three.js environment with orbit controls, dynamic lighting, and atmospheric effects
- **🧪 Interactive Medical Cabinet** — Victorian apothecary collection with 20+ authentic bottles, 2D inspection mode, and hidden secrets
- **Atmospheric prose narration** that shifts based on POV, visual mode, and intensity
- **Interactive anatomy diagram** — examine the subject's body, uncover medical and hidden lore
- **Specimen cabinet** — explore preserved organs, documents, and personal effects
- **Hidden secrets** — discover clues about the Red Rose Society, the Black Book, and more
- **Text-described ambient audio** — immersive soundscape rendered in prose
- **Direct ties to The Crimson Rose** — references to Alistair Fitzroy, Sebastian Carlisle, the Progressive Women's Society, and more

---

## 🚀 Quick Start

### Run Locally

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/anatomy-theatre.git
cd anatomy-theatre

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

### Deploy to Streamlit Cloud

1. Push this repository to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click "New app" → Select your repository
4. Set main file path: `app.py`
5. Deploy!

---

## 📁 Project Structure

```
anatomy-theatre/
├── app.py              # Main Streamlit application
├── content.py          # All narrative content, specimens, secrets
├── theatre_3d.py       # 3D Three.js theatre generator
├── cabinet_3d.py       # 3D Victorian medical cabinet
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

---

## 🎨 Customization

### Adding New Content

Edit `content.py` to add:

- **New POV openings** — Add entries to `OPENINGS` dict
- **Ambient sounds** — Add lines to `AMBIENT_SOUNDS` by intensity level
- **Specimen items** — Add to `SPECIMENS` dict
- **Secrets** — Add trigger conditions and content to `SECRETS` list

### Modifying Themes

CSS themes are embedded in `app.py`:

- `GASLIGHT_CSS` — Victorian warmth
- `GOTHIC_CSS` — Horror atmosphere
- `CLINICAL_CSS` — Modern sterility

Each theme uses CSS custom properties for easy color adjustments.

---

## 📚 The Crimson Rose Series

*The Anatomy Theatre* is set in the world of **The Crimson Rose**, a historical fiction thriller series exploring:

- Medical ethics and ambition in Victorian England
- Secret societies and institutional corruption
- The fight for women's rights in science and medicine
- Psychological manipulation and redemption

**Factions featured:**
- 🌹 Red Rose Society — Elite medical order with sinister ideals
- 📜 Progressive Women's Society — Feminist intellectuals fighting patriarchal science
- 🌿 Underground Network of Healers — Grassroots collective of outcasts and midwives
- ⚕️ Progressive Physicians' Circle — Radical reformers
- 💀 Anatomy Club — Students trafficking in bodies and secrets

---

## 🛠️ Technical Details

- **Framework:** Streamlit 1.54+
- **3D Engine:** Three.js r128 (loaded via CDN)
- **Python:** 3.10+
- **Styling:** Custom CSS injection via `st.markdown`
- **3D Rendering:** Embedded HTML/JS via `st.components.v1.html`
- **State Management:** `st.session_state` for POV, mode, intensity, discoveries
- **Content:** Procedural + curated narrative layers

---

## 📄 License

MIT License — feel free to adapt and expand!

---

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Inspired by Victorian anatomy theatres and Gothic literature
- Part of *The Crimson Rose* universe

---

<p align="center">
  <em>"The theatre is full tonight. They have come to see inside the human form — but it is their own interiors they will glimpse, reflected in the glass of the specimen jars."</em>
  <br><br>
  🌹
</p>
