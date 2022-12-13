import RPi.GPIO as GPIO
from multiprocessing import Process, Value
import time
import math

from drivetrain import Drivetrain
from sensing_system import Sensing_system
from beeper import Beeper
from map_tile import Map


TILE_SIZE = 6 # 6 x 6 cm
CM = 132 # 132 motor steps = 1cm

beeper = Beeper()
drivetrain = Drivetrain()
sensing_system = Sensing_system()


def explore_v1(map):
	while True:
		if sensing_system.get_front_sensor_distance() > 10.0:
			# If 33cm in front is free, 33/5 = 6 tiles of free non-obstacle tiles are added to map (theoretically). - Aistė
			for x in range(math.floor(sensing_system.get_front_sensor_distance() / 5.0)):
				map.add_tile(map.cur_x, map.cur_y + x + 1, unknown = False)
		
		step_count = 0

		while sensing_system.get_front_sensor_distance() >= 10.0 and sensing_system.get_left_sensor_distance() > 5.0 \
			and sensing_system.get_right_sensor_distance() > 5.0:

			drivetrain.rotate('f')
			step_count += 1
		
			if step_count == 5 * CM:
				map.add_tile(map.cur_x, map.cur_y + 1, unknown = False, visited = True)
				step_count = 0

		map.add_tile(map.cur_x, map.cur_y + 1, unknown = False)
		map.add_tile(map.cur_x, map.cur_y + 2, unknown = False, obstacle = True)

		map.display_map()

		if sensing_system.get_left_sensor_distance() > sensing_system.get_right_sensor_distance():
			drivetrain.turn('l', 90)
		else:
			drivetrain.turn('r', 90)
   

class explore_logic:
    def __init__(self, map_object):
        self.map = map_object
        self.orientation = 'N'
        self.step_count = 0
    
    def turn_left(self):
        drivetrain.turn('l', 90)

        if self.orientation == 'N':
            self.orientation = 'W'

        elif self.orientation == 'W':
            self.orientation = 'S'

        elif self.orientation == 'S':
            self.orientation = 'E'

        elif self.orientation == 'E':
            self.orientation = 'N'
    
    def turn_right(self):
        drivetrain.turn('r', 90)

        if self.orientation == 'N':
            self.orientation = 'E'

        elif self.orientation == 'E':
            self.orientation = 'S'

        elif self.orientation == 'S':
            self.orientation = 'W'

        elif self.orientation == 'W':
            self.orientation = 'N'
    
    def move_forward(self):
        for _ in range(CM * TILE_SIZE):
            drivetrain.rotate('f')

    def explore(self):
        # add tiles to map
        self.update_map()
        self.map.display_map()
        # check if front is free
        if self.is_facing_wall() == False:
            pass
        elif self.is_wall_on_left() == False:
            self.turn_left()
        elif self.is_wall_on_right() == False:
            self.turn_right()
        else:
            self.turn_left()
            self.turn_left()

        if self.is_facing_wall() == False:
            self.move_forward()
        
    
    def is_facing_wall(self):
        if self.orientation == 'N':
            return map.get_tile(self.map.cur_x, self.map.cur_y + 1).obstacle
        elif self.orientation == 'E':
            return map.get_tile(self.map.cur_x + 1, self.map.cur_y).obstacle
        elif self.orientation == 'S':
            return map.get_tile(self.map.cur_x, self.map.cur_y - 1).obstacle
        elif self.orientation == 'W':
            return map.get_tile(self.map.cur_x - 1, self.map.cur_y).obstacle
    
    def is_wall_on_left(self):
        if self.orientation == 'N':
            return map.get_tile(self.map.cur_x - 1, self.map.cur_y).obstacle
        elif self.orientation == 'E':
            return map.get_tile(self.map.cur_x, self.map.cur_y + 1).obstacle
        elif self.orientation == 'S':
            return map.get_tile(self.map.cur_x + 1, self.map.cur_y).obstacle
        elif self.orientation == 'W':
            return map.get_tile(self.map.cur_x, self.map.cur_y - 1).obstacle

    def update_map(self):
        if self.orientation == 'N':
            # adding forward tiles
            distance = sensing_system.get_front_sensor_distance()
            tile_count = math.floor(distance / TILE_SIZE)
            for i in range(tile_count):
                self.map.add_tile(self.map.cur_x, self.map.cur_y + i + 1, unknown = False)
            self.map.add_tile(self.map.cur_x, self.map.cur_y +
                              tile_count, unknown=False, obstacle=True)
            # adding left tiles
            distance = sensing_system.get_left_sensor_distance()
            tile_count = math.floor(distance / TILE_SIZE)
            for i in range(tile_count):
                self.map.add_tile(self.map.cur_x - 1,
                                  self.map.cur_y + i + 1, unknown=False)
            self.map.add_tile(self.map.cur_x - 1, self.map.cur_y + tile_count,
                              unknown=False, obstacle=True)
            # adding right tiles
            distance = sensing_system.get_right_sensor_distance()
            tile_count = math.floor(distance / TILE_SIZE)
            for i in range(tile_count):
                self.map.add_tile(self.map.cur_x + 1,
                                  self.map.cur_y + i + 1, unknown=False)
            self.map.add_tile(self.map.cur_x + 1, self.map.cur_y + tile_count,
                              unknown=False, obstacle=True)
        if self.orientation == 'E':
            # adding forward tiles
            distance = sensing_system.get_front_sensor_distance()
            tile_count = math.floor(distance / TILE_SIZE)
            for i in range(tile_count):
                self.map.add_tile(self.map.cur_x + i + 1, self.map.cur_y, unknown = False)
            self.map.add_tile(self.map.cur_x + tile_count, self.map.cur_y,
                              unknown=False, obstacle=True)
            # adding left tiles
            distance = sensing_system.get_left_sensor_distance()
            tile_count = math.floor(distance / TILE_SIZE)
            for i in range(tile_count):
                self.map.add_tile(self.map.cur_x + i + 1,
                                  self.map.cur_y + 1, unknown=False)
            self.map.add_tile(self.map.cur_x + tile_count, self.map.cur_y + 1,
                              unknown=False, obstacle=True)
            # adding right tiles
            distance = sensing_system.get_right_sensor_distance()
            tile_count = math.floor(distance / TILE_SIZE)
            for i in range(tile_count):
                self.map.add_tile(self.map.cur_x + i + 1,
                                  self.map.cur_y - 1, unknown=False)
            self.map.add_tile(self.map.cur_x + tile_count, self.map.cur_y - 1,
                              unknown=False, obstacle=True)
        if self.orientation == 'S':
            # adding forward tiles
            distance = sensing_system.get_front_sensor_distance()
            tile_count = math.floor(distance / TILE_SIZE)
            for i in range(tile_count):
                self.map.add_tile(self.map.cur_x, self.map.cur_y - i - 1, unknown = False)
            self.map.add_tile(self.map.cur_x, self.map.cur_y -
                              tile_count, unknown=False, obstacle=True)
            # adding left tiles
            distance = sensing_system.get_left_sensor_distance()
            tile_count = math.floor(distance / TILE_SIZE)
            for i in range(tile_count):
                self.map.add_tile(self.map.cur_x + 1,
                                  self.map.cur_y - i - 1, unknown=False)
            self.map.add_tile(self.map.cur_x + 1, self.map.cur_y - tile_count,
                              unknown=False, obstacle=True)
            # adding right tiles
            distance = sensing_system.get_right_sensor_distance()
            tile_count = math.floor(distance / TILE_SIZE)
            for i in range(tile_count):
                self.map.add_tile(self.map.cur_x - 1,
                                  self.map.cur_y - i - 1, unknown=False)
            self.map.add_tile(self.map.cur_x - 1, self.map.cur_y - tile_count,
                              unknown=False, obstacle=True)
        if self.orientation == 'W':
            # adding forward tiles
            distance = sensing_system.get_front_sensor_distance()
            tile_count = math.floor(distance / TILE_SIZE)
            for i in range(tile_count):
                self.map.add_tile(self.map.cur_x - i - 1, self.map.cur_y, unknown = False)
            self.map.add_tile(self.map.cur_x - tile_count, self.map.cur_y,
                              unknown=False, obstacle=True)
            # adding left tiles
            distance = sensing_system.get_left_sensor_distance()
            tile_count = math.floor(distance / TILE_SIZE)
            for i in range(tile_count):
                self.map.add_tile(self.map.cur_x - i - 1,
                                  self.map.cur_y - 1, unknown=False)
            self.map.add_tile(self.map.cur_x - tile_count, self.map.cur_y - 1,
                              unknown=False, obstacle=True)
            # adding right tiles
            distance = sensing_system.get_right_sensor_distance()
            tile_count = math.floor(distance / TILE_SIZE)
            for i in range(tile_count):
                self.map.add_tile(self.map.cur_x - i - 1,
                                  self.map.cur_y + 1, unknown=False)
            self.map.add_tile(self.map.cur_x - tile_count, self.map.cur_y + 1,
                              unknown=False, obstacle=True)
            
def explore_v3(map):
    explore_log = explore_logic(map)
    while True:
        explore_log.explore()
    
def explore_v2(map):
	orientation = 'N'

	while True:
		step_count = 0

		while sensing_system.get_front_sensor_distance() >= 2 * TILE_SIZE and sensing_system.get_left_sensor_distance() > TILE_SIZE \
			and sensing_system.get_right_sensor_distance() > TILE_SIZE:

			drivetrain.rotate('f')
			step_count += 1
		
			if step_count == TILE_SIZE * CM:
				if orientation == 'N':
					map.add_tile(map.cur_x, map.cur_y + 1, unknown = False, visited = True)
					map.cur_y += 1

				elif orientation == 'E':
					map.add_tile(map.cur_x + 1, map.cur_y, unknown = False, visited = True)
					map.cur_x += 1

				elif orientation == 'S':
					map.add_tile(map.cur_x, map.cur_y - 1, unknown = False, visited = True)
					map.cur_y -= 1

				elif orientation == 'W':
					map.add_tile(map.cur_x - 1, map.cur_y, unknown = False, visited = True)
					map.cur_x -= 1

				step_count = 0

		map.add_tile(map.cur_x, map.cur_y + 1, unknown = False)
		map.add_tile(map.cur_x, map.cur_y + 2, unknown = False, obstacle = True)

		if sensing_system.get_left_sensor_distance() > sensing_system.get_right_sensor_distance():
			drivetrain.turn('l', 90)

			if orientation == 'N':
				orientation = 'W'

			elif orientation == 'W':
				orientation = 'S'

			elif orientation == 'S':
				orientation = 'E'

			elif orientation == 'E':
				orientation = 'N'

		else:
			drivetrain.turn('r', 90)

			if orientation == 'N':
				orientation = 'E'

			elif orientation == 'E':
				orientation = 'S'

			elif orientation == 'S':
				orientation = 'W'

			elif orientation == 'W':
				orientation = 'N'

		map.display_map()
		print("----------------------------------------------------------------------------------------------------")


if __name__ == "__main__":
	map = Map()

	beeper.beep(3, 0.1)

	Process(target=explore_v3, args=(map,)).start()
	
