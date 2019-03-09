import pygame
import viewingdata
import skills
import language
import timekeeper
import logging
import sys
import imagepaths
import menuoptions
import math
import fontinfo
import itemdata

SIZE_TEST_STRING = "abcdefghijklmnopqrstuvwxyz" \
                    + "1234567890" \
                    + "ABCDEFGHIJKLMNOPQRSTUVWXYZ" \
                    + ":;[]{},./?<>-_=+~\`!@#$%^&*()\\|\"'"

# Space between text and the continue icon.
CONTINUE_ICON_HORIZ_SPACE = 6

# Space between text and the selected option icon.
SELECTION_ICON_HORIZ_SPACE = 8

# Spacing factors for space between lines.
DEFAULT_LINE_SPACING_FACTOR = 1.1
TEXT_BOX_LINE_SPACING_FACTOR = 1.1
MENU_LINE_SPACING_FACTOR = 1.5

# Number of pixels in between each item slot.
ITEM_VIEWING_PIXEL_SPACING = 10

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
ORIENTATION_RIGHT_JUSTIFIED = 0x3
ORIENTATION_TOP_JUSTIFIED = 0x4
ORIENTATION_BOTTOM_JUSTIFIED = 0x5


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
TOP_DISPLAY_HORIZONTAL_PADDING = 20
TEXT_DISPLAY_HORIZONTAL_PADDING = 28
TEXT_DISPLAY_VERTICAL_PADDING = 24

OW_SIDE_MENU_HORIZONTAL_PADDING = 40
OW_SIDE_MENU_VERTICAL_PADDING = 20

ITEM_LISTING_HORIZONTAL_PADDING = 20
ITEM_LISTING_VERTICAL_PADDING = 50

class Text_Page():
    def __init__(self, line_list):
        self.text_lines = []

        if line_list:
            for item in line_list:
                self.text_lines.append(item)

class Menu_Page():
    def __init__(self, option_id_list):
        self.option_id_list = []

        if option_id_list:
            for item in option_id_list:
                self.option_id_list.append(item)

    def get_num_options(self):
        return len(self.option_id_list)

    def get_option_id(self, index):
        return self.option_id_list[index]

class Display():
    # Will contain loaded fonts.
    font_listing = {}

    # Background color is color to use in case of no background image.
    # If background image is provided, we will use that rather than
    # background color. For best results, background image should be same
    # size as display_rect dimensions.
    def __init__(
                self,
                main_display_surface,
                display_rect,
                background_image_path=None,
                background_color=viewingdata.COLOR_WHITE,
            ):
        self.main_display_surface = main_display_surface
        self.display_rect = display_rect
        self.background_color = background_color

        self.background_image = None

        if background_image_path:
            # Load image if path is provided.
            self.background_image = pygame.image.load(
                                        background_image_path
                                    ).convert_alpha()

            logger.info("Image size: {0}".format(self.background_image.get_size()))


    # Does not update display, caller must do that.
    def blit_background(self, surface, alternative_top_left=None):
        if surface:
            target_rect = self.display_rect

            if alternative_top_left:
                target_rect = pygame.Rect(
                    alternative_top_left,
                    (self.display_rect.width, self.display_rect.height)
                )

            # Blit the background image/default fill color.
            # TODO - add in blitting the borders?
            if self.background_image:
                # TODO - tile repetition?
                surface.blit(
                    self.background_image,
                    target_rect,
                )
            elif self.background_color:
                pygame.draw.rect(
                    surface,
                    self.background_color,
                    target_rect,
                )

    @classmethod
    def add_font_to_listing(cls, font_id, font_obj):
        if font_obj and (font_id is not None):
            cls.font_listing[font_id] = font_obj

    @classmethod
    def get_font(cls, font_id):
        return cls.font_listing.get(font_id, None)

    @classmethod
    def init_fonts(cls):
        for font_id, font_info in fontinfo.FONT_INFO.items():
            font_obj = pygame.font.Font(
                font_info.get(
                    fontinfo.FONT_PATH_FIELD,
                    fontinfo.FONT_PATH_DEFAULT,
                ),
                font_info.get(
                    fontinfo.FONT_SIZE_FIELD,
                    fontinfo.FONT_SIZE_DEFAULT
                )
            )

            if font_obj:
                cls.add_font_to_listing(font_id, font_obj)

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
                background_image_path=None,
                background_color=viewingdata.COLOR_WHITE,
                font_color=fontinfo.FONT_COLOR_DEFAULT,
                horizontal_padding=TEXT_DISPLAY_HORIZONTAL_PADDING,
                vertical_padding=TEXT_DISPLAY_VERTICAL_PADDING,
                continue_icon_image_path=None,
                spacing_factor_between_lines=DEFAULT_LINE_SPACING_FACTOR,
            ):
        Display.__init__(
            self,
            main_display_surface,
            display_rect,
            background_image_path=background_image_path,
            background_color=background_color,
        )

        self.font_object = font_object
        self.font_color = font_color
        self.horizontal_padding = horizontal_padding
        self.vertical_padding = vertical_padding
        self.spacing_factor_between_lines = spacing_factor_between_lines

        # Define text space limits.
        self.text_space_horizontal = self.display_rect.width \
                                    - (2 * self.horizontal_padding)
        self.text_space_vertical = self.display_rect.height \
                                    - (2 * self.vertical_padding)
        self.text_space_top_left = (
            self.display_rect.x + self.horizontal_padding,
            self.display_rect.y + self.vertical_padding
        )

        logger.info("Text Space {0} x {1}. Top left: {2}".format(
            self.text_space_horizontal,
            self.text_space_vertical,
            self.text_space_top_left
        ))

        self.text_space_rect = pygame.Rect(
            self.text_space_top_left,
            (self.text_space_horizontal, self.text_space_vertical)
        )

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

        logger.info(
            "Char per line {0}, line per page {1}".format(
                self.char_per_line,
                self.lines_per_page
            )
        )

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

        if vertical_pixel_height \
                    and (vertical_pixel_height > 0) \
                    and font_object:
            text_height = font_object.get_linesize()

            # Let x be number of total lines that fit in
            # vertical_pixel_height v.
            # Let pixels_between_lines be p.
            # Then x*text_height + (x - 1)*p = v.
            # x(text_height + p) - p = v.
            # x = (v + p) / (text_height + p).
            pixels_between_lines = int(
                    text_height * max(0, spacing_factor_between_lines - 1)
                )

            num_lines = int(
                (vertical_pixel_height + pixels_between_lines) \
                / (text_height + pixels_between_lines)
            )

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

        logger.debug(
            "Converted {0} to word list {1}".format(
                text_string,
                ret_list
            )
        )

        return ret_list

    # Given a text string to display, returns a list of strings,
    # where each string takes up at most one line of display space.
    def get_text_lines(self, text_string):
        # List of strings
        ret_lines = []

        # Convert string to list of words to print. Newlines in the
        # string will carry over to a new text line.
        if text_string:
            text_lines = []

            # Separate out the string based on newlines.
            text_string_lines = [x.strip() for x in text_string.split('\n')]

            for line in text_string_lines:
                word_list = Text_Display.convert_to_word_list(line)

                logger.debug("Get text lines. Text: {0}\nWord List:{1}".format(line, word_list))

                curr_length = 0
                start_index = 0

                num_words = len(word_list)

                if num_words == 1:
                    # Simple case. Just 1 word.
                    text_lines.append(word_list[0])
                elif num_words > 1:
                    for index in range(num_words):
                        sub_list = None
                        str_to_add = None

                        word_length = len(word_list[index])

                        logger.debug(
                            "Word length for {0} is {1}".format(
                                word_list[index],
                                word_length
                            )
                        )

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
                            str_to_add = ''.join(sub_list).strip()

                            if str_to_add:
                                text_lines.append(str_to_add)
                                logger.debug(
                                    "Adding string {0} to text lines".format(
                                        str_to_add
                                    )
                                )

                    if start_index == (num_words - 1):
                        # We still need to add the last word.
                        str_to_add = word_list[start_index]
                        text_lines.append(str_to_add)
                        logger.debug(
                            "Adding string {0} to text lines".format(str_to_add)
                        )

        if text_lines:
            ret_lines = text_lines

        logger.debug(
            "Converted text \n{0}\nto lines\n{1}\n".format(
                text_string, ret_lines
            )
        )

        return ret_lines

    @classmethod
    def get_text_lines_test(cls, text_string, char_per_line):
        # List of strings
        ret_lines = []

        # Convert string to list of words to print. Newlines in the
        # string will carry over to a new text line.
        if text_string:
            text_lines = []

            # Separate out the string based on newlines.
            text_string_lines = [x.strip() for x in text_string.split('\n')]

            for line in text_string_lines:
                word_list = Text_Display.convert_to_word_list(line)

                logger.debug(
                    "Get text lines. Text: {0}\nWord List:{1}".format(
                        line,
                        word_list
                    )
                )

                curr_length = 0
                start_index = 0

                num_words = len(word_list)

                logger.debug("Max char in line: {0}".format(char_per_line))

                if num_words == 1:
                    # Simple case. Just 1 word.
                    text_lines.append(word_list[0])
                elif num_words > 1:
                    for index in range(num_words):
                        sub_list = None
                        str_to_add = None

                        word_length = len(word_list[index])

                        logger.debug(
                            "Word length for {0} is {1}".format(
                                word_list[index],
                                word_length
                            )
                        )

                        # Check if we can add this word or not.
                        if (curr_length + word_length) > char_per_line:
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
                            str_to_add = ''.join(sub_list).strip()

                            if str_to_add:
                                text_lines.append(str_to_add)
                                logger.debug(
                                    "Adding string {0} to text lines".format(
                                        str_to_add
                                    )
                                )

                    if start_index == (num_words - 1):
                        # We still need to add the last word.
                        str_to_add = word_list[start_index]
                        text_lines.append(str_to_add)
                        logger.debug(
                            "Adding string {0} to text lines".format(str_to_add)
                        )

        if text_lines:
            ret_lines = text_lines

        logger.debug(
            "Converted text \n{0}\nto lines\n{1}\n".format(
                text_string, ret_lines
            )
        )

        return ret_lines

    # Returns list of Text_Page objects, each containing
    # a list of strings, where each string represents one line of text
    # to place on display.
    def get_text_pages(self, text_string):
        ret_page_list = []
        page_list = []

        # Get lines of text to print.
        lines_to_print = self.get_text_lines(text_string)

        logger.debug(
            "Get text pages. Text: {0}\nLines:{1}".format(
                text_string,
                lines_to_print
            )
        )

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
                    page_list.append(
                        Text_Page(lines_to_print[start_index:end_index])
                    )

                    num_lines_processed = num_lines_processed + lines_to_add
                    remaining_lines = remaining_lines - lines_to_add
            else:
                # All lines can fit on a single page.
                page_list.append(Text_Page(lines_to_print))

        if page_list:
            ret_page_list = page_list

        # Debugging
        for page in ret_page_list:
            logger.debug(
                "Made page: {0}".format('\n#\n'.join(page.text_lines))
            )

        return ret_page_list

    def get_page_height(self, num_lines_in_page):
        ret_height = 0

        if num_lines_in_page:
            # Total height = n*(text_height) + (n - 1)*(pixels_between_lines),
            # where n is number of lines.
            # = n*(text_height + pixels_between_lines) - pixels_between_lines.
            text_height = self.font_object.get_linesize()
            pixels_between_lines = int(
                    text_height * max(0, self.spacing_factor_between_lines - 1)
                )

            ret_height = \
                (num_lines_in_page * (text_height + pixels_between_lines)) \
                - pixels_between_lines

        return ret_height

    # Blit text for the single page.
    # Does not update display, caller will need to do that.
    # If continue_icon is set to True, we will blit the object's continue
    # icon after the last line of the page.
    def blit_page(
                self,
                surface,
                text_page,
                show_continue_icon=False,
                alternative_top_left=None,
                horizontal_orientation=ORIENTATION_CENTERED,
                vertical_orientation=ORIENTATION_CENTERED,
            ):
        if surface and text_page:
            text_space_rect = self.text_space_rect

            if alternative_top_left:
                text_space_rect = pygame.rect(
                    alternative_top_left[0] + self.horizontal_padding,
                    alternative_top_left[1] + self.vertical_padding,
                    self.text_space_horizontal,
                    self.text_space_vertical,
                )

            # Blit background
            self.blit_background(
                surface,
                alternative_top_left=alternative_top_left,
            )

            num_lines = len(text_page.text_lines)

            page_height = self.get_page_height(num_lines)

            # Determine offsets based on placement.
            vertical_offset = 0
            if vertical_orientation == ORIENTATION_CENTERED:
                vertical_offset = int(
                        max(0, self.text_space_vertical - page_height) / 2
                    )
            elif vertical_orientation == ORIENTATION_TOP_JUSTIFIED:
                vertical_offset = 0
            elif vertical_orientation == ORIENTATION_BOTTOM_JUSTIFIED:
                vertical_offset = text_space_rect.bottom - page_height
            else:
                logger.error("Invalid vertical orientation.")

            for index in range(num_lines):
                text_line = text_page.text_lines[index]

                rendered_text = self.font_object.render(
                    text_line,
                    False,
                    self.font_color,
                )

                rendered_text_dimensions = rendered_text.get_size()
                text_width = rendered_text_dimensions[0]

                # Determine horizontal placement.
                text_top_left = None
                if horizontal_orientation == ORIENTATION_CENTERED:
                    text_top_left = (
                        text_space_rect.centerx - int(text_width / 2),
                        text_space_rect.y + vertical_offset
                    )
                elif horizontal_orientation == ORIENTATION_LEFT_JUSTIFIED:
                    text_top_left = (
                        text_space_rect.x,
                        text_space_rect.y + vertical_offset
                    )
                elif horizontal_orientation == ORIENTATION_RIGHT_JUSTIFIED:
                    text_top_left = (
                        text_space_rect.right - text_width,
                        text_space_rect.y + vertical_offset
                    )
                else:
                    logger.error("Invalid horizontal orientation.")

                if text_top_left:
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
                                - self.continue_icon.get_height() \
                                - 4
                        )

                        surface.blit(
                            self.continue_icon,
                            icon_top_left
                        )

                # Move to spot for next line.
                vertical_offset += int(
                            self.spacing_factor_between_lines \
                            * self.text_height
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
                background_image_path=None,
                background_color=viewingdata.COLOR_WHITE,
                font_color=fontinfo.FONT_COLOR_DEFAULT,
                horizontal_padding=OW_SIDE_MENU_HORIZONTAL_PADDING,
                vertical_padding=OW_SIDE_MENU_VERTICAL_PADDING,
                selection_icon_image_path=imagepaths.DEFAULT_MENU_SELECTION_ICON_PATH,
                spacing_factor_between_lines=MENU_LINE_SPACING_FACTOR,
            ):
        Text_Display.__init__(
            self,
            main_display_surface,
            display_rect,
            font_object,
            background_image_path=background_image_path,
            background_color=background_color,
            font_color=font_color,
            horizontal_padding=horizontal_padding,
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

        logger.info(
            "Max options per menu page: {0}".format(self.max_options_per_page)
        )

        # Maps option ID to dict that maps language ID to the rendered
        # text image for the option text.
        self.rendered_menu_option_mapping = self.get_menu_option_rendered_text()

    def get_menu_option_rendered_text(self):
        ret_dict = {}
        for option_id, option_info in menuoptions.OPTION_NAME_INFO.items():
            ret_dict[option_id] = {}

            for lang_id in language.Language.valid_language_ids:
                option_text = option_info.get(lang_id, None)

                if option_text:
                    ret_dict[option_id][lang_id] = self.font_object.render(
                        option_text,
                        False,
                        self.font_color,
                    )

        return ret_dict


    # Returns list of Menu Pages containing the menu option names.
    # If the returned list contains multiple Menu Pages, then each
    # Menu Page (including the final one) will have its last
    # option name be the "MORE OPTIONS" option to indicate that there
    # are additional menu options. The "MORE OPTIONS" option on the final
    # page will lead to the first page to allow looping.
    # option_id_list is a list of integers representing the option IDs
    # for the menu. They cannot be equal to MORE_OPTIONS_OPTION_ID.
    # additional options on a subsequent menu page.
    # max_options_per_page indicates how many options (lines) fit on one page.
    def get_menu_page_list(
                self,
                option_id_list,
            ):
        ret_pages = []

        if option_id_list and self.max_options_per_page:
            logger.debug(
                ("Adding {0} options to page with max of {1}"\
                + " options per page").format(
                    len(option_id_list),
                    self.max_options_per_page
                )
            )

            done = False
            remaining_options = option_id_list

            while not done:
                options_to_add = []

                if len(remaining_options) <= self.max_options_per_page:
                    # We can add all remaining options to this page.
                    options_to_add = remaining_options
                    logger.debug(
                        "Adding remaining {0} pages to menu page: {1}".format(
                            len(options_to_add),
                            options_to_add
                        )
                    )
                    done = True
                else:
                    # Options will carry on to next page.
                    options_to_add = \
                        remaining_options[0:self.max_options_per_page - 1]
                    options_to_add.append(MORE_OPTIONS_OPTION_ID)
                    logger.debug(
                        ("Adding {0} options plus \"more options\" " \
                        + "to menu page: {1}").format(
                            len(options_to_add) - 1,
                            options_to_add
                        )
                    )

                    remaining_options = \
                        remaining_options[self.max_options_per_page - 1:]
                    logger.debug(
                        "Remaining options: {0}".format(remaining_options)
                    )

                if options_to_add:
                    curr_page = Menu_Page(options_to_add)
                    ret_pages.append(curr_page)

        return ret_pages

    @classmethod
    def get_menu_page_list_test(
                cls,
                option_list,
                max_options_per_page
            ):
        ret_pages = []

        if option_list and max_options_per_page and more_options_str:
            logger.debug(
                ("Adding {0} options to page with max of {1}" \
                + " options per page").format(
                    len(option_list),
                    max_options_per_page
                )
            )

            done = False
            remaining_options = option_list

            while not done:
                options_to_add = []

                if len(remaining_options) <= max_options_per_page:
                    # We can add all remaining options to this page.
                    options_to_add = remaining_options
                    logger.debug(
                        "Adding remaining {0} pages to menu page: {1}".format(
                            len(options_to_add),
                            options_to_add
                        )
                    )
                    done = True
                else:
                    # Options will carry on to next page.
                    options_to_add = \
                        remaining_options[0:max_options_per_page - 1]
                    options_to_add.append(more_options_str)
                    logger.debug(
                        ("Adding {0} options plus \"more options\" " \
                        + "to menu page: {1}").format(
                            len(options_to_add) - 1,
                            options_to_add
                        )
                    )

                    remaining_options = \
                        remaining_options[max_options_per_page - 1:]
                    logger.debug(
                        "Remaining options: {0}".format(remaining_options)
                    )

                if options_to_add:
                    curr_page = Menu_Page(options_to_add)
                    ret_pages.append(curr_page)

        return ret_pages

    def get_rendered_menu_option_text(self, option_id):
        return self.rendered_menu_option_mapping.get(
            option_id,
            {}
        ).get(
            language.Language.current_language_id,
            None
        )

    # Does not update display.
    def blit_menu_page(
                self,
                surface,
                menu_page,
                curr_selected_index,
                alternative_top_left=None,
                horizontal_orientation=ORIENTATION_CENTERED,
                vertical_orientation=ORIENTATION_CENTERED,
            ):
        if surface and menu_page and curr_selected_index >= 0:
            num_options = menu_page.get_num_options()

            if num_options <= self.max_options_per_page:
                # Blit background.
                self.blit_background(
                    surface,
                    alternative_top_left=alternative_top_left,
                )

                page_height = self.get_page_height(num_options)

                # Determine space to blit text.
                target_rect = self.text_space_rect
                if alternative_top_left:
                    text_space_rect = pygame.rect(
                        alternative_top_left[0] + self.horizontal_padding,
                        alternative_top_left[1] + self.vertical_padding,
                        self.text_space_horizontal,
                        self.text_space_vertical,
                    )

                # Determine offsets based on placement.
                vertical_offset = 0
                if vertical_orientation == ORIENTATION_CENTERED:
                    vertical_offset = int(
                            max(0, self.text_space_vertical - page_height) / 2
                        )
                elif vertical_orientation == ORIENTATION_TOP_JUSTIFIED:
                    vertical_offset = 0
                elif vertical_orientation == ORIENTATION_BOTTOM_JUSTIFIED:
                    vertical_offset = text_space_rect.bottom - page_height
                else:
                    logger.error("Invalid vertical orientation.")

                vertical_offset = 0

                for index in range(num_options):
                    curr_option_id = menu_page.get_option_id(index)
                    curr_option = menuoptions.get_option_name(
                            curr_option_id,
                            language.Language.current_language_id
                        )

                    # Get rendered text and dimensions.
                    rendered_text = self.get_rendered_menu_option_text(
                            curr_option_id
                        )

                    if rendered_text:
                        rendered_text_dimensions = rendered_text.get_size()
                        text_width = rendered_text_dimensions[0]
                        text_height = rendered_text_dimensions[1]

                        text_top_left = None

                        if horizontal_orientation == ORIENTATION_CENTERED:
                            # Get top left for centered option text.
                            # Center the text horizontally.
                            text_top_left = (
                                target_rect.centerx - int(text_width / 2),
                                target_rect.y + vertical_offset
                            )
                        elif horizontal_orientation == ORIENTATION_LEFT_JUSTIFIED:
                            text_top_left = (
                                target_rect.x,
                                target_rect.y + vertical_offset
                            )
                        elif horizontal_orientation == ORIENTATION_RIGHT_JUSTIFIED:
                            text_top_left = (
                                target_rect.right - text_width,
                                target_rect.y + vertical_offset
                            )

                        if text_top_left:
                            # Blit the text.
                            surface.blit(
                                rendered_text,
                                text_top_left
                            )

                            # Blit the selection icon if we
                            # are on the selected index.
                            if index == curr_selected_index \
                                    and self.selection_icon:
                                # Vertically center the selection
                                # icon with the option.
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
                    vertical_offset += \
                        + int(self.spacing_factor_between_lines * text_height)

class Item_Listing_Display(Display):
    def __init__(
                self,
                main_display_surface,
                display_rect,
                item_quantity_font_object,
                background_image_path=None,
                background_color=viewingdata.COLOR_WHITE,
                item_quantity_font_color=fontinfo.FONT_COLOR_DEFAULT, # TODO change
                horizontal_padding=TEXT_DISPLAY_HORIZONTAL_PADDING,
                vertical_padding=TEXT_DISPLAY_VERTICAL_PADDING,
                continue_up_icon_image_path=None,
                continue_down_icon_image_path=None,
                selection_image_path=imagepaths.ITEM_LISTING_SELECTED_DEFAULT_PATH,
            ):
        Display.__init__(
            self,
            main_display_surface,
            display_rect,
            background_image_path=background_image_path,
            background_color=background_color,
        )

        self.item_quantity_font_object = item_quantity_font_object
        self.item_quantity_font_color = item_quantity_font_color

        self.horizontal_padding = horizontal_padding
        self.vertical_padding = vertical_padding
        self.pixels_between_items = ITEM_VIEWING_PIXEL_SPACING

        self.item_viewing_top_left = (
                self.display_rect.x + self.horizontal_padding,
                self.display_rect.y + self.vertical_padding,
            )

        self.item_viewing_space_horizontal = self.display_rect.width  \
                                            - (2 * self.horizontal_padding)
        self.item_viewing_space_vertical = self.display_rect.height  \
                                            - (2 * self.vertical_padding)

        self.item_viewing_space_rect = pygame.Rect(
            self.item_viewing_top_left[0],
            self.item_viewing_top_left[1],
            self.item_viewing_space_horizontal,
            self.item_viewing_space_vertical
        )

        # Row, col dimensions.
        self.item_viewing_grid_dimensions = \
            Item_Listing_Display.get_item_viewing_grid_dimensions(
                self.item_viewing_space_horizontal,
                self.item_viewing_space_vertical,
            )
        self.num_columns = \
            self.item_viewing_grid_dimensions[0]
        self.num_rows = \
            self.item_viewing_grid_dimensions[1]

        self.max_num_items = self.num_columns * self.num_rows

        # Define continue icons if possible.
        self.continue_up_icon = None
        self.continue_down_icon = None

        if continue_up_icon_image_path:
            self.continue_up_icon = pygame.image.load(
                    continue_up_icon_image_path
                ).convert_alpha()

        if continue_down_icon_image_path:
            self.continue_down_icon = pygame.image.load(
                    continue_down_icon_image_path
                ).convert_alpha()

        self.selection_image = None
        if selection_image_path:
            self.selection_image = pygame.image.load(
                    selection_image_path
                ).convert_alpha()

    @classmethod
    def get_item_viewing_grid_dimensions(
                cls,
                horizontal_space,
                vertical_space,
                item_icon_size=itemdata.ITEM_ICON_SIZE,
                space_between_items=ITEM_VIEWING_PIXEL_SPACING,
            ):
        dimensions = (0,0)

        if horizontal_space and vertical_space:
            # Let n be number of items in the row,
            # Let s be the space between items.
            # Let h be the horizontal space available.
            # Then (n * icon_size) + (n - 1) * s = h.
            # n * (icon_size + s) - s = h.
            # n = (h + s) / (icon_size + s).
            num_row_items = int(
                (horizontal_space + space_between_items)    \
                / (item_icon_size + space_between_items)
            )

            num_column_items = int(
                (vertical_space + space_between_items)  \
                / (item_icon_size + space_between_items)
            )

            if num_row_items and num_column_items:
                dimensions = (num_row_items, num_column_items)

        return dimensions

    # Item listing data must be list of length-2 lists of the form
    # [item object, quantity].
    # selected_index is teh index in item_listing_data for the
    # item currently selected.
    # first_viewable_row_index is the row index for the first row of items
    # to be visible in the viewing.
    def blit_item_listing(
                self,
                surface,
                item_listing_data,
                first_viewable_row_index,
                selected_index,
                show_continue_icon=True,
                alternative_top_left=None,
            ):
        if surface and item_listing_data \
                and selected_index >= 0 and first_viewable_row_index >= 0:
            item_space_rect = self.item_viewing_space_rect

            if alternative_top_left:
                item_space_rect = pygame.rect(
                    alternative_top_left[0] + self.horizontal_padding,
                    alternative_top_left[1] + self.vertical_padding,
                    self.item_viewing_space_rect.width,
                    self.item_viewing_space_rect.height
                )

            # Blit background
            self.blit_background(
                surface,
                alternative_top_left=alternative_top_left,
            )

            # Blit the items, starting with the first viewable row.
            starting_index = \
                first_viewable_row_index * self.num_columns

            # Go until we run out of space or items.
            total_items = len(item_listing_data)
            num_remaining_items = min(
                    self.max_num_items,
                    total_items - starting_index
                )

            curr_index = starting_index
            logger.info("Starting with item index {0}".format(curr_index))

            horizontal_offset = 0
            vertical_offset = 0

            while curr_index < num_remaining_items:
                curr_viewing_row = int(
                        (curr_index - starting_index) / self.num_columns
                    )
                curr_viewing_col = \
                    (curr_index - starting_index) % self.num_columns

                horizontal_offset = \
                    ((curr_index - starting_index) % self.num_columns) \
                    * (itemdata.ITEM_ICON_SIZE + self.pixels_between_items)

                vertical_offset = \
                    (curr_viewing_row - first_viewable_row_index) \
                    * (itemdata.ITEM_ICON_SIZE + self.pixels_between_items)

                curr_item_info = item_listing_data[curr_index]
                curr_item = curr_item_info[0]
                item_name = curr_item.get_name()
                item_quantity = curr_item_info[1]
                item_image = curr_item.get_icon()

                logger.info("Curr item {0} x{1} at {2}".format(
                    item_name,
                    item_quantity,
                    (curr_viewing_row, curr_viewing_col)
                ))

                # Get rendered quantity text if item is stackable.
                rendered_quantity_text = None
                if curr_item.is_stackable():
                    rendered_quantity_text = \
                        self.item_quantity_font_object.render(
                            str(quantity),
                            False,
                            self.item_quantity_font_color,
                        )

                # Blit item and quantity text if needed.
                item_rect = pygame.Rect(
                    item_space_rect.x + horizontal_offset,
                    item_space_rect.y + vertical_offset,
                    itemdata.ITEM_ICON_SIZE,
                    itemdata.ITEM_ICON_SIZE,
                )

                # Check if this is the selected icon. If so,
                # blit the selection background.
                if (selected_index == curr_index) \
                        and self.selection_image:
                    # Center on the item icon.
                    select_image_rect = self.selection_image.get_rect(
                        center=item_rect.center
                    )

                    surface.blit(
                        self.selection_image,
                        select_image_rect,
                    )

                if item_image:
                    surface.blit(
                        item_image,
                        item_rect,
                    )

                if rendered_quantity_text:
                    text_top_left = item_rect.topleft
                    surface.blit(
                        item_image,
                        text_top_left,
                    )

                curr_index += 1

            # Blit the up and down arrows if there are items above/below.
            if (starting_index >= self.num_columns):
                # We have at least 1 row above us.

                # Center and line with top of display.
                continue_up_rect = self.continue_up_icon.get_rect(
                    center=self.display_rect.center
                )
                #continue_up_rect.centerx = self.display_rect.centerx
                continue_up.rect.top = self.display_rect.top

                surface.blit(
                    self.continue_up_icon,
                    continue_up_rect
                )

            if (total_items - starting_index) > self.max_num_items:
                # We have items after us.

                # Center and line with bottom of display.
                continue_down_rect = self.continue_down_icon.get_rect(
                    center=self.display_rect.center
                )
                #continue_down_rect.centerx = self.display_rect.centerx
                continue_down.rect.bottom = self.display_rect.bottom

                surface.blit(
                    self.continue_down_icon,
                    continue_down_rect
                )

# set up logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
