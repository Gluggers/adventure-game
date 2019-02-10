import pygame
import language
import logging
import viewing
import viewingdata
import entity
import map
import mapdata
import tile
import tiledata
import timekeeper
import objdata
import interactiveobj
import sys
import skills

logger = None

### GAME CONSTANTS ###
GAME_TITLE = "Adventure Game v0.1"

### DIFFICULTY CONSTANTS ###
DIFFICULTY_NORMAL = 0x0
DIFFICULTY_HARD = 0x1


class Game():
    def __init__(self, game_name, game_language=language.DEFAULT_LANGUAGE):
        if game_name and game_name:
            # will change as game progresses
            self.protagonist = None
            self.curr_map = None
            self.game_language = game_language

            # create main display screen
            self.main_display_screen = pygame.display.set_mode(             \
                (viewingdata.MAIN_DISPLAY_WIDTH, viewingdata.MAIN_DISPLAY_HEIGHT)   \
            )

            pygame.display.set_caption(game_name)

            # create initial viewing object
            self.viewing = viewing.Viewing.create_viewing(
                self.main_display_screen,
                display_language=self.game_language,
            )

            if not self.viewing:
                logger.error("Failed to create viewing object.")
            else:
                logger.debug("Created viewing object.")

            # set default difficulty to normal.
            self.difficulty = DIFFICULTY_NORMAL

    # TODO document
    # centers map automatically depending on where protagonist is
    # DOES NOT UPDATE SURFACE
    def set_and_blit_current_game_map(                                      \
                self,                                                       \
                curr_map_id,                                                \
                protag_tile_location=(0,0),                                 \
                default_color=viewingdata.COLOR_BLACK                           \
            ):
        curr_map = map.Map.get_map(curr_map_id)

        if curr_map and protag_tile_location:
            self.curr_map = curr_map
            self.viewing.curr_map = curr_map
            self.curr_map.protagonist_location = protag_tile_location

            self.viewing.set_and_blit_map_on_view(                          \
                viewing.Viewing.get_centered_map_top_left_pixel(            \
                    protag_tile_location                                    \
                ),                                                          \
                default_color                                               \
            )

    # TODO
    def build_protagonist(self, name):
        protagonist = None

        # build fields
        protag_id = objdata.PROTAGONIST_ID
        protag_name = name
        protag_image_path_dict = objdata.IMAGE_PATH_DICT_PROTAG
        protag_skills_dict = {
            skills.SKILL_ID_HITPOINTS: 10,
        }

        protagonist = entity.Protagonist(                       \
            protag_id,  \
            protag_name,    \
            protag_image_path_dict,  \
            skills_dict=protag_skills_dict,
            gender=entity.GENDER_MALE, \
            race=entity.RACE_HUMAN,
        )

        logger.debug("Protagonist ID: {0}".format(protagonist.object_id))
        logger.debug("Protagonist obj type: {0}".format(protagonist.object_type))
        logger.debug("Protagonist name: {0}".format(protagonist.name))
        logger.debug("Protagonist gender: {0}".format(protagonist.gender))
        logger.debug("Protagonist race: {0}".format(protagonist.race))

        # associate protag with game and viewing
        self.protagonist = protagonist
        self.viewing.protagonist = protagonist

        # Add protagonist to object listing
        interactiveobj.Interactive_Object.interactive_obj_listing[objdata.PROTAGONIST_ID] = protagonist

        return protagonist

    def set_protagonist_tile_position(self, new_position):
        if new_position and self.protagonist and self.curr_map:
            self.curr_map.protagonist_location = new_position

    # change and transition to new map
    # updates display screen
    # TODO document
    def change_current_map(self, dest_map, protag_dest_tile_pos, default_color=viewingdata.COLOR_BLACK):
        if dest_map and protag_dest_tile_pos:
            # set and blit map
            self.set_and_blit_current_game_map(dest_map, protag_dest_tile_loc)

            self.set_protagonist_tile_position(protag_dest_tile_loc)

            # blit protagonist
            self.viewing.blit_interactive_object_bottom_left(self.protagonist, objdata.OW_IMAGE_ID_DEFAULT, viewingdata.CENTER_OW_TILE_BOTTOM_LEFT)

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
        curr_tile_loc = self.curr_map.protagonist_location
        intended_dest_tile_loc = None
        real_dest_tile_loc = None

        if protag_move_dir == mapdata.DIR_NORTH:
            intended_dest_tile_loc = (curr_tile_loc[0], curr_tile_loc[1]-1)
            map_scroll_dir = mapdata.DIR_SOUTH
        elif protag_move_dir == mapdata.DIR_SOUTH:
            intended_dest_tile_loc = (curr_tile_loc[0], curr_tile_loc[1]+1)
            map_scroll_dir = mapdata.DIR_NORTH
        elif protag_move_dir == mapdata.DIR_EAST:
            intended_dest_tile_loc = (curr_tile_loc[0]+1, curr_tile_loc[1])
            map_scroll_dir = mapdata.DIR_WEST
        elif protag_move_dir == mapdata.DIR_WEST:
            intended_dest_tile_loc = (curr_tile_loc[0]-1, curr_tile_loc[1])
            map_scroll_dir = mapdata.DIR_EAST

        # Check for out of bounds destination.
        if self.curr_map.location_within_bounds(intended_dest_tile_loc):
            # Check if the destination tile is reachable with given
            # transportation type.
            if self.curr_map.valid_transportation(intended_dest_tile_loc, transportation_type):
                # Check if the intended dest tile is occupied by
                # an interactive object.
                if self.curr_map.tile_occupied(intended_dest_tile_loc):
                    # Object is in the way.
                    logger.debug("Cannot move to occupied dest tile {0}".format(intended_dest_tile_loc))
                else:
                    # We can move here.
                    real_dest_tile_loc = intended_dest_tile_loc
                    can_move = True
            else:
                logger.debug("Cannot move to destination tile {0} " + \
                    "with transportation type {1}".format(intended_dest_tile_loc, transportation_type))
        else:
            # Check if map has neighbor in the intended direction.
            adj_map_info = self.curr_map.get_adjacent_map_info(protag_move_dir)

            if adj_map_info:
                # Get destination map and tile position.
                dest_map_id = adj_map_info[0]
                dest_map = map.Map.get_map(dest_map_id)
                real_dest_tile_loc = adj_map_info[1]

                # Make sure dest tile is reachable with given transportation method.
                if dest_map and dest_map.valid_transportation(real_dest_tile_loc, transportation_type):
                    # Check if the tile is occupied by an interactive object.
                    if dest_map.tile_occupied(real_dest_tile_loc):
                        # Object is in the way.
                        logger.debug("Cannot move to occupied dest tile {0}".format(real_dest_tile_loc))
                    else:
                        # We can move here.
                        can_move = True
                        changing_maps = True
                else:
                    logger.debug("Cannot reach tile position {0} on map {1} with \
                        transportation type {2}".format(real_dest_tile_loc, dest_map_id, transportation_type))
            else:
                # no adjacent map, we can't move here
                logger.debug("No adjacent map found in this direction. Can't move out of map boundary")

        if can_move:
            # TODO check if collision between protag and dest map/tile
            # change protagonist tile location
            self.set_protagonist_tile_position(real_dest_tile_loc)
            logger.debug("Moving to destination tile: {0}".format(real_dest_tile_loc))

            if changing_maps:
                self.change_current_map(dest_map, real_dest_tile_loc)
                logger.debug("Changing map - Dest map ID: {0}".format(dest_map_id))
            else:
                # same map, just scroll
                self.viewing.scroll_map_single_tile(map_scroll_dir)

    # does not update surface - caller will have to do that
    def turn_protagonist(self, direction_to_face):
        # reblit tile that the protagonist is on
        self.curr_map.blit_tile(                \
            self.viewing.main_display_surface,  \
            self.curr_map.protagonist_location,     \
            viewingdata.CENTER_OW_TILE_TOP_LEFT     \
        )

        # make protagonist face the direction
        self.protagonist.face_direction(                            \
            self.viewing.main_display_surface,                      \
            direction_to_face,                                      \
            bottom_left_pixel=viewingdata.CENTER_OW_TILE_BOTTOM_LEFT    \
        )

    # Returns the tile location tuple for the tile that the protagonist
    # is facing.
    def get_protagonist_facing_tile_location(self):
        front_tile_pos = None

        if self.protagonist and (self.protagonist.facing_direction is not None):
            front_tile_pos = self.curr_map.get_adjacent_tile_position(
                self.curr_map.protagonist_location,
                self.protagonist.facing_direction
            )

        return front_tile_pos

    def handle_overworld_loop(self):
        continue_playing = True

        # pressed keys
        pressed_right = False
        pressed_left = False
        pressed_up = False
        pressed_down = False

        move_up = False
        move_down = False
        move_right = False
        move_left = False
        protag_move_dir = None

        interact_in_front = False
        examine_in_front = False

        while continue_playing:
            # Tick clock.
            timekeeper.Timekeeper.tick()

            # TODO: update map

            interact_in_front = False
            examine_in_front = False

            for events in pygame.event.get():
                if events.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
                elif events.type == pygame.KEYDOWN:
                    if events.key == pygame.K_RIGHT:
                        pressed_right = True
                        protag_move_dir = mapdata.DIR_EAST
                        #move_right = True
                        logger.debug("Right pressed down")
                    elif events.key == pygame.K_LEFT:
                        pressed_left = True
                        protag_move_dir = mapdata.DIR_WEST
                        #move_left = True
                        logger.debug("Left pressed down")
                    elif events.key == pygame.K_UP:
                        pressed_up = True
                        protag_move_dir = mapdata.DIR_NORTH
                        #move_up = True
                        logger.debug("Up pressed down")
                    elif events.key == pygame.K_DOWN:
                        pressed_down = True
                        protag_move_dir = mapdata.DIR_SOUTH
                        #move_down = True
                        logger.debug("Down pressed down")
                    elif events.key == pygame.K_SPACE:
                        interact_in_front = True
                        logger.debug("Space pressed down")
                    elif events.key == pygame.K_e:
                        examine_in_front = True
                        logger.debug("Examine key E pressed down")
                    elif events.key == pygame.K_RETURN:
                        examine_in_front = True
                        logger.debug("Examine key Return (Enter) pressed down")
                elif events.type == pygame.KEYUP:
                    if events.key == pygame.K_RIGHT:
                        pressed_right = False
                        #move_right = False
                        logger.debug("Right released")
                    elif events.key == pygame.K_LEFT:
                        pressed_left = False
                        #move_left = False
                        logger.debug("Left released")
                    elif events.key == pygame.K_UP:
                        pressed_up = False
                        #move_up = False
                        logger.debug("Up released")
                    elif events.key == pygame.K_DOWN:
                        pressed_down = False
                        #move_down = False
                        logger.debug("Down released")

            if pressed_up or pressed_down or pressed_right or pressed_left:
                # TODO for now, just stick with walking
                transport_type = tiledata.WALKABLE_F

                # Make protagonist face the direction and update tile
                # that protagonist is on to clear the previous protagonist
                # sprite image.
                self.turn_protagonist(protag_move_dir)

                # Blit top display on top of the current viewing.
                self.viewing.blit_top_display()

                # Update display to reflect blit changes.
                pygame.display.update()

                # Attempt to move the protagonist.
                self.move_protagonist(protag_move_dir, transport_type)
                logger.debug("Protagonist tile_pos: {0}".format(self.curr_map.protagonist_location))
                logger.debug("Map top left now at {0}".format(self.curr_map.top_left_position))
            elif interact_in_front or examine_in_front:
                logger.debug("Trying to interact/examine in front")

                # Get tile coordinate in front of protagonist
                front_tile_pos = self.get_protagonist_facing_tile_location()

                logger.debug("Facing tile loc: {0}".format(front_tile_pos))

                # See if the map has an interactive object whose collision
                # space takes up the facing tile.
                inter_obj = self.curr_map.get_object_occupying_tile(front_tile_pos)

                if inter_obj:
                    logger.debug("Facing object {0}".format(inter_obj.object_id))

                    if interact_in_front:
                        # Interact with object.
                        pass
                    elif examine_in_front:
                        # Examine object.

                        # Display examine text at bottom of screen.
                        self.viewing.display_bottom_text(inter_obj.get_examine_info(self.game_language))

                        # TODO update map
                        #self.viewing.set_and_blit_current_game_map

                        #logger.debug("EXAMINE INFO: {0}".format(inter_obj.get_examine_info(self.game_language)))

# set up logger
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
