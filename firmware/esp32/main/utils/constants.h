// This module contains the constants used in the project

#ifndef UTILS_CONSTANTS_H
#define UTILS_CONSTANTS_H

#include "freertos/FreeRTOS.h"
#include "driver/i2c.h"


// ***** I2C RELATED CONSTANTS ***** //

// Defines the GPIO pin for I2C SDA
#define GPIO_21_I2C_SDA 21

// Defines the GPIO pin for I2C SCL
#define GPIO_22_I2C_SCL 22

// Defines the I2C slave address on raspberry pi
#define I2C_SLAVE_ADDRESS_RASP 0x18

// Defines the max speed for the I2C slave
#define I2C_SLAVE_MAX_SPEED 1000

// Defines master port for ESP
#define I2C_MASTER_PORT 0

// Defines the I2C slave port for the ESP
#define I2C_SLAVE_PORT I2C_NUM_0

// Defines I2C mode for ESP as slave
#define I2C_ESP_MODE I2C_MODE_SLAVE

// ***** I2C RELATED CONSTANTS ***** //


#endif //UTILS_CONSTANTS_H
