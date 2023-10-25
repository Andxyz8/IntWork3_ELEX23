from database.database_controller import DatabaseController
from database.notification_controller import NotificationController
from utils.datetime_operator import get_str_datetime_agora

class RouteExecutionMediator:

    

    def __init__(
        self,
        ctrl_database: DatabaseController,
        ctrl_notification: NotificationController,
        id_route: int = 1,
        id_robot: int = 1
    ):
        self.__ctrl_database: DatabaseController  = ctrl_database
        self.__ctrl_notification: NotificationController = ctrl_notification

        self.__id_route_execution: int = -1
        self.__id_route: int = id_route
        self.__id_robot: int = id_robot

        self.__notify_route_execution_state()
        self.__insert_route_execution()

    def __notify_route_execution_state(self) -> bool:
        flag_success = self.__ctrl_notification.send_notification(
            message = 'route_execution_state',
            value = True
        )

        return flag_success

    def __insert_route_execution(self) -> bool:
        self.__id_route_execution = self.__ctrl_database.get_next_id_collection(
            collection = 'route_execution'
        )

        data_insert = {
            "id_route_execution": self.__id_route_execution,
            "id_route": self.__id_route,
            "id_robot": self.__id_robot,
            "moment_start": get_str_datetime_agora(),
            "moment_end": ""
        }

        self.__ctrl_database.insert_data_into_collection(
            collection = 'route_execution',
            info_insert = data_insert
        )

    def __update_moment_end_route_execution(self) -> None:
        data_insert = {
            "id_route_execution": self.__id_route_execution,
            "moment_end": get_str_datetime_agora()
        }

        self.__ctrl_database.update_data_into_collection(
            collection = 'route_execution',
            unique_id = self.__id_route_execution,
            info_insert = data_insert
        )

    def start(self) -> bool:
        return True

    def end(self) -> bool:
        self.__update_moment_end_route_execution()

        return True
