#!/usr/bin/env python3
#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#

import wpilib
import commands2
import commands2.cmd

import constants

class Intake(commands2.SubsystemBase):

    def __init__(self) -> None:
        super().__init__()

        self.motor = wpilib.PWMSparkMax(constants.IntakeConstants.kMotorPort)
        self.pistons = wpilib.DoubleSolenoid(
            wpilib.PneumaticsModuleType.REVPH,
            *constants.IntakeConstants.kSolenoidPorts
        )
    
    # Returns a command that deploys the intake, and then runs the intake motor indefinitely.
    def intakeCommand(self) -> commands2.Command:
        self.motorSetCommand = self.run(lambda: self.motor.set(1))
        self.motorSetCommand.setName("Intake")
        return self.runOnce(
            lambda: self.pistons.set(wpilib.DoubleSolenoid.Value.kForward)
        ).andThen(
            self.motorSetCommand
        )

    # Returns a command that turns off and retracts the intake.
    def retractCommand(self) -> commands2.Command:
        command = self.runOnce(
            lambda: [self.motor.disable(), self.pistons.set(wpilib.DoubleSolenoid.Value.kReverse)]
        )
        command.setName("Retract")
        return command