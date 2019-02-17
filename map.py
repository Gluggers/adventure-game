import logging
import pygame
import random
import sys
import interactiveobj
import objdata
import tile
import tiledata
import mapdata
import imageids
import viewingdata
from pygame.locals import *

### CLASS NAME ###
MAP_CLASS = 'Map'

class Map:
    # maps map IDs to map objects
    map_listing = {}

    ### INITIALIZER METHODS ###

    # Create a Map object.
    # tile_grid must be a List of List of Tiles that contains the tiles for
    # the map. tile_grid must have a valid rectangular dimension, meaning
    # each inner List must be of the same size.  tile_grid can contain
    # None in the inner List to represent missing Tiles.
    #
    # connector_tile_dict must be a dict that maps a tuple of integers
    # (representing the X and Y tile coordinates of the map, NOT
    # pixel coordinates) to a corresponding Connector object.
    #
    # adj_map_dict must be a dict that maps a direction ID to a tuple
    # (Map ID, dest location coordinate) to represent the neighboring map and
    # where the Entity will end up by walking past the map boundary.
    #
    # top_left represents the (x,y) pixel coordinate on the display screen where the
    # top left corner of the map should start.
    def __init__(self, map_id, tile_grid, connector_tile_dict={}, \
                adj_map_dict={}, top_left=(0,0)):
        self.height = 0
        self.width = 0
        self.map_id = map_id
        self.tile_grid = []
        self.connector_tile_dict = {}
        self.adj_map_dict = {}
        self.top_left_position = top_left

        # maps bottom left tile coordinate tuple to
        # a length-2 list of [object ID, collision tile set],
        # where collision tile set is a set of Tile coordinates that
        # make up the object's collision rect
        self.bottom_left_tile_obj_mapping = {}

        # dict that maps a Tile coordinate tuple to the bottom left
        # tile coordinate tuple of the object whose collision rect occupies
        # that tile. If no object occupies the Tile, then the dict
        # should not have an entry for that Tile location.
        self.occupied_tile_dict = {}

        # (x,y) tuple representing location of protagonist.
        self._protagonist_location = None

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
                # build tile grid
                grid_to_copy = []

                # get the Tile objects and make sure they're all Tiles
                for grid_row in tile_grid:
                    row_to_copy = []
                    for x in grid_row:
                        if (x is not None) and (x.__class__.__name__ != tile.TILE_CLASS):
                            logger.error("Tile grids can only accept None or Tile objects")
                            valid_grid_dimensions = False
                            sys.exit(1)

                    row_to_copy = [x for x in grid_row]
                    grid_to_copy.append(row_to_copy)

                # save grid
                self.tile_grid = grid_to_copy
                self.height = grid_height
                self.width = grid_width

                # get connector tiles
                if connector_tile_dict:
                    for x, y in connector_tile_dict.items():
                        self.connector_tile_dict[x] = y

                # get neighboring maps
                if adj_map_dict:
                    for x, y in adj_map_dict.items():
                        self.adj_map_dict[x] = y

    # interactive_obj_dict must be a dict that maps a tuple of integers
    # (representing the X and Y tile coordinates of the map, NOT
    # pixel coordinates), representing the bottom left tiles of interactive
    # objects, to the interactive object ID.
    # The caller must take care to ensure that the objects do not collide
    # with each other when all fully placed on the map - otherwise, the method
    # will not fully place all the objects
    # This method must only be called during the map factory method
    # Returns True if all items set successfully, false otherwise
    def init_interactive_obj_dict(self, interactive_obj_dict):
        successful = True
        # set up initial interactive objects for map
        for bottom_left_tile_loc, object_id in interactive_obj_dict.items():
            if (object_id is not None) and bottom_left_tile_loc:
                logger.debug("About to set object {0} at {1}".format(object_id, bottom_left_tile_loc))
                if not self.set_interactive_object(object_id, bottom_left_tile_loc):
                    successful = False
                    logger.warn("Could not place object {0} at {1}".format(object_id, bottom_left_tile_loc))
        return successful

    ### GETTERS AND SETTERS ###

    @property
    def protagonist_location(self):
        """Return the protagonist location on map."""
        return self._protagonist_location

    @protagonist_location.setter
    def protagonist_location(self, new_location):
        """Set the protagonist location on map."""
        if new_location:
            if self._protagonist_location:
                # Clear old tile location
                self.bottom_left_tile_obj_mapping.pop(self._protagonist_location, None)
                self.occupied_tile_dict.pop(self._protagonist_location, None)

            # Check if new location is occupied
            if self.bottom_left_tile_obj_mapping.get(new_location, None) \
                    or self.occupied_tile_dict.get(new_location, None):
                logger.error("Cannot move protag from {0} to {1}".format(self._protagonist_location, new_location))
            else:
                # Mark new location as occupied
                self.bottom_left_tile_obj_mapping[new_location] = [objdata.PROTAGONIST_ID, set([new_location])]
                self.occupied_tile_dict[new_location] = new_location

                logger.debug("Moving protag away from {0} to {1}".format(self._protagonist_location, new_location))

                self._protagonist_location = new_location

    ### ADJACENT MAP METHODS ###

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


    ### OBJECT SETTING/REMOVING METHODS ###

    # Sets an interactive object corresponding to obj_id
    # such that the bottom left tile of the
    # object is at the at the specified Tile coordinate
    # location (x, y) tuple on the Map.
    # Returns True if successful, False otherwise. Reasons for
    # failure include:
    #   - Map is empty
    #   - location is invalid
    #   - interactive object already exists at the location
    # Caller will need to reblit the map and update the surface to show
    # the new images
    def set_interactive_object(self, obj_id, bottom_left_tile_loc):
        success = False
        can_set = True
        obj_to_set = interactiveobj.Interactive_Object.get_interactive_object(obj_id)

        if not obj_to_set:
            logger.debug("Could not find object with ID {0}".format(obj_id))

        if self and obj_to_set and bottom_left_tile_loc and self.tile_grid:
            # Check that each tile in the colliion rect is within map
            # bounds and is not already occupied by another interactive
            # object.
            collision_tile_set = obj_to_set.get_collision_tile_set(bottom_left_tile_loc)
            for tile_loc in collision_tile_set:
                curr_tile_x = tile_loc[0]
                curr_tile_y = tile_loc[1]

                if self.location_within_bounds(tile_loc):
                    # We are within map bounds. Check for occupied tiles.
                    if self.tile_occupied(tile_loc):
                        can_set = False
                        # tile is occupied
                        logger.error(                               \
                            "Obj already exists at location %s",    \
                            str(tile_loc)                           \
                        )
                    # TODO check if the tile is walkable before putting an object on it?
                else:
                    can_set = False
                    logger.error(                                           \
                        "Out of bounds location at: {0} ".format(tile_loc)  \
                    )
            # Set if we can
            if can_set:
                # Associate object id and collision rect with the bottom left tile coordinate.
                self.bottom_left_tile_obj_mapping[bottom_left_tile_loc] = [obj_id, collision_tile_set]
                logger.debug("Setting obj ID {0} to bottom left tile {1}".format(obj_to_set.object_id, bottom_left_tile_loc))

                # Mark all tiles within object's collision rect as occupied
                for tile_loc in collision_tile_set:
                    self.occupied_tile_dict[tile_loc] = bottom_left_tile_loc
                    logger.debug("Marking {0} as occupied".format(tile_loc))

                success = True

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

    # Removes an interactive object that occupies the tile_location
    # coordinate (x,y) on the Map. Note that for interactive objects
    # that take up more than one tile, passing in just one of the tiles
    # will remove the object.
    # Returns True if removal was successful, False otherwise. Reasons for
    # failure include:
    #   - Map is empty
    #   - location is invalid
    #   - invalid or no tile location specified
    # If no interactive object has a bottom left tile at the location,
    # the method still returns True.
    # Caller will need to reblit the map and update the surface to show
    # the updated images
    def unset_interactive_object(self, tile_location):
        successful_remove = False

        if self and tile_location and self.tile_grid:
            # make sure (x,y) location is in bounds
            if self.location_within_bounds(tile_location):
                # Check if the tile location maps to an object's
                # bottom left tile location.
                successful_remove = True
                bottom_left_tile_loc = self.occupied_tile_dict.get(tile_location, None)

                if bottom_left_tile_loc:
                    # Get object to remove and remove from map
                    obj_info =                                      \
                        self.bottom_left_tile_obj_mapping.pop(      \
                            bottom_left_tile_loc,                   \
                            None                                    \
                        )
                    if obj_info:
                        obj_id = obj_info[0]
                        collision_set = obj_info[1]

                        logger.debug("Removing object {0} from {1}".format(obj_id, bottom_left_tile_loc))

                        # Clear object's collision tiles on map
                        for tile_loc in collision_set:
                            self.occupied_tile_dict.pop(tile_loc, None)
                            logger.debug("Freed tile {0}".format(tile_loc))

            else:
                logger.error(                                            \
                    "Invalid location %s for unset_interactive_object", \
                    str(tile_location))


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

    ### OBJECT SEARCH METHODS ###

    # Returns None if invalid direction, invalid initial tile position,
    # or adjacent tile is out of bounds (does not look for adjacent maps).
    def get_adjacent_tile_position(self, tile_position, adjacent_direction):
        ret_tile_pos = None

        if tile_position and (adjacent_direction is not None):
            # Only proceed if we're within bounds.
            if self.location_within_bounds(tile_position):
                adj_tile_pos = None

                if adjacent_direction == mapdata.DIR_NORTH:
                    # Adjacent tile position is above.
                    adj_tile_pos = (tile_position[0], tile_position[1] - 1)
                elif adjacent_direction == mapdata.DIR_SOUTH:
                    # Adjacent tile position is below.
                    adj_tile_pos = (tile_position[0], tile_position[1] + 1)
                elif adjacent_direction == mapdata.DIR_EAST:
                    # Adjacent tile position is to the right.
                    adj_tile_pos = (tile_position[0] + 1, tile_position[1])
                elif adjacent_direction == mapdata.DIR_WEST:
                    # Adjacent tile position is to the left.
                    adj_tile_pos = (tile_position[0] - 1, tile_position[1])

                if adj_tile_pos and self.location_within_bounds(adj_tile_pos):
                    ret_tile_pos = adj_tile_pos

        return ret_tile_pos

    # Returns None if invalid direction, invalid initial tile position,
    # or adjacent tile is out of bounds (does not look for adjacent maps).
    def get_adjacent_tile(self, tile_position, adjacent_direction):
        ret_tile = None

        if tile_position and (adjacent_direction is not None):
            # Get adjacent tile position, and then get tile from there.
            adj_tile_pos = self.get_adjacent_tile_position(
                tile_position,
                adjacent_direction
            )

            if adj_tile_pos:
                ret_tile = self.get_tile_from_pos(adj_tile_pos)

        return ret_tile

    def get_object_occupying_tile(self, tile_position):
        occupying_object = None

        if tile_position and self.location_within_bounds(tile_position):
            # Check if the tile is part of an object's collision space.
            bottom_left_tile_pos = self.occupied_tile_dict.get(tile_position, None)

            if bottom_left_tile_pos:
                # Get ID of object occupying the space.
                obj_id = self.bottom_left_tile_obj_mapping.get(bottom_left_tile_pos, [None])[0]

                if obj_id:
                    # Get object.
                    occupying_object = interactiveobj.Interactive_Object.get_interactive_object(obj_id)

        return occupying_object



    """
    def change_protagonist_location(self, new_location):
        if new_location:
            if self._protagonist_location:
                # Clear old tile location
                self.bottom_left_tile_obj_mapping.pop(self._protagonist_location, None)
                self.occupied_tile_dict.pop(self._protagonist_location, None)

            # Mark new location as occupied
            self.bottom_left_tile_obj_mapping[new_location] = [objdata.PROTAGONIST_ID, set([new_location])]
            self.occupied_tile_dict[new_location] = new_location

            logger.debug("Moving protag away from {0} to {1}".format(self._protagonist_location, new_location))

            self._protagonist_location = new_location
    """

    ### OBJECT RESPAWNING METHODS ###

    # TODO document
    def set_respawn_timer(self, obj_to_respawn, tile_location, num_ticks):
        success = False
        if self and obj_to_respawn and tile_location and num_ticks >= 0:
            if self.tile_grid:
                # make sure (x,y) location is in bounds
                if self.location_within_bounds(tile_location):
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

    ### TILE-RELATED METHODS ###

    def tile_occupied(self, tile_loc):
        occupied = False

        if tile_loc and self.occupied_tile_dict.get(tile_loc, None):
            occupied = True

        return occupied

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

    ### BLIT METHODS ###

    def blit_tile(self, surface, tile_coordinate, dest_top_left):
        if surface and tile_coordinate and dest_top_left and self.location_within_bounds(tile_coordinate):
            # y, x
            tile_obj = self.get_tile_from_pos(tile_coordinate)

            if tile_obj:
                tile_obj.blit_onto_surface(surface, dest_top_left)

    # Blits tiles starting at current top left position
    # caller needs to update surface after method
    # tile_subset_rect is rect of tile coordinates that indicates which
    # tiles to blit, rather than blitting the whole map. Setting to None
    # will blit the whole map
    def blit_tiles(self, surface, tile_subset_rect=None):
        if surface and self.tile_grid and self.top_left_position:
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
                start_pixel_x = self.top_left_position[0] + (start_tile_x*tile.TILE_SIZE)
                start_pixel_y = self.top_left_position[1] + (start_tile_y*tile.TILE_SIZE)

                # Blit tiles.
                curr_pixel_y = start_pixel_y
                for grid_row in range(start_tile_y, end_tile_y + 1):
                    curr_pixel_x = start_pixel_x
                    for tile_index in range(start_tile_x, end_tile_x + 1):
                        single_tile = self.tile_grid[grid_row][tile_index]
                        single_tile.blit_onto_surface(surface, (curr_pixel_x, curr_pixel_y))
                        curr_pixel_x = curr_pixel_x + tile.TILE_SIZE
                    curr_pixel_y = curr_pixel_y + tile.TILE_SIZE

    # Blits spawned interactive objects starting at current
    # top left position of map
    # Caller needs to update surface after method
    # tile_subset_rect is rect of tile coordinates that indicates which
    # tiles to include for blitting, rather than blitting the whole map.
    # Setting to None will blit all the current spawned objects on
    # the map.
    def blit_interactive_objects(self, surface, tile_subset_rect=None):
        if surface and self.tile_grid and self.top_left_position:
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
                # Check if the Tile is occupied. Go by order of bottom left tile
                for grid_row in range(start_tile_y, end_tile_y + 1):
                    for tile_index in range(start_tile_x, end_tile_x + 1):
                        tile_loc = (tile_index, grid_row)

                        # Check if this tile is a bottom left tile for an
                        # interactive object.
                        obj_info = self.bottom_left_tile_obj_mapping.get(tile_loc, None)
                        if obj_info:
                            obj_to_blit =                       \
                                interactiveobj.Interactive_Object.get_interactive_object(obj_info[0])

                            if obj_to_blit:
                                bottom_left_pixel = None

                                if (obj_info[0] == objdata.PROTAGONIST_ID):
                                    bottom_left_pixel = viewingdata.CENTER_OW_TILE_BOTTOM_LEFT
                                    obj_to_blit.blit_onto_surface(
                                        surface,
                                        bottom_left_pixel=bottom_left_pixel
                                    )
                                else:
                                    bottom_left_pixel = (                           \
                                        self.top_left_position[0]                   \
                                            + (tile_loc[0] * tile.TILE_SIZE),       \
                                        self.top_left_position[1]                   \
                                            + ((tile_loc[1] + 1) * tile.TILE_SIZE)  \
                                    )

                                    # Blit the object.
                                    # Use default image ID for overworld.
                                    # TODO - change this image ID depending
                                    # on object type?
                                    obj_to_blit.blit_onto_surface(
                                        surface,
                                        image_type_id=imageids.OW_IMAGE_ID_DEFAULT,
                                        bottom_left_pixel=bottom_left_pixel
                                    )


    # blit entire map, including tiles and spawned interactive objects
    # Starts at the map's current top left position
    # caller needs to update surface after method
    # tile_subset_rect is rect of tile coordinates that indicates which
    # tiles and objects to blit, rather than blitting the whole map.
    # Setting to None will blit the whole map
    def blit_onto_surface(self, surface, tile_subset_rect=None):
        if self and surface and self.top_left_position and self.tile_grid:
            # Blit the tiles.
            self.blit_tiles(surface, tile_subset_rect=tile_subset_rect)

            # Next, blit the objects
            self.blit_interactive_objects(
                surface,
                tile_subset_rect=tile_subset_rect
            )

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
                # Update map top left and blit map.
                self.top_left_position = new_pixel_location
                self.blit_onto_surface(                                 \
                    surface,                                            \
                    tile_subset_rect=tile_subset_rect                   \
                )

    # Refreshes map. Check for respawns.
    # Does not reblit map - caller will have to do that.
    def refresh_self(
                self,
                #surface,
                #tile_subset_rect=None,
            ):
        # TODO - check for respawns
        pass
        """
        if surface:
            self.blit_onto_surface(                                 \
                surface,                                            \
                tile_subset_rect=tile_subset_rect                   \
            )
        """

    ### CLASS METHODS ###

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
                        connector_tile_dict=ret_map_data.get(               \
                            mapdata.MAP_CONNECTOR_TILE_DICT_FIELD, {}       \
                        ),                                                  \
                        adj_map_dict=ret_map_data.get(                      \
                            mapdata.MAP_ADJ_MAP_DICT_FIELD, {}              \
                        )                                                   \
                    )
                    # TODO - separate out the above into separate init methods
                    # like with the interactive objects?

                    if ret_map:
                        # set up initial interactive objects for map
                        if ret_map.init_interactive_obj_dict(               \
                                    ret_map_data.get(                       \
                                        mapdata.MAP_INTER_OBJ_DICT_FIELD,   \
                                        {}                                  \
                                    )                                       \
                                ):
                            logger.debug("Successfully initialized interactive objects on map {0}".format(map_id))
                        else:
                            logger.warn("Failed to initialize all interactive objects on map {0}".format(map_id))
                        # Add map to listing,
                        # even if the objects weren't all successfully initialized.
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

    @classmethod
    def build_maps(cls):
        logger.debug("Building maps")

        for map_id in mapdata.MAP_DATA:
            if not Map.map_factory(map_id):
                logger.error("Could not construct map with ID {0}".format(map_id))

# set up logger
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
