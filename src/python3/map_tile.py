class Map_tile:
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
