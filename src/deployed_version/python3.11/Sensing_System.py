from multiprocessing import Process, Event, Value
from time import sleep
from sys import exit as sys_exit
from Distance_Sensor import Distance_Sensor

from Constants import Sensing_System_Constants
from Constants import Robot_Constants


class Sensing_System:
    def __init__(self, front_sensor_trig_pin = Sensing_System_Constants.FRONT_SENSOR_TRIG_PIN, \
                       front_sensor_echo_pin = Sensing_System_Constants.FRONT_SENSOR_ECHO_PIN, \
                       rear_sensor_trig_pin = Sensing_System_Constants.REAR_SENSOR_TRIG_PIN, \
                       rear_sensor_echo_pin = Sensing_System_Constants.REAR_SENSOR_ECHO_PIN, \
                       left_sensor_trig_pin = Sensing_System_Constants.LEFT_SENSOR_TRIG_PIN, \
                       left_sensor_echo_pin = Sensing_System_Constants.LEFT_SENSOR_ECHO_PIN, \
                       right_sensor_trig_pin = Sensing_System_Constants.RIGHT_SENSOR_TRIG_PIN, \
                       right_sensor_echo_pin = Sensing_System_Constants.RIGHT_SENSOR_ECHO_PIN, \
                       buzzer = None, sound_signals = False, debug = False):

        self.__debug = debug
        self.__sound_signals = sound_signals

        self.__buzzer = buzzer

        if self.__debug:
            print("Sensing System: Initialising Distance Sensors")

        self.__sensors = {}

        self.__sensors['f'] = Distance_Sensor(front_sensor_trig_pin, front_sensor_echo_pin)
        self.__sensors['b'] = Distance_Sensor(rear_sensor_trig_pin, rear_sensor_echo_pin)
        self.__sensors['l'] = Distance_Sensor(left_sensor_trig_pin, left_sensor_echo_pin)
        self.__sensors['r'] = Distance_Sensor(right_sensor_trig_pin, right_sensor_echo_pin)

        self.__sensor_data = {
            'f': Value('f', float(Sensing_System_Constants.MIN_FRONT_DISTANCE + 1)),
            'b': Value('f', float(Sensing_System_Constants.MIN_BACK_DISTANCE + 1)),
            'l': Value('f', float(Sensing_System_Constants.MIN_LEFT_DISTANCE + 1)),
            'r': Value('f', float(Sensing_System_Constants.MIN_RIGHT_DISTANCE + 1))
        }

        self.__termination_event = Event()

        if self.__debug:
            print("Sensing System: Starting a background process")

        # Start a process, that constantly updates distance sensor in the background
        self.__background_process = Process(target = self.__update_sensor_data)
        self.__background_process.start()


    # Reads data from Ultrasound Distance Sensors consecutively
    def __update_sensor_data(self):
        try:
            while not self.__termination_event.is_set():
                for direction in Robot_Constants.DIRECTIONS:
                    distance = self.__sensors[direction].get_distance()

                    if distance is not None:
                        with self.__sensor_data[direction].get_lock():
                            self.__sensor_data[direction].value = distance

        except:
            if self.__debug:
                print("Sensing System error!")

            if self.__buzzer and self.__sound_signals:
                self.__buzzer.sound_signal("Error")

            sys_exit(1)



    # Returns the distance in CM between front distance sensor and the obstacle
    def get_front_sensor_distance(self) -> float:
        with self.__sensor_data['f'].get_lock():
            return self.__sensor_data['f'].value


    # Returns the distance in CM between the rear sensor and the obstacle
    def get_rear_sensor_distance(self) -> float:
        with self.__sensor_data['b'].get_lock():
            return self.__sensor_data['b'].value


    # Returns the distance in CM between the left sensor and the obstacle
    def get_left_sensor_distance(self) -> float:
        with self.__sensor_data['l'].get_lock():
            return self.__sensor_data['l'].value - Sensing_System_Constants.SIDE_SENSOR_OFFSET


    # Returns the distance in CM between the right sensor and the obstacle
    def get_right_sensor_distance(self) -> float:
        with self.__sensor_data['r'].get_lock():
            return self.__sensor_data['r'].value - Sensing_System_Constants.SIDE_SENSOR_OFFSET

    # Returns the distance in CM between distance sensors and the obstacles
    def get_sensor_data(self) -> dict:
        return {
            'f': self.get_front_sensor_distance(),
            'b': self.get_rear_sensor_distance(),
            'l': self.get_left_sensor_distance(),
            'r': self.get_right_sensor_distance()
	    }


    # Returns True if there are no obstacles in the front of the robot
    def is_front_clear(self) -> bool:
        if self.get_front_sensor_distance() > Sensing_System_Constants.MIN_FRONT_DISTANCE and \
           self.get_left_sensor_distance() > Sensing_System_Constants.MIN_LEFT_DISTANCE and \
           self.get_right_sensor_distance() > Sensing_System_Constants.MIN_RIGHT_DISTANCE:

            return True 
        
        return False


    # Returns True if there are no obstacles in the rear of the robot
    def is_back_clear(self) -> bool:
        if self.get_rear_sensor_distance() > Sensing_System_Constants.MIN_BACK_DISTANCE:
            return True
        
        return False


    def terminate_background_process(self):
        self.__termination_event.set()
        
