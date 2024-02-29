#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#

import commands2
from subsystems.elevator import Elevator

class SetElevatorSetpoint(commands2.Command):
    """Move the elevator to a given location. This command finishes when it is 
    within the tolerance, but leaves the PID loop running to maintain the position. 
    Other commands using the elevator should make sure they disable PID!
    """
    def __init__(self, setpoint: float, elevator: Elevator) -> None:
        """Create a new SetElevatorSetpoint command.

        :param setpoint: The setpoint to set the elevator to
        :param elevator: The elevator to use
        """
        super().__init__()
        self.elevator = elevator
        self.setpoint = setpoint
        self.addRequirements(self.elevator)

    def initialize(self) -> None:
        # Called just before this Command runs the first time
        self.elevator.setSetpoint(self.setpoint)
        self.elevator.enable()

    def isFinished(self) -> bool:
        # Make this return true when this Command no longer needs to run execute()
        return self.elevator.getController().atSetpoint()
