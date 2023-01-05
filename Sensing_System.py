from time import sleep
from multiprocessing import Process, Value

from Distance_Sensor import Distance_Sensor

from Constants import Sensing_System_Constants


class Sensing_System:
    __front_sensor = None
    __rear_sensor = None
    __left_sensor = None
    __right_sensor = None

    __front_sensor_last_scan = Value('f', float(Sensing_System_Constants.MIN_FRONT_DISTANCE))
    __rear_sensor_last_scan = Value('f', float(Sensing_System_Constants.MIN_BACK_DISTANCE))
    __left_sensor_last_scan = Value('f', float(Sensing_System_Constants.MIN_LEFT_DISTANCE))
    __right_sensor_last_scan = Value('f', float(Sensing_System_Constants.MIN_RIGHT_DISTANCE))

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
            distance = self.__front_sensor.get_distance()

            if distance is not None:
                with self.__front_sensor_last_scan.get_lock():
                    self.__front_sensor_last_scan.value = distance
                    print("1", distance)


            distance = self.__rear_sensor.get_distance()

            if distance is not None:
                with self.__rear_sensor_last_scan.get_lock():
                    self.__rear_sensor_last_scan.value = distance
                    print("2", distance)


            distance = self.__left_sensor.get_distance()

            if distance is not None:
                with self.__left_sensor_last_scan.get_lock():
                    self.__left_sensor_last_scan.value = distance
                    print("3", distance)


            distance = self.__right_sensor.get_distance()

            if distance is not None:
                with self.__right_sensor_last_scan.get_lock():
                    self.__right_sensor_last_scan.value = distance
                    print("4", distance)


    def get_front_sensor_distance(self) -> float:
        with self.__front_sensor_last_scan.get_lock():
            return round(self.__front_sensor_last_scan.value, 1)


    def get_rear_sensor_distance(self) -> float:
        with self.__rear_sensor_last_scan.get_lock():
            return round(self.__rear_sensor_last_scan.value, 1)


    def get_left_sensor_distance(self) -> float:
        with self.__left_sensor_last_scan.get_lock():
            return round(self.__left_sensor_last_scan.value, 1)


    def get_right_sensor_distance(self) -> float:
        with self.__right_sensor_last_scan.get_lock():
            return round(self.__right_sensor_last_scan.value, 1)


    def get_sensor_data(self) -> dict:
        return {
            "front": round(self.__front_sensor_last_scan.value, 1),
            "rear": round(self.__rear_sensor_last_scan.value, 1),
            "left": round(self.__left_sensor_last_scan.value, 1),
            "right": round(self.__right_sensor_last_scan.value, 1)
	    }


    def is_front_clear(self) -> bool:
        if self.__front_sensor_last_scan.value > Sensing_System_Constants.MIN_FRONT_DISTANCE and \
           self.__left_sensor_last_scan.value > Sensing_System_Constants.MIN_LEFT_DISTANCE and \
           self.__right_sensor_last_scan.value > Sensing_System_Constants.MIN_RIGHT_DISTANCE:

            return True 
        
        return False


    def is_back_clear(self) -> bool:
        if self.__rear_sensor_last_scan.value > Sensing_System_Constants.MIN_BACK_DISTANCE:
            return True
        
        return False


# For testing purposes
if __name__ == "__main__":
    sensing_system = Sensing_System()

    while True:
        #print(sensing_system.get_sensor_data())
        print(sensing_system.get_front_sensor_distance(), \
              sensing_system.get_rear_sensor_distance(), \
              sensing_system.get_left_sensor_distance(), \
              sensing_system.get_right_sensor_distance())
