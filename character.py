import pygame
import interactiveobj
import adventure

### CONSTANTS ###
GENDER_NEUTRAL = 0x0
GENDER_MALE = 0x1
GENDER_FEMALE = 0x2

RACE_DEFAULT = 0x0
RACE_HUMAN = 0x1

class Character(interactiveobj.Interactive_Object):
    def __init__(self, image_path, id, name, \
                gender=GENDER_NEUTRAL, race=RACE_HUMAN):
        interactiveobj.Interactive_Object.__init__(self)
        # TODO Fill in rest
        self.map_position = (0,0) # default

class Protagonist(Character):
    def __init__(self, game, image_path, id, name, \
                gender=GENDER_NEUTRAL, race=RACE_HUMAN):
        Character.__init__(self, image_path, id, name, \
                    gender=GENDER_NEUTRAL, race=RACE_HUMAN)

        # TODO FILL IN REST

        # protagonist pixel location MUST be as close to center tile
        # as possible
        self.pixel_location =
