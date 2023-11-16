#include "taskHandler.h"


static void IRAM_ATTR gpio_interruption_handler(void *args){
    // Receive the pin_number that activated the interruption
    int pin_number = (int) args;

    // Send the pin_number to the queue to be treated by the controller
    xQueueSendFromISR(task_handler_interrupt_queue, &pin_number, NULL);
}

void task_controller(void *params){
    // Declare variable to receive the interruption pin_number
    int pin_number;

    // Interruption handling functions must always be in a infinite loop
    while (true) {
        // Check if there is any interruption to be treated in the queue
        if (xQueueReceive(task_handler_interrupt_queue, &pin_number, portMAX_DELAY)) {
            printf("PINNUMBER ACTIVATED: %d\n", pin_number);

            // if the interruption pin_number is from the i2c communication
            if (pin_number == GPIO_21_I2C_SDA_RPI){
                printf("PINNUMBER FUNCTION: %d\n", pin_number);

                // receive the command from raspberry
                uint8_t *command_received;
                command_received = i2c_handler_receive_command();
                printf("COMMAND RECEIVED: %c%c\n", command_received[0], command_received[1]);

                // compare command_received with possible commands
                // command: 'ct' -> communication test
                if ((char) command_received[0] == 'c' && (char) command_received[1] == 't') {
                    printf("COMMAND RESPONSE FOR COMMUNICATION TEST: ct\n");
                    // send information asked to raspberry
                    i2c_handler_send_data((uint8_t *) "OKOK");
                }

                if ((char) command_received[0] == 'm' && (char) command_received[1] == 'f') {
                    printf("COMMAND RESPONSE FOR MOVE FORWARD: mf\n");
                    
                    move_forward(48, 50, 1);
                    stop_motor_movement_x_seg(1);

                    // send information asked to raspberry
                    i2c_handler_send_data((uint8_t *) "MFOK");
                }

                if ((char) command_received[0] == 'f' && (char) command_received[1] == 'f') {
                    printf("COMMAND RESPONSE FOR MOVE FORWARD FINE: ff\n");
                    
                    float left_float = i2c_handler_receive_float();
                    float right_float = i2c_handler_receive_float();

                    float time_in_secs_float = i2c_handler_receive_float();

                    // receive a float from i2chandler and store in a int variable
                    int time_in_secs = (int) time_in_secs_float;

                    move_forward_fine(left_float, right_float, time_in_secs);
                    stop_motor_movement_x_seg(1);

                    // send information asked to raspberry
                    i2c_handler_send_data((uint8_t *) "FFOK");
                }

                if ((char) command_received[0] == 'r' && (char) command_received[1] == 'l') {
                    printf("COMMAND RESPONSE FOR ROTATE LEFT: rl\n");
                    
                    rotate_left(40, 1);
                    stop_motor_movement_x_seg(1);

                    // send information asked to raspberry
                    i2c_handler_send_data((uint8_t *) "RLOK");
                }

                if ((char) command_received[0] == 'r' && (char) command_received[1] == 'r') {
                    printf("COMMAND RESPONSE FOR ROTATE RIGHT: rr\n");

                    rotate_right(40, 1);
                    stop_motor_movement_x_seg(1);

                    // send information asked to raspberry
                    i2c_handler_send_data((uint8_t *) "RROK");
                }

                // command: 'rc' -> read compass module
                if ((char) command_received[0] == 'r' && (char) command_received[1] == 'c') {
                    printf("COMMAND RESPONSE FOR READ COMPASS MODULE: rc\n");
                    // get the compass value
                    int compass_value = get_compass_module_degrees();

                    // convert compass value to bytes
                    uint8_t *bytes_compass_value;
                    bytes_compass_value = int_to_bytes(compass_value);

                    // for (int i = 0; i < 4; i++){
                    //     printf("BYTE %d: %d\n", i, bytes_compass_value[i]);
                    // }

                    // send information asked to raspberry
                    i2c_handler_send_data(bytes_compass_value);
                }

                if ((char) command_received[0] == 's' && (char) command_received[1] == 'm') {
                    printf("COMMAND RESPONSE FOR SET SERVO MIDDLE ANGLE: sm\n");
                    // set servo middle angle
                    set_servo_middle_angle();

                    // send information asked to raspberry
                    i2c_handler_send_data((uint8_t *) "SMOK");
                }

                if ((char) command_received[0] == 's' && (char) command_received[1] == 'f') {
                    printf("COMMAND RESPONSE FOR SET SERVO FULL ANGLE: sf\n");
                    // set servo full angle
                    set_servo_full_angle();

                    // send information asked to raspberry
                    i2c_handler_send_data((uint8_t *) "SFOK");
                }

                if ((char) command_received[0] == 's' && (char) command_received[1] == 'z') {
                    printf("COMMAND RESPONSE FOR SET SERVO ZERO ANGLE: sz\n");
                    // set servo zero angle
                    set_servo_zero_angle();

                    // send information asked to raspberry
                    i2c_handler_send_data((uint8_t *) "SZOK");
                }

                if ((char) command_received[0] == 'o' && (char) command_received[1] == 'b') {
                    printf("COMMAND RESPONSE FOR TURN ON BUZZER: ob\n");
                    // turn off buzzer
                    turn_on_buzzer();

                    // send information asked to raspberry
                    i2c_handler_send_data((uint8_t *) "BZOK");
                }
                free(command_received);
                printf("ENCERRANDO TRATAMENTO DA INTERRUPCAO\n");
            }
        }

        printf("ENCERRANDO LOOP INTERRUPCAO\n");
        // vTaskDelayUntil(NULL, pdMS_TO_TICKS(100));
    }
}


void initialize_interruption_handler(){
    // Defines the controller for interruptions
    xTaskCreate(
        task_controller,
        "task_controller",
        8192,
        NULL,
        1,
        NULL
    );

    gpio_install_isr_service(0);

    // define the handler for the interruptions
    gpio_isr_handler_add(
        GPIO_21_I2C_SDA_RPI,
        gpio_interruption_handler,
        (void *) GPIO_21_I2C_SDA_RPI
    );
}