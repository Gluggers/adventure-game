import skills
import language
import currency
import menuoptions
import imageids
import imagepaths

ITEM_ICON_WIDTH = 50
ITEM_ICON_HEIGHT = 50
ITEM_ICON_DIMENSIONS = (ITEM_ICON_WIDTH, ITEM_ICON_HEIGHT)

### ITEM PROPERTY FLAGS ###
STACKABLE_F = 0x1
SELLABLE_F = 0x2
CONSUMABLE_F = 0x4
QUEST_ITEM_F = 0x8 # Special quest-related item that shouldn't be sold or destroyed.
ALCHABLE_F = 0x10
COOKABLE_FIRE_F = 0x20
COOKABLE_RANGE_F = 0x40
TOOL_ITEM_F = 0x80

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

### ITEM ID NUMBERS ###

# SPECIAL ITEMS 1 TO 9999

CURRENCY_GOLD_COIN_ID = 101
CURRENCY_SILVER_COIN_ID = 102
CURRENCY_TRADING_STICKS_ID = 103
CURRENCY_YEN_ID = 104

# Maps currency IDs to the number of units equivalent to 1 Base Value
CURRENCY_VALUE_MAPPING = {
    CURRENCY_GOLD_COIN_ID: 1,
    CURRENCY_SILVER_COIN_ID: 3,
    CURRENCY_TRADING_STICKS_ID: 5,
    CURRENCY_YEN_ID: 2,
}

# TOOLS 10000 TO 19999
KNIFE_ID = 10001
TINDERBOX_ID = 10002
NEEDLE_ID = 10003
HAMMER_NORMAL_ID = 10102 # For metals up to steel.
HAMMER_TITANIUM_ID = 10106 # For metals up to titanium.
HAMMER_MITHRIL_ID = 10107 # For metals up to mithril.
HAMMER_ADAMANT_ID = 10108 # For metals up to adamant.
HAMMER_ANCIENT_ID = 10109 # For metals up to ancient.
HAMMER_ASTRAL_ID = 10110 # For metals up to astral.
HAMMER_DRAGONITE_ID = 10111 # For metals up to dragonite.
HAMMER_CELESTIAL_ID = 10112 # For all metals.
HATCHET_STONE_ID = 10202
HATCHET_BRONZE_ID = 10203
HATCHET_IRON_ID = 10204
HATCHET_STEEL_ID = 10205
HATCHET_TITANIUM_ID = 10206
HATCHET_MITHRIL_ID = 10207
HATCHET_ADAMANT_ID = 10208
HATCHET_ANCIENT_ID = 10209
HATCHET_ASTRAL_ID = 10210
HATCHET_DRAGONITE_ID = 10211
HATCHET_CELESTIAL_ID = 10212
# TODO pickaxe

# WEAPONS 50000 TO 0x59999
DAGGER_WOODEN_ID = 50001
DAGGER_STONE_ID = 50002
DAGGER_BRONZE_ID = 50003
DAGGER_IRON_ID = 50004
DAGGER_STEEL_ID = 50005
DAGGER_TITANIUM_ID = 50006
DAGGER_MITHRIL_ID = 50007
DAGGER_ADAMANT_ID = 50008
DAGGER_ANCIENT_ID = 50009
DAGGER_ASTRAL_ID = 50010
DAGGER_DRAGONITE_ID = 50011
DAGGER_CELESTIAL_ID = 50012
SWORD_WOODEN_ID = 50101
SWORD_STONE_ID = 50102
SWORD_BRONZE_ID = 50103
SWORD_IRON_ID = 50104
SWORD_STEEL_ID = 50105
SWORD_TITANIUM_ID = 50106
SWORD_MITHRIL_ID = 50107
SWORD_ADAMANT_ID = 50108
SWORD_ANCIENT_ID = 50109
SWORD_ASTRAL_ID = 50110
SWORD_DRAGONITE_ID = 50111
SWORD_CELESTIAL_ID = 50112
BATTLEAXE_WOODEN_ID = 50201
BATTLEAXE_STONE_ID = 50202
BATTLEAXE_BRONZE_ID = 50203
BATTLEAXE_IRON_ID = 50204
BATTLEAXE_STEEL_ID = 50205
BATTLEAXE_TITANIUM_ID = 50206
BATTLEAXE_MITHRIL_ID = 50207
BATTLEAXE_ADAMANT_ID = 50208
BATTLEAXE_ANCIENT_ID = 50209
BATTLEAXE_ASTRAL_ID = 50210
BATTLEAXE_DRAGONITE_ID = 50211
BATTLEAXE_CELESTIAL_ID = 50212
BROADSWORD_WOODEN_ID = 50301
BROADSWORD_STONE_ID = 50302
BROADSWORD_BRONZE_ID = 50303
BROADSWORD_IRON_ID = 50304
BROADSWORD_STEEL_ID = 50305
BROADSWORD_TITANIUM_ID = 50306
BROADSWORD_MITHRIL_ID = 50307
BROADSWORD_ADAMANT_ID = 50308
BROADSWORD_ANCIENT_ID = 50309
BROADSWORD_ASTRAL_ID = 50310
BROADSWORD_DRAGONITE_ID = 50311
BROADSWORD_CELESTIAL_ID = 50312
ARROW_WOODEN_ID = 50401
ARROW_STONE_ID = 50402
ARROW_BRONZE_ID = 50403
ARROW_IRON_ID = 50404
ARROW_STEEL_ID = 50405
ARROW_TITANIUM_ID = 50406
ARROW_MITHRIL_ID = 50407
ARROW_ADAMANT_ID = 50408
ARROW_ANCIENT_ID = 50409
ARROW_ASTRAL_ID = 50410
ARROW_DRAGONITE_ID = 50411
ARROW_CELESTIAL_ID = 50412
STAFF_WOODEN_ID = 51001
STAFF_NOVICE_ID = 51002

# RESOURCES 140000 TO 149999
LOG_TREE_ID = 140001
LOG_OAK_ID = 140002
LOG_WILLOW_ID = 140003
LOG_MAPLE_ID = 140004
LOG_YEW_ID = 140005
LOG_TEAK_ID = 140006
LOG_MAHOGANY_ID = 140007
LOG_ANCIENT_ID = 140008
LOG_ASTRAL_ID = 140009
LOG_SPIRIT_ID = 140010
LOG_DARK_ID = 140011
LOG_LIGHT_ID = 140012
LOG_CELESTIAL_ID = 140013
LOG_BLOOD_ID = 140014

ORE_COPPER_ID = 140101
ORE_TIN_ID = 140102
ORE_IRON_ID = 140103
ORE_COAL_ID = 140104
ORE_TITANIUM_ID = 140105
ORE_MITHRIL_ID = 140106
ORE_ADAMANT_ID = 140107
ORE_ANCIENT_ID = 140108
#ORE_DRAGONITE_ID = 140109
#ORE_CELESTIAL_ID = 140110
ORE_SILVER_ID = 140111
ORE_GOLD_ID = 140112
ORE_PLATINUM_ID = 140113

### VALID HATCHETS FOR WOODCUTTING ###
HATCHETS = set([
    HATCHET_STONE_ID,
    HATCHET_BRONZE_ID,
    HATCHET_IRON_ID,
    HATCHET_STEEL_ID,
    HATCHET_TITANIUM_ID,
    HATCHET_MITHRIL_ID,
    HATCHET_ADAMANT_ID,
    HATCHET_ANCIENT_ID,
    HATCHET_ASTRAL_ID,
    HATCHET_DRAGONITE_ID,
    HATCHET_CELESTIAL_ID,
])


### BASIC ITEM FIELD IDs ###
NAME_INFO_FIELD = 0x101 # Dict mapping language ID to string.
# TYPE_FIELD = 0x102 # Int representing item type ID.
BASE_VALUE_LOW_FIELD = 0x103 # Int representing base value.
BASE_VALUE_HIGH_FIELD = 0x104 # Int representing base value.
TOOL_TYPE_FIELD = 0x105 # Int representing tool type ID.
IMAGE_PATH_DICT_FIELD = 0x106 # Maps image ID to image path.
DESCRIPTION_INFO_FIELD = 0x107 # Maps language ID to string.
USAGE_INFO_FIELD = 0x108 # Maps language ID to string.
WEIGHT_POINT_FIELD = 0x109 # Int representing weight points. 10 weight points = 1KG.
PROPERTIES_FIELD = 0x10A # Int representing OR-ed boolean flags.
INTERACTION_ID_FIELD = 0x10B # Int representing interaction ID for using this item.
# List of option IDs for this object. Default is [discard].
ITEM_OPTION_ID_LIST_FIELD = 0x10C

### FOR CREATABLE ITEMS ###
 # Dict mapping item IDs to number of items required to make this item.
CREATE_REQ_ITEMS_FIELD = 0x201

 # Dict mapping skill IDs to the level required to make this item.
CREATE_REQ_LEVELS_FIELD = 0x202

# List of quest IDs required to make this item.
CREATE_REQ_QUEST_FIELD = 0x203

### CONSUMABLE ITEM FIELD IDs ###
HEAL_VALUE_FIELD = 0x301 # Int.
SKILL_EFFECT_FIELD = 0x302 # Maps skill IDs to tuple (effect type ID, int).
CONSUME_COMBAT_BOOST_FIELD = 0x303 # Maps boost type ID to tuple (effect type ID, int).
CONSUME_QUEST_REQ_FIELD = 0x304 # List of quest IDs required to consume.

### EQUIPPABLE ITEM FIELD IDs ###
EQUIPMENT_SLOT_FIELD = 0x401 # Int representing equipment slot ID.
COMBAT_TYPE_FIELD = 0x402 # Int representing combat type for the item.
ATTACK_VALUE_INFO_FIELD = 0x403 # Maps damage type ID to int.
DEFENSE_VALUE_INFO_FIELD = 0x404 # Maps damage type ID to int.
EQUIP_COMBAT_BOOST_INFO_FIELD = 0x405 # Maps boost type ID to tuple (effect type ID, int).
EQUIP_LEVEL_REQ_FIELD = 0x406 # Dict mapping skill ID to required level.
EQUIP_QUEST_REQ_FIELD = 0x407 # List of quest IDs required to equip.

# For default equipment slot items.
EQUIPMENT_SLOT_DATA_INFO = {
    EQUIP_SLOT_HEAD: {
        NAME_INFO_FIELD: {
            language.LANG_ENGLISH: "Head Slot",
            language.LANG_ESPANOL: "Espacio de Cabeza",
        },
        BASE_VALUE_LOW_FIELD: 0,
        BASE_VALUE_HIGH_FIELD: 0,
        DESCRIPTION_INFO_FIELD: {
            language.LANG_ENGLISH: "For helmets, hats, and other headgear.",
            language.LANG_ESPANOL: "Para yelmos, sombreros, y otros tocados.",
        },
        WEIGHT_POINT_FIELD: 0,
        PROPERTIES_FIELD: 0,
        ITEM_OPTION_ID_LIST_FIELD: None,
        IMAGE_PATH_DICT_FIELD: {
            imagepaths.EQUIPMENT_ICON_HEAD_PATH,
        },
    },
    EQUIP_SLOT_MAIN_HAND: {
        NAME_INFO_FIELD: {
            language.LANG_ENGLISH: "Main Hand Slot",
            language.LANG_ESPANOL: "Espacio de Brazo Principal",
        },
        BASE_VALUE_LOW_FIELD: 0,
        BASE_VALUE_HIGH_FIELD: 0,
        DESCRIPTION_INFO_FIELD: {
            language.LANG_ENGLISH: "For swords, bows, staffs, and other weapons.",
            language.LANG_ESPANOL: "Para espadas, arcos, bastones, y otras armas.",
        },
        WEIGHT_POINT_FIELD: 0,
        PROPERTIES_FIELD: 0,
        ITEM_OPTION_ID_LIST_FIELD: None,
        IMAGE_PATH_DICT_FIELD: {
            imagepaths.EQUIPMENT_ICON_MAIN_HAND_PATH,
        },
    },
    EQUIP_SLOT_OFF_HAND: {
        NAME_INFO_FIELD: {
            language.LANG_ENGLISH: "Off Hand Slot",
            language.LANG_ESPANOL: "Espacio de Secundario",
        },
        BASE_VALUE_LOW_FIELD: 0,
        BASE_VALUE_HIGH_FIELD: 0,
        DESCRIPTION_INFO_FIELD: {
            language.LANG_ENGLISH: "For shields and secondary weapons.",
            language.LANG_ESPANOL: "Para escudos y armas secundarias.",
        },
        WEIGHT_POINT_FIELD: 0,
        PROPERTIES_FIELD: 0,
        ITEM_OPTION_ID_LIST_FIELD: None,
        IMAGE_PATH_DICT_FIELD: {
            imagepaths.EQUIPMENT_ICON_OFF_HAND_PATH,
        },
    },
    EQUIP_SLOT_MAIN_BODY: {
        NAME_INFO_FIELD: {
            language.LANG_ENGLISH: "Torso Slot",
            language.LANG_ESPANOL: "Espacio de Torso",
        },
        BASE_VALUE_LOW_FIELD: 0,
        BASE_VALUE_HIGH_FIELD: 0,
        DESCRIPTION_INFO_FIELD: {
            language.LANG_ENGLISH: "For clothing and armour for the torso.",
            language.LANG_ESPANOL: "Para ropa y armadura para el torso.",
        },
        WEIGHT_POINT_FIELD: 0,
        PROPERTIES_FIELD: 0,
        ITEM_OPTION_ID_LIST_FIELD: None,
        IMAGE_PATH_DICT_FIELD: {
            imagepaths.EQUIPMENT_ICON_BODY_PATH,
        },
    },
    EQUIP_SLOT_LEGS: {
        NAME_INFO_FIELD: {
            language.LANG_ENGLISH: "Legs Slot",
            language.LANG_ESPANOL: "Espacio de Piernas",
        },
        BASE_VALUE_LOW_FIELD: 0,
        BASE_VALUE_HIGH_FIELD: 0,
        DESCRIPTION_INFO_FIELD: {
            language.LANG_ENGLISH: "For clothing and armour for the legs.",
            language.LANG_ESPANOL: "Para ropa y armadura para las piernas.",
        },
        WEIGHT_POINT_FIELD: 0,
        PROPERTIES_FIELD: 0,
        ITEM_OPTION_ID_LIST_FIELD: None,
        IMAGE_PATH_DICT_FIELD: {
            imagepaths.EQUIPMENT_ICON_LEGS_PATH,
        },
    },
    EQUIP_SLOT_NECK: {
        NAME_INFO_FIELD: {
            language.LANG_ENGLISH: "Neck Slot",
            language.LANG_ESPANOL: "Espacio de Cuello",
        },
        BASE_VALUE_LOW_FIELD: 0,
        BASE_VALUE_HIGH_FIELD: 0,
        DESCRIPTION_INFO_FIELD: {
            language.LANG_ENGLISH: "For necklaces and other neck items.",
            language.LANG_ESPANOL: "Para collares y otras cosas para el cuello.",
        },
        WEIGHT_POINT_FIELD: 0,
        PROPERTIES_FIELD: 0,
        ITEM_OPTION_ID_LIST_FIELD: None,
        IMAGE_PATH_DICT_FIELD: {
            imagepaths.EQUIPMENT_ICON_NECK_PATH,
        },
    },
    EQUIP_SLOT_AMMO: {
        NAME_INFO_FIELD: {
            language.LANG_ENGLISH: "Ammo Slot",
            language.LANG_ESPANOL: "Espacio de Munición",
        },
        BASE_VALUE_LOW_FIELD: 0,
        BASE_VALUE_HIGH_FIELD: 0,
        DESCRIPTION_INFO_FIELD: {
            language.LANG_ENGLISH: "For arrows and other types of ammunition.",
            language.LANG_ESPANOL: "Para las flechas y otros tipos de munición.",
        },
        WEIGHT_POINT_FIELD: 0,
        PROPERTIES_FIELD: 0,
        ITEM_OPTION_ID_LIST_FIELD: None,
        IMAGE_PATH_DICT_FIELD: {
            imagepaths.EQUIPMENT_ICON_AMMO_PATH,
        },
    },
    EQUIP_SLOT_HANDS: {
        NAME_INFO_FIELD: {
            language.LANG_ENGLISH: "Hands Slot",
            language.LANG_ESPANOL: "Espacio de Manos",
        },
        BASE_VALUE_LOW_FIELD: 0,
        BASE_VALUE_HIGH_FIELD: 0,
        DESCRIPTION_INFO_FIELD: {
            language.LANG_ENGLISH: "For gloves and other hand gear.",
            language.LANG_ESPANOL: "Para guantes y otras equipo para las manos.",
        },
        WEIGHT_POINT_FIELD: 0,
        PROPERTIES_FIELD: 0,
        ITEM_OPTION_ID_LIST_FIELD: None,
        IMAGE_PATH_DICT_FIELD: {
            imagepaths.EQUIPMENT_ICON_HANDS_PATH,
        },
    },
    EQUIP_SLOT_FEET: {
        NAME_INFO_FIELD: {
            language.LANG_ENGLISH: "Feet Slot",
            language.LANG_ESPANOL: "Espacio de Pies",
        },
        BASE_VALUE_LOW_FIELD: 0,
        BASE_VALUE_HIGH_FIELD: 0,
        DESCRIPTION_INFO_FIELD: {
            language.LANG_ENGLISH: "For boots, shoes, and other footwear.",
            language.LANG_ESPANOL: "Para botas, zapatos, y otros calzados.",
        },
        WEIGHT_POINT_FIELD: 0,
        PROPERTIES_FIELD: 0,
        ITEM_OPTION_ID_LIST_FIELD: None,
        IMAGE_PATH_DICT_FIELD: {
            imagepaths.EQUIPMENT_ICON_FEET_PATH,
        },
    },
    EQUIP_SLOT_RING: {
        NAME_INFO_FIELD: {
            language.LANG_ENGLISH: "Ring Slot",
            language.LANG_ESPANOL: "Espacio de Anillos",
        },
        BASE_VALUE_LOW_FIELD: 0,
        BASE_VALUE_HIGH_FIELD: 0,
        DESCRIPTION_INFO_FIELD: {
            language.LANG_ENGLISH: "For rings.",
            language.LANG_ESPANOL: "Para anillos.",
        },
        WEIGHT_POINT_FIELD: 0,
        PROPERTIES_FIELD: 0,
        ITEM_OPTION_ID_LIST_FIELD: None,
        IMAGE_PATH_DICT_FIELD: {
            imagepaths.EQUIPMENT_ICON_RING_PATH,
        },
    },
    EQUIP_SLOT_BACK: {
        NAME_INFO_FIELD: {
            language.LANG_ENGLISH: "Back Slot.",
            language.LANG_ESPANOL: "Espacio de Espalda",
        },
        BASE_VALUE_LOW_FIELD: 0,
        BASE_VALUE_HIGH_FIELD: 0,
        DESCRIPTION_INFO_FIELD: {
            language.LANG_ENGLISH: "For capes and other items that go on the back.",
            language.LANG_ESPANOL: "Para capas y otras cosas para la espalda.",
        },
        WEIGHT_POINT_FIELD: 0,
        PROPERTIES_FIELD: 0,
        ITEM_OPTION_ID_LIST_FIELD: None,
        IMAGE_PATH_DICT_FIELD: {
            imagepaths.EQUIPMENT_ICON_BACK_PATH,
        },
    },
    EQUIP_SLOT_WRIST: {
        NAME_INFO_FIELD: {
            language.LANG_ENGLISH: "Wrist Slot",
            language.LANG_ESPANOL: "Espacio de Muñeca",
        },
        BASE_VALUE_LOW_FIELD: 0,
        BASE_VALUE_HIGH_FIELD: 0,
        DESCRIPTION_INFO_FIELD: {
            language.LANG_ENGLISH: "For bracelets and other wrist items.",
            language.LANG_ESPANOL: "Para pulseras y otras cosas para la muñeca.",
        },
        WEIGHT_POINT_FIELD: 0,
        PROPERTIES_FIELD: 0,
        ITEM_OPTION_ID_LIST_FIELD: None,
        IMAGE_PATH_DICT_FIELD: {
            imagepaths.EQUIPMENT_ICON_WRIST_PATH,
        },
    },
}


# For items that are not consumable nor equippable.
STANDARD_ITEM_DATA = {
    CURRENCY_GOLD_COIN_ID: {
        NAME_INFO_FIELD: {
            language.LANG_ENGLISH: "Gold Coins",
            language.LANG_ESPANOL: "Monedas de Oro",
        },
        BASE_VALUE_LOW_FIELD: 0,
        BASE_VALUE_HIGH_FIELD: 0,
        DESCRIPTION_INFO_FIELD: {
            language.LANG_ENGLISH: "Shiny gold coins!",
            language.LANG_ESPANOL: "Brillante monedas de oro!",
        },
        USAGE_INFO_FIELD: {
            language.LANG_ENGLISH: "I can use this to buy items.",
            language.LANG_ESPANOL: "Se sirven para comprar cosas.",
        },
        WEIGHT_POINT_FIELD: 0,
        PROPERTIES_FIELD: STACKABLE_F,
        ITEM_OPTION_ID_LIST_FIELD: [menuoptions.DISCARD_OPTION_ID],
        IMAGE_PATH_DICT_FIELD: {
            imageids.ITEM_ICON_IMAGE_ID: imagepaths.GOLD_COINS_ICON_PATH,
        },
    },
    CURRENCY_SILVER_COIN_ID: {
        NAME_INFO_FIELD: {
            language.LANG_ENGLISH: "Silver Coins",
            language.LANG_ESPANOL: "Monedas de Plata",
        },
        BASE_VALUE_LOW_FIELD: 0,
        BASE_VALUE_HIGH_FIELD: 0,
        DESCRIPTION_INFO_FIELD: {
            language.LANG_ENGLISH: "Not worth as much as gold, but they'll do.",
            language.LANG_ESPANOL: "Valen menos que oro, pero son suficientes.",
        },
        USAGE_INFO_FIELD: {
            language.LANG_ENGLISH: "I can use this to buy items.",
            language.LANG_ESPANOL: "Se sirven para comprar cosas.",
        },
        WEIGHT_POINT_FIELD: 0,
        PROPERTIES_FIELD: STACKABLE_F,
        ITEM_OPTION_ID_LIST_FIELD: [menuoptions.DISCARD_OPTION_ID],
        IMAGE_PATH_DICT_FIELD: {
            imageids.ITEM_ICON_IMAGE_ID: imagepaths.SILVER_COINS_ICON_PATH,
        },
    },
    CURRENCY_TRADING_STICKS_ID: {
        NAME_INFO_FIELD: {
            language.LANG_ENGLISH: "Trading Sticks",
            language.LANG_ESPANOL: "Palos de Comercio",
        },
        BASE_VALUE_LOW_FIELD: 0,
        BASE_VALUE_HIGH_FIELD: 0,
        DESCRIPTION_INFO_FIELD: {
            language.LANG_ENGLISH: "People still use this for trading?",
            language.LANG_ESPANOL: "Todavia se usan estos para el comercio?",
        },
        USAGE_INFO_FIELD: {
            language.LANG_ENGLISH: "I can use this to buy items.",
            language.LANG_ESPANOL: "Se sirven para comprar cosas.",
        },
        WEIGHT_POINT_FIELD: 0,
        PROPERTIES_FIELD: STACKABLE_F,
        ITEM_OPTION_ID_LIST_FIELD: [menuoptions.DISCARD_OPTION_ID],
        IMAGE_PATH_DICT_FIELD: {

        },
    },
    CURRENCY_YEN_ID: {
        NAME_INFO_FIELD: {
            language.LANG_ENGLISH: "Yen",
            language.LANG_ESPANOL: "Yen",
        },
        BASE_VALUE_LOW_FIELD: 0,
        BASE_VALUE_HIGH_FIELD: 0,
        DESCRIPTION_INFO_FIELD: {
            language.LANG_ENGLISH: "Some foreign currency.",
            language.LANG_ESPANOL: "Moneda extranjera.",
        },
        USAGE_INFO_FIELD: {
            language.LANG_ENGLISH: "I can use this to buy items.",
            language.LANG_ESPANOL: "Se sirven para comprar cosas.",
        },
        WEIGHT_POINT_FIELD: 0,
        PROPERTIES_FIELD: STACKABLE_F,
        ITEM_OPTION_ID_LIST_FIELD: [menuoptions.DISCARD_OPTION_ID],
        IMAGE_PATH_DICT_FIELD: {

        },
    },
    HAMMER_NORMAL_ID: {
        NAME_INFO_FIELD: {
            language.LANG_ENGLISH: "Hammer",
            language.LANG_ESPANOL: "Martillo",
        },
        BASE_VALUE_LOW_FIELD: 0,
        BASE_VALUE_HIGH_FIELD: 0,
        DESCRIPTION_INFO_FIELD: {
            language.LANG_ENGLISH: "A normal hammer.",
            language.LANG_ESPANOL: "Un martillo tipico.",
        },
        USAGE_INFO_FIELD: {
            language.LANG_ENGLISH: "I could use this to build things.",
            language.LANG_ESPANOL: "Puede servir para construir cosas.",
        },
        WEIGHT_POINT_FIELD: 10,
        PROPERTIES_FIELD: TOOL_ITEM_F,
        ITEM_OPTION_ID_LIST_FIELD: [],
        IMAGE_PATH_DICT_FIELD: {
            imageids.ITEM_ICON_IMAGE_ID: imagepaths.HAMMER_NORMAL_ICON_PATH,
        },
    },
    KNIFE_ID: {
        NAME_INFO_FIELD: {
            language.LANG_ENGLISH: "Knife",
            language.LANG_ESPANOL: "Cuchillo",
        },
        BASE_VALUE_LOW_FIELD: 0,
        BASE_VALUE_HIGH_FIELD: 0,
        DESCRIPTION_INFO_FIELD: {
            language.LANG_ENGLISH: "A normal knife.",
            language.LANG_ESPANOL: "Un cuchillo tipico.",
        },
        USAGE_INFO_FIELD: {
            language.LANG_ENGLISH: "I could use this to cut things.",
            language.LANG_ESPANOL: "Puede servir para cortar cosas.",
        },
        WEIGHT_POINT_FIELD: 5,
        PROPERTIES_FIELD: TOOL_ITEM_F,
        ITEM_OPTION_ID_LIST_FIELD: [],
        IMAGE_PATH_DICT_FIELD: {
            imageids.ITEM_ICON_IMAGE_ID: imagepaths.KNIFE_NORMAL_ICON_PATH,
        },
    },
    TINDERBOX_ID: {
        NAME_INFO_FIELD: {
            language.LANG_ENGLISH: "Tinderbox",
            language.LANG_ESPANOL: "Fosforos",
        },
        BASE_VALUE_LOW_FIELD: 0,
        BASE_VALUE_HIGH_FIELD: 0,
        DESCRIPTION_INFO_FIELD: {
            language.LANG_ENGLISH: "A box of matches.",
            language.LANG_ESPANOL: "Una caja de fosforos.",
        },
        USAGE_INFO_FIELD: {
            language.LANG_ENGLISH: "I could use this to make fire.",
            language.LANG_ESPANOL: "Puede servir para prender una hoguera.",
        },
        WEIGHT_POINT_FIELD: 2,
        PROPERTIES_FIELD: TOOL_ITEM_F,
        ITEM_OPTION_ID_LIST_FIELD: [],
        IMAGE_PATH_DICT_FIELD: {
            imageids.ITEM_ICON_IMAGE_ID: imagepaths.TINDERBOX_ICON_PATH,
        },
    },
    NEEDLE_ID: {
        NAME_INFO_FIELD: {
            language.LANG_ENGLISH: "Needle",
            language.LANG_ESPANOL: "Aguja",
        },
        BASE_VALUE_LOW_FIELD: 0,
        BASE_VALUE_HIGH_FIELD: 0,
        DESCRIPTION_INFO_FIELD: {
            language.LANG_ENGLISH: "It's pointy!",
            language.LANG_ESPANOL: "Que puntiaguda!.",
        },
        USAGE_INFO_FIELD: {
            language.LANG_ENGLISH: "I could use this to sew fabric.",
            language.LANG_ESPANOL: "Puede servir para coser teijdo.",
        },
        WEIGHT_POINT_FIELD: 0,
        PROPERTIES_FIELD: TOOL_ITEM_F,
        ITEM_OPTION_ID_LIST_FIELD: [],
        IMAGE_PATH_DICT_FIELD: {
            imageids.ITEM_ICON_IMAGE_ID: imagepaths.NEEDLE_ICON_PATH,
        },
    },
    LOG_TREE_ID: {
        NAME_INFO_FIELD: {
            language.LANG_ENGLISH: "Log",
            language.LANG_ESPANOL: "Lena",
        },
        BASE_VALUE_LOW_FIELD: 3,
        BASE_VALUE_HIGH_FIELD: 5,
        DESCRIPTION_INFO_FIELD: {
            language.LANG_ENGLISH: "Some logs from a tree.",
            language.LANG_ESPANOL: "Lena de un arbol.",
        },
        USAGE_INFO_FIELD: {
            language.LANG_ENGLISH: "I could use this to make a fire or crafting.",
            language.LANG_ESPANOL: "Puede servir para una fogata o para la artesania.",
        },
        WEIGHT_POINT_FIELD: 10,
        PROPERTIES_FIELD: (SELLABLE_F | ALCHABLE_F),
        ITEM_OPTION_ID_LIST_FIELD: menuoptions.DEFAULT_LOG_OPTION_ID_LIST,
        IMAGE_PATH_DICT_FIELD: {
            imageids.ITEM_ICON_IMAGE_ID: imagepaths.LOG_NORMAL_ICON_PATH,
        },
    },
    LOG_OAK_ID: {
        NAME_INFO_FIELD: {
            language.LANG_ENGLISH: "Oak Log",
            language.LANG_ESPANOL: "Lena de Roble",
        },
        BASE_VALUE_LOW_FIELD: 6,
        BASE_VALUE_HIGH_FIELD: 12,
        DESCRIPTION_INFO_FIELD: {
            language.LANG_ENGLISH: "Some oak logs.",
            language.LANG_ESPANOL: "Lena de un roble.",
        },
        USAGE_INFO_FIELD: {
            language.LANG_ENGLISH: "I could use this to make a fire or for crafting.",
            language.LANG_ESPANOL: "Puede servir para una fogata o para la artesania.",
        },
        WEIGHT_POINT_FIELD: 10,
        PROPERTIES_FIELD: (SELLABLE_F | ALCHABLE_F),
        ITEM_OPTION_ID_LIST_FIELD: menuoptions.DEFAULT_LOG_OPTION_ID_LIST,
        IMAGE_PATH_DICT_FIELD: {
            imageids.ITEM_ICON_IMAGE_ID: imagepaths.LOG_OAK_ICON_PATH,
        },
    },
    LOG_WILLOW_ID: {
        NAME_INFO_FIELD: {
            language.LANG_ENGLISH: "Willow Log",
            language.LANG_ESPANOL: "Lena de Sauce",
        },
        BASE_VALUE_LOW_FIELD: 25,
        BASE_VALUE_HIGH_FIELD: 50,
        DESCRIPTION_INFO_FIELD: {
            language.LANG_ENGLISH: "Some willow logs.",
            language.LANG_ESPANOL: "Lena de un sauce.",
        },
        USAGE_INFO_FIELD: {
            language.LANG_ENGLISH: "I could use this to make a fire or for crafting.",
            language.LANG_ESPANOL: "Puede servir para una fogata o para la artesania.",
        },
        WEIGHT_POINT_FIELD: 10,
        PROPERTIES_FIELD: (SELLABLE_F | ALCHABLE_F),
        ITEM_OPTION_ID_LIST_FIELD: menuoptions.DEFAULT_LOG_OPTION_ID_LIST,
        IMAGE_PATH_DICT_FIELD: {
            imageids.ITEM_ICON_IMAGE_ID: imagepaths.LOG_WILLOW_ICON_PATH,
        },
    },
    LOG_MAPLE_ID: {
        NAME_INFO_FIELD: {
            language.LANG_ENGLISH: "Maple Log",
            language.LANG_ESPANOL: "Lena de Arce",
        },
        BASE_VALUE_LOW_FIELD: 60,
        BASE_VALUE_HIGH_FIELD: 120,
        DESCRIPTION_INFO_FIELD: {
            language.LANG_ENGLISH: "Some maple logs.",
            language.LANG_ESPANOL: "Lena de un arce.",
        },
        USAGE_INFO_FIELD: {
            language.LANG_ENGLISH: "I could use this to make a fire or for crafting.",
            language.LANG_ESPANOL: "Puede servir para una fogata o para la artesania.",
        },
        WEIGHT_POINT_FIELD: 10,
        PROPERTIES_FIELD: (SELLABLE_F | ALCHABLE_F),
        ITEM_OPTION_ID_LIST_FIELD: menuoptions.DEFAULT_LOG_OPTION_ID_LIST,
        IMAGE_PATH_DICT_FIELD: {
            imageids.ITEM_ICON_IMAGE_ID: imagepaths.LOG_MAPLE_ICON_PATH,
        },
    },
}

# TODO set boost type IDs
# TODO set boost effect type IDs
# TODO set damage type IDs
