from multiprocessing import Process, Queue, Value
from time import sleep
from beeper import Beeper

import evdev 


MIN_KEY = 61184
MAX_KEY = 61207

CLEAR_QUEUE_KEY = 61191

COMMANDS = {
    "61184": "AI mode",
    "61185": "Manual mode",
    "61186": "Stop",
    "61187": "Start",
    "61188": "Unsigned",
    "61189": "Unsigned",
    "61190": "Unsigned",
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


class IR_Receiver:
    def __init__(self, debug = False, sound_signals = True):
        self.debug = debug
        self.sound_signals = sound_signals
        
        self.receiver = self.get_device()
        self.beeper = Beeper()

        self.command_queue = Queue()

        # 0 - "AI mode"; 1 - "Manual mode";
        #self.mode = Value('b', 0)

        # Start a process, that constantly reads IR receiver data
        Process(target = self.receive_command_keys).start()


    def get_device(self):
        devices = [evdev.InputDevice(path) for path in evdev.list_devices()]

        for device in devices:
            if (device.name == "gpio_ir_recv"):
                if self.debug:
                    print("Using device", device.path, "\n")

                return device

        if self.debug:
            print("No device found!")


    def receive_command_keys(self):
        last_reading = None

        while(True):
            reading = self.receiver.read_one()

            if (reading):
                if reading.value == CLEAR_QUEUE_KEY and reading.value != last_reading:
                    if self.debug:
                        print("Clearing the queue")

                    last_reading = reading.value
                    self.clear_queue()

                    if self.sound_signals:
                        self.beeper.beep(1, 0.3)

                    continue

                if reading.value >= MIN_KEY and reading.value <= MAX_KEY and reading.value != last_reading:
                    last_reading = reading.value
                    self.command_queue.put(reading.value)

                    if self.debug:
                        print("Last read:", reading.value)

                    if self.sound_signals:
                        self.beeper.beep(1, 0.1)

        
    def clear_queue(self):
        while not self.command_queue.empty():
            self.command_queue.get()


    def get_command(self):
        if self.command_queue.empty():
            return None

        command = COMMANDS[str(self.command_queue.get())]

        if command == "Unsigned":
            command = self.get_command()

        return command


if __name__ == "__main__":
    receiver = IR_Receiver(debug = True)

    sleep(5)

    print(receiver.get_command())