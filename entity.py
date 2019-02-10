import pygame
import tiledata
import map
import mapdata
import skills
import interactiveobj
import objdata
import logging

### CONSTANTS ###
GENDER_NEUTRAL = 0x0
GENDER_MALE = 0x1
GENDER_FEMALE = 0x2

RACE_DEFAULT = 0x0
RACE_HUMAN = 0x1

# skils_dict maps the skill ID to the corresponding levels
# for the entity (ID -> [level, xp]). Not passing one in sets default values
# equipment_dict maps the equipment slot ID to the corresponding item ID
# that the Entity is wielding
# TODO - set up item class and have it map IDs to item objects (build_item method)
class Entity(interactiveobj.Interactive_Object):
    def __init__(
                    self,
                    id,
                    name,
                    image_path_dict,
                    collision_width=1,
                    collision_height=1,
                    skills_dict={},
                    equipment_dict={},
                    gender=GENDER_NEUTRAL,
                    race=RACE_HUMAN,
                    examine_info=None,
                ):
        interactiveobj.Interactive_Object.__init__(
            self,
            objdata.TYPE_CHARACTER,
            name,
            id,
            image_path_dict,
            collision_width=collision_width,
            collision_height=collision_height,
            examine_info=examine_info,
        )

        self.gender = gender
        self.race = race

        # by default, face south
        self.facing_direction = mapdata.DIR_SOUTH

        # set up skills
        self.skills_dict = {}
        for skill_id in skills.SKILL_ID_LIST:
            skill_level = skills_dict.get(skill_id, None)
            if skill_level:
                exp = skills.get_experience_from_level(skill_level)
                logger.debug("Setting skill level {0}, exp {1}".format(skill_level, exp))
                self.skills_dict[skill_id] = [skill_level, exp]
            else:
                # default values
                self.skills_dict[skill_id] = [skills.DEFAULT_LEVEL, skills.DEFAULT_EXP]

        # Set up health - use hitpoint stat if possible, otherwise default hitpoints value.
        self.max_health = self.skills_dict.get(skills.SKILL_ID_HITPOINTS, [skills.DEFAULT_HITPOINTS])[0]
        self.curr_health = self.max_health

        # set up equipment
        self.equipment_dict = {}
        for equipment_slot_id, item_id in equipment_dict.items():
            self.equipment_dict[equipment_slot_id] = item_id

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

# extend Entity class
class Character(Entity):
    # maps character-related object IDs to character objects
    character_listing = {}

    def __init__(
                    self,
                    id,
                    name,
                    image_path_dict,
                    collision_width=1,
                    collision_height=1,
                    skills_dict={},
                    equipment_dict={},
                    gender=GENDER_NEUTRAL,
                    race=RACE_HUMAN,
                    examine_info=None
                ):

        # a Character is an Entity type of interactive object
        Entity.__init__(
            self,
            id,
            name,
            image_path_dict,
            collision_width=collision_width,
            collision_height=collision_height,
            skills_dict=skills_dict,
            equipment_dict=equipment_dict,
            gender=gender,
            race=race,
            examine_info=examine_info,
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

# image_path contains the default sprite image for the character
# images_path_dict must map character image scenarios to the
# file path containing the appropriate sprite image.
# must contain the following keys:
# OW_IMAGE_ID_DEFAULT
# OW_IMAGE_ID_FACE_NORTH
# OW_IMAGE_ID_FACE_EAST
# OW_IMAGE_ID_FACE_SOUTH
# OW_IMAGE_ID_FACE_WEST
# OW_IMAGE_ID_WALK_NORTH
# OW_IMAGE_ID_WALK_EAST
# OW_IMAGE_ID_WALK_SOUTH
# OW_IMAGE_ID_WALK_WEST
# BATTLE_IMAGE_ID_DEFAULT
# BATTLE_IMAGE_ID_STAND
# BATTLE_IMAGE_ID_ATTACK
# BATTLE_IMAGE_ID_FAINTED
class Protagonist(Character):
    def __init__(
                    self,
                    id,
                    name,
                    image_path_dict,
                    skills_dict={},
                    equipment_dict={},
                    gender=GENDER_NEUTRAL,
                    race=RACE_HUMAN,
                ):

        Character.__init__(
            self,
            id,
            name,
            image_path_dict,
            collision_width=1, # protagonist is always 1x1 tile
            collision_height=1,
            skills_dict=skills_dict,
            equipment_dict=equipment_dict,
            gender=gender,
            race=race,
        )
        self.quest_journal = {}
        self.inventory = []

        # TODO FILL IN REST


# set up logger
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
