// This module contains the constants used in the project

#ifndef UTILS_CONSTANTS_H
#define UTILS_CONSTANTS_H

#include "freertos/FreeRTOS.h"
#include "driver/i2c.h"
#include "driver/mcpwm.h"


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
#define GPIO_23_I2C_SDA_CMD 21 // TODO: change this pin

// Defines the GPIO pin for I2C SCL with Compass Module
#define GPIO_19_I2C_SCL_CMD 22 // TODO: change this pin

// Defines the max speed for the I2C master with Compass Module
#define I2C_MASTER_MAX_SPEED 1000

// Defines the I2C slave port for the compass module
#define I2C_COMPASS_MODULE_ADDRESS 0x1E

// Defines the I2C mode with compass module
#define I2C_ESP_MODE_WITH_COMPASS_MODULE I2C_MODE_MASTER

// Defines the I2C number for communicating with compass module
#define I2C_ESP_NUM_FOR_COMPASS_MODULE I2C_NUM_1
/*
    TODO: if using i2c, must be different
    from raspberry and esp32 communication i2c_num
*/ 

// ***** I2C COMPASS MODULE RELATED CONSTANTS ***** //


// ***** BUZZER RELATED CONSTANTS ***** //

#define GPIO_18_BUZZER 18

// ***** BUZZER RELATED CONSTANTS ***** //


// ***** PWM LEFT MOTOR RELATED CONSTANTS ***** //

#define PWM_UNIT_LEFT MCPWM_UNIT_0

#define PWM_TIMER_LEFT MCPWM_TIMER_0

#define PWM_LEFT_SIGNAL_LEFT MCPWM0A

#define PWM_RIGHT_SIGNAL_LEFT MCPWM0B

#define GPIO_LEFT_SIGNAL_LEFT 14

#define GPIO_RIGHT_SIGNAL_LEFT 12

// ***** PWM LEFT MOTOR RELATED CONSTANTS ***** //

#define PWM_GEN_F MCPWM_GEN_B

#define PWM_GEN_R MCPWM_GEN_A

#define PWM_DUTY_MODE MCPWM_DUTY_MODE_0

#define PWM_COUNTER_MODE MCPWM_TIMER_COUNT_MODE_UP

// ***** PWM RIGHT MOTOR RELATED CONSTANTS ***** //

#define PWM_UNIT_RIGHT MCPWM_UNIT_1

#define PWM_TIMER_RIGHT MCPWM_TIMER_1

#define PWM_LEFT_SIGNAL_RIGHT MCPWM1A

#define PWM_RIGHT_SIGNAL_RIGHT MCPWM1B

#define GPIO_LEFT_SIGNAL_RIGHT 26

#define GPIO_RIGHT_SIGNAL_RIGHT 27

// ***** PWM RIGHT MOTOR RELATED CONSTANTS ***** //


#endif // UTILS_CONSTANTS_H
