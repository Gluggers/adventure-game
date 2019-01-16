import pygame
import language
import logging
import viewing

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
            self.current_map = None

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

# set up logger
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
