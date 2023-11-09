from mall_security_robot import obj_patrole, server
from handlers.app_communication import AppCommunicationHandler

class Main:
    def __init__(self):
        AppCommunicationHandler.register(
            server,
            route_base = '/command/'
        )

    def start(self):
        """Start the patrole firmware and the local
            communication server for the mobile app.
        """
        obj_patrole.start()
        server.run(
            host = '0.0.0.0',
            port = '5002',
            debug = True # Must change to False if in production
        )

if __name__ == "__main__":
    obj_main = Main()
    obj_main.start()
