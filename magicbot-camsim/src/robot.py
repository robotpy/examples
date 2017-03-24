#!/usr/bin/env python3

import magicbot
import wpilib

from components.autoaim import AutoAim
from components.drivetrain import DriveTrain
from components.robotangle import RobotAngle

class MyRobot(magicbot.MagicRobot):
    '''Main robot class'''
    
    autoaim = AutoAim
    robot_angle = RobotAngle
    drivetrain = DriveTrain
    
    def createObjects(self):
        '''Robot-wide initialization code should go here'''
        
        # Basic robot chassis setup
        self.stick = wpilib.Joystick(0)
        self.robotdrive = wpilib.RobotDrive(0, 1)
        
        # Position gets automatically updated as robot moves
        self.gyro = wpilib.ADXRS450_Gyro()

    def teleopPeriodic(self):
        '''Called every 20ms in teleop'''
        
        self.drivetrain.move(self.stick.getY(), self.stick.getX())
        
        # if trigger is pressed, then center the robot to the camera target
        if self.stick.getTrigger():
            self.autoaim.aim()

if __name__ == '__main__':
    wpilib.run(MyRobot)
