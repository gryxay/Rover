from time import sleep
import RPi.GPIO as GPIO


SPR = 800       # Signal pulses Per Revolution
DELAY = 0.0004  # Time between signal pulses


GPIO.setwarnings(False)


class Drivetrain:
	def __init__(self, dir_pin_1, step_pin_1, dir_pin_2, step_pin_2):

		# Motor 1

		self.dir_pin_1 = dir_pin_1
		self.step_pin_1 = step_pin_1

		# Motor 2

		self.dir_pin_2 = dir_pin_2
		self.step_pin_2 = step_pin_2

		# GPIO setup

		GPIO.setmode(GPIO.BCM)

		GPIO.setup(self.dir_pin_1, GPIO.OUT)
		GPIO.setup(self.step_pin_1, GPIO.OUT)
		GPIO.setup(self.dir_pin_2, GPIO.OUT)
		GPIO.setup(self.step_pin_2, GPIO.OUT)


	# Direction == 1 || 0; 1 = forward; 0 = backward;

	def rotate(self, rotations, direction):
		GPIO.output(self.dir_pin_1, direction)
		GPIO.output(self.dir_pin_2, direction)

		for i in range(int(SPR * rotations)):
			GPIO.output(self.step_pin_1, GPIO.HIGH)
			GPIO.output(self.step_pin_2, GPIO.HIGH)
			sleep(DELAY)

			GPIO.output(self.step_pin_1, GPIO.LOW)
			GPIO.output(self.step_pin_2, GPIO.LOW)
			sleep(DELAY)


	def turn_left(self, rotations):
		GPIO.output(self.dir_pin_1, 0)
		GPIO.output(self.dir_pin_2, 1)

		for i in range(int(SPR * rotations)):
			GPIO.output(self.step_pin_1, GPIO.HIGH)
			GPIO.output(self.step_pin_2, GPIO.HIGH)
			sleep(DELAY)

			GPIO.output(self.step_pin_1, GPIO.LOW)
			GPIO.output(self.step_pin_2, GPIO.LOW)
			sleep(DELAY)


	def turn_right(self, rotations):
		GPIO.output(self.dir_pin_1, 1)
		GPIO.output(self.dir_pin_2, 0)

		for i in range(int(SPR * rotations)):
			GPIO.output(self.step_pin_1, GPIO.HIGH)
			GPIO.output(self.step_pin_2, GPIO.HIGH)
			sleep(DELAY)

			GPIO.output(self.step_pin_1, GPIO.LOW)
			GPIO.output(self.step_pin_2, GPIO.LOW)
			sleep(DELAY)


if __name__ == '__main__':

	drivetrain = Drivetrain(15, 14, 20, 16)

	drivetrain.rotate(20, 1)
	sleep(1)
	drivetrain.turn_left(10)
	sleep(1)
	drivetrain.turn_right(10)
