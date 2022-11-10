from time import sleep
import RPi.GPIO as GPIO


SPR = 800       # Steps Per Revolution
DELAY = 0.0005  # Time between signal pulses


class Motor:
    def __init__(self, dir_pin, step_pin):
        self.dir_pin = dir_pin
        self.step_pin = step_pin

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.dir_pin, GPIO.OUT)
        GPIO.setup(self.step_pin, GPIO.OUT)


    def rotate(self, rotations, direction):     # direction = 1 (clockwise); direction = 0 (counterclockwise);
        GPIO.output(self.dir_pin, direction)

        for x in range(int(SPR * rotations)):
            GPIO.output(self.step_pin, GPIO.HIGH)
            sleep(DELAY)
            GPIO.output(self.step_pin, GPIO.LOW)
            sleep(DELAY)
