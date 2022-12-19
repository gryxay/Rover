from multiprocessing import Process, Queue, Value
from collections import deque
from time import sleep
import evdev

from beeper import Beeper


START_KEY = 61187
STOP_KEY = 61186
CLEAR_QUEUE_KEY = 61191
AI_MODE_KEY = 61184
SEMI_MANUAL_MODE_KEY = 61185

# Commands for AI mode
COMMANDS = {
    "61188": "Explore",
    "61189": "Find a human",
    "61190": "Return to home",
    "61192": "Unsigned",
    "61193": "Unsigned",
    "61194": "Unsigned",
    "61195": "Unsigned",
    "61196": "Unsigned",
    "61197": "Unsigned",
    "61198": "Unsigned",
    "61199": "Unsigned",
    "61200": "Unsigned",
    "61201": "Unsigned",
    "61202": "Unsigned",
    "61203": "Unsigned",
    "61204": "Unsigned",
    "61205": "Unsigned",
    "61206": "Unsigned",
    "61207": "Unsigned",
}

# Controlls for Semi-manual mode
CONTROLLS = {
    "61197": "Forward",
    "61205": "Backward",
    "61200": "Left",
    "61202": "Right"
}


class IR_Receiver:
    def __init__(self, debug = False, sound_signals = True):
        self.__sound_signals = sound_signals
        self.__debug = debug
        
        self.__receiver = self.__get_device()
        self.__beeper = Beeper()

        self.__command_queue = Queue()
        self.__last_command = Value('i', 0)
        self.__mode = Value('b', 0)   # 0 - "AI mode"; 1 - "Semi-manual mode"
        self.__start_button_pressed = Value('b', 0)

        # Start a process, that constantly reads IR receiver data
        Process(target = self.__receive_command_keys).start()


    def __get_device(self):
        devices = [evdev.InputDevice(path) for path in evdev.list_devices()]

        for device in devices:
            if (device.name == "gpio_ir_recv"):
                if self.__debug:
                    print("Receiver: Using device", device.path, "\n")

                return device

        if self.__debug:
            print("Receiver: No device found!")


    def __receive_command_keys(self):
        last_reading = None
        semi_manual_mode_filter = deque([0, 0], maxlen = 2)

        while True:
            reading = self.__receiver.read_one()

            if reading:
                if reading.value == START_KEY and reading.value != last_reading:
                    self.__start_button_pressed.value = 1

                    last_reading = START_KEY

                    if self.__sound_signals:
                        self.__beeper.beep(1, 0.1)

                    if self.__debug:
                        print("Receiver: Start button has been pressed")

                elif reading.value == STOP_KEY and reading.value != last_reading:
                    self.__start_button_pressed.value = 0

                    last_reading = STOP_KEY

                    if self.__sound_signals:
                        self.__beeper.beep(1, 0.1)

                    if self.__debug:
                        print("Receiver: Stop button has been pressed")

                elif reading.value == AI_MODE_KEY and self.__mode.value == 1:
                    self.__mode.value = 0
                    self.__clear_queue()

                    last_reading = AI_MODE_KEY

                    if self.__sound_signals:
                        self.__beeper.beep(1, 0.1)

                    if self.__debug:
                        print("Receiver: Mode changed to \"AI\"")

                elif reading.value == SEMI_MANUAL_MODE_KEY and self.__mode.value == 0:
                    self.__mode.value = 1

                    last_reading = SEMI_MANUAL_MODE_KEY

                    if self.__sound_signals:
                        self.__beeper.beep(1, 0.1)

                    if self.__debug:
                        print("Receiver: Mode changed to \"Semi-manual\"")

                # If remote is in AI mode
                if self.__mode.value == 0:
                    if reading.value == CLEAR_QUEUE_KEY and reading.value != last_reading:
                        last_reading = reading.value
                        self.__clear_queue()

                        if self.__sound_signals:
                            self.__beeper.beep(1, 0.3)

                        continue

                    elif str(reading.value) in COMMANDS and reading.value != last_reading:
                        last_reading = reading.value
                        self.__command_queue.put(reading.value)

                        if self.__sound_signals:
                            self.__beeper.beep(1, 0.1)

                        if self.__debug:
                            print("Receiver: Key added to the queue:", reading.value)

                # If remote is in Semi-manual mode
                elif self.__mode.value == 1:
                    if str(reading.value) in CONTROLLS:
                        self.__last_command.value = reading.value

                        semi_manual_mode_filter.appendleft(reading.value)

                        if self.__debug:
                            print("Receiver: Last command set to", reading.value)

                    else:
                        semi_manual_mode_filter.appendleft(0)

                        if all(value == 0 for value in semi_manual_mode_filter):
                            self.__last_command.value = 0
                            
                            if self.__debug:
                                print("Receiver: Last command set to 0")

        
    def __clear_queue(self):
        if self.__debug:
            print("Receiver: Clearing the queue")

        while not self.__command_queue.empty():
            self.__command_queue.get()


    # Should be used in AI mode
    def get_command(self):
        if self.__command_queue.empty():
            return None

        command = COMMANDS[str(self.__command_queue.get())]

        if command == "Unsigned":
            command = self.get_command()

        return command


    # Should be used in semi-manual mode
    def get_last_command(self):
        if str(self.__last_command.value) in CONTROLLS:
            return CONTROLLS[str(self.__last_command.value)]

        return None

    
    def reset_last_command(self):
        self.__last_command.value = 0


    def is_start_button_pressed(self):
        if self.__start_button_pressed.value == 0:
            return False

        return True


    def get_mode(self):
        if self.__mode.value == 0:
            return "AI mode"
        
        return "Semi-manual mode"


# For testing purposes
if __name__ == "__main__":
    receiver = IR_Receiver(debug = True)
