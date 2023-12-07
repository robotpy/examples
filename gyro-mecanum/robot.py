#!/usr/bin/env python3
"""
    This is a sample program that uses mecanum drive with a gyro sensor to maintain rotation vectors
    in relation to the starting orientation of the robot (field-oriented controls).
"""

import wpilib
import wpilib.drive


class MyRobot(wpilib.TimedRobot):
    # gyro calibration constant, may need to be adjusted;
    # gyro value of 360 is set to correspond to one full revolution
    kVoltsPerDegreePerSecond = 0.0128

    kFrontLeftChannel = 0
    kRearLeftChannel = 1
    kFrontRightChannel = 2
    kRearRightChannel = 3
    kGyroPort = 0
    kJoystickPort = 0

    def robotInit(self):
        """Robot initialization function"""

        self.gyro = wpilib.AnalogGyro(self.kGyroPort)
        self.joystick = wpilib.Joystick(self.kJoystickPort)

        frontLeft = wpilib.PWMSparkMax(self.kFrontLeftChannel)
        rearLeft = wpilib.PWMSparkMax(self.kRearLeftChannel)
        frontRight = wpilib.PWMSparkMax(self.kFrontRightChannel)
        rearRight = wpilib.PWMSparkMax(self.kRearRightChannel)

        frontRight.setInverted(True)
        rearRight.setInverted(True)

        self.robotDrive = wpilib.drive.MecanumDrive(
            frontLeft, rearLeft, frontRight, rearRight
        )

        self.gyro.setSensitivity(self.kVoltsPerDegreePerSecond)

    def teleopPeriodic(self):
        self.robotDrive.driveCartesian(
            -self.joystick.getY(),
            -self.joystick.getX(),
            -self.joystick.getZ(),
            self.gyro.getRotation2d(),
        )


if __name__ == "__main__":
    wpilib.run(MyRobot)
