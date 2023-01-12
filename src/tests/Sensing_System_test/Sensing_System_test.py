from Sensing_System import Sensing_System
from time import sleep

from Constants import Sensing_System_Constants



def distance_accuracy_test(sensing_system) -> int:
    passed_tests = 0

    print("< 1. Distance accuracy test.")
    print("< Measure the actual distances from the sensors to the objects with a measuring tool.")

    print("Press enter when you are ready. You will have 60 seconds to test the sensors.", end = " ")
    input()

    for _ in range(60):
        print(sensing_system.get_sensor_data())

        sleep(1)
    
    answer = input("Does the front distance sensor return the correct distance? [y/n]")

    if answer == "y":
        passed_tests += 1


    answer = input("Does the rear distance sensor return the correct distance? [y/n]")

    if answer == "y":
        passed_tests += 1


    answer = input("Does the left distance sensor return the correct distance? [y/n]")

    if answer == "y":
        passed_tests += 1


    answer = input("Does the right distance sensor return the correct distance? [y/n]")

    if answer == "y":
        passed_tests += 1


          
    print("\n" + "------------------------------------------------------------------------------------" + "\n")

    return passed_tests


if __name__ == "__main__":
    sensing_system = Sensing_System(debug = True)
    passed_tests = 0


    passed_tests = distance_accuracy_test(sensing_system)


    print("Total tests passed: [" + str(passed_tests) + "/4]")
