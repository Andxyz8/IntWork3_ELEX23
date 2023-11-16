#include "buzzer.h"

void init_buzzer_config(){
    gpio_config_t gpio_buzzer_conf = {
        .pin_bit_mask = (1ULL << GPIO_NUM_13),
        .mode = GPIO_MODE_OUTPUT,
        .pull_up_en = 0,
        .pull_down_en = 0
    };
    gpio_config(&gpio_buzzer_conf);
}

void turn_off_buzzer(){
    gpio_set_level(GPIO_NUM_13, 0);
}

void turn_on_buzzer(){
    gpio_set_level(GPIO_NUM_13, 1);

    vTaskDelay((1000) / portTICK_PERIOD_MS);

    turn_off_buzzer();
}
