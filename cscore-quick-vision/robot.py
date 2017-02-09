#!/usr/bin/env python3
"""
    This is a good foundation to build your robot code on
"""

import wpilib


class MyRobot(wpilib.IterativeRobot):
    
    def robotInit(self):
        wpilib.CameraServer.launch()


if __name__ == '__main__':
    wpilib.run(MyRobot)
