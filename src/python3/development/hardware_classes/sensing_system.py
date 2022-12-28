from multiprocessing import Process, Value

from distance_sensor import Distance_sensor


MIN_FRONT_DISTANCE = 10 
MIN_LEFT_DISTANCE = 15
MIN_RIGHT_DISTANCE = 15

MIN_BACK_DISTANCE = 10


FRONT_SENSOR_TRIG_PIN = 24
FRONT_SENSOR_ECHO_PIN = 23

REAR_SENSOR_TRIG_PIN = 14
REAR_SENSOR_ECHO_PIN = 15

LEFT_SENSOR_TRIG_PIN = 25
LEFT_SENSOR_ECHO_PIN = 8

RIGHT_SENSOR_TRIG_PIN = 7
RIGHT_SENSOR_ECHO_PIN = 12


class Sensing_system:
    def __init__(self, front_sensor_trig_pin = FRONT_SENSOR_TRIG_PIN, front_sensor_echo_pin = FRONT_SENSOR_ECHO_PIN, \
                    rear_sensor_trig_pin = REAR_SENSOR_TRIG_PIN, rear_sensor_echo_pin = REAR_SENSOR_ECHO_PIN, \
                    left_sensor_trig_pin = LEFT_SENSOR_TRIG_PIN, left_sensor_echo_pin = LEFT_SENSOR_ECHO_PIN, \
                    right_sensor_trig_pin = RIGHT_SENSOR_TRIG_PIN, right_sensor_echo_pin = RIGHT_SENSOR_ECHO_PIN):
        self.__front_sensor = Distance_sensor(front_sensor_trig_pin, front_sensor_echo_pin)
        self.__rear_sensor = Distance_sensor(rear_sensor_trig_pin, rear_sensor_echo_pin)
        self.__left_sensor = Distance_sensor(left_sensor_trig_pin, left_sensor_echo_pin)
        self.__right_sensor = Distance_sensor(right_sensor_trig_pin, right_sensor_echo_pin)

        self.__front_sensor_last_scan = Value('f', 0.0)
        self.__rear_sensor_last_scan = Value('f', 0.0)
        self.__left_sensor_last_scan = Value('f', 0.0)
        self.__right_sensor_last_scan = Value('f', 0.0)

        # Start a process, that constantly updates distance sensor in the background
        Process(target = self.__update_sensor_data).start()


    def __update_sensor_data(self):
        while True:
            self.__front_sensor_last_scan.value = self.__front_sensor.get_distance()
            self.__rear_sensor_last_scan.value = self.__rear_sensor.get_distance()
            self.__left_sensor_last_scan.value = self.__left_sensor.get_distance()
            self.__right_sensor_last_scan.value = self.__right_sensor.get_distance()


    def get_front_sensor_distance(self):
        return self.__front_sensor_last_scan.value


    def get_rear_sensor_distance(self):
        return self.__rear_sensor_last_scan.value


    def get_left_sensor_distance(self):
        return self.__left_sensor_last_scan.value


    def get_right_sensor_distance(self):
        return self.__right_sensor_last_scan.value


    def get_sensor_data(self):
        return {
            "front": self.__front_sensor_last_scan.value,
            "rear": self.__rear_sensor_last_scan.value,
            "left": self.__left_sensor_last_scan.value,
            "right": self.__right_sensor_last_scan.value
	    }


    def is_front_clear(self):
        if self.__front_sensor_last_scan.value > MIN_FRONT_DISTANCE and \
            self.__left_sensor_last_scan.value > MIN_LEFT_DISTANCE and \
                self.__right_sensor_last_scan.value > MIN_RIGHT_DISTANCE:
            return True 
        
        return False


    def is_back_clear(self):
        if self.__rear_sensor_last_scan.value > MIN_BACK_DISTANCE:
            return True
        
        return False


# For testing purposes
if __name__ == "__main__":
    sensing_system = Sensing_system()

    while True:
        print(sensing_system.get_sensor_data())