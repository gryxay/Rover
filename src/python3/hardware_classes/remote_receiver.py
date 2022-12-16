from multiprocessing import Process, Queue, Value
from time import sleep
from collections import deque
from beeper import Beeper

import evdev 


START_KEY = 61187
STOP_KEY = 61186
CLEAR_QUEUE_KEY = 61191
AI_MODE_KEY = 61184
MANUAL_MODE_KEY = 61185

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

CONTROLLS = {
    "61197": "Forward",
    "61205": "Backward",
    "61200": "Left",
    "61202": "Right"
}


class IR_Receiver:
    def __init__(self, debug = False, sound_signals = True):
        self.__debug = debug
        self.__sound_signals = sound_signals
        
        self.__receiver = self.__get_device()
        self.__beeper = Beeper()

        self.__command_queue = Queue()
        self.__last_command = Value('i', 0)
        self.__mode = Value('b', 0)   # 0 - "AI mode"; 1 - "Manual mode"
        self.__start_button_pressed = Value('b', 0)
        self.__stop_button_pressed = Value('b', 0)

        # Start a process, that constantly reads IR receiver data
        Process(target = self.__receive_command_keys).start()


    def __get_device(self):
        devices = [evdev.InputDevice(path) for path in evdev.list_devices()]

        for device in devices:
            if (device.name == "gpio_ir_recv"):
                if self.__debug:
                    print("Using device", device.path, "\n")

                return device

        if self.__debug:
            print("No device found!")


    def __receive_command_keys(self):
        last_reading = None
        manual_mode_filter = deque([0, 0, 0], maxlen = 2)

        while(True):
            reading = self.__receiver.read_one()

            if (reading):
                if reading.value == START_KEY and reading.value != last_reading:
                    last_reading = START_KEY

                    if self.__sound_signals:
                        self.__beeper.beep(1, 0.1)

                    if self.__debug:
                        print("Start button has been pressed")

                elif reading.value == STOP_KEY and reading.value != last_reading:
                    last_reading = STOP_KEY

                    if self.__sound_signals:
                        self.__beeper.beep(1, 0.1)

                    if self.__debug:
                        print("Stop button has been pressed")

                elif reading.value == AI_MODE_KEY and self.__mode.value == 1:
                    last_reading = AI_MODE_KEY

                    self.__clear_queue()
                    self.__mode.value = 0

                    if self.__sound_signals:
                        self.__beeper.beep(1, 0.1)

                    if self.__debug:
                        print("Mode changed to \"AI\"")

                elif reading.value == MANUAL_MODE_KEY and self.__mode.value == 0:
                    last_reading = MANUAL_MODE_KEY

                    self.__mode.value = 1

                    if self.__sound_signals:
                        self.__beeper.beep(1, 0.1)

                    if self.__debug:
                        print("Mode changed to \"Manual\"")

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
                            print("Kay added to the queue:", reading.value)

                elif self.__mode.value == 1:
                    if str(reading.value) in CONTROLLS:
                        self.__last_command.value = reading.value

                        manual_mode_filter.appendleft(reading.value)

                        if self.__debug:
                            print("Last command set to", reading.value)

                    else:
                        manual_mode_filter.appendleft(0)

                        if all(value == 0 for value in manual_mode_filter):
                            self.__last_command.value = 0
                            
                            if self.__debug:
                                print("Last command set to 0")

        
    def __clear_queue(self):
        if self.__debug:
            print("Clearing the queue")

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


    # Should be used in manual mode
    def get_last_command(self):
        if str(self.__last_command.value) in CONTROLLS:
            return CONTROLLS[str(self.__last_command.value)]

        return None


    def get_start_button_state(self):
        if self.__start_button_pressed.value == 0:
            return False

        return True


    def get_stop_button_state(self):
        if self.__stop_button_pressed.value == 0:
            return False

        return True


    def get_mode(self):
        return self.__mode.value
