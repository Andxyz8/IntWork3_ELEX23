from copy import deepcopy
from handlers.esp_communication import ESPCommunicationHandler
from handlers.camera_handler import CameraHandler
from database.database_controller import DatabaseController


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

        self.__first_aruco = None
        self.__current_aruco = None
        self.__number_arucos_readed = 0

    def __add_route_step(
        self,
        step_type: str,
        pwm_intensity_left: float = 48,
        pwm_intensity_right: float = 50
    ) -> None:
        step_number = len(self.__route_steps) + 1
        step = {}
        if step_type == 'MF':
            step = {
                'step_sequence': f'{step_number}/',
                'start_aruco_marker': self.__current_aruco,
                'next_aruco_marker': 0,
                'number_rotations_left_encoder': 3,
                'number_rotations_right_encoder': 3,
                'left_pwm_intensity': pwm_intensity_left,
                'right_pwm_intensity': pwm_intensity_right,
                'compass_module_degrees': 0
            }
        if step_type == 'RL':
            step = {
                'step_sequence': f'{step_number}/',
                'start_aruco_marker': self.__current_aruco,
                'next_aruco_marker': 0,
                'number_rotations_left_encoder': 4,
                'number_rotations_right_encoder': 2,
                'left_pwm_intensity': 0,
                'right_pwm_intensity': 48,
                'compass_module_degrees': 0
            }
        if step_type == 'RR':
            step = {
                'step_sequence': f'{step_number}/',
                'start_aruco_marker': self.__current_aruco,
                'next_aruco_marker': 0,
                'number_rotations_left_encoder': 2,
                'number_rotations_right_encoder': 4,
                'left_pwm_intensity': 48,
                'right_pwm_intensity': 0,
                'compass_module_degrees': 0
            }
        if step_type == 'RA':
            self.__number_arucos_readed += 1
            step = {
                'step_sequence': f'{step_number}/',
                'start_aruco_marker': self.__current_aruco,
                'next_aruco_marker': 0,
                'number_rotations_left_encoder': 0,
                'number_rotations_right_encoder': 0,
                'left_pwm_intensity': 0,
                'right_pwm_intensity': 0,
                'compass_module_degrees': 0
            }

        self.__route_steps.append(step)

    def __format_step_sequence(self):
        last = len(self.__route_steps)
        for step in self.__route_steps:
            step['step_sequence'] += f'{last}'

    def __format_next_aruco_marker(self):
        total_steps = len(self.__route_steps)
        index_previous_aruco_start = 0
        for idx in range(total_steps):
            # if is the last aruco end formating
            if idx + 1 == total_steps:
                break

            # if the next step is aruco reading
            if (self.__route_steps[idx + 1]['left_pwm_intensity'] == 0
                and self.__route_steps[idx + 1]['right_pwm_intensity'] == 0
            ):
                index_previous_aruco_end = idx + 1
                id_next_aruco_marker = deepcopy(
                    self.__route_steps[index_previous_aruco_end]['start_aruco_marker']
                )
                for index_change in range(index_previous_aruco_start, index_previous_aruco_end):
                    self.__route_steps[index_change]['next_aruco_marker'] = deepcopy(
                        id_next_aruco_marker
                    )
                index_previous_aruco_start = deepcopy(index_previous_aruco_end)

    def __insert_new_route(self):
        self.__id_route = self.__ctrl_database.insert_route_recording_start()

    def turn_camera_servo_right(self) -> bool:
        self.__ctrl_camera.turn_servo(30)
        return True

    def move_forward(self) -> bool:
        self.__add_route_step('MF')
        return self.__ctrl_esp.move_forward()

    def rotate_left(self) -> bool:
        self.__add_route_step('RL')
        return self.__ctrl_esp.rotate_left()

    def rotate_right(self) -> bool:
        self.__add_route_step('RR')
        return self.__ctrl_esp.rotate_right()

    def read_aruco_marker(self) -> int:

        if self.__first_aruco is not None:
            self.__previous_aruco = deepcopy(self.__current_aruco)

        self.__current_aruco = self.__ctrl_camera.read_aruco_marker_routine(
            self.__ctrl_esp
        )
        if self.__first_aruco is None:
            self.__first_aruco = deepcopy(self.__current_aruco)

        self.__add_route_step('RA')
        return self.__current_aruco

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
        interval_between_repeats: str,
        number_arucos_readed: int
    ) -> None:
        self.__ctrl_database.update_route_recording_end(
            self.__id_route,
            title,
            description,
            n_repeats,
            interval_between_repeats,
            number_arucos_readed
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
            interval_between_repeats,
            self.__number_arucos_readed
        )

        self.__format_step_sequence()

        self.__format_next_aruco_marker()

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
