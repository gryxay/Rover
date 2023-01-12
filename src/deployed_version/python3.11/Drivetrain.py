import RPi.GPIO as GPIO
from time import sleep

from Constants import Drivetrain_Constants


class Drivetrain:
	def __init__(self, left_motor_dir_pin = Drivetrain_Constants.LEFT_MOTOR_DIR_PIN, \
				 	   left_motor_step_pin = Drivetrain_Constants.LEFT_MOTOR_STEP_PIN, \
					   right_motor_dir_pin = Drivetrain_Constants.RIGHT_MOTOR_DIR_PIN, \
					   right_motor_step_pin = Drivetrain_Constants.RIGHT_MOTOR_STEP_PIN, \
					   sleep_pin = Drivetrain_Constants.SLEEP_PIN, \
					   imu = None, \
					   debug = False):
		
		self.__debug = debug

		if self.__debug and imu:
			print("Drivetrain: Adding the IMU")

		self.__imu = imu

		if self.__debug:
			print("Drivetrain: Setting up GPIO pins")

		self.__left_motor_dir_pin = left_motor_dir_pin
		self.__left_motor_step_pin = left_motor_step_pin

		self.__right_motor_dir_pin = right_motor_dir_pin
		self.__right_motor_step_pin = right_motor_step_pin

		self.__sleep_pin = sleep_pin

		# GPIO setup
		GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BCM)

		GPIO.setup(self.__left_motor_dir_pin, GPIO.OUT)
		GPIO.setup(self.__left_motor_step_pin, GPIO.OUT)
		GPIO.setup(self.__right_motor_dir_pin, GPIO.OUT)
		GPIO.setup(self.__right_motor_step_pin, GPIO.OUT)
		GPIO.setup(self.__sleep_pin, GPIO.OUT)


	# Returns delay in seconds between signal pulses
	def get_delay(self, speed) -> float:
		if speed == "fast":
			return Drivetrain_Constants.FAST_DRIVING_DELAY

		elif speed == "slow":
			return Drivetrain_Constants.SLOW_DRIVING_DELAY

		elif speed == "turning":
			return Drivetrain_Constants.TURNING_DELAY

	
	# Sets the direction for motors
	def set_direction(self, direction):
		if direction == 'f':
			GPIO.output(self.__left_motor_dir_pin, GPIO.HIGH)
			GPIO.output(self.__right_motor_dir_pin, GPIO.HIGH)

		elif direction == 'b':
			GPIO.output(self.__left_motor_dir_pin, GPIO.LOW)
			GPIO.output(self.__right_motor_dir_pin, GPIO.LOW)

		elif direction == 'l':
			GPIO.output(self.__left_motor_dir_pin, GPIO.LOW)
			GPIO.output(self.__right_motor_dir_pin, GPIO.HIGH)

		elif direction == 'r':
			GPIO.output(self.__left_motor_dir_pin, GPIO.HIGH)
			GPIO.output(self.__right_motor_dir_pin, GPIO.LOW)


	# Rotates both motors one step
	def rotate_one_step(self, delay):
		GPIO.output(self.__left_motor_step_pin, GPIO.HIGH)
		GPIO.output(self.__right_motor_step_pin, GPIO.HIGH)
		sleep(delay)

		GPIO.output(self.__left_motor_step_pin, GPIO.LOW)
		GPIO.output(self.__right_motor_step_pin, GPIO.LOW)
		sleep(delay)


	# Moves the robot a specified amount of CM
	def drive(self, direction, distance_cm, speed):
		delay = self.get_delay(speed)

		self.set_direction(direction)

		for _ in range(round(distance_cm * Drivetrain_Constants.CM)):
			self.rotate_one_step(delay)


	# Turns the robot to the specified direction a tiny bit
	# Is used for adjusting the robots orientation
	def micro_turn(self, direction):
		delay = self.get_delay("turning")

		self.set_direction(direction)
		
		for _ in range(Drivetrain_Constants.MICRO_TURN_STEPS):
			self.rotate_one_step(delay)


	# Turns the robot to the specified direction certain amount of degrees
	# Works for turns up to 360 degrees
	def turn(self, direction, degrees):
		if self.__imu:
			final_orientation = None
			turning_offset = (degrees % 360.0) / Drivetrain_Constants.OFFSET
			delay = self.get_delay("turning")

			if direction == 'l':
				final_orientation = self.__imu.get_yaw_value() - degrees % 360.0
				turning_offset *= -1

				if final_orientation < 0:
					final_orientation = 360.0 + final_orientation

			elif direction == 'r':
				final_orientation = (self.__imu.get_yaw_value() + degrees % 360.0) % 360.0

			self.set_direction(direction)

			while round(self.__imu.get_yaw_value()) != round(final_orientation - turning_offset):
				self.rotate_one_step(delay)

		else:
			if self.__debug:
				print("Drivetrain: IMU is missing!")


	# Turns the robot 90 degrees and adjusts drifting 
	def strict_turn(self, direction):
		if direction == 'l':
			self.drive('f', Drivetrain_Constants.LEFT_STRICT_TURN_FORWARD_OFFSET, "slow")

		elif direction == 'r':
			self.drive('f', Drivetrain_Constants.RIGHT_STRICT_TURN_FORWARD_OFFSET, "slow")

		self.turn(direction, Drivetrain_Constants.STRICT_TURN_TURNING_ANGLE)

		if direction == 'l':
			self.drive('b', Drivetrain_Constants.LEFT_STRICT_TURN_BACKWARD_OFFSET, "slow")

		elif direction == 'r':
			self.drive('b', Drivetrain_Constants.RIGHT_STRICT_TURN_BACKWARD_OFFSET, "slow")


	# Turns motors and their controllers ON/OFF
	# Saves battery life
	def toggle_power(self, is_on):
		GPIO.output(self.__sleep_pin, is_on)
		
