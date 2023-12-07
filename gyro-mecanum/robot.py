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
    VOLTS_PER_DEGREE_PER_SECOND = 0.0128

    FRONT_LEFT_CHANNEL = 0
    REAR_LEFT_CHANNEL = 1
    FRONT_RIGHT_CHANNEL = 2
    REAR_RIGHT_CHANNEL = 3
    GYRO_PORT = 0
    JOYSTICK_PORT = 0

    def robotInit(self):
        """Robot initialization function"""

        self.gyro = wpilib.AnalogGyro(self.GYRO_PORT)
        self.joystick = wpilib.Joystick(self.JOYSTICK_PORT)

        frontLeft = wpilib.PWMSparkMax(self.FRONT_LEFT_CHANNEL)
        rearLeft = wpilib.PWMSparkMax(self.REAR_LEFT_CHANNEL)
        frontRight = wpilib.PWMSparkMax(self.FRONT_RIGHT_CHANNEL)
        rearRight = wpilib.PWMSparkMax(self.REAR_RIGHT_CHANNEL)

        frontRight.setInverted(True)
        rearRight.setInverted(True)

        self.robotDrive = wpilib.drive.MecanumDrive(
            frontLeft, rearLeft, frontRight, rearRight
        )

        self.gyro.setSensitivity(self.VOLTS_PER_DEGREE_PER_SECOND)

    def teleopPeriodic(self):
        self.robotDrive.driveCartesian(
            -self.joystick.getY(),
            -self.joystick.getX(),
            -self.joystick.getZ(),
            self.gyro.getRotation2d(),
        )


if __name__ == "__main__":
    wpilib.run(MyRobot)
