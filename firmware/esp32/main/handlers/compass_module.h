#ifndef HANDLERS_COMPASS_MODULE_H
#define HANDLERS_COMPASS_MODULE_H

#include <math.h>
#include "utils/constants.h"

extern i2c_cmd_handle_t i2c_cmd_compass_module;

void init_i2c_config_compass_module();

void destroy_i2c_config_compass_module();

void start_command_sequece_write();

void start_command_sequence_read();

void set_compass_module();

void set_compass_module_config();

void end_command_sequence();

void initialize_compass_module();

void read_compass_module_raw_data(uint8_t* raw_data);

int proccess_compass_module_raw_data(uint8_t* raw_data);

int get_compass_module_degrees();

#endif // HANDLERS_COMPASS_MODULE_H