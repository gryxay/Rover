from multiprocessing import Process, Value
import cv2

from Constants import Computer_Vision_Constants


class Computer_Vision:
    def __init__(self):
        self.__camera = cv2.VideoCapture(0)
        self.__camera.set(cv2.CAP_PROP_FRAME_WIDTH, Computer_Vision_Constants.IMAGE_WIDTH)
        self.__camera.set(cv2.CAP_PROP_FRAME_HEIGHT, Computer_Vision_Constants.IMAGE_HEIGHT)
        self.__camera.set(cv2.CAP_PROP_FPS, Computer_Vision_Constants.MAX_FPS)
        
        self.__net = cv2.dnn.readNetFromCaffe(Computer_Vision_Constants.PROTOTXT_PATH, Computer_Vision_Constants.MODEL_PATH)

        self.__last_detected_object = Value("i", Computer_Vision_Constants.CLASSES.index("unknown"))

        Process(target = self.__detect_objects).start()
                

    # Detects objects using the camera
    def __detect_objects(self):
        while True:
            image_exists, image = self.__camera.read()
            
            if image_exists:
                blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 0.007, (300, 300), 130)

                self.__net.setInput(blob)

                detected_objects = self.__net.forward()

                for i in range(detected_objects.shape[2]):
                    confidence = detected_objects[0][0][i][2]

                    if confidence > Computer_Vision_Constants.MIN_CONFIDENCE:
                        class_index = int(detected_objects[0][0][i][1])

                        with self.__last_detected_object.get_lock():
                            self.__last_detected_object.value = class_index


    # Returns the last detected object
    def get_last_detected_object(self):
        with self.__last_detected_object.get_lock():
            return Computer_Vision_Constants.CLASSES[self.__last_detected_object.value]


    # Sets the last detected object to "unknown"
    def reset_last_detected_object(self):
        with self.__last_detected_object.get_lock():
            self.__last_detected_object.value = Computer_Vision_Constants.CLASSES.index("unknown")
