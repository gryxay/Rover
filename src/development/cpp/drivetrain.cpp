#include "drivetrain.h"

unsigned short SPR = 800; // Signal pulses Per Revolution.
unsigned int DRIVING_DELAY = 500; // Microseconds (0.0005 seconds). Time between signal pulses when driving.
unsigned int TURNING_DELAY = 500; // Microseconds (0.0005 seconds). Time between signal pulses when turning.

Drivetrain::Drivetrain(unsigned short left_motor_dir_pin, unsigned short left_motor_step_pin,
                        unsigned short right_motor_dir_pin, unsigned short right_motor_step_pin) 
{
    this->left_motor_dir_pin = left_motor_dir_pin;
    this->left_motor_step_pin = left_motor_step_pin;
    this->right_motor_dir_pin = right_motor_dir_pin;
    this->right_motor_step_pin = right_motor_step_pin;

    wiringPiSetupGpio();

    pinMode(left_motor_dir_pin, OUTPUT);
    pinMode(left_motor_step_pin, OUTPUT);
    pinMode(right_motor_dir_pin, OUTPUT);
    pinMode(right_motor_step_pin, OUTPUT);
}

// Direction 'f' = forwards, 'b' = backwards.
// Should be used in a while loop.
void Drivetrain::drive(char direction)
{   
    if(direction == 'f')
    {
        digitalWrite(left_motor_dir_pin, HIGH);
        digitalWrite(right_motor_dir_pin, HIGH);
    }
    else if(direction == 'b')
    {
        digitalWrite(left_motor_dir_pin, LOW);
        digitalWrite(right_motor_dir_pin, LOW);
    }

    digitalWrite(left_motor_step_pin, HIGH);
    digitalWrite(right_motor_step_pin, HIGH);

    usleep(DRIVING_DELAY);

    digitalWrite(left_motor_step_pin, LOW);
    digitalWrite(right_motor_step_pin, LOW);

    usleep(DRIVING_DELAY);
}

// Direction 'l' = left, 'r' = right. 
void Drivetrain::turn(float rotations, char direction)
{
    if(direction == 'l')
    {
        digitalWrite(left_motor_dir_pin, LOW);
        digitalWrite(right_motor_dir_pin, HIGH);
    }
    else if(direction == 'r')
    {
        digitalWrite(left_motor_dir_pin, HIGH);
        digitalWrite(right_motor_dir_pin, LOW);
    }

    for(int pulse = 0; pulse < (int) SPR * rotations; pulse++)
    {
        digitalWrite(left_motor_step_pin, HIGH);
        digitalWrite(right_motor_step_pin, HIGH);

        usleep(TURNING_DELAY);

        digitalWrite(left_motor_step_pin, LOW);
        digitalWrite(right_motor_step_pin, LOW);

        usleep(TURNING_DELAY);
    }
}

// Direction 'f' = forwards, 'b' = backwards.
void Drivetrain::rotate(float rotations, char direction)
{
    if(direction == 'f')
    {
        digitalWrite(left_motor_dir_pin, HIGH);
        digitalWrite(right_motor_dir_pin, HIGH);
    }
    else if(direction == 'b')
    {
        digitalWrite(left_motor_dir_pin, LOW);
        digitalWrite(right_motor_dir_pin, LOW);
    }

    for(int pulse = 0; pulse < (int) SPR * rotations; pulse++)
    {
        digitalWrite(left_motor_step_pin, HIGH);
        digitalWrite(right_motor_step_pin, HIGH);

        usleep(DRIVING_DELAY);

        digitalWrite(left_motor_step_pin, LOW);
        digitalWrite(right_motor_step_pin, LOW);

        usleep(DRIVING_DELAY);
    }
}
