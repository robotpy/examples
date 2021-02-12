from commands2 import SubsystemBase

from wpilib import SpeedControllerGroup, PWMVictorSPX, Encoder, ADXRS450_Gyro
from wpilib.drive import DifferentialDrive

from wpimath.kinematics import DifferentialDriveOdometry, DifferentialDriveWheelSpeeds

from constants import *

class Drivetrain(SubsystemBase):
    
    def __init__(self):
        self.leftMotors = SpeedControllerGroup(
            PWMVictorSPX(frontLeftMotorID),
            PWMVictorSPX(backLeftMotorID)
        )
        
        self.rightMotors = SpeedControllerGroup(
            PWMVictorSPX(frontRightMotorID),
            PWMVictorSPX(backRightMotorID)
        )
        
        self.drivetrain = DifferentialDrive(self.leftMotors, self.rightMotors)
        
        self.leftEncoder = Encoder(
            leftEncoderPorts[0],
            leftEncoderPorts[1],
            leftEncoderReversed
                                   )
        
        self.leftEncoder.setDistancePerPulse(encoderDistancePerPulse)
        
        self.rightEncoder = Encoder(
            rightEncoderPorts[0],
            rightEncoderPorts[1],
            rightEncoderReversed
        )
        
        self.rightEncoder.setDistancePerPulse(encoderDistancePerPulse)
        
        self.gyro = ADXRS450_Gyro()
    
        self.odometry = DifferentialDriveOdometry(self.gyro.getRotation2d())
        
        self.resetEncoders()
        
    def periodic(self):
        self.odometry.update(
            self.gyro.getRotation2d(), self.leftEncoder.getDistance(), 
            self.rightEncoder.getDistance()
        )
        
    def getPose(self):
        return self.odometry.getPoseMeters()
    
    def getWheelSpeeds(self):
        return DifferentialDriveWheelSpeeds(self.leftEncoder.getRate(), self.rightEncoder.getRate())
    
    def resetOdometry(self, pose):
        self.resetEncoders()
        self.odometry.resetPosition(pose, self.gyro.getRotation2d())
    
    def arcadeDrive(self, fwd, rot):
        self.drivetrain.arcadeDrive(fwd, rot)
        
    def tankDriveVolts(self, leftVolts, rightVolts):
        self.leftMotors.setVoltage(leftVolts)
        self.rightMotors.setVoltage(-rightVolts)
        self.drivetrain.feed()
    
    def resetEncoders(self):
        self.leftEncoder.reset()
        self.rightEncoder.reset()
    
    def getAverageEncoderDistance(self):
        return (self.leftEncoder.getDistance() + self.rightEncoder.getDistance()) / 2.0
    
    def getLeftEncoder(self):
        return self.leftEncoder
    
    def getRightEncoder(self):
        return self.rightEncoder
    
    def setMaxOutput(self, maxOutput):
        self.drivetrain.setMaxOutput(maxOutput)
    
    def zeroHeading(self):
        self.gyro.reset()
    
    def getHeading(self):
        return self.gyro.getRotation2d().getDegrees()
    
    def getTurnRate(self):
        # The minus sign negates the value. 
        return -self.gyro.getRate()
    