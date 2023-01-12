from Buzzer import Buzzer

from Buzzer_Constants import Buzzer_Constants


def sound_signal_test(buzzer) -> list:
    passed_tests = 0
    count = 1

    print("< 1. Sound signal tests" + " [" + str(len(Buzzer_Constants.SOUND_SIGNALS)) + "]")
    print("< You will have to listen, and enter the amount of beeps that you heard.")

    for sound_signal in Buzzer_Constants.SOUND_SIGNALS:
        print("< [" + str(count) + "/" + str(len(Buzzer_Constants.SOUND_SIGNALS)) + "]", end = " ")
        print("Press enter when you are ready.", end = " ")
        input()

        print("< Playing: \"" + sound_signal + "\" soung signal...")
        buzzer.sound_signal(sound_signal)

        print("How many beeps did you hear? ")
        answer = input("> ")

        if answer == str(Buzzer_Constants.SOUND_SIGNALS[sound_signal][0] * Buzzer_Constants.SOUND_SIGNALS[sound_signal][1]):
            passed_tests += 1

        count += 1

    print("Test passed: [" + str(passed_tests) + "/" + str(len(Buzzer_Constants.SOUND_SIGNALS)) + "]")
    print("\n" + "------------------------------------------------------------------" + "\n")

    return [passed_tests, len(Buzzer_Constants.SOUND_SIGNALS)]


def song_test(buzzer) -> list:
    passed_tests = 0
    count = 1

    print("< 2. Song tests" + " [" + str(len(Buzzer_Constants.SONGS)) + "]")
    print("< You will have to listen to a few short songs and anwer questions")

    for song in Buzzer_Constants.SONGS:
        print("< [" + str(count) + "/" + str(len(Buzzer_Constants.SONGS)) + "]", end = " ")
        print("Press enter when you are ready.", end = " ")
        input()

        print("< Playing: \"" + song + "\"...")
        buzzer.play_song(song)

        print("Did the song play correctly? [y/n]")
        answer = input("> ")

        if answer == "y":
            passed_tests += 1

        count += 1

    print("Test passed: [" + str(passed_tests) + "/" + str(len(Buzzer_Constants.SONGS)) + "]")
    print("\n" + "------------------------------------------------------------------" + "\n")

    return [passed_tests, len(Buzzer_Constants.SONGS)]


if __name__ == "__main__":
    buzzer = Buzzer(debug = True)
    buzzer = None
    passed_tests = 0
    total_tests = 0


    passes, tests = sound_signal_test(buzzer)
    passed_tests += passes
    total_tests += tests


    passes, tests = song_test(buzzer)
    passed_tests += passes
    total_tests += tests


    print("Total tests passed: [" + str(passed_tests) + "/" + str(total_tests) + "]")
