import RPi.GPIO as GPIO
from time import sleep

from Constants import Buzzer_Constants


# Available songs:
# 1. "Exploring"
# 2. "Found it!"
# 3. "Mario underworld"
# 4. "He's a Pirate"


class Buzzer:
	def __init__(self, trig_pin = Buzzer_Constants.TRIG_PIN, debug = False):
		self.__debug = debug

		if self.__debug:
			print("Buzzer: Setting up GPIO pins")

		self.__trig_pin = trig_pin

		GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(self.__trig_pin, GPIO.OUT)

		# Prevent constant beeping after initialization
		GPIO.output(self.__trig_pin, GPIO.HIGH)


	def __play_note(self, note_frequency, length):
		half_wave_time = 1 / (note_frequency * 2)
		waves = int(length * note_frequency)

		for _ in range(waves):
			GPIO.output(self.__trig_pin, GPIO.HIGH)

			sleep(half_wave_time)

			GPIO.output(self.__trig_pin, GPIO.LOW)

			sleep(half_wave_time)


		GPIO.output(self.__trig_pin, GPIO.HIGH)


	def beep(self, count, delay):
		for i in range(count):
			GPIO.output(self.__trig_pin, GPIO.LOW)
			sleep(delay)

			GPIO.output(self.__trig_pin, GPIO.HIGH)
			sleep(delay)


	def sound_signal(self, signal_name):
		for _ in range(Buzzer_Constants.SOUND_SIGNALS[signal_name][0]):
			if signal_name in Buzzer_Constants.SOUND_SIGNALS:
				self.beep(Buzzer_Constants.SOUND_SIGNALS[signal_name][1], Buzzer_Constants.SOUND_SIGNALS[signal_name][2])

				sleep(Buzzer_Constants.SOUND_SIGNALS[signal_name][3])

	
	def play_song(self, song_name):
		if song_name in Buzzer_Constants.SONGS:
			for i in range(len(Buzzer_Constants.SONGS[song_name])):
				note = Buzzer_Constants.SONGS[song_name][i][0]
				note_length = Buzzer_Constants.SONGS[song_name][i][1]

				if note:
					self.__play_note(Buzzer_Constants.NOTES[note], note_length)
					sleep(note_length * 0.1)

				else:
					sleep(note_length)
		
		else:
			print("Buzzer: Song \"" + song_name + "\" doesn't exist!")
