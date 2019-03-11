import skills
import language
import currency
import menuoptions
import imageids
import imagepaths

ITEM_ICON_SIZE = 50

### ITEM PROPERTY FLAGS ###
STACKABLE_F = 0x1
SELLABLE_F = 0x2
CONSUMABLE_F = 0x4
QUEST_ITEM_F = 0x8 # Special quest-related item that shouldn't be sold or destroyed.
ALCHABLE_F = 0x10
COOKABLE_FIRE = 0x20
COOKABLE_RANGE = 0x40

### EQUIPMENT SLOT ID VALUES ###
EQUIP_SLOT_NONE = 0x0 # Not equippable
EQUIP_SLOT_HEAD = 0x1 # Helmets, hats, etc.
EQUIP_SLOT_MAIN_HAND = 0x2 # Weapons.
EQUIP_SLOT_OFF_HAND = 0x3 # Shields.
EQUIP_SLOT_MAIN_BODY = 0x4 # Plate armour, chainmail, etc.
EQUIP_SLOT_NECK = 0x5 # Amulets, necklaces, etc.
EQUIP_SLOT_AMMO = 0x6 # Arrows, etc.
EQUIP_SLOT_HANDS = 0x7 # Gloves, bracelets, etc.
EQUIP_SLOT_FEET = 0x8 # Boots, etc.
EQUIP_SLOT_RING = 0x9 # Rings.

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
HAMMER_STONE_ID = 10102
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
HATCHET_MASTER_ID = 10212
HATCHET_CELESTIAL_ID = 10213

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
DAGGER_MASTER_ID = 50012
DAGGER_CELESTIAL_ID = 50013
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
SWORD_MASTER_ID = 50112
SWORD_CELESTIAL_ID = 50113
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
BATTLEAXE_MASTER_ID = 50212
BATTLEAXE_CELESTIAL_ID = 50213
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
BROADSWORD_MASTER_ID = 50312
BROADSWORD_CELESTIAL_ID = 50313
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
ARROW_MASTER_ID = 50412
ARROW_CELESTIAL_ID = 50413
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

ORE_COPPER_ID = 140101
ORE_TIN_ID = 140102
ORE_IRON_ID = 140103
ORE_COAL_ID = 140104
ORE_TITANIUM_ID = 140105
ORE_MITHRIL_ID = 140106
ORE_ADAMANT_ID = 140107
ORE_ANCIENT_ID = 140108
ORE_DRAGONITE_ID = 140109
ORE_CELESTIAL_ID = 140110
ORE_SILVER_ID = 140111
ORE_GOLD_ID = 140112
ORE_PLATINUM_ID = 140113

### VALID HATCHETS FOR WOODCUTTING ###
HATCHETS = set([
    HATCHET_BRONZE_ID,

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
    LOG_TREE_ID: {
        NAME_INFO_FIELD: {
            language.LANG_ENGLISH: "LOG",
            language.LANG_ESPANOL: "LENA",
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
            language.LANG_ENGLISH: "OAK LOG",
            language.LANG_ESPANOL: "LENA DE ROBLE",
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
    },
}

# TODO set boost type IDs
# TODO set boost effect type IDs
# TODO set damage type IDs
