import RPi.GPIO as GPIO
from time import sleep, time

from Constants import Distance_Sensor_Constants


class Distance_Sensor:
	def __init__(self, trig_pin, echo_pin):
		self.__trig_pin = trig_pin
		self.__echo_pin = echo_pin

		GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(trig_pin, GPIO.OUT)
		GPIO.setup(echo_pin, GPIO.IN)


	# Returns distance in cm (sensor <-> object)
	def get_distance(self) -> float or None:
		pulse_start = None
		pulse_end = None


		GPIO.output(self.__trig_pin, GPIO.LOW)
		sleep(Distance_Sensor_Constants.DELAY)

		GPIO.output(self.__trig_pin, GPIO.HIGH)
		sleep(Distance_Sensor_Constants.SIGNAL_LENGTH)

		GPIO.output(self.__trig_pin, GPIO.LOW)


		loop_start = time()

		while GPIO.input(self.__echo_pin) == 0:
			pulse_start = time()

			# Prevents infinite while loop, that can cause Sensing_System to fail
			if pulse_start - loop_start > Distance_Sensor_Constants.TIMEOUT:
				return None


		if pulse_start is None:
			return None


		while GPIO.input(self.__echo_pin) == 1:
			pulse_end = time()

			# Prevents infinite while loop, that can cause Sensing_System to fail
			if pulse_end - pulse_start > Distance_Sensor_Constants.TIMEOUT:
				return None


		if pulse_end is None:
			return None


		return (pulse_end - pulse_start) * Distance_Sensor_Constants.HALF_SPEED_OF_SOUND
