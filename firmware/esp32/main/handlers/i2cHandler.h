#ifndef HANDLERS_I2C_HANDLER_H
#define HANDLERS_I2C_HANDLER_H

#include "utils/constants.h"

void i2c_handler_initialize();
uint8_t* i2c_handler_receive_command();
void i2c_handler_send_data(uint8_t *data_to_send_i2c);

#endif // HANDLERS_I2C_HANDLER_H
