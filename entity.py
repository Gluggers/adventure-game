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
            image_path_dict                             \
            #tile_position                               \
        )

        self.gender = gender
        self.race = race
        self.tile_position = tile_position

        # by default, face south
        self.facing_direction = map.DIR_SOUTH

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

    # reblit the entity to face the specified direction.
    # DOES NOT update surface - caller will have to do that
    def face_direction(self, surface, direction, pixel_location_tuple):
        image_id = None

        if self and surface and pixel_location_tuple:
            if direction == map.DIR_NORTH:
                image_id = interactive_obj.OW_IMAGE_ID_FACE_NORTH
            elif direction == map.DIR_EAST:
                image_id = interactive_obj.OW_IMAGE_ID_FACE_EAST
            elif direction == map.DIR_SOUTH:
                image_id = interactive_obj.OW_IMAGE_ID_FACE_SOUTH
            elif direction == map.DIR_WEST:
                image_id = interactive_obj.OW_IMAGE_ID_FACE_WEST

            if image_id is not None:
                # change direction variable and blit
                self.facing_direction = direction
                self.blit_onto_surface(surface, image_id, pixel_location_tuple)

    # reblit the entity to face the specified direction.
    # DOES NOT update surface - caller will have to do that
    def face_direction_bottom_left(self, surface, direction, bottom_left_pixel_location):
        image_id = None

        if self and surface and bottom_left_pixel_location:
            if direction == map.DIR_NORTH:
                image_id = interactive_obj.OW_IMAGE_ID_FACE_NORTH
            elif direction == map.DIR_EAST:
                image_id = interactive_obj.OW_IMAGE_ID_FACE_EAST
            elif direction == map.DIR_SOUTH:
                image_id = interactive_obj.OW_IMAGE_ID_FACE_SOUTH
            elif direction == map.DIR_WEST:
                image_id = interactive_obj.OW_IMAGE_ID_FACE_WEST

            if image_id is not None:
                # change direction variable and blit
                self.facing_direction = direction
                self.blit_onto_surface_bottom_left(surface, image_id, bottom_left_pixel_location)

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

        self.quest_journal = {}
        self.inventory = []

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
