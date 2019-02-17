import logging
import pygame
import imagepaths
import tiledata

### TILE CONSTANTS ###
TILE_SIZE = 32
TILE_CLASS = 'Tile'

class Tile:
    # maps tile IDs to tile objects
    tile_listing = {}

    def __init__(self,                                          \
                tile_id,                                        \
                image_path=imagepaths.TILE_DEFAULT_PATH,        \
                allowed_transport=(                             \
                    tiledata.WALKABLE_F | tiledata.FLYABLE_F)   \
                ):
        """Create and return a Tile object."""

        # Each tile_id should map to a distinct Tile
        self.tile_id = tile_id

        # Represents the base terrain image (e.g. grass, water)
        logger.debug("Loading tile image from path {0}".format(image_path))
        self._image = pygame.image.load(image_path).convert()

        # OR-ed flags that represent the allowed methods of transportation on
        # this tile - walking, canoing, sailing, and flying.
        self._allowed_transport = allowed_transport

    @property
    def image(self):
        """Return Tile image."""
        return self._image

    @image.setter
    def image(self, value):
        """Set Tile image."""
        self._image = value

    @image.deleter
    def image(self):
        """Delete Tile image."""
        del self._image

    @property
    def allowed_transport(self):
        """Return the allowed transportation for the Tile."""
        return self._allowed_transport

    @allowed_transport.setter
    def allowed_transport(self, value):
        """Set the allowed transportation for the Tile."""
        self._allowed_transport = value

    @allowed_transport.deleter
    def allowed_transport(self):
        """Delete the allowed transportation for the Tile."""
        del self._allowed_transport

    def valid_transportation(self, transportation_flag):
        """Checks if the transportation method is allowed."""

        if transportation_flag & self._allowed_transport:
            return True
        else:
            return False

    # Blits the tile image onto the surface at the designated pixel
    # coordinate position (x,y).
    # Does not update the surface display - caller will have to do that.
    def blit_onto_surface(self, surface, top_left_pixel_tuple):
        """Blit Tile object onto surface at the provided top left pixel."""
        if self and surface and top_left_pixel_tuple:
            surface.blit(self._image, top_left_pixel_tuple)

    # Builds Tile based on the given Tile ID.
    # Adds Tile to tile listing if a new tile was created.
    # If the corresponding tile already exists, the method
    # will simply return the original Tile rather than creating a new one.
    @classmethod
    def tile_factory(cls, tile_id):
        """Returns a Tile object corresponding to the given Tile ID."""

        ret_tile = None

        # Check if the corresponding Tile has already been made.
        tile_from_listing = Tile.tile_listing.get(tile_id, None)

        if tile_from_listing:
            ret_tile = tile_from_listing
        else:
            # We need to make Tile. Grab tile data.
            ret_tile_data = tiledata.TILE_DATA.get(tile_id, None)
            if (ret_tile_data):
                tile_image_path = ret_tile_data.get(                    \
                    tiledata.TILE_IMAGE_PATH_FIELD,                     \
                    imagepaths.TILE_DEFAULT_PATH                        \
                )

                # Default allowed transportation is walking and flying.
                tile_transport_flag = ret_tile_data.get(                \
                    tiledata.TILE_ALLOWED_TRANSPORT_FIELD,              \
                    (tiledata.WALKABLE_F | tiledata.FLYABLE_F)          \
                )

                ret_tile = Tile(                                        \
                    tile_id,                                            \
                    image_path=tile_image_path,                         \
                    allowed_transport=tile_transport_flag               \
                )

                # Add tile to the class' tile listing.
                if ret_tile:
                    Tile.tile_listing[tile_id] = ret_tile
                else:
                    logger.warn("Could not get tile for id {0}".format(tile_id))

        return ret_tile

    # Get the Tile corresponding to the given ID. Returns None if such
    # a Tile does not exist.
    # Does not create a new Tile. Use tile_factory to create a Tile.
    @classmethod
    def get_tile(cls, tile_id):
        return Tile.tile_listing.get(tile_id, None)

    # Builds all configured Tiles and adds them to the tile listing.
    @classmethod
    def build_tiles(cls):
        logger.debug("Building tiles")

        for tile_id in tiledata.TILE_DATA:
            if not Tile.tile_factory(tile_id):
                logger.error("Could not construct tile with ID {0}".format(tile_id))

# Set up logger.
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
# logger.setLevel(logging.INFO)
