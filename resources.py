import pygame
import interactiveobj
import logging
import objdata
import interactiondata

class Resource(interactiveobj.Interactive_Object):
    # Initialize Resource
    # respawn_time_s value of None means the resource object will not respawn?
    def __init__(
                self,
                object_id,
                name_info,
                image_path_dict,
                collision_width=1,
                collision_height=1,
                related_skill_id=None,
                required_level=0,
                gained_xp=0,
                resource_item=None,
                respawn_time_s=1,
                exhaustion_probability=1,
                examine_info=None,
                interaction_id=interactiondata.DEFAULT_ID,
            ):
        # Call the parent class init
        interactiveobj.Interactive_Object.__init__(
            self,
            objdata.TYPE_RESOURCE,
            object_id,
            name_info,
            image_path_dict,
            collision_width=collision_width,
            collision_height=collision_height,
            examine_info=examine_info,
            interaction_id=interaction_id
        )

        self.related_skill_id = related_skill_id
        self.required_level = required_level
        self.gained_xp = gained_xp
        self.resource_item = resource_item
        self.respawn_time_s = respawn_time_s
        self.exhaustion_probability = float(exhaustion_probability)

    # Factory method to create a resource
    @classmethod
    def resource_factory(cls, resource_id):
        ret_resource = None

        # Make sure we are dealing with a resource ID
        if interactiveobj.Interactive_Object.is_resource_id(resource_id):
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
                    image_path_dict = resource_data.get(objdata.IMAGE_PATH_DICT_FIELD, {})
                    collision_width = resource_data.get(objdata.COLLISION_WIDTH_FIELD, 1)
                    collision_height = resource_data.get(objdata.COLLISION_HEIGHT_FIELD, 1)
                    skill_id = resource_data.get(objdata.RELATED_SKILL_ID_FIELD, None)
                    required_level = resource_data.get(objdata.REQUIRED_LEVEL_FIELD, 0)
                    gained_xp = resource_data.get(objdata.GAINED_XP_FIELD, 0)
                    resource_item = resource_data.get(objdata.RESOURCE_ITEM_FIELD, None)
                    respawn_time_s = resource_data.get(objdata.RESPAWN_TIME_S_FIELD, 1)
                    exhaustion_probability = resource_data.get(objdata.EXHAUSTION_PROBABILITY_FIELD, 1)
                    examine_info = resource_data.get(objdata.EXAMINE_INFO_FIELD, None)
                    interaction_id = resource_data.get(
                        objdata.INTERACTION_ID_FIELD,
                        interactiondata.DEFAULT_ID
                    )

                    # Ensure we have the required fields.
                    if name_info and image_path_dict and (interaction_id is not None):
                        # Make the resource.
                        new_resource = Resource(
                            resource_id,
                            name_info,
                            image_path_dict,
                            collision_width=collision_width,
                            collision_height=collision_height,
                            related_skill_id=skill_id,
                            required_level=required_level,
                            gained_xp=gained_xp,
                            resource_item=resource_item,
                            respawn_time_s=respawn_time_s,
                            exhaustion_probability=exhaustion_probability,
                            examine_info=examine_info,
                            interaction_id=interaction_id,
                        )

                        logger.debug("Made resource with ID {0}".format(resource_id))

                        # Update the interactive object mapping
                        result = interactiveobj.Interactive_Object.add_interactive_obj_to_listing(
                            resource_id,
                            new_resource
                        )

                        if result:
                            ret_resource = new_resource
                    else:
                        logger.warn("Required fields not found in resource data for ID {0}".format(resource_id))
                else:
                    logger.warn("Resource data not found for resource ID {0}".format(resource_id))

        return ret_resource

    # Does not make new resource.
    @classmethod
    def get_resource(cls, resource_id):
        ret_resource = None

        # Make sure we are dealing with a resource ID
        if interactiveobj.Interactive_Object.is_resource_id(resource_id):
            ret_resource = interactiveobj.Interactive_Object.get_interactive_object(resource_id)

        return ret_resource

    @classmethod
    def build_resources(cls):
        logger.debug("Building resources")

        for resource_id in objdata.RESOURCE_DATA:
            if not Resource.resource_factory(resource_id):
                logger.error("Could not construct resource with ID {0}".format(resource_id))

# set up logger
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
