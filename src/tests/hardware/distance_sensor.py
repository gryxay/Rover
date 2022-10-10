import RPi.GPIO as GPIO
import time


trigger_gpio_pin = 14
echo_gpio_pin = 15


GPIO.setmode(GPIO.BCM)
GPIO.setup(trigger_gpio_pin, GPIO.OUT)
GPIO.setup(echo_gpio_pin, GPIO.IN)

try:
	while True:
		GPIO.output(trigger_gpio_pin, GPIO.LOW)
		time.sleep(0.5)
		GPIO.output(trigger_gpio_pin, GPIO.HIGH)
		time.sleep(0.00001)
		GPIO.output(trigger_gpio_pin, GPIO.LOW)

		while GPIO.input(echo_gpio_pin) == 0:
			pulse_start = time.time()

		while GPIO.input(echo_gpio_pin) == 1:
			pulse_end = time.time()

		pulse_duration = pulse_end - pulse_start
		distance = pulse_duration * 17150
		distance = round(distance, 2)

		print("Distance: ", distance, "cm")

except KeyboardInterrupt:
	GPIO.cleanup()
	print("\nGPIO pins are reset!")