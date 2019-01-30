import pygame
import imagepaths
import logging

### IMAGE FLAGS ###
#IMAGE_F_OVERWORLD = 0x1 # sets overworld images
#IMAGE_F_BATTLE = 0x2 # sets battle images


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
    def blit_onto_surface(                                                  \
            self,                                                           \
            surface,                                                        \
            image_type_id,                                                  \
            bottom_left_pixel=None,                                         \
            top_left_pixel=None                                             \
        ):
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
