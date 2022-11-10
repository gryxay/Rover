#ifndef DISTANCE_SENSOR_H
#define DISTANCE_SENSOR_H

#include <wiringPi.h>
#include <chrono>

class Distance_sensor 
{
private:
    unsigned short trig_pin;
    unsigned short echo_pin;

public:
    Distance_sensor(unsigned short trig_pin, unsigned short echo_pin);
    double get_distance();
};

#endif