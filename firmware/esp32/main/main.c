// OWN LIBRARIES IMPORTS
#include "main.h"


QueueHandle_t task_handler_interrupt_queue;
i2c_cmd_handle_t i2c_cmd_compass_module;
mcpwm_config_t pwm_timer_config;
int servo_duty;
int servo_delta;

void app_main(){
    // // IF DIFFERENT FROM 1, PAY ATTENTION TO THIS AND CHECK THE REASON
    printf("LAST RESTART REASON: %d.\n", esp_reset_reason());
    printf("STARTING ESP32 FIRMWARE.\n");

    printf("STARTING I2C HANDLER.\n");
    i2c_handler_initialize();
    printf("FINISHED STARTING I2C HANDLER.\n");

    printf("STARTING TASK HANDLER.\n");
    // // Defines the task queue for interruptions
    task_handler_interrupt_queue = xQueueCreate(10, sizeof(int));
    printf("FINISHED STARTING TASK HANDLER.\n");

    printf("STARTING MOTOR PWM HANDLER.\n");
    initialize_motor_pwm();
    printf("FINISHED STARTING MOTOR PWM HANDLER.\n");

    printf("STARTING LEDC SERVO PWM HANDLER.\n");
    initialize_ledc_servo();
    printf("FINISHED STARTING LEDC SERVO PWM HANDLER.\n");

    printf("STARTING COMPASS MODULE PWM HANDLER.\n");
    init_i2c_config_compass_module();
    printf("FINISHED STARTING COMPASS MODULE PWM HANDLER.\n");

    // D13
    printf("STARTING STARTING BUZZER.\n");
    init_buzzer_config();
    printf("FINISHED STARTING BUZZER.\n");

    printf("STARTING TASK HANDLER.\n");
    initialize_interruption_handler();
    printf("FINISHED TASK HANDLER.\n");

    printf("FINISHED STARTING ESP32 FIRMWARE.\n");
}
