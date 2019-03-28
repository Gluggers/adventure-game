import equipmentdata
import viewingicondata
import pygame
import viewingicon
import logging

class EquipmentSlot(viewingicon.ViewingIcon):
    # Maps equipment IDs to equipment slot objects.
    slot_listing = {}

    def __init__(
            self,
            slot_id,
            name_info,
            description_info,
            image_path_dict=None,
            menu_option_ids=None,
        ):
        viewingicon.ViewingIcon.__init__(
            self,
            slot_id,
            name_info,
            description_info,
            image_path_dict=image_path_dict,
            menu_option_ids=menu_option_ids,
        )

    @classmethod
    def get_slot_object(cls, slot_id):
        return cls.slot_listing.get(slot_id, None)

    # Adds/updates the equipment slot object listing for the given object ID.
    # Returns True upon success, false otherwise.
    @classmethod
    def add_slot_object_to_listing(cls, slot_id, slot_obj):
        if slot_obj and (slot_id is not None):
            cls.slot_listing[slot_id] = slot_obj
            logger.debug("Added slot ID {0} to slot listing.".format(slot_id))
            return True
        else:
            return False

    @classmethod
    def equipment_slot_factory(cls, slot_id):
        ret_object = None

        # Check if we already have the item made.
        slot_from_listing = cls.get_slot_object(slot_id)

        if slot_from_listing:
            # Return the already made item.
            ret_object = item_from_listing
        else:
            # Make the new object ourselves. First, get the
            # object data.
            slot_data = equipmentdata.EQUIPMENT_SLOT_DATA.get(slot_id, None)

            if slot_data:
                # Get the slot fields
                name_info = slot_data.get(viewingicondata.NAME_INFO_FIELD, None)
                description_info = slot_data.get(viewingicondata.DESCRIPTION_INFO_FIELD, None)
                image_path_dict = slot_data.get(viewingicondata.IMAGE_PATH_DICT_FIELD, None)
                menu_option_ids = slot_data.get(
                    viewingicondata.OPTION_ID_LIST_FIELD,
                    None
                )

                # Ensure we have the required fields.
                if name_info and description_info:
                    # Make the slot object.
                    new_slot_obj = EquipmentSlot(
                        slot_id,
                        name_info,
                        description_info,
                        image_path_dict=image_path_dict,
                        menu_option_ids=menu_option_ids,
                    )

                    logger.debug("Made slot object with ID {0}".format(slot_id))

                    # Update the item mapping.
                    result = cls.add_slot_object_to_listing(
                        slot_id,
                        new_slot_obj
                    )

                    if result:
                        ret_object = new_slot_obj
                    else:
                        logger.error("Failed to add slot ID {0} to listing.".format(slot_id))
                else:
                    logger.error("Required fields not found in slot data for ID {0}".format(slot_id))
            else:
                logger.error("Slot data not found for item ID {0}".format(slot_id))

        return ret_object

    @classmethod
    def build_equipment_slots(cls):
        logger.info("Building equipment slots.")

        for slot_id in equipmentdata.EQUIPMENT_SLOT_DATA:
            if not cls.equipment_slot_factory(slot_id):
                logger.error("Could not construct equipment slot object with ID {0}".format(slot_id))


# set up logger
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
