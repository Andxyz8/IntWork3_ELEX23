// LIBRARIES IMPORTS


// OWN LIBRARIES IMPORTS
#include "main.h"


QueueHandle_t task_handler_interrupt_queue;


void app_main(){
    // IF DIFFERENT FROM 1, PAY ATTENTION TO THIS AND CHECK THE REASON
    printf("LAST RESTART REASON: %d.\n", esp_reset_reason());
    printf("STARTING ESP32 FIRMWARE.\n");

    printf("STARTING I2C HANDLER.\n");
    i2c_handler_initialize();
    printf("FINISHED STARTING I2C HANDLER.\n");

    printf("STARTING TASK HANDLER.\n");
    // Defines the task queue for interruptions
    task_handler_interrupt_queue = xQueueCreate(10, sizeof(int));

    initialize_interruption_handler();
    printf("FINISHED STARTING TASK HANDLER.\n");
    printf("FINISHED STARTING ESP32 FIRMWARE.\n");
}
