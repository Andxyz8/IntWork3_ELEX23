#include "i2cHandler.h"


void i2c_handler_initialize(){
    // Define the i2c configuration for esp
    i2c_config_t conf_slave = {
        .sda_io_num = GPIO_21_I2C_SDA_RPI,            // select SDA GPIO specific to your project
        .sda_pullup_en = GPIO_PULLDOWN_ENABLE,
        .scl_io_num = GPIO_22_I2C_SCL_RPI,            // select SCL GPIO specific to your project
        .scl_pullup_en = GPIO_PULLUP_ENABLE,
        .mode = I2C_ESP_MODE_WITH_RASPBERRY_PI,
        .slave.addr_10bit_en = 0,
        .slave.slave_addr = I2C_SLAVE_ADDRESS_RASP, // slave address of your project
        .slave.maximum_speed = I2C_SLAVE_MAX_SPEED, // expected maximum clock speed
        .clk_flags = 0                              // optional; you can use I2C_SCLK_SRC_FLAG_* flags to choose I2C source clock here
    };

    // Configure the I2C bus
    i2c_param_config(I2C_MASTER_PORT, &conf_slave);

    // Install the i2c driver
    i2c_driver_install(I2C_MASTER_PORT, I2C_ESP_MODE_WITH_RASPBERRY_PI, 1024, 1024, 0);

    // Configure I2C pin to be able to have interruptions
    gpio_set_intr_type(GPIO_21_I2C_SDA_RPI, GPIO_INTR_POSEDGE);
}

uint8_t* read_32_bytes(){
    // Allocate memory for the data
    uint8_t *data_received_i2c = (uint8_t *) malloc(32 * sizeof(uint8_t));

    // Read the i2c buffer communication directly with raspberry
    i2c_slave_read_buffer(I2C_ESP_NUM_FOR_RASPBERRY, data_received_i2c, 32, pdMS_TO_TICKS(20));

    return data_received_i2c;
}

uint8_t* i2c_handler_receive_command(){
    // Allocate memory for the data
    uint8_t *data_received_i2c = (uint8_t *) malloc(2 * sizeof(uint8_t));

    // Read the i2c buffer communication directly with raspberry
    i2c_slave_read_buffer(I2C_ESP_NUM_FOR_RASPBERRY, data_received_i2c, 2, pdMS_TO_TICKS(20));

    return data_received_i2c;
}

float i2c_handler_receive_float(){
    // Allocate memory for the data
    uint8_t *data_received_i2c = (uint8_t *) malloc(4 * sizeof(uint8_t));

    // Read the i2c buffer communication directly with raspberry
    i2c_slave_read_buffer(I2C_ESP_NUM_FOR_RASPBERRY, data_received_i2c, 4, pdMS_TO_TICKS(20));

    float float_received = bytes_to_float(data_received_i2c);

    return float_received;
}

void i2c_handler_send_data(uint8_t *data_to_send_i2c){
    // Send the data to raspberry
    i2c_slave_write_buffer(
        I2C_ESP_NUM_FOR_RASPBERRY,
        data_to_send_i2c,
        sizeof(data_to_send_i2c),
        pdMS_TO_TICKS(20)
    );

    // printf("DATA SENT: %s\n", data_to_send_i2c);
}