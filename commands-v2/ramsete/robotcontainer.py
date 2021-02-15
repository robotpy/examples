from commands2 import RunCommand, RamseteCommand
from commands2.button import JoystickButton

from wpilib import XboxController
from wpilib.controller import RamseteController, PIDController

from wpimath.controller import SimpleMotorFeedforwardMeters

from wpilib.kinematics import ChassisSpeeds

from wpilib.interfaces import GenericHID

from wpimath.trajectory.constraint import DifferentialDriveVoltageConstraint
from wpimath.trajectory import TrajectoryConfig, TrajectoryGenerator, Trajectory

from wpimath.geometry import Pose2d, Rotation2d, Translation2d

from subsystems.drivetrain import Drivetrain

from constants import constant


class RobotContainer:
    def __init__(self):

        self.driverController = XboxController(constant.driverControllerID)
        self.driveSubsystem = Drivetrain(self.driverController)

        self.configureButtons()

        doThis = RunCommand(self.driveSubsystem.arcadeDrive, self.driveSubsystem)

        self.driveSubsystem.setDefaultCommand(doThis)

    def getAutonomousCommand(self):
        motorFFOne = SimpleMotorFeedforwardMeters(
            constant.ksVolts,
            constant.kvVoltSecondsPerMeter,
            constant.kaVoltSecondsSquaredPerMeter,
        )

        autoVoltageConstraint = DifferentialDriveVoltageConstraint(
            motorFFOne, constant.driveKinematics, 10  # 10 volts max.
        )

        config = TrajectoryConfig(
            constant.maxSpeedMetersPerSecond,
            constant.maxAccelerationMetersPerSecondSquared,
        )

        config.setKinematics(constant.driveKinematics)
        config.addConstraint(autoVoltageConstraint)

        initial = Pose2d(0, 0, Rotation2d(0))
        movements = [Translation2d(50, 50)]
        final = Pose2d(100, 0, Rotation2d(0))

        self.exampleTrajectory = TrajectoryGenerator.generateTrajectory(
            initial, movements, final, config
        )

        ramseteController = RamseteController(constant.ramseteB, constant.ramseteZeta)
        leftPIDController, rightPIDController = (
            PIDController(constant.kPDriveVel, 0, 0),
            PIDController(constant.kPDriveVel, 0, 0),
        )
        motorFFTwo = SimpleMotorFeedforwardMeters(
            constant.ksVolts,
            constant.kvVoltSecondsPerMeter,
            constant.kaVoltSecondsSquaredPerMeter,
        )

        ramseteCommand = RamseteCommand(
            self.exampleTrajectory,
            self.driveSubsystem.getPose,
            ramseteController,
            motorFFTwo,
            constant.driveKinematics,
            self.driveSubsystem.getWheelSpeeds,
            leftPIDController,
            rightPIDController,
            self.driveSubsystem.tankDriveVolts,
            [self.driveSubsystem],
        )

        initialPosition = self.exampleTrajectory.initialPose()
        self.driveSubsystem.resetOdometry(initialPosition)

        return ramseteCommand.andThen(self.driveSubsystem.stopMoving)

    def configureButtons(self):
        pass
