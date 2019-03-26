import pygame
import viewing
import viewingdata
import items
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


# SELECTION DIRECTION CONSTANTS
MOVE_UP = 0x1
MOVE_RIGHT = 0x2
MOVE_DOWN = 0x3
MOVE_LEFT = 0x4

# Maps equipment IDs to the dict that maps directions one can
# traverse in the display to the adjacent equipment slot ID.
ALLOWED_MOVEMENT_MAPPING = {
    itemdata.EQUIP_SLOT_HEAD: {
        MOVE_DOWN: itemdata.EQUIP_SLOT_NECK,
        MOVE_LEFT: itemdata.EQUIP_SLOT_AMMO,
        MOVE_RIGHT: itemdata.EQUIP_SLOT_BACK,
    },
    itemdata.EQUIP_SLOT_MAIN_HAND: {
        MOVE_UP: itemdata.EQUIP_SLOT_AMMO,
        MOVE_DOWN: itemdata.EQUIP_SLOT_HANDS,
        MOVE_RIGHT: itemdata.EQUIP_SLOT_MAIN_BODY,
    },
    itemdata.EQUIP_SLOT_OFF_HAND: {
        MOVE_UP: itemdata.EQUIP_SLOT_BACK,
        MOVE_DOWN: itemdata.EQUIP_SLOT_WRIST,
        MOVE_LEFT: itemdata.EQUIP_SLOT_MAIN_BODY,
    },
    itemdata.EQUIP_SLOT_MAIN_BODY: {
        MOVE_UP: itemdata.EQUIP_SLOT_NECK,
        MOVE_DOWN: itemdata.EQUIP_SLOT_LEGS,
        MOVE_LEFT: itemdata.EQUIP_SLOT_MAIN_HAND,
        MOVE_RIGHT: itemdata.EQUIP_SLOT_OFF_HAND,
    },
    itemdata.EQUIP_SLOT_LEGS: {
        MOVE_UP: itemdata.EQUIP_SLOT_MAIN_BODY,
        MOVE_DOWN: itemdata.EQUIP_SLOT_FEET,
        MOVE_LEFT: itemdata.EQUIP_SLOT_HANDS,
        MOVE_RIGHT: itemdata.EQUIP_SLOT_WRIST,
    },
    itemdata.EQUIP_SLOT_NECK: {
        MOVE_UP: itemdata.EQUIP_SLOT_HEAD,
        MOVE_DOWN: itemdata.EQUIP_SLOT_MAIN_BODY,
        MOVE_LEFT: itemdata.EQUIP_SLOT_AMMO,
        MOVE_RIGHT: itemdata.EQUIP_SLOT_BACK,
    },
    itemdata.EQUIP_SLOT_AMMO: {
        MOVE_UP: itemdata.EQUIP_SLOT_HEAD,
        MOVE_DOWN: itemdata.EQUIP_SLOT_MAIN_HAND,
        MOVE_RIGHT: itemdata.EQUIP_SLOT_NECK,
    },
    itemdata.EQUIP_SLOT_HANDS: {
        MOVE_UP: itemdata.EQUIP_SLOT_MAIN_HAND,
        MOVE_DOWN: itemdata.EQUIP_SLOT_FEET,
        MOVE_RIGHT: itemdata.EQUIP_SLOT_LEGS,
    },
    itemdata.EQUIP_SLOT_FEET: {
        MOVE_UP: itemdata.EQUIP_SLOT_LEGS,
        MOVE_LEFT: itemdata.EQUIP_SLOT_HANDS,
        MOVE_RIGHT: itemdata.EQUIP_SLOT_RING,
    },
    itemdata.EQUIP_SLOT_RING: {
        MOVE_UP: itemdata.EQUIP_SLOT_WRIST,
        MOVE_LEFT: itemdata.EQUIP_SLOT_FEET,
    },
    itemdata.EQUIP_SLOT_BACK: {
        MOVE_UP: itemdata.EQUIP_SLOT_HEAD,
        MOVE_DOWN: itemdata.EQUIP_SLOT_OFF_HAND,
        MOVE_LEFT: itemdata.EQUIP_SLOT_NECK,
    },
    itemdata.EQUIP_SLOT_WRIST: {
        MOVE_UP: itemdata.EQUIP_SLOT_OFF_HAND,
        MOVE_DOWN: itemdata.EQUIP_SLOT_RING,
        MOVE_LEFT: itemdata.EQUIP_SLOT_LEGS,
    },
}

EQUIPMENT_VIEWING_NAME_INFO = {
    language.LANG_ENGLISH: "Equipment",
    language.LANG_ESPANOL: "Equipo"

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
    def convert_to_icon_data(self, equipment_dict):
        ret_data = None

        if equipment_dict is not None:
            ret_data = {}

            for slot_id in itemdata.EQUIPMENT_SLOT_ID_LIST:
                equipment_info = equipment_dict.get(slot_id, None)

                quantity_text = None
                rendered_supertext = None
                curr_object = None
                equipped_id = None
                curr_image = None

                if equipment_info:
                    equipped_id = equipment_info[0]
                    curr_object = equipment_info[1]
                    quantity = equipment_info[2]

                    if curr_object.is_stackable():
                        quantity_text = display.Display.get_abbreviated_quantity(
                            quantity
                        )
                else:
                    equipped_id = slot_id
                    curr_object = items.Item.get_item(slot_id)

                if curr_object:
                    curr_image = curr_object.get_icon()
                else:
                    logger.warn("Couldn't get image.")

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
        icon_data_mapping = {}
        curr_slot_id = None

        display_to_use = self.selection_area_display

        if bottom_text:
            display_to_use = self.truncated_selection_area_display

        if selection_data is not None:
            icon_data_mapping = self.convert_to_icon_data(selection_data)

        logger.info("{0} items in icon data mapping.".format(
            len(icon_data_mapping)
        ))

        if icon_data_mapping:
            curr_slot_id = starting_selected_slot_id

            done = False

            new_slot_id = None
            changed_id = True

            while not done:
                movement_dir = None
                open_options = False

                received_input = False

                curr_selection_info = None
                equipped_info = selection_data.get(curr_slot_id, None)

                if equipped_info:
                    # We only want item object and quantity.
                    curr_selection_info = equipped_info[1:3]
                else:
                    curr_slot_obj = items.Item.get_item(curr_slot_id)
                    curr_selection_info = [curr_slot_obj, None]

                if changed_id:
                    self.blit_selection_background(
                        title_info,
                        bottom_text=bottom_text,
                    )
                    display_to_use.blit_equipment_icons(
                        self.main_display_surface,
                        icon_data_mapping,
                        selected_slot_id=curr_slot_id,
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
                                logger.info("Leaving equipment viewing.")
                                received_input = True
                                done = True
                            elif events.key == pygame.K_DOWN:
                                logger.info("Going down in viewing.")
                                movement_dir = MOVE_DOWN
                                received_input = True
                            elif events.key == pygame.K_UP:
                                logger.info("Going up in viewing.")
                                movement_dir = MOVE_UP
                                received_input = True
                            elif events.key == pygame.K_LEFT:
                                logger.info("Going left in viewing.")
                                movement_dir = MOVE_LEFT
                                received_input = True
                            elif events.key == pygame.K_RIGHT:
                                logger.info("Going right in viewing.")
                                movement_dir = MOVE_RIGHT
                                received_input = True
                            elif events.key == pygame.K_RETURN:
                                logger.info("Opening menu")
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
                                    ret_info = (ret_option_id, curr_slot_id)
                                    done = True

                if received_input:
                    new_slot_id = curr_slot_id

                    if open_options:
                        # Show item options.
                        ret_option = self.display_selection_options(
                            curr_selection_info
                        )

                        if ret_option \
                            and ret_option != menuoptions.CANCEL_OPTION_ID:
                            done = True
                            ret_info = (ret_option, curr_slot_id)
                        else:
                            if curr_selection_info:
                                self.blit_selection_details(
                                    curr_selection_info
                                )
                            pygame.display.update()
                            
                    elif movement_dir is not None:
                        # Move to other slot if possible.
                        new_slot_id = ALLOWED_MOVEMENT_MAPPING.get(
                            curr_slot_id,
                            {}
                        ).get(
                            movement_dir,
                            curr_slot_id
                        )

                    if new_slot_id is not None and new_slot_id != curr_slot_id:
                        changed_id = True
                        curr_slot_id = new_slot_id
                    else:
                        changed_id = False

                    logger.info("Curr id now: {0}".format(curr_slot_id))
                    # TODO rest

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
