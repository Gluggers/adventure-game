import language

### GAME OPTION ID NUMBERS ###
INVENTORY_OPTION_ID = 0x1
EQUIPMENT_OPTION_ID = 0x2
STATS_OPTION_ID = 0x3
QUESTS_OPTION_ID = 0x4
CONFIGURATION_OPTION_ID = 0x5
SAVE_GAME_OPTION_ID = 0x6
LOAD_GAME_OPTION_ID = 0x7
QUIT_GAME_OPTION_ID = 0x8

MORE_OPTIONS_OPTION_ID = 0xFFFF

# Maps option ID to dict that maps language ID to the option name.
OPTION_NAME_INFO = {
    INVENTORY_OPTION_ID: {
        language.LANG_ENGLISH: "Inventory",
        language.LANG_ESPANOL: "Inventario",
    },
    EQUIPMENT_OPTION_ID: {
        language.LANG_ENGLISH: "Equipment",
        language.LANG_ESPANOL: "Equipo",
    },
    STATS_OPTION_ID: {
        language.LANG_ENGLISH: "Stats",
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
    MORE_OPTIONS_OPTION_ID: {
        language.LANG_ENGLISH: "More Options...",
        language.LANG_ESPANOL: "Mas Opciones...",
    },
}

# List of menu option IDs that are for the overworld menu.
OVERWORLD_MENU_OPTION_IDS = [
    INVENTORY_OPTION_ID,
    EQUIPMENT_OPTION_ID,
    STATS_OPTION_ID,
    QUESTS_OPTION_ID,
    CONFIGURATION_OPTION_ID,
    SAVE_GAME_OPTION_ID,
    LOAD_GAME_OPTION_ID,
    QUIT_GAME_OPTION_ID,
]

def get_option_name(option_id, language_id):
    return OPTION_NAME_INFO.get(option_id, {}).get(
        language_id,
        None
    )
