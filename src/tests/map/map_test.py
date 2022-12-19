from map import Map


if __name__ == "__main__":
    map = Map()

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