#ifndef HANDLERS_MOTOR_HANDLER_H
#define HANDLERS_MOTOR_HANDLER_H

#include "constants.h"

extern mcpwm_config_t pwm_timer_config;

void initialize_motor_pwm();

void stop_motor_movement_x_seg(int time_in_secs);

void move_forward(float speed, int time_in_secs);

#endif // HANDLERS_MOTOR_HANDLER_H
