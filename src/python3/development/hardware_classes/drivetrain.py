from imu import IMU
import RPi.GPIO as GPIO
from time import sleep


# Drivetrain constants
LEFT_MOTOR_DIR_PIN = 16
LEFT_MOTOR_STEP_PIN = 20
RIGHT_MOTOR_DIR_PIN = 19
RIGHT_MOTOR_STEP_PIN = 26
SLEEP_PIN = 21

SPR = 800       		# Signal pulses Per Revolution
DRIVING_DELAY = 0.0001	# Time between signal pulses when driving
TURNING_DELAY = 0.0005	# Time between signal pulses when turning


class Drivetrain:
	def __init__(self, dir_pin_1 = LEFT_MOTOR_DIR_PIN, step_pin_1 = LEFT_MOTOR_STEP_PIN, \
					dir_pin_2 = RIGHT_MOTOR_DIR_PIN, step_pin_2 = RIGHT_MOTOR_STEP_PIN, sleep_pin = SLEEP_PIN, imu_auto_calibrate = False, debug = False):
		self.__debug = debug

		# Left motor setup
		self.__dir_pin_1 = dir_pin_1
		self.__step_pin_1 = step_pin_1

		# Right motor setup
		self.__dir_pin_2 = dir_pin_2
		self.__step_pin_2 = step_pin_2

		# Sleep pin
		self.__sleep_pin = sleep_pin

		# GPIO setup
		GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BCM)

		GPIO.setup(self.__dir_pin_1, GPIO.OUT)
		GPIO.setup(self.__step_pin_1, GPIO.OUT)
		GPIO.setup(self.__dir_pin_2, GPIO.OUT)
		GPIO.setup(self.__step_pin_2, GPIO.OUT)
		GPIO.setup(self.__sleep_pin, GPIO.OUT)

		self.__imu = IMU(auto_calibrate = imu_auto_calibrate, debug = debug)


	def rotate(self, direction):
		if direction == 'f':
			GPIO.output(self.__dir_pin_1, GPIO.HIGH)
			GPIO.output(self.__dir_pin_2, GPIO.HIGH)
		elif direction == 'b':
			GPIO.output(self.__dir_pin_1, GPIO.LOW)
			GPIO.output(self.__dir_pin_2, GPIO.LOW)

		GPIO.output(self.__step_pin_1, GPIO.HIGH)
		GPIO.output(self.__step_pin_2, GPIO.HIGH)
		sleep(DRIVING_DELAY)

		GPIO.output(self.__step_pin_1, GPIO.LOW)
		GPIO.output(self.__step_pin_2, GPIO.LOW)
		sleep(DRIVING_DELAY)


	def drive(self, direction, rotations):
		if direction == 'f':
			GPIO.output(self.__dir_pin_1, GPIO.HIGH)
			GPIO.output(self.__dir_pin_2, GPIO.HIGH)
		elif direction == 'b':
			GPIO.output(self.__dir_pin_1, GPIO.LOW)
			GPIO.output(self.__dir_pin_2, GPIO.LOW)
	
		for i in range(rotations * SPR):
			GPIO.output(self.__step_pin_1, GPIO.HIGH)
			GPIO.output(self.__step_pin_2, GPIO.HIGH)

			sleep(DRIVING_DELAY)

			GPIO.output(self.__step_pin_1, GPIO.LOW)
			GPIO.output(self.__step_pin_2, GPIO.LOW)
			
			sleep(DRIVING_DELAY)


	# Works for turns up to 360 degrees
	def turn(self, direction, degrees):
		turning_offset = (degrees % 360.0) / 30

		if direction == 'l':
			GPIO.output(self.__dir_pin_1, GPIO.LOW)
			GPIO.output(self.__dir_pin_2, GPIO.HIGH)

			final_orientation = self.__imu.get_yaw_value() - degrees % 360.0
			turning_offset *= -1

			if final_orientation < 0:
				final_orientation = 360.0 + final_orientation

		elif direction == 'r':
			GPIO.output(self.__dir_pin_1, GPIO.HIGH)
			GPIO.output(self.__dir_pin_2, GPIO.LOW)

			final_orientation = (self.__imu.get_yaw_value() + degrees % 360.0) % 360.0

		while round(self.__imu.get_yaw_value(), 0) != round(final_orientation - turning_offset, 0):
			GPIO.output(self.__step_pin_1, GPIO.HIGH)
			GPIO.output(self.__step_pin_2, GPIO.HIGH)

			sleep(TURNING_DELAY)
			
			GPIO.output(self.__step_pin_1, GPIO.LOW)
			GPIO.output(self.__step_pin_2, GPIO.LOW)
			
			sleep(TURNING_DELAY)


	def toggle_power(self, is_on):
		GPIO.output(self.__sleep_pin, is_on)
