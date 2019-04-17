import sys
import pygame
import tiledata
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
import directions

### CONSTANTS ###
GENDER_NEUTRAL = 0x0
GENDER_MALE = 0x1
GENDER_FEMALE = 0x2

RACE_DEFAULT = 0x0
RACE_HUMAN = 0x1

START_NUM_GOLD_COINS = 100

DEFAULT_MAX_HEALTH = 10

MAX_RUN_ENERGY = 100.0

# Health recovery rate in health points per minute.
DEFAULT_HEALTH_REGEN_PER_MIN = 2

# Run energy recovery rate in points per minute.
DEFAULT_RUN_REGEN_PER_MIN = 30

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
            skill_levels=None,
            equipment_dict=None,
            gender=GENDER_NEUTRAL,
            race=RACE_HUMAN,
            examine_info=None,
            interaction_id=interactiondata.DEFAULT_ID,
            manual_hitpoints=None,
        ):
        """Initializes the Entity object.

        Args:
            id: object ID number for the Entity. Must be unique
                among interactive objects?
            name_info: dict that maps language IDs to Strings for
                the Entity name translation.
            image_path_dict: dict that maps image IDs to the file paths
                for the image file.
            collision_width: width, in Tiles, of the collision box for the
                Entity.
            collision_height: height, in Tiles, of the collision box for the
                Entity.
            skill_levels: dict that maps the skill ID to the corresponding
                level for the entity. The method automatically calculates the
                experience required for the level and set it accordingly for
                the entity. Excluding the skill_levels dict or excluding
                individual skill IDs will set default levels for all
                applicable skills.
            equipment_dict: dict that maps equipment slot ID to a 2-tuple
                of form (item_ID, quantity)
            gender: gender ID for the Entity.
            race: race ID for the Entity.
            examine_info: dict that maps language IDs to Strings containing
                the corresponding examine info translation.
            interaction_id: interaction ID that determines what interaction
                method to use when interacting with the Entity.
            manual_hitpoints: manually sets the hitpoints for the Entity,
                regardless of the Entity's hitpoints skill level. If None,
                uses the default hitpoints formula based on the hitpoints
                skill level.
        """

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

        # Determines walk/run.
        self.run_on = False

        # Determines how much longer the entity can run.
        self.run_energy = MAX_RUN_ENERGY

        # By default, face south.
        self.facing_direction = directions.DIR_SOUTH
        self.curr_image_id = imageids.IMAGE_ID_FACE_SOUTH

        # Set up skills. self.skill_info_mapping maps skill IDs to
        # a length-3 list
        # [skill level, current experience, experience to next level]
        self.skill_info_mapping = {}

        if skill_levels:
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

                LOGGER.debug(
                    "Setting skill level %d, exp %d. exp to next level %d",
                    skill_level,
                    exp,
                    remaining_exp
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
        # to length-3 list of [item_id, item object, quantity].
        self.equipment_dict = {}
        if equipment_dict:
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

    # TODO - increment run energy.

    def decrement_run_energy(self, distance=1,):
        """Reduce run energy based on distance ran and the entity's
        weight and agility level.

        Args:
            distance: number of tiles moved, not counting map
                switches, teleports, or connector tiles.
        """

        # TODO change calculation based on weight.
        if distance:
            self.run_energy = max(
                0.0,
                self.run_energy - (2 * distance)
            )

    def inventory_full(self):
        """Returns True if inventory is full, False otherwise."""

        return self.inventory.is_full()

    def clear_all_items(self):
        """Removes all items from entity."""

        self.inventory.clear_items()
        self.tool_inventory.clear_items()
        self.equipment_dict = {}

    def add_item_to_inventory(self, item_id, quantity=1):
        """Adds the corresponding number of items to the inventory and
        returns True upon success, False upon failure.

        Args:
            item_id: ID number for the Item to add.
            quantity: amount of item_id to add.

        Returns:
            True upon successful addition to the inventory, False otherwise.
        """

        return self.inventory.add_item(item_id, quantity=quantity)

    def add_item_to_toolbelt(self, item_id, quantity=1):
        """Adds the corresponding number of items to the toolbelt and
        returns True upon success, False upon failure.

        Args:
            item_id: ID number for the tool Item to add.
            quantity: amount of item_id to add.

        Returns:
            True upon successful addition to the toolbelt, False otherwise.
        """

        return self.tool_inventory.add_item(item_id, quantity=quantity)

    def add_item_to_equipment(self, equipment_slot_id, item_id, quantity=1):
        """Adds item to equipment dict for entity.

        Does not remove item from inventory or check if item
        exists in inventory.
        """

        if item_id is not None and quantity:
            # Get item object.
            item_obj = items.Item.get_item(item_id)

            if item_obj:
                self.equipment_dict[equipment_slot_id] = [
                    item_id,
                    item_obj,
                    quantity,
                ]

    def equip_item(self, equipment_slot_id, item_id):
        """Equipts the given item and places it into the equipment slot."""

        # TODO.
        pass


    def has_item_equipped(self, item_id):
        """Returns True if entity has the corresponding item equipped, False
        otherwise."""

        has_equipped = False

        for equipment_slot_id, equipped_item_info in self.equipment_dict.items():
            if equipped_item_info[0] == item_id:
                has_equipped = True

        return has_equipped

    def has_tool(self, item_id):
        """Returns True if entity has the corresponding tool in its toolbelt,
        False otherwise."""

        return self.tool_inventory.has_item(item_id)

    def has_item(self, item_id):
        """Returns True if entity has the corresponding item, False otherwise.

        The item can be in the inventory, toolbelt, or equipment.
        """

        return self.inventory.has_item(item_id) \
            or self.has_item_equipped(item_id) \
            or self.has_tool(item_id)

    def get_skill_level(self, skill_id):
        """Returns the entity's skill level for the given skill ID."""

        ret_level = None

        if skill_id is not None:
            skill_info = self.skill_info_mapping.get(skill_id, None)

            if skill_info:
                ret_level = skill_info[0]

        return ret_level

    def get_skill_experience(self, skill_id):
        """Returns the entity's experience for the given skill ID."""

        ret_exp = None

        if skill_id is not None:
            skill_info = self.skill_info_mapping.get(skill_id, None)

            if skill_info:
                ret_exp = skill_info[1]

        return ret_exp

    def get_experience_to_next_level(self, skill_id):
        """Returns the entity's remaining experience for the next skill level
        for the given skill ID."""

        ret_exp = None

        if skill_id is not None:
            skill_info = self.skill_info_mapping.get(skill_id, None)

            if skill_info:
                ret_exp = skill_info[2]

        return ret_exp

    # Returns the number of levels gained when adding exp to skill_id.
    def gain_experience(self, skill_id, exp):
        """Adds experience to the entity for the given skill and returns the
        number of levels gained in that skill."""

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
                    LOGGER.error("Error in exp gain.")
                else:
                    LOGGER.info(
                        "Started at level %d with %d exp (%d remaining to next level.)",
                        old_level,
                        old_exp,
                        skill_info[2]
                    )
                    LOGGER.info(
                        "Now reached level %d with %d exp (%d remaining to next level.)",
                        new_level,
                        new_exp,
                        new_exp_to_next_level,
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
        if self and surface and (bottom_left_pixel or top_left_pixel):
            image_id = imageids.get_direction_image_id(direction)

            if image_id is not None:
                # change direction variable and blit
                self.facing_direction = direction
                self.blit_onto_surface(
                    surface,
                    bottom_left_pixel=bottom_left_pixel,
                    top_left_pixel=top_left_pixel,
                )
                self.curr_image_id = image_id

    @classmethod
    def calculate_max_health(cls, hitpoint_level):
        """Returns the maximum amount of health based on hitpoint level.

        Follows the formula max_health = hitpoint_level * 10.
        """

        max_health = 0

        if hitpoint_level and hitpoint_level > 0:
            max_health = hitpoint_level * 10.0

        return max_health

class Character(Entity):
    # Maps character-related object IDs to Character objects.
    character_listing = {}

    def __init__(
            self,
            id,
            name_info,
            image_path_dict,
            collision_width=1,
            collision_height=1,
            skill_levels=None,
            equipment_dict=None,
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
            LOGGER.warn("Cannot use character_factory to build protagonist.")
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
            skill_levels=None,
            equipment_dict=None,
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

        # Time in MS of last refresh.
        self.last_refresh_time_ms = pygame.time.get_ticks()

        # TODO make max_size constant. Add items here?
        self.tool_inventory = inventory.Inventory.inventory_factory(max_size=10)

    def refresh_self(self):
        """Refreshes self, including attributes like run energy and health."""

        # Get elapsed time since last refresh.
        curr_time_ms = pygame.time.get_ticks()

        elapsed_ms = curr_time_ms - self.last_refresh_time_ms

        self.last_refresh_time_ms = curr_time_ms

        if elapsed_ms < 0:
            logger.error("Error in elapsed time %d", elapsed_ms)
            sys.exit(4)

        elapsed_min = elapsed_ms / 60000

        # Regenerate some health and run energy.
        if self.curr_health < self.max_health:
            self.curr_health = min(
                self.max_health,
                self.curr_health + (elapsed_min * DEFAULT_HEALTH_REGEN_PER_MIN)
            )

        if self.run_energy < MAX_RUN_ENERGY:
            self.run_energy = min(
                MAX_RUN_ENERGY,
                self.run_energy + (elapsed_min * DEFAULT_RUN_REGEN_PER_MIN)
            )

        LOGGER.debug(
            "Protag run energy %d, health %d",
            self.run_energy,
            self.curr_health,
        )

    @classmethod
    def protagonist_factory(cls, name):
        """Creates protagonist with given name and gives default attributes.

        The returned protagonist will have the all of its stats at level 1
        by default and will have the following starting items:
            Inventory:
                - 100 gold coins
            Equipment: None
            Toolbelt:
                - Hammer
                - Knife
                - Tinderbox
                - Needle
        """

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
            skills.SKILL_ID_WOODCUTTING: 40, # TESTING.
            skills.SKILL_ID_MINING: 40, # TESTING.
            skills.SKILL_ID_FISHING: 60, # TESTING.
        }

        protagonist = Protagonist(
            protag_id,
            protag_name_info,
            protag_image_path_dict,
            skill_levels=protag_skill_levels,
            gender=GENDER_MALE,
            race=RACE_HUMAN,
        )

        LOGGER.debug("Protagonist ID: %d", protagonist.object_id)
        LOGGER.debug(
            "Protagonist obj type: %s",
            protagonist.object_type
        )
        LOGGER.debug("Protagonist name info: %s", protagonist.name_info)
        LOGGER.debug("Protagonist gender: %s", protagonist.gender)
        LOGGER.debug("Protagonist race: %s", protagonist.race)

        # Set initial money.
        protagonist.add_item_to_inventory(
            itemdata.CURRENCY_GOLD_COIN_ID,
            quantity=START_NUM_GOLD_COINS,
        )

        # Set tool belt.
        protagonist.add_item_to_toolbelt(
            itemdata.HAMMER_NORMAL_ID,
            quantity=1,
        )
        protagonist.add_item_to_toolbelt(
            itemdata.KNIFE_ID,
        )
        protagonist.add_item_to_toolbelt(
            itemdata.NEEDLE_ID,
        )
        protagonist.add_item_to_toolbelt(
            itemdata.TINDERBOX_ID,
        )

        # TODO rest of setup

        # Add protagonist to object listing
        interactiveobj.Interactive_Object.add_interactive_obj_to_listing(
            objdata.PROTAGONIST_ID,
            protagonist
        )

        return protagonist

# Set up logger.
logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)
