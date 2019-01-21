import pygame
import sys
import map
import tile
import logging
import viewing
import language
import interactive_obj
import game

from pygame.locals import *

logger = None

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
    game_obj = game.Game(game.GAME_TITLE, language.DEFAULT_LANGUAGE)

    # load tiles
    tile.build_tiles()

    # load maps
    map.build_maps()

    # load resources

    # load items

    # load characters

    # clock
    #clock = pygame.time.Clock()

    # create protagonist
    protag_tile_loc = (2,2)
    protagonist = game_obj.build_protagonist("Bob", protag_tile_loc)

    # set map and blit
    #game_obj.set_current_game_map(map.R0_A0_ID, map_top_left=viewing.get_centered_map_top_left_pixel(protag_tile_loc))
    game_obj.set_and_blit_current_game_map(map.R0_A0_ID, protag_tile_loc)

    # blit protagonist
    game_obj.viewing.blit_interactive_object(protagonist, interactive_obj.OW_IMAGE_ID_DEFAULT, viewing.CENTER_OW_TILE_PIXEL_LOCATION)

    # update screen
    pygame.display.update()

    # start looping overworld
    game_obj.handle_overworld_loop()

    logger.debug("Should not reach here")

if __name__ == '__main__':
    pygame.init()
    main()
