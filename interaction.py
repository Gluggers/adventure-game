import pygame
import interactiondata
import interactiveobj
import resource
import entity
import language
import display

class Interaction():
    # Maps interaction IDs to methods
    interaction_mapping = {}

    @classmethod
    def default_interaction(cls, game_object, acting_object, target_object):
        if game_object and acting_object and target_object:
            display_text = ""
            if game_object.game_language == language.LANG_ENGLISH:
                display_text = "Default interaction with {0}".format(
                    target_object.name
                )
            elif game_object.game_language == language.LANG_ESPANOL:
                display_text = "Interaccion por defecto con {0}".format(
                    target_object.name
                )

            game_object.display_bottom_text_and_refresh(display_text)

    # Main skilling text must be 1 page or less.
    @classmethod
    def gathering_interaction(
                cls,
                game_object,
                acting_object,
                target_object,
                interaction_id,
                main_skilling_text,
                resource_exhaust_text=None,
                intro_skilling_text=None,
            ):
        if game_object \
                and game_object.viewing \
                and acting_object \
                and target_object   \
                and (interaction_id is not None)    \
                and main_skilling_text:
            if intro_skilling_text:
                game_object.viewing.display_text(intro_skilling_text, )

    # TODO - pass in interaction ID?
    @classmethod
    def chop_tree_interaction(
                cls,
                interaction_id,
                game_object,
                acting_object,
                target_object,
            ):
        if game_object and acting_object and target_object:
            # TODO - language functionality
            display_text = ""
            obj_name = target_object.get_name(game_object.game_language)

            if game_object.game_language == language.LANG_ENGLISH:
                display_text = "Attempting to chop down {0}".format(
                    obj_name
                )
            elif game_object.game_language == language.LANG_ESPANOL:
                display_text = "Tratando de cortar el/la {0}".format(
                    obj_name
                )

            game_object.display_bottom_text_and_refresh(display_text)

            # TODO - chopping tree logic

    @classmethod
    def mine_rock_interaction(
                cls,
                interaction_id,
                game_object,
                acting_object,
                target_object,
            ):
        if game_object and acting_object and target_object:
            pass

    @classmethod
    def fishing_interaction(
                cls,
                interaction_id,
                game_object,
                acting_object,
                target_object,
            ):
        if game_object and acting_object and target_object:
            pass

    @classmethod
    def cooking_interaction(
                cls,
                interaction_id,
                game_object,
                acting_object,
                target_object,
            ):
        if game_object and acting_object and target_object:
            pass

    @classmethod
    def herblore_gather_interaction(
                cls,
                interaction_id,
                game_object,
                acting_object,
                target_object,
            ):
        if game_object and acting_object and target_object:
            pass

    @classmethod
    def get_interaction_method(cls, interaction_id):
        ret_method = Interaction.default_interaction
        if interaction_id is not None:
            ret_method = Interaction.interaction_mapping.get(
                interaction_id,
                Interaction.default_interaction
            )
        return ret_method

    @classmethod
    def init_interactions(cls):
        for interaction_id, method in ID_TO_METHOD_MAPPING.items():
            Interaction.interaction_mapping[interaction_id] = method

### MAP INTERACTION IDS TO METHODS ###
ID_TO_METHOD_MAPPING = {
    interactiondata.DEFAULT_ID: Interaction.default_interaction,
    interactiondata.CHOP_TREE_ID: Interaction.chop_tree_interaction,
    interactiondata.MINE_ROCK_ID: Interaction.mine_rock_interaction,
    interactiondata.FISHING_ID: Interaction.fishing_interaction,
    interactiondata.COOKING_ID: Interaction.cooking_interaction,
    interactiondata.HERBLORE_GATHER_ID: Interaction.herblore_gather_interaction,
}
