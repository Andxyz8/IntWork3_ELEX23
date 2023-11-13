#include "byte_operator.h"

uint8_t* float_to_bytes(float float_value) {
    uint8_t *bytes_value = (uint8_t *) malloc(4);
    memcpy(bytes_value, (uint8_t *) (&float_value), 4);

    return bytes_value;
}

float bytes_to_float(uint8_t *bytes_value) {
    float *float_value = (float *) malloc (sizeof(float));

    memcpy(float_value, bytes_value, 4);

    return *float_value;
}

uint8_t* int_to_bytes(int int_value){
    uint8_t *bytes_value = (uint8_t *) malloc(4);

    memcpy(bytes_value, (uint8_t *) (&int_value), 4);

    return bytes_value;
}