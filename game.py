import json
import logging
import pprint
import re
import sys
import pygame
import directions
import display
import entity
import equipmentdata
import equipmentviewing
import interaction
import inventory
import itemdata
import language
import gamemap
import menuoptions
import savefiledata
import selectionviewing
import skills
import tiledata
import timekeeper
import viewing
import viewingdata

### GAME CONSTANTS ###
GAME_TITLE = "Adventure Game v0.1"

### DIFFICULTY CONSTANTS ###
DIFFICULTY_NORMAL = 0x0
DIFFICULTY_HARD = 0x1

DEFAULT_SAVE_FILE_NAME = "savegame.pkl"

class Game(object):
    def __init__(
            self,
            display_surface,
            game_language=language.DEFAULT_LANGUAGE,
        ):
        if display_surface:
            # will change as game progresses
            self.protagonist = None
            self.curr_map = None
            language.Language.set_current_language_id(game_language)

            # create main display screen
            self.main_display_screen = display_surface

            # create initial viewing object
            self.overworld_viewing = \
                viewing.OverworldViewing.create_overworld_viewing(
                    self.main_display_screen,
                )

            self.overworld_inventory_viewing = None
            self.overworld_toolbelt_viewing = None
            self.overworld_equipment_viewing = None

            # Create inventory viewing and toolbelt viewings for overworld..
            self.overworld_inventory_viewing = \
                selectionviewing.ItemSelectionGridViewing.create_item_selection_grid_viewing(
                    self.main_display_screen,
                    itemdata.ITEM_ICON_DIMENSIONS,
                    display_pattern=display.PATTERN_2_ID,
                )

            self.overworld_toolbelt_viewing = \
                selectionviewing.ItemSelectionGridViewing.create_item_selection_grid_viewing(
                    self.main_display_screen,
                    itemdata.ITEM_ICON_DIMENSIONS,
                    display_pattern=display.PATTERN_2_ID,
                )

            self.overworld_equipment_viewing = \
                equipmentviewing.EquipmentViewing.create_equipment_viewing(
                    self.main_display_screen,
                    itemdata.ITEM_ICON_DIMENSIONS,
                    display_pattern=display.PATTERN_2_ID,
                )

            if not self.overworld_viewing:
                LOGGER.error("Failed to create viewing object.")
            else:
                LOGGER.debug("Created viewing object.")

            # set default difficulty to normal.
            self.difficulty = DIFFICULTY_NORMAL

    # TODO document
    # centers map automatically depending on where protagonist is
    # DOES NOT UPDATE SURFACE
    def set_and_blit_current_game_map(
            self,
            curr_map_id,
            protag_tile_location=(0, 0),
        ):
        curr_map = gamemap.Map.get_map(curr_map_id)

        if curr_map and protag_tile_location:
            self.curr_map = curr_map
            self.overworld_viewing.curr_map = curr_map

            self.set_protagonist_tile_position(protag_tile_location)
            #self.curr_map.protagonist_location = protag_tile_location

            # TODO - check if protag tile location is not collision-bound?

            self.overworld_viewing.set_and_blit_map_on_view(
                protag_tile_location,
            )

            LOGGER.info(
                "Protag location: %s",
                self.curr_map.protagonist_location
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
    def change_current_map(
            self,
            dest_map_id,
            protag_dest_tile_pos,
        ):
        if dest_map_id and protag_dest_tile_pos:
            # Set and blit map.#$$
            self.set_and_blit_current_game_map(
                dest_map_id,
                protag_dest_tile_loc,
            )

            # Blit protagonist.
            self.overworld_viewing.blit_interactive_object_bottom_left(
                self.protagonist,
                imageids.OW_IMAGE_ID_DEFAULT,
                viewingdata.CENTER_OW_TILE_BOTTOM_LEFT
            )

            # Update display to show changes.
            pygame.display.update()

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

        if protag_move_dir == directions.DIR_NORTH:
            intended_dest_tile_loc = (curr_tile_loc[0], curr_tile_loc[1]-1)
            map_scroll_dir = directions.DIR_SOUTH
        elif protag_move_dir == directions.DIR_SOUTH:
            intended_dest_tile_loc = (curr_tile_loc[0], curr_tile_loc[1]+1)
            map_scroll_dir = directions.DIR_NORTH
        elif protag_move_dir == directions.DIR_EAST:
            intended_dest_tile_loc = (curr_tile_loc[0]+1, curr_tile_loc[1])
            map_scroll_dir = directions.DIR_WEST
        elif protag_move_dir == directions.DIR_WEST:
            intended_dest_tile_loc = (curr_tile_loc[0]-1, curr_tile_loc[1])
            map_scroll_dir = directions.DIR_EAST

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
                    LOGGER.debug(
                        "Cannot move to occupied dest tile %s",
                        intended_dest_tile_loc
                    )
                else:
                    # We can move here.
                    real_dest_tile_loc = intended_dest_tile_loc
                    can_move = True
            else:
                LOGGER.debug(
                    "Cannot move to destination tile %s " + \
                        "with transportation type %s",
                    intended_dest_tile_loc,
                    transportation_type,
                )
        else:
            # Check if map has neighbor in the intended direction.
            adj_map_info = self.curr_map.get_adjacent_map_info(protag_move_dir)

            if adj_map_info:
                # Get destination map and tile position.
                dest_map_id = adj_map_info[0]
                dest_map = gamemap.Map.get_map(dest_map_id)
                real_dest_tile_loc = adj_map_info[1]

                # Make sure dest tile is reachable
                # with given transportation method.
                is_valid_transport = dest_map.valid_transportation(
                    real_dest_tile_loc,
                    transportation_type
                )

                if dest_map and is_valid_transport:
                    # Check if the tile is occupied by an interactive object.
                    if dest_map.tile_occupied(real_dest_tile_loc):
                        # Object is in the way.
                        LOGGER.debug(
                            "Cannot move to occupied dest tile %s",
                            real_dest_tile_loc
                        )
                    else:
                        # We can move here.
                        can_move = True
                        changing_maps = True
                else:
                    LOGGER.debug(
                        "Cannot reach tile position %s on map %s with" + \
                            "transportation type %s",
                        real_dest_tile_loc,
                        dest_map_id,
                        transportation_type
                    )
            else:
                # no adjacent map, we can't move here
                LOGGER.debug(
                    "No adjacent map found in this direction." \
                    + " Can't move out of map boundary"
                )

        if can_move:
            # TODO check if collision between protag and dest map/tile
            # change protagonist tile location
            self.set_protagonist_tile_position(real_dest_tile_loc)
            LOGGER.debug(
                "Moving to destination tile: %s",
                real_dest_tile_loc
            )

            if changing_maps:
                # TODO - Make sure protag maintains facing direction.
                #self.change_current_map(dest_map, real_dest_tile_loc)
                LOGGER.debug(
                    "Changing map - Dest map ID: %s",
                    dest_map_id
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
            skill_name = skills.get_skill_name(
                skill_id,
                language.Language.current_language_id
            )
            curr_skill_level = self.protagonist.get_skill_level(skill_id)

            if skill_name and curr_skill_level:
                level_up_message = skills.LEVEL_UP_MESSAGE_INFO.get(
                    language.Language.current_language_id,
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

    def get_input_quantity(self, viewing_obj, display_obj, prompt_text):
        ret_quantity = None

        if viewing_obj and display_obj and prompt_text:
            input_str = viewing_obj.display_input_text_box(
                display_obj,
                prompt_text,
                prompt_font_color=viewingdata.COLOR_BLACK,
                input_font_color=viewingdata.COLOR_BLUE_TEXT,
                input_delay_ms=viewingdata.INITIAL_INPUT_DELAY_MS,
                refresh_during=False,
                horizontal_orientation=display.ORIENTATION_CENTERED,
                vertical_orientation=display.ORIENTATION_CENTERED,
                alternative_top_left=None,
                no_display_update=False,
            )

            LOGGER.info("Returned string from input: %s", input_str)

            if input_str:
                result = re.search(
                    viewingdata.ALLOWED_NUMBER_INPUT_STR_REGEX,
                    input_str,
                )

                if result:
                    ret_quantity = display.Display.parse_abbreviated_quantity(
                        input_str
                    )

        return ret_quantity

    # TODO enhance once menus are set up.
    def handle_overworld_inventory(self):
        if self.overworld_inventory_viewing and self.protagonist:
            # Sort inventory first before displaying it.
            self.protagonist.inventory.standard_sort()

            done = False
            curr_index = 0
            preset_top_viewing_row_index = None

            while not done:
                ret_info = self.overworld_inventory_viewing.handle_selection_area(
                    inventory.Inventory.inventory_name_info,
                    self.protagonist.inventory.item_listing_data,
                    starting_selected_index=curr_index,
                    preset_top_viewing_row_index=preset_top_viewing_row_index,
                    preselected_index_list=None,
                    custom_actions=None,
                    bottom_text=None,
                    allowed_selection_option_set=menuoptions.OVERWORLD_INVENTORY_ITEM_OPTION_SET,
                )
                LOGGER.info("Ret info from inventory viewing: %s", ret_info)
                # TODO handle ret_info.

                if ret_info is None:
                    done = True
                else:
                    option_id = ret_info[0]
                    selected_index = ret_info[1]
                    preset_top_viewing_row_index = ret_info[2]

                    if option_id == menuoptions.DISCARD_OPTION_ID:
                        # Remove this item. Shouldn't be stackable.
                        self.protagonist.inventory.remove_item_by_index(
                            selected_index,
                            quantity=1,
                        )

                        curr_index = min(
                            selected_index,
                            self.protagonist.inventory.get_last_index()
                        )
                    elif option_id == menuoptions.DISCARD_1_OPTION_ID:
                        # Remove this item. Should be stackable.
                        self.protagonist.inventory.remove_item_by_index(
                            selected_index,
                            quantity=1,
                        )

                        curr_index = min(
                            selected_index,
                            self.protagonist.inventory.get_last_index()
                        )
                    elif option_id == menuoptions.DISCARD_5_OPTION_ID:
                        # Remove this item. Should be stackable.
                        self.protagonist.inventory.remove_item_by_index(
                            selected_index,
                            quantity=5,
                        )

                        curr_index = min(
                            selected_index,
                            self.protagonist.inventory.get_last_index()
                        )
                    elif option_id == menuoptions.DISCARD_ALL_OPTION_ID:
                        # Remove this item. Should be stackable.
                        selected_item_info = \
                            self.protagonist.inventory.get_item_entry(
                                selected_index
                            )
                        self.protagonist.inventory.remove_item_all(
                            selected_item_info[0]
                        )

                        curr_index = min(
                            selected_index,
                            self.protagonist.inventory.get_last_index()
                        )
                    elif option_id == menuoptions.DISCARD_X_OPTION_ID:
                        # Get user input on how many to remove.
                        # TESTING
                        to_remove_str = self.get_input_quantity(
                            self.overworld_inventory_viewing,
                            self.overworld_inventory_viewing.selection_option_menu_display,
                            "Select how many to discard."
                        )

                        to_remove = display.Display.parse_abbreviated_quantity(
                            to_remove_str
                        )
                        LOGGER.info("Number to remove: %s", to_remove)

                        if to_remove:
                            self.protagonist.inventory.remove_item_by_index(
                                selected_index,
                                quantity=to_remove,
                            )

                        curr_index = min(
                            selected_index,
                            self.protagonist.inventory.get_last_index()
                        )
                    else:
                        done = True

            #self.overworld_viewing.refresh_and_blit_self()
        else:
            LOGGER.warn("No overworld inventory viewing or protagonist set.")

    def handle_overworld_toolbelt(self):
        """Handles interactions with the protagonist toolbelt in overworld.

        The method brings up the toolbelt display, which allows the user
        to view which tools are in the toolbelt.

        Does not automatically update the overworld display after finishing
        the interaction.
        """

        if self.overworld_toolbelt_viewing and self.protagonist:
            # Sort inventory first before displaying it.
            self.protagonist.tool_inventory.standard_sort()

            self.protagonist.tool_inventory.print_self()
            self.overworld_toolbelt_viewing.blit_selection_background(
                inventory.Inventory.toolbelt_name_info,
                bottom_text=None,
            )

            ret_info = self.overworld_toolbelt_viewing.handle_selection_area(
                inventory.Inventory.toolbelt_name_info,
                self.protagonist.tool_inventory.item_listing_data,
                bottom_text=None,
                allowed_selection_option_set=None,
            )
            LOGGER.info("Ret info from toolbet viewing: %s", ret_info)
            # TODO handle ret_info.
        else:
            LOGGER.warn("No overworld toolbelt viewing or protagonist set.")

    def handle_overworld_equipment_viewing(self):
        """Handles interactions with the protagonist equipment in overworld.

        The method brings up the equipment display, which allows the user
        to view and iteract with equipped items.

        Does not automatically update the overworld display after finishing
        the interaction.
        """

        if self.overworld_equipment_viewing and self.protagonist:
            self.overworld_equipment_viewing.blit_selection_background(
                equipmentviewing.EQUIPMENT_VIEWING_NAME_INFO,
                bottom_text=None,
            )

            ret_info = self.overworld_equipment_viewing.handle_equipment_selection_area(
                equipmentviewing.EQUIPMENT_VIEWING_NAME_INFO,
                self.protagonist.equipment_dict,
                starting_selected_slot_id=equipmentdata.EQUIP_SLOT_HEAD,
                bottom_text=None,
                custom_actions=None,
                allowed_selection_option_set=menuoptions.OVERWORLD_EQUIPMENT_ITEM_OPTION_SET,
            )
            LOGGER.info("Ret info from equipment viewing: %s", ret_info)
            # TODO handle ret_info.

            #self.overworld_viewing.refresh_and_blit_self()
        else:
            LOGGER.warn("No overworld equipment viewing or protagonist set.")

    def toggle_language(self):
        """Switches between the supported languages for the game."""

        # For now, just switch to other language
        if language.Language.current_language_id == language.LANG_ENGLISH:
            self.change_language(language.LANG_ESPANOL)
        elif language.Language.current_language_id == language.LANG_ESPANOL:
            self.change_language(language.LANG_ENGLISH)

        # Update display.
        pygame.display.update()

    def change_language(self, new_language):
        """Changes the game language to the specified language.

        Args:
            new_language: language ID value for the langauge to change to.
        """

        if new_language is not None:
            language.Language.set_current_language_id(new_language)

            # Refresh viewings.
            self.overworld_viewing.refresh_and_blit_self()
            pygame.display.update()

    def refresh_and_blit_overworld_viewing(self):
        """Updates the overworld viewing and updates the pygame display."""

        self.overworld_viewing.refresh_and_blit_self()
        pygame.display.update()

    # Blits text in bottom text box.
    # If refresh_after is True, refreshes
    # overworld and blits and updates display
    def display_overworld_bottom_text(
            self,
            text,
            advance_delay_ms=viewingdata.DEFAULT_ADVANCE_DELAY_MS,
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
            advance_delay_ms=viewingdata.DEFAULT_ADVANCE_DELAY_MS,
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
                LOGGER.info("No interaction ID set for the object.")

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
        LOGGER.info(
            "Setting spawn action for tile loc %s " \
                + "using obj id %s with countdown %s",
            bottom_left_tile_loc,
            object_id,
            countdown_time_s,
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
        save_data[savefiledata.GAME_LANGUAGE] = \
            language.Language.current_language_id

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
        LOGGER.info("Saved game.")

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
        LOGGER.info("Loaded game.")

        # Debugging
        LOGGER.debug(
            "Protag location: %s",
            self.get_protagonist_tile_position()
        )

    def display_statistics(self, target_entity):
        # Debugging for now. TODO.
        if target_entity:
            LOGGER.info("Stats (level, curr exp, exp to next level):")
            for skill_id in skills.SKILL_ID_LIST:
                skill_name = skills.get_skill_name(
                    skill_id,
                    language.Language.current_language_id
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
                    LOGGER.info(
                        "%s: Level %s; Curr Exp %s;" \
                            + " Remaining Exp %s",
                        skill_name,
                        level,
                        curr_exp,
                        remaining_exp
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
            LOGGER.info("Quitting game from menu.")
            pygame.quit()
            sys.exit(0)
        elif option_id == menuoptions.INVENTORY_OPTION_ID:
            LOGGER.info("Displaying inventory from menu.")
            self.handle_overworld_inventory()
            self.overworld_viewing.refresh_and_blit_self()
        elif option_id == menuoptions.LEVELS_OPTION_ID:
            LOGGER.info("Displaying stat levels from menu.")
            self.display_statistics(self.protagonist)
        elif option_id == menuoptions.TOOLS_OPTION_ID:
            LOGGER.info("Displaying toolbelt from menu.")
            self.handle_overworld_toolbelt()
            self.overworld_viewing.refresh_and_blit_self()
        elif option_id == menuoptions.EQUIPMENT_OPTION_ID:
            LOGGER.info("Displaying equipment from menu.")
            self.handle_overworld_equipment_viewing()
            self.overworld_viewing.refresh_and_blit_self()

    def handle_overworld_loop(self):
        continue_playing = True

        # pressed keys
        pressed_right = False
        pressed_left = False
        pressed_up = False
        pressed_down = False
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
                        protag_move_dir = directions.DIR_EAST
                        #move_right = True
                        LOGGER.debug("Right pressed down")
                    elif events.key == pygame.K_LEFT:
                        pressed_left = True
                        protag_move_dir = directions.DIR_WEST
                        #move_left = True
                        LOGGER.debug("Left pressed down")
                    elif events.key == pygame.K_UP:
                        pressed_up = True
                        protag_move_dir = directions.DIR_NORTH
                        #move_up = True
                        LOGGER.debug("Up pressed down")
                    elif events.key == pygame.K_DOWN:
                        pressed_down = True
                        protag_move_dir = directions.DIR_SOUTH
                        #move_down = True
                        LOGGER.debug("Down pressed down")
                    elif events.key == pygame.K_SPACE:
                        interact_in_front = True
                        LOGGER.debug("Space pressed down")
                    elif events.key == pygame.K_e:
                        examine_in_front = True
                        LOGGER.debug("Examine key E pressed down")
                    elif events.key == pygame.K_RETURN:
                        examine_in_front = True
                        LOGGER.debug("Examine key Return (Enter) pressed down")
                    elif events.key == pygame.K_i:
                        # Language switch initiated.
                        LOGGER.info("Language change toggled.")
                        self.toggle_language()
                    elif events.key == pygame.K_s:
                        # Save game.
                        LOGGER.info("Save game initiated.")
                        self.save_game()
                    elif events.key == pygame.K_l:
                        # Load game.
                        LOGGER.info("Loading game initiated.")
                        self.load_game()
                    elif events.key == pygame.K_1:
                        # Testing inventory.
                        self.protagonist.inventory.add_item(
                            itemdata.LOG_TREE_ID,
                            2
                        )
                        self.protagonist.inventory.add_item(
                            itemdata.LOG_OAK_ID,
                            2
                        )
                        self.protagonist.inventory.add_item(
                            itemdata.LOG_WILLOW_ID,
                            2
                        )
                        self.protagonist.inventory.add_item(
                            itemdata.LOG_MAPLE_ID,
                            2
                        )
                        self.protagonist.inventory.add_item(
                            itemdata.CURRENCY_SILVER_COIN_ID,
                            500,
                        )
                    elif events.key == pygame.K_2:
                        # Display stats. # TESTING TODO.
                        LOGGER.info("Displaying statistics.")
                        self.display_statistics(self.protagonist)
                    elif events.key == pygame.K_3:
                        # Testing inventory.
                        curr_money = \
                            self.protagonist.inventory.get_item_quantity(
                                itemdata.CURRENCY_GOLD_COIN_ID
                            )
                        LOGGER.info("Curr money: %d", curr_money)
                        self.protagonist.inventory.add_item(
                            itemdata.CURRENCY_GOLD_COIN_ID,
                            curr_money,
                        )
                    elif events.key == pygame.K_4:
                        # Testing stuff.
                        test_display = display.Display(
                            self.main_display_screen,
                            pygame.Rect(100, 100, 50, 150),
                            background_pattern=display.PATTERN_1_ID
                        )
                        test_display.blit_background(
                            self.main_display_screen
                        )
                        pygame.display.update()
                    elif events.key == pygame.K_t:
                        # Testing stuff.
                        LOGGER.info("Testing.")
                    elif events.key == pygame.K_ESCAPE:
                        # Display menu.
                        LOGGER.info("Displaying menu.")
                        # TODO get menu options.
                        # TESTING.
                        selected_option_id = self.display_overworld_side_menu()
                        LOGGER.info(
                            "Selected option: %s, ID %s",
                            menuoptions.get_option_name(
                                selected_option_id,
                                language.Language.current_language_id
                            ),
                            selected_option_id,
                        )
                        self.refresh_and_blit_overworld_viewing()

                        self.process_overworld_menu_option(selected_option_id)
                elif events.type == pygame.KEYUP:
                    if events.key == pygame.K_RIGHT:
                        pressed_right = False
                        #move_right = False
                        LOGGER.debug("Right released")
                    elif events.key == pygame.K_LEFT:
                        pressed_left = False
                        #move_left = False
                        LOGGER.debug("Left released")
                    elif events.key == pygame.K_UP:
                        pressed_up = False
                        #move_up = False
                        LOGGER.debug("Up released")
                    elif events.key == pygame.K_DOWN:
                        pressed_down = False
                        #move_down = False
                        LOGGER.debug("Down released")

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
                    LOGGER.debug(
                        "Protagonist tile_pos: %s",
                        self.curr_map.protagonist_location
                    )
                    LOGGER.debug(
                        "Map top left now at %s",
                        self.curr_map.top_left_position
                    )

                    # Update map and display.
                    self.refresh_and_blit_overworld_viewing()
            elif interact_in_front or examine_in_front:
                LOGGER.debug("Trying to interact/examine in front")

                # Get tile coordinate in front of protagonist
                front_tile_pos = self.get_protagonist_facing_tile_location()

                LOGGER.debug("Facing tile loc: %s", front_tile_pos)

                # See if the map has an interactive object whose collision
                # space takes up the facing tile.
                inter_obj = self.curr_map.get_object_occupying_tile(
                    front_tile_pos
                )

                # Get bottom left tile of object.
                obj_bottom_left_tile_pos = \
                    self.get_bottom_left_tile_of_occupied_tile(front_tile_pos)

                if inter_obj and obj_bottom_left_tile_pos:
                    LOGGER.debug(
                        "Facing object %s", inter_obj.object_id
                    )

                    if interact_in_front:
                        # Interact with object.
                        self.protag_interact(
                            inter_obj,
                            obj_bottom_left_tile_pos
                        )
                    elif examine_in_front:
                        LOGGER.info("Examining")
                        # Display examine text at bottom of screen.
                        self.display_overworld_bottom_text(
                            inter_obj.get_examine_info(
                                language.Language.current_language_id
                            ),
                            refresh_after=True,
                            refresh_during=True,
                        )


# Set up logger.
logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)
