import skills
import language
import currency
import menuoptions
import imageids
import imagepaths
import viewingicondata
import equipmentdata

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
FISHING_ROD_ID = 10010
FISHING_NET_ID = 10011
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
PICKAXE_STONE_ID = 10302
PICKAXE_BRONZE_ID = 10303
PICKAXE_IRON_ID = 10304
PICKAXE_STEEL_ID = 10305
PICKAXE_TITANIUM_ID = 10306
PICKAXE_MITHRIL_ID = 10307
PICKAXE_ADAMANT_ID = 10308
PICKAXE_ANCIENT_ID = 10309
PICKAXE_ASTRAL_ID = 10310
PICKAXE_DRAGONITE_ID = 10311
PICKAXE_CELESTIAL_ID = 10312

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

### COOKABLE ITEMS 150000 TO 159999
FISH_RAW_TROUT_ID = 150001 # Freshwater.
FISH_RAW_CATFISH_ID = 150002 # Freshwater.
FISH_RAW_SHRIMP_ID = 150003 # Saltwater.
FISH_RAW_PERCH_ID = 150004 # Freshwater.
FISH_RAW_SALMON_ID = 150005 # Freshwater.
# sardines
# tilapia
# herring
# red snapper
# salmon
# swordfish/marlin
# tuna
# bluefin tuna
# shark
# mackerel
# pike
# bass
# sunfish
# barracuda
# squid
# octopus
# pufferfish
# eel

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

### VALID LOGS FOR LIGHTING FIRES ###
LIGHTABLE_LOGS = set([
    LOG_TREE_ID,
    LOG_OAK_ID,
    LOG_WILLOW_ID,
    LOG_MAPLE_ID,
    LOG_YEW_ID,
    LOG_TEAK_ID,
    LOG_MAHOGANY_ID,
    LOG_ANCIENT_ID,
    LOG_ASTRAL_ID,
    LOG_SPIRIT_ID,
    LOG_DARK_ID,
    LOG_LIGHT_ID,
    LOG_CELESTIAL_ID,
    LOG_BLOOD_ID,
])


# LEVELS FOR LIGHTING LOGS #
# TODO change.
LIGHTING_LOG_SKILL_MAPPING = {
    LOG_TREE_ID: 1,
    LOG_OAK_ID: 10,
    LOG_WILLOW_ID: 20,
    LOG_MAPLE_ID: 30,
    LOG_YEW_ID: 60,
    LOG_TEAK_ID: 40,
    LOG_MAHOGANY_ID: 50,
    LOG_ANCIENT_ID: 60,
    LOG_ASTRAL_ID: 70,
    LOG_SPIRIT_ID: 80,
    LOG_DARK_ID: 85,
    LOG_LIGHT_ID: 85,
    LOG_CELESTIAL_ID: 90,
    LOG_BLOOD_ID: 75,
}


### BASIC ITEM FIELD IDs ###

# TYPE_FIELD = 0x102 # Int representing item type ID.
BASE_VALUE_LOW_FIELD = 0x103 # Int representing base value.
BASE_VALUE_HIGH_FIELD = 0x104 # Int representing base value.
TOOL_TYPE_FIELD = 0x105 # Int representing tool type ID.
USAGE_INFO_FIELD = 0x108 # Maps language ID to string.
WEIGHT_POINT_FIELD = 0x109 # Int representing weight points. 10 weight points = 1KG.
PROPERTIES_FIELD = 0x10A # Int representing OR-ed boolean flags.
INTERACTION_ID_FIELD = 0x10B # Int representing interaction ID for using this item.

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
        viewingicondata.NAME_INFO_FIELD: {
            language.LANG_ENGLISH: "Gold Coins",
            language.LANG_ESPANOL: "Monedas de Oro",
        },
        BASE_VALUE_LOW_FIELD: 0,
        BASE_VALUE_HIGH_FIELD: 0,
        viewingicondata.DESCRIPTION_INFO_FIELD: {
            language.LANG_ENGLISH: "Shiny gold coins!",
            language.LANG_ESPANOL: "Brillante monedas de oro!",
        },
        USAGE_INFO_FIELD: {
            language.LANG_ENGLISH: "I can use this to buy items.",
            language.LANG_ESPANOL: "Se sirven para comprar cosas.",
        },
        WEIGHT_POINT_FIELD: 0,
        PROPERTIES_FIELD: STACKABLE_F,
        viewingicondata.OPTION_ID_LIST_FIELD: menuoptions.DEFAULT_STACKABLE_OPTION_ID_LIST,
        viewingicondata.IMAGE_PATH_DICT_FIELD: {
            imageids.ICON_IMAGE_ID: imagepaths.GOLD_COINS_ICON_PATH,
        },
    },
    CURRENCY_SILVER_COIN_ID: {
        viewingicondata.NAME_INFO_FIELD: {
            language.LANG_ENGLISH: "Silver Coins",
            language.LANG_ESPANOL: "Monedas de Plata",
        },
        BASE_VALUE_LOW_FIELD: 0,
        BASE_VALUE_HIGH_FIELD: 0,
        viewingicondata.DESCRIPTION_INFO_FIELD: {
            language.LANG_ENGLISH: "Not worth as much as gold, but they'll do.",
            language.LANG_ESPANOL: "Valen menos que oro, pero son suficientes.",
        },
        USAGE_INFO_FIELD: {
            language.LANG_ENGLISH: "I can use this to buy items.",
            language.LANG_ESPANOL: "Se sirven para comprar cosas.",
        },
        WEIGHT_POINT_FIELD: 0,
        PROPERTIES_FIELD: STACKABLE_F,
        viewingicondata.OPTION_ID_LIST_FIELD: menuoptions.DEFAULT_STACKABLE_OPTION_ID_LIST,
        viewingicondata.IMAGE_PATH_DICT_FIELD: {
            imageids.ICON_IMAGE_ID: imagepaths.SILVER_COINS_ICON_PATH,
        },
    },
    CURRENCY_TRADING_STICKS_ID: {
        viewingicondata.NAME_INFO_FIELD: {
            language.LANG_ENGLISH: "Trading Sticks",
            language.LANG_ESPANOL: "Palos de Comercio",
        },
        BASE_VALUE_LOW_FIELD: 0,
        BASE_VALUE_HIGH_FIELD: 0,
        viewingicondata.DESCRIPTION_INFO_FIELD: {
            language.LANG_ENGLISH: "People still use this for trading?",
            language.LANG_ESPANOL: "Todavia se usan estos para el comercio?",
        },
        USAGE_INFO_FIELD: {
            language.LANG_ENGLISH: "I can use this to buy items.",
            language.LANG_ESPANOL: "Se sirven para comprar cosas.",
        },
        WEIGHT_POINT_FIELD: 0,
        PROPERTIES_FIELD: STACKABLE_F,
        viewingicondata.OPTION_ID_LIST_FIELD: menuoptions.DEFAULT_STACKABLE_OPTION_ID_LIST,
        viewingicondata.IMAGE_PATH_DICT_FIELD: {

        },
    },
    CURRENCY_YEN_ID: {
        viewingicondata.NAME_INFO_FIELD: {
            language.LANG_ENGLISH: "Yen",
            language.LANG_ESPANOL: "Yen",
        },
        BASE_VALUE_LOW_FIELD: 0,
        BASE_VALUE_HIGH_FIELD: 0,
        viewingicondata.DESCRIPTION_INFO_FIELD: {
            language.LANG_ENGLISH: "Some foreign currency.",
            language.LANG_ESPANOL: "Moneda extranjera.",
        },
        USAGE_INFO_FIELD: {
            language.LANG_ENGLISH: "I can use this to buy items.",
            language.LANG_ESPANOL: "Se sirven para comprar cosas.",
        },
        WEIGHT_POINT_FIELD: 0,
        PROPERTIES_FIELD: STACKABLE_F,
        viewingicondata.OPTION_ID_LIST_FIELD: menuoptions.DEFAULT_STACKABLE_OPTION_ID_LIST,
        viewingicondata.IMAGE_PATH_DICT_FIELD: {

        },
    },
    HAMMER_NORMAL_ID: {
        viewingicondata.NAME_INFO_FIELD: {
            language.LANG_ENGLISH: "Hammer",
            language.LANG_ESPANOL: "Martillo",
        },
        BASE_VALUE_LOW_FIELD: 0,
        BASE_VALUE_HIGH_FIELD: 0,
        viewingicondata.DESCRIPTION_INFO_FIELD: {
            language.LANG_ENGLISH: "A normal hammer.",
            language.LANG_ESPANOL: "Un martillo tipico.",
        },
        USAGE_INFO_FIELD: {
            language.LANG_ENGLISH: "I could use this to build things.",
            language.LANG_ESPANOL: "Puede servir para construir cosas.",
        },
        WEIGHT_POINT_FIELD: 10,
        PROPERTIES_FIELD: TOOL_ITEM_F,
        viewingicondata.OPTION_ID_LIST_FIELD: [],
        viewingicondata.IMAGE_PATH_DICT_FIELD: {
            imageids.ICON_IMAGE_ID: imagepaths.HAMMER_NORMAL_ICON_PATH,
        },
    },
    KNIFE_ID: {
        viewingicondata.NAME_INFO_FIELD: {
            language.LANG_ENGLISH: "Knife",
            language.LANG_ESPANOL: "Cuchillo",
        },
        BASE_VALUE_LOW_FIELD: 0,
        BASE_VALUE_HIGH_FIELD: 0,
        viewingicondata.DESCRIPTION_INFO_FIELD: {
            language.LANG_ENGLISH: "A normal knife.",
            language.LANG_ESPANOL: "Un cuchillo tipico.",
        },
        USAGE_INFO_FIELD: {
            language.LANG_ENGLISH: "I could use this to cut things.",
            language.LANG_ESPANOL: "Puede servir para cortar cosas.",
        },
        WEIGHT_POINT_FIELD: 5,
        PROPERTIES_FIELD: TOOL_ITEM_F,
        viewingicondata.OPTION_ID_LIST_FIELD: [],
        viewingicondata.IMAGE_PATH_DICT_FIELD: {
            imageids.ICON_IMAGE_ID: imagepaths.KNIFE_NORMAL_ICON_PATH,
        },
    },
    TINDERBOX_ID: {
        viewingicondata.NAME_INFO_FIELD: {
            language.LANG_ENGLISH: "Tinderbox",
            language.LANG_ESPANOL: "Fosforos",
        },
        BASE_VALUE_LOW_FIELD: 0,
        BASE_VALUE_HIGH_FIELD: 0,
        viewingicondata.DESCRIPTION_INFO_FIELD: {
            language.LANG_ENGLISH: "A box of matches.",
            language.LANG_ESPANOL: "Una caja de fosforos.",
        },
        USAGE_INFO_FIELD: {
            language.LANG_ENGLISH: "I could use this to make fire.",
            language.LANG_ESPANOL: "Puede servir para prender una hoguera.",
        },
        WEIGHT_POINT_FIELD: 2,
        PROPERTIES_FIELD: TOOL_ITEM_F,
        viewingicondata.OPTION_ID_LIST_FIELD: [],
        viewingicondata.IMAGE_PATH_DICT_FIELD: {
            imageids.ICON_IMAGE_ID: imagepaths.TINDERBOX_ICON_PATH,
        },
    },
    NEEDLE_ID: {
        viewingicondata.NAME_INFO_FIELD: {
            language.LANG_ENGLISH: "Needle",
            language.LANG_ESPANOL: "Aguja",
        },
        BASE_VALUE_LOW_FIELD: 0,
        BASE_VALUE_HIGH_FIELD: 0,
        viewingicondata.DESCRIPTION_INFO_FIELD: {
            language.LANG_ENGLISH: "It's pointy!",
            language.LANG_ESPANOL: "Que puntiaguda!.",
        },
        USAGE_INFO_FIELD: {
            language.LANG_ENGLISH: "I could use this to sew fabric.",
            language.LANG_ESPANOL: "Puede servir para coser teijdo.",
        },
        WEIGHT_POINT_FIELD: 0,
        PROPERTIES_FIELD: TOOL_ITEM_F,
        viewingicondata.OPTION_ID_LIST_FIELD: [],
        viewingicondata.IMAGE_PATH_DICT_FIELD: {
            imageids.ICON_IMAGE_ID: imagepaths.NEEDLE_ICON_PATH,
        },
    },
    LOG_TREE_ID: {
        viewingicondata.NAME_INFO_FIELD: {
            language.LANG_ENGLISH: "Log",
            language.LANG_ESPANOL: "Lena",
        },
        BASE_VALUE_LOW_FIELD: 3,
        BASE_VALUE_HIGH_FIELD: 5,
        viewingicondata.DESCRIPTION_INFO_FIELD: {
            language.LANG_ENGLISH: "Some logs from a tree.",
            language.LANG_ESPANOL: "Lena de un arbol.",
        },
        USAGE_INFO_FIELD: {
            language.LANG_ENGLISH: "I could use this to make a fire or crafting.",
            language.LANG_ESPANOL: "Puede servir para una fogata o para la artesania.",
        },
        WEIGHT_POINT_FIELD: 10,
        PROPERTIES_FIELD: (SELLABLE_F | ALCHABLE_F),
        viewingicondata.OPTION_ID_LIST_FIELD: menuoptions.DEFAULT_LOG_OPTION_ID_LIST,
        viewingicondata.IMAGE_PATH_DICT_FIELD: {
            imageids.ICON_IMAGE_ID: imagepaths.LOG_NORMAL_ICON_PATH,
        },
    },
    LOG_OAK_ID: {
        viewingicondata.NAME_INFO_FIELD: {
            language.LANG_ENGLISH: "Oak Log",
            language.LANG_ESPANOL: "Lena de Roble",
        },
        BASE_VALUE_LOW_FIELD: 6,
        BASE_VALUE_HIGH_FIELD: 12,
        viewingicondata.DESCRIPTION_INFO_FIELD: {
            language.LANG_ENGLISH: "Some oak logs.",
            language.LANG_ESPANOL: "Lena de un roble.",
        },
        USAGE_INFO_FIELD: {
            language.LANG_ENGLISH: "I could use this to make a fire or for crafting.",
            language.LANG_ESPANOL: "Puede servir para una fogata o para la artesania.",
        },
        WEIGHT_POINT_FIELD: 10,
        PROPERTIES_FIELD: (SELLABLE_F | ALCHABLE_F),
        viewingicondata.OPTION_ID_LIST_FIELD: menuoptions.DEFAULT_LOG_OPTION_ID_LIST,
        viewingicondata.IMAGE_PATH_DICT_FIELD: {
            imageids.ICON_IMAGE_ID: imagepaths.LOG_OAK_ICON_PATH,
        },
    },
    LOG_WILLOW_ID: {
        viewingicondata.NAME_INFO_FIELD: {
            language.LANG_ENGLISH: "Willow Log",
            language.LANG_ESPANOL: "Lena de Sauce",
        },
        BASE_VALUE_LOW_FIELD: 25,
        BASE_VALUE_HIGH_FIELD: 50,
        viewingicondata.DESCRIPTION_INFO_FIELD: {
            language.LANG_ENGLISH: "Some willow logs.",
            language.LANG_ESPANOL: "Lena de un sauce.",
        },
        USAGE_INFO_FIELD: {
            language.LANG_ENGLISH: "I could use this to make a fire or for crafting.",
            language.LANG_ESPANOL: "Puede servir para una fogata o para la artesania.",
        },
        WEIGHT_POINT_FIELD: 10,
        PROPERTIES_FIELD: (SELLABLE_F | ALCHABLE_F),
        viewingicondata.OPTION_ID_LIST_FIELD: menuoptions.DEFAULT_LOG_OPTION_ID_LIST,
        viewingicondata.IMAGE_PATH_DICT_FIELD: {
            imageids.ICON_IMAGE_ID: imagepaths.LOG_WILLOW_ICON_PATH,
        },
    },
    LOG_MAPLE_ID: {
        viewingicondata.NAME_INFO_FIELD: {
            language.LANG_ENGLISH: "Maple Log",
            language.LANG_ESPANOL: "Lena de Arce",
        },
        BASE_VALUE_LOW_FIELD: 60,
        BASE_VALUE_HIGH_FIELD: 120,
        viewingicondata.DESCRIPTION_INFO_FIELD: {
            language.LANG_ENGLISH: "Some maple logs.",
            language.LANG_ESPANOL: "Lena de un arce.",
        },
        USAGE_INFO_FIELD: {
            language.LANG_ENGLISH: "I could use this to make a fire or for crafting.",
            language.LANG_ESPANOL: "Puede servir para una fogata o para la artesania.",
        },
        WEIGHT_POINT_FIELD: 10,
        PROPERTIES_FIELD: (SELLABLE_F | ALCHABLE_F),
        viewingicondata.OPTION_ID_LIST_FIELD: menuoptions.DEFAULT_LOG_OPTION_ID_LIST,
        viewingicondata.IMAGE_PATH_DICT_FIELD: {
            imageids.ICON_IMAGE_ID: imagepaths.LOG_MAPLE_ICON_PATH,
        },
    },
    ORE_COPPER_ID: {
        viewingicondata.NAME_INFO_FIELD: {
            language.LANG_ENGLISH: "Copper Ore",
            language.LANG_ESPANOL: "Mineral de Cobre",
        },
        BASE_VALUE_LOW_FIELD: 5,
        BASE_VALUE_HIGH_FIELD: 10,
        viewingicondata.DESCRIPTION_INFO_FIELD: {
            language.LANG_ENGLISH: "Pieces of copper core.",
            language.LANG_ESPANOL: "Es mineral de cobre.",
        },
        USAGE_INFO_FIELD: {
            language.LANG_ENGLISH: "I could use this to create and smith metals.",
            language.LANG_ESPANOL: "Puedo usar eso en la herrería.",
        },
        WEIGHT_POINT_FIELD: 10,
        PROPERTIES_FIELD: (SELLABLE_F | ALCHABLE_F),
        viewingicondata.OPTION_ID_LIST_FIELD: [menuoptions.DISCARD_OPTION_ID],
        viewingicondata.IMAGE_PATH_DICT_FIELD: {
            imageids.ICON_IMAGE_ID: imagepaths.ORE_COPPER_ICON_PATH,
        },
    },
    ORE_TIN_ID: {
        viewingicondata.NAME_INFO_FIELD: {
            language.LANG_ENGLISH: "Tin Ore",
            language.LANG_ESPANOL: "Mineral de Estaño",
        },
        BASE_VALUE_LOW_FIELD: 5,
        BASE_VALUE_HIGH_FIELD: 10,
        viewingicondata.DESCRIPTION_INFO_FIELD: {
            language.LANG_ENGLISH: "Pieces of tin ore.",
            language.LANG_ESPANOL: "Es mineral de estaño.",
        },
        USAGE_INFO_FIELD: {
            language.LANG_ENGLISH: "I could use this to create and smith metals.",
            language.LANG_ESPANOL: "Puedo usar eso en la herrería.",
        },
        WEIGHT_POINT_FIELD: 10,
        PROPERTIES_FIELD: (SELLABLE_F | ALCHABLE_F),
        viewingicondata.OPTION_ID_LIST_FIELD: [menuoptions.DISCARD_OPTION_ID],
        viewingicondata.IMAGE_PATH_DICT_FIELD: {
            imageids.ICON_IMAGE_ID: imagepaths.ORE_TIN_ICON_PATH,
        },
    },
    ORE_IRON_ID: {
        viewingicondata.NAME_INFO_FIELD: {
            language.LANG_ENGLISH: "Iron Ore",
            language.LANG_ESPANOL: "Mineral de Hierro",
        },
        BASE_VALUE_LOW_FIELD: 15,
        BASE_VALUE_HIGH_FIELD: 30,
        viewingicondata.DESCRIPTION_INFO_FIELD: {
            language.LANG_ENGLISH: "Pieces of iron ore.",
            language.LANG_ESPANOL: "Es mineral de hierro.",
        },
        USAGE_INFO_FIELD: {
            language.LANG_ENGLISH: "I could use this to create and smith metals.",
            language.LANG_ESPANOL: "Puedo usar eso en la herrería.",
        },
        WEIGHT_POINT_FIELD: 10,
        PROPERTIES_FIELD: (SELLABLE_F | ALCHABLE_F),
        viewingicondata.OPTION_ID_LIST_FIELD: [menuoptions.DISCARD_OPTION_ID],
        viewingicondata.IMAGE_PATH_DICT_FIELD: {
            imageids.ICON_IMAGE_ID: imagepaths.ORE_IRON_ICON_PATH,
        },
    },
    ORE_COAL_ID: {
        viewingicondata.NAME_INFO_FIELD: {
            language.LANG_ENGLISH: "Coal Ore",
            language.LANG_ESPANOL: "Mineral de Carbón",
        },
        BASE_VALUE_LOW_FIELD: 35,
        BASE_VALUE_HIGH_FIELD: 80,
        viewingicondata.DESCRIPTION_INFO_FIELD: {
            language.LANG_ENGLISH: "Pieces of coal.",
            language.LANG_ESPANOL: "Es mineral de carbón.",
        },
        USAGE_INFO_FIELD: {
            language.LANG_ENGLISH: "I could use this to create and smith metals.",
            language.LANG_ESPANOL: "Puedo usar eso en la herrería.",
        },
        WEIGHT_POINT_FIELD: 10,
        PROPERTIES_FIELD: (SELLABLE_F | ALCHABLE_F),
        viewingicondata.OPTION_ID_LIST_FIELD: [menuoptions.DISCARD_OPTION_ID],
        viewingicondata.IMAGE_PATH_DICT_FIELD: {
            imageids.ICON_IMAGE_ID: imagepaths.ORE_COAL_ICON_PATH,
        },
    },
    ORE_SILVER_ID: {
        viewingicondata.NAME_INFO_FIELD: {
            language.LANG_ENGLISH: "Silver Ore",
            language.LANG_ESPANOL: "Mineral de Plata",
        },
        BASE_VALUE_LOW_FIELD: 40,
        BASE_VALUE_HIGH_FIELD: 100,
        viewingicondata.DESCRIPTION_INFO_FIELD: {
            language.LANG_ENGLISH: "Pieces of silver ore.",
            language.LANG_ESPANOL: "Es mineral de plata.",
        },
        USAGE_INFO_FIELD: {
            language.LANG_ENGLISH: "I could use this to create and smith metals.",
            language.LANG_ESPANOL: "Puedo usar eso en la herrería.",
        },
        WEIGHT_POINT_FIELD: 10,
        PROPERTIES_FIELD: (SELLABLE_F | ALCHABLE_F),
        viewingicondata.OPTION_ID_LIST_FIELD: [menuoptions.DISCARD_OPTION_ID],
        viewingicondata.IMAGE_PATH_DICT_FIELD: {
            imageids.ICON_IMAGE_ID: imagepaths.ORE_SILVER_ICON_PATH,
        },
    },
    ORE_GOLD_ID: {
        viewingicondata.NAME_INFO_FIELD: {
            language.LANG_ENGLISH: "Gold Ore",
            language.LANG_ESPANOL: "Mineral de Oro",
        },
        BASE_VALUE_LOW_FIELD: 100,
        BASE_VALUE_HIGH_FIELD: 200,
        viewingicondata.DESCRIPTION_INFO_FIELD: {
            language.LANG_ENGLISH: "Pieces of gold ore.",
            language.LANG_ESPANOL: "Es mineral de oro.",
        },
        USAGE_INFO_FIELD: {
            language.LANG_ENGLISH: "I could use this to create and smith metals.",
            language.LANG_ESPANOL: "Puedo usar eso en la herrería.",
        },
        WEIGHT_POINT_FIELD: 10,
        PROPERTIES_FIELD: (SELLABLE_F | ALCHABLE_F),
        viewingicondata.OPTION_ID_LIST_FIELD: [menuoptions.DISCARD_OPTION_ID],
        viewingicondata.IMAGE_PATH_DICT_FIELD: {
            imageids.ICON_IMAGE_ID: imagepaths.ORE_GOLD_ICON_PATH,
        },
    },
    ORE_TITANIUM_ID: {
        viewingicondata.NAME_INFO_FIELD: {
            language.LANG_ENGLISH: "Titanium Ore",
            language.LANG_ESPANOL: "Mineral de Titanio",
        },
        BASE_VALUE_LOW_FIELD: 110,
        BASE_VALUE_HIGH_FIELD: 250,
        viewingicondata.DESCRIPTION_INFO_FIELD: {
            language.LANG_ENGLISH: "Pieces of titanium ore.",
            language.LANG_ESPANOL: "Es mineral de titanio.",
        },
        USAGE_INFO_FIELD: {
            language.LANG_ENGLISH: "I could use this to create and smith metals.",
            language.LANG_ESPANOL: "Puedo usar eso en la herrería.",
        },
        WEIGHT_POINT_FIELD: 10,
        PROPERTIES_FIELD: (SELLABLE_F | ALCHABLE_F),
        viewingicondata.OPTION_ID_LIST_FIELD: [menuoptions.DISCARD_OPTION_ID],
        viewingicondata.IMAGE_PATH_DICT_FIELD: {
            imageids.ICON_IMAGE_ID: imagepaths.ORE_TITANIUM_ICON_PATH,
        },
    },
    FISH_RAW_TROUT_ID: {
        viewingicondata.NAME_INFO_FIELD: {
            language.LANG_ENGLISH: "Trout",
            language.LANG_ESPANOL: "Trucha",
        },
        BASE_VALUE_LOW_FIELD: 15,
        BASE_VALUE_HIGH_FIELD: 30,
        viewingicondata.DESCRIPTION_INFO_FIELD: {
            language.LANG_ENGLISH: "It's a raw trout.",
            language.LANG_ESPANOL: "Es trucha cruda.",
        },
        USAGE_INFO_FIELD: {
            language.LANG_ENGLISH: "I could cook this.",
            language.LANG_ESPANOL: "Puedo cocinar esto.",
        },
        WEIGHT_POINT_FIELD: 1,
        PROPERTIES_FIELD: (SELLABLE_F | ALCHABLE_F),
        viewingicondata.OPTION_ID_LIST_FIELD: [menuoptions.DISCARD_OPTION_ID],
        viewingicondata.IMAGE_PATH_DICT_FIELD: {
            imageids.ICON_IMAGE_ID: imagepaths.FISH_RAW_TROUT_ICON_PATH,
        },
    },
    FISH_RAW_SALMON_ID: {
        viewingicondata.NAME_INFO_FIELD: {
            language.LANG_ENGLISH: "Salmon",
            language.LANG_ESPANOL: "Salmón",
        },
        BASE_VALUE_LOW_FIELD: 23,
        BASE_VALUE_HIGH_FIELD: 50,
        viewingicondata.DESCRIPTION_INFO_FIELD: {
            language.LANG_ENGLISH: "It's fresh, raw salmon.",
            language.LANG_ESPANOL: "Es salmón fresco y crudo.",
        },
        USAGE_INFO_FIELD: {
            language.LANG_ENGLISH: "I could cook this.",
            language.LANG_ESPANOL: "Puedo cocinar esto.",
        },
        WEIGHT_POINT_FIELD: 1,
        PROPERTIES_FIELD: (SELLABLE_F | ALCHABLE_F),
        viewingicondata.OPTION_ID_LIST_FIELD: [menuoptions.DISCARD_OPTION_ID],
        viewingicondata.IMAGE_PATH_DICT_FIELD: {
            imageids.ICON_IMAGE_ID: imagepaths.FISH_RAW_SALMON_ICON_PATH,
        },
    },
    FISH_RAW_PERCH_ID: {
        viewingicondata.NAME_INFO_FIELD: {
            language.LANG_ENGLISH: "Perch",
            language.LANG_ESPANOL: "Perca",
        },
        BASE_VALUE_LOW_FIELD: 7,
        BASE_VALUE_HIGH_FIELD: 15,
        viewingicondata.DESCRIPTION_INFO_FIELD: {
            language.LANG_ENGLISH: "It's fresh, raw perch.",
            language.LANG_ESPANOL: "Es perca fresca y cruda.",
        },
        USAGE_INFO_FIELD: {
            language.LANG_ENGLISH: "I could cook this.",
            language.LANG_ESPANOL: "Puedo cocinar esto.",
        },
        WEIGHT_POINT_FIELD: 1,
        PROPERTIES_FIELD: (SELLABLE_F | ALCHABLE_F),
        viewingicondata.OPTION_ID_LIST_FIELD: [menuoptions.DISCARD_OPTION_ID],
        viewingicondata.IMAGE_PATH_DICT_FIELD: {
            imageids.ICON_IMAGE_ID: imagepaths.FISH_RAW_PERCH_ICON_PATH,
        },
    },
}

# TODO set boost type IDs
# TODO set boost effect type IDs
# TODO set damage type IDs
