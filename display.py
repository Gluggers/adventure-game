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
FONT_SIZE_BOTTOM_TEXT_DISPLAY = 16

FONT_TYPE_DEFAULT = 'Comic Sans MS'
FONT_TYPE_TOP_DISPLAY = 'Comic Sans MS'

# For best results, use mono-spaced font
FONT_PATH_DEFAULT = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
FONT_PATH_TOP_DISPLAY = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
FONT_PATH_BOTTOM_TEXT_DISPLAY = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"

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

CONTINUE_ICON_HORIZ_SPACE = 10
LINE_SPACING_FACTOR = 1.25

# Number of milliseconds to wait in between each
# text display.
BOTTOM_TEXT_DELAY_MS = 500
DEFAULT_ADVANCE_DELAY_MS = 1500

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

TEXT_ADVANCE_KEYS = set([
    pygame.K_SPACE,
    pygame.K_RETURN,
    pygame.K_BACKSPACE,
    pygame.K_TAB,
    pygame.K_ESCAPE,
    pygame.K_e,
    pygame.K_RIGHT,
])

class Text_Page():
    def __init__(self, line_list):
        self.text_lines = []

        if line_list:
            self.text_lines = line_list

class Display():
    default_font = None
    top_display_font = None
    bottom_text_display_font = None

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
                display_language=language.DEFAULT_LANGUAGE,
            ):
        self.main_display_surface = main_display_surface
        self.display_rect = display_rect
        self.top_left_pixel_position = (self.display_rect[0], self.display_rect[1])
        self.font_object = font_object
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
            FONT_SIZE_BOTTOM_TEXT_DISPLAY
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
            display_language=display_language
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
                FONT_COLOR_TOP_DISPLAY
            )

        if self.health_text_str:
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
                side_padding=TEXT_DISPLAY_SIDE_PADDING,
                vertical_padding=TEXT_DISPLAY_VERTICAL_PADDING,
                continue_icon_image_path=None,
            ):
        Display.__init__(
            self,
            main_display_surface,
            display_rect,
            font_object,
            display_language=display_language,
            background_image_path=background_image_path,
            background_color=background_color,
        )

        self.side_padding = side_padding
        self.vertical_padding = vertical_padding

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
        self.lines_per_page = Text_Display.get_line_per_page(
            self.text_space_vertical,
            self.font_object
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

    # Includes spaces in between the lines, as well
    @classmethod
    def get_line_per_page(cls, vertical_pixel_height, font_object):
        num_lines = 0

        if vertical_pixel_height and (vertical_pixel_height > 0) and font_object:
            text_height = font_object.get_linesize()

            num_total_lines = int(vertical_pixel_height / text_height)

            if (num_total_lines % 2) == 0:
                # Even number of total lines. Divide by line space factor
                # to account for space in between the lines.
                num_lines = int(num_total_lines / LINE_SPACING_FACTOR)
            else:
                # Odd number of total lines. We don't need space after
                # the final line.
                num_lines = int(num_total_lines / LINE_SPACING_FACTOR) + 1

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
                continue_icon=False,
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
                    FONT_COLOR_BOTTOM_TEXT_DISPLAY
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
                        and continue_icon:
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
                        + int(LINE_SPACING_FACTOR * self.text_height)

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
                    continue_icon=True
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

# set up logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
