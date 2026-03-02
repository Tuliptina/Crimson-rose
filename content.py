"""
The Anatomy Theatre — Content Module
All narrative content, specimens, ambient text, and secrets.
Tied to the world of The Crimson Rose series.

BUG FIX: Removed mutable 'discovered' fields from SECRETS and SPECIMENS.
Discovery state is now tracked exclusively in st.session_state.
"""

import random

# =============================================================================
# POV OPENING NARRATIONS
# =============================================================================

OPENINGS = {
    "observer": {
        "gaslight": """
You take your seat in the third row of the gallery, between a medical student whose hands won't stop moving and a gentleman who smells of pipe tobacco and something sharper underneath.

Below, the table waits. White cloth. Instruments arranged with geometric precision. The gaslights hiss and flicker, casting long shadows that seem to breathe.

*The scratch of chalk on slate. Someone marking attendance.*

You are here to watch. That is all. You will not participate. You will not intervene.

You tell yourself this.

The theatre fills slowly. Whispers rise and fall like tide. A woman in the back row wears a veil — mourning clothes, perhaps, though her posture suggests something other than grief. Anticipation. Recognition.

A red rose is pinned to a gentleman's lapel three rows ahead. You've seen that symbol before. In the newspapers. In the warnings.

The anatomist enters. The crowd falls silent.

It begins.
        """,
        "gothic": """
THE GALLERY BREATHES.

You feel it — the collective inhale of a hundred souls pressed into wooden seats worn smooth by generations of witnesses. The air is thick with carbolic acid and something sweeter. Something wrong.

Below, the table. The cloth. The body beneath it, a landscape of secrets waiting to be excavated.

*Somewhere, a woman weeps. Or laughs. The acoustics make it impossible to tell.*

You should not be here. You know this. The pamphlet in your pocket — the one from the Progressive Women's Society — burns against your thigh. THEY USE OUR SISTERS FOR SPECTACLE, it reads. THEY MAKE THEATRE OF OUR DEAD.

And yet.

And yet you came.

The gaslights flare crimson for a moment — a trick of the flame, nothing more — and in that bleeding light you see them: figures in the shadows of the upper gallery, watching the watchers.

One of them is looking directly at you.
        """,
        "clinical": """
SUBJECT: Theatre observation, Session 1
LOCATION: Anatomical demonstration theatre, third-row gallery position
TIME: 19:42

Environmental conditions noted: Gas lighting at approximately 60% illumination. Ambient temperature 16°C. Humidity elevated due to audience respiration. Faint chemical odor consistent with preservation compounds.

Observer count: 94 individuals. Demographics skew male (78%), age range 20-55. Three females present in rear gallery — unusual for public demonstration.

Notable details:
- Red floral pin observed on 4 audience members (pattern?)
- One attendee taking shorthand notes (press? documentation?)
- Anatomist has not yet entered
- Subject on table: covered, unmoving, gender indeterminate from this position

Personal notation: Elevated heart rate. Sweating despite cool temperature. These are involuntary responses. They mean nothing.

The demonstration will begin shortly.

You are here to observe. Document. Understand.

Nothing more.
        """
    },

    "anatomist": {
        "gaslight": """
The instruments are arranged. The subject is draped. The audience is — irrelevant. Background noise. Let them watch.

You flex your fingers. Clean hands. Steady hands. Hands that have done this one hundred and seven times.

*One hundred and eight, after tonight.*

The first incision is always the most honest. Before interpretation, before theory — just blade and truth. The body does not lie. The body cannot lie. It is only we who impose meaning upon its silent testimony.

Somewhere in the gallery, a red rose is tucked into a buttonhole. You do not look up. You do not need to.

They are always watching.

Dr. Fitzroy's words echo in your memory: *"The worthy shape progress. The others... contribute differently."* You had dismissed it as rhetoric, once. Now you understand. Now you see.

The scalpel finds your grip like an old friend.

"Ladies and gentlemen," you begin, your voice carrying to the highest gallery, "tonight we examine the architecture of mortality."

You pull back the cloth.
        """,
        "gothic": """
THERE IS A CHURCH IN YOUR HANDS.

Every incision is a prayer. Every organ, a testament. You have held hearts that still dreamed of beating and brains that harbored secrets their owners died to protect.

The audience thinks they understand what they are witnessing. Anatomy. Science. Progress.

They are children watching fire.

*The blade whispers against the strop. Sharper. Always sharper.*

You remember the first time — Edinburgh, the winter of your twenty-third year. How your hands trembled. How the professor had to guide your wrist. "Steady, boy. The dead feel nothing."

He was wrong. You know that now.

The dead feel everything. They simply cannot scream.

The cloth is cold beneath your fingers. The shape beneath it — female, young, cause of death listed as "consumption" though the bruising around her throat tells a different story — awaits your revelation.

Somewhere, a man with a red rose watches.
Somewhere, a ledger holds your name.
Somewhere, Sebastian Carlisle rots in a cell you helped design.

You smile for the audience.

"Shall we begin?"
        """,
        "clinical": """
PRE-PROCEDURE CHECKLIST:
- Instruments sterilized: CONFIRMED
- Subject positioned: CONFIRMED
- Drainage channels clear: CONFIRMED
- Audience safety barriers in place: CONFIRMED
- Documentation photographer present: CONFIRMED

Personal preparation:
- Caffeine consumption: 2 cups, adequate
- Hand tremor: Absent
- Mental state: Focused

The procedure tonight is routine. Thoracic examination, standard demonstration format. Time allocated: 90 minutes. Expected learning outcomes for students: identification of major organs, understanding of circulatory system basics, observation of pathological indicators.

The subject is female, approximately 25-30 years of age, acquired through standard institutional channels. Documentation indicates death by natural causes. This documentation is likely accurate.

Do not think about the documentation.

The audience settles. Your assistant dims the peripheral lights, directing illumination to the central table. Theatrical, yes, but effective. Students learn better when they can focus.

You have done this 107 times.

108 after tonight.

Begin.
        """
    },

    "investigator": {
        "gaslight": """
You shouldn't be here. Women aren't permitted in the main gallery — not officially — but the veil obscures your features and the borrowed mourning dress suggests a grief that grants access to places normally forbidden.

They think you're here for a lost husband. A brother. Perhaps a son.

Let them think what they will.

*The pamphlet crinkles in your pocket. The list of names. The connections you've been tracing for months.*

Three women dead this month alone. All young. All beautiful. All appearing on certain postcards before their bodies appeared on tables like this one.

The French postcards. Thomas Blackwood's special project.

You've seen the studio. You know what he does there. The photographs, the manipulation, the way he makes respectable women look like... like...

And then they die. And then they end up here.

The anatomist enters — not Blackwood himself, but someone connected. They're all connected. The Red Rose Society touches everything in this city like rot in an apple's core.

You pull your notebook from your sleeve.

Tonight, you watch. Tomorrow, you expose.
        """,
        "gothic": """
THE DEAD KNOW YOUR NAME.

You feel their eyes — not the corpse on the table, but all of them. The ones who came before. The ones whose names fill your notebook in increasingly frantic handwriting. The ones who appeared on postcards before appearing on slabs.

Mary. Catherine. Ellen. Jane.

*Their faces swim in your memory. Pretty faces. Trusting faces. Faces that didn't know they'd been photographed until it was far, far too late.*

You are Evelyn's shadow now. You carry her fire while she recovers from what they did to her — what the Society did, what Fitzroy orchestrated, what Blackwood documented in that damned Black Book of his.

The gallery smells like death dressed up as science.

You push through the crowd, a woman in borrowed clothes with borrowed courage, searching for evidence you know is here. It's always here. They can't help themselves. They leave traces like animals marking territory.

A red rose.
A knowing glance.
A ledger entry that doesn't quite add up.

You will find it.

You will burn them all.
        """,
        "clinical": """
INVESTIGATION LOG — Entry 47
OPERATIVE: [REDACTED]
LOCATION: Public anatomical theatre
DATE: [CURRENT]

Cover identity: Mourning widow, recently bereaved. Backstory memorized. Documentation forged. Access granted without incident.

OBJECTIVES:
1. Identify Society members in attendance (look for: red rose pins, specific seating patterns, known associates)
2. Document subject acquisition irregularities
3. Photograph any evidence of Fitzroy Protocol implementation
4. Note exits, guard positions, potential extraction routes

PRELIMINARY OBSERVATIONS:
- 4 confirmed rose pins visible from current position
- Subject on table matches description of missing person #23 (Sarah Whitmore, reported "emigrated" three weeks prior)
- Anatomist: Unknown, requires identification
- Unusual presence: Dr. A. Fitzroy in private box, upper gallery

RISK ASSESSMENT: Elevated. If identified, cover is compromised. Society has demonstrated willingness to silence investigators permanently.

NOTE TO SELF: The Black Book is here. Somewhere in this building. Find it.

Proceeding with observation.
        """
    },

    "subject": {
        "gaslight": """
Cold.

That is the first thing. The last thing. The only thing that remains when everything else has been taken.

Cold metal beneath your back. Cold air on skin that should be covered. Cold hands — so many hands — arranging you like flowers for a viewing.

*Were there flowers? At your funeral? Did anyone come?*

You cannot remember. The laudanum took the memories first. Then the pain. Then the names and faces of everyone you loved.

Now there is only cold.

And light. Blinding, searing light from above, turning your closed eyelids red-gold like stained glass.

And voices. So many voices. Murmuring. Laughing. Discussing you like you are a curiosity. A specimen. A thing.

You were not always a thing.

You had a name, once. It starts with... it starts with...

*The scratch of metal on metal. A blade being sharpened.*

You cannot scream. Cannot move. Cannot do anything but exist in this frozen moment between life and something worse than death.

The blade descends.
        """,
        "gothic": """
THEY HAVE MADE A CATHEDRAL OF YOUR BODY.

You feel them enter — not physically, not anymore, that mercy was taken hours ago with the final dose — but spiritually. Their gazes are communion wafers dissolving on your exposed flesh. Their whispers are hymns in a language you no longer understand.

*Hail Mary, full of grace—*

No. That prayer belongs to another life. The life where you had a name. Where you wore dresses instead of death. Where men looked at you with desire rather than clinical fascination.

The postcard. You remember the postcard.

A man with soft hands and a softer voice. "Just a photograph, my dear. For a private collection. No one will ever know."

But they knew. They always knew.

The blade is a scripture written in silver.

You are the sermon.

You are the sacrifice.

You are—

*nothing nothing nothing nothing nothing*

—meat.
        """,
        "clinical": """
SENSORY INPUT LOG:
- Temperature: Decreasing. Estimated 4°C at surface contact points.
- Light: Intense. Source positioned approximately 1.2m above. Brightness causing optical nerve response despite closed eyelids.
- Sound: Multiple voices. Counting approximately 47 distinct sources. Primary voice (male, authoritative) originating 0.3m from left ear.
- Touch: Metallic surface. Slight vibration suggesting structural instability or footsteps.
- Smell: Carbolic acid. Formaldehyde. Iron. Sweat.
- Taste: Copper. Blood? Source unclear.

COGNITIVE STATUS:
Fragmentary. Identity recall: FAILED. Recent memory: FAILED. Long-term memory: PARTIAL (flashes of color, a woman's voice singing, the smell of bread).

MOTOR FUNCTION:
None detected. Paralysis complete. Source: Unknown compound administered via [MEMORY CORRUPT].

HYPOTHESIS:
This unit is experiencing dissection while retaining consciousness. Statistical likelihood of survival: 0%.

EMOTIONAL RESPONSE:
[REDACTED]
[REDACTED]
[REDACTED]

FINAL NOTATION:
Mother, I'm sorry. I should never have gone to that studio. I should never have trusted him.

I should never have
        """
    }
}


# =============================================================================
# AMBIENT ATMOSPHERE LINES (Scaled by intensity)
# =============================================================================

AMBIENT_SOUNDS = {
    1: [
        "*The soft hiss of gaslight.*",
        "*Distant footsteps on stone.*",
        "*The rustle of fabric as someone shifts in their seat.*",
        "*A page turning in the gallery.*",
        "*The creak of aged wood.*",
    ],
    2: [
        "*A cough echoes. Then another.*",
        "*Somewhere, a door closes heavily.*",
        "*The scratch of pen on paper — frantic, hurried.*",
        "*A woman's sharp intake of breath.*",
        "*The gaslights flicker. Once. Twice.*",
    ],
    3: [
        "*A wet sound. Organic. Intimate.*",
        "*Someone whispers your name. No — not your name. Close, though.*",
        "*The unmistakable sound of metal parting flesh.*",
        "*A laugh from the upper gallery. Too loud. Too long.*",
        "*The drip of something into the drainage channel.*",
    ],
    4: [
        "*The gaslights dim without explanation.*",
        "*A child crying. But there are no children here. There shouldn't be.*",
        "*Your own heartbeat, deafening, drowning out everything else.*",
        "*The subject's hand twitches. The anatomist doesn't notice. You do.*",
        "*A voice in your ear: 'You're next.' But there's no one beside you.*",
    ],
    5: [
        "*The lights die. In the darkness, something moves.*",
        "*Blood. You can smell it now. Fresh. Wrong.*",
        "*The subject sits up. Looks at you. Opens her mouth and—*",
        "*Your hands. Look at your hands. Why are they red? WHY ARE THEY RED?*",
        "*The anatomist turns. His face is your face. His face is your face. His face is—*",
    ]
}

AMBIENT_OBSERVATIONS = {
    "observer": [
        "A gentleman in the front row is sketching. His hand moves with unsettling precision.",
        "The woman beside you hasn't blinked. Not once. You've been counting.",
        "Three men with red roses have positioned themselves at each exit.",
        "Someone has left a pamphlet on the empty seat beside you. 'THE TRUTH ABOUT THE ANATOMY CLUB.'",
        "The anatomist's assistant keeps glancing at the upper gallery. Waiting for a signal?",
        "A medical student is crying silently. No one else seems to notice.",
        "You recognize the subject's locket. You've seen it before. In a photograph. On a postcard.",
    ],
    "anatomist": [
        "Your hands know the path. They have always known.",
        "The audience is larger tonight. Word has spread. They come for spectacle, not science.",
        "In your peripheral vision, Dr. Fitzroy nods. You have performed adequately.",
        "The subject's face is familiar. You push the thought away. They are all familiar now.",
        "Your assistant whispers: 'The photographer is ready.' For the medical archives, of course.",
        "The blood is darker than expected. She was ill before death. Or poisoned.",
        "You think of Sebastian. What he would say. What he would do. You continue cutting.",
    ],
    "investigator": [
        "The ledger. It must be in the preparation room. If you could just—",
        "That man. Third row. You've seen his face in Blackwood's studio.",
        "The anatomist's technique is precise. Too precise. Edinburgh-trained. Red Rose.",
        "A woman is taking notes. PWS? A potential ally? Or another trap?",
        "The exits are covered. Getting out will be harder than getting in.",
        "You recognize the dress on the subject. Last seen on Mary Holloway. Before she 'emigrated.'",
        "In your notebook: twelve names, six connections, one society. Not enough. Never enough.",
    ],
    "subject": [
        "Floating now. Above the pain. Above the table. Above it all.",
        "Mother's voice: 'Come home, love. Come home.'",
        "The ceiling is beautiful. Has it always been beautiful?",
        "Names. You remember names. But whose? Your own? Theirs?",
        "Cold is leaving now. Everything is leaving now.",
        "The light is warm. The light is—",
        "Someone is crying for you. That's nice. That's very nice.",
    ]
}


# =============================================================================
# ANATOMY DIAGRAM CONTENT
# =============================================================================

ANATOMY_REGIONS = {
    "heart": {
        "medical": "The heart: a hollow muscular organ, approximately the size of a closed fist, positioned slightly left of center in the thoracic cavity. Four chambers — two atria, two ventricles — maintain the circulation of blood throughout the body.",
        "lore": "Dr. Fitzroy's notation (recovered from the Black Book): 'The heart of Subject 23 showed unusual resistance to standard preservation techniques. Recommend investigation into blood type abnormalities. See also: Carlisle, S. — similar presentation.'",
        "emotional": {
            "observer": "You watch the anatomist's blade circle the organ. Around you, students lean forward, hungry for knowledge. Or just hungry.",
            "anatomist": "The heart resists you. They all do, at first. As if the body knows. As if it remembers how to fight.",
            "investigator": "Hearts tell stories. This one speaks of struggle. The bruising pattern suggests she was held down when—",
            "subject": "My heart. My heart. I gave it to him and he— he—"
        }
    },
    "brain": {
        "medical": "The brain: approximately 1.4 kilograms of neural tissue, protected by the skull and three membrane layers (meninges). Seat of consciousness, cognition, and bodily control.",
        "lore": "Fitzroy Protocol, Appendix C: 'Neurological examination of subjects exposed to Protocol compounds reveals accelerated degradation in memory-associated regions. This is considered a feature, not a defect.'",
        "emotional": {
            "observer": "The anatomist handles the brain with something approaching reverence. Or is it hunger?",
            "anatomist": "Grey matter. White matter. The architecture of a soul, reduced to meat and electricity. Beautiful.",
            "investigator": "Memory lives here. If only the dead could testify. If only they could name their killers.",
            "subject": "The memories are going now. Slipping away like water through fingers. What was my name? What was my—"
        }
    },
    "lungs": {
        "medical": "The lungs: paired organs of respiration, occupying the majority of the thoracic cavity. Right lung: three lobes. Left lung: two lobes, smaller to accommodate the heart.",
        "lore": "Anatomy Club Records, Entry 44: 'Subject acquired from St. Mary's Workhouse. Cause of death listed as consumption. Actual cause: suffocation. The distinction matters only to the paperwork.'",
        "emotional": {
            "observer": "Black spots on the tissue. The anatomist notes them for the students. 'London air,' he says. Everyone laughs.",
            "anatomist": "The lungs collapse without the negative pressure of an intact thorax. A useful metaphor, perhaps.",
            "investigator": "These lungs are clean. Too clean for a 'consumptive.' She was young and healthy when she died.",
            "subject": "I can't breathe. I can't— but I don't need to breathe anymore, do I?"
        }
    },
    "hands": {
        "medical": "The hand: a complex structure of 27 bones, 34 muscles, and over 100 ligaments and tendons. Capable of both extraordinary precision and significant force.",
        "lore": "PWS Pamphlet (recovered): 'They examine our hands and declare us suited for labor or beauty, for service or display. But whose hands built the galleries where they dissect us? Whose hands sewed the sheets they lay us upon?'",
        "emotional": {
            "observer": "The subject's hands are callused. A working woman. Someone's daughter. Someone's mother, perhaps.",
            "anatomist": "The hands tell profession. These belonged to a seamstress. The needle pricks are still visible.",
            "investigator": "Defense wounds. Under the fingernails — skin cells? She fought back. They never record that.",
            "subject": "My hands held children. Held lovers. Held hope. Now they hold nothing at all."
        }
    },
    "eyes": {
        "medical": "The eye: a spherical organ approximately 24mm in diameter, capable of detecting light across the visible spectrum. The window through which consciousness perceives the external world.",
        "lore": "Red Rose Society Cipher (decoded): 'The eyes are removed before public demonstration. Protocol requires it. The students must not see what the subjects saw. They must not witness their own reflection in the vitreous.'",
        "emotional": {
            "observer": "The subject's eyes are closed. They're always closed. You wonder what they last looked upon.",
            "anatomist": "The eyes are problematic. They seem to watch, even in death. Best to cover them. For the audience's comfort.",
            "investigator": "Someone closed her eyes. A kindness, or a mercy for themselves? The dead should not stare.",
            "subject": "I saw him. I saw his face. I saw— I saw— why can't I remember what I saw?"
        }
    },
    "blood": {
        "medical": "Blood: the vital fluid comprising plasma, erythrocytes, leukocytes, and thrombocytes. Approximately 5 liters in the adult body, responsible for oxygen transport, immune response, and waste removal.",
        "lore": "From Sebastian Carlisle's confiscated journal: 'They covet my blood. Something in it— some quality they cannot replicate. Fitzroy calls it 'evolutionary potential.' I call it a curse that will not let me die.'",
        "emotional": {
            "observer": "The drainage channels fill slowly. Red becoming rust becoming brown. The color of truth.",
            "anatomist": "Blood type A. Common. Ordinary. Nothing that would interest the Society. Nothing worth preserving.",
            "investigator": "Blood evidence. Impossible to forge. If only the courts would accept anatomical testimony.",
            "subject": "It's leaving me now. Everything I was, flowing into the dark beneath the table."
        }
    }
}


# =============================================================================
# SPECIMEN CABINET
# BUG FIX: Removed 'discovered' field — tracked in session_state now
# =============================================================================

SPECIMENS = {
    "anatomical": [
        {
            "name": "Preserved Heart (Item 23-A)",
            "description": "A human heart suspended in pale yellow fluid. The label is handwritten: 'Female, approx. 25 years. Acquired: October 1887. Unusual coloration noted.'",
            "secret": "Hidden beneath the label, in different handwriting: 'Blood type matches S.C. — DO NOT DISCARD. Priority specimen for Protocol trials.'",
        },
        {
            "name": "Collection of Infant Bones",
            "description": "A wooden box lined with velvet, containing the delicate bones of what must have been a very young child. The arrangement is almost artistic.",
            "secret": "The base of the box contains a false bottom. Beneath it: a receipt from 'Mrs. Mitchell's Baby Farm, Brixton.' The date matches the height of the mortality crisis.",
        },
        {
            "name": "Brain in Spirits",
            "description": "A brain floating in preservation spirits, its wrinkles and folds clearly visible. A tag reads: 'Hysteria patient, Bethlem Hospital.'",
            "secret": "Pencil marks on the jar indicate measurement dates. The brain has been shrinking. The preservation fluid has been tampered with.",
        },
        {
            "name": "Articulated Hand",
            "description": "A human hand, completely stripped of flesh, the bones wired together in perfect anatomical position. The fingertips show evidence of old scarring.",
            "secret": "The ring finger is missing. Removed post-mortem. A wedding band, perhaps? Kept as a trophy?",
        }
    ],
    "documentary": [
        {
            "name": "Black Book Fragment",
            "description": "A torn page of heavy paper, covered in dense handwriting. Names, dates, amounts. Some kind of ledger.",
            "secret": "Legible entries include: 'Fitzroy, A. — initiation complete, see Mentor Protocol' and 'Carlisle, S. — DEFECTED. Recovery priority alpha. Bounty authorized.'",
        },
        {
            "name": "French Postcard (Damaged)",
            "description": "A photograph mounted on card, heavily water-damaged. The image is unclear but appears to show a woman in classical dress.",
            "secret": "Under magnification, the image is clearly a composite. The woman's face has been added to the body — different lighting, different grain. The photographer's mark is visible: 'T.B. Studio, Private Commission.'",
        },
        {
            "name": "PWS Pamphlet",
            "description": "A cheaply printed pamphlet, its pages worn soft with handling. 'THE PROGRESSIVE WOMEN'S SOCIETY DEMANDS JUSTICE.'",
            "secret": "Handwritten in the margin: 'E.W. speaks at the Midnight Salon, Thursday. Bring evidence. Trust no one affiliated with Edinburgh.'",
        },
        {
            "name": "Fitzroy Protocol Notes",
            "description": "Clinical notes on thick paper, detailing dosage schedules for something called 'Protocol Seven.'",
            "secret": "Marginal notation in red ink: 'Subject 12 showing unexpected consciousness during procedure. Increase paralytic. They must not move. They must not scream. They must not be perceived as human.'",
        }
    ],
    "personal": [
        {
            "name": "Tarnished Locket",
            "description": "A small silver locket, blackened with age. It refuses to open.",
            "secret": "When finally forced open, it contains a tiny photograph of a child and a lock of dark hair. On the back, barely legible: 'For my Mary. Until we meet again.'",
        },
        {
            "name": "Child's Shoe",
            "description": "A single small shoe, sized for an infant. Well-made but heavily worn. Found among effects in the specimen room.",
            "secret": "Inside the shoe, a folded paper. A receipt from a Magdalene laundry: 'Child surrendered by mother, Catherine H. Care provided until placement.' No placement record exists.",
        },
        {
            "name": "Romani Amulet",
            "description": "A small brass charm on a broken leather cord. The symbols are unfamiliar to conventional scholarship.",
            "secret": "This is a token of the Underground Network of Healers. Carrying it guarantees aid from any member. Its presence here means one of them was taken. The Network will want to know.",
        },
        {
            "name": "Unsent Letter",
            "description": "A letter in elegant handwriting, folded but never sealed. It begins: 'Dearest Brother—'",
            "secret": "The letter is from Elijah Cartwright to his brother Alistair: 'I know what you have become. I know what the Society asks of you. There is still time, Alistair. There is still time to choose differently. Come to Tuck's Retreat. Let me help you find peace.' It was never sent.",
        }
    ]
}


# =============================================================================
# SECRETS AND HIDDEN CONTENT
# BUG FIX: Removed 'discovered' field — tracked in session_state now
# BUG FIX: Added 'condition' dict for programmatic trigger evaluation
# =============================================================================

SECRETS = [
    {
        "id": "red_rose_signal",
        "trigger": "Observe the gallery three times in Gothic mode",
        "condition": {"pov": "observer", "mode": "gothic", "min_visits": 3},
        "content": "You finally understand the pattern. The men with red roses — they're not just watching. They're signaling. A touch to the brow: acquisition approved. A hand to the heart: payment confirmed. A rose lifted to the lips: target identified. You scan the gallery. Three roses at lips. All pointed toward living women.",
    },
    {
        "id": "black_book_location",
        "trigger": "Investigate while at intensity 4+",
        "condition": {"pov": "investigator", "min_intensity": 4},
        "content": "The Black Book. You've been looking in the wrong place. It's not in the preparation room — it's in plain sight. The anatomist's podium. The hollow space beneath the reading stand. You can see the edge of dark leather from here, if you know where to look.",
    },
    {
        "id": "subject_identity",
        "trigger": "Examine the Subject's hands, then their eyes",
        "condition": {"required_regions": ["hands", "eyes"]},
        "content": "You know her. God help you, you know her. Sarah Whitmore. Evelyn's cousin. The one who was supposed to have emigrated to America three weeks ago. The one whose letters suddenly stopped. The one who posed for a photograph at a society party, not knowing her image would be... manipulated. Sold. Used.",
    },
    {
        "id": "anatomist_doubt",
        "trigger": "Play as Anatomist in Clinical mode",
        "condition": {"pov": "anatomist", "mode": "clinical"},
        "content": "Your hands hesitate. For the first time in 108 procedures, your hands hesitate. This one— she has a birthmark. Left shoulder. Shaped like a crescent moon. Just like... No. Impossible. That was years ago. Edinburgh. A different life. A different you. ...Wasn't it?",
    },
    {
        "id": "escape_route",
        "trigger": "Check all specimen categories",
        "condition": {"all_categories_examined": True},
        "content": "The Romani amulet. The PWS pamphlet. The letter from Elijah. They form a network — a map, almost. The Underground Network of Healers. The Athena Rooms. Tuck's Retreat. These are the places they cannot reach. These are the places survivors run. If you ever need to disappear... now you know how.",
    },
    {
        "id": "fitzroy_fear",
        "trigger": "Examine brain specimen while at intensity 5",
        "condition": {"required_regions": ["brain"], "min_intensity": 5},
        "content": "You find a second label, hidden beneath the first. Different handwriting — shaky, hurried. 'Father's brain. Post-mortem examination reveals advanced deterioration consistent with senile dementia. The affliction is hereditary in 43% of cases.' Signed: A.F. Now you understand Alistair Fitzroy's obsession. He's not chasing immortality. He's running from his own mind.",
    }
]


# =============================================================================
# ENTRY EPIGRAPHS
# =============================================================================

EPIGRAPHS = [
    '"The theatre is full tonight. They have come to see inside the human form -- but it is their own interiors they will glimpse, reflected in the glass of the specimen jars."\n-- Unsigned, found in the margins of the Black Book',

    '"We are all anatomists of a sort. Every glance dissects. Every judgment lays bare."\n-- Dr. Edmund Fitzroy, "On the Philosophy of Medical Practice"',

    '"They tell us the dead feel nothing. They tell us this so we may continue."\n-- Progressive Women\'s Society pamphlet, 1886',

    '"The table does not discriminate. Lord or beggar, virgin or whore -- beneath the blade, we are all merely meat awaiting meaning."\n-- Anatomy Club initiation text',

    '"I have held hearts that still dreamed of beating."\n-- Attributed to Sebastian Carlisle, unconfirmed',

    '"What is a body? A vessel. A vehicle. A temple. A prison. A library of secrets written in blood and bone. We read what we can and burn the rest."\n-- Alistair Fitzroy, private correspondence',
]


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_opening(pov: str, mode: str) -> str:
    """Get the opening narration for a POV and visual mode."""
    return OPENINGS.get(pov, {}).get(mode, OPENINGS["observer"]["gaslight"])


def get_ambient_sound(intensity: int) -> str:
    """Get a random ambient sound based on intensity level."""
    level = min(max(intensity, 1), 5)
    return random.choice(AMBIENT_SOUNDS[level])


def get_ambient_observation(pov: str) -> str:
    """Get a random observation for the current POV."""
    observations = AMBIENT_OBSERVATIONS.get(pov, AMBIENT_OBSERVATIONS["observer"])
    return random.choice(observations)


def get_anatomy_text(region: str, layer: str, pov: str = "observer") -> str:
    """Get text for an anatomy region."""
    region_data = ANATOMY_REGIONS.get(region, ANATOMY_REGIONS["heart"])
    if layer == "emotional":
        return region_data["emotional"].get(pov, region_data["emotional"]["observer"])
    else:
        return region_data.get(layer, region_data["medical"])


def get_random_epigraph() -> str:
    """Get a random entry epigraph."""
    return random.choice(EPIGRAPHS)


def get_specimens_by_category(category: str) -> list:
    """Get all specimens in a category."""
    return SPECIMENS.get(category, [])


def check_secret_condition(secret: dict, pov: str, mode: str, intensity: int,
                           examined_regions: list, examined_specimens: list,
                           visit_count: int) -> bool:
    """
    Programmatically evaluate whether a secret's condition is met.
    Returns True if the secret should be revealed.
    """
    cond = secret.get("condition", {})

    # Check POV requirement
    if "pov" in cond and cond["pov"] != pov:
        return False

    # Check mode requirement
    if "mode" in cond and cond["mode"] != mode:
        return False

    # Check minimum intensity
    if "min_intensity" in cond and intensity < cond["min_intensity"]:
        return False

    # Check minimum visits
    if "min_visits" in cond and visit_count < cond["min_visits"]:
        return False

    # Check required anatomy regions
    if "required_regions" in cond:
        if not all(r in examined_regions for r in cond["required_regions"]):
            return False

    # Check all specimen categories examined
    if cond.get("all_categories_examined"):
        categories = ["anatomical", "documentary", "personal"]
        all_checked = all(
            any(f"{cat}_" in s for s in examined_specimens)
            for cat in categories
        )
        if not all_checked:
            return False

    return True


# =============================================================================
# DISSECTION TABLE ITEMS
# Unified data for the immersive dissection table interface.
# Each item has: id, name, icon, category, position hints,
# medical/lore/emotional text layers, UV reveals, and animation notes.
# =============================================================================

DISSECTION_TABLE_ITEMS = [
    # ─── ORGANS (left side of table) ───
    {
        "id": "heart",
        "name": "Human Heart",
        "icon": "🫀",
        "category": "organ",
        "region_key": "heart",
        "specimen_key": "anatomical_Preserved Heart (Item 23-A)",
        "position": {"x": 180, "y": 220},
        "animation": "double-throb",
        "medical": "The heart: a hollow muscular organ, approximately the size of a closed fist, positioned slightly left of center in the thoracic cavity. Four chambers — two atria, two ventricles — maintain the circulation of blood. Vessels trail from the aortic arch like the roots of an inverted tree. This specimen shows unusual coloration — darker than expected, almost violet near the left ventricle.",
        "lore": "Dr. Fitzroy's notation (recovered from the Black Book): 'The heart of Subject 23 showed unusual resistance to standard preservation techniques. Recommend investigation into blood type abnormalities. See also: Carlisle, S. — similar presentation.' A second annotation in different ink: 'The worthy heart persists. The unworthy dissolves. This is proof.'",
        "emotional": {
            "observer": "You watch the anatomist's blade circle the organ. Around you, students lean forward, hungry for knowledge. Or just hungry. The vessels trailing from the aortic arch look like roots reaching for soil that isn't there.",
            "anatomist": "The heart resists you. They all do, at first. As if the body knows. As if it remembers how to fight. You have held one hundred and seven hearts. This is the first that made your own skip a beat.",
            "investigator": "Hearts tell stories. This one speaks of struggle. The bruising pattern around the left ventricle suggests she was held down when the final dose was administered. Not consumption. Never consumption.",
            "subject": "My heart. My heart. I gave it to him and he— he— it's still beating. Can you hear it? It's still beating. Why won't it stop?"
        },
        "uv_text": "Injection sites visible at the base of the aorta — three puncture marks in a triangular pattern. Consistent with Protocol Seven administration. Faint chemical residue fluoresces blue-green. Handwritten note in margin: 'VIABLE — flag for Carlisle comparison.'"
    },
    {
        "id": "brain",
        "name": "Brain",
        "icon": "🧠",
        "category": "organ",
        "region_key": "brain",
        "specimen_key": "anatomical_Brain in Spirits",
        "position": {"x": 300, "y": 200},
        "animation": "electrical-pulse",
        "medical": "The brain: approximately 1.4 kilograms of neural tissue, protected by the skull and three membrane layers. Sulci and gyri form the characteristic folded landscape. This specimen shows notable asymmetry in the temporal lobes — the left significantly larger than expected. The cerebellum appears intact but discolored.",
        "lore": "Fitzroy Protocol, Appendix C: 'Neurological examination of subjects exposed to Protocol compounds reveals accelerated degradation in memory-associated regions. The hippocampus dissolves first. Then the amygdala. The subject forgets fear before they forget love. This is considered a feature, not a defect.'",
        "emotional": {
            "observer": "The anatomist handles the brain with something approaching reverence. Or is it hunger? His fingers trace the folds like a cartographer mapping unknown territory.",
            "anatomist": "Grey matter. White matter. The architecture of a soul, reduced to meat and electricity. Beautiful. And somewhere in these folds — the memory of a name, a face, a life. Now silent.",
            "investigator": "Memory lives here. If only the dead could testify. If only they could name their killers. The hippocampal degradation is not natural — it matches the Protocol signature exactly.",
            "subject": "The memories are going now. Slipping away like water through fingers. What was my name? What was my— there was a garden. Roses. Someone singing. Gone."
        },
        "uv_text": "Fitzroy's annotations visible along the corpus callosum in fluorescent ink: 'DEGRADATION RATE: 0.3mm/day. MEMORY LOSS: Complete by Day 12. CONSCIOUSNESS: Persists until Day 18. NOTE — Subject reported hearing music that was not present. Auditory hallucinations = promising indicator.'"
    },
    {
        "id": "lungs",
        "name": "Lungs (Pair)",
        "icon": "🫁",
        "category": "organ",
        "region_key": "lungs",
        "specimen_key": None,
        "position": {"x": 180, "y": 310},
        "animation": "inflate-deflate",
        "medical": "The lungs: paired organs of respiration. Right lung: three lobes. Left lung: two lobes, smaller to accommodate the heart. This pair presents a striking contrast — the right lung is pink and healthy, while the left is blackened and shriveled. The cause of blackening is not consistent with consumption or coal dust exposure.",
        "lore": "Anatomy Club Records, Entry 44: 'Subject acquired from St. Mary's Workhouse. Cause of death listed as consumption. Actual cause: suffocation. The distinction matters only to the paperwork. NOTE: Left lung treated with Protocol compound post-mortem. The blackening is chemical, not pathological.'",
        "emotional": {
            "observer": "Black spots on the tissue. The anatomist notes them for the students. 'London air,' he says. Everyone laughs. But you've seen London air damage. This is something else entirely.",
            "anatomist": "The lungs collapse without the negative pressure of an intact thorax. A useful metaphor, perhaps. We all collapse when the pressure changes.",
            "investigator": "These lungs tell two stories. One healthy, one destroyed. The blackened lung was treated with something. A chemical. Post-mortem experimentation. They're using the dead as laboratories.",
            "subject": "I can't breathe. I can't— but I don't need to breathe anymore, do I? The air tastes like copper and something sweet. Laudanum. Always laudanum."
        },
        "uv_text": "Chemical formula visible on the blackened lung surface: C₁₇H₁₉NO₃ + [UNKNOWN COMPOUND]. The unknown compound fluoresces in a pattern resembling crystal growth. Notation: 'Warren Protocol — pulmonary application test #7. Result: TISSUE NECROSIS. Discontinue this vector.'"
    },
    {
        "id": "eye",
        "name": "Eye (Preserved)",
        "icon": "👁️",
        "category": "organ",
        "region_key": "eyes",
        "specimen_key": None,
        "position": {"x": 300, "y": 310},
        "animation": "pupil-dilation",
        "medical": "The eye: a spherical organ approximately 24mm in diameter. This specimen is remarkably well-preserved, the iris still showing a vivid green coloration. The pupil is fixed and dilated — maximally so, suggesting atropine or belladonna exposure at the time of death. Vitreous humor is clouded but intact.",
        "lore": "Red Rose Society Cipher (decoded): 'The eyes are removed before public demonstration. Protocol requires it. The students must not see what the subjects saw. They must not witness their own reflection in the vitreous humour. EXCEPTION: This specimen retained for Fitzroy's private collection. The green is... uncommon.'",
        "emotional": {
            "observer": "The subject's eye stares at nothing. At everything. You have the absurd, terrifying feeling that it can see you. That somewhere behind that clouded lens, something is still watching.",
            "anatomist": "The eyes are problematic. They seem to watch, even in death. Best to cover them. For the audience's comfort. For my comfort. This one is green. Like—",
            "investigator": "Someone preserved this eye separately. Carefully. Lovingly, almost. The dilated pupil means belladonna — the 'beautiful woman' poison. Used to make eyes appear larger. Used in photography studios.",
            "subject": "I saw him. I saw his face. I saw— I saw— why can't I remember what I saw? The light was so bright. The flash of the camera. The flash of the blade."
        },
        "uv_text": "Traces of belladonna compound visible in the iris. The pupil, under UV, reveals a reflected image burned into the retina — too small to discern without magnification, but the shape suggests a human figure holding a camera. Beneath the specimen jar: 'T.B. — PRIVATE. DO NOT CATALOGUE.'"
    },
    {
        "id": "skeletal_hand",
        "name": "Skeletal Hand",
        "icon": "🦴",
        "category": "organ",
        "region_key": "hands",
        "specimen_key": "anatomical_Articulated Hand",
        "position": {"x": 240, "y": 390},
        "animation": "galvanic-twitch",
        "medical": "The hand: 27 bones, 34 muscles, over 100 ligaments and tendons. This specimen is fully articulated, wired in anatomical position. The phalanges show callusing consistent with manual labor — seamstress or laundress work. The ring finger has been removed at the proximal phalanx. Post-mortem, judging by the clean cut.",
        "lore": "PWS Pamphlet (recovered): 'They examine our hands and declare us suited for labor or beauty, for service or display. But whose hands built the galleries where they dissect us? Whose hands sewed the sheets they lay us upon? Whose hands will tear this rotten system down?'",
        "emotional": {
            "observer": "The subject's hands are callused. A working woman. Someone's daughter. Someone's mother, perhaps. The missing finger tells a story no one in this room wants to hear.",
            "anatomist": "The hands tell profession. These belonged to a seamstress. The needle pricks are still visible. Extraordinary dexterity, once. Now mere demonstration material.",
            "investigator": "Defense wounds under the remaining fingernails — skin cells. She fought back. And the missing ring finger — a wedding band removed post-mortem. Kept as a trophy. Or as proof of... acquisition.",
            "subject": "My hands held children. Held lovers. Held hope. Now they hold nothing at all. But they twitch. Did you see? They twitched. The galvanic current makes them dance."
        },
        "uv_text": "Bone cataloguing numbers visible on each phalanx in fluorescent ink: F-23-VII through F-23-XXVII. A complete set. Catalogued before death? The numbering system matches Fitzroy's private collection index. On the missing finger's stump: a tiny engraved rose."
    },

    # ─── INSTRUMENTS (right side of table) ───
    {
        "id": "bone_saw",
        "name": "Bone Saw",
        "icon": "🪚",
        "category": "instrument",
        "region_key": None,
        "specimen_key": None,
        "position": {"x": 600, "y": 220},
        "animation": "steel-glint",
        "medical": "A surgical bone saw, approximately 14 inches in length. The blade shows a fine-toothed pattern designed for clean transverse cuts through compact bone. Well-maintained, recently sharpened. The handle is rosewood with brass fittings — an expensive instrument, likely custom-commissioned.",
        "lore": "This saw bears the maker's mark of Heinrich Müller, Berlin — one of only twelve produced for the Red Rose Society's founding members. Each handle is unique. This one has been used more than any other. The dark flecks in the teeth are not rust.",
        "emotional": {
            "observer": "The saw catches the gaslight and throws it back in fragments. Beautiful and terrible. The anatomist reaches for it with the familiarity of a violinist lifting their bow.",
            "anatomist": "My saw. My instrument. Müller made it to my specifications — the weight, the balance, the tooth pattern. It has never failed me. It has never hesitated.",
            "investigator": "Custom-made. Expensive. The dark material between the teeth — I need a sample. If it's blood, it can be tested. If it matches the missing women—",
            "subject": "The sound. Oh God, the sound. Metal on bone. The vibration travels through the table and into what's left of me. I can feel it. I can still feel it."
        },
        "uv_text": "The blade fluoresces with residue from at least four distinct biological sources. The handle bears an engraved inscription visible only under UV: 'TO THE WORTHY — R.R.S. 1881.' One of the brass fittings conceals a hollow compartment."
    },
    {
        "id": "scalpel",
        "name": "Scalpel (#4, Missing #3)",
        "icon": "🔪",
        "category": "instrument",
        "region_key": None,
        "specimen_key": None,
        "position": {"x": 700, "y": 220},
        "animation": "red-edge-line",
        "medical": "A #4 surgical scalpel with a fixed blade. The instrument tray shows spaces for a matched set of five; the #3 scalpel is conspicuously absent. The remaining blade is honed to extraordinary sharpness — the edge catches light as a thin red line. Recent use evident from faint discoloration near the bolster.",
        "lore": "The missing #3 scalpel has not been seen since the night of Sebastian Carlisle's arrest. It was his preferred instrument — smaller, more precise, suited to the delicate work he favoured over Fitzroy's brute methodology. Some say he took it with him. Others say it was taken from him.",
        "emotional": {
            "observer": "Four scalpels in a case designed for five. The empty slot is more eloquent than any of the instruments beside it. Someone is missing from this set. Someone who isn't coming back.",
            "anatomist": "Carlisle's scalpel. I should have replaced it. Filled the gap. But the empty space serves as a reminder. Every set has its defector. Every order, its Judas.",
            "investigator": "The missing scalpel. Carlisle's instrument. If I can find it, it may still carry evidence. His fingerprints. His victims' blood. Or proof that he was the only one who tried to stop this.",
            "subject": "The blade is so thin. So precise. You almost don't feel it. Almost. A line of fire, then cold. Then nothing."
        },
        "uv_text": "The #4 blade shows a message etched near the tang, visible only under UV: 'S.C. — I KEPT YOUR PLACE.' The empty slot in the case has fingerprint residue — not the anatomist's. Smaller hands. A woman's hands."
    },
    {
        "id": "retractors",
        "name": "Surgical Retractors",
        "icon": "⚙️",
        "category": "instrument",
        "region_key": None,
        "specimen_key": None,
        "position": {"x": 600, "y": 310},
        "animation": "slow-open-close",
        "medical": "A pair of self-retaining retractors, designed to hold open an incision site during extended examination. The ratchet mechanism allows precise adjustment. These are an older model — the modern Balfour design has largely replaced them — suggesting the anatomist prefers tradition over innovation.",
        "lore": "These retractors were used during the Warren Protocol's first human trial. The ratchet mechanism was modified to operate silently — the original clicking sound caused 'undesirable responses in conscious subjects.' The modification order was signed by Dr. Edmund Fitzroy, Alistair's father.",
        "emotional": {
            "observer": "The retractors open and close with mechanical patience. They don't care what they hold apart. Skin, muscle, the truth — all yield to sufficient pressure.",
            "anatomist": "Father's retractors. Modified to his specifications. Silent operation. He understood that the sounds disturb more than the sights. The body can accept what the ears cannot.",
            "investigator": "Modified for silent operation. Why would surgical retractors need to be silent? Unless the subjects could hear them. Unless the subjects were—",
            "subject": "They're opening me. Layer by layer. I am a book and they are reading me and I cannot close my covers."
        },
        "uv_text": "Serial number matches Edmund Fitzroy's personal surgical inventory, item #F-E-034. The ratchet mechanism shows traces of a paralytic compound in its joints — not for the patient. For the instrument itself. Someone tried to jam it. Someone fought back."
    },
    {
        "id": "suture_needle",
        "name": "Suture Needle & Catgut",
        "icon": "🪡",
        "category": "instrument",
        "region_key": None,
        "specimen_key": None,
        "position": {"x": 700, "y": 310},
        "animation": "thread-sway",
        "medical": "A curved suture needle threaded with catgut. The catgut is genuine — processed sheep intestine, not the modern chromic variety. The needle is half-circle pattern, appropriate for deep tissue closure. Oddly, it appears unused despite being threaded and ready.",
        "lore": "Suturing is the anatomist's final act — closing what was opened, restoring the illusion of wholeness. But this needle has never been used in this theatre. It sits ready for a purpose no one speaks of: the subjects that must be returned looking... undisturbed.",
        "emotional": {
            "observer": "The thread sways in the faintest draft. A pendulum measuring time in a place where time has stopped mattering. Ready to close. Ready to seal. Ready to pretend none of this happened.",
            "anatomist": "Thread and needle. The tools of concealment. When we're done, they go back. Stitched. Dressed. Returned. And no one asks why Aunt Mary looks different at the viewing.",
            "investigator": "An unused suture kit at a dissection theatre. This isn't for demonstration — it's for cleanup. They sew them back up. They return the bodies. The families never know what was done.",
            "subject": "Will they sew me back together? Will they make me whole again? Will anyone be able to tell? Will my mother know?"
        },
        "uv_text": "The catgut thread fluoresces differently than standard surgical material — it's been treated with the same compound found in the Black Book's 'concealment protocol.' Bodies sutured with this thread show no visible scarring within 48 hours. The perfect cover."
    },
    {
        "id": "magnifying_lens",
        "name": "Magnifying Lens",
        "icon": "🔍",
        "category": "instrument",
        "region_key": None,
        "specimen_key": None,
        "position": {"x": 650, "y": 390},
        "animation": "light-refraction",
        "medical": "A brass-mounted magnifying lens, 3x magnification, with a handle worn smooth by decades of use. The lens is crystal — not glass — offering superior clarity. A small crack runs through the lower quadrant, creating a prismatic effect.",
        "lore": "This lens belonged to Dr. Edmund Fitzroy before his son inherited it. Under its magnification, the elder Fitzroy first identified the 'crimson thread' — the anomalous blood factor that would become the Society's obsession. The crack appeared the night Edmund died. Alistair has never repaired it.",
        "emotional": {
            "observer": "Through the lens, everything becomes more. More detailed. More real. More terrible. Some truths are better viewed from a distance.",
            "anatomist": "Father's lens. The crack is a feature now, not a flaw. It splits the image — shows you two truths at once. The medical and the personal. The science and the sin.",
            "investigator": "The prismatic crack. When you look through it at the right angle, text that appears solid breaks apart into layers. Hidden messages beneath visible ones. A cipher tool disguised as a medical instrument.",
            "subject": "Don't look at me through that. Don't magnify me. I am already too seen. I am already too exposed. Let me be small again. Let me disappear."
        },
        "uv_text": "The lens frame bears microscopic engraving visible only under UV magnification: a complete list of 23 names. The first is 'Edmund Fitzroy.' The last is 'Alistair Fitzroy.' Between them — the 21 founding members of the Red Rose Society. Three names have been crossed out. One is Sebastian Carlisle."
    },

    # ─── ATMOSPHERIC DETAILS (scattered around table) ───
    {
        "id": "pocket_watch",
        "name": "Pocket Watch",
        "icon": "⌚",
        "category": "detail",
        "region_key": None,
        "specimen_key": "personal_Tarnished Locket",
        "position": {"x": 450, "y": 480},
        "animation": "ticking",
        "medical": "A gentleman's pocket watch, silver case, hunter style. The mechanism is visible through a glass back. Currently running, though the time displayed does not correspond to any reasonable hour. The winding crown shows heavy wear suggesting obsessive adjustment.",
        "lore": "The watch runs backwards in the gothic light. Not a malfunction — a modification. The watchmaker who altered it was found in the Thames three days later. The watch was commissioned by someone who wanted to measure how long the Protocol takes. Counting down, not up.",
        "emotional": {
            "observer": "Tick. Tick. Tick. The watch measures something, but not time. Not any time you recognize. The hands move in the wrong direction and somehow that feels more honest.",
            "anatomist": "My father's watch. It has never kept correct time. I've come to prefer it that way. Correct time is for people who believe in progress. I believe in cycles.",
            "investigator": "The watch runs backwards. A timer, counting down to something. The inscription inside the case will tell me whose it is. If I can get close enough—",
            "subject": "Time. Is there still time? The ticking sounds like a heartbeat. Like my heartbeat. Slowing. Slowing. Slow—"
        },
        "uv_text": "Inside the case lid, an inscription fluoresces: 'FOR A.F. — MEASURE TWICE, CUT ONCE. — E.F.' Edmund to Alistair. The glass back reveals the mechanism has been modified with a secondary gear train. It's counting something specific: the watch resets every 18 days. The length of the Protocol."
    },
    {
        "id": "handwritten_note",
        "name": "Handwritten Note (Bleeding Ink)",
        "icon": "📝",
        "category": "detail",
        "region_key": None,
        "specimen_key": "documentary_Black Book Fragment",
        "position": {"x": 350, "y": 120},
        "animation": "ink-bleed",
        "medical": "A fragment of heavy writing paper, partially obscured by spreading ink. The handwriting is educated but hurried — a physician's hand under stress. Some words are legible; others have been consumed by the bleeding ink. The paper stock matches that used in the Black Book.",
        "lore": "Legible fragments: '...cannot continue this... the Warren Protocol must be... Carlisle was right about the... God forgive me, I have seen what... the women deserve...' The ink bleeds outward as if trying to escape the words it carries. The note was found tucked beneath the dissection table's drainage tray.",
        "emotional": {
            "observer": "The ink is still spreading. Still running. As if the words themselves are trying to flee the page. You catch fragments — 'cannot continue' — 'Carlisle was right' — 'God forgive me.'",
            "anatomist": "I wrote this. Last night. Or last week. The dates blur. The ink runs because my hand was shaking. It hasn't stopped shaking since I saw what the Protocol does at day sixteen.",
            "investigator": "Evidence. Written in the anatomist's own hand. Partial confession. If I can preserve this before the ink destroys the remaining words—",
            "subject": "Someone wrote about me. About what happened. The ink bleeds like I bled. The words dissolve like I dissolved. At least someone tried to say something."
        },
        "uv_text": "Beneath the bleeding ink, the UV reveals the original complete text — the ink was deliberately smeared to obscure it. The full note reads: 'The Warren Protocol must be stopped. Subject 23 remained conscious throughout. She spoke my name. She knew me. I cannot continue this. Carlisle was right about the crimson thread — it is not a gift. It is a curse. God forgive me, I have seen what we have become. The women deserve justice. —A.F.'"
    },
    {
        "id": "candle",
        "name": "Tallow Candle",
        "icon": "🕯️",
        "category": "detail",
        "region_key": None,
        "specimen_key": None,
        "position": {"x": 100, "y": 100},
        "animation": "flame-flicker",
        "medical": "A tallow candle, approximately 40% consumed, set in a brass holder. The flame burns with unusual steadiness given the theatre's draughts. Wax has pooled and solidified in layered formations down the brass stem. The tallow composition is non-standard — the rendering smells wrong.",
        "lore": "The candles in this theatre are rendered from a specific tallow blend maintained by the Society since 1847. The fat source has never been officially documented. The flame burns longer and steadier than standard tallow. The Society considers their candles a point of pride. No one asks about the rendering process.",
        "emotional": {
            "observer": "The flame won't die. Despite the cold, despite the draught from the gallery, it burns on. The light cone it casts makes everything within its reach look like a painting. Everything outside — shadow.",
            "anatomist": "The candles are always lit when I arrive. I've never seen who lights them. I've stopped asking. Some traditions in this place predate questions.",
            "investigator": "The tallow smells wrong. Too sweet. Standard candles are rendered from beef or mutton fat. This is something else. I don't want to think about what it might be. I have to think about what it might be.",
            "subject": "The flame is warm. The only warm thing left. It dances like it's alive. Like it's the only living thing in this room. Except— except I'm still—"
        },
        "uv_text": "The wax pooling on the brass holder has trapped several strands of hair — invisible to the naked eye but fluorescing under UV. Human hair. Multiple sources. The brass holder itself bears an engraving: a rose, and beneath it, the number 23."
    },
    {
        "id": "blood_spots",
        "name": "Blood Spots (Oxidizing)",
        "icon": "🩸",
        "category": "detail",
        "region_key": None,
        "specimen_key": None,
        "position": {"x": 450, "y": 300},
        "animation": "oxidation-darken",
        "medical": "Several drops of blood on the marble surface, in various stages of oxidation. The freshest are bright crimson; the oldest have darkened to near-black. The distribution pattern suggests multiple procedures over time — the marble is porous and has absorbed generations of evidence.",
        "lore": "The marble of this table has never been replaced, despite numerous requests. The Society considers the accumulated blood a form of consecration. 'Each drop is a lesson learned,' reads the Anatomy Club charter. 'Each stain, a truth revealed.' The oldest stains date to the table's installation in 1843.",
        "emotional": {
            "observer": "The blood spots form a constellation on the marble. You could chart them like stars. Name them. Each one is a person. Each one was someone.",
            "anatomist": "I used to scrub the table between sessions. Now I don't. The stains have become a map of my career. My history, written in other people's blood.",
            "investigator": "Blood evidence. Layered in the marble like geological strata. If forensic science advances far enough, every drop could identify a victim. Every stain could name a name.",
            "subject": "My blood joins the others. Mixing. Merging. I am part of this table now. Part of its history. One more stain among hundreds. One more name that will be forgotten."
        },
        "uv_text": "Under UV, the blood spots reveal a hidden pattern — they've been deliberately arranged around a central point to form the shape of a five-petalled rose. Not random spillage. A ritual. The central spot, the oldest and darkest, fluoresces differently from the others. It's not human blood."
    },
    {
        "id": "red_rose",
        "name": "Red Rose (Wilting)",
        "icon": "🌹",
        "category": "detail",
        "region_key": None,
        "specimen_key": "personal_Romani Amulet",
        "position": {"x": 750, "y": 480},
        "animation": "petal-wilt",
        "medical": "A single red rose, variety Rosa gallica, placed at the corner of the dissection table. The petals are in mid-wilt — edges curling brown, but the center still holds its crimson depth. Three petals have fallen to the marble surface. The thorns have been removed with surgical precision.",
        "lore": "A rose is placed on the table before every session. No one admits to placing it. The tradition predates the current anatomist, the previous one, and possibly the theatre itself. The rose is always Red — never white, never pink. It is always wilting. It is never fresh. As if it was cut days before anyone knew a demonstration would occur.",
        "emotional": {
            "observer": "Three petals fallen. Three women missing this month. Coincidence is a word for people who haven't been paying attention. The rose watches you as much as you watch it.",
            "anatomist": "I find it every time. Already wilting. Already dying. Like everything in this room. I've stopped removing it. It belongs here more than I do.",
            "investigator": "The Crimson Rose. The Society's mark. Left in plain sight like a signature on a crime scene. They're not hiding anymore. They're boasting. Daring someone to connect the thorns.",
            "subject": "A rose for me? How kind. How terribly, terribly kind. It's dying too. We match. We are the same. Fading crimson on cold marble."
        },
        "uv_text": "The rose petals fluoresce a deep, impossible crimson under UV — far brighter than any natural pigment. The fallen petals, arranged on the marble, spell three letters: R. R. S. The stem, stripped of thorns, bears microscopic text: 'THE WARREN PROTOCOL CONTINUES.'"
    },
]


def get_dissection_table_items(category: str = None) -> list:
    """Get dissection table items, optionally filtered by category."""
    if category:
        return [i for i in DISSECTION_TABLE_ITEMS if i["category"] == category]
    return DISSECTION_TABLE_ITEMS
