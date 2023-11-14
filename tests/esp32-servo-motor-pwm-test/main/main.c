/*
 * ADAPTED FROM: https://github.com/sankarcheppali/esp_idf_esp32_posts/blob/master/gradient_servo/main/gradient_servo.c
*/

#include <stdio.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/queue.h"
#include "driver/ledc.h"
#include "sdkconfig.h"
#include "esp_log.h"

#define SERVO_GPIO GPIO_NUM_19
#define SERVO_MIN_DUTY 900  // micro seconds (uS), for 0
#define SERVO_MAX_DUTY  3800 // micro seconds (uS),for 180
#define SERVO_TRANSITION_TIME 1000 // in ms
#define SERVO_TIME_PERIOD 5000 // in ms
#define FULL_ANGLE 180
#define MIDDLE_ANGLE 90
#define ZERO_ANGLE 0

int servo_duty;
int servo_delta;

void configureServo(){	
	ledc_timer_config_t timer_config = {
	    .duty_resolution = LEDC_TIMER_15_BIT,
	    .freq_hz    = 50,
	    .speed_mode = LEDC_HIGH_SPEED_MODE,
	    .timer_num  = LEDC_TIMER_0,
        .clk_cfg = LEDC_AUTO_CLK
    };
	ledc_timer_config(&timer_config);

	ledc_channel_config_t ledc_config = {
	    .channel    = LEDC_CHANNEL_0,
	    .duty       = servo_duty,
	    .gpio_num   = SERVO_GPIO,
	    .intr_type  = LEDC_INTR_DISABLE,
	    .speed_mode = LEDC_HIGH_SPEED_MODE,
	    .timer_sel  = LEDC_TIMER_0
    };

	ledc_channel_config(&ledc_config);
	ledc_fade_func_install(0);
}

void setServoAngle(int target_angle, int transition_time){
    ledc_set_fade_with_time(
        LEDC_HIGH_SPEED_MODE,
        LEDC_CHANNEL_0,
        (uint16_t) (servo_duty + (servo_delta*(target_angle/180.0))),
        transition_time
    );
    ledc_fade_start(LEDC_HIGH_SPEED_MODE, LEDC_CHANNEL_0,LEDC_FADE_WAIT_DONE);
}

void app_main(){
    servo_duty = SERVO_MIN_DUTY ; 
    servo_delta = SERVO_MAX_DUTY - SERVO_MIN_DUTY;
    configureServo();
    while(1){
            setServoAngle(MIDDLE_ANGLE, 1000);
            printf("Servo in angle: %d\n", MIDDLE_ANGLE);
            vTaskDelay(pdMS_TO_TICKS(SERVO_TIME_PERIOD));

            setServoAngle(FULL_ANGLE, 1000);
            printf("Servo in angle: %d\n", FULL_ANGLE);
            vTaskDelay(pdMS_TO_TICKS(SERVO_TIME_PERIOD));

            setServoAngle(ZERO_ANGLE, 2000);
            printf("Servo in angle: %d\n", ZERO_ANGLE);
            vTaskDelay(pdMS_TO_TICKS(SERVO_TIME_PERIOD));

            setServoAngle(MIDDLE_ANGLE, 1000);
            printf("Servo in angle: %d\n", MIDDLE_ANGLE);
            vTaskDelay(pdMS_TO_TICKS(SERVO_TIME_PERIOD));
    }
    // xTaskCreate(&gradientServoTask, "servo_task", 2048, NULL, 5, NULL);
}
