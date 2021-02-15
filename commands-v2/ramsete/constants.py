from commands2 import RamseteCommand

from wpilib import AnalogGyro

from wpimath.kinematics import DifferentialDriveKinematics

from math import pi

"""
A place for the constant values in the code
that may be used in more than one place. 
"""


class Constants:
    def __init__(self):

        # Universal gyro.
        self.gyroObject = AnalogGyro(1)

        # ID for the driver's joystick.
        self.driverControllerID = 0

        # The CAN IDs for the drivetrain motor controllers.
        self.frontLeftMotorID = 0
        self.frontRightMotorID = 1

        self.backLeftMotorID = 2
        self.backRightMotorID = 3

        # Encoders and their respective motor controllers.

        self.leftEncoderPorts = (0, 1)
        self.rightEncoderPorts = (2, 3)

        self.leftEncoderReversed = False
        self.rightEncoderReversed = True

        # Encoder counts per rotation.
        self.encoderCPR = 1024

        # In meters, distance between wheels on each side of robot.

        self.trackWidth = 0.69
        self.drivetrainMotorCount = 4
        self.driveKinematics = DifferentialDriveKinematics(self.trackWidth)

        self.wheelDiameterMeters = 0.15

        # The following works assuming the encoders are directly mounted to the wheel shafts.
        self.encoderDistancePerPulse = (self.wheelDiameterMeters * pi) / self.encoderCPR

        # NOTE: Please do NOT use these values on your robot. Rather, characterize your
        # drivetrain using the FRC Characterization tool. These are for demo purposes
        # only!

        self.ksVolts = 0.268
        self.kvVoltSecondsPerMeter = 1.89
        self.kaVoltSecondsSquaredPerMeter = 0.243

        self.kPDriveVel = 0.001  # 8.5

        # Auto constants

        self.maxSpeedMetersPerSecond = 3
        self.maxAccelerationMetersPerSecondSquared = 3

        # Baseline values for a RAMSETE follower in units of meters
        # and seconds.

        self.ramseteB = 2
        self.ramseteZeta = 0.7


constant = Constants()
