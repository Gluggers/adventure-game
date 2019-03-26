import pygame
import viewing
import viewingdata
import equipmentdisplay
import display
import imagepaths
import fontinfo
import menuoptions
import language
import timekeeper
import inventory
import selectionviewing
import itemdata
import logging
import sys

# Maps equipment IDs to the directions one can traverse in the display.
ALLOWED_MOVEMENT_MAPPING = {
# TODO
    EQUIP_SLOT_HEAD: [

    ],
    EQUIP_SLOT_MAIN_HAND: [

    ],
    EQUIP_SLOT_OFF_HAND: [

    ],
    EQUIP_SLOT_MAIN_BODY: [

    ],
    EQUIP_SLOT_LEGS: [

    ],
    EQUIP_SLOT_NECK: [

    ],
    EQUIP_SLOT_AMMO: [

    ],
    EQUIP_SLOT_HANDS: [

    ],
    EQUIP_SLOT_FEET: [

    ],
    EQUIP_SLOT_RING: [

    ],
    EQUIP_SLOT_BACK: [

    ],
    EQUIP_SLOT_WRIST: [

    ],
}

class EquipmentViewing(selectionviewing.ItemSelectionGridViewing):
    # TODO update documentation
    # background color is fill color for background in case no
    # background image is available.
    # bottom_text_display_height indicates the pixel height for the
    # area where text will appear at the bottom of the viewing.
    # bottom_text is the text to blit in the bottom_text_rect.
    # allowed_selection_option_set is a set of allowed option IDs to show for
    # icons selected in this viewing. Set to None or empty set to allow
    # no options.
    def __init__(
            self,
            main_display_surface,
            selection_icon_dimensions,
            display_pattern=display.PATTERN_2_ID,
            enlarged_selection_background_path=imagepaths.ITEM_LISTING_SELECTED_ENLARGED_BACKGROUND_PATH,
        ):
        selectionviewing.ItemSelectionGridViewing.__init__(
            self,
            main_display_surface,
            selection_icon_dimensions,
            display_pattern=display_pattern,
            enlarged_selection_background_path=enlarged_selection_background_path,
        )

    # Overridden.
    def create_selection_area_display(self):
        logger.info("Creating main selection area display...")
        font_obj = display.Display.get_font(
                fontinfo.SELECTION_SUPERTEXT_FONT_ID
            )
        if font_obj:
            self.icon_supertext_font_object = font_obj
            self.icon_supertext_font_color = viewingdata.COLOR_WHITE
            self.selection_area_display = equipmentdisplay.EquipmentDisplay(
                self.main_display_surface,
                self.selection_area_rect,
                self.selection_icon_dimensions,
                background_pattern=self.display_pattern,
                horizontal_padding=viewingdata.ITEM_LISTING_HORIZONTAL_PADDING,
                vertical_padding=viewingdata.ITEM_LISTING_VERTICAL_PADDING,
                selection_image_path=imagepaths.ITEM_LISTING_SELECTED_DEFAULT_PATH,
                non_selection_image_path=imagepaths.ITEM_LISTING_UNSELECTED_DEFAULT_PATH,
            )

            if not self.selection_area_display:
                logger.error("Failed to make selection area display")
        else:
            logger.error("Selection area supertext font not found.")
            logger.error("Must init fonts through display.Display.init_fonts.")

    # Overridden.
    def create_truncated_selection_area_display(self):
        logger.info("Creating truncated selection area display...")
        font_obj = display.Display.get_font(
                fontinfo.SELECTION_SUPERTEXT_FONT_ID
            )
        if font_obj:
            self.icon_supertext_font_object = font_obj
            self.icon_supertext_font_color = viewingdata.COLOR_WHITE
            self.truncated_selection_area_display = equipmentdisplay.EquipmentDisplay(
                self.main_display_surface,
                self.selection_area_rect,
                self.selection_icon_dimensions,
                background_pattern=self.display_pattern,
                horizontal_padding=viewingdata.ITEM_LISTING_HORIZONTAL_PADDING,
                vertical_padding=viewingdata.ITEM_LISTING_VERTICAL_PADDING,
                selection_image_path=imagepaths.ITEM_LISTING_SELECTED_DEFAULT_PATH,
                non_selection_image_path=imagepaths.ITEM_LISTING_UNSELECTED_DEFAULT_PATH,
            )

            if not self.truncated_selection_area_display:
                logger.error("Failed to make truncated selection area display")
        else:
            logger.error("Selection grid supertext font not found.")
            logger.error("Must init fonts through display.Display.init_fonts.")

    # Overridden.
    def blit_selection_description(self, selected_obj):
        # Blit item description and usage info.
        if selected_obj:
            item_info = "\n".join([
                selected_obj.get_description_info(),
            ])
            self.display_text_display_first_page(
                self.selection_description_display,
                item_info,
                advance_delay_ms=0,
                auto_advance=True,
                refresh_during=False,
                refresh_after=False,
                horizontal_orientation=display.ORIENTATION_LEFT_JUSTIFIED,
                vertical_orientation=display.ORIENTATION_TOP_JUSTIFIED,
                alternative_top_left=None,
            )

    def blit_main_selection_details(self, selection_info):
        self.blit_selected_object_name(selection_info[0])
        self.blit_selected_object_quantity(selection_info[1])
        self.blit_selected_object_enlarged_icon(selection_info[0])

    def blit_selection_details(self, selection_info):
        self.blit_main_selection_details(selection_info)
        self.blit_selection_description(selection_info[0])

    # Overridden.
    def convert_to_icon_data_list(self, equipment_dict):
        ret_data = None

        if equipment_dict:
            ret_data = {}

            for slot_id in itemdata.EQUIPMENT_SLOT_ID_LIST:
                equipment_info = equipment_dict.get(slot_id, None)

                quantity_text = None
                rendered_supertext = None
                curr_obj = None
                equipped_id = None

                if equipment_info:
                    equipped_id = equipment_info[0]
                    curr_obj = equipment_info[1]
                    quantity = equipment_info[2]

                    if curr_object.is_stackable():
                        quantity_text = display.Display.get_abbreviated_quantity(
                            quantity
                        )
                else:
                    equipped_id = slot_id
                    curr_obj= items.Item.get_item(slot_id)

                if curr_object:
                    curr_image = curr_object.get_icon()

                if quantity_text:
                    rendered_supertext = \
                    self.icon_supertext_font_object.render(
                        quantity_text,
                        False,
                        self.icon_supertext_font_color,
                    )

                ret_data[slot_id] = [curr_image, rendered_supertext]

        return ret_data

    # Overridden.
    def handle_selection_area(
            self,
            title_info,
            selection_data,
            starting_selected_index=0,
            preselected_index_list=None,
            custom_actions=None,
            bottom_text=None,
            allowed_selection_option_set=None,
        ):
        pass

    def handle_equipment_selection_area(
            self,
            title_info,
            selection_data, # Equipment dict.
            starting_selected_slot_id=itemdata.EQUIP_SLOT_HEAD,
            custom_actions=None,
            bottom_text=None,
            allowed_selection_option_set=None,
        ):

        ret_info = None
        icon_data_list = [] #$$

        display_to_use = self.selection_area_display

        if bottom_text:
            display_to_use = self.truncated_selection_area_display

        if selection_data:
            icon_data_list = self.convert_to_icon_data_list(selection_data)

        if selection_data and icon_data_list:
            # Start with the first item.
            curr_index = starting_selected_index
            first_viewable_row_index = \
                display_to_use.get_row_index(curr_index)
            last_viewable_row_index = \
                first_viewable_row_index \
                + display_to_use.num_rows \
                - 1

            done = False

            new_index = False
            changed_index = True

            while not done:
                curr_selected_row = display_to_use.get_row_index(
                        curr_index
                    )

                if curr_selected_row < first_viewable_row_index:
                    # Scroll down.
                    first_viewable_row_index = curr_selected_row
                    last_viewable_row_index = \
                        first_viewable_row_index \
                        + display_to_use.num_rows \
                        - 1
                elif curr_selected_row > last_viewable_row_index:
                    # Scroll up.
                    last_viewable_row_index = curr_selected_row
                    first_viewable_row_index = max(
                            0,
                            last_viewable_row_index \
                            - display_to_use.num_rows \
                            + 1
                        )

                logger.debug("Curr row index {0}. First viewable: {1}. Last viewable: {2}".format(
                    curr_selected_row,
                    first_viewable_row_index,
                    last_viewable_row_index
                ))

                if changed_index:
                    self.blit_selection_background(
                        title_info,
                        bottom_text=bottom_text,
                    )
                    pygame.display.update()

                go_down = False
                go_up = False
                go_left = False
                go_right = False
                open_options = False

                received_input = False

                curr_selection_info = selection_data[curr_index]

                if changed_index:
                    display_to_use.blit_icon_listing(
                        self.main_display_surface,
                        icon_data_list,
                        first_viewable_row_index,
                        curr_index,
                        preselected_index_list=preselected_index_list,
                        show_continue_icon=True,
                        alternative_top_left=None,
                    )

                    if curr_selection_info:
                        self.blit_selection_details(
                            curr_selection_info
                        )

                    pygame.display.update()

                while not received_input:
                    timekeeper.Timekeeper.tick()

                    for events in pygame.event.get():
                        if events.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit(0)
                        elif events.type == pygame.KEYDOWN:
                            if events.key == pygame.K_ESCAPE:
                                logger.info("Leaving selection viewing.")
                                received_input = True
                                done = True
                                go_down = False
                                go_up = False
                                go_left = False
                                go_right = False
                                open_options = False
                            elif events.key == pygame.K_DOWN:
                                logger.info("Going down in grid.")
                                go_down = True
                                go_up = False
                                go_left = False
                                go_right = False
                                open_options = False
                                received_input = True
                            elif events.key == pygame.K_UP:
                                logger.info("Going up in grid.")
                                go_down = False
                                go_up = True
                                go_left = False
                                go_right = False
                                open_options = False
                                received_input = True
                            elif events.key == pygame.K_LEFT:
                                logger.info("Going left in grid.")
                                go_down = False
                                go_up = False
                                go_left = True
                                go_right = False
                                open_options = False
                                received_input = True
                            elif events.key == pygame.K_RIGHT:
                                logger.info("Going right in grid.")
                                go_down = False
                                go_up = False
                                go_left = False
                                go_right = True
                                open_options = False
                                received_input = True
                            elif events.key == pygame.K_RETURN:
                                logger.info("Opening menu")
                                go_down = False
                                go_up = False
                                go_left = False
                                go_right = False
                                open_options = True
                                received_input = True
                            elif custom_actions and events.key in custom_actions:
                                ret_option_id = custom_actions.get(
                                    events.key,
                                    None
                                )

                                if ret_option_id:
                                    logger.info("Activating custom action {0}".format(
                                        ret_option_id
                                    ))
                                    received_input = True
                                    ret_info = (ret_option_id, curr_index)
                                    done = True
                                else:
                                    received_input = False

                                go_down = False
                                go_up = False
                                go_left = False
                                go_right = False
                                open_options = False

                if received_input:
                    new_index = curr_index
                    if go_down:
                        new_index = min(
                            max_index,
                            curr_index + display_to_use.num_columns
                        )
                    elif go_up:
                        new_index = max(
                            0,
                            curr_index - display_to_use.num_columns
                        )
                    elif go_right:
                        new_index = min(
                            max_index,
                            curr_index + 1
                        )
                    elif go_left:
                        new_index = max(
                            0,
                            curr_index - 1
                        )
                    elif open_options:
                        # Show item options.
                        self.blit_selection_background(
                            title_info,
                            bottom_text=bottom_text,
                        )

                        ret_option = self.display_selection_options(
                            curr_selection_info
                        )

                        if ret_option \
                            and ret_option != menuoptions.CANCEL_OPTION_ID:
                            done = True
                            ret_info = (ret_option, curr_index)
                        else:
                            self.blit_selection_background(
                                title_info,
                                bottom_text=bottom_text,
                            )

                            self.blit_selection_details(
                                curr_selection_info
                            )

                            pygame.display.update()

                    if new_index != curr_index:
                        changed_index = True
                        curr_index = new_index
                    else:
                        changed_index = False

                    logger.info("Curr index now: {0}".format(curr_index))
                    # TODO rest

        # Handle blank selection data.
        elif len(selection_data) == 0:
            self.blit_selection_background(
                title_info,
                bottom_text=bottom_text,
            )

            pygame.display.update()

            received_input = False

            while not received_input:
                timekeeper.Timekeeper.tick()

                for events in pygame.event.get():
                    if events.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit(0)
                    elif events.type == pygame.KEYDOWN:
                        if events.key == pygame.K_ESCAPE:
                            logger.info("Leaving selection viewing.")
                            received_input = True

        logger.info("Returning selection: {0}".format(ret_info))
        return ret_info

    @classmethod
    def create_equipment_viewing(
                cls,
                main_display_surface,
                item_icon_dimensions,
                display_pattern=display.PATTERN_2_ID,
            ):
        ret_viewing = None

        if main_display_surface:
            ret_viewing = EquipmentViewing(
                main_display_surface,
                item_icon_dimensions,
                display_pattern=display_pattern,
            )

            # Create displays for viewing.
            ret_viewing.create_base_displays()
            ret_viewing.create_additional_displays()

        return ret_viewing

# set up logger
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
