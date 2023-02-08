import wpilib
import commands2
import commands2.cmd

import constants


class HatchSubsystem(commands2.SubsystemBase):
    def __init__(self) -> None:
        super().__init__()

        self.hatchSolenoid = wpilib.DoubleSolenoid(
            constants.kHatchSolenoidModule,
            constants.kHatchSolenoidModuleType,
            *constants.kHatchSolenoidPorts
        )

    def grabHatch(self) -> commands2.Command:
        """Grabs the hatch"""
        return commands2.cmd.runOnce(
            lambda: self.hatchSolenoid.set(wpilib.DoubleSolenoid.Value.kForward), [self]
        )

    def releaseHatch(self) -> commands2.Command:
        """Releases the hatch"""
        return commands2.cmd.runOnce(
            lambda: self.hatchSolenoid.set(wpilib.DoubleSolenoid.Value.kReverse), [self]
        )
