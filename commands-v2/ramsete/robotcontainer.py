from commands2 import RunCommand, RamseteCommand
from commands2.button import JoystickButton

from wpilib import XboxController
from wpilib.controller import RamseteController, PIDController

from wpimath.controller import SimpleMotorFeedforwardMeters

from wpilib.interfaces import GenericHID

from wpimath.trajectory.constraint import DifferentialDriveVoltageConstraint
from wpimath.trajectory import TrajectoryConfig, TrajectoryGenerator, Trajectory

from wpimath.geometry import Pose2d, Rotation2d, Translation2d

from subsystems.drivetrain import Drivetrain

from constants import *

class RobotContainer:
    
    def __init__(self):
        
        self.driverController = XboxController(driverControllerID)
        self.driveSubsystem = Drivetrain(self.driverController)
        
        doThis = RunCommand(
                self.driveSubsystem.arcadeDrive,
                self.driveSubsystem
            )
        
        self.driveSubsystem.setDefaultCommand(
            doThis    
        )
        
    def getAutonomousCommand(self):
        motorFFOne = SimpleMotorFeedforwardMeters(
                ksVolts,
                kvVoltSecondsPerMeter,
                kaVoltSecondsSquaredPerMeter)
        
        autoVoltageConstraint = DifferentialDriveVoltageConstraint(
            motorFFOne,
            driveKinematics,
            10 # 10 volts max.
        )
        
        config = TrajectoryConfig(
            maxSpeedMetersPerSecond,
            maxAccelerationMetersPerSecondSquared
                                  )
        
        config.setKinematics(driveKinematics)
        config.addConstraint(autoVoltageConstraint)
        
        initial = Pose2d(0, 0, Rotation2d(0))
        movements = [Translation2d(1, 1), Translation2d(2, -1)]
        final = Pose2d(3, 0, Rotation2d(0))
        
        exampleTrajectory = TrajectoryGenerator.generateTrajectory(
            initial,
            movements,
            final,
            config
            )
        
        ramseteController = RamseteController(ramseteB, ramseteZeta)
        leftPIDController, rightPIDController = PIDController(kPDriveVel, 0, 0), PIDController(kPDriveVel, 0, 0)
        motorFFTwo = SimpleMotorFeedforwardMeters(
                                            ksVolts,
                                            kvVoltSecondsPerMeter,
                                            kaVoltSecondsSquaredPerMeter
                                        ),
        requiredSubsystems = [self.driveSubsystem]
                
        ramseteCommand = RamseteCommand(exampleTrajectory,
                                        self.driveSubsystem.getPose,
                                        ramseteController,
                                        motorFFTwo[0], # Returns a tuple fsr.
                                        driveKinematics,
                                        self.driveSubsystem.getWheelSpeeds,
                                        leftPIDController, 
                                        rightPIDController,
                                        self.driveSubsystem.tankDriveVolts,
                                        requiredSubsystems
                                        )
        
        initialPosition = exampleTrajectory.initialPose()
        self.driveSubsystem.resetOdometry(initialPosition)
        
        return ramseteCommand.andThen(self.driveSubsystem.stopMoving)
        
    def configureButtons(self):
        self.slowButton = JoystickButton(self.driverController, 1).whenPressed
        (self.driveSubsystem.setMaxOutput(0.5)).whenReleased
        (self.driveSubsystem.setMaxOutput(1.0))
        
    