import imagepaths

### EQUIPMENT SLOT ID VALUES ###
EQUIP_SLOT_NONE = 0x0 # Not equippable
EQUIP_SLOT_HEAD = 0x1 # Helmets, hats, etc.
EQUIP_SLOT_MAIN_HAND = 0x2 # Weapons.
EQUIP_SLOT_OFF_HAND = 0x3 # Shields.
EQUIP_SLOT_MAIN_BODY = 0x4 # Plate armour, chainmail, etc.
EQUIP_SLOT_LEGS = 0x5
EQUIP_SLOT_NECK = 0x6 # Amulets, necklaces, etc.
EQUIP_SLOT_AMMO = 0x7 # Arrows, etc.
EQUIP_SLOT_HANDS = 0x8 # Gloves, etc.
EQUIP_SLOT_FEET = 0x9 # Boots, etc.
EQUIP_SLOT_RING = 0xA # Rings.
EQUIP_SLOT_BACK = 0xB # Capes.
EQUIP_SLOT_WRIST = 0xC # Bracelets, etc.

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
# TODO #$$
EQUIPMENT_SLOT_DESCRIPTION_INFO = {
    EQUIP_SLOT_HEAD: "",
    EQUIP_SLOT_MAIN_HAND: "",
    EQUIP_SLOT_OFF_HAND: "",
    EQUIP_SLOT_MAIN_BODY: "",
    EQUIP_SLOT_LEGS: "",
    EQUIP_SLOT_NECK: "",
    EQUIP_SLOT_AMMO: "",
    EQUIP_SLOT_HANDS: "",
    EQUIP_SLOT_FEET: "",
    EQUIP_SLOT_RING: "",
    EQUIP_SLOT_BACK: "",
    EQUIP_SLOT_WRIST: "",
}
