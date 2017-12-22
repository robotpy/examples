#!/usr/bin/env python3

import wpilib
from wpilib.drive import MecanumDrive


class MyRobot(wpilib.SampleRobot):
    '''Main robot class'''

    # Channels on the roboRIO that the motor controllers are plugged in to
    frontLeftChannel = 2
    rearLeftChannel = 3
    frontRightChannel = 1
    rearRightChannel = 0

    # The channel on the driver station that the joystick is connected to
    lStickChannel = 0
    rStickChannel = 1

    def robotInit(self):
        '''Robot initialization function'''
        self.frontLeftMotor = wpilib.Talon(self.frontLeftChannel)
        self.rearLeftMotor = wpilib.Talon(self.rearLeftChannel)
        self.frontRightMotor = wpilib.Talon(self.frontRightChannel)
        self.rearRightMotor = wpilib.Talon(self.rearRightChannel)

        # invert the left side motors
        self.frontLeftMotor.setInverted(True)

        # you may need to change or remove this to match your robot
        self.rearLeftMotor.setInverted(True)

        self.drive = MecanumDrive(self.frontLeftMotor,
                                         self.rearLeftMotor,
                                         self.frontRightMotor,
                                         self.rearRightMotor)

        self.drive.setExpiration(0.1)

        self.lstick = wpilib.Joystick(self.lStickChannel)
        self.rstick = wpilib.Joystick(self.rStickChannel)

        # Position gets automatically updated as robot moves
        self.gyro = wpilib.AnalogGyro(1)

    def disabled(self):
        '''Called when the robot is disabled'''
        while self.isDisabled():
            wpilib.Timer.delay(0.01)

    def autonomous(self):
        '''Called when autonomous mode is enabled'''

        timer = wpilib.Timer()
        timer.start()

        while self.isAutonomous() and self.isEnabled():

            if timer.get() < 2.0:
                self.drive.driveCartesian(0, -1, 1, 0)
            else:
                self.drive.driveCartesian(0, 0, 0, 0)

            wpilib.Timer.delay(0.01)

    def operatorControl(self):
        '''Called when operation control mode is enabled'''

        while self.isOperatorControl() and self.isEnabled():
            self.drive.driveCartesian(self.lstick.getX(), self.lstick.getY(), self.rstick.getX(), 0)

            wpilib.Timer.delay(0.04)


if __name__ == '__main__':
    wpilib.run(MyRobot,
               physics_enabled=True)
