// This module contains the constants used in the project

#ifndef UTILS_CONSTANTS_H
#define UTILS_CONSTANTS_H

#include "freertos/FreeRTOS.h"
#include "driver/i2c.h"


// ***** I2C RASPBERRY RELATED CONSTANTS ***** //

// Defines the GPIO pin for I2C SDA Raspberry Pi
#define GPIO_21_I2C_SDA_RPI 21

// Defines the GPIO pin for I2C SCL with Raspberry Pi
#define GPIO_22_I2C_SCL_RPI 22

// Defines the I2C slave address on Raspberry Pi
#define I2C_SLAVE_ADDRESS_RASP 0x18

// Defines the max speed for the I2C slave with Raspberry Pi
#define I2C_SLAVE_MAX_SPEED 1000

// Defines master port for ESP I2C communication with Raspberry Pi
#define I2C_MASTER_PORT 0

// Defines the I2C slave port for the ESP I2C communication with Raspberry Pi
#define I2C_ESP_NUM_FOR_RASPBERRY I2C_NUM_0

// Defines I2C mode for ESP as slave with Raspberry Pi
#define I2C_ESP_MODE_WITH_RASPBERRY_PI I2C_MODE_SLAVE

// ***** I2C RASPBERRY RELATED CONSTANTS ***** //

// ***** I2C COMPASS MODULE RELATED CONSTANTS ***** //

// Defines the GPIO pin for I2C SDA with Compass Module
#define GPIO_23_I2C_SDA_CMD 21

// Defines the GPIO pin for I2C SCL with Compass Module
#define GPIO_19_I2C_SCL_CMD 22

// Defines the max speed for the I2C master with Compass Module
#define I2C_MASTER_MAX_SPEED 1000

// Defines the I2C slave port for the compass module
#define I2C_COMPASS_MODULE_ADDRESS 0x1E

// Defines the I2C mode with compass module
#define I2C_ESP_MODE_WITH_COMPASS_MODULE I2C_MODE_MASTER

// Defines the I2C number for communicating with compass module
#define I2C_ESP_NUM_FOR_COMPASS_MODULE I2C_NUM_0

// ***** I2C COMPASS MODULE RELATED CONSTANTS ***** //

#endif //UTILS_CONSTANTS_H
