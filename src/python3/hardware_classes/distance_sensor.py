import RPi.GPIO as GPIO
import time


DELAY = 0.01			# Seconds
SIGNAL_LENGTH = 0.00001 # Seconds


class Distance_sensor:
	def __init__(self, trig_pin, echo_pin):
		self.trig_pin = trig_pin
		self.echo_pin = echo_pin

		GPIO.setmode(GPIO.BCM)
		GPIO.setup(trig_pin, GPIO.OUT)
		GPIO.setup(echo_pin, GPIO.IN)


	def get_distance(self):
		GPIO.output(self.trig_pin, GPIO.LOW)
		time.sleep(DELAY)

		GPIO.output(self.trig_pin, GPIO.HIGH)
		time.sleep(SIGNAL_LENGTH)

		GPIO.output(self.trig_pin, GPIO.LOW)

		while GPIO.input(self.echo_pin) == 0:
			pulse_start = time.time()

		while GPIO.input(self.echo_pin) == 1:
			pulse_end = time.time()

		return round((pulse_end - pulse_start) * 17150, 2)
