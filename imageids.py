import directions

### IMAGE ID NUMBERS ###
ICON_IMAGE_ID = 10

### DEFAULT IMAGE SEQUENCE ID ###
SEQUENCE_ID_DEFAULT = 1
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


def get_direction_sequence_id(direction):
    """Returns image sequence ID for the sprite for facing the specified
    direction.

    Args:
        direction: direction ID for which to retrieve the image sequence ID.
    """
    sequence_id = None

    if direction == directions.DIR_NORTH:
        sequence_id = SEQUENCE_ID_FACE_NORTH
    elif direction == directions.DIR_EAST:
        sequence_id = SEQUENCE_ID_FACE_EAST
    elif direction == directions.DIR_SOUTH:
        sequence_id = SEQUENCE_ID_FACE_SOUTH
    elif direction == directions.DIR_WEST:
        sequence_id = SEQUENCE_ID_FACE_WEST

    return sequence_id
