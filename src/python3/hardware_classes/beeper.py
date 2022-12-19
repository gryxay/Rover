import RPi.GPIO as GPIO
import time


TRIG_PIN = 5


class Beeper:
	def __init__(self, trig_pin = TRIG_PIN, debug = False):
		self.trig_pin = trig_pin

		GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(debug)
		GPIO.setup(self.trig_pin, GPIO.OUT)

		# Prevent constant beeping after initialization
		GPIO.output(self.trig_pin, GPIO.HIGH)


	def beep(self, count, delay):
		for i in range(count):
			GPIO.output(self.trig_pin, GPIO.LOW)
			time.sleep(delay)

			GPIO.output(self.trig_pin, GPIO.HIGH)
			time.sleep(delay)
