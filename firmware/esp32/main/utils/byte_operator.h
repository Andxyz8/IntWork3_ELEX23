#ifndef UTILS_BYTE_OPERATOR_H_
#define UTILS_BYTE_OPERATOR_H_

#include <stdint.h>
#include <string.h>

uint8_t* float_to_bytes(float float_value);
float bytes_to_float(uint8_t *bytes_value);

#endif // UTILS_BYTE_OPERATOR_H_
