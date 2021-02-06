import wpilib
import commands2

import constants


class HatchSubsystem(commands2.SubsystemBase):
    def __init__(self) -> None:
        super().__init__()

        self.hatchSolenoid = wpilib.DoubleSolenoid(
            constants.kHatchSolenoidModule, *constants.kHatchSolenoidPorts
        )

    def grabHatch(self) -> None:
        """Grabs the hatch"""
        self.hatchSolenoid.set(wpilib.DoubleSolenoid.Value.kForward)

    def releaseHatch(self) -> None:
        """Releases the hatch"""
        self.hatchSolenoid.set(wpilib.DoubleSolenoid.Value.kReverse)
