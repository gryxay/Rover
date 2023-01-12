#ifndef DRIVETRAIN_H
#define DRIVETRAIN_H

#include <wiringPi.h>
#include <unistd.h>

class Drivetrain 
{
private:
    unsigned short left_motor_dir_pin;
    unsigned short left_motor_step_pin;
    unsigned short right_motor_dir_pin;
    unsigned short right_motor_step_pin;

public:
    Drivetrain(unsigned short left_motor_dir_pin, unsigned short left_motor_step_pin,
                unsigned short right_motor_dir_pin, unsigned short right_motor_step_pin);
    void drive(char direction);
    void turn(float rotations, char direction);
    void rotate(float rotations, char direction);
};

#endif
