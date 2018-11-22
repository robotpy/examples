#!/usr/bin/env python3
'''
    This is a demo program showing the use of the RobotDrive class,
    specifically it contains the code necessary to operate a robot with
    a single joystick
'''

import wpilib

class MyRobot(wpilib.IterativeRobot):
    
    def robotInit(self):
        '''Robot initialization function'''
        
        # object that handles basic drive operations
        self.myRobot = wpilib.RobotDrive(0, 1)
        self.myRobot.setExpiration(0.1)
        
        # joystick #0
        self.stick = wpilib.Joystick(0)
    
    def teleopInit(self):
        '''Executed at the start of teleop mode'''
        self.myRobot.setSafetyEnabled(True)
    
    def teleopPeriodic(self):
        '''Runs the motors with tank steering'''
        self.myRobot.arcadeDrive(self.stick, True)
            
if __name__ == '__main__':
    wpilib.run(MyRobot)
