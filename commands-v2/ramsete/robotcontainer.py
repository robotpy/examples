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
        
        self.configureButtons()
        
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
        movements = [Translation2d(50, 0)]
        final = Pose2d(100, 0, Rotation2d(0))
                
        self.exampleTrajectory = TrajectoryGenerator.generateTrajectory(
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
                                        )
        requiredSubsystems = [self.driveSubsystem]
        
        #print('start at ' + str(self.driveSubsystem.getPose()))
        
        ramseteCommand = RamseteCommand(self.exampleTrajectory,
                                        self.driveSubsystem.getPose,
                                        ramseteController,
                                        motorFFTwo,
                                        driveKinematics,
                                        self.driveSubsystem.getWheelSpeeds,
                                        leftPIDController, 
                                        rightPIDController,
                                        self.driveSubsystem.tankDriveVolts,
                                        requiredSubsystems
                                        )
        
        initialPosition = self.exampleTrajectory.initialPose()
        self.driveSubsystem.resetOdometry(initialPosition)
        
        return ramseteCommand.andThen(self.driveSubsystem.stopMoving)
        
    def configureButtons(self):
        pass
    