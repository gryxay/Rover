from multiprocessing import Process, Event, Queue, Value
from time import time, sleep
from sys import exit as sys_exit
import evdev

from Constants import IR_Receiver_Constants


class IR_Receiver:
    def __init__(self, buzzer = None, sound_signals = True, debug = False):
        self.__sound_signals = sound_signals
        self.__debug = debug
        
        self.__buzzer = buzzer
        self.__receiver = self.__get_device()

        self.__command_queue = Queue()
        self.__start_button_state = Value('b', 0)
        self.__last_key_press = Value('i', 0)

        # 0 - "Autonomous"; 1 - "Manual"
        self.__mode = Value('b', 0)

        self.__termination_event = Event()

        if self.__debug:
            print("IR Receiver: Starting a background process")

        # Start a process, that constantly reads IR receiver data
        self.__background_process = Process(target = self.__receive_command_keys)
        self.__background_process.start()


    def __get_device(self):
        devices = [evdev.InputDevice(path) for path in evdev.list_devices()]

        for device in devices:
            if (device.name == "gpio_ir_recv"):
                if self.__debug:
                    print("IR Receiver: Using device", device.path)

                return device

        if self.__debug:
            print("IR Receiver: No device found!")


    def __get_key(self, value, keybinds):
        for key, val in keybinds.items():
            if value == val:
                return key

        return None


    def __clear_queue(self):
        if self.__debug:
            print("IR Receiver: Clearing the queue")

        while not self.__command_queue.empty():
            self.__command_queue.get()


    def __main_keybind_handler(self, signal_key):
        keybinds = IR_Receiver_Constants.MAIN_KEYBINDS
        was_handled = False

        if signal_key == self.__get_key("Start", keybinds):
            with self.__start_button_state.get_lock():
                self.__start_button_state.value = 1

            was_handled = True

        elif signal_key == self.__get_key("Stop", keybinds):
            self.reset_start_button_state()

            was_handled = True

        elif signal_key == self.__get_key("Autonomous", keybinds) and self.get_mode() == "Manual":
            with self.__mode.get_lock():
                self.__mode.value = 0

            was_handled = True

        elif signal_key == self.__get_key("Manual", keybinds) and self.get_mode() == "Autonomous":
            with self.__mode.get_lock():
                self.__mode.value = 1

            was_handled = True

        elif signal_key == self.__get_key("Clear the map", keybinds):
            was_handled = True
            

        if was_handled:
            with self.__last_key_press.get_lock():
                self.__last_key_press.value = int(signal_key)

            if self.__buzzer and self.__sound_signals:
                self.__buzzer.beep(1, IR_Receiver_Constants.MAIN_KEYBINDS_BEEP_LENGTH)

            if self.__debug:
                print("IR Receiver (Main Keybinds): >", keybinds[signal_key], "< button was handled!")


    def __autonomous_mode_keybind_handler(self, signal_key):
        keybinds = IR_Receiver_Constants.AUTONOMOUS_MODE_KEYBINDS
        was_handled = False

        if signal_key == self.__get_key("Clear queue", keybinds):
            self.__clear_queue()

            was_handled = True

        elif signal_key in keybinds:
            self.__command_queue.put(signal_key)

            was_handled = True

            if self.__debug:
                print("IR Receiver: Item >", keybinds[signal_key], "< was added to the queue!")
        
        if was_handled:
            with self.__last_key_press.get_lock():
                self.__last_key_press.value = int(signal_key)

            if self.__buzzer and self.__sound_signals:
                self.__buzzer.beep(1, IR_Receiver_Constants.AUTONOMOUS_MODE_KEYBINDS_BEEP_LENGTH)

            if self.__debug:
                print("IR Receiver (Autonomous Mode Keybinds): >", keybinds[signal_key], "< button was handled!")


    def __manual_mode_keybind_handler(self, signal_key):
        keybinds = IR_Receiver_Constants.MANUAL_MODE_KEYBINDS

        if signal_key in keybinds:
            with self.__last_key_press.get_lock():
                self.__last_key_press.value = int(signal_key)

            if self.__buzzer and self.__sound_signals:
                self.__buzzer.beep(1, IR_Receiver_Constants.MAIN_KEYBINDS_BEEP_LENGTH)

            if self.__debug:
                print("IR Receiver (Manual Mode Keybinds): >", keybinds[signal_key], "< button was handled!")


    def __receive_command_keys(self):
        last_button_press = None
        button_press_time = time()

        try:
            while not self.__termination_event.is_set():
                signal_key = self.__receiver.read_one()

                if signal_key:
                    signal_key = str(signal_key.value)

                    if signal_key == last_button_press:
                        continue    

                    if signal_key in IR_Receiver_Constants.BUTTON_KEYS:
                        if signal_key not in IR_Receiver_Constants.MANUAL_MODE_KEYBINDS:
                            last_button_press = signal_key

                    # Main keybinds
                    if signal_key in IR_Receiver_Constants.MAIN_KEYBINDS:

                        self.__main_keybind_handler(signal_key)

                    # Autonomous mode keybinds
                    elif self.get_mode() == "Autonomous" and signal_key in IR_Receiver_Constants.AUTONOMOUS_MODE_KEYBINDS:
                    
                        self.__autonomous_mode_keybind_handler(signal_key)

                    # Manual mode Keybinds
                    elif self.get_mode() == "Manual" and signal_key in IR_Receiver_Constants.MANUAL_MODE_KEYBINDS:
                        if time() - button_press_time > IR_Receiver_Constants.LAST_BUTTON_PRESS_TIMEOUT:
                            self.__manual_mode_keybind_handler(signal_key)

                            button_press_time = time()

                sleep(IR_Receiver_Constants.LOOP_TIMEOUT)

        except:
            if self.__sound_signals:
                self.__buzzer.sound_signal("Error")

            sys_exit(1)


    # Returns True if start button is pressed
    def is_start_button_pressed(self):
        with self.__start_button_state.get_lock():
            if self.__start_button_state.value == 0:
                return False

        return True


    # Sets start button state to OFF
    def reset_start_button_state(self):
        with self.__start_button_state.get_lock():
            self.__start_button_state.value = 0


    # Returns mode of the remote
    def get_mode(self):
        with self.__mode.get_lock():
            if self.__mode.value == 0:
                return "Autonomous"
        
        return "Manual"


    # Should be used in Autonomous mode
    def get_command(self):
        if self.__command_queue.empty():
            return None

        return IR_Receiver_Constants.AUTONOMOUS_MODE_KEYBINDS[str(self.__command_queue.get())]


    # Should be used in Manual mode
    def get_last_button_press(self):
        last_key_press = None

        with self.__last_key_press.get_lock():
            last_key_press = str(self.__last_key_press.value)

        if last_key_press in IR_Receiver_Constants.MAIN_KEYBINDS:
            return IR_Receiver_Constants.MAIN_KEYBINDS[last_key_press]

        if last_key_press in IR_Receiver_Constants.AUTONOMOUS_MODE_KEYBINDS and self.get_mode() == "Autonomous":
            return IR_Receiver_Constants.AUTONOMOUS_MODE_KEYBINDS[last_key_press]

        if last_key_press in IR_Receiver_Constants.MANUAL_MODE_KEYBINDS and self.get_mode() == "Manual":
            return IR_Receiver_Constants.MANUAL_MODE_KEYBINDS[last_key_press]

        return None



    def reset_last_button_press(self):
        with self.__last_key_press.get_lock():
            self.__last_key_press.value = 0


    def terminate_background_process(self):
        self.__termination_event.set()
