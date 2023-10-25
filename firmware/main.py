from mall_security_robot.mall_security_robot import MallSecurityRobot

class Main:
    def __init__(self):
        robot: MallSecurityRobot = None
    
    def start(self):
        obj_patrole = MallSecurityRobot()
        obj_patrole.start()


if __name__ == "__main__":
    obj_main = Main()
    obj_main.start()
