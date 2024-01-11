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
import constants


class DriveSubsystem:
    def __init__(self):
        """
        Robot swerve modules
        """
        self.frontLeft = SwerveModule(
            constants.DriveConstants.kFrontLeftDriveMotorPort,
            constants.DriveConstants.kFrontLeftTurningMotorPort,
            constants.DriveConstants.kFrontLeftDriveEncoderPorts,
            constants.DriveConstants.kFrontLeftTurningEncoderPorts,
            constants.DriveConstants.kFrontLeftDriveEncoderReversed,
            constants.DriveConstants.kFrontLeftTurningEncoderReversed,
        )

        self.rearLeft = SwerveModule(
            constants.DriveConstants.kRearLeftDriveMotorPort,
            constants.DriveConstants.kRearLeftTurningMotorPort,
            constants.DriveConstants.kRearLeftDriveEncoderPorts,
            constants.DriveConstants.kRearLeftTurningEncoderPorts,
            constants.DriveConstants.kRearLeftDriveEncoderReversed,
            constants.DriveConstants.kRearLeftTurningEncoderReversed,
        )

        self.frontRight = SwerveModule(
            constants.DriveConstants.kFrontRightDriveMotorPort,
            constants.DriveConstants.kFrontRightTurningMotorPort,
            constants.DriveConstants.kFrontRightDriveEncoderPorts,
            constants.DriveConstants.kFrontRightTurningEncoderPorts,
            constants.DriveConstants.kFrontRightDriveEncoderReversed,
            constants.DriveConstants.kFrontRightTurningEncoderReversed,
        )

        self.rearRight = SwerveModule(
            constants.DriveConstants.kRearRightDriveMotorPort,
            constants.DriveConstants.kRearRightTurningMotorPort,
            constants.DriveConstants.kRearRightDriveEncoderPorts,
            constants.DriveConstants.kRearRightTurningEncoderPorts,
            constants.DriveConstants.kRearRightDriveEncoderReversed,
            constants.DriveConstants.kRearRightTurningEncoderReversed,
        )

        # The gyro sensor

        self.gyro = ADXRS450_Gyro()

        # Odometry class for tracking robot pose

        self.odometry = SwerveDrive3Odometry(
            constants.DriveConstants.kDriveKinematics,
            self.gyro.getRotation2d(),
            [
                self.frontLeft.getPosition(),
                self.frontRight.getPosition(),
                self.rearLeft.getPosition(),
                self.rearRight.getPosition(),
            ],
        )

    def periodic(self):
        """
        Update the odometry in the periodic block
        """
        self.odometry.update(
            self.gyro.getRotation2d(),
            [
                self.frontLeft.getPosition(),
                self.frontRight.getPosition(),
                self.rearLeft.getPosition(),
                self.rearRight.getPosition(),
            ],
        )

    def getPose(self):
        """
        Returns the currently-estimated pose of the robot.
        """
        return self.odometry.getPoseMeters()

    def resetOdometry(self, pose):
        """
        Resets the odometry to the specified pose.
        """
        self.odometry.resetPosition(
            self.gyro.getRotation2d(),
            [
                self.frontLeft.getPosition(),
                self.frontRight.getPosition(),
                self.rearLeft.getPosition(),
                self.rearRight.getPosition(),
            ],
            pose,
        )

    def drive(self, xSpeed, ySpeed, rot, fieldRelative):
        """
        Method to drive the robot using joystick info.
        """
        swerveModuleStates = (
            constants.DriveConstants.kDriveKinematics.toSwerveModuleStates(
                ChassisSpeeds.discretize(
                    (
                        ChassisSpeeds.fromFieldRelativeSpeeds(
                            xSpeed, ySpeed, rot, self.gyro.getRotation2d()
                        )
                        if fieldRelative
                        else ChassisSpeeds(xSpeed, ySpeed, rot)
                    ),
                    constants.DriveConstants.kDrivePeriod,
                )
            )
        )
        SwerveDrive3Kinematics.desaturateWheelSpeeds(
            swerveModuleStates, constants.DriveConstants.kMaxSpeedMetersPerSecond
        )
        self.frontLeft.setDesiredState(swerveModuleStates[0])
        self.frontRight.setDesiredState(swerveModuleStates[1])
        self.rearLeft.setDesiredState(swerveModuleStates[2])
        self.rearRight.setDesiredState(swerveModuleStates[3])

    def setModuleStates(self, desiredStates):
        """
        Sets the swerve ModuleStates.
        """
        SwerveDrive3Kinematics.desaturateWheelSpeeds(
            desiredStates, constants.DriveConstants.kMaxSpeedMetersPerSecond
        )
        self.frontLeft.setDesiredState(desiredStates[0])
        self.frontRight.setDesiredState(desiredStates[1])
        self.rearLeft.setDesiredState(desiredStates[2])
        self.rearRight.setDesiredState(desiredStates[3])


def resetEncoders(self):
    """
    Resets the drive encoders to currently read a position of 0.
    """
    self.frontLeft.resetEncoders()
    self.rearLeft.resetEncoders()
    self.frontRight.resetEncoders()
    self.rearRight.resetEncoders()


def zeroHeading(self):
    """
    Zeroes the heading of the robot.
    """
    self.gyro.reset()


def getHeading(self):
    """
    Returns the heading of the robot.
    """
    return self.gyro.getRotation2d().getDegrees()


def getTurnRate(self):
    """
    Returns the turn rate of the robot.
    """
    return self.gyro.getRate() * (
        -1.0 if constants.DriveConstants.kGyroReversed else 1.0
    )
