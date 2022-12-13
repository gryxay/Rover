class map_tile:
    def __init__(self, x, y, unknown=False, start=False, visited=False, obstacle=False, end=False) -> None:
        self.x = x
        self.y = y
        self.unknown = unknown
        self.is_obstacle = obstacle
        self.is_visited = visited
        self.is_start = start
        self.is_end = end
        self.distance = None

    def set_start(self, start) -> None:
        self.is_start = start
    
    def set_end(self, end) -> None:
        self.is_end = end

    def set_visited(self, visited) -> None:
        self.is_visited = visited

    def set_obstacle(self, obstacle) -> None:
        self.is_obstacle = obstacle
    
    def get_position(self) -> tuple:
        return (self.x, self.y)
    
    
class map:
    def __init__(self) -> None:
        self.cur_x = 0
        self.cur_y = 0
        self.bounds = [0, 0, 0, 0]
        self.map = {}
        self.start = [self.cur_x, self.cur_y]
        self.end = [None, None]
        self.map[str(self.cur_x) + str(self.cur_y)] = map_tile(
            self.cur_x, self.cur_y, start=True)
        
    
    def get_current_tile(self) -> map_tile:
        return self.map[str(self.cur_x) + str(self.cur_y)]
    
    def get_tile(self, x, y) -> map_tile:
        return self.map[str(x) + str(y)]

    def add_tile(self, x, y, unknown=False, start=False, visited=False, obstacle=False, end=False) -> bool:
        key = str(x) + str(y)
        #if key in self.map:
        #    return False
        self.__update_bounds(x, y)
        if start:
            self.start = [x, y]
        elif end:
            self.end = [x, y]
        self.map[key] = map_tile(x, y, unknown, start, visited, obstacle, end)
        return True
    
    def __update_bounds(self, x, y) -> None:
        if x < self.bounds[0]:
            self.bounds[0] = x
        elif x > self.bounds[1]:
            self.bounds[1] = x
        if y < self.bounds[2]:
            self.bounds[2] = y
        elif y > self.bounds[3]:
            self.bounds[3] = y

    def print_map_info(self) -> None:
        for x in self.map:
            tile = self.map[x]
            self.print_tile_info(tile)
    
    def display_map(self) -> None:
        for x in range(self.bounds[0], self.bounds[1] + 1)[::-1]:
            for y in range(self.bounds[2], self.bounds[3] + 1):
                self.display_tile(x, y)
            print()

    def display_tile(self, x, y) -> None:
        if x == self.cur_x and y == self.cur_y:
            print("X", end="")
        elif str(x) + str(y) in self.map:
            tile = self.map[str(x) + str(y)]
            if tile is not None:
                if tile.is_obstacle:
                    print("#", end="")
                elif tile.is_start:
                    print("S", end="")
                elif tile.is_end:
                    print("E", end="")
                elif tile.is_visited:
                    print(".", end="")
                elif tile.unknown:
                    print("?", end="")
                elif tile.distance is not None:
                    print(tile.distance, end="")
                else:
                    print("N", end="")
        else:
            print(" ", end="")
    
    def get_neighbours(self, tile) -> list:
        neighbours = []
        if str(tile.x) + str(tile.y + 1) in self.map:
            neighbours.append(self.map[str(tile.x) + str(tile.y + 1)])
        if str(tile.x) + str(tile.y - 1) in self.map:
            neighbours.append(self.map[str(tile.x) + str(tile.y - 1)])
        if str(tile.x + 1) + str(tile.y) in self.map:
            neighbours.append(self.map[str(tile.x + 1) + str(tile.y)])
        if str(tile.x - 1) + str(tile.y) in self.map:
            neighbours.append(self.map[str(tile.x - 1) + str(tile.y)])
        return neighbours

    def __calculate_distances(self, tile, n=0) -> list:
        neighbours = self.get_neighbours(tile)
        for i in range(len(neighbours)):
            if neighbours[i].is_obstacle or neighbours[i].unknown:
                continue
            elif neighbours[i].distance is None or neighbours[i].distance > n + 1:
                self.map[str(neighbours[i].x) +
                         str(neighbours[i].y)].distance = n + 1
                neighbours[i].distance = n + 1
                if neighbours[i].is_end:
                    break
                self.__calculate_distances(neighbours[i], n + 1)
            if n == 0:
                self.display_map()


    def get_lowest_distance_neighbour(self, tile) -> map_tile:
        neighbours = self.get_neighbours(tile)
        lowest_distance = None
        lowest_distance_neighbour = None
        for neighbour in neighbours:
            if neighbour.is_obstacle or neighbour.unknown:
                continue
            elif lowest_distance is None or neighbour.distance < lowest_distance:
                lowest_distance = neighbour.distance
                lowest_distance_neighbour = neighbour
        return lowest_distance_neighbour

    def get_shortest_path(self) -> list:
        path = []
        if self.start[0] is None or self.end[0] is None:
            return path
        start_tile = self.map[str(self.start[0]) + str(self.start[1])]
        end_tile = self.map[str(self.end[0]) + str(self.end[1])]
        start_tile.distance = 0
        self.__calculate_distances(start_tile)
        if end_tile.distance is None:
            return path
        cur_tile = end_tile
        for i in range(cur_tile.distance):
            path.append(cur_tile)
            cur_tile = self.get_lowest_distance_neighbour(cur_tile)
        return path[::-1]

    def print_tile_info(self, tile) -> None:
        print("Position: ", tile.get_position())
        print("is_obstacle: ", tile.is_obstacle)
        print("is_visited: ", tile.is_visited)
        print("is_start: ", tile.is_start)
        print("is_end: ", tile.is_end)
        print("distance: ", tile.distance)
        print("unknown: ", tile.unknown)
        print()


# Test
map = map()

map.add_tile(0, 0, start = True)  # Start tile
map.add_tile(1, 0, False, False, False, False)
map.add_tile(2, 0, False, False, False, False)
map.add_tile(3, 0, obstacle = True)  # Obstacle
map.add_tile(4, 0, False, False, False, False)
map.add_tile(5, 0, False, False, False, False)
map.add_tile(6, 0, False, False, False, False)
map.add_tile(7, 0, False, False, False, False)
map.add_tile(8, 0, False, False, False, False)
map.add_tile(9, 0, False, False, False, False)

map.add_tile(0, 1, False, False, False, False)
map.add_tile(1, 1, False, False, False, False)
map.add_tile(2, 1, False, False, False, False)
map.add_tile(3, 1, obstacle=True)  # Obstacle
map.add_tile(4, 1, False, False, False, False)
map.add_tile(5, 1, False, False, False, False)
map.add_tile(6, 1, False, False, False, False)
map.add_tile(7, 1, False, False, False, False)
map.add_tile(8, 1, False, False, False, False)
map.add_tile(9, 1, False, False, False, False)

map.add_tile(0, 2, False, False, False, False)
map.add_tile(1, 2, False, False, False, False)
map.add_tile(2, 2, False, False, False, False)
map.add_tile(3, 2, obstacle=True)  # Obstacle
map.add_tile(4, 2, False, False, False, False)
map.add_tile(5, 2, False, False, False, False)
map.add_tile(6, 2, False, False, False, False)
map.add_tile(7, 2, False, False, False, False)
map.add_tile(8, 2, False, False, False, False)
map.add_tile(9, 2, False, False, False, False)

map.add_tile(0, 3, False, False, False, False)
map.add_tile(1, 3, False, False, False, False)
map.add_tile(2, 3, False, False, False, False)
map.add_tile(3, 3, obstacle=True)  # Obstacle
map.add_tile(4, 3, False, False, False, False)
map.add_tile(5, 3, False, False, False, False)
map.add_tile(6, 3, False, False, False, False)
map.add_tile(7, 3, False, False, False, False)
map.add_tile(8, 3, False, False, False, False)
map.add_tile(9, 3, False, False, False, False)

map.add_tile(0, 4, False, False, False, False)
map.add_tile(1, 4, False, False, False, False)
map.add_tile(2, 4, False, False, False, False)
map.add_tile(3, 4, False, False, False, False)
map.add_tile(4, 4, False, False, False, False)
map.add_tile(5, 4, False, False, False, False)
map.add_tile(6, 4, False, False, False, False)
map.add_tile(7, 4, False, False, False, False)
map.add_tile(8, 4, False, False, False, False)
map.add_tile(9, 4, False, False, False, False)

map.add_tile(0, 5, False, False, False, False)
map.add_tile(1, 5, False, False, False, False)
map.add_tile(2, 5, False, False, False, False)
map.add_tile(3, 5, False, False, False, False)
map.add_tile(3, 6, obstacle=True)  # Obstacle
map.add_tile(4, 5, False, False, False, False)
map.add_tile(5, 5, False, False, False, False)
map.add_tile(6, 5, False, False, False, False)
map.add_tile(7, 5, False, False, False, False)
map.add_tile(8, 5, False, False, False, False)
map.add_tile(9, 5, end=True)  # End tile)

map.display_map()


path_ = map.get_shortest_path()
for tile in path_:
    map.print_tile_info(tile)
map.display_map()
