import time
import RPi.GPIO as GPIO

class CameraHandler:
    def __init__(self) -> None:
        pass

    #Set function to calculate percent from angle
    def __angle_to_percent (self, angle) :
        if angle > 180 or angle < 0 :
            return False

        start = 4
        end = 12.5
        ratio = (end - start)/180 #Calcul ratio from angle to percent

        angle_as_percent = angle * ratio

        return start + angle_as_percent

    def turn_servo(self, degrees: int) -> bool:
        GPIO.setmode(GPIO.BOARD) #Use Board numerotation mode
        GPIO.setwarnings(False) #Disable warnings

        #Use pin 12 for PWM signal
        pwm_gpio = 12
        frequence = 50
        GPIO.setup(pwm_gpio, GPIO.OUT)

        # Instantiate pwm for servo
        pwm = GPIO.PWM(pwm_gpio, frequence)
        print("AQUI 1")

        pwm.start(self.__angle_to_percent(90))
        time.sleep(2)

        #Init at 0°
        pwm.start(self.__angle_to_percent(0))
        time.sleep(2)
        print("AQUI 2")

        #Go at 90°
        pwm.ChangeDutyCycle(self.__angle_to_percent(90))
        time.sleep(2)
        print("AQUI 3")

        #Finish at 180°
        pwm.ChangeDutyCycle(self.__angle_to_percent(180))

        time.sleep(2)
        print("AQUI 4")

        pwm.ChangeDutyCycle(self.__angle_to_percent(90))
        time.sleep(2)
        #Close GPIO & cleanup
        pwm.stop()
        GPIO.cleanup()
        print("AQUI 5")
        return True
