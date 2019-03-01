import tile
import pygame

### Display IDs ###
OW_TOP_DISPLAY_ID = 0x1
OW_SIDE_MENU_DISPLAY_ID = 0x2
OW_BOTTOM_TEXT_DISPLAY_ID = 0x3

# Overworld viewing constants.
OW_VIEWING_NUM_TILES_HORIZONTAL = 21
OW_VIEWING_NUM_TILES_VERTICAL = 15

OW_VIEWING_WIDTH = tile.TILE_SIZE * OW_VIEWING_NUM_TILES_HORIZONTAL
OW_VIEWING_HEIGHT = tile.TILE_SIZE * OW_VIEWING_NUM_TILES_VERTICAL

# viewing space at top of game display. This display will
# show things like current health, money, level, et
OW_TOP_DISPLAY_HEIGHT = tile.TILE_SIZE
OW_TOP_DISPLAY_WIDTH = OW_VIEWING_WIDTH

# Viewing space for bottom text box.
OW_BOTTOM_TEXT_DISPLAY_WIDTH = tile.TILE_SIZE * (OW_VIEWING_NUM_TILES_HORIZONTAL - 1)
OW_BOTTOM_TEXT_DISPLAY_HEIGHT = tile.TILE_SIZE * int(OW_VIEWING_NUM_TILES_VERTICAL / 4)

# main display width is same as overworld viewing width
# main display height is overworld viewing height + space for
# the top display
MAIN_DISPLAY_WIDTH = OW_VIEWING_WIDTH
MAIN_DISPLAY_HEIGHT = OW_VIEWING_HEIGHT + OW_TOP_DISPLAY_HEIGHT

# dimensions for side menu to launch during overworld
OW_SIDE_MENU_WIDTH = 220
OW_SIDE_MENU_HEIGHT = OW_VIEWING_HEIGHT - (tile.TILE_SIZE*2)

# location constants
MAIN_DISPLAY_LOCATION = (0,0)
TOP_DISPLAY_LOCATION = (0,0)
OW_VIEWING_LOCATION = (0, OW_TOP_DISPLAY_HEIGHT)
OW_SIDE_MENU_LOCATION = (                                               \
    MAIN_DISPLAY_WIDTH - OW_SIDE_MENU_WIDTH,                            \
    OW_TOP_DISPLAY_HEIGHT + tile.TILE_SIZE                                  \
)

CENTER_OW_TILE_TOP_LEFT = (                                     \
    int(OW_VIEWING_NUM_TILES_HORIZONTAL / 2) * tile.TILE_SIZE,  \
    int(OW_VIEWING_NUM_TILES_VERTICAL / 2)*tile.TILE_SIZE +     \
        OW_TOP_DISPLAY_HEIGHT                                      \
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
    MAIN_DISPLAY_LOCATION,
    (MAIN_DISPLAY_WIDTH, MAIN_DISPLAY_HEIGHT)
)

OW_VIEWING_RECT = pygame.Rect(
    OW_VIEWING_LOCATION,
    (OW_VIEWING_WIDTH, OW_VIEWING_HEIGHT)
)

OW_TOP_DISPLAY_RECT = pygame.Rect(
    TOP_DISPLAY_LOCATION,
    (OW_TOP_DISPLAY_WIDTH, OW_TOP_DISPLAY_HEIGHT)
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
COLOR_WHITE = (255,255,255)
COLOR_BLACK = (0,0,0)
