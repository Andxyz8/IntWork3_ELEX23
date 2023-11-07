#include "motor_handler.h"


void initialize_motor_pwm(){
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

void stop_motor_movement_x_seg(int time_in_secs){
    // Define o como 0 o duty para ambos os pinos PWM do motor por 1 seg
    mcpwm_set_duty(PWM_UNIT_LEFT, PWM_TIMER_LEFT, PWM_GEN_F, 0.0);
    mcpwm_set_duty(PWM_UNIT_LEFT, PWM_TIMER_LEFT, PWM_GEN_R, 0.0);

    mcpwm_set_duty(PWM_UNIT_RIGHT, PWM_TIMER_RIGHT, PWM_GEN_F, 0.0);
    mcpwm_set_duty(PWM_UNIT_RIGHT, PWM_TIMER_RIGHT, PWM_GEN_R, 0.0);
    vTaskDelay((time_in_secs * 1000) / portTICK_PERIOD_MS);
}

void move_forward(double speed, int time_in_secs){
    mcpwm_set_duty(PWM_UNIT_LEFT, PWM_TIMER_LEFT, PWM_GEN_F, speed);
    mcpwm_set_duty(PWM_UNIT_LEFT, PWM_TIMER_LEFT, PWM_GEN_R, 0.0);

    mcpwm_set_duty(PWM_UNIT_RIGHT, PWM_TIMER_RIGHT, PWM_GEN_F, speed);
    mcpwm_set_duty(PWM_UNIT_RIGHT, PWM_TIMER_RIGHT, PWM_GEN_R, 0.0);
    vTaskDelay((time_in_secs * 1000) / portTICK_PERIOD_MS);
}