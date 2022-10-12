import RPi.GPIO as GPIO
import time
from motor import Motor
from distance_sensor import Sensor
from beeper import Beeper


motor_1 = Motor(14, 15)
motor_2 = Motor(23, 24)
sensor = Sensor(16, 12)
beeper = Beeper(5)


# Beeper test

beeper.beep(3, 0.1)

# Motor test

motor_1.rotate(3, 1)
motor_2.rotate(3, 1)

time.sleep(1)

motor_1.rotate(3, 0)
motor_2.rotate(3, 0)

# Distance sensor test

for i in range(10):
        beeper.beep(1, 0.3)
        print(sensor.get_distance(), " cm")

# Clear GPIO settings

GPIO.cleanup()