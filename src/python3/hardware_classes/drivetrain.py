import RPi.GPIO as GPIO
from multiprocessing import Process, Value
from time import sleep
from math import floor, ceil

from MPU6050 import MPU6050


# Drivetrain constants
LEFT_MOTOR_DIR_PIN = 16
LEFT_MOTOR_STEP_PIN = 20
RIGHT_MOTOR_DIR_PIN = 19
RIGHT_MOTOR_STEP_PIN = 26
SLEEP_PIN = 21

SPR = 800       		# Signal pulses Per Revolution
DRIVING_DELAY = 0.0001	# Time between signal pulses when driving
TURNING_DELAY = 0.0005	# Time between signal pulses when turning

# MPU6050 constants
I2C_BUS = 1
DEVICE_ADDRESS = 0x68

X_ACCEL_OFFSET = -1803
Y_ACCEL_OFFSET = -2956
Z_ACCEL_OFFSET = -396
X_GYRO_OFFSET = -58
Y_GYRO_OFFSET = 72
Z_GYRO_OFFSET = -23

ENABLE_DEBUG_OUTPUT = False


class Drivetrain:
	def __init__(self, dir_pin_1 = LEFT_MOTOR_DIR_PIN, step_pin_1 = LEFT_MOTOR_STEP_PIN, \
					dir_pin_2 = RIGHT_MOTOR_DIR_PIN, step_pin_2 = RIGHT_MOTOR_STEP_PIN, sleep_pin = SLEEP_PIN):
		# Left motor setup
		self.dir_pin_1 = dir_pin_1
		self.step_pin_1 = step_pin_1

		# Right motor setup
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

		# Accelerometer / gyroscope setup
		self.mpu = MPU6050(I2C_BUS, DEVICE_ADDRESS, X_ACCEL_OFFSET, Y_ACCEL_OFFSET, Z_ACCEL_OFFSET, \
						X_GYRO_OFFSET, Y_GYRO_OFFSET, Z_GYRO_OFFSET, ENABLE_DEBUG_OUTPUT)
		self.mpu.dmp_initialize()
		self.mpu.set_DMP_enabled(True)

		# Rotation around z axis in degrees
		self.yaw = Value('f', 0.0)
		
		# Start a process, that constantly updates yaw data in the background
		Process(target = self.update_yaw_data).start()

		# Wait for yaw data to stabilize
		print("Setting up the positioning system...")
		sleep(20)


	def rotate(self, direction):
		if direction == 'f':
			GPIO.output(self.dir_pin_1, GPIO.HIGH)
			GPIO.output(self.dir_pin_2, GPIO.HIGH)
		elif direction == 'b':
			GPIO.output(self.dir_pin_1, GPIO.LOW)
			GPIO.output(self.dir_pin_2, GPIO.LOW)

		GPIO.output(self.step_pin_1, GPIO.HIGH)
		GPIO.output(self.step_pin_2, GPIO.HIGH)
		sleep(DRIVING_DELAY)

		GPIO.output(self.step_pin_1, GPIO.LOW)
		GPIO.output(self.step_pin_2, GPIO.LOW)
		sleep(DRIVING_DELAY)


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

			sleep(DRIVING_DELAY)

			GPIO.output(self.step_pin_1, GPIO.LOW)
			GPIO.output(self.step_pin_2, GPIO.LOW)
			
			sleep(DRIVING_DELAY)


	# Works for turns up to 360 degrees
	def turn(self, direction, degrees):
		turning_offset = (degrees % 360.0) / 60

		if direction == 'l':
			GPIO.output(self.dir_pin_1, GPIO.LOW)
			GPIO.output(self.dir_pin_2, GPIO.HIGH)

			final_orientation = self.yaw.value - degrees % 360.0
			turning_offset *= -1

			if final_orientation < 0:
				final_orientation = 360.0 + final_orientation

		elif direction == 'r':
			GPIO.output(self.dir_pin_1, GPIO.HIGH)
			GPIO.output(self.dir_pin_2, GPIO.LOW)

			final_orientation = (self.yaw.value + degrees % 360.0) % 360.0

		while floor(self.yaw.value) != floor(final_orientation - turning_offset):
			GPIO.output(self.step_pin_1, GPIO.HIGH)
			GPIO.output(self.step_pin_2, GPIO.HIGH)

			sleep(TURNING_DELAY)
			
			GPIO.output(self.step_pin_1, GPIO.LOW)
			GPIO.output(self.step_pin_2, GPIO.LOW)
			
			sleep(TURNING_DELAY)


	def toggle_power(self, is_on):
		GPIO.output(self.sleep_pin, is_on)


	def update_yaw_data(self):
		mpu_int_status = self.mpu.get_int_status()
		packet_size = self.mpu.DMP_get_FIFO_packet_size()
		FIFO_count = self.mpu.get_FIFO_count()
		FIFO_buffer = [0]*64
		FIFO_count_list = list()

		while True:
			FIFO_count = self.mpu.get_FIFO_count()
			mpu_int_status = self.mpu.get_int_status()

			# If overflow is detected by status or fifo count we want to reset
			if (FIFO_count == 1024) or (mpu_int_status & 0x10):
				self.mpu.reset_FIFO()
			# Check if fifo data is ready
			elif (mpu_int_status & 0x02):
				while FIFO_count < packet_size:
					FIFO_count = self.mpu.get_FIFO_count()

				FIFO_buffer = self.mpu.get_FIFO_bytes(packet_size)
				accel = self.mpu.DMP_get_acceleration_int16(FIFO_buffer)
				quat = self.mpu.DMP_get_quaternion_int16(FIFO_buffer)
				grav = self.mpu.DMP_get_gravity(quat)

				self.yaw.value = self.mpu.DMP_get_euler_roll_pitch_yaw(quat, grav).z
