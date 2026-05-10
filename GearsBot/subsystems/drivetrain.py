#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#

import wpilib
import wpilib.drive
import wpiutil
import commands2
import constants
import robot

class Drivetrain(commands2.SubsystemBase):
    """The Drivetrain subsystem incorporates the sensors and actuators
    attached to the robots chassis. These include four drive motors, 
    a left and right encoder and a gyro."""

    def __init__(self) -> None:
        """Create a new drivetrain subsystem."""
        super().__init__()

        self.leftLeader = wpilib.PWMSparkMax(constants.DriveConstants.kLeftMotor1Port)
        self.leftFollower = wpilib.PWMSparkMax(constants.DriveConstants.kLeftMotor2Port)
        self.rightLeader = wpilib.PWMSparkMax(constants.DriveConstants.kRightMotor1Port)
        self.rightFollower = wpilib.PWMSparkMax(constants.DriveConstants.kRightMotor2Port)
        
        self.drive = wpilib.drive.DifferentialDrive(
            lambda s : self.leftLeader.set(s), 
            lambda s : self.rightLeader.set(s)
        )

        self.leftEncoder = wpilib.Encoder(
            constants.DriveConstants.kLeftEncoderPorts[0],
            constants.DriveConstants.kLeftEncoderPorts[1],
            constants.DriveConstants.kLeftEncoderReversed
        )

        self.rightEncoder = wpilib.Encoder(
            constants.DriveConstants.kRightEncoderPorts[0],
            constants.DriveConstants.kRightEncoderPorts[1],
            constants.DriveConstants.kRightEncoderReversed
        )

        self.rangefinder = wpilib.AnalogInput(constants.DriveConstants.kRangeFinderPort)
        self.gyro = wpilib.AnalogGyro(constants.DriveConstants.kAnalogGyroPort)
        
        wpiutil.SendableRegistry.addChild(self.drive, self.leftLeader)
        wpiutil.SendableRegistry.addChild(self.drive, self.rightLeader)

        self.leftLeader.addFollower(self.leftFollower)
        self.rightLeader.addFollower(self.rightFollower)
        
        # We need to invert one side of the drivetrain so that positive voltages
        # result in both sides moving forward. Depending on how your robot's
        # gearbox is constructed, you might have to invert the left side instead.
        self.rightLeader.setInverted(true)
        
        # Encoders may measure differently in the real world and in
        # simulation. In this example the robot moves 0.042 barleycorns
        # per tick in the real world, but the simulated encoders
        # simulate 360 tick encoders. This if statement allows for the
        # real robot to handle this difference in devices.
        if robot.MyRobot.isReal():
            self.leftEncoder.setDistancePerPulse(DriveConstants.kEncoderDistancePerPulse)
            self.rightEncoder.setDistancePerPulse(DriveConstants.kEncoderDistancePerPulse)
        else:
            # Circumference = diameter in feet * pi. 360 tick simulated encoders.
            self.leftEncoder.setDistancePerPulse((4.0 / 12.0 * math.pi) / 360.0)
            self.rightEncoder.setDistancePerPulse((4.0 / 12.0 * Math.PI) / 360.0)

        # Let's name the sensors on the LiveWindow
        self.addChild("Drive", self.drive);
        self.addChild("Left Encoder", self.leftEncoder);
        self.addChild("Right Encoder", self.rightEncoder);
        self.addChild("Rangefinder", self.rangefinder);
        self.addChild("Gyro", self.gyro);

    def log(self) -> None:
        """The log method puts interesting information to the SmartDashboard."""
        wpilib.SmartDashboard.putNumber("Left Distance", self.leftEncoder.getDistance())
        wpilib.SmartDashboard.putNumber("Right Distance", self.rightEncoder.getDistance())
        wpilib.SmartDashboard.putNumber("Left Speed", self.leftEncoder.getRate())
        wpilib.SmartDashboard.putNumber("Right Speed", self.rightEncoder.getRate())
        wpilib.SmartDashboard.putNumber("Gyro", self.gyro.getAngle())

    def drive(self, left: float, right: float) -> None:
        """Tank style driving for the Drivetrain.

        :param left:  Speed in range [-1,1]
        :param right: Speed in range [-1,1]
        """
        self.drive.tankDrive(left, right)

    def getHeading(self) -> float:
        """Get the robot's heading.

        :returns: The robots heading in degrees.
        """
        return self.gyro.getAngle()
    
    def reset(self) -> None:
        """Reset the robots sensors to the zero states."""
        self.gyro.reset()
        self.leftEncoder.reset()
        self.rightEncoder.reset()

    def getDistance(self) -> float:
        """Get the average distance of the encoders since the last reset.

        :returns: The distance driven (average of left and
        right encoders).
        """
        return (self.leftEncoder.getDistance() + self.rightEncoder.getDistance()) / 2
    
    def getDistanceToObstacle(self) -> float:
        """Get the distance to the obstacle.

        :returns: The distance to the obstacle detected by the rangefinder.
        """
        # Really meters in simulation since it's a rangefinder...
        return self.rangefinder.getAverageVoltage()
    
    def periodic(self) -> None:
        """Call log method every loop."""
        self.log()
