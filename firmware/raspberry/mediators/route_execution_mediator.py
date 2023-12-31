from time import sleep as time_sleep
from pandas import DataFrame
from database.database_controller import DatabaseController
from database.notification_controller import NotificationController
from handlers.esp_communication import ESPCommunicationHandler
from handlers.camera_handler import CameraHandler

class RouteExecutionMediator:

    def __init__(
        self,
        ctrl_database: DatabaseController,
        ctrl_notification: NotificationController,
        ctrl_esp_communication: ESPCommunicationHandler,
        ctrl_camera: CameraHandler,
        id_route: int = 1,
        id_robot: int = 1
    ):
        self.__ctrl_database: DatabaseController  = ctrl_database
        self.__ctrl_notification: NotificationController = ctrl_notification
        self.__ctrl_esp_communication: ESPCommunicationHandler = ctrl_esp_communication
        self.__ctrl_camera: CameraHandler = ctrl_camera

        self.__id_route_execution: int = -1
        self.__id_route: int = id_route
        self.__id_robot: int = id_robot

    def __notify_route_execution_status(self, state: str) -> bool:
        flag_success = self.__ctrl_notification.inform_route_execution_status(
            value = state
        )

        return flag_success

    def __notify_route_execution_movement_detection(
        self,
        id_camera_triggering: int
    ) -> bool:
        flag_success = self.__ctrl_notification.inform_route_execution_movement_detection(
            id_camera_triggering
        )

        return flag_success

    def __notify_route_execution_face_detection(
        self,
        id_camera_triggering: int
    ) -> bool:
        flag_success = self.__ctrl_notification.inform_route_execution_face_detection(
            id_camera_triggering
        )

        return flag_success

    def __notify_route_execution_aruco_read(self, id_aruco: int) -> bool:
        flag_success = self.__ctrl_notification.inform_route_execution_aruco_read(
            aruco_id = id_aruco
        )

        return flag_success

    def __insert_route_execution(self) -> bool:
        self.__id_route_execution = self.__ctrl_database.insert_route_execution(
            self.__id_route,
            self.__id_robot
        )

    def __get_route_steps(self) -> DataFrame:
        route_steps = self.__ctrl_database.get_route_steps(
            id_route = self.__id_route
        )

        return route_steps

    def __movement_face_detection_routine(self) -> bool:
        result_detection = self.__ctrl_camera.movement_face_detection_routine(
            self.__ctrl_esp_communication
        )
        return result_detection

    def __insert_route_execution_movement_detection(self, step_sequence: int) -> int:
        id_camera_triggering = self.__ctrl_database.insert_route_execution_movement_detection(
            self.__id_route_execution,
            self.__ctrl_camera.last_image_unique_id,
            step_sequence
        )
        return id_camera_triggering

    def __insert_route_execution_face_detection(self, step_sequence: int) -> None:
        id_camera_triggering = self.__ctrl_database.insert_route_execution_face_detection(
            self.__id_route_execution,
            self.__ctrl_camera.last_image_unique_id,
            step_sequence
        )
        return id_camera_triggering

    def __verify_user_response(self):
        user_response = False
        while not user_response:
            user_response = self.__ctrl_database.verify_user_response(
                self.__id_route_execution
            )

        return user_response

    def __stop_motors(self):
        # time_sleep(0.3)
        success = self.__ctrl_esp_communication.stop_motor_executing()
        # while not success:
            # time_sleep(0.3)
            # success = self.__ctrl_esp_communication.stop_motor_executing()

    def __turn_on_buzzer(self):
        success = self.__ctrl_esp_communication.turn_on_buzzer()
        while not success:
            success = self.__ctrl_esp_communication.turn_on_buzzer()
            time_sleep(0.3)

    def __turn_off_buzzer(self):
        success = self.__ctrl_esp_communication.turn_off_buzzer()
        while not success:
            success = self.__ctrl_esp_communication.turn_off_buzzer()
            time_sleep(0.3)

    def __notify_aruco_marker_not_found(self, step_sequence: int):
        self.__ctrl_database.insert_notification(
            self.__id_route_execution,
            "aruco_marker_not_found",
            step_sequence
        )

    def __update_moment_end_route_execution(self) -> None:
        self.__ctrl_database.update_route_execution_ending(
            unique_id = self.__id_route_execution
        )

    def __end(self) -> bool:
        self.__notify_route_execution_status("Finalized")
        self.__update_moment_end_route_execution()
        return True

    def start(self) -> bool:
        """Start all the proccess to perform a route execution.
        """
        self.__insert_route_execution()

        df_route_steps = self.__get_route_steps()

        print(df_route_steps)
        self.__ctrl_notification.initializa_notification_controller(
            id_route_exec = self.__id_route_execution
        )
        self.__notify_route_execution_status("Executing")

        for step_index, route_step in df_route_steps.iterrows():
            step_sequence = step_index + 1
            if (route_step['right_pwm_intensity'] > 0
                and route_step['left_pwm_intensity'] > 0
            ):
                print("MOVING FORWARD")
                self.__ctrl_esp_communication.move_forward_executing()
                print("ENDED MOVING FORWARD")

            if (route_step['right_pwm_intensity'] > 0
                and route_step['left_pwm_intensity'] == 0
            ):
                self.__ctrl_esp_communication.rotate_left_executing()

            if (route_step['right_pwm_intensity'] == 0
                and route_step['left_pwm_intensity'] > 0
            ):
                self.__ctrl_esp_communication.rotate_right_executing()

            print(f"MOVEU {route_step['step_sequence']}")
            # TODO: improve this condition, too dummy
                print("STOPPING MOTORS")
                self.__stop_motors()
                print("MOTORS STOPPED")

                print(f"MOVEMENT FACE DETECTION {route_step['step_sequence']}")
                result_detection = self.__movement_face_detection_routine()

                if result_detection == "movement detected":
                    print(f"MOVEMENT DETECTED {route_step['step_sequence']}")
                    id_camera_triggering = self.__insert_route_execution_movement_detection(
                        route_step['step_sequence']
                    )
                    self.__notify_route_execution_movement_detection(id_camera_triggering)
                    self.__turn_on_buzzer()

                    user_response = self.__verify_user_response()
                    if user_response == "Continue Route":
                        pass
                        self.__turn_off_buzzer()
                    elif user_response == "Stop Route":
                        self.__turn_off_buzzer()
                        self.__end()
                        return True

                if result_detection ==  "face detected":
                    print(f"FACE DETECTED {route_step['step_sequence']}")
                    id_camera_triggering = self.__insert_route_execution_face_detection(
                        route_step['step_sequence']
                    )
                    self.__notify_route_execution_face_detection(id_camera_triggering)
                    self.__turn_on_buzzer()

                    user_response = self.__verify_user_response()
                    if user_response == "Continue Route":
                        self.__turn_off_buzzer()
                        pass
                    elif user_response == "Stop Route":
                        self.__turn_off_buzzer()
                        self.__end()
                        return True

            if (route_step['right_pwm_intensity'] == 0
                and route_step['left_pwm_intensity'] == 0
            ):
                print("MOTORS STARTED")
                self.__stop_motors()
                print("MOTORS STOPPED")
                print(f"READING ARUCO {route_step['step_sequence']}")
                id_aruco = self.__ctrl_camera.read_aruco_marker_routine(
                    self.__ctrl_esp_communication
                )
                if id_aruco == -1:
                    self.__notify_aruco_marker_not_found(step_sequence)
                    self.__end()
                    return True
                self.__notify_route_execution_aruco_read(
                    id_aruco
                )
                # TODO: implement the logic to turn the robot to the correct direction

        self.__stop_motors()
        self.__end()
        return True
