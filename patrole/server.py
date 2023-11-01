from flask import Flask
from flask import request

app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def index():
    return {"found": True}
    
@app.route('/command', methods = ['GET', 'POST'])
def commands():
    if request.method == 'POST':
        data = request.get_json()
        print(data["command"])
        if data["command"] == "READ": #e o aruco lido e igual ao primeiro
            return {"last": True}
    return {"last": False}

@app.route('/route', methods = ['GET'])
def route():
    #array de route steps
    return [{"motorModuleRight": 10, "motorModuleLeft": 10, "compass": 70.2, "executionTime": 5.2, "aruco": None, "id": 1}, 
            {"motorModuleRight": 0, "motorModuleLeft": 0, "compass": 60, "executionTime": 3.1, "aruco": 5, "id": 2},
            {"motorModuleRight": 10, "motorModuleLeft": 0, "compass": 68, "executionTime": 6.5, "aruco": None, "id": 3}]
    
    
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
    
