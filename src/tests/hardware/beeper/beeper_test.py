import RPi.GPIO as GPIO
import time


beeper_gpio_pin = 17
beeps = 10

GPIO.setmode(GPIO.BCM)
GPIO.setup(beeper_gpio_pin, GPIO.OUT)

for i in range(beeps):
	GPIO.output(beeper_gpio_pin, GPIO.LOW)
	time.sleep(0.5)

	GPIO.output(beeper_gpio_pin, GPIO.HIGH)
	time.sleep(0.5)


GPIO.cleanup()
