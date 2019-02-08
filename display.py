import pygame
import viewingdata
import skills

### FONTS AND TEXT ###
DEFAULT_FONT = None
TOP_DISPLAY_TEXT = None
FONT_SIZE_DEFAULT = 16
FONT_SIZE_TOP_DISPLAY = 16
FONT_TYPE_DEFAULT = 'Comic Sans MS'
FONT_TYPE_TOP_DISPLAY = 'Comic Sans MS'
FONT_COLOR_DEFAULT = viewingdata.COLOR_BLACK
FONT_COLOR_TOP_DISPLAY = viewingdata.COLOR_BLACK

LEVEL_TEXT_PREFIX = "LEVEL: "
HEALTH_TEXT_PREFIX = "HEALTH: "

### PADDING ###
TOP_DISPLAY_SIDE_PADDING = 16

class Display():
    default_font = None
    top_display_font = None

    def __init__(
                self,
                main_display_surface,
                top_left_pixel_position,
                font_object,
                pixel_width,
                pixel_height,
                background_color=viewingdata.COLOR_WHITE,
            ):
        self.main_display_surface = main_display_surface
        self.top_left_pixel_position = top_left_pixel_position
        self.font_object = font_object
        self.pixel_width = pixel_width
        self.pixel_height = pixel_height
        self.background_color = background_color
        self.display_rect = (
            top_left_pixel_position[0],
            top_left_pixel_position[1],
            pixel_width,
            pixel_height
        )

    @classmethod
    def init_fonts(cls):
        Display.default_font = pygame.font.SysFont(
            FONT_TYPE_DEFAULT,
            FONT_SIZE_DEFAULT
        )
        Display.top_display_font = pygame.font.SysFont(
            FONT_TYPE_TOP_DISPLAY,
            FONT_SIZE_TOP_DISPLAY
        )

class Top_Display(Display):
    def __init__(
                self,
                main_display_surface,
                top_left_pixel_position,
                font_object,
                pixel_width=viewingdata.TOP_DISPLAY_WIDTH,
                pixel_height=viewingdata.TOP_DISPLAY_HEIGHT,
                background_color=viewingdata.COLOR_WHITE,
                protagonist=None,
                curr_map=None,
            ):
        Display.__init__(
            self,
            main_display_surface,
            top_left_pixel_position,
            font_object,
            pixel_width,
            pixel_height,
            background_color=background_color,
        )

        self._protagonist = protagonist
        self.curr_map = curr_map

        # Set up text
        self.level_text_str = LEVEL_TEXT_PREFIX
        self.health_text_str = HEALTH_TEXT_PREFIX

        self.level_text = Display.top_display_font.render(
            self.level_text_str,
            False,
            FONT_COLOR_TOP_DISPLAY
        )

        self.health_text = Display.top_display_font.render(
            self.health_text_str,
            False,
            FONT_COLOR_TOP_DISPLAY
        )

        # Get top left positions for rendering each text.
        text_height = max(
            self.health_text.get_height(),
            self.level_text.get_height()
        )
        vertical_offset = int(
            (viewingdata.TOP_DISPLAY_HEIGHT - text_height) / 2
        )

        self.level_text_top_left_pixel = (                                  \
            viewingdata.TOP_DISPLAY_LOCATION[0] + TOP_DISPLAY_SIDE_PADDING, \
            viewingdata.TOP_DISPLAY_LOCATION[1] + vertical_offset           \
        )

        self.health_text_top_left_pixel = (                                 \
            viewingdata.TOP_DISPLAY_LOCATION[0]                             \
                + int(viewingdata.TOP_DISPLAY_WIDTH / 4),                   \
            viewingdata.TOP_DISPLAY_LOCATION[1] + vertical_offset           \
        )

        # TODO - call this after initialization?
        # Update the text.
        self.update_self()

    # Updates the display text and text positioning
    # with the current protagonist information.
    def update_self(self):
        if self._protagonist:
            # Get protagonist level.
            protag_level = skills.calculate_combat_level(self._protagonist.skills_dict)
            self.level_text_str = LEVEL_TEXT_PREFIX + str(protag_level)

            # Get protagonist health.
            self.health_text_str = ''.join([
                    HEALTH_TEXT_PREFIX,
                    str(self._protagonist.curr_health),
                    ' / ',
                    str(self._protagonist.max_health)
                ])

            # Render the texts.
            if Display.top_display_font:
                self.level_text = Display.top_display_font.render(
                    self.level_text_str,
                    False,
                    FONT_COLOR_TOP_DISPLAY
                )
                self.health_text = Display.top_display_font.render(
                    self.health_text_str,
                    False,
                    FONT_COLOR_TOP_DISPLAY
                )

    @property
    def protagonist(self):
        """Return protagonist."""
        return self._protagonist

    @protagonist.setter
    def protagonist(self, value):
        """Assign protagonist to Top Display."""
        if value:
            self._protagonist = value

            # Update top display
            self.update_self()

    # Blits the top display onto the given surface.
    # Uses self's top left pixel
    def blit_onto_surface(self, surface):
        if surface:
            # Blit the background.
            pygame.draw.rect(
                surface,
                self.background_color,
                self.display_rect
            )

            # Blit the level text.
            if self.level_text and self.level_text_top_left_pixel:
                surface.blit(
                    self.level_text,
                    self.level_text_top_left_pixel
                )

            # Blit the healthl text.
            if self.health_text and self.health_text_top_left_pixel:
                surface.blit(
                    self.health_text,
                    self.health_text_top_left_pixel
                )
