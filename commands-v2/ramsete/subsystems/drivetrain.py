from commands2 import SubsystemBase

from wpilib import SpeedControllerGroup, PWMSparkMax, Encoder, ADXRS450_Gyro
from wpilib.drive import DifferentialDrive
from wpilib.interfaces import GenericHID

from wpimath.geometry import Pose2d, Rotation2d
from wpimath.kinematics import DifferentialDriveOdometry, DifferentialDriveWheelSpeeds

import constants


class Drivetrain(SubsystemBase):
    def __init__(self, controller: GenericHID):

        super().__init__()

        # Create the motor controllers and their respective speed controllers.
        self.leftMotors = SpeedControllerGroup(
            PWMSparkMax(constants.kLeftMotor1Port),
            PWMSparkMax(constants.kLeftMotor2Port),
        )

        self.rightMotors = SpeedControllerGroup(
            PWMSparkMax(constants.kRightMotor1Port),
            PWMSparkMax(constants.kRightMotor2Port),
        )

        # Create the differential drivetrain object, allowing for easy motor control.
        self.drive = DifferentialDrive(self.leftMotors, self.rightMotors)

        # Create the encoder objects.
        self.leftEncoder = Encoder(
            constants.kLeftEncoderPorts[0],
            constants.kLeftEncoderPorts[1],
            constants.kLeftEncoderReversed,
        )

        self.rightEncoder = Encoder(
            constants.kRightEncoderPorts[0],
            constants.kRightEncoderPorts[1],
            constants.kRightEncoderReversed,
        )

        # Configure the encoder so it knows how many encoder units are in one rotation.
        self.leftEncoder.setDistancePerPulse(constants.kEncoderDistancePerPulse)
        self.rightEncoder.setDistancePerPulse(constants.kEncoderDistancePerPulse)

        # Create the gyro, a sensor which can indicate the heading of the robot relative
        # to a customizable position.
        self.gyro = ADXRS450_Gyro()

        # Create the an object for our odometry, which will utilize sensor data to
        # keep a record of our position on the field.
        self.odometry = DifferentialDriveOdometry(self.gyro.getRotation2d())

        # Make the controller object universal an attribute to the drivetrain.
        self.controller = controller

        # Reset the encoders upon the initilization of the robot.
        self.resetEncoders()

    def periodic(self):
        """
        Called periodically when it can be called. Updates the robot's
        odometry with sensor data.
        """
        self.odometry.update(
            self.gyro.getRotation2d(),
            self.leftEncoder.getDistance(),
            self.rightEncoder.getDistance(),
        )

    def getPose(self):
        """Returns the current position of the robot using it's odometry."""
        return self.odometry.getPose()

    def getWheelSpeeds(self):
        """Return an object which represents the wheel speeds of our drivetrain."""
        speeds = DifferentialDriveWheelSpeeds(
            self.leftEncoder.getRate(), self.rightEncoder.getRate()
        )
        return speeds

    def resetOdometry(self, pose):
        """ Resets the robot's odometry to a given position."""
        self.resetEncoders()
        self.odometry.resetPosition(pose, self.gyro.getRotation2d())

    def arcadeDrive(self):
        """Drive the robot with standard arcade controls."""
        self.drive.arcadeDrive(
            -self.controller.getRawAxis(1),  # Invert the y-axis's input.
            self.controller.getRawAxis(2) * 0.65,  # Multiply by 65% for more control.
        )

    def tankDriveVolts(self, leftVolts, rightVolts):
        """Control the robot's drivetrain with voltage inputs for each side."""
        self.leftMotors.setVoltage(leftVolts)  # Set the voltage of the left side.
        self.rightMotors.setVoltage(
            -rightVolts
        )  # Set the voltage of the right side. It's
        # inverted with a negative sign because it's motors need to spin in the negative direction
        # to move forward.

        self.drive.feed()  # Resets the timer for this motor's MotorSafety

    def stopMoving(self):
        """Stops the robot from moving. This is important because we need a reference to not take any arguments."""
        self.leftMotors.setVoltage(0)
        self.rightMotors.setVoltage(0)

    def resetEncoders(self):
        """Resets the encoders of the drivetrain."""
        self.leftEncoder.reset()
        self.rightEncoder.reset()

    def getAverageEncoderDistance(self):
        """
        Take the sum of each encoder's traversed distance and divide it by two,
        since we have two encoder values, to find the average value of the two.
        """
        return (self.leftEncoder.getDistance() + self.rightEncoder.getDistance()) / 2

    def getLeftEncoder(self):
        """Returns the left encoder object."""
        return self.leftEncoder

    def getRightEncoder(self):
        """Returns the right encoder object."""
        return self.rightEncoder

    def setMaxOutput(self, maxOutput):
        """Set the max percent output of the drivetrain, allowing for slower control."""
        self.drive.setMaxOutput(maxOutput)

    def setSlowMaxOutput(self):
        """Sets the slow max output. Needed a method that doesn't take any arguments."""
        self.setMaxOutput(0.5)

    def setNormalMaxOutput(self):
        """Sets the standard max output. Needed a method that doesn't take any arguments."""
        self.setMaxOutput(1)

    def zeroHeading(self):
        """Zeroes the gyro's heading."""
        self.gyro.reset()

    def getHeading(self):
        """Return the current heading of the robot."""
        return self.gyro.getRotation2d().getDegrees()

    def getTurnRate(self):
        """Returns the turning rate of the robot using the gyro."""

        # The minus sign negates the value.
        return -self.gyro.getRate()
