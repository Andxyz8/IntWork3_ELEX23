#include "compass_module.h"

void init_i2c_config_compass_module(){
    // i2c_set_pin(
        // I2C_ESP_NUM_FOR_COMPASS_MODULE,
        // GPIO_23_I2C_SDA_CMD,
        // GPIO_19_I2C_SCL_CMD,
        // GPIO_PULLUP_ENABLE,
        // GPIO_PULLUP_DISABLE,
        // I2C_ESP_MODE_WITH_COMPASS_MODULE
    // );

    i2c_config_t i2c_config_master_compass = {
        .mode = I2C_ESP_MODE_WITH_COMPASS_MODULE,
        .sda_io_num = GPIO_23_I2C_SDA_CMD,
        .sda_pullup_en = GPIO_PULLUP_ENABLE,
        .scl_io_num = GPIO_19_I2C_SCL_CMD,
        .scl_pullup_en = GPIO_PULLUP_DISABLE,
        .master.clk_speed = I2C_MASTER_MAX_SPEED,
        .clk_flags = 0
    };

    i2c_param_config(
        I2C_ESP_NUM_FOR_COMPASS_MODULE,
        &i2c_config_master_compass
    );

    i2c_driver_install(
        I2C_ESP_NUM_FOR_COMPASS_MODULE,
        I2C_ESP_MODE_WITH_COMPASS_MODULE,
        0, // As we are the master, we don't need the buffer
        0, // As we are the master, we don't need the buffer
        0  // Use of flags for interruptions
    );

    //Set value in "Configuration Register B"
	// i2c_cmd_compass_module = i2c_cmd_link_create();
	// i2c_master_start(i2c_cmd_compass_module);
	// i2c_master_write_byte(i2c_cmd_compass_module, (I2C_COMPASS_MODULE_ADDRESS << 1) | I2C_MASTER_WRITE, 1);
	// i2c_master_write_byte(i2c_cmd_compass_module, 0x00, 1); // 0x00 = "Configuration Register A"
	// i2c_master_write(i2c_cmd_compass_module, (uint8_t) 0x54, 1, 1); // 0x54 = 0101 0100 configuration
	// i2c_master_stop(i2c_cmd_compass_module);
	// i2c_master_cmd_begin(I2C_ESP_NUM_FOR_COMPASS_MODULE, i2c_cmd_compass_module, 1000/portTICK_PERIOD_MS);
	// i2c_cmd_link_delete(i2c_cmd_compass_module);
}

void destroy_i2c_config_compass_module(){
    i2c_driver_delete(I2C_ESP_NUM_FOR_COMPASS_MODULE);
}

float read_compass_module(){
    uint8_t data[6];
    // //Set active registert to "Data Output X MSB Register"
    // i2c_cmd_compass_module = i2c_cmd_link_create();
    // i2c_master_start(i2c_cmd_compass_module);
    // i2c_master_write_byte(i2c_cmd_compass_module, (I2C_COMPASS_MODULE_ADDRESS << 1) | I2C_MASTER_WRITE, 1);
    // i2c_master_write_byte(i2c_cmd_compass_module, 0x03, 0); //0x03 = "Data Output X MSB Register"
    // i2c_master_stop(i2c_cmd_compass_module);
    // i2c_master_cmd_begin(I2C_ESP_NUM_FOR_COMPASS_MODULE, i2c_cmd_compass_module, pdMS_TO_TICKS(1000));
    // i2c_cmd_link_delete(i2c_cmd_compass_module);

    //Read values for X, Y and Z
    i2c_cmd_compass_module = i2c_cmd_link_create();
    i2c_master_start(i2c_cmd_compass_module);
    i2c_master_write_byte(i2c_cmd_compass_module, (I2C_COMPASS_MODULE_ADDRESS << 1) | I2C_MASTER_READ, 1);
    i2c_master_write_byte(i2c_cmd_compass_module, 0x03, 1);
    i2c_master_read_byte(i2c_cmd_compass_module, data,   0); //"Data Output X MSB Register"
    i2c_master_read_byte(i2c_cmd_compass_module, data+1, 0); //"Data Output X LSB Register"
    i2c_master_read_byte(i2c_cmd_compass_module, data+2, 0); //"Data Output Z MSB Register"
    i2c_master_read_byte(i2c_cmd_compass_module, data+3, 0); //"Data Output Z LSB Register"
    i2c_master_read_byte(i2c_cmd_compass_module, data+4, 0); //"Data Output Y MSB Register"
    i2c_master_read_byte(i2c_cmd_compass_module, data+5, 0); //"Data Output Y LSB Register "
    i2c_master_stop(i2c_cmd_compass_module);

    i2c_master_cmd_begin(
        I2C_ESP_MODE_WITH_COMPASS_MODULE,
        i2c_cmd_compass_module,
        pdMS_TO_TICKS(20)
    );

    i2c_cmd_link_delete(i2c_cmd_compass_module);

    short x = data[0] << 8 | data[1];
    short z = data[2] << 8 | data[3];
    short y = data[4] << 8 | data[5];
    int angle = atan2((double)y,(double)x) * (180 / 3.14159265) + 180; // angle in degrees

    printf("angle: %d, x: %d, y: %d, z: %d\n", angle, x, y, z);

    return angle;
}
