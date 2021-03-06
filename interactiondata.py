import language

### INTERACTION ID NUMBERS ###

# SPECIAL INTERACTION ID NUMBERS ARE 0X000001 TO 0X0FFFFF
MIN_SPECIAL_ID = 0x000001
MAX_SPECIAL_ID = 0x0FFFFF
DEFAULT_ID = 0x000002

# CHARACTER INTERACTION IDS ARE 0X100000 TO 0X1FFFFF
MIN_CHARACTER_ID = 0x100000
MAX_CHARACTER_ID = 0x1FFFFF

# MONSTER INTERACTION IDS ARE 0X200000 TO 0X2FFFFF
MIN_MONSTER_ID = 0x200000
MAX_MONSTER_ID = 0x2FFFFF

# RESOURCE INTERACTION IDS ARE 0X300000 TO 0X3FFFFF
MIN_RESOURCE_ID = 0x300000
MAX_RESOURCE_ID = 0x3FFFFF
CHOP_TREE_ID = 0x300001
MINE_ROCK_ID = 0x300021
CATCH_FISH_ROD_ID = 0x300031
CATCH_FISH_NET_ID = 0x300032
CATCH_FISH_HARPOON_ID = 0x300033
COOKING_ID = 0x300041
HERBLORE_GATHER_ID = 0x300051

# ITEM INTERACTION IDS ARE 0X400000 TO 0X4FFFFF
MIN_ITEM_ID = 0x400000
USE_TINDERBOX_ID = 0x400001
MAX_ITEM_ID = 0x4FFFFF

# OBSTACLE INTERACTION IDS ARE 0X500000 TO 0X5FFFFF
MIN_OBSTACLE_ID = 0x500000
MAX_OBSTACLE_ID = 0x5FFFFF

# CHEST INTERACTION IDS ARE 0X600000 TO 0X6FFFFF
MIN_CHEST_ID = 0x600000
MAX_CHEST_ID = 0x6FFFFF

### RESOURCE GATHERING MESSAGES ###
# Maps interaction IDs to dicts that map language IDs to strings.
GATHERING_MAIN_MESSAGES = {
    CHOP_TREE_ID: {
        language.LANG_ENGLISH: "You attempt to chop down the {0}...",
        language.LANG_ESPANOL: "Tratas de cortar {0}...",
    },
    MINE_ROCK_ID: {
        language.LANG_ENGLISH: "You attempt to mine the {0}...",
        language.LANG_ESPANOL: "Tratas de extraer minerales de {0}...",
    },
    CATCH_FISH_ROD_ID: {
        language.LANG_ENGLISH: "You cast out your rod at the {0} to catch some fish...",
        language.LANG_ESPANOL: "Lanzas tu caña para pescar en {0}...",
    },
}

# Maps interaction IDs to dicts that map language IDs to strings.
GATHERING_RESOURCE_EXHAUST_MESSAGES = {
    CHOP_TREE_ID: {
        language.LANG_ENGLISH: "You cut down the {0}.",
        language.LANG_ESPANOL: "Has talado el/la {0}.",
    },
    MINE_ROCK_ID: {
        language.LANG_ENGLISH: "You have exhausted the {0}.",
        language.LANG_ESPANOL: "Ya se agotó el/la {0}.",
    },
    CATCH_FISH_ROD_ID: {
        language.LANG_ENGLISH: "It looks like there aren't any more fish at this {0}...",
        language.LANG_ESPANOL: "Parece que ya no hay peces en este {0}...",
    },
}

# Maps interaction IDs to dicts that map language IDs to strings.
GATHERING_RESOURCE_GAIN_MESSAGES = {
    CHOP_TREE_ID: {
        language.LANG_ENGLISH: "You obtain a(n) {0} and earned {1} experience!",
        language.LANG_ESPANOL: "Has conseguido un(a) {0}, y has ganado {1} puntos de experiencia!",
    },
    MINE_ROCK_ID: {
        language.LANG_ENGLISH: "You mined a(n) {0} and earned {1} experience!",
        language.LANG_ESPANOL: "Has extraído un(a) {0}, y has ganado {1} puntos de experiencia!",
    },
    CATCH_FISH_ROD_ID: {
        language.LANG_ENGLISH: "You caught a(n) {0} and earned {1} experience!",
        language.LANG_ESPANOL: "Has pescado un(a) {0}, y has ganado {1} puntos de experiencia!",
    },
}

# FIREMAKING MESSAGES #
CANNOT_LIGHT_IN_FRONT_INFO = {
    language.LANG_ENGLISH: "You cannot light a fire in front of you. Try moving elsewhere.",
    language.LANG_ESPANOL: "No puedes encender una hoguera enfrente de ti. Intentalo en otro lugar.",
}

LIGHT_LOG_FIRE_INFO = {
    language.LANG_ENGLISH: "You light a fire and gain {0} firemaking experience!",
    language.LANG_ESPANOL: "Has encendido una hoguera y has ganado {0} puntos de experiencia en Dominio de Fuego!",
}
