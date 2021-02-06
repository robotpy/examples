import commands2
import wpilib
import wpilib.drive

import constants


class DriveSubsystem(commands2.SubsystemBase):
    def __init__(self) -> None:
        super().__init__()

        self.left1 = wpilib.PWMVictorSPX(constants.kLeftMotor1Port)
        self.left2 = wpilib.PWMVictorSPX(constants.kLeftMotor2Port)
        self.right1 = wpilib.PWMVictorSPX(constants.kRightMotor1Port)
        self.right2 = wpilib.PWMVictorSPX(constants.kRightMotor2Port)

        # The robot's drive
        self.drive = wpilib.drive.DifferentialDrive(
            wpilib.SpeedControllerGroup(self.left1, self.left2),
            wpilib.SpeedControllerGroup(self.right1, self.right2),
        )

        # The left-side drive encoder
        self.leftEncoder = wpilib.Encoder(
            *constants.kLeftEncoderPorts,
            reverseDirection=constants.kLeftEncoderReversed
        )

        # The right-side drive encoder
        self.rightEncoder = wpilib.Encoder(
            *constants.kRightEncoderPorts,
            reverseDirection=constants.kRightEncoderReversed
        )

        # Sets the distance per pulse for the encoders
        self.leftEncoder.setDistancePerPulse(constants.kEncoderDistancePerPulse)
        self.rightEncoder.setDistancePerPulse(constants.kEncoderDistancePerPulse)

    def arcadeDrive(self, fwd: float, rot: float) -> None:
        """
        Drives the robot using arcade controls.

        :param fwd: the commanded forward movement
        :param rot: the commanded rotation
        """
        self.drive.arcadeDrive(fwd, rot)

    def resetEncoders(self) -> None:
        """Resets the drive encoders to currently read a position of 0."""

    def getAverageEncoderDistance(self) -> float:
        """Gets the average distance of the TWO encoders."""
        return (self.leftEncoder.getDistance() + self.rightEncoder.getDistance()) / 2.0

    def setMaxOutput(self, maxOutput: float):
        """
        Sets the max output of the drive. Useful for scaling the
        drive to drive more slowly.
        """
        self.drive.setMaxOutput(maxOutput)
