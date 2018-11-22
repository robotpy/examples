#!/usr/bin/env python3
'''
    The SampleRobot class is the base of a robot application that will
    automatically call your Autonomous and OperatorControl methods at
    the right time as controlled by the switches on the driver station
    or the field controls.
    
    WARNING: While it may look like a good choice to use for your code
    if you're inexperienced, don't. Unless you know what you are doing,
    complex code will be much more difficult under this system. Use
    IterativeRobot or Command-Based instead if you're new.
'''


import wpilib
from wpilib.drive import DifferentialDrive

class MyRobot(wpilib.SampleRobot):
    '''Main robot class'''
    
    def robotInit(self):
        '''Robot-wide initialization code should go here'''
        
        self.lstick = wpilib.Joystick(1)
        self.motor = wpilib.Jaguar(8)
        
    def disabled(self):
        '''Called when the robot is disabled'''
        while self.isDisabled():
            wpilib.Timer.delay(0.01)

    def autonomous(self):
        '''Called when autonomous mode is enabled'''
        
        while self.isAutonomous() and self.isEnabled():
            wpilib.Timer.delay(0.01)

    def operatorControl(self):
        '''Called when operation control mode is enabled'''

        timer = wpilib.Timer()
        timer.start()

        while self.isOperatorControl() and self.isEnabled():

            # Move a motor with a Joystick
            self.motor.set(self.lstick.getY())

            if timer.hasPeriodPassed(1.0):
                print("Analog 8: %s" % self.ds.getBatteryVoltage())

            wpilib.Timer.delay(0.02)

if __name__ == '__main__':
    wpilib.run(MyRobot)

