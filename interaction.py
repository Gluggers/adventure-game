import pygame
import interactiondata
import resource
import entity
import language
import display
import timekeeper
import random
import skills
import viewingdata
import sys
import items
import itemdata
import logging
import objdata

GATHERING_START_DELAY_MS = 500
GATHERING_EXHAUST_DELAY_MS = 1000
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
            target_object,
            acting_object_loc,
            target_object_loc,
        ):
        if game_object and acting_object and target_object:
            display_text = DEFAULT_INTERACTION_MESSAGE_INFO.get(
                    language.Language.current_language_id,
                    ""
                ).format(
                    target_object.get_name()
                )

            game_object.display_overworld_bottom_text(
                display_text,
                refresh_after=True,
            )

    @classmethod
    def meets_resource_level(
            cls,
            acting_object,
            target_object,
        ):
        """Returns True if the acting object has a high enough level to interact
        with the target object, False otherwise.

        Args:
            acting_object: the object trying to interact with the target_object
                resource.
            target_object: the object being interacted with, typically a
                resource object.
        """

        meets_level = False

        if acting_object and target_object:
            # Check we have the required level.
            skill_id = target_object.related_skill_id
            min_required_level = target_object.min_required_level

            if acting_object.get_skill_level(skill_id) >= min_required_level:
                meets_level = True

        return meets_level

    @classmethod
    def display_inventory_full_message(cls, game_object):
        """Displays message indicating that the inventory is full."""

        if game_object:
            game_object.display_overworld_bottom_text(
                INVENTORY_FULL_MESSAGE_INFO.get(
                    language.Language.current_language_id,
                    ""
                ),
                auto_advance=False,
                advance_delay_ms=viewingdata.DEFAULT_ADVANCE_DELAY_MS,
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
            acting_object_loc,
            target_object_loc,
            main_skilling_text,
            skill_id,
            resource_exhaust_text=None,
            intro_skilling_text=None,
        ):
        if game_object \
                and game_object.overworld_viewing \
                and acting_object \
                and target_object   \
                and acting_object_loc   \
                and target_object_loc   \
                and (interaction_id is not None)    \
                and main_skilling_text  \
                and (skill_id is not None):
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
                min_required_level = target_object.min_required_level
                skill_name = skills.get_skill_name(
                    target_object.related_skill_id,
                    language.Language.current_language_id
                )

                reject_message = NOT_HIGH_ENOUGH_LEVEL_MESSAGE_INFO.get(
                    language.Language.current_language_id,
                    ""
                ).format(min_required_level, skill_name)

                game_object.display_overworld_bottom_text(
                    reject_message,
                    auto_advance=False,
                    advance_delay_ms=viewingdata.DEFAULT_ADVANCE_DELAY_MS,
                    refresh_after=True,
                    refresh_during=True,
                )
            # TODO equipment check
            else:
                # Display intro skilling text if needed.
                if intro_skilling_text:
                    game_object.display_overworld_bottom_text(
                        intro_skilling_text,
                        auto_advance=False,
                        advance_delay_ms=viewingdata.DEFAULT_ADVANCE_DELAY_MS,
                        refresh_after=True,
                        refresh_during=True,
                    )

                # Display main skilling text. Pause before we start skilling.
                game_object.display_overworld_bottom_text_first_page(
                    main_skilling_text,
                    auto_advance=True,
                    advance_delay_ms=GATHERING_START_DELAY_MS,
                    refresh_after=False,
                    refresh_during=False
                )

                LOGGER.info("Beginning gathering.")

                # Start skilling.
                skilling = True
                resource_exhausted = False
                num_skill_ticks = 0
                image_id_index = 0
                pygame.event.clear()
                prev_sequence_id = acting_object.curr_image_sequence

                while skilling and not resource_exhausted:
                    timekeeper.Timekeeper.tick()

                    num_skill_ticks = num_skill_ticks + 1

                    # TODO set next character image ID for skilling.
                    if (num_skill_ticks \
                            % GATHERING_IMAGE_INTERVAL_NUM_TICKS) == 0:
                        LOGGER.debug("Switch image IDs here.")
                        game_object.refresh_and_blit_overworld_viewing(
                            display_update=False
                        )
                    elif (num_skill_ticks \
                            % timekeeper.OW_REFRESH_TICK_INTERVAL) == 0:
                        # Refresh and reblit overworld.
                        game_object.refresh_and_blit_overworld_viewing(
                            display_update=False
                        )
                    elif (num_skill_ticks \
                            % timekeeper.OW_REBLIT_TICK_INTERVAL) == 0:
                        game_object.overworld_viewing.blit_self()

                    # This will update display for us.
                    game_object.display_overworld_bottom_text_first_page(
                        main_skilling_text,
                        auto_advance=True,
                        advance_delay_ms=0,
                        refresh_after=False,
                        refresh_during=False,
                    )

                    # Check if user is ending early by pressing a valid key.
                    exit_key_pressed = False
                    for events in pygame.event.get():
                        if events.type == pygame.QUIT:
                            LOGGER.info("Quitting.")
                            pygame.quit()
                            sys.exit(0)
                        elif events.type == pygame.KEYDOWN:
                            if events.key in SKILLING_EXIT_KEYS:
                                LOGGER.info("Quitting gathering early.")
                                exit_key_pressed = True

                    if exit_key_pressed:
                        skilling = False

                    # Chance to generate a resource after every gathering
                    # interval.
                    elif (num_skill_ticks \
                            % GATHERING_INTERVAL_NUM_TICKS) == 0:
                        # Check if we have generated a resource.
                        # (for now, just use strict probability. later,
                        # implement function that determines generation based on
                        # resource required level and character level and
                        # character equipment)
                        #if random.randint(0,4) == 0:
                        if random.randint(0,1) == 0:
                            # We generated a resource.
                            LOGGER.info("Gathered resource!")

                            # Determine which resource we obtained.
                            resource_gather_text = None
                            gained_resource = None
                            resource_exp = None

                            resource_item_info = \
                                target_object.select_resource_item_info(
                                    acting_object.get_skill_level(
                                        target_object.related_skill_id
                                    )
                                )

                            LOGGER.info(
                                "Resource item info: %s",
                                resource_item_info,
                            )

                            if resource_item_info:
                                gained_resource = items.Item.get_item(
                                    resource_item_info[0]
                                )
                                # TODO handle cases of boosted exp?
                                resource_exp = resource_item_info[1]

                            if gained_resource:
                                resource_gather_text = \
                                    interactiondata.GATHERING_RESOURCE_GAIN_MESSAGES.get(
                                        interaction_id,
                                        {}
                                    ).get(
                                        language.Language.current_language_id,
                                        ""
                                    ).format(
                                        gained_resource.get_name(),
                                        resource_exp
                                    )

                                # Add item to inventory.
                                acting_object.add_item_to_inventory(
                                    gained_resource.item_id
                                )

                                # Check if resource has been exhausted.
                                if random.randint(0, 100) < int(
                                        100 \
                                        * target_object.exhaustion_probability
                                    ):
                                    # Resource has been exhausted.
                                    skilling = False
                                    resource_exhausted = True
                                    LOGGER.info("Resource exhausted.")

                                    # Set respawn.
                                    game_object.set_object_respawn(
                                        target_object,
                                        target_object_loc,
                                    )

                                game_object.refresh_and_blit_overworld_viewing()

                            # Display the resource gather message.
                            if resource_gather_text:
                                game_object.display_overworld_bottom_text_first_page(
                                    resource_gather_text,
                                    auto_advance=False,
                                    refresh_after=True,
                                    refresh_during=True,
                                )
                            else:
                                game_object.refresh_and_blit_overworld_viewing()

                            # This will display level up message if needed.
                            levels_gained = game_object.gain_experience(
                                acting_object,
                                skill_id,
                                resource_exp,
                            )

                            # Stop skilling if we level up.
                            if levels_gained and levels_gained > 0:
                                skilling = False

                            if resource_exhausted:
                                # Display exhaust message.
                                game_object.display_overworld_bottom_text_first_page(
                                    resource_exhaust_text,
                                    auto_advance=False,
                                    advance_delay_ms=GATHERING_EXHAUST_DELAY_MS,
                                    refresh_after=True,
                                    refresh_during=True,
                                )

                                #game_object.refresh_and_blit_overworld_viewing()

                            if skilling and acting_object.inventory_full():
                                # Inventory is full.
                                skilling = False
                                cls.display_inventory_full_message()
                                game_object.refresh_and_blit_overworld_viewing()

                pygame.event.clear()
                acting_object.curr_image_sequence = prev_sequence_id

        # Update overworld and display.
        game_object.refresh_and_blit_overworld_viewing()
        pygame.display.update()

    @classmethod
    def chop_tree_interaction(
            cls,
            #interaction_id,
            game_object,
            acting_object,
            target_object,
            acting_object_loc,
            target_object_loc,
        ):
        if game_object and acting_object \
                and target_object and acting_object_loc and target_object_loc:
            obj_name = target_object.get_name()

            main_skilling_text = interactiondata.GATHERING_MAIN_MESSAGES.get(
                #interaction_id,
                interactiondata.CHOP_TREE_ID,
                {}
            ).get(
                language.Language.current_language_id,
                ""
            ).format(obj_name)

            resource_exhaust_text = interactiondata.GATHERING_RESOURCE_EXHAUST_MESSAGES.get(
                #interaction_id,
                interactiondata.CHOP_TREE_ID,
                {}
            ).get(
                language.Language.current_language_id,
                ""
            ).format(obj_name)

            cls.gathering_interaction(
                #interaction_id,
                interactiondata.CHOP_TREE_ID,
                game_object,
                acting_object,
                target_object,
                acting_object_loc,
                target_object_loc,
                main_skilling_text,
                skills.SKILL_ID_WOODCUTTING,
                resource_exhaust_text=resource_exhaust_text,
            )

    @classmethod
    def mine_rock_interaction(
            cls,
            #interaction_id,
            game_object,
            acting_object,
            target_object,
            acting_object_loc,
            target_object_loc,
        ):
        if game_object and acting_object \
                and target_object and acting_object_loc and target_object_loc:
            obj_name = target_object.get_name()

            main_skilling_text = interactiondata.GATHERING_MAIN_MESSAGES.get(
                #interaction_id,
                interactiondata.MINE_ROCK_ID,
                {}
            ).get(
                language.Language.current_language_id,
                ""
            ).format(obj_name)

            resource_exhaust_text = interactiondata.GATHERING_RESOURCE_EXHAUST_MESSAGES.get(
                #interaction_id,
                interactiondata.MINE_ROCK_ID,
                {}
            ).get(
                language.Language.current_language_id,
                ""
            ).format(obj_name)

            cls.gathering_interaction(
                #interaction_id,
                interactiondata.MINE_ROCK_ID,
                game_object,
                acting_object,
                target_object,
                acting_object_loc,
                target_object_loc,
                main_skilling_text,
                skills.SKILL_ID_MINING,
                resource_exhaust_text=resource_exhaust_text,
            )

    @classmethod
    def fishing_rod_interaction(
            cls,
            #interaction_id,
            game_object,
            acting_object,
            target_object,
            acting_object_loc,
            target_object_loc,
        ):
        if game_object and acting_object \
                and target_object and acting_object_loc and target_object_loc:
            obj_name = target_object.get_name()

            main_skilling_text = interactiondata.GATHERING_MAIN_MESSAGES.get(
                #interaction_id,
                interactiondata.CATCH_FISH_ROD_ID,
                {}
            ).get(
                language.Language.current_language_id,
                ""
            ).format(obj_name)

            resource_exhaust_text = interactiondata.GATHERING_RESOURCE_EXHAUST_MESSAGES.get(
                #interaction_id,
                interactiondata.CATCH_FISH_ROD_ID,
                {}
            ).get(
                language.Language.current_language_id,
                ""
            ).format(obj_name)

            cls.gathering_interaction(
                interactiondata.CATCH_FISH_ROD_ID,
                game_object,
                acting_object,
                target_object,
                acting_object_loc,
                target_object_loc,
                main_skilling_text,
                skills.SKILL_ID_FISHING,
                resource_exhaust_text=resource_exhaust_text,
            )

    @classmethod
    def fishing_net_interaction(
            cls,
            #interaction_id,
            game_object,
            acting_object,
            target_object,
            acting_object_loc,
            target_object_loc,
        ):
        if game_object and acting_object \
                and target_object and acting_object_loc and target_object_loc:
            pass

    @classmethod
    def cooking_interaction(
            cls,
            #interaction_id,
            game_object,
            acting_object,
            target_object,
            acting_object_loc,
            target_object_loc,
        ):
        if game_object and acting_object \
                and target_object and acting_object_loc and target_object_loc:
            pass

    @classmethod
    def herblore_gather_interaction(
            cls,
            #interaction_id,
            game_object,
            acting_object,
            target_object,
            acting_object_loc,
            target_object_loc,
        ):
        if game_object and acting_object \
                and target_object and acting_object_loc and target_object_loc:
            LOGGER.info("Place herb gather interaction here.")

    @classmethod
    def light_log_interaction(
            cls,
            game_object,
            log_obj_id,
        ):
        """Lights fire in front of protagonist.

        The fire duration depends on the log object corresponding to
        log_obj_id. If the protagonist doesn't have a high enough skill level
        to light the given log, or if the protagonist cannot light a fire in
        front of itself, then the method will display the appropriate message
        to the user.

        Args:
            log_obj_id: item ID for the log to burn.
        """

        log_obj = None
        skill_name = skills.get_skill_name(
            skills.SKILL_ID_FIREMAKING,
            language.Language.current_language_id
        )

        # Get tile loc in front of protagonist.
        front_tile_pos = game_object.get_protagonist_facing_tile_location()

        if log_obj_id in itemdata.LIGHTABLE_LOGS:
            log_obj = items.Item.get_item(log_obj_id)
        else:
            LOGGER.warn(
                "Cannot light a log using non-lightable-log item ID %d",
                log_obj_id
            )

        if log_obj:
            # Check if protagonist has proper level.
            req_level = itemdata.LIGHTING_LOG_SKILL_MAPPING.get(
                log_obj_id,
                None
            )
            protag_fire_level = game_object.protagonist.get_skill_level(skills.SKILL_ID_FIREMAKING)

            if req_level is not None:
                if protag_fire_level < req_level:
                    # Not high enough level.
                    user_message = \
                        NOT_HIGH_ENOUGH_LEVEL_MESSAGE_INFO.get(
                            language.Language.current_language_id,
                            ""
                        ).format(
                            req_level,
                            skill_name
                        )

                    game_object.display_overworld_bottom_text(
                        user_message,
                        auto_advance=False,
                        refresh_after=True,
                        refresh_during=True,
                    )
                elif not game_object.can_light_fire_on_tile(front_tile_pos):
                    # Cannot light fire.
                    user_message = \
                        interactiondata.CANNOT_LIGHT_IN_FRONT_INFO.get(
                            language.Language.current_language_id,
                            ""
                        )

                    game_object.display_overworld_bottom_text(
                        user_message,
                        auto_advance=False,
                        refresh_after=True,
                        refresh_during=True,
                    )
                else:
                    # TODO randomize success for lighting fire.

                    LOGGER.info("Lighting fire in front.")
                    # Can light fire. TODO - success message,
                    # add fire and add spawn action to remove fire,
                    # and raise XP.
                    fire_obj_id = objdata.LOG_TO_FIRE_MAPPING.get(
                        log_obj_id,
                        None,
                    )
                    fire_duration_s = objdata.FIRE_DURATION_S_MAPPING.get(
                        fire_obj_id,
                        None
                    )
                    if fire_obj_id is not None and fire_duration_s:
                        # Make fire.
                        game_object.set_temporary_spawn(
                            fire_obj_id,
                            front_tile_pos,
                            fire_duration_s
                        )

                        exp_gained = itemdata.LIGHTING_LOG_EXP_MAPPING.get(
                            log_obj_id,
                            0
                        )

                        # Remove log from protagonist inventory.
                        game_object.protagonist.inventory.remove_item(
                            log_obj_id,
                            quantity=1,
                        )

                        # Display message to user.
                        fire_success_msg = interactiondata.LIGHT_LOG_FIRE_INFO.get(
                            language.Language.current_language_id,
                            ""
                        ).format(
                            exp_gained,
                        )

                        game_object.display_overworld_bottom_text(
                            fire_success_msg,
                            auto_advance=False,
                            refresh_after=True,
                            refresh_during=True,
                        )

                        levels_gained = game_object.gain_experience(
                            game_object.protagonist,
                            skills.SKILL_ID_FIREMAKING,
                            exp_gained,
                        )
                    else:
                        LOGGER.warn(
                            "No fire ID or fire duration found for log ID %d",
                            log_obj_id,
                        )

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
    interactiondata.CATCH_FISH_ROD_ID: Interaction.fishing_rod_interaction,
    interactiondata.CATCH_FISH_NET_ID: Interaction.fishing_net_interaction,
    interactiondata.COOKING_ID: Interaction.cooking_interaction,
    interactiondata.HERBLORE_GATHER_ID: Interaction.herblore_gather_interaction,
}

# Set up logger.
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)
