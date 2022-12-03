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


#beeper = Beeper(5)
drivetrain = Drivetrain()
sensing_system = Sensing_system()


def update_sensor_data(sensor_data):
	while True:
		sensor_data["front"].value = sensing_system.get_front_sensor_distance()
		sensor_data["rear"].value = sensing_system.get_rear_sensor_distance()
		sensor_data["left"].value = sensing_system.get_left_sensor_distance()
		sensor_data["right"].value = sensing_system.get_right_sensor_distance()


def drive(sensor_data, is_moving, map):
	if sensor_data["front"].value > 10.0:
		# If 33cm in front is free, 33/5 = 6 tiles of free non-obstacle tiles are added to map (theoretically). - Aistė
		for x in range(math.floor(sensor_data["front"].value/5.0)):
			map.add_tile(map.cur_x, map.cur_y + x + 1, unknown = False)
	
	step_count = 0

	while sensor_data["front"].value >= 10.0 and sensor_data["left"].value > 5.0 and sensor_data["right"].value > 5.0:
		drivetrain.rotate('f')
		step_count += 1
	
		if step_count == 5 * CM:
			map.add_tile(map.cur_x, map.cur_y + 1, unknown = False, visited = True)
			step_count = 0

	map.add_tile(map.cur_x, map.cur_y + 1, unknown = False)
	map.add_tile(map.cur_x, map.cur_y + 2, unknown = False, obstacle = True)

	map.display_map()

	if sensor_data["left"].value > sensor_data["right"].value:
		drivetrain.turn('l', 3.15)	# 3.15 ~= 90 degree turn
	else:
		drivetrain.turn('r', 3.15)	# 3.15 ~= 90 degree turn

	is_moving.value = 0


if __name__ == "__main__":
	sensor_data = {
		"front": Value('f', sensing_system.get_front_sensor_distance()),
		"rear": Value('f', sensing_system.get_rear_sensor_distance()),
		"left": Value('f', sensing_system.get_left_sensor_distance()),
		"right": Value('f', sensing_system.get_right_sensor_distance())
	}
	is_moving = Value('b', 1)
	map = Map()

	drivetrain.toggle_power(True)

	Process(target=update_sensor_data, args=(sensor_data,)).start()
	Process(target=drive, args=(sensor_data, is_moving, map,)).start()
	
	while True:
		if is_moving.value == 0:
			Process(target=drive, args=(sensor_data, is_moving, map,)).start()
			is_moving.value = 1
