#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#

import commands2
import commands2.cmd
from . import preparetopickup
import constants
from subsystems.drivetrain import Drivetrain
from subsystems.claw import Claw
from subsystems.elevator import Elevator
from subsystems.wrist import Wrist

class Autonomous(commands2.SequentialCommandGroup):
    """The main autonomous command to pickup and deliver the soda to the box."""

    def __init__(self, drive: Drivetrain, claw: Claw, wrist: Wrist, elevator:
                 Elevator) -> None:
        """Create a new autonomous command."""
        super().__init__()

        self.addCommands(
            preparetopickup.PrepareToPickup(claw, wrist, elevator),
            pickup.Pickup(claw, wrist, elevator),
            setdistancetobox.SetDistanceToBox(
                constants.AutoConstants.kDistToBox1, drive
            ),
            # drivestraight.DriveStraight(4) # Use encoders if ultrasonic is broken
            place.Place(claw, wrist, elevator),
            setdistancetobox.SetDistanceToBox(
                constants.AutoConstants.kDistToBox2, drive
            ),
            # drivestraight.DriveStraight(-2) # Use encoders if ultrasonic is broken
            commands2.parallel(
                setwristsetpoint.SetWristSetpoint(
                    constants.AutoConstants.kWristSetpoint, wrist
                ),
                closeclaw.CloseClaw(claw)
            )
        )
