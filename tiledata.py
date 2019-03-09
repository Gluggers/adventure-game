import imagepaths

### TRANSPORTATION FLAGS ###
NO_TRANSPORT_F = 0x0
WALKABLE_F = 0x1
CANOEABLE_F = 0x2
SAILABLE_F = 0x4
FLYABLE_F = 0x8

DEFAULT_TRANSPORTATION = (WALKABLE_F | FLYABLE_F)

### TILE ID NUMBERS ###
TILE_DEFAULT_ID = 1
TILE_GRASS_1_ID = 100
TILE_GRASS_2_ID = 101
TILE_GRASS_PLAIN_ID = 102
TILE_GRASS_FLOWERS_ID = 103
TILE_WATER_NORMAL_1_ID = 200
TILE_WATER_NORMAL_2_ID = 201
TILE_WATER_NORMAL_3_ID = 202
TILE_SAND_ID = 300

### TILE FACTORY DATA ###
TILE_IMAGE_PATH_FIELD = 1
TILE_ALLOWED_TRANSPORT_FIELD = 2

TILE_DATA = {
    TILE_DEFAULT_ID: {
        TILE_IMAGE_PATH_FIELD: imagepaths.TILE_DEFAULT_PATH,
        TILE_ALLOWED_TRANSPORT_FIELD: NO_TRANSPORT_F,
    },
    TILE_GRASS_1_ID: {
        TILE_IMAGE_PATH_FIELD: imagepaths.TILE_GRASS_1_PATH,
    },
    TILE_GRASS_2_ID: {
        TILE_IMAGE_PATH_FIELD: imagepaths.TILE_GRASS_2_PATH,
    },
    TILE_GRASS_PLAIN_ID: {
        TILE_IMAGE_PATH_FIELD: imagepaths.TILE_GRASS_PLAIN_PATH,
    },
    TILE_GRASS_FLOWERS_ID: {
        TILE_IMAGE_PATH_FIELD: imagepaths.TILE_GRASS_FLOWERS_PATH,
    },
    TILE_WATER_NORMAL_1_ID: {
        TILE_IMAGE_PATH_FIELD: imagepaths.TILE_WATER_NORMAL_1_PATH,
        TILE_ALLOWED_TRANSPORT_FIELD: (FLYABLE_F | SAILABLE_F),
    },
    TILE_WATER_NORMAL_2_ID: {
        TILE_IMAGE_PATH_FIELD: imagepaths.TILE_WATER_NORMAL_2_PATH,
        TILE_ALLOWED_TRANSPORT_FIELD: (FLYABLE_F | SAILABLE_F),
    },
    TILE_WATER_NORMAL_3_ID: {
        TILE_IMAGE_PATH_FIELD: imagepaths.TILE_WATER_NORMAL_3_PATH,
        TILE_ALLOWED_TRANSPORT_FIELD: (FLYABLE_F | SAILABLE_F),
    },
    TILE_SAND_ID: {
        TILE_IMAGE_PATH_FIELD: imagepaths.TILE_SAND_PATH,
    },
}
