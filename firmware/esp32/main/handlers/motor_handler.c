#include "motor_handler.h"

/**
 * @brief Função para inicializar o módulo de PWM da ESP.
*/
void initialize_motor_pwm(){
    performing_movement = false;
    // Configuração dos pinos do PWM do motor
    mcpwm_gpio_init(PWM_UNIT_LEFT, PWM_LEFT_SIGNAL_LEFT, GPIO_LEFT_SIGNAL_LEFT);
    mcpwm_gpio_init(PWM_UNIT_LEFT, PWM_RIGHT_SIGNAL_LEFT, GPIO_RIGHT_SIGNAL_LEFT);

    mcpwm_gpio_init(PWM_UNIT_RIGHT, PWM_LEFT_SIGNAL_RIGHT, GPIO_LEFT_SIGNAL_RIGHT);
    mcpwm_gpio_init(PWM_UNIT_RIGHT, PWM_RIGHT_SIGNAL_RIGHT, GPIO_RIGHT_SIGNAL_RIGHT);

    // Configuração do timer
    mcpwm_config_t timer_config = {
        .frequency = 1000,
        .cmpr_a = 0.0,
        .cmpr_b = 0.0,
        .duty_mode = PWM_DUTY_MODE,
        .counter_mode = PWM_COUNTER_MODE,
    };

    // Inicializa o módulo de PWM da ESP
    mcpwm_init(PWM_UNIT_LEFT, PWM_TIMER_LEFT, &timer_config);

    mcpwm_init(PWM_UNIT_RIGHT, PWM_TIMER_RIGHT, &timer_config);
}

/**
 * @brief Function to stop the motor for a certain time in seconds.
 * 
 * @param time_in_secs (int) Time in second to let the motor stopped.
*/
void stop_motor_movement_x_seg(int time_in_secs){
    // Define o como 0 o duty para ambos os pinos PWM do motor
    mcpwm_set_duty(PWM_UNIT_LEFT, PWM_TIMER_LEFT, PWM_GEN_F, 0.0);
    mcpwm_set_duty(PWM_UNIT_LEFT, PWM_TIMER_LEFT, PWM_GEN_R, 0.0);

    mcpwm_set_duty(PWM_UNIT_RIGHT, PWM_TIMER_RIGHT, PWM_GEN_F, 0.0);
    mcpwm_set_duty(PWM_UNIT_RIGHT, PWM_TIMER_RIGHT, PWM_GEN_R, 0.0);
    vTaskDelay((time_in_secs * 1000) / portTICK_PERIOD_MS);
}

/**
 * @brief Function to power on both motors and perform a forward movimentation.
 * 
 * @param speed (float) Speed that both motors will perform the movement.
 * @param time_in_secs (int) Time in seconds to be performing the movement.
*/
void move_forward(float pwm_left, float pwm_right, int time_in_secs){
    performing_movement = true;
    mcpwm_set_duty(PWM_UNIT_RIGHT, PWM_TIMER_RIGHT, PWM_GEN_F, pwm_right);
    mcpwm_set_duty(PWM_UNIT_RIGHT, PWM_TIMER_RIGHT, PWM_GEN_R, 0.0);
    mcpwm_set_duty(PWM_UNIT_LEFT, PWM_TIMER_LEFT, PWM_GEN_F, pwm_left);
    mcpwm_set_duty(PWM_UNIT_LEFT, PWM_TIMER_LEFT, PWM_GEN_R, 0.0);
    vTaskDelay((time_in_secs * 1000) / portTICK_PERIOD_MS);
}

/**
 * @brief Function to power on both motors in the opposite way
 * and perform a backwards movimentation.
 * 
 * @param speed (float) Speed that both motors will perform the movement.
 * @param time_in_secs (int) Time in seconds to be performing the movement.
*/
void move_backward(float speed, int time_in_secs){
    performing_movement = true;
    mcpwm_set_duty(PWM_UNIT_LEFT, PWM_TIMER_LEFT, PWM_GEN_F, 0.0);
    mcpwm_set_duty(PWM_UNIT_LEFT, PWM_TIMER_LEFT, PWM_GEN_R, speed);

    mcpwm_set_duty(PWM_UNIT_RIGHT, PWM_TIMER_RIGHT, PWM_GEN_F, 0.0);
    mcpwm_set_duty(PWM_UNIT_RIGHT, PWM_TIMER_RIGHT, PWM_GEN_R, speed);
    vTaskDelay((time_in_secs * 1000) / portTICK_PERIOD_MS);
}

/**
 * @brief Function to power more right motor than left motor 
 * at a certain speed for some seconds.
 * 
 * @param speed (float) Speed that the motor will perform the movement.
 * @param time_in_secs (int) Time in second to be performing the movement.
*/
void rotate_left(float speed, int time_in_secs){
    performing_movement = true;
    mcpwm_set_duty(PWM_UNIT_LEFT, PWM_TIMER_LEFT, PWM_GEN_F, 0.0);
    mcpwm_set_duty(PWM_UNIT_LEFT, PWM_TIMER_LEFT, PWM_GEN_R, 0.0);

    mcpwm_set_duty(PWM_UNIT_RIGHT, PWM_TIMER_RIGHT, PWM_GEN_F, speed);
    mcpwm_set_duty(PWM_UNIT_RIGHT, PWM_TIMER_RIGHT, PWM_GEN_R, 0.0);
    vTaskDelay((time_in_secs * 1000) / portTICK_PERIOD_MS);
}

/**
 * @brief Function to power more left motor than right motor 
 * at a certain speed for some seconds.
 * 
 * @param speed (float) Speed that the motor will perform the movement.
 * @param time_in_secs (int) Time in second to be performing the movement.
*/
void rotate_right(float speed, int time_in_secs){
    performing_movement = true;
    TickType_t delayzao = ((time_in_secs * 1000) / portTICK_PERIOD_MS);

    mcpwm_set_duty(PWM_UNIT_LEFT, PWM_TIMER_LEFT, PWM_GEN_F, speed);
    mcpwm_set_duty(PWM_UNIT_LEFT, PWM_TIMER_LEFT, PWM_GEN_R, 0.0);

    mcpwm_set_duty(PWM_UNIT_RIGHT, PWM_TIMER_RIGHT, PWM_GEN_F, 0.0);
    mcpwm_set_duty(PWM_UNIT_RIGHT, PWM_TIMER_RIGHT, PWM_GEN_R, 0.0);
    vTaskDelay(delayzao);
}
