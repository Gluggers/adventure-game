# -*- coding: utf-8 -*-
"""This module contains classes and methods for magic and spells.

NORMAL SPELLBOOK
    APPRENTICE LEVEL SPELL
    1   water pulse - BM
    4   earth pulse - BM
    7   air pulse - BM
    10  fire pulse - BM

    LOW LEVEL SPELL
    18  water burst - BM
    22  earth burst - BM
    26  air burst - BM
    30  fire burst - BM

    MEDIUM LEVEL SPELL
    40  water beam - BM
    45  earth beam - BM
    50  air beam - BM
    55  fire beam - BM

    HIGH LEVEL SPELL
    67  water surge - BM
    73  earth surge - BM
    79  air surge - BM
    85  fire surge - BM

    MASTER SPELLS
    97  tsunami - BM
    98  earthquake - BM
    99  tornado - BM
    100 eruption - BM

FORBIDDEN SPELLBOOK


ARCANE SPELLBOOK


GAIA SPELLBOOK


DIVINE SPELLBOOK
"""

import imageids
import imagepaths
import battledata
import language
import viewingicondata
import menuoptions

### SPELL CLASSES ###
BLACK_MAGIC_CLASS = 0x1 # For spells that inflict damage, curses, etc.
WHITE_MAGIC_CLASS = 0x2 # For non-damage and non-curse spells.

### SPELL BOOKS ###
SPELL_BOOK_NORMAL = 0x1

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
SPELL_CLASS_FIELD = 0x302
SPELL_TYPES_FIELD = 0x303 # Set of spell type IDs.
SPELL_REQUIRED_LEVEL_FIELD = 0x311
SPELL_REQUIRED_MANA_FIELD = 0x312
SPELL_DAMAGE_TYPES_FIELD = 0x313 # Set of damage type IDs.
SPELL_BASE_POWER_FIELD = 0x314
SPELL_REQUIRED_QUESTS_FIELD = 0x315 # List of quest IDs required to cast spell.
# Mapping of equipment slot IDs to item IDs required to cast the spell.
SPELL_REQUIRED_EQUIPPED_ITEMS_FIELD = 0x316

### SPELL ID NUMBERS ###
SPELL_WATER_PULSE_ID = 0x1
SPELL_EARTH_PULSE_ID = 0x2
SPELL_AIR_PULSE_ID = 0x3
SPELL_FIRE_PULSE_ID = 0x4

### SPELL BOOK INFO
SPELL_BOOK_INFO = {
    SPELL_BOOK_NORMAL: {
        SPELL_WATER_PULSE_ID,
        SPELL_EARTH_PULSE_ID,
        SPELL_AIR_PULSE_ID,
        SPELL_FIRE_PULSE_ID,
    }
}

# SPELL OBJECT DATA
SPELL_OBJECT_DATA = {
    SPELL_WATER_PULSE_ID: {
        viewingicondata.NAME_INFO_FIELD: {
            language.LANG_ENGLISH: "Water Pulse",
            language.LANG_ESPANOL: "Impulso de Agua",
        },
        viewingicondata.DESCRIPTION_INFO_FIELD: {
            language.LANG_ENGLISH: "An apprentice-level water spell.",
            language.LANG_ESPANOL: "En hechizo de agua para los principiantes.",
        },
        viewingicondata.OPTION_ID_LIST_FIELD: [menuoptions.CAST_SPELL_OPTION_ID],
        viewingicondata.IMAGE_PATH_DICT_FIELD: {
            imageids.ICON_IMAGE_ID: None, # TODO
        },
        SPELL_CLASS_FIELD: BLACK_MAGIC_CLASS,
        SPELL_TYPES_FIELD: {SPELL_TYPE_WATER},
        SPELL_REQUIRED_LEVEL_FIELD: 1,
        SPELL_REQUIRED_MANA_FIELD: 1,
        SPELL_DAMAGE_TYPES_FIELD: {
            battledata.DAMAGE_TYPE_MAGIC_WATER,
        },
        SPELL_BASE_POWER_FIELD: 5, # TODO change.
        SPELL_REQUIRED_QUESTS_FIELD: None,
        SPELL_REQUIRED_EQUIPPED_ITEMS_FIELD: None,
    },
}
