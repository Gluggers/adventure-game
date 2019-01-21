import pygame
import language
import logging
import viewing
import entity
import map
import tile
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

    """
    def set_current_game_map(self, curr_map_id, map_top_left=viewing.OW_VIEWING_LOCATION, default_color=viewing.COLOR_BLACK):
        curr_map = map.get_map(curr_map_id)

        if curr_map:
            self.curr_map = curr_map
            self.viewing.curr_map = curr_map
            self.viewing.set_map_on_view(map_top_left, default_color)
    """

    # TODO document
    # centers map automatically depending on where protagonist is
    # DOES NOT UPDATE SURFACE
    def set_and_blit_current_game_map(self, curr_map_id, protag_tile_location=(0,0), default_color=viewing.COLOR_BLACK):
        curr_map = map.get_map(curr_map_id)

        if curr_map and protag_tile_location:
            self.curr_map = curr_map
            self.viewing.curr_map = curr_map
            self.viewing.set_and_blit_map_on_view(viewing.get_centered_map_top_left_pixel(protag_tile_location), default_color)

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
        self.viewing.protagonist = protagonist

        return protagonist

    # change and transition to new map
    # updates display screen
    # TODO document
    def change_current_map(self, dest_map, protag_dest_tile_pos, default_color=viewing.COLOR_BLACK):
        if dest_map and protag_dest_tile_pos:
            # set and blit map
            self.set_and_blit_current_game_map(dest_map, protag_dest_tile_loc)

            self.protagonist.tile_position = protag_dest_tile_pos

            # blit protagonist
            self.viewing.blit_interactive_object(self.protagonist, interactive_obj.OW_IMAGE_ID_DEFAULT, viewing.CENTER_OW_TILE_PIXEL_LOCATION)

            # update screen
            pygame.display.update()

    # moves protagonist in the direction specified,
    # using the specified transportation type
    # successful moves will cause the map to scroll and blit along with
    # screen updates.  Successful moves across different maps will
    # also trigger map changes and associated display changes.
    def move_protagonist(self, protag_move_dir, transportation_type):
        can_move = False
        changing_maps = False
        dest_map = None
        dest_map_id = None
        map_scroll_dir = None

        # get intended destination tile and check if protagonist is
        # trying to go out of bounds
        curr_tile_loc = self.protagonist.tile_position
        intended_dest_tile_loc = None
        real_dest_tile_loc = None

        if protag_move_dir == map.DIR_NORTH:
            intended_dest_tile_loc = (curr_tile_loc[0], curr_tile_loc[1]-1)
            map_scroll_dir = map.DIR_SOUTH
        elif protag_move_dir == map.DIR_SOUTH:
            intended_dest_tile_loc = (curr_tile_loc[0], curr_tile_loc[1]+1)
            map_scroll_dir = map.DIR_NORTH
        elif protag_move_dir == map.DIR_EAST:
            intended_dest_tile_loc = (curr_tile_loc[0]+1, curr_tile_loc[1])
            map_scroll_dir = map.DIR_WEST
        elif protag_move_dir == map.DIR_WEST:
            intended_dest_tile_loc = (curr_tile_loc[0]-1, curr_tile_loc[1])
            map_scroll_dir = map.DIR_EAST

        # check for out of bounds destination
        if self.curr_map.location_within_bounds(intended_dest_tile_loc):
            # check if the destination tile is reachable with given
            # transportation type
            if self.curr_map.valid_transportation(intended_dest_tile_loc, transportation_type):
                # we can move here
                real_dest_tile_loc = intended_dest_tile_loc
                can_move = True
            else:
                logger.debug("Cannot move to destination tile {0} \
                    with transportation type {1}".format(real_dest_tile_loc, transportation_type))
        else:
            # check if map has neighbor in the intended direction
            adj_map_info = self.curr_map.get_adjacent_map_info(protag_move_dir)

            if adj_map_info:
                # get destination map and tile position
                dest_map_id = adj_map_info[0]
                dest_map = map.get_map(dest_map_id)
                real_dest_tile_loc = adj_map_info[1]

                # make sure dest tile is reachable
                if dest_map and dest_map.valid_transportation(real_dest_tile_loc, transportation_type):
                    # we can move here
                    can_move = True
                    changing_maps = True
                else:
                    logger.debug("Cannot reach tile position {0} on map {1} with \
                        transportation type {2}".format(real_dest_tile_loc, dest_map_id, transportation_type))
            else:
                # no adjacent map, we can't move here
                logger.debug("No adjacent map found in this direction. Can't move out of map boundary")

        if can_move:
            # change protagonist tile location
            self.protagonist.tile_position = real_dest_tile_loc
            logger.debug("Moving to destination tile: {0}".format(real_dest_tile_loc))

            if changing_maps:
                self.change_current_map(dest_map, real_dest_tile_loc)
                logger.debug("Changing map - Dest map ID: {0}".format(dest_map_id))
            else:
                # same map, just scroll
                self.viewing.scroll_map_single_tile(map_scroll_dir)

    def handle_overworld_loop(self):
        continue_playing = True

        # pressed keys
        pressed_right = False
        pressed_left = False
        pressed_up = False
        pressed_down = False

        move_protag = False
        protag_move_dir = None

        while continue_playing:
            # TODO: update map

            for events in pygame.event.get():
                if events.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
                elif events.type == pygame.KEYDOWN:
                    if events.key == pygame.K_RIGHT:
                        pressed_right = True
                        move_protag = True
                        logger.debug("Right pressed down")
                    elif events.key == pygame.K_LEFT:
                        pressed_left = True
                        move_protag = True
                        logger.debug("Left pressed down")
                    elif events.key == pygame.K_UP:
                        pressed_up = True
                        move_protag = True
                        logger.debug("Up pressed down")
                    elif events.key == pygame.K_DOWN:
                        pressed_down = True
                        move_protag = True
                        logger.debug("Down pressed down")
                elif events.type == pygame.KEYUP:
                    if events.key == pygame.K_RIGHT:
                        pressed_right = False
                        move_protag = False
                        logger.debug("Right released")
                    elif events.key == pygame.K_LEFT:
                        pressed_left = False
                        move_protag = False
                        logger.debug("Left released")
                    elif events.key == pygame.K_UP:
                        pressed_up = False
                        move_protag = False
                        logger.debug("Up released")
                    elif events.key == pygame.K_DOWN:
                        pressed_down = False
                        move_protag = False
                        logger.debug("Down released")

            if pressed_up:
                protag_move_dir = map.DIR_NORTH
                #map_scroll_dir = map.DIR_SOUTH

                # do character walking animation while scrolling map DOWN
                # TODO
                # scroll map down and update display. scroll one Tile length
                #self.viewing.scroll_map_single_tile(map.DIR_SOUTH)
                logger.debug("Moved up")
                #logger.debug("Protagonist tile_pos: {0}".format(self.protagonist.tile_position))
            elif pressed_right:
                protag_move_dir = map.DIR_EAST
                #map_scroll_dir = map.DIR_WEST

                # do character walking animation while scrolling map LEFT
                # TODO
                # scroll map left and update display. scroll one Tile length
                #self.viewing.scroll_map_single_tile(map.DIR_WEST)
                logger.debug("Moved right")
                #logger.debug("Protagonist tile_pos: {0}".format(self.protagonist.tile_position))
            elif pressed_down:
                protag_move_dir = map.DIR_SOUTH
                #map_scroll_dir = map.DIR_NORTH

                # do character walking animation while scrolling map UP
                # TODO
                # scroll map up and update display. scroll one Tile length
                #self.viewing.scroll_map_single_tile(map.DIR_NORTH)
                logger.debug("Moved down")
                #logger.debug("Protagonist tile_pos: {0}".format(self.protagonist.tile_position))
            elif pressed_left:
                protag_move_dir = map.DIR_WEST
                #map_scroll_dir = map.DIR_EAST

                # do character walking animation while scrolling map RIGHT
                # TODO
                # scroll map right and update display. scroll one Tile length
                #self.viewing.scroll_map_single_tile(map.DIR_EAST)
                logger.debug("Moved left")
                #logger.debug("Protagonist tile_pos: {0}".format(self.protagonist.tile_position))

            if move_protag:
                # TODO for now, just stick with walking
                transport_type = tile.WALKABLE_F
                self.move_protagonist(protag_move_dir, transport_type)
                logger.debug("Protagonist tile_pos: {0}".format(self.protagonist.tile_position))

# set up logger
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
