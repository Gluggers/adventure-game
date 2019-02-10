import logging

### SKILLS CONSTANTS ###
SKILL_ID_ATTACK = 0x1
SKILL_ID_STRENGTH = 0x2
SKILL_ID_DEFENSE = 0x3
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

SKILL_ID_LIST = [
    SKILL_ID_ATTACK,
    SKILL_ID_STRENGTH,
    SKILL_ID_DEFENSE,
    SKILL_ID_HITPOINTS,
    SKILL_ID_ARCHERY,
    SKILL_ID_WHITE_MAGIC,
    SKILL_ID_BLACK_MAGIC,
    SKILL_ID_SMITHING,
    SKILL_ID_HERBLORE,
    SKILL_ID_CRAFTING,
    SKILL_ID_COOKING,
    SKILL_ID_FIREMAKING,
    SKILL_ID_CONSTRUCTION,
    SKILL_ID_INTELLIGENCE,
    SKILL_ID_CHARISMA,
    SKILL_ID_AGILITY,
    SKILL_ID_MINING,
    SKILL_ID_FARMING,
    SKILL_ID_FISHING,
    SKILL_ID_WOODCUTTING,
    SKILL_ID_HUSBANDRY
]

### LEVEL AND EXPERIENCE CONSTANTS ###
DEFAULT_HITPOINTS = 10
DEFAULT_LEVEL = 1
DEFAULT_EXP = 0
MIN_LEVEL = 1
MIN_EXP = 0
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

MAX_LEVEL = len(EXP_LADDER)
MAX_EXP = 1000000

def get_level_from_experience(experience):
    ret_level = DEFAULT_LEVEL
    for i in range(MAX_LEVEL):
        if EXP_LADDER[i] <= experience:
            ret_level = i + 1
        else:
            break

def get_experience_from_level(level):
    ret_exp = DEFAULT_EXP
    if level and level <= len(EXP_LADDER):
        ret_exp = EXP_LADDER[len(EXP_LADDER) - level]

    logger.debug("Exp for level {0} is {1}".format(level, ret_exp))
    return ret_exp

def calculate_combat_level(skill_dict):
    ret_level = 1

    if skill_dict:
        ret_level = int((                                         \
            skill_dict.get(SKILL_ID_ATTACK, [1])[0]              \
            + skill_dict.get(SKILL_ID_STRENGTH, [1])[0]          \
            + skill_dict.get(SKILL_ID_DEFENSE, [1])[0]           \
            + skill_dict.get(SKILL_ID_HITPOINTS, [1])[0]         \
            + max(                                               \
                skill_dict.get(SKILL_ID_ARCHERY, [1])[0],        \
                skill_dict.get(SKILL_ID_BLACK_MAGIC, [1])[0],    \
                skill_dict.get(SKILL_ID_WHITE_MAGIC, [1])[0],    \
            )
        )  / 3)
        logger.debug("Combat level: {0}".format(ret_level))

    return ret_level

# set up logger
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
