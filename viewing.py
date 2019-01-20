import pygame
import logging
import map
import tile

# overworld display constants
OW_DISPLAY_NUM_TILES_HORIZONTAL = 31
OW_DISPLAY_NUM_TILES_VERTICAL = 21

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
CENTER_OW_TILE_PIXEL_LOCATION = (                               \
    int(OW_DISPLAY_NUM_TILES_HORIZONTAL / 2) * tile.TILE_SIZE,  \
    int(OW_DISPLAY_NUM_TILES_VERTICAL / 2)*tile.TILE_SIZE +     \
        TOP_DISPLAY_HEIGHT                                      \
)

### COLOR CONSTANTS ###
COLOR_WHITE = (255,255,255)
COLOR_BLACK = (0,0,0)

### TIME CONSTANTS ###
NUM_MS_SECOND = 1000
SINGLE_TILE_SCROLL_TIME_MS = int(NUM_MS_SECOND * 0.75)
SINGLE_PIXEL_SCROLL_TIME_MS = int(SINGLE_TILE_SCROLL_TIME_MS / tile.TILE_SIZE)

class Viewing():
    def __init__(self, main_display_surface, protagonist=None, curr_map=None):
        self.main_display_surface = main_display_surface
        self.protagonist = protagonist
        self.curr_map = curr_map

        # create Rect objects for main display
        self.top_display_rect = pygame.Rect(                            \
            TOP_DISPLAY_LOCATION,                                       \
            (TOP_DISPLAY_WIDTH, TOP_DISPLAY_HEIGHT)                     \
        )
        self.ow_viewing_rect = pygame.Rect(                             \
            OW_VIEWING_LOCATION,                                        \
            (OW_VIEWING_WIDTH, OW_VIEWING_HEIGHT)                       \
        )
        self.ow_side_menu_rect = pygame.Rect(                           \
            OW_SIDE_MENU_LOCATION,                                      \
            (OW_SIDE_MENU_WIDTH, OW_SIDE_MENU_HEIGHT)                   \
        )
        self.main_display_rect = pygame.Rect(                           \
            MAIN_DISPLAY_LOCATION,                                      \
            (MAIN_DISPLAY_WIDTH, MAIN_DISPLAY_HEIGHT)                     \
        )

    # blits the top display view onto the main display screen
    # does not update the main display - caller will have to do that
    def blit_top_display(self):
        if self.main_display_surface:
            # TODO - add to this as we get more top display details
            pygame.draw.rect(self.main_display_surface, COLOR_WHITE, \
                self.top_display_rect)

    # scroll map one Tile distance in the indicated direction.
    # updates main display with each new viewpoint
    # scroll_wait_time is the time (in milliseconds)
    def scroll_map_single_tile(self, direction):
        for i in range(tile.TILE_SIZE):
            # reset the surface screen to default to black for empty map
            # spaces
            self.set_viewing_screen_default(default_color=COLOR_BLACK)

            # scroll 1 pixel at a time
            self.curr_map.scroll(self.main_display_surface, direction, 1)

            # also blit the top view
            self.blit_top_display()

            # blit protagonist
            # TODO - have designated spot for protagonist?
            if self.protagonist:
                self.protagonist.blit_onto_surface(self.main_display_surface, \
                    CENTER_OW_TILE_PIXEL_LOCATION)

            # update main display
            pygame.display.update()

            # wait till next iteration
            pygame.time.wait(SINGLE_PIXEL_SCROLL_TIME_MS)

    # TODO document
    # DOES NOT update viewing - caller needs to do that by updating surface
    def set_viewing_screen_default(self, default_color=COLOR_BLACK):
        self.main_display_surface.fill(COLOR_BLACK)

    # TODO document
    # DOES NOT update viewing - caller needs to do that by updating surface
    def set_map_on_view(self, map_top_left=OW_VIEWING_LOCATION, default_color=COLOR_BLACK):
        self.set_viewing_screen_default(default_color)

        # set current map's top left position on display screen
        if self.curr_map:
            self.curr_map.top_left_position = map_top_left
            self.curr_map.blit_onto_surface(self.main_display_surface, map_top_left)
        else:
            logger.error("No map set for current viewing.")

        # don't forget top display
        self.blit_top_display()

    # TODO DOCUMENT
    def blit_interactive_object(self, obj_to_blit, image_type_id, pixel_location):
        if self and obj_to_blit and pixel_location:
            obj_to_blit.blit_onto_surface(self.main_display_surface, image_type_id, pixel_location)

    def blit_protagonist(self, protag_image):
        if self and protag_image:
            self.main_display_surface.blit(protag_image, CENTER_OW_TILE_PIXEL_LOCATION)

# return top left pixel coordinate for the map given the protagonist's
# tile coordinates
def get_centered_map_top_left_pixel(protag_tile_coordinate):
    top_left = (0,0)
    if protag_tile_coordinate:
        pixel_distance_horiz = CENTER_OW_TILE_PIXEL_LOCATION[0] - (protag_tile_coordinate[0] * tile.TILE_SIZE)
        pixel_distance_vert = CENTER_OW_TILE_PIXEL_LOCATION[1] - (protag_tile_coordinate[1] * tile.TILE_SIZE)

        top_left = (pixel_distance_horiz, pixel_distance_vert)


    return top_left

# set up logger
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
