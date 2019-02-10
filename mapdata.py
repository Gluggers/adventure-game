import tile
import tiledata
import objdata

### DIRECTION CONSTANTS ###
DIR_NORTH = 0x1
DIR_EAST = 0x2
DIR_SOUTH = 0x3
DIR_WEST = 0x4

### MAP ID CONSTANTS ###
R0_A0_ID = 0x0
R0_A1_ID = 0x1
R0_A2_ID = 0x2
R0_A3_ID = 0x3
R0_A4_ID = 0x4
R0_A5_ID = 0x5
R1_A0_ID = 0x1000
R1_A1_ID = 0x1001
R1_A2_ID = 0x1002
R1_A3_ID = 0x1003
R1_A4_ID = 0x1004
R1_A5_ID = 0x1005
R2_A0_ID = 0x2000
R2_A1_ID = 0x2001
R2_A2_ID = 0x2002
R2_A3_ID = 0x2003
R2_A4_ID = 0x2004
R2_A5_ID = 0x2005

### MAP DATA CONSTANTS ###
MAP_TILE_GRID_FIELD = 0x1
MAP_TILE_GRID_KEY_FIELD = 0x2
MAP_INTER_OBJ_DICT_FIELD = 0x3
MAP_CONNECTOR_TILE_DICT_FIELD = 0x4
MAP_ADJ_MAP_DICT_FIELD = 0x5

### MAP TILE GRIDS ###
MAP_DATA = {
    R0_A0_ID: {
        MAP_TILE_GRID_FIELD: [
            '0100020020',
            '3010010201',
            '0201040120',
            '0200301020',
            '0010020010',
            '0300241020',
            '0010440100',
            '0010442003',
            '1003204410',
            '0010042030',
            '0002440100',
            '0310442013',
            '0001400100',
            '0210010002',
            '4441000230'
        ],
        MAP_TILE_GRID_KEY_FIELD: {
            '0': tiledata.TILE_GRASS_PLAIN_ID,
            '1': tiledata.TILE_GRASS_1_ID,
            '2': tiledata.TILE_GRASS_2_ID,
            '3': tiledata.TILE_GRASS_FLOWERS_ID,
            '4': tiledata.TILE_WATER_NORMAL_1_ID
        },
        MAP_INTER_OBJ_DICT_FIELD: {
            (0,0):  objdata.HERB_BASIC_ID,
            (9,12): objdata.HERB_BASIC_ID,
            (3,7):  objdata.ORE_EMPTY_BASIC_ID,
            (5,3):  objdata.ORE_EMPTY_BASIC_ID,
            (7,9):  objdata.TREE_BASIC_ID,
            (1,4):  objdata.TREE_OAK_ID,
        },
        MAP_CONNECTOR_TILE_DICT_FIELD: {},
        MAP_ADJ_MAP_DICT_FIELD: {}
    },
    R0_A1_ID: {
        MAP_TILE_GRID_FIELD: [
            '0100020020',
            '3010010201',
            '0201040120',
            '0200301020',
            '0010020010'
        ],
        MAP_TILE_GRID_KEY_FIELD: {
            '0': tiledata.TILE_GRASS_PLAIN_ID,
            '1': tiledata.TILE_GRASS_1_ID,
            '2': tiledata.TILE_GRASS_2_ID,
            '3': tiledata.TILE_GRASS_FLOWERS_ID,
            '4': tiledata.TILE_WATER_NORMAL_1_ID
        },
        MAP_INTER_OBJ_DICT_FIELD: {},
        MAP_CONNECTOR_TILE_DICT_FIELD: {},
        MAP_ADJ_MAP_DICT_FIELD: {}
    }
}
