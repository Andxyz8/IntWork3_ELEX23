from database.database_controller import DatabaseController
from database.notification_controller import NotificationController
from handlers.esp_communication import ESPCommunicationHandler
from utils.datetime_operator import get_str_datetime_agora
from time import sleep as time_sleep

class RouteExecutionMediator:

    def __init__(
        self,
        ctrl_database: DatabaseController,
        ctrl_notification: NotificationController,
        ctrl_esp_communication: ESPCommunicationHandler,
        id_route: int = 1,
        id_robot: int = 1
    ):
        self.__ctrl_database: DatabaseController  = ctrl_database
        self.__ctrl_notification: NotificationController = ctrl_notification
        self.__ctrl_esp_communication: ESPCommunicationHandler = ctrl_esp_communication

        self.__id_route_execution: int = -1
        self.__id_route: int = id_route
        self.__id_robot: int = id_robot

    def __notify_route_execution_state(self, state: bool) -> bool:
        flag_success = self.__ctrl_notification.send_notification(
            message = 'route_execution_state',
            value = state
        )

        return flag_success

    def __insert_route_execution(self) -> bool:
        self.__id_route_execution = self.__ctrl_database.insert_route_execution(
            self.__id_route,
            self.__id_robot
        )

    def __update_moment_end_route_execution(self) -> None:
        self.__ctrl_database.update_route_ending(
            unique_id = self.__id_route_execution
        )

    def start(self) -> bool:
        # self.__notify_route_execution_state(True)
        self.__insert_route_execution()


        print("antes de iniciar")
        iterations = 0

        while iterations < 10:
            self.__ctrl_database.insert_camera_triggering(
                self.__id_route_execution,
                reason = "Testing database.",
                image_url = 'testing.jkpg'
            )

            print(f"looping {iterations}")
            if iterations == 10:
                break
            # time_sleep(1)
            iterations += 1

        return True

    def end(self) -> bool:
        # self.__notify_route_execution_state(False)
        self.__update_moment_end_route_execution()
        return True
