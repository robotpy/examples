#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#

import commands2
from subsystems.claw import Claw
import ..robot

class CloseClaw(commands2.Command):
    """Closes the claw until the limit switch is tripped."""

    def __init__(self, claw: Claw) -> None:
        self.claw = claw
        self.addRequirements(self.claw)

    def initialize(self) -> None:
        # Called just before this Command runs the first time
        self.claw.close()

    def isFinished(self) -> bool:
        # Make this return true when this Command no longer needs to run execute()
        return self.claw.isGrabbing()
    
    def end(self, interrupted: bool) -> None:
        # Called once after isFinished returns true
        
        # NOTE: Doesn't stop in simulation due to lower friction causing the
        # can to fall out + there is no need to worry about stalling the motor 
        # or crushing the can.

        if !robot.MyRobot.isSimulation():
            self.claw.stop()
