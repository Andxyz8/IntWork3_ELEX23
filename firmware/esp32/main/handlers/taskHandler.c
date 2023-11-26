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
                uint8_t *raw_data;
                raw_data = read_32_bytes();
                // raw_data = i2c_handler_receive_command();
                printf("COMMAND RECEIVED: %s\n", raw_data);

                // printf("COMMAND ALL BYTES: %s\n", raw_data);
                // compare raw_data with possible commands
                // command: 'ct' -> communication test
                if ((char) raw_data[0] == 'c' && (char) raw_data[1] == 't') {
                    printf("COMMAND RESPONSE FOR COMMUNICATION TEST: ct\n");
                    // send information asked to raspberry
                    i2c_handler_send_data((uint8_t *) "OKOK");
                }

                // TODO: test removing stop motor movement to see if it works more continuously
                if ((char) raw_data[0] == 'm' && (char) raw_data[1] == 'f') {
                    // portDISABLE_INTERRUPTS();
                    // printf("COMMAND RESPONSE FOR MOVE FORWARD: mf\n");
                    
                    move_forward(50, 51, 1);
                    stop_motor_movement_x_seg(0.5);

                    // send information asked to raspberry
                    i2c_handler_send_data((uint8_t *) "MFOK");
                    // portENABLE_INTERRUPTS();
                }

                if ((char) raw_data[0] == 'e' && (char) raw_data[1] == 'f') {
                    portDISABLE_INTERRUPTS();
                    if (!performing_movement){
                        // printf("COMMAND RESPONSE FOR MOVE FORWARD: ef\n");

                        move_forward(50, 53, 1);

                        // send information asked to raspberry
                        i2c_handler_send_data((uint8_t *) "EFOK");
                        // TODO: test including right here to reset rx to exclude repeated queued commands
                        performing_movement = false;
                    } else {
                        // clean the rx buffer
                        // i2c_reset_rx_fifo(I2C_ESP_NUM_FOR_RASPBERRY);
                        // send information asked to raspberry
                        i2c_handler_send_data((uint8_t *) "NOOK");
                    }
                    portENABLE_INTERRUPTS();
                }

                if ((char) raw_data[0] == 'e' && (char) raw_data[1] == 's') {
                    portDISABLE_INTERRUPTS();
                    // printf("COMMAND RESPONSE FOR STOP MOTOR: es\n");

                    stop_motor_movement_x_seg(0.5);

                    // send information asked to raspberry
                    i2c_handler_send_data((uint8_t *) "ESOK");
                    performing_movement = false;
                    portENABLE_INTERRUPTS();
                }

                if ((char) raw_data[0] == 'r' && (char) raw_data[1] == 'l') {
                    // portDISABLE_INTERRUPTS();
                    // printf("COMMAND RESPONSE FOR ROTATE LEFT: rl\n");
                    
                    rotate_left(50, 1.9);
                    stop_motor_movement_x_seg(1);

                    // send information asked to raspberry
                    i2c_handler_send_data((uint8_t *) "RLOK");
                    // portENABLE_INTERRUPTS();
                }

                if ((char) raw_data[0] == 'e' && (char) raw_data[1] == 'l') {
                    portDISABLE_INTERRUPTS();
                    if (!performing_movement){
                        // printf("COMMAND RESPONSE FOR MOVE FORWARD: el\n");

                        rotate_left(50, 0.95);

                        // send information asked to raspberry
                        i2c_handler_send_data((uint8_t *) "ELOK");
                        performing_movement = false;
                    } else {
                        // clean the rx buffer
                        // i2c_reset_rx_fifo(I2C_ESP_NUM_FOR_RASPBERRY);
                        // send information asked to raspberry
                        i2c_handler_send_data((uint8_t *) "NOOK");
                    }
                    portENABLE_INTERRUPTS();
                }

                if ((char) raw_data[0] == 'r' && (char) raw_data[1] == 'r') {
                    // portDISABLE_INTERRUPTS();
                    // printf("COMMAND RESPONSE FOR ROTATE RIGHT: rr\n");

                    rotate_right(50, 1.9);
                    stop_motor_movement_x_seg(1);

                    // send information asked to raspberry
                    i2c_handler_send_data((uint8_t *) "RROK");
                    // portENABLE_INTERRUPTS();
                }

                if ((char) raw_data[0] == 'e' && (char) raw_data[1] == 'r') {
                    portDISABLE_INTERRUPTS();

                    if (!performing_movement){
                        // printf("COMMAND RESPONSE FOR MOVE FORWARD: er\n");

                        rotate_right(50, 0.95);

                        // send information asked to raspberry
                        i2c_handler_send_data((uint8_t *) "EROK");
                        performing_movement = false;
                    } else {
                        // send information asked to raspberry
                        i2c_handler_send_data((uint8_t *) "NOOK");
                    }
                    portENABLE_INTERRUPTS();
                }

                // command: 'rc' -> read compass module
                if ((char) raw_data[0] == 'r' && (char) raw_data[1] == 'c') {
                    printf("COMMAND RESPONSE FOR READ COMPASS MODULE: rc\n");
                    // get the compass value
                    int compass_value = get_compass_module_degrees();

                    // convert compass value to bytes
                    uint8_t *bytes_compass_value;
                    bytes_compass_value = int_to_bytes(compass_value);

                    // send information asked to raspberry
                    i2c_handler_send_data(bytes_compass_value);
                }

                if ((char) raw_data[0] == 's' && (char) raw_data[1] == 'm') {
                    printf("COMMAND RESPONSE FOR SET SERVO MIDDLE ANGLE: sm\n");
                    // set servo middle angle
                    set_servo_middle_angle();

                    // send information asked to raspberry
                    i2c_handler_send_data((uint8_t *) "SMOK");
                }

                if ((char) raw_data[0] == 's' && (char) raw_data[1] == 'f') {
                    printf("COMMAND RESPONSE FOR SET SERVO FULL ANGLE: sf\n");
                    // set servo full angle
                    set_servo_full_angle();

                    // send information asked to raspberry
                    i2c_handler_send_data((uint8_t *) "SFOK");
                }

                if ((char) raw_data[0] == 's' && (char) raw_data[1] == 'z') {
                    printf("COMMAND RESPONSE FOR SET SERVO ZERO ANGLE: sz\n");
                    // set servo zero angle
                    set_servo_zero_angle();

                    // send information asked to raspberry
                    i2c_handler_send_data((uint8_t *) "SZOK");
                }

                if ((char) raw_data[0] == 'o' && (char) raw_data[1] == 'b') {
                    printf("COMMAND RESPONSE FOR TURN ON BUZZER: ob\n");
                    // turn off buzzer
                    turn_on_buzzer();

                    // send information asked to raspberry
                    i2c_handler_send_data((uint8_t *) "BZOK");
                }

                if ((char) raw_data[0] == 'i' && (char) raw_data[1] == 'b') {
                    printf("COMMAND RESPONSE FOR TURN OFF BUZZER: ob\n");
                    // turn off buzzer
                    turn_off_buzzer();

                    // send information asked to raspberry
                    i2c_handler_send_data((uint8_t *) "BZOK");
                }
                free(raw_data);
                printf("ENCERRANDO TRATAMENTO DA INTERRUPCAO\n");
            }
        }

        printf("ENCERRANDO LOOP INTERRUPCAO\n");
        // vTaskDelayUntil(NULL, pdMS_TO_TICKS(100));
    }
}


void initialize_interruption_handler(){
    // Defines the controller for interruptions
    xTaskCreatePinnedToCore (
        task_controller,
        "task_controller",
        2048,
        NULL,
        5,
        NULL,
        0
    );

    //  xTaskCreate(
    //     task_controller,
    //     "task_controller",
    //     8192,
    //     NULL,
    //     1,
    //     NULL
    // );

    gpio_install_isr_service(0);

    // define the handler for the interruptions
    gpio_isr_handler_add(
        GPIO_21_I2C_SDA_RPI,
        gpio_interruption_handler,
        (void *) GPIO_21_I2C_SDA_RPI
    );
}