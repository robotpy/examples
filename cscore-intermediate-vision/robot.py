#!/usr/bin/env python3
#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#

import wpilib


class MyRobot(wpilib.TimedRobot):
    """
    This is a good foundation to build your robot code on
    """

    def robotInit(self):
        wpilib.CameraServer.launch("vision.py:main")


if __name__ == "__main__":
    wpilib.run(MyRobot)
