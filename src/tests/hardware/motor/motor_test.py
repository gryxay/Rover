import RPi.GPIO as GPIO

from time import sleep


DIR_PIN = 16   	# Direction GPIO Pin
STEP_PIN = 20	# Step GPIO Pin
CW = 1     	# Clockwise Rotation
CCW = 0    	# Counterclockwise Rotation
SPR = 800	# Signal pulses per revolution

SLOW_TEST_DELAY = .001	# Time between signal pulses
SLOW_TEST_ROTATIONS = 3	# Times that the motor shaft turns

FAST_TEST_DELAY = .001	# Time between signal pulses
FAST_TEST_ROTATIONS = 50	# Times that the motor shaft turns


def rotate(direction, rotations, delay):
		GPIO.output(DIR_PIN, direction)
	
		for pulse in range(rotations * SPR):
			GPIO.output(STEP_PIN, GPIO.HIGH)
			sleep(delay)

			GPIO.output(STEP_PIN, GPIO.LOW)
			sleep(delay)


if __name__ == "__main__":
	# GPIO setup
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(DIR, GPIO.OUT)
	GPIO.setup(STEP, GPIO.OUT)

	# Motor test 1. Clockwise direction. Low speed.
	rotate(CW, SLOW_TEST_ROTATIONS, SLOW_TEST_DELAY)

	# Motor test 2. Counterclockwise direction. Low speed.
	rotate(CCW, SLOW_TEST_ROTATIONS, SLOW_TEST_DELAY)

	# Motor test 3. Clockwise direction. High speed.
	rotate(CW, FAST_TEST_ROTATIONS, FAST_TEST_DELAY)

	# Motor test 4. Counterclockwise direction. High speed.
	rotate(CCW, FAST_TEST_ROTATIONS, FAST_TEST_DELAY)
