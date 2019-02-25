import logging
import language

### SKILLS CONSTANTS ###
#SKILL_ID_ATTACK = 0x1
#SKILL_ID_STRENGTH = 0x2
#SKILL_ID_DEFENSE = 0x3
SKILL_ID_MELEE = 0x3
SKILL_ID_HITPOINTS = 0x4
SKILL_ID_ARCHERY = 0x5
SKILL_ID_WHITE_MAGIC = 0x6
SKILL_ID_BLACK_MAGIC = 0x7
SKILL_ID_SMITHING = 0x8
SKILL_ID_HERBLORE = 0x9
SKILL_ID_CRAFTING = 0xa
SKILL_ID_COOKING = 0xb
SKILL_ID_FIREMAKING = 0xc
SKILL_ID_CONSTRUCTION = 0xd
SKILL_ID_INTELLIGENCE = 0xe
SKILL_ID_CHARISMA = 0xf
SKILL_ID_AGILITY = 0x10
SKILL_ID_MINING = 0x11
SKILL_ID_FARMING = 0x12
SKILL_ID_FISHING = 0x13
SKILL_ID_WOODCUTTING = 0x14
SKILL_ID_HUSBANDRY = 0x15

# Maps skill IDs to their names in the various languages.
SKILL_ID_NAME_MAPPING = {
    #SKILL_ID_ATTACK: {
        #language.LANG_ENGLISH: "ATTACK",
        #language.LANG_ESPANOL: "ATAQUE",
    #},
    #SKILL_ID_STRENGTH: {
         # language.LANG_ENGLISH: "STRENGTH",
          #language.LANG_ESPANOL: "FUERZA",
    #},
    #SKILL_ID_DEFENSE: {
          #language.LANG_ENGLISH: "DEFENSE",
          #language.LANG_ESPANOL: "DEFENSA",
#    },
    SKILL_ID_MELEE: {
        language.LANG_ENGLISH: "MELEE",
        language.LANG_ESPANOL: "MELEE",
    },
    SKILL_ID_HITPOINTS: {
          language.LANG_ENGLISH: "HITPOINTS",
          language.LANG_ESPANOL: "SALUD",
    },
    SKILL_ID_ARCHERY: {
          language.LANG_ENGLISH: "ARCHERY",
          language.LANG_ESPANOL: "ARQUERIA",
    },
    SKILL_ID_WHITE_MAGIC: {
          language.LANG_ENGLISH: "WHITE MAGIC",
          language.LANG_ESPANOL: "MAGIA BLANCA",
    },
    SKILL_ID_BLACK_MAGIC: {
          language.LANG_ENGLISH: "BLACK MAGIC",
          language.LANG_ESPANOL: "MAGIA NEGRA",
    },
    SKILL_ID_SMITHING: {
          language.LANG_ENGLISH: "SMITHING",
          language.LANG_ESPANOL: "HERRERO",
    },
    SKILL_ID_HERBLORE: {
          language.LANG_ENGLISH: "HERBLORE",
          language.LANG_ESPANOL: "HERBOLARIA",
    },
    SKILL_ID_CRAFTING: {
          language.LANG_ENGLISH: "CRAFTING",
          language.LANG_ESPANOL: "ARTESANIA",
    },
    SKILL_ID_COOKING: {
          language.LANG_ENGLISH: "COOKING",
          language.LANG_ESPANOL: "COCINA",
    },
    SKILL_ID_FIREMAKING: {
          language.LANG_ENGLISH: "FIREMAKING",
          language.LANG_ESPANOL: "DOMINIO DEL FUEGO",
    },
    SKILL_ID_CONSTRUCTION: {
          language.LANG_ENGLISH: "CONSTRUCTION",
          language.LANG_ESPANOL: "CONSTRUCCION",
    },
    SKILL_ID_INTELLIGENCE: {
          language.LANG_ENGLISH: "INTELLIGENCE",
          language.LANG_ESPANOL: "INTELIGENCIA",
    },
    SKILL_ID_CHARISMA: {
          language.LANG_ENGLISH: "CHARISMA",
          language.LANG_ESPANOL: "CARISMA",
    },
    SKILL_ID_AGILITY: {
          language.LANG_ENGLISH: "AGILITY",
          language.LANG_ESPANOL: "AGILIDAD",
    },
    SKILL_ID_MINING: {
          language.LANG_ENGLISH: "MINING",
          language.LANG_ESPANOL: "MINERIA",
    },
    SKILL_ID_FARMING: {
          language.LANG_ENGLISH: "FARMING",
          language.LANG_ESPANOL: "AGRICULTURA",
    },
    SKILL_ID_FISHING: {
          language.LANG_ENGLISH: "FISHING",
          language.LANG_ESPANOL: "PESCA",
    },
    SKILL_ID_WOODCUTTING: {
          language.LANG_ENGLISH: "WOODCUTTING",
          language.LANG_ESPANOL: "TALA DE ARBOLES",
    },
    SKILL_ID_HUSBANDRY: {
          language.LANG_ENGLISH: "HUSBANDRY",
          language.LANG_ESPANOL: "CRIA DE ANIMALES",
    },
}

SKILL_ID_LIST = sorted(list(SKILL_ID_NAME_MAPPING.keys()))

### LEVEL UP INFO ###
LEVEL_UP_MESSAGE_INFO = {
     language.LANG_ENGLISH: "You gained {0} level(s) in {1}! You are now level {2} in {1}.",
     language.LANG_ESPANOL: "Has logrado {0} nivel(es) en {1}! Ya tienes un nivel de {2} en {1}.",
}

### LEVEL AND EXPERIENCE CONSTANTS ###
DEFAULT_LEVEL_HITPOINTS = 10
DEFAULT_LEVEL = 1
DEFAULT_EXP = 0
MIN_LEVEL = 1
MIN_EXP = 0
### EXP FORMULA: Level 1 = 0
### Level N for N = 2 to 100:
###  sum from x = 1 to N-1 of floor(100*2^(x/11) + 32x + 49.425)
EXP_LADDER = [
    3000,
    2500,
    2000,
    1500,
    1100,
    800, # level 5
    500, # level 4
    300, # level 3
    100, # level 2
    0 # level 1
]

LEVEL_EXP_MAPPING = {
    1: 0,
    2: 187,
    3: 413,
    4: 679,
    5: 985,
    6: 1331,
    7: 1718,
    8: 2146,
    9: 2616,
    10: 3129,
    11: 3686,
    12: 4287,
    13: 4933,
    14: 5625,
    15: 6364,
    16: 7150,
    17: 7985,
    18: 8870,
    19: 9806,
    20: 10794,
    21: 11836,
    22: 12932,
    23: 14085,
    24: 15296,
    25: 16567,
    26: 17899,
    27: 19295,
    28: 20756,
    29: 22285,
    30: 23884,
    31: 25555,
    32: 27301,
    33: 29125,
    34: 31030,
    35: 33019,
    36: 35095,
    37: 37262,
    38: 39524,
    39: 41885,
    40: 44350,
    41: 46922,
    42: 49607,
    43: 52410,
    44: 55337,
    45: 58394,
    46: 61587,
    47: 64923,
    48: 68409,
    49: 72053,
    50: 75862,
    51: 79846,
    52: 84014,
    53: 88376,
    54: 92942,
    55: 97724,
    56: 102733,
    57: 107982,
    58: 113485,
    59: 119256,
    60: 125310,
    61: 131664,
    62: 138335,
    63: 145342,
    64: 152705,
    65: 160444,
    66: 168582,
    67: 177143,
    68: 186152,
    69: 195637,
    70: 205626,
    71: 216150,
    72: 227241,
    73: 238935,
    74: 251268,
    75: 264280,
    76: 278013,
    77: 292512,
    78: 307825,
    79: 324002,
    80: 341098,
    81: 359170,
    82: 378280,
    83: 398493,
    84: 419879,
    85: 442512,
    86: 466471,
    87: 491841,
    88: 518711,
    89: 547176,
    90: 577338,
    91: 609305,
    92: 643193,
    93: 679125,
    94: 717231,
    95: 757651,
    96: 800533,
    97: 846035,
    98: 894325,
    99: 945583,
    100: 1000000,
}

MAX_LEVEL = len(LEVEL_EXP_MAPPING)
DEFAULT_MAX_XP = 1000000
MAX_EXP = LEVEL_EXP_MAPPING.get(MAX_LEVEL, DEFAULT_MAX_XP)

def get_level_from_experience_test(experience):
    ret_level = MIN_LEVEL
    for i in range(MAX_LEVEL):
        if EXP_LADDER[i] <= experience:
            ret_level = i + 1
        else:
            break

    return ret_level

# Returns the lowest level that the given experience will satisfy.
def get_level_from_experience(experience):
    ret_level = MIN_LEVEL
    for i in range(MAX_LEVEL):
        if LEVEL_EXP_MAPPING.get(i + 1, DEFAULT_MAX_XP) <= experience:
            ret_level = i + 1
        else:
            break

    return ret_level

def get_experience_from_level_test(level):
    ret_exp = MIN_EXP
    if level and level <= len(EXP_LADDER):
        ret_exp = EXP_LADDER[len(EXP_LADDER) - level]

    logger.debug("Exp for level {0} is {1}".format(level, ret_exp))
    return ret_exp

def get_experience_from_level(level):
    ret_exp = MIN_EXP
    if level and (level >= MIN_LEVEL) and (level <= MAX_LEVEL):
        ret_exp = LEVEL_EXP_MAPPING.get(level, DEFAULT_MAX_XP)

    logger.debug("Exp for level {0} is {1}".format(level, ret_exp))
    return ret_exp

# Assumes exp is a valid experience value for the level.
def get_experience_to_next_level(level, curr_exp):
    ret_exp = 0

    if (curr_exp is not None) \
            and curr_exp >= MIN_EXP \
            and level \
            and (level < MAX_LEVEL) \
            and (level >= MIN_LEVEL):
        next_level = level + 1
        next_level_exp = get_experience_from_level(next_level)

        if next_level_exp:
            ret_exp = max(0, next_level_exp - curr_exp)

    return ret_exp

"""
def calculate_combat_level_test(skill_info_dict):
    ret_level = 1

    if skill_info_dict:
        ret_level = int((                                           \
            skill_info_dict.get(SKILL_ID_ATTACK, [1])[0]            \
            + skill_info_dict.get(SKILL_ID_STRENGTH, [1])[0]        \
            + skill_info_dict.get(SKILL_ID_DEFENSE, [1])[0]         \
            + skill_info_dict.get(SKILL_ID_HITPOINTS, [1])[0]       \
            + max(                                                  \
                skill_info_dict.get(SKILL_ID_ARCHERY, [1])[0],      \
                skill_info_dict.get(SKILL_ID_BLACK_MAGIC, [1])[0],  \
                skill_info_dict.get(SKILL_ID_WHITE_MAGIC, [1])[0],  \
            )
        ) / 3)
        logger.debug("Combat level: {0}".format(ret_level))

    return ret_level
"""

def calculate_combat_level(skill_info_dict):
    ret_level = 1

    if skill_info_dict:
        ret_level = int((                                           \
            skill_info_dict.get(SKILL_ID_MELEE, [1])[0]             \
            + skill_info_dict.get(SKILL_ID_HITPOINTS, [1])[0]       \
            + skill_info_dict.get(SKILL_ID_ARCHERY, [1])[0]         \
            + max(                                                  \
                skill_info_dict.get(SKILL_ID_BLACK_MAGIC, [1])[0],  \
                skill_info_dict.get(SKILL_ID_WHITE_MAGIC, [1])[0],  \
            )
        ) / 3)
        logger.debug("Combat level: {0}".format(ret_level))

    return ret_level

def get_skill_name(skill_id, language_id):
    ret_name = ""

    if (skill_id is not None) and (language_id is not None):
        ret_name = SKILL_ID_NAME_MAPPING.get(
                skill_id,
                {}
            ).get(language_id, "")

    return ret_name

# set up logger
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
