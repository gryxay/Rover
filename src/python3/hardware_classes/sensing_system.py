from multiprocessing import Process, Value
from distance_sensor import Distance_sensor


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
        self.front_sensor = Distance_sensor(front_sensor_trig_pin, front_sensor_echo_pin)
        self.rear_sensor = Distance_sensor(rear_sensor_trig_pin, rear_sensor_echo_pin)
        self.left_sensor = Distance_sensor(left_sensor_trig_pin, left_sensor_echo_pin)
        self.right_sensor = Distance_sensor(right_sensor_trig_pin, right_sensor_echo_pin)

        self.front_sensor_last_scan = Value('f', 0.0)
        self.rear_sensor_last_scan = Value('f', 0.0)
        self.left_sensor_last_scan = Value('f', 0.0)
        self.right_sensor_last_scan = Value('f', 0.0)

        # Start a process, that constantly updates distance sensor in the background
        Process(target = self.update_sensor_data).start()


    def update_sensor_data(self):
        while True:
            self.front_sensor_last_scan.value = self.front_sensor.get_distance()
            self.rear_sensor_last_scan.value = self.rear_sensor.get_distance()
            self.left_sensor_last_scan.value = self.left_sensor.get_distance()
            self.right_sensor_last_scan.value = self.right_sensor.get_distance()


    def get_sensor_data(self):
        return {
            "front": self.front_sensor_last_scan.value,
            "rear": self.rear_sensor_last_scan.value,
            "left": self.left_sensor_last_scan.value,
            "right": self.right_sensor_last_scan.value
	    }


    def get_front_sensor_distance(self):
        return self.front_sensor_last_scan.value


    def get_rear_sensor_distance(self):
        return self.rear_sensor_last_scan.value


    def get_left_sensor_distance(self):
        return self.left_sensor_last_scan.value


    def get_right_sensor_distance(self):
        return self.right_sensor_last_scan.value
