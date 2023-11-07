from flask_classful import FlaskView, route
from flask import Flask, request
from handlers.esp_communication import ESPCommunicationHandler
from mediators.route_execution_mediator import RouteExecutionMediator


class AppCommunicationHandler(FlaskView):

    route_base = 'command'

    def __init__(self, ) -> None:
        # Instantiate a flask object
        self.app = Flask(__name__)
        self.__ctrl_esp_communication: ESPCommunicationHandler = None
        self.__route_recording: RouteExecutionMediator = None

    @property
    def ctrl_esp_communication(self) -> ESPCommunicationHandler:
        return self.__ctrl_esp_communication

    @ctrl_esp_communication.setter
    def ctrl_esp_communication(self, ctrl_esp_communication: ESPCommunicationHandler):
        self.__ctrl_esp_communication = ctrl_esp_communication

    @property
    def route_recording(self) -> RouteExecutionMediator:
        return self.__route_recording

    @route_recording.setter
    def route_recording(self, route_recording: RouteExecutionMediator):
        self.__route_recording = route_recording

    @route('/move_forward', methods = ['GET', 'POST'])
    def post_move_forward(self):
        json_request = request.get_json()

        print("REQUISICAO DEU BOA: ")
        print(json_request)

        if self.__ctrl_esp_communication is None:
            self.__ctrl_esp_communication = ESPCommunicationHandler()

        self.__ctrl_esp_communication.move_forward()

        return {
            'status': 200,
            'message': 'Success move_forward'
        }

    @route('/rotate_right', methods = ['GET', 'POST'])
    def post_rotate_right(self):
        json_request = request.get_json()

        print("REQUISICAO DEU BOA: ")
        print(json_request)

        return {
            'status': 200,
            'message': 'Success rotate_right'
        }

    @route('/rotate_left', methods = ['GET', 'POST'])
    def post_rotate_left(self):
        json_request = request.get_json()

        print("REQUISICAO DEU BOA: ")
        print(json_request)

        if self.__ctrl_esp_communication is None:
            self.__ctrl_esp_communication = ESPCommunicationHandler()

        self.__ctrl_esp_communication.test_esp32_i2c_communication()

        return {
            'status': 200,
            'message': 'Success rotate_left'
        }

    def initialize_server_communication(self):
        """StartS the communication server.

        - Allows Patrole to receive commands from the mobile app.
        """
        # Starts the communication server
        self.app.run(
            host = '127.0.0.1',
            port = '5000',
            debug = True # Must change to False if in production
        )
