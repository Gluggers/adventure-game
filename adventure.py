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
import interactiveobj
import display
import timekeeper
import interaction
import imageids
import game
import items

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

    # init clock
    timekeeper.Timekeeper.init_clock()

    # init locked logging
    #lockedlogging.Locked_Logger.init_locked_loggers()

    # init interactions
    interaction.Interaction.init_interactions()

    # load fonts
    display.Display.init_fonts()

    # Init spawn handler queues.
    #spawnhandler.Spawn_Handler.init_spawn_queues()

    # create game
    game_obj = game.Game(game.GAME_TITLE, language.LANG_ESPANOL)

    # load tiles
    tile.Tile.build_tiles()

    # Load miscellaneous objects.
    interactiveobj.Interactive_Object.build_misc_objects()

    # Load resources.
    resources.Resource.build_resources()

    # Load items.
    items.Item.build_standard_items()

    # load characters

    # load maps
    map.Map.build_maps()

    # create protagonist
    protag_tile_loc = (12,12)
    game_obj.build_protagonist("Bob")

    # set map and blit
    game_obj.set_and_blit_current_game_map(mapdata.R0_A0_ID, protag_tile_loc)

    # blit protagonist
    game_obj.viewing.blit_interactive_object(
        game_obj.protagonist,
        imageids.OW_IMAGE_ID_DEFAULT,
        bottom_left_pixel=viewingdata.CENTER_OW_TILE_BOTTOM_LEFT,
    )

    # update screen
    pygame.display.update()

    # start looping overworld
    game_obj.handle_overworld_loop()

if __name__ == '__main__':
    pygame.init()
    pygame.font.init()
    main()
