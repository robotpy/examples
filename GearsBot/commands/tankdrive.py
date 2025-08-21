#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#

import typing
import commands2
from subsystems.drivetrain import Drivetrain

class TankDrive(commands2.Command):
    """Have the robot drive tank style."""

    def __init__(self, left: typing.Callable[[], float], right:
                 typing.Callable[[], float], drivetrain: Drivetrain) -> None:
        """Creates a new TankDrive command.

        :param left:       The control input for the left side of the drive
        :param right:      The control input for the right sight of the drive
        :param drivetrain: The drivetrain subsystem to drive
        """
        super().__init__()

        self.drivetrain = drivetrain
        self.left = left
        self.right = right
        self.addRequirements([self.drivetrain])

    def execute(self) -> None:
        # Called repeatedly when this Command is scheduled to run
        self.drivetrain.drive(self.left(), self.right())

    def isFinished(self) -> bool:
        # Make this return true when this Command no longer needs to run execute()
        return False
    
    def end(self, interrupted: bool) -> None:
        # Called once after isFinished returns true
        self.drivetrain.drive(0, 0)
