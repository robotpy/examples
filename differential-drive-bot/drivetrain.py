#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#

import wpilib.drive
import wpimath.controller
import wpimath.kinematics
import wpimath.units

import math


class Drivetrain:
    """Represents a differential drive style drivetrain."""

    MAX_SPEED = 3.0  # meters per second
    MAX_ANGULAR_SPEED = 2 * math.pi  # one rotation per second

    TRACK_WIDTH = 0.381 * 2  # meters
    WHEEL_RADIUS = 0.0508  # meters
    ENCODER_RESOLUTION = 4096  # counts per revolution

    def __init__(self):
        leftLeader = wpilib.PWMSparkMax(1)
        leftFollower = wpilib.PWMSparkMax(2)
        rightLeader = wpilib.PWMSparkMax(3)
        rightFollower = wpilib.PWMSparkMax(4)

        self.leftEncoder = wpilib.Encoder(0, 1)
        self.rightEncoder = wpilib.Encoder(2, 3)

        self.leftGroup = wpilib.MotorControllerGroup(leftLeader, leftFollower)
        self.rightGroup = wpilib.MotorControllerGroup(rightLeader, rightFollower)

        self.gyro = wpilib.AnalogGyro(0)

        self.leftPIDController = wpimath.controller.PIDController(1.0, 0.0, 0.0)
        self.rightPIDController = wpimath.controller.PIDController(1.0, 0.0, 0.0)

        self.kinematics = wpimath.kinematics.DifferentialDriveKinematics(
            self.TRACK_WIDTH
        )

        # Gains are for example purposes only - must be determined for your own robot!
        self.feedforward = wpimath.controller.SimpleMotorFeedforwardMeters(1, 3)

        self.gyro.reset()

        # We need to invert one side of the drivetrain so that positive voltages
        # result in both sides moving forward. Depending on how your robot's
        # gearbox is constructed, you might have to invert the left side instead.
        self.rightGroup.setInverted(True)

        # Set the distance per pulse for the drive encoders. We can simply use the
        # distance traveled for one rotation of the wheel divided by the encoder
        # resolution.
        self.leftEncoder.setDistancePerPulse(
            2 * math.pi * self.WHEEL_RADIUS / self.ENCODER_RESOLUTION
        )
        self.rightEncoder.setDistancePerPulse(
            2 * math.pi * self.WHEEL_RADIUS / self.ENCODER_RESOLUTION
        )

        self.leftEncoder.reset()
        self.rightEncoder.reset()

        self.odometry = wpimath.kinematics.DifferentialDriveOdometry(
            self.gyro.getRotation2d(),
            self.leftEncoder.getDistance(),
            self.rightEncoder.getDistance(),
        )

    def setSpeeds(self, speeds: wpimath.kinematics.DifferentialDriveWheelSpeeds):
        """Sets the desired wheel speeds."""
        leftFeedforward = self.feedforward.calculate(speeds.left)
        rightFeedforward = self.feedforward.calculate(speeds.right)

        leftOutput = self.leftPIDController.calculate(
            self.leftEncoder.getRate(), speeds.left
        )
        rightOutput = self.rightPIDController.calculate(
            self.rightEncoder.getRate(), speeds.right
        )

        self.leftGroup.setVoltage(leftOutput + leftFeedforward)
        self.rightGroup.setVoltage(rightOutput + rightFeedforward)

    def drive(self, xSpeed, rot):
        """Drives the robot with the given linear velocity and angular velocity."""
        wheelSpeeds = self.kinematics.toWheelSpeeds(
            wpimath.kinematics.ChassisSpeeds(xSpeed, 0, rot)
        )
        self.setSpeeds(wheelSpeeds)

    def updateOdometry(self):
        """Updates the field-relative position."""
        self.odometry.update(
            self.gyro.getRotation2d(),
            self.leftEncoder.getDistance(),
            self.rightEncoder.getDistance(),
        )
