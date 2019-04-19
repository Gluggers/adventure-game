# -*- coding: utf-8 -*-
"""This module contains classes and methods for Viewing objects.

Viewing objects handle Display objects and act as an interface between
the Game object and Display-related methods. The Viewing classes handle
functions such as blitting objects onto the screen, blitting text,
handling traversals through menus and text sequences, and scrolling the map
upon character movement.
"""

import logging
import sys
import pygame
import display
import fontinfo
import imageids
import imagepaths
import language
import menuoptions
import tile
import timekeeper
import viewingdata

# Pixel distance for each phase of the walking animation.
STEP_DURATION = int(tile.TILE_SIZE / 4)

### TIME CONSTANTS ###
NUM_MS_SECOND = 1000
WALK_SINGLE_TILE_SCROLL_TIME_MS = int(NUM_MS_SECOND * 0.65)
WALK_SINGLE_PIXEL_SCROLL_TIME_MS = int(WALK_SINGLE_TILE_SCROLL_TIME_MS / tile.TILE_SIZE)
RUN_SINGLE_TILE_SCROLL_TIME_MS = int(NUM_MS_SECOND * 0.25)
RUN_SINGLE_PIXEL_SCROLL_TIME_MS = int(RUN_SINGLE_TILE_SCROLL_TIME_MS / tile.TILE_SIZE)


VIEWING_TILE_PADDING = 2

# Base Viewing class.
class Viewing(object):
    """Base class that handles viewing-based methods and functions.

    Viewing objects handle Display objects and act as an interface between
    the Game object and Display-related methods. This base class provides
    basic inheritable methods, some of which are templates for child classes
    to fully implement or customize by overriding.

    Attributes:
        main_display_surface: the pygame Surface object for the main display
            screen linked to the Viewing object. This Surface object is used
            to blit pixels and changes to the display screen.
    """

    def __init__(
            self,
            main_display_surface,
        ):
        """Initializes the Viewing object.

        Args:
            main_display_surface: the pygame Surface object for the main
                display screen that will be linked to the Viewing object.
                This Surface object is used to blit pixels and changes to
                the display screen.
        """

        self._main_display_surface = main_display_surface

    @property
    def main_display_surface(self):
        """Returns the pygame Surface object for the main display."""

        return self._main_display_surface

    def refresh_self(self):
        """Refreshes self. Does not update display.

        Base parent class method does not do anything.
        Child classes are responsible for implementation.

        Caller must update display if needed.
        """

        pass

    def blit_self(self):
        """Blits self. Does not update display.

        Base parent class method does not do anything.
        Child classes are responsible for implementation.

        Caller must update display if needed.
        """

        pass

    def refresh_and_blit_self(self):
        """Updates and blits self. Does not update display.

        Base parent class method calls refresh_self and
        blit_self, which do not do anything by default.
        Child classes are responsible for implementation.

        Caller must update display if needed.
        """

        self.refresh_self()
        self.blit_self()

    def display_single_text_page(
            self,
            text_display,
            page,
            advance_delay_ms=viewingdata.DEFAULT_ADVANCE_DELAY_MS,
            auto_advance=False,
            refresh_during=True,
            horizontal_orientation=display.ORIENTATION_CENTERED,
            vertical_orientation=display.ORIENTATION_CENTERED,
            alternative_top_left=None,
            no_display_update=True,
        ):
        """Displays a single page's worth of text.

        The amount of text on the single page is determined by the page
        argument, which should be constructed by the same display as
        text_display.

        Args:
            text_display: the TextDisplay object that should be used to
                display the text. For best results, use the same TextDisplay
                object that generated the page argument.
            page: the TextPage object that contains the text to display.
                For best results, use a TextPage object that was made by
                the text_display argument.
            advance_delay_ms: number of milliseconds to wait before user
                can exit out of or continue through the text display.
            auto_advance: if True, the text display will finish and exit
                after advance_delay_ms milliseconds without any user
                input or interaction. If False, user must manually continue
                through or exit out of the text display.
            refresh_during: if True, the calling Viewing object will refresh
                itself periodically while waiting for the text display
                to finish up. If False, the calling Viewing object will not
                refresh during the text display.
            horizontal_orientation: determines the text's horizontal
                orientation as defined by the orientation constants in
                the display module. Current accepted values are:
                    ORIENTATION_CENTERED - center horizontally.
                    ORIENTATION_LEFT_JUSTIFIED - left justify the text.
                    ORIENTATION_RIGHT_JUSTIFIED - right justify the text.
            vertical_orientation: determines the text's vertical
                orientation as defined by the orientation constants in
                the display module. Current accepted values are:
                    ORIENTATION_CENTERED - center vertically.
                    ORIENTATION_TOP_JUSTIFIED = top justify the text.
                    ORIENTATION_BOTTOM_JUSTIFIED = bottom justify the text.
            alternative_top_left: optional argument where the caller can pass
                in a tuple of x,y screen pixel coordinates to define a custom
                top left corner for text_display when blitting the text.
                Default is None (use the predefined top left of text_display).
            no_display_update: if True, the pygame display will not update
                when blitting the text in this method or while waiting for
                the user, even if refresh_during is set to True. This option
                is set for method callers who want to blit multiple things
                before updating the display.
        """

        if page and text_display and self._main_display_surface:
            text_display.blit_page(
                self._main_display_surface,
                page,
                show_continue_icon=False,
                horizontal_orientation=horizontal_orientation,
                vertical_orientation=vertical_orientation,
                alternative_top_left=alternative_top_left,
            )

            if not no_display_update:
                pygame.display.update()

            # Pause if needed.
            if advance_delay_ms:
                pygame.time.wait(advance_delay_ms)

            if not auto_advance:
                # Refresh and reblit self.
                if refresh_during:
                    self.refresh_and_blit_self()

                # Reblit page but with continue icon if available.
                text_display.blit_page(
                    self._main_display_surface,
                    page,
                    show_continue_icon=True,
                    horizontal_orientation=horizontal_orientation,
                    vertical_orientation=vertical_orientation,
                    alternative_top_left=alternative_top_left,
                )

                if not no_display_update:
                    pygame.display.update()

                # Clear event queue to prevent premature advancement.
                pygame.event.clear()

                # Wait for user to advance.
                advance = False
                refresh_tick_counter = 0
                reblit_tick_counter = 0

                LOGGER.debug("Waiting to advance...")

                while not advance:
                    timekeeper.Timekeeper.tick()
                    refresh_tick_counter = (refresh_tick_counter + 1) \
                                    % timekeeper.REFRESH_INTERVAL_NUM_TICKS
                    reblit_tick_counter = (reblit_tick_counter + 1) \
                                    % timekeeper.OW_REBLIT_INTERVAL_NUM_TICKS

                    if refresh_during \
                            and (refresh_tick_counter == 0):
                        # Refresh and reblit self and page.
                        LOGGER.debug("Refreshing while waiting.")
                        self.refresh_and_blit_self()
                        text_display.blit_page(
                            self._main_display_surface,
                            page,
                            show_continue_icon=True,
                            horizontal_orientation=horizontal_orientation,
                            vertical_orientation=vertical_orientation,
                            alternative_top_left=alternative_top_left,
                        )

                        if not no_display_update:
                            pygame.display.update()

                    elif reblit_tick_counter == 0:
                        self.blit_self()
                        text_display.blit_page(
                            self._main_display_surface,
                            page,
                            show_continue_icon=True,
                            horizontal_orientation=horizontal_orientation,
                            vertical_orientation=vertical_orientation,
                            alternative_top_left=alternative_top_left,
                        )

                        if not no_display_update:
                            pygame.display.update()

                    for events in pygame.event.get():
                        if events.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit(0)
                        elif events.type == pygame.KEYDOWN:
                            if events.key in viewingdata.TEXT_ADVANCE_KEYS:
                                LOGGER.debug("Advancing to next page")
                                advance = True

    def display_text_display(
            self,
            text_display,
            text_to_display,
            font_color=viewingdata.COLOR_BLACK,
            advance_delay_ms=viewingdata.DEFAULT_ADVANCE_DELAY_MS,
            auto_advance=False,
            refresh_during=True,
            refresh_after=True,
            horizontal_orientation=display.ORIENTATION_CENTERED,
            vertical_orientation=display.ORIENTATION_CENTERED,
            alternative_top_left=None,
            no_display_update=True,
        ):
        """Displays text on the specified TextDisplay object.

        The amount of text on each line and in a single text box space is
        determined by the TextDisplay object properties.

        By default, the user will have to manually advance through the
        text display sequence to move on to the next chunk of text or to
        finish displaying the text.

        Args:
            text_display: the TextDisplay object will display the text.
                Depending on the TextDisplay object properties and on
                the amount of text in the text_to_display argument,
                the text may show up across multiple lines or even across
                multiple text pages.
            text_to_display: can either be a String or a list of Strings that
                represent the text to display. If passing in a single String,
                the String will be broken up across several lines depending
                on length and whether or not newline characters appear in the
                string.
                If passing in a list of Strings, each String in the list will
                start on a new line of text, and each individual String may
                take up multiple lines depending on length and whether or not
                the String contains newline characters.
            font_color: can either be a tuple or a list of tuples that
                represent the font color for the text lines. Note that
                each font_color tuple is a 3-tuple that defines the hex
                value of the color, such as (0x23, 0x4A, 0x5F).
                If passing in a single tuple, the entire text will be
                displayed in that color.
                If passing in a list of tuples, the user must also pass in
                a list of Strings for text_to_display, and each list
                must be of the same length.
                List values of font_color are only valid if text_to_display
                is a list of strings, and each index of the list will
                correspond to the next. In other words, each tuple will define
                the color of the corresponding String (the first tuple
                in the font_color list will define the color for the first
                String in text_to-display, etc).
                If text_to_display is a list of strings and font_color
                is a single tuple, then that color will apply to each text
                string in text_to_display.
            advance_delay_ms: number of milliseconds to wait before user
                can exit out of or continue through the text display.
            auto_advance: if True, the text display will finish and exit
                after advance_delay_ms milliseconds without any user
                input or interaction. If False, user must manually continue
                through or exit out of the text display.
            refresh_during: if True, the calling Viewing object will refresh
                itself periodically while waiting for the text display
                to finish up. If False, the calling Viewing object will not
                refresh during the text display.
            refresh_after: if True, the calling Viewing object will refresh
                itself once the TextDisplay object has finished displaying
                the text.
                If False, the calling Viewing object will not
                refresh after the text display.
            horizontal_orientation: determines the text's horizontal
                orientation as defined by the orientation constants in
                the display module. Current accepted values are:
                    ORIENTATION_CENTERED - center horizontally.
                    ORIENTATION_LEFT_JUSTIFIED - left justify the text.
                    ORIENTATION_RIGHT_JUSTIFIED - right justify the text.
            vertical_orientation: determines the text's vertical
                orientation as defined by the orientation constants in
                the display module. Current accepted values are:
                    ORIENTATION_CENTERED - center vertically.
                    ORIENTATION_TOP_JUSTIFIED = top justify the text.
                    ORIENTATION_BOTTOM_JUSTIFIED = bottom justify the text.
            alternative_top_left: optional argument where the caller can pass
                in a tuple of x,y screen pixel coordinates to define a custom
                top left corner for text_display when blitting the text.
                Default is None (use the predefined top left of text_display).
            no_display_update: if True, the pygame display will not update
                when blitting the text in this method or while waiting for
                the user, even if refresh_during or refresh_after are
                set to True. This option is set for method callers who want
                to blit multiple things before updating the display.
        """

        if self._main_display_surface and text_display \
            and text_to_display and font_color:
            page_list = []

            if isinstance(text_to_display, str) \
                and not isinstance(font_color, tuple):
                LOGGER.error(
                    "Invalid format for font color with" \
                    + "single string for text_to_display."
                )
            else:
                # Get the pages.
                page_list = text_display.get_text_pages(
                    text_to_display,
                    font_color=font_color,
                )

            if page_list:
                # Display each text page.
                for page in page_list:
                    self.display_single_text_page(
                        text_display,
                        page,
                        advance_delay_ms=advance_delay_ms,
                        auto_advance=auto_advance,
                        refresh_during=refresh_during,
                        horizontal_orientation=horizontal_orientation,
                        vertical_orientation=vertical_orientation,
                        alternative_top_left=alternative_top_left,
                        no_display_update=no_display_update,
                    )

                    # Refresh and reblit self.
                    if refresh_during:
                        self.refresh_and_blit_self()
                        self.display_single_text_page(
                            text_display,
                            page,
                            advance_delay_ms=0,
                            auto_advance=True,
                            refresh_during=False,
                            horizontal_orientation=horizontal_orientation,
                            vertical_orientation=vertical_orientation,
                            alternative_top_left=alternative_top_left,
                            no_display_update=True,
                        )

                        if not no_display_update:
                            pygame.display.update()

            if refresh_after:
                self.refresh_and_blit_self()
                if not no_display_update:
                    pygame.display.update()

    def display_text_display_first_page(
            self,
            text_display,
            text_to_display,
            font_color=viewingdata.COLOR_BLACK,
            advance_delay_ms=viewingdata.DEFAULT_ADVANCE_DELAY_MS,
            auto_advance=False,
            refresh_during=True,
            refresh_after=True,
            horizontal_orientation=display.ORIENTATION_CENTERED,
            vertical_orientation=display.ORIENTATION_CENTERED,
            alternative_top_left=None,
            no_display_update=True,
        ):
        """Displays a single page's worth of text on the specified TextDisplay.

        The amount of text on each line and in a single text page space is
        determined by the TextDisplay object properties.

        Even if the amount of input text is more than the amount that will
        fit on a single text page, the method will display only the first
        page.

        By default, the user will have to manually advance through the
        text display sequence to finish displaying the text.

        Args:
            text_display: the TextDisplay object will display the text.
                Depending on the TextDisplay object properties and on
                the amount of text in the text_to_display argument,
                the text may show up across multiple lines or may be cut off
                if it does not all fit on one page.
            text_to_display: can either be a String or a list of Strings that
                represent the text to display. If passing in a single String,
                the String will be broken up across several lines depending
                on length and whether or not newline characters appear in the
                string.
                If passing in a list of Strings, each String in the list will
                start on a new line of text, and each individual String may
                take up multiple lines depending on length and whether or not
                the String contains newline characters.
            font_color: can either be a tuple or a list of tuples that
                represent the font color for the text lines. Note that
                each font_color tuple is a 3-tuple that defines the hex
                value of the color, such as (0x23, 0x4A, 0x5F).
                If passing in a single tuple, the entire text will be
                displayed in that color.
                If passing in a list of tuples, the user must also pass in
                a list of Strings for text_to_display, and each list
                must be of the same length.
                List values of font_color are only valid if text_to_display
                is a list of strings, and each index of the list will
                correspond to the next. In other words, each tuple will define
                the color of the corresponding String (the first tuple
                in the font_color list will define the color for the first
                String in text_to-display, etc).
                If text_to_display is a list of strings and font_color
                is a single tuple, then that color will apply to each text
                string in text_to_display.
            advance_delay_ms: number of milliseconds to wait before user
                can exit out of or continue through the text display.
            auto_advance: if True, the text display will finish and exit
                after advance_delay_ms milliseconds without any user
                input or interaction. If False, user must manually continue
                through or exit out of the text display.
            refresh_during: if True, the calling Viewing object will refresh
                itself periodically while waiting for the text display
                to finish up. If False, the calling Viewing object will not
                refresh during the text display.
            refresh_after: if True, the calling Viewing object will refresh
                itself once the TextDisplay object has finished displaying
                the text.
                If False, the calling Viewing object will not
                refresh after the text display.
            horizontal_orientation: determines the text's horizontal
                orientation as defined by the orientation constants in
                the display module. Current accepted values are:
                    ORIENTATION_CENTERED - center horizontally.
                    ORIENTATION_LEFT_JUSTIFIED - left justify the text.
                    ORIENTATION_RIGHT_JUSTIFIED - right justify the text.
            vertical_orientation: determines the text's vertical
                orientation as defined by the orientation constants in
                the display module. Current accepted values are:
                    ORIENTATION_CENTERED - center vertically.
                    ORIENTATION_TOP_JUSTIFIED = top justify the text.
                    ORIENTATION_BOTTOM_JUSTIFIED = bottom justify the text.
            alternative_top_left: optional argument where the caller can pass
                in a tuple of x,y screen pixel coordinates to define a custom
                top left corner for text_display when blitting the text.
                Default is None (use the predefined top left of text_display).
            no_display_update: if True, the pygame display will not update
                when blitting the text in this method or while waiting for
                the user, even if refresh_during or refresh_after are
                set to True. This option is set for method callers who want
                to blit multiple things before updating the display.
        """

        if text_to_display and self._main_display_surface \
            and text_display and font_color:
            page_list = []

            if isinstance(text_to_display, str) \
                and not isinstance(font_color, tuple):
                LOGGER.error(
                    "Invalid format for font color" \
                    +  " with single string for text_to_display."
                )
            else:
                # Get the pages.
                page_list = text_display.get_text_pages(
                    text_to_display,
                    font_color=font_color,
                )

            if page_list:
                num_pages = len(page_list)

                if num_pages > 1:
                    LOGGER.warn("This method only blits first page.")
                    LOGGER.warn("Submitted text is %d pages.", num_pages)

                # Display just the first page.
                self.display_single_text_page(
                    text_display,
                    page_list[0],
                    advance_delay_ms=advance_delay_ms,
                    auto_advance=auto_advance,
                    refresh_during=refresh_during,
                    horizontal_orientation=horizontal_orientation,
                    vertical_orientation=vertical_orientation,
                    alternative_top_left=alternative_top_left,
                    no_display_update=no_display_update,
                )

            if refresh_after:
                self.refresh_and_blit_self()

                if not no_display_update:
                    pygame.display.update()

    def display_input_text_box(
            self,
            text_display,
            prompt_text_to_display,
            prompt_font_color=viewingdata.COLOR_BLACK,
            input_font_color=viewingdata.COLOR_BLUE_TEXT,
            input_delay_ms=viewingdata.INITIAL_INPUT_DELAY_MS,
            refresh_during=True,
            horizontal_orientation=display.ORIENTATION_CENTERED,
            vertical_orientation=display.ORIENTATION_CENTERED,
            alternative_top_left=None,
            no_display_update=True,
        ):
        """Displays a text input box for user interaction and returns input.

        The amount of text that fits on each line and on the overall input
        box is determined by the TextDisplay object properties.

        Even if the amount of text is more than the amount that will
        fit on a single text page, the method will display only the first
        page.

        The text input box will show the current inputted text as the user
        interacts with the input box. Only a subset of keyboard keys will
        generate user input, as defined in the viewingdata module.

        The user can delete the last character of the passed-in input by
        pressing the backspace key.

        Args:
            text_display: the TextDisplay object will display the input
                prompt and the inputted text.
                Depending on the TextDisplay object properties and on
                the amount of text in the text_to_display argument,
                the text may show up across multiple lines or may be cut off
                if it does not all fit on one page.
            prompt_text_to_display: String that represents the input prompt
                to display to the user.
            prompt_font_color:  3-tuple that defines the hex value of the
                font color for the input prompt text.
            input_font_color:  3-tuple that defines the hex value of the
                font color for the user's inputted text.
            input_delay_ms: number of milliseconds to wait before user
                can start inputting text.
            refresh_during: if True, the calling Viewing object will refresh
                itself periodically while waiting for the text display
                to finish up. If False, the calling Viewing object will not
                refresh during the text display.
            horizontal_orientation: determines the text's horizontal
                orientation as defined by the orientation constants in
                the display module. Current accepted values are:
                    ORIENTATION_CENTERED - center horizontally.
                    ORIENTATION_LEFT_JUSTIFIED - left justify the text.
                    ORIENTATION_RIGHT_JUSTIFIED - right justify the text.
            vertical_orientation: determines the text's vertical
                orientation as defined by the orientation constants in
                the display module. Current accepted values are:
                    ORIENTATION_CENTERED - center vertically.
                    ORIENTATION_TOP_JUSTIFIED = top justify the text.
                    ORIENTATION_BOTTOM_JUSTIFIED = bottom justify the text.
            alternative_top_left: optional argument where the caller can pass
                in a tuple of x,y screen pixel coordinates to define a custom
                top left corner for text_display when blitting the text.
                Default is None (use the predefined top left of text_display).
            no_display_update: if True, the pygame display will not update
                when blitting the text in this method or while waiting for
                the user, even if refresh_during or refresh_after are
                set to True. This option is set for method callers who want
                to blit multiple things before updating the display.

        Returns:
            Input string from the user. The returned String will be an empty
            string if no input is given or if the user the passed-in
            input. Max input string length is defined in the viewingdata
            module using the constant MAX_INPUT_STR_LEN.
        """

        user_input_str = ""

        if prompt_text_to_display and self._main_display_surface \
            and text_display:
            done = False
            input_suffix = "*"
            refresh_tick_counter = 0
            reblit_tick_counter = 0
            font_colors = [prompt_font_color, input_font_color]

            # Display just the first page.
            self.display_text_display_first_page(
                text_display,
                [prompt_text_to_display, user_input_str + input_suffix],
                font_color=font_colors,
                advance_delay_ms=input_delay_ms,
                auto_advance=True,
                refresh_during=refresh_during,
                refresh_after=False,
                horizontal_orientation=horizontal_orientation,
                vertical_orientation=vertical_orientation,
                alternative_top_left=alternative_top_left,
                no_display_update=no_display_update,
            )

            if not no_display_update:
                pygame.display.update()

            while not done:
                # Wait for user to give input.
                given_input = False
                while not given_input:
                    timekeeper.Timekeeper.tick()

                    refresh_tick_counter = (refresh_tick_counter + 1) \
                            % timekeeper.REFRESH_INTERVAL_NUM_TICKS
                    reblit_tick_counter = (reblit_tick_counter + 1) \
                                    % timekeeper.OW_REBLIT_INTERVAL_NUM_TICKS

                    if refresh_during \
                            and (refresh_tick_counter == 0):
                        LOGGER.debug("Refreshing while waiting.")
                        self.refresh_and_blit_self()
                        text_lines = [
                            prompt_text_to_display,
                            user_input_str + input_suffix
                        ]
                        self.display_text_display_first_page(
                            text_display,
                            text_lines,
                            font_color=font_colors,
                            advance_delay_ms=0,
                            auto_advance=True,
                            refresh_during=refresh_during,
                            refresh_after=False,
                            horizontal_orientation=horizontal_orientation,
                            vertical_orientation=vertical_orientation,
                            alternative_top_left=alternative_top_left,
                            no_display_update=no_display_update,
                        )
                        if not no_display_update:
                            pygame.display.update()
                    elif reblit_tick_counter == 0:
                        self.blit_self()
                        text_lines = [
                            prompt_text_to_display,
                            user_input_str + input_suffix
                        ]
                        self.display_text_display_first_page(
                            text_display,
                            text_lines,
                            font_color=font_colors,
                            advance_delay_ms=0,
                            auto_advance=True,
                            refresh_during=refresh_during,
                            refresh_after=False,
                            horizontal_orientation=horizontal_orientation,
                            vertical_orientation=vertical_orientation,
                            alternative_top_left=alternative_top_left,
                            no_display_update=no_display_update,
                        )
                        if not no_display_update:
                            pygame.display.update()

                    for events in pygame.event.get():
                        if events.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit(0)
                        elif events.type == pygame.KEYDOWN:
                            if events.key == pygame.K_RETURN:
                                given_input = True
                                done = True
                            elif events.key == pygame.K_ESCAPE:
                                # Exit and return None.
                                given_input = True
                                done = True
                                user_input_str = None
                            elif events.key == pygame.K_BACKSPACE:
                                # Delete last character.
                                given_input = True

                                if user_input_str:
                                    user_input_str = user_input_str[:-1]
                            else:
                                entered_char = viewingdata.get_pygame_key_str(
                                    events.key,
                                    shift_on=False,
                                )

                                if entered_char and len(user_input_str) \
                                        < viewingdata.MAX_INPUT_STR_LEN:
                                    given_input = True
                                    user_input_str += entered_char

                # Display just the first page.
                self.display_text_display_first_page(
                    text_display,
                    [prompt_text_to_display, user_input_str + input_suffix],
                    font_color=font_colors,
                    advance_delay_ms=0,
                    auto_advance=True,
                    refresh_during=refresh_during,
                    refresh_after=False,
                    horizontal_orientation=horizontal_orientation,
                    vertical_orientation=vertical_orientation,
                    alternative_top_left=alternative_top_left,
                    no_display_update=no_display_update,
                )

                if not no_display_update:
                    pygame.display.update()

        return user_input_str

    def display_menu_display(
            self,
            menu_display,
            option_id_list,
            font_color=viewingdata.COLOR_BLACK,
            horizontal_orientation=display.ORIENTATION_CENTERED,
            vertical_orientation=display.ORIENTATION_CENTERED,
            load_delay_ms=viewingdata.DEFAULT_MENU_LOAD_DELAY_MS,
            option_switch_delay_ms=viewingdata.DEFAULT_MENU_OPTION_SWITCH_DELAY_MS,
            refresh_during=True,
            refresh_after=True,
            alternative_top_left=None,
        ):
        """Displays a menu for user interaction and returns the selected option.

        The number of menu options visible on each menu page is determined by
        the properties of menu_display.

        In the event where all the options in option_id_list cannot fit on a
        single menu page, each menu page will have an option at
        the end indicating that more options are available. The "more options"
        option on the last page will loop back to the first page of menu
        options to allow for backtracking.

        For best results, each menu option name should not be longer than the
        horizontal space available in the menu_display object.

        Args:
            menu_display: MenuDisplay object that will display the menu
                options.
            option_id_list: list of menu option ID values for the menu_display
                object to display. The option ID values will be translated
                into their corresponding names depending on the
                current game language.
            font_color:  3-tuple that defines the font color for the text.
            load_delay_ms: time in milliseconds that the user must wait once
                the menu loads before being able to choose options.
            option_switch_delay_ms: time in milliseconds that the user must wait
                after each option switch before taking another action.
            refresh_during: if True, the calling Viewing object will refresh
                itself periodically while waiting for the text display
                to finish up. If False, the calling Viewing object will not
                refresh during the text display.
            refresh_after: if True, the calling Viewing object will refresh
                itself and update the pygame display after the user finishes
                interacting with the menu.
            horizontal_orientation: determines the text's horizontal
                orientation as defined by the orientation constants in
                the display module. Current accepted values are:
                    ORIENTATION_CENTERED - center horizontally.
                    ORIENTATION_LEFT_JUSTIFIED - left justify the text.
                    ORIENTATION_RIGHT_JUSTIFIED - right justify the text.
            vertical_orientation: determines the text's vertical
                orientation as defined by the orientation constants in
                the display module. Current accepted values are:
                    ORIENTATION_CENTERED - center vertically.
                    ORIENTATION_TOP_JUSTIFIED = top justify the text.
                    ORIENTATION_BOTTOM_JUSTIFIED = bottom justify the text.
            alternative_top_left: optional argument where the caller can pass
                in a tuple of x,y screen pixel coordinates to define a custom
                top left corner for text_display when blitting the text.
                Default is None (use the predefined top left of menu_display).

        Returns:
            option ID value for the selected option. None if no option was
            selected (e.g. if the user exits the menu via an escape key).
        """

        ret_option_id = None
        menu_pages = []

        if self._main_display_surface \
                and menu_display \
                and option_id_list:
            # Get list of menu pages.
            menu_pages = menu_display.get_menu_page_list(
                option_id_list,
                font_color=font_color,
            )

        if menu_pages:
             # Start at top of menu.
            curr_selected_index = 0

            # Blit first menu page.
            curr_page_index = 0

            num_pages = len(menu_pages)

            done = False
            refresh_tick_counter = 0
            reblit_tick_counter = 0

            while not done:
                curr_page = menu_pages[curr_page_index]
                num_options = curr_page.get_num_options()
                curr_option_id = None

                # Blit the current menu page.
                menu_display.blit_menu_page(
                    self._main_display_surface,
                    curr_page,
                    curr_selected_index,
                    horizontal_orientation=horizontal_orientation,
                    vertical_orientation=vertical_orientation,
                    alternative_top_left=alternative_top_left,
                )

                pygame.display.update()

                # Wait a bit before allowing user to select options.
                if load_delay_ms:
                    pygame.time.wait(load_delay_ms)

                if refresh_during:
                    self.refresh_and_blit_self()
                    # Blit the current menu page.
                    menu_display.blit_menu_page(
                        self._main_display_surface,
                        curr_page,
                        curr_selected_index,
                        horizontal_orientation=horizontal_orientation,
                        vertical_orientation=vertical_orientation,
                        alternative_top_left=alternative_top_left,
                    )
                    pygame.display.update()

                LOGGER.debug("Waiting for user to select a menu option...")
                selected = False
                while not selected:
                    timekeeper.Timekeeper.tick()

                    next_option = False
                    prev_option = False

                    refresh_tick_counter = (refresh_tick_counter + 1) \
                            % timekeeper.REFRESH_INTERVAL_NUM_TICKS
                    reblit_tick_counter = (reblit_tick_counter + 1) \
                                    % timekeeper.OW_REBLIT_INTERVAL_NUM_TICKS

                    if refresh_during \
                            and (refresh_tick_counter == 0):
                        LOGGER.debug("Refreshing while waiting.")
                        self.refresh_and_blit_self()
                        menu_display.blit_menu_page(
                            self._main_display_surface,
                            curr_page,
                            curr_selected_index,
                            horizontal_orientation=horizontal_orientation,
                            vertical_orientation=vertical_orientation,
                            alternative_top_left=alternative_top_left,
                        )
                        pygame.display.update()
                    if reblit_tick_counter == 0:
                        self.blit_self()
                        menu_display.blit_menu_page(
                            self._main_display_surface,
                            curr_page,
                            curr_selected_index,
                            horizontal_orientation=horizontal_orientation,
                            vertical_orientation=vertical_orientation,
                            alternative_top_left=alternative_top_left,
                        )
                        pygame.display.update()

                    for events in pygame.event.get():
                        if events.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit(0)
                        elif events.type == pygame.KEYDOWN:
                            if events.key == pygame.K_DOWN:
                                prev_option = False
                                next_option = True
                            elif events.key == pygame.K_UP:
                                prev_option = True
                                next_option = False
                            elif events.key in viewingdata.MENU_OPTION_EXIT_KEYS:
                                # Exit without selecting option.
                                selected = True
                                done = True
                                ret_option_id = None
                                prev_option = False
                                next_option = False

                                LOGGER.info(
                                    "Leaving menu without selecting option."
                                )
                            elif events.key in viewingdata.MENU_OPTION_SELECT_KEYS:
                                # We selected the current option.
                                selected = True
                                prev_option = False
                                next_option = False
                                curr_option_id = curr_page.get_option_id(
                                    curr_selected_index
                                )

                                LOGGER.info(
                                    "Selecting option %s",
                                    menuoptions.get_option_name(
                                        curr_option_id,
                                        language.Language.current_language_id
                                    )
                                )

                                if curr_option_id \
                                    == menuoptions.MORE_OPTIONS_OPTION_ID:
                                    # Go to next page and don't return.
                                    # Loops through menu if needed.
                                    curr_page_index = \
                                        (curr_page_index + 1) % num_pages
                                    curr_selected_index = 0
                                    LOGGER.info(
                                        "Moving to next menu page."
                                    )
                                elif curr_option_id:
                                    # Selected a valid option.
                                    done = True
                                    ret_option_id = curr_option_id
                                    LOGGER.info(
                                        "Selected option %s",
                                        menuoptions.get_option_name(
                                            ret_option_id,
                                            language.Language.current_language_id
                                        )
                                    )

                    if (not done) \
                            and (not selected) \
                            and (prev_option or next_option):
                        if prev_option:
                            curr_selected_index = (curr_selected_index - 1) \
                                            % num_options
                            LOGGER.info(
                                "Advancing to previous option %s",
                                menuoptions.get_option_name(
                                    curr_page.get_option_id(
                                        curr_selected_index
                                    ),
                                    language.Language.current_language_id
                                )
                            )
                        elif next_option:
                            curr_selected_index = (curr_selected_index + 1) \
                                            % num_options
                            LOGGER.info(
                                "Advancing to next option %s",
                                menuoptions.get_option_name(
                                    curr_page.get_option_id(
                                        curr_selected_index
                                    ),
                                    language.Language.current_language_id
                                )
                            )

                        if refresh_during:
                            self.refresh_and_blit_self()

                        # Reblit menu page with new selected option.
                        menu_display.blit_menu_page(
                            self._main_display_surface,
                            curr_page,
                            curr_selected_index,
                            horizontal_orientation=horizontal_orientation,
                            vertical_orientation=vertical_orientation,
                            alternative_top_left=alternative_top_left,
                        )
                        pygame.display.update()

                        # Delay before allowing user to go to next option.
                        if option_switch_delay_ms:
                            pygame.time.wait(option_switch_delay_ms)

                        if refresh_during:
                            self.refresh_and_blit_self()
                            menu_display.blit_menu_page(
                                self._main_display_surface,
                                curr_page,
                                curr_selected_index,
                                horizontal_orientation=horizontal_orientation,
                                vertical_orientation=vertical_orientation,
                                alternative_top_left=alternative_top_left,
                            )
                            pygame.display.update()

        if refresh_after:
            self.refresh_and_blit_self()
            pygame.display.update()

        return ret_option_id

class OverworldViewing(Viewing):
    """Handles viewing-based methods and functions for the overworld.

    The OverworldViewing class handles overworld-related displays and
    visual interactions, such as the overworld side menu, map scrolling,
    and overworld text boxes.  The class also acts as an interface between
    the Game object and Display-related methods.

    Attributes:
        main_display_surface: the pygame Surface object for the main display
            screen linked to the Viewing object. This Surface object is used
            to blit pixels and changes to the display screen.
        protagonist: the Protagonist object to link to the OverworldViewing
            object. The Protagonist object will determine things like
            what to display in the top health display.
        # TODO
    """

    def __init__(
            self,
            main_display_surface,
            protagonist=None,
            curr_map=None,
            background_pattern=display.PATTERN_1_ID,
        ):
        """Initialize the OverworldViewing object.

        Args:
            main_display_surface: the pygame Surface object for the main
                display screen linked to the Viewing object.
            protagonist: the Protagonist object to link to the OverworldViewing
                object. This object can be set later on.
            curr_map: the Map object for the current map to link to the
                OverworldViewing object. This object can be set later on.
            background_pattern: background pattern ID value to determine
                the background pattern for the displays.
        """

        Viewing.__init__(
            self,
            main_display_surface,
        )

        self._protagonist = protagonist
        self._curr_map = curr_map
        self._background_pattern = background_pattern

        self._top_display = None
        self._bottom_text_display = None
        self._side_menu_display = None
        self._top_health_display = None
        self._bottom_menu_display = None

    @property
    def curr_map(self):
        """Returns the current map object."""

        return self._curr_map

    @curr_map.setter
    def curr_map(self, value):
        """Sets the current map object for the viewing."""

        if value:
            self._curr_map = value

    def _create_top_health_display(self):
        """Initializes the top health display.

        The top health display will display the protagonist's current
        health and max health.

        Requires fonts to be loaded via Display.init_fonts() in
        the display module.
        """

        top_display_font = display.Display.get_font(
            fontinfo.OW_HEALTH_DISPLAY_FONT_ID
        )
        if top_display_font:
            self._top_health_display = display.Text_Display(
                self._main_display_surface,
                viewingdata.OW_TOP_HEALTH_DISPLAY_RECT,
                top_display_font,
                background_pattern=self._background_pattern,
                horizontal_padding=6,
                vertical_padding=6,
            )

            if not self._top_health_display:
                LOGGER.error("Failed to make top health display")
                sys.exit(1)
        else:
            LOGGER.error("Top display font not found.")
            LOGGER.error("Must init fonts through display.Display.init_fonts.")
            sys.exit(1)

    def _create_bottom_text_display(self):
        """Initializes the bottom text display.

        The bottom text display will display various messages and dialogues
        during interactions in the overworld.

        Requires fonts to be loaded via Display.init_fonts() in
        the display module.
        """

        font_obj = display.Display.get_font(
            fontinfo.OW_BOTTOM_TEXT_FONT_ID
        )
        if font_obj:
            self._bottom_text_display = display.Text_Display(
                self._main_display_surface,
                viewingdata.OW_BOTTOM_TEXT_DISPLAY_RECT,
                font_obj,
                continue_icon_image_path=imagepaths.DEFAULT_TEXT_CONTINUE_ICON_PATH,
                background_pattern=self._background_pattern,
                spacing_factor_between_lines=display.TEXT_BOX_LINE_SPACING_FACTOR,
                horizontal_padding=viewingdata.TEXT_DISPLAY_HORIZONTAL_PADDING,
                vertical_padding=viewingdata.TEXT_DISPLAY_VERTICAL_PADDING,
            )
            if not self._bottom_text_display:
                LOGGER.error("Failed to make bottom text display")
                sys.exit(1)
        else:
            LOGGER.error("Bottom text display font not found.")
            LOGGER.error("Must init fonts through display.Display.init_fonts.")
            sys.exit(1)

    def _create_bottom_menu_display(self):
        """Initializes the bottom menu display.

        The bottom menu display will display menu options during interactions
        in the overworld.

        Requires fonts to be loaded via Display.init_fonts() in
        the display module.
        """

        font_obj = display.Display.get_font(
            fontinfo.OW_BOTTOM_MENU_FONT_ID
        )
        if font_obj:
            self._bottom_menu_display = display.MenuDisplay(
                self._main_display_surface,
                viewingdata.OW_BOTTOM_TEXT_DISPLAY_RECT,
                font_obj,
                background_pattern=self._background_pattern,
                horizontal_padding=15,
                vertical_padding=15,
                selection_icon_image_path=imagepaths.DEFAULT_MENU_SELECTION_ICON_PATH,
                spacing_factor_between_lines=display.MENU_LINE_SPACING_FACTOR,
            )
            if not self._bottom_menu_display:
                LOGGER.error("Failed to make bottom menu display")
                sys.exit(1)
        else:
            LOGGER.error("Bottom menu display font not found.")
            LOGGER.error("Must init fonts through display.Display.init_fonts.")
            sys.exit(1)

    def _create_side_menu_display(self):
        """Initializes the side menu display.

        The side menu display will display the overworld side menu options
        for the user to choose from.

        Requires fonts to be loaded via Display.init_fonts() in
        the display module.
        """

        font_obj = display.Display.get_font(
            fontinfo.OW_SIDE_MENU_FONT_ID
        )
        if font_obj:
            self._side_menu_display = display.MenuDisplay(
                self._main_display_surface,
                viewingdata.OW_SIDE_MENU_RECT,
                font_obj,
                background_pattern=self._background_pattern,
                horizontal_padding=viewingdata.OW_SIDE_MENU_HORIZONTAL_PADDING,
                vertical_padding=viewingdata.OW_SIDE_MENU_VERTICAL_PADDING,
                selection_icon_image_path=imagepaths.DEFAULT_MENU_SELECTION_ICON_PATH,
                spacing_factor_between_lines=display.MENU_LINE_SPACING_FACTOR,
            )
            if not self._side_menu_display:
                LOGGER.error("Failed to make side menu display.")
                sys.exit(1)
        else:
            LOGGER.error("Side menu display font not found.")
            LOGGER.error("Must init fonts through display.Display.init_fonts.")
            sys.exit(1)


    def create_displays(self):
        """Initializes the the main displays for the OverworldViewing.

        The method sets the following displays:
            - Top health display
            - Side menu display
            - Bottom text display

        Requires fonts to be loaded via Display.init_fonts() in
        the display module.
        """

        self._create_top_health_display()
        self._create_bottom_text_display()
        self._create_bottom_menu_display()
        self._create_side_menu_display()

    @property
    def protagonist(self):
        """Returns protagonist."""

        return self._protagonist

    @protagonist.setter
    def protagonist(self, value):
        """Sets protagonist for viewing."""
        if value:
            self._protagonist = value

            # Assign protagonist to top display, as well, which should update
            # the top display
            if self._top_display:
                self._top_display.protagonist = value

    def _get_overworld_health_text(self):
        """Returns the health String for the protagonist.

        The String format is "<current health> / <max health>",
        for example "5 / 12". Rounds health down to the nearest integer.

        Returns:
            String representing the current health for the protagonist.
        """

        ret_text = None

        ret_text = ''.join([
            viewingdata.HEALTH_TEXT_PREFIX_INFO.get(
                language.Language.current_language_id,
                ""
            ),
            str(int(self._protagonist.curr_health)),
            ' / ',
            str(int(self._protagonist.max_health)),
        ])

        return ret_text

    # Blits the top health display onto the main display screen.
    # Does not update the main display - caller will have to do that
    def blit_top_health_display(self, font_color=viewingdata.COLOR_BLACK):
        """Blits the top health display using specified font color.

        Caller must update the main pygame display if needed.

        Args:
            font_color: 3-tuple representing the font color for the health
                display text.
        """

        if self._main_display_surface and self._top_health_display:
            self.display_text_display_first_page(
                self._top_health_display,
                self._get_overworld_health_text(),
                font_color=font_color,
                advance_delay_ms=0,
                auto_advance=True,
                refresh_during=False,
                refresh_after=False,
                no_display_update=True,
            )

    # If refresh_after is True, refreshes
    # overworld and blits and updates display
    def display_bottom_text(
            self,
            text,
            font_color=viewingdata.COLOR_BLACK,
            advance_delay_ms=viewingdata.DEFAULT_ADVANCE_DELAY_MS,
            auto_advance=False,
            refresh_during=True,
            refresh_after=True,
        ):
        """Displays text on the bottom text display.

        The amount of text on each line and in a single text box space is
        determined by the TextDisplay object properties.

        By default, the user will have to manually advance through the
        text display sequence to move on to the next chunk of text or to
        finish displaying the text.

        Args:
            text: can either be a String or a list of Strings that
                represent the text to display. If passing in a single String,
                the String will be broken up across several lines depending
                on length and whether or not newline characters appear in the
                string.
                If passing in a list of Strings, each String in the list will
                start on a new line of text, and each individual String may
                take up multiple lines depending on length and whether or not
                the String contains newline characters.
            font_color: can either be a tuple or a list of tuples that
                represent the font color for the text lines. Note that
                each font_color tuple is a 3-tuple that defines the hex
                value of the color, such as (0x23, 0x4A, 0x5F).
                If passing in a single tuple, the entire text will be
                displayed in that color.
                If passing in a list of tuples, the user must also pass in
                a list of Strings for text_to_display, and each list
                must be of the same length.
                List values of font_color are only valid if text_to_display
                is a list of strings, and each index of the list will
                correspond to the next. In other words, each tuple will define
                the color of the corresponding String (the first tuple
                in the font_color list will define the color for the first
                String in text_to-display, etc).
                If text_to_display is a list of strings and font_color
                is a single tuple, then that color will apply to each text
                string in text_to_display.
            advance_delay_ms: number of milliseconds to wait before user
                can exit out of or continue through the text display.
            auto_advance: if True, the text display will finish and exit
                after advance_delay_ms milliseconds without any user
                input or interaction. If False, user must manually continue
                through or exit out of the text display.
            refresh_during: if True, the calling Viewing object will refresh
                itself periodically while waiting for the text display
                to finish up. If False, the calling Viewing object will not
                refresh during the text display.
            refresh_after: if True, the calling Viewing object will refresh
                itself once the TextDisplay object has finished displaying
                the text.
                If False, the calling Viewing object will not
                refresh after the text display.
        """

        if text and self._bottom_text_display:
            self.display_text_display(
                self._bottom_text_display,
                text,
                font_color=font_color,
                advance_delay_ms=advance_delay_ms,
                auto_advance=auto_advance,
                refresh_during=refresh_during,
                refresh_after=refresh_after,
                no_display_update=False,
            )

    # If refresh_after is True, refreshes
    # overworld and blits and updates display
    def display_bottom_text_first_page(
            self,
            text,
            font_color=viewingdata.COLOR_BLACK,
            advance_delay_ms=viewingdata.DEFAULT_ADVANCE_DELAY_MS,
            auto_advance=False,
            refresh_during=True,
            refresh_after=True,
        ):
        """Displays a single page's worth of text on bottom text display.

        The amount of text on each line and in a single text page space is
        determined by the bottom text display's properties.

        Even if the amount of input text is more than the amount that will
        fit on a single text page, the method will display only the first
        page.

        By default, the user will have to manually advance through the
        text display sequence to finish displaying the text.

        Args:
            text: can either be a String or a list of Strings that
                represent the text to display. If passing in a single String,
                the String will be broken up across several lines depending
                on length and whether or not newline characters appear in the
                string.
                If passing in a list of Strings, each String in the list will
                start on a new line of text, and each individual String may
                take up multiple lines depending on length and whether or not
                the String contains newline characters.
            font_color: can either be a tuple or a list of tuples that
                represent the font color for the text lines. Note that
                each font_color tuple is a 3-tuple that defines the hex
                value of the color, such as (0x23, 0x4A, 0x5F).
                If passing in a single tuple, the entire text will be
                displayed in that color.
                If passing in a list of tuples, the user must also pass in
                a list of Strings for text_to_display, and each list
                must be of the same length.
                List values of font_color are only valid if text_to_display
                is a list of strings, and each index of the list will
                correspond to the next. In other words, each tuple will define
                the color of the corresponding String (the first tuple
                in the font_color list will define the color for the first
                String in text_to-display, etc).
                If text_to_display is a list of strings and font_color
                is a single tuple, then that color will apply to each text
                string in text_to_display.
            advance_delay_ms: number of milliseconds to wait before user
                can exit out of or continue through the text display.
            auto_advance: if True, the text display will finish and exit
                after advance_delay_ms milliseconds without any user
                input or interaction. If False, user must manually continue
                through or exit out of the text display.
            refresh_during: if True, the calling Viewing object will refresh
                itself periodically while waiting for the text display
                to finish up. If False, the calling Viewing object will not
                refresh during the text display.
            refresh_after: if True, the calling Viewing object will refresh
                itself once the TextDisplay object has finished displaying
                the text.
                If False, the calling Viewing object will not
                refresh after the text display.
        """

        if text and self._main_display_surface and self._bottom_text_display:
            self.display_text_display_first_page(
                self._bottom_text_display,
                text,
                font_color=font_color,
                advance_delay_ms=advance_delay_ms,
                auto_advance=auto_advance,
                refresh_during=refresh_during,
                refresh_after=refresh_after,
                no_display_update=False,
            )

    def set_and_blit_map_on_view(self, protag_tile_location):
        """Sets the map while keeping the protagonist in the screen center.

        Since the protagonist stays centered in the screen, the method adjusts
        the map accordingly.

        Does not update the pygame display - caller must do that.

        Args:
            protag_tile_location: (x,y) Tile coordinate tuple representing
                the protagonist's location on the map.
        """

        # Set current map's top left position on display screen.
        if self._curr_map and protag_tile_location:
            # Calculate map top left position based on protag location.
            map_top_left = OverworldViewing.get_centered_map_top_left_pixel(
                protag_tile_location
            )

            if map_top_left:
                self._curr_map.top_left_position = map_top_left
            else:
                self._curr_map.top_left_position = viewingdata.OW_VIEWING_TOP_LEFT

            # Refresh and blit viewing.
            self.refresh_and_blit_self()
        else:
            LOGGER.error("Missing parameters for setting and blitting map.")
            sys.exit(1)

    def refresh_protagonist(self):
        """Refreshes the protagonist, such as health and run energy."""

        if self._protagonist:
            self._protagonist.refresh_self()

    def refresh_self(self):
        """Refreshes overworld data, including map, linked protagonist,
        and top display.

        Does not reblit the map or top display - caller must do
        that.
        """

        # Update protagonist.
        self.refresh_protagonist()

        # Update map.
        self.refresh_map()

        # Update top display.
        self.refresh_top_display()

    def blit_map(self):
        """Blits the current map.

        Does not update the map or pygame display.
        """

        if self._curr_map:
            # Set top left viewing tile to define what portions of map to blit
            top_left_viewing_tile_coord =                           \
                OverworldViewing.get_top_left_ow_viewing_tile(
                    self._curr_map.top_left_position
                )

            # Get subset of tiles to blit.
            tile_subset_rect = OverworldViewing.calculate_tile_viewing_rect(
                self._curr_map,
                top_left_viewing_tile_coord
            )

            self._curr_map.blit_map(
                self._main_display_surface,
                tile_subset_rect=tile_subset_rect,
                blit_time_ms=pygame.time.get_ticks(),
            )

    def display_overworld_side_menu(
            self,
            menu_option_ids,
            refresh_after=True,
            refresh_during=True,
            #horizontal_orientation=display.ORIENTATION_LEFT_JUSTIFIED,
            #load_delay_ms=viewingdata.DEFAULT_MENU_LOAD_DELAY_MS,
            #option_switch_delay_ms=viewingdata.DEFAULT_MENU_OPTION_SWITCH_DELAY_MS,
        ):
        """Displays the overworld side menu and returns the selected option.

        The number of menu options visible on each menu page is determined by
        the properties of the overworld side menu.

        In the event where all the options in option_id_list cannot fit on a
        single menu page, each menu page will have an option at
        the end indicating that more options are available. The "more options"
        option on the last page will loop back to the first page of menu
        options to allow for backtracking.

        For best results, each menu option name should not be longer than the
        horizontal space available in the side menu.

        Args:
            menu_option_ids: list of menu option ID values for the menu display
                object to display. The option ID values will be translated
                into their corresponding names depending on the
                current game language.
            refresh_during: if True, the calling Viewing object will refresh
                itself periodically while waiting for the text display
                to finish up. If False, the calling Viewing object will not
                refresh during the text display.
            refresh_after: if True, the calling Viewing object will refresh
                itself and update the pygame display after the user finishes
                interacting with the menu.

        Returns:
            option ID value for the selected option. None if no option was
            selected (e.g. if the user exits the menu via an escape key).
        """

        ret_option_id = None
        if menu_option_ids:
            ret_option_id = self.display_menu_display(
                self._side_menu_display,
                menu_option_ids,
                horizontal_orientation=display.ORIENTATION_LEFT_JUSTIFIED,
                #vertical_orientation=display.ORIENTATION_TOP_JUSTIFIED,
                vertical_orientation=display.ORIENTATION_CENTERED,
                load_delay_ms=viewingdata.DEFAULT_MENU_LOAD_DELAY_MS,
                option_switch_delay_ms=viewingdata.DEFAULT_MENU_OPTION_SWITCH_DELAY_MS,
                refresh_after=refresh_after,
                refresh_during=refresh_during,
            )

        return ret_option_id

    def display_overworld_bottom_menu(
            self,
            menu_option_ids,
            refresh_after=True,
            refresh_during=True,
        ):
        """Displays the overworld bottom menu and returns the selected option.

        The number of menu options visible on each menu page is determined by
        the properties of the overworld bottom menu.

        In the event where all the options in option_id_list cannot fit on a
        single menu page, each menu page will have an option at
        the end indicating that more options are available. The "more options"
        option on the last page will loop back to the first page of menu
        options to allow for backtracking.

        For best results, each menu option name should not be longer than the
        horizontal space available in the bottom menu.

        Args:
            menu_option_ids: list of menu option ID values for the menu display
                object to display. The option ID values will be translated
                into their corresponding names depending on the
                current game language.
            refresh_during: if True, the calling Viewing object will refresh
                itself periodically while waiting for the text display
                to finish up. If False, the calling Viewing object will not
                refresh during the text display.
            refresh_after: if True, the calling Viewing object will refresh
                itself and update the pygame display after the user finishes
                interacting with the menu.

        Returns:
            option ID value for the selected option. None if no option was
            selected (e.g. if the user exits the menu via an escape key).
        """

        ret_option_id = None
        if menu_option_ids:
            ret_option_id = self.display_menu_display(
                self._bottom_menu_display,
                menu_option_ids,
                horizontal_orientation=display.ORIENTATION_CENTERED,
                vertical_orientation=display.ORIENTATION_CENTERED,
                load_delay_ms=viewingdata.DEFAULT_MENU_LOAD_DELAY_MS,
                option_switch_delay_ms=viewingdata.DEFAULT_MENU_OPTION_SWITCH_DELAY_MS,
                refresh_after=refresh_after,
                refresh_during=refresh_during,
            )

        return ret_option_id

    def blit_self(self):
        """Blits overworld viewing as is, without updating.

        Does not update the pygame display.
        Caller must update display if needed.
        """

        # Blit background.
        self.blit_background()

        # Blit map and top display.
        self.blit_map()

        self.blit_top_health_display()

    def refresh_top_display(self):
        """Refreshes top display.

        Does not update the pygame display.
        Caller must update display if needed.
        """

        if self._top_display:
            self._top_display.update_self()

    def refresh_and_blit_top_display(self):
        """Refreshes and blits top display.

        Does not update the pygame display.
        Caller must update display if needed.
        """

        if self._top_display:
            self.refresh_top_display()
            self.blit_top_health_display()

    def refresh_map(self):
        """Refreshes the current map.

        Does not update the pygame display.
        Caller must update display if needed.
        """

        if self._curr_map:
            # Refresh map to update it.
            self._curr_map.refresh_self()

    def refresh_and_blit_map(self):
        """Refreshes and blits the current map.

        Does not update the pygame display.
        Caller must update display if needed.
        """

        self.refresh_map()
        self.blit_map()

    # scroll map one Tile distance in the indicated direction.
    # updates main display with each new viewpoint
    # scroll_wait_time is the time (in milliseconds)
    def scroll_map_single_tile(
            self,
            scroll_direction,
            char_move_direction,
            run=False,
        ):
        """Scrolls the map while walking the main character.

        Note that the character should walk in the opposite direction of the
        map scrolling, so for best results, ensure that scroll_direction
        and char_move_direction are opposite directions.

        Args:
            scroll_direction: direction ID that indicates in which direction
                the map should scroll.
            char_move_direction: direction ID that indicates in which direction
                the character should walk.
            run: if True, have the character run. If False, have the character
                walk.
        """

        # Get top left viewing tile and tile subset rect to blit.
        tile_subset_rect = OverworldViewing.calculate_tile_viewing_rect(
            self._curr_map,
            OverworldViewing.get_top_left_ow_viewing_tile(
                self._curr_map.top_left_position
            )
        )

        LOGGER.debug(
            "Tile subset viewing rect for map at %s",
            tile_subset_rect
        )

        # Get image ID list for the walk animation in this direction.
        walk_image_ids = imageids.get_entity_walk_image_ids(
            char_move_direction
        )

        # Get wait time in between pixel movements.
        wait_time = None

        if run:
            wait_time = int(RUN_SINGLE_TILE_SCROLL_TIME_MS / tile.TILE_SIZE)
        else:
            wait_time = int(WALK_SINGLE_TILE_SCROLL_TIME_MS / tile.TILE_SIZE)

        if walk_image_ids:
            # Number of steps in the walk animation.
            phase_duration = int(tile.TILE_SIZE / len(walk_image_ids))

            for i in range(tile.TILE_SIZE):
                # Reset the surface screen to default to black for empty map
                # spaces.
                self.blit_background(fill_color=viewingdata.COLOR_BLACK)

                if self._protagonist:
                    # Get image ID for protagonist.
                    image_type_id = walk_image_ids[int(i / phase_duration)]

                    if image_type_id:
                        self._protagonist.curr_image_id = image_type_id

                    # scroll 1 pixel at a time
                    self._curr_map.scroll(
                        self._main_display_surface,
                        scroll_direction,
                        1,
                        tile_subset_rect=tile_subset_rect
                    )

                    # Also blit the top view on top.
                    self.blit_top_health_display()

                    # Update main display
                    pygame.display.update()

                    # Wait till next iteration
                    pygame.time.wait(wait_time)

    def blit_background(self, fill_color=viewingdata.COLOR_BLACK):
        """Fills in the viewing background for the overworld.

        Does not update the pygame display.
        Caller must update display if needed.

        Args:
            fill_color: 3-tuple that defines the color to fil in the
                overworld viewing background. For example,
                (0, 0, 0).
        """

        self._main_display_surface.fill(fill_color)

    @classmethod
    def get_top_left_ow_viewing_tile(cls, map_top_left_pixel_pos):
        """Calculates the tile coordinates for the top left Tile in viewing.

        Given the top left pixel position of the map, the method will
        determine which Tile coordinate represents the top left Tile in the
        viewing window.

        Args:
            map_top_left_pixel_pos: (x,y) pixel coordinate tuple for the
                map's top left pixel position in the viewing.

        Returns:
            (x,y) tile coordinate tuple for the Tile in the top left viewing
            position.
        """

        ret_coord = None
        if map_top_left_pixel_pos:
            coord_x = 0
            coord_y = 0
            if map_top_left_pixel_pos[0] < 0:
                # Map top left is behind the left side of viewing.
                coord_x = -1 * int(map_top_left_pixel_pos[0] / tile.TILE_SIZE)
            if map_top_left_pixel_pos[1] < 0:
                # Map top left is above top of overworld viewing.
                coord_y = -1 * int(
                    (map_top_left_pixel_pos[1] \
                    - viewingdata.OW_TOP_DISPLAY_HEIGHT) \
                    / tile.TILE_SIZE
                )

            ret_coord = (coord_x, coord_y)
            LOGGER.debug(
                "Top left ow viewing tile: %s, map top left %s",
                ret_coord,
                map_top_left_pixel_pos,
            )

        return ret_coord

    @classmethod
    def get_centered_map_top_left_pixel(cls, protag_tile_coordinate):
        """Returns the top left pixel display coordinate for the map.

        The top left coordinate for the current map viewing depends on
        the protagonist's location on the map, as the screen will stay
        centered on the protagonist.

        Args:
            protag_tile_coordinate: tile coordinate for the protagonist's
                current location on the current map.

        Returns:
            2-tuple representing the x,y pixel coordinates for the top
            left corner of the map display in the current viewing.
        """

        top_left = (0, 0)
        if protag_tile_coordinate:
            pixel_distance_horiz = viewingdata.CENTER_OW_TILE_TOP_LEFT[0] \
                - (protag_tile_coordinate[0] * tile.TILE_SIZE)
            pixel_distance_vert = viewingdata.CENTER_OW_TILE_TOP_LEFT[1] \
                - (protag_tile_coordinate[1] * tile.TILE_SIZE)

            top_left = (pixel_distance_horiz, pixel_distance_vert)


        return top_left

    @classmethod
    def calculate_tile_viewing_rect(cls, map_object, top_left_viewing_tile_coord):
        """Returns a 4-tuple representing the viewable rectangular tile grid.

        The 4-tuple is of the form (top left tile x, top left tile y,
        num horizontal tiles, num vertical tiles), where
        "top left tile x" is the top left tile x coordinate for the top left
        Tile that is defined as viewable, "top left tile y" is the top left
        tile y coordinate for the top left Tile that is defined as viewable,
        "num horizontal tiles" is the number of columns in the viewable
        Tile grid, and "num vertical tiles" is the number of rows in the
        viewable Tile grid. The viewable Tile grid is defined as all Tiles
        in the current viewing window with at most a 2-Tile-wide padding
        due to Tiles that appear when scrolling the map.

        Args:
            map_object: Map object that defines the Tile grid.
            top_left_viewing_tile_coord: the x,y tile coordinates of the top left
                Tile in the current viewing window.
        """

        ret_rect = None

        if map_object and top_left_viewing_tile_coord:
            # see if we can get the Tile padding to the left of the screen
            # and Tile padding above above the screen
            start_tile_x = max(
                0,
                top_left_viewing_tile_coord[0] - VIEWING_TILE_PADDING,
            )
            start_tile_y = max(
                0,
                top_left_viewing_tile_coord[1] - VIEWING_TILE_PADDING,
            )

            end_tile_x = start_tile_x
            end_tile_y = start_tile_y

            # get the map right edge and bottom edge
            map_right_edge = map_object.top_left_position[0] \
                            + (map_object.width * tile.TILE_SIZE)
            map_bottom_edge = map_object.top_left_position[1] \
                            + (map_object.height * tile.TILE_SIZE)

            if map_right_edge > viewingdata.MAIN_DISPLAY_WIDTH:
                # map right edge is past the main display right edge
                end_tile_x = min(
                    map_object.width \
                    - 1 \
                    - int(
                        (map_right_edge - viewingdata.MAIN_DISPLAY_WIDTH) \
                        / tile.TILE_SIZE
                    ) \
                    + VIEWING_TILE_PADDING,
                    map_object.width - 1
                )
            else:
                end_tile_x = map_object.width - 1

            if map_bottom_edge > viewingdata.MAIN_DISPLAY_HEIGHT:
                # map bottom edge is past the main display bottom edge
                end_tile_y = min(
                    map_object.height \
                    - 1 \
                    - int(
                        (map_bottom_edge - viewingdata.MAIN_DISPLAY_HEIGHT) \
                        / tile.TILE_SIZE
                    ) \
                    + VIEWING_TILE_PADDING,
                    map_object.height - 1
                )
            else:
                end_tile_y = map_object.height - 1

            ret_rect = (
                start_tile_x,
                start_tile_y,
                end_tile_x - start_tile_x + 1,
                end_tile_y - start_tile_y + 1
            )

        return ret_rect

    @classmethod
    def create_overworld_viewing(
            cls,
            main_display_surface,
            protagonist=None,
            curr_map=None,
        ):
        """Factory method for an OverworldViewing object.

        Use this method instead of the OverworldViewing init method.

        Args:
            main_display_surface: pygame Surface object for the display
                screen.
            protagonist: optional argument that defines the protagonist
                object to link to the OverworldViewing object.
                A Protagonist object can always be linked to the
                OverworldViewing object after the fact.
            curr_map: optional argument that defines the current Map object
                to link to the OverworldViewing object. Map objects can
                be linked to the OverworldViewing object after the
                fact, and will actually need to be adjusted due to
                changing maps throughout gameplay.

            Returns:
                OverworldViewing object with the specified properties.
        """

        ret_viewing = None

        if main_display_surface:
            ret_viewing = OverworldViewing(
                main_display_surface,
                protagonist=protagonist,
                curr_map=curr_map,
            )

            # Create displays for viewing.
            ret_viewing.create_displays()

        return ret_viewing

# Set up logger.
logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)
