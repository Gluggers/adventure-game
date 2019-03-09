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

class Item(pygame.sprite.Sprite):
    # Master dict mapping item IDs to item objects.
    item_listing = {}

    def __init__(
                self,
                item_id,
                name_info,
                description_info,
                usage_info={},
                image_path_dict={},
                base_value_low=0,
                base_value_high=0,
                weight_points=0,
                properties=(itemdata.SELLABLE_F | itemdata.ALCHABLE_F),
                interaction_id=None,
                required_creation_items={},
                required_creation_levels={},
                required_creation_quests=[],
                item_menu_option_ids=menuoptions.DEFAULT_ITEM_MENU_OPTION_IDS,
            ):
        # Call the parent class (Sprite) init
        pygame.sprite.Sprite.__init__(self)

        # Set up Item.
        self.item_id = item_id
        self.name_info = {}
        for lang_id, name_str in name_info.items():
            self.name_info[lang_id] = name_str

        self.description_info = {}
        for lang_id, desc_str in description_info.items():
            self.description_info[lang_id] = desc_str

        self.usage_info = {}
        for lang_id, usage_str in usage_info.items():
            self.usage_info[lang_id] = usage_str

        self.image_dict = {}
        for image_type_id, image_path in image_path_dict.items():
            logger.debug("Loading image from path {0}".format(image_path))
            # convert alpha for transparency
            self.image_dict[image_type_id] = \
                pygame.image.load(image_path).convert_alpha()

        self.curr_image_id = imageids.OW_IMAGE_ID_DEFAULT

        self.equipment_slot_id = itemdata.EQUIP_SLOT_NONE
        self.base_value_low = base_value_low
        self.base_value_high = base_value_high
        self.weight_points = weight_points
        self.properties = properties
        self.interaction_id = interaction_id

        self.required_creation_item_mapping = {}
        for item_id, quantity in required_creation_items.items():
            self.required_creation_item_mapping[item_id] = quantity

        self.required_creation_level_mapping = {}
        for skill_id, level in required_creation_levels.items():
            self.required_creation_level_mapping[skill_id] = level

        self.required_creation_quests = []
        for quest_id in required_creation_quests:
            self.required_creation_quests.append(quest_id)

        self.item_menu_option_ids = menuoptions.DEFAULT_ITEM_MENU_OPTION_IDS
        if item_menu_option_ids:
            self.item_menu_option_ids = []
            for option_id in item_menu_option_ids:
                self.item_menu_option_ids.append(option_id)

    def get_name(self, language_id=language.Language.current_language_id):
        ret_name = ""
        if language_id is not None:
            ret_name = self.name_info.get(language_id, "")

        return ret_name

    def get_image(self, image_id):
        return self.image_dict.get(image_id, None)

    def get_icon(self):
        return self.get_image(imageids.ITEM_ICON_IMAGE_ID)

    # Returns the appropriate language translation for the item's usage
    # info string.
    def get_usage_info(self, language_id=language.Language.current_language_id):
        ret_str = "?????"

        if (language_id is not None) and self.usage_info:
            info = self.usage_info.get(language_id, None)
            if info:
                ret_str = info
        elif self.name_info:
            ret_str = self.get_name(language_id=langauge_id)

        return ret_str

    # Returns the appropriate language translation for the item's description
    # info string.
    def get_description_info(
                self,
                language_id=language.Language.current_language_id
            ):
        ret_str = "?????"

        if (language_id is not None) and self.description_info:
            info = self.description_info.get(language_id, None)
            if info:
                ret_str = info
        elif self.name_info:
            ret_str = ret_str = self.get_name(language_id=langauge_id)

        return ret_str

    def is_stackable(self):
        if self.properties & itemdata.STACKABLE_F:
            return True
        else:
            return False

    @classmethod
    def get_item(cls, item_id):
        return cls.item_listing.get(item_id, None)

    # Adds/updates the interactive object listing for the given object ID.
    # Returns True upon success, false otherwise.
    @classmethod
    def add_item_to_listing(cls, item_id, item_obj):
        if item_obj and (item_id is not None):
            cls.item_listing[item_id] = item_obj
            logger.debug("Added item ID {0} to item listing.".format(item_id))
            return True
        else:
            return False

    # Factory method to create items that are not equippable nor
    # consumable.
    @classmethod
    def standard_item_factory(cls, item_id):
        ret_item = None

        # Check if we already have the item made.
        item_from_listing = cls.get_item(item_id)

        if item_from_listing:
            # Return the already made item.
            ret_object = item_from_listing
        else:
            # Make the new object ourselves. First, get the
            # object data.
            item_data = itemdata.STANDARD_ITEM_DATA.get(item_id, None)

            if item_data:
                # Get the item fields
                # TODO - change default values?
                name_info = item_data.get(itemdata.NAME_INFO_FIELD, {})
                description_info = item_data.get(itemdata.DESCRIPTION_INFO_FIELD, {})
                usage_info = item_data.get(itemdata.USAGE_INFO_FIELD, {})
                image_path_dict = item_data.get(itemdata.IMAGE_PATH_DICT_FIELD, {})
                base_value_low = item_data.get(itemdata.BASE_VALUE_LOW_FIELD, 0)
                base_value_high = item_data.get(itemdata.BASE_VALUE_HIGH_FIELD, 0)
                weight_points = item_data.get(itemdata.WEIGHT_POINT_FIELD, 0)
                properties = item_data.get(
                        itemdata.PROPERTIES_FIELD,
                        (itemdata.SELLABLE_F | itemdata.ALCHABLE_F)
                    )
                interaction_id = item_data.get(
                        itemdata.INTERACTION_ID_FIELD,
                        None
                    )
                required_creation_items = item_data.get(
                        itemdata.CREATE_REQ_ITEMS_FIELD,
                        {}
                    )
                required_creation_levels = item_data.get(
                        itemdata.CREATE_REQ_LEVELS_FIELD,
                        {}
                    )
                required_creation_quests = item_data.get(
                        itemdata.CREATE_REQ_QUEST_FIELD,
                        []
                    )
                item_menu_option_ids = item_data.get(
                        itemdata.ITEM_OPTION_ID_LIST_FIELD,
                        menuoptions.DEFAULT_ITEM_MENU_OPTION_IDS
                    )


                # Ensure we have the required fields.
                if name_info and description_info:
                    # Make the item.
                    new_item = Item(
                        item_id,
                        name_info,
                        description_info,
                        usage_info=usage_info,
                        image_path_dict=image_path_dict,
                        base_value_low=base_value_low,
                        base_value_high=base_value_high,
                        weight_points=weight_points,
                        properties=properties,
                        interaction_id=interaction_id,
                        required_creation_items=required_creation_items,
                        required_creation_levels=required_creation_levels,
                        required_creation_quests=required_creation_quests,
                        item_menu_option_ids=item_menu_option_ids,
                    )

                    logger.debug("Made item with ID {0}".format(item_id))

                    # Update the item mapping.
                    result = cls.add_item_to_listing(
                        item_id,
                        new_item
                    )

                    if result:
                        ret_item = new_item
                    else:
                        logger.error("Failed to add item ID {0} to listing.".format(item_id))
                else:
                    logger.error("Required fields not found in item data for ID {0}".format(item_id))
            else:
                logger.error("Item data not found for item ID {0}".format(item_id))

        return ret_item

    @classmethod
    def build_standard_items(cls):
        logger.info("Building standard items.")

        for item_id in itemdata.STANDARD_ITEM_DATA:
            if not cls.standard_item_factory(item_id):
                logger.error("Could not construct item with ID {0}".format(item_id))

class Equipable_Item(Item):
    def __init__(
                self,
                item_id,
                name_info,
                equipment_slot_id,
                description_info,
                usage_info={},
                image_path_dict={},
                base_value_low=0,
                base_value_high=0,
                weight_points=0,
                properties=(itemdata.SELLABLE_F | itemdata.ALCHABLE_F),
                interaction_id=interactiondata.DEFAULT_ID,
                required_creation_items={},
                required_creation_levels={},
                required_creation_quests=[],
                item_menu_option_ids=menuoptions.DEFAULT_ITEM_MENU_OPTION_IDS,
                combat_type=battledata.COMBAT_TYPE_NONE,
                attack_value_info={},
                defense_value_info={},
                combat_boost_info={},
                required_equip_levels={},
                required_equip_quests=[],
            ):
        Item.__init__(
            self,
            item_id,
            name_info,
            description_info,
            usage_info=usage_info,
            image_path_dict=image_path_dict,
            base_value_low=base_value_low,
            base_value_high=base_value_high,
            weight_points=weight_points,
            properties=properties,
            interaction_id=interaction_id,
            required_creation_items=required_creation_items,
            required_creation_levels=required_creation_levels,
            required_creation_quests=required_creation_quests,
            item_menu_option_ids=item_menu_option_ids,
        )

        self.equipment_slot_id = equipment_slot_id
        self.combat_type = combat_type
        self.attack_value_info = {}
        for damage_type, value in attack_value_info.items():
            self.attack_value_info[damage_type] = value

        self.defense_value_info = {}
        for damage_type, value in defense_value_info.items():
            self.defense_value_info[damage_type] = value

        self.combat_boost_info = {}
        for boost_type, value_tuple in combat_boost_info.items():
            self.combat_boost_info[boost_type] = value_tuple

        self.required_equip_level_mapping = {}
        for skill_id, level in required_equip_levels.items():
            self.required_equip_level_mapping[skill_id] = level

        self.required_equip_quests = []
        for quest_id in required_equip_quests:
            self.required_equip_quests.append(quest_id)

class Consumable_Item(Item):
    def __init__(
                self,
                item_id,
                name_info,
                description_info,
                heal_value=0,
                usage_info={},
                image_path_dict={},
                base_value_low=0,
                base_value_high=0,
                weight_points=0,
                properties=(itemdata.SELLABLE_F | itemdata.ALCHABLE_F),
                interaction_id=interactiondata.DEFAULT_ID,
                required_creation_items={},
                required_creation_levels={},
                required_creation_quests=[],
                item_menu_option_ids=menuoptions.DEFAULT_ITEM_MENU_OPTION_IDS,
                skill_effect_info={},
                combat_boost_info={},
                required_consume_quests=[],
            ):
        Item.__init__(
            self,
            item_id,
            name_info,
            description_info,
            usage_info=usage_info,
            image_path_dict=image_path_dict,
            base_value_low=base_value_low,
            base_value_high=base_value_high,
            weight_points=weight_points,
            properties=properties,
            interaction_id=interaction_id,
            required_creation_items=required_creation_items,
            required_creation_levels=required_creation_levels,
            required_creation_quests=required_creation_quests,
            item_menu_option_ids=item_menu_option_ids,
        )

        self.heal_value = 0
        self.skill_effect_info = {}
        for skill_id, effect_info in skill_effect_info.items():
            self.skill_effect_info[skill_id] = effect_info

        self.combat_boost_info = {}
        for boost_type, value_tuple in combat_boost_info.items():
            self.combat_boost_info[boost_type] = value_tuple

        self.required_consume_quests = []
        for quest_id in required_consume_quests:
            self.required_consume_quests.append(quest_id)

# set up logger
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
