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
   

def explore_v2(map):
    orientations = ['N', 'E', 'S', 'W']
    orientation = orientations[0]

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
            
            else:
                orientation = orientations[orientations.index(orientation) - 1]

        else:
            drivetrain.turn('r', 90)

            if orientation == 'W':
                orientation = 'N'
            
            else:
                orientation = orientations[orientations.index(orientation) + 1]

        map.display_map()
        print("----------------------------------------------------------------------------------------------------")


if __name__ == "__main__":
    map = Map()

    beeper.beep(3, 0.1)

    Process(target = explore_v2, args = (map,)).start()
