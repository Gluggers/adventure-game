import logging
import pygame
import imagepaths
import tiledata

### TILE CONSTANTS ###
TILE_SIZE = 32
TILE_CLASS = 'Tile'

# TODO make this extend sprite?

# SHOULD THIS BE IMMUTABLE?
class Tile:
    tile_listing = {} # maps tile IDs to tile objects

    def __init__(self,                                          \
                tile_id,                                        \
                image_path=imagepaths.TILE_DEFAULT_PATH,        \
                allowed_transport=(                             \
                    tiledata.WALKABLE_F | tiledata.FLYABLE_F)   \
                ):
        self.tile_id = tile_id

        # represents the base terrain image (e.g. grass, water)
        self._image = pygame.image.load(image_path).convert()

        # OR-ed flags that represent the allowed methods of transportation on
        # this tile - walking, canoing, sailing, and flying.
        self._allowed_transport = allowed_transport

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, value):
        self._image = value

    @image.deleter
    def image(self):
        del self._image

    @property
    def allowed_transport(self):
        return self._allowed_transport

    @allowed_transport.setter
    def allowed_transport(self, value):
        self._allowed_transport = value

    @allowed_transport.deleter
    def allowed_transport(self):
        del self._allowed_transport

    def valid_transportation(self, transportation_flag):
        # and the flags
        if transportation_flag & self._allowed_transport:
            return True
        else:
            return False

    # blits the tile image onto the surface at the designated pixel
    # coordinate position (x,y).
    # Does not update the surface display - caller will have to do that.
    def blit_onto_surface(self, surface, top_left_pixel_tuple):
        if self and surface and top_left_pixel_tuple:
            surface.blit(self._image, top_left_pixel_tuple)

    # builds Tile. Adds Tile to tile listing if a new tile was created
    # if the corresponding tile already exists, the method
    # will simply return the Tile rather than creating a new one.
    @classmethod
    def tile_factory(cls, tile_id):
        ret_tile = None
        # check if we already have the tile made
        tile_from_listing = Tile.tile_listing.get(tile_id, None)

        if tile_from_listing:
            ret_tile = tile_from_listing
        else:
            # need to make tile. grab tile data
            ret_tile_data = tiledata.TILE_DATA.get(tile_id, None)
            if (ret_tile_data):
                tile_image_path = ret_tile_data.get(                    \
                    tiledata.TILE_IMAGE_PATH_FIELD,                     \
                    imagepaths.TILE_DEFAULT_PATH                        \
                )
                tile_transport_flag = ret_tile_data.get(                \
                    tiledata.TILE_ALLOWED_TRANSPORT_FIELD,              \
                    (tiledata.WALKABLE_F | tiledata.FLYABLE_F)          \
                )

                ret_tile = Tile(                                        \
                    tile_id,                                            \
                    image_path=tile_image_path,                         \
                    allowed_transport=tile_transport_flag               \
                )

                # add tile to listing
                if ret_tile:
                    Tile.tile_listing[tile_id] = ret_tile
                else:
                    logger.warn("Could not make tile for id {0}".format(tile_id))

        return ret_tile

    @classmethod
    def get_tile(cls, tile_id):
        return Tile.tile_listing.get(tile_id, None)

    # builds all set tiles and adds them to the tile listing
    @classmethod
    def build_tiles(cls):
        logger.debug("Building tiles")

        for tile_id in tiledata.TILE_DATA:
            new_tile = Tile.tile_factory(tile_id)

# set up logger
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
