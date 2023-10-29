from sys import exit as sys_exit
from time import sleep as time_sleep
from mediators.route_execution_mediator import RouteExecutionMediator
from database.database_controller import DatabaseController
from database.notification_controller import NotificationController
from handlers.esp_communication import ESPCommunicationHandler

class MallSecurityRobot:

    def __init__(self):
        self.__ctrl_notification: NotificationController = None
        self.__ctrl_database: DatabaseController = None
        self.__ctrl_esp_communication: ESPCommunicationHandler = None
        self.__ctrl_route_execution: RouteExecutionMediator = None

        self.__route_execution_is_running: bool = False
    
    def __initialize_bluetooth_connection(self) -> bool:
        # TODO: implement __initialize_bluetooth_connection
        return True

    
    def __initialize_route_recording_mode(self) -> bool:
        # TODO: implement __initialize_route_recording_mode
        raise NotImplementedError("__initialize_route_recording_mode() not implemented yet.")

    def __initialize_route_execution_mode(self) -> bool:
        try:
            self.__ctrl_database = DatabaseController()

            self.__ctrl_notification = NotificationController(self.__ctrl_database)

            print("FIREBASE CLOUD SERVER COMMUNICATION WITH RASPBERRY ESTABLISHED.")

            self.__ctrl_esp_communication = ESPCommunicationHandler()
            self.__ctrl_esp_communication.test_esp32_i2c_communication()
            print("ESP32 I2C COMMUNICATION WITH RASPBERRY ESTABLISHED.")

            self.__ctrl_route_execution = RouteExecutionMediator(
                ctrl_database = self.__ctrl_database,
                ctrl_notification = self.__ctrl_notification,
                ctrl_esp_communication = self.__ctrl_esp_communication
            )

            self.__route_execution_is_running = True
        except Exception as exc:
            raise NotImplementedError from exc

    def start(self):
        try:
            while True:
                # First state to initialize Patrole is allowing bluetooth connection
                if not self.__initialize_bluetooth_connection():
                    break

                # TODO: module AppCommunicationHandler
                # Start communication
                # Wait for commands
                # process command
                # return here to execute command

                print(
                    "1 - Route Recording Mode.\n"
                    + "2 - Route Execution Mode.\n"
                    + "3 - Ask ESP.\n"
                    + "0 - Exit."
                )
                command = input("Execute command: ")
                print(f"executing command {command}")
                if command == '1':
                    if not self.__initialize_route_recording_mode():
                        raise NotImplementedError("Somethin gone wrong while initializing route recording mode!")
                elif command == '2':
                    if not self.__route_execution_is_running:
                        self.__initialize_route_execution_mode()
                    self.__ctrl_route_execution.start()
                    time_sleep(10)
                    self.__ctrl_route_execution.end()

                elif command == '3':
                    if self.__ctrl_esp_communication is None:
                        self.__ctrl_esp_communication = ESPCommunicationHandler()
                    print(f"ESP ANSWER: {self.__ctrl_esp_communication.get_compass_module_data()}")
                else:
                    print("Shutting down...")
                    sys_exit(0)
                time_sleep(5)

        except KeyboardInterrupt:
            print("Shutting down...")
