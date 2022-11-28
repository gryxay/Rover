import time
from drivetrain import Drivetrain


cm = 132 # It takes 132 motor steps to move 1 cm 
degrees_90 = 3.15 # It takes 3.15 rotations for both motors (turning in the opposite directions) to turn 90 degrees


drivetrain = Drivetrain(20, 16, 26, 19, 13)


def precision_test():
    while True:
        # Drives 1 cm forwards
        for i in range(cm):
            drivetrain.rotate('f') 

        time.sleep(1)

        # Drives 1 cm backwards
        for i in range(cm):
            drivetrain.rotate('b')

        time.sleep(1)

        # Drives 2 cm forwards
        for i in range(2 * cm):
            drivetrain.rotate('f')

        time.sleep(1)

        # Drives 2 cm backwards
        for i in range(2 * cm):
            drivetrain.rotate('b')	

        time.sleep(1)


def power_toggle_test():
    drivetrain.toggle_power(True)
    time.sleep(3)
    drivetrain.toggle_power(False)


if __name__ == "__main__":
    #drivetrain.turn('r', degrees_90)

    #precision_test()

    power_toggle_test()
