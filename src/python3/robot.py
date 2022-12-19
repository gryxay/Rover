from drivetrain import Drivetrain
from sensing_system import Sensing_system
from remote_receiver import IR_Receiver
from beeper import Beeper

from map import Map

from time import sleep

# In development
class Robot():
    def __init__(self, debug = False, sound_signals = True):
        self.__sound_signals = sound_signals
        self.__debug = debug

        self.__drivetrain = Drivetrain(debug = True)
        self.__sensing_system = Sensing_system()
        self.__remote_receiver = IR_Receiver(debug = True, sound_signals = False)
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
                if self.__remote_receiver.get_mode() == "AI mode":
                    command = self.__remote_receiver.get_command()

                    if command == "Explore":
                        # TODO
                        print("Explore")

                    elif command == "Find a human": 
                        # TODO
                        print("Find a human")

                    elif command == "Return to home":
                        # TODO
                        print("Return to home")

                elif self.__remote_receiver.get_mode() == "Semi-manual mode":
                    self.__manual_mode()


    def __manual_mode(self):
        while self.__remote_receiver.is_start_button_pressed() and self.__remote_receiver.get_mode() == "Manual mode":
            if self.__remote_receiver.get_last_command() == "Forward":
                if not self.__sensing_system.is_front_clear():
                    self.__remote_receiver.reset_last_command()

                while self.__sensing_system.is_front_clear() and self.__remote_receiver.get_last_command() == "Forward":
                    self.__drivetrain.rotate('f')

            elif self.__remote_receiver.get_last_command() == "Backward":
                if not self.__sensing_system.is_back_clear():
                    self.__remote_receiver.reset_last_command()

                while self.__sensing_system.is_back_clear() and self.__remote_receiver.get_last_command() == "Backward":
                    self.__drivetrain.rotate('b')

            elif self.__remote_receiver.get_last_command() == "Left":
                self.__drivetrain.turn('l', 90)
                self.__remote_receiver.reset_last_command()

            elif self.__remote_receiver.get_last_command() == "Right":
                self.__drivetrain.turn('r', 90)
                self.__remote_receiver.reset_last_command()


if __name__ == "__main__":
    robot = Robot(debug = True, sound_signals = False)
