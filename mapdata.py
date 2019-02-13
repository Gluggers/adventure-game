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
            '444444444444444444444444444444444444444444444444',
            '444444444444444444444444444444444444444444444444',
            '444444444444444444444444444444444444444444444444',
            '444444444444444444444444444444444444444444444444',
            '444444444444444444444444444444444444444444444444',
            '444444444444444444444444444444444444444444444444',
            '444444444444444444444444444444444444444444444444',
            '444444444444444444444444444444444444444444444444',
            '444444444444444444444444444444444444444444444444',
            '444444444444012444403444444444400441444444444444',
            '444444444401000200200010203014430100444444444444',
            '444444444430100102012010040201000203444444444444',
            '444444444402010401204444444401200104444444444444',
            '444444444402003010202444444400010004444444444444',
            '444444444400100200101444444431010304444444444444',
            '444444444403002410203444444100102044444444444444',
            '444444444400104401004444401204100144444444444444',
            '444444444400104420030124440123200044444444444444',
            '444444444410032044101022000304001044444444444444',
            '444444444400100420300030102030300244444444444444',
            '444444444400024401004402010304404444444444444444',
            '444444444403104420134440120301021444444444444444',
            '444444444400014001001301002031000444444444444444',
            '444444444402100100020010130240200444444444444444',
            '444444444444410002304444440120401444444444444444',
            '444444444400100203010102030100010444444444444444',
            '444444444400100010020010301031023444444444444444',
            '444444444400100002010030010203010444444444444444',
            '444444444404402030444010403444444444444444444444',
            '444444444444411044444444444444444444444444444444',
            '444444444444444444444444444444444444444444444444',
            '444444444444444444444444444444444444444444444444',
            '444444444444444444444444444444444444444444444444',
            '444444444444444444444444444444444444444444444444',
            '444444444444444444444444444444444444444444444444',
            '444444444444444444444444444444444444444444444444',
            '444444444444444444444444444444444444444444444444',
            '444444444444444444444444444444444444444444444444',
        ],
        MAP_TILE_GRID_KEY_FIELD: {
            '0': tiledata.TILE_GRASS_PLAIN_ID,
            '1': tiledata.TILE_GRASS_1_ID,
            '2': tiledata.TILE_GRASS_2_ID,
            '3': tiledata.TILE_GRASS_FLOWERS_ID,
            '4': tiledata.TILE_WATER_NORMAL_1_ID
        },
        MAP_INTER_OBJ_DICT_FIELD: {
            (10,10):  objdata.HERB_BASIC_ID,
            (12,10):  objdata.TREE_BASIC_ID,
            (14,10):  objdata.TREE_BASIC_ID,
            (16,10):  objdata.TREE_BASIC_ID,
            (18,10):  objdata.TREE_BASIC_ID,
            (20,10):  objdata.TREE_BASIC_ID,
            (27,11):  objdata.TREE_BASIC_ID,
            (29,11):  objdata.TREE_BASIC_ID,
            (19,22): objdata.HERB_BASIC_ID,
            (13,17):  objdata.ORE_EMPTY_BASIC_ID,
            (15,13):  objdata.ORE_EMPTY_BASIC_ID,
            (16,20):  objdata.TREE_BASIC_ID,
            (16,17):  objdata.TREE_BASIC_ID,
            (16,15):  objdata.TREE_BASIC_ID,
            (17,14):  objdata.TREE_BASIC_ID,
            (16,13):  objdata.TREE_BASIC_ID,
            (11,14):  objdata.TREE_OAK_ID,
            (11,16):  objdata.TREE_OAK_ID,
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
