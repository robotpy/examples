#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#

import commands2
import commands2.cmd
from . import setwristsetpoint
from . import setelevatorsetpoint
from . import openclaw
from subsystems.elevator import Elevator
from subsystems.wrist import Wrist
from subsystems.claw import Claw

class PrepareToPickup(commands2.SequentialCommandGroup):
    def __init__(self, claw: Claw, wrist: Wrist, elevator: Elevator) -> None:
        """Create a new prepare to pickup command.

        :param claw:     The claw subsystem to use
        :param wrist:    The wrist subsystem to use
        :param elevator: The elevator subsystem to use
        """
        super().__init__()
        self.addCommands(
            openclaw.OpenClaw(claw),
            commands2.cmd.parallel(
                setwristsetpoint.SetWristSetpoint(
                    constants.Positions.Place.kWristSetpoint, wrist
                ),
                setelevatorsetpoint.SetElevatorSetpoint(
                    constants.Positions.Place.kElevatorSetpoint, elevator
                ),
            )
        )
