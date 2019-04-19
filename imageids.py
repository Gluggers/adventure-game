import directions

### IMAGE ID NUMBERS ###

### DEFAULT IMAGE SEQUENCE ID ###
SEQUENCE_ID_DEFAULT = 1

ICON_SEQUENCE_ID = 10
OBJ_SPRITE_SEQUENCE_ID = 20

SEQUENCE_ID_FACE_NORTH = 100
SEQUENCE_ID_FACE_EAST = 101
SEQUENCE_ID_FACE_SOUTH = 102
SEQUENCE_ID_FACE_WEST = 103
SEQUENCE_ID_WALK_NORTH = 110
SEQUENCE_ID_WALK_EAST = 120
SEQUENCE_ID_WALK_SOUTH = 130
SEQUENCE_ID_WALK_WEST = 140

### BATTLE MODE IMAGE TYPE ID NUMBERS ###
BATTLE_SEQUENCE_ID_DEFAULT = 200
BATTLE_SEQUENCE_ID_STAND = 201
BATTLE_SEQUENCE_ID_ATTACK = 202
BATTLE_SEQUENCE_ID_FAINTED = 203

### SKILLING IMAGE ID NUMBERS ###
SEQUENCE_ID_SMITHING_SMELTING_1 = 1001
SEQUENCE_ID_SMITHING_SMELTING_2 = 1002
SEQUENCE_ID_HERBLORE_HARVEST_1 = 1101
SEQUENCE_ID_HERBLORE_HARVEST_2 = 1102
SEQUENCE_ID_MINING_1 = 1801
SEQUENCE_ID_MINING_2 = 1802
SEQUENCE_ID_WOODCUTTING_1 = 2101
SEQUENCE_ID_WOODCUTTING_2 = 2102

### SKILLING IMAGE CATEGORY IDS ###
SEQUENCE_ID_SMITHING_SMELTING = 101
SEQUENCE_ID_SMITHING_ANVIL = 102
SEQUENCE_ID_HERBLORE_HARVEST = 201
SEQUENCE_ID_HERBLORE_POTION = 202
SEQUENCE_ID_CRAFTING_CLOTHES = 301
SEQUENCE_ID_CRAFTING_GEMS = 302
SEQUENCE_ID_CRAFTING_WOOD = 303
SEQUENCE_ID_COOKING = 401
SEQUENCE_ID_FIREMAKING = 501
SEQUENCE_ID_CONSTRUCTION = 601
SEQUENCE_ID_AGILITY_SHORTCUT = 701
SEQUENCE_ID_AGILITY_OBSTACLE = 702
SEQUENCE_ID_MINING = 801
SEQUENCE_ID_FARMING_PLANTING = 901
SEQUENCE_ID_FARMING_HARVEST = 902
SEQUENCE_ID_FISHING = 1001
SEQUENCE_ID_WOODCUTTING = 1101
SEQUENCE_ID_HUSBANDRY = 1201

# Maps entity animation IDs to a dict that maps direction IDs
# to a list of image_ids that represent the sequence of sprite images
# to blit when the protagonist performs the particular skill
# when facing the particular direction.
# If the list contains in an index, then that represents
# blitting the previous standing overworld image for the Protagonist.
# An empty list means just use the previous standing overworld image.
ENTITY_SEQUENCE_ID_MAPPING = {
    SEQUENCE_ID_WALK: {
        directions.DIR_NORTH: [
            SEQUENCE_ID_WALK1_NORTH,
            SEQUENCE_ID_FACE_NORTH,
            SEQUENCE_ID_WALK2_NORTH,
            SEQUENCE_ID_FACE_NORTH,
        ],
        directions.DIR_SOUTH: [
            SEQUENCE_ID_WALK1_SOUTH,
            SEQUENCE_ID_FACE_SOUTH,
            SEQUENCE_ID_WALK2_SOUTH,
            SEQUENCE_ID_FACE_SOUTH,
        ],
        directions.DIR_EAST: [
            SEQUENCE_ID_WALK1_EAST,
            SEQUENCE_ID_FACE_EAST,
            SEQUENCE_ID_WALK2_EAST,
            SEQUENCE_ID_FACE_EAST,
        ],
        directions.DIR_WEST: [
            SEQUENCE_ID_WALK1_WEST,
            SEQUENCE_ID_FACE_WEST,
            SEQUENCE_ID_WALK2_WEST,
            SEQUENCE_ID_FACE_WEST,
        ],
    },
}

def get_direction_image_id(direction):
    """Returns image ID for the sprite for facing the specified direction.

    Args:
        direction: direction ID for which to retrieve the image ID.
    """
    image_id = None

    if direction == directions.DIR_NORTH:
        image_id = SEQUENCE_ID_FACE_NORTH
    elif direction == directions.DIR_EAST:
        image_id = SEQUENCE_ID_FACE_EAST
    elif direction == directions.DIR_SOUTH:
        image_id = SEQUENCE_ID_FACE_SOUTH
    elif direction == directions.DIR_WEST:
        image_id = SEQUENCE_ID_FACE_WEST

    return image_id

def get_entity_walk_image_ids(direction):
    """Returns image ID list for the walk animation in the specified direction.

    Args:
        direction: direction ID for which to retrieve the image ID list.
    """
    return ENTITY_SEQUENCE_ID_MAPPING.get(
        SEQUENCE_ID_WALK,
        {},
    ).get(
        direction,
        None
    )
