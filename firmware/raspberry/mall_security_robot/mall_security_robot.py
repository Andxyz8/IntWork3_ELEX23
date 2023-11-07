from mediators.route_execution_mediator import RouteExecutionMediator
from mediators.route_recording_mediator import RouteRecordingMediator
from database.database_controller import DatabaseController
from database.notification_controller import NotificationController
from handlers.esp_communication import ESPCommunicationHandler
from handlers.app_communication import AppCommunicationHandler

class MallSecurityRobot:

    def __init__(self):
        self.__ctrl_notification: NotificationController = None
        self.__ctrl_database: DatabaseController = None
        self.__ctrl_esp_communication: ESPCommunicationHandler = None
        self.__ctrl_app_communication: AppCommunicationHandler = None
        self.__route_execution: RouteExecutionMediator = None
        self.__route_recording: RouteRecordingMediator = None

    def __initialize_app_communication(self) -> bool:
        self.__ctrl_app_communication = AppCommunicationHandler()

        # Initialize necessary objects
        self.__ctrl_app_communication.ctrl_esp_communication = self.__ctrl_esp_communication

        # Register the route in the server app
        self.__ctrl_app_communication.register(
            self.__ctrl_app_communication.app,
            route_base = '/command/'
        )

        self.__ctrl_app_communication.initialize_server_communication()

        print(f"APP flask: {self.__ctrl_app_communication.app}")

        return True

    def __initialize_route_recording_mode(self) -> bool:
        self.__route_recording = RouteRecordingMediator()

        return True

    def __initialize_route_execution_mode(self) -> bool:
        try:
            self.__ctrl_database = DatabaseController()

            self.__ctrl_notification = NotificationController(self.__ctrl_database)

            print("FIREBASE CLOUD SERVER COMMUNICATION WITH RASPBERRY ESTABLISHED.")

            self.__ctrl_esp_communication = ESPCommunicationHandler()
            self.__ctrl_esp_communication.test_esp32_i2c_communication()
            print("ESP32 I2C COMMUNICATION WITH RASPBERRY ESTABLISHED.")

            self.__route_execution = RouteExecutionMediator(
                ctrl_database = self.__ctrl_database,
                ctrl_notification = self.__ctrl_notification,
                ctrl_esp_communication = self.__ctrl_esp_communication
            )

        except Exception as exc:
            raise NotImplementedError from exc

    def start(self):
        """Starts Patrole operating firmware.

            - Initialize app communication and wait for commands to perform.
        """
        try:
            # First state to initialize Patrole is allowing receiving http requests
            flag_app_communication = self.__initialize_app_communication()
            print(f"status app comm {flag_app_communication}")

            if not flag_app_communication:
                raise NotImplementedError
        except KeyboardInterrupt:
            print("Shutting down by keyboard...")
        finally:
            print("Turning Off...")
            print(f"Situation: {flag_app_communication}")
