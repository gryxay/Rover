class map_tile:
    def __init__(self, x, y, unknown=True, start=False, visited=False, obstacle=False, end=False) -> None:
        self.x = x
        self.y = y
        self.unknown = unknown
        self.is_obstacle = obstacle
        self.is_visited = visited
        self.is_start = start
        self.is_end = end

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
        self.map[str(self.cur_x) + str(self.cur_y)] = map_tile(self.cur_x, self.cur_y, unknown=False, start=True, visited=True)
    
    def get_current_tile(self) -> map_tile:
        return self.map[str(self.cur_x) + str(self.cur_y)]
    
    def get_tile(self, x, y) -> map_tile:
        return self.map[str(x) + str(y)]

    def add_tile(self, x, y, unknown=True, start=False, visited=False, obstacle=False, end=False) -> bool:
        key = str(x) + str(y)
        if key in self.map:
            return False
        self.__update_bounds(x, y)
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
                else:
                    print("0", end="")
        else:
            print(" ", end="")

    def print_tile_info(self, tile) -> None:
        print("Position: ", tile.get_position())
        print("is_obstacle: ", tile.is_obstacle)
        print("is_visited: ", tile.is_visited)
        print("is_start: ", tile.is_start)
        print("is_end: ", tile.is_end)
        print()

class path:
    def __init__(self, map) -> None:
        self.map = map
        self.path = []
        self.cur_x = 0
        self.cur_y = 0
        self.length = 0
        self.visited_positions = {}
    
    def add_step(self, direction) -> None:
        self.path.append(direction)
        self.length += 1
        self.visited_positions[str(self.cur_x) + str(self.cur_y)] = True
        if direction == "N":
            self.cur_y += 1
        elif direction == "S":
            self.cur_y -= 1
        elif direction == "E":
            self.cur_x += 1
        elif direction == "W":
            self.cur_x -= 1
    
    def get_viable_neighbours(self) -> list:
        neighbours = []
        if self.__is_viable_position(self.cur_x, self.cur_y + 1):
            neighbours.append([self.cur_x, self.cur_y + 1])
        if self.__is_viable_position(self.cur_x, self.cur_y - 1):
            neighbours.append([self.cur_x, self.cur_y - 1])
        if self.__is_viable_position(self.cur_x + 1, self.cur_y):
            neighbours.append([self.cur_x + 1, self.cur_y])
        if self.__is_viable_position(self.cur_x - 1, self.cur_y):
            neighbours.append([self.cur_x - 1, self.cur_y])
        return neighbours
        
    def __is_viable_position(self, x, y) -> bool:
        if str(x) + str(y) in self.visited_positions:
            return False
        if str(x) + str(y) in self.map:
            return not self.map[str(x) + str(y)].is_obstacle
        return True


map = map()
map.add_tile(1, 1, end = True)
map.add_tile(0, 1, visited=True, unknown=False)
map.add_tile(-2, -2 , False, False, obstacle=True)
# Add more tiles here
map.print_map_info()
map.display_map()
