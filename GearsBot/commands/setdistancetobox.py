#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#

import commands2
import wpimath.controller
from subsystems.drivetrain import Drivetrain

class SetDistanceToBox(commands2.PIDCommand):
    """Drive until the robot is the given distance away from the box. Uses a local 
    PID controller to run a simple PID loop that is only enabled while this command is
    running. The input is the averaged values of the left and right encoders.
    """

    def __init__(self, distance: float, drivetrain: Drivetrain) -> None:
        """Create a new set distance to box command.

        :param distance: The distance away from the box to drive to
        """
        super().__init__(
            wpimath.controller.PIDController(-2, 0, 0),
            drivetrain.getDistanceToObstacle(),
            distance,
            lambda d : drivetrain.drive(d, d)
        )
        self.drivetrain = drivetrain
        self.addRequirements(self.drivetrain)
        self.getController().setTolerance(0.01)

    def initialize(self) -> None:
        # Called just before this Command runs the first time
        # Get everything in a safe starting state.
        self.drivetrain.reset()
        super().initialize()

    def isFinished(self) -> bool:
        # Make this return true when this Command no longer needs to run execute()
        return self.getController().atSetpoint()
