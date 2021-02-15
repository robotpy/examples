from commands2 import RunCommand, RamseteCommand
from commands2.button import JoystickButton, Button

from wpilib import XboxController
from wpilib.controller import RamseteController, PIDController

from wpimath.controller import SimpleMotorFeedforwardMeters

from wpilib.kinematics import ChassisSpeeds

from wpilib.interfaces import GenericHID

from wpimath.trajectory.constraint import DifferentialDriveVoltageConstraint
from wpimath.trajectory import TrajectoryConfig, TrajectoryGenerator, Trajectory

from wpimath.geometry import Pose2d, Rotation2d, Translation2d

from subsystems.drivetrain import Drivetrain

import constants


class RobotContainer:
    def __init__(self):

        # Create the driver's controller.
        self.m_driverController = XboxController(constants.kDriverControllerID)
        
        # Create an instance of the drivetrain subsystem.
        self.m_robotDrive = Drivetrain(self.m_driverController)

        # Configure and set the button bindings for the driver's controller.
        self.configureButtons()

        # Set the default command for the drive subsystem. It's default command will allow
        # the robot to drive with the controller.
                
        self.m_robotDrive.setDefaultCommand(
            RunCommand(self.m_robotDrive.arcadeDrive, self.m_robotDrive)
        )

    # Return the autonomous command, the RAMSETE command.
    def getAutonomousCommand(self):

        # Create a voltage constraint to ensure we don't accelerate too fast.
        
        autoVoltageConstraint = DifferentialDriveVoltageConstraint(
            SimpleMotorFeedforwardMeters(
                constants.ksVolts,
                constants.kvVoltSecondsPerMeter,
                constants.kaVoltSecondsSquaredPerMeter,
            ), 
            constants.kDriveKinematics, 
            10,  # 10 volts max.
        )
        
        """Below will generate the trajectory using a set of programmed configurations"""

        # Create a configuration for the trajctory. This tells the trajectory its constraints
        # as well as its resources, such as the kinematics object.
        config = TrajectoryConfig(
            constants.kMaxSpeedMetersPerSecond,
            constants.kMaxAccelerationMetersPerSecondSquared,
        )
        
        config.setKinematics(
            constants.kDriveKinematics
        )
        
        config.addConstraint(
            autoVoltageConstraint
        )

        # Ensures that the max speed is actually obeyed.
        
        # Apply the previously defined voltage constraint.

        # Start at the origin facing the +x direction.
        initialPosition = Pose2d(0, 0, Rotation2d(0))
        
        # Here are the movements we also want to make during this command.
        # These movements should make an "S" like curve.
        movements = [Translation2d(1, 1), Translation2d(2, -1)]
        
        # End at this position, three meters straight ahead of us, facing forward.
        finalPosition = Pose2d(3, 0, Rotation2d(0))

        # An example trajectory to follow. All of these units are in meters.
        self.exampleTrajectory = TrajectoryGenerator.generateTrajectory(
            initialPosition, movements, finalPosition, config,
        )

        """Below creates the RAMSETE command"""

        ramseteCommand = RamseteCommand(
            self.exampleTrajectory,                     # The trajectory to follow.
            self.m_robotDrive.getPose,                  # A reference to a method that will return our position.
            RamseteController(                          # Our RAMSETE controller.
                constants.kRamseteB,  
                constants.kRamseteZeta
                ),
            SimpleMotorFeedforwardMeters(               # A feedforward object for the robot.
                constants.ksVolts,
                constants.kvVoltSecondsPerMeter,
                constants.kaVoltSecondsSquaredPerMeter,
                ),
            constants.kDriveKinematics,                 # Our drive kinematics.
            self.m_robotDrive.getWheelSpeeds,           # A reference to a method which will return a 
            PIDController(constants.kPDriveVel, 0, 0),  # The turn controller for the left side of the drivetrain.
            PIDController(constants.kPDriveVel, 0, 0),  # The turn controller for the right side of the drivetrain.
            self.m_robotDrive.tankDriveVolts,           # A reference to a method which will set a specified 
                                                        # voltage to each motor. The command will pass the two parameters.
            [self.m_robotDrive],                        # The subsystems the command should require.
        )

        # Reset the robot's position to the starting position of the trajectory.
        self.m_robotDrive.resetOdometry(self.exampleTrajectory.initialPose())

        # Return the command to schedule. The "andThen()" will halt the robot after 
        # the command finishes.
        return ramseteCommand.andThen(self.m_robotDrive.stopMoving)

    def configureButtons(self):
        # We won't do anything with this button itself, so we don't need to
        # define a variable.

        JoystickButton(
            self.m_driverController, 
            XboxController.Button.kBumperRight.value
        ).whenPressed(
            self.m_robotDrive.setSlowMaxOutput
        ).whenReleased(
            self.m_robotDrive.setNormalMaxOutput
        )