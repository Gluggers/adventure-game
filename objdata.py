import imagepaths
import skills
import language
import interactiondata
import imageids

### INTERACTIVE OBJECT TYPE ID CONSTANTS ###
TYPE_CHARACTER = 0x1
TYPE_MONSTER = 0x2
TYPE_RESOURCE = 0x3
TYPE_ITEM = 0x4
TYPE_OBSTACLE = 0x5
TYPE_CHEST = 0x6
TYPE_MISC = 0x7

### INTERACTIVE OBJECT ID NUMBERS ###
# SPECIAL IDS ARE 0X1 TO 0XFFFFF
MIN_SPECIAL_ID = 0x000001
MAX_SPECIAL_ID = 0x0FFFFF
PROTAGONIST_ID = 0x000002

# CHARACTER IDS ARE 0X100000 TO 0X1FFFFF
MIN_CHARACTER_ID = 0x100000
MAX_CHARACTER_ID = 0x1FFFFF

# MONSTER IDS ARE 0X200000 TO 0X2FFFFF
MIN_MONSTER_ID = 0x200000
MAX_MONSTER_ID = 0x2FFFFF

# RESOURCE IDS ARE 0X300000 TO 0X3FFFFF
MIN_RESOURCE_ID = 0x300000
MAX_RESOURCE_ID = 0x3FFFFF
HERB_BASIC_ID = 0x300001
TREE_BASIC_ID = 0x300003
TREE_OAK_ID = 0x300004

# ITEM IDS ARE 0X400000 TO 0X4FFFFF
MIN_ITEM_ID = 0x400000
MAX_ITEM_ID = 0x4FFFFF

# OBSTACLE IDS ARE 0X500000 TO 0X5FFFFF
MIN_OBSTACLE_ID = 0x500000
MAX_OBSTACLE_ID = 0x5FFFFF

# CHEST IDS ARE 0X600000 TO 0X6FFFFF
MIN_CHEST_ID = 0x600000
MAX_CHEST_ID = 0x6FFFFF

# MISCELLANEOUS IDS ARE 0x700000 TO 0x7FFFFF
MIN_MISC_ID = 0x700000
ORE_EMPTY_ID = 0x700001
TREE_STUMP_ID = 0x700002
MAX_MISC_ID = 0x7FFFFF

### OBJECT DATA FIELDS ###
OBJECT_NAME_INFO_FIELD = 0x1
IMAGE_PATH_DICT_FIELD = 0x2
COLLISION_WIDTH_FIELD = 0x3
COLLISION_HEIGHT_FIELD = 0x4
EXAMINE_INFO_FIELD = 0x5
INTERACTION_ID_FIELD = 0x6
REPLACEMENT_OBJECT_ID_FIELD = 0x7
RESPAWN_TIME_S_FIELD = 0x8

### RESOURCE DATA FIELDS ###
RELATED_SKILL_ID_FIELD = 0x301
REQUIRED_LEVEL_FIELD = 0x302
GAINED_XP_FIELD = 0x303
RESOURCE_ITEM_FIELD = 0x304
EXHAUSTION_PROBABILITY_FIELD = 0x305 # Values must be between 0.0 and 1.0

## TESTING PROTAG IMAGE PATH DICT
IMAGE_PATH_DICT_PROTAG = {
    imageids.OW_IMAGE_ID_DEFAULT: imagepaths.PROT_RANGER_F_OW_DEFAULT,
    imageids.OW_IMAGE_ID_FACE_NORTH: imagepaths.PROT_RANGER_F_OW_FACE_NORTH,
    imageids.OW_IMAGE_ID_FACE_EAST: imagepaths.PROT_RANGER_F_OW_FACE_EAST,
    imageids.OW_IMAGE_ID_FACE_SOUTH: imagepaths.PROT_RANGER_F_OW_FACE_SOUTH,
    imageids.OW_IMAGE_ID_FACE_WEST: imagepaths.PROT_RANGER_F_OW_FACE_WEST,
    imageids.OW_IMAGE_ID_WALK1_NORTH: imagepaths.PROT_RANGER_F_OW_WALK1_NORTH,
    imageids.OW_IMAGE_ID_WALK1_EAST: imagepaths.PROT_RANGER_F_OW_WALK1_EAST,
    imageids.OW_IMAGE_ID_WALK1_SOUTH: imagepaths.PROT_RANGER_F_OW_WALK1_SOUTH,
    imageids.OW_IMAGE_ID_WALK1_WEST: imagepaths.PROT_RANGER_F_OW_WALK1_WEST,
    imageids.OW_IMAGE_ID_WALK2_NORTH: imagepaths.PROT_RANGER_F_OW_WALK2_NORTH,
    imageids.OW_IMAGE_ID_WALK2_EAST: imagepaths.PROT_RANGER_F_OW_WALK2_EAST,
    imageids.OW_IMAGE_ID_WALK2_SOUTH: imagepaths.PROT_RANGER_F_OW_WALK2_SOUTH,
    imageids.OW_IMAGE_ID_WALK2_WEST: imagepaths.PROT_RANGER_F_OW_WALK2_WEST,
    imageids.BATTLE_IMAGE_ID_DEFAULT: imagepaths.PROT_RANGER_F_OW_DEFAULT,
    imageids.BATTLE_IMAGE_ID_STAND: imagepaths.PROT_RANGER_F_OW_DEFAULT,
    imageids.BATTLE_IMAGE_ID_ATTACK: imagepaths.PROT_RANGER_F_OW_DEFAULT,
    imageids.BATTLE_IMAGE_ID_FAINTED: imagepaths.PROT_RANGER_F_OW_DEFAULT,
}

### MISCELLANEOUS OBJECT DATA ###
MISC_OBJECT_DATA = {
    ORE_EMPTY_ID: {
        OBJECT_NAME_INFO_FIELD: {
            language.LANG_ENGLISH: "EMPTY ORE",
            language.LANG_ESPANOL: "VENA AGOTADA",
        },
        IMAGE_PATH_DICT_FIELD: {
            imageids.IMAGE_ID_DEFAULT: imagepaths.ORE_EMPTY_BASIC_PATH,
            imageids.OW_IMAGE_ID_DEFAULT: imagepaths.ORE_EMPTY_BASIC_PATH,
        },
        COLLISION_WIDTH_FIELD: 1,
        COLLISION_HEIGHT_FIELD: 1,
        RESPAWN_TIME_S_FIELD:  None,
        EXAMINE_INFO_FIELD: {
            language.LANG_ENGLISH: "This ore is empty.",
            language.LANG_ESPANOL: "Esta vena esta agotada.",
        },
    },
    TREE_STUMP_ID: {
        OBJECT_NAME_INFO_FIELD: {
            language.LANG_ENGLISH: "TREE STUMP",
            language.LANG_ESPANOL: "TOCON",
        },
        IMAGE_PATH_DICT_FIELD: {
            imageids.IMAGE_ID_DEFAULT: imagepaths.TREE_STUMP_PATH,
            imageids.OW_IMAGE_ID_DEFAULT: imagepaths.TREE_STUMP_PATH,
        },
        COLLISION_WIDTH_FIELD: 2,
        COLLISION_HEIGHT_FIELD: 1,
        RESPAWN_TIME_S_FIELD:  None,
        EXAMINE_INFO_FIELD: {
            language.LANG_ENGLISH: "There used to be a tree here.",
            language.LANG_ESPANOL: "Solia haber un arbol aqui.",
        },
    },
}

### RESOURCE DATA ###
RESOURCE_DATA = {
    HERB_BASIC_ID: {
        OBJECT_NAME_INFO_FIELD: {
            language.LANG_ENGLISH: "BASIC HERB",
            language.LANG_ESPANOL: "HIERBA BASICA",
        },
        IMAGE_PATH_DICT_FIELD: {
            imageids.IMAGE_ID_DEFAULT: imagepaths.HERB_BASIC_PATH,
            imageids.OW_IMAGE_ID_DEFAULT: imagepaths.HERB_BASIC_PATH,
        },
        COLLISION_WIDTH_FIELD: 1,
        COLLISION_HEIGHT_FIELD: 1,
        RELATED_SKILL_ID_FIELD: skills.SKILL_ID_HERBLORE,
        REQUIRED_LEVEL_FIELD: 1,
        GAINED_XP_FIELD: 20,
        RESOURCE_ITEM_FIELD: None,
        RESPAWN_TIME_S_FIELD:  1,
        EXAMINE_INFO_FIELD: {
            language.LANG_ENGLISH: "Maybe I can pick this herb.",
            language.LANG_ESPANOL: "Tal vez pueda cosechar esta hierba.",
        },
        INTERACTION_ID_FIELD: interactiondata.HERBLORE_GATHER_ID,
        EXHAUSTION_PROBABILITY_FIELD: 0.3,
    },
    TREE_BASIC_ID: {
        OBJECT_NAME_INFO_FIELD: {
            language.LANG_ENGLISH: "TREE",
            language.LANG_ESPANOL: "ARBOL",
        },
        IMAGE_PATH_DICT_FIELD: {
            imageids.IMAGE_ID_DEFAULT: imagepaths.TREE_BASIC_PATH,
            imageids.OW_IMAGE_ID_DEFAULT: imagepaths.TREE_BASIC_PATH,
        },
        COLLISION_WIDTH_FIELD: 2,
        COLLISION_HEIGHT_FIELD: 1,
        RELATED_SKILL_ID_FIELD: skills.SKILL_ID_WOODCUTTING,
        REQUIRED_LEVEL_FIELD: 1,
        GAINED_XP_FIELD: 20,
        RESOURCE_ITEM_FIELD: None,
        RESPAWN_TIME_S_FIELD:  1,
        EXAMINE_INFO_FIELD: {
            language.LANG_ENGLISH: "It's just a tree. Maybe I can cut it down.",
            language.LANG_ESPANOL: "Es solo un arbol. Tal vez pueda talarlo.",
        },
        INTERACTION_ID_FIELD: interactiondata.CHOP_TREE_ID,
        EXHAUSTION_PROBABILITY_FIELD: 1.0,
    },
    TREE_OAK_ID: {
        OBJECT_NAME_INFO_FIELD: {
            language.LANG_ENGLISH: "OAK TREE",
            language.LANG_ESPANOL: "ROBLE",
        },
        IMAGE_PATH_DICT_FIELD: {
            imageids.IMAGE_ID_DEFAULT: imagepaths.TREE_OAK_PATH,
            imageids.OW_IMAGE_ID_DEFAULT: imagepaths.TREE_OAK_PATH,
        },
        COLLISION_WIDTH_FIELD: 2,
        COLLISION_HEIGHT_FIELD: 1,
        RELATED_SKILL_ID_FIELD: skills.SKILL_ID_WOODCUTTING,
        REQUIRED_LEVEL_FIELD: 10,
        GAINED_XP_FIELD: 50,
        RESOURCE_ITEM_FIELD: None,
        RESPAWN_TIME_S_FIELD:  10,
        EXAMINE_INFO_FIELD: {
            language.LANG_ENGLISH: "What a magnificent oak. Maybe I can cut it down.",
            language.LANG_ESPANOL: "Que roble tan maravilloso! Tal vez pueda talarlo.",
        },
        INTERACTION_ID_FIELD: interactiondata.CHOP_TREE_ID,
        EXHAUSTION_PROBABILITY_FIELD: 0.2,
    },
}
