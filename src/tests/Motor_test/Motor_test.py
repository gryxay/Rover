import RPi.GPIO as GPIO
from time import sleep

from Motor_Constants import Motor_Constants


def setup_GPIO_pins():
	GPIO.setmode(GPIO.BCM)

	GPIO.setup(Motor_Constants.DIR_PIN, GPIO.OUT)
	GPIO.setup(Motor_Constants.STEP_PIN, GPIO.OUT)
	GPIO.setup(Motor_Constants.SLEEP_PIN, GPIO.OUT)

	GPIO.output(Motor_Constants.STEP_PIN, GPIO.HIGH)


def rotate(motor, direction, rotations, delay):
	if motor == "l":
		dir_pin = Motor_Constants.LEFT_MOTOR_DIR_PIN
		step_pin = Motor_Constants.LEFT_MOTOR_STEP_PIN

	elif motor == 'r':
		dir_pin = Motor_Constants.RIGHT_MOTOR_DIR_PIN
		step_pin = Motor_Constants.RIGHT_MOTOR_STEP_PIN


	GPIO.output(dir_pin, direction)

	for pulse in range(rotations * Motor_Constants.SPR):
		GPIO.output(step_pin, GPIO.HIGH)
		sleep(delay)

		GPIO.output(step_pin, GPIO.LOW)
		sleep(delay)


def low_speed_test(motor) -> list:
	passed_tests = 0

	print("< 1. Low speed tests [2]")
	print("< You will have to track the rotation of the motor shaft.")

	print("< [1/2] Press enter when you are ready.", end = " ")
	input()

	rotate(motor, Motor_Constants.CW, Motor_Constants.SLOW_TEST_ROTATIONS, Motor_Constants.SLOW_TEST_DELAY)
	
	print("Did the motor rotate 3 time in a clockwise direction? [y/n]")
	answer = input("> ")

	if answer == "y":
		passed_tests += 1


	print("< [2/2] Press enter when you are ready.", end = " ")
	input()

	rotate(motor, Motor_Constants.CCW, Motor_Constants.SLOW_TEST_ROTATIONS, Motor_Constants.SLOW_TEST_DELAY)
	
	print("Did the motor rotate 3 time in a counter-clockwise direction? [y/n]")
	answer = input("> ")

	if answer == "y":
		passed_tests += 1

	return [passed_tests, 2]


def high_speed_test(motor) -> list:
	passed_tests = 0

	print("< 2. High speed tests [2]")
	print("< You will have to keep track of the motor's speed, direction and any unwanted sounds.")

	print("< [1/2] Press enter when you are ready.", end = " ")
	input()

	rotate(motor, Motor_Constants.CW, Motor_Constants.FAST_TEST_ROTATIONS, Motor_Constants.FAST_TEST_DELAY)
	
	print("Did the motor spin in a constant speed and didn't make any unwanted sounds " + \
		  "while turning in a clockwise direction? [y/n]")
	answer = input("> ")

	if answer == "y":
		passed_tests += 1


	print("< [2/2] Press enter when you are ready.", end = " ")
	input()

	rotate(motor, Motor_Constants.CCW, Motor_Constants.FAST_TEST_ROTATIONS, Motor_Constants.FAST_TEST_DELAY)
	
	print("Did the motor spin in a constant speed and didn't make any unwanted sounds " + \
		  "while turning in a counter-clockwise direction? [y/n]")
	answer = input("> ")

	if answer == "y":
		passed_tests += 1

	return [passed_tests, 2]
 

if __name__ == "__main__":
	passed_tests = 0
	total_tests = 0


	motor = input("< Select which motor do you want to test [l (left) / r (right)]: ")


	# Turning on the motor controller
	GPIO.output(Motor_Constants.SLEEP_PIN, GPIO.LOW)


	passes, tests = low_speed_test(motor)
	passed_tests += passes
	total_tests += tests


	passes, tests = high_speed_test(motor)
	passed_tests += passes
	total_tests += tests


	# Turning off the motor controller
	GPIO.output(Motor_Constants.SLEEP_PIN, GPIO.LOW)


	print("Total tests passed: [" + str(passed_tests) + "/" + str(total_tests) + "]")
