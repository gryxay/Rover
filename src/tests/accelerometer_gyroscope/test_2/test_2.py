from MPU6050 import MPU6050


I2C_BUS = 1
DEVICE_ADDRESS = 0x68

# The offsets are different for each device and should be changed accordingly using a calibration procedure
X_ACCEL_OFFSET = -1803
Y_ACCEL_OFFSET = -2956
Z_ACCEL_OFFSET = -396

X_GYRO_OFFSET = -58
Y_GYRO_OFFSET = 72
Z_GYRO_OFFSET = -23

ENABLE_DEBUG_OUTPUT = False


mpu = MPU6050(I2C_BUS, DEVICE_ADDRESS, X_ACCEL_OFFSET, Y_ACCEL_OFFSET, Z_ACCEL_OFFSET, \
                X_GYRO_OFFSET, Y_GYRO_OFFSET, Z_GYRO_OFFSET, ENABLE_DEBUG_OUTPUT)

mpu.dmp_initialize()
mpu.set_DMP_enabled(True)
mpu_int_status = mpu.get_int_status()
print(hex(mpu_int_status))

packet_size = mpu.DMP_get_FIFO_packet_size()
print(packet_size)
FIFO_count = mpu.get_FIFO_count()
print(FIFO_count)

count = 0
FIFO_buffer = [0]*64
FIFO_count_list = list()

while True:
    FIFO_count = mpu.get_FIFO_count()
    mpu_int_status = mpu.get_int_status()

    # If overflow is detected by status or fifo count we want to reset
    if (FIFO_count == 1024) or (mpu_int_status & 0x10):
        mpu.reset_FIFO()
    # Check if fifo data is ready
    elif (mpu_int_status & 0x02):
        while FIFO_count < packet_size:
            FIFO_count = mpu.get_FIFO_count()

        FIFO_buffer = mpu.get_FIFO_bytes(packet_size)
        accel = mpu.DMP_get_acceleration_int16(FIFO_buffer)
        quat = mpu.DMP_get_quaternion_int16(FIFO_buffer)
        grav = mpu.DMP_get_gravity(quat)
        roll_pitch_yaw = mpu.DMP_get_euler_roll_pitch_yaw(quat, grav)

        if count % 5 == 0:
            print('roll: ' + str(roll_pitch_yaw.x))
            print('pitch: ' + str(roll_pitch_yaw.y))
            print('yaw: ' + str(2 * roll_pitch_yaw.z))

        count += 1
