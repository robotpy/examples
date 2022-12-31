import commands2

import constants

from .drivedistance import DriveDistance
from .releasehatch import ReleaseHatch

from subsystems.drivesubsystem import DriveSubsystem
from subsystems.hatchsubsystem import HatchSubsystem


class ComplexAuto(commands2.SequentialCommandGroup):
    """
    A complex auto command that drives forward, releases a hatch, and then drives backward.
    """

    def __init__(self, drive: DriveSubsystem, hatch: HatchSubsystem):
        super().__init__(
            # Drive forward the specified distance
            DriveDistance(
                constants.kAutoDriveDistanceInches, constants.kAutoDriveSpeed, drive
            ),
            # Release the hatch
            ReleaseHatch(hatch),
            # Drive backward the specified distance
            DriveDistance(
                constants.kAutoBackupDistanceInches, -constants.kAutoDriveSpeed, drive
            ),
        )
