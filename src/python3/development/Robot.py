import random

from Drivetrain import Drivetrain
from IMU import IMU
from Computer_Vision import Computer_Vision
from Sensing_System import Sensing_System
from IR_Receiver import IR_Receiver
from Buzzer import Buzzer
from Map import Map

from Constants import Robot_Constants
from Constants import Drivetrain_Constants
from Constants import Map_Constants


# In development
class Robot():
    def __init__(self, imu_auto_calibrate = True, sound_signals = True, debug = False):
        self.__sound_signals = sound_signals
        self.__debug = debug

        self.__buzzer = Buzzer()

        if sound_signals:
            self.__buzzer.sound_signal("Loading")

        self.__remote_receiver = IR_Receiver(buzzer = self.__buzzer, sound_signals = self.__sound_signals, debug = self.__debug)
        self.__imu = IMU(buzzer = self.__buzzer, auto_calibrate = imu_auto_calibrate, debug = self.__debug)
        self.__drivetrain = Drivetrain(imu = self.__imu, debug = self.__debug)
        #self.__computer_vision = Computer_Vision()
        self.__sensing_system = Sensing_System()
        self.__map = Map()

        if sound_signals:
            self.__buzzer.sound_signal("Initialised")

        # Listen to remote for commands
        self.__listen_to_remote()


    # Listens to the remote controller key presses
    def __listen_to_remote(self):
        if self.__debug:
            print("Robot: Listening to remote")


        while True:
            if self.__remote_receiver.is_start_button_pressed():
                if self.__remote_receiver.get_mode() == "Autonomous mode":
                    self.__autonomous_mode()

                elif self.__remote_receiver.get_mode() == "Manual mode":
                    self.__remote_receiver.reset_last_key_press()
                    self.__manual_mode()

            elif self.__remote_receiver.get_last_key_press() == "Clear the map":
                self.__map.reset()

                self.__remote_receiver.reset_last_key_press()

                if self.__debug:
                    print("The map was cleared")
    
    
    # Lets the user give commands to the robot
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

            elif command == "Play a song":
                if self.__debug:
                    print("Task \"Play a song\" is being executed")

                self.__buzzer.play_song("He's a Pirate")


    # Lets the user control movement of the robot using the remote controller
    def __manual_mode(self):
        self.__drivetrain.toggle_power(True)

        while self.__remote_receiver.is_start_button_pressed() and self.__remote_receiver.get_mode() == "Manual mode":
            if self.__remote_receiver.get_last_key_press() == "Forward":
                while self.__sensing_system.is_front_clear() and self.__remote_receiver.get_last_key_press() == "Forward":
                    status = self.__drive('f', "fast")

                    self.__map.update_map(self.__sensing_system.get_sensor_data())
                
                    if not status:
                        self.__remote_receiver.reset_last_key_press()

            elif self.__remote_receiver.get_last_key_press() == "Backward":
                while self.__sensing_system.is_back_clear() and self.__remote_receiver.get_last_key_press() == "Backward":
                    status = self.__drive('b', "fast")

                    self.__map.update_map(self.__sensing_system.get_sensor_data())

                    if not status:
                        self.__remote_receiver.reset_last_key_press()

            elif self.__remote_receiver.get_last_key_press() == "Left":
                self.__turn('l')
                self.__remote_receiver.reset_last_key_press()

            elif self.__remote_receiver.get_last_key_press() == "Right":
                self.__turn('r')
                self.__remote_receiver.reset_last_key_press()

            elif self.__remote_receiver.get_last_key_press() == "Left micro turn":
                self.__drivetrain.micro_turn('l')
                self.__remote_receiver.reset_last_key_press()

            elif self.__remote_receiver.get_last_key_press() == "Right micro turn":
                self.__drivetrain.micro_turn('r')
                self.__remote_receiver.reset_last_key_press()

        self.__map.display_map()
        self.__drivetrain.toggle_power(False)


    # The robot drives around and explores the room
    # Needs to be fixed
    def __explore(self):
        last_action = None

        if self.__sound_signals:
            self.__buzzer.play_song("Explore")

        self.__drivetrain.toggle_power(True)

        while self.__remote_receiver.is_start_button_pressed():
            self.__map.update_map(self.__sensing_system.get_sensor_data())

            action = self.__get_action(last_action)
            last_action = action

            if action == 'f' or action == 'b':
                self.__drive(action, "fast")

            elif action == 'l' or action == 'r':
                self.__turn(action)

            elif action is None:
                if self.__check_if_stuck():
                    break

        self.__drivetrain.toggle_power(False)

        if self.__debug:
            self.__map.display_map()


    # The robot drives around and explores the room until it finds an object it was searching for
    # Needs to be fixed
    def __find_object(self, object):
        last_action = None

        if self.__sound_signals:
            self.__buzzer.play_song("Explore")

        self.__drivetrain.toggle_power(True)

        while self.__remote_receiver.is_start_button_pressed() and self.__computer_vision.get_last_detected_object() != object:
            self.__map.update_map(self.__sensing_system.get_sensor_data())

            action = self.__get_action(last_action)
            last_action = action

            if action == 'f' or action == 'b':
                self.__drive(action, "fast")

            elif action == 'l' or action == 'r':
                self.__turn(action)

            elif action is None:
                if self.__check_if_stuck():
                    break


        self.__drivetrain.toggle_power(False)
        self.__computer_vision.reset_last_detected_object()
        self.__map.set_last_object_location()

        if self.__sound_signals:
            self.__buzzer.play_song("Found it!")


        if self.__debug:
            self.__map.display_map()


    # TODO
    def __return_to_home(self):
        print("Not implemented yet!")


    # If the robot doesn't fully pass the tile, it will move to the previous one 
    def __reposition_on_tile(self, previous_direction, motor_steps):
        direction = None
        delay = self.__drivetrain.get_delay("slow")
        
        if previous_direction == 'f':
            direction = 'b'

        elif previous_direction == 'b':
            direction = 'f'

        self.__drivetrain.set_direction(direction)

        for _ in range(motor_steps):
            self.__drivetrain.rotate_one_step(delay)


    # Moves one tile in a specified direction and speed
    def __drive(self, direction, speed) -> bool:
        delay = self.__drivetrain.get_delay(speed)
        is_direction_clear = None
        initial_yaw_reading = self.__imu.get_yaw_value()

        if direction == 'f':
            is_direction_clear = self.__sensing_system.is_front_clear
                    
        elif direction == 'b':
            is_direction_clear = self.__sensing_system.is_back_clear

        self.__drivetrain.set_direction(direction)

        for step in range(Drivetrain_Constants.CM * Map_Constants.TILE_SIZE):
            if is_direction_clear():
                self.__drivetrain.rotate_one_step(delay)
                
                if step % (Robot_Constants.COLLISION_CHECKING_FREQUENCY) == 0:
                    yaw = self.__imu.get_yaw_value()
                    difference = abs(yaw - initial_yaw_reading)

                    if difference > Robot_Constants.MINIMUM_COLLISION_DETECTION_ANGLE:
                        self.__reposition_on_tile(direction, step)
                        
                        if direction == 'f':
                            self.__drivetrain.drive('b', Map_Constants.TILE_SIZE, "slow")

                        elif direction == 'b':
                            self.__drivetrain.drive('f', Map_Constants.TILE_SIZE, "slow")


                        if yaw > initial_yaw_reading:
                            self.__drivetrain.turn('l', difference)

                        elif yaw < initial_yaw_reading:
                            self.__drivetrain.turn('r', difference)

                        return False

            else:
                self.__reposition_on_tile(direction, step)
        
                return False


        self.__map.update_position(direction)

        return True

    # old version (without bump detection)
    '''
    def __drive(self, direction, speed) -> bool:
        delay = self.__drivetrain.get_delay(speed)
        is_direction_clear = None

        if direction == 'f':
            is_direction_clear = self.__sensing_system.is_front_clear
                    
        elif direction == 'b':
            is_direction_clear = self.__sensing_system.is_back_clear

        self.__drivetrain.set_direction(direction)

        for step in range(Drivetrain_Constants.CM * Map_Constants.TILE_SIZE):
            if is_direction_clear():
                self.__drivetrain.rotate_one_step(delay)
                
            else:
                self.__reposition_on_tile(direction, step)
        
                return False


        self.__map.update_position(direction)

        return True
    '''

    
    # Turns the robot 90 degrees to the specified direction and updates orientation
    def __turn(self, direction):
        self.__drivetrain.strict_turn(direction)
        self.__map.update_orientation(direction)


    # Checks if there are obstacles present in the front or back
    def __check_if_stuck(self):
        if self.__sensing_system.is_front_clear():
            self.__drive('f', "slow")
            self.__map.update_map(self.__sensing_system.get_sensor_data())

        elif self.__sensing_system.is_back_clear():
            self.__drive('b', "slow")
            self.__map.update_map(self.__sensing_system.get_sensor_data())

        else:
            self.__buzzer.sound_signal("Stuck")

            return True

        return False


    # Returns the action, that the robot should take
    def __get_action(self, last_action):
        # Least visited clear direction or multiple clear directions that have been visited the same amount of times
        possible_directions = self.__get_least_visited_sides(self.__get_clear_sides())

        if last_action == 'l':
            possible_directions.remove('r')

        elif last_action == 'r':
            possible_directions.remove('l')


        if 'f' in possible_directions:
            return 'f'

        elif 'l' in possible_directions and 'r' in possible_directions:
            if random.choice([0, 1]) == 0:
                return 'l'

            else:
                return 'r'

        elif 'l' in possible_directions:
            return 'l'

        elif 'r' in possible_directions:
            return 'r'

        elif 'b' in possible_directions:
            return 'b'

        else:
            return None


    # Returns directions that don't have obstacles
    def __get_clear_sides(self):
        clear_sides = []

        for direction in Robot_Constants.DIRECTIONS:
            if not self.__map.check_for_obstacles(direction):
                clear_sides.append(direction)

        return clear_sides

    
    # Returns least visited sides from clear directions
    def __get_least_visited_sides(self, directions):
        if not directions:
            return None

        side_data = {}
        least_visited_sides = []

        for direction in directions:
            side_data[direction] = self.__map.check_visited_tiles(direction)

        if not side_data:
            return None

        min_times_visited = min(side_data.values())

        for direction, times_visited in side_data.items():
            if times_visited == min_times_visited:
                least_visited_sides.append(direction)

        return least_visited_sides


if __name__ == "__main__":
    robot = Robot(imu_auto_calibrate = False, sound_signals = True, debug = True)
    