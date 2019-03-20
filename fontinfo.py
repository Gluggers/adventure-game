### COLOR CONSTANTS ###
COLOR_WHITE = (255,255,255)
COLOR_BLACK = (0,0,0)

### FONT ID NUMBERS ###
DEFAULT_FONT_ID = 0x1
OW_HEALTH_DISPLAY_FONT_ID = 0x2
OW_BOTTOM_TEXT_FONT_ID = 0x3
OW_SIDE_MENU_FONT_ID = 0x4
SELECTION_TOP_DISPLAY_FONT_ID = 0x10
SELECTION_NAME_FONT_ID = 0x11
SELECTION_DESCRIPTION_FONT_ID = 0x12
SELECTION_SUBTITLE_FONT_ID = 0x13
SELECTION_SUPERTEXT_FONT_ID = 0x14
SELECTION_MENU_FONT_ID = 0x15
SELECTION_BOTTOM_TEXT_FONT_ID = 0x16

### FONT INFO FIELDS ###
FONT_SIZE_FIELD = 0x1
FONT_PATH_FIELD = 0x2

### FONT INFO ###
FONT_INFO = {
    DEFAULT_FONT_ID: {
        FONT_SIZE_FIELD: 16,
        FONT_PATH_FIELD: "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
    },
    OW_HEALTH_DISPLAY_FONT_ID: {
        FONT_SIZE_FIELD: 18,
        FONT_PATH_FIELD: "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
    },
    OW_BOTTOM_TEXT_FONT_ID: {
        FONT_SIZE_FIELD: 16,
        FONT_PATH_FIELD: "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
    },
    OW_SIDE_MENU_FONT_ID: {
        FONT_SIZE_FIELD: 16,
        FONT_PATH_FIELD: "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
    },
    SELECTION_TOP_DISPLAY_FONT_ID: {
        FONT_SIZE_FIELD: 22,
        FONT_PATH_FIELD: "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
    },
    SELECTION_NAME_FONT_ID: {
        FONT_SIZE_FIELD: 22,
        FONT_PATH_FIELD: "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
    },
    SELECTION_DESCRIPTION_FONT_ID: {
        FONT_SIZE_FIELD: 16,
        FONT_PATH_FIELD: "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
    },
    SELECTION_SUBTITLE_FONT_ID: {
        FONT_SIZE_FIELD: 18,
        FONT_PATH_FIELD: "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
    },
    SELECTION_SUPERTEXT_FONT_ID: {
        FONT_SIZE_FIELD: 11,
        FONT_PATH_FIELD: "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
    },
    SELECTION_MENU_FONT_ID: {
        FONT_SIZE_FIELD: 16,
        FONT_PATH_FIELD: "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
    },
    SELECTION_BOTTOM_TEXT_FONT_ID: {
        FONT_SIZE_FIELD: 16,
        FONT_PATH_FIELD: "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
    },
}

FONT_SIZE_DEFAULT = 16
FONT_COLOR_DEFAULT = COLOR_BLACK
FONT_PATH_DEFAULT = "/usr/share/fonts/truetype/liberation/" \
                    + "LiberationSerif-Regular.ttf"
