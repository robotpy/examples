import commands2

from subsystems.hatchsubsystem import HatchSubsystem


class ReleaseHatch(commands2.InstantCommand):
    def __init__(self, hatch: HatchSubsystem) -> None:
        super().__init__(hatch.releaseHatch, hatch)
