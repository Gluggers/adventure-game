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
import interaction
import sys
import display
import skills
import json
import savefiledata
import pprint
import time
import items
import menuoptions

logger = None

### GAME CONSTANTS ###
GAME_TITLE = "Adventure Game v0.1"

### DIFFICULTY CONSTANTS ###
DIFFICULTY_NORMAL = 0x0
DIFFICULTY_HARD = 0x1

DEFAULT_SAVE_FILE_NAME = "savegame.pkl"

class Game():
    def __init__(
                self,
                game_name,
                game_language=language.DEFAULT_LANGUAGE,
            ):
        if game_name and game_name:
            # will change as game progresses
            self.protagonist = None
            self.curr_map = None
            self.game_language = game_language

            # create main display screen
            self.main_display_screen = pygame.display.set_mode(
                (
                    viewingdata.MAIN_DISPLAY_WIDTH,
                    viewingdata.MAIN_DISPLAY_HEIGHT
                )
            )

            pygame.display.set_caption(game_name)

            # create initial viewing object
            self.overworld_viewing = \
                viewing.Overworld_Viewing.create_overworld_viewing(
                    self.main_display_screen,
                    display_language=self.game_language,
                )

            if not self.overworld_viewing:
                logger.error("Failed to create viewing object.")
            else:
                logger.debug("Created viewing object.")

            # set default difficulty to normal.
            self.difficulty = DIFFICULTY_NORMAL

    # TODO document
    # centers map automatically depending on where protagonist is
    # DOES NOT UPDATE SURFACE
    def set_and_blit_current_game_map(
                self,
                curr_map_id,
                protag_tile_location=(0,0),
                default_color=viewingdata.COLOR_BLACK,
            ):
        curr_map = map.Map.get_map(curr_map_id)

        if curr_map and protag_tile_location:
            self.curr_map = curr_map
            self.overworld_viewing.curr_map = curr_map
            self.curr_map.protagonist_location = protag_tile_location

            # TODO - check if protag tile location is not collision-bound?

            self.overworld_viewing.set_and_blit_map_on_view(
                protag_tile_location,
                default_color
            )

            logger.info(
                "Protag location: {0}".format(
                    self.curr_map.protagonist_location
                )
            )

    # TODO
    def build_protagonist(self, name):
        protagonist = entity.Protagonist.protagonist_factory(name)

        # Associate protag with game and viewing.
        self.protagonist = protagonist
        self.overworld_viewing.protagonist = protagonist

    def set_protagonist_tile_position(self, new_position):
        if new_position and self.protagonist and self.curr_map:
            self.curr_map.protagonist_location = new_position

    def get_protagonist_tile_position(self):
        position = None
        if self.curr_map:
            position = self.curr_map.protagonist_location
        return position

    # change and transition to new map
    # updates display screen
    # TODO document and change
    """
    def change_current_map(
                self,
                dest_map,
                protag_dest_tile_pos,
                default_color=viewingdata.COLOR_BLACK
            ):
        if dest_map and protag_dest_tile_pos:
            # set and blit map
            self.set_and_blit_current_game_map(dest_map, protag_dest_tile_loc)

            self.set_protagonist_tile_position(protag_dest_tile_loc)

            # blit protagonist
            self.overworld_viewing.blit_interactive_object_bottom_left(
                self.protagonist,
                objdata.OW_IMAGE_ID_DEFAULT,
                viewingdata.CENTER_OW_TILE_BOTTOM_LEFT
            )

            # update screen
            pygame.display.update()
    """

    # moves protagonist in the direction specified,
    # using the specified transportation type
    # successful moves will cause the map to scroll and blit along with
    # screen updates.  Successful moves across different maps will
    # also trigger map changes and associated display changes.
    # Returns True if successful move, False otherwise.
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
            if self.curr_map.valid_transportation(
                        intended_dest_tile_loc,
                        transportation_type
                    ):
                # Check if the intended dest tile is occupied by
                # an interactive object.
                if self.curr_map.tile_occupied(intended_dest_tile_loc):
                    # Object is in the way.
                    logger.debug(
                        "Cannot move to occupied dest tile {0}".format(
                            intended_dest_tile_loc
                        )
                    )
                else:
                    # We can move here.
                    real_dest_tile_loc = intended_dest_tile_loc
                    can_move = True
            else:
                logger.debug(
                    "Cannot move to destination tile {0} " + \
                    "with transportation type {1}".format(
                        intended_dest_tile_loc, transportation_type
                    )
                )
        else:
            # Check if map has neighbor in the intended direction.
            adj_map_info = self.curr_map.get_adjacent_map_info(protag_move_dir)

            if adj_map_info:
                # Get destination map and tile position.
                dest_map_id = adj_map_info[0]
                dest_map = map.Map.get_map(dest_map_id)
                real_dest_tile_loc = adj_map_info[1]

                # Make sure dest tile is reachable
                # with given transportation method.
                if dest_map \
                        and dest_map.valid_transportation(
                            real_dest_tile_loc,
                            transportation_type
                        ):
                    # Check if the tile is occupied by an interactive object.
                    if dest_map.tile_occupied(real_dest_tile_loc):
                        # Object is in the way.
                        logger.debug(
                            "Cannot move to occupied dest tile {0}".format(
                                real_dest_tile_loc
                            )
                        )
                    else:
                        # We can move here.
                        can_move = True
                        changing_maps = True
                else:
                    logger.debug(
                        "Cannot reach tile position {0} on map {1} with" + \
                        "transportation type {2}".format(
                            real_dest_tile_loc,
                            dest_map_id,
                            transportation_type
                        )
                    )
            else:
                # no adjacent map, we can't move here
                logger.debug(
                    "No adjacent map found in this direction." \
                    + " Can't move out of map boundary"
                )

        if can_move:
            # TODO check if collision between protag and dest map/tile
            # change protagonist tile location
            self.set_protagonist_tile_position(real_dest_tile_loc)
            logger.debug(
                "Moving to destination tile: {0}".format(real_dest_tile_loc)
            )

            if changing_maps:
                # TODO - Make sure protag maintains facing direction.
                self.change_current_map(dest_map, real_dest_tile_loc)
                logger.debug(
                    "Changing map - Dest map ID: {0}".format(dest_map_id)
                )
            else:
                # same map, just scroll
                self.overworld_viewing.scroll_map_single_tile(map_scroll_dir)

                # Check if the new tile is a connector tile for the map.
                # If so, switch to the map and tile position.
                # (always call change map method?)
                # Make sure protag maintains facing direction.

        return can_move

    # does not update surface - caller will have to do that
    def turn_protagonist(self, direction_to_face):
        # reblit tile that the protagonist is on
        self.curr_map.blit_tile(
            self.overworld_viewing.main_display_surface,
            self.curr_map.protagonist_location,
            viewingdata.CENTER_OW_TILE_TOP_LEFT,
        )

        # make protagonist face the direction
        self.protagonist.face_direction(
            self.overworld_viewing.main_display_surface,
            direction_to_face,
            bottom_left_pixel=viewingdata.CENTER_OW_TILE_BOTTOM_LEFT,
        )

        # refresh viewing and update display.
        self.refresh_and_blit_overworld_viewing()

    # Returns the tile location tuple for the tile that the protagonist
    # is facing.
    def get_protagonist_facing_tile_location(self):
        front_tile_pos = None

        if self.protagonist \
                and (self.protagonist.facing_direction is not None):
            front_tile_pos = self.curr_map.get_adjacent_tile_position(
                self.curr_map.protagonist_location,
                self.protagonist.facing_direction
            )

        return front_tile_pos

    # Gain experience. Returns number of levels gained from experience gain.
    # Displays bottom message in case of level up.
    def gain_experience(self, target_entity, skill_id, exp_gained):
        levels_gained = 0
        if target_entity:
            levels_gained = target_entity.gain_experience(skill_id, exp_gained)

        if levels_gained and levels_gained > 0:
            # Display level-up message.
            skill_name = skills.get_skill_name(skill_id, self.game_language)
            curr_skill_level = self.protagonist.get_skill_level(skill_id)

            if skill_name and curr_skill_level:
                level_up_message = skills.LEVEL_UP_MESSAGE_INFO.get(
                        self.game_language,
                        ""
                    ).format(
                        levels_gained,
                        skill_name,
                        curr_skill_level,
                    )

                if level_up_message:
                    # This will update display.
                    self.display_overworld_bottom_text(
                        level_up_message,
                        refresh_after=True,
                        refresh_during=True,
                        auto_advance=False,
                    )

    # TODO enhance once menus are set up.
    def display_inventory(self, target_entity):
        if target_entity:
            for item_id, quantity in target_entity.inventory.items():
                item_obj = items.Item.get_item(item_id)

                if item_obj:
                    item_name = item_obj.get_name(self.game_language)
                    logger.info("{0} x{1}".format(item_name, quantity))
                else:
                    logger.error(
                        "Invalid item with ID {0} in inventory.".format(
                            item_id
                        )
                    )
                    break

    def toggle_language(self):
        # For now, just switch to other language
        if self.game_language == language.LANG_ENGLISH:
            self.change_language(language.LANG_ESPANOL)
        elif self.game_language == language.LANG_ESPANOL:
            self.change_language(language.LANG_ENGLISH)

        # Update display.
        pygame.display.update()

    def change_language(self, new_language):
        if new_language is not None:
            self.game_language = new_language
            self.overworld_viewing.change_language(new_language)

    # Updates display.
    def refresh_and_blit_overworld_viewing(self):
        self.overworld_viewing.refresh_and_blit_self()
        pygame.display.update()

    # Blits text in bottom text box.
    # If refresh_after is True, refreshes
    # overworld and blits and updates display
    def display_overworld_bottom_text(
                self,
                text,
                advance_delay_ms=display.DEFAULT_ADVANCE_DELAY_MS,
                auto_advance=False,
                refresh_after=True,
                refresh_during=True,
            ):
        if text and self.overworld_viewing:
            # Display text at bottom of screen.
            self.overworld_viewing.display_bottom_text(
                text,
                advance_delay_ms=advance_delay_ms,
                auto_advance=auto_advance,
                refresh_after=refresh_after,
                refresh_during=refresh_during,
            )

    # If refresh_after is True, refreshes
    # overworld and blits and updates display
    def display_overworld_bottom_text_first_page(
                self,
                text,
                advance_delay_ms=display.DEFAULT_ADVANCE_DELAY_MS,
                auto_advance=False,
                refresh_after=True,
                refresh_during=True,
            ):
        if text and self.overworld_viewing:
            self.overworld_viewing.display_bottom_text_first_page(
                text,
                advance_delay_ms=advance_delay_ms,
                auto_advance=auto_advance,
                refresh_after=refresh_after,
                refresh_during=refresh_during,
            )

    # Have protagonist interact with object.
    def protag_interact(self, target_object, obj_bottom_left_tile_pos):
        if target_object and self.protagonist and obj_bottom_left_tile_pos:
            # Call appropriate interaction method.
            interaction_id = target_object.interaction_id
            interact_method = None

            if interaction_id is not None:
                interact_method = \
                    interaction.Interaction.get_interaction_method(
                        interaction_id
                    )
            else:
                logger.info("No interaction ID set for the object.")

            if interact_method:
                # Get protag tile location.
                protag_loc = self.get_protagonist_tile_position()
                if protag_loc:
                    interact_method(
                        interaction_id,
                        self,
                        self.protagonist,
                        target_object,
                        protag_loc,
                        obj_bottom_left_tile_pos,
                    )

    # Returns bottom left tile location tuple of the bottom left
    # tile associated with the object occupying the given tile location tuple
    # on the game's current map.
    # Returns None if the provided tile location tuple is not occupied.
    def get_bottom_left_tile_of_occupied_tile(self, tile_loc):
        return self.curr_map.get_bottom_left_tile_of_occupied_tile(tile_loc)

    # Sets spawn action for the given map.
    def set_pending_spawn_action(
                self,
                map_obj,
                bottom_left_tile_loc,
                object_id=None,
                countdown_time_s=0,
            ):
        logger.info(
            ("Setting spawn action for tile loc {0} " \
            + "using obj id {1} with countdown {2}").format(
                bottom_left_tile_loc,
                object_id,
                countdown_time_s
            )
        )

        if map_obj and bottom_left_tile_loc:
            map_obj.set_pending_spawn_action(
                bottom_left_tile_loc,
                object_id=object_id,
                countdown_time_s=countdown_time_s,
            )

    # Sets spawn action for the current map.
    def set_pending_spawn_action_curr_map(
                self,
                bottom_left_tile_loc,
                object_id=None,
                countdown_time_s=0,
            ):
        self.set_pending_spawn_action(
            self.curr_map,
            bottom_left_tile_loc,
            object_id=object_id,
            countdown_time_s=countdown_time_s,
        )

    def get_save_data(self):
        save_data = {}

        save_data[savefiledata.CURRENT_MAP_ID] = self.curr_map.map_id
        save_data[savefiledata.CURRENT_PROTAG_TILE_LOCATION] = \
            self.get_protagonist_tile_position()
        save_data[savefiledata.GAME_LANGUAGE] = self.game_language

        # TODO implement further

        return save_data

    def write_data_to_save_file(self, save_file_name):
        if save_file_name:
            # Obtain save data.
            save_data = self.get_save_data()

            # Write save data.
            with open(save_file_name, "w") as save_file:
                json.dump(save_data, save_file)
                #pickle.dump(save_data, save_file, pickle.HIGHEST_PROTOCOL)

    def save_game(self):
        #

        self.write_data_to_save_file(DEFAULT_SAVE_FILE_NAME)
        logger.info("Saved game.")

    def load_data_from_save_file(self, save_file_name):
        if save_file_name:
            # Obtain save data.
            save_data = {}

            with open(save_file_name, "r") as save_file:
                #loaded_game = pickle.load(save_file)
                save_data = json.load(save_file)

            if save_data:
                # Update game information.
                pprint.pprint(save_data)

    def load_game(self):
        self.load_data_from_save_file(DEFAULT_SAVE_FILE_NAME)
        logger.info("Loaded game.")

        # Debugging
        logger.debug("Curr game language: {0}".format(self.game_language))
        logger.debug(
            "Protag location: {0}".format(self.get_protagonist_tile_position())
        )

    def display_statistics(self, target_entity):
        # Debugging for now. TODO.
        if target_entity:
            logger.info("Stats (level, curr exp, exp to next level):")
            for skill_id in skills.SKILL_ID_LIST:
                skill_name = skills.get_skill_name(
                        skill_id,
                        self.game_language
                    )
                level = target_entity.get_skill_level(skill_id)
                curr_exp = target_entity.get_skill_experience(skill_id)
                remaining_exp = target_entity.get_experience_to_next_level(
                        skill_id
                    )

                if skill_name \
                        and (level is not None) \
                        and (curr_exp is not None) \
                        and (remaining_exp is not None):
                    logger.info(
                        ("{0}: Level {1}; Curr Exp {2};" \
                        + " Remaining Exp {3}").format(
                            skill_name,
                            level,
                            curr_exp,
                            remaining_exp
                        )
                    )

    def get_overworld_more_menu_option_str(self):
        return menuoptions.OVERWORLD_MENU_MORE_OPTION_INFO.get(
            self.game_language,
            ""
        )

    # Returns option ID of selected option, None if none selected.
    def display_overworld_side_menu(
                self,
                refresh_after=True,
                refresh_during=True,
            ):

        ret_option_id = self.overworld_viewing.display_overworld_side_menu(
            menuoptions.OVERWORLD_MENU_OPTION_IDS,
            refresh_after=refresh_after,
            refresh_during=refresh_during,
        )

        return ret_option_id

    def process_overworld_menu_option(self, option_id):
        if option_id == menuoptions.QUIT_GAME_OPTION_ID:
            logger.info("Quitting game from menu.")
            pygame.quit()
            sys.exit(0)
        elif option_id == menuoptions.INVENTORY_OPTION_ID:
            logger.info("Displaying inventory from menu.")
            self.display_inventory(self.protagonist)
        elif option_id == menuoptions.STATS_OPTION_ID:
            logger.info("Displaying stat levels from menu.")
            self.display_statistics(self.protagonist)

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

        num_ticks = 0

        while continue_playing:
            # Tick clock.
            timekeeper.Timekeeper.tick()
            num_ticks = num_ticks + 1

            # TODO: update map
            if num_ticks % timekeeper.REFRESH_INTERVAL_NUM_TICKS == 0:
                self.refresh_and_blit_overworld_viewing()

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
                    elif events.key == pygame.K_i:
                        # Language switch initiated.
                        logger.info("Language change toggled.")
                        self.toggle_language()
                    elif events.key == pygame.K_s:
                        # Save game.
                        logger.info("Save game initiated.")
                        self.save_game()
                    elif events.key == pygame.K_l:
                        # Load game.
                        logger.info("Loading game initiated.")
                        self.load_game()
                    elif events.key == pygame.K_1:
                        # Display inventory. # TESTING TODO.
                        logger.info("Displaying inventory.")
                        self.display_inventory(self.protagonist)
                    elif events.key == pygame.K_2:
                        # Display stats. # TESTING TODO.
                        logger.info("Displaying statistics.")
                        self.display_statistics(self.protagonist)
                    elif events.key == pygame.K_ESCAPE:
                        # Display menu.
                        logger.info("Displaying menu.")
                        # TODO get menu options.
                        # TESTING.
                        selected_option_id = self.display_overworld_side_menu()
                        logger.info(
                            "Selected option: {0}, ID {1}".format(
                                menuoptions.get_option_name(
                                    selected_option_id,
                                    self.game_language
                                ),
                                selected_option_id,
                            )
                        )
                        self.refresh_and_blit_overworld_viewing()

                        self.process_overworld_menu_option(selected_option_id)
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
                # sprite image. This will update display.
                self.turn_protagonist(protag_move_dir)

                # Blit top display on top of the current viewing.
                #self.overworld_viewing.blit_top_display()

                # Update display to reflect blit changes.
                #pygame.display.update()

                # Attempt to move the protagonist.
                if self.move_protagonist(protag_move_dir, transport_type):
                    logger.debug(
                        "Protagonist tile_pos: {0}".format(
                            self.curr_map.protagonist_location
                        )
                    )
                    logger.debug(
                        "Map top left now at {0}".format(
                            self.curr_map.top_left_position
                        )
                    )

                    # Update map and display.
                    self.refresh_and_blit_overworld_viewing()
            elif interact_in_front or examine_in_front:
                logger.debug("Trying to interact/examine in front")

                # Get tile coordinate in front of protagonist
                front_tile_pos = self.get_protagonist_facing_tile_location()

                logger.debug("Facing tile loc: {0}".format(front_tile_pos))

                # See if the map has an interactive object whose collision
                # space takes up the facing tile.
                inter_obj = self.curr_map.get_object_occupying_tile(
                        front_tile_pos
                    )

                # Get bottom left tile of object.
                obj_bottom_left_tile_pos = \
                    self.get_bottom_left_tile_of_occupied_tile(front_tile_pos)

                if inter_obj and obj_bottom_left_tile_pos:
                    logger.debug(
                        "Facing object {0}".format(inter_obj.object_id)
                    )

                    if interact_in_front:
                        # Interact with object.
                        self.protag_interact(
                            inter_obj,
                            obj_bottom_left_tile_pos
                        )
                    elif examine_in_front:
                        # Display examine text at bottom of screen.
                        self.display_overworld_bottom_text(
                            inter_obj.get_examine_info(self.game_language),
                            refresh_after=True,
                            refresh_during=True,
                        )


# set up logger
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
