# -*- coding: utf-8 -*-
"""Contains functions and constants for Tile objects."""

import logging
import sys
import pygame
import imagepaths
import tiledata

### TILE CONSTANTS ###
TILE_SIZE = 32
TILE_CLASS = 'Tile'

LOGGER = None

class Tile(object):
    """A class used to represent map tiles for the overworld.

    Each Tile ID as defined in tiledata.py should map to a single Tile object
    that should not change.

    To create Tiles at the initial game loading, call the class method
    build_tiles. To build an individual Tile, use the class factory
    method tile_factory.  To retrieve a Tile object by a given ID, use
    the class method get_tile.

    Attributes:
        tile_id: integer ID number for the Tile.
        image_list: list of pygame Surface representing the Tile images.
        image_sequence_duration: duration in milliseconds for the image
            sequence for the Tile (in other words, how many milliseconds
            it takes for the Tile to cycle through its image list.)
            If None, only the first image in the image list will be used.
        allowed_transport: integer representing OR-ed integer flags to
            indicate allowed transportation methods (as defined in tiledata)
            for this Tile.
    """

    # Maps tile IDs to Tile objects.
    tile_listing = {}

    def __init__(
            self,
            tile_id,
            image_path_list=None,
            image_sequence_duration=None,
            allowed_transport=tiledata.DEFAULT_TRANSPORTATION,
        ):
        """Creates and returns a Tile object.

        Args:
            tile_id: integer representing the unique ID number of the
                Tile. There should only be one Tile object for a tile_id
                number, and only one Tile object for each type of tile.
            image_path_list: list of Strings indicating the file paths for the
                image files containing the images for the Tile.
            image_sequence_duration: duration in milliseconds for the image
                sequence for the Tile (in other words, how many milliseconds
                it takes for the Tile to cycle through its image list.)
                If None, only the first image in the image list will be used.
            allowed_transport: integer representing OR-ed integer boolean
                flags from tiledata. These boolean flags determine which
                types of transportation are allowed on the Tile.
                Current valid options are:

                    1. NO_TRANSPORT_F: no type of transport is allowed.
                        Do not OR this with other flags.
                    2. WALKABLE_F: walking is allowed.
                    3. CANOEABLE_F: canoeing is allowed.
                    4. SAILABLE_F: sailing is allowed.
                    5. FLYABLE_F: flying is allowed.

                To allow multiple types of transportation, pass in
                bitwise ORed flags, such as WALKABLE_F | CANOEABLE_F.
                The default value is WALKABLE_F | FLYABLE_F.
        """
        # Each tile_id should map to a distinct Tile.
        self._tile_id = tile_id

        self._image_sequence_duration = image_sequence_duration

        # Represents the base terrain image (e.g. grass, water).
        self._image_list = []
        if image_path_list:
            for image_path in image_path_list:
                rendered_image = pygame.image.load(image_path).convert_alpha()
                if rendered_image:
                    self._image_list.append(rendered_image)
                else:
                    LOGGER.error(
                        "Error rendering tile image %s",
                        image_path
                    )
                    sys.exit(2)
        else:
            # Use default tile image.
            image_path = imagepaths.TILE_DEFAULT_PATH
            rendered_image = pygame.image.load(
                image_path
            ).convert_alpha()

            if rendered_image:
                self._image_list.append(rendered_image)
            else:
                LOGGER.error(
                    "Error rendering tile image %s",
                    image_path
                )
                sys.exit(2)

        self._allowed_transport = allowed_transport

        self._individual_image_duration = None
        if self._image_sequence_duration and self._image_list:
            self._individual_image_duration = int(
                self._image_sequence_duration / len(self._image_list)
            )

    @property
    def tile_id(self):
        """Returns tile ID number for Tile."""
        return self._tile_id

    @property
    def image_list(self):
        """Returns Tile image list."""
        return self._image_list

    @property
    def image_sequence_duration(self):
        """Returns Tile image sequence duration."""
        return self._image_sequence_duration

    @property
    def allowed_transport(self):
        """Returns the allowed transportation for the Tile."""
        return self._allowed_transport

    def valid_transportation(self, transportation_flag):
        """Checks if the transportation method is allowed.

        Args:
            self: calling object.
            transportation_flag: integer flag representing the
                transportation method to check.

        Returns:
            True if the transportation method is allowed for the calling
            Tile, False otherwise.
        """
        return bool(transportation_flag & self._allowed_transport) \
            or (transportation_flag == self._allowed_transport)

    def blit_tile(
            self,
            surface,
            top_left_pixel_tuple,
            blit_time_ms=None,
        ):
        """Blits Tile at the provided top left pixel.

        Does not update the surface display - caller will have to do that.
        If the Tile has multiple images in the image sequence and has an
        image sequence duration, the image in the sequence will be determined
        based on blit_time_ms and the Tile's image_sequence_duration attribute.

        Args:
            self: calling object.
            surface: pygame Surface object to blit the Tile onto.
            top_left_pixel_tuple: tuple containing the x,y pixel coordinates
                to place the top left corner of the Tile.
            blit_time_ms: the system time in milliseconds to use for blitting
                the Tile. This time is used to determine which image to use
                from the Tile's image sequence. If None, or if the Tile doesn't
                have an image sequence duration, only the first Tile image
                will be blitted.
        """
        if self and surface and top_left_pixel_tuple:
            # Determine image to blit.
            image_to_blit = None

            if not self._image_sequence_duration:
                image_to_blit = self._image_list[0]
            elif not blit_time_ms:
                image_to_blit = self._image_list[0]
            else:
                image_to_blit = self._image_list[
                    (blit_time_ms // self._individual_image_duration) \
                    % len(self._image_list)
                ]

            if image_to_blit:
                surface.blit(image_to_blit, top_left_pixel_tuple)

    @classmethod
    def tile_factory(cls, tile_id):
        """Factory method for creating Tile objects.

        Builds Tile based on the given Tile ID, and adds Tile to the
        class tile listing if a new valid tile was created.
        If the corresponding tile already exists, the method
        will simply return the original Tile rather than creating a new one.

        Args:
            cls: calling Class.
            tile_id: Tile ID number corresponding to the Tile to create.

        Returns:
            Tile object for the corresponding Tile ID.
            Returns None if something went wrong.
        """
        ret_tile = None

        # Check if the corresponding Tile has already been made.
        tile_from_listing = Tile.tile_listing.get(tile_id, None)

        if tile_from_listing:
            ret_tile = tile_from_listing
        else:
            # We need to make Tile. Grab tile data.
            ret_tile_data = tiledata.TILE_DATA.get(tile_id, None)
            if ret_tile_data:
                tile_image_paths = ret_tile_data.get(
                    tiledata.TILE_IMAGE_PATHS_FIELD,
                    imagepaths.TILE_DEFAULT_PATH
                )

                tile_transport_flag = ret_tile_data.get(
                    tiledata.TILE_ALLOWED_TRANSPORT_FIELD,
                    tiledata.DEFAULT_TRANSPORTATION
                )

                tile_image_seq_duration = ret_tile_data.get(
                    tiledata.TILE_IMAGE_SEQUENCE_DURATION_FIELD,
                    None
                )

                ret_tile = Tile(
                    tile_id,
                    image_path_list=tile_image_paths,
                    image_sequence_duration=tile_image_seq_duration,
                    allowed_transport=tile_transport_flag,
                )

                # Record the Tile in the class listing.
                if ret_tile:
                    Tile.tile_listing[tile_id] = ret_tile
                else:
                    LOGGER.warn("Could not get tile for id %d.", tile_id)

        return ret_tile

    @classmethod
    def get_tile(cls, tile_id):
        """Gets the Tile corresponding to the given ID.

        Gets the Tile corresponding to the given ID. Returns None if such
        a tile does not exist.

        Does not create a new Tile. Use Tile.tile_factory to create a Tile.

        Args:
            cls: calling Class.
            tile_id: Tile ID number for the Tile to fetch.

        Returns:
            Tile object for the corresponding Tile ID.
            Returns None if something went wrong.
        """

        return Tile.tile_listing.get(tile_id, None)

    @classmethod
    def build_tiles(cls):
        """Builds configured Tiles.

        Builds all configured Tiles as defined in tiledata and adds them
        to the tile listing.
        """

        LOGGER.debug("Building tiles")

        for tile_id in tiledata.TILE_DATA:
            if not Tile.tile_factory(tile_id):
                LOGGER.error("Could not construct tile with ID %d", tile_id)
                sys.exit(1)

# Set up logger.
logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)
