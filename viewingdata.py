# -*- coding: utf-8 -*-
"""This module contains constants for the viewing module."""

import pygame
import tile
import language

### DISPLAY ID NUMBERS ###
OW_TOP_HEALTH_DISPLAY_ID = 0x1
OW_SIDE_MENU_DISPLAY_ID = 0x2
OW_BOTTOM_TEXT_DISPLAY_ID = 0x3
OW_TOP_DISPLAY_ID = 0x10
INVENTORY_TOP_DISPLAY_ID = 0x20
INVENTORY_ITEM_LISTING_DISPLAY_ID = 0x21
INVENTORY_ITEM_NAME_DISPLAY_ID = 0x22
INVENTORY_ITEM_ENLARGED_DISPLAY_ID = 0x23
INVENTORY_ITEM_QUANTITY_DISPLAY_ID = 0x24
INVENTORY_ITEM_DESCRIPTION_DISPLAY_ID = 0x25
INVENTORY_ITEM_OPTIONS_DISPLAY_ID = 0x26
INVENTORY_BOTTOM_TEXT_DISPLAY_ID = 0x27

# Overworld viewing constants.
OW_VIEWING_NUM_TILES_HORIZONTAL = 23
OW_VIEWING_NUM_TILES_VERTICAL = 17

OW_VIEWING_WIDTH = tile.TILE_SIZE * OW_VIEWING_NUM_TILES_HORIZONTAL # 672
OW_VIEWING_HEIGHT = tile.TILE_SIZE * OW_VIEWING_NUM_TILES_VERTICAL # 480

# viewing space at top of game display. This display will
# show things like current health, money, level, et
OW_TOP_DISPLAY_HEIGHT = int(1.5 * tile.TILE_SIZE) # 48
OW_TOP_DISPLAY_WIDTH = OW_VIEWING_WIDTH # 672
OW_TOP_HEALTH_DISPLAY_HEIGHT = 56
OW_TOP_HEALTH_DISPLAY_WIDTH = 264

# Viewing space for bottom text box.
#OW_BOTTOM_TEXT_DISPLAY_WIDTH = tile.TILE_SIZE * (OW_VIEWING_NUM_TILES_HORIZONTAL - 1) # 640
#OW_BOTTOM_TEXT_DISPLAY_HEIGHT = tile.TILE_SIZE * 3 # 96
OW_BOTTOM_TEXT_DISPLAY_WIDTH = 640
OW_BOTTOM_TEXT_DISPLAY_HEIGHT = 96

# Main display width is same as overworld viewing width.
# Main display height is overworld viewing height.
MAIN_DISPLAY_WIDTH = OW_VIEWING_WIDTH # 672
MAIN_DISPLAY_HEIGHT = OW_VIEWING_HEIGHT # 480

# Dimensions for side menu to launch during overworld.
OW_SIDE_MENU_WIDTH = 220
OW_SIDE_MENU_HEIGHT = 380

INVENTORY_TOP_DISPLAY_HEIGHT = 36
INVENTORY_TOP_DISPLAY_WIDTH = 160

# Location constants.
MAIN_DISPLAY_TOP_LEFT = (0, 0)
TOP_DISPLAY_LOCATION = (0, 0)
OW_TOP_HEALTH_DISPLAY_LOCATION = (
    int(tile.TILE_SIZE / 2),
    int(tile.TILE_SIZE / 2),
)
INVENTORY_TOP_DISPLAY_LOCATION = (
    6,
    10,
)
INVENTORY_ITEM_DETAILS_LOCATION = (
    int(2 * MAIN_DISPLAY_WIDTH / 3), # 448
    #int(0.6 * MAIN_DISPLAY_WIDTH),
    0,
)

OW_VIEWING_TOP_LEFT = MAIN_DISPLAY_TOP_LEFT
OW_SIDE_MENU_LOCATION = (
    MAIN_DISPLAY_WIDTH - OW_SIDE_MENU_WIDTH - (tile.TILE_SIZE),
    tile.TILE_SIZE
)

CENTER_OW_TILE_TOP_LEFT = (
    int(OW_VIEWING_NUM_TILES_HORIZONTAL / 2) * tile.TILE_SIZE,
    int(OW_VIEWING_NUM_TILES_VERTICAL / 2) * tile.TILE_SIZE
)

CENTER_OW_TILE_BOTTOM_LEFT = (                      \
    CENTER_OW_TILE_TOP_LEFT[0],                     \
    CENTER_OW_TILE_TOP_LEFT[1] + tile.TILE_SIZE     \
)

# Have the bottom text display bottom edge be a little above the
# bottom edge of the display.
OW_BOTTOM_TEXT_DISPLAY_TOP_LEFT = (
    int(OW_VIEWING_WIDTH / 2) - int(OW_BOTTOM_TEXT_DISPLAY_WIDTH / 2),
    MAIN_DISPLAY_HEIGHT - int(tile.TILE_SIZE / 2) - OW_BOTTOM_TEXT_DISPLAY_HEIGHT
)

### Viewing Rects ###
MAIN_DISPLAY_RECT = pygame.Rect(
    MAIN_DISPLAY_TOP_LEFT,
    (MAIN_DISPLAY_WIDTH, MAIN_DISPLAY_HEIGHT)
)

OW_VIEWING_RECT = pygame.Rect(
    OW_VIEWING_TOP_LEFT,
    (OW_VIEWING_WIDTH, OW_VIEWING_HEIGHT)
)

OW_TOP_DISPLAY_RECT = pygame.Rect(
    TOP_DISPLAY_LOCATION,
    (OW_TOP_DISPLAY_WIDTH, OW_TOP_DISPLAY_HEIGHT)
)

OW_TOP_HEALTH_DISPLAY_RECT = pygame.Rect(
    OW_TOP_HEALTH_DISPLAY_LOCATION,
    (OW_TOP_HEALTH_DISPLAY_WIDTH, OW_TOP_HEALTH_DISPLAY_HEIGHT)
)

OW_SIDE_MENU_RECT = pygame.Rect(
    OW_SIDE_MENU_LOCATION,
    (OW_SIDE_MENU_WIDTH, OW_SIDE_MENU_HEIGHT)
)

OW_BOTTOM_TEXT_DISPLAY_RECT = pygame.Rect(
    OW_BOTTOM_TEXT_DISPLAY_TOP_LEFT[0],
    OW_BOTTOM_TEXT_DISPLAY_TOP_LEFT[1],
    OW_BOTTOM_TEXT_DISPLAY_WIDTH,
    OW_BOTTOM_TEXT_DISPLAY_HEIGHT
)

INVENTORY_BASIC_VIEWING_RECT = pygame.Rect(
    MAIN_DISPLAY_TOP_LEFT,
    (MAIN_DISPLAY_WIDTH, MAIN_DISPLAY_HEIGHT)
)

TEXT_ADVANCE_KEYS = set([
    pygame.K_SPACE,
    pygame.K_RETURN,
    pygame.K_BACKSPACE,
    pygame.K_TAB,
    pygame.K_ESCAPE,
    pygame.K_e,
    pygame.K_RIGHT,
])

MENU_OPTION_SELECT_KEYS = set([
    pygame.K_SPACE,
    pygame.K_RETURN,
    pygame.K_RIGHT,
    pygame.K_TAB,
])

MENU_OPTION_EXIT_KEYS = set([
    pygame.K_BACKSPACE,
    pygame.K_ESCAPE,
])

### COLOR CONSTANTS ###
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_BLUE_TEXT = (0x05, 0x03, 0x47)

INPUT_TEXT_COLOR_LIST = [COLOR_BLACK, COLOR_BLUE_TEXT]

HEALTH_TEXT_PREFIX_INFO = {
    language.LANG_ENGLISH: "HEALTH: ",
    language.LANG_ESPANOL: "SALUD: ",
}

### VIEWING DELAY CONSTANTS ###

# Number of milliseconds to wait in between each
# text display.
BOTTOM_TEXT_DELAY_MS = 500
DEFAULT_ADVANCE_DELAY_MS = 1500
INITIAL_INPUT_DELAY_MS = 300

# Number of milliseconds to wait when loading menu.
DEFAULT_MENU_LOAD_DELAY_MS = 750

# Number of milliseconds to wait after changing selected options.
DEFAULT_MENU_OPTION_SWITCH_DELAY_MS = 750

### VIEWING DISPLAY PADDINGS ###
OW_SIDE_MENU_HORIZONTAL_PADDING = 40
OW_SIDE_MENU_VERTICAL_PADDING = 20

TOP_DISPLAY_HORIZONTAL_PADDING = 20

TEXT_DISPLAY_HORIZONTAL_PADDING = 28
TEXT_DISPLAY_VERTICAL_PADDING = 24

ITEM_LISTING_HORIZONTAL_PADDING = 25
ITEM_LISTING_VERTICAL_PADDING = 25

GRID_VIEWING_IN_BETWEEN_PADDING = 0

# Max length for a user input string.
MAX_INPUT_STR_LEN = 15

### MAPPING BETWEEN PYGAME KEYS AND STRING VALUES ###
PYGAME_KEY_STR_MAPPING = {
    pygame.K_a: ("a", "A"),
    pygame.K_b: ("b", "B"),
    pygame.K_c: ("c", "C"),
    pygame.K_d: ("d", "D"),
    pygame.K_e: ("e", "E"),
    pygame.K_f: ("f", "F"),
    pygame.K_g: ("g", "G"),
    pygame.K_h: ("h", "H"),
    pygame.K_i: ("i", "I"),
    pygame.K_j: ("j", "J"),
    pygame.K_k: ("k", "K"),
    pygame.K_l: ("l", "L"),
    pygame.K_m: ("m", "M"),
    pygame.K_n: ("n", "N"),
    pygame.K_o: ("o", "O"),
    pygame.K_p: ("p", "P"),
    pygame.K_q: ("q", "Q"),
    pygame.K_r: ("r", "R"),
    pygame.K_s: ("s", "S"),
    pygame.K_t: ("t", "T"),
    pygame.K_u: ("u", "U"),
    pygame.K_v: ("v", "V"),
    pygame.K_w: ("w", "W"),
    pygame.K_x: ("x", "X"),
    pygame.K_y: ("y", "Y"),
    pygame.K_z: ("z", "Z"),
    pygame.K_1: ("1", "!"),
    pygame.K_2: ("2", "@"),
    pygame.K_3: ("3", "#"),
    pygame.K_4: ("4", "$"),
    pygame.K_5: ("5", "%"),
    pygame.K_6: ("6", "^"),
    pygame.K_7: ("7", "&"),
    pygame.K_8: ("8", "*"),
    pygame.K_9: ("9", "("),
    pygame.K_0: ("0", ")"),
    pygame.K_KP0: ("0", "0"),
    pygame.K_KP1: ("1", "1"),
    pygame.K_KP2: ("2", "2"),
    pygame.K_KP3: ("3", "3"),
    pygame.K_KP4: ("4", "4"),
    pygame.K_KP5: ("5", "5"),
    pygame.K_KP6: ("6", "6"),
    pygame.K_KP7: ("7", "7"),
    pygame.K_KP8: ("8", "8"),
    pygame.K_KP9: ("9", "9"),
    pygame.K_SPACE: (" ", " "),
}

DEFAULT_ALLOWED_INPUT_STR_REGEX = "^[0-9a-zA-Z ]+$"
#ALLOWED_NUMBER_INPUT_STR_REGEX = "^[0-9]+[kKmMbB]?$"
ALLOWED_NUMBER_INPUT_STR_REGEX = "^[0-9]+$"

def get_pygame_key_str(key_id, shift_on=False):
    """Returns the character string for the given key ID.

    Args:
        key_id: pygame key ID constant for the pressed key.
        shift_on: boolean that indicates whether or not the shift key
            was held when key_id was pressed. shift_on is used to
            get capital letters and certain special characters.

    Returns:
        String representation of the pressed key, depending on
        whether or not the shift button was pressed, as well.
    """
    ret_val = None

    key_info = PYGAME_KEY_STR_MAPPING.get(key_id, None)

    if key_info:
        if shift_on:
            ret_val = key_info[1]
        else:
            ret_val = key_info[0]
    return ret_val
