import pygame
import logging
import map
import mapdata
import tile
import display
import objdata
import language
import imageids
import menuoptions
import viewingdata
import imagepaths
import timekeeper
import sys
import fontinfo
import inventory
import itemdata

### WALKING CONSTANTS ###
WALK1_FRAME_END = (tile.TILE_SIZE / 4)
WALK2_FRAME_END = 3*(tile.TILE_SIZE / 4)
STAND_FRAME_END = 2*(tile.TILE_SIZE / 4)

### TIME CONSTANTS ###
NUM_MS_SECOND = 1000
SINGLE_TILE_SCROLL_TIME_MS = int(NUM_MS_SECOND * 0.75)
SINGLE_PIXEL_SCROLL_TIME_MS = int(SINGLE_TILE_SCROLL_TIME_MS / tile.TILE_SIZE)

VIEWING_TILE_PADDING = 2

# Base Viewing class.
class Viewing():
    ### INITIALIZER METHODS ###

    def __init__(
                self,
                main_display_surface,
            ):
        self.main_display_surface = main_display_surface

    ### GETTERS AND SETTERS ###

    ### DISPLAY HANDLING METHODS ###

    # Refreshes self. Does not update display.
    def refresh_self(self):
        pass

    # Does not update display.
    def blit_self(self):
        pass

    # Updates and blits self.
    # Does not update display - caller must do that.
    def refresh_and_blit_self(self):
        self.refresh_self()
        self.blit_self()

    def display_single_text_page(
                self,
                text_display,
                page,
                advance_delay_ms=viewingdata.DEFAULT_ADVANCE_DELAY_MS,
                auto_advance=False,
                refresh_during=True,
                horizontal_orientation=display.ORIENTATION_CENTERED,
                vertical_orientation=display.ORIENTATION_CENTERED,
                alternative_top_left=None,
            ):
        if page and text_display and self.main_display_surface:
            text_display.blit_page(
                self.main_display_surface,
                page,
                show_continue_icon=False,
                horizontal_orientation=horizontal_orientation,
                vertical_orientation=vertical_orientation,
                alternative_top_left=alternative_top_left,
            )

            pygame.display.update()

            # Pause if needed.
            if advance_delay_ms:
                pygame.time.wait(advance_delay_ms)

            if not auto_advance:
                # Refresh and reblit self.
                if refresh_during:
                    self.refresh_and_blit_self()

                # Reblit page but with continue icon if available.
                text_display.blit_page(
                    self.main_display_surface,
                    page,
                    show_continue_icon=True,
                    horizontal_orientation=horizontal_orientation,
                    vertical_orientation=vertical_orientation,
                    alternative_top_left=alternative_top_left,
                )

                pygame.display.update()

                # Clear event queue to prevent premature advancement.
                pygame.event.clear()

                # Wait for user to advance.
                advance = False
                refresh_tick_counter = 0

                logger.debug("Waiting to advance...")

                while not advance:
                    timekeeper.Timekeeper.tick()
                    refresh_tick_counter = (refresh_tick_counter + 1) \
                                    % timekeeper.REFRESH_INTERVAL_NUM_TICKS

                    if refresh_during \
                            and (refresh_tick_counter == 0):
                        # Refresh and reblit self and page.
                        logger.debug("Refreshing while waiting.")
                        self.refresh_and_blit_self()
                        text_display.blit_page(
                            self.main_display_surface,
                            page,
                            show_continue_icon=True,
                            horizontal_orientation=horizontal_orientation,
                            vertical_orientation=vertical_orientation,
                            alternative_top_left=alternative_top_left,
                        )
                        pygame.display.update()

                    for events in pygame.event.get():
                        if events.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit(0)
                        elif events.type == pygame.KEYDOWN:
                            if events.key in viewingdata.TEXT_ADVANCE_KEYS:
                                logger.debug("Advancing to next page")
                                advance = True

    # If refresh_after is True, refreshes
    # and blits self and updates display after all pages.
    # If refresh_during is True, refreshes and blits self and updates display
    # while waiting for advancement and in between pages.
    def display_text_display(
                self,
                text_display,
                text_to_display,
                advance_delay_ms=viewingdata.DEFAULT_ADVANCE_DELAY_MS,
                auto_advance=False,
                refresh_during=True,
                refresh_after=True,
                horizontal_orientation=display.ORIENTATION_CENTERED,
                vertical_orientation=display.ORIENTATION_CENTERED,
                alternative_top_left=None,
            ):
        if self.main_display_surface and text_display and text_to_display:
            # Get the pages.
            page_list = text_display.get_text_pages(text_to_display)

            if page_list:
                # Display each text page.
                for page in page_list:
                    self.display_single_text_page(
                        text_display,
                        page,
                        advance_delay_ms=advance_delay_ms,
                        auto_advance=auto_advance,
                        refresh_during=refresh_during,
                        horizontal_orientation=horizontal_orientation,
                        vertical_orientation=vertical_orientation,
                        alternative_top_left=alternative_top_left,
                    )

                    # Refresh and reblit self.
                    if refresh_during:
                        self.refresh_and_blit_self()
                        pygame.display.update()

            if refresh_after:
                self.refresh_and_blit_self()
                pygame.display.update()

    # If refresh_after is True, refreshes
    # and blits self and updates display after all pages.
    # If refresh_during is True, refreshes and blits self and updates display
    # while waiting for advancement and in between pages.
    def display_text_display_first_page(
                self,
                text_display,
                text_to_display,
                advance_delay_ms=viewingdata.DEFAULT_ADVANCE_DELAY_MS,
                auto_advance=False,
                refresh_during=True,
                refresh_after=True,
                horizontal_orientation=display.ORIENTATION_CENTERED,
                vertical_orientation=display.ORIENTATION_CENTERED,
                alternative_top_left=None,
            ):
        if text_to_display and self.main_display_surface and text_display:
            # Get the pages.
            page_list = text_display.get_text_pages(text_to_display)
            num_pages = len(page_list)

            if num_pages > 1:
                logger.warn("This method only blits first page.")
                logger.warn("Submitted text is {0} pages.".format(num_pages))

            if page_list:
                # Display just the first page.
                self.display_single_text_page(
                    text_display,
                    page_list[0],
                    advance_delay_ms=advance_delay_ms,
                    auto_advance=auto_advance,
                    refresh_during=refresh_during,
                    horizontal_orientation=horizontal_orientation,
                    vertical_orientation=vertical_orientation,
                    alternative_top_left=alternative_top_left,
                )

            if refresh_after:
                self.refresh_and_blit_self()
                pygame.display.update()

    # Returns option ID for selected option, None if no option selected.
    def display_menu_display(
                self,
                menu_display,
                option_id_list,
                horizontal_orientation=display.ORIENTATION_CENTERED,
                vertical_orientation=display.ORIENTATION_CENTERED,
                load_delay_ms=viewingdata.DEFAULT_MENU_LOAD_DELAY_MS,
                option_switch_delay_ms=viewingdata.DEFAULT_MENU_OPTION_SWITCH_DELAY_MS,
                refresh_during=True,
                refresh_after=True,
                alternative_top_left=None,
            ):
        ret_option_id = None
        menu_pages = []

        if self.main_display_surface \
                and menu_display \
                and option_id_list:
            # Get list of menu pages.
            menu_pages = menu_display.get_menu_page_list(option_id_list)

        if menu_pages:
             # Start at top of menu.
            curr_selected_index = 0

            # Blit first menu page.
            curr_page_index = 0

            num_pages = len(menu_pages)

            done = False
            refresh_tick_counter = 0

            while not done:
                curr_page = menu_pages[curr_page_index]
                num_options = len(curr_page.option_id_list)
                curr_option_id = None

                # Blit the current menu page.
                menu_display.blit_menu_page(
                    self.main_display_surface,
                    curr_page,
                    curr_selected_index,
                    horizontal_orientation=horizontal_orientation,
                    vertical_orientation=vertical_orientation,
                    alternative_top_left=alternative_top_left,
                )

                pygame.display.update()

                # Wait a bit before allowing user to select options.
                if load_delay_ms:
                    pygame.time.wait(load_delay_ms)

                if refresh_during:
                    self.refresh_and_blit_self()
                    # Blit the current menu page.
                    menu_display.blit_menu_page(
                        self.main_display_surface,
                        curr_page,
                        curr_selected_index,
                        horizontal_orientation=horizontal_orientation,
                        vertical_orientation=vertical_orientation,
                        alternative_top_left=alternative_top_left,
                    )
                    pygame.display.update()

                # Clear event queue to prevent premature advancement.
                #pygame.event.clear() # TODO remove?

                logger.debug("Waiting for user to select a menu option...")
                selected = False
                while not selected:
                    timekeeper.Timekeeper.tick()

                    next_option = False
                    prev_option = False

                    refresh_tick_counter = (refresh_tick_counter + 1) \
                            % timekeeper.REFRESH_INTERVAL_NUM_TICKS

                    if refresh_during \
                            and (refresh_tick_counter == 0):
                        logger.debug("Refreshing while waiting.")
                        self.refresh_and_blit_self()
                        menu_display.blit_menu_page(
                            self.main_display_surface,
                            curr_page,
                            curr_selected_index,
                            horizontal_orientation=horizontal_orientation,
                            vertical_orientation=vertical_orientation,
                            alternative_top_left=alternative_top_left,
                        )
                        pygame.display.update()

                    for events in pygame.event.get():
                        if events.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit(0)
                        elif events.type == pygame.KEYDOWN:
                            if events.key == pygame.K_DOWN:
                                prev_option = False
                                next_option = True
                            elif events.key == pygame.K_UP:
                                prev_option = True
                                next_option = False
                            elif events.key in viewingdata.MENU_OPTION_EXIT_KEYS:
                                # Exit without selecting option.
                                selected = True
                                done = True
                                ret_option = None
                                prev_option = False
                                next_option = False

                                logger.info(
                                    "Leaving menu without selecting option."
                                )
                            elif events.key in viewingdata.MENU_OPTION_SELECT_KEYS:
                                # We selected the current option.
                                selected = True
                                prev_option = False
                                next_option = False
                                curr_option_id = curr_page.get_option_id(
                                            curr_selected_index
                                        )

                                logger.info(
                                    "Selecting option {0}".format(
                                         menuoptions.get_option_name(
                                            curr_option_id,
                                            language.Language.current_language_id
                                        )
                                    )
                                )

                                if curr_option_id \
                                        == menuoptions.MORE_OPTIONS_OPTION_ID:
                                    # Go to next page and don't return.
                                    curr_page_index = \
                                        (curr_page_index + 1) % num_pages
                                    curr_selected_index = 0
                                    logger.info(
                                        "Moving to next menu page."
                                    )
                                elif curr_option_id:
                                    # Selected a valid option.
                                    done = True
                                    ret_option_id = curr_option_id
                                    logger.info(
                                        "Selected option {0}".format(
                                         menuoptions.get_option_name(
                                                ret_option_id,
                                                language.Language.current_language_id
                                            )
                                        )
                                    )

                    if (not done) \
                            and (not selected) \
                            and (prev_option or next_option):
                        if prev_option:
                            curr_selected_index = (curr_selected_index - 1) \
                                            % num_options
                            logger.info(
                                "Advancing to previous option {0}".format(
                                    menuoptions.get_option_name(
                                        curr_page.get_option_id(
                                            curr_selected_index
                                        ),
                                        language.Language.current_language_id
                                    )
                                )
                            )
                        elif next_option:
                            curr_selected_index = (curr_selected_index + 1) \
                                            % num_options
                            logger.info(
                                "Advancing to next option {0}".format(
                                    menuoptions.get_option_name(
                                        curr_page.get_option_id(
                                            curr_selected_index
                                        ),
                                        language.Language.current_language_id
                                    )
                                )
                            )

                        if refresh_during:
                            self.refresh_and_blit_self()

                        # Reblit menu page with new selected option.
                        menu_display.blit_menu_page(
                            self.main_display_surface,
                            curr_page,
                            curr_selected_index,
                            horizontal_orientation=horizontal_orientation,
                            vertical_orientation=vertical_orientation,
                            alternative_top_left=alternative_top_left,
                        )
                        pygame.display.update()

                        # Delay before allowing user to go to next option.
                        if option_switch_delay_ms:
                            pygame.time.wait(option_switch_delay_ms)

                        if refresh_during:
                            self.refresh_and_blit_self()
                            menu_display.blit_menu_page(
                                self.main_display_surface,
                                curr_page,
                                curr_selected_index,
                                horizontal_orientation=horizontal_orientation,
                                vertical_orientation=vertical_orientation,
                                alternative_top_left=alternative_top_left,
                            )
                            pygame.display.update()

                        # Clear event queue to prevent
                        # premature advancement.
                        #pygame.event.clear() # TODO remove?

        if refresh_after:
            self.refresh_and_blit_self()
            pygame.display.update()

        return ret_option_id

    @classmethod
    def init_text_surfaces(cls):
        global DEFAULT_FONT
        global TOP_DISPLAY_TEXT
        DEFAULT_FONT = pygame.font.SysFont('Comic Sans MS', 30)
        TOP_DISPLAY_TEXT = DEFAULT_FONT.render('Test text', False, viewingdata.COLOR_BLACK)

class Overworld_Viewing(Viewing):
    def __init__(
                self,
                main_display_surface,
                protagonist=None,
                curr_map=None,
                background_pattern=display.PATTERN_1_ID,
            ):
        Viewing.__init__(
            self,
            main_display_surface,
        )

        self._protagonist = protagonist
        self.curr_map = curr_map
        self.background_pattern = background_pattern

        self.top_display = None
        self.bottom_text_display = None
        self.side_menu_display = None
        self.top_health_display = None

    # Requires fonts to be loaded. see display.Display.init_fonts()
    def create_top_health_display(self):
        top_display_font = display.Display.get_font(
                fontinfo.OW_HEALTH_DISPLAY_FONT_ID
            )
        if top_display_font:
            self.top_health_display = display.Text_Display(
                self.main_display_surface,
                viewingdata.OW_TOP_HEALTH_DISPLAY_RECT,
                top_display_font,
                background_pattern=self.background_pattern,
                #background_color=viewingdata.COLOR_WHITE,
                #background_image_path=imagepaths.OW_TOP_HEALTH_DISPLAY_BACKGROUND_PATH,
                horizontal_padding=6,
                vertical_padding=6,
            )

            if self.top_health_display:
                #self.displays[viewingdata.OW_TOP_HEALTH_DISPLAY_ID] = self.top_health_display
                pass
            else:
                logger.error("Failed to make top health display")
        else:
            logger.error("Top display font not found.")
            logger.error("Must init fonts through display.Display.init_fonts.")

    def create_bottom_text_display(self):
        font_obj = display.Display.get_font(
                fontinfo.OW_BOTTOM_TEXT_FONT_ID
            )
        if font_obj:
            self.bottom_text_display = display.Text_Display(
                self.main_display_surface,
                viewingdata.OW_BOTTOM_TEXT_DISPLAY_RECT,
                font_obj,
                continue_icon_image_path=imagepaths.DEFAULT_TEXT_CONTINUE_ICON_PATH,
                background_pattern=self.background_pattern,
                #background_image_path=imagepaths.OW_BOTTOM_TEXT_DISPLAY_BACKGROUND_PATH,
                spacing_factor_between_lines=display.TEXT_BOX_LINE_SPACING_FACTOR,
                horizontal_padding=viewingdata.TEXT_DISPLAY_HORIZONTAL_PADDING,
                vertical_padding=viewingdata.TEXT_DISPLAY_VERTICAL_PADDING,
            )
            if self.bottom_text_display:
                #self.displays[viewingdata.OW_BOTTOM_TEXT_DISPLAY_ID] = self.bottom_text_display
                pass
            else:
                logger.error("Failed to make bottom text display")
        else:
            logger.error("Bottom text display font not found.")
            logger.error("Must init fonts through display.Display.init_fonts.")

    def create_side_menu_display(self):
        font_obj = display.Display.get_font(
                fontinfo.OW_SIDE_MENU_FONT_ID
            )
        if font_obj:
            self.side_menu_display = display.Menu_Display(
                self.main_display_surface,
                viewingdata.OW_SIDE_MENU_RECT,
                font_obj,
                #background_image_path=imagepaths.OW_SIDE_MENU_BACKGROUND_PATH,
                #background_color=viewingdata.COLOR_WHITE,
                background_pattern=self.background_pattern,
                font_color=fontinfo.FONT_COLOR_DEFAULT,
                horizontal_padding=viewingdata.OW_SIDE_MENU_HORIZONTAL_PADDING,
                vertical_padding=viewingdata.OW_SIDE_MENU_VERTICAL_PADDING,
                selection_icon_image_path=imagepaths.DEFAULT_MENU_SELECTION_ICON_PATH,
                spacing_factor_between_lines=display.MENU_LINE_SPACING_FACTOR,
            )
            if self.side_menu_display:
                #self.displays[viewingdata.OW_SIDE_MENU_DISPLAY_ID] = self.side_menu_display
                pass
            else:
                logger.error("Failed to make side menu display.")
        else:
            logger.error("Side menu display font not found.")
            logger.error("Must init fonts through display.Display.init_fonts.")


    # Requires fonts to be loaded. see display.Display.init_fonts()
    def create_displays(self):
        self.create_top_health_display()
        self.create_bottom_text_display()
        self.create_side_menu_display()


    ### GETTERS AND SETTERS ###

    @property
    def protagonist(self):
        """Return protagonist."""
        return self._protagonist

    @protagonist.setter
    def protagonist(self, value):
        """Set protagonist for viewing."""
        if value:
            self._protagonist = value

            # Assign protagonist to top display, as well, which should update
            # the top display
            if self.top_display:
                self.top_display.protagonist = value

    ### DISPLAY HANDLING METHODS ###

    # Blits the top display view onto the main display screen.
    # Does not update the main display - caller will have to do that
    def blit_top_display(self):
        if self.main_display_surface and self.top_display:
            self.top_display.blit_onto_surface(self.main_display_surface)

    def get_health_text(self):
        ret_text = None

        ret_text = ''.join([
            viewingdata.HEALTH_TEXT_PREFIX_INFO.get(
                language.Language.current_language_id,
                ""
            ),
            str(self._protagonist.curr_health),
            ' / ',
            str(self._protagonist.max_health),
        ])

        return ret_text

    # Blits the top health display onto the main display screen.
    # Does not update the main display - caller will have to do that
    def blit_top_health_display(self):
        if self.main_display_surface and self.top_health_display:
            self.display_text_display_first_page(
                self.top_health_display,
                self.get_health_text(),
                advance_delay_ms=0,
                auto_advance=True,
                refresh_during=False,
                refresh_after=False,
            )

    # If refresh_after is True, refreshes
    # overworld and blits and updates display
    def display_bottom_text(
                self,
                text,
                advance_delay_ms=viewingdata.DEFAULT_ADVANCE_DELAY_MS,
                auto_advance=False,
                refresh_during=True,
                refresh_after=True,
            ):
        if text and self.bottom_text_display:
            self.display_text_display(
                self.bottom_text_display,
                text,
                advance_delay_ms=advance_delay_ms,
                auto_advance=auto_advance,
                refresh_during=refresh_during,
                refresh_after=refresh_after,
            )

    # If refresh_after is True, refreshes
    # overworld and blits and updates display
    def display_bottom_text_first_page(
                self,
                text,
                advance_delay_ms=viewingdata.DEFAULT_ADVANCE_DELAY_MS,
                auto_advance=False,
                refresh_during=True,
                refresh_after=True,
            ):
        if text and self.main_display_surface and self.bottom_text_display:
            self.display_text_display_first_page(
                self.bottom_text_display,
                text,
                advance_delay_ms=advance_delay_ms,
                auto_advance=auto_advance,
                refresh_during=refresh_during,
                refresh_after=refresh_after,
            )


    ### MAP HANDLING METHODS ###

    # TODO document
    # DOES NOT update viewing - caller needs to do that by updating surface
    def set_and_blit_map_on_view(
                self,
                protag_tile_location,
                fill_color=viewingdata.COLOR_BLACK
            ):
        # set current map's top left position on display screen
        if self.curr_map and protag_tile_location:
            # Calculate map top left position based on protag location.
            map_top_left = Overworld_Viewing.get_centered_map_top_left_pixel(
                protag_tile_location
            )

            if map_top_left:
                self.curr_map.top_left_position = map_top_left
            else:
                self.curr_map.top_left_position = viewingdata.OW_VIEWING_TOP_LEFT

            # Refresh and blit viewing.
            self.refresh_and_blit_self()
        else:
            logger.error("Missing parameters for setting and blitting map.")

    # Refreshes the data for the overworld, including the map
    # and top display.
    # Does not reblit map or top display - caller will have
    # to do that.
    def refresh_self(self):
        # Update map.
        self.refresh_map()

        # Update top display.
        self.refresh_top_display()

    # Does not update map or display.
    def blit_map(self):
        if self.curr_map:
            # Set top left viewing tile to define what portions of map to blit
            top_left_viewing_tile_coord =                           \
                Overworld_Viewing.calculate_top_left_ow_viewing_tile(
                    self.curr_map.top_left_position
                )

            #logger.debug("Top left viewing tile for map at {0}".format(top_left_viewing_tile_coord))

            # get subset of tiles to blit
            tile_subset_rect = Overworld_Viewing.calculate_tile_viewing_rect(
                self.curr_map,
                top_left_viewing_tile_coord
            )

            #logger.debug("Tile subset viewing rect for map at {0}".format(tile_subset_rect))

            self.curr_map.blit_onto_surface(
                self.main_display_surface,
                tile_subset_rect=tile_subset_rect
            )

    def display_overworld_side_menu(
                self,
                menu_option_ids,
                refresh_after=True,
                refresh_during=True,
                #horizontal_orientation=display.ORIENTATION_LEFT_JUSTIFIED,
                #load_delay_ms=viewingdata.DEFAULT_MENU_LOAD_DELAY_MS,
                #option_switch_delay_ms=viewingdata.DEFAULT_MENU_OPTION_SWITCH_DELAY_MS,
            ):
        ret_option_id = None
        if menu_option_ids:
            # TODO - parent class call display menu

            ret_option_id = self.display_menu_display(
                self.side_menu_display,
                menu_option_ids,
                horizontal_orientation=display.ORIENTATION_LEFT_JUSTIFIED,
                #vertical_orientation=display.ORIENTATION_TOP_JUSTIFIED,
                vertical_orientation=display.ORIENTATION_CENTERED,
                load_delay_ms=viewingdata.DEFAULT_MENU_LOAD_DELAY_MS,
                option_switch_delay_ms=viewingdata.DEFAULT_MENU_OPTION_SWITCH_DELAY_MS,
                refresh_after=refresh_after,
                refresh_during=refresh_during,
            )

        return ret_option_id

    # Blits overworld viewing as is, without updating.
    # Does not update display.
    # OVERRIDES
    def blit_self(self):
        # Blit background.
        self.blit_background()

        # Blit map and top display.
        self.blit_map()

        #self.blit_top_display()
        self.blit_top_health_display()

    def refresh_top_display(self):
        if self.top_display:
            self.top_display.update_self()

    def refresh_and_blit_top_display(self):
        if self.top_display:
            self.refresh_top_display()
            #self.blit_top_display()
            self.blit_top_health_display()

    # Refreshes map.
    # Does not blit map or update display - caller must
    # do that.
    def refresh_map(self):
        if self.curr_map:
            # Refresh map to update it.
            self.curr_map.refresh_self()

    def refresh_and_blit_map(self):
        self.refresh_map()
        self.blit_map()

    # scroll map one Tile distance in the indicated direction.
    # updates main display with each new viewpoint
    # scroll_wait_time is the time (in milliseconds)
    def scroll_map_single_tile(self, direction):
        # get top left viewing tile and tile subset rect to blit

        tile_subset_rect = Overworld_Viewing.calculate_tile_viewing_rect(
            self.curr_map,
            Overworld_Viewing.calculate_top_left_ow_viewing_tile(
                self.curr_map.top_left_position
            )
        )

        logger.debug(
            "Tile subset viewing rect for map at {0}".format(tile_subset_rect)
        )

        # walk1 for TILE_SIZE/4 duration, stand for TILE_SIZE/4,
        # walk2 for TILE_SIZE/4, stand for TILE_SIZE/4
        # walk1 for 0 to 7, stand for 8 to 15,
        # walk2 for 16 to 23, stand for 24 to 31
        for i in range(tile.TILE_SIZE):
            # reset the surface screen to default to black for empty map
            # spaces
            self.blit_background(fill_color=viewingdata.COLOR_BLACK)

            # blit protagonist
            # TODO - have designated spot for protagonist?
            if self._protagonist:
                # get image type ID for protagonist:
                image_type_id = imageids.OW_IMAGE_ID_DEFAULT
                offset = i % tile.TILE_SIZE

                if direction == mapdata.DIR_SOUTH:
                    # map scrolls south, character walks north
                    if offset < WALK1_FRAME_END:
                        image_type_id = imageids.OW_IMAGE_ID_WALK1_NORTH
                    elif (offset >= STAND_FRAME_END) and (offset < WALK2_FRAME_END):
                        image_type_id = imageids.OW_IMAGE_ID_WALK2_NORTH
                    else:
                        image_type_id = imageids.OW_IMAGE_ID_FACE_NORTH
                elif direction == mapdata.DIR_WEST:
                    if offset < WALK1_FRAME_END:
                        image_type_id = imageids.OW_IMAGE_ID_WALK1_EAST
                    elif (offset >= STAND_FRAME_END) and (offset < WALK2_FRAME_END):
                        image_type_id = imageids.OW_IMAGE_ID_WALK2_EAST
                    else:
                        image_type_id = imageids.OW_IMAGE_ID_FACE_EAST
                elif direction == mapdata.DIR_NORTH:
                    if offset < WALK1_FRAME_END:
                        image_type_id = imageids.OW_IMAGE_ID_WALK1_SOUTH
                    elif (offset >= STAND_FRAME_END) and (offset < WALK2_FRAME_END):
                        image_type_id = imageids.OW_IMAGE_ID_WALK2_SOUTH
                    else:
                        image_type_id = imageids.OW_IMAGE_ID_FACE_SOUTH
                elif direction == mapdata.DIR_EAST:
                    if offset < WALK1_FRAME_END:
                        image_type_id = imageids.OW_IMAGE_ID_WALK1_WEST
                    elif (offset >= STAND_FRAME_END) and (offset < WALK2_FRAME_END):
                        image_type_id = imageids.OW_IMAGE_ID_WALK2_WEST
                    else:
                        image_type_id = imageids.OW_IMAGE_ID_FACE_WEST

                # Set new protagonist image id
                self._protagonist.curr_image_id = image_type_id

                # scroll 1 pixel at a time
                self.curr_map.scroll(
                    self.main_display_surface,
                    direction,
                    1,
                    tile_subset_rect=tile_subset_rect
                )

                # Also blit the top view on top.
                #self.blit_top_display()
                self.blit_top_health_display()

            # Update main display
            pygame.display.update()

            # wait till next iteration
            pygame.time.wait(SINGLE_PIXEL_SCROLL_TIME_MS)

    ### SELF BLIT METHODS ###

    # TODO document
    # DOES NOT update viewing - caller needs to do that by updating surface
    def blit_background(self, fill_color=viewingdata.COLOR_BLACK):
        self.main_display_surface.fill(fill_color)

    # blits the obj_to_blit sprite image corresponding to image_type_id
    # onto the designated surface. Can specify either top_left_pixel or
    # bottom_left_pixel as the reference point for blitting the image.
    # bottom_left_pixel is recommended for images that are larger than
    # a single Tile image. If both top_left_pixel and bottom_left_pixel are
    # specified, the method will use bottom_left_pixel as an override.
    # top_left_pixel and bottom_left_pixel are tuples of pixel coordinates.
    # Does not update the surface display - caller will have to do that.
    def blit_interactive_object(                \
                self,                           \
                obj_to_blit,                    \
                image_type_id,                  \
                bottom_left_pixel=None,         \
                top_left_pixel=None             \
            ):
        if self and obj_to_blit and (bottom_left_pixel or top_left_pixel):
            obj_to_blit.blit_onto_surface(              \
                self.main_display_surface,              \
                image_type_id,                          \
                bottom_left_pixel=bottom_left_pixel,    \
                top_left_pixel=top_left_pixel           \
            )

    ### CLASS METHODS ###

    # assumes map_top_left_pixel_pos has coordinates equally divisible
    # by tile.TILE_SIZE
    @classmethod
    def calculate_top_left_ow_viewing_tile_old(cls, map_top_left_pixel_pos):
        ret_coord = None
        if map_top_left_pixel_pos:
            coord_x = 0
            coord_y = 0
            if map_top_left_pixel_pos[0] < 0:
                # map top left is behind the left side of viewing
                coord_x = -1 * int(map_top_left_pixel_pos[0] / tile.TILE_SIZE)
            if map_top_left_pixel_pos[1] >= viewingdata.OW_TOP_DISPLAY_HEIGHT:
                # map top left is aligned with or below top of overworld viewing
                coord_y = 0
            else:
                # map top left is above top of overworld viewing
                coord_y = -1 * int((map_top_left_pixel_pos[1] - viewingdata.OW_TOP_DISPLAY_HEIGHT) / tile.TILE_SIZE)

            ret_coord = (coord_x, coord_y)
            logger.debug("Top left ow viewing tile: {0}, map top left {1}".format(ret_coord, map_top_left_pixel_pos))

        return ret_coord

    # assumes map_top_left_pixel_pos has coordinates equally divisible
    # by tile.TILE_SIZE
    @classmethod
    def calculate_top_left_ow_viewing_tile(cls, map_top_left_pixel_pos):
        ret_coord = None
        if map_top_left_pixel_pos:
            coord_x = 0
            coord_y = 0
            if map_top_left_pixel_pos[0] < 0:
                # map top left is behind the left side of viewing
                coord_x = -1 * int(map_top_left_pixel_pos[0] / tile.TILE_SIZE)
            if map_top_left_pixel_pos[1] < 0:
                # map top left is above top of overworld viewing
                coord_y = -1 * int((map_top_left_pixel_pos[1] - viewingdata.OW_TOP_DISPLAY_HEIGHT) / tile.TILE_SIZE)

            ret_coord = (coord_x, coord_y)
            logger.debug("Top left ow viewing tile: {0}, map top left {1}".format(ret_coord, map_top_left_pixel_pos))

        return ret_coord

    # return top left pixel coordinate for the map given the protagonist's
    # tile coordinates
    @classmethod
    def get_centered_map_top_left_pixel(cls, protag_tile_coordinate):
        top_left = (0,0)
        if protag_tile_coordinate:
            pixel_distance_horiz = viewingdata.CENTER_OW_TILE_TOP_LEFT[0] - (protag_tile_coordinate[0] * tile.TILE_SIZE)
            pixel_distance_vert = viewingdata.CENTER_OW_TILE_TOP_LEFT[1] - (protag_tile_coordinate[1] * tile.TILE_SIZE)

            top_left = (pixel_distance_horiz, pixel_distance_vert)


        return top_left

    # Returns rect in tile coordinates that defines the tiles that
    # are in the current viewing window with at most a 2-Tile-wide padding
    # for smoother scrolling and map loading.
    @classmethod
    def calculate_tile_viewing_rect(cls, map_object, top_left_viewing_tile):
        ret_rect = None

        if map_object and top_left_viewing_tile:
            # see if we can get the Tile padding to the left of the screen
            # and Tile padding above above the screen
            start_tile_x = max(0, top_left_viewing_tile[0] - VIEWING_TILE_PADDING)
            start_tile_y = max(0, top_left_viewing_tile[1] - VIEWING_TILE_PADDING)
            end_tile_x = start_tile_x
            end_tile_y = start_tile_y

            # get the map right edge and bottom edge
            map_right_edge = map_object.top_left_position[0] \
                            + (map_object.width * tile.TILE_SIZE)
            map_bottom_edge = map_object.top_left_position[1] \
                            + (map_object.height * tile.TILE_SIZE)

            if map_right_edge > viewingdata.MAIN_DISPLAY_WIDTH:
                # map right edge is past the main display right edge
                end_tile_x = min(                                           \
                    map_object.width                                        \
                        - 1                                                 \
                        - int(                                              \
                                (map_right_edge - viewingdata.MAIN_DISPLAY_WIDTH)   \
                                / tile.TILE_SIZE                                    \
                            )                                               \
                        + VIEWING_TILE_PADDING,                             \
                    map_object.width - 1                                    \
                )
            else:
                end_tile_x = map_object.width - 1

            if map_bottom_edge > viewingdata.MAIN_DISPLAY_HEIGHT:
                # map bottom edge is past the main display bottom edge
                end_tile_y = min(                                           \
                    map_object.height                                       \
                        - 1                                                 \
                        - int(                                              \
                                (map_bottom_edge - viewingdata.MAIN_DISPLAY_HEIGHT) \
                                / tile.TILE_SIZE                                    \
                            )                                               \
                        + VIEWING_TILE_PADDING,                             \
                    map_object.height - 1
                )
            else:
                end_tile_y = map_object.height - 1

            ret_rect = (
                start_tile_x,
                start_tile_y,
                (end_tile_x - start_tile_x + 1),
                (end_tile_y - start_tile_y + 1)
            )

        return ret_rect

    @classmethod
    def create_overworld_viewing(
                cls,
                main_display_surface,
                protagonist=None,
                curr_map=None,
            ):
        ret_viewing = None

        if main_display_surface:
            ret_viewing = Overworld_Viewing(
                main_display_surface,
                protagonist=protagonist,
                curr_map=curr_map,
            )

            # Create displays for viewing.
            ret_viewing.create_displays()

        return ret_viewing

class SelectionGridViewing(Viewing):
    # TODO update documentation
    # background color is fill color for background in case no
    # background image is available.
    # bottom_text_display_height indicates the pixel height for the
    # area where text will appear at the bottom of the viewing.
    # bottom_text is the text to blit in the bottom_text_rect.
    # allowed_selection_option_set is a set of allowed option IDs to show for
    # icons selected in this viewing. Set to None or empty set to allow
    # no options.
    def __init__(
                self,
                title_info,
                main_display_surface,
                selection_icon_dimensions,
                background_image_path=None,
                background_color=None,
                background_pattern=display.PATTERN_2_ID,
                bottom_text=None,
                #supertext_font_id=fontinfo.SELECTION_SUPERTEXT_FONT_ID,
                #supertext_font_color=viewingdata.COLOR_BLACK,
                #bottom_text_font_id=fontinfo.SELECTION_BOTTOM_TEXT_FONT_ID,
                #bottom_text_font_color=viewingdata.COLOR_BLACK,
                allowed_selection_option_set=None,
                enlarged_selection_background_path=imagepaths.ITEM_LISTING_SELECTED_ENLARGED_BACKGROUND_PATH,
            ):
        Viewing.__init__(
            self,
            main_display_surface,
        )

        self.title_info = title_info
        self.background_image = None
        self.background_color = background_color
        self.background_pattern = background_pattern

        self.icon_supertext_font_object = None
        self.icon_supertext_font_color = viewingdata.COLOR_WHITE

        self.display_rect = viewingdata.INVENTORY_BASIC_VIEWING_RECT
        self.selection_icon_dimensions = selection_icon_dimensions
        self.enlarged_icon_dimensions = (
            2 * selection_icon_dimensions[0],
            2 * selection_icon_dimensions[1]
        )
        self.bottom_text = bottom_text
        self.allowed_selection_option_set = set()
        if allowed_selection_option_set:
            for allowed_option in allowed_selection_option_set:
                self.allowed_selection_option_set.add(allowed_option)

        self.enlarged_selection_background = None
        if enlarged_selection_background_path:
            self.enlarged_selection_background = pygame.image.load(
                    enlarged_selection_background_path
                ).convert_alpha()


        # Calculate the various viewing rects for the inventory.
        top_display_width = int(0.6 * self.display_rect.width)
        top_display_height = 50

        self.top_display_rect = pygame.Rect(
            self.display_rect.x,
            self.display_rect.y,
            top_display_width,
            top_display_height,
        )

        selection_details_width = self.display_rect.width \
                            - top_display_width \
                            - viewingdata.GRID_VIEWING_IN_BETWEEN_PADDING
        selection_details_height = self.display_rect.height
        self.selection_details_rect = pygame.Rect(
            self.top_display_rect.right \
                + viewingdata.GRID_VIEWING_IN_BETWEEN_PADDING,
            self.display_rect.y,
            selection_details_width,
            selection_details_height
        )

        selection_listing_width = top_display_width
        selection_listing_height = self.display_rect.height \
                            - self.top_display_rect.height \
                            - viewingdata.GRID_VIEWING_IN_BETWEEN_PADDING
        bottom_text_width = top_display_width
        bottom_text_height = 0

        self.bottom_text_rect = None
        self.bottom_text_display = None

        if self.bottom_text:
            # Make room for bottom text.
            bottom_text_height = int(self.display_rect.height / 4) \
                                - viewingdata.GRID_VIEWING_IN_BETWEEN_PADDING
            selection_listing_height -= (
                    bottom_text_height \
                    + viewingdata.GRID_VIEWING_IN_BETWEEN_PADDING
                )
            self.bottom_text_rect = pygame.Rect(
                self.display_rect.x,
                self.display_rect.bottom - bottom_text_height,
                bottom_text_width,
                bottom_text_height,
            )

        self.selection_grid_rect = pygame.Rect(
            self.display_rect.x,
            self.top_display_rect.bottom \
                + viewingdata.GRID_VIEWING_IN_BETWEEN_PADDING,
            selection_listing_width,
            selection_listing_height
        )

        if background_image_path:
            self.background_image = pygame.image.load(
                                        background_image_path
                                    ).convert_alpha()

        # Load selection details background image. TODO?
        self.details_background_image = None

        # Will display the word "Inventory".
        self.title_display = None

        # Will display the selections in the inventory.
        self.selection_grid_display = None

        self.selection_details_side_display = display.Display(
            self.main_display_surface,
            self.selection_details_rect,
            background_pattern=self.background_pattern,
        )

        # Will display item name of selected item.
        self.selection_name_display = None
        self.selection_name_rect = pygame.Rect(
            self.selection_details_rect.x,
            self.selection_details_rect.y + 15,
            self.selection_details_rect.width,
            80,
        )
        self.selection_name_rect.centerx = self.selection_details_rect.centerx

        # Will display subtitle of selected object.
        self.selection_subtitle_display = None
        self.selection_subtitle_rect = pygame.Rect(
            self.selection_details_rect.x,
            self.selection_name_rect.bottom \
                + 10,
            self.selection_details_rect.width,
            30,
        )
        self.selection_subtitle_rect.centerx = self.selection_details_rect.centerx

        # Will display enlarged image icon of selected item.
        self.icon_enlarged_display = None
        self.icon_enlarged_rect = pygame.Rect(
            self.selection_details_rect.x,
            self.selection_subtitle_rect.bottom + 10,
            self.enlarged_icon_dimensions[0],
            self.enlarged_icon_dimensions[1]
        )
        self.icon_enlarged_rect.centerx = self.selection_details_rect.centerx

        # Will display details about a single item in the inventory.
        self.selection_description_display = None
        self.selection_description_rect = pygame.Rect(
            self.selection_details_rect.x,
            self.icon_enlarged_rect.bottom,
            self.selection_details_rect.width,
            self.selection_details_rect.bottom \
                - (self.icon_enlarged_rect.bottom)
        )

        # Will display item options for a selected item.
        self.selection_option_menu_display = None
        self.selection_option_menu_rect = pygame.Rect(
            self.selection_details_rect.x,
            self.icon_enlarged_rect.bottom + 15,
            self.selection_details_rect.width - 30,
            self.selection_details_rect.bottom \
                - (self.icon_enlarged_rect.bottom + 15) \
                - 30
        )
        self.selection_option_menu_rect.centerx = \
            self.selection_description_rect.centerx

    # Requires fonts to be loaded. see display.Display.init_fonts()
    def create_title_display(self):
        logger.info("Creating title display...")
        font_obj = display.Display.get_font(
                fontinfo.SELECTION_TOP_DISPLAY_FONT_ID
            )
        if font_obj:
            self.title_display = display.Text_Display(
                self.main_display_surface,
                self.top_display_rect,
                font_obj,
                background_color=None,
                #background_image_path=imagepaths.INVENTORY_BASIC_TITLE_BACKGROUND_PATH,
                background_pattern=self.background_pattern,
                background_image_path=None,
                horizontal_padding=0,
                vertical_padding=0,
            )

            if not self.title_display:
                logger.error("Failed to make title display")
        else:
            logger.error("Top display font not found.")
            logger.error("Must init fonts through display.Display.init_fonts.")

    def create_selection_grid_display(self):
        logger.info("Creating main selection grid display...")
        font_obj = display.Display.get_font(
                fontinfo.SELECTION_SUPERTEXT_FONT_ID
            )
        if font_obj:
            self.icon_supertext_font_object = font_obj
            self.icon_supertext_font_color = viewingdata.COLOR_WHITE
            self.selection_grid_display = display.IconGridDisplay(
                self.main_display_surface,
                self.selection_grid_rect,
                self.selection_icon_dimensions,
                background_pattern=self.background_pattern,
                background_image_path=None,
                background_color=None,
                horizontal_padding=viewingdata.ITEM_LISTING_HORIZONTAL_PADDING,
                vertical_padding=viewingdata.ITEM_LISTING_VERTICAL_PADDING,
                continue_up_icon_image_path=imagepaths.ITEM_LISTING_CONT_UP_PATH,
                continue_down_icon_image_path=imagepaths.ITEM_LISTING_CONT_DOWN_PATH,
                selection_image_path=imagepaths.ITEM_LISTING_SELECTED_DEFAULT_PATH,
            )

            if not self.selection_grid_display:
                logger.error("Failed to make selection grid display")
        else:
            logger.error("Selection grid supertext font not found.")
            logger.error("Must init fonts through display.Display.init_fonts.")

    def create_selection_name_display(self):
        logger.info("Creating selection name display...")
        font_obj = display.Display.get_font(
                fontinfo.SELECTION_NAME_FONT_ID,
            )
        if font_obj:
            self.selection_name_display = display.Text_Display(
                self.main_display_surface,
                self.selection_name_rect,
                font_obj,
                background_color=None,
                background_image_path=None,
                horizontal_padding=20,
                vertical_padding=0,
            )

            if not self.selection_name_display:
                logger.error("Failed to make selection name display")
        else:
            logger.error("Font not found.")
            logger.error("Must init fonts through display.Display.init_fonts.")

    def create_selection_subtitle_display(self):
        logger.info("Creating selection subtitle display...")
        font_obj = display.Display.get_font(
                fontinfo.SELECTION_SUBTITLE_FONT_ID,
            )
        if font_obj:
            self.selection_subtitle_display = display.Text_Display(
                self.main_display_surface,
                self.selection_subtitle_rect,
                font_obj,
                background_color=None,
                background_image_path=None,
                horizontal_padding=20,
                vertical_padding=0,
            )

            if not self.selection_subtitle_display:
                logger.error("Failed to make selection subtitle display")
        else:
            logger.error("Font not found.")
            logger.error("Must init fonts through display.Display.init_fonts.")


    def create_selection_description_display(self):
        logger.info("Creating selection description display...")
        font_obj = display.Display.get_font(
                fontinfo.SELECTION_DESCRIPTION_FONT_ID,
            )
        if font_obj:
            self.selection_description_display = display.Text_Display(
                self.main_display_surface,
                self.selection_description_rect,
                font_obj,
                background_color=None,
                background_image_path=None,
                horizontal_padding=20,
                vertical_padding=20,
            )

            if not self.selection_description_display:
                logger.error("Failed to make selection description display")
        else:
            logger.error("Display font not found.")
            logger.error("Must init fonts through display.Display.init_fonts.")


    def create_selection_options_display(self):
        logger.info("Creating selection options display...")
        font_obj = display.Display.get_font(
                fontinfo.SELECTION_MENU_FONT_ID
            )
        if font_obj:
            self.selection_option_menu_display = display.Menu_Display(
                self.main_display_surface,
                self.selection_option_menu_rect,
                font_obj,
                background_color=display.P1_BG_3_COLOR,
                background_image_path=None,
                background_pattern=None,
                horizontal_padding=20,
                vertical_padding=20,
            )

            if not self.selection_option_menu_display:
                logger.error("Failed to make selection options display")
        else:
            logger.error("Display font not found.")
            logger.error("Must init fonts through display.Display.init_fonts.")

    def create_bottom_text_display(self):
        if self.bottom_text and self.bottom_text_rect:
            logger.info("Creating iselection bottom text display...")
            font_obj = display.Display.get_font(
                    fontinfo.SELECTION_BOTTOM_TEXT_FONT_ID
                )
            if font_obj:
                self.bottom_text_display = display.Text_Display(
                    self.main_display_surface,
                    self.bottom_text_rect,
                    font_obj,
                    background_color=None,
                    background_image_path=None,
                    background_pattern=self.background_pattern,
                    horizontal_padding=20,
                    vertical_padding=20,
                )

                if not self.bottom_text_display:
                    logger.error("Failed to make inventory bottom text display")
            else:
                logger.error("Display font not found.")
                logger.error("Must init fonts through display.Display.init_fonts.")

    # Requires fonts to be loaded. see display.Display.init_fonts().
    def create_base_displays(self):
        self.create_title_display()
        self.create_selection_grid_display()
        self.create_selection_name_display()
        self.create_selection_subtitle_display()
        self.create_selection_description_display()
        self.create_selection_options_display()
        self.create_bottom_text_display()

    # Refreshes self. Does not update display.
    def refresh_self(self):
        pass

    def refresh_and_blit_self_no_background(self):
        self.refresh_self()
        self.blit_self_no_background()

    def blit_background(self):
        # Handle background.
        if self.background_image:
            self.main_display_surface.blit(
                self.background_image,
                self.display_rect,
            )
        elif self.background_color:
            pygame.draw.rect(
                self.main_display_surface,
                self.background_color,
                self.display_rect,
            )

    # Blits self without reblitting background.
    def blit_self_no_background(self):
        # Blit details background.
        if self.details_background_image:
            self.main_display_surface.blit(
                self.details_background_image,
                self.selection_details_rect
            )

        if self.selection_details_side_display:
            self.selection_details_side_display.blit_background(
                self.main_display_surface
            )

        # Handle selection title display.
        if self.title_display:
            # Get title text.
            #inventory_name = inventory.Inventory.get_inventory_name(
            #    #language.Language.get_current_language_id()
            #)
            title_text = self.title_info.get(
                language.Language.get_current_language_id(),
                None
            )

            if title_text:
                self.display_text_display_first_page(
                    self.title_display,
                    title_text,
                    advance_delay_ms=0,
                    auto_advance=True,
                    refresh_during=False,
                    refresh_after=False,
                )

        # Handle bottom text display.
        if self.bottom_text_display:
            self.display_text_display_first_page(
                self.bottom_text_display,
                self.bottom_text,
                advance_delay_ms=0,
                auto_advance=True,
                refresh_during=False,
                refresh_after=False,
            )

    # Does not update display.
    # This method should be called before calling display_
    def blit_self(self):
        self.blit_background()
        self.blit_self_no_background()

    # TODO make this child method?
    def blit_selected_object_name(self, selected_obj):
        if selected_obj:
            # Blit object name.
            obj_name = selected_obj.get_name()
            self.display_text_display_first_page(
                self.selection_name_display,
                obj_name,
                advance_delay_ms=0,
                auto_advance=True,
                refresh_during=False,
                refresh_after=False,
                horizontal_orientation=display.ORIENTATION_CENTERED,
                vertical_orientation=display.ORIENTATION_TOP_JUSTIFIED,
                alternative_top_left=None,
            )

    # TODO make this child method?
    def blit_selected_object_quantity(self, quantity):
        if quantity:
            # Blit quantity.
            quantity_text = "x" + str(quantity)
            self.display_text_display_first_page(
                self.selection_subtitle_display,
                quantity_text,
                advance_delay_ms=0,
                auto_advance=True,
                refresh_during=False,
                refresh_after=False,
                horizontal_orientation=display.ORIENTATION_CENTERED,
                vertical_orientation=display.ORIENTATION_TOP_JUSTIFIED,
                alternative_top_left=None,
            )

    # TODO make this child method?
    def blit_selected_object_enlarged_icon(self, selected_obj):
        if selected_obj:
            # Blit enlarged icon and background.
            enlarged_icon = selected_obj.get_enlarged_icon()
            if enlarged_icon:
                if self.enlarged_selection_background:
                    enlarged_background_rect = \
                        self.enlarged_selection_background.get_rect(
                            center=self.icon_enlarged_rect.center
                        )
                    self.main_display_surface.blit(
                        self.enlarged_selection_background,
                        enlarged_background_rect
                    )

                enlarged_icon_rect = enlarged_icon.get_rect(
                    center=self.icon_enlarged_rect.center
                )
                self.main_display_surface.blit(
                    enlarged_icon,
                    enlarged_icon_rect,
                )

    # Overridable by child.
    def blit_selection_description(self, selected_obj):
        # Blit item description and usage info.
        if selected_obj:
            item_info = "\n".join([
                selected_obj.get_description_info(),
                '--------',
                selected_obj.get_usage_info()
            ])
            self.display_text_display_first_page(
                self.selection_description_display,
                item_info,
                advance_delay_ms=0,
                auto_advance=True,
                refresh_during=False,
                refresh_after=False,
                horizontal_orientation=display.ORIENTATION_LEFT_JUSTIFIED,
                vertical_orientation=display.ORIENTATION_TOP_JUSTIFIED,
                alternative_top_left=None,
            )

    # Overridable by child.
    def blit_main_selection_details(self, selection_info):
        self.blit_selected_object_name(selection_info[0])
        self.blit_selected_object_quantity(selection_info[1])
        self.blit_selected_object_enlarged_icon(selection_info[0])

    # Overridable by child.
    def blit_selection_details(self, selection_info):
        self.blit_main_selection_details(selection_info)
        self.blit_selection_description(selection_info[0])

    # Overridable by child.
    def get_selection_options(self, selection_info):
        selection_options = []

        selection_obj = selection_info[0]

        option_list = selection_obj.item_menu_option_ids \
            + [menuoptions.CANCEL_OPTION_ID]

        for option in option_list:
            if option in self.allowed_selection_option_set:
                selection_options.append(option)

        return selection_options

    def display_selection_options(
            self,
            selection_info
        ):
        ret_option = None

        self.blit_main_selection_details(selection_info)

        # Get valid options.
        options_to_show = self.get_selection_options(
            selection_info
        )

        if options_to_show:
            ret_option = self.display_menu_display(
                self.selection_option_menu_display,
                options_to_show,
                horizontal_orientation=display.ORIENTATION_CENTERED,
                vertical_orientation=display.ORIENTATION_TOP_JUSTIFIED,
                load_delay_ms=viewingdata.DEFAULT_MENU_LOAD_DELAY_MS,
                option_switch_delay_ms=viewingdata.DEFAULT_MENU_OPTION_SWITCH_DELAY_MS,
                refresh_during=False,
                refresh_after=False,
                alternative_top_left=None,
            )

        return ret_option

    # Overridable by child.
    def convert_to_icon_data_list(self, selection_data_list):
        ret_data = None

        if selection_data_list:
            ret_data = []

            for data in selection_data_list:
                curr_object = data[0]
                curr_image = None
                quantity = data[1]
                quantity_text = None

                if curr_object:
                    curr_image = curr_object.get_icon()

                if curr_object.is_stackable():
                    quantity_text = display.Display.get_abbreviated_quantity(
                        quantity
                    )

                rendered_supertext = None

                if quantity_text:
                    rendered_supertext = \
                    self.icon_supertext_font_object.render(
                        quantity_text,
                        False,
                        self.icon_supertext_font_color,
                    )

                ret_data.append([curr_image, rendered_supertext])

        return ret_data

    # Handles displaying the item listing and returns
    # the selected option and item index as a tuple
    # (None if no option is selected).
    def handle_selection_grid(
                self,
                selection_data_list, # list of tuples (selection object, supertext)
                starting_selected_index=0,
                preselected_index_list=[],
            ):
        ret_info = None
        max_index = len(selection_data_list) - 1
        icon_data_list = []

        if selection_data_list:
            icon_data_list = self.convert_to_icon_data_list(selection_data_list)

        if selection_data_list and icon_data_list:
            # Start with the first item.
            curr_index = starting_selected_index
            first_viewable_row_index = \
                self.selection_grid_display.get_row_index(curr_index)
            last_viewable_row_index = \
                first_viewable_row_index \
                + self.selection_grid_display.num_rows \
                - 1

            done = False

            new_index = False
            changed_index = True

            while not done:
                curr_selected_row = self.selection_grid_display.get_row_index(
                        curr_index
                    )

                if curr_selected_row < first_viewable_row_index:
                    # Scroll down.
                    first_viewable_row_index = curr_selected_row
                    last_viewable_row_index = \
                        first_viewable_row_index \
                        + self.selection_grid_display.num_rows \
                        - 1
                elif curr_selected_row > last_viewable_row_index:
                    # Scroll up.
                    last_viewable_row_index = curr_selected_row
                    first_viewable_row_index = max(
                            0,
                            last_viewable_row_index \
                            - self.selection_grid_display.num_rows \
                            + 1
                        )

                logger.debug("Curr row index {0}. First viewable: {1}. Last viewable: {2}".format(
                    curr_selected_row,
                    first_viewable_row_index,
                    last_viewable_row_index
                ))

                if changed_index:
                    self.refresh_and_blit_self_no_background()
                    pygame.display.update()

                go_down = False
                go_up = False
                go_left = False
                go_right = False
                open_options = False

                received_input = False

                curr_selection_info = selection_data_list[curr_index]

                if changed_index:
                    self.selection_grid_display.blit_icon_listing(
                        self.main_display_surface,
                        icon_data_list,
                        first_viewable_row_index,
                        curr_index,
                        preselected_index_list=preselected_index_list,
                        show_continue_icon=True,
                        alternative_top_left=None,
                    )

                    if curr_selection_info:
                        self.blit_selection_details(
                            curr_selection_info
                        )

                    pygame.display.update()

                while not received_input:
                    timekeeper.Timekeeper.tick()

                    for events in pygame.event.get():
                        if events.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit(0)
                        elif events.type == pygame.KEYDOWN:
                            if events.key == pygame.K_ESCAPE:
                                logger.info("Leaving selection viewing.")
                                received_input = True
                                done = True
                            elif events.key == pygame.K_DOWN:
                                logger.info("Going down in grid.")
                                go_down = True
                                go_up = False
                                go_left = False
                                go_right = False
                                open_options = False
                                received_input = True
                            elif events.key == pygame.K_UP:
                                logger.info("Going up in grid.")
                                go_down = False
                                go_up = True
                                go_left = False
                                go_right = False
                                open_options = False
                                received_input = True
                            elif events.key == pygame.K_LEFT:
                                logger.info("Going left in grid.")
                                go_down = False
                                go_up = False
                                go_left = True
                                go_right = False
                                open_options = False
                                received_input = True
                            elif events.key == pygame.K_RIGHT:
                                logger.info("Going right in grid.")
                                go_down = False
                                go_up = False
                                go_left = False
                                go_right = True
                                open_options = False
                                received_input = True
                            elif events.key == pygame.K_RETURN:
                                logger.info("Opening menu")
                                go_down = False
                                go_up = False
                                go_left = False
                                go_right = False
                                open_options = True
                                received_input = True

                if received_input:
                    new_index = curr_index
                    if go_down:
                        new_index = min(
                            max_index,
                            curr_index + self.selection_grid_display.num_columns
                        )
                    elif go_up:
                        new_index = max(
                            0,
                            curr_index - self.selection_grid_display.num_columns
                        )
                    elif go_right:
                        new_index = min(
                            max_index,
                            curr_index + 1
                        )
                    elif go_left:
                        new_index = max(
                            0,
                            curr_index - 1
                        )
                    elif open_options:
                        # Show item options.
                        self.refresh_and_blit_self_no_background()
                        ret_option = self.display_selection_options(
                            curr_selection_info
                        )

                        if ret_option \
                            and ret_option != menuoptions.CANCEL_OPTION_ID:
                            done = True
                            ret_info = (ret_option, curr_index)
                        else:
                            self.refresh_and_blit_self_no_background()
                            self.blit_selection_details(
                                curr_selection_info
                            )
                            pygame.display.update()

                    if new_index != curr_index:
                        changed_index = True
                        curr_index = new_index
                    else:
                        changed_index = False

                    logger.info("Curr index now: {0}".format(curr_index))
                    # TODO rest

        logger.info("Returning selection: {0}".format(ret_info))
        return ret_info

    @classmethod
    def create_selection_grid_viewing(
                cls,
                title_info,
                main_display_surface,
                selection_icon_dimensions,
                bottom_text=None,
                background_image_path=None,
                background_color=viewingdata.COLOR_BLACK,
                background_pattern=display.PATTERN_2_ID,
                allowed_selection_option_set=None,
            ):
        ret_viewing = None

        if main_display_surface:
            ret_viewing = SelectionGridViewing(
                title_info,
                main_display_surface,
                selection_icon_dimensions,
                background_image_path=background_image_path,
                background_color=background_color,
                background_pattern=background_pattern,
                bottom_text=bottom_text,
                allowed_selection_option_set=allowed_selection_option_set,
            )

            # Create displays for viewing.
            ret_viewing.create_base_displays()

        return ret_viewing

# set up logger
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
