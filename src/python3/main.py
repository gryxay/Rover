import RPi.GPIO as GPIO
import time
import threading
import math
from multiprocessing import Process, Value

from motor import Motor
from distance_sensor import Sensor
from beeper import Beeper
from drivetrain import Drivetrain
from map_tile import map as Map


#beeper = Beeper(5)
drivetrain = Drivetrain(20, 16, 26, 19)
front_sensor = Sensor(21, 12)
left_sensor = Sensor(25, 24)
right_sensor = Sensor(17, 4)


def update_sensor_data(front_sensor_last_scan, left_sensor_last_scan, right_sensor_last_scan):
	while True:
		front_sensor_last_scan.value = front_sensor.get_distance()
		left_sensor_last_scan.value = left_sensor.get_distance()
		right_sensor_last_scan.value = right_sensor.get_distance()


def drive(front_sensor_last_scan, left_sensor_last_scan, right_sensor_last_scan, is_moving, map):
	if front_sensor_last_scan > 10.0:
		for x in range(math.floor(front_sensor_last_scan/5.0)):		#if 33cm in front is free, 33/5 = 6 tiles of free non-obstacle tiles are added to map (theoretically)
			map.add_tile(map.cur_x, map.cur_y + x + 1, obstacle = False)
	
	if(front_sensor_last_scan <= 5.0):							# if front last scan <=5 cm - must be osbtacle 
		map.add_tile(map.cur_x, map.cur_y + 1, obstacle = True)
		if left_sensor_last_scan.value > right_sensor_last_scan.value:
			drivetrain.turn('l', 3.15)	# 3.15 ~= 90 degree turn
		else:
			drivetrain.turn('r', 3.15)	# 3.15 ~= 90 degree turn

		while front_sensor_last_scan.value > 10.0 and left_sensor_last_scan.value > 5.0 and right_sensor_last_scan.value > 5.0:
			drivetrain.rotate('f')
			# somehow every 5cm do map.add_tile(map.cur_x, map.cur_y - 1, visited = True) when we know how much robot has moved 

	map.display_map()

	is_moving.value = 0

if __name__ == "__main__":
	front_sensor_last_scan = Value('f', 11.0)
	left_sensor_last_scan = Value('f', 7.0)
	right_sensor_last_scan = Value('f', 7.0)
	is_moving = Value('b', 1)
	map = Map();

	p1 = Process(target=update_sensor_data, args=(front_sensor_last_scan, left_sensor_last_scan, right_sensor_last_scan,))
	p2 = Process(target=drive, args=(front_sensor_last_scan, left_sensor_last_scan, right_sensor_last_scan, is_moving, map))

	p1.start()
	p2.start()
	
	while True:
		if is_moving.value == 0:
			p2 = Process(target=drive, args=(front_sensor_last_scan, left_sensor_last_scan, right_sensor_last_scan, is_moving, map))
			p2.start()

			is_moving.value = 1