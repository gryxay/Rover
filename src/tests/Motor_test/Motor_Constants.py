class Motor_Constants:
    LEFT_MOTOR_DIR_PIN = 16
    LEFT_MOTOR_STEP_PIN = 20
    RIGHT_MOTOR_DIR_PIN = 19
    RIGHT_MOTOR_STEP_PIN = 26
    SLEEP_PIN = 21
    
    CW = 1     	# Clockwise Rotation
    CCW = 0    	# Counterclockwise Rotation
    SPR = 800	# Signal pulses per revolution

    SLOW_TEST_DELAY = .001	# Time between signal pulses
    SLOW_TEST_ROTATIONS = 3	# Times that the motor shaft turns

    FAST_TEST_DELAY = .0001		# Time between signal pulses
    FAST_TEST_ROTATIONS = 50	# Times that the motor shaft turns
