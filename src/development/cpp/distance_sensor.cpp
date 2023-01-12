#include "distance_sensor.h"

unsigned int DELAY = 100000; // Microseconds (0.1 seconds).
unsigned int SIGNAL_LENGTH = 10; // Microseconds (0.00001 seconds).

Distance_sensor::Distance_sensor(unsigned short trig_pin, unsigned short echo_pin)
{
    this->trig_pin = trig_pin;
    this->echo_pin = echo_pin;

    wiringPiSetupGpio();

    pinMode(trig_pin, OUTPUT);
    pinMode(echo_pin, INPUT);
}

double Distance_sensor::get_distance() 
{   
    double pulse_start;
    double pulse_end;

    digitalWrite(trig_pin, LOW);
    delayMicroseconds(DELAY);

    digitalWrite(trig_pin, HIGH);
    delayMicroseconds(SIGNAL_LENGTH);

    digitalWrite(trig_pin, LOW);

    while(digitalRead(echo_pin) == 0)
    {
        pulse_start = std::chrono::duration_cast<std::chrono::duration<double>>
            (std::chrono::system_clock::now().time_since_epoch()).count();
    }

    while(digitalRead(echo_pin) == 1)
    {
        pulse_end = std::chrono::duration_cast<std::chrono::duration<double>>
            (std::chrono::system_clock::now().time_since_epoch()).count();
    }

    return (pulse_end - pulse_start) * 17150;
}
