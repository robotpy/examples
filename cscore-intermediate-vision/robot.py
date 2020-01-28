#!/usr/bin/env python3
"""
    This is a good foundation to build your robot code on
"""

import wpilib


class MyRobot(wpilib.TimedRobot):
    def robotInit(self):
        wpilib.CameraServer.launch("vision.py:main")


if __name__ == "__main__":
    wpilib.run(MyRobot)
