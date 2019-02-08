import tile

# overworld display constants
OW_DISPLAY_NUM_TILES_HORIZONTAL = 21
OW_DISPLAY_NUM_TILES_VERTICAL = 15

OW_VIEWING_WIDTH = tile.TILE_SIZE * OW_DISPLAY_NUM_TILES_HORIZONTAL
OW_VIEWING_HEIGHT = tile.TILE_SIZE * OW_DISPLAY_NUM_TILES_VERTICAL

# viewing space at top of game display. This display will
# show things like current health, money, level, et
TOP_DISPLAY_HEIGHT = tile.TILE_SIZE
TOP_DISPLAY_WIDTH = OW_VIEWING_WIDTH

# main display width is same as overworld viewing width
# main display height is overworld viewing height + space for
# the top display
MAIN_DISPLAY_WIDTH = OW_VIEWING_WIDTH
MAIN_DISPLAY_HEIGHT = OW_VIEWING_HEIGHT + TOP_DISPLAY_HEIGHT

# dimensions for side menu to launch during overworld
OW_SIDE_MENU_WIDTH = 150
OW_SIDE_MENU_HEIGHT = OW_VIEWING_HEIGHT - (tile.TILE_SIZE*2)

# location constants
MAIN_DISPLAY_LOCATION = (0,0)
TOP_DISPLAY_LOCATION = (0,0)
OW_VIEWING_LOCATION = (0, TOP_DISPLAY_HEIGHT)
OW_SIDE_MENU_LOCATION = (                                               \
    MAIN_DISPLAY_WIDTH - OW_SIDE_MENU_WIDTH,                            \
    TOP_DISPLAY_HEIGHT + tile.TILE_SIZE                                  \
)
CENTER_OW_TILE_TOP_LEFT = (                                     \
    int(OW_DISPLAY_NUM_TILES_HORIZONTAL / 2) * tile.TILE_SIZE,  \
    int(OW_DISPLAY_NUM_TILES_VERTICAL / 2)*tile.TILE_SIZE +     \
        TOP_DISPLAY_HEIGHT                                      \
)

CENTER_OW_TILE_BOTTOM_LEFT = (                      \
    CENTER_OW_TILE_TOP_LEFT[0],                     \
    CENTER_OW_TILE_TOP_LEFT[1] + tile.TILE_SIZE     \
)

### COLOR CONSTANTS ###
COLOR_WHITE = (255,255,255)
COLOR_BLACK = (0,0,0)
