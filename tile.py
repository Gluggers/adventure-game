import logging
import pygame
import imagepaths


### TILE CONSTANTS ###
TILE_SIZE = 32
TILE_CLASS = 'Tile'

### TRANSPORTATION FLAGS ###
WALKABLE_F = 0x1
CANOEABLE_F = 0x2
SAILABLE_F = 0x4
FLYABLE_F = 0x8

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

# TODO make this extend sprite?

# SHOULD THIS BE IMMUTABLE?
class Tile:
    tile_listing = {} # maps tile IDs to tile objects

    def __init__(self,                                                      \
                image_path=imagepaths.TILE_DEFAULT_PATH,                        \
                allowed_transport=(WALKABLE_F | FLYABLE_F),                 \
                ):
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

    @classmethod
    def get_tile(cls, tile_id):
        return Tile.tile_listing.get(tile_id, None)

    @classmethod
    def build_tiles(cls):
        logger.debug("Building tiles")

        Tile.tile_listing[TILE_DEFAULT_ID] = Tile()
        Tile.tile_listing[TILE_GRASS_1_ID] = Tile(image_path=imagepaths.TILE_GRASS_1_PATH)
        Tile.tile_listing[TILE_GRASS_2_ID] = Tile(image_path=imagepaths.TILE_GRASS_2_PATH)
        Tile.tile_listing[TILE_GRASS_PLAIN_ID] = Tile(image_path=imagepaths.TILE_GRASS_PLAIN_PATH)
        Tile.tile_listing[TILE_WATER_NORMAL_1_ID] = Tile(image_path=imagepaths.TILE_WATER_NORMAL_1_PATH, allowed_transport=FLYABLE_F | CANOEABLE_F)
        Tile.tile_listing[TILE_SAND_ID] = Tile(image_path=imagepaths.TILE_SAND_PATH)

# set up logger
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
