#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#

from wpilib import Encoder, Spark
from wpimath.geometry import Rotation2d
from wpimath.kinematics import SwerveModulePosition, SwerveModuleState
from wpimath.trajectory import TrapezoidProfile
from wpimath.controller import PIDController, ProfiledPIDController
import math
import constants


class SwerveModule:
    """
    Represents a swerve module.
    """

    def __init__(
        self,
        driveMotorChannel,
        turningMotorChannel,
        driveEncoderChannels,
        turningEncoderChannels,
        driveEncoderReversed,
        turningEncoderReversed,
    ):
        self.driveMotor = Spark(driveMotorChannel)
        self.turningMotor = Spark(turningMotorChannel)

        self.driveEncoder = Encoder(*driveEncoderChannels)
        self.turningEncoder = Encoder(*turningEncoderChannels)

        self.drivePIDController = PIDController(
            constants.ModuleConstants.kPModuleDriveController, 0, 0
        )

        self.turningPIDController = ProfiledPIDController(
            constants.ModuleConstants.kPModuleTurningController,
            0,
            0,
            TrapezoidProfile.Constraints(
                constants.ModuleConstants.kMaxModuleAngularSpeedRadiansPerSecond,
                constants.ModuleConstants.kMaxModuleAngularAccelerationRadiansPerSecondSquared,
            ),
        )

        # Set the distance per pulse for the drive encoder.

        self.driveEncoder.setDistancePerPulse(
            constants.ModuleConstants.kDriveEncoderDistancePerPulse
        )
        self.driveEncoder.setReverseDirection(driveEncoderReversed)

        # Set the distance in radians per pulse for the turning encoder.

        self.turningEncoder.setDistancePerPulse(
            constants.ModuleConstants.kTurningEncoderDistancePerPulse
        )
        self.turningEncoder.setReverseDirection(turningEncoderReversed)

        # Limit the PID Controller's input range between -pi and pi and set the input
        # to be continuous.

        self.turningPIDController.enableContinuousInput(-math.pi, math.pi)

    def getState(self):
        """
        Returns the state of the module
        """
        return SwerveModuleState(
            self.driveEncoder.getRate(),
            Rotation2d(self.turningEncoder.getDistance()),
        )

    def getPosition(self):
        """
        Gets the position of the module based on the encoder
        """

        return SwerveModulePosition(
            self.driveEncoder.getDistance(),
            Rotation2d(self.turningEncoder.getDistance()),
        )

    def setDesiredState(self, desiredState):
        """
        Using desiredState, calculate the drive and turn output
        """

        encoderRotation = Rotation2d(self.turningEncoder.getDistance())

        # Optimize the reference state to avoid spinning further than 90 degrees

        state = SwerveModuleState.optimize(desiredState, encoderRotation)

        # Scale speed by cosine of angle error.

        state.speedMetersPerSecond *= state.angle.minus(encoderRotation).getCos()

        # Calculate the drive output from the drive PID controller.

        driveOutput = self.drivePIDController.calculate(
            self.driveEncoder.getRate(), state.speedMetersPerSecond
        )

        # Calculate the turning motor output from the turning PID controller.

        turnOutput = self.turningPIDController.calculate(
            self.turningEncoder.getDistance(), state.angle.getRadians()
        )

        # Set motor outputs

        self.driveMotor.set(driveOutput)
        self.turningMotor.set(turnOutput)

    def resetEncoders(self):
        """
        Resets the drive encoders
        """
        self.driveEncoder.reset()
        self.turningEncoder.reset()
