class Connector:
    # create a Connector object. The purpose of a Connector object is to
    # indicate where an Entity will go when reaching an area of the map
    # linked to the Connector.
    # x and y destination coordinates are Tile coordinates, NOT pixels
    def __init__(self,
                dest_region,
                dest_area,
                dest_x_coord,
                dest_y_coord):
        self.dest_region = dest_region
        self.dest_area = dest_area
        self.dest_x_coord = dest_x_coord
        self.dest_y_coord = dest_y_coord

# set up logger
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
