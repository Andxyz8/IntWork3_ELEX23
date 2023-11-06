#ifndef HANDLERS_COMPASS_MODULE_H
#define HANDLERS_COMPASS_MODULE_H

#include <math.h>
#include "utils/constants.h"

extern i2c_cmd_handle_t i2c_cmd_compass_module;

void init_i2c_config_compass_module();

void destroy_i2c_config_compass_module();

float read_compass_module();

#endif // HANDLERS_COMPASS_MODULE_H