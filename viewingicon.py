import pygame
import objdata
import interactiveobj
import interactiondata
import itemdata
import battledata
import logging
import imageids
import menuoptions
import language

class ViewingIcon(pygame.sprite.Sprite):
    def __init__(
            self,
            icon_id,
            name_info,
            description_info,
            image_path_dict=None,
            menu_option_ids=None,
        ):
        # Call the parent class (Sprite) init
        pygame.sprite.Sprite.__init__(self)

        # Set up icon.
        self.icon_id = icon_id
        self.name_info = {}
        for lang_id, name_str in name_info.items():
            self.name_info[lang_id] = name_str

        self.description_info = {}
        for lang_id, desc_str in description_info.items():
            self.description_info[lang_id] = desc_str

        self.image_dict = {}
        if image_path_dict:
            for image_type_id, image_path in image_path_dict.items():
                logger.debug("Loading image from path {0}".format(image_path))
                # convert alpha for transparency
                self.image_dict[image_type_id] = \
                    pygame.image.load(image_path).convert_alpha()

        self.enlarged_icon = None
        icon_image = self.image_dict.get(imageids.ICON_IMAGE_ID, None)
        if icon_image:
            self.enlarged_icon = pygame.transform.scale(
                icon_image,
                (icon_image.get_width() * 2, icon_image.get_height() * 2)
            )

        self.curr_image_id = imageids.ICON_IMAGE_ID

        self.menu_option_ids = []
        if menu_option_ids:
            for option_id in menu_option_ids:
                self.menu_option_ids.append(option_id)

    def get_name(self, alternative_language_id=None):
        ret_name = ""
        if alternative_language_id is not None:
            ret_name = self.name_info.get(alternative_language_id, "")
        else:
            ret_name = self.name_info.get(language.Language.current_language_id, "")

        return ret_name

    def get_image(self, image_id):
        return self.image_dict.get(image_id, None)

    def get_enlarged_icon(self):
        return self.enlarged_icon

    def get_icon(self):
        return self.get_image(imageids.ICON_IMAGE_ID)

    # Returns the appropriate language translation for the item's description
    # info string.
    def get_description_info(
                self,
                alternative_language_id=None,
            ):
        ret_str = None

        if self.description_info:
            if alternative_language_id is not None:
                ret_str = self.description_info.get(
                        alternative_language_id,
                        None
                    )
            else:
                ret_str = self.description_info.get(
                        language.Language.current_language_id,
                        None
                    )
        elif self.name_info:
            ret_str = ret_str = self.get_name(
                alternative_language_id=alternative_language_id
            )

        return ret_str

    # Overridable by child.
    def get_info_text(self):
        return self.get_description_info()

# set up logger
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
