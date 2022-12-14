from time import sleep

from sensing_system import Sensing_system


sensing_system = Sensing_system()


if __name__ == "__main__":
    try:
        while True:
            print("------------------------")
            print(sensing_system.get_front_sensor_distance())
            print(sensing_system.get_rear_sensor_distance())
            print(sensing_system.get_left_sensor_distance())
            print(sensing_system.get_right_sensor_distance())

            sleep(1)

    except KeyboardInterrupt:
        print("End of the test")