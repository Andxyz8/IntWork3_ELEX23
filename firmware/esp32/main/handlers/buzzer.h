#ifndef HANDLERS_BUZZER_H
#define HANDLERS_BUZZER_H

#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/gpio.h"

void init_buzzer_config();

void turn_on_buzzer();

void turn_off_buzzer();

#endif // HANDLERS_BUZZER_H