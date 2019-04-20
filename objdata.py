import imagepaths
import skills
import language
import interactiondata
import imageids
import itemdata

### INTERACTIVE OBJECT TYPE ID CONSTANTS ###
TYPE_CHARACTER = 0x1
TYPE_MONSTER = 0x2
TYPE_RESOURCE = 0x3
TYPE_ITEM = 0x4
TYPE_OBSTACLE = 0x5
TYPE_CHEST = 0x6
TYPE_MISC = 0x7

### INTERACTIVE OBJECT ID NUMBERS ###
# SPECIAL IDS ARE 1 TO 0X99999
MIN_SPECIAL_ID = 1
MAX_SPECIAL_ID = 99999
PROTAGONIST_ID = 2

# CHARACTER IDS ARE 100000 TO 199999
MIN_CHARACTER_ID = 100000
MAX_CHARACTER_ID = 199999

# MONSTER IDS ARE 200000 TO 299999
MIN_MONSTER_ID = 200000
MAX_MONSTER_ID = 299999

# RESOURCE IDS ARE 300000 TO 399999
MIN_RESOURCE_ID = 300000
MAX_RESOURCE_ID = 399999

# 301000 for harvestable plants.
HERB_BASIC_ID = 301001
PALM_WITH_COCONUT_ID = 301101 # turn into standard palm tree after?

# 302000 for Trees.

# Standard trees.
TREE_BASIC_ID = 302001 # 1 woodcutting.
TREE_BAMBOO_ID = 302005 # 5 woodcutting.
TREE_OAK_ID = 302010 # 10 woodcutting?
TREE_WILLOW_ID = 302015 # 25 woodcutting?
TREE_MAPLE_ID = 302020 # 40 woodcutting?
TREE_YEW_ID = 302025 # 55 woodcutting?
TREE_ANCIENT_ID = 302030 # 70 woodcutting?
TREE_ASTRAL_ID = 302035 # 85 woodcutting?
TREE_CELESTIAL_ID = 302040 # 95 woodcutting.
TREE_TEAK_ID = 302045 # 30 woodcutting?
TREE_MAHOGANY_ID = 302050 # 45 woodcutting?
TREE_EUCALYPTUS_ID = 302055 # 60 woodcutting?

# Winter region trees.
TREE_PINE_ID = 302101 # 1 woodcutting.

# Tropical region trees.
TREE_PALM_ID = 302201 # 20 woodcutting.

# Other trees.
TREE_SPIRIT_ID = 302301
TREE_DARK_ID = 302305

# 303000 for ore rocks.
ROCK_COPPER_ID = 303001
ROCK_COPPER_2_ID = 303002
ROCK_TIN_ID = 303011
ROCK_TIN_2_ID = 303012
ROCK_ZINC_ID = 303021
ROCK_ZINC_2_ID = 303022
ROCK_ZINC_ID = 303021
ROCK_ZINC_2_ID = 303022
ROCK_IRON_ID = 303031
ROCK_IRON_2_ID = 303032
ROCK_COAL_ID = 303041
ROCK_COAL_2_ID = 303042
ROCK_TITANIUM_ID = 303051
ROCK_TITANIUM_2_ID = 303052
ROCK_MITHRIL_ID = 303061
ROCK_MITHRIL_2_ID = 303062
ROCK_ADAMANT_ID = 303071
ROCK_ADAMANT_2_ID = 303072
ROCK_ANCIENT_ID = 303081
ROCK_ANCIENT_2_ID = 303082
ROCK_METEORITE_ID = 303091
ROCK_METEORITE_2_ID = 303092
ROCK_CELESTIAL_ID = 303101
ROCK_CELESTIAL_2_ID = 303102
ROCK_SILVER_ID = 303201
ROCK_SILVER_2_ID = 303202
ROCK_GOLD_ID = 303211
ROCK_GOLD_2_ID = 303212

# 304000 for fishing spots.
FISHING_SPOT_1_ID = 304001

# ITEM IDS ARE 400000 TO 499999
MIN_ITEM_ID = 400000
MAX_ITEM_ID = 499999

# OBSTACLE IDS ARE 500000 TO 599999
MIN_OBSTACLE_ID = 500000
MAX_OBSTACLE_ID = 599999

# CHEST IDS ARE 600000 TO 699999
MIN_CHEST_ID = 600000
MAX_CHEST_ID = 699999

# MISCELLANEOUS IDS ARE 700000 TO 799999
MIN_MISC_ID = 700000
ROCK_EMPTY_ID = 700001
TREE_STUMP_ID = 700002
WILLOW_STUMP_ID = 700003
FISHING_SPOT_EMPTY_ID = 700100
MAX_MISC_ID = 799999

### OBJECT DATA FIELDS ###
OBJECT_NAME_INFO_FIELD = 0x1
IMAGE_INFO_DICT_FIELD = 0x2
COLLISION_WIDTH_FIELD = 0x3
COLLISION_HEIGHT_FIELD = 0x4
EXAMINE_INFO_FIELD = 0x5
INTERACTION_ID_FIELD = 0x6
REPLACEMENT_OBJECT_ID_FIELD = 0x7
RESPAWN_TIME_S_FIELD = 0x8

### RESOURCE DATA FIELDS ###
RELATED_SKILL_ID_FIELD = 0x301
MIN_REQUIRED_LEVEL_FIELD = 0x302

# Map to list of tuples of the form
#(resource item ID, required level,
# probability weighting, exp gained)
RESOURCE_ITEM_INFO_FIELD = 0x306

#GAINED_XP_FIELD = 0x303
#RESOURCE_ITEM_FIELD = 0x304
EXHAUSTION_PROBABILITY_FIELD = 0x305 # Values must be between 0.0 and 1.0

## TESTING PROTAG IMAGE PATH DICT
IMAGE_INFO_DICT_PROTAG = {
    imageids.SEQUENCE_ID_DEFAULT: imagepaths.PROT_RANGER_F_OW_DEFAULT,
    imageids.SEQUENCE_ID_FACE_NORTH: imagepaths.PROT_RANGER_F_OW_FACE_NORTH,
    imageids.SEQUENCE_ID_FACE_EAST: imagepaths.PROT_RANGER_F_OW_FACE_EAST,
    imageids.SEQUENCE_ID_FACE_SOUTH: imagepaths.PROT_RANGER_F_OW_FACE_SOUTH,
    imageids.SEQUENCE_ID_FACE_WEST: imagepaths.PROT_RANGER_F_OW_FACE_WEST,
    imageids.SEQUENCE_ID_WALK_NORTH: [
        [
            imagepaths.PROT_RANGER_F_OW_WALK1_NORTH,
            imagepaths.PROT_RANGER_F_OW_FACE_NORTH,
            imagepaths.PROT_RANGER_F_OW_WALK2_NORTH,
            imagepaths.PROT_RANGER_F_OW_FACE_NORTH,
        ],
        None
    ],
    imageids.SEQUENCE_ID_WALK_EAST: [
        [
            imagepaths.PROT_RANGER_F_OW_WALK1_EAST,
            imagepaths.PROT_RANGER_F_OW_FACE_EAST,
            imagepaths.PROT_RANGER_F_OW_WALK2_EAST,
            imagepaths.PROT_RANGER_F_OW_FACE_EAST,
        ],
        None
    ],
    imageids.SEQUENCE_ID_WALK_SOUTH: [
        [
            imagepaths.PROT_RANGER_F_OW_WALK1_SOUTH,
            imagepaths.PROT_RANGER_F_OW_FACE_SOUTH,
            imagepaths.PROT_RANGER_F_OW_WALK2_SOUTH,
            imagepaths.PROT_RANGER_F_OW_FACE_SOUTH,
        ],
        None
    ],
    imageids.SEQUENCE_ID_WALK_WEST: [
        [
            imagepaths.PROT_RANGER_F_OW_WALK1_WEST,
            imagepaths.PROT_RANGER_F_OW_FACE_WEST,
            imagepaths.PROT_RANGER_F_OW_WALK2_WEST,
            imagepaths.PROT_RANGER_F_OW_FACE_WEST,
        ],
        None
    ],
    imageids.BATTLE_SEQUENCE_ID_DEFAULT: imagepaths.PROT_RANGER_F_OW_DEFAULT,
    imageids.BATTLE_SEQUENCE_ID_STAND: imagepaths.PROT_RANGER_F_OW_DEFAULT,
    imageids.BATTLE_SEQUENCE_ID_ATTACK: imagepaths.PROT_RANGER_F_OW_DEFAULT,
    imageids.BATTLE_SEQUENCE_ID_FAINTED: imagepaths.PROT_RANGER_F_OW_DEFAULT,
}

### MISCELLANEOUS OBJECT DATA ###
MISC_OBJECT_DATA = {
    ROCK_EMPTY_ID: {
        OBJECT_NAME_INFO_FIELD: {
            language.LANG_ENGLISH: "EMPTY ORE",
            language.LANG_ESPANOL: "VENA AGOTADA",
        },
        IMAGE_INFO_DICT_FIELD: {
            imageids.OBJ_SPRITE_SEQUENCE_ID: imagepaths.ROCK_EMPTY_BASIC_PATH,
        },
        COLLISION_WIDTH_FIELD: 1,
        COLLISION_HEIGHT_FIELD: 1,
        RESPAWN_TIME_S_FIELD:  None,
        EXAMINE_INFO_FIELD: {
            language.LANG_ENGLISH: "This ore is empty.",
            language.LANG_ESPANOL: "Esta vena esta agotada.",
        },
    },
    FISHING_SPOT_EMPTY_ID: {
        OBJECT_NAME_INFO_FIELD: {
            language.LANG_ENGLISH: "EMPTY FISHING SPOT",
            language.LANG_ESPANOL: "LUGAR PARA PESCAR AGOTADO",
        },
        IMAGE_INFO_DICT_FIELD: {
            imageids.OBJ_SPRITE_SEQUENCE_ID: imagepaths.FISHING_SPOT_1_PATH,
        },
        COLLISION_WIDTH_FIELD: 1,
        COLLISION_HEIGHT_FIELD: 1,
        RESPAWN_TIME_S_FIELD:  None,
        EXAMINE_INFO_FIELD: {
            language.LANG_ENGLISH: "There used to be fish here.",
            language.LANG_ESPANOL: "Solia haber peces aqui.",
        },
    },
    TREE_STUMP_ID: {
        OBJECT_NAME_INFO_FIELD: {
            language.LANG_ENGLISH: "TREE STUMP",
            language.LANG_ESPANOL: "TOCON",
        },
        IMAGE_INFO_DICT_FIELD: {
            imageids.OBJ_SPRITE_SEQUENCE_ID: imagepaths.TREE_STUMP_PATH,
        },
        COLLISION_WIDTH_FIELD: 2,
        COLLISION_HEIGHT_FIELD: 1,
        RESPAWN_TIME_S_FIELD:  None,
        EXAMINE_INFO_FIELD: {
            language.LANG_ENGLISH: "There used to be a tree here.",
            language.LANG_ESPANOL: "Solia haber un arbol aqui.",
        },
    },
    WILLOW_STUMP_ID: {
        OBJECT_NAME_INFO_FIELD: {
            language.LANG_ENGLISH: "WILLOW STUMP",
            language.LANG_ESPANOL: "TOCON DE SAUCE",
        },
        IMAGE_INFO_DICT_FIELD: {
            imageids.OBJ_SPRITE_SEQUENCE_ID: imagepaths.WILLOW_STUMP_PATH,
        },
        COLLISION_WIDTH_FIELD: 2,
        COLLISION_HEIGHT_FIELD: 1,
        RESPAWN_TIME_S_FIELD:  None,
        EXAMINE_INFO_FIELD: {
            language.LANG_ENGLISH: "There used to be a willow here.",
            language.LANG_ESPANOL: "Solia haber un sauce aqui.",
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
        IMAGE_INFO_DICT_FIELD: {
            imageids.OBJ_SPRITE_SEQUENCE_ID: imagepaths.HERB_BASIC_PATH,
        },
        COLLISION_WIDTH_FIELD: 1,
        COLLISION_HEIGHT_FIELD: 1,
        RELATED_SKILL_ID_FIELD: skills.SKILL_ID_HERBLORE,
        MIN_REQUIRED_LEVEL_FIELD: 1,
        #GAINED_XP_FIELD: 20,
        #RESOURCE_ITEM_FIELD: None,
        RESPAWN_TIME_S_FIELD:  10,
        EXAMINE_INFO_FIELD: {
            language.LANG_ENGLISH: "Maybe I can pick this herb.",
            language.LANG_ESPANOL: "Tal vez pueda cosechar esta hierba.",
        },
        INTERACTION_ID_FIELD: interactiondata.HERBLORE_GATHER_ID,
        EXHAUSTION_PROBABILITY_FIELD: 0.3,
        RESOURCE_ITEM_INFO_FIELD: [
            (None, 1, 1, 20),
        ],
    },
    TREE_BASIC_ID: {
        OBJECT_NAME_INFO_FIELD: {
            language.LANG_ENGLISH: "TREE",
            language.LANG_ESPANOL: "ARBOL",
        },
        IMAGE_INFO_DICT_FIELD: {
            imageids.OBJ_SPRITE_SEQUENCE_ID: imagepaths.TREE_BASIC_PATH,
        },
        COLLISION_WIDTH_FIELD: 2,
        COLLISION_HEIGHT_FIELD: 1,
        RELATED_SKILL_ID_FIELD: skills.SKILL_ID_WOODCUTTING,
        MIN_REQUIRED_LEVEL_FIELD: 1,
        #GAINED_XP_FIELD: 20,
        #RESOURCE_ITEM_FIELD: itemdata.LOG_TREE_ID,
        RESPAWN_TIME_S_FIELD:  10,
        EXAMINE_INFO_FIELD: {
            language.LANG_ENGLISH: "It's just a tree. Maybe I can cut it down.",
            language.LANG_ESPANOL: "Es solo un arbol. Tal vez pueda talarlo.",
        },
        INTERACTION_ID_FIELD: interactiondata.CHOP_TREE_ID,
        EXHAUSTION_PROBABILITY_FIELD: 1.0,  # TODO change.
        REPLACEMENT_OBJECT_ID_FIELD: TREE_STUMP_ID,
        RESOURCE_ITEM_INFO_FIELD: [
            (itemdata.LOG_TREE_ID, 1, 1, 20),
        ],
    },
    TREE_OAK_ID: {
        OBJECT_NAME_INFO_FIELD: {
            language.LANG_ENGLISH: "OAK TREE",
            language.LANG_ESPANOL: "ROBLE",
        },
        IMAGE_INFO_DICT_FIELD: {
            imageids.OBJ_SPRITE_SEQUENCE_ID: imagepaths.TREE_OAK_PATH,
        },
        COLLISION_WIDTH_FIELD: 2,
        COLLISION_HEIGHT_FIELD: 1,
        RELATED_SKILL_ID_FIELD: skills.SKILL_ID_WOODCUTTING,
        MIN_REQUIRED_LEVEL_FIELD: 10,
        #GAINED_XP_FIELD: 50,
        #RESOURCE_ITEM_FIELD: itemdata.LOG_OAK_ID,
        RESPAWN_TIME_S_FIELD:  30,
        EXAMINE_INFO_FIELD: {
            language.LANG_ENGLISH: "What a magnificent oak. Maybe I can cut it down.",
            language.LANG_ESPANOL: "Que roble tan maravilloso! Tal vez pueda talarlo.",
        },
        INTERACTION_ID_FIELD: interactiondata.CHOP_TREE_ID,
        EXHAUSTION_PROBABILITY_FIELD: 0.2,
        REPLACEMENT_OBJECT_ID_FIELD: TREE_STUMP_ID,
        RESOURCE_ITEM_INFO_FIELD: [
            (itemdata.LOG_OAK_ID, 10, 1, 50),
        ],
    },
    TREE_WILLOW_ID: {
        OBJECT_NAME_INFO_FIELD: {
            language.LANG_ENGLISH: "WILLOW TREE",
            language.LANG_ESPANOL: "SAUCE",
        },
        IMAGE_INFO_DICT_FIELD: {
            imageids.OBJ_SPRITE_SEQUENCE_ID: imagepaths.TREE_WILLOW_PATH,
        },
        COLLISION_WIDTH_FIELD: 2,
        COLLISION_HEIGHT_FIELD: 1,
        RELATED_SKILL_ID_FIELD: skills.SKILL_ID_WOODCUTTING,
        MIN_REQUIRED_LEVEL_FIELD: 25,
        #GAINED_XP_FIELD: 100,
        #RESOURCE_ITEM_FIELD: itemdata.LOG_WILLOW_ID,
        RESPAWN_TIME_S_FIELD:  120,
        EXAMINE_INFO_FIELD: {
            language.LANG_ENGLISH: "What a magnificent willow. These grow by water.",
            language.LANG_ESPANOL: "Que sauce tan maravilloso! Estos crecen cerca de agua.",
        },
        INTERACTION_ID_FIELD: interactiondata.CHOP_TREE_ID,
        EXHAUSTION_PROBABILITY_FIELD: 0.2,
        REPLACEMENT_OBJECT_ID_FIELD: WILLOW_STUMP_ID,
        RESOURCE_ITEM_INFO_FIELD: [
            (itemdata.LOG_WILLOW_ID, 25, 1, 100),
        ],
    },
    ROCK_COPPER_ID: {
        OBJECT_NAME_INFO_FIELD: {
            language.LANG_ENGLISH: "COPPER VEIN",
            language.LANG_ESPANOL: "VENA DE COBRE",
        },
        IMAGE_INFO_DICT_FIELD: {
            imageids.OBJ_SPRITE_SEQUENCE_ID: imagepaths.ROCK_COPPER_BASIC_PATH,
        },
        COLLISION_WIDTH_FIELD: 1,
        COLLISION_HEIGHT_FIELD: 1,
        RELATED_SKILL_ID_FIELD: skills.SKILL_ID_MINING,
        MIN_REQUIRED_LEVEL_FIELD: 10,
        #GAINED_XP_FIELD: 35,
        #RESOURCE_ITEM_FIELD: itemdata.ORE_COPPER_ID,
        RESPAWN_TIME_S_FIELD:  10,
        EXAMINE_INFO_FIELD: {
            language.LANG_ENGLISH: "There is some copper ore in this rock. Maybe I can mine it.",
            language.LANG_ESPANOL: "Hay mineral de cobre en esta vena. Tal vez pueda extraerlo.",
        },
        INTERACTION_ID_FIELD: interactiondata.MINE_ROCK_ID,
        EXHAUSTION_PROBABILITY_FIELD: 1.0,
        REPLACEMENT_OBJECT_ID_FIELD: ROCK_EMPTY_ID,
        RESOURCE_ITEM_INFO_FIELD: [
            (itemdata.ORE_COPPER_ID, 10, 1, 35),
        ],
    },
    ROCK_TIN_ID: {
        OBJECT_NAME_INFO_FIELD: {
            language.LANG_ENGLISH: "TIN VEIN",
            language.LANG_ESPANOL: "VENA DE ESTAÑO",
        },
        IMAGE_INFO_DICT_FIELD: {
            imageids.OBJ_SPRITE_SEQUENCE_ID: imagepaths.ROCK_TIN_BASIC_PATH,
        },
        COLLISION_WIDTH_FIELD: 1,
        COLLISION_HEIGHT_FIELD: 1,
        RELATED_SKILL_ID_FIELD: skills.SKILL_ID_MINING,
        MIN_REQUIRED_LEVEL_FIELD: 10,
        #GAINED_XP_FIELD: 35,
        #RESOURCE_ITEM_FIELD: itemdata.ORE_TIN_ID,
        RESPAWN_TIME_S_FIELD:  10,
        EXAMINE_INFO_FIELD: {
            language.LANG_ENGLISH: "There is some tin ore in this rock. Maybe I can mine it.",
            language.LANG_ESPANOL: "Hay mineral de estaño en esta vena. Tal vez pueda extraerlo.",
        },
        INTERACTION_ID_FIELD: interactiondata.MINE_ROCK_ID,
        EXHAUSTION_PROBABILITY_FIELD: 1.0,
        REPLACEMENT_OBJECT_ID_FIELD: ROCK_EMPTY_ID,
        RESOURCE_ITEM_INFO_FIELD: [
            (itemdata.ORE_TIN_ID, 10, 1, 35),
        ],
    },
    ROCK_IRON_ID: {
        OBJECT_NAME_INFO_FIELD: {
            language.LANG_ENGLISH: "IRON VEIN",
            language.LANG_ESPANOL: "VENA DE HIERRO",
        },
        IMAGE_INFO_DICT_FIELD: {
            imageids.OBJ_SPRITE_SEQUENCE_ID: imagepaths.ROCK_IRON_BASIC_PATH,
        },
        COLLISION_WIDTH_FIELD: 1,
        COLLISION_HEIGHT_FIELD: 1,
        RELATED_SKILL_ID_FIELD: skills.SKILL_ID_MINING,
        MIN_REQUIRED_LEVEL_FIELD: 20,
        #GAINED_XP_FIELD: 50,
        #RESOURCE_ITEM_FIELD: itemdata.ORE_IRON_ID,
        RESPAWN_TIME_S_FIELD:  20,
        EXAMINE_INFO_FIELD: {
            language.LANG_ENGLISH: "There is some iron ore in this rock. Maybe I can mine it.",
            language.LANG_ESPANOL: "Hay mineral de hierro en esta vena. Tal vez pueda extraerlo.",
        },
        INTERACTION_ID_FIELD: interactiondata.MINE_ROCK_ID,
        EXHAUSTION_PROBABILITY_FIELD: 1.0,
        REPLACEMENT_OBJECT_ID_FIELD: ROCK_EMPTY_ID,
        RESOURCE_ITEM_INFO_FIELD: [
            (itemdata.ORE_IRON_ID, 20, 1, 50),
        ],
    },
    ROCK_COAL_ID: {
        OBJECT_NAME_INFO_FIELD: {
            language.LANG_ENGLISH: "COAL VEIN",
            language.LANG_ESPANOL: "VENA DE CARBÓN",
        },
        IMAGE_INFO_DICT_FIELD: {
            imageids.OBJ_SPRITE_SEQUENCE_ID: imagepaths.ROCK_COAL_BASIC_PATH,
        },
        COLLISION_WIDTH_FIELD: 1,
        COLLISION_HEIGHT_FIELD: 1,
        RELATED_SKILL_ID_FIELD: skills.SKILL_ID_MINING,
        MIN_REQUIRED_LEVEL_FIELD: 30,
        #GAINED_XP_FIELD: 75,
        #RESOURCE_ITEM_FIELD: itemdata.ORE_COAL_ID,
        RESPAWN_TIME_S_FIELD:  100,
        EXAMINE_INFO_FIELD: {
            language.LANG_ENGLISH: "There is some coal in this rock. Maybe I can mine it.",
            language.LANG_ESPANOL: "Hay mineral de carbón en esta vena. Tal vez pueda extraerlo.",
        },
        INTERACTION_ID_FIELD: interactiondata.MINE_ROCK_ID,
        EXHAUSTION_PROBABILITY_FIELD: 1.0,
        REPLACEMENT_OBJECT_ID_FIELD: ROCK_EMPTY_ID,
        RESOURCE_ITEM_INFO_FIELD: [
            (itemdata.ORE_COAL_ID, 30, 1, 75),
        ],
    },
    ROCK_SILVER_ID: {
        OBJECT_NAME_INFO_FIELD: {
            language.LANG_ENGLISH: "SILVER VEIN",
            language.LANG_ESPANOL: "VENA DE PLATA",
        },
        IMAGE_INFO_DICT_FIELD: {
            imageids.OBJ_SPRITE_SEQUENCE_ID: imagepaths.ROCK_SILVER_BASIC_PATH,
        },
        COLLISION_WIDTH_FIELD: 1,
        COLLISION_HEIGHT_FIELD: 1,
        RELATED_SKILL_ID_FIELD: skills.SKILL_ID_MINING,
        MIN_REQUIRED_LEVEL_FIELD: 35,
        #GAINED_XP_FIELD: 80,
        #RESOURCE_ITEM_FIELD: itemdata.ORE_SILVER_ID,
        RESPAWN_TIME_S_FIELD:  200,
        EXAMINE_INFO_FIELD: {
            language.LANG_ENGLISH: "There is some silver ore in this rock. Maybe I can mine it.",
            language.LANG_ESPANOL: "Hay mineral de plata en esta vena. Tal vez pueda extraerlo.",
        },
        INTERACTION_ID_FIELD: interactiondata.MINE_ROCK_ID,
        EXHAUSTION_PROBABILITY_FIELD: 1.0,
        REPLACEMENT_OBJECT_ID_FIELD: ROCK_EMPTY_ID,
        RESOURCE_ITEM_INFO_FIELD: [
            (itemdata.ORE_SILVER_ID, 35, 1, 80),
        ],
    },
    ROCK_TITANIUM_ID: {
        OBJECT_NAME_INFO_FIELD: {
            language.LANG_ENGLISH: "TITANIUM VEIN",
            language.LANG_ESPANOL: "VENA DE TITANIO",
        },
        IMAGE_INFO_DICT_FIELD: {
            imageids.OBJ_SPRITE_SEQUENCE_ID: imagepaths.ROCK_TITANIUM_BASIC_PATH,
        },
        COLLISION_WIDTH_FIELD: 1,
        COLLISION_HEIGHT_FIELD: 1,
        RELATED_SKILL_ID_FIELD: skills.SKILL_ID_MINING,
        MIN_REQUIRED_LEVEL_FIELD: 40,
        #GAINED_XP_FIELD: 85,
        #RESOURCE_ITEM_FIELD: itemdata.ORE_TITANIUM_ID,
        RESPAWN_TIME_S_FIELD:  180,
        EXAMINE_INFO_FIELD: {
            language.LANG_ENGLISH: "There is some titanium ore in this rock. Maybe I can mine it.",
            language.LANG_ESPANOL: "Hay mineral de titanio en esta vena. Tal vez pueda extraerlo.",
        },
        INTERACTION_ID_FIELD: interactiondata.MINE_ROCK_ID,
        EXHAUSTION_PROBABILITY_FIELD: 1.0,
        REPLACEMENT_OBJECT_ID_FIELD: ROCK_EMPTY_ID,
        RESOURCE_ITEM_INFO_FIELD: [
            (itemdata.ORE_TITANIUM_ID, 40, 1, 85),
        ],
    },
    ROCK_GOLD_ID: {
        OBJECT_NAME_INFO_FIELD: {
            language.LANG_ENGLISH: "GOLD VEIN",
            language.LANG_ESPANOL: "VENA DE ORO",
        },
        IMAGE_INFO_DICT_FIELD: {
            imageids.OBJ_SPRITE_SEQUENCE_ID: imagepaths.ROCK_GOLD_BASIC_PATH,
        },
        COLLISION_WIDTH_FIELD: 1,
        COLLISION_HEIGHT_FIELD: 1,
        RELATED_SKILL_ID_FIELD: skills.SKILL_ID_MINING,
        MIN_REQUIRED_LEVEL_FIELD: 55,
        #GAINED_XP_FIELD: 110,
        #RESOURCE_ITEM_FIELD: itemdata.ORE_GOLD_ID,
        RESPAWN_TIME_S_FIELD:  240,
        EXAMINE_INFO_FIELD: {
            language.LANG_ENGLISH: "There is some gold ore in this rock. Maybe I can mine it.",
            language.LANG_ESPANOL: "Hay mineral de oro en esta vena. Tal vez pueda extraerlo.",
        },
        INTERACTION_ID_FIELD: interactiondata.MINE_ROCK_ID,
        EXHAUSTION_PROBABILITY_FIELD: 1.0,
        REPLACEMENT_OBJECT_ID_FIELD: ROCK_EMPTY_ID,
        RESOURCE_ITEM_INFO_FIELD: [
            (itemdata.ORE_GOLD_ID, 55, 1, 110),
        ],
    },
    FISHING_SPOT_1_ID: {
        OBJECT_NAME_INFO_FIELD: {
            language.LANG_ENGLISH: "FISHING SPOT",
            language.LANG_ESPANOL: "LUGAR PARA PESCAR",
        },
        IMAGE_INFO_DICT_FIELD: {
            imageids.OBJ_SPRITE_SEQUENCE_ID: [
                [
                    imagepaths.FISHING_SPOT_5_PATH,
                    imagepaths.FISHING_SPOT_6_PATH,
                    imagepaths.FISHING_SPOT_7_PATH,
                ],
                900,
            ]
        },
        COLLISION_WIDTH_FIELD: 1,
        COLLISION_HEIGHT_FIELD: 1,
        RELATED_SKILL_ID_FIELD: skills.SKILL_ID_FISHING,
        MIN_REQUIRED_LEVEL_FIELD: 1,
        #GAINED_XP_FIELD: 20,
        #RESOURCE_ITEM_FIELD: itemdata.ORE_GOLD_ID,
        RESPAWN_TIME_S_FIELD:  60,
        EXAMINE_INFO_FIELD: {
            language.LANG_ENGLISH: "I can see fish in the water. Maybe I can catch them.",
            language.LANG_ESPANOL: "Se veían peces en el agua. Tal vez pueda atraparlos.",
        },
        INTERACTION_ID_FIELD: interactiondata.CATCH_FISH_ROD_ID,
        EXHAUSTION_PROBABILITY_FIELD: 0.2,
        REPLACEMENT_OBJECT_ID_FIELD: FISHING_SPOT_EMPTY_ID,
        RESOURCE_ITEM_INFO_FIELD: [
            (itemdata.FISH_RAW_PERCH_ID, 1, 1, 20),
            (itemdata.FISH_RAW_TROUT_ID, 10, 2, 40),
            (itemdata.FISH_RAW_SALMON_ID, 25, 2, 65),
        ],
    },
}
