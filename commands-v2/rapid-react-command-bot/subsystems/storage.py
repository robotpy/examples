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


class Storage(commands2.SubsystemBase):
    def __init__(self) -> None:
        "Create a new Storage subsystem."

        super().__init__()

        self.motor = wpilib.PWMSparkMax(constants.StorageConstants.kMotorPort)
        self.ballSensor = wpilib.DigitalInput(
            constants.StorageConstants.kBallSensorPort
        )

        # Set default command to turn off the storage motor and then idle
        self.defaultCommand = commands2.cmd.nothing()
        self.defaultCommand.setName("Idle")
        self.setDefaultCommand(
            self.runOnce(lambda: self.motor.disable()).andThen(self.defaultCommand)
        )

    def isFull(self) -> bool:
        "Whether the ball storage is full."
        return self.ballSensor.get()

    def runCommand(self) -> commands2.CommandBase:
        "Returns a command that runs the storage motor indefinitely."
        command = self.run(lambda: self.motor.set(1))
        command.setName("Run")

        return command
