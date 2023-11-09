from flask import request
from flask_classful import FlaskView, route
from mall_security_robot import obj_patrole

class AppCommunicationHandler(FlaskView):
    route_base = 'command'

    def __init__(self) -> None:
        pass

    @route("/", methods = ['GET', 'POST'])
    def post_establish_communication(self):
        """Base route for mobile app to establish communication with Raspberry Pi.

        Headers:
            None
        
        Body:
            None

        Response (JSON):
            found (bool): always True if receive a request.
        """
        # TODO: implement some authentication
        return {'found': True}

    @route("/route_recording_mode", methods = ['GET', 'POST'])
    def put_route_recording_mode(self):
        """Instantiate the route recording mode on the Raspberry Pi.

        Headers:
            Content-Type (str): application/json

        Body (JSON):
            title (str): title to set to the route being created.
            description (str): brief description of the route.
            n_repeats (int): times route should be completed before finish.
            interval_between_repeats (int): time between each repetition.

        Response (JSON):
            status (int): always 200, if successfull.
        """
        json_request = request.get_json()

        title = json_request['title']
        description = json_request['description']
        n_repeats = json_request['n_repeats']
        interval_between_repeats = json_request['interval_between_repeats']

        obj_patrole.initialize_route_recording_mode(
            title,
            description,
            n_repeats,
            interval_between_repeats
        )
        return {'status': 200}

    @route("/end_route_recording_mode", methods = ['GET', 'POST'])
    def post_end_route_recording(self):
        """Finish the route recording mode on the Raspberry Pi.

        Send all data to the cloud server and turn raspberry at initial mode again.

        Headers:
            None

        Body:
            None

        Response (JSON):
            status (int): always 200, if successfull.
        """
        obj_patrole.end_route_recording_mode()
        return {'status': 200}

    @route("/recording_move_forward", methods = ['GET', 'POST'])
    def post_move_forward_recording(self):
        execution_succed = obj_patrole.route_recording.move_forward()

        return {"status": 200, "value": execution_succed}

    @route("/recording_move_forward_fine", methods = ['GET', 'POST'])
    def post_move_forward_fine(self):
        """THIS IS NOT BEING USED AT THE MOMENT"""
        # TODO: future improvements on robot navegation
        json_request = request.get_json()

        time_in_seconds = json_request['time_in_seconds']
        pwm_intensity_left = json_request['pwm_intensity_left']
        pwm_intensity_right = json_request['pwm_intensity_right']

        execution_succed = obj_patrole.route_recording.move_forward_fine(
            pwm_intensity_left,
            pwm_intensity_right,
            time_in_seconds
        )

        return {"status": 200, "value": execution_succed}

    @route("/route_execution_mode", methods = ['GET', 'POST'])
    def post_route_execution_mode(self):
        """Instantiate the route execution mode on the Raspberry Pi.

        Headers:
            Content-Type (str): application/json

        Body (JSON):
            id_route (int): route id stored on the cloud server to execute.
            id_robot (int): robot id which will be executing route.

        Response (JSON):
            status (int): always 200, if successfull.
        """
        # Get values from json body for this request
        json_request = request.get_json()

        id_route = json_request['id_route']
        id_robot = json_request['id_robot']

        obj_patrole.initialize_route_execution_mode(
            id_route = id_route,
            id_robot = id_robot
        )

        return {'status': 200}

    @route("/turn_camera_servo_right", methods = ['GET', 'POST'])
    def post_turn_camera_servo_right(self):
        obj_patrole.route_recording.turn_camera_servo_right()

        return {'status': 200}

    '''@route("/go_back_initial_state", methods = ['GET', 'POST'])
    def post_go_back_initial_state(self):
        self.__route_execution = None
        self.__route_recording = None
        self.__initialize_initial_mediator()
        return {
            "status": 200
        }

    @route("/rotate_right", methods = ['GET', 'POST'])
    def post_rotate_right(self):
        json_request = request.get_json()

        print("REQUISICAO DEU BOA: ")
        print(json_request)

        return {
            'status': 200,
            'message': 'Success rotate_right'
        }

    @route("/rotate_left", methods = ['GET', 'POST'])
    def post_rotate_left(self):
        json_request = request.get_json()

        print("REQUISICAO DEU BOA: ")
        print(json_request)'''
