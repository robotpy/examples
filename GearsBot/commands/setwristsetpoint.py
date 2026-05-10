#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#

import commands2
from subsystems.wrist import Wrist

class SetWristSetpoint(commands2.Command):
    def __init__(self, setpoint: float, wrist: Wrist) -> None:
        """Create a new SetWristSetpoint command.

        :param setpoint: The setpoint to set the wrist to
        :param wrist:    The wrist to use
        """
        super().__init__()
        self.wrist = wrist
        self.setpoint = setpoint
        self.addRequirements(self.wrist)

    def initialize(self) -> None:
        # Called just before this Command runs the first time
        self.wrist.setSetpoint(self.setpoint)
        self.wrist.enable()

    def isFinished(self) -> bool:
        # Make this return true when this Command no longer needs to run execute()
        return self.wrist.getController().atSetpoint()
