# -*- coding: utf-8 -*-
"""This module contains constants and data for Tile objects."""

import imagepaths

### TRANSPORTATION FLAGS ###
NO_TRANSPORT_F = 0x0  # To indicate no type of transportation.
WALKABLE_F = 0x1  # For walking.
CANOEABLE_F = 0x2  # For canoeing.
SAILABLE_F = 0x4  # For sailing.
FLYABLE_F = 0x8  # For flying.

# By default, Tiles can be walked on or flown on.
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
TILE_WATER_SHALLOW_1_ID = 210
TILE_SAND_ID = 300

### TILE DATA FOR CREATING TILES ###
TILE_IMAGE_PATHS_FIELD = 1
TILE_ALLOWED_TRANSPORT_FIELD = 2
TILE_IMAGE_SEQUENCE_DURATION_FIELD = 3

# This dict contains Tile object values used to create Tile objects.
# To create a new Tile object, add a new Tile ID and enter
# the field values in the dict.
TILE_DATA = {
    TILE_DEFAULT_ID: {
        TILE_IMAGE_PATHS_FIELD: [imagepaths.TILE_DEFAULT_PATH],
        TILE_ALLOWED_TRANSPORT_FIELD: NO_TRANSPORT_F,
        TILE_IMAGE_SEQUENCE_DURATION_FIELD: None,
    },
    TILE_GRASS_1_ID: {
        TILE_IMAGE_PATHS_FIELD: [imagepaths.TILE_GRASS_1_PATH],
    },
    TILE_GRASS_2_ID: {
        TILE_IMAGE_PATHS_FIELD: [imagepaths.TILE_GRASS_2_PATH],
    },
    TILE_GRASS_PLAIN_ID: {
        TILE_IMAGE_PATHS_FIELD: [imagepaths.TILE_GRASS_PLAIN_PATH],
    },
    TILE_GRASS_FLOWERS_ID: {
        TILE_IMAGE_PATHS_FIELD: [
            imagepaths.TILE_GRASS_FLOWERS_1_PATH,
            imagepaths.TILE_GRASS_FLOWERS_2_PATH,
        ],
        TILE_IMAGE_SEQUENCE_DURATION_FIELD: 1500,
    },
    TILE_WATER_NORMAL_1_ID: {
        TILE_IMAGE_PATHS_FIELD: [imagepaths.TILE_WATER_NORMAL_1_PATH],
        TILE_ALLOWED_TRANSPORT_FIELD: (FLYABLE_F | SAILABLE_F),
    },
    TILE_WATER_NORMAL_2_ID: {
        TILE_IMAGE_PATHS_FIELD: [imagepaths.TILE_WATER_NORMAL_2_PATH],
        TILE_ALLOWED_TRANSPORT_FIELD: (FLYABLE_F | SAILABLE_F),
    },
    TILE_WATER_NORMAL_3_ID: {
        TILE_IMAGE_PATHS_FIELD: [imagepaths.TILE_WATER_NORMAL_3_PATH],
        TILE_ALLOWED_TRANSPORT_FIELD: (FLYABLE_F | SAILABLE_F),
    },
    TILE_WATER_SHALLOW_1_ID: {
        TILE_IMAGE_PATHS_FIELD: [imagepaths.TILE_WATER_SHALLOW_1_PATH],
        TILE_ALLOWED_TRANSPORT_FIELD: (FLYABLE_F),
    },
    TILE_SAND_ID: {
        TILE_IMAGE_PATHS_FIELD: [imagepaths.TILE_SAND_PATH],
    },
}
