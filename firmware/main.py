from mall_security_robot.mall_security_robot import MallSecurityRobot

class Main:
    def __init__(self):
        self.patrole: MallSecurityRobot = None
    
    def start(self):
        self.patrole = MallSecurityRobot()
        self.patrole.start()


if __name__ == "__main__":
    obj_main = Main()
    obj_main.start()
