#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#

"""
The constants module is a convenience place for teams to hold robot-wide
numerical or boolean constants. Don't use this for any other purpose!
"""

import math

# Drivetrain
kMaxSpeed = 3.0  # 3 meters per second
kMaxAngularSpeed = math.pi  # 1/2 rotation per second

# Swerve Module
kWheelRadius = 0.0508
kEncoderResolution = 4096
kModuleMaxAngularVelocity = kMaxAngularSpeed
kModuleMaxAngularAcceleration = 2 * math.pi
