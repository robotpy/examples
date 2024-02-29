#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#

"""
The constants module is a convenience place for teams to hold robot-wide
numerical or boolean constants. Don't use this for any other purpose!
"""

import math

class DriveConstants:
    # The PWM IDs for the drivetrain motor controllers.
    kLeftMotor1Port = 0
    kLeftMotor2Port = 1
    kRightMotor1Port = 2
    kRightMotor2Port = 3

    # Encoders and their respective motor controllers.
    kLeftEncoderPorts = (0, 1)
    kRightEncoderPorts = (2, 3)
    kLeftEncoderReversed = False
    kRightEncoderReversed = True

    # Encoder counts per revolution/rotation.
    kEncoderCPR = 1024
    kWheelDiameterInches = 6

    # Assumes the encoders are directly mounted on the wheel shafts
    kEncoderDistancePerPulse = (kWheelDiameterInches * math.pi) / kEncoderCPR

class ClawConstants:
    kMotorPort = 7
    kContactPort = 5

class WristConstants:
    kMotorPort = 6

    # These pid constants are not real, and will need to be tuned
    kP = 0.1
    kI = 0.0
    kD = 0.0

    kTolerance = 2.5
    kPotentiometerPort = 3;

class ElevatorConstants:
    kMotorPort = 5
    kPotentiometerPort = 2

    # These pid constants are not real, and will need to be tuned
    kP_real = 4
    kI_real = 0.007

    kP_simulation = 18
    kI_simulation = 0.2

    kD = 0.0

    kTolerance = 0.005

class AutoConstants:
    kDistToBox1 = 0.10
    kDistToBox2 = 0.60
    kWristSetpoint = -45.0

class DriveStraightConstants:
    kP = 4.0
    kI = 0.0
    kD = 0.0

class Positions:
    class Pickup:
        kWristSetpoint = -45.0
        kElevatorSetpoint = 0.2

    class Place:
        kWristSetpoint = 0.0
        kElevatorSetpoint = 0.25

    class PrepareToPickup:
        kWristSetpoint = 0.0
        kElevatorSetpoint = 0.0
