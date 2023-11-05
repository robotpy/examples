import commands2
from subsystems.hatchsubsystem import HatchSubsystem


class GrabHatch(commands2.Command):
    def __init__(self, hatch: HatchSubsystem) -> None:
        super().__init__()
        self.hatch = hatch
        self.addRequirements(hatch)

    def initialize(self) -> None:
        self.hatch.grabHatch()

    def isFinished(self) -> bool:
        return True
