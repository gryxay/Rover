import RPi.GPIO as GPIO
import time

from Constants import Beeper_Constants


class Beeper:
	__trig_pin = None

	
	def __init__(self, trig_pin = Beeper_Constants.TRIG_PIN):
		self.__trig_pin = trig_pin

		GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(self.__trig_pin, GPIO.OUT)

		# Prevent constant beeping after initialization
		GPIO.output(self.__trig_pin, GPIO.HIGH)


	def beep(self, count, delay):
		for i in range(count):
			GPIO.output(self.__trig_pin, GPIO.LOW)
			time.sleep(delay)

			GPIO.output(self.__trig_pin, GPIO.HIGH)
			time.sleep(delay)
