import pygame
import sys
import map
import mapdata
import tile
import logging
import viewing
import language
import objdata
import game

from pygame.locals import *

logger = None

def main():
    logging.basicConfig(level=logging.DEBUG)
    global logger
    logger = logging.getLogger(__name__)

    # create game
    game_obj = game.Game(game.GAME_TITLE, language.DEFAULT_LANGUAGE)

    # load tiles
    tile.Tile.build_tiles()

    # load maps
    map.Map.build_maps()

    # load resources

    # load items

    # load characters

    # clock
    #clock = pygame.time.Clock()

    # create protagonist
    protag_tile_loc = (2,2)
    protagonist = game_obj.build_protagonist("Bob", protag_tile_loc)

    # set map and blit
    game_obj.set_and_blit_current_game_map(mapdata.R0_A0_ID, protag_tile_loc)

    # blit protagonist
    game_obj.viewing.blit_interactive_object(                   \
        protagonist,                                            \
        objdata.OW_IMAGE_ID_DEFAULT,                     \
        bottom_left_pixel=viewing.CENTER_OW_TILE_BOTTOM_LEFT    \
    )

    # update screen
    pygame.display.update()

    # start looping overworld
    game_obj.handle_overworld_loop()

if __name__ == '__main__':
    pygame.init()
    pygame.font.init()
    main()
