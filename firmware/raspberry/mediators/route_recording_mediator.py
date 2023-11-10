from handlers.esp_communication import ESPCommunicationHandler
from database.database_controller import DatabaseController
from handlers.camera_handler import CameraHandler


class RouteRecordingMediator:
    def __init__(
        self,
        ctrl_esp: ESPCommunicationHandler,
        ctrl_database: DatabaseController,
        ctrl_camera: CameraHandler
    ):
        self.__ctrl_esp: ESPCommunicationHandler = ctrl_esp
        self.__ctrl_database: DatabaseController = ctrl_database
        self.__ctrl_camera: CameraHandler = ctrl_camera

        self.__id_route = None
        self.__route_steps = []

    def __add_route_step(
        self,
        step_type: str,
        pwm_intensity_left: float = 30,
        pwm_intensity_right: float = 30
    ) -> None:
        number_steps = len(self.__route_steps) + 1
        step = {}
        if step_type == 'MF':
            step = {
                'step_sequence': f'{number_steps}/',
                'start_aruco_marker': 1,
                'next_aruco_marker': 2,
                'number_rotations_left_encoder': 3,
                'number_rotations_right_encoder': 3,
                'left_pwm_intensity': pwm_intensity_left,
                'right_pwm_intensity': pwm_intensity_right,
                'compass_module_degrees': 0
            }

        self.__route_steps.append(step)

    def __format_step_sequence(self):
        last = len(self.__route_steps)
        for step in self.__route_steps:
            step['step_sequence'] += f'{last}'

    def __insert_new_route(self):
        self.__id_route = self.__ctrl_database.insert_route_recording_start()

    def turn_camera_servo_right(self) -> bool:
        self.__ctrl_camera.turn_servo(30)
        return True

    def move_forward(self) -> bool:
        self.__add_route_step('MF')
        return self.__ctrl_esp.move_forward()

    def move_forward_fine(
        self,
        pwm_intensity_left: float,
        pwm_intensity_right: float,
        time_in_seconds: int
    ) -> bool:
        self.__add_route_step(
            'FF',
            pwm_intensity_left,
            pwm_intensity_right
        )
        return self.__ctrl_esp.move_forward_fine(
            pwm_intensity_left,
            pwm_intensity_right,
            time_in_seconds
        )

    def __update_route_information(
        self,
        title: str,
        description: str,
        n_repeats: int,
        interval_between_repeats: str
    ) -> None:
        self.__id_route = self.__ctrl_database.update_route_recording_end(
            self.__id_route,
            title,
            description,
            n_repeats,
            interval_between_repeats
        )

    def end_route_recording(
        self,
        title: str,
        description: str,
        n_repeats: int,
        interval_between_repeats: str
    ) -> None:
        """Executes some operations to properly finish the route recording proccess.

        - Update basic route information as title, description number of times 
            to repeat the route execution, and the interval between routes.
        - Format recorded steps to be properly stored at the cloud database
            and upload to cloud database.
        """
        self.__update_route_information(
            title,
            description,
            n_repeats,
            interval_between_repeats
        )

        self.__format_step_sequence()

        self.__ctrl_database.insert_route_steps(
            self.__id_route,
            self.__route_steps
        )

    def start(self):
        """Starts the proccess of recording a route.
        
        - Insert the initial values for the route into the database.
        - Keeps the route id that was inserted to later updates to the route info.
        """
        self.__insert_new_route()
