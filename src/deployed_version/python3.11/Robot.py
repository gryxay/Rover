from time import sleep
from sys import exit as sys_exit
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


class Robot():
    def __init__(self, imu_auto_calibrate = True, sound_signals = True, debug = False):
        self.__sound_signals = sound_signals
        self.__debug = debug

        try:
            self.__buzzer = Buzzer(debug = self.__debug)
            self.__remote_receiver = IR_Receiver(buzzer = self.__buzzer, sound_signals = self.__sound_signals, debug = self.__debug)

        except:
            if self.__debug:
                print("Robot: Failed to initialize one or more hardware components")

            if self.__buzzer and sound_signals:
                self.__buzzer.sound_signal("Error")

            sys_exit(1)


        if sound_signals:
            self.__buzzer.sound_signal("Loading")

        self.__boot_handler()

        try:
            self.__computer_vision = Computer_Vision(buzzer = self.__buzzer, sound_signals = self.__sound_signals, debug = self.__debug)
            self.__sensing_system = Sensing_System(buzzer = self.__buzzer, sound_signals = self.__sound_signals, debug = self.__debug)
            self.__imu = IMU(buzzer = self.__buzzer, sound_signals = self.__sound_signals, auto_calibrate = imu_auto_calibrate, debug = self.__debug)
            self.__drivetrain = Drivetrain(imu = self.__imu, debug = self.__debug)

        except:
            if self.__debug:
                print("Robot: Failed to initialize one or more hardware components")

            if sound_signals:
                self.__buzzer.sound_signal("Error")

            sys_exit(1)


        self.__map = Map()

        if sound_signals:
            self.__buzzer.sound_signal("Ready")

        # Listen to remote for commands
        self.__listen_to_remote()


    def __boot_handler(self):
        if self.__debug:
            print("Robot: Waiting for a signal to continue loading...")
            print("Using the remote controller:")
            print("> Press ON to continue")
            print("> Press OFF to cancel")

        while True:
            if self.__remote_receiver.get_last_button_press() == "Start":
                self.__remote_receiver.reset_start_button_state()

                if self.__debug:
                    print("Robot: Continuing...")

                return

            elif self.__remote_receiver.get_last_button_press() == "Stop":
                self.__remote_receiver.terminate_background_process()

                if self.__sound_signals:
                    self.__buzzer.sound_signal("Cancelling")

                if self.__debug:
                    print("Robot: Cancelling...")

                exit()


    # Listens to the remote controller key presses
    def __listen_to_remote(self):
        if self.__debug:
            print("Robot: Listening to the remote controller")

        while True:
            if self.__remote_receiver.is_start_button_pressed():
                if self.__remote_receiver.get_mode() == "Autonomous":
                    self.__autonomous_mode()

                elif self.__remote_receiver.get_mode() == "Manual":
                    self.__remote_receiver.reset_last_button_press()
                    self.__manual_mode()

            elif self.__remote_receiver.get_last_button_press() == "Clear the map":
                self.__map.reset()

                self.__remote_receiver.reset_last_button_press()

                if self.__debug:
                    print("The map was cleared")

            sleep(Robot_Constants.LOOP_TIMEOUT)
    
    
    # Lets the user give commands to the robot
    def __autonomous_mode(self):
        while self.__remote_receiver.is_start_button_pressed() and self.__remote_receiver.get_mode() == "Autonomous":
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

            sleep(Robot_Constants.LOOP_TIMEOUT)


    # Lets the user control movement of the robot using the remote controller
    def __manual_mode(self):
        self.__drivetrain.toggle_power(True)

        while self.__remote_receiver.is_start_button_pressed() and self.__remote_receiver.get_mode() == "Manual":
            if self.__remote_receiver.get_last_button_press() == "Forward":
                while self.__sensing_system.is_front_clear() and self.__remote_receiver.get_last_button_press() == "Forward":
                    status = self.__drive('f', "fast")

                    self.__map.update_map(self.__sensing_system.get_sensor_data())
                
                    if not status:
                        self.__remote_receiver.reset_last_button_press()

            elif self.__remote_receiver.get_last_button_press() == "Backward":
                while self.__sensing_system.is_back_clear() and self.__remote_receiver.get_last_button_press() == "Backward":
                    status = self.__drive('b', "fast")

                    self.__map.update_map(self.__sensing_system.get_sensor_data())

                    if not status:
                        self.__remote_receiver.reset_last_button_press()

            elif self.__remote_receiver.get_last_button_press() == "Left":
                self.__turn('l')
                self.__remote_receiver.reset_last_button_press()

            elif self.__remote_receiver.get_last_button_press() == "Right":
                self.__turn('r')
                self.__remote_receiver.reset_last_button_press()

            elif self.__remote_receiver.get_last_button_press() == "Left micro turn":
                self.__drivetrain.micro_turn('l')
                self.__remote_receiver.reset_last_button_press()

            elif self.__remote_receiver.get_last_button_press() == "Right micro turn":
                self.__drivetrain.micro_turn('r')
                self.__remote_receiver.reset_last_button_press()

            sleep(Robot_Constants.LOOP_TIMEOUT)

        self.__map.display_map()
        self.__drivetrain.toggle_power(False)


    # The robot drives around and explores the room
    def __explore(self):
        consecutive_turns = []

        if self.__sound_signals:
            self.__buzzer.play_song("Exploring")

        self.__drivetrain.toggle_power(True)

        while self.__remote_receiver.is_start_button_pressed():
            self.__map.update_map(self.__sensing_system.get_sensor_data())

            action = self.__get_action(consecutive_turns)

            if action == 'f' or action == 'b':
                self.__drive(action, "fast")

                consecutive_turns.clear()

            elif action == 'l' or action == 'r':
                self.__turn(action)

                consecutive_turns.append(action)

            elif action is None:
                if self.__check_if_stuck():
                    break

                consecutive_turns.clear()

        self.__drivetrain.toggle_power(False)

        if self.__debug:
            self.__map.display_map()


    # The robot drives around and explores the room until it finds an object it was searching for
    def __find_object(self, object_to_find):
        consecutive_turns = []

        if self.__sound_signals:
            self.__buzzer.play_song("Exploring")

        self.__drivetrain.toggle_power(True)

        while self.__remote_receiver.is_start_button_pressed() and self.__computer_vision.get_last_detected_object() != object_to_find:
            self.__map.update_map(self.__sensing_system.get_sensor_data())

            action = self.__get_action(consecutive_turns)

            if action == 'f' or action == 'b':
                self.__drive(action, "fast")

                consecutive_turns.clear()

            elif action == 'l' or action == 'r':
                self.__turn(action)

                consecutive_turns.append(action)

            elif action is None:
                if self.__check_if_stuck():
                    break

                consecutive_turns.clear()

        self.__drivetrain.toggle_power(False)

        if self.__sound_signals and self.__computer_vision.get_last_detected_object() == object_to_find:
            self.__buzzer.play_song("Found it!")

        self.__computer_vision.reset_last_detected_object()

        self.__map.set_last_object_location()

        if self.__sound_signals and self.__computer_vision.get_last_detected_object() == object_to_find:
            self.__buzzer.play_song("Found it!")


        if self.__debug:
            self.__map.display_map()


    # Returns to the starting position
    def __return_to_home(self):
        self.__map.update_map(self.__sensing_system.get_sensor_data())
        directions = self.__get_directions_from_path(self.__map.get_shortest_path())

        if not directions:
            if self.__sound_signals:
                self.__buzzer.sound_signal("Stuck")

            self.__map.remove_distances_from_tiles()

            return

        while not self.__move_according_to_directions(directions):
            self.__map.remove_distances_from_tiles()
            self.__map.update_map(self.__sensing_system.get_sensor_data())

            directions = self.__get_directions_from_path(self.__map.get_shortest_path())

            if not directions:
                if self.__sound_signals:
                    self.__buzzer.sound_signal("Stuck")

                self.__map.remove_distances_from_tiles()

                return
            
        self.__turn_north()

        self.__buzzer.play_song("Found it!")

        self.__map.remove_distances_from_tiles()

        if self.__debug:
            self.__map.display_map()


    def __move_according_to_directions(self, directions) -> bool:
        self.__drivetrain.toggle_power(True)

        for direction in directions:
            if self.__remote_receiver.is_start_button_pressed():
                if direction == 'f' or direction == 'b':
                    if not self.__drive(direction, "fast"):
                        return False

                elif direction == 'l' or direction == 'r':
                    self.__turn(direction)

                self.__map.update_map(self.__sensing_system.get_sensor_data())

            else:
                return False
                
        self.__drivetrain.toggle_power(False)

        return True


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


    # Returns action that the robot should take
    def __get_action(self, consecutive_turns):
        clear_sides = self.__get_clear_sides()
        least_visited_sides = self.__get_least_visited_sides(clear_sides)

        if not least_visited_sides:
            return None

        if consecutive_turns and len(consecutive_turns) > 2 and least_visited_sides:
            if consecutive_turns[-1] == 'l' and 'r' in least_visited_sides:
                least_visited_sides.remove('r')

            elif consecutive_turns[-1] == 'r' and 'l' in least_visited_sides:
                least_visited_sides.remove('l')


        if 'f' in least_visited_sides:
            return 'f'

        elif 'l' in least_visited_sides and 'r' in least_visited_sides:
            if random.choice([0, 1]) == 0:
                return 'l'

            else:
                return 'r'

        elif 'l' in least_visited_sides:
            return 'l'

        elif 'r' in least_visited_sides:
            return 'r'

        elif 'b' in least_visited_sides:
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


    def __turn_north(self):
        direction = self.__map.get_current_orientation()

        if direction == 'N':
            return

        self.__drivetrain.toggle_power(True)

        if direction == 'W':
            self.__turn('r')

        elif direction == 'E':
            self.__turn('l')

        elif direction == 'S':
            if random.choice([0, 1]) == 0:
                self.__turn('l')
                self.__turn('l')

            else:
                self.__turn('r')
                self.__turn('r')

        self.__drivetrain.toggle_power(False)


    def __get_directions_from_path(self, path):
        directions = []

        if not path:
            return directions

        orientation = self.__map.get_current_orientation()
        current_x, current_y = path[0].get_x_position(), path[0].get_y_position()
        
        for i in range(1, len(path)):
            next_tile = path[i]
            next_x, next_y = next_tile.get_x_position(), next_tile.get_y_position()

            if current_x == next_x:
                if current_y > next_y:
                    
                    if orientation == 'N':
                        if random.choice([0, 1]) == 0:
                            directions.append('l')
                            directions.append('l')

                        else:
                            directions.append('r')
                            directions.append('r')

                        directions.append('f')

                        orientation = 'S'
                    
                    elif orientation == 'E':
                        directions.append('r')
                        directions.append('f')

                        orientation = 'S'
                    
                    elif orientation == 'S':
                        directions.append('f')
                    
                    elif orientation == 'W':
                        directions.append('l')
                        directions.append('f')

                        orientation = 'S'

                elif current_y < next_y:
                    
                    if orientation == 'N':
                        directions.append('f')
                    
                    elif orientation == "E":
                        directions.append('l')
                        directions.append('f')

                        orientation = 'N'
                    
                    elif orientation == 'S':
                        if random.choice([0, 1]) == 0:
                            directions.append('l')
                            directions.append('l')

                        else:
                            directions.append('r')
                            directions.append('r')

                        directions.append('f')

                        orientation = 'N'
                    
                    elif orientation == 'W':
                        directions.append('r')
                        directions.append('f')

                        orientation = 'N'

            elif current_y == next_y:
                if current_x > next_x:
                    
                    if orientation == "N":
                        directions.append("l")
                        directions.append("f")

                        orientation = 'W'
                    
                    elif orientation == "E":
                        if random.choice([0, 1]) == 0:
                            directions.append('l')
                            directions.append('l')
                        
                        else:
                            directions.append('r')
                            directions.append('r')

                        directions.append('f')

                        orientation = 'W'
                    
                    elif orientation == "S":
                        directions.append("r")
                        directions.append("f")

                        orientation = 'W'
                    
                    elif orientation == "W":
                        directions.append("f")
                
                if current_x < next_x:
                    
                    if orientation == "N":
                        directions.append('r')
                        directions.append('f')

                        orientation = 'E'
                    
                    elif orientation == "E":
                        directions.append('f')
                    
                    elif orientation == "S":
                        directions.append('l')
                        directions.append('f')

                        orientation = 'E'
                    
                    elif orientation == "W":
                        if random.choice([0, 1]) == 0:
                            directions.append('l')
                            directions.append('l')

                        else:
                            directions.append('r')
                            directions.append('r')

                        directions.append("f")

                        orientation = "E"

            current_x, current_y = next_x, next_y

        return directions


    def __terminate_background_processes(self):
        for process in [self.__remote_receiver, self.__imu, self.__computer_vision, self.__sensing_system]:
            process.terminate_background_process()


if __name__ == "__main__":
    robot = Robot(imu_auto_calibrate = False, sound_signals = True, debug = True)
    
