from flask import Flask
from flask import request

app = Flask(__name__)

@app.route('/', methods = ['GET'])
def index():
    return {"found": True}
    
@app.route('/command', methods = ['GET', 'POST'])
def commands():
    return {"found": True}

@app.route('/route', methods = ['GET'])
def route():
    #array de route steps
    return [{"motorModuleRight": 10, "motorModuleLeft": 10, "compass": 70.2, "executionTime": 5.2, "aruco": None, "id": 1}, 
            {"motorModuleRight": 0, "motorModuleLeft": 0, "compass": 60, "executionTime": 3.1, "aruco": 5, "id": 2},
            {"motorModuleRight": 10, "motorModuleLeft": 0, "compass": 68, "executionTime": 6.5, "aruco": None, "id": 3}]

@app.route("/command/route_recording_mode", methods = ['POST'])
def put_route_recording_mode():
    return {'status': 200}

@app.route("/command/end_route_recording_mode", methods = ['POST'])
def post_end_route_recording():
    json_request= request.get_json()
    
    title = json_request['title']
    description = json_request['description']
    n_repeats = json_request['n_repeats']
    interval_between_repeats = json_request['interval_between_repeats']
    return {'status': 200}

@app.route("/command/recording_move_forward", methods = ['POST'])
def post_move_forward():
    execution_succed = True

    return {"status": 200, "value": execution_succed}

@app.route("/command/recording_rotate_right", methods = ['POST'])
def post_rotate_right():
    execution_succed = True

    return {"status": 200, "value": execution_succed}

@app.route("/command/recording_rotate_left", methods = ['POST'])
def post_rotate_left():
    execution_succed = True

    return {"status": 200, "value": execution_succed}

@app.route("/command/recording_read_aruco", methods = ['POST'])
def post_read_aruco():
    aruco = 1

    return {"status": 200, "aruco": aruco}

@app.route("/recording_move_forward_fine", methods = ['GET', 'POST'])
def post_move_forward_fine():
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

@app.route("/command/route_execution_mode", methods = ['GET', 'POST'])
def post_route_execution_mode():
    json_request = request.get_json()

    id_route = json_request['id_route']
    id_robot = json_request['id_robot']
    print(id_route, id_robot)

    return {'status': 200}

@app.route("/turn_camera_servo_right", methods = ['POST'])
def post_turn_camera_servo_right():
    obj_patrole.route_recording.turn_camera_servo_right()

    return {'status': 200, 'aruco': 1}
    
    
if __name__ == "__main__":
    app.run(host = '0.0.0.0',
            port = '5002',
            debug = True) # Must change to False if in production
    
