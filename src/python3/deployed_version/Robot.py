from Drivetrain import Drivetrain
from Sensing_System import Sensing_System
from IR_Receiver import IR_Receiver
from Buzzer import Buzzer
from Map import Map

from Constants import Robot_Constants
from Constants import Drivetrain_Constants
from Constants import Map_Constants


# In development
class Robot():
    __drivetrain = None
    __sensing_system = Sensing_System()
    __remote_receiver = None
    __buzzer = Buzzer()
    __map = Map()

    __sound_signals = None
    __debug = None

    def __init__(self, imu_auto_calibrate = True, sound_signals = True, debug = False):
        '''
        self.__sound_signals = sound_signals
        self.__debug = debug

        self.__drivetrain = Drivetrain(imu_auto_calibrate = imu_auto_calibrate, debug = self.__debug)
        self.__remote_receiver = IR_Recebuzzer = sebuzzer, sound_signals = self.__sound_signals, debug = self.__debug)

        if sound_signals:
            sebuzzer.beep(3, 0.1)

        # Listen to remote for commands
        self.__listen_to_remote()
        '''
        self.__map.add_tile(3, 0, is_obstacle = True)
        self.__map.add_tile(-5, 0, is_obstacle = True)
        self.__map.add_tile(0, 6, times_visited = 1)
        self.__map.add_tile(-6, 0, times_visited = 1)
        self.__map.add_tile(0, -4, times_visited = 1)

        print(self.__get_least_visited_sides(self.__get_clear_sides()))


    def __listen_to_remote(self):
        if self.__debug:
            print("Robot: Listening to remote")

        while True:
            if self.__remote_receiver.is_start_button_pressed():
                if self.__remote_receiver.get_mode() == "Autonomous mode":
                    self.__autonomous_mode()

                elif self.__remote_receiver.get_mode() == "Manual mode":
                    self.__manual_mode()
    
    #
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
        self.__drivetrain.toggle_power(True)

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
                self.__turn('l')
                self.__remote_receiver.reset_last_key_press()

            elif self.__remote_receiver.get_last_key_press() == "Right":
                self.__turn('r')
                self.__remote_receiver.reset_last_key_press()

        self.__drivetrain.toggle_power(False)

    #
    def __explore(self):
        self.__drivetrain.toggle_power(True)

        while self.__remote_receiver.is_start_button_pressed():
            # add tiles to map
            self.__map.update_map(self.__sensing_system.get_sensor_data())

            # check if front is free
            if not self.__map.check_for_obstacles('f') and self.__sensing_system.is_front_clear():
                self.__move_forward()
                self.__map.update_position()

            elif not self.__map.check_for_obstacles('l'):
                self.__turn('l')

            elif not self.__map.check_for_obstacles('r'):
                self.__turn('r')

            else:
                self.__turn('l')
                self.__turn('l')

        self.__drivetrain.toggle_power(False)
        self.__map.display_map()

    #
    def __find_object(self, object):
        print("Not implemented yet!")

    #
    def __return_to_home(self):
        print("Not implemented yet!")

    #
    def __move_forward(self):
        for _ in range(Drivetrain_Constants.CM * Map_Constants.TILE_SIZE):
            if self.__sensing_system.is_front_clear():
                self.__drivetrain.rotate('f')

            else:
                break

    
    def __turn(self, direction):
        self.__drivetrain.strict_turn(direction)
        self.__map.update_orientation(direction)


    # Todo
    def __get_action(self):
        current_tile_times_visited = self.__map.get_current_tile.get_times_visited()
        possible_directions = self.__get_least_visited_sides(self.__get_clear_sides)

        if len(possible_directions) >= 0:
            print("TODO")

        else:
            return None


    def __get_clear_sides(self):
        clear_sides = []

        for direction in Robot_Constants.DIRECTIONS:
            contains_obstacles = self.__map.check_for_obstacles(direction)

            if not contains_obstacles:
                clear_sides.append(direction)

        return clear_sides


    def __get_least_visited_sides(self, directions):
        side_data = {}

        for direction in directions:
            side_data[direction] = self.__map.check_visited_tiles(direction)

        min_times_visited = min(side_data.values())
        least_visited_sides = []

        for direction, times_visited in side_data.items():
            if times_visited == min_times_visited:
                least_visited_sides.append(direction)

        return least_visited_sides


if __name__ == "__main__":
    robot = Robot(imu_auto_calibrate = False, sound_signals = True, debug = True)
    