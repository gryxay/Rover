from MPU6050 import MPU6050


mpu = MPU6050(1, 0x68, 0, 0, 0, 0, 0, 0, True)
mpu.dmp_initialize()
mpu.set_DMP_enabled(True)
mpu_int_status = mpu.get_int_status()

print(hex(mpu_int_status))

while True:
    print(mpu.get_acceleration())
    print(mpu.get_rotation())
