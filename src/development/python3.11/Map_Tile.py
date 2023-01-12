class Map_Tile:
    def __init__(self, x, y, times_visited = 0, is_known = False, is_obstacle = False, is_under_robot = False):
        self.__x = x
        self.__y = y
        self.__times_visited = times_visited
        self.is_known = is_known
        self.is_obstacle = is_obstacle
        self.is_under_robot = is_under_robot
        self.__distance = None
    

    def get_x_position(self) -> int:
        return self.__x


    def get_y_position(self) -> int:
        return self.__y


    def get_position(self) -> tuple:
        return (self.__x, self.__y)


    def increment_times_visited(self):
        self.__times_visited += 1


    def get_times_visited(self) -> int:
        return self.__times_visited


    def set_distance(self, distance):
        self.__distance = distance


    def get_distance(self) -> int:
        return self.__distance
