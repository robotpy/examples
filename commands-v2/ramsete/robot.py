from commands2 import TimedCommandRobot

from robotcontainer import RobotContainer

class MyRobot(TimedCommandRobot):
    
    def robotInit(self) -> None:
        self.container = RobotContainer()