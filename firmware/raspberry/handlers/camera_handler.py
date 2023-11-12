"""Module that contains the class to handle camera controlling.

- Handles the camera servo motor to rotate the camera.
- Handles the algorithms to perform face recognition.
- Handles the algorithms to perform movement detection.
"""
# pylint: disable = E1101:no-member, E0611:no-name-in-module, E0401:import-error
from time import time as this_moment, sleep as time_sleep
from uuid import uuid4 as generate_unique_id
import numpy as np
from cv2 import (
    VideoCapture,
    createBackgroundSubtractorMOG2,
    resize,
    waitKey,
    threshold,
    erode,
    dilate,
    findContours,
    contourArea,
    boundingRect,
    rectangle,
    putText,
    imwrite,
    # imshow,
    # destroyAllWindows,
    THRESH_BINARY,
    RETR_EXTERNAL,
    CHAIN_APPROX_SIMPLE,
    FONT_HERSHEY_SIMPLEX
)
from RPi import GPIO

class CameraHandler:

    def __init__(self) -> None:
        self.__pwm_gpio: int = 12
        self.__pwm_frequence: int = 50
        self.__pwm_servo = None
        self.__last_image_unique_id: str = ""

    @property
    def last_image_unique_id(self) -> str:
        """Return the last image unique id.
        """
        return self.__last_image_unique_id

    def __install_camera_servo(self) -> None:
        # Use Board numerotation mode
        GPIO.setmode(GPIO.BOARD)

        # Disable warnings
        GPIO.setwarnings(False)

        GPIO.setup(self.__pwm_gpio, GPIO.OUT)
        self.__pwm_servo = GPIO.PWM(self.__pwm_gpio, self.__pwm_frequence)

    def __uninstall_camera_servo(self) -> None:
        self.__pwm_servo.stop()
        GPIO.cleanup()

    #Set function to calculate percent from angle
    def __angle_to_percent (self, angle) :
        if angle > 180 or angle < 0 :
            return False

        start = 4
        end = 12.5

        # Calculate ratio from angle to percent
        ratio = (end - start)/180

        angle_as_percent = angle * ratio

        return start + angle_as_percent

    def __move_servo_from_center_to_right(self) -> bool:
        """Move the camera to the right side.
        """
        self.__pwm_servo.start(self.__angle_to_percent(90))
        time_sleep(2)
        self.__pwm_servo.start(self.__angle_to_percent(0))
        time_sleep(2)
        return True

    def __move_servo_from_right_to_center(self) -> bool:
        """Move the camera to the front side.
        """
        self.__pwm_servo.ChangeDutyCycle(self.__angle_to_percent(90))
        time_sleep(2)
        return True

    def __move_servo_from_center_to_left(self) -> bool:
        """Move the camera to the left side.
        """
        self.__pwm_servo.ChangeDutyCycle(self.__angle_to_percent(180))
        time_sleep(2)
        return True

    def __move_servo_from_left_to_center(self) -> bool:
        """Move the camera to the initial position, centralized.
        """
        self.__pwm_servo.ChangeDutyCycle(self.__angle_to_percent(90))
        time_sleep(2)
        return True

    def __save_image_locally(self, image_to_save) -> None:
        """Save the image locally.
        """
        self.__last_image_unique_id = str(generate_unique_id())

        path_image_to_save = f"handlers/.imgs/{self.__last_image_unique_id}.jpeg"

        imwrite(path_image_to_save, image_to_save)

    def __detect_movement(self, duration: int) -> bool:
        cap = VideoCapture(0)

        fgbg = createBackgroundSubtractorMOG2(detectShadows = True)

        # Initial time
        start_time = this_moment()

        movement_detected = False

        while (this_moment() - start_time) < start_time + duration:
            success_capturing, image_captured = cap.read()

            # Check if we get the frame
            if success_capturing:
                image_captured = resize(image_captured, (600, 500))
                waitKey(30)
                fgmask = fgbg.apply(image_captured)
                _, thresh = threshold(fgmask.copy(), 180, 255, THRESH_BINARY)
                # creating a kernel of 4*4
                kernel = np.ones((7, 7), np.uint8)
                # applying errosion to avoid any small motion in video
                thresh = erode(thresh, kernel)
                # dilating our image
                thresh = dilate(thresh, None, iterations=6)

                # finding the contours, we are not using the hierarchy return
                contours, _ = findContours(
                    thresh,
                    RETR_EXTERNAL,
                    CHAIN_APPROX_SIMPLE
                )

                for contour in contours:
                    # finding area of contour
                    area = contourArea(contour)
                    # print(area)
                    # if area greater than the specified value the only then we will consider it
                    if area > 1200 and this_moment() - start_time > 1:
                        movement_detected = True
                        # find the rectangle co-ordinates
                        x, y, w, h = boundingRect(contour)
                        # and then dra it to indicate the moving object
                        rectangle(image_captured, (x, y), (x + w, y + h), (255, 0, 255), 3)

                        # Insert text in the image to indicate which part triggered the alarm
                        putText(
                            img = image_captured,
                            text = 'MOTION DETECTED',
                            org = (x, y - 5),
                            fontFace = FONT_HERSHEY_SIMPLEX,
                            fontScale = 0.5,
                            color = (255, 0, 0),
                            thickness = 2
                        )

                        # Save the image locally before send to cloud storage database
                        self.__save_image_locally(image_captured)

                # imshow('frame',img)
                # imshow('frame2', thresh)
                if movement_detected:
                    break

            else:
                break

        cap.release()
        # destroyAllWindows()
        return movement_detected

    def movement_detection_routine(self):
        # TODO: review this part (time_sleep) not working very well
        self.__install_camera_servo()

        self.__move_servo_from_center_to_right()

        movement_detected = self.__detect_movement(5)

        if movement_detected:
            self.__uninstall_camera_servo()
            return movement_detected

        self.__move_servo_from_right_to_center()
        self.__detect_movement(5)
        if movement_detected:
            self.__uninstall_camera_servo()
            return movement_detected

        self.__move_servo_from_center_to_left()
        self.__detect_movement(5)
        if movement_detected:
            self.__uninstall_camera_servo()
            return movement_detected

        self.__move_servo_from_left_to_center()
        self.__uninstall_camera_servo()
        return False

# pylint: enable = E1101:no-member, E0611:no-name-in-module, E0401:import-error
