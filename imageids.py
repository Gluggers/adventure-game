import directions

### IMAGE ID NUMBERS ###

### DEFAULT IMAGE ID ###
IMAGE_ID_DEFAULT = 1

ICON_IMAGE_ID = 10
OBJ_SPRITE_IMAGE_ID = 20

IMAGE_ID_FACE_NORTH = 100
IMAGE_ID_FACE_EAST = 101
IMAGE_ID_FACE_SOUTH = 102
IMAGE_ID_FACE_WEST = 103
IMAGE_ID_WALK1_NORTH = 110
IMAGE_ID_WALK1_EAST = 120
IMAGE_ID_WALK1_SOUTH = 130
IMAGE_ID_WALK1_WEST = 140
IMAGE_ID_WALK2_NORTH = 111
IMAGE_ID_WALK2_EAST = 121
IMAGE_ID_WALK2_SOUTH = 131
IMAGE_ID_WALK2_WEST = 141

### BATTLE MODE IMAGE TYPE ID NUMBERS ###
BATTLE_IMAGE_ID_DEFAULT = 200
BATTLE_IMAGE_ID_STAND = 201
BATTLE_IMAGE_ID_ATTACK = 202
BATTLE_IMAGE_ID_FAINTED = 203

### SKILLING IMAGE ID NUMBERS ###
IMAGE_ID_SMITHING_SMELTING_1 = 1001
IMAGE_ID_SMITHING_SMELTING_2 = 1002
IMAGE_ID_HERBLORE_HARVEST_1 = 1101
IMAGE_ID_HERBLORE_HARVEST_2 = 1102
IMAGE_ID_MINING_1 = 1801
IMAGE_ID_MINING_2 = 1802
IMAGE_ID_WOODCUTTING_1 = 2101
IMAGE_ID_WOODCUTTING_2 = 2102

### SKILLING IMAGE CATEGORY IDS ###
ANIMATION_ID_WALK = 10
ANIMATION_ID_SMITHING_SMELTING = 101
ANIMATION_ID_SMITHING_ANVIL = 102
ANIMATION_ID_HERBLORE_HARVEST = 201
ANIMATION_ID_HERBLORE_POTION = 202
ANIMATION_ID_CRAFTING_CLOTHES = 301
ANIMATION_ID_CRAFTING_GEMS = 302
ANIMATION_ID_CRAFTING_WOOD = 303
ANIMATION_ID_COOKING = 401
ANIMATION_ID_FIREMAKING = 501
ANIMATION_ID_CONSTRUCTION = 601
ANIMATION_ID_AGILITY_SHORTCUT = 701
ANIMATION_ID_AGILITY_OBSTACLE = 702
ANIMATION_ID_MINING = 801
ANIMATION_ID_FARMING_PLANTING = 901
ANIMATION_ID_FARMING_HARVEST = 902
ANIMATION_ID_FISHING = 1001
ANIMATION_ID_WOODCUTTING = 1101
ANIMATION_ID_HUSBANDRY = 1201

# Maps entity animation IDs to a dict that maps direction IDs
# to a list of image_ids that represent the sequence of sprite images
# to blit when the protagonist performs the particular skill
# when facing the particular direction.
# If the list contains in an index, then that represents
# blitting the previous standing overworld image for the Protagonist.
# An empty list means just use the previous standing overworld image.
ENTITY_ANIMATION_ID_MAPPING = {
    ANIMATION_ID_WALK: {
        directions.DIR_NORTH: [
            IMAGE_ID_WALK1_NORTH,
            IMAGE_ID_FACE_NORTH,
            IMAGE_ID_WALK2_NORTH,
            IMAGE_ID_FACE_NORTH,
        ],
        directions.DIR_SOUTH: [
            IMAGE_ID_WALK1_SOUTH,
            IMAGE_ID_FACE_SOUTH,
            IMAGE_ID_WALK2_SOUTH,
            IMAGE_ID_FACE_SOUTH,
        ],
        directions.DIR_EAST: [
            IMAGE_ID_WALK1_EAST,
            IMAGE_ID_FACE_EAST,
            IMAGE_ID_WALK2_EAST,
            IMAGE_ID_FACE_EAST,
        ],
        directions.DIR_WEST: [
            IMAGE_ID_WALK1_WEST,
            IMAGE_ID_FACE_WEST,
            IMAGE_ID_WALK2_WEST,
            IMAGE_ID_FACE_WEST,
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
        image_id = IMAGE_ID_FACE_NORTH
    elif direction == directions.DIR_EAST:
        image_id = IMAGE_ID_FACE_EAST
    elif direction == directions.DIR_SOUTH:
        image_id = IMAGE_ID_FACE_SOUTH
    elif direction == directions.DIR_WEST:
        image_id = IMAGE_ID_FACE_WEST

    return image_id

def get_entity_walk_image_ids(direction):
    """Returns image ID list for the walk animation in the specified direction.

    Args:
        direction: direction ID for which to retrieve the image ID list.
    """
    return ENTITY_ANIMATION_ID_MAPPING.get(
        ANIMATION_ID_WALK,
        {},
    ).get(
        direction,
        None
    )
