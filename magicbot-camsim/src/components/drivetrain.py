
import wpilib

class DriveTrain:
    '''
        Simple magicbot drive object
    '''
    
    robotdrive = wpilib.RobotDrive
    
    def __init__(self):
        self.x = 0
        self.y = 0
    
    def move(self, y, x):
        self.y = y
        self.x = x
        
    def rotate(self, x):
        self.x = x
        
    def execute(self):
        self.robotdrive.arcadeDrive(self.y, self.x, True)
        
        self.x = 0
        self.y = 0
