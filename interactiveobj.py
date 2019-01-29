import pygame
import imagepaths
import logging

#INTERACTIVE_OBJ_LISTING = {} # maps interactive object IDs to objects

### INTERACTIVE OBJECT TYPE ID CONSTANTS ###
TYPE_ENTITY = 0x0
TYPE_OBSTACLE = 0x1
TYPE_RESOURCE = 0x2
TYPE_ITEM = 0x3

### INTERACTIVE OBJECT ID NUMBERS ###
PROTAGONIST_ID = 0x0
# TESTING
HERB_BASIC_ID = 0x1
ORE_EMPTY_BASIC_ID = 0x2
TREE_BASIC_ID = 0x3
TREE_OAK_ID = 0x4

### IMAGE FLAGS ###
#IMAGE_F_OVERWORLD = 0x1 # sets overworld images
#IMAGE_F_BATTLE = 0x2 # sets battle images

### OVERWORLD IMAGE TYPE ID NUMBERS ###
OW_IMAGE_ID_DEFAULT = 0x0
OW_IMAGE_ID_FACE_NORTH = 0x1
OW_IMAGE_ID_FACE_EAST = 0x2
OW_IMAGE_ID_FACE_SOUTH = 0x3
OW_IMAGE_ID_FACE_WEST = 0x4
OW_IMAGE_ID_WALK1_NORTH = 0x5
OW_IMAGE_ID_WALK1_EAST = 0x6
OW_IMAGE_ID_WALK1_SOUTH = 0x7
OW_IMAGE_ID_WALK1_WEST = 0x8
OW_IMAGE_ID_WALK2_NORTH = 0x9
OW_IMAGE_ID_WALK2_EAST = 0xa
OW_IMAGE_ID_WALK2_SOUTH = 0xb
OW_IMAGE_ID_WALK2_WEST = 0xc

### BATTLE MODE IMAGE TYPE ID NUMBERS ###
BATTLE_IMAGE_ID_DEFAULT = 0xd
BATTLE_IMAGE_ID_STAND = 0xe
BATTLE_IMAGE_ID_ATTACK = 0xf
BATTLE_IMAGE_ID_FAINTED = 0x10


## TESTING PROTAG IMAGE PATH DICT
IMAGE_PATH_DICT_PROTAG = {
    OW_IMAGE_ID_DEFAULT: imagepaths.PROT_RANGER_F_OW_DEFAULT,
    OW_IMAGE_ID_FACE_NORTH: imagepaths.PROT_RANGER_F_OW_FACE_NORTH,
    OW_IMAGE_ID_FACE_EAST: imagepaths.PROT_RANGER_F_OW_FACE_EAST,
    OW_IMAGE_ID_FACE_SOUTH: imagepaths.PROT_RANGER_F_OW_FACE_SOUTH,
    OW_IMAGE_ID_FACE_WEST: imagepaths.PROT_RANGER_F_OW_FACE_WEST,
    OW_IMAGE_ID_WALK1_NORTH: imagepaths.PROT_RANGER_F_OW_WALK1_NORTH,
    OW_IMAGE_ID_WALK1_EAST: imagepaths.PROT_RANGER_F_OW_WALK1_EAST,
    OW_IMAGE_ID_WALK1_SOUTH: imagepaths.PROT_RANGER_F_OW_WALK1_SOUTH,
    OW_IMAGE_ID_WALK1_WEST: imagepaths.PROT_RANGER_F_OW_WALK1_WEST,
    OW_IMAGE_ID_WALK2_NORTH: imagepaths.PROT_RANGER_F_OW_WALK2_NORTH,
    OW_IMAGE_ID_WALK2_EAST: imagepaths.PROT_RANGER_F_OW_WALK2_EAST,
    OW_IMAGE_ID_WALK2_SOUTH: imagepaths.PROT_RANGER_F_OW_WALK2_SOUTH,
    OW_IMAGE_ID_WALK2_WEST: imagepaths.PROT_RANGER_F_OW_WALK2_WEST,
    BATTLE_IMAGE_ID_DEFAULT: imagepaths.PROT_RANGER_F_OW_DEFAULT,
    BATTLE_IMAGE_ID_STAND: imagepaths.PROT_RANGER_F_OW_DEFAULT,
    BATTLE_IMAGE_ID_ATTACK: imagepaths.PROT_RANGER_F_OW_DEFAULT,
    BATTLE_IMAGE_ID_FAINTED: imagepaths.PROT_RANGER_F_OW_DEFAULT
}

class Interactive_Object(pygame.sprite.Sprite):
    # maps interactive obj ID to interactive obj
    interactive_obj_listing = {}

    def __init__(                           \
                    self,                   \
                    object_type,            \
                    object_id,              \
                    name,                   \
                    image_path_dict         \
                    #tile_position=(0,0)     \
                ):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        self.object_type = object_type
        self.object_id = object_id
        self.name = name
        #self.tile_position = tile_position

        # load images
        self.image_dict = {}
        for image_type_id, image_path in image_path_dict.items():
            # convert alpha for transparency
            self.image_dict[image_type_id] = pygame.image.load(image_path).convert_alpha()

    # blits the interactive object sprite image corresponding to image_type_id
    # onto the designated surface. Can specify either top_left_pixel or
    # bottom_left_pixel as the reference point for blitting the image.
    # bottom_left_pixel is recommended for images that are larger than
    # a single Tile image. If both top_left_pixel and bottom_left_pixel are
    # specified, the method will use bottom_left_pixel as an override.
    # top_left_pixel and bottom_left_pixel are tuples of pixel coordinates.
    # Does not update the surface display - caller will have to do that.
    def blit_onto_surface(self, surface, image_type_id, bottom_left_pixel=None, top_left_pixel=None):
        if self and surface and (bottom_left_pixel or top_left_pixel):
            image_to_blit = self.image_dict.get(image_type_id, None)
            top_left = None

            if image_to_blit:
                if bottom_left_pixel:
                    # get image dimensions
                    width, height = image_to_blit.get_size()

                    # get top left pixel based on bottom left pixel
                    top_left = (bottom_left_pixel[0], bottom_left_pixel[1] - height)
                elif top_left_pixel:
                    top_left = top_left_pixel

                if top_left:
                    surface.blit(image_to_blit, top_left)

# set up logger
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
