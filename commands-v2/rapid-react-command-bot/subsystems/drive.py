#!/usr/bin/env python3
#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#

import wpilib
import wpilib.drive
import commands2
import commands2.cmd

import constants


class Drive(commands2.SubsystemBase):
    def __init__(self) -> None:
        """Creates a new Drive subsystem."""

        super().__init__()

        # The motors on the left side of the drive.
        self.leftMotors = wpilib.MotorControllerGroup(
            wpilib.PWMSparkMax(constants.DriveConstants.kLeftMotor1Port),
            wpilib.PWMSparkMax(constants.DriveConstants.kLeftMotor2Port),
        )

        # The motors on the right side of the drive.
        self.rightMotors = wpilib.MotorControllerGroup(
            wpilib.PWMSparkMax(constants.DriveConstants.kRightMotor1Port),
            wpilib.PWMSparkMax(constants.DriveConstants.kRightMotor2Port),
        )

        # The robot's drive
        self.drive = wpilib.drive.DifferentialDrive(self.leftMotors, self.rightMotors)

        # The left-side drive encoder
        self.leftEncoder = wpilib.Encoder(
            *constants.DriveConstants.kLeftEncoderPorts,
            constants.DriveConstants.kLeftEncoderReversed
        )

        # The right-side drive encoder
        self.rightEncoder = wpilib.Encoder(
            *constants.DriveConstants.kRightEncoderPorts,
            constants.DriveConstants.kRightEncoderReversed
        )

        # We need to invert one side of the drivetrain so that positive voltages
        # result in both sides moving forward. Depending on how your robot's
        # gearbox is constructed, you might have to invert the left side instead.
        self.rightMotors.setInverted(True)

        # Sets the distance per pulse for the encoders
        self.leftEncoder.setDistancePerPulse(
            constants.DriveConstants.kEncoderDistancePerPulse
        )
        self.rightEncoder.setDistancePerPulse(
            constants.DriveConstants.kEncoderDistancePerPulse
        )

    def arcadeDriveCommand(self, fwd, rot) -> commands2.Command:
        # A split-stick arcade command, with forward/backward controlled by the left
        # hand, and turning controlled by the right.
        command = self.run(lambda: self.drive.arcadeDrive(fwd(), rot()))
        command.setName("arcadeDrive")
        return command

    def driveDistanceCommand(
        self, distanceMeters: float, speed: float
    ) -> commands2.SequentialCommandGroup:
        return (
            self.runOnce(
                # Reset encoders at the start of the command
                lambda: [self.leftEncoder.reset(), self.rightEncoder.reset()]
            )
            .andThen(
                # Drive forward at specified speed
                self.run(lambda: self.drive.arcadeDrive(speed, 0))
            )
            .until(
                # End command when we've traveled the specified distance
                lambda: max(
                    self.leftEncoder.getDistance(), self.rightEncoder.getDistance()
                )
                >= distanceMeters
            )
            .andThen(
                # Stop the drive when the command ends
                commands2.cmd.runOnce(lambda: self.drive.stopMotor(), [self])
            )
        )
