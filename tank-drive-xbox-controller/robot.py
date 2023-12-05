#!/usr/bin/env python3
"""
    This is a demo program showing the use of the DifferentialDrive class.
    Runs the motors with tank steering and an Xbox controller.
"""

import wpilib
from wpilib.drive import DifferentialDrive


class MyRobot(wpilib.TimedRobot):
    def robotInit(self):
        """Robot initialization function"""

        # object that handles basic drive operations
        left = wpilib.PWMSparkMax(0)
        right = wpilib.PWMSparkMax(1)

        self.robotDrive = DifferentialDrive(left, right)

        # xbox controller 0 on the driver station
        self.driverController = wpilib.XboxController(0)

        # We need to invert one side of the drivetrain so that positive voltages
        # result in both sides moving forward. Depending on how your robot's
        # gearbox is constructed, you might have to invert the left side instead.
        right.setInverted(True)

    def teleopPeriodic(self):
        # Drive with tank drive.
        # That means that the Y axis of the left stick moves the left side
        # of the robot forward and backward, and the Y axis of the right stick
        # moves the right side of the robot forward and backward.
        self.robotDrive.tankDrive(
            -self.driverController.getLeftY(), -self.driverController.getRightY()
        )


if __name__ == "__main__":
    wpilib.run(MyRobot)
