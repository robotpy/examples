from commands2 import RamseteCommand

from wpimath.kinematics import DifferentialDriveKinematics

from math import pi

"""
A place for the constant values in the code
that may be used in more than one place. 
"""

# ID for the driver's joystick. 
driverControllerID = 0

# The CAN IDs for the drivetrain motor controllers. 
frontLeftMotorID = 0
frontRightMotorID = 1

backLeftMotorID = 2
backRightMotorID = 3

# Encoders and their respective motor controllers.

leftEncoderPorts = (0, 1)
rightEncoderPorts = (2, 3)

leftEncoderReversed = False
rightEncoderReversed = True

# Encoder counts per rotation.
encoderCPR = 1024

# In meters, distance between wheels on each side of robot. 

trackWidth = 0.69
drivetrainMotorCount = 4
driveKinematics = DifferentialDriveKinematics(trackWidth)

wheelDiameterMeters = 0.15

# The following works assuming the encoders are directly mounted to the wheel shafts.
encoderDistancePerPulse = (wheelDiameterMeters * pi) / encoderCPR

# NOTE: Please do NOT use these values on your robot. Rather, characterize your 
# drivetrain using the FRC Characterization tool. These are for demo purposes
# only!

ksVolts = 0.22
kvVoltSecondsPerMeter = 1.98
kaVoltSecondsSquaredPerMeter = 0.2

kPDriveVel = 8.5

# Auto constants

maxSpeedMetersPerSecond = 3
maxAccelerationMetersPerSecondSquared = 3

# Baseline values for a RAMSETE follower in units of meters
# and seconds. 

ramseteB = 2
ramseteZeta = 0.7