import pygame
import sys
import map
import logging

from pygame.locals import *

GAME_TITLE = "Adventure Game v0.1"

### DISPLAY AND WINDOW CONSTANTS ###

# overworld display constants
OW_DISPLAY_NUM_TILES_HORIZONTAL = 31
OW_DISPLAY_NUM_TILES_VERTICAL = 21
OW_SIDE_MENU_WIDTH = 150

### DIFFICULTY CONSTANTS ###
DIFFICULTY_NORMAL = 0x0
DIFFICULTY_HARD = 0x1

### TIME CONSTANTS ###
NUM_MS_SECOND = 1000
SINGLE_TILE_SCROLL_TIME = NUM_MS_SECOND

### COLOR CONSTANTS ###
WHITE_COLOR = (255,255,255)
BLACK_COLOR = (0,0,0)

logger = None

class Game():
    def __init__(self, game_name):
        if game_name and game_name:
            # will change as game progresses
            self.protagonist = None
            self.current_map = None

            # set game display dimensions

            # get number of tiles for overworld viewing
            self.ow_viewing_num_tiles_horizontal = OW_DISPLAY_NUM_TILES_HORIZONTAL
            self.ow_viewing_num_tiles_vertical = OW_DISPLAY_NUM_TILES_VERTICAL

            # get dimensions for overworld viewing
            self.ow_viewing_width = map.TILE_SIZE * self.ow_viewing_num_tiles_horizontal
            self.ow_viewing_height = map.TILE_SIZE * self.ow_viewing_num_tiles_vertical

            # viewing space at top of game display. This display will
            # show things like current health, money, level, etc
            self.top_display_height = map.TILE_SIZE
            self.top_display_width = self.ow_viewing_width

            # main display width is same as overworld viewing width
            # main display height is overworld viewing height + space for
            # the top display
            self.main_display_width = self.ow_viewing_width
            self.main_display_height = self.ow_viewing_height + self.top_display_height

            # dimensions for side menu to launch during overworld
            self.ow_side_menu_width = OW_SIDE_MENU_WIDTH
            self.ow_side_menu_height = self.ow_viewing_height

            # define center overworld tile pixel coordinates for displaying
            # protagonist
            self.center_ow_tile_pixel_location = (                          \
                int(OW_DISPLAY_NUM_TILES_HORIZONTAL / 2),                   \
                int(OW_DISPLAY_NUM_TILES_VERTICAL / 2) +                    \
                    self.top_display_height                                 \
                )
            # set locations
            self.main_display_location = (0, 0)
            self.top_display_location = (0, 0)
            self.ow_viewing_location = (0, self.top_display_height)
            self.ow_side_menu_location = (                                  \
                    self.main_display_width - self.ow_side_menu_width,      \
                    self.top_display_height                                 \
                )

            # create Rect objects for main display
            self.top_display_rect = pygame.Rect(                            \
                    self.top_display_location,                              \
                    (self.top_display_width, self.top_display_height)       \
                )
            self.ow_viewing_rect = pygame.Rect(                             \
                    self.ow_viewing_location,                               \
                    (self.ow_viewing_width, self.ow_viewing_height)         \
                )
            self.ow_side_menu_rect = pygame.Rect(                           \
                    self.ow_side_menu_location,                             \
                    (self.ow_side_menu_width, self.ow_side_menu_height)     \
                )
            self.main_display_rect = pygame.Rect(                           \
                    self.main_display_location,                             \
                    (self.main_display_width, self.main_display_height)     \
                )

            # create main display screen
            self.main_display_screen = pygame.display.set_mode(             \
                    (self.main_display_width, self.main_display_height)     \
                )

            pygame.display.set_caption(game_name)

            # set default difficulty to normal.
            self.difficulty = DIFFICULTY_NORMAL

    # returns the main display screen pygame.Surface object for the Game
    def get_main_display_surface(self):
        return self.main_display_screen

    # blits the top display view onto the main display screen
    # does not update the main display - caller will have to do that
    def blit_top_display(self):
        # TODO - add to this as we get more top display details
        pygame.draw.rect(self.get_main_display_surface(), WHITE_COLOR, \
            self.top_display_rect)

def main():
    logging.basicConfig(level=logging.DEBUG)
    global logger
    logger = logging.getLogger(__name__)

    # testing
    """
    testmap = [map.TILE_DEFAULT]*5
    testmap2 = [testmap, testmap, testmap]
    testmap3 = [[map.TILE_DEFAULT]*5,[map.TILE_DEFAULT]*5,[map.TILE_DEFAULT]*5]
    logger.debug('%s',sys.getsizeof(testmap))
    logger.info('%s', sys.getsizeof(testmap2))
    logger.info('%s', sys.getsizeof(testmap3))
    """

    # create game
    game = Game(GAME_TITLE)

    # load tiles
    map.build_tiles()

    # load maps
    map.build_maps()

    # clock
    clock = pygame.time.Clock()

    # blit a map and update display
    black = (0,0,0)
    game.main_display_screen.fill(black)

    game.current_map = map.REGION_GRASSLANDS_AREA_0_MAP
    logger.debug("Current map top left is {0}".format(game.current_map.top_left_position))
    game.current_map.set_top_left(game.ow_viewing_location)
    game.current_map.blit_onto_surface(game, game.ow_viewing_location)
    logger.debug("Current map top left is {0}".format(game.current_map.top_left_position))

    # blit top viewing area
    game.blit_top_display()

    # update screen
    pygame.display.update()

    pressed_right = False
    pressed_left = False
    pressed_up = False
    pressed_down = False
    scroll_wait_time = int(SINGLE_TILE_SCROLL_TIME / map.TILE_SIZE)

    # main loop for now
    while True:
        clock.tick(40)

        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif events.type == pygame.KEYDOWN:
                if events.key == pygame.K_RIGHT:
                    pressed_right = True
                    logger.debug("Right pressed down")
                elif events.key == pygame.K_LEFT:
                    pressed_left = True
                    logger.debug("Left pressed down")
                elif events.key == pygame.K_UP:
                    pressed_up = True
                    logger.debug("Up pressed down")
                elif events.key == pygame.K_DOWN:
                    pressed_down = True
                    logger.debug("Down pressed down")
            elif events.type == pygame.KEYUP:
                if events.key == pygame.K_RIGHT:
                    pressed_right = False
                    logger.debug("Right released")
                elif events.key == pygame.K_LEFT:
                    pressed_left = False
                    logger.debug("Left released")
                elif events.key == pygame.K_UP:
                    pressed_up = False
                    logger.debug("Up released")
                elif events.key == pygame.K_DOWN:
                    pressed_down = False
                    logger.debug("Down released")

        if pressed_up:
            # do character walking animation while scrolling map DOWN
            # TODO
            # scroll map down and update display. scroll one Tile length
            game.current_map.scroll_single_tile(game, map.DIR_SOUTH, scroll_wait_time)

            logger.debug("Scrolled up")
        elif pressed_right:
            # do character walking animation while scrolling map LEFT
            # TODO
            # scroll map left and update display. scroll one Tile length
            game.current_map.scroll_single_tile(game, map.DIR_WEST, scroll_wait_time)

            logger.debug("Scrolled right")
        elif pressed_down:
            # do character walking animation while scrolling map UP
            # TODO
            # scroll map up and update display. scroll one Tile length
            game.current_map.scroll_single_tile(game, map.DIR_NORTH, scroll_wait_time)

            logger.debug("Scrolled down")
        elif pressed_left:
            # do character walking animation while scrolling map RIGHT
            # TODO
            # scroll map right and update display. scroll one Tile length
            game.current_map.scroll_single_tile(game, map.DIR_EAST, scroll_wait_time)

            logger.debug("Scrolled left")


if __name__ == '__main__':
    pygame.init()
    main()
