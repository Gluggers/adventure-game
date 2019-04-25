# -*- coding: utf-8 -*-
"""Contains functions and constants for ViewingIcon objects."""

import logging
import pygame
import imageids
import language

class ViewingIcon(pygame.sprite.Sprite):
    """A class used to represent icons for selection viewings.

    ViewingIcon objects are used in selection viewings such as inventory
    viewings, skill viewings, and equipment viewings. The ViewingIcon objects
    represent a selectable object within that viewing; in the example of the
    inventory viewing, the corresponding ViewingIcon object is an Item object,
    which extends the ViewingIcon class.  Other child classes of ViewingIcon
    object can include skill icons, equipment slots, and spells.

    Attributes:
        icon_id: the ID number for this icon. Must be unique
            within the child class.
        icon: the pygame Surface object representing the icon image for
            the ViewingIcon.
        enlarged_icon: pygame Surface object representing the enlarged icon
            image for the ViewingIcon object. Enlarged Icons are set to be
            twice as large (double the width and height) as the regular
            icon.
        curr_image_id: the current image ID being used by the object.
            This value will change for animated objects that change
            sprites after a certain number of game ticks.
        menu_option_ids: list of option ID values that represent the
            menu options to display when the ViewingIcon is selected
            in a viewing.
    """

    def __init__(
            self,
            icon_id,
            name_info,
            description_info,
            image_path_dict=None,
            menu_option_ids=None,
        ):
        # Call the parent class (Sprite) init.
        pygame.sprite.Sprite.__init__(self)

        # Set up icon.
        self._icon_id = icon_id

        self._name_info = {}
        for lang_id, name_str in name_info.items():
            self._name_info[lang_id] = name_str

        self._description_info = {}
        for lang_id, desc_str in description_info.items():
            self._description_info[lang_id] = desc_str

        self._image_dict = {}
        if image_path_dict:
            for image_type_id, image_path in image_path_dict.items():
                LOGGER.debug("Loading image from path %s", image_path)

                # Convert alpha for transparency.
                if image_path:
                    self._image_dict[image_type_id] = \
                        pygame.image.load(image_path).convert_alpha()

        self._enlarged_icon = None
        self._icon = self._image_dict.get(imageids.ICON_IMAGE_ID, None)
        if self._icon:
            self._enlarged_icon = pygame.transform.scale(
                self._icon,
                (self._icon.get_width() * 2, self._icon.get_height() * 2)
            )

        self._curr_image_id = imageids.ICON_IMAGE_ID

        self._menu_option_ids = []
        if menu_option_ids:
            for option_id in menu_option_ids:
                self._menu_option_ids.append(option_id)

    def get_name(self, alternative_language_id=None):
        """Returns the ViewingIcon's name.

        By default, the name is set according to the current game
        language.  The caller can set a custom language ID if needed.

        Args:
            alternative_language_id: language ID value that will
                determine which name translation to bring back. By
                default, this value is None, which means the method
                returns the name corresponding to the current game
                language.

        Returns:
            String representing the ViewingIcon name.
        """

        ret_name = None
        if alternative_language_id is not None:
            ret_name = self._name_info.get(alternative_language_id, None)
        else:
            ret_name = self._name_info.get(
                language.Language.current_language_id,
                None,
            )

        return ret_name

    def get_image(self, image_id):
        """Returns the ViewingIcon image for the specified image ID value.

        Args:
            image_id: image ID value to determine which image to bring back.

        Returns:
            pygame Surface object representing the requested image, or
            None if no corresponding image is found for the specified image
            ID.
        """
        return self._image_dict.get(image_id, None)

    @property
    def enlarged_icon(self):
        """Returns the enlarged icon for the object.

        Enlarged icons are twice as large as the standard icon.
        """

        return self._enlarged_icon

    @property
    def icon(self):
        """Returns the regular icon for the object."""

        return self._icon

    @property
    def icon_id(self):
        """Returns the object's icon ID."""

        return self._icon_id

    @property
    def curr_image_id(self):
        """Returns the image ID for the current object image."""

        return self._curr_image_id

    @property
    def menu_option_ids(self):
        """Returns the list of menu option ID values for the object."""

        return self._menu_option_ids

    # Returns the appropriate language translation for the item's description
    # info string.
    def get_description_info(
            self,
            alternative_language_id=None,
        ):
        """Returns the ViewingIcon's description.

        By default, the description is set according to the current game
        language.  The caller can set a custom language ID if needed.

        Args:
            alternative_language_id: language ID value that will
                determine which description translation to bring back. By
                default, this value is None, which means the method
                returns the description corresponding to the current game
                language.

        Returns:
            String representing the ViewingIcon description.
        """

        ret_str = None

        if self._description_info:
            if alternative_language_id is not None:
                ret_str = self._description_info.get(
                    alternative_language_id,
                    None
                )
            else:
                ret_str = self._description_info.get(
                    language.Language.current_language_id,
                    None
                )
        elif self._name_info:
            ret_str = ret_str = self.get_name(
                alternative_language_id=alternative_language_id
            )

        return ret_str

    # Overridable by child.
    def get_info_text(self, alternative_language_id=None):
        """Returns the ViewingIcon's information text.

        By default, the information text is set according to the current game
        language, and the information is equivalent to the description.
        The caller can set a custom language ID if needed.
        Child classes can define their own implementation of the information
        text by overriding this method.

        Args:
            alternative_language_id: language ID value that will
                determine which translation to bring back. By
                default, this value is None, which means the method
                returns the information text corresponding to the current game
                language.

        Returns:
            String representing the ViewingIcon information text.
        """

        return self.get_description_info(
            alternative_language_id=alternative_language_id,
        )

# Set up logger.
logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)
