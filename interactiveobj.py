import pygame
import imagepaths
import logging

### IMAGE FLAGS ###
#IMAGE_F_OVERWORLD = 0x1 # sets overworld images
#IMAGE_F_BATTLE = 0x2 # sets battle images


class Interactive_Object(pygame.sprite.Sprite):
    # maps interactive obj ID to interactive obj
    interactive_obj_listing = {}

    def __init__(
                    self,
                    object_type,
                    object_id,
                    name,
                    image_path_dict,
                    collision_width=1,
                    collision_height=1
                ):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        self.object_type = object_type
        self.object_id = object_id
        self.name = name
        self.collision_width = collision_width
        self.collision_height = collision_height

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

    @classmethod
    def get_interactive_object(cls, obj_id):
        return Interactive_Object.interactive_obj_listing.get(obj_id, None)


    # Returns tile collision rect in the tuple form
    # (top left tile x, top left tile y, width, height)
    def get_collision_tile_rect(self, bottom_left_tile_loc):
        ret_rect = None

        if self and bottom_left_tile_loc:
            ret_rect = (                                                \
                bottom_left_tile_loc[0],                                \
                bottom_left_tile_loc[1] - obj_to_set.collision_height,  \
                obj_to_set.collision_width,                             \
                obj_to_set.collision_height                             \
            )

        return ret_rect

    # Returns set of tile coordinate tuples that make up the
    # object's collision rectangle given the object's bottom left tile
    # location
    def get_collision_tile_set(self, bottom_left_tile_loc):
        collision_set = set()

        if self and bottom_left_tile_loc:
            collision_rect = self.get_collision_tile_rect(bottom_left_tile_loc)

            if collision_rect:
                start_x = collision_rect[0]
                start_y = collision_rect[1]
                for y in range(collision_rect[3]):
                    for x in range(collision_rect[2]):
                        collision_set.add((start_x + x, start_y + y))

        return collision_set

# set up logger
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
