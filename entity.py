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

### CONSTANTS ###
GENDER_NEUTRAL = 0x0
GENDER_MALE = 0x1
GENDER_FEMALE = 0x2

RACE_DEFAULT = 0x0
RACE_HUMAN = 0x1

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
    # equipment_dict maps the equipment slot ID to the corresponding item ID
    # that the Entity is wielding.
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
        self.curr_image_id = objdata.OW_IMAGE_ID_FACE_SOUTH

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
            remaining_exp = skills.get_experience_to_next_level(skill_level, exp)

            logger.debug(
                "Setting skill level {0}, exp {1}. exp to next level {2}".format(
                    skill_level,
                    exp,
                    remaining_exp
                )
            )

            # Record skill information.
            self.skill_info_mapping[skill_id] = [skill_level, exp, remaining_exp]

        # Set up health - use hitpoint stat if possible, otherwise default hitpoints value.
        self.max_health = self.skill_info_mapping.get(
            skills.SKILL_ID_HITPOINTS, [skills.DEFAULT_LEVEL_HITPOINTS]
        )[0]

        self.curr_health = self.max_health

        # set up equipment
        self.equipment_dict = {}
        for equipment_slot_id, item_id in equipment_dict.items():
            self.equipment_dict[equipment_slot_id] = item_id

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

    # reblit the entity to face the specified direction.
    # Can specify either top_left_pixel or
    # bottom_left_pixel as the reference point for blitting the image.
    # bottom_left_pixel is recommended for images that are larger than
    # a single Tile image. If both top_left_pixel and bottom_left_pixel are
    # specified, the method will use bottom_left_pixel as an override.
    # top_left_pixel and bottom_left_pixel are tuples of pixel coordinates.
    # DOES NOT update surface - caller will have to do that
    def face_direction(self, surface, direction, bottom_left_pixel=None, top_left_pixel=None):
        image_id = None

        if self and surface and (bottom_left_pixel or top_left_pixel):
            if direction == mapdata.DIR_NORTH:
                image_id = objdata.OW_IMAGE_ID_FACE_NORTH
                logger.debug("Facing NORTH")
            elif direction == mapdata.DIR_EAST:
                image_id = objdata.OW_IMAGE_ID_FACE_EAST
                logger.debug("Facing EAST")
            elif direction == mapdata.DIR_SOUTH:
                image_id = objdata.OW_IMAGE_ID_FACE_SOUTH
                logger.debug("Facing SOUTH")
            elif direction == mapdata.DIR_WEST:
                image_id = objdata.OW_IMAGE_ID_FACE_WEST
                logger.debug("Facing WEST")

            if image_id is not None:
                # change direction variable and blit
                self.facing_direction = direction
                self.blit_onto_surface(                     \
                    surface,                                \
                    image_id,                               \
                    bottom_left_pixel=bottom_left_pixel,    \
                    top_left_pixel=top_left_pixel           \
                )
                self.curr_image_id = image_id

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
            char_from_listing = Character.character_listing.get(object_id, None)

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

        # Maps Item IDs to the number of items held.
        self.inventory = {}

        # TODO FILL IN REST

    # Returns True if inventory is full, false otherwise.
    def inventory_full(self):
        return False

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
            skills.SKILL_ID_HITPOINTS: 10,
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
        logger.debug("Protagonist obj type: {0}".format(protagonist.object_type))
        logger.debug("Protagonist name: {0}".format(protagonist.name_info))
        logger.debug("Protagonist gender: {0}".format(protagonist.gender))
        logger.debug("Protagonist race: {0}".format(protagonist.race))

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
