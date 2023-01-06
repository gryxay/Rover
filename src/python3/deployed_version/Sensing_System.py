from multiprocessing import Process, Value

from Distance_Sensor import Distance_Sensor

from Constants import Sensing_System_Constants
from Constants import Robot_Constants

#
from time import time, sleep


class Sensing_System:
    __sensors = {}

    __sensor_data = {
        'f': Value('f', float(Sensing_System_Constants.MIN_FRONT_DISTANCE + 1)),
        'b': Value('f', float(Sensing_System_Constants.MIN_BACK_DISTANCE + 1)),
        'l': Value('f', float(Sensing_System_Constants.MIN_LEFT_DISTANCE + 1)),
        'r': Value('f', float(Sensing_System_Constants.MIN_RIGHT_DISTANCE + 1))
    }

    __background_process = None


    def __init__(self, front_sensor_trig_pin = Sensing_System_Constants.FRONT_SENSOR_TRIG_PIN, \
                       front_sensor_echo_pin = Sensing_System_Constants.FRONT_SENSOR_ECHO_PIN, \
                       rear_sensor_trig_pin = Sensing_System_Constants.REAR_SENSOR_TRIG_PIN, \
                       rear_sensor_echo_pin = Sensing_System_Constants.REAR_SENSOR_ECHO_PIN, \
                       left_sensor_trig_pin = Sensing_System_Constants.LEFT_SENSOR_TRIG_PIN, \
                       left_sensor_echo_pin = Sensing_System_Constants.LEFT_SENSOR_ECHO_PIN, \
                       right_sensor_trig_pin = Sensing_System_Constants.RIGHT_SENSOR_TRIG_PIN, \
                       right_sensor_echo_pin = Sensing_System_Constants.RIGHT_SENSOR_ECHO_PIN):

        self.__sensors['f'] = Distance_Sensor(front_sensor_trig_pin, front_sensor_echo_pin)
        self.__sensors['b'] = Distance_Sensor(rear_sensor_trig_pin, rear_sensor_echo_pin)
        self.__sensors['l'] = Distance_Sensor(left_sensor_trig_pin, left_sensor_echo_pin)
        self.__sensors['r'] = Distance_Sensor(right_sensor_trig_pin, right_sensor_echo_pin)

        # Start a process, that constantly updates distance sensor in the background
        self.__background_process = Process(target = self.__update_sensor_data)
        self.__background_process.start()


    def __update_sensor_data(self):
        while True:
            for direction in Robot_Constants.DIRECTIONS:
                distance = self.__sensors[direction].get_distance()

                if distance is not None:
                    with self.__sensor_data[direction].get_lock():
                        self.__sensor_data[direction].value = distance


    def get_front_sensor_distance(self) -> float:
        with self.__sensor_data['f'].get_lock():
            return self.__sensor_data['f'].value


    def get_rear_sensor_distance(self) -> float:
        with self.__sensor_data['b'].get_lock():
            return self.__sensor_data['b'].value


    def get_left_sensor_distance(self) -> float:
        with self.__sensor_data['l'].get_lock():
            return self.__sensor_data['l'].value


    def get_right_sensor_distance(self) -> float:
        with self.__sensor_data['r'].get_lock():
            return self.__sensor_data['r'].value


    def get_sensor_data(self) -> dict:
        return {
            'f': self.get_front_sensor_distance(),
            'b': self.get_rear_sensor_distance(),
            'l': self.get_left_sensor_distance(),
            'r': self.get_right_sensor_distance()
	    }


    def is_front_clear(self) -> bool:
        if self.get_front_sensor_distance() > Sensing_System_Constants.MIN_FRONT_DISTANCE and \
           self.get_left_sensor_distance() > Sensing_System_Constants.MIN_LEFT_DISTANCE and \
           self.get_right_sensor_distance() > Sensing_System_Constants.MIN_RIGHT_DISTANCE:

            return True 
        
        return False


    def is_back_clear(self) -> bool:
        if self.get_rear_sensor_distance() > Sensing_System_Constants.MIN_BACK_DISTANCE:
            return True
        
        return False


# For testing purposes
if __name__ == "__main__":
    sensing_system = Sensing_System()

    starting_time = time()
    count = 0

    try:
        while True:
            count += 1
            print(sensing_system.get_sensor_data())
            print("Execution length: ", time() - starting_time)
            #sleep(0.001)

    except:
        print("Execution length: ", time() - starting_time)
        print("Count: ", count)