from database.database_controller import DatabaseController
from utils.datetime_operator import get_str_datetime_agora


class NotificationController:

    def __init__(self, ctrl_database: DatabaseController) -> None:
        self.__ctrl_database: DatabaseController = ctrl_database

    def send_notification(self, message: str, value: str) -> bool:
        # pyres_notifications: PyreResponse = self.__cloud_database.child(
        # "notifications"
        # ).order_by_child("id_notification").get()

        # notifications: list[Pyre] = pyres_notifications.each()

        next_key = self.__ctrl_database.get_next_id_collection(
            collection = "notifications"
        )

        dict_message = {
            "id_notification": next_key,
            "id_route": 1,
            message: value,
            "moment": get_str_datetime_agora()
        }

        self.__ctrl_database.insert_data_into_collection(
            collection = 'notifications',
            info_insert = dict_message
        )

        return True
