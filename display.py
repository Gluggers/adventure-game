import pygame
import viewingdata
import skills
import language
import timekeeper
import logging
import sys
import imagepaths
import math

### FONTS AND TEXT ###
DEFAULT_FONT = None
#TOP_DISPLAY_TEXT = None

FONT_SIZE_DEFAULT = 24
FONT_SIZE_TOP_DISPLAY = 24
FONT_SIZE_BOTTOM_TEXT = 16
FONT_SIZE_SIDE_MENU_TEXT = 16

FONT_TYPE_DEFAULT = 'Comic Sans MS'
FONT_TYPE_TOP_DISPLAY = 'Comic Sans MS'

# For best results, use mono-spaced font
FONT_PATH_DEFAULT = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
FONT_PATH_TOP_DISPLAY = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
FONT_PATH_BOTTOM_TEXT_DISPLAY = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
FONT_PATH_SIDE_MENU_DISPLAY = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"

FONT_COLOR_DEFAULT = viewingdata.COLOR_BLACK
FONT_COLOR_TOP_DISPLAY = viewingdata.COLOR_BLACK
FONT_COLOR_BOTTOM_TEXT_DISPLAY = viewingdata.COLOR_BLACK

# For best results, use mono-spaced font
FONT_PATH_DEFAULT = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
FONT_PATH_TOP_DISPLAY = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
# "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"

SIZE_TEST_STRING = "abcdefghijklmnopqrstuvwxyz" \
                    + "1234567890" \
                    + "ABCDEFGHIJKLMNOPQRSTUVWXYZ" \
                    + ":;[]{},./?<>-_=+~\`!@#$%^&*()\\|\"'"

# Space between text and the continue icon.
CONTINUE_ICON_HORIZ_SPACE = 10

# Space between text and the selected option icon.
SELECTION_ICON_HORIZ_SPACE = 8

# Spacing factors for space between lines.
DEFAULT_LINE_SPACING_FACTOR = 1.25
MENU_LINE_SPACING_FACTOR = 1.5

# Number of milliseconds to wait in between each
# text display.
BOTTOM_TEXT_DELAY_MS = 500
DEFAULT_ADVANCE_DELAY_MS = 1500

# Number of milliseconds to wait when loading menu.
DEFAULT_MENU_LOAD_DELAY_MS = 750

# Number of milliseconds to wait after changing selected options.
DEFAULT_MENU_OPTION_SWITCH_DELAY_MS = 750


### ORIENTATIONS FOR MENU OPTIONS ###
ORIENTATION_CENTERED = 0x1
ORIENTATION_LEFT_JUSTIFIED = 0x2

MORE_OPTIONS_MENU_INFO = {
    language.LANG_ENGLISH: "More Options",
    language.LANG_ESPANOL: "Mas Opciones",
}

LEVEL_TEXT_PREFIX_INFO = {
    language.LANG_ENGLISH: "LEVEL: ",
    language.LANG_ESPANOL: "NIVEL: ",
}
HEALTH_TEXT_PREFIX_INFO = {
    language.LANG_ENGLISH: "HEALTH: ",
    language.LANG_ESPANOL: "SALUD: ",
}

### PADDING ###
TOP_DISPLAY_SIDE_PADDING = 16
TEXT_DISPLAY_SIDE_PADDING = 16
TEXT_DISPLAY_VERTICAL_PADDING = 16

OW_SIDE_MENU_SIDE_PADDING = 32
OW_SIDE_MENU_VERTICAL_PADDING = 16

TEXT_ADVANCE_KEYS = set([
    pygame.K_SPACE,
    pygame.K_RETURN,
    pygame.K_BACKSPACE,
    pygame.K_TAB,
    pygame.K_ESCAPE,
    pygame.K_e,
    pygame.K_RIGHT,
])

MENU_OPTION_SELECT_KEYS = set([
    pygame.K_SPACE,
    pygame.K_RETURN,
    pygame.K_RIGHT,
    pygame.K_TAB,
])

MENU_OPTION_EXIT_KEYS = set([
    pygame.K_BACKSPACE,
    pygame.K_ESCAPE,
])

class Text_Page():
    def __init__(self, line_list):
        self.text_lines = []

        if line_list:
            for item in line_list:
                self.text_lines.append(item)

class Menu_Page():
    def __init__(self, option_list):
        self.option_list = []

        if option_list:
            for item in option_list:
                self.option_list.append(item)

    def get_num_options(self):
        return len(self.option_list)

    def get_option(self, index):
        return self.option_list[index]

class Display():
    default_font = None
    top_display_font = None
    bottom_text_display_font = None
    side_menu_display_font = None

    # Background color is color to use in case of no background image.
    # If background image is provided, we will use that rather than
    # background color. For best results, background image should be same
    # size as display_rect dimensions.
    def __init__(
                self,
                main_display_surface,
                display_rect,
                font_object,
                background_image_path=None,
                background_color=viewingdata.COLOR_WHITE,
                font_color=FONT_COLOR_DEFAULT,
                display_language=language.DEFAULT_LANGUAGE,
            ):
        self.main_display_surface = main_display_surface
        self.display_rect = display_rect
        self.top_left_pixel_position = (self.display_rect[0], self.display_rect[1])
        self.font_object = font_object
        self.font_color = font_color,
        self.pixel_width = self.display_rect[2]
        self.pixel_height = self.display_rect[3]
        self.background_color = background_color
        self.display_language = display_language

        self.background_image = None

        if background_image_path:
            # Load image if path is provided.
            self.background_image = pygame.image.load(
                                        background_image_path
                                    ).convert_alpha()

    # Does not update display, caller must do that.
    def blit_background(self, surface):
        if surface:
            # Blit the background image/default fill color.
            if self.background_image:
                surface.blit(
                    self.background_image,
                    self.display_rect,
                    area=self.display_rect
                )
            else:
                pygame.draw.rect(
                    surface,
                    self.background_color,
                    self.display_rect
                )

    @classmethod
    def init_fonts(cls):
        Display.default_font = pygame.font.Font(
            FONT_PATH_DEFAULT,
            FONT_SIZE_DEFAULT
        )
        Display.top_display_font = pygame.font.Font(
            FONT_PATH_TOP_DISPLAY,
            FONT_SIZE_TOP_DISPLAY
        )
        Display.bottom_text_display_font = pygame.font.Font(
            FONT_PATH_BOTTOM_TEXT_DISPLAY,
            FONT_SIZE_BOTTOM_TEXT
        )
        Display.side_menu_display_font = pygame.font.Font(
            FONT_PATH_SIDE_MENU_DISPLAY,
            FONT_SIZE_SIDE_MENU_TEXT
        )
        """
        Display.default_font = pygame.font.SysFont(
            FONT_TYPE_DEFAULT,
            FONT_SIZE_DEFAULT
        )
        Display.top_display_font = pygame.font.SysFont(
            FONT_TYPE_TOP_DISPLAY,
            FONT_SIZE_TOP_DISPLAY
        )
        """

class Top_Display(Display):
    def __init__(
                self,
                main_display_surface,
                display_rect,
                font_object,
                background_image_path=None,
                background_color=viewingdata.COLOR_WHITE,
                font_color=FONT_COLOR_DEFAULT,
                protagonist=None,
                curr_map=None,
                display_language=language.DEFAULT_LANGUAGE,
            ):
        Display.__init__(
            self,
            main_display_surface,
            display_rect,
            font_object,
            background_image_path=background_image_path,
            background_color=background_color,
            font_color=font_color,
            display_language=display_language,
        )

        self._protagonist = protagonist
        self.curr_map = curr_map

        # Set up text
        self.level_text_str = LEVEL_TEXT_PREFIX_INFO.get(self.display_language, None)
        self.health_text_str = HEALTH_TEXT_PREFIX_INFO.get(self.display_language, None)

        self.level_text = None
        self.health_text = None

        if self.level_text_str:
            self.level_text = Display.top_display_font.render(
                self.level_text_str,
                False,
                self.font_color
            )

        if self.health_text_str:
            self.health_text = Display.top_display_font.render(
                self.health_text_str,
                False,
                self.font_color
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
            viewingdata.TOP_DISPLAY_LOCATION[1]                             \
                + self.pixel_height                                         \
                - vertical_offset                                           \
                - text_height                                               \
        )

        self.health_text_top_left_pixel = (                                 \
            viewingdata.TOP_DISPLAY_LOCATION[0]                             \
                + int(viewingdata.TOP_DISPLAY_WIDTH / 3),                   \
            viewingdata.TOP_DISPLAY_LOCATION[1]                             \
                + self.pixel_height                                         \
                - vertical_offset                                           \
                - text_height                                               \
        )

        # TODO - call this after initialization?
        # Update the text.
        self.update_self()

    # Updates the display text and text positioning
    # with the current protagonist information.
    def update_self(self):
        if self._protagonist:
            # Get protagonist level.
            protag_level = skills.calculate_combat_level(self._protagonist.skill_info_mapping)
            self.level_text_str = LEVEL_TEXT_PREFIX_INFO.get(           \
                                    self.display_language,              \
                                    ""                                  \
                                )                                       \
                                + str(protag_level)

            # Get protagonist health.
            self.health_text_str = ''.join([
                    HEALTH_TEXT_PREFIX_INFO.get(self.display_language, ""),
                    str(self._protagonist.curr_health),
                    ' / ',
                    str(self._protagonist.max_health)
                ])

            # Render the texts.
            if Display.top_display_font:
                self.level_text = Display.top_display_font.render(
                    self.level_text_str,
                    False,
                    self.font_color
                )
                self.health_text = Display.top_display_font.render(
                    self.health_text_str,
                    False,
                    self.font_color
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
            # Blit the background image/default fill color.
            self.blit_background(surface)

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

class Text_Display(Display):
    # If no background image is specified, default to background_color.
    # For best results, ensure that background_image_path points to an image
    # of size equal to the display_rect dimension values.
    # continue_icon_image_path points to the image path for an icon
    # to blit after the last line of a page if needed. The icon should be
    # small.
    def __init__(
                self,
                main_display_surface,
                display_rect,
                font_object,
                display_language=language.DEFAULT_LANGUAGE,
                background_image_path=None,
                background_color=viewingdata.COLOR_WHITE,
                font_color=FONT_COLOR_DEFAULT,
                side_padding=TEXT_DISPLAY_SIDE_PADDING,
                vertical_padding=TEXT_DISPLAY_VERTICAL_PADDING,
                continue_icon_image_path=None,
                spacing_factor_between_lines=DEFAULT_LINE_SPACING_FACTOR,
            ):
        Display.__init__(
            self,
            main_display_surface,
            display_rect,
            font_object,
            display_language=display_language,
            background_image_path=background_image_path,
            background_color=background_color,
            font_color=font_color,
        )

        self.side_padding = side_padding
        self.vertical_padding = vertical_padding
        self.spacing_factor_between_lines = spacing_factor_between_lines

        # Define where text will start.
        self.text_top_left_pixel = (
            self.top_left_pixel_position[0] + self.side_padding,
            self.top_left_pixel_position[1] + self.vertical_padding
        )

        # Define text space limits.
        self.text_space_horizontal = self.pixel_width - (2 * self.side_padding)
        self.text_space_vertical = self.pixel_height - (2 * self.vertical_padding)

        self.text_space_rect = (
            self.text_top_left_pixel[0],
            self.text_top_left_pixel[1],
            self.text_space_horizontal,
            self.text_space_vertical
        )

        self.text_center_x = self.text_space_rect[0] + int(self.text_space_rect[2] / 2)

        self.text_height = self.font_object.get_linesize()

        # Get max number of characters that we can blit per line.
        # Assuming monospaced font.
        self.char_per_line = Text_Display.get_char_per_line(
            self.text_space_horizontal,
            self.font_object
        )

        # Get max number of lines that we can blit per page.
        # Assuming monospaced font.
        self.lines_per_page = Text_Display.get_num_lines_per_page(
            self.text_space_vertical,
            self.font_object,
            self.spacing_factor_between_lines
        )

        logger.debug("Char per line {0}, line per page {1}".format(self.char_per_line, self.lines_per_page))

        # Define background image if possible.
        self.background_image = None
        if background_image_path:
            # Load image if path is provided.
            self.background_image = pygame.image.load(
                                        background_image_path
                                    ).convert_alpha()

        # Define continuation icon if possible.
        self.continue_icon = None
        if continue_icon_image_path:
            # Load image if path is provided.
            self.continue_icon = pygame.image.load(
                    continue_icon_image_path
                ).convert_alpha()

    @classmethod
    def get_char_per_line(cls, horizontal_pixels, font_object):
        num_char = 0

        if horizontal_pixels and (horizontal_pixels > 0) and font_object:
            avg_char_width = 0

            ####for char in SIZE_TEST_STRING:
            str_size_info = font_object.size(SIZE_TEST_STRING)

            if str_size_info:
                avg_char_width = int(
                    max(
                        avg_char_width,
                        math.ceil(
                            str_size_info[0] / (1.0 * len(SIZE_TEST_STRING))
                        )
                    )
                )

            if avg_char_width > 0:
                # Allow for some extra space?
                num_char = int(horizontal_pixels / avg_char_width)

        return num_char

    # Includes spaces in between the lines, as well.
    # spacing_factor_between_lines is a float that determines
    # spacing in between lines (e.g. 1.25 means add 0.25 of the text height
    # as spacing in between lines)
    @classmethod
    def get_num_lines_per_page(
                cls,
                vertical_pixel_height,
                font_object,
                spacing_factor_between_lines=DEFAULT_LINE_SPACING_FACTOR):
        num_lines = 0

        if vertical_pixel_height and (vertical_pixel_height > 0) and font_object:
            text_height = font_object.get_linesize()

            num_total_lines = int(vertical_pixel_height / text_height)

            if (num_total_lines % 2) == 0:
                # Even number of total lines. Divide by line space factor
                # to account for space in between the lines.
                num_lines = int(num_total_lines / spacing_factor_between_lines)
            else:
                # Odd number of total lines. We don't need space after
                # the final line.
                num_lines = int(num_total_lines / spacing_factor_between_lines) + 1

        return num_lines

    @classmethod
    def convert_to_word_list(cls, text_string):
        ret_list = []

        if text_string:
            # Split string based on whitespace.
            word_list = text_string.split()

            if word_list:
                # Add a space to every word except the last one.
                for i in range(len(word_list) - 1):
                    ret_list.append(word_list[i] + " ")
                ret_list.append(word_list[len(word_list) - 1])

        logger.debug("Converted {0} to word list {1}".format(text_string, ret_list))

        return ret_list

    # Given a text string to display, returns a list of strings,
    # where each string takes up one line of display space.
    def get_text_lines(self, text_string):
        # List of strings
        ret_lines = []

        # Convert string to list of words to print.
        if text_string:
            word_list = Text_Display.convert_to_word_list(text_string)

            text_lines = []

            curr_length = 0
            start_index = 0

            num_words = len(word_list)

            logger.debug("Max char in line: {0}".format(self.char_per_line))

            for index in range(num_words):
                sub_list = None
                str_to_add = None

                word_length = len(word_list[index])

                logger.debug("Word length for {0} is {1}".format(word_list[index], word_length))

                # Check if we can add this word or not.
                if (curr_length + word_length) > self.char_per_line:
                    # Adding this word would bring us over the limit.
                    # Collect all the words from the last end point up
                    # to the word before.
                    if start_index < index:
                        sub_list = word_list[start_index:index]
                    else:
                        sub_list = [word_list[index]]

                    start_index = index

                    # Reset counter, and throw in the length of the
                    # overflow word.
                    curr_length = word_length
                else:
                    if (index == (num_words - 1)):
                        # We reached the end of the word list and
                        # did not overpass to the next line.
                        sub_list = word_list[start_index:]
                    else:
                        curr_length = curr_length + word_length

                # Create line.
                if sub_list:
                    str_to_add = ''.join(sub_list)

                    if str_to_add:
                        text_lines.append(str_to_add)
                        logger.debug("Adding string {0} to text lines".format(str_to_add))

            if start_index == (num_words - 1):
                # We still need to add the last word.
                str_to_add = word_list[start_index]
                text_lines.append(str_to_add)
                logger.debug("Adding string {0} to text lines".format(str_to_add))

            if text_lines:
                ret_lines = text_lines
            else:
                # Entire string fits on one line.
                ret_lines = [''.join(word_list)]

        logger.debug("Converted text \n{0}\nto lines\n{1}\n".format(text_string, ret_lines))

        return ret_lines

    @classmethod
    def get_text_lines_test(cls, text_string):
        # List of strings
        ret_lines = []

        # Convert string to list of words to print.
        if text_string:
            word_list = Text_Display.convert_to_word_list(text_string)

            text_lines = []

            curr_length = 0
            start_index = 0

            num_words = len(word_list)

            for index in range(num_words):
                sub_list = None
                str_to_add = None

                word_length = len(word_list[index])

                logger.debug("Word length for {0} is {1}".format(word_list[index], word_length))

                # Check if we can add this word or not.
                if (curr_length + word_length) > 52:
                    # Adding this word would bring us over the limit.
                    # Collect all the words from the last end point up
                    # to the word before.
                    if start_index < index:
                        sub_list = word_list[start_index:index]
                    else:
                        sub_list = [word_list[index]]

                    start_index = index

                    # Reset length counter.
                    curr_length = 0
                else:
                    if (index == (num_words - 1)):
                        # We reached the end of the word list and
                        # did not overpass to the next line.
                        if start_index < index:
                            sub_list = word_list[start_index:]
                        else:
                            sub_list = [word_list[index]]

                        logger.debug("Adding single word to list: {0}".format(sub_list))
                    else:
                        curr_length = curr_length + word_length

                # Create line.
                if sub_list:
                    str_to_add = ''.join(sub_list)

                    if str_to_add:
                        text_lines.append(str_to_add)
                        logger.debug("Adding string {0} to text lines".format(str_to_add))

            if start_index == (num_words - 1):
                # We still need to add the last word.
                str_to_add = word_list[start_index]
                text_lines.append(str_to_add)
                logger.debug("Adding string {0} to text lines".format(str_to_add))

            if text_lines:
                ret_lines = text_lines
            else:
                # Entire string fits on one line.
                ret_lines = [''.join(word_list)]

        logger.debug("Converted text \n{0}\nto lines\n{1}\n".format(text_string, ret_lines))

        return ret_lines

    # Returns list of Text_Page objects, each containing
    # a list of strings, where each string represents one line of text
    # to place on display.
    def get_text_pages(self, text_string):
        ret_page_list = []
        page_list = []

        # Get lines of text to print.
        lines_to_print = self.get_text_lines(text_string)

        if lines_to_print:
            num_lines = len(lines_to_print)

            if num_lines > self.lines_per_page:
                num_lines_processed = 0
                remaining_lines = num_lines

                while remaining_lines > 0:
                    # Get number of lines to add to page.
                    lines_to_add = min(self.lines_per_page, remaining_lines)

                    # Get indices for list slicing.
                    start_index = num_lines_processed
                    end_index = start_index + lines_to_add

                    # Create page and add to page list.
                    page_list.append(Text_Page(lines_to_print[start_index:end_index]))

                    num_lines_processed = num_lines_processed + lines_to_add
                    remaining_lines = remaining_lines - lines_to_add
            else:
                # All lines can fit on a single page.
                page_list.append(Text_Page(lines_to_print))

        if page_list:
            ret_page_list = page_list

        # Debugging
        for page in ret_page_list:
            logger.debug("Made page: {0}".format('\n#\n'.join(page.text_lines)))

        return ret_page_list

    # Blit text for the single page.
    # Does not update display, caller will need to do that.
    # If continue_icon is set to True, we will blit the object's continue
    # icon after the last line of the page.
    def blit_page(
                self,
                surface,
                text_page,
                show_continue_icon=False,
            ):
        if surface and text_page:
            # Blit background
            self.blit_background(surface)

            vertical_offset = 0

            logger.debug("Page has {0} line(s)".format(len(text_page.text_lines)))

            #for text_line in text_page.text_lines:
            num_lines = len(text_page.text_lines)
            for index in range(num_lines):
                text_line = text_page.text_lines[index]

                rendered_text = self.font_object.render(
                    text_line,
                    False,
                    self.font_color,
                )

                rendered_text_dimensions = rendered_text.get_size()
                text_width = rendered_text_dimensions[0]

                # Center the text horizontally.
                text_top_left = (
                    self.text_center_x - int(text_width / 2),
                    self.text_top_left_pixel[1] + vertical_offset
                )

                # Blit the text.
                surface.blit(
                    rendered_text,
                    text_top_left
                )

                # Blit the continue icon if we are on the last line.
                if (index == (num_lines - 1)) \
                        and self.continue_icon \
                        and show_continue_icon:
                    text_height = rendered_text_dimensions[1]
                    icon_top_left = (
                        text_top_left[0] \
                            + text_width \
                            + CONTINUE_ICON_HORIZ_SPACE,
                        text_top_left[1] \
                            + text_height \
                            - self.continue_icon.get_height()
                    )

                    surface.blit(
                        self.continue_icon,
                        icon_top_left
                    )

                # Move to spot for next line.
                vertical_offset = vertical_offset \
                        + int(self.spacing_factor_between_lines * self.text_height)

    # advance_delay_ms is time in milliseconds to pause before allowing
    # manual advance.
    # if auto_advance is True, the method will wait for advance_delay_ms
    # milliseconds before returning execution to caller.
    # If False, the method will wait for the same amount of time before
    # waiting for the user to continue.
    def display_single_page(
                self,
                surface,
                page,
                advance_delay_ms=DEFAULT_ADVANCE_DELAY_MS,
                auto_advance=False,
            ):
        if surface and page:
            self.blit_page(
                surface,
                page,
            )

            pygame.display.update()

            # Pause if needed.
            if advance_delay_ms:
                pygame.time.wait(advance_delay_ms)

            if not auto_advance:
                # Reblit page but with continue icon if available.
                self.blit_page(
                    surface,
                    page,
                    show_continue_icon=True
                )

                pygame.display.update()

                # Clear event queue to prevent premature advancement.
                pygame.event.clear()

                # Wait for user to advance.
                advance = False

                logger.debug("Waiting to advance...")

                while not advance:
                    timekeeper.Timekeeper.tick()

                    for events in pygame.event.get():
                        if events.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit(0)
                        elif events.type == pygame.KEYDOWN:
                            if events.key in TEXT_ADVANCE_KEYS:
                                logger.debug("Advancing to next page")
                                advance = True

    def display_text(
                self,
                surface,
                text_to_display,
                advance_delay_ms=DEFAULT_ADVANCE_DELAY_MS,
                auto_advance=False,
            ):
        if surface and text_to_display:
            # Get the pages.
            page_list = self.get_text_pages(text_to_display)

            logger.debug("Blitting {0} page(s)".format(len(page_list)))

            if page_list:
                # Display each text page.
                for page in page_list:
                    self.display_single_page(
                        surface,
                        page,
                        advance_delay_ms=advance_delay_ms,
                        auto_advance=auto_advance,
                    )

            # pygame.event.clear()

    def display_first_text_page(
                self,
                surface,
                text_to_display,
                advance_delay_ms=DEFAULT_ADVANCE_DELAY_MS,
                auto_advance=False,
            ):
        if surface and text_to_display:
            # Get the pages.
            page_list = self.get_text_pages(text_to_display)
            num_pages = len(page_list)

            logger.debug("Blitting {0} page(s)".format(num_pages))

            if num_pages > 1:
                logger.warn("Display_first_text_page only blits first page.")
                logger.warn("Submitted text is {0} pages.".format(num_pages))

            if page_list:
                # Display just the first page.
                self.display_single_page(
                    surface,
                    page_list[0],
                    advance_delay_ms=advance_delay_ms,
                    auto_advance=auto_advance,
                )

class Menu_Display(Text_Display):
    # If no background image is specified, default to background_color.
    # For best results, ensure that background_image_path points to an image
    # of size equal to the display_rect dimension values.
    # For best results, ensure that selection_icon_image_path points to an
    # image of small enough size.
    def __init__(
                self,
                main_display_surface,
                display_rect,
                font_object,
                display_language=language.DEFAULT_LANGUAGE,
                background_image_path=None,
                background_color=viewingdata.COLOR_WHITE,
                font_color=FONT_COLOR_DEFAULT,
                side_padding=OW_SIDE_MENU_SIDE_PADDING,
                vertical_padding=OW_SIDE_MENU_VERTICAL_PADDING,
                selection_icon_image_path=imagepaths.DEFAULT_MENU_SELECTION_ICON_PATH,
                spacing_factor_between_lines=MENU_LINE_SPACING_FACTOR,
            ):
        Text_Display.__init__(
            self,
            main_display_surface,
            display_rect,
            font_object,
            display_language=display_language,
            background_image_path=background_image_path,
            background_color=background_color,
            font_color=font_color,
            side_padding=side_padding,
            vertical_padding=vertical_padding,
            spacing_factor_between_lines=spacing_factor_between_lines,
        )

        # Define selection icon.
        self.selection_icon = None
        if selection_icon_image_path:
            # Load image if path is provided.
            self.selection_icon = pygame.image.load(
                    selection_icon_image_path
                ).convert_alpha()

        if not self.selection_icon:
            logger.error("Error setting up selection icon for menu.")

        # determine max number of options (one option per line)
        # that can be blitted per page.
        self.max_options_per_page = Text_Display.get_num_lines_per_page(
                self.text_space_vertical,
                self.font_object,
                self.spacing_factor_between_lines
            )

        logger.info("Max options per menu page: {0}".format(self.max_options_per_page))

    # Returns list of Menu Pages containing the menu option names.
    # If the returned list contains multiple Menu Pages, then each
    # Menu Page (including the final one) will have its last
    # option name be the "MORE OPTIONS" option to indicate that there
    # are additional menu options. The "MORE OPTIONS" option on the final
    # page will lead to the first page to allow looping.
    # option_list is a list of strings representing the options
    # for the menu. They cannot be equal to the "MORE OPTIONS" option name.
    # more_options_str indicates the string to display if we need to display
    # additional options on a subsequent menu page.
    # max_options_per_page indicates how many options (lines) fit on one page.
    @classmethod
    def get_menu_page_list(
                cls,
                option_list,
                more_options_str,
                max_options_per_page
            ):
        ret_pages = []

        if option_list and max_options_per_page and more_options_str:
            logger.debug("Adding {0} options to page with max of {1} options per page".format(
                len(option_list),
                max_options_per_page
            ))

            done = False
            remaining_options = option_list

            while not done:
                options_to_add = []

                if len(remaining_options) <= max_options_per_page:
                    # We can add all remaining options to this page.
                    options_to_add = remaining_options
                    logger.debug("Adding remaining {0} pages to menu page: {1}".format(
                        len(options_to_add),
                        options_to_add
                    ))
                    done = True
                else:
                    # Options will carry on to next page.
                    options_to_add = remaining_options[0:max_options_per_page - 1]
                    options_to_add.append(more_options_str)
                    logger.debug("Adding {0} options plus \"more options\" to menu page: {1}".format(
                        len(options_to_add) - 1,
                        options_to_add
                    ))
                    remaining_options = remaining_options[max_options_per_page - 1:]
                    logger.debug("Remaining options: {0}".format(
                        remaining_options
                    ))

                if options_to_add:
                    curr_page = Menu_Page(options_to_add)
                    ret_pages.append(curr_page)

        return ret_pages

    # Does not update display.
    def blit_menu_page(
                self,
                surface,
                menu_page,
                curr_selected_index,
                orientation=ORIENTATION_LEFT_JUSTIFIED,
            ):
        if surface and menu_page and (orientation is not None):
            num_options = menu_page.get_num_options()

            if num_options <= self.max_options_per_page:
                # Blit background.
                self.blit_background(surface)

                vertical_offset = 0

                for index in range(num_options):
                    curr_option = menu_page.get_option(index)

                    # Get rendered text and dimensions.
                    rendered_text = self.font_object.render(
                        curr_option,
                        False,
                        self.font_color,
                    )

                    rendered_text_dimensions = rendered_text.get_size()
                    text_width = rendered_text_dimensions[0]
                    text_height = rendered_text_dimensions[1]

                    text_top_left = None

                    if orientation == ORIENTATION_CENTERED:
                        # Get top left for centered option text.
                        # Center the text horizontally.
                        text_top_left = (
                            self.text_center_x - int(text_width / 2),
                            self.text_top_left_pixel[1] + vertical_offset
                        )
                    elif orientation == ORIENTATION_LEFT_JUSTIFIED:
                        # Left justify the text.
                        text_top_left = (
                            self.text_top_left_pixel[0],
                            self.text_top_left_pixel[1] + vertical_offset
                        )

                    if text_top_left:
                        # Blit the text.
                        surface.blit(
                            rendered_text,
                            text_top_left
                        )

                        # Blit the selection icon if we are on the selected index.
                        if index == curr_selected_index and self.selection_icon:
                            # Vertically center the selection icon with the option.
                            icon_top_left = (
                                text_top_left[0] \
                                    - self.selection_icon.get_width()
                                    - SELECTION_ICON_HORIZ_SPACE,
                                text_top_left[1] \
                                    + int(text_height / 2) \
                                    - int(self.selection_icon.get_height() / 2)
                            )

                            surface.blit(
                                self.selection_icon,
                                icon_top_left
                            )

                    # Advance.
                    vertical_offset = vertical_offset \
                        + int(self.spacing_factor_between_lines * text_height)

    # Orientation can be centered or left justified (default).
    # Returns option that was selected (None if menu was exited without
    # selecting option).
    def display_self(
                self,
                surface,
                option_list,
                more_options_str,
                orientation=ORIENTATION_LEFT_JUSTIFIED,
                load_delay_ms=DEFAULT_MENU_LOAD_DELAY_MS,
                option_switch_delay_ms=DEFAULT_MENU_OPTION_SWITCH_DELAY_MS,
            ):
        ret_option = None

        if surface and option_list and more_options_str and (orientation is not None):
            # Get list of menu pages.
            menu_pages = Menu_Display.get_menu_page_list(
                    option_list,
                    more_options_str,
                    self.max_options_per_page,
                )

            if menu_pages:
                 # Start at top of menu.
                curr_selected_index = 0

                # Blit first menu page.
                curr_page_index = 0

                num_pages = len(menu_pages)

                done = False
                while not done:
                    curr_page = menu_pages[curr_page_index]
                    num_options = len(curr_page.option_list)

                    # Blit the current menu page.
                    self.blit_menu_page(
                        surface,
                        curr_page,
                        curr_selected_index,
                        orientation=orientation,
                    )

                    pygame.display.update()

                    # Wait a bit before allowing user to select options.
                    if load_delay_ms:
                        pygame.time.wait(load_delay_ms)

                    # Clear event queue to prevent premature advancement.
                    #pygame.event.clear() # TODO remove?

                    logger.info("Waiting for user to select a menu option...")
                    selected = False
                    while not selected:
                        timekeeper.Timekeeper.tick()
                        changed_options = False
                        curr_option = curr_page.get_option(curr_selected_index)

                        for events in pygame.event.get():
                            if events.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit(0)
                            elif events.type == pygame.KEYDOWN:
                                if events.key == pygame.K_DOWN:
                                    curr_selected_index = (curr_selected_index + 1) % num_options
                                    logger.info("Advancing to next option {0}".format(
                                        curr_option
                                    ))
                                    changed_options = True

                                    pygame.display.update()
                                elif events.key == pygame.K_UP:
                                    curr_selected_index = (curr_selected_index - 1) % num_options
                                    logger.info("Advancing to previous option {0}".format(
                                        curr_option
                                    ))
                                    changed_options = True
                                elif events.key in MENU_OPTION_EXIT_KEYS:
                                    # Exit without selecting option.
                                    selected = True
                                    done = True
                                    ret_option = None
                                    logger.info("Leaving menu without selecting option.")
                                elif events.key in MENU_OPTION_SELECT_KEYS:
                                    # We selected the current option.
                                    selected = True
                                    logger.info("Selecting option {0}".format(
                                        curr_option
                                    ))

                                    if curr_option == more_options_str:
                                        # Go to next page and don't return.
                                        curr_page_index = (curr_page_index + 1) % num_pages
                                        curr_selected_index = 0
                                        logger.info("Moving to next menu page.")
                                    else:
                                        # Selected a valid option.
                                        done = True
                                        ret_option = curr_option
                                        logger.info("Selected option {0}".format(
                                            ret_option
                                        ))

                        if changed_options:
                            # Reblit menu page with new selected option.
                            self.blit_menu_page(
                                surface,
                                curr_page,
                                curr_selected_index,
                                orientation=orientation,
                            )

                            pygame.display.update()

                            # Delay before allowing user to go to next option.
                            if option_switch_delay_ms:
                                pygame.time.wait(option_switch_delay_ms)

                            # Clear event queue to prevent premature advancement.
                            #pygame.event.clear() # TODO remove?

        logger.info("returning option {0}".format(ret_option))
        return ret_option

    # TODO - set up display method
    # display_curr_options(option list, selected_option_index)
    #   make sure len(option list) <= max options per page
    # display menu(option list)
    #   if num options <= max options per page, we good
    #   else, show max num options - 1 and then make last option
    #   "MORE"
    #   if more is selected, go to next page, etc

# set up logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
