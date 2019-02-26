### IMAGE ID NUMBERS ###

### DEFAULT IMAGE ID ###
IMAGE_ID_DEFAULT = 0x001

### OVERWORLD IMAGE TYPE ID NUMBERS ###
OW_IMAGE_ID_DEFAULT = 0x101
OW_IMAGE_ID_FACE_NORTH = 0x102
OW_IMAGE_ID_FACE_EAST = 0x103
OW_IMAGE_ID_FACE_SOUTH = 0x104
OW_IMAGE_ID_FACE_WEST = 0x105
OW_IMAGE_ID_WALK1_NORTH = 0x106
OW_IMAGE_ID_WALK1_EAST = 0x107
OW_IMAGE_ID_WALK1_SOUTH = 0x108
OW_IMAGE_ID_WALK1_WEST = 0x109
OW_IMAGE_ID_WALK2_NORTH = 0x10a
OW_IMAGE_ID_WALK2_EAST = 0x10b
OW_IMAGE_ID_WALK2_SOUTH = 0x10c
OW_IMAGE_ID_WALK2_WEST = 0x10d

### BATTLE MODE IMAGE TYPE ID NUMBERS ###
BATTLE_IMAGE_ID_DEFAULT = 0x201
BATTLE_IMAGE_ID_STAND = 0x202
BATTLE_IMAGE_ID_ATTACK = 0x203
BATTLE_IMAGE_ID_FAINTED = 0x204

### SKILLING IMAGE CATEGORY IDS ###
IMAGE_CATEGORY_SMITHING_SMELTING = 0x101
IMAGE_CATEGORY_SMITHING_ANVIL = 0x102
IMAGE_CATEGORY_HERBLORE_HARVEST = 0x201
IMAGE_CATEGORY_HERBLORE_POTION = 0x202
IMAGE_CATEGORY_CRAFTING_CLOTHES = 0x301
IMAGE_CATEGORY_CRAFTING_GEMS = 0x302
IMAGE_CATEGORY_CRAFTING_WOOD = 0x303
IMAGE_CATEGORY_COOKING = 0x401
IMAGE_CATEGORY_FIREMAKING = 0x501
IMAGE_CATEGORY_CONSTRUCTION = 0x601
IMAGE_CATEGORY_AGILITY_SHORTCUT = 0x701
IMAGE_CATEGORY_AGILITY_OBSTACLE = 0x702
IMAGE_CATEGORY_MINING = 0x801
IMAGE_CATEGORY_FARMING_PLANTING = 0x901
IMAGE_CATEGORY_FARMING_HARVEST = 0x902
IMAGE_CATEGORY_FISHING = 0xa01
IMAGE_CATEGORY_WOODCUTTING = 0xb01
IMAGE_CATEGORY_HUSBANDRY = 0xc01

### SKILLING IMAGE ID NUMBERS ###
IMAGE_ID_SMITHING_SMELTING_1 = 0x10001
IMAGE_ID_SMITHING_SMELTING_2 = 0x10002
IMAGE_ID_HERBLORE_HARVEST_1 = 0x20001
IMAGE_ID_HERBLORE_HARVEST_2 = 0x20001
IMAGE_ID_MINING_1 = 0x80001
IMAGE_ID_MINING_2 = 0x80002
IMAGE_ID_WOODCUTTING_1 = 0xb0001
IMAGE_ID_WOODCUTTING_2 = 0xb0002

# Maps skilling image category IDs
# to a list of image_ids that represent the sequence of sprite images
# to blit when the protagonist performs the particular skill.
# If the list contains in an index, then that represents
# blitting the previous standing overworld image for the Protagonist.
# An empty list means just use the previous standing overworld image.
SKILLING_IMAGE_ID_MAPPING = {
    IMAGE_CATEGORY_SMITHING_SMELTING: [
        IMAGE_ID_SMITHING_SMELTING_1,
        IMAGE_ID_SMITHING_SMELTING_2,
        IMAGE_ID_SMITHING_SMELTING_1,
        None,
    ],
    IMAGE_CATEGORY_SMITHING_ANVIL: [],
    IMAGE_CATEGORY_HERBLORE_HARVEST: [],
    IMAGE_CATEGORY_HERBLORE_POTION: [],
    IMAGE_CATEGORY_CRAFTING_CLOTHES: [],
    IMAGE_CATEGORY_CRAFTING_GEMS: [],
    IMAGE_CATEGORY_CRAFTING_WOOD: [],
    IMAGE_CATEGORY_COOKING: [],
    IMAGE_CATEGORY_FIREMAKING: [],
    IMAGE_CATEGORY_CONSTRUCTION: [],
    IMAGE_CATEGORY_AGILITY_SHORTCUT: [],
    IMAGE_CATEGORY_AGILITY_OBSTACLE: [],
    IMAGE_CATEGORY_MINING: [
        IMAGE_ID_MINING_1,
        IMAGE_ID_MINING_2,
        IMAGE_ID_MINING_1,
        None,
    ],
    IMAGE_CATEGORY_FARMING_PLANTING: [],
    IMAGE_CATEGORY_FARMING_HARVEST: [],
    IMAGE_CATEGORY_FISHING: [],
    IMAGE_CATEGORY_WOODCUTTING: [
        IMAGE_ID_WOODCUTTING_1,
        IMAGE_ID_WOODCUTTING_2,
        IMAGE_ID_WOODCUTTING_1,
        None,
    ],
    IMAGE_CATEGORY_HUSBANDRY: [],
}