class Computer_Vision_Constants:
    IMAGE_WIDTH = 640
    IMAGE_HEIGHT = 480
    MAX_FPS = 15
    LOOP_TIMEOUT = 1 / MAX_FPS

    # Percentage of confidence needed to categorise an object
    MIN_CONFIDENCE = 0.75 # 1 = 100%;

    PROTOTXT_PATH = "models/MobileNetSSD_deploy.prototxt"
    MODEL_PATH = "models/MobileNetSSD_deploy.caffemodel"

    CLASSES = [
        "background", "aeroplane", "bicycle", "bird", "boat",
        "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
        "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
        "sofa", "train", "tvmonitor", "unknown"
    ]
