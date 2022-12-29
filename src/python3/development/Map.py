from math import floor

from Map_Tile import Map_Tile

from Constants import Map_Constants


# Robot's size:
# Width = 3 Tiles
# Length = 5 Tiles

# After initialising the Map, the default tiles will represent the robot's size.
# Example of the map after initialisation:
#
#       ...
#       ...
#       ...
#       .T.
#       ...
#
# T - Is the tile, that will be used to track the robot's position.


class Map:
    __map = {}

    # [-x, x, -y, y]
    __bounds = [0, 0, 0, 0]

    # N - North, E - East, S - South, W - West
    __orientation = 'N'

    # [x, y]
    __starting_tile_position = [0, 0]
    __current_tile_position = [0, 0]


    def __init__(self):
        self.__setup_starting_position()


    def __setup_starting_position(self):
        for y in range(-1, 4):
            for x in range(-1, 2):
                self.add_tile(x, y, times_visited = 1, is_known = True, is_under_robot = True)
    

    def __update_bounds(self, x, y):
        if x < self.__bounds[0]:
            self.__bounds[0] = x

        elif x > self.__bounds[1]:
            self.__bounds[1] = x

        if y < self.__bounds[2]:
            self.__bounds[2] = y

        elif y > self.__bounds[3]:
            self.__bounds[3] = y


    def __get_tile(self, x, y) -> Map_Tile:
        key = str(x) + "," + str(y)

        if key in self.__map:
            return self.__map[key]

        return None

    
    def __get_tile_count(self, distance):
        tile_count = floor(distance / Map_Constants.TILE_SIZE)

        if tile_count > Map_Constants.VISION_RANGE:
            return Map_Constants.VISION_RANGE, False

        else:
            return tile_count, True


    def __get_neighbouring_tiles(self, tile) -> list:
        neighbours = []

        if str(tile.get_x_position()) + "," + str(tile.get_y_position() + 1) in self.__map:
            neighbours.append(self.__map[str(tile.get_x_position()) + "," + str(tile.get_y_position() + 1)])

        if str(tile.get_x_position()) + "," + str(tile.get_y_position() - 1) in self.__map:
            neighbours.append(self.__map[str(tile.get_x_position()) + "," + str(tile.get_y_position() - 1)])

        if str(tile.get_x_position() + 1) + "," + str(tile.get_y_position()) in self.__map:
            neighbours.append(self.__map[str(tile.get_x_position() + 1) + "," + str(tile.get_y_position())])

        if str(tile.get_x_position() - 1) + "," + str(tile.get_y_position()) in self.__map:
            neighbours.append(self.__map[str(tile.get_x_position() - 1) + "," + str(tile.get_y_position())])

        return neighbours


    def __calculate_distances(self, tile, n = 0) -> list:
        neighbours = self.__get_neighbouring_tiles(tile)

        for i in range(len(neighbours)):
            if neighbours[i].is_obstacle or neighbours[i].is_known:
                continue

            elif neighbours[i].get_distance() is None or neighbours[i].get_distance() > n + 1:
                x = neighbours[i].get_x_position()
                y = neighbours[i].get_y_position()

                self.__map[str(x) + "," + str(y)].set_distance(n + 1)

                neighbours[i].set_distance(n + 1)

                if neighbours[i].get_position() == self.__current_tile_position:
                    break

                self.__calculate_distances(neighbours[i], n + 1)

            if n == 0:
                self.display_map()


    def __get_lowest_distance_neighbour(self, tile) -> Map_Tile:
        neighbours = self.__get_neighbouring_tiles(tile)
        lowest_distance = None
        lowest_distance_neighbour = None

        for neighbour in neighbours:
            if neighbour.is_obstacle or neighbour.is_known:
                continue

            elif lowest_distance is None or neighbour.get_distance() < lowest_distance:
                lowest_distance = neighbour.get_distance()
                lowest_distance_neighbour = neighbour

        return lowest_distance_neighbour


    def __update_corner_tiles(self, direction):
        if (direction == 'l' and self.__orientation == 'N') or (direction == 'r' and self.__orientation == 'W'):
            for x in range(self.get_current_x_position() - 3, self.get_current_x_position() - 1):
                for y in range(self.get_current_y_position() + 2, self.get_current_y_position() + 4):
                    tile = self.__get_tile(x, y)

                    if tile:
                        tile.increment_times_visited()

                    else:
                        self.add_tile(x, y, times_visited = 1, is_known = True)

        elif (direction == 'l' and self.__orientation == 'E') or (direction == 'r' and self.__orientation == 'N'):
            for x in range(self.get_current_x_position() + 2, self.get_current_x_position() + 4):
                for y in range(self.get_current_y_position() + 2, self.get_current_y_position() + 4):
                    tile = self.__get_tile(x, y)

                    if tile:
                        tile.increment_times_visited()

                    else:
                        self.add_tile(x, y, times_visited = 1, is_known = True)

        elif (direction == 'l' and self.__orientation == 'S') or (direction == 'r' and self.__orientation == 'E'):
            for x in range(self.get_current_x_position()+ 2, self.get_current_x_position() + 4):
                for y in range(self.get_current_y_position() - 3, self.get_current_y_position() - 1):
                    tile = self.__get_tile(x, y)

                    if tile:
                        tile.increment_times_visited()

                    else:
                        self.add_tile(x, y, times_visited = 1, is_known = True)

        elif (direction == 'l' and self.__orientation == 'W') or (direction == 'r' and self.__orientation == 'S'):
            for x in range(self.get_current_x_position() - 3, self.get_current_x_position() - 1):
                for y in range(self.get_current_y_position() - 3, self.get_current_y_position() - 1):
                    tile = self.__get_tile(x, y)

                    if tile:
                        tile.increment_times_visited()

                    else:
                        self.add_tile(x, y, times_visited = 1, is_known = True)
            

    def set_current_x_position(self, x):
        self.__current_tile_position[0] = x


    def get_current_x_position(self) -> int:
        return self.__current_tile_position[0]


    def set_current_y_position(self, y):
        self.__current_tile_position[1] = y


    def get_current_y_position(self) -> int:
        return self.__current_tile_position[1]


    def update_orientation(self, direction):
        self.__update_corner_tiles(direction)

        if direction == 'l':
            if self.__orientation == 'N':
                self.__orientation = 'W'

                # Setting is_under_robot to False for tiles, that are representing 2 front rows of the robot figure
                for x in range(self.get_current_x_position() - 1, self.get_current_x_position() + 2):
                    for y in range(self.get_current_y_position() + 2, self.get_current_y_position() + 4):
                        tile = self.__get_tile(x, y)

                        if tile:
                            tile.is_under_robot = False

                # Setting is_under_robot to True for tiles, that are representing 2 front rows of the robot figure
                for x in range(self.get_current_x_position() - 3, self.get_current_x_position() - 1):
                    for y in range(self.get_current_y_position() - 1, self.get_current_y_position() + 2):
                        tile = self.__get_tile(x, y)

                        if tile:
                            tile.is_under_robot = True

                        else:
                            self.add_tile(x, y, times_visited = 1, is_known = True, is_under_robot = True)

            elif self.__orientation == 'W':
                self.__orientation = 'S'

                # Setting is_under_robot to False for tiles, that are representing 2 front rows of the robot figure
                for x in range(self.get_current_x_position() - 3, self.get_current_x_position() - 1):
                    for y in range(self.get_current_y_position() - 1, self.get_current_y_position() + 2):
                        tile = self.__get_tile(x, y)

                        if tile:
                            tile.is_under_robot = False

                # Setting is_under_robot to True for tiles, that are representing 2 front rows of the robot figure
                for x in range(self.get_current_x_position() - 1, self.get_current_x_position() + 2):
                    for y in range(self.get_current_y_position() - 3, self.get_current_y_position() - 1):
                        tile = self.__get_tile(x, y)

                        if tile:
                            tile.is_under_robot = True

                        else:
                            self.add_tile(x, y, times_visited = 1, is_known = True, is_under_robot = True)

            elif self.__orientation == 'S':
                self.__orientation = 'E'

                # Setting is_under_robot to False for tiles, that are representing 2 front rows of the robot figure
                for x in range(self.get_current_x_position() - 1, self.get_current_x_position() + 2):
                    for y in range(self.get_current_y_position() - 3, self.get_current_y_position() - 1):
                        tile = self.__get_tile(x, y)

                        if tile:
                            tile.is_under_robot = False

                # Setting is_under_robot to True for tiles, that are representing 2 front rows of the robot figure
                for x in range(self.get_current_x_position() + 2, self.get_current_x_position() + 4):
                    for y in range(self.get_current_y_position() - 1, self.get_current_y_position() + 2):
                        tile = self.__get_tile(x, y)

                        if tile:
                            tile.is_under_robot = True

                        else:
                            self.add_tile(x, y, times_visited = 1, is_known = True, is_under_robot = True)

            elif self.__orientation == 'E':
                self.__orientation = 'N'

                # Setting is_under_robot to False for tiles, that are representing 2 front rows of the robot figure
                for x in range(self.get_current_x_position() + 2, self.get_current_x_position() + 4):
                    for y in range(self.get_current_y_position() - 1, self.get_current_y_position() + 2):
                        tile = self.__get_tile(x, y)

                        if tile:
                            tile.is_under_robot = False

                # Setting is_under_robot to True for tiles, that are representing 2 front rows of the robot figure
                for x in range(self.get_current_x_position() - 1, self.get_current_x_position() + 2):
                    for y in range(self.get_current_y_position() + 2, self.get_current_y_position() + 4):
                        tile = self.__get_tile(x, y)

                        if tile:
                            tile.is_under_robot = True

                        else:
                            self.add_tile(x, y, times_visited = 1, is_known = True, is_under_robot = True)


        elif direction == 'r':
            if self.__orientation == 'N':
                self.__orientation = 'E'

                # Setting is_under_robot to False for tiles, that are representing 2 front rows of the robot figure
                for x in range(self.get_current_x_position() - 1, self.get_current_x_position() + 2):
                    for y in range(self.get_current_y_position() + 2, self.get_current_y_position() + 4):
                        tile = self.__get_tile(x, y)

                        if tile:
                            tile.is_under_robot = False

                # Setting is_under_robot to True for tiles, that are representing 2 front rows of the robot figure
                for x in range(self.get_current_x_position() + 2, self.get_current_x_position() + 4):
                    for y in range(self.get_current_y_position() - 1, self.get_current_y_position() + 2):
                        tile = self.__get_tile(x, y)

                        if tile:
                            tile.is_under_robot = True

                        else:
                            self.add_tile(x, y, times_visited = 1, is_known = True, is_under_robot = True)

            elif self.__orientation == 'E':
                self.__orientation = 'S'

                # Setting is_under_robot to False for tiles, that are representing 2 front rows of the robot figure
                for x in range(self.get_current_x_position() + 2, self.get_current_x_position() + 4):
                    for y in range(self.get_current_y_position() - 1, self.get_current_y_position() + 2):
                        tile = self.__get_tile(x, y)

                        if tile:
                            tile.is_under_robot = False

                # Setting is_under_robot to True for tiles, that are representing 2 front rows of the robot figure
                for x in range(self.get_current_x_position() - 1, self.get_current_x_position() + 2):
                    for y in range(self.get_current_y_position() - 3, self.get_current_y_position() - 1):
                        tile = self.__get_tile(x, y)

                        if tile:
                            tile.is_under_robot = True

                        else:
                            self.add_tile(x, y, times_visited = 1, is_known = True, is_under_robot = True)
                
            elif self.__orientation == 'S':
                self.__orientation = 'W'

                # Setting is_under_robot to False for tiles, that are representing 2 front rows of the robot figure
                for x in range(self.get_current_x_position() - 1, self.get_current_x_position() + 2):
                    for y in range(self.get_current_y_position() - 3, self.get_current_y_position() - 1):
                        tile = self.__get_tile(x, y)

                        if tile:
                            tile.is_under_robot = False
                
                # Setting is_under_robot to True for tiles, that are representing 2 front rows of the robot figure
                for x in range(self.get_current_x_position() - 3, self.get_current_x_position() - 1):
                    for y in range(self.get_current_y_position() - 1, self.get_current_y_position() + 2):
                        tile = self.__get_tile(x, y)

                        if tile:
                            tile.is_under_robot = True

                        else:
                            self.add_tile(x, y, times_visited = 1, is_known = True, is_under_robot = True)
                
            elif self.__orientation == 'W':
                self.__orientation = 'N'

                # Setting is_under_robot to False for tiles, that are representing 2 front rows of the robot figure
                for x in range(self.get_current_x_position() - 3, self.get_current_x_position() - 1):
                    for y in range(self.get_current_y_position() - 1, self.get_current_y_position() + 2):
                        tile = self.__get_tile(x, y)

                        if tile:
                            tile.is_under_robot = False
                
                # Setting is_under_robot to True for tiles, that are representing 2 front rows of the robot figure
                for x in range(self.get_current_x_position() - 1, self.get_current_x_position() + 2):
                    for y in range(self.get_current_y_position() + 2, self.get_current_y_position() + 4):
                        tile = self.__get_tile(x, y)

                        if tile:
                            tile.is_under_robot = True

                        else:
                            self.add_tile(x, y, times_visited = 1, is_known = True, is_under_robot = True)


    def get_current_orientation(self) -> str:
        return self.__orientation

    
    def add_tile(self, x, y, times_visited = 0, is_known = False, is_obstacle = False, is_under_robot = False) -> bool:
        key = str(x) + "," + str(y)

        if key in self.__map:
            return False

        self.__update_bounds(x, y)
        self.__map[key] = Map_Tile(x, y, times_visited, is_known, is_obstacle, is_under_robot)

        return True


    def get_current_tile(self) -> Map_Tile:
        return self.__map[str(self.get_current_x_position()) + "," + str(self.get_current_y_position())]

    
    def update_position(self):
        if self.__orientation == 'N':
            self.__current_tile_position[1] += 1

            min_range = self.get_current_x_position() - 1
            max_range = self.get_current_x_position() + 2

            # Moving robot-representing tiles to the front
            y = self.get_current_y_position() + 3

            for x in range(min_range, max_range):
                tile = self.__get_tile(x, y)

                if tile:
                    tile.increment_times_visited()
                    tile.is_under_robot = True

                else:
                    self.add_tile(x, y, times_visited = 1, is_known = True, is_under_robot = True) 
            
            # Removing robot-representing tiles from the back
            y = self.get_current_y_position() - 2

            for x in range(min_range, max_range):
                tile = self.__get_tile(x, y)

                if tile:
                    tile.is_under_robot = False

        elif self.__orientation == 'E':
            self.__current_tile_position[1] += 1

            min_range = self.get_current_y_position() - 1
            max_range = self.get_current_y_position() + 2

            # Moving robot-representing tiles to the front
            x = self.get_current_x_position() + 3

            for y in range(min_range, max_range):
                tile = self.__get_tile(x, y)

                if tile:
                    tile.increment_times_visited()
                    tile.is_under_robot = True

                else:
                    self.add_tile(x, y, times_visited = 1, is_known = True, is_under_robot = True) 
            
            # Removing robot-representing tiles from the back
            x = self.get_current_x_position() - 2

            for y in range(min_range, max_range):
                tile = self.__get_tile(x, y)

                if tile:
                    tile.is_under_robot = False

        elif self.__orientation == 'S':
            self.__current_tile_position[1] -= 1

            min_range = self.get_current_x_position() - 1
            max_range = self.get_current_x_position() + 2

            # Moving robot-representing tiles to the front
            y = self.get_current_y_position() - 3

            for x in range(min_range, max_range):
                tile = self.__get_tile(x, y)

                if tile:
                    tile.increment_times_visited()
                    tile.is_under_robot = True

                else:
                    self.add_tile(x, y, times_visited = 1, is_known = True, is_under_robot = True) 
            
            # Removing robot-representing tiles from the back
            y = self.get_current_y_position() + 2

            for x in range(min_range, max_range):
                tile = self.__get_tile(x, y)

                if tile:
                    tile.is_under_robot = False

        elif self.__orientation == 'W':
            self.__current_tile_position[1] -= 1

            min_range = self.get_current_y_position() - 1
            max_range = self.get_current_y_position() + 2

            # Moving robot-representing tiles to the front
            x = self.get_current_x_position() - 3

            for y in range(min_range, max_range):
                tile = self.__get_tile(x, y)

                if tile:
                    tile.increment_times_visited()
                    tile.is_under_robot = True

                else:
                    self.add_tile(x, y, times_visited = 1, is_known = True, is_under_robot = True) 
            
            # Removing robot-representing tiles from the back
            x = self.get_current_x_position() + 2

            for y in range(min_range, max_range):
                tile = self.__get_tile(x, y)

                if tile:
                    tile.is_under_robot = False


    def update_map(self, sensor_data):
        if self.__orientation == 'N':
            # adding forward tiles
            tile_count, has_obstacle = self.__get_tile_count(sensor_data["front"])

            for i in range(tile_count):
                if not self.__get_tile(self.get_current_x_position(), self.get_current_y_position() + i + 4):
                    self.add_tile(self.get_current_x_position(), self.get_current_y_position() + i + 4, is_known = True)

            if has_obstacle:
                self.add_tile(self.get_current_x_position(), self.get_current_y_position() + tile_count + 4, is_known = True, is_obstacle = True)

            # adding left tiles
            tile_count, has_obstacle = self.__get_tile_count(sensor_data["left"])

            for i in range(tile_count):
                if not self.__get_tile(self.get_current_x_position() - 1, self.get_current_y_position() + i + 4):
                    self.add_tile(self.get_current_x_position() - 1, self.get_current_y_position() + i + 4, is_known = True)

            if has_obstacle:
                self.add_tile(self.get_current_x_position() - 1, self.get_current_y_position() + tile_count + 4, is_known = True, is_obstacle = True)

            # adding right tiles
            tile_count, has_obstacle = self.__get_tile_count(sensor_data["right"])

            for i in range(tile_count):
                if not self.__get_tile(self.get_current_x_position() + 1, self.get_current_y_position() + i + 4):
                    self.add_tile(self.get_current_x_position() + 1, self.get_current_y_position() + i + 4, is_known = True)

            if has_obstacle:
                self.add_tile(self.get_current_x_position() + 1, self.get_current_y_position() + tile_count + 4, is_known = True, is_obstacle = True)

        elif self.__orientation == 'E':
            # adding forward tiles
            tile_count, has_obstacle = self.__get_tile_count(sensor_data["front"])

            for i in range(tile_count):
                if not self.__get_tile(self.get_current_x_position() + i + 4, self.get_current_y_position()):
                    self.add_tile(self.get_current_x_position() + i + 4, self.get_current_y_position(), is_known = True)

            if has_obstacle:
                self.add_tile(self.get_current_x_position() + tile_count + 4, self.get_current_y_position(), is_known = True, is_obstacle = True)

            # adding left tiles
            tile_count, has_obstacle = self.__get_tile_count(sensor_data["left"])

            for i in range(tile_count):
                if not self.__get_tile(self.get_current_x_position() + i + 4, self.get_current_y_position() + 1):
                    self.add_tile(self.get_current_x_position() + i + 4, self.get_current_y_position() + 1, is_known = True)

            if has_obstacle:
                self.add_tile(self.get_current_x_position() + tile_count + 4, self.get_current_y_position() + 1, is_known = True, is_obstacle = True)

            # adding right tiles
            tile_count, has_obstacle = self.__get_tile_count(sensor_data["right"])

            for i in range(tile_count):
                if not self.__get_tile(self.get_current_x_position() + i + 4, self.get_current_y_position() - 1):
                    self.add_tile(self.get_current_x_position() + i + 4, self.get_current_y_position() - 1, is_known = True)

            if has_obstacle:
                self.add_tile(self.get_current_x_position() + tile_count + 4, self.get_current_y_position() - 1, is_known = True, is_obstacle = True)

        elif self.__orientation == 'S':
            # adding forward tiles
            tile_count, has_obstacle = self.__get_tile_count(sensor_data["front"])

            for i in range(tile_count):
                if not self.__get_tile(self.get_current_x_position(), self.get_current_y_position() - i - 4):
                    self.add_tile(self.get_current_x_position(), self.get_current_y_position() - i - 4, is_known = True)

            if has_obstacle:
                self.add_tile(self.get_current_x_position(), self.get_current_y_position() - tile_count - 4, is_known = True, is_obstacle = True)

            # adding left tiles
            tile_count, has_obstacle = self.__get_tile_count(sensor_data["left"])

            for i in range(tile_count):
                if not self.__get_tile(self.get_current_x_position() + 1, self.get_current_y_position() - i - 4):
                    self.add_tile(self.get_current_x_position() + 1, self.get_current_y_position() - i - 4, is_known = True)

            if has_obstacle:
                self.add_tile(self.get_current_x_position() + 1, self.get_current_y_position() - tile_count - 4, is_known = True, is_obstacle = True)

            # adding right tiles
            tile_count, has_obstacle = self.__get_tile_count(sensor_data["right"])

            for i in range(tile_count):
                if not self.__get_tile(self.get_current_x_position() - 1, self.get_current_y_position() - i - 4):
                    self.add_tile(self.get_current_x_position() - 1, self.get_current_y_position() - i - 4, is_known = True)

            if has_obstacle:
                self.add_tile(self.get_current_x_position() - 1, self.get_current_y_position() - tile_count - 4, is_known = True, is_obstacle = True)

        elif self.__orientation == 'W':
            # adding forward tiles
            tile_count, has_obstacle = self.__get_tile_count(sensor_data["front"])

            for i in range(tile_count):
                if not self.__get_tile(self.get_current_x_position() - i - 4, self.get_current_y_position()):
                    self.add_tile(self.get_current_x_position() - i - 4, self.get_current_y_position(), is_known = True)

            if has_obstacle:
                self.add_tile(self.get_current_x_position() - tile_count - 4, self.get_current_y_position(), is_known = True, is_obstacle = True)

            # adding left tiles
            tile_count, has_obstacle = self.__get_tile_count(sensor_data["left"])

            for i in range(tile_count):
                if not self.__get_tile(self.get_current_x_position() - i - 4, self.get_current_y_position() - 1):
                    self.add_tile(self.get_current_x_position() - i - 4, self.get_current_y_position() - 1, is_known = True)

            if has_obstacle:
                self.add_tile(self.get_current_x_position() - tile_count - 3, self.get_current_y_position() - 1, is_known = True, is_obstacle = True)

            # adding right tiles
            tile_count, has_obstacle = self.__get_tile_count(sensor_data["right"])

            for i in range(tile_count):
                if not self.__get_tile(self.get_current_x_position() - i - 4, self.get_current_y_position() + 1):
                    self.add_tile(self.get_current_x_position() - i - 4, self.get_current_y_position() + 1, is_known = True)

            if has_obstacle:
                self.add_tile(self.get_current_x_position() - tile_count - 4, self.get_current_y_position() + 1, is_known = True, is_obstacle = True)


    def is_obstacle(self, x, y) -> bool:
        key = str(x) + "," + str(y)

        if key not in self.__map:
            return False

        return self.__map[key].is_obstacle


    def check_for_obstacles(self, direction) -> bool:
        if direction == 'f':
            if self.__orientation == 'N':
                for x in range(self.get_current_x_position() - 2, self.get_current_x_position() + 3):
                    for y in range(self.get_current_y_position() + 4, self.get_current_y_position() + 4 + Map_Constants.OBSTACLE_CHECKING_RANGE):
                        if self.is_obstacle(x, y):
                            return True

            elif self.__orientation == 'E':
                for x in range(self.get_current_x_position() + 4, self.get_current_x_position() + 4 + Map_Constants.OBSTACLE_CHECKING_RANGE):
                    for y in range(self.get_current_y_position() - 2, self.get_current_y_position() + 3):
                        if self.is_obstacle(x, y):
                            return True

            elif self.__orientation == 'S':
                for x in range(self.get_current_x_position() - 2, self.get_current_x_position() + 3):
                    for y in range(self.get_current_y_position() - 3 - Map_Constants.OBSTACLE_CHECKING_RANGE, self.get_current_y_position() - 3):
                        if self.is_obstacle(x, y):
                            return True

            elif self.__orientation == 'W':
                for x in range(self.get_current_x_position() - 3 - Map_Constants.OBSTACLE_CHECKING_RANGE, self.get_current_x_position() - 3):
                    for y in range(self.get_current_y_position() - 2, self.get_current_y_position() + 3):
                        if self.is_obstacle(x, y):
                            return True

        
        elif (direction == 'b' and self.__orientation == 'N') or \
             (direction == 'l' and self.__orientation == 'W') or \
             (direction == 'r' and self.__orientation == 'E'):

             for x in range(self.get_current_x_position() - 2, self.get_current_x_position() + 3):
                for y in range(self.get_current_y_position() - 1 - Map_Constants.OBSTACLE_CHECKING_RANGE, self.get_current_y_position() - 1):
                    if self.is_obstacle(x, y):
                        return True


        elif (direction == 'b' and self.__orientation == 'E') or \
             (direction == 'l' and self.__orientation == 'N') or \
             (direction == 'r' and self.__orientation == 'S'):

             for x in range(self.get_current_x_position() - 1 - Map_Constants.OBSTACLE_CHECKING_RANGE, self.get_current_x_position() - 1):
                for y in range(self.get_current_y_position() - 2, self.get_current_y_position() + 3):
                    if self.is_obstacle(x, y):
                        return True
        

        elif (direction == 'b' and self.__orientation == 'S') or \
             (direction == 'l' and self.__orientation == 'E') or \
             (direction == 'r' and self.__orientation == 'W'):

             for x in range(self.get_current_x_position() - 2, self.get_current_x_position() + 3):
                for y in range(self.get_current_y_position() + 2, self.get_current_y_position() + 2 + Map_Constants.OBSTACLE_CHECKING_RANGE):
                    if self.is_obstacle(x, y):
                        return True


        elif (direction == 'b' and self.__orientation == 'W') or \
             (direction == 'l' and self.__orientation == 'S') or \
             (direction == 'r' and self.__orientation == 'N'):

            for x in range(self.get_current_x_position() + 2, self.get_current_x_position() + 2 + Map_Constants.OBSTACLE_CHECKING_RANGE):
                for y in range(self.get_current_y_position() - 2, self.get_current_y_position() + 3):
                    if self.is_obstacle(x, y):
                        return True
        
        
        return False


    def is_facing_obstacle(self):
        if self.__orientation == 'N':
            return self.is_obstacle(self.get_current_x_position(), self.get_current_y_position() + 1) or \
                   self.is_obstacle(self.get_current_x_position() + 1, self.get_current_y_position() + 1) or \
                   self.is_obstacle(self.get_current_x_position() - 1, self.get_current_y_position() + 1)
        
        elif self.__orientation == 'E':
            return self.is_obstacle(self.get_current_x_position() + 1, self.get_current_y_position()) or \
                   self.is_obstacle(self.get_current_x_position() + 1, self.get_current_y_position() + 1) or \
                   self.is_obstacle(self.get_current_x_position() + 1, self.get_current_y_position() - 1)
        
        elif self.__orientation == 'S':
            return self.is_obstacle(self.get_current_x_position(), self.get_current_y_position() - 1) or \
                   self.is_obstacle(self.get_current_x_position() + 1, self.get_current_y_position() - 1) or \
                   self.is_obstacle(self.get_current_x_position() - 1, self.get_current_y_position() - 1)
        
        elif self.__orientation == 'W':
            return self.is_obstacle(self.get_current_x_position() - 1, self.get_current_y_position()) or \
                   self.is_obstacle(self.get_current_x_position() - 1, self.get_current_y_position() + 1) or \
                   self.is_obstacle(self.get_current_x_position() - 1, self.get_current_y_position() - 1)

    
    def is_obstacle_on_left(self):
        if self.__orientation == 'N':
            return self.is_obstacle(self.get_current_x_position() - 1, self.get_current_y_position())

        elif self.__orientation == 'E':
            return self.is_obstacle(self.get_current_x_position(), self.get_current_y_position() + 1)

        elif self.__orientation == 'S':
            return self.is_obstacle(self.get_current_x_position() + 1, self.get_current_y_position())

        elif self.__orientation == 'W':
            return self.is_obstacle(self.get_current_x_position(), self.get_current_y_position() - 1)

    
    def is_obstacle_on_right(self):
        if self.__orientation == 'N':
            return self.is_obstacle(self.get_current_x_position() + 1, self.get_current_y_position())

        elif self.__orientation == 'E':
            return self.is_obstacle(self.get_current_x_position(), self.get_current_y_position() - 1)

        elif self.__orientation == 'S':
            return self.is_obstacle(self.get_current_x_position() - 1, self.get_current_y_position())

        elif self.__orientation == 'W':
            return self.is_obstacle(self.get_current_x_position(), self.get_current_y_position() + 1)


    def get_shortest_path(self) -> list:
        path = []

        start_tile = self.__map[str(self.__starting_tile_position[0]) + "," + str(self.__starting_tile_position[1])]
        end_tile = self.__map[str(self.get_current_x_position()) + "," + str(self.get_current_y_position())]
        start_tile.set_distance(0)
        self.__calculate_distances(start_tile)

        if end_tile.get_distance() is None:
            return path

        cur_tile = end_tile

        for i in range(cur_tile.get_distance()):
            path.append(cur_tile)
            cur_tile = self.__get_lowest_distance_neighbour(cur_tile)

        return path[::-1]


    def print_tile_info(self, tile):
        print("Position: ", tile.get_position())
        print("times_visited: ", tile.get_times_visited())
        print("distance: ", tile.get_distance())
        print("is_known: ", tile.is_known)
        print("is_obstacle: ", tile.is_obstacle)
        print()


    def print_map_info(self):
        for x in self.__map:
            tile = self.__map[x]
            self.print_tile_info(tile)


    def display_tile(self, x, y):
        key = str(x) + "," + str(y)

        if x == self.__starting_tile_position[0] and y == self.__starting_tile_position[1]:
            print("S", end="")

        elif x == self.get_current_x_position() and y == self.get_current_y_position():
            print("X", end="")

        elif key in self.__map:
            tile = self.__map[key]

            if tile:
                if tile.is_under_robot:
                    print("R", end="")

                elif tile.is_obstacle:
                    print("#", end="")

                elif tile.get_times_visited() > 0:
                    print(".", end="")

                elif not tile.is_known:
                    print("?", end="")

                elif tile.get_distance():
                    print(tile.get_distance(), end="")

                else:
                    print("N", end="")

        else:
            print(" ", end="")


    def display_map(self):
        for y in range(self.__bounds[2], self.__bounds[3] + 1)[::-1]:
            for x in range(self.__bounds[0], self.__bounds[1] + 1):
                self.display_tile(x, y)

            print()
