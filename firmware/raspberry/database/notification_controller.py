from database.database_controller import DatabaseController


class NotificationController:

    def __init__(self, ctrl_database: DatabaseController) -> None:
        self.__ctrl_database: DatabaseController = ctrl_database
        self.__id_route_execution: int = None

    def initializa_notification_controller(self, id_route_exec: int) -> bool:
        self.__id_route_execution = id_route_exec
        return True

    def inform_route_execution_status(
        self,
        value: str
    ) -> bool:
        message = "route_execution_status"

        self.__ctrl_database.insert_notification(
            self.__id_route_execution,
            message,
            value
        )
        return True

    def inform_route_execution_aruco_read(
        self,
        aruco_id: int
    ) -> bool:
        message = "aruco_read"

        self.__ctrl_database.insert_notification(
            self.__id_route_execution,
            message,
            f"{aruco_id}"
        )
        return True

    def inform_route_execution_movement_detection(
        self,
        id_camera_triggering: int
    ) -> bool:
        message = "movement_detection"

        self.__ctrl_database.insert_notification(
            self.__id_route_execution,
            message,
            f"{id_camera_triggering}"
        )
        return True

    def inform_route_execution_face_detection(
        self,
        id_camera_triggering: int
    ) -> bool:
        message = "person_detection"

        self.__ctrl_database.insert_notification(
            self.__id_route_execution,
            message,
            f"{id_camera_triggering}"
        )
        return True
