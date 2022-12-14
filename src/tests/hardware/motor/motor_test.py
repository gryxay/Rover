from time import sleep
import RPi.GPIO as GPIO

DIR = 21   # Direction GPIO Pin
STEP = 20  # Step GPIO Pin
CW = 1     # Clockwise Rotation
CCW = 0    # Counterclockwise Rotation

GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(STEP, GPIO.OUT)
GPIO.output(DIR, CW)

delay = .0005

try:
	while True:
		GPIO.output(STEP, GPIO.HIGH)
		sleep(delay)
		GPIO.output(STEP, GPIO.LOW)
		sleep(delay)

except KeyboardInterrupt:
	GPIO.cleanup()
	print("\nGPIO pins are reset!")
