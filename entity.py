import pygame
import tiledata
import map
import mapdata
import skills
import interactiveobj
import objdata
import logging
import interactiondata
import language
import imageids
import items
import inventory
import itemdata

### CONSTANTS ###
GENDER_NEUTRAL = 0x0
GENDER_MALE = 0x1
GENDER_FEMALE = 0x2

RACE_DEFAULT = 0x0
RACE_HUMAN = 0x1

START_NUM_GOLD_COINS = 100

DEFAULT_MAX_HEALTH = 10

class Entity(interactiveobj.Interactive_Object):
    # id represents the object ID.
    # name_info maps language ID to entity name.
    # image_path_dict maps image type IDs to the file paths for the image.
    # collision_width and collision_height define the tile dimensions
    # for the object's collision space. Must be integers greater than or equal
    # to 1?
    # skill_levels maps the skill ID to the corresponding level
    # for the entity (skill ID -> level). The method will automatically
    # calculate the experience required for the level and set it accordingly
    # for the entity.  Excluding the skill_levels dict or excluding individual
    # skill IDs will set default values.
    # equipment_dict maps the equipment slot ID to a length-3 list of form
    # [equipped item ID, item object, quantity of item].
    # manual_hitpoints allows manually setting the number of hitpoints
    # for the entity. If None, hitpoints will be set according to
    # the default formula of 10*hitpoints level.
    def __init__(
                    self,
                    id,
                    name_info,
                    image_path_dict,
                    collision_width=1,
                    collision_height=1,
                    skill_levels={},
                    equipment_dict={},
                    gender=GENDER_NEUTRAL,
                    race=RACE_HUMAN,
                    examine_info=None,
                    interaction_id=interactiondata.DEFAULT_ID,
                    manual_hitpoints=None,
                ):
        interactiveobj.Interactive_Object.__init__(
            self,
            objdata.TYPE_CHARACTER,
            name_info,
            id,
            image_path_dict,
            collision_width=collision_width,
            collision_height=collision_height,
            examine_info=examine_info,
            interaction_id=interaction_id,
        )

        self.gender = gender
        self.race = race

        # By default, face south.
        self.facing_direction = mapdata.DIR_SOUTH
        self.curr_image_id = imageids.OW_IMAGE_ID_FACE_SOUTH

        # Set up skills. self.skill_info_mapping maps skill IDs to
        # a length-3 list
        # [skill level, current experience, experience to next level]
        self.skill_info_mapping = {}

        for skill_id in skills.SKILL_ID_NAME_MAPPING:
            # See if caller passed in a custom level for the skill.
            skill_level = skill_levels.get(skill_id, None)

            # Default hitpoints level is different.
            if not skill_level:
                if skill_id == skills.SKILL_ID_HITPOINTS:
                    skill_level = skills.DEFAULT_LEVEL_HITPOINTS
                else:
                    skill_level = skills.DEFAULT_LEVEL

            # Get the required experience for the level.
            exp = skills.get_experience_from_level(skill_level)

            # Get remaining experience for next level.
            remaining_exp = skills.get_experience_to_next_level(
                    skill_level,
                    exp
                )

            logger.debug(
                ("Setting skill level {0}, exp {1}. " \
                + "exp to next level {2}").format(
                    skill_level,
                    exp,
                    remaining_exp
                )
            )

            # Record skill information.
            self.skill_info_mapping[skill_id] = [
                                                    skill_level,
                                                    exp,
                                                    remaining_exp
                                                ]

        # Set up health - use hitpoint stat if possible,
        # otherwise default hitpoints value.
        self.max_health = DEFAULT_MAX_HEALTH
        if manual_hitpoints and (manual_hitpoints > 0):
            self.max_health = manual_hitpoints
        else:
            hitpoint_level = self.skill_info_mapping.get(
                skills.SKILL_ID_HITPOINTS, [skills.DEFAULT_LEVEL_HITPOINTS]
            )[0]
            max_health = Entity.calculate_max_health(hitpoint_level)

            if max_health:
                self.max_health = max_health

        self.curr_health = self.max_health

        # Set up equipment. The equipment_dict will map equipment slot ID
        # to length-2 list of [item object, quantity].
        self.equipment_dict = {}
        for equipment_slot_id, item_info_list in equipment_dict.items():
            item_id = item_info_list[0]
            quantity = item_info_list[1]

            # Get item object.
            item_obj = items.Item.get_item(item_id)

            if item_obj and quantity > 0:
                self.equipment_dict[equipment_slot_id] = [
                        item_id,
                        item_obj,
                        quantity,
                    ]

        # Maps Item IDs to the number of items held.
        self.inventory = inventory.Inventory.inventory_factory()

    def inventory_full(self):
        return self.inventory.is_full()

    def add_item_to_inventory_by_id(self, item_id, quantity=1):
        return self.inventory.add_item_by_id(item_id, quantity=quantity)

    def add_item_to_tool_inventory_by_id(self, item_id, quantity=1):
        return self.tool_inventory.add_item_by_id(item_id, quantity=quantity)

    def has_item_equipped(self, item_id):
        has_equipped = False

        for equipment_slot_id, equipped_item_info in self.equipment_dict.items():
            if equipped_item_info[0] == item_id:
                has_equipped = True

        return has_equipped

    def has_tool_id(self, item_id):
        return self.tool_inventory.has_item_id_in_inventory(item_id)

    # TODO test this.
    def has_item(self, item_id):
        return self.inventory.has_item_id_in_inventory(item_id) \
            or self.has_item_equipped(item_id) \
            or self.has_tool_id(item_id)

    def get_skill_level(self, skill_id):
        ret_level = None

        if skill_id is not None:
            skill_info = self.skill_info_mapping.get(skill_id, None)

            if skill_info:
                ret_level = skill_info[0]

        return ret_level

    def get_skill_experience(self, skill_id):
        ret_exp = None

        if skill_id is not None:
            skill_info = self.skill_info_mapping.get(skill_id, None)

            if skill_info:
                ret_exp = skill_info[1]

        return ret_exp

    def get_experience_to_next_level(self, skill_id):
        ret_exp = None

        if skill_id is not None:
            skill_info = self.skill_info_mapping.get(skill_id, None)

            if skill_info:
                ret_exp = skill_info[2]

        return ret_exp

    # Returns the number of levels gained when adding exp to skill_id.
    def gain_experience(self, skill_id, exp):
        levels_gained = 0

        if (skill_id is not None) and exp and (exp > 0):
            skill_info = self.skill_info_mapping.get(skill_id, None)
            exp_to_process = exp

            if skill_info:
                old_level = skill_info[0]
                old_exp = skill_info[1]

                new_exp = old_exp + exp
                new_level = skills.get_level_from_experience(new_exp)
                new_exp_to_next_level = skills.get_experience_to_next_level(
                        new_level,
                        new_exp
                    )

                if new_level < old_level:
                    logger.error("Error in exp gain.")
                else:
                    logger.info(
                        ("Started at level {0} with {1} exp " \
                        + "({2} remaining to next level.)").format(
                            old_level,
                            old_exp,
                            skill_info[2]
                        )
                    )
                    logger.info(
                        ("Now reached level {0} with {1} " \
                        + " exp ({2} remaining to next level.)").format(
                            new_level,
                            new_exp,
                            new_exp_to_next_level,
                        )
                    )

                    skill_info[0] = new_level
                    skill_info[1] = new_exp
                    skill_info[2] = new_exp_to_next_level

                    self.skill_info_mapping[skill_id] = skill_info

                    levels_gained = max(0, new_level - old_level)

        return levels_gained

    # reblit the entity to face the specified direction.
    # Can specify either top_left_pixel or
    # bottom_left_pixel as the reference point for blitting the image.
    # bottom_left_pixel is recommended for images that are larger than
    # a single Tile image. If both top_left_pixel and bottom_left_pixel are
    # specified, the method will use bottom_left_pixel as an override.
    # top_left_pixel and bottom_left_pixel are tuples of pixel coordinates.
    # DOES NOT update surface - caller will have to do that
    def face_direction(
                self,
                surface,
                direction,
                bottom_left_pixel=None,
                top_left_pixel=None,
            ):
        image_id = None

        if self and surface and (bottom_left_pixel or top_left_pixel):
            if direction == mapdata.DIR_NORTH:
                image_id = imageids.OW_IMAGE_ID_FACE_NORTH
                logger.debug("Facing NORTH")
            elif direction == mapdata.DIR_EAST:
                image_id = imageids.OW_IMAGE_ID_FACE_EAST
                logger.debug("Facing EAST")
            elif direction == mapdata.DIR_SOUTH:
                image_id = imageids.OW_IMAGE_ID_FACE_SOUTH
                logger.debug("Facing SOUTH")
            elif direction == mapdata.DIR_WEST:
                image_id = imageids.OW_IMAGE_ID_FACE_WEST
                logger.debug("Facing WEST")

            if image_id is not None:
                # change direction variable and blit
                self.facing_direction = direction
                self.blit_onto_surface(
                    surface,
                    image_id,
                    bottom_left_pixel=bottom_left_pixel,
                    top_left_pixel=top_left_pixel,
                )
                self.curr_image_id = image_id

    @classmethod
    def calculate_max_health(cls, hitpoint_level):
        max_health = 0

        if hitpoint_level and hitpoint_level > 0:
            max_health = hitpoint_level * 10

        return max_health

# extend Entity class
class Character(Entity):
    # maps character-related object IDs to character objects
    character_listing = {}

    def __init__(
                    self,
                    id,
                    name_info,
                    image_path_dict,
                    collision_width=1,
                    collision_height=1,
                    skill_levels={},
                    equipment_dict={},
                    gender=GENDER_NEUTRAL,
                    race=RACE_HUMAN,
                    examine_info=None,
                    interaction_id=interactiondata.DEFAULT_ID,
                ):

        # a Character is an Entity type of interactive object
        Entity.__init__(
            self,
            id,
            name_info,
            image_path_dict,
            collision_width=collision_width,
            collision_height=collision_height,
            skill_levels=skill_levels,
            equipment_dict=equipment_dict,
            gender=gender,
            race=race,
            examine_info=examine_info,
            interaction_id=interaction_id,
        )

        # TODO Fill in rest

    # given object id, returns character if it pertains to object ID
    # do not use this to build protagonist
    @classmethod
    def character_factory(cls, object_id):
        ret_character = None

        # reject if object ID is for protagonist
        if (object_id == objdata.PROTAGONIST_ID):
            logger.warn("Cannot use character_factory to build protagonist.")
        else:
            # check if we already have this object
            char_from_listing = Character.character_listing.get(
                        object_id,
                        None
                    )

            if char_from_listing:
                ret_character = char_from_listing
            else:
                # we need to make character ourselves
                # TODO
                pass

                # check if object id pertains to a character

        return ret_character

class Protagonist(Character):
    def __init__(
                    self,
                    id,
                    name_info,
                    image_path_dict,
                    skill_levels={},
                    equipment_dict={},
                    gender=GENDER_NEUTRAL,
                    race=RACE_HUMAN,
                ):

        Character.__init__(
            self,
            id,
            name_info,
            image_path_dict,
            collision_width=1, # protagonist is always 1x1 tile
            collision_height=1,
            skill_levels=skill_levels,
            equipment_dict=equipment_dict,
            gender=gender,
            race=race,
        )
        self.quest_journal = {}

        # TODO make max_size constant. Add items here?
        self.tool_inventory = inventory.Inventory.inventory_factory(max_size=10)

        # Maps currency IDs to the number of units of currency.
        # DEPRECATED?
        #self.money_pouch = {}

        # TODO FILL IN REST

    # DEPRECATED?
    """
    def init_money_pouch(self):
        self.money_pouch = {}

        for currency_id in currency.CURRENCY_VALUE_MAPPING:
            self.money_pouch[currency_id] = 0

        # Set default gold value.
        self.money_pouch[currency.CURRENCY_GOLD_COIN] = START_NUM_GOLD_COINS
    """

    @classmethod
    def protagonist_factory(
                cls,
                name
            ):
        protagonist = None

        # TODO check if we already have protagonist?

        # Build fields.
        protag_id = objdata.PROTAGONIST_ID
        protag_name_info = {
            language.LANG_ENGLISH: name,
            language.LANG_ESPANOL: name,
        }
        protag_image_path_dict = objdata.IMAGE_PATH_DICT_PROTAG
        protag_skill_levels = {
            skills.SKILL_ID_HITPOINTS: 1,
            skills.SKILL_ID_WOODCUTTING: 9, # TESTING.
        }

        protagonist = Protagonist(
            protag_id,
            protag_name_info,
            protag_image_path_dict,
            skill_levels=protag_skill_levels,
            gender=GENDER_MALE,
            race=RACE_HUMAN,
        )

        logger.debug("Protagonist ID: {0}".format(protagonist.object_id))
        logger.debug(
            "Protagonist obj type: {0}".format(protagonist.object_type)
        )
        logger.debug("Protagonist name: {0}".format(protagonist.name_info))
        logger.debug("Protagonist gender: {0}".format(protagonist.gender))
        logger.debug("Protagonist race: {0}".format(protagonist.race))

        # Set initial money.
        protagonist.add_item_to_inventory_by_id(
            itemdata.CURRENCY_GOLD_COIN_ID,
            quantity=START_NUM_GOLD_COINS,
        )

        # Set tool inventory. TESTING
        protagonist.add_item_to_tool_inventory_by_id(
            itemdata.CURRENCY_SILVER_COIN_ID,
            quantity=5618274,
        )

        # TODO rest of setup

        # Add protagonist to object listing
        interactiveobj.Interactive_Object.add_interactive_obj_to_listing(
            objdata.PROTAGONIST_ID,
            protagonist
        )

        return protagonist

# set up logger
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
