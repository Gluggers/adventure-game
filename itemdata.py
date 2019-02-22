import skills
import language
import currency
import objdata

### ITEM TYPE ID NUMBERS ###
"""
ITEM_TYPE_WEAPON = 0x1
ITEM_TYPE_ARMOUR = 0x2
ITEM_TYPE_CLOTHES = 0x3
ITEM_TYPE_RESOURCE = 0x4
ITEM_TYPE_FOOD = 0x5
ITEM_TYPE_MISC = 0xF
"""

### ITEM TOOL TYPE ID NUMBERS ###
"""
TOOL_TYPE_NONE = 0x0 # Not a tool.
TOOL_TYPE_PICKAXE = 0x1
TOOL_TYPE_HATCHET = 0x2
TOOL_TYPE_KNIFE = 0x3
TOOL_TYPE_HAMMER = 0x4
TOOL_TYPE_NEEDLE = 0x5
"""

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

# SPECIAL ITEMS 0x00001 TO 0x0FFFF

# TOOLS 0x10000 TO 0x1FFFF
KNIFE_ID = 0x10001 # 65537
TINDERBOX_ID = 0x10002 # 65538
NEEDLE_ID = 0x10003 # 65539
HAMMER_STONE_ID = 0x10102
HATCHET_STONE_ID = 0x10202
HATCHET_BRONZE_ID = 0x10203
HATCHET_IRON_ID = 0x10204
HATCHET_STEEL_ID = 0x10205
HATCHET_TITANIUM_ID = 0x10206
HATCHET_MITHRIL_ID = 0x10207
HATCHET_ADAMANT_ID = 0x10208
HATCHET_ANCIENT_ID = 0x10209
HATCHET_ASTRAL_ID = 0x1020A
HATCHET_DRAGONITE_ID = 0x1020B
HATCHET_MASTER_ID = 0x1020C

# WEAPONS 0x50000 TO 0x5FFFF
DAGGER_WOODEN_ID = 0x50001
DAGGER_STONE_ID = 0x50002
DAGGER_BRONZE_ID = 0x50003
DAGGER_IRON_ID = 0x50004
DAGGER_STEEL_ID = 0x50005
DAGGER_TITANIUM_ID = 0x50006
DAGGER_MITHRIL_ID = 0x50007
DAGGER_ADAMANT_ID = 0x50008
DAGGER_ANCIENT_ID = 0x50009
DAGGER_ASTRAL_ID = 0x5000A
DAGGER_DRAGONITE_ID = 0x5000B
DAGGER_MASTER_ID = 0x5000C
SWORD_WOODEN_ID = 0x50101
SWORD_STONE_ID = 0x50102
SWORD_BRONZE_ID = 0x50103
SWORD_IRON_ID = 0x50104
SWORD_STEEL_ID = 0x50105
SWORD_TITANIUM_ID = 0x50106
SWORD_MITHRIL_ID = 0x50107
SWORD_ADAMANT_ID = 0x50108
SWORD_ANCIENT_ID = 0x50109
SWORD_ASTRAL_ID = 0x5010A
SWORD_DRAGONITE_ID = 0x5010B
SWORD_MASTER_ID = 0x5010C
BATTLEAXE_WOODEN_ID = 0x50201
BATTLEAXE_STONE_ID = 0x50202
BATTLEAXE_BRONZE_ID = 0x50203
BATTLEAXE_IRON_ID = 0x50204
BATTLEAXE_STEEL_ID = 0x50205
BATTLEAXE_TITANIUM_ID = 0x50206
BATTLEAXE_MITHRIL_ID = 0x50207
BATTLEAXE_ADAMANT_ID = 0x50208
BATTLEAXE_ANCIENT_ID = 0x50209
BATTLEAXE_ASTRAL_ID = 0x5020A
BATTLEAXE_DRAGONITE_ID = 0x5020B
BATTLEAXE_MASTER_ID = 0x5020C
BROADSWORD_WOODEN_ID = 0x50301
BROADSWORD_STONE_ID = 0x50302
BROADSWORD_BRONZE_ID = 0x50303
BROADSWORD_IRON_ID = 0x50304
BROADSWORD_STEEL_ID = 0x50305
BROADSWORD_TITANIUM_ID = 0x50306
BROADSWORD_MITHRIL_ID = 0x50307
BROADSWORD_ADAMANT_ID = 0x50308
BROADSWORD_ANCIENT_ID = 0x50309
BROADSWORD_ASTRAL_ID = 0x5030A
BROADSWORD_DRAGONITE_ID = 0x5030B
BROADSWORD_MASTER_ID = 0x5030C
ARROW_WOODEN_ID = 0x50401
ARROW_STONE_ID = 0x50402
ARROW_BRONZE_ID = 0x50403
ARROW_IRON_ID = 0x50404
ARROW_STEEL_ID = 0x50405
ARROW_TITANIUM_ID = 0x50406
ARROW_MITHRIL_ID = 0x50407
ARROW_ADAMANT_ID = 0x50408
ARROW_ANCIENT_ID = 0x50409
ARROW_ASTRAL_ID = 0x5040A
ARROW_DRAGONITE_ID = 0x5040B
ARROW_MASTER_ID = 0x5040C
STAFF_WOODEN_ID = 0x51001
STAFF_NOVICE_ID = 0x51002

# RESOURCES 0x140000 TO 0x14FFFF
LOG_TREE_ID = 0x140001
LOG_OAK_ID = 0x140002
LOG_WILLOW_ID = 0x140003
LOG_MAPLE_ID = 0x140004
LOG_YEW_ID = 0x140005
LOG_TEAK_ID = 0x140006
LOG_MAHOGANY_ID = 0x140007
LOG_ANCIENT_ID = 0x140008
LOG_ASTRAL_ID = 0x140009
LOG_SPIRIT_ID = 0x14000A
LOG_DARK_ID = 0x14000B
LOG_LIGHT_ID = 0x14000B
LOG_MASTER_ID = 0x14000C

ORE_COPPER_ID = 0x140101
ORE_TIN_ID = 0x140102
ORE_IRON_ID = 0x140103
ORE_COAL_ID = 0x140104
ORE_TITANIUM_ID = 0x140105
ORE_MITHRIL_ID = 0x140106
ORE_ADAMANT_ID = 0x140107
ORE_ANCIENT_ID = 0x140108
ORE_DRAGONITE_ID = 0x140109
ORE_MASTER_ID = 0x14010A
ORE_SILVER_ID = 0x14010B
ORE_GOLD_ID = 0x14010C
ORE_PLATINUM_ID = 0x14010D





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

### FOR CREATABLE ITEMS ###
 # Dict mapping item IDs to number of items required to make this item.
CREATE_REQ_ITEMS_FIELD = 0x10B

 # Dict mapping skill IDs to the level required to make this item.
CREATE_REQ_LEVELS_FIELD = 0x10C

# List of quest IDs required to make this item.
CREATE_REQ_QUEST_FIELD = 0x10D

### CONSUMABLE ITEM FIELD IDs ###
HEAL_VALUE_FIELD = 0x201 # Int.
SKILL_EFFECT_FIELD = 0x202 # Maps skill IDs to tuple (effect type ID, int).
CONSUME_COMBAT_BOOST_FIELD = 0x203 # Maps boost type ID to tuple (effect type ID, int).
CONSUME_QUEST_REQ_FIELD = 0x204 # List of quest IDs required to consume.

### EQUIPPABLE ITEM FIELD IDs ###
EQUIPMENT_SLOT_FIELD = 0x301 # Int representing equipment slot ID.
COMBAT_TYPE_FIELD = 0x302 # Int representing combat type for the item.
ATTACK_VALUE_INFO_FIELD = 0x303 # Maps damage type ID to int.
DEFENSE_VALUE_INFO_FIELD = 0x304 # Maps damage type ID to int.
EQUIP_COMBAT_BOOST_INFO_FIELD = 0x305 # Maps boost type ID to tuple (effect type ID, int).
EQUIP_LEVEL_REQ_FIELD = 0x306 # Dict mapping skill ID to required level.
EQUIP_QUEST_REQ_FIELD = 0x307 # List of quest IDs required to equip.

# For items that are not consumable nor equippable.
STANDARD_ITEM_DATA = {
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
    },
}

# TODO set boost type IDs
# TODO set boost effect type IDs
# TODO set damage type IDs
