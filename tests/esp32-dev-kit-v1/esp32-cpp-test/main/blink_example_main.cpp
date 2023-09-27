/*
 * SPDX-FileCopyrightText: 2010-2022 Espressif Systems (Shanghai) CO LTD
 *
 * SPDX-License-Identifier: CC0-1.0
 */

#include <stdio.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_flash.h"
#include "driver/gpio.h"

extern "C" void app_main(void)
{
    printf("Hello world!\n");

    int PIN_RESET = 2;

    // Usado para inicializar a porta como GPIO
    gpio_reset_pin((gpio_num_t) PIN_RESET);
    gpio_set_direction((gpio_num_t) PIN_RESET, GPIO_MODE_OUTPUT);

    int x = 0;

    while(x < 20){
        gpio_set_level((gpio_num_t) PIN_RESET, 0);
        vTaskDelay(1000 / portTICK_PERIOD_MS);
        printf("Loading %d seconds has past...\n", x);
        x++;

        gpio_set_level((gpio_num_t) PIN_RESET, 1);
        vTaskDelay(1000 / portTICK_PERIOD_MS);
        printf("Loading %d seconds has past...\n", x);
        x++;
    }

    fflush(stdout);
}
