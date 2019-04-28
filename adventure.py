# -*- coding: utf-8 -*-
"""Main module that sets up and starts the game."""

import pygame
import display
import equipmentslot
import game
import gamemap
import language
import interaction
import items
import mapdata
import resources
import spells
import tile
import timekeeper
import viewingdata
import interactiveobj

def setup():
    """Initializes game parts."""

    interaction.Interaction.init_interactions()
    display.Display.init_fonts()
    display.Display.init_background_patterns()
    tile.Tile.build_tiles()
    interactiveobj.InteractiveObject.build_misc_objects()
    resources.Resource.build_resources()
    equipmentslot.EquipmentSlot.build_equipment_slots()
    items.Item.build_standard_items()
    spells.Spell.build_spells()

    # Load characters. # TODO

    gamemap.Map.build_maps()

def main():
    """Sets up and runs the game."""

    timekeeper.Timekeeper.init_clock()

    game_name = game.GAME_TITLE
    game_surface = pygame.display.set_mode(
        (
            viewingdata.MAIN_DISPLAY_WIDTH,
            viewingdata.MAIN_DISPLAY_HEIGHT
        )
    )

    pygame.display.set_caption(game_name)

    setup()

    game_obj = game.Game(game_surface, game_language=language.LANG_ESPANOL)

    # Create protagonist.
    protag_tile_loc = (12, 12)
    game_obj.build_protagonist("Bob")

    # Set map and blit.
    game_obj.set_and_blit_game_map(
        mapdata.R0_A0_ID,
        protag_tile_loc
    )

    pygame.display.update()

    # Start looping overworld.
    game_obj.handle_overworld_loop()

if __name__ == '__main__':
    pygame.init()
    pygame.font.init()
    main()
