#!/usr/bin/env python3
#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#

import commands2
import commands2.cmd
import wpilib
import wpimath.controller

import constants


class Shooter(commands2.SubsystemBase):
    def __init__(self) -> None:
        "The shooter subsystem for the robot."

        super().__init__()

        self.shooterMotor = wpilib.PWMSparkMax(
            constants.ShooterConstants.kShooterMotorPort
        )
        self.feederMotor = wpilib.PWMSparkMax(
            constants.ShooterConstants.kFeederMotorPort
        )
        self.shooterEncoder = wpilib.Encoder(
            *constants.ShooterConstants.kEncoderPorts,
            constants.ShooterConstants.kEncoderReversed
        )
        self.shooterFeedforward = wpimath.controller.SimpleMotorFeedforwardMeters(
            constants.ShooterConstants.kSVolts,
            constants.ShooterConstants.kVVoltSecondsPerRotation,
        )
        self.shooterFeedback = wpimath.controller.PIDController(
            constants.ShooterConstants.kP, 0, 0
        )

        self.shooterFeedback.setTolerance(
            constants.ShooterConstants.kShooterToleranceRPS
        )
        self.shooterEncoder.setDistancePerPulse(
            constants.ShooterConstants.kEncoderDistancePerPulse
        )

        # Set default command to turn off both the shooter and feeder motors, and then idle
        self.defaultCommand = self.runOnce(
            lambda: [self.shooterMotor.disable(), self.feederMotor.disable()]
        )
        self.defaultCommand.setName("Idle")
        self.setDefaultCommand(
            self.defaultCommand.andThen(self.run(lambda: commands2.cmd.nothing()))
        )

    def shootCommand(self, setpointRotationsPerSecond: float):
        """Returns a command to shoot the balls currently stored in the robot. Spins the shooter flywheel
        up to the specified setpoint, and then runs the feeder motor.

        :param setpointRotationsPerSecond: The desired shooter velocity
        """
        command = commands2.cmd.parallel(
            # Run the shooter flywheel at the desired setpoint using feedforward and feedback
            self.run(
                lambda: self.shooterMotor.set(
                    self.shooterFeedforward.calculate(setpointRotationsPerSecond)
                    + self.shooterFeedback.calculate(
                        self.shooterEncoder.getRate(), setpointRotationsPerSecond
                    )
                )
            ),
            # Wait until the shooter has reached the setpoint, and then run the feeder
            commands2.cmd.waitUntil(lambda: self.shooterFeedback.atSetpoint()).andThen(
                lambda: self.feederMotor.set(1)
            ),
        )
        command.setName("Shoot")

        return command
