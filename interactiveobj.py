import pygame
import imagepaths
import objdata
import logging
import interactiondata

### IMAGE FLAGS ###
#IMAGE_F_OVERWORLD = 0x1 # sets overworld images
#IMAGE_F_BATTLE = 0x2 # sets battle images


class Interactive_Object(pygame.sprite.Sprite):
    # maps interactive obj ID to interactive obj
    interactive_obj_listing = {}

    # examine_info maps language IDs to an examine string.
    def __init__(
                    self,
                    object_type,
                    object_id,
                    name_info, # maps language id to name
                    image_path_dict,
                    collision_width=1,
                    collision_height=1,
                    examine_info=None,
                    interaction_id=interactiondata.DEFAULT_ID,
                ):
        # Call the parent class (Sprite) init
        pygame.sprite.Sprite.__init__(self)
        self.object_type = object_type
        self.object_id = object_id
        self.name_info = name_info
        self.collision_width = collision_width
        self.collision_height = collision_height

        # Set interaction ID.
        self.interaction_id = interactiondata.DEFAULT_ID
        if interaction_id is not None:
            self.interaction_id = interaction_id

        # get examine info
        self.examine_info = {}
        if examine_info:
            for x, y in examine_info.items():
                self.examine_info[x] = y

        # load images
        self.image_dict = {}
        for image_type_id, image_path in image_path_dict.items():
            # convert alpha for transparency
            self.image_dict[image_type_id] = pygame.image.load(image_path).convert_alpha()

        self.curr_image_id = objdata.OW_IMAGE_ID_DEFAULT

    def get_name(self, language_id):
        ret_name = ""
        if language_id is not None:
            ret_name = self.name_info.get(language_id, "")

        return ret_name


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
            image_type_id=None,                                             \
            bottom_left_pixel=None,                                         \
            top_left_pixel=None                                             \
        ):
        if self and surface and (bottom_left_pixel or top_left_pixel):
            id_to_use = None

            if image_type_id:
                id_to_use = image_type_id
            else:
                id_to_use = self.curr_image_id

            image_to_blit = self.image_dict.get(id_to_use, None)
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

    # Adds/updates the interactive object listing for the given object ID.
    # Returns True upon success, false otherwise
    @classmethod
    def add_interactive_obj_to_listing(cls, obj_id, inter_obj):
        if inter_obj and (obj_id is not None):
            cls.interactive_obj_listing[obj_id] = inter_obj
            logger.debug("Added object ID {0} to inter obj listing.".format(obj_id))
            return True
        else:
            return False

    # Returns tile collision rect in the tuple form
    # (top left tile x, top left tile y, width, height)
    def get_collision_tile_rect(self, bottom_left_tile_loc):
        ret_rect = None

        if self and bottom_left_tile_loc:
            ret_rect = (                                                \
                bottom_left_tile_loc[0],                                \
                bottom_left_tile_loc[1] - self.collision_height + 1,    \
                self.collision_width,                                   \
                self.collision_height                                   \
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
                collision_set.add((start_x, start_y))
                for y in range(collision_rect[3]):
                    for x in range(collision_rect[2]):
                        collision_set.add((start_x + x, start_y + y))
        logger.debug("Collision set: {0}".format(collision_set))
        return collision_set

    @classmethod
    def is_resource_id(cls, object_id):
        return (object_id is not None)                  \
            and (object_id >= objdata.MIN_RESOURCE_ID)  \
            and (object_id <= objdata.MAX_RESOURCE_ID)

    # Returns a String containing the text to display when the protagonist
    # examines an object.
    def get_examine_info(self, language_id):
        ret_str = "?????"
        if self.name_info:
            ret_str = "It's a {0}".format(self.get_name(language_id))

        if (language_id is not None) and self.examine_info:
            info = self.examine_info.get(language_id, None)
            if info:
                ret_str = info
        elif self.name_info:
            ret_str = "It's a {0}".format(self.get_name(language_id))

        return ret_str


# set up logger
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
