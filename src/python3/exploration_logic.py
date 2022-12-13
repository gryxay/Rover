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


beeper = Beeper()
drivetrain = Drivetrain()
sensing_system = Sensing_system()


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
            if self.can_move_forward():
                drivetrain.rotate('f')

            else:
                #print("Can't move forward!!!!!!")
                break
    

    def can_move_forward(self):
        if sensing_system.get_front_sensor_distance() < 10:
            return False

        return True


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
            self.update_position()
    

    def update_position(self):
        if self.orientation == 'N':
            self.map.cur_y += 1

        elif self.orientation == 'E':
            self.map.cur_x += 1

        elif self.orientation == 'S':
            self.map.cur_y -= 1

        elif self.orientation == 'W':
            self.map.cur_x -= 1
    

    def is_facing_wall(self):
        if self.orientation == 'N':
            return map.get_tile(self.map.cur_x, self.map.cur_y + 1).is_obstacle

        elif self.orientation == 'E':
            return map.get_tile(self.map.cur_x + 1, self.map.cur_y).is_obstacle

        elif self.orientation == 'S':
            return map.get_tile(self.map.cur_x, self.map.cur_y - 1).is_obstacle

        elif self.orientation == 'W':
            return map.get_tile(self.map.cur_x - 1, self.map.cur_y).is_obstacle
    

    def is_wall_on_left(self):
        if self.orientation == 'N':
            return map.get_tile(self.map.cur_x - 1, self.map.cur_y).is_obstacle

        elif self.orientation == 'E':
            return map.get_tile(self.map.cur_x, self.map.cur_y + 1).is_obstacle

        elif self.orientation == 'S':
            return map.get_tile(self.map.cur_x + 1, self.map.cur_y).is_obstacle

        elif self.orientation == 'W':
            return map.get_tile(self.map.cur_x, self.map.cur_y - 1).is_obstacle


    def is_wall_on_right(self):
        if self.orientation == 'N':
            return map.get_tile(self.map.cur_x + 1, self.map.cur_y).is_obstacle

        elif self.orientation == 'E':
            return map.get_tile(self.map.cur_x, self.map.cur_y - 1).is_obstacle

        elif self.orientation == 'S':
            return map.get_tile(self.map.cur_x - 1, self.map.cur_y).is_obstacle

        elif self.orientation == 'W':
            return map.get_tile(self.map.cur_x, self.map.cur_y + 1).is_obstacle


    def get_tile_count(self, distance):
        tile_count = math.floor(distance / TILE_SIZE)

        if tile_count > VISION_RANGE:
            return VISION_RANGE, False

        else:
            return tile_count, True


    def update_map(self):
        if self.orientation == 'N':
            # adding forward tiles
            distance = sensing_system.get_front_sensor_distance()
            tile_count, has_obstacle = self.get_tile_count(distance)

            for i in range(tile_count):
                self.map.add_tile(self.map.cur_x, self.map.cur_y + i + 1, unknown = False)

            if has_obstacle:
                self.map.add_tile(self.map.cur_x, self.map.cur_y +
                              tile_count, unknown=False, obstacle=True)

            # adding left tiles
            distance = sensing_system.get_left_sensor_distance()
            tile_count, has_obstacle = self.get_tile_count(distance)

            for i in range(tile_count):
                self.map.add_tile(self.map.cur_x - 1,
                                  self.map.cur_y + i + 1, unknown=False)

            if has_obstacle:
                self.map.add_tile(self.map.cur_x - 1, self.map.cur_y + tile_count,
                              unknown=False, obstacle=True)

            # adding right tiles
            distance = sensing_system.get_right_sensor_distance()
            tile_count, has_obstacle = self.get_tile_count(distance)

            for i in range(tile_count):
                self.map.add_tile(self.map.cur_x + 1,
                                  self.map.cur_y + i + 1, unknown=False)

            if has_obstacle:
                self.map.add_tile(self.map.cur_x + 1, self.map.cur_y + tile_count,
                              unknown=False, obstacle=True)

        if self.orientation == 'E':
            # adding forward tiles
            distance = sensing_system.get_front_sensor_distance()
            tile_count, has_obstacle = self.get_tile_count(distance)

            for i in range(tile_count):
                self.map.add_tile(self.map.cur_x + i + 1, self.map.cur_y, unknown = False)

            if has_obstacle:
                self.map.add_tile(self.map.cur_x + tile_count, self.map.cur_y,
                              unknown=False, obstacle=True)

            # adding left tiles
            distance = sensing_system.get_left_sensor_distance()
            tile_count, has_obstacle = self.get_tile_count(distance)

            for i in range(tile_count):
                self.map.add_tile(self.map.cur_x + i + 1,
                                  self.map.cur_y + 1, unknown=False)

            if has_obstacle:
                self.map.add_tile(self.map.cur_x + tile_count, self.map.cur_y + 1,
                              unknown=False, obstacle=True)

            # adding right tiles
            distance = sensing_system.get_right_sensor_distance()
            tile_count, has_obstacle = self.get_tile_count(distance)

            for i in range(tile_count):
                self.map.add_tile(self.map.cur_x + i + 1,
                                  self.map.cur_y - 1, unknown=False)

            if has_obstacle:
                self.map.add_tile(self.map.cur_x + tile_count, self.map.cur_y - 1,
                              unknown=False, obstacle=True)

        if self.orientation == 'S':
            # adding forward tiles
            distance = sensing_system.get_front_sensor_distance()
            tile_count, has_obstacle = self.get_tile_count(distance)

            for i in range(tile_count):
                self.map.add_tile(self.map.cur_x, self.map.cur_y - i - 1, unknown = False)

            if has_obstacle:
                self.map.add_tile(self.map.cur_x, self.map.cur_y -
                              tile_count, unknown=False, obstacle=True)

            # adding left tiles
            distance = sensing_system.get_left_sensor_distance()
            tile_count, has_obstacle = self.get_tile_count(distance)

            for i in range(tile_count):
                self.map.add_tile(self.map.cur_x + 1,

                                  self.map.cur_y - i - 1, unknown=False)
            if has_obstacle:
                self.map.add_tile(self.map.cur_x + 1, self.map.cur_y - tile_count,
                              unknown=False, obstacle=True)

            # adding right tiles
            distance = sensing_system.get_right_sensor_distance()
            tile_count, has_obstacle = self.get_tile_count(distance)

            for i in range(tile_count):
                self.map.add_tile(self.map.cur_x - 1,
                                  self.map.cur_y - i - 1, unknown=False)

            if has_obstacle:
                self.map.add_tile(self.map.cur_x - 1, self.map.cur_y - tile_count,
                              unknown=False, obstacle=True)

        if self.orientation == 'W':
            # adding forward tiles
            distance = sensing_system.get_front_sensor_distance()
            tile_count, has_obstacle = self.get_tile_count(distance)

            for i in range(tile_count):
                self.map.add_tile(self.map.cur_x - i - 1, self.map.cur_y, unknown = False)

            if has_obstacle:
                self.map.add_tile(self.map.cur_x - tile_count, self.map.cur_y,
                              unknown=False, obstacle=True)

            # adding left tiles
            distance = sensing_system.get_left_sensor_distance()
            tile_count, has_obstacle = self.get_tile_count(distance)

            for i in range(tile_count):
                self.map.add_tile(self.map.cur_x - i - 1,
                                  self.map.cur_y - 1, unknown=False)

            if has_obstacle:
                self.map.add_tile(self.map.cur_x - tile_count, self.map.cur_y - 1,
                              unknown=False, obstacle=True)

            # adding right tiles
            distance = sensing_system.get_right_sensor_distance()
            tile_count, has_obstacle = self.get_tile_count(distance)

            for i in range(tile_count):
                self.map.add_tile(self.map.cur_x - i - 1,
                                  self.map.cur_y + 1, unknown=False)

            if has_obstacle:
                self.map.add_tile(self.map.cur_x - tile_count, self.map.cur_y + 1,
                              unknown=False, obstacle=True)
            

def explore_v3(map):
    explore_log = explore_logic(map)

    while True:
        explore_log.explore()
    

if __name__ == "__main__":
    map = Map()

    drivetrain.toggle_power(True)
    beeper.beep(3, 0.1)

    Process(target=explore_v3, args=(map,)).start()
	