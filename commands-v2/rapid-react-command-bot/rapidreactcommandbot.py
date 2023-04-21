#!/usr/bin/env python3
#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#

import commands2
import commands2.button
import commands2.cmd

import subsystems.intake
import subsystems.drive
import subsystems.shooter
import subsystems.storage

import constants


class RapidReactCommandBot:
    """
    This class is where the bulk of the robot should be declared. Since Command-based is a
    "declarative" paradigm, very little robot logic should actually be handled in the :class:`.Robot`
    periodic methods (other than the scheduler calls). Instead, the structure of the robot (including
    subsystems, commands, and button mappings) should be declared here.
    """

    def __init__(self) -> None:
        # The robot's subsystems
        self.drive = subsystems.drive.Drive()
        self.intake = subsystems.intake.Intake()
        self.storage = subsystems.storage.Storage()
        self.shooter = subsystems.shooter.Shooter()

        # The driver's controller
        self.driverController = commands2.button.CommandXboxController(
            constants.OIConstants.kDriverControllerPort
        )

        self.configureButtonBindings()

    def configureButtonBindings(self):
        """Use this method to define bindings between conditions and commands. These are useful for
        automating robot behaviors based on button and sensor input.

        Should be called during :meth:`.Robot.robotInit`.

        Event binding methods are available on the {@link Trigger} class.
        """
        # Automatically run the storage motor whenever the ball storage is not full,
        # and turn it off whenever it fills.
        commands2.Trigger(lambda: self.storage.isFull()).whileFalse(
            self.storage.runCommand()
        )

        # Automatically disable and retract the intake whenever the ball storage is full.
        commands2.Trigger(lambda: self.storage.isFull()).onTrue(
            self.intake.retractCommand()
        )

        # Control the drive with split-stick arcade controls
        self.drive.setDefaultCommand(
            self.drive.arcadeDriveCommand(
                lambda: self.driverController.getLeftY(),
                lambda: self.driverController.getRightX(),
            )
        )

        # Deploy the intake with the X button
        self.driverController.X().onTrue(self.intake.intakeCommand())
        # Retract the intake with the Y button
        self.driverController.Y().onTrue(self.intake.retractCommand())

        # Compose master shoot command
        self.masterShootCommand = commands2.cmd.parallel(
            self.shooter.shootCommand(constants.ShooterConstants.kShooterTargetRPS),
            self.storage.runCommand(),
        )
        # Since we composed this inline we should give it a name
        self.masterShootCommand.setName("Shoot")
        # Fire the shooter with the A button
        self.driverController.A().onTrue(self.masterShootCommand)

    def getAutonomousCommand(self) -> commands2.Command:
        """Use this to define the command that runs during autonomous.

        Scheduled during :meth:`.Robot.autonomousInit`.
        """
        return self.drive.driveDistanceCommand(
            constants.AutoConstants.kDriveDistanceMeters,
            constants.AutoConstants.kDriveSpeed,
        ).withTimeout(constants.AutoConstants.kTimeoutSeconds)
