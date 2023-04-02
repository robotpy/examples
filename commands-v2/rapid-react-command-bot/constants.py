#!/usr/bin/env python3
#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#

import wpimath.units
import math

"""The Constants class provides a convenient place for teams to hold robot-wide numerical or boolean
constants. This class should not be used for any other purpose. All constants should be declared
globally (i.e. public static). Do not put anything functional in this class.

It is advised to statically import this class (or one of its inner classes) wherever the
constants are needed, to reduce verbosity.
"""

class DriveConstants:
    kLeftMotor1Port = 0
    kLeftMotor2Port = 1
    kRightMotor1Port = 2
    kRightMotor2Port = 3

    kLeftEncoderPorts = (0, 1)
    kRightEncoderPorts = (2, 3)
    kLeftEncoderReversed = False
    kRightEncoderReversed = True

    kEncoderCPR = 1024
    kWheelDiameterMeters = wpimath.units.inchesToMeters(6)
    # Assumes the encoders are directly mounted on the wheel shafts
    kEncoderDistancePerPulse = (kWheelDiameterMeters * math.pi) / kEncoderCPR

class ShooterConstants:
    kEncoderPorts = (4, 5)
    kEncoderReversed = False
    kEncoderCPR = 1024
    # Distance units will be rotations
    kEncoderDistancePerPulse =  1 / kEncoderCPR

    kShooterMotorPort = 4
    kFeederMotorPort = 5

    kShooterFreeRPS = 5300
    kShooterTargetRPS = 4000
    kShooterToleranceRPS = 50

    # These are not real PID gains, and will have to be tuned for your specific robot.
    kP = 1

    # On a real robot the feedforward constants should be empirically determined; these are
    # reasonable guesses.
    kSVolts = 0.05
    #Should have value 12V at free speed...
    kVVoltSecondsPerRotation = 12.0 / kShooterFreeRPS

    kFeederSpeed = 0.5

class IntakeConstants:
    kMotorPort = 6
    kSolenoidPorts = (0, 1)

class StorageConstants:
    kMotorPort = 7
    kBallSensorPort = 6

class AutoConstants:
    kTimeoutSeconds = 3
    kDriveDistanceMeters = 2
    kDriveSpeed = 0.5

class OIConstants:
    kDriverControllerPort = 0