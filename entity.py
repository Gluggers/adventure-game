import pygame
import interactive_obj
import adventure
import map
import skills

### CONSTANTS ###
GENDER_NEUTRAL = 0x0
GENDER_MALE = 0x1
GENDER_FEMALE = 0x2

RACE_DEFAULT = 0x0
RACE_HUMAN = 0x1

# skils_dict maps the skill ID to the corresponding levels
# for the entity. Not passing one in sets default values
# equipment_dict maps the equipment slot ID to the corresponding item ID
# that the Entity is wielding
# TODO - set up item class and have it map IDs to item objects (build_item method)
class Entity(interactive_obj.Interactive_Object):
    def __init__(                           \
                    self,                   \
                    id,                     \
                    name,                   \
                    image_path_dict,        \
                    tile_position=(0,0),    \
                    skills_dict={},         \
                    equipment_dict={},      \
                    gender=GENDER_NEUTRAL,  \
                    race=RACE_HUMAN         \
                ):
        interactive_obj.Interactive_Object.__init__(    \
            self,                                       \
            interactive_obj.TYPE_ENTITY,                \
            name,                                       \
            id,                                         \
            image_path_dict,                            \
            #tile_position                               \
        )

        self.gender = gender
        self.race = race
        self.tile_position = tile_position

        # set up skills
        self.skills_dict = {}
        for skill_id in skills.SKILL_ID_LIST:
            skill_level = skills_dict.get(skill_id, None)
            if skill_level:
                exp = skills.get_experience_from_level(skill_level)
                self.skills_dict[skill_id] = [skill_value, exp]
            else:
                # default values
                self.skills_dict[skill_id] = [skills.DEFAULT_LEVEL, skills.DEFAULT_EXP]

        # set up equipment
        self.equipment_dict = {}
        for equipment_slot_id, item_id in equipment_dict.items():
            self.equipment_dict[equipment_slot_id] = item_id

# extend Entity class
class Character(Entity):
    def __init__(                           \
                    self,                   \
                    id,                     \
                    name,                   \
                    image_path_dict,        \
                    tile_position=(0,0),    \
                    skills_dict={},         \
                    equipment_dict={},      \
                    gender=GENDER_NEUTRAL,  \
                    race=RACE_HUMAN         \
                ):

        # a Character is an Entity type of interactive object
        Entity.__init__(        \
            self,               \
            id,                 \
            name,               \
            image_path_dict,    \
            tile_position,      \
            skills_dict,        \
            equipment_dict,     \
            gender,             \
            race                \
        )

        # TODO Fill in rest

        """
        def blit_onto_surface(self, surface, pixel_location_tuple):
            if self and surface:
                surface.blit(self.curr_image, pixel_location_tuple)
        """

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
    def __init__(                           \
                    self,                   \
                    id,                     \
                    name,                   \
                    image_path_dict,        \
                    tile_position=(0,0),    \
                    skills_dict={},         \
                    equipment_dict={},      \
                    gender=GENDER_NEUTRAL,  \
                    race=RACE_HUMAN         \
                ):

        Character.__init__(         \
            self,                   \
            id,                     \
            name,                   \
            image_path_dict,        \
            tile_position,          \
            skills_dict,            \
            equipment_dict,         \
            gender,                 \
            race                    \
        )

        # TODO FILL IN REST

def build_characters():
    # TODO - build monsters and NPCs
    """
    protag_image_dict = {
        OW_STAND_NORTH_ID:images.HERB_BASIC_PATH,
        OW_STAND_EAST_ID:images.HERB_BASIC_PATH,
        OW_STAND_SOUTH_ID:images.HERB_BASIC_PATH,
        OW_STAND_WEST_ID:images.HERB_BASIC_PATH,
        OW_WALK_NORTH_ID:images.HERB_BASIC_PATH,
        OW_WALK_EAST_ID:images.HERB_BASIC_PATH,
        OW_WALK_SOUTH_ID:images.HERB_BASIC_PATH,
        OW_WALK_WEST_ID:images.HERB_BASIC_PATH,
        BATTLE_STAND_ID:images.HERB_BASIC_PATH,
        BATTLE_ATTACK_ID:images.HERB_BASIC_PATH
    }
    """

    pass
