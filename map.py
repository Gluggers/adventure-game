import logging
import pygame
import random
import sys
import interactiveobj
import tile
import tiledata
import mapdata
from pygame.locals import *

### CLASS NAMES ###
MAP_CLASS = 'Map'
REGION_CLASS = 'Region'

class Map:
    map_listing = {} # maps map IDs to map objects

    # create a Map object. tile_grid must be a List of List objects, where
    # the inner List object must contain Tile objects, tile_grid will
    # effectively define the tiles for the map.  The grid must be rectangular,
    # meaning each inner List must be of the same length.
    # interactive_obj_dict must be a dict that maps a tuple of integers
    # (representing the X and Y tile coordinates of the map, NOT
    # pixel coordinates) to an Interactive_Object ID which represents one of:
    #   - Entity
    #   - Obstacle
    #   - Resource
    #   - Item
    # connector_tile_dict must be a dict that maps a tuple of integers
    # (representing the X and Y tile coordinates of the map, NOT
    # pixel coordinates) to a corresponding Connector object
    # adj_map_dict must be a dict that maps a direction ID to a tuple
    # (Map ID, dest location coordinate) to represent the neighboring map and
    # where the Entity will end up by walking past the map boundary.
    # top_left represents the (x,y) pixel coordinate on the display screen where the
    # top left corner of the map should start. Defaults to (0,0)
    def __init__(self, map_id, tile_grid, interactive_obj_dict={}, connector_tile_dict={}, \
                adj_map_dict={}, top_left=(0,0)):
        self.height = 0
        self.width = 0
        self.map_id = map_id
        self.tile_grid = []
        self.interactive_obj_dict = {}
        self.connector_tile_dict = {}
        self.adj_map_dict = {}
        self.top_left_position = top_left # (x,y) tuple of top left, default top viewing

        # (x,y) tuple representing location of protagonist. Default is (0,0)
        #self.protagonist_location = (0, 0)

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
                        if not (x and (x.__class__.__name__ == tile.TILE_CLASS)):
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
                for x, y in interactive_obj_dict.items():
                    self.interactive_obj_dict[x] = y

            # get connector tiles
            if connector_tile_dict:
                for x, y in connector_tile_dict.items():
                    self.connector_tile_dict[x] = y

            # get neighboring maps
            if adj_map_dict:
                for x, y in adj_map_dict.items():
                    self.adj_map_dict[x] = y

    # TODO - document
    def add_adjacent_map(self, direction, dest_map_id, dest_location_coordinate):
        # TODO - more arg checks?
        if self and dest_location_coordinate:
            self.adj_map_dict[direction] = (int(dest_map_id), \
                    (dest_location_coordinate[0], dest_location_coordinate[1]))

    # removes map that is adjacent according to direction
    def remove_adjacent_map(self, direction):
        if self:
            self.adj_map_dict.pop(direction, None)

    # get (Map ID, destination tile coordinate) tuple for the map
    # that is adjacent to this map in the given direction.
    # None if no such neighboring map exists
    def get_adjacent_map_info(self, direction):
        return self.adj_map_dict.get(direction, None)

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
        for location, obj_data in self.pending_respawns.items():
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

    # returns True if the tile position to check is within current map
    # boundaries
    def location_within_bounds(self, tile_pos_to_check):
        x_pos = tile_pos_to_check[0]
        y_pos = tile_pos_to_check[1]

        return  (x_pos >= 0) and            \
                (y_pos >= 0) and            \
                (x_pos < self.width) and    \
                (y_pos < self.height)

    def get_tile_from_pos(self, tile_pos):
        ret_tile = None

        if self.location_within_bounds(tile_pos):
            # y,x
            ret_tile = self.tile_grid[tile_pos[1]][tile_pos[0]]

        return ret_tile

    def valid_transportation(self, dest_tile_pos, transport_flag):
        ret_val = 0x0
        dest_tile = self.get_tile_from_pos(dest_tile_pos)

        if dest_tile:
            ret_val = dest_tile.valid_transportation(transport_flag)

        return ret_val

    def blit_tile(self, surface, tile_coordinate, dest_top_left):
        if surface and tile_coordinate and dest_top_left and self.location_within_bounds(tile_coordinate):
            # y, x
            tile_obj = self.get_tile_from_pos(tile_coordinate)

            if tile_obj:
                tile_obj.blit_onto_surface(surface, dest_top_left)


    # blit entire map, including tiles and spawned interactive objects
    # caller needs to update surface after method
    # tile_subset_rect is rect of tile coordinates that indicates which
    # tiles to blit, rather than blitting the whole map. Setting to None
    # will blit the whole map
    def blit_onto_surface(self, surface, top_left_pixel_tuple, tile_subset_rect=None):
        if self and surface and top_left_pixel_tuple and self.tile_grid:
            tile_subset = (0, 0, self.width, self.height)

            if tile_subset_rect:
                tile_subset = tile_subset_rect

            start_tile_x = tile_subset[0]
            start_tile_y = tile_subset[1]
            end_tile_x = start_tile_x + tile_subset[2] - 1
            end_tile_y = start_tile_y + tile_subset[3] - 1

            if (start_tile_x >= 0)                          \
                    and (start_tile_y >= 0)                 \
                    and (end_tile_x <= self.width)          \
                    and (end_tile_y <= self.height)         \
                    and (end_tile_x >= start_tile_x)        \
                    and (end_tile_y >= start_tile_y):
                start_pixel_x = top_left_pixel_tuple[0] + (start_tile_x*tile.TILE_SIZE)
                start_pixel_y = top_left_pixel_tuple[1] + (start_tile_y*tile.TILE_SIZE)

                # blit tiles
                curr_pixel_y = start_pixel_y
                for grid_row in range(start_tile_y, end_tile_y + 1):
                    curr_pixel_x = start_pixel_x
                    for tile_index in range(start_tile_x, end_tile_x + 1):
                        single_tile = self.tile_grid[grid_row][tile_index]
                        single_tile.blit_onto_surface(surface, (curr_pixel_x, curr_pixel_y))
                        curr_pixel_x = curr_pixel_x + tile.TILE_SIZE
                    curr_pixel_y = curr_pixel_y + tile.TILE_SIZE



            """
            start_x = top_left_pixel_tuple[0]
            start_y = top_left_pixel_tuple[1]

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
                # TODO - should interactive obj dict map tile location to obj
                # ID?
                if self.interactive_obj_dict:
                    for tile_location, obj in self.interactive_obj_dict.items():
                        if tile_location and obj:
                            pos_x = tile_location[0] * tile.TILE_SIZE
                            pos_y = tile_location[1] * tile.TILE_SIZE

                            # blit sprite image
                            # TODO
                            #obj.blit_onto_surface(surface, (pos_x, pos_y + tile.TILE_SIZE))
            """

    # scroll map in the indicated direction for the indicated distancet
    # also pass in surface object to blit on and update
    # does NOT update the main display - caller will have to do that
    def scroll(self, surface, scroll_direction, distance, tile_subset_rect=None):
        # don't bother if distance <= 0
        if self and surface and (distance > 0):
            new_pixel_location = None
            curr_top_left = self.top_left_position

            if scroll_direction == mapdata.DIR_NORTH:
                # scroll up
                new_pixel_location = (curr_top_left[0], curr_top_left[1] - distance)
            elif scroll_direction == mapdata.DIR_EAST:
                # scroll right
                new_pixel_location = (curr_top_left[0] + distance, curr_top_left[1])
            elif scroll_direction == mapdata.DIR_SOUTH:
                new_pixel_location = (curr_top_left[0], curr_top_left[1] + distance)
            elif scroll_direction == mapdata.DIR_WEST:
                # scroll left
                new_pixel_location = (curr_top_left[0] - distance, curr_top_left[1])
            else:
                # invalid scroll direction
                logger.error("Invalid scroll direction {0}".format(scroll_direction))

            if new_pixel_location:
                #logger.debug("Scrolling. tile subset rect: {0}".format(tile_subset_rect))
                # scroll in indicated direction
                self.blit_onto_surface(                                 \
                    surface,                                            \
                    new_pixel_location,                                 \
                    tile_subset_rect=tile_subset_rect                   \
                )

                # update map top left
                self.top_left_position = new_pixel_location

    # builds map based on given map ID. Returns map if valid map ID.
    # Adds the map to the class map_listing variable if a new
    # map was created
    # if the corresponding map already exists, the method will
    # return that map rather than making a new one
    @classmethod
    def map_factory(cls, map_id):
        ret_map = None

        # check if we already have the map
        map_from_listing = Map.map_listing.get(map_id, None)

        if map_from_listing:
            ret_map = map_from_listing
        else:
            # need to make map
            ret_map_data = mapdata.MAP_DATA.get(map_id, None)
            if (ret_map_data):
                logger.debug("Parsing map data")
                tile_grid_str_list = ret_map_data.get(mapdata.MAP_TILE_GRID_FIELD, None)
                tile_grid_legend = ret_map_data.get(mapdata.MAP_TILE_GRID_KEY_FIELD, None)

                map_tile_grid = Map.parse_tile_grid(tile_grid_str_list, tile_grid_legend)

                if map_tile_grid:
                    logger.debug("making map")
                    ret_map = Map(                                          \
                        map_id,                                             \
                        map_tile_grid,                                      \
                        interactive_obj_dict=ret_map_data.get(              \
                            mapdata.MAP_INTER_OBJ_DICT_FIELD, {}            \
                        ),                                                  \
                        connector_tile_dict=ret_map_data.get(               \
                            mapdata.MAP_CONNECTOR_TILE_DICT_FIELD, {}       \
                        ),                                                  \
                        adj_map_dict=ret_map_data.get(                      \
                            mapdata.MAP_ADJ_MAP_DICT_FIELD, {}              \
                        )                                                   \
                    )

                    if ret_map:
                        # add map to listing
                        Map.map_listing[map_id] = ret_map
                    else:
                        logger.warn("failed to make map with id {0}".format(map_id))

        return ret_map

    # TODO document
    @classmethod
    def parse_tile_grid(cls, tile_grid_str_list, legend):
        ret_grid = None
        failed = False

        if tile_grid_str_list and legend:
            curr_grid = []

            for row_str in tile_grid_str_list:
                curr_row = []
                if not failed:
                    for tile_char in row_str:
                        curr_id = legend.get(tile_char, None)
                        if curr_id:
                            curr_tile = tile.Tile.get_tile(curr_id)
                            if curr_tile:
                                curr_row.append(curr_tile)
                            else:
                                logger.warn("No tile found for tile id {0}".format(curr_id))
                                failed = True
                                break
                        else:
                            logger.warn("No tile id found for tile char {0}".format(tile_char))
                            failed = True
                            break
                    if curr_row:
                        curr_grid.append(curr_row)
                    else:
                        logger.warn("No tiles added to row")
                        failed = True
                        break
            if not failed:
                ret_grid = curr_grid

        return ret_grid

    @classmethod
    def get_map(cls, map_id):
        ret_map = Map.map_listing.get(map_id, None)

        if not ret_map:
            logger.warn("Get_map: No map found for map id {0}".format(map_id))

        return ret_map

    # TODO
    @classmethod
    def parse_map(cls, map_json_data):
        # TODO
        pass

    @classmethod
    def build_maps(cls):
        logger.debug("Building maps")
        """
        grasslands_area_0_grid = []
        grasslands_area_1_grid = []

        # R0_A0
        for i in range(15):
            grasslands_area_0_grid.append([tile.Tile.get_tile(tiledata.TILE_GRASS_PLAIN_ID)]*15)

        for i in range(100):
            x = random.randint(0, len(grasslands_area_0_grid[0]) - 1)
            y = random.randint(0, len(grasslands_area_0_grid) - 1)

            if i % 4 == 0:
                grasslands_area_0_grid[y][x] = tile.Tile.get_tile(tiledata.TILE_GRASS_FLOWERS_ID)
            elif i % 4 == 1:
                grasslands_area_0_grid[y][x] = tile.Tile.get_tile(tiledata.TILE_GRASS_2_ID)
            elif i % 4 == 2:
                grasslands_area_0_grid[y][x] = tile.Tile.get_tile(tiledata.TILE_GRASS_1_ID)
            else:
                grasslands_area_0_grid[y][x] = tile.Tile.get_tile(tiledata.TILE_WATER_NORMAL_1_ID)

        # R0_A1
        for i in range(30):
            grasslands_area_1_grid.append([tile.Tile.get_tile(tiledata.TILE_GRASS_1_ID)]*50)

        grasslands_area_1_grid[10][15] = tile.Tile.get_tile(tiledata.TILE_WATER_NORMAL_1_ID)

        Map.map_listing[R0_A0_ID] = Map(R0_A0_ID, grasslands_area_0_grid)
        Map.map_listing[R0_A1_ID] = Map(R0_A1_ID, grasslands_area_1_grid)
        """
        for map_id in mapdata.MAP_DATA:
            Map.map_factory(map_id)

# set up logger
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
