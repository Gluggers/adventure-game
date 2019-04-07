# -*- coding: utf-8 -*-
"""This module contains constants and information for menu options."""

import language

### GAME OPTION ID NUMBERS ###
MORE_OPTIONS_OPTION_ID = 0xFFFF
YES_OPTION_ID = 0x1
NO_OPTION_ID = 0x2
CANCEL_OPTION_ID = 0x3

# OVERWORLD SIDE MENU OPTIONS #
INVENTORY_OPTION_ID = 0x11
EQUIPMENT_OPTION_ID = 0x12
LEVELS_OPTION_ID = 0x13
QUESTS_OPTION_ID = 0x14
CONFIGURATION_OPTION_ID = 0x15
SAVE_GAME_OPTION_ID = 0x16
LOAD_GAME_OPTION_ID = 0x17
QUIT_GAME_OPTION_ID = 0x18
CHARACTER_OPTION_ID = 0x19
SPELLS_OPTION_ID = 0x1A
TOOLS_OPTION_ID = 0x1B

# ITEM OPTION IDS
#USE_OPTION_ID = 0x30 # For using an item with another.
LIGHT_OPTION_ID = 0x32 # For lighting items like logs on fire.
EQUIP_OPTION_ID = 0x33 # For equipping equippable items.
UNEQUIP_OPTION_ID = 0x34 # For unequipping equippable items.
CRAFT_OPTION_ID = 0x35 # For craftable items.
IDENTIFY_OPTION_ID = 0x36 # For identifying unknown items.
READ_OPTION_ID = 0x37 # For identifying readable items.
EAT_OPTION_ID = 0x38
DRINK_OPTION_ID = 0x39
VIEW_ITEM_STATS_OPTION_ID = 0x3A
DISCARD_OPTION_ID = 0x3B # For discarding nonstackable items.
DISCARD_1_OPTION_ID = 0x3C # For discarding stackable items.
DISCARD_5_OPTION_ID = 0x3D # For discarding stackable items.
DISCARD_X_OPTION_ID = 0x3E # For discarding stackable items.
DISCARD_ALL_OPTION_ID = 0x3F # For discarding stackable items.


# STORE OPTION IDS
BUY_1_OPTION_ID = 0x41 # For buying items in stores.
BUY_5_OPTION_ID = 0x42
BUY_X_OPTION_ID = 0x44
BUY_ALL_OPTION_ID = 0x45
SELL_1_OPTION_ID = 0x51 # For selling items in stores.
SELL_5_OPTION_ID = 0x52
SELL_X_OPTION_ID = 0x54
SELL_ALL_OPTION_ID = 0x55

# LOOT OPTION IDS
TAKE_1_OPTION_ID = 0x61
TAKE_5_OPTION_ID = 0x62
TAKE_X_OPTION_ID = 0x65
TAKE_ALL_OPTION_ID = 0x65

DEPOSIT_1_OPTION_ID = 0x71
DEPOSIT_5_OPTION_ID = 0x72
DEPOSIT_X_OPTION_ID = 0x74
DEPOSIT_ALL_OPTION_ID = 0x75

# Some convenient option ID lists for common items.
DEFAULT_LOG_OPTION_ID_LIST = [
    LIGHT_OPTION_ID,
    CRAFT_OPTION_ID,
    DISCARD_OPTION_ID,
]

DEFAULT_ITEM_MENU_OPTION_IDS = [
    DISCARD_OPTION_ID,
]

DEFAULT_STACKABLE_OPTION_ID_LIST = [
    DISCARD_1_OPTION_ID,
    DISCARD_5_OPTION_ID,
    DISCARD_X_OPTION_ID,
    DISCARD_ALL_OPTION_ID,
]

# Maps option ID to dict that maps language ID to the option name.
OPTION_NAME_INFO = {
    CANCEL_OPTION_ID:{
        language.LANG_ENGLISH: "Cancel",
        language.LANG_ESPANOL: "Cancelar",
    },
    YES_OPTION_ID: {
        language.LANG_ENGLISH: "Yes",
        language.LANG_ESPANOL: "Si",
    },
    NO_OPTION_ID: {
        language.LANG_ENGLISH: "No",
        language.LANG_ESPANOL: "No",
    },
    INVENTORY_OPTION_ID: {
        language.LANG_ENGLISH: "Inventory",
        language.LANG_ESPANOL: "Inventario",
    },
    EQUIPMENT_OPTION_ID: {
        language.LANG_ENGLISH: "Equipment",
        language.LANG_ESPANOL: "Equipo",
    },
    LEVELS_OPTION_ID: {
        language.LANG_ENGLISH: "Levels",
        language.LANG_ESPANOL: "Niveles",
    },
    QUESTS_OPTION_ID: {
        language.LANG_ENGLISH: "Quests",
        language.LANG_ESPANOL: "Misiones",
    },
    CONFIGURATION_OPTION_ID: {
        language.LANG_ENGLISH: "Configuration",
        language.LANG_ESPANOL: "Configuracion",
    },
    SAVE_GAME_OPTION_ID: {
        language.LANG_ENGLISH: "Save Game",
        language.LANG_ESPANOL: "Guardar Juego",
    },
    LOAD_GAME_OPTION_ID: {
        language.LANG_ENGLISH: "Load Game",
        language.LANG_ESPANOL: "Cargar Juego",
    },
    QUIT_GAME_OPTION_ID: {
        language.LANG_ENGLISH: "Quit Game",
        language.LANG_ESPANOL: "Salir del Juego",
    },
    CHARACTER_OPTION_ID: {
        language.LANG_ENGLISH: "Character",
        language.LANG_ESPANOL: "Caracter",
    },
    SPELLS_OPTION_ID: {
        language.LANG_ENGLISH: "Spells",
        language.LANG_ESPANOL: "Hechizos",
    },
    TOOLS_OPTION_ID: {
        language.LANG_ENGLISH: "Toolbelt",
        language.LANG_ESPANOL: "Herramientas",
    },
    MORE_OPTIONS_OPTION_ID: {
        language.LANG_ENGLISH: "More Options...",
        language.LANG_ESPANOL: "Mas Opciones...",
    },
    DISCARD_OPTION_ID: {
        language.LANG_ENGLISH: "Discard",
        language.LANG_ESPANOL: "Descartar",
    },
    DISCARD_1_OPTION_ID: {
        language.LANG_ENGLISH: "Discard 1",
        language.LANG_ESPANOL: "Descartar 1",
    },
    DISCARD_5_OPTION_ID: {
        language.LANG_ENGLISH: "Discard 5",
        language.LANG_ESPANOL: "Descartar 5",
    },
    DISCARD_X_OPTION_ID: {
        language.LANG_ENGLISH: "Discard X",
        language.LANG_ESPANOL: "Descartar X",
    },
    DISCARD_ALL_OPTION_ID: {
        language.LANG_ENGLISH: "Discard ALL",
        language.LANG_ESPANOL: "Descartar TODOS",
    },
    LIGHT_OPTION_ID: {
        language.LANG_ENGLISH: "Light",
        language.LANG_ESPANOL: "Encender",
    },
    EQUIP_OPTION_ID: {
        language.LANG_ENGLISH: "Equip",
        language.LANG_ESPANOL: "Equipar",
    },
    UNEQUIP_OPTION_ID: {
        language.LANG_ENGLISH: "Unequip",
        language.LANG_ESPANOL: "Desequipar",
    },
    CRAFT_OPTION_ID: {
        language.LANG_ENGLISH: "Craft",
        language.LANG_ESPANOL: "Elaborar",
    },
    IDENTIFY_OPTION_ID: {
        language.LANG_ENGLISH: "Identify",
        language.LANG_ESPANOL: "Identificar",
    },
    READ_OPTION_ID: {
        language.LANG_ENGLISH: "Read",
        language.LANG_ESPANOL: "Leer",
    },
    EAT_OPTION_ID: {
        language.LANG_ENGLISH: "Eat",
        language.LANG_ESPANOL: "Comer",
    },
    DRINK_OPTION_ID: {
        language.LANG_ENGLISH: "Drink",
        language.LANG_ESPANOL: "Tomar",
    },
    VIEW_ITEM_STATS_OPTION_ID: {
        language.LANG_ENGLISH: "Item Stats",
        language.LANG_ESPANOL: "Datos del Artículo",
    },
    BUY_1_OPTION_ID: {
        language.LANG_ENGLISH: "Buy 1",
        language.LANG_ESPANOL: "Comprar 1",
    },
    SELL_1_OPTION_ID: {
        language.LANG_ENGLISH: "Sell 1",
        language.LANG_ESPANOL: "Vender 1",
    },
    BUY_5_OPTION_ID: {
        language.LANG_ENGLISH: "Buy 5",
        language.LANG_ESPANOL: "Comprar 5",
    },
    SELL_5_OPTION_ID: {
        language.LANG_ENGLISH: "Sell 5",
        language.LANG_ESPANOL: "Vender 5",
    },
    BUY_ALL_OPTION_ID: {
        language.LANG_ENGLISH: "Buy All",
        language.LANG_ESPANOL: "Comprar Todos",
    },
    BUY_X_OPTION_ID: {
        language.LANG_ENGLISH: "Buy X",
        language.LANG_ESPANOL: "Comprar X",
    },
    SELL_ALL_OPTION_ID: {
        language.LANG_ENGLISH: "Sell All",
        language.LANG_ESPANOL: "Vender Todos",
    },
    SELL_X_OPTION_ID: {
        language.LANG_ENGLISH: "Sell X",
        language.LANG_ESPANOL: "Vender X",
    },
    TAKE_1_OPTION_ID: {
        language.LANG_ENGLISH: "Take 1",
        language.LANG_ESPANOL: "Recoger 1",
    },
    TAKE_5_OPTION_ID: {
        language.LANG_ENGLISH: "Take 5",
        language.LANG_ESPANOL: "Recoger 5",
    },
    TAKE_X_OPTION_ID: {
        language.LANG_ENGLISH: "Take X",
        language.LANG_ESPANOL: "Recoger X",
    },
    TAKE_ALL_OPTION_ID: {
        language.LANG_ENGLISH: "Take All",
        language.LANG_ESPANOL: "Recoger Todos",
    },
}

# List of menu option IDs that are for the overworld menu.
OVERWORLD_MENU_OPTION_IDS = [
    INVENTORY_OPTION_ID,
    EQUIPMENT_OPTION_ID,
    LEVELS_OPTION_ID,
    SPELLS_OPTION_ID,
    TOOLS_OPTION_ID,
    QUESTS_OPTION_ID,
    CONFIGURATION_OPTION_ID,
    CHARACTER_OPTION_ID,
    SAVE_GAME_OPTION_ID,
    LOAD_GAME_OPTION_ID,
    QUIT_GAME_OPTION_ID,
    CANCEL_OPTION_ID,
]

COMPREHENSIVE_INVENTORY_ITEM_OPTION_SET = set([
    VIEW_ITEM_STATS_OPTION_ID,
    DISCARD_OPTION_ID,
    DISCARD_1_OPTION_ID,
    DISCARD_5_OPTION_ID,
    DISCARD_X_OPTION_ID,
    DISCARD_ALL_OPTION_ID,
    LIGHT_OPTION_ID,
    EQUIP_OPTION_ID,
    CRAFT_OPTION_ID,
    IDENTIFY_OPTION_ID,
    READ_OPTION_ID,
    EAT_OPTION_ID,
    DRINK_OPTION_ID,
    CANCEL_OPTION_ID,
])

OVERWORLD_INVENTORY_ITEM_OPTION_SET = set([
    VIEW_ITEM_STATS_OPTION_ID,
    DISCARD_OPTION_ID,
    DISCARD_1_OPTION_ID,
    DISCARD_5_OPTION_ID,
    DISCARD_X_OPTION_ID,
    DISCARD_ALL_OPTION_ID,
    LIGHT_OPTION_ID,
    EQUIP_OPTION_ID,
    CRAFT_OPTION_ID,
    IDENTIFY_OPTION_ID,
    READ_OPTION_ID,
    EAT_OPTION_ID,
    DRINK_OPTION_ID,
    CANCEL_OPTION_ID,
])

OVERWORLD_EQUIPMENT_ITEM_OPTION_SET = set([
    VIEW_ITEM_STATS_OPTION_ID,
    UNEQUIP_OPTION_ID,
    CANCEL_OPTION_ID,
])

SHOP_ITEM_OPTION_SET = set([
    BUY_1_OPTION_ID,
    BUY_5_OPTION_ID,
    BUY_X_OPTION_ID,
    BUY_ALL_OPTION_ID,
    CANCEL_OPTION_ID,
])

SHOP_MODE_INVENTORY_ITEM_OPTION_SET = set([
    SELL_1_OPTION_ID,
    SELL_5_OPTION_ID,
    SELL_X_OPTION_ID,
    SELL_ALL_OPTION_ID,
    CANCEL_OPTION_ID,
])

BATTLE_MODE_INVENTORY_ITEM_OPTION_SET = set([
    DISCARD_OPTION_ID,
    DISCARD_1_OPTION_ID,
    DISCARD_5_OPTION_ID,
    DISCARD_X_OPTION_ID,
    DISCARD_ALL_OPTION_ID,
    VIEW_ITEM_STATS_OPTION_ID,
    EQUIP_OPTION_ID,
    EAT_OPTION_ID,
    DRINK_OPTION_ID,
    CANCEL_OPTION_ID,
])

BATTLE_LOOT_ITEM_OPTION_SET = set([
    TAKE_1_OPTION_ID,
    TAKE_5_OPTION_ID,
    TAKE_X_OPTION_ID,
    TAKE_ALL_OPTION_ID,
    CANCEL_OPTION_ID,
])

def get_option_name(option_id, language_id):
    return OPTION_NAME_INFO.get(option_id, {}).get(
        language_id,
        None
    )
