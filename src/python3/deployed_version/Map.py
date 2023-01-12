from math import floor

from Map_Tile import Map_Tile

from Constants import Map_Constants


# Robot's size:
# Width = 3 Tiles
# Length = 5 Tiles

# After initialising the Map, the default tiles will represent the robot's size.
# Example of the map after initialisation:
#
#       RRR
#       RRR
#       RRR
#       RXR
#       RRR
#
# X - Is the tile, that will be used to track the robot's position.


class Map:
    def __init__(self):
        self.__map = {}

        # [-x, x, -y, y]
        self.__bounds = [0, 0, 0, 0]

        # N - North, E - East, S - South, W - West
        self.__orientation = 'N'

        # [x, y]
        self.__starting_tile_position = [0, 0]
        self.__current_tile_position = [0, 0]

        # Stores tracked tile position and orientation where was the last searched object seen
        self.__last_object_position = {
            "x": None,
            "y": None,
            "orientation": None
        }

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


    def __is_obstacle(self, x, y) -> bool:
        key = str(x) + "," + str(y)

        if key not in self.__map:
            return False

        return self.__map[key].is_obstacle

    
    def __get_tile_count(self, distance):
        tile_count = floor(distance / Map_Constants.TILE_SIZE)

        if tile_count > Map_Constants.VISION_RANGE:
            return Map_Constants.VISION_RANGE, False

        else:
            return tile_count, True


    def __get_neighbouring_tiles(self, tile) -> list:
        neighbours = []

        if not tile:
            return neighbours

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
            if neighbours[i].is_obstacle or not neighbours[i].is_known:
                continue

            elif neighbours[i].get_distance() is None or neighbours[i].get_distance() > n + 1:
                x = neighbours[i].get_x_position()
                y = neighbours[i].get_y_position()

                self.__map[str(x) + "," + str(y)].set_distance(n + 1)

                neighbours[i].set_distance(n + 1)

                if neighbours[i].get_position() == self.__current_tile_position:
                    break

                self.__calculate_distances(neighbours[i], n + 1)

    
    def __has_empty_neighbours(self, tile):
        neighbours = self.__get_neighbouring_tiles(tile)
        for neighbour in neighbours:
            if neighbour.is_obstacle:
                continue
            return True
        return False


    def __get_lowest_distance_neighbour(self, tile) -> Map_Tile:
        neighbours = self.__get_neighbouring_tiles(tile)
        lowest_distance = None
        lowest_distance_neighbour = None

        if not neighbours:
            return None

        for neighbour in neighbours:
            if neighbour and neighbour.get_distance():
                if neighbour.is_obstacle:
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


    def __check_corners_for_obstacles(self, direction):
        if (direction == 'l' and self.__orientation == 'N') or (direction == 'r' and self.__orientation == 'W'):
            for x in range(self.get_current_x_position() - 3, self.get_current_x_position() - 1):
                for y in range(self.get_current_y_position() + 3, self.get_current_y_position() + 4):
                    if self.__is_obstacle(x, y):
                        return True

        elif (direction == 'l' and self.__orientation == 'E') or (direction == 'r' and self.__orientation == 'N'):
            for x in range(self.get_current_x_position() + 2, self.get_current_x_position() + 4):
                for y in range(self.get_current_y_position() + 3, self.get_current_y_position() + 4):
                    if self.__is_obstacle(x, y):
                        return True

        elif (direction == 'l' and self.__orientation == 'S') or (direction == 'r' and self.__orientation == 'E'):
            for x in range(self.get_current_x_position()+ 2, self.get_current_x_position() + 4):
                for y in range(self.get_current_y_position() - 3, self.get_current_y_position() - 2):
                    if self.__is_obstacle(x, y):
                        return True

        elif (direction == 'l' and self.__orientation == 'W') or (direction == 'r' and self.__orientation == 'S'):
            for x in range(self.get_current_x_position() - 3, self.get_current_x_position() - 1):
                for y in range(self.get_current_y_position() - 3, self.get_current_y_position() - 2):
                    if self.__is_obstacle(x, y):
                        return True

        return False
            

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

    
    def update_position(self, direction):
        if self.__orientation == 'N' or self.__orientation == 'S':
            min_x_range = self.get_current_x_position() - 1
            max_x_range = self.get_current_x_position() + 2

            y_axis_to_mark = None
            y_axis_to_unmark = None

            if self.__orientation == 'N':
                if direction == 'f':
                    self.__current_tile_position[1] += 1

                    y_axis_to_mark = self.get_current_y_position() + 3
                    y_axis_to_unmark = self.get_current_y_position() - 2

                elif direction == 'b':
                    self.__current_tile_position[1] -= 1

                    y_axis_to_mark = self.get_current_y_position() - 1
                    y_axis_to_unmark = self.get_current_y_position() + 4


            elif self.__orientation == 'S':
                if direction == 'f':
                    self.__current_tile_position[1] -= 1

                    y_axis_to_mark = self.get_current_y_position() - 3
                    y_axis_to_unmark = self.get_current_y_position() + 2

                elif direction == 'b':
                    self.__current_tile_position[1] += 1

                    y_axis_to_mark = self.get_current_y_position() + 1
                    y_axis_to_unmark = self.get_current_y_position() - 4


            for x in range(min_x_range, max_x_range):
                tile_to_mark = self.__get_tile(x, y_axis_to_mark)
                tile_to_unmark = self.__get_tile(x, y_axis_to_unmark)

                # Setting is_under_robot to True, because the Robot has moved and is "on" the tile
                if tile_to_mark:
                    tile_to_mark.increment_times_visited()
                    tile_to_mark.is_under_robot = True
                    tile_to_mark.is_obstacle = False

                else:
                    self.add_tile(x, y_axis_to_mark, times_visited = 1, is_known = True, is_under_robot = True) 


                # Setting is_under_robot to False, because the Robot has moved and is no longer "on" the tile
                if tile_to_unmark:
                    tile_to_unmark.is_under_robot = False


        elif self.__orientation == 'W' or self.__orientation == 'E':
            min_y_range = self.get_current_y_position() - 1
            max_y_range = self.get_current_y_position() + 2

            x_axis_to_mark = None
            x_axis_to_unmart = None

            if self.__orientation == 'W':
                if direction == 'f':
                    self.__current_tile_position[0] -= 1

                    x_axis_to_mark = self.get_current_x_position() - 3
                    x_axis_to_unmark = self.get_current_x_position() + 2

                elif direction == 'b':
                    self.__current_tile_position[0] += 1

                    x_axis_to_mark = self.get_current_x_position() + 1
                    x_axis_to_unmark = self.get_current_x_position() - 4


            elif self.__orientation == 'E':
                if direction == 'f':
                    self.__current_tile_position[0] += 1

                    x_axis_to_mark = self.get_current_x_position() + 3
                    x_axis_to_unmark = self.get_current_x_position() - 2

                elif direction == 'b':
                    self.__current_tile_position[0] -= 1

                    x_axis_to_mark = self.get_current_x_position() - 1
                    x_axis_to_unmark = self.get_current_x_position() + 4


            for y in range(min_y_range, max_y_range):
                tile_to_mark = self.__get_tile(x_axis_to_mark, y)
                tile_to_unmark = self.__get_tile(x_axis_to_unmark, y)

                # Setting is_under_robot to True, because the Robot has moved and is "on" the tile
                if tile_to_mark:
                    tile_to_mark.increment_times_visited()
                    tile_to_mark.is_under_robot = True
                    tile_to_mark.is_obstacle = False

                else:
                    self.add_tile(x_axis_to_mark, y, times_visited = 1, is_known = True, is_under_robot = True) 


                # Setting is_under_robot to False, because the Robot has moved and is no longer "on" the tile
                if tile_to_unmark:
                    tile_to_unmark.is_under_robot = False
                

    def update_map(self, sensor_data):
        if self.__orientation == 'N':
            # Updating tiles in the front (middle)
            tile_count, has_obstacle = self.__get_tile_count(sensor_data['f'])
            x = self.get_current_x_position()
            y = self.get_current_y_position() + 4 

            for i in range(tile_count):
                if self.__get_tile(x, y + i):
                    self.__get_tile(x, y + i).is_obstacle = False

                else: 
                    self.add_tile(x, y + i, is_known = True)

            if has_obstacle:
                y += tile_count

                if self.__get_tile(x, y):
                    self.__get_tile(x, y).is_obstacle = True

                else:
                    self.add_tile(x, y, is_known = True, is_obstacle = True)

            # Updating tiles in the back (middle)
            tile_count, has_obstacle = self.__get_tile_count(sensor_data['b'])
            y = self.get_current_y_position() - 2

            for i in range(tile_count):
                if self.__get_tile(x, y - i):
                    self.__get_tile(x, y - i).is_obstacle = False

                else:
                    self.add_tile(x, y - i , is_known = True)

            if has_obstacle:
                y -= tile_count

                if self.__get_tile(x, y):
                    self.__get_tile(x, y).is_obstacle = True

                else:
                    self.add_tile(x, y, is_known = True, is_obstacle = True)

            # Updating tiles in the front (left)
            tile_count, has_obstacle = self.__get_tile_count(sensor_data['l'])
            x = self.get_current_x_position() - 1
            y = self.get_current_y_position() + 4

            for i in range(tile_count):
                if self.__get_tile(x, y + i):
                    self.__get_tile(x, y + i).is_obstacle = False

                else:
                    self.add_tile(x, y + i, is_known = True)

            if has_obstacle:
                y += tile_count

                if self.__get_tile(x, y):
                    self.__get_tile(x, y).is_obstacle = True

                else:
                    self.add_tile(x, y, is_known = True, is_obstacle = True)

            # Updating tiles in the front (right)
            tile_count, has_obstacle = self.__get_tile_count(sensor_data['r'])
            x = self.get_current_x_position() + 1
            y = self.get_current_y_position() + 4

            for i in range(tile_count):
                if self.__get_tile(x, y + i):
                    self.__get_tile(x, y + i).is_obstacle = False

                else:
                    self.add_tile(x, y + i, is_known = True)

            if has_obstacle:
                y += tile_count

                if self.__get_tile(x, y):
                    self.__get_tile(x, y).is_obstacle = True

                else:
                    self.add_tile(x, y, is_known = True, is_obstacle = True)


        elif self.__orientation == 'E':
            # Updating tiles in the front (middle)
            tile_count, has_obstacle = self.__get_tile_count(sensor_data['f'])
            x = self.get_current_x_position() + 4
            y = self.get_current_y_position()

            for i in range(tile_count):
                if self.__get_tile(x + i, y):
                    self.__get_tile(x + i, y).is_obstacle = False

                else: 
                    self.add_tile(x + i, y, is_known = True)

            if has_obstacle:
                x += tile_count

                if self.__get_tile(x, y):
                    self.__get_tile(x, y).is_obstacle = True

                else:
                    self.add_tile(x, y, is_known = True, is_obstacle = True)

            # Updating tiles in the back (middle)
            tile_count, has_obstacle = self.__get_tile_count(sensor_data['b'])
            x = self.get_current_x_position() - 2

            for i in range(tile_count):
                if self.__get_tile(x - i, y):
                    self.__get_tile(x - i, y).is_obstacle = False

                else:
                    self.add_tile(x - i, y, is_known = True)

            if has_obstacle:
                x -= tile_count

                if self.__get_tile(x, y):
                    self.__get_tile(x, y).is_obstacle = True

                else:
                    self.add_tile(x, y, is_known = True, is_obstacle = True)

            # Updating tiles in the front (left)
            tile_count, has_obstacle = self.__get_tile_count(sensor_data['l'])
            x = self.get_current_x_position() + 4
            y = self.get_current_y_position() + 1

            for i in range(tile_count):
                if self.__get_tile(x + i, y):
                    self.__get_tile(x + i, y).is_obstacle = False

                else:
                    self.add_tile(x + i, y, is_known = True)

            if has_obstacle:
                x += tile_count

                if self.__get_tile(x, y):
                    self.__get_tile(x, y).is_obstacle = True

                else:
                    self.add_tile(x, y, is_known = True, is_obstacle = True)

            # Updating tiles in the front (right)
            tile_count, has_obstacle = self.__get_tile_count(sensor_data['r'])
            x = self.get_current_x_position() + 4
            y = self.get_current_y_position() - 1

            for i in range(tile_count):
                if self.__get_tile(x + i, y):
                    self.__get_tile(x + i, y).is_obstacle = False

                else:
                    self.add_tile(x + i, y, is_known = True)

            if has_obstacle:
                x += tile_count

                if self.__get_tile(x, y):
                    self.__get_tile(x, y).is_obstacle = True

                else:
                    self.add_tile(x, y, is_known = True, is_obstacle = True)


        elif self.__orientation == 'S':
            # Updating tiles in the front (middle)
            tile_count, has_obstacle = self.__get_tile_count(sensor_data['f'])
            x = self.get_current_x_position() 
            y = self.get_current_y_position() - 4

            for i in range(tile_count):
                if self.__get_tile(x, y - i):
                    self.__get_tile(x, y - i).is_obstacle = False

                else: 
                    self.add_tile(x, y - i, is_known = True)

            if has_obstacle:
                y -= tile_count

                if self.__get_tile(x, y):
                    self.__get_tile(x, y).is_obstacle = True

                else:
                    self.add_tile(x, y, is_known = True, is_obstacle = True)

            # Updating tiles in the back (middle)
            tile_count, has_obstacle = self.__get_tile_count(sensor_data['b'])
            y = self.get_current_y_position() + 2

            for i in range(tile_count):
                if self.__get_tile(x, y + i):
                    self.__get_tile(x, y + i).is_obstacle = False

                else:
                    self.add_tile(x, y + i , is_known = True)

            if has_obstacle:
                y += tile_count

                if self.__get_tile(x, y):
                    self.__get_tile(x, y).is_obstacle = True

                else:
                    self.add_tile(x, y, is_known = True, is_obstacle = True)

            # Updating tiles in the front (left)
            tile_count, has_obstacle = self.__get_tile_count(sensor_data['l'])
            x = self.get_current_x_position() + 1
            y = self.get_current_y_position() - 4

            for i in range(tile_count):
                if self.__get_tile(x, y - i):
                    self.__get_tile(x, y - i).is_obstacle = False

                else:
                    self.add_tile(x, y - i, is_known = True)

            if has_obstacle:
                y -= tile_count

                if self.__get_tile(x, y):
                    self.__get_tile(x, y).is_obstacle = True

                else:
                    self.add_tile(x, y, is_known = True, is_obstacle = True)

            # Updating tiles in the front (right)
            tile_count, has_obstacle = self.__get_tile_count(sensor_data['r'])
            x = self.get_current_x_position() - 1
            y = self.get_current_y_position() - 4

            for i in range(tile_count):
                if self.__get_tile(x, y - i):
                    self.__get_tile(x, y - i).is_obstacle = False

                else:
                    self.add_tile(x, y - i, is_known = True)

            if has_obstacle:
                y -= tile_count

                if self.__get_tile(x, y):
                    self.__get_tile(x, y).is_obstacle = True

                else:
                    self.add_tile(x, y, is_known = True, is_obstacle = True)


        elif self.__orientation == 'W':
            # Updating tiles in the front (middle)
            tile_count, has_obstacle = self.__get_tile_count(sensor_data['f'])
            x = self.get_current_x_position() - 4
            y = self.get_current_y_position()

            for i in range(tile_count):
                if self.__get_tile(x - i, y):
                    self.__get_tile(x - i, y).is_obstacle = False

                else: 
                    self.add_tile(x - i, y, is_known = True)

            if has_obstacle:
                x -= tile_count

                if self.__get_tile(x, y):
                    self.__get_tile(x, y).is_obstacle = True

                else:
                    self.add_tile(x, y, is_known = True, is_obstacle = True)

            # Updating tiles in the back (middle)
            tile_count, has_obstacle = self.__get_tile_count(sensor_data['b'])
            x = self.get_current_x_position() + 2

            for i in range(tile_count):
                if self.__get_tile(x + i, y):
                    self.__get_tile(x + i, y).is_obstacle = False

                else:
                    self.add_tile(x + i, y, is_known = True)

            if has_obstacle:
                x += tile_count

                if self.__get_tile(x, y):
                    self.__get_tile(x, y).is_obstacle = True

                else:
                    self.add_tile(x, y, is_known = True, is_obstacle = True)

            # Updating tiles in the front (left)
            tile_count, has_obstacle = self.__get_tile_count(sensor_data['l'])
            x = self.get_current_x_position() - 4
            y = self.get_current_y_position() - 1

            for i in range(tile_count):
                if self.__get_tile(x - i, y):
                    self.__get_tile(x - i, y).is_obstacle = False

                else:
                    self.add_tile(x - i, y, is_known = True)

            if has_obstacle:
                x -= tile_count

                if self.__get_tile(x, y):
                    self.__get_tile(x, y).is_obstacle = True

                else:
                    self.add_tile(x, y, is_known = True, is_obstacle = True)

            # Updating tiles in the front (right)
            tile_count, has_obstacle = self.__get_tile_count(sensor_data['r'])
            x = self.get_current_x_position() - 4
            y = self.get_current_y_position() + 1

            for i in range(tile_count):
                if self.__get_tile(x - i, y):
                    self.__get_tile(x - i, y).is_obstacle = False

                else:
                    self.add_tile(x - i, y, is_known = True)

            if has_obstacle:
                x -= tile_count

                if self.__get_tile(x, y):
                    self.__get_tile(x, y).is_obstacle = True

                else:
                    self.add_tile(x, y, is_known = True, is_obstacle = True)


    def check_for_obstacles(self, direction) -> bool:
        if self.__check_corners_for_obstacles(direction):
            return True

        if direction == 'f':
            if self.__orientation == 'N':
                for x in range(self.get_current_x_position() - 2, self.get_current_x_position() + 3):
                    for y in range(self.get_current_y_position() + 4, self.get_current_y_position() + 4 + Map_Constants.OBSTACLE_CHECKING_RANGE):
                        if self.__is_obstacle(x, y):
                            return True

            elif self.__orientation == 'E':
                for x in range(self.get_current_x_position() + 4, self.get_current_x_position() + 4 + Map_Constants.OBSTACLE_CHECKING_RANGE):
                    for y in range(self.get_current_y_position() - 2, self.get_current_y_position() + 3):
                        if self.__is_obstacle(x, y):
                            return True

            elif self.__orientation == 'S':
                for x in range(self.get_current_x_position() - 2, self.get_current_x_position() + 3):
                    for y in range(self.get_current_y_position() - 3 - Map_Constants.OBSTACLE_CHECKING_RANGE, self.get_current_y_position() - 3):
                        if self.__is_obstacle(x, y):
                            return True

            elif self.__orientation == 'W':
                for x in range(self.get_current_x_position() - 3 - Map_Constants.OBSTACLE_CHECKING_RANGE, self.get_current_x_position() - 3):
                    for y in range(self.get_current_y_position() - 2, self.get_current_y_position() + 3):
                        if self.__is_obstacle(x, y):
                            return True

        
        elif (direction == 'b' and self.__orientation == 'N') or \
             (direction == 'l' and self.__orientation == 'W') or \
             (direction == 'r' and self.__orientation == 'E'):

             for x in range(self.get_current_x_position() - 2, self.get_current_x_position() + 3):
                for y in range(self.get_current_y_position() - 1 - Map_Constants.OBSTACLE_CHECKING_RANGE, self.get_current_y_position() - 1):
                    if self.__is_obstacle(x, y):
                        return True


        elif (direction == 'b' and self.__orientation == 'E') or \
             (direction == 'l' and self.__orientation == 'N') or \
             (direction == 'r' and self.__orientation == 'S'):

             for x in range(self.get_current_x_position() - 1 - Map_Constants.OBSTACLE_CHECKING_RANGE, self.get_current_x_position() - 1):
                for y in range(self.get_current_y_position() - 2, self.get_current_y_position() + 3):
                    if self.__is_obstacle(x, y):
                        return True
        

        elif (direction == 'b' and self.__orientation == 'S') or \
             (direction == 'l' and self.__orientation == 'E') or \
             (direction == 'r' and self.__orientation == 'W'):

             for x in range(self.get_current_x_position() - 2, self.get_current_x_position() + 3):
                for y in range(self.get_current_y_position() + 2, self.get_current_y_position() + 2 + Map_Constants.OBSTACLE_CHECKING_RANGE):
                    if self.__is_obstacle(x, y):
                        return True


        elif (direction == 'b' and self.__orientation == 'W') or \
             (direction == 'l' and self.__orientation == 'S') or \
             (direction == 'r' and self.__orientation == 'N'):

            for x in range(self.get_current_x_position() + 2, self.get_current_x_position() + 2 + Map_Constants.OBSTACLE_CHECKING_RANGE):
                for y in range(self.get_current_y_position() - 2, self.get_current_y_position() + 3):
                    if self.__is_obstacle(x, y):
                        return True
        
        
        return False


    def check_visited_tiles(self, direction) -> int:
        max_times_visited = 0


        if direction == 'f':
            if self.__orientation == 'N':
                for x in range(self.get_current_x_position() - 1, self.get_current_x_position() + 2):
                    for y in range(self.get_current_y_position() + 4, self.get_current_y_position() + 4 + Map_Constants.VISITED_TILES_CHECKING_RANGE):
                        tile = self.__get_tile(x, y)

                        if tile and tile.get_times_visited() > max_times_visited:
                            max_times_visited = tile.get_times_visited()

            elif self.__orientation == 'E':
                for x in range(self.get_current_x_position() + 4, self.get_current_x_position() + 4 + Map_Constants.VISITED_TILES_CHECKING_RANGE):
                    for y in range(self.get_current_y_position() - 1, self.get_current_y_position() + 2):
                        tile = self.__get_tile(x, y)

                        if tile and tile.get_times_visited() > max_times_visited:
                            max_times_visited = tile.get_times_visited()

            elif self.__orientation == 'S':
                for x in range(self.get_current_x_position() - 1, self.get_current_x_position() + 2):
                    for y in range(self.get_current_y_position() - 3 - Map_Constants.VISITED_TILES_CHECKING_RANGE, self.get_current_y_position() - 3):
                        tile = self.__get_tile(x, y)

                        if tile and tile.get_times_visited() > max_times_visited:
                            max_times_visited = tile.get_times_visited()

            elif self.__orientation == 'W':
                for x in range(self.get_current_x_position() - 3 - Map_Constants.VISITED_TILES_CHECKING_RANGE, self.get_current_x_position() - 3):
                    for y in range(self.get_current_y_position() - 1, self.get_current_y_position() + 2):
                        tile = self.__get_tile(x, y)

                        if tile and tile.get_times_visited() > max_times_visited:
                            max_times_visited = tile.get_times_visited()

        
        elif (direction == 'b' and self.__orientation == 'N') or \
             (direction == 'l' and self.__orientation == 'W') or \
             (direction == 'r' and self.__orientation == 'E'):

             for x in range(self.get_current_x_position() - 1, self.get_current_x_position() + 2):
                for y in range(self.get_current_y_position() - 1 - Map_Constants.VISITED_TILES_CHECKING_RANGE, self.get_current_y_position() - 1):
                    tile = self.__get_tile(x, y)

                    if tile and tile.get_times_visited() > max_times_visited:
                            max_times_visited = tile.get_times_visited()


        elif (direction == 'b' and self.__orientation == 'E') or \
             (direction == 'l' and self.__orientation == 'N') or \
             (direction == 'r' and self.__orientation == 'S'):

             for x in range(self.get_current_x_position() - 1 - Map_Constants.VISITED_TILES_CHECKING_RANGE, self.get_current_x_position() - 1):
                for y in range(self.get_current_y_position() - 1, self.get_current_y_position() + 2):
                    tile = self.__get_tile(x, y)

                    if tile and tile.get_times_visited() > max_times_visited:
                            max_times_visited = tile.get_times_visited()
        

        elif (direction == 'b' and self.__orientation == 'S') or \
             (direction == 'l' and self.__orientation == 'E') or \
             (direction == 'r' and self.__orientation == 'W'):

             for x in range(self.get_current_x_position() - 1, self.get_current_x_position() + 2):
                for y in range(self.get_current_y_position() + 2, self.get_current_y_position() + 2 + Map_Constants.VISITED_TILES_CHECKING_RANGE):
                    tile = self.__get_tile(x, y)

                    if tile and tile.get_times_visited() > max_times_visited:
                            max_times_visited = tile.get_times_visited()


        elif (direction == 'b' and self.__orientation == 'W') or \
             (direction == 'l' and self.__orientation == 'S') or \
             (direction == 'r' and self.__orientation == 'N'):

            for x in range(self.get_current_x_position() + 2, self.get_current_x_position() + 2 + Map_Constants.VISITED_TILES_CHECKING_RANGE):
                for y in range(self.get_current_y_position() - 1, self.get_current_y_position() + 2):
                    tile = self.__get_tile(x, y)

                    if tile and tile.get_times_visited() > max_times_visited:
                            max_times_visited = tile.get_times_visited()
        
        
        return max_times_visited


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
            if cur_tile:
                path.append(cur_tile)

            cur_tile = self.__get_lowest_distance_neighbour(cur_tile)

        if not path:
            return None

        path.append(self.__get_tile(0, 0))

        return path


    def remove_distances_from_tiles(self):
        for y in range(self.__bounds[2], self.__bounds[3] + 1)[::-1]:
            for x in range(self.__bounds[0], self.__bounds[1] + 1):
                tile = self.__get_tile(x, y)

                if tile:
                    tile.set_distance(None)


    def set_last_object_location(self):
        self.__last_object_position["x"] = self.__current_tile_position[0]
        self.__last_object_position["y"] = self.__current_tile_position[1]
        self.__last_object_position["orientation"] = self.__orientation


    def get_last_object_location(self):
        return self.__last_object_position


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

        elif x == self.__last_object_position["x"] and y == self.__last_object_position["y"]:
            print("O", end="")

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


    def reset(self):
        self.__map = {}
        self.__bounds = [0, 0, 0, 0]
        self.__orientation = 'N'
        self. __starting_tile_position = [0, 0]
        self.__current_tile_position = [0, 0]

        self.__setup_starting_position()
