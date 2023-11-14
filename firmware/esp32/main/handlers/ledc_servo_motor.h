#ifndef HANDLERS_TASK_HANDLER_H
#define HANDLERS_TASK_HANDLER_H

#include "driver/ledc.h"

#define SERVO_GPIO GPIO_NUM_19
#define SERVO_MIN_DUTY 900  // micro seconds (uS), for 0
#define SERVO_MAX_DUTY  3800 // micro seconds (uS),for 180
#define SERVO_TRANSITION_TIME 1000 // in ms
#define SERVO_TIME_PERIOD 5000 // in ms
#define FULL_ANGLE 180
#define MIDDLE_ANGLE 90
#define ZERO_ANGLE 0

extern int servo_duty;
extern int servo_delta;

void initialize_ledc_servo();

void set_servo_angle(int target_angle, int transition_time);

void set_servo_middle_angle();

void set_servo_full_angle();

void set_servo_zero_angle();

#endif // HANDLERS_TASK_HANDLER_H