// REFERENCE: https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/peripherals/i2c.html?highlight=i2c
// https://www.kernel.org/doc/Documentation/i2c/smbus-protocol

#include <stdio.h>
#include <stdlib.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/i2c.h"


#define I2C_SLAVE_SDA_IO 21 // GPIO number userd for SDA
#define I2C_SLAVE_SCL_IO 22 // GPIO number userd for SCL
#define I2C_SLAVE_MAX_SPEED 10000 // I2C slave clock frequency
#define ESP_SLAVE_ADDR 0x18 // ESP32 slave address, you can set any 7bit value


void app_main(void){

    int i2c_master_port = 0;

    i2c_port_t i2c_slave_port = I2C_NUM_0;
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

    while(1){
        // obtem comando do master
        uint8_t *data = (uint8_t *) malloc(32);
        i2c_slave_read_buffer(i2c_slave_port, data, 32, pdMS_TO_TICKS(100));
        printf("Data: %s\n", data);
        free(data);

        const uint8_t *answer = (const uint8_t *)"Hi, from ESP32";
        // envia resposta para o master
        i2c_slave_write_buffer(i2c_slave_port, answer, 12, pdMS_TO_TICKS(100));

        vTaskDelay(pdMS_TO_TICKS(250));
    }
}
