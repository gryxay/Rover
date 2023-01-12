from Distance_Sensor import Distance_Sensor

from Distance_Sensor_Constants import Distance_Sensor_Constants


def distance_accuracy_test(distance_sensor) -> bool:
    print("< 1. Distance accuracy test")
    print("< Put the sensor near a wall or another flat object.")
    print("< Keep the distance < 50CM.")
    print("< Measure the actual distance from the sensor to the object with a measuring tool")

    print("Press enter when you are ready.", end = " ")
    input()

    print("Distance measured by the sensor: " + str(distance_sensor.get_distance()))
    
    answer = input("Do the measured distcances correspond to each other? [y/n]")
          
    print("\n" + "------------------------------------------------------------------------------------" + "\n")

    if answer == "y":
        return True

    return False


if __name__ == "__main__":
    passed_tests = 0

    trig_pin = int(input("Enter the trig pin of the distance sensor: "))
    echo_pin = int(input("Enter the echo pin of the distance sensor: "))

    distance_sensor = Distance_Sensor(trig_pin, echo_pin)


    if distance_accuracy_test(distance_sensor):
        passed_tests += 1


    print("Total tests passed: [" + str(passed_tests) + "/1]")
