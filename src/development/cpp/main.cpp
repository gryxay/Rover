#include <iostream>
#include <wiringPi.h>
#include <atomic>
#include "drivetrain.h"
#include "distance_sensor.h"

using namespace std;

unsigned short FRONT_SENSOR_TRIG_PIN = 21;
unsigned short FRONT_SENSOR_ECHO_PIN = 12;
/*
unsigned short REAR_SENSOR_TRIG_PIN = NULL;
unsigned short REAR_SENSOR_ECHO_PIN = NULL;
unsigned short LEFT_SENSOR_TRIG_PIN = NULL;
unsigned short LEFT_SENSOR_ECHO_PIN = NULL;
unsigned short RIGHT_SENSOR_TRIG_PIN = NULL;
unsigned short RIGHT_SENSOR_ECHO_PIN = NULL;
*/
unsigned short LEFT_MOTOR_DIR_PIN = 20;
unsigned short LEFT_MOTOR_STEP_PIN = 16;
unsigned short RIGHT_MOTOR_DIR_PIN = 26;
unsigned short RIGHT_MOTOR_STEP_PIN = 19;

atomic<float> front_sensor_last_scan;

PI_THREAD (update_sensor_data)
{
    Distance_sensor front_sensor = Distance_sensor(FRONT_SENSOR_TRIG_PIN, FRONT_SENSOR_ECHO_PIN);

    while(true)
    {
        front_sensor_last_scan = front_sensor.get_distance();
    }
}

int main() {
    Drivetrain drivetrain = Drivetrain(LEFT_MOTOR_DIR_PIN, LEFT_MOTOR_STEP_PIN, RIGHT_MOTOR_DIR_PIN, RIGHT_MOTOR_STEP_PIN);
    // Distance_sensor front_sensor = Distance_sensor(FRONT_SENSOR_TRIG_PIN, FRONT_SENSOR_ECHO_PIN);

    int x = piThreadCreate(update_sensor_data);

    if (x != 0) 
    {
        printf ("it didn't start\n");
    }

    front_sensor_last_scan = 11.0;

    while(front_sensor_last_scan > 10.0)
    {
        drivetrain.drive('f');
    }
}
