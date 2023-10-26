#include <stdio.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/queue.h"
#include "driver/gpio.h"
#include "driver/i2c.h"
#include "string.h"

#define RESET_BUTTON_PIN 0
#define LED_PIN 2

#define I2C_SLAVE_SDA_IO 21 // GPIO number userd for SDA
#define I2C_SLAVE_SCL_IO 22 // GPIO number userd for SCL
#define I2C_SLAVE_MAX_SPEED 1000 // I2C slave clock frequency
#define ESP_SLAVE_ADDR 0x18 // ESP32 slave address in the raspberry pi

i2c_port_t i2c_slave_port = I2C_NUM_0;
QueueHandle_t interputQueue;

static void IRAM_ATTR gpio_interrupt_handler(void *args)
{
    int pinNumber = (int)args;
    xQueueSendFromISR(interputQueue, &pinNumber, NULL);
}

void turn_onboard_led_on(){
    gpio_set_level(LED_PIN, 1);
}

void turn_onboard_led_off(){
    gpio_set_level(LED_PIN, 0);
}

void Control_Task(void *params)
{
    int pinNumber, count = 0;
    while (true)
    {
        if (xQueueReceive(interputQueue, &pinNumber, portMAX_DELAY))
        {
            if (pinNumber == RESET_BUTTON_PIN){
                printf("GPIO %d was pressed %d times. The state is %d\n", pinNumber, count++, gpio_get_level(RESET_BUTTON_PIN));
                gpio_set_level(LED_PIN, gpio_get_level(RESET_BUTTON_PIN));

                const uint8_t *answer = (const uint8_t *)"Hi, from ESP32";
                // envia resposta para o master
                i2c_slave_write_buffer(i2c_slave_port, answer, 12, pdMS_TO_TICKS(20));
            }
            if (pinNumber == I2C_SLAVE_SDA_IO){
                uint8_t *data = (uint8_t *) malloc(2);
                i2c_slave_read_buffer(i2c_slave_port, data, 2, pdMS_TO_TICKS(20));
                // concatenate the first two characters from data
                // and compare with "ca"

                printf("TAMANHO MSG: %d\n", sizeof(data));

                if ((char) data[0] == 'c' && (char) data[1] == 'b') {
                    // coloca o valor do gpio do botão na variavel answer e envia para o master
                    const uint8_t *answer = (const uint8_t *)"aquiosdados";

                    // descreve na saida padrao o valor da variavel *answer
                    printf("%s\n", answer);
                    printf("TAMANHO ANSWER: %d\n", sizeof(answer));
                    
                    // envia resposta para o master
                    i2c_slave_write_buffer(i2c_slave_port, answer, 12, pdMS_TO_TICKS(20));
                }

                if ((char) data[0] == 'c' && (char) data[1] == 'd') {
                    turn_onboard_led_on();
                }
                printf("%s\n", data);

                free(data);
            }
        }
        gpio_set_level(LED_PIN, 0);
    }
}

void i2c_initialize(){
    
    int i2c_master_port = 0;

    // Define o tipo de funcionamento do I2C da ESP como slave
    i2c_mode_t esp_mode = I2C_MODE_SLAVE;

    i2c_config_t conf_slave = {
        .sda_io_num = I2C_SLAVE_SDA_IO,            // select SDA GPIO specific to your project
        .sda_pullup_en = GPIO_PULLUP_ENABLE,
        .scl_io_num = I2C_SLAVE_SCL_IO,            // select SCL GPIO specific to your project
        .scl_pullup_en = GPIO_PULLUP_ENABLE,
        .mode = esp_mode,
        .slave.addr_10bit_en = 0,
        .slave.slave_addr = ESP_SLAVE_ADDR,        // slave address of your project
        .slave.maximum_speed = I2C_SLAVE_MAX_SPEED, // expected maximum clock speed
        .clk_flags = 0,                            // optional; you can use I2C_SCLK_SRC_FLAG_* flags to choose I2C source clock here
    };

    i2c_param_config(i2c_master_port, &conf_slave);
    
    i2c_driver_install(i2c_slave_port, esp_mode, 1024, 1024, 0);
}

void app_main()
{
    i2c_initialize();

    // Configura o pino do LED como saída
    esp_rom_gpio_pad_select_gpio(LED_PIN);
    gpio_set_direction(LED_PIN, GPIO_MODE_OUTPUT);

    // Configura o pino do botão como entrada
    esp_rom_gpio_pad_select_gpio(RESET_BUTTON_PIN);
    gpio_set_direction(RESET_BUTTON_PIN, GPIO_MODE_INPUT);
    gpio_pulldown_en(RESET_BUTTON_PIN);
    gpio_pullup_dis(RESET_BUTTON_PIN);
    gpio_set_intr_type(RESET_BUTTON_PIN, GPIO_INTR_POSEDGE);

    // Configura o pino I2C para receber interrupções
    gpio_set_intr_type(I2C_SLAVE_SDA_IO, GPIO_INTR_ANYEDGE);

    // TASK ASSOCIADA AO BOTÃO
    interputQueue = xQueueCreate(10, sizeof(int));
    xTaskCreate(Control_Task, "Control_Task", 2048, NULL, 1, NULL);

    gpio_install_isr_service(0);
    gpio_isr_handler_add(RESET_BUTTON_PIN, gpio_interrupt_handler, (void *)RESET_BUTTON_PIN);
    gpio_isr_handler_add(I2C_SLAVE_SDA_IO, gpio_interrupt_handler, (void *)I2C_SLAVE_SDA_IO);
}
