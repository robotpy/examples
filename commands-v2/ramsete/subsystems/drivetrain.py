from commands2 import SubsystemBase

from wpilib import SpeedControllerGroup, PWMVictorSPX, Encoder, ADXRS450_Gyro, XboxController
from wpilib.drive import DifferentialDrive
from wpilib.interfaces import GenericHID

from wpimath.kinematics import DifferentialDriveOdometry, DifferentialDriveWheelSpeeds

from constants import *

class Drivetrain(SubsystemBase):
    
    def __init__(self, controller: XboxController):
        
        super().__init__()
        
        frontLeftMotor, backLeftMotor = PWMVictorSPX(frontLeftMotorID), PWMVictorSPX(backLeftMotorID)
        frontRightMotor, backRightMotor = PWMVictorSPX(frontRightMotorID), PWMVictorSPX(backRightMotorID)
        
        self.leftMotors = SpeedControllerGroup(
            frontLeftMotor,
            backLeftMotor
        )
        
        self.rightMotors = SpeedControllerGroup(
            frontRightMotor,
            backRightMotor
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
        
        self.controller = controller
        
        self.resetEncoders()
        
    def periodic(self):
        self.odometry.update(
            self.gyro.getRotation2d(), self.leftEncoder.getDistance(), 
            self.rightEncoder.getDistance()
        )
        
    def getPose(self):
        return self.odometry.getPose()
    
    def getWheelSpeeds(self):
        speeds = DifferentialDriveWheelSpeeds(self.leftEncoder.getRate(), self.rightEncoder.getRate())
        return speeds
    
    def resetOdometry(self, pose):
        self.resetEncoders()
        self.odometry.resetPosition(pose, self.gyro.getRotation2d())
    
    def arcadeDrive(self):
        self.drivetrain.arcadeDrive(
            self.controller.getY(GenericHID.Hand.kLeftHand), 
            self.controller.getX(GenericHID.Hand.kRightHand)
        )
        
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
    
    def stopMoving(self):
        self.tankDriveVolts(0, 0)
    
    def zeroHeading(self):
        self.gyro.reset()
    
    def getHeading(self):
        return self.gyro.getRotation2d().getDegrees()
    
    def getTurnRate(self):
        # The minus sign negates the value. 
        return -self.gyro.getRate()
    