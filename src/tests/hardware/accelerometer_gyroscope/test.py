import time
from mpu6050 import mpu6050


mpu = mpu6050(0x68)


while True:
    accel_data = mpu.get_accel_data()
    print("ax: ", accel_data['x'])
    print("ay: ", accel_data['y'])
    print("az: ", accel_data['z'])

    gyro_data = mpu.get_gyro_data()
    print("gx: ", gyro_data['x'])
    print("gy: ", gyro_data['y'])
    print("gz: ", gyro_data['z'])

    print()
    time.sleep(0.1)
