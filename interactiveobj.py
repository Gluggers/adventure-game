import pygame
import imagepaths
import objdata
import logging
import interactiondata
import imageids
import language

### IMAGE FLAGS ###
#IMAGE_F_OVERWORLD = 0x1 # sets overworld images
#IMAGE_F_BATTLE = 0x2 # sets battle images

class InteractiveObject(pygame.sprite.Sprite):
    # maps interactive obj ID to interactive obj
    interactive_obj_listing = {}

    # examine_info maps language IDs to an examine string.
    def __init__(
            self,
            object_type,
            object_id,
            name_info, # maps language id to name
            image_info_dict,
            collision_width=1,
            collision_height=1,
            examine_info={},
            interaction_id=None,
            replacement_object_id=None,
            respawn_time_s=None, # None means never respawns.
        ):
        # Call the parent class (Sprite) init
        pygame.sprite.Sprite.__init__(self)
        self.object_type = object_type
        self.object_id = object_id
        self.name_info = name_info
        self.collision_width = collision_width
        self.collision_height = collision_height
        self.replacement_object_id = replacement_object_id
        self.respawn_time_s = respawn_time_s

        # Set interaction ID.
        self.interaction_id = interaction_id

        # get examine info
        self.examine_info = {}
        if examine_info:
            for x, y in examine_info.items():
                self.examine_info[x] = y

        # Load images.
        self.image_sequence_dict = {}
        self._image_sequence_duration_dict = {}
        self._individual_image_duration_dict = {}
        self.in_adhoc_animation = False
        self.adhoc_animation_index = 0

        for image_sequence_id, image_sequence_info in image_info_dict.items():
            image_list = []

            if isinstance(image_sequence_info, str):
                loaded_image = pygame.image.load(
                    image_sequence_info
                ).convert_alpha()

                if loaded_image:
                    self.image_sequence_dict[image_sequence_id] = [loaded_image]
            elif isinstance(image_sequence_info, list):
                image_path_list = image_sequence_info[0]
                image_sequence_duration = image_sequence_info[1]

                self._image_sequence_duration_dict[image_sequence_id] = \
                    image_sequence_duration

                for image_path in image_path_list:
                    loaded_image = pygame.image.load(image_path).convert_alpha()
                    if loaded_image:
                        image_list.append(loaded_image)

                if image_list:
                    self.image_sequence_dict[image_sequence_id] = image_list
                    if image_sequence_duration:
                        self._individual_image_duration_dict[image_sequence_id] = \
                            image_sequence_duration // len(image_list)

        self.curr_image_sequence = imageids.OBJ_SPRITE_SEQUENCE_ID

    def get_name(self, alternative_language_id=None):
        ret_name = ""
        if alternative_language_id is not None:
            ret_name = self.name_info.get(alternative_language_id, "")
        else:
            ret_name = self.name_info.get(language.Language.current_language_id, "")

        return ret_name

    # blits the interactive object sprite image corresponding to image_sequence_id
    # onto the designated surface. Can specify either top_left_pixel or
    # bottom_left_pixel as the reference point for blitting the image.
    # bottom_left_pixel is recommended for images that are larger than
    # a single Tile image. If both top_left_pixel and bottom_left_pixel are
    # specified, the method will use bottom_left_pixel as an override.
    # top_left_pixel and bottom_left_pixel are tuples of pixel coordinates.
    # Does not update the surface display - caller will have to do that.
    def blit_onto_surface(
            self,
            surface,
            image_sequence_id=None,
            bottom_left_pixel=None,
            top_left_pixel=None,
            blit_time_ms=None,
        ):
        if self and surface and (bottom_left_pixel or top_left_pixel):
            id_to_use = None
            image_to_blit = None
            top_left = None

            if image_sequence_id:
                id_to_use = image_sequence_id
            else:
                id_to_use = self.curr_image_sequence

            image_list = self.image_sequence_dict.get(
                id_to_use,
                None
            )

            if self.in_adhoc_animation:
                image_to_blit = image_list[
                    self.adhoc_animation_index % len(image_list)
                ]
            else:
                individual_image_duration = self._individual_image_duration_dict.get(
                    id_to_use,
                    None
                )

                # Get image to blit.
                if image_list:
                    if not individual_image_duration:
                        image_to_blit = image_list[0]
                    elif not blit_time_ms:
                        image_to_blit = image_list[0]
                    else:
                        image_to_blit = image_list[
                            (blit_time_ms // individual_image_duration) \
                            % len(image_list)
                        ]

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
    def misc_interactive_object_factory(cls, obj_id):
        ret_object = None

        # Make sure we are dealing with a miscellaneous object.
        if cls.is_miscellaneous_id(obj_id):
            # Check if we already have the object made.
            obj_from_listing = cls.get_interactive_object(obj_id)

            if obj_from_listing:
                # Return the already made object.
                ret_object = obj_from_listing
            else:
                # Make the new object ourselves. First, get the
                # object data.
                obj_data = objdata.MISC_OBJECT_DATA.get(obj_id, None)

                if obj_data:
                    # Get the object fields
                    # TODO - change default values?
                    name_info = obj_data.get(objdata.OBJECT_NAME_INFO_FIELD, {})
                    image_info_dict = obj_data.get(objdata.IMAGE_INFO_DICT_FIELD, {})
                    collision_width = obj_data.get(objdata.COLLISION_WIDTH_FIELD, 1)
                    collision_height = obj_data.get(objdata.COLLISION_HEIGHT_FIELD, 1)
                    respawn_time_s = obj_data.get(objdata.RESPAWN_TIME_S_FIELD, None)
                    examine_info = obj_data.get(objdata.EXAMINE_INFO_FIELD, None)
                    interaction_id = obj_data.get(
                        objdata.INTERACTION_ID_FIELD,
                        None,
                    )
                    replacement_object_id = obj_data.get(
                        objdata.REPLACEMENT_OBJECT_ID_FIELD,
                        None
                    )

                    # Ensure we have the required fields.
                    if name_info and image_info_dict:
                        # Make the miscellaneous object.
                        new_object = InteractiveObject(
                            objdata.TYPE_MISC,
                            obj_id,
                            name_info,
                            image_info_dict,
                            collision_width=collision_width,
                            collision_height=collision_height,
                            respawn_time_s=respawn_time_s,
                            examine_info=examine_info,
                            interaction_id=interaction_id,
                            replacement_object_id=replacement_object_id,
                        )

                        logger.debug("Made object with ID {0}".format(obj_id))

                        # Update the interactive object mapping.
                        result = cls.add_interactive_obj_to_listing(
                            obj_id,
                            new_object
                        )

                        if result:
                            ret_object = new_object
                        else:
                            logger.error("Failed to add object ID {0} to listing.".format(obj_id))
                    else:
                        logger.error("Required fields not found in misc object data for ID {0}".format(obj_id))
                else:
                    logger.error("Object data not found for object ID {0}".format(obj_id))
        else:
            logger.error("You cannot use misc factory for non-misc object ID {0}".format(obj_id))

        return ret_object

    @classmethod
    def get_interactive_object(cls, obj_id):
        return cls.interactive_obj_listing.get(obj_id, None)

    # Adds/updates the interactive object listing for the given object ID.
    # Returns True upon success, false otherwise.
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

    @classmethod
    def is_miscellaneous_id(cls, object_id):
        return (object_id is not None)                  \
            and (object_id >= objdata.MIN_MISC_ID)  \
            and (object_id <= objdata.MAX_MISC_ID)

    # Returns a String containing the text to display when the protagonist
    # examines an object.
    def get_examine_info(self, language_id):
        ret_str = "?????"

        if (language_id is not None) and self.examine_info:
            info = self.examine_info.get(language_id, None)
            if info:
                ret_str = info
        elif self.name_info:
            ret_str = self.get_name(language_id)

        return ret_str

    @classmethod
    def build_misc_objects(cls):
        logger.info("Building miscellaneous interactive objects.")

        for obj_id in objdata.MISC_OBJECT_DATA:
            if not cls.misc_interactive_object_factory(obj_id):
                logger.error("Could not construct misc object with ID {0}".format(obj_id))

# set up logger
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
