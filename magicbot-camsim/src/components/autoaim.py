
from networktables.util import ntproperty

from .robotangle import RobotAngle

class AutoAim:
    
    #
    # Magic imports
    #
    
    robot_angle = RobotAngle
    
    #
    # NetworkTables variables
    #
    
    # array of (found, timestamp, angle)
    target = ntproperty('/camera/target', (0.0, float('inf'), 0.0))
    
    def __init__(self):
        self.lastTs = None
        self.angle = None
    
    def aim(self):
        '''Tell the robot to align itself with the target. Returns
           True if found, False otherwise'''
        found, timestamp, offset = self.target
        
        if found > 0:
            
            # Only update the angle when the camera feeds us new data
            if self.lastTs != timestamp:
            
                # remember: the camera tells you the *offset*, so the angle you
                # want the robot to go to is the angle + the offset
                self.angle = self.robot_angle.getAngle() + offset
                
            return self.robot_angle.rotateTo(self.angle)
    
    def execute(self):
        pass
