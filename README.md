# 🎭 The Anatomy Theatre

An immersive, atmospheric interactive experience set in a Victorian anatomy theatre. Built with Streamlit and Three.js. Part of **The Crimson Rose** series.

## Overview

Step into the gaslit world of 1880s London. Choose your perspective — observer, anatomist, investigator, or subject — and explore a fully realized anatomy theatre through narrative text, interactive 3D environments, and layered secrets waiting to be uncovered.

## Features

### 3D Anatomy Theatre
A full Three.js scene with orbit controls, clickable objects, and atmospheric effects:
- Tiered gallery with spectators (some wearing Red Rose pins)
- Domed ceiling with painted fresco and grand chandelier
- Stone columns, arched entrance doorway, and anatomical wall charts
- Dissection table with draped subject and working anatomist
- Gaslights, candelabras, and fog effects
- Grandfather clock with animated pendulum
- Drainage channels with liquid at higher intensities
- Rats, ravens, blood stains, and a second stretcher — all scaling with intensity
- Hidden red roses to discover

### 3D Apothecary Cabinet (The Fitzroy Collection)
An interactive Victorian medical cabinet with UV blacklight mode:
- 15 labelled bottles with lore (Laudanum, Vita Aeterna, Strychnine, and more)
- Human skull, dripping candle, leather-bound books
- Brass balance scales, mortar & pestle, Victorian syringe
- Magnifying glass, pocket watch, wax seal stamps
- Cobwebs, dust particles, dried herbs, chemical stains
- Mouse peeking out at higher intensities
- UV mode reveals hidden text and messages on the back wall

### Narrative System
- **4 POVs**: Observer, Anatomist, Investigator, Subject — each with unique openings and observations
- **3 Visual Modes**: Gaslight (warm amber), Gothic (crimson horror), Clinical (sterile white)
- **5 Intensity Levels**: From Candlelit (1) to Visceral (5) — controls atmosphere, CSS effects, creature spawns, and narrative darkness
- **6 Hidden Secrets**: Unlocked through specific combinations of POV, mode, intensity, and exploration progress
- **Specimen Cabinet**: 12 specimens across 3 categories, each with hidden details revealed on examination

### Anatomy Examination
Interactive body region selector with three content layers per region:
- **Medical**: Clinical anatomical description
- **Hidden**: Lore from the Black Book, Fitzroy Protocol, and faction documents
- **Personal**: POV-specific emotional reactions

## File Structure

```
├── app.py            # Main Streamlit application (UI, routing, state management)
├── content.py        # All narrative content, specimens, secrets, and helper functions
├── theatre_3d.py     # 3D anatomy theatre (Three.js r128)
├── cabinet_3d.py     # 3D apothecary cabinet (Three.js r128)
├── requirements.txt  # Python dependencies
└── README.md
```

## Running Locally

```bash
pip install streamlit
streamlit run app.py
```

## Deploying to Streamlit Cloud

1. Push all files to a GitHub repository
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repo and set `app.py` as the main file
4. Deploy

No additional configuration needed — the app uses only Streamlit and the Python standard library. Three.js is loaded via CDN.

## Technical Notes

- **Session-scoped state**: All discovery progress is tracked in `st.session_state`, not module-level variables. Safe for multi-user Streamlit Cloud deployment.
- **Secret triggers**: Programmatic condition evaluation (POV + mode + intensity + exploration progress), not substring matching.
- **Serialization-safe**: Session state uses lists instead of sets for compatibility across Streamlit versions.
- **Three.js r128**: All 3D scenes use Three.js r128 via CDN. No npm dependencies.
- **No JavaScript in markdown**: SVG interactivity uses selectbox fallbacks since Streamlit sanitizes JS event handlers.

## The Crimson Rose

This app is part of an interactive companion experience for *The Crimson Rose* novel series — a historical fiction thriller set in Victorian England exploring medical ethics, institutional corruption, and the dark side of scientific progress.

---

*"The theatre is full tonight. They have come to see inside the human form — but it is their own interiors they will glimpse, reflected in the glass of the specimen jars."*
