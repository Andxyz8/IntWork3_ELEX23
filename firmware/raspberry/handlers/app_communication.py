from flask import request
from flask_classful import FlaskView, route
from mall_security_robot import obj_patrole

class AppCommunicationHandler(FlaskView):
    route_base = 'command'

    def __init__(self) -> None:
        pass

    @route("/route_recording_mode", methods = ['PUT'])
    def put_route_recording_mode(self):
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

    @route("/end_route_recording_mode", methods = ['POST'])
    def post_end_route_recording(self):
        obj_patrole.end_route_recording_mode()
        return {'status': 200}

    @route("/recording_move_forward", methods = ['GET', 'POST'])
    def post_move_forward(self):
        execution_succed = obj_patrole.route_recording.move_forward()

        return {"status": 200, "value": execution_succed}

    @route("/route_execution_mode", methods = ['PUT'])
    def put_route_execution_mode(self):
        obj_patrole.initialize_route_execution_mode()

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