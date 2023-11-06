#include <stdio.h>
#include <stdlib.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_log.h"
// #include "driver/mcpwm_prelude.h"
#include "driver/mcpwm.h"

// Pinos de PWM/conexão - Esquerda
mcpwm_unit_t UNIDADE_PWM_ESQ = MCPWM_UNIT_0;
mcpwm_timer_t TIMER_PWM_ESQ = MCPWM_TIMER_0;
mcpwm_io_signals_t LPWM_SIGNAL_ESQ = MCPWM0A;
mcpwm_io_signals_t RPWM_SIGNAL_ESQ = MCPWM0B;

const int LPWM_PIN_ESQ = 14;
const int RPWM_PIN_ESQ = 12;


// Pinos de PWM/conexão - Direita
mcpwm_unit_t UNIDADE_PWM_DIR = MCPWM_UNIT_1;
mcpwm_timer_t TIMER_PWM_DIR = MCPWM_TIMER_1;
mcpwm_io_signals_t LPWM_SIGNAL_DIR = MCPWM1A;
mcpwm_io_signals_t RPWM_SIGNAL_DIR = MCPWM1B;

const int LPWM_PIN_DIR = 26;
const int RPWM_PIN_DIR = 27;

mcpwm_generator_t FGEN_PWM = MCPWM_GEN_B;
mcpwm_generator_t RGEN_PWM = MCPWM_GEN_A;

void para_movimento_motor_x_seg(int tempo_segundos);

void goForward(double velocidade, int tempo_segundos);
void goBack(double velocidade, int tempo_segundos);
void goLeft(double velocidade, int tempo_segundos);
void goRight(double velocidade, int tempo_segundos);

void app_main(void){

    // Configuração dos pinos do PWM do motor
    mcpwm_gpio_init(UNIDADE_PWM_ESQ, LPWM_SIGNAL_ESQ, LPWM_PIN_ESQ);
    mcpwm_gpio_init(UNIDADE_PWM_ESQ, RPWM_SIGNAL_ESQ, RPWM_PIN_ESQ);

    mcpwm_gpio_init(UNIDADE_PWM_DIR, LPWM_SIGNAL_DIR, LPWM_PIN_DIR);
    mcpwm_gpio_init(UNIDADE_PWM_DIR, RPWM_SIGNAL_DIR, RPWM_PIN_DIR);

    // Configuração do timer
    mcpwm_config_t timer_config = {
        .frequency = 1000,
        .cmpr_a = 0.0,
        .cmpr_b = 0.0,
        .duty_mode = MCPWM_DUTY_MODE_0,
        .counter_mode = MCPWM_TIMER_COUNT_MODE_UP,
    };

    // Inicializa o módulo de PWM da ESP
    mcpwm_init(UNIDADE_PWM_ESQ, MCPWM_TIMER_0, &timer_config);

    mcpwm_init(UNIDADE_PWM_DIR, MCPWM_TIMER_1, &timer_config);

    para_movimento_motor_x_seg(2);

    goForward(40, 3);
    goBack(40, 3);
    goLeft(40, 3);
    goRight(40, 3);

    para_movimento_motor_x_seg(2);

}


/**
 * @brief Função para parar o motor por x segundos.
 * 
 * @param tempo_segundos Tempo em segundos para deixar o motor parado.
*/
void para_movimento_motor_x_seg(int tempo_segundos){
    // Define o como 0 o duty para ambos os pinos PWM do motor por 1 seg
    mcpwm_set_duty(UNIDADE_PWM_ESQ, TIMER_PWM_ESQ, FGEN_PWM, 0.0);
    mcpwm_set_duty(UNIDADE_PWM_ESQ, TIMER_PWM_ESQ, RGEN_PWM, 0.0);

    mcpwm_set_duty(UNIDADE_PWM_DIR, TIMER_PWM_DIR, FGEN_PWM, 0.0);
    mcpwm_set_duty(UNIDADE_PWM_DIR, TIMER_PWM_DIR, RGEN_PWM, 0.0);
    vTaskDelay((tempo_segundos * 1000) / portTICK_PERIOD_MS);
}

/**
 * @brief Função para andar com o motor para frente por x segundos a uma velocidade x.
 * 
 * @param velocidade Velocidade com que o motor executará o comando
 * @param tempo_segundos Tempo em segundos para deixar o motor parado.
*/
void goForward(double velocidade, int tempo_segundos){

    mcpwm_set_duty(UNIDADE_PWM_ESQ, TIMER_PWM_ESQ, FGEN_PWM, velocidade);
    mcpwm_set_duty(UNIDADE_PWM_ESQ, TIMER_PWM_ESQ, RGEN_PWM, 0.0);

    mcpwm_set_duty(UNIDADE_PWM_DIR, TIMER_PWM_DIR, FGEN_PWM, velocidade);
    mcpwm_set_duty(UNIDADE_PWM_DIR, TIMER_PWM_DIR, RGEN_PWM, 0.0);
    vTaskDelay((tempo_segundos * 1000) / portTICK_PERIOD_MS);
}

/**
 * @brief Função para andar com o motor para trás por x segundos a uma velocidade x.
 * 
 * @param velocidade Velocidade com que o motor executará o comando
 * @param tempo_segundos Tempo em segundos para deixar o motor parado.
*/
void goBack(double velocidade, int tempo_segundos){

    mcpwm_set_duty(UNIDADE_PWM_ESQ, TIMER_PWM_ESQ, FGEN_PWM, 0.0);
    mcpwm_set_duty(UNIDADE_PWM_ESQ, TIMER_PWM_ESQ, RGEN_PWM, velocidade);

    mcpwm_set_duty(UNIDADE_PWM_DIR, TIMER_PWM_DIR, FGEN_PWM, 0.0);
    mcpwm_set_duty(UNIDADE_PWM_DIR, TIMER_PWM_DIR, RGEN_PWM, velocidade);
    vTaskDelay((tempo_segundos * 1000) / portTICK_PERIOD_MS);
}

/**
 * @brief Função para andar com o motor para esquerda por x segundos a uma velocidade x.
 * 
 * @param velocidade Velocidade com que o motor executará o comando
 * @param tempo_segundos Tempo em segundos para deixar o motor parado.
*/
void goLeft(double velocidade, int tempo_segundos){

    mcpwm_set_duty(UNIDADE_PWM_ESQ, TIMER_PWM_ESQ, FGEN_PWM, (velocidade-25.0));
    mcpwm_set_duty(UNIDADE_PWM_ESQ, TIMER_PWM_ESQ, RGEN_PWM, 0.0);

    mcpwm_set_duty(UNIDADE_PWM_DIR, TIMER_PWM_DIR, FGEN_PWM, velocidade);
    mcpwm_set_duty(UNIDADE_PWM_DIR, TIMER_PWM_DIR, RGEN_PWM, 0.0);
    vTaskDelay((tempo_segundos * 1000) / portTICK_PERIOD_MS);
}

/**
 * @brief Função para andar com o motor para direita por x segundos a uma velocidade x.
 * 
 * @param velocidade Velocidade com que o motor executará o comando
 * @param tempo_segundos Tempo em segundos para deixar o motor parado.
*/
void goRight(double velocidade, int tempo_segundos){

    mcpwm_set_duty(UNIDADE_PWM_ESQ, TIMER_PWM_ESQ, FGEN_PWM, velocidade);
    mcpwm_set_duty(UNIDADE_PWM_ESQ, TIMER_PWM_ESQ, RGEN_PWM, 0.0);

    mcpwm_set_duty(UNIDADE_PWM_DIR, TIMER_PWM_DIR, FGEN_PWM, (velocidade-25.0));
    mcpwm_set_duty(UNIDADE_PWM_DIR, TIMER_PWM_DIR, RGEN_PWM, 0.0);
    vTaskDelay((tempo_segundos * 1000) / portTICK_PERIOD_MS);
}
