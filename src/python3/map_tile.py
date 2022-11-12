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
        self.map[key] = map_tile(x, y, unknown, start, visited, obstacle, end)
        return True

    def print_map(self) -> None:
        for x in self.map:
            tile = self.map[x]
            self.print_tile(tile)

    def print_tile(self, tile) -> None:
        print("Position: ", tile.get_position())
        print("is_obstacle: ", tile.is_obstacle)
        print("is_visited: ", tile.is_visited)
        print("is_start: ", tile.is_start)
        print("is_end: ", tile.is_end)
        print()

map = map()
map.add_tile(1, 1)
map.add_tile(1, 1)
map.add_tile(-2, -2 , False, False)
map.print_map()

#[print(x) for x in map.map]