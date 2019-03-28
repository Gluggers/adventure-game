import pygame
import display
import viewingdata
import equipmentslot
import equipmentdata
import imagepaths
import language
import logging

class EquipmentDisplay(display.Display):
    def __init__(
            self,
            main_display_surface,
            display_rect,
            icon_dimensions,
            background_pattern=None,
            horizontal_padding=0,
            vertical_padding=0,
            selection_image_path=imagepaths.ITEM_LISTING_SELECTED_DEFAULT_PATH,
            non_selection_image_path=imagepaths.ITEM_LISTING_UNSELECTED_DEFAULT_PATH,
        ):
        display.Display.__init__(
            self,
            main_display_surface,
            display_rect,
            background_pattern=background_pattern,
            background_image_path=None,
            background_color=None,
        )
        self.horizontal_padding = horizontal_padding
        self.vertical_padding = vertical_padding
        self.icon_dimensions = icon_dimensions

        self.selection_image = None
        if selection_image_path:
            self.selection_image = pygame.image.load(
                selection_image_path
            ).convert_alpha()

        self.non_selection_image = None
        if non_selection_image_path:
            self.non_selection_image = pygame.image.load(
                non_selection_image_path
            ).convert_alpha()

        self.icon_display_rect = pygame.Rect(
            display_rect.x + self.horizontal_padding,
            display_rect.y + self.vertical_padding,
            display_rect.width - (2 * self.horizontal_padding),
            display_rect.height - (2 * self.vertical_padding),
        )

        """
                    HEAD
            AMMO    NECK    BACK/CAPE
            WEAPON1 BODY    WEAPON2/SHIELD
            HANDS   LEGS    WRIST
                    FEET    RING
        """

        # Determine center pixel for where each equipment icon slot goes.
        self.equipment_icon_center = {}

        icon_width = icon_dimensions[0]
        icon_height = icon_dimensions[1]
        num_rows = 5
        #vertical_pixels_between_icons = \
            #int((self.icon_display_rect.height - (5 * icon_height)) / num_rows)
        vertical_pixels_between_icons = 20

        #horizontal_pixels_between_icons = int(icon_width / 2)
        horizontal_pixels_between_icons = 20

        third_row_center_y = self.icon_display_rect.centery
        second_row_center_y = third_row_center_y \
            - vertical_pixels_between_icons \
            - icon_height
        first_row_center_y = second_row_center_y \
            - vertical_pixels_between_icons \
            - icon_height
        fourth_row_center_y = third_row_center_y \
            + vertical_pixels_between_icons \
            + icon_height
        fifth_row_center_y = fourth_row_center_y \
            + vertical_pixels_between_icons \
            + icon_height
        second_column_center_x = self.icon_display_rect.centerx
        first_column_center_x = second_column_center_x \
            - horizontal_pixels_between_icons \
            - icon_width
        third_column_center_x = second_column_center_x \
            + horizontal_pixels_between_icons \
            + icon_width

        self.equipment_icon_center[equipmentdata.EQUIP_SLOT_HEAD] = (
            second_column_center_x,
            first_row_center_y
        )
        self.equipment_icon_center[equipmentdata.EQUIP_SLOT_NECK] = (
            second_column_center_x,
            second_row_center_y
        )
        self.equipment_icon_center[equipmentdata.EQUIP_SLOT_MAIN_BODY] = (
            second_column_center_x,
            third_row_center_y
        )
        self.equipment_icon_center[equipmentdata.EQUIP_SLOT_LEGS] = (
            second_column_center_x,
            fourth_row_center_y
        )
        self.equipment_icon_center[equipmentdata.EQUIP_SLOT_FEET] = (
            second_column_center_x,
            fifth_row_center_y
        )
        self.equipment_icon_center[equipmentdata.EQUIP_SLOT_AMMO] = (
            first_column_center_x,
            second_row_center_y
        )
        self.equipment_icon_center[equipmentdata.EQUIP_SLOT_MAIN_HAND] = (
            first_column_center_x,
            third_row_center_y
        )
        self.equipment_icon_center[equipmentdata.EQUIP_SLOT_HANDS] = (
            first_column_center_x,
            fourth_row_center_y
        )
        self.equipment_icon_center[equipmentdata.EQUIP_SLOT_BACK] = (
            third_column_center_x,
            second_row_center_y
        )
        self.equipment_icon_center[equipmentdata.EQUIP_SLOT_OFF_HAND] = (
            third_column_center_x,
            third_row_center_y
        )
        self.equipment_icon_center[equipmentdata.EQUIP_SLOT_WRIST] = (
            third_column_center_x,
            fourth_row_center_y
        )
        self.equipment_icon_center[equipmentdata.EQUIP_SLOT_RING] = (
            third_column_center_x,
            fifth_row_center_y
        )

    # equipment_info_dict is dict that maps equipment slot ID
    # to 2-list of form [item_icon, rendered_supertext]
    def blit_equipment_icons(
            self,
            surface,
            equipment_info_dict,
            selected_slot_id=equipmentdata.EQUIP_SLOT_HEAD,
            alternative_top_left=None,
        ):
        if surface and equipment_info_dict \
                and (selected_slot_id is not None):
            icon_space_rect = self.icon_display_rect

            if alternative_top_left:
                icon_space_rect = pygame.Rect(
                    alternative_top_left[0] + self.horizontal_padding,
                    alternative_top_left[1] + self.vertical_padding,
                    self.icon_display_rect.width,
                    self.icon_display_rect.height
                )

            # Blit background
            self.blit_background(
                surface,
                alternative_top_left=alternative_top_left,
            )

            logger.debug("Icon space top left: {0}".format(
                icon_space_rect.topleft
            ))

            # Blit the icons.
            for slot_id in equipmentdata.EQUIPMENT_SLOT_DATA:
                # Check if we have info in the argument dict.
                equipped_info = equipment_info_dict.get(slot_id, None)

                icon_background = None
                icon_to_blit = None
                rendered_supertext = None
                icon_rect = None
                icon_background_rect = None

                if equipped_info:
                    # This slot is equipped.
                    icon_to_blit = equipped_info[0]
                    rendered_supertext = equipped_info[1]
                """
                else:
                    equipment_slot_obj = \
                        equipmentslot.EquipmentSlot.get_slot_object(slot_id)
                    if equipment_slot_obj:
                        icon_to_blit = \
                            equipment_slot_obj.get_icon()
                """

                if slot_id == selected_slot_id:
                    # This slot is selected.
                    icon_background = self.selection_image
                else:
                    icon_background = self.non_selection_image

                icon_rect_center = self.equipment_icon_center.get(slot_id, None)
                if icon_rect_center:
                    if icon_background:
                        icon_background_rect = icon_background.get_rect(
                            center=icon_rect_center
                        )
                        surface.blit(
                            icon_background,
                            icon_background_rect,
                        )

                    if icon_to_blit:
                        icon_rect = icon_to_blit.get_rect(
                            center=icon_rect_center
                        )
                        surface.blit(
                            icon_to_blit,
                            icon_rect,
                        )

                        if rendered_supertext:
                            surface.blit(
                                rendered_supertext,
                                icon_rect.topleft,
                            )

# set up logger
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
