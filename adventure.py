import pygame
import sys
import map
import tile
import logging
import viewing
import language
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

    # clock
    #clock = pygame.time.Clock()

    # set map and blit
    game_obj.viewing.curr_map = map.REGION_GRASSLANDS_AREA_0_MAP
    game_obj.viewing.set_map_on_view(map_top_left=viewing.OW_VIEWING_LOCATION)

    # update screen
    pygame.display.update()

    pressed_right = False
    pressed_left = False
    pressed_up = False
    pressed_down = False

    # main loop for now
    while True:
        #clock.tick(40)

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
            game_obj.viewing.scroll_map_single_tile(map.DIR_SOUTH, viewing.SINGLE_TILE_SCROLL_TIME)
            logger.debug("Moved up")
        elif pressed_right:
            # do character walking animation while scrolling map LEFT
            # TODO
            # scroll map left and update display. scroll one Tile length
            game_obj.viewing.scroll_map_single_tile(map.DIR_WEST, viewing.SINGLE_TILE_SCROLL_TIME)
            logger.debug("Moved right")
        elif pressed_down:
            # do character walking animation while scrolling map UP
            # TODO
            # scroll map up and update display. scroll one Tile length
            game_obj.viewing.scroll_map_single_tile(map.DIR_NORTH, viewing.SINGLE_TILE_SCROLL_TIME)
            logger.debug("Moved down")
        elif pressed_left:
            # do character walking animation while scrolling map RIGHT
            # TODO
            # scroll map right and update display. scroll one Tile length
            game_obj.viewing.scroll_map_single_tile(map.DIR_EAST, viewing.SINGLE_TILE_SCROLL_TIME)
            logger.debug("Moved left")

if __name__ == '__main__':
    pygame.init()
    main()
