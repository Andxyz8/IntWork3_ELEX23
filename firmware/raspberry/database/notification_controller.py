from database.database_controller import DatabaseController
from utils.datetime_operator import get_str_datetime_agora


class NotificationController:

    def __init__(self, ctrl_database: DatabaseController) -> None:
        self.__ctrl_database: DatabaseController = ctrl_database
        self.__id_route_execution: int = None

    def initializa_notification_controller(self, id_route_exec: int) -> bool:
        self.__id_route_execution = id_route_exec
        return True

    def inform_route_execution_status(
        self,
        id_route_execution: int,
        value: str
    ) -> bool:
        message = "route_execution_status"

        self.__ctrl_database.insert_notification(
            id_route_execution,
            message,
            value
        )
        return True
