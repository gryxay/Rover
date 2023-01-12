class Distance_Sensor_Constants:
    # cm
    MAX_READING_DISTANCE = 400

    # cm/s
    SPEED_OF_SOUND = 34300
    HALF_SPEED_OF_SOUND = SPEED_OF_SOUND / 2

    # Values in seconds
    DELAY = 0.01		
    SIGNAL_LENGTH = 0.00001
    TIMEOUT = MAX_READING_DISTANCE / HALF_SPEED_OF_SOUND