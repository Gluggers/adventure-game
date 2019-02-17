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
            '566656546546546546556456454654654654656454654645',
            '545654545644564564564564564646465465465646456456',
            '546646456445454564565464565656456456455656545546',
            '466565646464564645654645646465645646654655454665',
            '456546546546454665465656565465464646465464565466',
            '465544654464546464564646564656465646556464546546',
            '465465464646546546546456456456456456456456456456',
            '456465465446465465465465465465465465456456454654',
            '465465464646456465464564546465465465465465465466',
            '654656546645012456503465465646500641656546546546',
            '565465465401000200200010203014430100545656565464',
            '565465654630100102012010040201000203546546546546',
            '456565465402010401204444444401200106565465465465',
            '545645665402003010202444444400010004564656546546',
            '456546566400100200101444444431010306546546546546',
            '656546546603002410203444444100102055645654654664',
            '456546546600104401004564601204100145656565465664',
            '564565465600104420030125460123200046565645656565',
            '654665465610032056101022000304001045645665464564',
            '455465654600100620300030102030300266456645654656',
            '655465646600024501004602010304504566465456656545',
            '565465465603104620135460120301021655656565465654',
            '455464564600014001001301002031000654545656545644',
            '565465465402100100020010130260200456455646564564',
            '456546546565410002304564650120501445645645545664',
            '456465465600100203010102030100010454565654565454',
            '465664656400100010020010301031023456456544546546',
            '456454564400100002010030010203010465646464465646',
            '454656446404402030454010603646546654646564646564',
            '456465465456411045646564654465646464654665464654',
            '456465445454564645645465465466446464646564564654',
            '445645656444646546565464566565464565464645645445',
            '456646465465465465464646465654654654646456464656',
            '456465656465465465465656565465465464564564564545',
            '455456546456564565464456565464654654644564645464',
            '465645564545465656456456456454665464654646454645',
            '444444444444444444444444444444444444444444444444',
            '444444444444444444444444444444444444444444444444',
        ],
        MAP_TILE_GRID_KEY_FIELD: {
            '0': tiledata.TILE_GRASS_PLAIN_ID,
            '1': tiledata.TILE_GRASS_1_ID,
            '2': tiledata.TILE_GRASS_2_ID,
            '3': tiledata.TILE_GRASS_FLOWERS_ID,
            '4': tiledata.TILE_WATER_NORMAL_1_ID,
            '5': tiledata.TILE_WATER_NORMAL_2_ID,
            '6': tiledata.TILE_WATER_NORMAL_3_ID,
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
            (13,17):  objdata.ORE_EMPTY_ID,
            (15,13):  objdata.ORE_EMPTY_ID,
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
