# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.

import commands2
import commands2.cmd
import constants
import wpilib
import wpilib.drive
import typing


class DriveSubsystem(commands2.SubsystemBase):
    def __init__(self) -> None:
        super().__init__()

        # The motors on the left side of the drive.
        self.left = wpilib.MotorControllerGroup(
            wpilib.PWMSparkMax(constants.kLeftMotor1Port),
            wpilib.PWMSparkMax(constants.kLeftMotor2Port),
        )

        # The motors on the right side of the drive.
        self.right = wpilib.MotorControllerGroup(
            wpilib.PWMSparkMax(constants.kRightMotor1Port),
            wpilib.PWMSparkMax(constants.kRightMotor2Port),
        )

        # The robot's drive
        self.drive = wpilib.drive.DifferentialDrive(self.left, self.right)

        # The left-side drive encoder
        self.left_encoder = wpilib.Encoder(
            constants.kLeftEncoderPorts[0],
            constants.kLeftEncoderPorts[1],
            constants.kLeftEncoderReversed,
        )

        # The right-side drive encoder
        self.right_encoder = wpilib.Encoder(
            constants.kRightEncoderPorts[0],
            constants.kRightEncoderPorts[1],
            constants.kRightEncoderReversed,
        )

        # Creates a new drive subsystem
        self.left_encoder.setDistancePerPulse(constants.kEncoderDistancePerPulse)
        self.right_encoder.setDistancePerPulse(constants.kEncoderDistancePerPulse)

        # We need to invert one side of the drivetrain so that positive voltages
        # result in both sides moving forward. Depending on how your robot's
        # gearbox is constructed, you might have to invert the left side instead.
        self.right.setInverted(True)

    def arcadeDriveCommand(
        self, fwd: typing.Callable[[], float], rot: typing.Callable[[], float]
    ) -> commands2.Command:
        """
        A split-stick arcade command, with forward/backward controlled by the left hand, and turning
        controlled by the right.

        Args:
            fwd: Supplier for the commanded forward movement
            rot: Supplier for the commanded rotation
        """
        return commands2.cmd.run(
            lambda: self.drive.arcadeDrive(fwd(), rot(), True), [self]
        )

    def resetEncoders(self) -> None:
        """Resets the drive encoders to currently read a position of 0."""
        self.left.reset()
        self.right.reset()

    def getAverageEncoderDistance(self) -> float:
        """Gets the average distance of the two encoders.

        Returns:
            The average of the two encoder readings.
        """
        return (self.left_encoder.getDistance() + self.right_encoder.getDistance()) / 2

    def getLeftEncoder(self) -> wpilib.Encoder:
        """Gets the left drive encoder.

        Returns:
            The left drive encoder.
        """
        return self.left_encoder

    def getRightEncoder(self) -> wpilib.Encoder:
        """Gets the right drive encoder.

        Returns:
            The right drive encoder.
        """
        return self.right_encoder

    def limitOutputCommand(self, max_output: float) -> commands2.Command:
        """Sets the max output of the drive. Useful for scaling the drive to drive more slowly.

        Args:
            maxoutput: The maximum output to which the drive will be constrained.
        """
        return commands2.cmd.runOnce(
            lambda: self.drive.setMaxOutput(max_output), [self]
        )
