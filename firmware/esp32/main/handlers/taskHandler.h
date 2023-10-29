#ifndef HANDLERS_TASK_HANDLER_H
#define HANDLERS_TASK_HANDLER_H

#include <stdio.h>

#include "handlers/i2cHandler.h"

#include "driver/gpio.h"
#include "freertos/task.h"
#include "freertos/queue.h"


extern QueueHandle_t task_handler_interrupt_queue;

// static void IRAM_ATTR gpio_interruption_handler(void *args);

void task_controller(void *params);

void initialize_interruption_handler();

#endif // HANDLERS_TASK_HANDLER_H
