from Drivetrain import Drivetrain
from IMU import IMU
from time import sleep

from Constants import Drivetrain_Constants, IMU_Constants


def drivetrain_test(drivetrain) -> int:
    passed_tests = 0

    print("< Drivetrain test [2]")
    print("< The robot will drive forward 100CM and backward 100CM.")
    print("< You will have to check if the robot goes in a straight line and that it returns to the starting position.")

    print("Press enter when you are ready.", end = " ")
    input()

    drivetrain.toggle_power(True)

    drivetrain.drive('f', 100, "fast")

    sleep(1)

    drivetrain.drive('b', 100, "fast")

    drivetrain.toggle_power(False)

    print("Did the robot drive in a straight line? [y/n]")
    answer = input("> ")

    if answer == 'y':
        passed_tests += 1

    print("Did the robot return to the starting position?? [y/n]")
    answer = input("> ")

    if answer == 'y':
        passed_tests += 1

    return passed_tests


if __name__ == "__main__":
    imu = IMU(debug = True)
    drivetrain = Drivetrain(imu = imu)


    passed_tests = drivetrain_test(drivetrain)


    print("Total tests passed: [" + str(passed_tests) + "/2]")
