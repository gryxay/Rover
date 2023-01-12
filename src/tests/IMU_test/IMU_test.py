from time import time
from IMU import IMU

from Constants import IMU_Constants, MPU_Constants


def roll_angle_test(imu) -> bool:
    start_time = time()

    print("< 1. Roll angle test (around x axis).")
    print("< You will have 30 seconds to test the correctness of a given angle...")
    print("< Try rotating the robot in 90 degree angles for easier testing.")
    print("< Press enter when you are ready.", end = " ")
    input()

    while time() - start_time < 30:
        print(imu.get_roll_value())

    print("Was the angle accurate? [y/n]")
    answer = input("> ")

    if answer == "y":
        return True

    return False


def pitch_angle_test(imu) -> bool:
    start_time = time()

    print("< 2. Pitch angle test (around y axis).")
    print("< You will have 30 seconds to test the correctness of a given angle...")
    print("< Try rotating the robot in 90 degree angles for easier testing.")
    print("< Press enter when you are ready.", end = " ")
    input()

    while time() - start_time < 30:
        print(imu.get_pitch_value())

    print("Was the angle accurate? [y/n]")
    answer = input("> ")

    if answer == "y":
        return True

    return False


def yaw_angle_test(imu) -> bool:
    start_time = time()

    print("< 3. Yaw angle test (around z axis).")
    print("< You will have 30 seconds to test the correctness of a given angle...")
    print("< Try rotating the robot in 90 degree angles for easier testing.")
    print("< Press enter when you are ready.", end = " ")
    input()

    while time() - start_time < 30:
        print(imu.get_yaw_value())

    print("Was the angle accurate? [y/n]")
    answer = input("> ")

    if answer == "y":
        return True

    return False


if __name__ == "__main__":
    imu = IMU(auto_calibrate = True, debug = True)

    passed_tests = 0


    if roll_angle_test(imu):
        passed_tests += 1

    if pitch_angle_test(imu):
        passed_tests += 1

    if yaw_angle_test(imu):
        passed_tests += 1

    
    print("Total tests passed: [" + str(passed_tests) + "/3]")