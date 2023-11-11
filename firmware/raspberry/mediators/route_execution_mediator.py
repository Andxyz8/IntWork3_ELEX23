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
            id_route_execution = self.__id_route_execution,
            value = state
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

    def __movement_detection_routine(self) -> bool:
        flag_detected = self.__ctrl_camera.movement_detection_routine()
        return flag_detected

    def __insert_route_execution_movement_detection(self, step_sequence: int) -> None:
        self.__ctrl_database.insert_route_execution_movement_detection(
            self.__id_route_execution,
            self.__ctrl_camera.__last_image_unique_id,
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

        self.__notify_route_execution_status("Executing")

        for step_index, route_step in df_route_steps.iterrows():
            if (route_step['right_pwm_intensity'] > 0
                and route_step['left_pwm_intensity'] > 0
            ):
                flag_success = self.__ctrl_esp_communication.move_forward()
                if flag_success:
                    continue
                while not flag_success:
                    flag_success = self.__ctrl_esp_communication.move_forward()
                    if flag_success:
                        continue
            print(f"MOVEU {route_step['step_sequence']}")

            # TODO: improve this condition, too dummy
            if step_index % 4 == 0:
                flag_detected = self.__movement_detection_routine()
                if flag_detected:
                    self.__insert_route_execution_movement_detection(
                        route_step['step_sequence']
                    )
        self.__end()
        return True
