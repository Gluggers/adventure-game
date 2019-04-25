# -*- coding: utf-8 -*-
"""This module contains classes and methods for Spell objects.

Spell objects represent and contain information for the various spells in the
game.  Spells are visualized in the spell viewing, and thus inherit from the
ViewingIcon class.
"""

import logging
import sys
import magicdata
import viewingicon
import viewingicondata

class Spell(viewingicon.ViewingIcon):
    # Maps spell IDs to spell objects.
    _spell_listing = {}

    def __init__(
            self,
            spell_id,
            name_info,
            description_info,
            spell_class,
            spell_types,
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
        self._spell_types = set()

        for spell_type in spell_types:
            self._spell_types.add(spell_type)

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

        return cls._spell_listing.get(spell_id, None)

    #$$ TODO change these.
    @classmethod
    def _add_spell_to_listing(cls, spell_id, spell_obj):
        """Adds the spell object to the class spell listing
        for the given spell ID. Returns True on success,
        False on failure.

        Args:
            spell_id: spell ID for the spell object.
            spell_obj: spell object to set for the spell ID.

        Returns:
            True on success, False on failure.
        """

        if spell_obj and (spell_id is not None):
            cls._spell_listing[spell_id] = spell_obj
            LOGGER.debug(
                "Added spell ID %d to spell listing.",
                spell_id,
            )
            return True
        else:
            return False

    @classmethod
    def spell_factory(cls, spell_id):
        """Creates and returns a spell object associated with the
        given spell ID."""

        ret_object = None

        # Check if we already have the item made.
        spell_from_listing = cls.get_spell_object(spell_id)

        if spell_from_listing:
            # Return the already made item.
            ret_object = spell_from_listing
        else:
            # Make the new object ourselves. First, get the
            # object data.
            spell_data = magicdata.SPELL_OBJECT_DATA.get(spell_id, None)

            if spell_data:
                # Get the spell fields.
                name_info = spell_data.get(viewingicondata.NAME_INFO_FIELD, None)
                description_info = spell_data.get(viewingicondata.DESCRIPTION_INFO_FIELD, None)
                image_path_dict = spell_data.get(viewingicondata.IMAGE_PATH_DICT_FIELD, None)
                menu_option_ids = spell_data.get(
                    viewingicondata.OPTION_ID_LIST_FIELD,
                    None
                )
                spell_class = spell_data.get(magicdata.SPELL_CLASS_FIELD, None)
                spell_types = spell_data.get(magicdata.SPELL_TYPES_FIELD, None)
                required_level = spell_data.get(
                    magicdata.SPELL_REQUIRED_LEVEL_FIELD,
                    1
                )
                required_mana = spell_data.get(
                    magicdata.SPELL_REQUIRED_MANA_FIELD,
                    0
                )
                damage_types = spell_data.get(
                    magicdata.SPELL_DAMAGE_TYPES_FIELD,
                    None
                )
                base_power = spell_data.get(
                    magicdata.SPELL_BASE_POWER_FIELD,
                    0
                )
                required_quests = spell_data.get(
                    magicdata.SPELL_REQUIRED_QUESTS_FIELD,
                    None
                )
                required_equipped_items = spell_data.get(
                    magicdata.SPELL_REQUIRED_EQUIPPED_ITEMS_FIELD,
                    None
                )

                # Ensure we have the required fields.
                if name_info and description_info \
                    and spell_class and spell_types:
                    # Make the spell object.
                    new_spell_obj = Spell(
                        spell_id,
                        name_info,
                        description_info,
                        spell_class,
                        spell_types,
                        image_path_dict=image_path_dict,
                        menu_option_ids=menu_option_ids,
                        required_level=required_level,
                        required_mana=required_mana,
                        damage_types=damage_types,
                        base_power=base_power,
                        required_quests=required_quests,
                        required_equipped_items=required_equipped_items,
                    )

                    LOGGER.debug(
                        "Made spell object with ID %d",
                        spell_id,
                    )

                    # Update the item mapping.
                    result = Spell._add_spell_to_listing(
                        spell_id,
                        new_spell_obj
                    )

                    if result:
                        ret_object = new_spell_obj
                    else:
                        LOGGER.error(
                            "Failed to add spell ID %d to listing.",
                            spell_id,
                        )
                        sys.exit(2)
                else:
                    LOGGER.error(
                        "Required fields not found in spell data for ID %d",
                        spell_id,
                    )
                    sys.exit(2)
            else:
                LOGGER.error(
                    "spell data not found for spell ID %d",
                    spell_id,
                )
                sys.exit(2)

        return ret_object

    @classmethod
    def build_spells(cls):
        """Creates the available spell objects."""

        LOGGER.info("Building spells.")

        for spell_id in magicdata.SPELL_OBJECT_DATA:
            if not cls.spell_factory(spell_id):
                LOGGER.error(
                    "Could not construct spell object with ID %d",
                    spell_id,
                )
                sys.exit(2)

# Set up logger.
logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)
