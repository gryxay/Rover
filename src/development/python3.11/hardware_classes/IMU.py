from multiprocessing import Process, Event, Value
from time import sleep

from MPU6050 import MPU6050
from SimplePID import SimplePID

from Constants import IMU_Constants


class IMU:
    def __init__(self, buzzer = None, auto_calibrate = False, sound_signals = False, debug = False):
        self.__debug = debug
        self.__sound_signals = sound_signals

        self.__buzzer = buzzer

        if auto_calibrate:
            self.__calibrate()

        self.__mpu = MPU6050(IMU_Constants.I2C_BUS, IMU_Constants.DEVICE_ADDRESS, 0, 0, 0, 0, 0, 0)

        if self.__debug:
            print("IMU: Applying offsets")

        self.__apply_offsets()

        if self.__debug:
            print("IMU: Initialising the DMP")

        self.__mpu.dmp_initialize()
        self.__mpu.set_DMP_enabled(True)

        self.__roll = Value('f', 0)
        self.__pitch = Value('f', 0)
        self.__yaw = Value('f', 0)

        self.__termination_event = Event()

        if self.__debug:
            print("IMU: Starting a background process")

        # Start a process, that constantly updates yaw data in the background
        self.__background_process = Process(target = self.__update_imu_data)
        self.__background_process.start()

        # Wait for yaw data to stabilize
        if self.__debug:
            print("IMU: Stabilising yaw value...")
        
        sleep(IMU_Constants.DMP_INITIALIZATION_TIMEOUT)


    def __array_average(self, array):
        sum = 0.0

        for index in range(0, len(array)):
            sum += array[index]

        return sum / len(array)


    def __calibrate(self):
        if self.__debug:
            print("IMU: Calibrating...")


        mpu = MPU6050(IMU_Constants.I2C_BUS, \
                      IMU_Constants.DEVICE_ADDRESS, \
                      0, 0, 0, 0, 0, 0, \
                      self.__debug)
    

        x_accelerometer_offset = 0
        y_accelerometer_offset = 0
        z_accelerometer_offset = 0

        x_gyroscope_offset = 0
        y_gyroscope_offset = 0
        z_gyroscope_offset = 0


        kp = 0.03125
        ki = 0.25
        kd = 0


        pidax = SimplePID(0, -15000, 15000, kp, ki, kd, 100, True)
        piday = SimplePID(0, -15000, 15000, kp, ki, kd, 100, True)
        pidaz = SimplePID(0, -15000, 15000, kp, ki, kd, 100, True)

        pidgx = SimplePID(0, -15000, 15000, kp, ki, kd, 100, True)
        pidgy = SimplePID(0, -15000, 15000, kp, ki, kd, 100, True)
        pidgz = SimplePID(0, -15000, 15000, kp, ki, kd, 100, True)


        acceleration_reading = mpu.get_acceleration()

        x_acceleration_reading = acceleration_reading[0]
        y_acceleration_reading = acceleration_reading[1]
        z_acceleration_reading = acceleration_reading[2]

        x_acceleration_average = [0]*100
        y_acceleration_average = [0]*100
        z_acceleration_average = [0]*100

        x_accelerometer_offset_average = [0]*100
        y_accelerometer_offset_average = [0]*100
        z_accelerometer_offset_average = [0]*100

        acceleration_x_index = 0
        acceleration_y_index = 0
        acceleration_z_index = 0


        gyro_reading = mpu.get_rotation()

        x_gyro_reading = gyro_reading[0]
        y_gyro_reading = gyro_reading[1]
        z_gyro_reading = gyro_reading[2]

        x_gyro_average = [0]*100
        y_gyro_average = [0]*100
        z_gyro_average = [0]*100

        x_gyroscope_offset_average = [0]*100
        y_gyroscope_offset_average = [0]*100
        z_gyroscope_offset_average = [0]*100

        gyro_x_index = 0
        gyro_y_index = 0
        gyro_z_index = 0
        
        passthroughs = 0

        while passthroughs < IMU_Constants.CALIBRATION_PASSTHROUGHS:
            acceleration_reading = mpu.get_acceleration()

            x_acceleration_reading = acceleration_reading[0]
            y_acceleration_reading = acceleration_reading[1]
            z_acceleration_reading = acceleration_reading[2]


            gyro_reading = mpu.get_rotation()

            x_gyro_reading = gyro_reading[0]
            y_gyro_reading = gyro_reading[1]
            z_gyro_reading = gyro_reading[2]

        
            if pidax.check_time():
                x_accelerometer_offset = pidax.get_output_value(x_acceleration_reading)

                mpu.set_x_accel_offset(int(x_accelerometer_offset))

                x_acceleration_average[acceleration_x_index] = x_acceleration_reading
                x_accelerometer_offset_average[acceleration_x_index] = x_accelerometer_offset

                acceleration_x_index += 1
                
                if acceleration_x_index == len(x_acceleration_average):
                    acceleration_x_index = 0
                    

            if piday.check_time():
                y_accelerometer_offset = piday.get_output_value(y_acceleration_reading)

                mpu.set_y_accel_offset(int(y_accelerometer_offset))

                y_acceleration_average[acceleration_y_index] = y_acceleration_reading
                y_accelerometer_offset_average[acceleration_y_index] = y_accelerometer_offset

                acceleration_y_index += 1

                if acceleration_y_index == len(y_acceleration_average):
                    acceleration_y_index = 0


            if pidaz.check_time():
                z_accelerometer_offset = pidaz.get_output_value(z_acceleration_reading)

                mpu.set_z_accel_offset(int(z_accelerometer_offset))

                z_acceleration_average[acceleration_z_index] = z_acceleration_reading
                z_accelerometer_offset_average[acceleration_z_index] = z_accelerometer_offset

                acceleration_z_index += 1

                if acceleration_z_index == len(z_acceleration_average):
                    acceleration_z_index = 0


            # Gyro calibration
            if pidgx.check_time():
                x_gyroscope_offset = pidgx.get_output_value(x_gyro_reading)

                mpu.set_x_gyro_offset(int(x_gyroscope_offset))

                x_gyro_average[gyro_x_index] = x_gyro_reading
                x_gyroscope_offset_average[gyro_x_index] = x_gyroscope_offset

                gyro_x_index += 1

                if gyro_x_index == len(x_gyro_average):
                    gyro_x_index = 0
                    passthroughs += 1
                        

            if pidgy.check_time():
                y_gyroscope_offset = pidgy.get_output_value(y_gyro_reading)

                mpu.set_y_gyro_offset(int(y_gyroscope_offset))

                y_gyro_average[gyro_y_index] = y_gyro_reading
                y_gyroscope_offset_average[gyro_y_index] = y_gyroscope_offset

                gyro_y_index += 1

                if gyro_y_index == len(y_gyro_average):
                    gyro_y_index = 0


            if pidgz.check_time():
                z_gyroscope_offset = pidgz.get_output_value(z_gyro_reading)

                mpu.set_z_gyro_offset(int(z_gyroscope_offset))

                z_gyro_average[gyro_z_index] = z_gyro_reading
                z_gyroscope_offset_average[gyro_z_index] = z_gyroscope_offset

                gyro_z_index += 1
                
                if gyro_z_index == len(z_gyro_average):
                    gyro_z_index = 0


        self.__update_offsets({
            "x_accelerometer": self.__array_average(x_accelerometer_offset_average),
            "y_accelerometer": self.__array_average(y_accelerometer_offset_average),
            "z_accelerometer": self.__array_average(z_accelerometer_offset_average),
            "x_gyroscope": self.__array_average(x_gyroscope_offset_average),
            "y_gyroscope": self.__array_average(y_gyroscope_offset_average),
            "z_gyroscope": self.__array_average(z_gyroscope_offset_average)
        })


    def __update_offsets(self, offsets):
        file = open(IMU_Constants.CALIBRATION_DATA_FILE, 'w')

        file.write(str(offsets["x_accelerometer"]) + "\n" + 
                   str(offsets["y_accelerometer"]) + "\n" +
                   str(offsets["z_accelerometer"]) + "\n" +
                   str(offsets["x_gyroscope"]) + "\n" + 
                   str(offsets["y_gyroscope"]) + "\n" +
                   str(offsets["z_gyroscope"]))

        file.close()


    def __apply_offsets(self):
        file = open(IMU_Constants.CALIBRATION_DATA_FILE, 'r')

        file_data = file.readlines()
        
        file.close()

        self.__mpu.set_x_accel_offset(int(round(float(file_data[0].strip()))))
        self.__mpu.set_y_accel_offset(int(round(float(file_data[1].strip()))))
        self.__mpu.set_z_accel_offset(int(round(float(file_data[2].strip()))))
        self.__mpu.set_x_gyro_offset(int(round(float(file_data[3].strip()))))
        self.__mpu.set_y_gyro_offset(int(round(float(file_data[4].strip()))))
        self.__mpu.set_z_gyro_offset(int(round(float(file_data[5].strip()))))


    def __handle_error(self):
        self.terminate_background_process()
        self.__background_process = Process(target = self.__update_imu_data)
        self.__background_process.start()

        if self.__buzzer and self.__sound_signals:
            self.__buzzer.sound_signal("Error")


    def __update_imu_data(self):
        try:
            mpu_int_status = self.__mpu.get_int_status()
            packet_size = self.__mpu.DMP_get_FIFO_packet_size()
            FIFO_count = self.__mpu.get_FIFO_count()

            FIFO_buffer = [0]*64
            FIFO_count_list = list()

            last_yaw_read = 0

            while not self.__termination_event.is_set():
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
                    acceleration = self.__mpu.DMP_get_acceleration_int16(FIFO_buffer)
                    quaternion = self.__mpu.DMP_get_quaternion_int16(FIFO_buffer)
                    gravity = self.__mpu.DMP_get_gravity(quaternion)

                    with self.__roll.get_lock():
                        self.__roll.value = self.__mpu.DMP_get_euler_roll_pitch_yaw(quaternion, gravity).x


                    with self.__pitch.get_lock():
                        self.__pitch.value = self.__mpu.DMP_get_euler_roll_pitch_yaw(quaternion, gravity).y


                    with self.__yaw.get_lock():
                        self.__yaw.value = self.__mpu.DMP_get_euler_roll_pitch_yaw(quaternion, gravity).z

        except:
            self.__handle_error()
        

    def get_roll_value(self):
        with self.__roll.get_lock():
            return self.__roll.value


    def get_pitch_value(self):
        with self.__pitch.get_lock():
            return self.__pitch.value


    def get_yaw_value(self):
        with self.__yaw.get_lock():
            return self.__yaw.value


    def terminate_background_process(self):
        self.__termination_event.set()


if __name__ == "__main__":
    imu = IMU(debug = True)
    '''
    while True:
        print(imu.get_yaw_value())
    '''