#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#

from wpilib import ADXRS450_Gyro
from subsystems.swervemodule import SwerveModule
from wpimath.kinematics import ChassisSpeeds
from wpimath.kinematics import SwerveDrive3Kinematics, SwerveDrive3Odometry
from wpimath.geometry import Pose2d, Rotation2d
import constants as Constants


class DriveSubsystem:
    def __init__(self):
        """
        Robot swerve modules
        """
        self.m_frontLeft = SwerveModule(
            Constants.DriveConstants.kFrontLeftDriveMotorPort,
            Constants.DriveConstants.kFrontLeftTurningMotorPort,
            Constants.DriveConstants.kFrontLeftDriveEncoderPorts,
            Constants.DriveConstants.kFrontLeftTurningEncoderPorts,
            Constants.DriveConstants.kFrontLeftDriveEncoderReversed,
            Constants.DriveConstants.kFrontLeftTurningEncoderReversed,
        )

        self.m_rearLeft = SwerveModule(
            Constants.DriveConstants.kRearLeftDriveMotorPort,
            Constants.DriveConstants.kRearLeftTurningMotorPort,
            Constants.DriveConstants.kRearLeftDriveEncoderPorts,
            Constants.DriveConstants.kRearLeftTurningEncoderPorts,
            Constants.DriveConstants.kRearLeftDriveEncoderReversed,
            Constants.DriveConstants.kRearLeftTurningEncoderReversed,
        )

        self.m_frontRight = SwerveModule(
            Constants.DriveConstants.kFrontRightDriveMotorPort,
            Constants.DriveConstants.kFrontRightTurningMotorPort,
            Constants.DriveConstants.kFrontRightDriveEncoderPorts,
            Constants.DriveConstants.kFrontRightTurningEncoderPorts,
            Constants.DriveConstants.kFrontRightDriveEncoderReversed,
            Constants.DriveConstants.kFrontRightTurningEncoderReversed,
        )

        self.m_rearRight = SwerveModule(
            Constants.DriveConstants.kRearRightDriveMotorPort,
            Constants.DriveConstants.kRearRightTurningMotorPort,
            Constants.DriveConstants.kRearRightDriveEncoderPorts,
            Constants.DriveConstants.kRearRightTurningEncoderPorts,
            Constants.DriveConstants.kRearRightDriveEncoderReversed,
            Constants.DriveConstants.kRearRightTurningEncoderReversed,
        )

        # The gyro sensor

        self.m_gyro = ADXRS450_Gyro()

        # Odometry class for tracking robot pose

        self.m_odometry = SwerveDrive3Odometry(
            Constants.DriveConstants.kDriveKinematics,
            self.m_gyro.getRotation2d(),
            [
                self.m_frontLeft.getPosition(),
                self.m_frontRight.getPosition(),
                self.m_rearLeft.getPosition(),
                self.m_rearRight.getPosition(),
            ],
        )

    def periodic(self):
        """
        Update the odometry in the periodic block
        """
        self.m_odometry.update(
            self.m_gyro.getRotation2d(),
            [
                self.m_frontLeft.getPosition(),
                self.m_frontRight.getPosition(),
                self.m_rearLeft.getPosition(),
                self.m_rearRight.getPosition(),
            ],
        )

    def getPose(self):
        """
        Returns the currently-estimated pose of the robot.
        """
        return self.m_odometry.getPoseMeters()

    def resetOdometry(self, pose):
        """
        Resets the odometry to the specified pose.
        """
        self.m_odometry.resetPosition(
            self.m_gyro.getRotation2d(),
            [
                self.m_frontLeft.getPosition(),
                self.m_frontRight.getPosition(),
                self.m_rearLeft.getPosition(),
                self.m_rearRight.getPosition(),
            ],
            pose,
        )

    def drive(self, xSpeed, ySpeed, rot, fieldRelative):
        """
        Method to drive the robot using joystick info.
        """
        swerveModuleStates = (
            Constants.DriveConstants.kDriveKinematics.toSwerveModuleStates(
                ChassisSpeeds.discretize(
                    (
                        ChassisSpeeds.fromFieldRelativeSpeeds(
                            xSpeed, ySpeed, rot, self.m_gyro.getRotation2d()
                        )
                        if fieldRelative
                        else ChassisSpeeds(xSpeed, ySpeed, rot)
                    ),
                    Constants.DriveConstants.kDrivePeriod,
                )
            )
        )
        SwerveDrive3Kinematics.desaturateWheelSpeeds(
            swerveModuleStates, Constants.DriveConstants.kMaxSpeedMetersPerSecond
        )
        self.m_frontLeft.setDesiredState(swerveModuleStates[0])
        self.m_frontRight.setDesiredState(swerveModuleStates[1])
        self.m_rearLeft.setDesiredState(swerveModuleStates[2])
        self.m_rearRight.setDesiredState(swerveModuleStates[3])

    def setModuleStates(self, desiredStates):
        """
        Sets the swerve ModuleStates.
        """
        SwerveDrive3Kinematics.desaturateWheelSpeeds(
            desiredStates, Constants.DriveConstants.kMaxSpeedMetersPerSecond
        )
        self.m_frontLeft.setDesiredState(desiredStates[0])
        self.m_frontRight.setDesiredState(desiredStates[1])
        self.m_rearLeft.setDesiredState(desiredStates[2])
        self.m_rearRight.setDesiredState(desiredStates[3])


def resetEncoders(self):
    """
    Resets the drive encoders to currently read a position of 0.
    """
    self.m_frontLeft.resetEncoders()
    self.m_rearLeft.resetEncoders()
    self.m_frontRight.resetEncoders()
    self.m_rearRight.resetEncoders()


def zeroHeading(self):
    """
    Zeroes the heading of the robot.
    """
    self.m_gyro.reset()


def getHeading(self):
    """
    Returns the heading of the robot.
    """
    return self.m_gyro.getRotation2d().getDegrees()


def getTurnRate(self):
    """
    Returns the turn rate of the robot.
    """
    return self.m_gyro.getRate() * (
        -1.0 if Constants.DriveConstants.kGyroReversed else 1.0
    )
