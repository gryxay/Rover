from time import sleep

from drivetrain import Drivetrain


CM = 132 # It takes 132 motor steps to move 1 cm 


drivetrain = Drivetrain()


if __name__ == "__main__":
    # Turn on the motor controllers
    drivetrain.toggle_power(True)

    # Drive 50cm forwards
    for pulse in range(50 * CM):
        drivetrain.rotate('f')

    sleep(2)

    # Drive 50cm backwards
    for pulse in range(50 * CM):
        drivetrain.rotate('b')

    # Turn off the motor controllers
    drivetrain.toggle_power(False)
