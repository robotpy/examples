#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#

from wpilib import TimedRobot
from wpimath.geometry import Translation2d
from wpimath.kinematics import SwerveDrive4Kinematics
from wpimath.trajectory import TrapezoidProfile
import math


class DriveConstants:
    kFrontLeftDriveMotorPort = 0
    kRearLeftDriveMotorPort = 2
    kFrontRightDriveMotorPort = 4
    kRearRightDriveMotorPort = 6

    kFrontLeftTurningMotorPort = 1
    kRearLeftTurningMotorPort = 3
    kFrontRightTurningMotorPort = 5
    kRearRightTurningMotorPort = 7

    kFrontLeftTurningEncoderPorts = [0, 1]
    kRearLeftTurningEncoderPorts = [2, 3]
    kFrontRightTurningEncoderPorts = [4, 5]
    kRearRightTurningEncoderPorts = [6, 7]

    kFrontLeftTurningEncoderReversed = False
    kRearLeftTurningEncoderReversed = True
    kFrontRightTurningEncoderReversed = False
    kRearRightTurningEncoderReversed = True

    kFrontLeftDriveEncoderPorts = [8, 9]
    kRearLeftDriveEncoderPorts = [10, 11]
    kFrontRightDriveEncoderPorts = [12, 13]
    kRearRightDriveEncoderPorts = [14, 15]

    kFrontLeftDriveEncoderReversed = False
    kRearLeftDriveEncoderReversed = True
    kFrontRightDriveEncoderReversed = False
    kRearRightDriveEncoderReversed = True

    kDrivePeriod = TimedRobot.kDefaultPeriod

    kTrackWidth = 0.5
    kWheelBase = 0.7
    kDriveKinematics = SwerveDrive4Kinematics(
        Translation2d(kWheelBase / 2, kTrackWidth / 2),
        Translation2d(kWheelBase / 2, -kTrackWidth / 2),
        Translation2d(-kWheelBase / 2, kTrackWidth / 2),
        Translation2d(-kWheelBase / 2, -kTrackWidth / 2),
    )

    kGyroReversed = False

    ksVolts = 1
    kvVoltSecondsPerMeter = 0.8
    kaVoltSecondsSquaredPerMeter = 0.15

    kMaxSpeedMetersPerSecond = 3


class ModuleConstants:
    kMaxModuleAngularSpeedRadiansPerSecond = 2 * math.pi
    kMaxModuleAngularAccelerationRadiansPerSecondSquared = 2 * math.pi

    kEncoderCPR = 1024
    kWheelDiameterMeters = 0.15
    kDriveEncoderDistancePerPulse = (kWheelDiameterMeters * math.pi) / kEncoderCPR

    kTurningEncoderDistancePerPulse = (2 * math.pi) / kEncoderCPR

    kPModuleTurningController = 1
    kPModuleDriveController = 1


class OIConstants:
    kDriverControllerPort = 0


class AutoConstants:
    kMaxSpeedMetersPerSecond = 3
    kMaxAccelerationMetersPerSecondSquared = 3
    kMaxAngularSpeedRadiansPerSecond = math.pi
    kMaxAngularSpeedRadiansPerSecondSquared = math.pi

    kPXController = 1
    kPYController = 1
    kPThetaController = 1

    kThetaControllerConstraints = TrapezoidProfile.Constraints(
        kMaxAngularSpeedRadiansPerSecond, kMaxAngularSpeedRadiansPerSecondSquared
    )
