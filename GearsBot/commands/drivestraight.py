#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#

import commands2
import wpimath.controller
import ..constants2
from subsystems.drivetrain import Drivetrain

class DriveStraight(commands2.PIDCommand):
    """Drive the given distance straight (negative values go backwards). 
    Uses a local PID controller to run a simple PID loop that is only 
    enabled while this command is running. The input is the
    averaged values of the left and right encoders.
    """

    def __init__(self, distance: float, drivetrain: Drivetrain) -> None:
        """Create a new DriveStraight command.
        
        :param distance: The distance to drive
        """
        super().__init__(
            wpimath.controller.PIDController(
                constants.DriveStraightConstants.kP,
                constants.DriveStraightConstants.kI,
                constants.DriveStraightConstants.kD,
            ),
            drivetrain.getDistance(),
            distance,
            lambda d: drivetrain.drive(d, d)
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
