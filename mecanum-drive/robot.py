#!/usr/bin/env python3
"""
    This is a demo program showing how to use Mecanum control with the
    MecanumDrive class.
"""

import wpilib
import wpilib.drive


class MyRobot(wpilib.TimedRobot):
    # Channels on the roboRIO that the motor controllers are plugged in to
    kFrontLeftChannel = 2
    kRearLeftChannel = 3
    kFrontRightChannel = 1
    kRearRightChannel = 0

    # The channel on the driver station that the joystick is connected to
    kJoystickChannel = 0

    def robotInit(self):
        self.frontLeft = wpilib.PWMSparkMax(self.kFrontLeftChannel)
        self.rearLeft = wpilib.PWMSparkMax(self.kRearLeftChannel)
        self.frontRight = wpilib.PWMSparkMax(self.kFrontRightChannel)
        self.rearRight = wpilib.PWMSparkMax(self.kRearRightChannel)

        # invert the right side motors
        # you may need to change or remove this to match your robot
        self.frontRight.setInverted(True)
        self.rearRight.setInverted(True)

        self.robotDrive = wpilib.drive.MecanumDrive(
            self.frontLeft, self.rearLeft, self.frontRight, self.rearRight
        )

        self.stick = wpilib.Joystick(self.kJoystickChannel)

    def teleopPeriodic(self):
        # Use the joystick X axis for lateral movement, Y axis for forward
        # movement, and Z axis for rotation.
        self.robotDrive.driveCartesian(
            -self.stick.getY(),
            -self.stick.getX(),
            -self.stick.getZ(),
        )


if __name__ == "__main__":
    wpilib.run(MyRobot)
