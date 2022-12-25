from multiprocessing import Process
import numpy
import cv2
from time import sleep
from matplotlib import pyplot as plt


IMAGE_WIDTH = 320
IMAGE_HEIGHT = 240
MAX_FPS = 10

# Percentage of confidence needed to categorise an object
MIN_CONFIDENCE = 0.8 # 1 = 100%;

PROTOTXT_PATH = 'models/MobileNetSSD_deploy.prototxt'
MODEL_PATH = 'models/MobileNetSSD_deploy.caffemodel'

CLASSES = [
    "background", "aeroplane", "bicycle", "bird", "boat",
    "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
    "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
    "sofa", "train", "tvmonitor"
]

# In testing / development phase
class Computer_vision:
    def __init__(self):
        self.__left_camera = cv2.VideoCapture(2)
        self.__left_camera.set(cv2.CAP_PROP_FRAME_WIDTH, IMAGE_WIDTH)
        self.__left_camera.set(cv2.CAP_PROP_FRAME_HEIGHT, IMAGE_HEIGHT)

        self.__right_camera = cv2.VideoCapture(0)
        self.__right_camera.set(cv2.CAP_PROP_FRAME_WIDTH, IMAGE_WIDTH)
        self.__right_camera.set(cv2.CAP_PROP_FRAME_HEIGHT, IMAGE_HEIGHT)

        self.__net = net = cv2.dnn.readNetFromCaffe(PROTOTXT_PATH, MODEL_PATH)

        #Process(target=).start()


    def create_depth_map(self):
        while True:
            left_image_exists, left_image = self.__left_camera.read()
            right_image_exists, right_image = self.__right_camera.read()

            if left_image_exists and right_image_exists:
                left_image = cv2.cvtColor(left_image, cv2.COLOR_BGR2GRAY)
                right_image = cv2.cvtColor(right_image, cv2.COLOR_BGR2GRAY)

                stereo = cv2.StereoBM_create(numDisparities=16, blockSize=23)
                depth_map = stereo.compute(left_image, right_image)

                cv2.imwrite("left_image.jpg", left_image)
                cv2.imwrite("right_image.jpg", right_image)
                cv2.imwrite("depth_map.jpg", depth_map)

            sleep(1 / MAX_FPS)


    def detect_objects(self):
        while True:
            left_image_exists, left_image = self.__left_camera.read()
            right_image_exists, right_image = self.__right_camera.read()

            if left_image_exists and right_image_exists:
                # Left camera
                left_image_height = left_image.shape[0]
                left_image_width = left_image.shape[1]

                left_image_blob = cv2.dnn.blobFromImage(cv2.resize(left_image, (IMAGE_WIDTH, IMAGE_HEIGHT)), 0.007, (IMAGE_WIDTH, IMAGE_HEIGHT), 130)

                self.__net.setInput(left_image_blob)

                left_camera_detected_objects = self.__net.forward()

                for i in range(left_camera_detected_objects.shape[2]):
                    confidence = left_camera_detected_objects[0][0][i][2]

                    if confidence > MIN_CONFIDENCE:
                        class_index = int(left_camera_detected_objects[0][0][i][1])
                        prediction = f"{CLASSES[class_index]}: {confidence * 100:.2f}%"

                        print("Left:", prediction)

                # Right camera
                right_image_height = right_image.shape[0]
                right_image_width = right_image.shape[1]

                right_image_blob = cv2.dnn.blobFromImage(cv2.resize(right_image, (IMAGE_WIDTH, IMAGE_HEIGHT)), 0.007, (IMAGE_WIDTH, IMAGE_HEIGHT), 130)

                self.__net.setInput(right_image_blob)

                right_camera_detected_objects = self.__net.forward()

                for i in range(right_camera_detected_objects.shape[2]):
                    confidence = right_camera_detected_objects[0][0][i][2]

                    if confidence > MIN_CONFIDENCE:
                        class_index = int(right_camera_detected_objects[0][0][i][1])
                        prediction = f"{CLASSES[class_index]}: {confidence * 100:.2f}%"

                        print("Right:", prediction)

                sleep(1 / MAX_FPS)
        

    def camera_alignment_test(self):
        while True:
            left_image_exists, left_image = self.__left_camera.read()
            right_image_exists, right_image = self.__right_camera.read()

            if left_image_exists and right_image_exists:
                vertical_start_point = (160, 0)
                vertical_end_point = (160, 240)
                horizontal_start_point = (0, 120)
                horizontal_end_point = (320, 120)
                color = (0, 255, 0)
                thickness = 2

                left_image = cv2.line(left_image, vertical_start_point, vertical_end_point, color, thickness)
                left_image = cv2.line(left_image, horizontal_start_point, horizontal_end_point, color, thickness)

                right_image = cv2.line(right_image, vertical_start_point, vertical_end_point, color, thickness)
                right_image = cv2.line(right_image, horizontal_start_point, horizontal_end_point, color, thickness)

                cv2.imwrite("left_image.jpg", left_image)
                cv2.imwrite("right_image.jpg", right_image)

            sleep(1 / MAX_FPS)


if __name__ == "__main__":
    computer_vision = Computer_vision()

    #computer_vision.create_depth_map()
    computer_vision.detect_objects()
