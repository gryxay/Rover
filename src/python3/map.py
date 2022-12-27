from map_tile import Map_tile


class Map:
    def __init__(self):
        self.__map = {}
        # [-x, x, -y, y]
        self.__bounds = [0, 0, 0, 0]
        self.__orientation = 'N'

        # [x, y]
        self.__starting_tile_position = [0, 0]
        self.__current_tile_position = [0, 0]
        
        self.__map[str(self.__starting_tile_position[0]) + "," + str(self.__starting_tile_position[1])] = \
            Map_tile(self.__starting_tile_position[0], self.__starting_tile_position[1])


    # Private methods


    #def __setup_starting_position(self):
        # Starting posion should represent the robot's size
    

    def __update_bounds(self, x, y):
        if x < self.__bounds[0]:
            self.__bounds[0] = x

        elif x > self.__bounds[1]:
            self.__bounds[1] = x

        if y < self.__bounds[2]:
            self.__bounds[2] = y

        elif y > self.__bounds[3]:
            self.__bounds[3] = y


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


    def __calculate_distances(self, tile, n=0) -> list:
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


    def __get_lowest_distance_neighbour(self, tile) -> Map_tile:
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

    
    # Public methods


    def set_current_x_position(self, x):
        self.__current_tile_position[0] = x


    def get_current_x_position(self) -> int:
        return self.__current_tile_position[0]


    def set_current_y_position(self, y):
        self.__current_tile_position[1] = y


    def get_current_y_position(self) -> int:
        return self.__current_tile_position[1]


    def update_orientation(self, direction):
        if direction == 'l':
            if self.__orientation == 'N':
                self.__orientation = 'W'

            elif self.__orientation == 'W':
                self.__orientation = 'S'

            elif self.__orientation == 'S':
                self.__orientation = 'E'

            elif self.__orientation == 'E':
                self.__orientation = 'N'

        elif direction == 'r':
            if self.__orientation == 'N':
                self.__orientation = 'E'

            elif self.__orientation == 'E':
                self.orientation = 'S'

            elif self.__orientation == 'S':
                self.__orientation = 'W'

            elif self.__orientation == 'W':
                self.__orientation = 'N'


    def get_current_orientation(self) -> str:
        return self.__orientation

    # needs to be improved
    def update_position(self):
        if self.__orientation == 'N':
            self.__current_tile_position[1] = self.__current_tile_position[1] + 1

        elif self.__orientation == 'E':
            self.__current_tile_position[0] = self.__current_tile_position[0] + 1

        elif self.__orientation == 'S':
            self.__current_tile_position[1] = self.__current_tile_position[1] - 1

        elif self.__orientation == 'W':
            self.__current_tile_position[0] = self.__current_tile_position[0] - 1


    def add_tile(self, x, y, times_visited = 0, is_known = False, is_obstacle = False) -> bool:
        key = str(x) + "," + str(y)

        self.__update_bounds(x, y)

        self.__map[key] = Map_tile(x, y, times_visited, is_known, is_obstacle)

        return True

    
    def get_tile(self, x, y) -> Map_tile:
        key = str(x) + "," + str(y)

        if key in self.__map:
            return self.__map[key]

        return None


    def get_current_tile(self) -> Map_tile:
        return self.__map[str(self.__current_tile_position[0]) + "," + str(self.__current_tile_position[1])]


    def is_obstacle(self, x, y) -> bool:
        key = str(x) + "," + str(y)

        if key not in self.__map:
            return False

        return self.__map[key].is_obstacle


    def get_shortest_path(self) -> list:
        path = []

        start_tile = self.__map[str(self.__starting_tile_position[0]) + "," + str(self.__starting_tile_position[1])]
        end_tile = self.__map[str(self.__current_tile_position[0]) + "," + str(self.__current_tile_position[1])]
        start_tile.set_distance(0)
        self.__calculate_distances(start_tile)

        if end_tile.get_distance() is None:
            return path

        cur_tile = end_tile

        for i in range(cur_tile.get_distance()):
            path.append(cur_tile)
            cur_tile = self.__get_lowest_distance_neighbour(cur_tile)

        return path[::-1]


    # Methods for visualisation


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

        if x == self.__current_tile_position[0] and y == self.__current_tile_position[1]:
            print("X", end="")

        elif x == self.__starting_tile_position[0] and y == self.__starting_tile_position[1]:
            print("S", end="")

        elif key in self.__map:
            tile = self.__map[key]

            if tile:
                if tile.is_obstacle:
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
