#include "ledc_servo_motor.h"


void initialize_ledc_servo(){
    servo_duty = SERVO_MIN_DUTY;
    servo_delta = SERVO_MAX_DUTY - SERVO_MIN_DUTY;

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

void set_servo_angle(int target_angle, int transition_time){
    ledc_set_fade_with_time(
        LEDC_HIGH_SPEED_MODE,
        LEDC_CHANNEL_0,
        (uint16_t) (servo_duty + (servo_delta*(target_angle/180.0))),
        transition_time
    );
    ledc_fade_start(
        LEDC_HIGH_SPEED_MODE,
        LEDC_CHANNEL_0,
        LEDC_FADE_WAIT_DONE
    );
}

void set_servo_middle_angle(){
    set_servo_angle(MIDDLE_ANGLE, 1000);
    // printf("Servo in angle: %d\n", MIDDLE_ANGLE);
}

void set_servo_full_angle(){
    set_servo_angle(FULL_ANGLE, 1000);
    // printf("Servo in angle: %d\n", FULL_ANGLE);
}

void set_servo_zero_angle(){
    set_servo_angle(ZERO_ANGLE, 2000);
    // printf("Servo in angle: %d\n", ZERO_ANGLE);
}
