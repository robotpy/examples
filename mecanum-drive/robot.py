#!/usr/bin/env python3
"""
    This is a demo program showing how to use Mecanum control with the
    MecanumDrive class.
"""

import wpilib
from wpilib.drive import MecanumDrive
from wpilib import Joystick, PWMSparkMax, TimedRobot


class MyRobot(TimedRobot):
    # Channels on the roboRIO that the motor controllers are plugged in to
    kFrontLeftChannel = 2
    kRearLeftChannel = 3
    kFrontRightChannel = 1
    kRearRightChannel = 0

    # The channel on the driver station that the joystick is connected to
    kJoystickChannel = 0

    def robotInit(self):
        self.frontLeft = PWMSparkMax(self.kFrontLeftChannel)
        self.rearLeft = PWMSparkMax(self.kRearLeftChannel)
        self.frontRight = PWMSparkMax(self.kFrontRightChannel)
        self.rearRight = PWMSparkMax(self.kRearRightChannel)

        # invert the right side motors
        # you may need to change or remove this to match your robot
        self.frontRight.setInverted(True)
        self.rearRight.setInverted(True)

        self.m_drive = MecanumDrive(self.frontLeft, self.rearLeft, self.frontRight, self.rearRight)

        self.m_stick = Joystick(self.kJoystickChannel)

    def teleopPeriodic(self):
        # Use the joystick X axis for lateral movement, Y axis for forward
        # movement, and Z axis for rotation.
        self.m_drive.driveCartesian(-self.m_stick.getY(), self.m_stick.getX(), self.m_stick.getZ(), 0)


if __name__ == "__main__":
    wpilib.run(MyRobot)
