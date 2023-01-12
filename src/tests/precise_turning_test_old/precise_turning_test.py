from time import sleep

from drivetrain import Drivetrain


drivetrain = Drivetrain()


if __name__ == "__main__":
    # Turn on the motor controllers
    drivetrain.toggle_power(True)

    # Turn 90 degrees to the left
    drivetrain.turn('l', 90)

    sleep(2)

    # Turn 90 degrees to the right
    drivetrain.turn('r', 90)

    # Turn off the motor controllers
    drivetrain.toggle_power(False)
