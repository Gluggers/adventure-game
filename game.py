import pygame
import language
import logging
import viewing
import entity
import map
import interactive_obj
import sys

logger = None

### GAME CONSTANTS ###
GAME_TITLE = "Adventure Game v0.1"

### DIFFICULTY CONSTANTS ###
DIFFICULTY_NORMAL = 0x0
DIFFICULTY_HARD = 0x1


class Game():
    def __init__(self, game_name, language=language.DEFAULT_LANGUAGE):
        if game_name and game_name:
            # will change as game progresses
            self.protagonist = None
            self.curr_map = None

            # create main display screen
            self.main_display_screen = pygame.display.set_mode(             \
                (viewing.MAIN_DISPLAY_WIDTH, viewing.MAIN_DISPLAY_HEIGHT)   \
            )

            pygame.display.set_caption(game_name)

            # create initial viewing object
            self.viewing = viewing.Viewing(self.main_display_screen)

            # set default difficulty to normal.
            self.difficulty = DIFFICULTY_NORMAL

            # set game language to default
            self.language = language

            # set clock
            self.clock = pygame.time.Clock()
            self.clock.tick(40)

    def set_current_game_map(self, curr_map_id, map_top_left=viewing.OW_VIEWING_LOCATION, default_color=viewing.COLOR_BLACK):
        curr_map = map.get_map(curr_map_id)

        if curr_map:
            self.curr_map = curr_map
            self.viewing.curr_map = curr_map
            self.viewing.set_map_on_view(map_top_left, default_color)

    # TODO
    def build_protagonist(self, name, tile_pos):
        protagonist = None

        # build fields
        protag_id = interactive_obj.PROTAGONIST_ID
        protag_name = name
        protag_tile_pos = tile_pos
        protag_image_path_dict = interactive_obj.IMAGE_PATH_DICT_PROTAG

        protagonist = entity.Protagonist(                       \
            protag_id,  \
            protag_name,    \
            protag_image_path_dict,  \
            protag_tile_pos,    \
            gender=entity.GENDER_MALE, \
            race=entity.RACE_HUMAN   \
        )

        logger.debug("Protagonist ID: {0}".format(protagonist.object_id))
        logger.debug("Protagonist obj type: {0}".format(protagonist.object_type))
        logger.debug("Protagonist name: {0}".format(protagonist.name))
        logger.debug("Protagonist gender: {0}".format(protagonist.gender))
        logger.debug("Protagonist race: {0}".format(protagonist.race))
        logger.debug("Protagonist tile_pos: {0}".format(protagonist.tile_position))

        # associate protag with game
        self.protagonist = protagonist

        return protagonist

    def handle_overworld_loop(self):
        continue_playing = True

        # pressed keys
        pressed_right = False
        pressed_left = False
        pressed_up = False
        pressed_down = False


        while continue_playing:
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
                self.viewing.scroll_map_single_tile(map.DIR_SOUTH)
                logger.debug("Moved up")
            elif pressed_right:
                # do character walking animation while scrolling map LEFT
                # TODO
                # scroll map left and update display. scroll one Tile length
                self.viewing.scroll_map_single_tile(map.DIR_WEST)
                logger.debug("Moved right")
            elif pressed_down:
                # do character walking animation while scrolling map UP
                # TODO
                # scroll map up and update display. scroll one Tile length
                self.viewing.scroll_map_single_tile(map.DIR_NORTH)
                logger.debug("Moved down")
            elif pressed_left:
                # do character walking animation while scrolling map RIGHT
                # TODO
                # scroll map right and update display. scroll one Tile length
                self.viewing.scroll_map_single_tile(map.DIR_EAST)
                logger.debug("Moved left")

# set up logger
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
