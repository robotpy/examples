from commands2 import RunCommand, RamseteCommand
from commands2.button import JoystickButton, Button

from wpilib import XboxController
from wpilib.controller import RamseteController, PIDController

from wpimath.controller import SimpleMotorFeedforwardMeters

from wpimath.kinematics import ChassisSpeeds

from wpilib.interfaces import GenericHID

from wpimath.trajectory.constraint import DifferentialDriveVoltageConstraint
from wpimath.trajectory import TrajectoryConfig, TrajectoryGenerator, Trajectory

from wpimath.geometry import Pose2d, Rotation2d, Translation2d

from subsystems.drivetrain import Drivetrain

import constants


class RobotContainer:

    """
    This class hosts the bulk of the robot's functions. Little robot logic needs to be
    handled here or in the robot periodic methods, as this is a command-based system.
    The structure (commands, subsystems, and button mappings) should be done here.
    """

    def __init__(self):

        # Create the driver's controller.
        self.driverController = XboxController(constants.kDriverControllerPort)

        # Create an instance of the drivetrain subsystem.
        self.robotDrive = Drivetrain()

        # Configure and set the button bindings for the driver's controller.
        self.configureButtons()

        # Set the default command for the drive subsystem. It's default command will allow
        # the robot to drive with the controller.

        self.robotDrive.setDefaultCommand(
            RunCommand(
                lambda: self.robotDrive.arcadeDrive(
                    -self.driverController.getRawAxis(1),
                    self.driverController.getRawAxis(2) * 0.65,
                ),
                self.robotDrive,
            )
        )

    def getAutonomousCommand(self):
        """Returns the command to be ran during the autonomous period."""

        # Create a voltage constraint to ensure we don't accelerate too fast.

        autoVoltageConstraint = DifferentialDriveVoltageConstraint(
            SimpleMotorFeedforwardMeters(
                constants.ksVolts,
                constants.kvVoltSecondsPerMeter,
                constants.kaVoltSecondsSquaredPerMeter,
            ),
            constants.kDriveKinematics,
            maxVoltage=10,  # 10 volts max.
        )

        # Below will generate the trajectory using a set of programmed configurations

        # Create a configuration for the trajctory. This tells the trajectory its constraints
        # as well as its resources, such as the kinematics object.
        config = TrajectoryConfig(
            constants.kMaxSpeedMetersPerSecond,
            constants.kMaxAccelerationMetersPerSecondSquared,
        )

        # Ensures that the max speed is actually obeyed.
        config.setKinematics(constants.kDriveKinematics)

        # Apply the previously defined voltage constraint.
        config.addConstraint(autoVoltageConstraint)

        # Start at the origin facing the +x direction.
        initialPosition = Pose2d(0, 0, Rotation2d(0))

        # Here are the movements we also want to make during this command.
        # These movements should make an "S" like curve.
        movements = [Translation2d(1, 1), Translation2d(2, -1)]

        # End at this position, three meters straight ahead of us, facing forward.
        finalPosition = Pose2d(3, 0, Rotation2d(0))

        # An example trajectory to follow. All of these units are in meters.
        self.exampleTrajectory = TrajectoryGenerator.generateTrajectory(
            initialPosition,
            movements,
            finalPosition,
            config,
        )

        # Below creates the RAMSETE command

        ramseteCommand = RamseteCommand(
            # The trajectory to follow.
            self.exampleTrajectory,
            # A reference to a method that will return our position.
            self.robotDrive.getPose,
            # Our RAMSETE controller.
            RamseteController(constants.kRamseteB, constants.kRamseteZeta),
            # A feedforward object for the robot.
            SimpleMotorFeedforwardMeters(
                constants.ksVolts,
                constants.kvVoltSecondsPerMeter,
                constants.kaVoltSecondsSquaredPerMeter,
            ),
            # Our drive kinematics.
            constants.kDriveKinematics,
            # A reference to a method which will return a DifferentialDriveWheelSpeeds object.
            self.robotDrive.getWheelSpeeds,
            # The turn controller for the left side of the drivetrain.
            PIDController(constants.kPDriveVel, 0, 0),
            # The turn controller for the right side of the drivetrain.
            PIDController(constants.kPDriveVel, 0, 0),
            # A reference to a method which will set a specified
            # voltage to each motor. The command will pass the two parameters.
            self.robotDrive.tankDriveVolts,
            # The subsystems the command should require.
            [self.robotDrive],
        )

        # Reset the robot's position to the starting position of the trajectory.
        self.robotDrive.resetOdometry(self.exampleTrajectory.initialPose())

        # Return the command to schedule. The "andThen()" will halt the robot after
        # the command finishes.
        return ramseteCommand.andThen(lambda: self.robotDrive.tankDriveVolts(0, 0))

    def configureButtons(self):
        """Configure the buttons for the driver's controller"""

        # We won't do anything with this button itself, so we don't need to
        # define a variable.

        (
            JoystickButton(
                self.driverController, XboxController.Button.kBumperRight.value
            )
            .whenPressed(lambda: self.robotDrive.setSlowMaxOutput(0.5))
            .whenReleased(lambda: self.robotDrive.setNormalMaxOutput(1))
        )
