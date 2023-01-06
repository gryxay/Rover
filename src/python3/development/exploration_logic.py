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
VISION_RANGE = 3 # tiles in front of the robot
EMERGENCY_STOP_DISTANCE = 10 # cm


beeper = Beeper()
drivetrain = Drivetrain()
sensing_system = Sensing_system()


class explore_logic:
    def __init__(self, map_object):
        self.map = map_object
        self.orientations = ['N', 'E', 'S', 'W']
        self.orientation = self.orientations[0]
    

    def turn_left(self):
        drivetrain.turn('l', 90)

        if self.orientation == 'N':
            self.orientation = 'W'

        else:
            self.orientation = self.orientations[self.orientations.index(self.orientation) - 1]
    

    def turn_right(self):
        drivetrain.turn('r', 90)

        if self.orientation == 'W':
            self.orientation = 'N'

        else:
            self.orientation = self.orientations[self.orientations.index(self.orientation) + 1]
    

    def move_forward(self):
        for _ in range(CM * TILE_SIZE):
            if self.can_move_forward():
                drivetrain.rotate('f')
            else:
                #print("Can't move forward!!!!!!")
                break
    

    def can_move_forward(self):
        if sensing_system.get_front_sensor_distance() < EMERGENCY_STOP_DISTANCE or \
        sensing_system.get_right_sensor_distance() < EMERGENCY_STOP_DISTANCE or \
        sensing_system.get_left_sensor_distance() < EMERGENCY_STOP_DISTANCE:
            return False

        return True

    def explore_edges(self):
        # add tiles to map
        self.update_map()
        self.map.display_map()

        movements = [('turn_left', self.is_wall_on_left() == False),
                   ('move_forward', self.is_facing_wall() == False),
                   ('turn_right', self.is_wall_on_right() == False),
                   ('turn_right', True),
                   ('turn_right', True)]

        # executes first match
        for movement, condition in movements:
            if condition:
                if movement == 'turn_left':
                    self.turn_left()
                elif movement == 'move_forward':
                    self.move_forward()
                elif movement == 'turn_right':
                    self.turn_right()
                self.update_position()
                break


    def find_wall(self):
        if self.is_facing_wall() == False:
            self.move_forward()
            self.update_position()
            self.update_map()
            self.map.display_map()

            return False
        
        else:
            return True


    def explore(self):
        # add tiles to map
        self.update_map()
        self.map.display_map()

        # check if front has no obstacles
        if self.is_facing_wall() == False:
            pass

        elif self.is_wall_on_left() == False:
            self.turn_left()

        elif self.is_wall_on_right() == False:
            self.turn_right()

        else:
            for _ in range(2):
                self.turn_left()

        if self.is_facing_wall() == False:
            self.move_forward()
            self.update_position()
    

    def update_position(self):
        movements = {'N': (0, 1), 'E': (1, 0), 'S': (0, -1), 'W': (-1, 0)}
        self.map.cur_x += movements[self.orientation][0]
        self.map.cur_y += movements[self.orientation][1]
    

    def is_facing_wall(self):
        movements = {'N': [(0, 1), (1, 1), (-1, 1)],
                 'E': [(1, 0), (1, 1), (1, -1)],
                 'S': [(0, -1), (1, -1), (-1, -1)],
                 'W': [(-1, 0), (-1, 1), (-1, -1)]}
                 
        for x, y in movements[self.orientation]:
            if map.get_tile(self.map.cur_x + x, self.map.cur_y + y).is_obstacle:
                return True
        return False

    def is_wall_on_left(self):
        movements = {'N': (-1, 0), 'E': (0, 1), 'S': (1, 0), 'W': (0, -1)}
        x, y = movements[self.orientation]
        return map.get_tile(self.map.cur_x + x, self.map.cur_y + y).is_obstacle


    def is_wall_on_right(self):
        movements = {'N': (1, 0), 'E': (0, -1), 'S': (-1, 0), 'W': (0, 1)}
        x, y = movements[self.orientation]
        return map.get_tile(self.map.cur_x + x, self.map.cur_y + y).is_obstacle


    def get_tile_count(self, distance):
        tile_count = math.floor(distance / TILE_SIZE)

        if tile_count > VISION_RANGE:
            return VISION_RANGE, False

        else:
            return tile_count, True


    def update_map(self):
        if self.orientation == 'N':
            directions = [('N', sensing_system.get_front_sensor_distance()),
                        ('W', sensing_system.get_left_sensor_distance()),
                        ('E', sensing_system.get_right_sensor_distance())]
        elif self.orientation == 'E':
            directions = [('E', sensing_system.get_front_sensor_distance()),
                        ('S', sensing_system.get_left_sensor_distance()),
                        ('N', sensing_system.get_right_sensor_distance())]
        elif self.orientation == 'S':
            directions = [('S', sensing_system.get_front_sensor_distance()),
                        ('E', sensing_system.get_left_sensor_distance()),
                        ('W', sensing_system.get_right_sensor_distance())]
        elif self.orientation == 'W':
            directions = [('S', sensing_system.get_front_sensor_distance()),
                        ('N', sensing_system.get_left_sensor_distance()),
                        ('S', sensing_system.get_right_sensor_distance())]

        tile_counts = self.get_tile_count(directions)

        for direction, (tile_count, has_obstacle) in zip(directions, tile_counts):
            if direction == 'N':
                offset_x, offset_y = 0, 1
            elif direction == 'E':
                offset_x, offset_y = 1, 0
            elif direction == 'S':
                offset_x, offset_y = 0, -1
            elif direction == 'W':
                offset_x, offset_y = -1, 0

            for i in range(tile_count):
                self.map.add_tile(self.map.cur_x + offset_x, self.map.cur_y + offset_y, unknown=False)
                offset_x += 1

            if has_obstacle:
                self.map.add_tile(self.map.cur_x + offset_x, self.map.cur_y + offset_y, unknown=False, obstacle=True)

            
def explore_v3(map):
    explore_log = explore_logic(map)

    while True:
        explore_log.explore()


def explore_v4(map):
    explore_log = explore_logic(map)
    found = False

    while not found:
        found = explore_log.find_wall()

    while True:
        explore_log.explore_edges()

    
if __name__ == "__main__":
    map = Map()

    drivetrain.toggle_power(True)
    beeper.beep(3, 0.1)

    Process(target=explore_v3, args=(map,)).start()