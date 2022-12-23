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
EMERGENCY_STOP_DISTANCE = 10 # cm


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
        self.__orientation = 'N'

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
                    command = self.__remote_receiver.get_command()

                    if command == "Explore":
                        self.__explore()

                    elif command == "Find a human": 
                        # TODO
                        print("Find a human")

                    elif command == "Return to home":
                        # TODO
                        print("Return to home")

                elif self.__remote_receiver.get_mode() == "Manual mode":
                    self.__manual_mode()

       
    #----------------------------------------
    def __explore(self):
        while self.__remote_receiver.is_start_button_pressed():
            # add tiles to map
            self.__update_map()
            #self.__map.display_map()

            # check if front is free
            if not self.__is_facing_obstacle() and self.__sensing_system.is_front_clear():
                self.__move_forward()
                self.__update_position()

            elif not self.__is_obstacle_on_left():
                self.__turn_left()

            elif not self.__is_obstacle_on_right():
                self.__turn_right()

            else:
                self.__turn_left()
                self.__turn_left()


    #
    def __move_forward(self):
        for _ in range(CM * TILE_SIZE):
            if self.__sensing_system.is_front_clear():
                self.__drivetrain.rotate('f')
            else:
                break

    #
    def __turn_left(self):
        self.__drivetrain.turn('l', 90)

        if self.__orientation == 'N':
            self.__orientation = 'W'

        elif self.__orientation == 'W':
            self.__orientation = 'S'

        elif self.__orientation == 'S':
            self.__orientation = 'E'

        elif self.__orientation == 'E':
            self.__orientation = 'N'
    

    #
    def __turn_right(self):
        self.__drivetrain.turn('r', 90)

        if self.__orientation == 'N':
            self.__orientation = 'E'

        elif self.__orientation == 'E':
            self.orientation = 'S'

        elif self.__orientation == 'S':
            self.__orientation = 'W'

        elif self.__orientation == 'W':
            self.__orientation = 'N'
    

    def __update_position(self):
        if self.__orientation == 'N':
            self.__map.cur_y += 1

        elif self.__orientation == 'E':
            self.__map.cur_x += 1

        elif self.__orientation == 'S':
            self.__map.cur_y -= 1

        elif self.__orientation == 'W':
            self.__map.cur_x -= 1
    

    def __is_facing_obstacle(self):
        if self.__orientation == 'N':
            return self.__map.is_obstacle(self.__map.cur_x, self.__map.cur_y + 1) or self.__map.is_obstacle(self.__map.cur_x + 1, self.__map.cur_y + 1) or self.__map.is_obstacle(self.__map.cur_x - 1, self.__map.cur_y + 1)
        
        elif self.__orientation == 'E':
            return self.__map.is_obstacle(self.__map.cur_x + 1, self.__map.cur_y) or self.__map.is_obstacle(self.__map.cur_x + 1, self.__map.cur_y + 1) or self.__map.is_obstacle(self.__map.cur_x + 1, self.__map.cur_y - 1)
        
        elif self.__orientation == 'S':
            return self.__map.is_obstacle(self.__map.cur_x, self.__map.cur_y - 1) or self.__map.is_obstacle(self.__map.cur_x + 1, self.__map.cur_y - 1) or self.__map.is_obstacle(self.__map.cur_x - 1, self.__map.cur_y - 1)
        
        elif self.__orientation == 'W':
            return self.__map.is_obstacle(self.__map.cur_x - 1, self.__map.cur_y) or self.__map.is_obstacle(self.__map.cur_x - 1, self.__map.cur_y + 1) or self.__map.is_obstacle(self.__map.cur_x - 1, self.__map.cur_y - 1)


    def __is_obstacle_on_left(self):
        if self.__orientation == 'N':
            return self.__map.is_obstacle(self.__map.cur_x - 1, self.__map.cur_y)

        elif self.__orientation == 'E':
            return self.__map.is_obstacle(self.__map.cur_x, self.__map.cur_y + 1)

        elif self.__orientation == 'S':
            return self.__map.is_obstacle(self.__map.cur_x + 1, self.__map.cur_y)

        elif self.__orientation == 'W':
            return self.__map.is_obstacle(self.__map.cur_x, self.__map.cur_y - 1)


    def __is_obstacle_on_right(self):
        if self.__orientation == 'N':
            return self.__map.is_obstacle(self.__map.cur_x + 1, self.__map.cur_y)

        elif self.__orientation == 'E':
            return self.__map.is_obstacle(self.__map.cur_x, self.__map.cur_y - 1)

        elif self.__orientation == 'S':
            return self.__map.is_obstacle(self.__map.cur_x - 1, self.__map.cur_y)

        elif self.__orientation == 'W':
            return self.__map.is_obstacle(self.__map.cur_x, self.map.__cur_y + 1)


    def __get_tile_count(self, distance):
        tile_count = math.floor(distance / TILE_SIZE)

        if tile_count > VISION_RANGE:
            return VISION_RANGE, False

        else:
            return tile_count, True

    #
    def __update_map(self):
        if self.__orientation == 'N':
            # adding forward tiles
            distance =  self.__sensing_system.get_front_sensor_distance()
            tile_count, has_obstacle = self.__get_tile_count(distance)

            for i in range(tile_count):
                self.__map.add_tile(self.__map.cur_x, self.__map.cur_y + i + 1, unknown = False)

            if has_obstacle:
                self.__map.add_tile(self.__map.cur_x, self.__map.cur_y +
                              tile_count, unknown=False, obstacle=True)

            # adding left tiles
            distance =  self.__sensing_system.get_left_sensor_distance()
            tile_count, has_obstacle = self.__get_tile_count(distance)

            for i in range(tile_count):
                self.__map.add_tile(self.__map.cur_x - 1,
                                  self.__map.cur_y + i + 1, unknown=False)

            if has_obstacle:
                self.__map.add_tile(self.__map.cur_x - 1, self.__map.cur_y + tile_count,
                              unknown=False, obstacle=True)

            # adding right tiles
            distance =  self.__sensing_system.get_right_sensor_distance()
            tile_count, has_obstacle = self.__get_tile_count(distance)

            for i in range(tile_count):
                self.__map.add_tile(self.__map.cur_x + 1,
                                  self.__map.cur_y + i + 1, unknown=False)

            if has_obstacle:
                self.__map.add_tile(self.__map.cur_x + 1, self.__map.cur_y + tile_count,
                              unknown=False, obstacle=True)

        elif self.__orientation == 'E':
            # adding forward tiles
            distance =  self.__sensing_system.get_front_sensor_distance()
            tile_count, has_obstacle = self.__get_tile_count(distance)

            for i in range(tile_count):
                self.__map.add_tile(self.__map.cur_x + i + 1, self.__map.cur_y, unknown = False)

            if has_obstacle:
                self.__map.add_tile(self.__map.cur_x + tile_count, self.__map.cur_y,
                              unknown=False, obstacle=True)

            # adding left tiles
            distance =  self.__sensing_system.get_left_sensor_distance()
            tile_count, has_obstacle = self.__get_tile_count(distance)

            for i in range(tile_count):
                self.__map.add_tile(self.__map.cur_x + i + 1,
                                  self.__map.cur_y + 1, unknown=False)

            if has_obstacle:
                self.__map.add_tile(self.__map.cur_x + tile_count, self.__map.cur_y + 1,
                              unknown=False, obstacle=True)

            # adding right tiles
            distance =  self.__sensing_system.get_right_sensor_distance()
            tile_count, has_obstacle = self.__get_tile_count(distance)

            for i in range(tile_count):
                self.__map.add_tile(self.__map.cur_x + i + 1,
                                  self.__map.cur_y - 1, unknown=False)

            if has_obstacle:
                self.__map.add_tile(self.__map.cur_x + tile_count, self.__map.cur_y - 1,
                              unknown=False, obstacle=True)

        elif self.__orientation == 'S':
            # adding forward tiles
            distance =  self.__sensing_system.get_front_sensor_distance()
            tile_count, has_obstacle = self.__get_tile_count(distance)

            for i in range(tile_count):
                self.__map.add_tile(self.__map.cur_x, self.__map.cur_y - i - 1, unknown = False)

            if has_obstacle:
                self.__map.add_tile(self.__map.cur_x, self.__map.cur_y -
                              tile_count, unknown=False, obstacle=True)

            # adding left tiles
            distance =  self.__sensing_system.get_left_sensor_distance()
            tile_count, has_obstacle = self.__get_tile_count(distance)

            for i in range(tile_count):
                self.__map.add_tile(self.__map.cur_x + 1,
                                  self.__map.cur_y - i - 1, unknown=False)

            if has_obstacle:
                self.__map.add_tile(self.__map.cur_x + 1, self.__map.cur_y - tile_count,
                              unknown=False, obstacle=True)

            # adding right tiles
            distance =  self.__sensing_system.get_right_sensor_distance()
            tile_count, has_obstacle = self.__get_tile_count(distance)

            for i in range(tile_count):
                self.__map.add_tile(self.__map.cur_x - 1,
                                  self.__map.cur_y - i - 1, unknown=False)

            if has_obstacle:
                self.__map.add_tile(self.__map.cur_x - 1, self.__map.cur_y - tile_count,
                              unknown=False, obstacle=True)

        elif self.__orientation == 'W':
            # adding forward tiles
            distance =  self.__sensing_system.get_front_sensor_distance()
            tile_count, has_obstacle = self.__get_tile_count(distance)

            for i in range(tile_count):
                self.__map.add_tile(self.__map.cur_x - i - 1, self.__map.cur_y, unknown = False)

            if has_obstacle:
                self.__map.add_tile(self.__map.cur_x - tile_count, self.__map.cur_y,
                              unknown=False, obstacle=True)

            # adding left tiles
            distance =  self.__sensing_system.get_left_sensor_distance()
            tile_count, has_obstacle = self.__get_tile_count(distance)

            for i in range(tile_count):
                self.__map.add_tile(self.__map.cur_x - i - 1,
                                  self.__map.cur_y - 1, unknown=False)

            if has_obstacle:
                self.__map.add_tile(self.__map.cur_x - tile_count, self.__map.cur_y - 1,
                              unknown=False, obstacle=True)

            # adding right tiles
            distance =  self.__sensing_system.get_right_sensor_distance()
            tile_count, has_obstacle = self.__get_tile_count(distance)

            for i in range(tile_count):
                self.__map.add_tile(self.__map.cur_x - i - 1,
                                  self.__map.cur_y + 1, unknown=False)

            if has_obstacle:
                self.__map.add_tile(self.__map.cur_x - tile_count, self.__map.cur_y + 1,
                              unknown=False, obstacle=True)


    #----------------------------------------
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


if __name__ == "__main__":
    robot = Robot(imu_auto_calibrate = True, sound_signals = False, debug = True)
    