from multiprocessing import Process, Queue, Value
from time import sleep
import evdev

from beeper import Beeper


KEYBINDS = {
    "61184": "Autonomous mode",
    "61185": "Manual mode",
    "61186": "Stop",
    "61187": "Start",
    "61188": "Explore",
    "61189": "Find a human",
    "61190": "Return to home",
    "61191": "Clear queue",
    "61192": "Unsigned",
    "61193": "Unsigned",
    "61194": "Unsigned",
    "61195": "Unsigned",
    "61196": "Unsigned",
    "61197": "Forward",
    "61198": "Unsigned",
    "61199": "Unsigned",
    "61200": "Left",
    "61201": "Stop",
    "61202": "Right",
    "61203": "Unsigned",
    "61204": "Unsigned",
    "61205": "Backward",
    "61206": "Unsigned",
    "61207": "Unsigned"
}


class IR_Receiver:
    def __init__(self, sound_signals = True, debug = False):
        self.__sound_signals = sound_signals
        self.__debug = debug
        
        self.__receiver = self.__get_device()
        self.__beeper = Beeper()

        self.__command_queue = Queue()
        self.__last_key_press = Value('i', 0)
        self.__mode = Value('b', 0) # 0 - "Autonomous mode"; 1 - "Manual mode"
        self.__start_button_state = Value('b', 0)

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

        while True:
            reading = self.__receiver.read_one()

            if reading:
                if reading.value == self.__get_key("Start") and self.__start_button_state.value != 1:
                    self.__start_button_state.value = 1

                    last_reading = self.__get_key("Start")

                    if self.__sound_signals:
                        self.__beeper.beep(1, 0.1)

                    if self.__debug:
                        print("Receiver: Start button has been pressed")

                    continue

                elif reading.value == self.__get_key("Stop") and self.__start_button_state.value != 0:
                    self.__start_button_state.value = 0

                    last_reading = self.__get_key("Stop")

                    if self.__sound_signals:
                        self.__beeper.beep(1, 0.1)

                    if self.__debug:
                        print("Receiver: Stop button has been pressed")

                    continue

                elif reading.value == self.__get_key("Autonomous mode") and self.__mode.value == 1:
                    self.__mode.value = 0
                    self.__clear_queue()

                    last_reading = self.__get_key("Autonomous mode")

                    if self.__sound_signals:
                        self.__beeper.beep(1, 0.1)

                    if self.__debug:
                        print("Receiver: Mode changed to \"Autonomous\"")

                    continue

                elif reading.value == self.__get_key("Manual mode") and self.__mode.value == 0:
                    self.__mode.value = 1

                    last_reading = self.__get_key("Manual mode")

                    if self.__sound_signals:
                        self.__beeper.beep(1, 0.1)

                    if self.__debug:
                        print("Receiver: Mode changed to \"Manual\"")

                    continue

                # If remote is in Autonomous mode
                if self.__mode.value == 0:
                    if reading.value == self.__get_key("Clear queue") and reading.value != last_reading:
                        last_reading = reading.value
                        self.__clear_queue()

                        if self.__sound_signals:
                            self.__beeper.beep(1, 0.3)

                        continue

                    elif str(reading.value) in KEYBINDS and reading.value != last_reading:
                        last_reading = reading.value
                        self.__command_queue.put(reading.value)

                        if self.__sound_signals:
                            self.__beeper.beep(1, 0.1)

                        if self.__debug:
                            print("Receiver: Key added to the queue:", reading.value)

                        continue

                # If remote is in Manual mode
                elif self.__mode.value == 1:
                    if str(reading.value) in KEYBINDS and reading.value != self.__last_key_press.value:
                        self.__last_key_press.value = reading.value

                        last_reading = reading.value

                        if self.__debug:
                            print("Receiver: Last key press set to", reading.value)

    
    def __get_key(self, value):
        for key, val in KEYBINDS.items():
            if value == val:
                return int(key)

        return None


    def __clear_queue(self):
        if self.__debug:
            print("Receiver: Clearing the queue")

        while not self.__command_queue.empty():
            self.__command_queue.get()


    def is_start_button_pressed(self):
        if self.__start_button_state.value == 0:
            return False

        return True


    def get_mode(self):
        if self.__mode.value == 0:
            return "Autonomous mode"
        
        return "Manual mode"


    # Should be used in Autonomous mode
    def get_command(self):
        if self.__command_queue.empty():
            return None

        command = KEYBINDS[str(self.__command_queue.get())]

        if command == "Unsigned":
            command = self.get_command()

        return command


    # Should be used in Manual mode
    def get_last_key_press(self):
        if str(self.__last_key_press.value) in KEYBINDS:
            return KEYBINDS[str(self.__last_key_press.value)]

        return None


    def reset_last_key_press(self):
        self.__last_key_press.value = 0


# For testing purposes
if __name__ == "__main__":
    receiver = IR_Receiver(sound_signals = False, debug = True)
