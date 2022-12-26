from multiprocessing import Process, Value
import cv2


IMAGE_WIDTH = 640
IMAGE_HEIGHT = 480
MAX_FPS = 30

# Percentage of confidence needed to categorise an object
MIN_CONFIDENCE = 0.8 # 1 = 100%;

PROTOTXT_PATH = 'models/MobileNetSSD_deploy.prototxt'
MODEL_PATH = 'models/MobileNetSSD_deploy.caffemodel'

CLASSES = [
    "background", "aeroplane", "bicycle", "bird", "boat",
    "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
    "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
    "sofa", "train", "tvmonitor", "unknown"
]


class Computer_vision:
    def __init__(self):
        self.__camera = cv2.VideoCapture(0)
        self.__camera.set(cv2.CAP_PROP_FRAME_WIDTH, IMAGE_WIDTH)
        self.__camera.set(cv2.CAP_PROP_FRAME_HEIGHT, IMAGE_HEIGHT)
        self.__camera.set(cv2.CAP_PROP_FPS, MAX_FPS)
        
        self.__net = net = cv2.dnn.readNetFromCaffe(PROTOTXT_PATH, MODEL_PATH)

        self.__last_detected_object = Value("i", CLASSES.index("unknown"))

        Process(target=self.__detect_objects).start()
                

    def __detect_objects(self):
        while True:
            image_exists, image = self.__camera.read()
            
            if image_exists:
                blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 0.007, (300, 300), 130)

                self.__net.setInput(blob)

                detected_objects = self.__net.forward()

                for i in range(detected_objects.shape[2]):
                    confidence = detected_objects[0][0][i][2]

                    if confidence > MIN_CONFIDENCE:
                        class_index = int(detected_objects[0][0][i][1])

                        self.__last_detected_object.value = class_index


    def get_last_detected_object(self):
        return CLASSES[self.__last_detected_object.value]


    def reset_last_detected_object(self):
        self.__last_detected_object.value = CLASSES.index("unknown")
