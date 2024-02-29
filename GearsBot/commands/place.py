#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#

import commands2
import setelevatorsetpoint
import setwristsetpoint
import openclaw
import ..constants
from subsystems.claw import Claw
from subsystems.elevator import Elevator
from subsystems.wrist import Wrist

class Place(commands2.SequentialCommandGroup):
    """Place a held soda can onto the platform."""

    def __init__(self, claw: Claw, wrist: Wrist, elevator: Elevator) -> None:
        """Create a new place command.

        :param claw:     The claw subsystem to use
        :param wrist:    The wrist subsystem to use
        :param elevator: The elevator subsystem to use
        """
        super().__init__()
        self.addCommands(
            setelevatorsetpoint.SetElevatorSetpoint(
                constants.Positions.Place.kElevatorSetpoint, elevator
            ),
            setwristsetpoint.SetWristSetpoint(
                constants.Positions.Place.kWristSetpoint, wrist
            ),
            openclaw.OpenClaw(claw)
        )
