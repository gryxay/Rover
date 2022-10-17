import RPi.GPIO as GPIO
import time
from motor import Motor
from distance_sensor import Sensor
from beeper import Beeper


motor_1 = Motor(15, 14)
motor_2 = Motor(20, 16)

sensor_1 = Sensor(7, 24)
sensor_2 = Sensor(25, 8)
sensor_3 = Sensor(12, 19)
sensor_4 = Sensor(21, 26)

beeper = Beeper(5)


# Beeper test

beeper.beep(3, 0.1)

# Motor test

motor_1.rotate(5, 1)
motor_2.rotate(5, 1)

time.sleep(1)

motor_1.rotate(5, 0)
motor_2.rotate(5, 0)

# Distance sensor test

for i in range(30):
	print("Sensor_1: ", sensor_1.get_distance(), " cm")
	print("Sensor_2: ", sensor_2.get_distance(), " cm")
	print("Sensor_3: ", sensor_3.get_distance(), " cm")
	print("Sensor_4: ", sensor_4.get_distance(), " cm")

# Clear GPIO settings

GPIO.cleanup()
