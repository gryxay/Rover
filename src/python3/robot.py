from drivetrain import Drivetrain
from sensing_system import Sensing_system
from remote_receiver import IR_Receiver
from beeper import Beeper
from map import Map
from time import sleep
import math


TILE_SIZE = 6 # 6 x 6 cm
CM = 132 # 132 motor steps = 1cm
VISION_RANGE = 3 # tiles in front of the robot


# In development
class Robot():
    def __init__(self, imu_auto_calibrate = True, sound_signals = True, debug = False):
        self.__sound_signals = sound_signals
        self.__debug = debug

        self.__drivetrain = Drivetrain(imu_auto_calibrate = imu_auto_calibrate, debug = debug)
        self.__sensing_system = Sensing_system()
        self.__remote_receiver = IR_Receiver(sound_signals = sound_signals, debug = debug)
        self.__beeper = Beeper()

        self.__map = Map()

        if sound_signals:
            self.__beeper.beep(3, 0.1)

        self.__drivetrain.toggle_power(True)

        # Listen to remote for commands
        self.__listen_to_remote()


    def __listen_to_remote(self):
        if self.__debug:
            print("Robot: Listening to remote")

        while True:
            if self.__remote_receiver.is_start_button_pressed():
                if self.__remote_receiver.get_mode() == "Autonomous mode":
                    self.__autonomous_mode()

                elif self.__remote_receiver.get_mode() == "Manual mode":
                    self.__manual_mode()
    

    def __autonomous_mode(self):
        while self.__remote_receiver.is_start_button_pressed() and self.__remote_receiver.get_mode() == "Autonomous mode":
            command = self.__remote_receiver.get_command()

            if command == "Explore":
                if self.__debug:
                    print("Task \"Explore\" is being executed")

                self.__explore()

            elif command == "Find a bottle": 
                if self.__debug:
                    print("Task \"Find a bottle\" is being executed")

                self.__find_object("bottle")

            elif command == "Return to home":
                if self.__debug:
                    print("Task \"Return to home\" is being executed")

                self.__return_to_home()


    def __manual_mode(self):
        while self.__remote_receiver.is_start_button_pressed() and self.__remote_receiver.get_mode() == "Manual mode":
            if self.__remote_receiver.get_last_key_press() == "Forward":
                while self.__sensing_system.is_front_clear() and self.__remote_receiver.get_last_key_press() == "Forward":
                    self.__drivetrain.rotate('f')

                self.__remote_receiver.reset_last_key_press()

            elif self.__remote_receiver.get_last_key_press() == "Backward":
                while self.__sensing_system.is_back_clear() and self.__remote_receiver.get_last_key_press() == "Backward":
                    self.__drivetrain.rotate('b')

                self.__remote_receiver.reset_last_key_press()

            elif self.__remote_receiver.get_last_key_press() == "Left":
                self.__turn_left()
                self.__remote_receiver.reset_last_key_press()

            elif self.__remote_receiver.get_last_key_press() == "Right":
                self.__turn_right()
                self.__remote_receiver.reset_last_key_press()

       
    def __explore(self):
        while self.__remote_receiver.is_start_button_pressed():
            # add tiles to map
            self.__update_map()

            # check if front is free
            if not self.__is_facing_obstacle() and self.__sensing_system.is_front_clear():
                self.__move_forward()
                self.__map.update_position()

            elif not self.__is_obstacle_on_left():
                self.__turn_left()

            elif not self.__is_obstacle_on_right():
                self.__turn_right()

            else:
                self.__turn_left()
                self.__turn_left()

        self.__map.display_map()


    def __find_object(self, object):
        print("Not implemented yet!")


    def __return_to_home(self):
        print("Not implemented yet!")


    def __move_forward(self):
        for _ in range(CM * TILE_SIZE):
            if self.__sensing_system.is_front_clear():
                self.__drivetrain.rotate('f')
            else:
                break

    
    def __turn(self, direction):
        self.__drivetrain.turn(direction, 90)
        self.__map.update_orientation(direction)
    
    # move to Map() class
    def __is_facing_obstacle(self):
        current_orientation = self.__map.get_current_orientation()
        current_x_position = self.__map.get_current_x_position()
        current_y_position = self.__map.get_current_y_position()

        if current_orientation == 'N':
            return self.__map.is_obstacle(current_x_position, current_y_position + 1) or \
                   self.__map.is_obstacle(current_x_position + 1, current_y_position + 1) or \
                   self.__map.is_obstacle(current_x_position - 1, current_y_position + 1)
        
        elif current_orientation == 'E':
            return self.__map.is_obstacle(current_x_position + 1, current_y_position) or \
                   self.__map.is_obstacle(current_x_position + 1, current_y_position + 1) or \
                   self.__map.is_obstacle(current_x_position + 1, current_y_position - 1)
        
        elif current_orientation == 'S':
            return self.__map.is_obstacle(current_x_position, current_y_position - 1) or \
                   self.__map.is_obstacle(current_x_position + 1, current_y_position - 1) or \
                   self.__map.is_obstacle(current_x_position - 1, current_y_position - 1)
        
        elif current_orientation == 'W':
            return self.__map.is_obstacle(current_x_position - 1, current_y_position) or \
                   self.__map.is_obstacle(current_x_position - 1, current_y_position + 1) or \
                   self.__map.is_obstacle(current_x_position - 1, current_y_position - 1)

    # move to Map() class
    def __is_obstacle_on_left(self):
        current_orientation = self.__map.get_current_orientation()
        current_x_position = self.__map.get_current_x_position()
        current_y_position = self.__map.get_current_y_position()

        if current_orientation == 'N':
            return self.__map.is_obstacle(current_x_position - 1, current_y_position)

        elif current_orientation == 'E':
            return self.__map.is_obstacle(current_x_position, current_y_position + 1)

        elif current_orientation == 'S':
            return self.__map.is_obstacle(current_x_position + 1, current_y_position)

        elif current_orientation == 'W':
            return self.__map.is_obstacle(current_x_position, current_y_position - 1)

    # move to Map() class
    def __is_obstacle_on_right(self):
        current_orientation = self.__map.get_current_orientation()
        current_x_position = self.__map.get_current_x_position()
        current_y_position = self.__map.get_current_y_position()

        if current_orientation == 'N':
            return self.__map.is_obstacle(current_x_position + 1, current_y_position)

        elif current_orientation == 'E':
            return self.__map.is_obstacle(current_x_position, current_y_position - 1)

        elif current_orientation == 'S':
            return self.__map.is_obstacle(current_x_position - 1, current_y_position)

        elif current_orientation == 'W':
            return self.__map.is_obstacle(current_x_position, current_y_position + 1)


    def __get_tile_count(self, distance):
        tile_count = math.floor(distance / TILE_SIZE)

        if tile_count > VISION_RANGE:
            return VISION_RANGE, False

        else:
            return tile_count, True

    
    def __update_map(self):
        current_orientation = self.__map.get_current_orientation()
        current_x_position = self.__map.get_current_x_position()
        current_y_position = self.__map.get_current_y_position()

        if current_orientation == 'N':
            # adding forward tiles
            distance = self.__sensing_system.get_front_sensor_distance()
            tile_count, has_obstacle = self.__get_tile_count(distance)

            for i in range(tile_count):
                if not self.__map.get_tile(current_x_position, current_y_position + i + 1):
                    self.__map.add_tile(current_x_position, current_y_position + i + 1, is_known = True)

            if has_obstacle:
                self.__map.add_tile(current_x_position, current_y_position + tile_count, is_known = True, is_obstacle = True)

            # adding left tiles
            distance =  self.__sensing_system.get_left_sensor_distance()
            tile_count, has_obstacle = self.__get_tile_count(distance)

            for i in range(tile_count):
                if not self.__map.get_tile(current_x_position - 1, current_y_position + i + 1):
                    self.__map.add_tile(current_x_position - 1, current_y_position + i + 1, is_known = True)

            if has_obstacle:
                self.__map.add_tile(current_x_position - 1, current_y_position + tile_count, is_known = True, is_obstacle = True)

            # adding right tiles
            distance =  self.__sensing_system.get_right_sensor_distance()
            tile_count, has_obstacle = self.__get_tile_count(distance)

            for i in range(tile_count):
                if not self.__map.get_tile(current_x_position + 1, current_y_position + i + 1):
                    self.__map.add_tile(current_x_position + 1, current_y_position + i + 1, is_known = True)

            if has_obstacle:
                self.__map.add_tile(current_x_position + 1, current_y_position + tile_count, is_known = True, is_obstacle = True)

        elif current_orientation == 'E':
            # adding forward tiles
            distance =  self.__sensing_system.get_front_sensor_distance()
            tile_count, has_obstacle = self.__get_tile_count(distance)

            for i in range(tile_count):
                if not self.__map.get_tile(current_x_position + i + 1, current_y_position):
                    self.__map.add_tile(current_x_position + i + 1, current_y_position, is_known = True)

            if has_obstacle:
                self.__map.add_tile(current_x_position + tile_count, current_y_position, is_known = True, is_obstacle = True)

            # adding left tiles
            distance =  self.__sensing_system.get_left_sensor_distance()
            tile_count, has_obstacle = self.__get_tile_count(distance)

            for i in range(tile_count):
                if not self.__map.get_tile(current_x_position + i + 1, current_y_position + 1):
                    self.__map.add_tile(current_x_position + i + 1, current_y_position + 1, is_known = True)

            if has_obstacle:
                self.__map.add_tile(current_x_position + tile_count, current_y_position + 1, is_known = True, is_obstacle = True)

            # adding right tiles
            distance =  self.__sensing_system.get_right_sensor_distance()
            tile_count, has_obstacle = self.__get_tile_count(distance)

            for i in range(tile_count):
                if not self.__map.get_tile(current_x_position + i + 1, current_y_position - 1):
                    self.__map.add_tile(current_x_position + i + 1, current_y_position - 1, is_known = True)

            if has_obstacle:
                self.__map.add_tile(current_x_position + tile_count, current_y_position - 1, is_known = True, is_obstacle = True)

        elif current_orientation == 'S':
            # adding forward tiles
            distance =  self.__sensing_system.get_front_sensor_distance()
            tile_count, has_obstacle = self.__get_tile_count(distance)

            for i in range(tile_count):
                if not self.__map.get_tile(current_x_position, current_y_position - i - 1):
                    self.__map.add_tile(current_x_position, current_y_position - i - 1, is_known = True)

            if has_obstacle:
                self.__map.add_tile(current_x_position, current_y_position - tile_count, is_known = True, is_obstacle = True)

            # adding left tiles
            distance =  self.__sensing_system.get_left_sensor_distance()
            tile_count, has_obstacle = self.__get_tile_count(distance)

            for i in range(tile_count):
                if not self.__map.get_tile(current_x_position + 1, current_y_position - i - 1):
                    self.__map.add_tile(current_x_position + 1, current_y_position - i - 1, is_known = True)

            if has_obstacle:
                self.__map.add_tile(current_x_position + 1, current_y_position - tile_count, is_known = True, is_obstacle = True)

            # adding right tiles
            distance =  self.__sensing_system.get_right_sensor_distance()
            tile_count, has_obstacle = self.__get_tile_count(distance)

            for i in range(tile_count):
                if not self.__map.get_tile(current_x_position - 1, current_y_position - i - 1):
                    self.__map.add_tile(current_x_position - 1, current_y_position - i - 1, is_known = True)

            if has_obstacle:
                self.__map.add_tile(current_x_position - 1, current_y_position - tile_count, is_known = True, is_obstacle = True)

        elif current_orientation == 'W':
            # adding forward tiles
            distance =  self.__sensing_system.get_front_sensor_distance()
            tile_count, has_obstacle = self.__get_tile_count(distance)

            for i in range(tile_count):
                if not self.__map.get_tile(current_x_position - i - 1, current_y_position):
                    self.__map.add_tile(current_x_position - i - 1, current_y_position, is_known = True)

            if has_obstacle:
                self.__map.add_tile(current_x_position - tile_count, current_y_position, is_known = True, is_obstacle = True)

            # adding left tiles
            distance =  self.__sensing_system.get_left_sensor_distance()
            tile_count, has_obstacle = self.__get_tile_count(distance)

            for i in range(tile_count):
                if not self.__map.get_tile(current_x_position - i - 1, current_y_position - 1):
                    self.__map.add_tile(current_x_position - i - 1, current_y_position - 1, is_known = True)

            if has_obstacle:
                self.__map.add_tile(current_x_position - tile_count, current_y_position - 1, is_known = True, is_obstacle = True)

            # adding right tiles
            distance =  self.__sensing_system.get_right_sensor_distance()
            tile_count, has_obstacle = self.__get_tile_count(distance)

            for i in range(tile_count):
                if not self.__map.get_tile(current_x_position - i - 1, current_y_position + 1):
                    self.__map.add_tile(current_x_position - i - 1, current_y_position + 1, is_known = True)

            if has_obstacle:
                self.__map.add_tile(current_x_position - tile_count, current_y_position + 1, is_known = True, is_obstacle = True)


if __name__ == "__main__":
    robot = Robot(imu_auto_calibrate = False, sound_signals = False, debug = True)
    