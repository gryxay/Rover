from Computer_Vision import Computer_Vision
from time import sleep

from Computer_Vision_Constants import Computer_Vision_Constants


def object_detection_test(computer_vision):
    print("< Object detection test. Available object classes: ")
    print(Computer_Vision_Constants.CLASSES)
    print("< Try detectng at least one object from available classes.")

    while True:
        print(computer_vision.get_last_detected_object())
        
        sleep(1)

        
if __name__ == "__main__":
    object_detection_test(Computer_Vision())