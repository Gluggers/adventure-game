import pygame
import image_paths

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
OW_IMAGE_ID_WALK_NORTH = 0x5
OW_IMAGE_ID_WALK_EAST = 0x6
OW_IMAGE_ID_WALK_SOUTH = 0x7
OW_IMAGE_ID_WALK_WEST = 0x8

### BATTLE MODE IMAGE TYPE ID NUMBERS ###
BATTLE_IMAGE_ID_DEFAULT = 0x9
BATTLE_IMAGE_ID_STAND = 0xa
BATTLE_IMAGE_ID_ATTACK = 0xb
BATTLE_IMAGE_ID_FAINTED = 0xc


## TESTING PROTAG IMAGE PATH DICT
IMAGE_PATH_DICT_PROTAG = {
    OW_IMAGE_ID_DEFAULT: image_paths.TREE_BASIC_PATH,
    OW_IMAGE_ID_FACE_NORTH: image_paths.TREE_BASIC_PATH,
    OW_IMAGE_ID_FACE_EAST: image_paths.TREE_BASIC_PATH,
    OW_IMAGE_ID_FACE_SOUTH: image_paths.TREE_BASIC_PATH,
    OW_IMAGE_ID_FACE_WEST: image_paths.TREE_BASIC_PATH,
    OW_IMAGE_ID_WALK_NORTH: image_paths.TREE_BASIC_PATH,
    OW_IMAGE_ID_WALK_EAST: image_paths.TREE_BASIC_PATH,
    OW_IMAGE_ID_WALK_SOUTH: image_paths.TREE_BASIC_PATH,
    OW_IMAGE_ID_WALK_WEST: image_paths.TREE_BASIC_PATH,
    BATTLE_IMAGE_ID_DEFAULT: image_paths.TREE_BASIC_PATH,
    BATTLE_IMAGE_ID_STAND: image_paths.TREE_BASIC_PATH,
    BATTLE_IMAGE_ID_ATTACK: image_paths.TREE_BASIC_PATH,
    BATTLE_IMAGE_ID_FAINTED: image_paths.TREE_BASIC_PATH
}

class Interactive_Object(pygame.sprite.Sprite):
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

    # blits the interactive object sprite image onto surface at the
    # designated pixel coordinate position.
    # Does not update the surface display - caller will have to do that.
    def blit_onto_surface(self, surface, image_type_id, pixel_location_tuple):
        if self and surface:
            image_to_blit = self.image_dict.get(image_type_id, None)

            if image_to_blit:
                surface.blit(image_to_blit, pixel_location_tuple)

    # blits the interactive object sprite image onto surface at the
    # with the image's bottom left pixel set by bottom_left_pixel_loc
    # Does not update the surface display - caller will have to do that.
    def blit_onto_surface_bottom_left(self, surface, image_type_id, bottom_left_pixel_loc):
        if self and surface:
            image_to_blit = self.image_dict.get(image_type_id, None)

            # get image dimensions
            width, height = image_to_blit.get_size()

            # offset
            top_left = (bottom_left_pixel_loc[0], bottom_left_pixel_loc[1] - height)

            if image_to_blit:
                surface.blit(image_to_blit, top_left)
