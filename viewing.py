import pygame
import logging
import map
import mapdata
import tile
import display
import objdata
import language
import viewingdata

### WALKING CONSTANTS ###
WALK1_FRAME_END = (tile.TILE_SIZE / 4)
WALK2_FRAME_END = 3*(tile.TILE_SIZE / 4)
STAND_FRAME_END = 2*(tile.TILE_SIZE / 4)

### TIME CONSTANTS ###
NUM_MS_SECOND = 1000
SINGLE_TILE_SCROLL_TIME_MS = int(NUM_MS_SECOND * 0.75)
SINGLE_PIXEL_SCROLL_TIME_MS = int(SINGLE_TILE_SCROLL_TIME_MS / tile.TILE_SIZE)

class Viewing():
    def __init__(
                self,
                main_display_surface,
                protagonist=None,
                curr_map=None
            ):
        self.main_display_surface = main_display_surface
        self._protagonist = protagonist
        self.curr_map = curr_map

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

        self.top_display = None

    @classmethod
    def create_viewing(
                cls,
                main_display_surface,
                protagonist=None,
                curr_map=None,
            ):
        ret_viewing = None

        if main_display_surface:
            ret_viewing = Viewing(
                main_display_surface,
                protagonist=protagonist,
                curr_map=curr_map,
            )

            # Create displays for viewing.
            ret_viewing.create_displays()

        return ret_viewing

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
                image_type_id = objdata.OW_IMAGE_ID_DEFAULT
                offset = i % tile.TILE_SIZE

                if direction == mapdata.DIR_SOUTH:
                    # map scrolls south, character walks north
                    if offset < WALK1_FRAME_END:
                        image_type_id = objdata.OW_IMAGE_ID_WALK1_NORTH
                    elif (offset >= STAND_FRAME_END) and (offset < WALK2_FRAME_END):
                        image_type_id = objdata.OW_IMAGE_ID_WALK2_NORTH
                    else:
                        image_type_id = objdata.OW_IMAGE_ID_FACE_NORTH
                elif direction == mapdata.DIR_WEST:
                    if offset < WALK1_FRAME_END:
                        image_type_id = objdata.OW_IMAGE_ID_WALK1_EAST
                    elif (offset >= STAND_FRAME_END) and (offset < WALK2_FRAME_END):
                        image_type_id = objdata.OW_IMAGE_ID_WALK2_EAST
                    else:
                        image_type_id = objdata.OW_IMAGE_ID_FACE_EAST
                elif direction == mapdata.DIR_NORTH:
                    if offset < WALK1_FRAME_END:
                        image_type_id = objdata.OW_IMAGE_ID_WALK1_SOUTH
                    elif (offset >= STAND_FRAME_END) and (offset < WALK2_FRAME_END):
                        image_type_id = objdata.OW_IMAGE_ID_WALK2_SOUTH
                    else:
                        image_type_id = objdata.OW_IMAGE_ID_FACE_SOUTH
                elif direction == mapdata.DIR_EAST:
                    if offset < WALK1_FRAME_END:
                        image_type_id = objdata.OW_IMAGE_ID_WALK1_WEST
                    elif (offset >= STAND_FRAME_END) and (offset < WALK2_FRAME_END):
                        image_type_id = objdata.OW_IMAGE_ID_WALK2_WEST
                    else:
                        image_type_id = objdata.OW_IMAGE_ID_FACE_WEST

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

                self._protagonist.blit_onto_surface(                 \
                    self.main_display_surface,                      \
                    bottom_left_pixel=viewingdata.CENTER_OW_TILE_BOTTOM_LEFT    \
                )

            # Update main display
            pygame.display.update()

            # wait till next iteration
            pygame.time.wait(SINGLE_PIXEL_SCROLL_TIME_MS)

        # finished scrolling, adjust top left viewing tile accordingly
        """
        new_top_left_viewing_tile_x = self.top_left_viewing_tile_coord[0]
        new_top_left_viewing_tile_y = self.top_left_viewing_tile_coord[1]
        if direction == mapdata.DIR_SOUTH:
            new_top_left_viewing_tile_y = new_top_left_viewing_tile_y - 1
        elif direction == mapdata.DIR_NORTH:
            new_top_left_viewing_tile_y = new_top_left_viewing_tile_y + 1
        elif direction == mapdata.DIR_EAST:
            new_top_left_viewing_tile_x = new_top_left_viewing_tile_x + 1
        elif direction == mapdata.DIR_WEST:
            new_top_left_viewing_tile_x = new_top_left_viewing_tile_x - 1
        self.top_left_viewing_tile_coord = (                                \
            new_top_left_viewing_tile_x,                                    \
            new_top_left_viewing_tile_y                                     \
        )
        """

    # TODO document
    # DOES NOT update viewing - caller needs to do that by updating surface
    def set_viewing_screen_default(self, fill_color=viewingdata.COLOR_BLACK):
        self.main_display_surface.fill(fill_color)

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
                coord_x = -1 * int(map_top_left_pixel_pos / tile.TILE_SIZE)
            if map_top_left_pixel_pos[1] >= viewingdata.TOP_DISPLAY_HEIGHT:
                # map top left is aligned with or below top of overworld viewing
                coord_y = 0
            else:
                # map top left is above top of overworld viewing
                coord_y = -1 * int((map_top_left_pixel_pos[1] - viewingdata.TOP_DISPLAY_HEIGHT) / tile.TILE_SIZE)

            ret_coord = (coord_x, coord_y)
            logger.debug("Top left ow viewing tile: {0}, map top left {1}".format(ret_coord, map_top_left_pixel_pos))

        return ret_coord

    # returns rect in tile coordinates that defines the tiles that
    # are in the current viewing window or may enter in the viewing window
    # upon a single tile move
    # TODO FIGURE OUT
    @classmethod
    def calculate_tile_viewing_rect(cls, map_object, top_left_viewing_tile):
        ret_rect = None

        if map_object and top_left_viewing_tile:
            # see if we can get 1 column of tiles to the left of the screen
            # and 1 row of columns above the screen
            start_tile_x = max(0, top_left_viewing_tile[0] - 1)
            start_tile_y = max(0, top_left_viewing_tile[1] - 1)
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
                        - int(                                              \
                            (map_right_edge - viewingdata.MAIN_DISPLAY_WIDTH)           \
                            / tile.TILE_SIZE                                \
                        ),                                                  \
                    map_object.width - 1                                    \
                )
            else:
                end_tile_x = map_object.width - 1

            if map_bottom_edge > viewingdata.MAIN_DISPLAY_HEIGHT:
                # map bottom edge is past the main display bottom edge
                end_tile_y = min(                                           \
                    map_object.height                                       \
                    - int(                                                  \
                        (map_bottom_edge - viewingdata.MAIN_DISPLAY_HEIGHT)             \
                        / tile.TILE_SIZE                                    \
                    ),                                                      \
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

            #num_tile_horiz = 0
            #num_tile_vert = 0

            # calculate tile coordinate offset for when the map
            # top left tile is within the overworld display (but not at the top left of
            # the screen)
        """
        offset_x = int(map_object.top_left_position[0] / tile.TILE_SIZE)
        offset_y = int(map_object.top_left_position[0] / tile.TILE_SIZE)

        if offset_x > 0:
            # map top left tile is past the left screen edge.
            # we can blit as far as 1 tile past the right screen edge or
            # to end of map width, whichever comes first
            num_tile_horiz = min(map_object.width - start_tile_x, OW_DISPLAY_NUM_TILES_HORIZONTAL - offset_x + 1)
        else:
            # map top left tile is aligned with left screen edge or behind it.
            # we can blit as far as 1 tile past the right screen edge or
            # to end of map width, whichever comes first
            num_tile_horiz = min(map_object.width - start_tile_x, OW_DISPLAY_NUM_TILES_HORIZONTAL + 2)
        if offset_y > 0:
            num_tile_vert = min(map_object.height - start_tile_y,
                OW_DISPLAY_NUM_TILES_VERTICAL + 3)
        else:
            num_tile_vert = min(map_object.height - start_tile_y,
                OW_DISPLAY_NUM_TILES_VERTICAL + 3)
        """

            #num_tile_horiz = min(map_object.width - start_tile_x, OW_DISPLAY_NUM_TILES_HORIZONTAL + 2)
            #num_tile_vert = min(map_object.height - start_tile_y, OW_DISPLAY_NUM_TILES_VERTICAL + 3)

            #ret_rect = (start_tile_x, start_tile_y, num_tile_horiz, num_tile_vert)

        #return ret_rect


    # TODO document
    # DOES NOT update viewing - caller needs to do that by updating surface
    def set_and_blit_map_on_view(
                self,
                map_top_left=viewingdata.OW_VIEWING_LOCATION,
                fill_color=viewingdata.COLOR_BLACK
            ):
        self.set_viewing_screen_default(fill_color)

        # set current map's top left position on display screen
        if self.curr_map:
            self.curr_map.top_left_position = map_top_left

            # set top left viewing tile to define what portions of map to blit
            top_left_viewing_tile_coord =                           \
                Viewing.calculate_top_left_ow_viewing_tile(map_top_left)

            logger.debug("Top left viewing tile for map at {0}".format(top_left_viewing_tile_coord))

            # get subset of tiles to blit
            tile_subset_rect = Viewing.calculate_tile_viewing_rect(         \
                self.curr_map,                                              \
                top_left_viewing_tile_coord                             \
            )

            logger.debug("Tile subset viewing rect for map at {0}".format(tile_subset_rect))

            # blit map
            self.curr_map.blit_onto_surface(                                \
                self.main_display_surface,                                  \
                tile_subset_rect=tile_subset_rect,                          \
            )
        else:
            logger.error("No map set for current viewing.")

        # don't forget top display
        self.blit_top_display()

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

    # Requires fonts to be loaded. see display.Display.init_fonts()
    def create_top_display(self):
        if display.Display.top_display_font:
            self.top_display = display.Top_Display(
                self.main_display_surface,
                viewingdata.TOP_DISPLAY_LOCATION,
                display.Display.top_display_font,
                background_color=viewingdata.COLOR_WHITE,
                protagonist=self._protagonist
            )
        else:
            logger.error("Top display font not found.")
            logger.error("Must init fonts through display.Display.init_fonts.")

    # Requires fonts to be loaded. see display.Display.init_fonts()
    def create_displays(self):
        self.create_top_display()

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

    @classmethod
    def init_text_surfaces(cls):
        global DEFAULT_FONT
        global TOP_DISPLAY_TEXT
        DEFAULT_FONT = pygame.font.SysFont('Comic Sans MS', 30)
        TOP_DISPLAY_TEXT = DEFAULT_FONT.render('Test text', False, viewingdata.COLOR_BLACK)

# set up logger
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
