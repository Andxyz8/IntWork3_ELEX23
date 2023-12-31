#ifndef HANDLERS_MOTOR_HANDLER_H
#define HANDLERS_MOTOR_HANDLER_H

#include "constants.h"

extern mcpwm_config_t pwm_timer_config;
extern bool performing_movement;

void initialize_motor_pwm();

void stop_motor_movement_x_seg(int time_in_secs);

void move_forward(float pwm_left, float pwm_right, int time_in_secs);

void move_backward(float speed, int time_in_secs);

void rotate_left(float speed, int time_in_secs);

void rotate_right(float speed, int time_in_secs);

#endif // HANDLERS_MOTOR_HANDLER_H
