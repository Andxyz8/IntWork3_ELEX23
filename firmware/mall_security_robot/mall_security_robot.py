from mediators.route_execution_mediator import RouteExecutionMediator
from database.database_controller import DatabaseController
from database.notification_controller import NotificationController
from sys import exit as sys_exit
from time import sleep as time_sleep

class MallSecurityRobot:

    def __init__(self):
        self.__ctrl_notification: NotificationController = None
        self.__ctrl_database: DatabaseController = None
        self.__ctrl_route_execution: RouteExecutionMediator = None
    
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

            self.__ctrl_route_execution = RouteExecutionMediator(
                ctrl_database = self.__ctrl_database,
                ctrl_notification = self.__ctrl_notification
            )

            return True
        except Exception as exc:
            raise NotImplementedError from exc
            return False

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
                    + "0 - Exit."
                )
                command = input("Execute command: ")
                print(f"executing command {command}")
                if command == '1':
                    if not self.__initialize_route_recording_mode():
                        NotImplementedError("Somethin gone wrong while initializing route recording mode!")
                    self.__ctrl_route_execution.start()
                    time_sleep(8)
                    self.__ctrl_route_execution.end()
                elif command == '2':
                    if not self.__initialize_route_execution_mode():
                        NotImplementedError("Somethin gone wrong while initializing route execution mode!")
                else:
                    print("Shutting down...")
                    sys_exit(0)
                time_sleep(5)

        except KeyboardInterrupt:
            print("Shutting down...")
