from multiprocessing import Process, Event, Value
from cv2 import VideoCapture, dnn, resize, CAP_PROP_FRAME_WIDTH, CAP_PROP_FRAME_HEIGHT, CAP_PROP_FPS
from sys import exit as sys_exit
from time import sleep

from Constants import Computer_Vision_Constants


class Computer_Vision:
    def __init__(self, buzzer = None, sound_signals = False, debug = False):
        self.__debug = debug
        self.sound_signals = sound_signals

        self.__buzzer = buzzer

        if self.__debug:
            print("Computer Vision: Initialising the camera")

        self.__camera = VideoCapture(0)
        self.__camera.set(CAP_PROP_FRAME_WIDTH, Computer_Vision_Constants.IMAGE_WIDTH)
        self.__camera.set(CAP_PROP_FRAME_HEIGHT, Computer_Vision_Constants.IMAGE_HEIGHT)
        self.__camera.set(CAP_PROP_FPS, Computer_Vision_Constants.MAX_FPS)
        
        self.__net = dnn.readNetFromCaffe(Computer_Vision_Constants.PROTOTXT_PATH, Computer_Vision_Constants.MODEL_PATH)

        self.__last_detected_object = Value("i", Computer_Vision_Constants.CLASSES.index("unknown"))

        self.__termination_event = Event()
        
        if self.__debug:
            print("Computer Vision: Starting a background process")

        self.__background_process = Process(target = self.__detect_objects)
        self.__background_process.start()


    # Detects objects using the camera
    def __detect_objects(self):
        try:
            while not self.__termination_event.is_set():
                image_exists, image = self.__camera.read()
                
                if image_exists:
                    blob = dnn.blobFromImage(resize(image, (300, 300)), 0.007, (300, 300), 130)

                    self.__net.setInput(blob)

                    detected_objects = self.__net.forward()

                    for i in range(detected_objects.shape[2]):
                        confidence = detected_objects[0][0][i][2]

                        if confidence > Computer_Vision_Constants.MIN_CONFIDENCE:
                            class_index = int(detected_objects[0][0][i][1])

                            with self.__last_detected_object.get_lock():
                                self.__last_detected_object.value = class_index

                sleep(Computer_Vision_Constants.LOOP_TIMEOUT)

        except:
            if self.__debug:
                print("Computer Vision error!")

            if self.__buzzer and self.__sound_signals:
                self.__buzzer.sound_signal("Error")

            sys_exit(1)


    # Returns the last detected object
    def get_last_detected_object(self):
        with self.__last_detected_object.get_lock():
            return Computer_Vision_Constants.CLASSES[self.__last_detected_object.value]


    # Sets the last detected object to "unknown"
    def reset_last_detected_object(self):
        with self.__last_detected_object.get_lock():
            self.__last_detected_object.value = Computer_Vision_Constants.CLASSES.index("unknown")


    def terminate_background_process(self):
        self.__termination_event.set()
