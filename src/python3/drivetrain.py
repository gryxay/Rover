import time
import RPi.GPIO as GPIO


SPR = 800       		# Signal pulses Per Revolution
DRIVING_DELAY = 0.0002	# Time between signal pulses when driving
TURNING_DELAY = 0.0005	# Time between signal pulses when turning


class Drivetrain:
	def __init__(self, dir_pin_1, step_pin_1, dir_pin_2, step_pin_2, sleep_pin):
		# Motor 1
		self.dir_pin_1 = dir_pin_1
		self.step_pin_1 = step_pin_1

		# Motor 2
		self.dir_pin_2 = dir_pin_2
		self.step_pin_2 = step_pin_2

		# Sleep pin
		self.sleep_pin = sleep_pin

		# GPIO setup
		GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(False)

		GPIO.setup(self.dir_pin_1, GPIO.OUT)
		GPIO.setup(self.step_pin_1, GPIO.OUT)
		GPIO.setup(self.dir_pin_2, GPIO.OUT)
		GPIO.setup(self.step_pin_2, GPIO.OUT)
		GPIO.setup(self.sleep_pin, GPIO.OUT)


	def rotate(self, direction):
		if direction == 'f':
			GPIO.output(self.dir_pin_1, GPIO.HIGH)
			GPIO.output(self.dir_pin_2, GPIO.HIGH)
		elif direction == 'b':
			GPIO.output(self.dir_pin_1, GPIO.LOW)
			GPIO.output(self.dir_pin_2, GPIO.LOW)

		GPIO.output(self.step_pin_1, GPIO.HIGH)
		GPIO.output(self.step_pin_2, GPIO.HIGH)
		time.sleep(DRIVING_DELAY)

		GPIO.output(self.step_pin_1, GPIO.LOW)
		GPIO.output(self.step_pin_2, GPIO.LOW)
		time.sleep(DRIVING_DELAY)


	def drive(self, direction, rotations):
		if direction == 'f':
			GPIO.output(self.dir_pin_1, GPIO.HIGH)
			GPIO.output(self.dir_pin_2, GPIO.HIGH)
		elif direction == 'b':
			GPIO.output(self.dir_pin_1, GPIO.LOW)
			GPIO.output(self.dir_pin_2, GPIO.LOW)
	
		for i in range(rotations * SPR):
			GPIO.output(self.step_pin_1, GPIO.HIGH)
			GPIO.output(self.step_pin_2, GPIO.HIGH)

			time.sleep(DRIVING_DELAY)

			GPIO.output(self.step_pin_1, GPIO.LOW)
			GPIO.output(self.step_pin_2, GPIO.LOW)
			
			time.sleep(DRIVING_DELAY)


	def turn(self, direction, rotations):
		if direction == 'l':
			GPIO.output(self.dir_pin_1, GPIO.LOW)
			GPIO.output(self.dir_pin_2, GPIO.HIGH)
		elif direction == 'r':
			GPIO.output(self.dir_pin_1, GPIO.HIGH)
			GPIO.output(self.dir_pin_2, GPIO.LOW)

		for i in range(int(SPR * rotations)):
			GPIO.output(self.step_pin_1, GPIO.HIGH)
			GPIO.output(self.step_pin_2, GPIO.HIGH)

			time.sleep(TURNING_DELAY)
			
			GPIO.output(self.step_pin_1, GPIO.LOW)
			GPIO.output(self.step_pin_2, GPIO.LOW)
			
			time.sleep(TURNING_DELAY)


	def toggle_power(self, is_on):
		GPIO.output(self.sleep_pin, is_on)
