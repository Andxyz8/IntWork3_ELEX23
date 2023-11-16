#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/gpio.h"

// #include "task.h"

void app_main(void)
{
    gpio_config_t io_conf = {
        .pin_bit_mask = (1ULL << GPIO_NUM_13),
        .mode = GPIO_MODE_OUTPUT,
        .pull_up_en = 0,
        .pull_down_en = 0
    };
    gpio_config(&io_conf);

    // gpio_set_direction(GPIO_NUM_13, GPIO_MODE_OUTPUT);

    printf("configured");

    while (1)
    {
        gpio_set_level(GPIO_NUM_13, 1);
        vTaskDelay((2000) / portTICK_PERIOD_MS);
        gpio_set_level(GPIO_NUM_13, 0);
        printf("executing");
    }
}
