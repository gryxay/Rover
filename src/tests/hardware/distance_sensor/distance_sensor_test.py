from time import sleep

from distance_sensor import Distance_sensor


TRIG_PIN = 24
ECHO_PIN = 23


sensor = Distance_sensor(24, 23)


if __name__ == "__main__":
	try:
		while True:
			print(sensor.get_distance())

	except KeyboardInterrupt:
			print("End of the test")
