from mediators.initial_state_mediator import InitialStateMediator
from mediators.route_execution_mediator import RouteExecutionMediator
from mediators.route_recording_mediator import RouteRecordingMediator
from database.database_controller import DatabaseController
from database.notification_controller import NotificationController
from handlers.esp_communication import ESPCommunicationHandler
from handlers.camera_handler import CameraHandler

class Patrole():

    def __init__(self):
        self.__ctrl_notification: NotificationController = None
        self.__ctrl_database: DatabaseController = None
        self.__ctrl_esp_communication: ESPCommunicationHandler = None
        self.__ctrl_camera: CameraHandler = None
        self.initial_state: InitialStateMediator = None
        self.route_recording: RouteRecordingMediator = None
        self.route_execution: RouteExecutionMediator = None
        self.__flag_i2c_working: bool = False

    def __initialize_initial_mediator(self) -> bool:
        self.__ctrl_esp_communication = ESPCommunicationHandler()

        self.__ctrl_database = DatabaseController()

        # Initialize initial mediator
        self.initial_state = InitialStateMediator(
            ctrl_esp = self.__ctrl_esp_communication
        )

    def initialize_route_recording_mode(
        self,
        title: str,
        description: str,
        n_repeats: int,
        interval_between_repeats: str
    ) -> bool:
        # self.__initial_state = None

        self.__ctrl_camera = CameraHandler()

        self.route_recording = RouteRecordingMediator(
            ctrl_esp = self.__ctrl_esp_communication,
            ctrl_database = self.__ctrl_database,
            ctrl_camera = self.__ctrl_camera
        )

        self.route_recording.start(
            title,
            description,
            n_repeats,
            interval_between_repeats
        )

        return True

    def end_route_recording_mode(self) -> bool:
        """Turn route recording mode off.
        """
        self.route_recording.end_route_recording()

    def initialize_route_execution_mode(self, id_route: int, id_robot: int) -> bool:
        """Initialize and start the route execution mediator."""
        self.__ctrl_camera = CameraHandler()

        self.__ctrl_notification = NotificationController(self.__ctrl_database)

        self.route_execution = RouteExecutionMediator(
            ctrl_database = self.__ctrl_database,
            ctrl_notification = self.__ctrl_notification,
            ctrl_esp_communication = self.__ctrl_esp_communication,
            id_route = id_route,
            id_robot = id_robot
        )

        self.route_execution.start()

    def start(self):
        """Starts Patrole operating firmware.

            - Initialize app communication and wait for commands to perform.
        """
        # First state to initialize Patrole is allowing receiving http requests
        self.__initialize_initial_mediator()

        # if not self.__flag_i2c_working:
            # raise NotImplementedError
