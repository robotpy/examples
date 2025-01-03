#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#

import commands2
from subsystems.claw import Claw

class OpenClaw(commands2.WaitCommand):
    """Opens the claw for one second. Real robots should use sensors, stalling motors is BAD!"""
    def __init__(self, claw: Claw) -> None:
        """Creates a new OpenClaw command.

        :param claw: The claw to use
        """
        super().__init__(1)
        self.claw = claw
        self.addRequirements(self.claw)
        
    def initialize(self) -> None:
        # Called just before this Command runs the first time
        self.claw.open()
        super().initialize()

    def end(self, interrupted: bool) -> None:
        # Called once after isFinished returns true
        self.claw.stop()
