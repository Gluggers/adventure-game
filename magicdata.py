import imagepaths
import battledata

### SPELL CLASSES ###
BLACK_MAGIC_CLASS = 0x1 # For spells that inflict damage, curses, etc.
WHITE_MAGIC_CLASS = 0x2 # For non-damage and non-curse spells.

### SPELL BOOKS ###
SPELL_BOOK_NORMAL = 0x1
SPELL_BOOK

### SPELL TYPES ###
SPELL_TYPE_AIR = 0x300
SPELL_TYPE_WATER = 0x301
SPELL_TYPE_EARTH = 0x302
SPELL_TYPE_FIRE = 0x303
SPELL_TYPE_ICE = 0x310
SPELL_TYPE_ELECTRIC = 0x311
SPELL_TYPE_NATURE = 0x312
SPELL_TYPE_HOLY = 0x313
SPELL_TYPE_DARK = 0x314
SPELL_TYPE_TELEPORT = 0x320

### SPELL FIELDS ###
SPELL_BOOK_FIELD = 0x1
SPELL_CLASS_FIELD = 0x2
SPELL_TYPES_FIELD = 0x3 # Set of spell type IDs.
SPELL_NAME_INFO_FIELD = 0x10
SPELL_REQUIRED_LEVEL_FIELD = 0x11
SPELL_REQUIRED_MANA_FIELD = 0x12
SPELL_DAMAGE_TYPES_FIELD = 0x13 # Set of damage type IDs.
SPELL_BASE_DAMAGE_FIELD = 0x14
SPELL_ICON_PATH_FIELD = 0x15
SPELL_DESCRIPTION_PATH_FIELD = 0x16
SPELL_REQUIRED_QUESTS_FIELD = 0x17 # List of quest IDs required to cast spell.

### SPELL ID NUMBERS ###
SPELL_WATER_PULSE_ID = 0x1
SPELL_EARTH_PULSE_ID = 0x2

"""
NORMAL SPELLBOOK
    APPRENTICE LEVEL SPELL
    1   water pulse
    4   earth pulse
    7   air pulse
    10  fire pulse

    LOW LEVEL SPELL
    18  water burst
    22  earth burst
    26  air burst
    30  fire burst

    MEDIUM LEVEL SPELL
    40  water beam
    45  earth beam
    50  air beam
    55  fire beam

    HIGH LEVEL SPELL
    67  water surge
    73  earth surge
    79  air surge
    85  fire surge

    MASTER SPELLS
    97  tsunami
    98  earthquake
    99  tornado
    100 eruption

FORBIDDEN SPELLBOOK



ARCANE SPELLBOOK


GAIA SPELLBOOK


DIVINE SPELLBOOK
"""