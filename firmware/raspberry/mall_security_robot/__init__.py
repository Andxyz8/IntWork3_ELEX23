from flask import Flask
from mall_security_robot.patrole import Patrole

server = Flask(__name__)
obj_patrole = Patrole()
