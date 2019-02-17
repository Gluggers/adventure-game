import pygame
import logging
import map
import mapdata
import tile
import display
import objdata
import language
import imageids
import viewingdata

### WALKING CONSTANTS ###
WALK1_FRAME_END = (tile.TILE_SIZE / 4)
WALK2_FRAME_END = 3*(tile.TILE_SIZE / 4)
STAND_FRAME_END = 2*(tile.TILE_SIZE / 4)

### TIME CONSTANTS ###
NUM_MS_SECOND = 1000
SINGLE_TILE_SCROLL_TIME_MS = int(NUM_MS_SECOND * 0.75)
SINGLE_PIXEL_SCROLL_TIME_MS = int(SINGLE_TILE_SCROLL_TIME_MS / tile.TILE_SIZE)

VIEWING_TILE_PADDING = 2

class Viewing():
    ### INITIALIZER METHODS ###

    def __init__(
                self,
                main_display_surface,
                protagonist=None,
                curr_map=None,
                display_language=language.DEFAULT_LANGUAGE,
            ):
        self.main_display_surface = main_display_surface
        self._protagonist = protagonist
        self.curr_map = curr_map
        self.display_language=display_language

        # create Rect objects for main display
        self.top_display_rect = pygame.Rect(                            \
            viewingdata.TOP_DISPLAY_LOCATION,                         \
            (viewingdata.TOP_DISPLAY_WIDTH, viewingdata.TOP_DISPLAY_HEIGHT)     \
        )
        self.ow_viewing_rect = pygame.Rect(                             \
            viewingdata.OW_VIEWING_LOCATION,                           \
            (viewingdata.OW_VIEWING_WIDTH, viewingdata.OW_VIEWING_HEIGHT)   \
        )
        self.ow_side_menu_rect = pygame.Rect(                           \
            viewingdata.OW_SIDE_MENU_LOCATION,                                      \
            (viewingdata.OW_SIDE_MENU_WIDTH, viewingdata.OW_SIDE_MENU_HEIGHT)                   \
        )
        self.main_display_rect = pygame.Rect(                           \
            viewingdata.MAIN_DISPLAY_LOCATION,                                      \
            (viewingdata.MAIN_DISPLAY_WIDTH, viewingdata.MAIN_DISPLAY_HEIGHT)                     \
        )

        self.bottom_text_display_rect = pygame.Rect(
            viewingdata.BOTTOM_TEXT_DISPLAY_TOP_LEFT[0],
            viewingdata.BOTTOM_TEXT_DISPLAY_TOP_LEFT[1],
            viewingdata.BOTTOM_TEXT_DISPLAY_WIDTH,
            viewingdata.BOTTOM_TEXT_DISPLAY_HEIGHT
        )

        self.top_display = None
        self.bottom_text_display = None

    # Requires fonts to be loaded. see display.Display.init_fonts()
    def create_top_display(self):
        if display.Display.top_display_font:
            self.top_display = display.Top_Display(
                self.main_display_surface,
                self.top_display_rect,
                display.Display.top_display_font,
                background_color=viewingdata.COLOR_WHITE,
                protagonist=self._protagonist,
                display_language=self.display_language,
            )
        else:
            logger.error("Top display font not found.")
            logger.error("Must init fonts through display.Display.init_fonts.")

    def create_bottom_text_display(self):
        if display.Display.bottom_text_display_font:
            self.bottom_text_display = display.Text_Display(
                self.main_display_surface,
                self.bottom_text_display_rect,
                display.Display.bottom_text_display_font,
                display_language=self.display_language,
            )
        else:
            logger.error("Bottom text display font not found.")
            logger.error("Must init fonts through display.Display.init_fonts.")

    # Requires fonts to be loaded. see display.Display.init_fonts()
    def create_displays(self):
        self.create_top_display()
        self.create_bottom_text_display()


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
            self.top_display.protagonist = value

    def change_language(self, new_language):
        if new_language is not None:
            # Need to change language for Top Display.
            if self.top_display:
                self.top_display.display_language = new_language

                # Update self.
                self.refresh_and_blit_overworld()

    ### DISPLAY HANDLING METHODS ###

    # blits the top display view onto the main display screen
    # does not update the main display - caller will have to do that
    def blit_top_display(self):
        if self.main_display_surface and self.top_display:
            self.top_display.blit_onto_surface(self.main_display_surface)

            # Add background for top display.
            #pygame.draw.rect(self.main_display_surface, viewingdata.COLOR_WHITE, \
                #self.top_display_rect)

            # Blit the top display details
            #if self._protagonist:
                #self.main_display_surface.blit(TOP_DISPLAY_TEXT, (0,0))

    """
    def display_bottom_text(self, text):
        if text and self.main_display_surface and self.bottom_text_display:
            self.bottom_text_display.display_text(
                self.main_display_surface,
                text
            )

            # Wait a little after finishing pages.
            pygame.time.wait(display.BOTTOM_TEXT_DELAY_MS)
            pygame.event.clear()
    """
    # If refresh_after is True, refreshes
    # overworld and blits and updates display
    def display_bottom_text(
                self,
                text,
                advance_delay_ms=display.DEFAULT_ADVANCE_DELAY_MS,
                auto_advance=False,
                refresh_after=False,
            ):
        if text and self.main_display_surface and self.bottom_text_display:
            self.bottom_text_display.display_text(
                self.main_display_surface,
                text,
                advance_delay_ms=advance_delay_ms,
                auto_advance=auto_advance,
            )

            # pygame.event.clear()

            if refresh_after:
                self.refresh_and_blit_overworld()
                pygame.display.update()

    # If refresh_after is True, refreshes
    # overworld and blits and updates display
    def display_bottom_first_text_page(
                self,
                text,
                advance_delay_ms=display.DEFAULT_ADVANCE_DELAY_MS,
                auto_advance=False,
                refresh_after=False,
            ):
        if text and self.main_display_surface and self.bottom_text_display:
            self.bottom_text_display.display_first_text_page(
                self.main_display_surface,
                text,
                advance_delay_ms=advance_delay_ms,
                auto_advance=auto_advance,
            )

            # pygame.event.clear()

            if refresh_after:
                self.refresh_and_blit_overworld()
                pygame.display.update()

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
            map_top_left = Viewing.get_centered_map_top_left_pixel(
                protag_tile_location
            )

            if map_top_left:
                self.curr_map.top_left_position = map_top_left
            else:
                self.curr_map.top_left_position = viewingdata.OW_VIEWING_LOCATION

            # Refresh and blit viewing.
            self.refresh_and_blit_overworld()
        else:
            logger.error("Missing parameters for setting and blitting map.")

    # Refreshes the data for the overworld, including the map
    # and top display.
    # Does not reblit map or top display - caller will have
    # to do that.
    def refresh_overworld(self):
        # Update map.
        self.refresh_map()

        # Update top display.
        self.refresh_top_display()

    # Does not update map or display.
    def blit_map(self):
        if self.curr_map:
            # Set top left viewing tile to define what portions of map to blit
            top_left_viewing_tile_coord =                           \
                Viewing.calculate_top_left_ow_viewing_tile(
                    self.curr_map.top_left_position
                )

            #logger.debug("Top left viewing tile for map at {0}".format(top_left_viewing_tile_coord))

            # get subset of tiles to blit
            tile_subset_rect = Viewing.calculate_tile_viewing_rect(
                self.curr_map,
                top_left_viewing_tile_coord
            )

            #logger.debug("Tile subset viewing rect for map at {0}".format(tile_subset_rect))

            self.curr_map.blit_onto_surface(
                self.main_display_surface,
                tile_subset_rect=tile_subset_rect
            )

    # Blits overworld viewing as is, without updating.
    # Does not update display.
    def blit_overworld_viewing(self):
        # Blit background.
        self.set_viewing_screen_default()

        # Blit map and top display.
        self.blit_map()

        self.blit_top_display()

    # Updates and blit current overworld viewing.
    # Does not update display - caller must do that.
    def refresh_and_blit_overworld(self):
        # Blit background.
        self.set_viewing_screen_default()

        # Refresh and blit map.
        self.refresh_and_blit_map()

        # Update top display and blit.
        self.refresh_and_blit_top_display()

    def refresh_top_display(self):
        if self.top_display:
            self.top_display.update_self()

    def refresh_and_blit_top_display(self):
        if self.top_display:
            self.refresh_top_display()
            self.blit_top_display()

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

        tile_subset_rect = Viewing.calculate_tile_viewing_rect(         \
            self.curr_map,                                              \
            Viewing.calculate_top_left_ow_viewing_tile(                 \
                self.curr_map.top_left_position                         \
            )                                                           \
        )

        logger.debug("Tile subset viewing rect for map at {0}".format(tile_subset_rect))

        # walk1 for TILE_SIZE/4 duration, stand for TILE_SIZE/4,
        # walk2 for TILE_SIZE/4, stand for TILE_SIZE/4
        # walk1 for 0 to 7, stand for 8 to 15,
        # walk2 for 16 to 23, stand for 24 to 31
        for i in range(tile.TILE_SIZE):
            # reset the surface screen to default to black for empty map
            # spaces
            self.set_viewing_screen_default(fill_color=viewingdata.COLOR_BLACK)

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
                self.blit_top_display()

            # Update main display
            pygame.display.update()

            # wait till next iteration
            pygame.time.wait(SINGLE_PIXEL_SCROLL_TIME_MS)

    ### SELF BLIT METHODS ###

    # TODO document
    # DOES NOT update viewing - caller needs to do that by updating surface
    def set_viewing_screen_default(self, fill_color=viewingdata.COLOR_BLACK):
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
    def calculate_top_left_ow_viewing_tile(cls, map_top_left_pixel_pos):
        ret_coord = None
        if map_top_left_pixel_pos:
            coord_x = 0
            coord_y = 0
            if map_top_left_pixel_pos[0] < 0:
                # map top left is behind the left side of viewing
                coord_x = -1 * int(map_top_left_pixel_pos[0] / tile.TILE_SIZE)
            if map_top_left_pixel_pos[1] >= viewingdata.TOP_DISPLAY_HEIGHT:
                # map top left is aligned with or below top of overworld viewing
                coord_y = 0
            else:
                # map top left is above top of overworld viewing
                coord_y = -1 * int((map_top_left_pixel_pos[1] - viewingdata.TOP_DISPLAY_HEIGHT) / tile.TILE_SIZE)

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
    def init_text_surfaces(cls):
        global DEFAULT_FONT
        global TOP_DISPLAY_TEXT
        DEFAULT_FONT = pygame.font.SysFont('Comic Sans MS', 30)
        TOP_DISPLAY_TEXT = DEFAULT_FONT.render('Test text', False, viewingdata.COLOR_BLACK)

    @classmethod
    def create_viewing(
                cls,
                main_display_surface,
                protagonist=None,
                curr_map=None,
                display_language=language.DEFAULT_LANGUAGE,
            ):
        ret_viewing = None

        if main_display_surface:
            ret_viewing = Viewing(
                main_display_surface,
                protagonist=protagonist,
                curr_map=curr_map,
                display_language=display_language,
            )

            # Create displays for viewing.
            ret_viewing.create_displays()

        return ret_viewing

# set up logger
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
