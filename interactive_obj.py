import pygame

INTERACTIVE_OBJ_LISTING = {} # maps interactive object IDs to objects

### INTERACTIVE OBJECT TYPE ID CONSTANTS ###
TYPE_ENTITY = 0x0
TYPE_OBSTACLE = 0x1
TYPE_RESOURCE = 0x2
TYPE_ITEM = 0x3



class Interactive_Object(pygame.sprite.Sprite):
    def __init__(self, object_type, image_path):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        self.obj_type = object_type
        self.image = pygame.image.load(image_path).convert()

    # blits the interactive object sprite image onto surface at the
    # designated pixel coordinate position.
    # Does not update the surface display - caller will have to do that.
    def blit_onto_surface(self, surface, pixel_location_tuple):
        if self and surface:
            surface.blit(self.image, pixel_location_tuple)
