from multiprocessing import Process, Value
from time import sleep

from MPU6050 import MPU6050
from SimplePID import SimplePID

from Constants import IMU_Constants


class IMU:
    __mpu = None

    __x_accel_offset = 0
    __y_accel_offset = 0
    __z_accel_offset = 0
    __x_gyro_offset = 0
    __y_gyro_offset = 0
    __z_gyro_offset = 0

    __roll = Value('f', 0)
    __pitch = Value('f', 0)
    __yaw = Value('f', 0)

    __background_process = None

    __debug = None


    def __init__(self, auto_calibrate = False, debug = False):
        self.__debug = debug

        if auto_calibrate:
            self.__calibrate()

        self.__update_offsets()

        if self.__debug:
            print("Initialising IMU:")
        
        self.__mpu = MPU6050(IMU_Constants.I2C_BUS, \
                             IMU_Constants.DEVICE_ADDRESS, \
                             self.__x_accel_offset, \
                             self.__y_accel_offset, \
                             self.__z_accel_offset, \
                             self.__x_gyro_offset, \
                             self.__y_gyro_offset, \
                             self.__z_gyro_offset, \
                             self.__debug)

        self.__mpu.dmp_initialize()
        self.__mpu.set_DMP_enabled(True)

        # Start a process, that constantly updates yaw data in the background
        self.__background_process = Process(target = self.__update_imu_readings)
        self.__background_process.start()

        # Wait for yaw data to stabilize
        if self.__debug:
            print("Waiting for positioning system to stabilise yaw value...")
        
        sleep(20)


    def __calibrate(self):
        if self.__debug:
            print("Calibrating the IMU...")

        mpu = MPU6050(IMU_Constants.I2C_BUS, \
                      IMU_Constants.DEVICE_ADDRESS, \
                      0, 0, 0, 0, 0, 0, \
                      self.__debug)
    
        x_accel_offset = 0
        y_accel_offset = 0
        z_accel_offset = 0
        x_gyro_offset = 0
        y_gyro_offset = 0
        z_gyro_offset = 0

        kp = 0.03125
        ki = 0.25
        kd = 0

        pidax = SimplePID(0, -15000, 15000, kp, ki, kd, 100, True)
        piday = SimplePID(0, -15000, 15000, kp, ki, kd, 100, True)
        pidaz = SimplePID(0, -15000, 15000, kp, ki, kd, 100, True)
        pidgx = SimplePID(0, -15000, 15000, kp, ki, kd, 100, True)
        pidgy = SimplePID(0, -15000, 15000, kp, ki, kd, 100, True)
        pidgz = SimplePID(0, -15000, 15000, kp, ki, kd, 100, True)

        accel_reading = mpu.get_acceleration()

        x_accel_reading = accel_reading[0]
        y_accel_reading = accel_reading[1]
        z_accel_reading = accel_reading[2]

        x_accel_avg = [0]*100
        y_accel_avg = [0]*100
        z_accel_avg = [0]*100

        x_accel_offset_avg = [0]*100
        y_accel_offset_avg = [0]*100
        z_accel_offset_avg = [0]*100

        axindex = 0
        ayindex = 0
        azindex = 0

        gyro_reading = mpu.get_rotation()

        x_gyro_reading = gyro_reading[0]
        y_gyro_reading = gyro_reading[1]
        z_gyro_reading = gyro_reading[2]

        x_gyro_avg = [0]*100
        y_gyro_avg = [0]*100
        z_gyro_avg = [0]*100

        x_gyro_offset_avg = [0]*100
        y_gyro_offset_avg = [0]*100
        z_gyro_offset_avg = [0]*100

        gxindex = 0
        gyindex = 0
        gzindex = 0

        reading_count = 0

        try:
            while reading_count < 3:
                accel_reading = mpu.get_acceleration()
                x_accel_reading = accel_reading[0]
                y_accel_reading = accel_reading[1]
                z_accel_reading = accel_reading[2]

                gyro_reading = mpu.get_rotation()
                x_gyro_reading = gyro_reading[0]
                y_gyro_reading = gyro_reading[1]
                z_gyro_reading = gyro_reading[2]

                if pidax.check_time():
                    x_accel_offset = pidax.get_output_value(x_accel_reading)

                    mpu.set_x_accel_offset(int(x_accel_offset))

                    x_accel_avg[axindex] = x_accel_reading
                    x_accel_offset_avg[axindex] = x_accel_offset

                    axindex += 1

                    if axindex == len(x_accel_avg):
                        axindex = 0
                        
                        if self.__debug:
                            print('x_accel_avg_read: ' +
                                str(self.__array_average(x_accel_avg)) +
                                ' x_accel_avg_offset: ' +
                                str(self.__array_average(x_accel_offset_avg)))
                            print('y_accel_avg_read: ' +
                                str(self.__array_average(y_accel_avg)) +
                                ' y_accel_avg_offset: ' +
                                str(self.__array_average(y_accel_offset_avg)))
                            print('z_accel_avg_read: ' +
                                str(self.__array_average(z_accel_avg)) +
                                ' z_accel_avg_offset: ' +
                                str(self.__array_average(z_accel_offset_avg)))
                        
                if piday.check_time():
                    y_accel_offset = piday.get_output_value(y_accel_reading)

                    mpu.set_y_accel_offset(int(y_accel_offset))

                    y_accel_avg[ayindex] = y_accel_reading
                    y_accel_offset_avg[ayindex] = y_accel_offset

                    ayindex += 1

                    if ayindex == len(y_accel_avg):
                        ayindex = 0

                if pidaz.check_time():
                    z_accel_offset = pidaz.get_output_value(z_accel_reading)

                    mpu.set_z_accel_offset(int(z_accel_offset))

                    z_accel_avg[azindex] = z_accel_reading
                    z_accel_offset_avg[azindex] = z_accel_offset

                    azindex += 1

                    if azindex == len(z_accel_avg):
                        azindex = 0

                # Gyro calibration
                if pidgx.check_time():
                    x_gyro_offset = pidgx.get_output_value(x_gyro_reading)

                    mpu.set_x_gyro_offset(int(x_gyro_offset))

                    x_gyro_avg[gxindex] = x_gyro_reading
                    x_gyro_offset_avg[gxindex] = x_gyro_offset

                    gxindex += 1

                    if gxindex == len(x_gyro_avg):
                        gxindex = 0
                        reading_count += 1
                        
                        if self.__debug:
                            print('x_avg_read: ' +
                                str(self.__array_average(x_gyro_avg)) +
                                ' x_avg_offset: ' +
                                str(self.__array_average(x_gyro_offset_avg)))
                            print('y_avg_read: ' +
                                str(self.__array_average(y_gyro_avg)) +
                                ' y_avg_offset: ' +
                                str(self.__array_average(y_gyro_offset_avg)))
                            print('z_avg_read: ' +
                                str(self.__array_average(z_gyro_avg)) +
                                ' z_avg_offset: ' +
                                str(self.__array_average(z_gyro_offset_avg)))
                            print()

                if pidgy.check_time():
                    y_gyro_offset = pidgy.get_output_value(y_gyro_reading)

                    mpu.set_y_gyro_offset(int(y_gyro_offset))

                    y_gyro_avg[gyindex] = y_gyro_reading
                    y_gyro_offset_avg[gyindex] = y_gyro_offset

                    gyindex += 1

                    if gyindex == len(y_gyro_avg):
                        gyindex = 0

                if pidgz.check_time():
                    z_gyro_offset = pidgz.get_output_value(z_gyro_reading)

                    mpu.set_z_gyro_offset(int(z_gyro_offset))

                    z_gyro_avg[gzindex] = z_gyro_reading
                    z_gyro_offset_avg[gzindex] = z_gyro_offset

                    gzindex += 1
                    
                    if gzindex == len(z_gyro_avg):
                        gzindex = 0

        except KeyboardInterrupt:
            pass

        file = open(IMU_Constants.CALIBRATION_DATA_FILE, "w")

        file.write(str(self.__array_average(x_accel_offset_avg)) + "\n" + 
                    str(self.__array_average(y_accel_offset_avg)) + "\n" +
                    str(self.__array_average(z_accel_offset_avg)) + "\n" +
                    str(self.__array_average(x_gyro_offset_avg)) + "\n" + 
                    str(self.__array_average(y_gyro_offset_avg)) + "\n" +
                    str(self.__array_average(z_gyro_offset_avg)))

        file.close()


    def __update_offsets(self):
        file = open(IMU_Constants.CALIBRATION_DATA_FILE, "r")
        file_data = file.readlines()
        file.close()

        self.__x_accel_offset = int(round(float(file_data[0].strip()), 0))
        self.__y_accel_offset = int(round(float(file_data[1].strip()), 0))
        self.__z_accel_offset = int(round(float(file_data[2].strip()), 0))
        self.__x_gyro_offset = int(round(float(file_data[3].strip()), 0))
        self.__y_gyro_offset = int(round(float(file_data[4].strip()), 0))
        self.__z_gyro_offset = int(round(float(file_data[5].strip()), 0))


    def __update_imu_readings(self):
        mpu_int_status = self.__mpu.get_int_status()
        packet_size = self.__mpu.DMP_get_FIFO_packet_size()
        FIFO_count = self.__mpu.get_FIFO_count()
        FIFO_buffer = [0]*64
        FIFO_count_list = list()

        while True:
            FIFO_count = self.__mpu.get_FIFO_count()
            mpu_int_status = self.__mpu.get_int_status()

            # If overflow is detected by status or fifo count we want to reset
            if (FIFO_count == 1024) or (mpu_int_status & 0x10):
                self.__mpu.reset_FIFO()
            # Check if fifo data is ready
            elif (mpu_int_status & 0x02):
                while FIFO_count < packet_size:
                    FIFO_count = self.__mpu.get_FIFO_count()

                FIFO_buffer = self.__mpu.get_FIFO_bytes(packet_size)
                accel = self.__mpu.DMP_get_acceleration_int16(FIFO_buffer)
                quat = self.__mpu.DMP_get_quaternion_int16(FIFO_buffer)
                grav = self.__mpu.DMP_get_gravity(quat)

                self.__roll.value = self.__mpu.DMP_get_euler_roll_pitch_yaw(quat, grav).x
                self.__pitch.value = self.__mpu.DMP_get_euler_roll_pitch_yaw(quat, grav).y
                self.__yaw.value = self.__mpu.DMP_get_euler_roll_pitch_yaw(quat, grav).z


    def __array_average(self, array):
        sum = 0.0

        for index in range(0, len(array)):
            sum += array[index]

        return sum / len(array)


    def get_roll_value(self):
        return self.__roll.value


    def get_pitch_value(self):
        return self.__pitch.value


    def get_yaw_value(self):
        return self.__yaw.value


# For testing
if __name__ == "__main__":
    imu = IMU(auto_calibrate = False, debug = True)

    while True:
        print(imu.get_roll_value())
        print(imu.get_pitch_value())
        print(imu.get_yaw_value())
        print()

        sleep(1)
  
