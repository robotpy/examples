#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#

import commands2
import commands2.cmd
import constants
from . import closeclaw
from . import setwristsetpoint
from . import setelevatorsetpoint
from subsystems.claw import Claw
from subsystems.elevator import Elevator
from subsystems.wrist import Wrist

class Pickup(commands2.SequentialCommandGroup):
    """Pickup a soda can (if one is between the open claws) and get it in a
    safe state to drive around."""

    def __init__(self, claw: Claw, wrist: Wrist, elevator: Elevator) -> None:
        """Create a new pickup command.

        :param claw:     The claw subsystem to use
        :param wrist:    The wrist subsystem to use
        :param elevator: The elevator subsystem to use
        """
        self.addCommands(closeclaw.CloseClaw(claw))
        commands2.cmd.parallel(
            setwristsetpoint.SetWristSetpoint(
                constants.Position.Pickup.kWristSetpoint, wrist
            ),
            setelevatorsetpoint.SetElevatorSetpoint(
                constants.Position.Pickup.kElevatorSetpoint, elevator
            ),
        )
