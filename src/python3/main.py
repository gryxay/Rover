import RPi.GPIO as GPIO
from multiprocessing import Process, Value
import threading
import time
import math

from drivetrain import Drivetrain
from sensing_system import Sensing_system
from beeper import Beeper

from map_tile import Map


CM = 132 # 132 motor steps = 1cm


beeper = Beeper()
drivetrain = Drivetrain()
sensing_system = Sensing_system()


def explore(is_moving, map):
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

	is_moving.value = 0


if __name__ == "__main__":
	is_moving = Value('b', 1)
	map = Map()

	beeper.beep(3, 0.1)

	drivetrain.toggle_power(True)

	Process(target = explore, args = (is_moving, map,)).start()
	
	while True:
		if is_moving.value == 0:
			Process(target = explore, args = (is_moving, map,)).start()
			is_moving.value = 1
