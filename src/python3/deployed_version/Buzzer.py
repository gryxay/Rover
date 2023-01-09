import RPi.GPIO as GPIO
from time import sleep

from Constants import Buzzer_Constants


# Available songs:
# 1. "He's a Pirate"
# 2. "Found it!"


class Buzzer:
	__trig_pin = None

	
	def __init__(self, trig_pin = Buzzer_Constants.TRIG_PIN):
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


	def sound_signal(self, error_source):
		for _ in range(Buzzer_Constants.SOUND_SIGNALS[error_source][0]):
			if error_source in Buzzer_Constants.SOUND_SIGNALS:
				self.beep(Buzzer_Constants.SOUND_SIGNALS[error_source][1], Buzzer_Constants.SOUND_SIGNALS[error_source][2])

				sleep(Buzzer_Constants.SOUND_SIGNALS[error_source][3])

	
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
			print("Song \"" + song_name + "\" doesn't exist!")
