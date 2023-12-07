#!/usr/bin/env python3
#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#

import wpilib
import wpilib.drive


class MyRobot(wpilib.TimedRobot):
    """
    This is a demo program showing the use of the DifferentialDrive class.
    Runs the motors with arcade steering.
    """

    def robotInit(self):
        """Robot initialization function"""

        # create motor controller objects
        left = wpilib.PWMSparkMax(0)
        right = wpilib.PWMSparkMax(1)

        # object that handles basic drive operations
        self.robotDrive = wpilib.drive.DifferentialDrive(left, right)

        # joystick 0 on the driver station
        self.stick = wpilib.Joystick(0)

        # We need to invert one side of the drivetrain so that positive voltages
        # result in both sides moving forward. Depending on how your robot's
        # gearbox is constructed, you might have to invert the left side instead.
        right.setInverted(True)

    def teleopPeriodic(self):
        # Drive with split arcade style
        # That means that the Y axis of the left stick moves forward
        # and backward, and the X of the right stick turns left and right.
        self.robotDrive.arcadeDrive(-self.stick.getY(), -self.stick.getX())


if __name__ == "__main__":
    wpilib.run(MyRobot)
