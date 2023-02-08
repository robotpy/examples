#!/usr/bin/env python3

import wpilib
from wpilib.drive import DifferentialDrive


class MyRobot(wpilib.TimedRobot):
    """This is a demo program showing how to use Gyro control with the
    DifferentialDrive class."""

    def robotInit(self):
        """Robot initialization function"""
        gyroChannel = 0  # analog input

        self.joystickChannel = 0  # usb number in DriverStation

        # channels for motors
        self.leftMotorChannel = 1
        self.rightMotorChannel = 0
        self.leftRearMotorChannel = 3
        self.rightRearMotorChannel = 2

        self.angleSetpoint = 0.0
        self.pGain = 1  # propotional turning constant

        # gyro calibration constant, may need to be adjusted
        # gyro value of 360 is set to correspond to one full revolution
        self.voltsPerDegreePerSecond = 0.0128

        self.left = wpilib.MotorControllerGroup(
            wpilib.Talon(self.leftMotorChannel), wpilib.Talon(self.leftRearMotorChannel)
        )
        self.right = wpilib.MotorControllerGroup(
            wpilib.Talon(self.rightMotorChannel),
            wpilib.Talon(self.rightRearMotorChannel),
        )
        self.myRobot = DifferentialDrive(self.left, self.right)

        self.gyro = wpilib.AnalogGyro(gyroChannel)
        self.joystick = wpilib.Joystick(self.joystickChannel)

    def teleopInit(self):
        """
        Runs at the beginning of the teleop period
        """
        self.gyro.setSensitivity(
            self.voltsPerDegreePerSecond
        )  # calibrates gyro values to equal degrees

    def teleopPeriodic(self):
        """
        Sets the gyro sensitivity and drives the robot when the joystick is pushed. The
        motor speed is set from the joystick while the RobotDrive turning value is assigned
        from the error between the setpoint and the gyro angle.
        """

        turningValue = (self.angleSetpoint - self.gyro.getAngle()) * self.pGain
        if self.joystick.getY() <= 0:
            # forwards
            self.myRobot.arcadeDrive(self.joystick.getY(), turningValue)
        elif self.joystick.getY() > 0:
            # backwards
            self.myRobot.arcadeDrive(self.joystick.getY(), -turningValue)


if __name__ == "__main__":
    wpilib.run(MyRobot)
