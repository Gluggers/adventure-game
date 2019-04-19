import logging
import random
import sys
import pygame
import interactiveobj
import objdata
import interactiondata

class Resource(interactiveobj.InteractiveObject):
    # Initialize Resource
    # respawn_time_s value of None means the resource object will not respawn?
    def __init__(
            self,
            object_id,
            name_info,
            image_info_dict,
            collision_width=1,
            collision_height=1,
            related_skill_id=None,
            min_required_level=0,
            #gained_xp=0,
            resource_item_info=None,
            #resource_item=None,
            respawn_time_s=1,
            exhaustion_probability=1,
            examine_info=None,
            interaction_id=interactiondata.DEFAULT_ID,
            replacement_object_id=None,
        ):
        # Call the parent class init
        interactiveobj.InteractiveObject.__init__(
            self,
            objdata.TYPE_RESOURCE,
            object_id,
            name_info,
            image_info_dict,
            collision_width=collision_width,
            collision_height=collision_height,
            examine_info=examine_info,
            interaction_id=interaction_id,
            replacement_object_id=replacement_object_id,
            respawn_time_s=respawn_time_s,
        )

        self.related_skill_id = related_skill_id
        self.min_required_level = min_required_level
        #self.gained_xp = gained_xp
        #self.resource_item = resource_item
        self.exhaustion_probability = float(exhaustion_probability)
        self.resource_item_info = None

        if resource_item_info:
            self.resource_item_info = []

            for info_tuple in resource_item_info:
                self.resource_item_info.append(info_tuple)

    # Factory method to create a resource
    @classmethod
    def resource_factory(cls, resource_id):
        ret_resource = None

        # Make sure we are dealing with a resource ID
        if interactiveobj.InteractiveObject.is_resource_id(resource_id):
            # Check if we already have the resouce made
            resource_from_listing = cls.get_resource(resource_id)

            if resource_from_listing:
                # Return the already made resource
                ret_resource = resource_from_listing
            else:
                # Make the new resource ourselves. First, get the
                # resource data
                resource_data = objdata.RESOURCE_DATA.get(resource_id, None)

                if resource_data:
                    # Get the resource fields
                    # TODO - change default values?
                    name_info = resource_data.get(objdata.OBJECT_NAME_INFO_FIELD, {})
                    image_info_dict = resource_data.get(objdata.IMAGE_INFO_DICT_FIELD, {})
                    collision_width = resource_data.get(objdata.COLLISION_WIDTH_FIELD, 1)
                    collision_height = resource_data.get(objdata.COLLISION_HEIGHT_FIELD, 1)
                    skill_id = resource_data.get(objdata.RELATED_SKILL_ID_FIELD, None)
                    min_required_level = resource_data.get(objdata.MIN_REQUIRED_LEVEL_FIELD, 0)
                    #gained_xp = resource_data.get(objdata.GAINED_XP_FIELD, 0)
                    resource_item_info = resource_data.get(objdata.RESOURCE_ITEM_INFO_FIELD, None)
                    #resource_item = resource_data.get(objdata.RESOURCE_ITEM_FIELD, None)
                    respawn_time_s = resource_data.get(objdata.RESPAWN_TIME_S_FIELD, None)
                    exhaustion_probability = resource_data.get(objdata.EXHAUSTION_PROBABILITY_FIELD, 1)
                    examine_info = resource_data.get(objdata.EXAMINE_INFO_FIELD, None)
                    interaction_id = resource_data.get(
                        objdata.INTERACTION_ID_FIELD,
                        interactiondata.DEFAULT_ID
                    )
                    replacement_object_id = resource_data.get(
                        objdata.REPLACEMENT_OBJECT_ID_FIELD,
                        None
                    )

                    # Ensure we have the required fields.
                    if name_info and image_info_dict and (interaction_id is not None):
                        # Make the resource.
                        new_resource = Resource(
                            resource_id,
                            name_info,
                            image_info_dict,
                            collision_width=collision_width,
                            collision_height=collision_height,
                            related_skill_id=skill_id,
                            min_required_level=min_required_level,
                            #gained_xp=gained_xp,
                            #resource_item=resource_item,
                            resource_item_info=resource_item_info,
                            respawn_time_s=respawn_time_s,
                            exhaustion_probability=exhaustion_probability,
                            examine_info=examine_info,
                            interaction_id=interaction_id,
                            replacement_object_id=replacement_object_id,
                        )

                        LOGGER.debug("Made resource with ID %d", resource_id)

                        # Update the interactive object mapping
                        result = interactiveobj.InteractiveObject.add_interactive_obj_to_listing(
                            resource_id,
                            new_resource
                        )

                        if result:
                            ret_resource = new_resource
                    else:
                        LOGGER.error(
                            "Required fields not found in resource data for ID %d",
                            resource_id
                        )
                        sys.exit(2)
                else:
                    LOGGER.error(
                        "Resource data not found for resource ID %d",
                        resource_id
                    )
                    sys.exit(2)

        return ret_resource


    def select_resource_item_info(self, level):
        """Randomly selects one of the eligible resource items, and returns
        a tuple of (item ID, gained experience).

        For resources with only one resource item that meets the given level,
        that single item will be returned.
        For resources with multiple resource items that meet the given level,
        one will be selected according to the probability weightings of the
        eligible objects.

        Args:
            level: The skill level of the character trying to obtain the
                resource. The method assumes that the skill level is for
                the appropriate skill for this resource.

        Returns:
            Tuple of (item ID, gained exp) for one of the resource items.
        """

        ret_item_info = None

        if level and level >= self.min_required_level and self.resource_item_info:
            # Get the eligible items based on the given level.
            eligible_item_info = []

            total_weight = 0

            for item_info in self.resource_item_info:
                required_level = item_info[1]
                probability_weight = item_info[2]

                if level >= required_level:
                    eligible_item_info.append(item_info)
                    total_weight += probability_weight

            LOGGER.debug("Eligible items: %s", eligible_item_info)
            LOGGER.info("Total weight: %d", total_weight)

            if len(eligible_item_info) == 1:
                item_info = eligible_item_info[0]
                ret_item_info = (item_info[0], item_info[3])
            elif total_weight:
                # Select a random number to indicate the item choice.
                selection_num = random.randint(0, total_weight - 1)

                LOGGER.info("Selected num: %d", selection_num)

                curr_subtotal = 0
                selected_item_info = None

                for item_info in eligible_item_info:
                    item_id = item_info[0]
                    gained_exp = item_info[3]
                    probability_weight = item_info[2]

                    if selection_num >= curr_subtotal:
                        selected_item_info = item_info

                    curr_subtotal += probability_weight

                if selected_item_info:
                    ret_item_info = (selected_item_info[0], selected_item_info[3])

        return ret_item_info


    # Does not make new resource.
    @classmethod
    def get_resource(cls, resource_id):
        ret_resource = None

        # Make sure we are dealing with a resource ID
        if interactiveobj.InteractiveObject.is_resource_id(resource_id):
            ret_resource = interactiveobj.InteractiveObject.get_interactive_object(resource_id)

        return ret_resource

    @classmethod
    def build_resources(cls):
        LOGGER.info("Building resources")

        for resource_id in objdata.RESOURCE_DATA:
            if not Resource.resource_factory(resource_id):
                LOGGER.error("Could not construct resource with ID {0}".format(resource_id))
                sys.exit(2)

# set up logger
logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)
