import viewingicondata
import language
import imagepaths
import imageids

### EQUIPMENT SLOT ID VALUES ###
EQUIP_SLOT_NONE = 0 # Not equippable
EQUIP_SLOT_HEAD = 1 # Helmets, hats, etc.
EQUIP_SLOT_MAIN_HAND = 2 # Weapons.
EQUIP_SLOT_OFF_HAND = 3 # Shields.
EQUIP_SLOT_MAIN_BODY = 4 # Plate armour, chainmail, etc.
EQUIP_SLOT_LEGS = 5
EQUIP_SLOT_NECK = 6 # Amulets, necklaces, etc.
EQUIP_SLOT_AMMO = 7 # Arrows, etc.
EQUIP_SLOT_HANDS = 8 # Gloves, etc.
EQUIP_SLOT_FEET = 9 # Boots, etc.
EQUIP_SLOT_RING = 10 # Rings.
EQUIP_SLOT_BACK = 11 # Capes.
EQUIP_SLOT_WRIST = 12 # Bracelets, etc.

# For default equipment slot items.
EQUIPMENT_SLOT_DATA = {
    EQUIP_SLOT_HEAD: {
        viewingicondata.NAME_INFO_FIELD: {
            language.LANG_ENGLISH: "Head Slot",
            language.LANG_ESPANOL: "Espacio de Cabeza",
        },
        viewingicondata.DESCRIPTION_INFO_FIELD: {
            language.LANG_ENGLISH: "For helmets, hats, and other headgear.",
            language.LANG_ESPANOL: "Para yelmos, sombreros, y otros tocados.",
        },
        viewingicondata.OPTION_ID_LIST_FIELD: None,
        viewingicondata.IMAGE_PATH_DICT_FIELD: {
            imageids.ICON_IMAGE_ID: imagepaths.EQUIPMENT_ICON_HEAD_PATH,
        },
    },
    EQUIP_SLOT_MAIN_HAND: {
        viewingicondata.NAME_INFO_FIELD: {
            language.LANG_ENGLISH: "Main Hand Slot",
            language.LANG_ESPANOL: "Espacio de Brazo Principal",
        },
        viewingicondata.DESCRIPTION_INFO_FIELD: {
            language.LANG_ENGLISH: "For swords, bows, staffs, and other weapons.",
            language.LANG_ESPANOL: "Para espadas, arcos, bastones, y otras armas.",
        },
        viewingicondata.OPTION_ID_LIST_FIELD: None,
        viewingicondata.IMAGE_PATH_DICT_FIELD: {
            imageids.ICON_IMAGE_ID: imagepaths.EQUIPMENT_ICON_MAIN_HAND_PATH,
        },
    },
    EQUIP_SLOT_OFF_HAND: {
        viewingicondata.NAME_INFO_FIELD: {
            language.LANG_ENGLISH: "Off Hand Slot",
            language.LANG_ESPANOL: "Espacio de Secundario",
        },
        viewingicondata.DESCRIPTION_INFO_FIELD: {
            language.LANG_ENGLISH: "For shields and secondary weapons.",
            language.LANG_ESPANOL: "Para escudos y armas secundarias.",
        },
        viewingicondata.OPTION_ID_LIST_FIELD: None,
        viewingicondata.IMAGE_PATH_DICT_FIELD: {
            imageids.ICON_IMAGE_ID: imagepaths.EQUIPMENT_ICON_OFF_HAND_PATH,
        },
    },
    EQUIP_SLOT_MAIN_BODY: {
        viewingicondata.NAME_INFO_FIELD: {
            language.LANG_ENGLISH: "Torso Slot",
            language.LANG_ESPANOL: "Espacio de Torso",
        },
        viewingicondata.DESCRIPTION_INFO_FIELD: {
            language.LANG_ENGLISH: "For clothing and armour for the torso.",
            language.LANG_ESPANOL: "Para ropa y armadura para el torso.",
        },
        viewingicondata.OPTION_ID_LIST_FIELD: None,
        viewingicondata.IMAGE_PATH_DICT_FIELD: {
            imageids.ICON_IMAGE_ID: imagepaths.EQUIPMENT_ICON_BODY_PATH,
        },
    },
    EQUIP_SLOT_LEGS: {
        viewingicondata.NAME_INFO_FIELD: {
            language.LANG_ENGLISH: "Legs Slot",
            language.LANG_ESPANOL: "Espacio de Piernas",
        },
        viewingicondata.DESCRIPTION_INFO_FIELD: {
            language.LANG_ENGLISH: "For clothing and armour for the legs.",
            language.LANG_ESPANOL: "Para ropa y armadura para las piernas.",
        },
        viewingicondata.OPTION_ID_LIST_FIELD: None,
        viewingicondata.IMAGE_PATH_DICT_FIELD: {
            imageids.ICON_IMAGE_ID: imagepaths.EQUIPMENT_ICON_LEGS_PATH,
        },
    },
    EQUIP_SLOT_NECK: {
        viewingicondata.NAME_INFO_FIELD: {
            language.LANG_ENGLISH: "Neck Slot",
            language.LANG_ESPANOL: "Espacio de Cuello",
        },
        viewingicondata.DESCRIPTION_INFO_FIELD: {
            language.LANG_ENGLISH: "For necklaces and other neck items.",
            language.LANG_ESPANOL: "Para collares y otras cosas para el cuello.",
        },
        viewingicondata.OPTION_ID_LIST_FIELD: None,
        viewingicondata.IMAGE_PATH_DICT_FIELD: {
            imageids.ICON_IMAGE_ID: imagepaths.EQUIPMENT_ICON_NECK_PATH,
        },
    },
    EQUIP_SLOT_AMMO: {
        viewingicondata.NAME_INFO_FIELD: {
            language.LANG_ENGLISH: "Ammo Slot",
            language.LANG_ESPANOL: "Espacio de Munición",
        },
        viewingicondata.DESCRIPTION_INFO_FIELD: {
            language.LANG_ENGLISH: "For arrows and other types of ammunition.",
            language.LANG_ESPANOL: "Para las flechas y otros tipos de munición.",
        },
        viewingicondata.OPTION_ID_LIST_FIELD: None,
        viewingicondata.IMAGE_PATH_DICT_FIELD: {
            imageids.ICON_IMAGE_ID: imagepaths.EQUIPMENT_ICON_AMMO_PATH,
        },
    },
    EQUIP_SLOT_HANDS: {
        viewingicondata.NAME_INFO_FIELD: {
            language.LANG_ENGLISH: "Hands Slot",
            language.LANG_ESPANOL: "Espacio de Manos",
        },
        viewingicondata.DESCRIPTION_INFO_FIELD: {
            language.LANG_ENGLISH: "For gloves and other hand gear.",
            language.LANG_ESPANOL: "Para guantes y otras equipo para las manos.",
        },
        viewingicondata.OPTION_ID_LIST_FIELD: None,
        viewingicondata.IMAGE_PATH_DICT_FIELD: {
            imageids.ICON_IMAGE_ID: imagepaths.EQUIPMENT_ICON_HANDS_PATH,
        },
    },
    EQUIP_SLOT_FEET: {
        viewingicondata.NAME_INFO_FIELD: {
            language.LANG_ENGLISH: "Feet Slot",
            language.LANG_ESPANOL: "Espacio de Pies",
        },
        viewingicondata.DESCRIPTION_INFO_FIELD: {
            language.LANG_ENGLISH: "For boots, shoes, and other footwear.",
            language.LANG_ESPANOL: "Para botas, zapatos, y otros calzados.",
        },
        viewingicondata.OPTION_ID_LIST_FIELD: None,
        viewingicondata.IMAGE_PATH_DICT_FIELD: {
            imageids.ICON_IMAGE_ID: imagepaths.EQUIPMENT_ICON_FEET_PATH,
        },
    },
    EQUIP_SLOT_RING: {
        viewingicondata.NAME_INFO_FIELD: {
            language.LANG_ENGLISH: "Ring Slot",
            language.LANG_ESPANOL: "Espacio de Anillos",
        },
        viewingicondata.DESCRIPTION_INFO_FIELD: {
            language.LANG_ENGLISH: "For rings.",
            language.LANG_ESPANOL: "Para anillos.",
        },
        viewingicondata.OPTION_ID_LIST_FIELD: None,
        viewingicondata.IMAGE_PATH_DICT_FIELD: {
            imageids.ICON_IMAGE_ID: imagepaths.EQUIPMENT_ICON_RING_PATH,
        },
    },
    EQUIP_SLOT_BACK: {
        viewingicondata.NAME_INFO_FIELD: {
            language.LANG_ENGLISH: "Back Slot.",
            language.LANG_ESPANOL: "Espacio de Espalda",
        },
        viewingicondata.DESCRIPTION_INFO_FIELD: {
            language.LANG_ENGLISH: "For capes and other items that go on the back.",
            language.LANG_ESPANOL: "Para capas y otras cosas para la espalda.",
        },
        viewingicondata.OPTION_ID_LIST_FIELD: None,
        viewingicondata.IMAGE_PATH_DICT_FIELD: {
            imageids.ICON_IMAGE_ID: imagepaths.EQUIPMENT_ICON_BACK_PATH,
        },
    },
    EQUIP_SLOT_WRIST: {
        viewingicondata.NAME_INFO_FIELD: {
            language.LANG_ENGLISH: "Wrist Slot",
            language.LANG_ESPANOL: "Espacio de Muñeca",
        },
        viewingicondata.DESCRIPTION_INFO_FIELD: {
            language.LANG_ENGLISH: "For bracelets and other wrist items.",
            language.LANG_ESPANOL: "Para pulseras y otras cosas para la muñeca.",
        },
        viewingicondata.OPTION_ID_LIST_FIELD: None,
        viewingicondata.IMAGE_PATH_DICT_FIELD: {
            imageids.ICON_IMAGE_ID: imagepaths.EQUIPMENT_ICON_WRIST_PATH,
        },
    },
}
