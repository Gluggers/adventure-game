# -*- coding: utf-8 -*-
"""This module contains classes and methods for SpellSelectionViewing objects.

SpellSelectionViewing objects handle Displays and user interactions for
the spell selection viewing, where users can view spell information and cast
spells.
"""

import logging
import sys
import pygame
import display
import fontinfo
import imagepaths
import language
import menuoptions
import selectionviewing
import spells
import timekeeper
import viewing
import viewingdata

class SpellSelectionViewing(selectionviewing.SelectionGridViewing):
    def __init__(
            self,
            main_display_surface,
            spell_icon_dimensions,
            display_pattern=display.PATTERN_2_ID,
            enlarged_selection_background_path=imagepaths.ITEM_LISTING_SELECTED_ENLARGED_BACKGROUND_PATH,
        ):
        selectionviewing.SelectionGridViewing.__init__(
            self,
            main_display_surface,
            spell_icon_dimensions,
            display_pattern=display_pattern,
            enlarged_selection_background_path=enlarged_selection_background_path,
        )

    def create_additional_selection_displays(self):
        pass

    def blit_selected_object_name(self, selected_obj):
        if selected_obj:
            # Blit object name.
            obj_name = selected_obj.get_name()
            self.display_text_display_first_page(
                self.selection_name_display,
                obj_name,
                advance_delay_ms=0,
                auto_advance=True,
                refresh_during=False,
                refresh_after=False,
                horizontal_orientation=display.ORIENTATION_CENTERED,
                vertical_orientation=display.ORIENTATION_TOP_JUSTIFIED,
                alternative_top_left=None,
                no_display_update=True,
            )

    def blit_selected_object_enlarged_icon(self, selected_obj):
        if selected_obj:
            # Blit enlarged icon and background.
            enlarged_icon = selected_obj.enlarged_icon
            if enlarged_icon:
                if self.enlarged_selection_background:
                    enlarged_background_rect = \
                        self.enlarged_selection_background.get_rect(
                            center=self.icon_enlarged_rect.center
                        )
                    self.main_display_surface.blit(
                        self.enlarged_selection_background,
                        enlarged_background_rect
                    )

                enlarged_icon_rect = enlarged_icon.get_rect(
                    center=self.icon_enlarged_rect.center
                )
                self.main_display_surface.blit(
                    enlarged_icon,
                    enlarged_icon_rect,
                )

    def blit_selection_info_text(
            self,
            selected_obj,
            reference_entity=None,
        ):
        # Blit spell description and info.
        # Also include required objects.
        if selected_obj:
            spell_info = selected_obj.get_info_text()
            self.display_text_display_first_page(
                self.selection_description_display,
                spell_info,
                advance_delay_ms=0,
                auto_advance=True,
                refresh_during=False,
                refresh_after=False,
                horizontal_orientation=display.ORIENTATION_LEFT_JUSTIFIED,
                vertical_orientation=display.ORIENTATION_TOP_JUSTIFIED,
                alternative_top_left=None,
                no_display_update=True,
            )

    def blit_selected_object_subtitle(self, selected_obj):
        if selected_obj:
            # Blit subtitle.
            subtitle_text = selected_obj.get_subtitle_text()

            font_color_to_use = None

            if self.protagonist \
                and self.protagonist.has_level_for_spell(selected_obj):
                font_color_to_use = viewingdata.COLOR_BLACK
            else:
                font_color_to_use = viewingdata.COLOR_RED_REJECT

            self.display_text_display_first_page(
                self.selection_subtitle_display,
                subtitle_text,
                advance_delay_ms=0,
                auto_advance=True,
                refresh_during=False,
                refresh_after=False,
                font_color=font_color_to_use,
                horizontal_orientation=display.ORIENTATION_CENTERED,
                vertical_orientation=display.ORIENTATION_TOP_JUSTIFIED,
                alternative_top_left=None,
                no_display_update=True,
            )

    # Overridden.
    def blit_main_selection_info(
            self,
            selection_info,
            reference_entity=None,
        ):
        self.selection_details_side_display.blit_background(
            self.main_display_surface
        )
        spell_obj = spells.Spell.get_spell(selection_info)
        self.blit_selected_object_name(spell_obj)
        self.blit_selected_object_subtitle(spell_obj)
        self.blit_selected_object_enlarged_icon(spell_obj)

    # Overridden.
    def blit_selection_details(
            self,
            selection_info,
            reference_entity=None,
        ):
        spell_obj = spells.Spell.get_spell(selection_info)

        self.blit_main_selection_info(
            selection_info,
            reference_entity=reference_entity,
        )
        self.blit_selection_info_text(
            spell_obj,
            reference_entity=reference_entity,
        )

    # Overridden.
    def get_selection_options(
            self,
            selection_info,
            allowed_selection_option_set=None,
            reference_entity=None,
        ):
        selection_options = []
        selection_obj = None
        option_list = []

        if selection_info:
            selection_obj = spells.Spell.get_spell(selection_info)

        if selection_obj and selection_obj.menu_option_ids:
            for option_id in selection_obj.menu_option_ids:
                option_list.append(option_id)
            option_list.append(menuoptions.CANCEL_OPTION_ID)

        for option in option_list:
            if allowed_selection_option_set \
                and option in allowed_selection_option_set:
                if option == menuoptions.CAST_SPELL_OPTION_ID:
                    if self.protagonist and \
                        self.protagonist.has_level_for_spell(selection_obj):
                        selection_options.append(option)
                else:
                    selection_options.append(option)

        LOGGER.info("Selection options: %s", selection_options)
        return selection_options

    # Overridden. selection_data_list is list of spell IDs.
    def convert_to_icon_data(
            self,
            selection_data_list,
            reference_entity=None,
        ):
        ret_data = None

        if selection_data_list:
            ret_data = []

            for spell_id in selection_data_list:
                spell_object = spells.Spell.get_spell(spell_id)
                curr_image = None
                level_text = None

                if spell_object:
                    curr_image = spell_object.icon

                    rendered_supertext = None
                    level_text = str(spell_object.required_level)

                if level_text:
                    if self.protagonist \
                        and self.protagonist.has_level_for_spell(spell_object):
                        rendered_supertext = \
                            self.icon_supertext_font_object.render(
                                level_text,
                                False,
                                viewingdata.COLOR_WHITE,
                            )
                    else:
                        rendered_supertext = \
                            self.icon_supertext_font_object.render(
                                level_text,
                                False,
                                viewingdata.COLOR_RED_REJECT,
                            )

                ret_data.append([curr_image, rendered_supertext])

        return ret_data

    @classmethod
    def create_spell_selection_viewing(
            cls,
            main_display_surface,
            spell_icon_dimensions,
            display_pattern=display.PATTERN_2_ID,
        ):
        ret_viewing = None

        if main_display_surface:
            ret_viewing = SpellSelectionViewing(
                main_display_surface,
                spell_icon_dimensions,
                display_pattern=display_pattern,
            )

            # Create displays for viewing.
            ret_viewing.create_base_displays()
            ret_viewing.create_selection_detail_displays()
            ret_viewing.create_additional_selection_displays()

        return ret_viewing

# Set up logger.
logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)
