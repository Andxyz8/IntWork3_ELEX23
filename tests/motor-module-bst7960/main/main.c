#include <stdio.h>
#include <stdlib.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_log.h"
// #include "driver/mcpwm_prelude.h"
#include "driver/mcpwm.h"

mcpwm_unit_t UNIDADE_PWM = MCPWM_UNIT_0;
mcpwm_timer_t TIMER_PWM = MCPWM_TIMER_0;
mcpwm_io_signals_t LPWM_SIGNAL = MCPWM0A;
mcpwm_io_signals_t RPWM_SIGNAL = MCPWM0B;
mcpwm_generator_t FGEN_PWM = MCPWM_GEN_A;
mcpwm_generator_t RGEN_PWM = MCPWM_GEN_B;

// Pinos de conexão
const int RPWM_PIN = 21;
const int LPWM_PIN = 22;

void para_movimento_motor_x_seg(int tempo_segundos);

void app_main(void){

    // Configuração dos pinos do PWM do motor
    mcpwm_gpio_init(UNIDADE_PWM, LPWM_SIGNAL, LPWM_PIN);
    mcpwm_gpio_init(UNIDADE_PWM, RPWM_SIGNAL, RPWM_PIN);

    // Configuração do timer
    mcpwm_config_t timer_config = {
        .frequency = 1000,
        .cmpr_a = 0.0,
        .cmpr_b = 0.0,
        .duty_mode = MCPWM_DUTY_MODE_0,
        .counter_mode = MCPWM_TIMER_COUNT_MODE_UP,
    };

    // Inicializa o módulo de PWM da ESP
    mcpwm_init(UNIDADE_PWM, MCPWM_TIMER_0, &timer_config);

    para_movimento_motor_x_seg(2);

    // Teste de movimentação do motor no sentido forward por 3 segundos
    printf("FORWARD\n");
    mcpwm_set_duty(UNIDADE_PWM, TIMER_PWM, FGEN_PWM, 25.0); // PWM FORWARD duty = 25.0%
    mcpwm_set_duty(UNIDADE_PWM, TIMER_PWM, RGEN_PWM, 0.0); // PWM REVERSE parado
    vTaskDelay(3000 / portTICK_PERIOD_MS);

    // Teste de movimentação do motor no sentido reverse por 3 segundos
    printf("REVERSE\n");
    mcpwm_set_duty(UNIDADE_PWM, TIMER_PWM, FGEN_PWM, 0.0); // PWM FORWARD parado
    mcpwm_set_duty(UNIDADE_PWM, TIMER_PWM, RGEN_PWM, 35.0); // PWM REVERSE duty = 35.0%
    vTaskDelay(3000 / portTICK_PERIOD_MS);

    para_movimento_motor_x_seg(2);

    int delay = 100;

    printf("FORWARD CADENCIADO\n");
    for (int i = 1; i <= 100; i++){
        printf("FORWARD AUMENTANDO: i = %d\n", i);
        mcpwm_set_duty(UNIDADE_PWM, TIMER_PWM, FGEN_PWM, i); // PWM FORWARD
        mcpwm_set_duty(UNIDADE_PWM, TIMER_PWM, RGEN_PWM, 0.0); // PWM REVERSE parado
        vTaskDelay(delay / portTICK_PERIOD_MS);
    }

    for (int i = 1; i <= 100; i++){
        printf("FORWARD DIMINUINDO: i = %d\n", (100-i));
        mcpwm_set_duty(UNIDADE_PWM, TIMER_PWM, FGEN_PWM, (100-i)); // PWM FORWARD
        mcpwm_set_duty(UNIDADE_PWM, TIMER_PWM, RGEN_PWM, 0.0); // PWM REVERSE parado
        vTaskDelay(delay / portTICK_PERIOD_MS);
    }

    para_movimento_motor_x_seg(2);
    printf("REVERSE CADENCIADO\n");
    for (int i = 1; i <= 100; i++){
        printf("REVERSE AUMENTANDO: i = %d\n", i);
        mcpwm_set_duty(UNIDADE_PWM, TIMER_PWM, FGEN_PWM, 0.0); // PWM FORWARD
        mcpwm_set_duty(UNIDADE_PWM, TIMER_PWM, RGEN_PWM, i); // PWM REVERSE parado
        vTaskDelay(delay / portTICK_PERIOD_MS);
    }

    for (int i = 1; i <= 100; i++){
        printf("REVERSE DIMINUINDO: i = %d\n", (100-i));
        mcpwm_set_duty(UNIDADE_PWM, TIMER_PWM, FGEN_PWM, 0.0); // PWM FORWARD
        mcpwm_set_duty(UNIDADE_PWM, TIMER_PWM, RGEN_PWM, (100-i)); // PWM REVERSE parado
        vTaskDelay(delay / portTICK_PERIOD_MS);
    }

    para_movimento_motor_x_seg(1);
}


/**
 * @brief Função para parar o motor por x segundos.
 * 
 * @param tempo_segundos Tempo em segundos para deixar o motor parado.
*/
void para_movimento_motor_x_seg(int tempo_segundos){
    // Define o como 0 o duty para ambos os pinos PWM do motor por 1 seg
    mcpwm_set_duty(UNIDADE_PWM, TIMER_PWM, FGEN_PWM, 0.0);
    mcpwm_set_duty(UNIDADE_PWM, TIMER_PWM, RGEN_PWM, 0.0);
    vTaskDelay((tempo_segundos * 1000) / portTICK_PERIOD_MS);
}