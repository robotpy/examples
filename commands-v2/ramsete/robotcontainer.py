from commands2 import RunCommand, RamseteCommand
from commands2.button import JoystickButton

from wpilib import XboxController

from wpimath.controller import SimpleMotorFeedforward, RamseteController, PIDController

from wpilib.interfaces import GenericHID

from wpimath.trajectory.constraint import DifferentialDriveVoltageConstraint
from wpimath.trajectory import TrajectoryConfig, TrajectoryGenerator

from wpimath.geometry import Pose2d, Rotation2d, Translation2d

from subsystems.drivetrain import Drivetrain

from constants import *

class RobotContainer:
    
    def __init__(self):
        
        self.driveSubsystem = Drivetrain()
        
        self.driverController = XboxController(driverControllerID)
        
        self.driveSubsystem.setDefaultCommand(
            RunCommand(
                self.driveSubsystem.arcadeDrive(
                    self.driverController.getY(GenericHID.Hand.kLeft),
                    self.driverController.getX(GenericHID.Hand.kRight)
                ),
                self.driveSubsystem
            )
        )
        
    def getAutonomousCommand(self):
        autoVoltageConstraint = DifferentialDriveVoltageConstraint(
            SimpleMotorFeedforward(
                ksVolts,
                kvVoltSecondsPerMeter,
                kaVoltSecondsSquaredPerMeter),
            driveKinematics,
            10
        )
        
        config = TrajectoryConfig(
            maxSpeedMetersPerSecond,
            maxAccelerationMetersPerSecondSquared
                                  )
        
        self.config.setKinematics(driveKinematics)
        self.config.addConstraint(autoVoltageConstraint)
        
        exampleTrajectory = TrajectoryGenerator.generateTrajectory(
            Pose2d(0, 0, Rotation2d),
            [Translation2d(1, 1), Translation2d(2, -1)],
            Pose2d(3, 0, Rotation2d),
            config
            )
        
        ramseteCommand = RamseteCommand(exampleTrajectory,
                                        self.driveSubsystem.getPose,
                                        RamseteController(ramseteB, ramseteZeta),
                                        SimpleMotorFeedforward(
                                            ksVolts,
                                            kvVoltSecondsPerMeter,
                                            kaVoltSecondsSquaredPerMeter
                                        ),
                                        driveKinematics,
                                        self.driveSubsystem.getWheelSpeeds,
                                        PIDController(kPDriveVel, 0, 0),
                                        PIDController(kPDriveVel, 0, 0),
                                        self.driveSubsystem.tankDriveVolts,
                                        self.driveSubsystem
                                        )
        
        self.driveSubsystem.resetOdometry(exampleTrajectory.getInitialPose())
        
        return ramseteCommand.andThen(self.driveSubsystem.tankDriveVolts(0, 0))
        
    def configureButtons(self):
        self.slowButton = JoystickButton(self.driverController, 1).whenPressed
        (self.driveSubsystem.setMaxOutput(0.5)).whenReleased
        (self.driveSubsystem.setMaxOutput(1.0))
        
    