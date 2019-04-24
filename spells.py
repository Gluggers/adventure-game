# -*- coding: utf-8 -*-
"""This module contains classes and methods for Spell objects.

Spell objects represent and contain information for the various spells in the
game.  Spells are visualized in the spell viewing, and thus inherit from the
ViewingIcon class.
"""

import logging
import magicdata
import viewingicon
import viewingicondata

class Spell(viewingicon.ViewingIcon):
    # Maps spell IDs to spell objects.
    spell_listing = {}

    def __init__(
            self,
            spell_id,
            name_info,
            description_info,
            spell_class,
            spell_type,
            image_path_dict=None,
            menu_option_ids=None,
            required_level=1,
            required_mana=1,
            damage_types=None,
            base_power=0,
            required_quests=None,
            required_equipped_items=None,
        ):
        """Initializes the spell object.

        Args:
            spell_id: spell  ID for the object.
            name_info: dict that maps language IDs to Strings for the name
                translations of the spell.
            description_info: dict that maps language IDs to Strings for the
                translations of the spell description.
            image_path_dict: dict that maps image sequence IDs to the
                image path info.
            menu_option_ids: list of menu option IDs for the spell.
            base_power: base damage if the spell does damage, base heal
                if the spell heals.
            # TODO
        """

        viewingicon.ViewingIcon.__init__(
            self,
            spell_id,
            name_info,
            description_info,
            image_path_dict=image_path_dict,
            menu_option_ids=menu_option_ids,
        )

        self._spell_class = spell_class
        self._spell_type = spell_type
        self._required_level = max(1, required_level)
        self._required_mana = max(0, required_mana)
        self._base_power = max(0, base_power)

        self._damage_types = set()
        if damage_types:
            for damage_type in damage_types:
                self._damage_types.add(damage_type)

        self._required_quests = set()
        if required_quests:
            for quest_id in required_quests:
                self._required_quests.add(quest_id)

        self._required_equipped_items = {}
        if required_equipped_items:
            for slot_id, item_id in required_equipped_items.items():
                self._required_equipped_items[slot_id] = item_id

    @classmethod
    def get_spell_object(cls, spell_id):
        """Returns the spell object for the given spell ID."""

        return cls.spell_listing.get(spell_id, None)

    #$$ TODO change these.
    # Adds/updates the equipment slot object listing for the given object ID.
    # Returns True upon success, false otherwise.
    @classmethod
    def _add_slot_object_to_listing(cls, slot_id, slot_obj):
        """Adds the equipment slot object to the class equipment slot listing
        for the given equipment slot ID. Returns True on success,
        False on failure.

        Args:
            slot_id: equipment slot ID for the slot object.
            slot_obj: equipment slot object to set for the slot ID.

        Returns:
            True on success, False on failure.
        """

        if slot_obj and (slot_id is not None):
            cls.slot_listing[slot_id] = slot_obj
            LOGGER.debug(
                "Added slot ID %d to slot listing.",
                slot_id,
            )
            return True
        else:
            return False

    @classmethod
    def equipment_slot_factory(cls, slot_id):
        """Creates and returns an equipment slot object associated with the
        given equipment slot ID."""

        ret_object = None

        # Check if we already have the item made.
        slot_from_listing = cls.get_slot_object(slot_id)

        if slot_from_listing:
            # Return the already made item.
            ret_object = slot_from_listing
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

                    LOGGER.debug(
                        "Made slot object with ID %d",
                        slot_id,
                    )

                    # Update the item mapping.
                    result = EquipmentSlot._add_slot_object_to_listing(
                        slot_id,
                        new_slot_obj
                    )

                    if result:
                        ret_object = new_slot_obj
                    else:
                        LOGGER.error(
                            "Failed to add slot ID %d to listing.",
                            slot_id,
                        )
                else:
                    LOGGER.error(
                        "Required fields not found in slot data for ID %d",
                        slot_id,
                    )
            else:
                LOGGER.error(
                    "Slot data not found for item ID %d",
                    slot_id,
                )

        return ret_object

    @classmethod
    def build_equipment_slots(cls):
        """Creates the available equipment slot objects."""

        LOGGER.info("Building equipment slots.")

        for slot_id in equipmentdata.EQUIPMENT_SLOT_DATA:
            if not cls.equipment_slot_factory(slot_id):
                LOGGER.error(
                    "Could not construct equipment slot object with ID %d",
                    slot_id,
                )

# Set up logger.
logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)
