import RPi.GPIO as GPIO
import time


class Beeper:
	def __init__(self, trig_pin):
		self.trig_pin = trig_pin

		GPIO.setmode(GPIO.BCM)
		GPIO.setup(self.trig_pin, GPIO.OUT)

	def beep(self, count, delay):
		for i in range(count):
			GPIO.output(self.trig_pin, GPIO.LOW)
			time.sleep(delay)

			GPIO.output(self.trig_pin, GPIO.HIGH)
			time.sleep(delay)