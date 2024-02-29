#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#

import constants
import commands2.button
import commands2.cmd

class RobotContainer:
    """
    This class is where the bulk of the robot should be declared. Since Command-based is a
    "declarative" paradigm, very little robot logic should actually be handled in the :class:`.Robot`
    periodic methods (other than the scheduler calls). Instead, the structure of the robot (including
    subsystems, commands, and button mappings) should be declared here.
    """

    def __init__(self) -> None:
        # The robot's subsystems
        self.robotDrive = DriveSubsystem()
        self.robotArm = ArmSubsystem()

        # The driver's controller
        self.driverController = commands2.button.CommandXboxController(
            constants.kDriverControllerPort
        )
        # self.driverController = wpilib.Joystick(constants.kDriverControllerPort)

        # Configure the button bindings
        self.configureButtonBindings()

        # Set the default drive command
        self.robotDrive.setDefaultCommand(
            self.robotDrive.arcadeDriveCommand(
                lambda: -self.driverController.getLeftY(),
                lambda: -self.driverController.getRightX(),
            )
        )

    def configureButtonBindings(self) -> None:
        """
        Use this method to define your button->command mappings. Buttons can be created by
        instantiating a :GenericHID or one of its subclasses (Joystick or XboxController),
        and then passing it to a JoystickButton.
        """

    def getAutonomousCommand(self) -> commands2.Command:
        return commands2.cmd.none()
