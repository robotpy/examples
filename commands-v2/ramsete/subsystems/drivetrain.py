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
        self.m_leftMotors = SpeedControllerGroup(
            PWMSparkMax(constants.kLeftMotor1Port),
            PWMSparkMax(constants.kLeftMotor2Port),
        )

        self.m_rightMotors = SpeedControllerGroup(
            PWMSparkMax(constants.kRightMotor1Port),
            PWMSparkMax(constants.kRightMotor2Port),
        )

        # Create the differential drivetrain object, allowing for easy motor control.
        self.m_drive = DifferentialDrive(self.m_leftMotors, self.m_rightMotors)

        # Create the encoder objects.
        self.m_leftEncoder = Encoder(
            constants.kLeftEncoderPorts[0],
            constants.kLeftEncoderPorts[1],
            constants.kLeftEncoderReversed,
        )

        self.m_rightEncoder = Encoder(
            constants.kRightEncoderPorts[0],
            constants.kRightEncoderPorts[1],
            constants.kRightEncoderReversed,
        )
        
        # Configure the encoder so it knows how many encoder units are in one rotation.
        self.m_leftEncoder.setDistancePerPulse(constants.kEncoderDistancePerPulse)
        self.m_rightEncoder.setDistancePerPulse(constants.kEncoderDistancePerPulse)

        # Create the gyro, a sensor which can indicate the heading of the robot relative
        # to a customizable position.
        self.m_gyro = ADXRS450_Gyro()

        # Create the an object for our odometry, which will utilize sensor data to
        # keep a record of our position on the field.
        self.m_odometry = DifferentialDriveOdometry(self.m_gyro.getRotation2d())

        # Make the controller object universal an attribute to the drivetrain.
        self.m_controller = controller

        # Reset the encoders upon the initilization of the robot.
        self.resetEncoders()

    # Called periodically when it can be called. Updates the robot's
    # odometry with sensor data. 
    def periodic(self):
        self.m_odometry.update(
            self.m_gyro.getRotation2d(),
            self.m_leftEncoder.getDistance(),
            self.m_rightEncoder.getDistance(),
        )

    # Returns the current position of the robot using it's odometry.
    def getPose(self):
        return self.m_odometry.getPose()

    # Return an object which represents the wheel speeds of our drivetrain.
    def getWheelSpeeds(self):
        speeds = DifferentialDriveWheelSpeeds(
            self.m_leftEncoder.getRate(), self.m_rightEncoder.getRate()
        )
        return speeds

    # Resets the robot's odometry to a given position.
    def resetOdometry(self, pose):
        self.resetEncoders()
        self.m_odometry.resetPosition(pose, self.m_gyro.getRotation2d())

    # Drive the robot with standard arcade controls.
    def arcadeDrive(self):
        self.m_drive.arcadeDrive(
            -self.m_controller.getRawAxis(1), # Invert the y-axis's input.
            self.m_controller.getRawAxis(2) * 0.65, # Multiply by 65% for more control.
        )

    # Control the robot's drivetrain with voltage inputs for each side.
    def tankDriveVolts(self, leftVolts, rightVolts):
        self.m_leftMotors.setVoltage(leftVolts) # Set the voltage of the left side.
        self.m_rightMotors.setVoltage(-rightVolts) # Set the voltage of the right side. It's
        # inverted with a negative sign because it's motors need to spin in the negative direction
        # to move forward.
        
        self.m_drive.feed() # Resets the timer for this motor's MotorSafety
        
    # Stops the robot from moving. This is important because we need a reference to not take any arguments.
    def stopMoving(self):
        self.m_leftMotors.setVoltage(0)
        self.m_rightMotors.setVoltage(0)

    # Resets the encoders of the drivetrain.
    def resetEncoders(self):
        self.m_leftEncoder.reset()
        self.m_rightEncoder.reset()

    # Take the sum of each encoder's traversed distance and divide it by two, 
    # since we have two encoder values, to find the average value of the two.
    def getAverageEncoderDistance(self):
        return (self.m_leftEncoder.getDistance() + self.m_rightEncoder.getDistance()) / 2

    # Returns the left encoder object.
    def getLeftEncoder(self):
        return self.m_leftEncoder

    # Returns the right encoder object.
    def getRightEncoder(self):
        return self.m_rightEncoder

    # Set the max percent output of the drivetrain, allowing for slower control.
    def setMaxOutput(self, maxOutput):
        self.m_drive.setMaxOutput(maxOutput)

    # Sets the slow max output. Needed a method that doesn't take any arguments.
    def setSlowMaxOutput(self):
        self.setMaxOutput(0.5)

    # Sets the standard max output. Needed a method that doesn't take any arguments.
    def setNormalMaxOutput(self):
        self.setMaxOutput(1)

    # Zeroes the gyro's heading.
    def zeroHeading(self):
        self.m_gyro.reset()

    def getHeading(self):
        return self.m_gyro.getRotation2d().getDegrees()

    def getTurnRate(self):
        # The minus sign negates the value.
        return -self.m_gyro.getRate()
