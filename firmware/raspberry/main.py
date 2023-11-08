from mall_security_robot import obj_patrole, server
from handlers.app_communication import AppCommunicationHandler

class Main:
    def __init__(self):
        AppCommunicationHandler.register(
            server,
            route_base = '/command/'
        )

    def start(self):
        obj_patrole.start()
        server.run(
            host = '127.0.0.1',
            port = '5002',
            debug = True # Must change to False if in production
        )

if __name__ == "__main__":
    obj_main = Main()
    obj_main.start()
