import pygame
import sys
import gamemap
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
import equipmentslot

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

    game_name = game.GAME_TITLE
    game_surface = pygame.display.set_mode(
        (
            viewingdata.MAIN_DISPLAY_WIDTH,
            viewingdata.MAIN_DISPLAY_HEIGHT
        )
    )

    pygame.display.set_caption(game_name)

    # init interactions
    interaction.Interaction.init_interactions()

    # Load display information.
    display.Display.init_fonts()
    display.Display.init_background_patterns()

    # Init spawn handler queues.
    #spawnhandler.Spawn_Handler.init_spawn_queues()

    # create game. TODO make this a factory method.
    game_obj = game.Game(game_surface, game_language=language.LANG_ESPANOL)


    # load tiles
    tile.Tile.build_tiles()

    # Load miscellaneous objects.
    interactiveobj.Interactive_Object.build_misc_objects()

    # Load resources.
    resources.Resource.build_resources()

    # Load equipment slots.
    equipmentslot.EquipmentSlot.build_equipment_slots()

    # Load items.
    items.Item.build_standard_items()

    # Load characters. # TODO

    # load maps
    gamemap.Map.build_maps()

    # create protagonist
    protag_tile_loc = (12,12)
    game_obj.build_protagonist("Bob")

    # set map and blit
    game_obj.set_and_blit_current_game_map(
        mapdata.R0_A0_ID,
        protag_tile_loc
    )

    # blit protagonist
    #game_obj.viewing.blit_interactive_object(
        #game_obj.protagonist,
        #imageids.OW_IMAGE_ID_DEFAULT,
        #bottom_left_pixel=viewingdata.CENTER_OW_TILE_BOTTOM_LEFT,
    #)

    # update screen
    pygame.display.update()

    # start looping overworld
    game_obj.handle_overworld_loop()

if __name__ == '__main__':
    pygame.init()
    pygame.font.init()
    main()
