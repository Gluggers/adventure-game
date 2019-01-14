import logging
import pygame
import random
import sys
import images
import interactive_obj
import adventure
from pygame.locals import *

### DIRECTION CONSTANTS ###
DIR_NORTH = 0x0
DIR_EAST = 0x1
DIR_SOUTH = 0x2
DIR_WEST = 0x3

### TILE CONSTANTS ###
TILE_SIZE = 16
TILE_LISTING = {} # maps Tile IDs to tile objects

### TILE ID NUMBERS ###
TILE_DEFAULT_ID = 0x0
TILE_GRASS_1_ID = 0x100
TILE_GRASS_2_ID = 0x101
TILE_GRASS_PLAIN_ID = 0x103
TILE_WATER_NORMAL_1_ID = 0x200
TILE_WATER_NORMAL_2_ID = 0x201
TILE_WATER_NORMAL_3_ID = 0x202
TILE_WATER_NORMAL_4_ID = 0x203
TILE_WATER_NORMAL_5_ID = 0x204
TILE_WATER_NORMAL_6_ID = 0x205
TILE_WATER_NORMAL_7_ID = 0x206
TILE_WATER_NORMAL_8_ID = 0x207
TILE_WATER_NORMAL_9_ID = 0x208
TILE_SAND_ID = 0x300

### MAP CONSTANTS ###
MAP_LISTING = {} # maps Map IDs to Map objects

### MAP ID CONSTANTS ###
R0_A0_ID = 0x0
R0_A1_ID = 0x1
R0_A2_ID = 0x2
R0_A3_ID = 0x3
R0_A4_ID = 0x4
R0_A5_ID = 0x5
R1_A0_ID = 0x1000
R1_A1_ID = 0x1001
R1_A2_ID = 0x1002
R1_A3_ID = 0x1003
R1_A4_ID = 0x1004
R1_A5_ID = 0x1005
R2_A0_ID = 0x2000
R2_A1_ID = 0x2001
R2_A2_ID = 0x2002
R2_A3_ID = 0x2003
R2_A4_ID = 0x2004
R2_A5_ID = 0x2005

### TRANSPORTATION FLAGS ###
WALKABLE_F = 0x1
CANOEABLE_F = 0x2
SAILABLE_F = 0x4
FLYABLE_F = 0x8

### CLASS NAMES ###
MAP_CLASS = 'Map'
TILE_CLASS = 'Tile'
REGION_CLASS = 'Region'
AREA_CLASS = 'Area'

### LOGGER ###
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# TODO make this extend sprite?

# SHOULD THIS BE IMMUTABLE?
class Tile:
    def __init__(self,                                          \
                image_path=images.TILE_DEFAULT_PATH,            \
                allowed_transport=(WALKABLE_F | FLYABLE_F),     \
                ):
        # represents the base terrain image (e.g. grass, water)
        self.image = pygame.image.load(image_path).convert()

        # OR-ed flags that represent the allowed methods of transportation on
        # this tile - walking, canoing, sailing, and flying.
        self.allowed_transport = allowed_transport

    # blits the tile image onto the surface at the designated pixel
    # coordinate position (x,y).
    # Does not update the surface display - caller will have to do that.
    def blit_onto_surface(self, surface, pixel_location_tuple):
        if self and surface and pixel_location_tuple:
            surface.blit(self.image, pixel_location_tuple)

class Connector:
    # create a Connector object. The purpose of a Connector object is to
    # indicate where an Entity will go when reaching an area of the map
    # linked to the Connector.
    # x and y destination coordinates are Tile coordinates, NOT pixels
    def __init__(self,
                dest_region,
                dest_area,
                dest_x_coord,
                dest_y_coord):
        self.dest_region = dest_region
        self.dest_area = dest_area
        self.dest_x_coord = dest_x_coord
        self.dest_y_coord = dest_y_coord

class Map:
    # create a Map object. tile_grid must be a List of List objects, where
    # the inner List object must contain Tile objects, tile_grid will
    # effectively define the tiles for the map.  The grid must be rectangular,
    # meaning each inner List must be of the same length.
    # interactive_obj_dict must be a dict that maps a tuple of integers
    # (representing the X and Y tile coordinates of the map, NOT
    # pixel coordinates) to an Interactive_Object, which is one of:
    #   - Entity
    #   - Obstacle
    #   - Resource
    #   - Item
    # connector_tile_dict must be a dict that maps a tuple of integers
    # (representing the X and Y tile coordinates of the map, NOT
    # pixel coordinates) to a corresponding Connector object
    # adj_map_dict must be a dict that maps a direction ID to a tuple
    # (Map ID, (dest location coordinates) to represent the neighboring map and
    # where the Entity will end up by walking past the map boundary.
    # top_left represents the (x,y) pixel coordinate on the display screen where the
    # top left corner of the map should start. Defaults to (0,0)
    def __init__(self, tile_grid, interactive_obj_dict={}, connector_tile_dict={}, \
                adj_map_dict={}, top_left=(0,0)):
        self.height = 0
        self.width = 0
        self.tile_grid = []
        self.interactive_obj_dict = {}
        self.connector_tile_dict = {}
        self.adj_map_dict = {}
        self.top_left_position = (0,0) # (x,y) tuple of top left, default top viewing

        # (x,y) tuple representing location of protagonist. Default is (0,0)
        self.protagonist_location = (0, 0)

        # maps Tile grid location (x,y) tuple to a
        # [interactive obj, remaining ticks to respawn] list
        # that indicates when the corresponding interactive object should
        # respawn. For delayed respawns only
        self.pending_respawns = {}

        if tile_grid:
            grid_width = len(tile_grid[0])
            grid_height = len(tile_grid)
            valid_grid_dimensions = True

            # ensure our grid dimensions are correct
            for grid_row in tile_grid:
                if grid_width != len(grid_row):
                    # TODO ERROR MESSAGE
                    logger.error("Invalid grid format - check grid dimensions")
                    valid_grid_dimensions = False
                    sys.exit(1)

            if valid_grid_dimensions:
                grid_to_copy = []

                # get the Tile objects and make sure they're all Tiles
                for grid_row in tile_grid:
                    row_to_copy = []
                    for x in grid_row:
                        if not (x.__class__.__name__ == TILE_CLASS):
                            logger.error("Tile grids can only accept Tile objects")
                            valid_grid_dimensions = False
                            sys.exit(1)

                    row_to_copy = [x for x in grid_row]
                    grid_to_copy.append(row_to_copy)

                # save grid
                self.tile_grid = grid_to_copy
                self.height = grid_height
                self.width = grid_width

            # get interactive objects
            if interactive_obj_dict:
                for x, y in interactive_obj_dict.iteritems():
                    self.interactive_obj_dict[x] = y

            # get connector tiles
            if connector_tile_dict:
                for x, y in connector_tile_dict.iteritems():
                    self.connector_tile_dict[x] = y

            # get neighboring maps
            if adj_map_dict:
                for x, y in adj_map_dict.iteritems():
                    self.adj_map_dict[x] = y

    # set top left location (x,y) pixel coordinate tuple
    def set_top_left(self, top_left_position):
        if self and top_left_position:
            self.top_left_position = top_left_position

    # TODO - document
    def set_adj_map(self, direction, dest_map_id, dest_location_coordinate):
        # TODO - more arg checks?
        if self and dest_location_coordinate:
            self.adj_map_dict[direction] = (int(dest_map_id), \
                    (dest_location_coordinate[0], dest_location_coordinate[1]))

    # removes map that is adjacent according to direction
    def remove_adj_map(self, direction):
        if self:
            self.adj_map_dict.pop(direction, None)

    # Sets an interactive object at the specified Tile coordinate
    # location (x, y) tuple on the Map.
    # Returns True if successful, False otherwise. Reasons for
    # failure include:
    #   - Map is empty
    #   - location is invalid
    #   - interactive object already exists at the location
    # Caller will need to reblit the map and update the surface to show
    # the new images
    def set_interactive_object(self, obj_to_respawn, location):
        success = False

        if self and obj_to_respawn and location:
            if self.tile_grid:
                # make sure (x,y) location is in bounds
                if self.width > location[0] and self.height > location[1]:
                    # check if there is already an interactive object at
                    # the (x,y) location
                    if self.interactive_obj_dict.get(location, None):
                        logger.error("Obj already exists at location %s",   \
                            str(location))
                    else:
                        # set object
                        self.interactive_obj_dict[location] = (obj_to_respawn)
                        success = True
                else:
                    logger.error(                                           \
                        "Invalid location %s for set_interactive_object", \
                        str(location))
            else:
                logger.error("Empty map in set_interactive_object")

        return success

    # Spawns an interactive object at the specified Tile coordinate
    # location (x,y) tuple on the Map, and also blits and updates the surface
    #to show the new images.
    # Returns True if spawn was successful, False otherwise. Reasons for
    # failure include:
    #   - Map is empty
    #   - location is invalid
    #   - interactive object already exists at the location
    def spawn_interactive_object(self, game, obj_to_respawn, location):
        # TODO
        return False

    # removes an interactive object from the specified (x,) location on the Map.
    # Returns True if removal was successful, False otherwise. Reasons for
    # failure include:
    #   - Map is empty
    #   - location is invalid
    # If no interactive object exists at the location, the method still returns
    # True.
    # Caller will need to reblit the map and update the surface to show
    # the updated images
    def unset_interactive_object(self, location):
        successful_remove = False

        if self and location:
            if self.tile_grid:
                # make sure (x,y) location is in bounds
                if self.width > location[0] and self.height > location[1]:
                    # remove object if it exists
                    self.interactive_obj_dict.pop(location, None)
                    successful_remove = True
                else:
                    logger.error(                                            \
                        "Invalid location %s for unset_interactive_object", \
                        str(location))
            else:
                logger.error("Empty map in unset_interactive_object")

        return successful_remove

    # removes an interactive object from the specified (x,y) location on the
    # Map.
    # Also blits and updates the surface to show the updated map image.
    # Returns True if removal was successful, False otherwise. Reasons for
    # failure include:
    #   - Map is empty
    #   - location is invalid
    # If no interactive object exists at the location, the method still returns
    # True.
    def remove_interactive_object(self, game, location):
        # # TODO
        return False

    def set_respawn_timer(self, obj_to_respawn, location_tuple, num_ticks):
        success = False
        if self and obj_to_respawn and location_tuple and num_ticks >= 0:
            if self.tile_grid:
                # make sure (x,y) location is in bounds
                if self.width > location[0] and self.height > location[1]:
                    # TODO
                    pass
                else:
                    logger.error(                                           \
                        "Invalid location %s for set_respawn_timer", \
                        str(location))
            else:
                logger.error("Empty map in set_respawn_timer")

        return success

    # checks for pending respawns and updates their time to respawn
    # will respawn objects that have expired respawn timers
    def check_respawns(self, game, elapsed_ticks):
        pass
        # iterate through pending respawns
        """
        updated_pending_respawns = {}
        for location, obj_data in self.pending_respawns.iteritems():
            # get remaining number of ticks to respawn
            remaining_ticks = obj_data[1] - elapsed_ticks
            if remaining_ticks <= 0:
                # item needs to respawn
                item = obj_data[0]
                # TODO
            else:
                obj_data[1] = remaining_ticks
                updated_pending_respawns[location] = obj_data

        self.pending_respawns = updated_pending_respawns
        """

    # blit entire map, including tiles and spawned interactive objects
    # caller needs to update surface after method
    def blit_onto_surface(self, game, pixel_location_tuple):
        if self and game and pixel_location_tuple:
            surface = game.get_main_display_surface()
            start_x = pixel_location_tuple[0]
            start_y = pixel_location_tuple[1]

            # blit tiles
            if self.tile_grid and surface:
                curr_y = start_y
                for grid_row in self.tile_grid:
                    curr_x = start_x
                    for single_tile in grid_row:
                        # blit tile and move to next Tile position
                        single_tile.blit_onto_surface(surface, (curr_x, curr_y))
                        curr_x = curr_x + TILE_SIZE

                    # move to next row of Tiles to blit
                    curr_y = curr_y + TILE_SIZE

                # blit interactive objects
                if self.interactive_obj_dict:
                    for tile_location, obj in self.interactive_obj_dict.iteritems():
                        if tile_location and obj:
                            pos_x = tile_location[0] * TILE_SIZE
                            pos_y = tile_location[1] * TILE_SIZE

                            # blit sprite image
                            obj.blit_onto_surface(surface, (pos_x, pos_y))

    # set protagonist location (x,y) tile tuple, NOT pixel coordinates
    def set_protagonist_tile_location(self, tile_location_tuple):
        if self and tile_location_tuple:
            self.protagonist_location = (tile_location_tuple[0], tile_location_tuple[1])

    # scroll map in the indicated direction for the indicated distance
    # also pass in game object
    # does NOT update the main display - caller will have to do that
    def scroll(self, game, scroll_direction, distance):
        # don't bother if distance <= 0
        if self and game and (distance > 0):
            new_pixel_location = None
            curr_top_left = self.top_left_position

            if scroll_direction == DIR_NORTH:
                # scroll up
                new_pixel_location = (curr_top_left[0], curr_top_left[1] - distance)
            elif scroll_direction == DIR_EAST:
                # scroll right
                new_pixel_location = (curr_top_left[0] + distance, curr_top_left[1])
            elif scroll_direction == DIR_SOUTH:
                new_pixel_location = (curr_top_left[0], curr_top_left[1] + distance)
            elif scroll_direction == DIR_WEST:
                # scroll left
                new_pixel_location = (curr_top_left[0] - distance, curr_top_left[1])
            else:
                # invalid scroll direction
                logger.error("Invalid scroll direction {0}".format(scroll_direction))

            if new_pixel_location:
                # scroll in indicated direction
                self.blit_onto_surface(game, new_pixel_location)

                # update map top left
                self.set_top_left(new_pixel_location)

    # scroll map one Tile distance in the indicated direction.
    # updates main display with each new viewpoint
    # scroll_wait_time is the time (in milliseconds)
    # to wait in between each individual pixel scrolling
    def scroll_single_tile(self, game, direction, scroll_wait_time):
        if self and game and (scroll_wait_time >= 0):
            for i in range(TILE_SIZE):
                # scroll 1 pixel at a time
                game.main_display_screen.fill(adventure.BLACK_COLOR)

                # also updates top view
                self.scroll(game, direction, 1)

                # also blit the top view
                game.blit_top_display()

                # blit protagonist
                # TODO - have designated spot for protagonist?
                if game.protagonist:
                    game.protagonist.blit_onto_surface(game.get_main_display_surface(), \
                        game.center_ow_tile_pixel_location)

                # update main display
                pygame.display.update()

                # wait till next iteration
                pygame.time.wait(scroll_wait_time)



### TILES TO USE ###
TILE_DEFAULT = None
TILE_GRASS_1 = None
TILE_GRASS_2 = None
TILE_GRASS_PLAIN = None
TILE_WATER_NORMAL_1 = None
TILE_SAND = None

### MAPS TO USE ###
REGION_GRASSLANDS_AREA_0_MAP = None

# TODO
def parse_map(map_json_data):
    # TODO
    pass

def build_tiles():
    logger.debug("Building tiles")
    global TILE_DEFAULT
    global TILE_GRASS_1
    global TILE_GRASS_2
    global TILE_GRASS_PLAIN
    global TILE_WATER_NORMAL_1
    global TILE_SAND

    TILE_DEFAULT = Tile()
    TILE_GRASS_1 = Tile(image_path=images.TILE_GRASS_1_PATH)
    TILE_GRASS_2 = Tile(image_path=images.TILE_GRASS_2_PATH)
    TILE_GRASS_PLAIN = Tile(image_path=images.TILE_GRASS_PLAIN_PATH)
    TILE_WATER_NORMAL_1 = Tile(image_path=images.TILE_WATER_NORMAL_1_PATH)
    TILE_SAND = Tile(image_path=images.TILE_SAND_PATH)

def build_maps():
    logger.debug("Building maps")
    global REGION_GRASSLANDS_AREA_0_MAP
    grasslands_area_0_grid = []

    for i in range(40):
        grasslands_area_0_grid.append([TILE_GRASS_1]*50)

    grasslands_area_0_grid[10][15] = TILE_WATER_NORMAL_1
    """
    for i in range(100):
        x = random.randint(0, len(grasslands_area_0_grid[0]) - 1)
        y = random.randint(0, len(grasslands_area_0_grid) - 1)

        if i % 3 == 0:
            grasslands_area_0_grid[y][x] = TILE_SAND
        elif i % 3 == 1:
            grasslands_area_0_grid[y][x] = TILE_GRASS_2
        else:
            grasslands_area_0_grid[y][x] = TILE_WATER_NORMAL_1
    """

    REGION_GRASSLANDS_AREA_0_MAP = Map(grasslands_area_0_grid)
