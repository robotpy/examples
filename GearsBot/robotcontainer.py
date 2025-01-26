#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#

import wpilib
import constants
import commands2
import commands2.button
from subsystems.drivetrain import Drivetrain
from subsystems.elevator import Elevator
from subsystems.wrist import Wrist
from subsystems.claw import Claw
from commands.autonomous import Autonomous
from commands.setelevatorsetpoint import SetElevatorSetpoint
from commands.setwristsetpoint import SetWristSetpoint
from commands.openclaw import OpenClaw
from commands.closeclaw import CloseClaw
from commands.tankdrive import TankDrive
from commands.pickup import Pickup
from commands.place import Place

class RobotContainer:
    """This class is where the bulk of the robot should be declared. Since Command-based is a
    "declarative" paradigm, very little robot logic should actually be handled in the :class:`.Robot`
    periodic methods (other than the scheduler calls). Instead, the structure of the robot (including
    subsystems, commands, and button mappings) should be declared here.
    """

    def __init__(self) -> None:
        """The container for the robot. Contains subsystems, OI devices, and commands."""
        # The robot's subsystems and commands are defined here...
        self.drivetrain = Drivetrain()
        self.elevator = Elevator()
        self.wrist = Wrist()
        self.claw = Claw()

        self.joystick = wpilib.XboxController(0)
        
        self.autonomousCommand = Autonomous(
            self.drivetrain, self.claw, self.wrist, self.elevator
        )

        # Put Some buttons on the SmartDashboard
        wpilib.SmartDashboard.putData(
            "Elevator Bottom", SetElevatorSetpoint(0, self.elevator)
        )
        wpilib.SmartDashboard.putData(
            "Elevator Top", SetElevatorSetpoint(0.25, self.elevator)
        )
        wpilib.SmartDashboard.putData(
            "Wrist Horizontal", SetWristSetpoint(0, self.wrist)
        )
        wpilib.SmartDashboard.putData(
            "Raise Wrist", SetWristSetpoint(-45, self.wrist)
        )
        wpilib.SmartDashboard.putData(
            "Open Claw", OpenClaw(self.claw)
        )
        wpilib.SmartDashboard.putData(
            "Close Claw", CloseClaw(self.claw)
        )
        wpilib.SmartDashboard.putData(
            "Deliver Soda", 
            Autonomous(self.drivetrain, self.claw, self.wrist, self.elevator)
        )

        # Assign default commands
        self.drivetrain.setDefaultCommand(
            TankDrive(
                lambda: -self.joystick.getLeftY(),
                lambda: -self.joystick.getRightY(),
                self.drivetrain
            ),
        )

        # Show what command your subsystem is running on the SmartDashboard
        wpilib.SmartDashboard.putData(self.drivetrain)
        wpilib.SmartDashboard.putData(self.elevator)
        wpilib.SmartDashboard.putData(self.wrist)
        wpilib.SmartDashboard.putData(self.claw)

        # Configure the button bindings
        self.configureButtonBindings()

    def configureButtonBindings(self) -> None:
        """Use this method to define your button->command mappings. Buttons can be created by
        instantiating a :GenericHID or one of its subclasses (Joystick or XboxController),
        and then passing it to a JoystickButton.
        """
        # Create some buttons
        dpadUp = commands2.button.JoystickButton(self.joystick, 5)
        dpadRight = commands2.button.JoystickButton(self.joystick, 6)
        dpadDown = commands2.button.JoystickButton(self.joystick, 7)
        dpadLeft = commands2.button.JoystickButton(self.joystick, 8)
        l2 = commands2.button.JoystickButton(self.joystick, 9)
        r2 = commands2.button.JoystickButton(self.joystick, 10)
        l1 = commands2.button.JoystickButton(self.joystick, 11)
        r1 = commands2.button.JoystickButton(self.joystick, 12)
        
        # Connect the buttons to commands
        dpadUp.onTrue(SetElevatorSetpoint(0.25, self.elevator))
        dpadDown.onTrue(SetElevatorSetpoint(0.0, self.elevator))
        dpadRight.onTrue(CloseClaw(self.claw))
        dpadLeft.onTrue(OpenClaw(self.claw))

        r1.onTrue(PrepareToPickup(self.claw, self.wrist, self.elevator))
        r2.onTrue(Pickup(self.claw, self.wrist, self.elevator))
        l1.onTrue(Place(self.claw, self.wrist, self.elevator))
        l2.onTrue(Autonomous(self.drivetrain, self.claw, self.wrist, self.elevator))

    def getAutonomousCommand(self) -> commands2.Command:
        """Use this to pass the autonomous command to the main :class:`.Robot` class.

        :returns: the command to run in autonomous
        """
        return commands2.cmd.none()
