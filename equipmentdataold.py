import imagepaths


class EquipmentSlot(object):
    # Maps equipment slot IDs to icon images.
    equipment_slot_icon_mapping = {}
    equipment_slot_enlarged_icon_mapping = {}

    EQUIPMENT_SLOT_ID_LIST = [
        EQUIP_SLOT_HEAD,
        EQUIP_SLOT_MAIN_HAND,
        EQUIP_SLOT_OFF_HAND,
        EQUIP_SLOT_MAIN_BODY,
        EQUIP_SLOT_LEGS,
        EQUIP_SLOT_NECK,
        EQUIP_SLOT_AMMO,
        EQUIP_SLOT_HANDS,
        EQUIP_SLOT_FEET,
        EQUIP_SLOT_RING,
        EQUIP_SLOT_BACK,
        EQUIP_SLOT_WRIST,
    ]

    EQUIPMENT_SLOT_NAME_INFO = {
        EQUIP_SLOT_HEAD: {
            language.LANG_ENGLISH: "Head Slot",
            language.LANG_ESPANOL: "Espacio de Cabeza",
        },
        EQUIP_SLOT_MAIN_HAND: {
            language.LANG_ENGLISH: "Main Hand Slot",
            language.LANG_ESPANOL: "Espacio de Brazo Principal",
        },
        EQUIP_SLOT_OFF_HAND: {
            language.LANG_ENGLISH: "Off Hand Slot",
            language.LANG_ESPANOL: "Espacio de Secundario",
        },
        EQUIP_SLOT_MAIN_BODY: {
            language.LANG_ENGLISH: "Torso Slot",
            language.LANG_ESPANOL: "Espacio de Torso",
        },
        EQUIP_SLOT_LEGS: {
            language.LANG_ENGLISH: "Legs Slot",
            language.LANG_ESPANOL: "Espacio de Piernas",
        },
        EQUIP_SLOT_NECK: {
            language.LANG_ENGLISH: "Neck Slot",
            language.LANG_ESPANOL: "Espacio de Cuello",
        },
        EQUIP_SLOT_AMMO: {
            language.LANG_ENGLISH: "Ammo Slot",
            language.LANG_ESPANOL: "Espacio de Munición",
        },
        EQUIP_SLOT_HANDS: {
            language.LANG_ENGLISH: "Hands Slot",
            language.LANG_ESPANOL: "Espacio de Manos",
        },
        EQUIP_SLOT_FEET: {
            language.LANG_ENGLISH: "Feet Slot",
            language.LANG_ESPANOL: "Espacio de Pies",
        },
        EQUIP_SLOT_RING: {
            language.LANG_ENGLISH: "Ring Slot",
            language.LANG_ESPANOL: "Espacio de Anillos",
        },
        EQUIP_SLOT_BACK: {
            language.LANG_ENGLISH: "Back Slot.",
            language.LANG_ESPANOL: "Espacio de Espalda",
        },
        EQUIP_SLOT_WRIST: {
            language.LANG_ENGLISH: "Wrist Slot",
            language.LANG_ESPANOL: "Espacio de Muñeca",
        },
    }

    # MAPS EQUIPMENT SLOT ID TO DESCRIPTION INFORMATION.
    EQUIPMENT_SLOT_DESCRIPTION_INFO = {
        EQUIP_SLOT_HEAD: {
            language.LANG_ENGLISH: "For helmets, hats, and other headgear.",
            language.LANG_ESPANOL: "Para yelmos, sombreros, y otros tocados.",
        },
        EQUIP_SLOT_MAIN_HAND: {
            language.LANG_ENGLISH: "For swords, bows, staffs, and other weapons.",
            language.LANG_ESPANOL: "Para espadas, arcos, bastones, y otras armas.",
        },
        EQUIP_SLOT_OFF_HAND: {
            language.LANG_ENGLISH: "For shields and secondary weapons.",
            language.LANG_ESPANOL: "Para escudos y armas secundarias.",
        },
        EQUIP_SLOT_MAIN_BODY: {
            language.LANG_ENGLISH: "For clothing and armour for the torso.",
            language.LANG_ESPANOL: "Para ropa y armadura para el torso.",
        },
        EQUIP_SLOT_LEGS: {
            language.LANG_ENGLISH: "For clothing and armour for the legs.",
            language.LANG_ESPANOL: "Para ropa y armadura para las piernas.",
        },
        EQUIP_SLOT_NECK: {
            language.LANG_ENGLISH: "For necklaces and other neck items.",
            language.LANG_ESPANOL: "Para collares y otras cosas para el cuello.",
        },
        EQUIP_SLOT_AMMO: {
            language.LANG_ENGLISH: "For arrows and other types of ammunition.",
            language.LANG_ESPANOL: "Para las flechas y otros tipos de munición.",
        },
        EQUIP_SLOT_HANDS: {
            language.LANG_ENGLISH: "For gloves and other hand gear.",
            language.LANG_ESPANOL: "Para guantes y otras equipo para las manos.",
        },
        EQUIP_SLOT_FEET: {
            language.LANG_ENGLISH: "For boots, shoes, and other footwear.",
            language.LANG_ESPANOL: "Para botas, zapatos, y otros calzados.",
        },
        EQUIP_SLOT_RING: {
            language.LANG_ENGLISH: "For rings.",
            language.LANG_ESPANOL: "Para anillos.",
        },
        EQUIP_SLOT_BACK: {
            language.LANG_ENGLISH: "For capes and other items that go on the back.",
            language.LANG_ESPANOL: "Para capas y otras cosas para la espalda.",
        },
        EQUIP_SLOT_WRIST: {
            language.LANG_ENGLISH: "For bracelets and other wrist items.",
            language.LANG_ESPANOL: "Para pulseras y otras cosas para la muñeca.",
        },
    }

    # MAPS EQUIPMENT SLOT ID TO IMAGE PATH FOR ICON.
    EQUIPMENT_SLOT_IMAGE_PATHS = {
        EQUIP_SLOT_HEAD: imagepaths.EQUIPMENT_ICON_HEAD_PATH,
        EQUIP_SLOT_MAIN_HAND: imagepaths.EQUIPMENT_ICON_MAIN_HAND_PATH,
        EQUIP_SLOT_OFF_HAND: imagepaths.EQUIPMENT_ICON_OFF_HAND_PATH,
        EQUIP_SLOT_MAIN_BODY: imagepaths.EQUIPMENT_ICON_BODY_PATH,
        EQUIP_SLOT_LEGS: imagepaths.EQUIPMENT_ICON_LEGS_PATH,
        EQUIP_SLOT_NECK: imagepaths.EQUIPMENT_ICON_NECK_PATH,
        EQUIP_SLOT_AMMO: imagepaths.EQUIPMENT_ICON_AMMO_PATH,
        EQUIP_SLOT_HANDS: imagepaths.EQUIPMENT_ICON_HANDS_PATH,
        EQUIP_SLOT_FEET: imagepaths.EQUIPMENT_ICON_FEET_PATH,
        EQUIP_SLOT_RING: imagepaths.EQUIPMENT_ICON_RING_PATH,
        EQUIP_SLOT_BACK: imagepaths.EQUIPMENT_ICON_BACK_PATH,
        EQUIP_SLOT_WRIST: imagepaths.EQUIPMENT_ICON_WRIST_PATH,
    }

    def __init__(self):
        pass

    @classmethod
    def get_equipment_slot_description(cls, slot_id):
        return cls.EQUIPMENT_SLOT_DESCRIPTION_INFO.get(
            language.Language.current_language_id,
            None
        )

    @classmethod
    def get_equipment_slot_name(cls, slot_id):
        return cls.EQUIPMENT_SLOT_NAME_INFO.get(
            language.Language.current_language_id,
            None
        )

    @classmethod
    def get_equipment_slot_icon(cls, slot_id):
        return cls.equipment_slot_icon_mapping.get(
            slot_id,
            None
        )

    @classmethod
    def get_equipment_slot_enlarged_icon(cls, slot_id):
        return cls.equipment_slot_enlarged_icon_mapping.get(
            slot_id,
            None
        )

    @classmethod
    def init_equipment_slot_icons(cls):
        for slot_id, image_path in cls.EQUIPMENT_SLOT_IMAGE_PATHS.items():
            image_icon = pygame.image.load(
                image_path
            ).convert_alpha()

            if image_icon:
                cls.equipment_slot_icon_mapping[slot_id] = image_icon

                enlarged_icon = pygame.transform.scale(
                    image_icon,
                    (image_icon.get_width() * 2, image_icon.get_height() * 2)
                )

                if enlarged_icon:
                    cls.equipment_slot_enlarged_icon_mapping[slot_id] = \
                        enlarged_icon
