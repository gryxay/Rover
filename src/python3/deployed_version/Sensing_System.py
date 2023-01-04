from time import sleep
from multiprocessing import Process, Value

from Distance_Sensor import Distance_Sensor

from Constants import Sensing_System_Constants


class Sensing_System:
    __front_sensor = None
    __rear_sensor = None
    __left_sensor = None
    __right_sensor = None

    __front_sensor_last_scan = Value('i', 0)
    __rear_sensor_last_scan = Value('i', 0)
    __left_sensor_last_scan = Value('i', 0)
    __right_sensor_last_scan = Value('i', 0)

    __background_process = None


    def __init__(self, front_sensor_trig_pin = Sensing_System_Constants.FRONT_SENSOR_TRIG_PIN, \
                       front_sensor_echo_pin = Sensing_System_Constants.FRONT_SENSOR_ECHO_PIN, \
                       rear_sensor_trig_pin = Sensing_System_Constants.REAR_SENSOR_TRIG_PIN, \
                       rear_sensor_echo_pin = Sensing_System_Constants.REAR_SENSOR_ECHO_PIN, \
                       left_sensor_trig_pin = Sensing_System_Constants.LEFT_SENSOR_TRIG_PIN, \
                       left_sensor_echo_pin = Sensing_System_Constants.LEFT_SENSOR_ECHO_PIN, \
                       right_sensor_trig_pin = Sensing_System_Constants.RIGHT_SENSOR_TRIG_PIN, \
                       right_sensor_echo_pin = Sensing_System_Constants.RIGHT_SENSOR_ECHO_PIN):

        self.__front_sensor = Distance_Sensor(front_sensor_trig_pin, front_sensor_echo_pin)
        self.__rear_sensor = Distance_Sensor(rear_sensor_trig_pin, rear_sensor_echo_pin)
        self.__left_sensor = Distance_Sensor(left_sensor_trig_pin, left_sensor_echo_pin)
        self.__right_sensor = Distance_Sensor(right_sensor_trig_pin, right_sensor_echo_pin)

        # Start a process, that constantly updates distance sensor in the background
        self.__background_process = Process(target = self.__update_sensor_data)
        self.__background_process.start()


    def __update_sensor_data(self):
        while True:
            distance = round(self.__front_sensor.get_distance())

            with self.__front_sensor_last_scan.get_lock():
                self.__front_sensor_last_scan.value = distance


            distance = round(self.__rear_sensor.get_distance())

            with self.__rear_sensor_last_scan.get_lock():
                self.__rear_sensor_last_scan.value = distance


            distance = round(self.__left_sensor.get_distance())

            with self.__left_sensor_last_scan.get_lock():
                self.__left_sensor_last_scan.value = distance


            distance = round(self.__right_sensor.get_distance())

            with self.__right_sensor_last_scan.get_lock():
                self.__right_sensor_last_scan.value = distance


    def get_front_sensor_distance(self):
        with self.__front_sensor_last_scan.get_lock():
            return self.__front_sensor_last_scan.value


    def get_rear_sensor_distance(self):
        with self.__rear_sensor_last_scan.get_lock():
            return self.__rear_sensor_last_scan.value


    def get_left_sensor_distance(self):
        with self.__left_sensor_last_scan.get_lock():
            return self.__left_sensor_last_scan.value


    def get_right_sensor_distance(self):
        with self.__right_sensor_last_scan.get_lock():
            return self.__right_sensor_last_scan.value


    def get_sensor_data(self):
        return {
            "front": self.__front_sensor_last_scan.value,
            "rear": self.__rear_sensor_last_scan.value,
            "left": self.__left_sensor_last_scan.value,
            "right": self.__right_sensor_last_scan.value
	    }


    def is_front_clear(self):
        if self.__front_sensor_last_scan.value > Sensing_System_Constants.MIN_FRONT_DISTANCE and \
           self.__left_sensor_last_scan.value > Sensing_System_Constants.MIN_LEFT_DISTANCE and \
           self.__right_sensor_last_scan.value > Sensing_System_Constants.MIN_RIGHT_DISTANCE:

            return True 
        
        return False


    def is_back_clear(self):
        if self.__rear_sensor_last_scan.value > Sensing_System_Constants.MIN_BACK_DISTANCE:
            return True
        
        return False


# For testing purposes
if __name__ == "__main__":
    sensing_system = Sensing_System()

    while True:
        print(sensing_system.get_sensor_data())
