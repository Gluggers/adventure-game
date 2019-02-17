import pygame
import interactiondata
import interactiveobj
import resource
import entity
import language
import display
import timekeeper
import random
import skills
import sys
import logging

GATHERING_START_DELAY_MS = 500
GATHERING_EXHAUST_DELAY_MS = 1500
NUM_MS_SECOND = 1000

DEFAULT_INTERACTION_MESSAGE_INFO = {
    language.LANG_ENGLISH: "Default interaction with {0}.",
    language.LANG_ESPANOL: "Interaccion por defecto con {0}."
}

INVENTORY_FULL_MESSAGE_INFO = {
    language.LANG_ENGLISH: "You can't hold any more items.",
    language.LANG_ESPANOL: "No puedes guardar mas cosas."
}

NOT_HIGH_ENOUGH_LEVEL_MESSAGE_INFO = {
    language.LANG_ENGLISH: "You need a level of {0} in {1}.",
    language.LANG_ESPANOL: "Se necesita un nivel de {0} de {1}."
}

# Number of milliseconds in a gathering skilling interval.
GATHERING_INTERVAL_MS = 1000
GATHERING_INTERVAL_NUM_TICKS = int(
        timekeeper.CLOCK_TICK * (GATHERING_INTERVAL_MS / NUM_MS_SECOND)
    )

# Number of milliseconds between switching character gathering image IDs.
GATHERING_IMAGE_INTERVAL_MS = int(NUM_MS_SECOND / 4)
GATHERING_IMAGE_INTERVAL_NUM_TICKS = int(
        timekeeper.CLOCK_TICK * (GATHERING_IMAGE_INTERVAL_MS / NUM_MS_SECOND)
    )

# Number of game ticks to hold the resource gather message.
NUM_TICK_HOLD_RESOURCE_GATHER_MESSAGE = int(timekeeper.CLOCK_TICK * 2)

SKILLING_EXIT_KEYS = set([
    pygame.K_BACKSPACE,
    pygame.K_ESCAPE,
    pygame.K_RIGHT,
    pygame.K_DOWN,
    pygame.K_LEFT,
    pygame.K_UP,
])

class Interaction():
    # Maps interaction IDs to methods
    interaction_mapping = {}

    @classmethod
    def default_interaction(
                cls,
                interaction_id,
                game_object,
                acting_object,
                target_object
            ):
        if game_object and acting_object and target_object:
            display_text = DEFAULT_INTERACTION_MESSAGE_INFO.get(
                    game_object.game_language,
                    ""
                ).format(target_object.get_name(game_object.game_language))

            game_object.display_bottom_text(
                display_text,
                refresh_after=True,
            )

    @classmethod
    def meets_resource_level(
                cls,
                acting_object,
                target_object
            ):
        meets_level = False

        if acting_object and target_object:
            # Check we have the required level.
            skill_id = target_object.related_skill_id
            required_level = target_object.required_level

            if acting_object.get_skill_level(skill_id) >= required_level:
                meets_level = True

        return meets_level

    @classmethod
    def display_inventory_full_message(cls, game_object):
        if game_object:
            game_object.display_bottom_text(
                INVENTORY_FULL_MESSAGE_INFO.get(
                    game_object.game_language,
                    ""
                ),
                auto_advance=False,
                advance_delay_ms=display.DEFAULT_ADVANCE_DELAY_MS,
                refresh_after=True,
            )

    # Main skilling text must be 1 page or less.
    @classmethod
    def gathering_interaction(
                cls,
                interaction_id,
                game_object,
                acting_object,
                target_object,
                main_skilling_text,
                resource_gather_text=None,
                resource_exhaust_text=None,
                intro_skilling_text=None,
            ):
        if game_object \
                and game_object.viewing \
                and acting_object \
                and target_object   \
                and (interaction_id is not None)    \
                and main_skilling_text:
            # Check if inventory is full and if we have the right level
            # and equipment. TODO equipment check.
            if acting_object.inventory_full():
                # Inventory is full.
                cls.display_inventory_full_message()
            elif not Interaction.meets_resource_level(
                        acting_object,
                        target_object
                    ):
                # Don't have a high enough level.
                required_level = target_object.required_level
                skill_name = skills.get_skill_name(
                    target_object.related_skill_id,
                    game_object.game_language
                )

                reject_message = NOT_HIGH_ENOUGH_LEVEL_MESSAGE_INFO.get(
                        game_object.game_language,
                        ""
                    ).format(required_level, skill_name)

                game_object.display_bottom_text(
                    reject_message,
                    auto_advance=False,
                    advance_delay_ms=display.DEFAULT_ADVANCE_DELAY_MS,
                    refresh_after=True,
                )
            # TODO equipment check
            else:
                # Display intro skilling text if needed.
                if intro_skilling_text:
                    game_object.display_bottom_text(
                        intro_skilling_text,
                        auto_advance=False,
                        advance_delay_ms=display.DEFAULT_ADVANCE_DELAY_MS,
                        refresh_after=True,
                    )

                # Display main skilling text. Pause before we start skilling.
                game_object.display_bottom_first_text_page(
                    main_skilling_text,
                    auto_advance=True,
                    advance_delay_ms=GATHERING_START_DELAY_MS,
                    refresh_after=False,
                )

                logger.info("Beginning gathering.")

                # Start skilling.
                skilling = True
                num_skill_ticks = 0
                image_id_index = 0
                pygame.event.clear()
                curr_display_text = main_skilling_text
                countdown_resource_message = 0
                prev_overworld_image_id = acting_object.curr_image_id

                while skilling:
                    timekeeper.Timekeeper.tick()

                    num_skill_ticks = num_skill_ticks + 1

                    if countdown_resource_message <= 0:
                        curr_display_text = main_skilling_text

                    # TODO set next character image ID for skilling.
                    if num_skill_ticks % GATHERING_IMAGE_INTERVAL_NUM_TICKS == 0:
                        logger.debug("Switch image IDs here.")

                    # Refresh and reblit overworld and gathering message.
                    game_object.refresh_and_blit_overworld()

                    # This will update display for us.
                    game_object.display_bottom_first_text_page(
                        curr_display_text,
                        auto_advance=True,
                        advance_delay_ms=0,
                        refresh_after=False,
                    )

                    # Check if user is ending early by pressing a valid key.
                    exit_key_pressed = False
                    for events in pygame.event.get():
                        if events.type == pygame.QUIT:
                            logger.info("Quitting.")
                            pygame.quit()
                            sys.exit(0)
                        elif events.type == pygame.KEYDOWN:
                            if events.key in SKILLING_EXIT_KEYS:
                                logger.info("Quitting gathering early.")
                                exit_key_pressed = True

                    if exit_key_pressed:
                        skilling = False
                    # Chance to generate a resource after every gathering
                    # interval.
                    elif (num_skill_ticks % GATHERING_INTERVAL_NUM_TICKS) == 0:
                            # Check if we have generated a resource.
                            # (for now, just use strict probability. later,
                            # implement function that determines generation based on
                            # resource required level and character level and
                            # character equipment)
                            if random.randint(0,4) == 0:
                                # We generated a resource.

                                logger.info("Gathered resource!")

                                # TODO handle all the item stuff here.

                                # TODO handle experience stuff here.
                                    # Check if level up.
                                    # If level up:
                                        # skilling = False.
                                        # Handle level up.
                                        # refresh and blit overworld viewing
                                        # update display

                                # Display the resource gather message.
                                if resource_gather_text:
                                    curr_display_text = resource_gather_text
                                    countdown_resource_message = NUM_TICK_HOLD_RESOURCE_GATHER_MESSAGE

                                    game_object.display_bottom_first_text_page(
                                        resource_gather_text,
                                        auto_advance=False,
                                        refresh_after=True,
                                    )

                                # Check if resource has been exhausted.
                                if random.randint(0, 100) < int(100*target_object.exhaustion_probability):
                                    # Resource has been exhausted.
                                    skilling = False
                                    logger.info("Resource exhausted.")

                                    # TODO update map

                                    # TODO - unset and set objects.
                                    # remove object from map, place in exhausted version
                                    # and set respawn timer

                                    # Display exhaust message.
                                    game_object.display_bottom_first_text_page(
                                        resource_exhaust_text,
                                        auto_advance=False,
                                        advance_delay_ms=GATHERING_EXHAUST_DELAY_MS,
                                        refresh_after=True,
                                    )
                                elif acting_object.inventory_full():
                                    # Inventory is full.
                                    skilling = False
                                    cls.display_inventory_full_message()

                    countdown_resource_message = countdown_resource_message - 1

        pygame.event.clear()

        # Update overworld and display.
        game_object.refresh_and_blit_overworld()
        pygame.display.update()

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
            obj_name = target_object.get_name(game_object.game_language)
            resource_exp = target_object.gained_xp

            main_skilling_text = interactiondata.GATHERING_MAIN_MESSAGES.get(
                    interaction_id,
                    {}
                ).get(
                    game_object.game_language,
                    ""
                ).format(obj_name)

            resource_exhaust_text = interactiondata.GATHERING_RESOURCE_EXHAUST_MESSAGES.get(
                    interaction_id,
                    {}
                ).get(
                    game_object.game_language,
                    ""
                ).format(obj_name)

            resource_gain_text = interactiondata.GATHERING_RESOURCE_GAIN_MESSAGES.get(
                    interaction_id,
                    {}
                ).get(
                    game_object.game_language,
                    ""
                ).format("Item Name", resource_exp)

            cls.gathering_interaction(
                interaction_id,
                game_object,
                acting_object,
                target_object,
                main_skilling_text,
                resource_gather_text=resource_gain_text,
                resource_exhaust_text=resource_exhaust_text,
            )

            """
            game_object.display_bottom_text(
                display_text,
                refresh_after=True,
            )
            """

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
            logger.info("Place herb gather interaction here.")

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

# set up logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
