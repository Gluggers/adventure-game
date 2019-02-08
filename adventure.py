import pygame
import sys
import map
import mapdata
import tile
import logging
import viewing
import viewingdata
import language
import objdata
import resources
import display
import game

from pygame.locals import *

logger = None

# Loads tiles, maps, and objects
def setup():
    pass
    # TODO?

def main():
    logging.basicConfig(level=logging.DEBUG)
    global logger
    logger = logging.getLogger(__name__)

    # load fonts
    display.Display.init_fonts()

    # create game
    game_obj = game.Game(game.GAME_TITLE, language.DEFAULT_LANGUAGE)


    # load tiles
    tile.Tile.build_tiles()

    logger.debug("Adventure: about to load resources")

    # load resources
    resources.Resource.build_resources()

    # load items

    # load characters

    # load maps
    map.Map.build_maps()

    # create protagonist
    protag_tile_loc = (2,2)
    protagonist = game_obj.build_protagonist("Bob")

    # set map and blit
    game_obj.set_and_blit_current_game_map(mapdata.R0_A0_ID, protag_tile_loc)

    # blit protagonist
    game_obj.viewing.blit_interactive_object(                   \
        protagonist,                                            \
        objdata.OW_IMAGE_ID_DEFAULT,                     \
        bottom_left_pixel=viewingdata.CENTER_OW_TILE_BOTTOM_LEFT    \
    )

    # update screen
    pygame.display.update()

    # start looping overworld
    game_obj.handle_overworld_loop()

if __name__ == '__main__':
    pygame.init()
    pygame.font.init()
    main()
