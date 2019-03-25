import display
import viewingdata
import equipmentdata
import imagepaths
import language

# SELECTION DIRECTION CONSTANTS
MOVE_UP = 0x1
MOVE_RIGHT = 0x2
MOVE_DOWN = 0x3
MOVE_LEFT = 0x4

class EquipmentInfo(object):
    # Maps equipment slot IDs to icon images.
    equipment_slot_icon_mapping = {}

    def __init__(
            self
        ):
        pass

    @classmethod
    def get_equipment_slot_description(self, equipment_id):
        return equipmentdata.EQUIPMENT_SLOT_DESCRIPTION_INFO.get(
            language.Language.current_language_id,
            None
        )

    @classmethod
    def init_equipment_slot_icons(self):
        # TODO initialize.
        pass

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
        vertical_pixels_between_icons = \
            int((self.icon_display_rect.height - (5 * icon_height)) / num_rows)

        horizontal_pixels_between_icons = int(icon_width / 2)

        third_row_center_y = self.icon_display_rect.centery
        second_row_center_y = third_row_center_y \
            - vertical_pixels_between_icons \
            - icon_height
        second_row_center_y = second_row_center_y \
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
        self.equipment_icon_center[equipmentdata.EQUIP_EQUIP_SLOT_OFF_HAND] = (
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
    # to 3-list of form [item_icon, rendered_supertext]
    def blit_equipment_icons(
            self,
            surface,
            equipment_info_dict,
            selected_equipment_id,
            alternative_top_left=None,
        ):
        if surface and equipment_info_dict \
                and (selected_equipment_id is not None):
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


            curr_index = starting_index
            logger.debug("Starting with icon index {0}".format(curr_index))

            horizontal_offset = 0
            vertical_offset = 0

            # Blit icon and quantity text if needed.
            icon_rect = pygame.Rect(
                icon_space_rect.x + horizontal_offset,
                icon_space_rect.y + vertical_offset,
                self.icon_dimensions[0],
                self.icon_dimensions[1],
            )

            while curr_index <= last_index:
                curr_viewing_row = int(
                    (curr_index - starting_index) / self.num_columns
                )
                curr_viewing_col = \
                    (curr_index - starting_index) % self.num_columns

                horizontal_offset = \
                    ((curr_index - starting_index) % self.num_columns) \
                    * (self.icon_dimensions[0] + self.pixels_between_icons)

                vertical_offset = \
                    curr_viewing_row \
                    * (self.icon_dimensions[1] + self.pixels_between_icons)

                curr_icon_info = icon_data_list[curr_index]
                icon_image = curr_icon_info[0]
                rendered_supertext = curr_icon_info[1]

                # Blit icon image and quantity text if needed.
                icon_rect.topleft = (
                    icon_space_rect.x + horizontal_offset,
                    icon_space_rect.y + vertical_offset,
                )

                # Check if this is the selected icon. If so,
                # blit the selection background.
                if ((selected_index == curr_index) \
                    or (preselected_index_list is not None \
                        and selected_index in preselected_index_list)) \
                    and self.selection_image:
                    # Center on the icon.
                    select_image_rect = self.selection_image.get_rect(
                        center=icon_rect.center
                    )

                    surface.blit(
                        self.selection_image,
                        select_image_rect,
                    )

                if icon_image:
                    surface.blit(
                        icon_image,
                        icon_rect,
                    )

                if rendered_supertext:
                    text_top_left = icon_rect.topleft
                    surface.blit(
                        rendered_supertext,
                        text_top_left,
                    )

                curr_index += 1

            # Blit the up and down arrows if there are icons above/below.
            if (starting_index >= self.num_columns) and show_continue_icon:
                # We have at least 1 row above us.
                surface.blit(
                    self.continue_up_icon,
                    self.continue_up_rect
                )

            if ((total_icons - starting_index) > self.max_num_icons) \
                and show_continue_icon:
                # We have icons after us.
                surface.blit(
                    self.continue_down_icon,
                    self.continue_down_rect
                )
