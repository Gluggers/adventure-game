import logging
import pygame
import random
import sys
import images
import interactive_obj
import tile
from pygame.locals import *

### DIRECTION CONSTANTS ###
DIR_NORTH = 0x0
DIR_EAST = 0x1
DIR_SOUTH = 0x2
DIR_WEST = 0x3

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

### CLASS NAMES ###
MAP_CLASS = 'Map'
REGION_CLASS = 'Region'

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
                        if not (x.__class__.__name__ == tile.TILE_CLASS):
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

    # TODO - document
    def add_adj_map(self, direction, dest_map_id, dest_location_coordinate):
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
    def set_interactive_object(self, obj_to_respawn, tile_location):
        success = False

        if self and obj_to_respawn and tile_location:
            if self.tile_grid:
                # make sure (x,y) location is in bounds
                if self.width > tile_location[0] and self.height > tile_location[1]:
                    # check if there is already an interactive object at
                    # the (x,y) location
                    if self.interactive_obj_dict.get(tile_location, None):
                        logger.error("Obj already exists at location %s",   \
                            str(tile_location))
                    else:
                        # set object
                        self.interactive_obj_dict[tile_location] = (obj_to_respawn)
                        success = True
                else:
                    logger.error(                                           \
                        "Invalid location %s for set_interactive_object", \
                        str(tile_location))
            else:
                logger.error("Empty map in set_interactive_object")

        return success

    # Spawns an interactive object at the specified Tile coordinate
    # location (x,y) tuple on the Map, and also blits.
    # DOES NOT update the display - caller will have to do that
    # TODO CHANGE ^^??
    # Returns True if spawn was successful, False otherwise. Reasons for
    # failure include:
    #   - Map is empty
    #   - location is invalid
    #   - interactive object already exists at the location
    def spawn_interactive_object(self, surface, obj_to_respawn, tile_location):
        # TODO
        return False

    # removes an interactive object from the specified Tile
    # coordinate (x,y) location on the Map.
    # Returns True if removal was successful, False otherwise. Reasons for
    # failure include:
    #   - Map is empty
    #   - location is invalid
    # If no interactive object exists at the location, the method still returns
    # True.
    # Caller will need to reblit the map and update the surface to show
    # the updated images
    def unset_interactive_object(self, tile_location):
        successful_remove = False

        if self and tile_location:
            if self.tile_grid:
                # make sure (x,y) location is in bounds
                if self.width > tile_location[0] and self.height > tile_location[1]:
                    # remove object if it exists
                    self.interactive_obj_dict.pop(tile_location, None)
                    successful_remove = True
                else:
                    logger.error(                                            \
                        "Invalid location %s for unset_interactive_object", \
                        str(tile_location))
            else:
                logger.error("Empty map in unset_interactive_object")

        return successful_remove

    # removes an interactive object from the specified Tile coordinate
    # (x,y) location on the Map.
    # Also blits the surface.
    # DOES NOT update the display - caller will have to do that
    # Returns True if removal was successful, False otherwise. Reasons for
    # failure include:
    #   - Map is empty
    #   - location is invalid
    # If no interactive object exists at the location, the method still returns
    # True.
    def remove_interactive_object(self, surface, tile_location):
        # # TODO
        return False

    # TODO document
    def set_respawn_timer(self, obj_to_respawn, tile_location, num_ticks):
        success = False
        if self and obj_to_respawn and tile_location and num_ticks >= 0:
            if self.tile_grid:
                # make sure (x,y) location is in bounds
                if self.width > tile_location[0] and self.height > tile_location[1]:
                    # TODO
                    pass
                else:
                    logger.error(                                           \
                        "Invalid location %s for set_respawn_timer", \
                        str(tile_location))
            else:
                logger.error("Empty map in set_respawn_timer")

        return success

    # checks for pending respawns and updates their time to respawn
    # will respawn objects that have expired respawn timers
    def check_respawns(self, surface, elapsed_ticks):
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

                # check if protagonist is blocking the location - if so,
                # set item to respawn again in a couple more ticks.
                # if protag isnt' blocking location, then clear the tile
                # (by reblitting the tile object at the location)
                # and add the respawned object back in
            else:
                obj_data[1] = remaining_ticks
                updated_pending_respawns[location] = obj_data

        self.pending_respawns = updated_pending_respawns
        """

    # blit entire map, including tiles and spawned interactive objects
    # caller needs to update surface after method
    def blit_onto_surface(self, surface, pixel_location_tuple):
        if self and surface and pixel_location_tuple:
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
                        curr_x = curr_x + tile.TILE_SIZE

                    # move to next row of Tiles to blit
                    curr_y = curr_y + tile.TILE_SIZE

                # blit interactive objects
                if self.interactive_obj_dict:
                    for tile_location, obj in self.interactive_obj_dict.iteritems():
                        if tile_location and obj:
                            pos_x = tile_location[0] * tile.TILE_SIZE
                            pos_y = tile_location[1] * tile.TILE_SIZE

                            # blit sprite image
                            obj.blit_onto_surface(surface, (pos_x, pos_y))

    """
    # set protagonist location (x,y) tile tuple, NOT pixel coordinates
    def set_protagonist_tile_location(self, tile_location_tuple):
        if self and tile_location_tuple:
            self.protagonist_location = (tile_location_tuple[0], tile_location_tuple[1])
    """

    # scroll map in the indicated direction for the indicated distancet
    # also pass in surface object to blit on and update
    # does NOT update the main display - caller will have to do that
    def scroll(self, surface, scroll_direction, distance):
        # don't bother if distance <= 0
        if self and surface and (distance > 0):
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
                self.blit_onto_surface(surface, new_pixel_location)

                # update map top left
                self.top_left_position = new_pixel_location

### MAPS TO USE ###
REGION_GRASSLANDS_AREA_0_MAP = None

# TODO
def parse_map(map_json_data):
    # TODO
    pass

def build_maps():
    logger.debug("Building maps")
    global REGION_GRASSLANDS_AREA_0_MAP
    grasslands_area_0_grid = []

    for i in range(40):
        grasslands_area_0_grid.append([tile.TILE_GRASS_1]*50)

    grasslands_area_0_grid[10][15] = tile.TILE_WATER_NORMAL_1
    """
    for i in range(100):
        x = random.randint(0, len(grasslands_area_0_grid[0]) - 1)
        y = random.randint(0, len(grasslands_area_0_grid) - 1)

        if i % 3 == 0:
            grasslands_area_0_grid[y][x] = tile.TILE_SAND
        elif i % 3 == 1:
            grasslands_area_0_grid[y][x] = tile.TILE_GRASS_2
        else:
            grasslands_area_0_grid[y][x] = tile.TILE_WATER_NORMAL_1
    """

    REGION_GRASSLANDS_AREA_0_MAP = Map(grasslands_area_0_grid)

# set up logger
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
