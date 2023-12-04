#!/usr/bin/env python3

import wpilib
from wpilib.shuffleboard import Shuffleboard
from wpilib import SmartDashboard


class MyRobot(wpilib.TimedRobot):
    """
    This is a sample program demonstrating how to read from a ping-response ultrasonic sensor with
    the :class:`.Ultrasonic` class.
    """

    def robotInit(self):
        # Creates a ping-response Ultrasonic object on DIO 1 and 2.
        self.rangeFinder = wpilib.Ultrasonic(1, 2)

        # Add the ultrasonic to the "Sensors" tab of the dashboard
        # Data will update automatically
        Shuffleboard.getTab("Sensors").add(self.rangeFinder)

    def teleopPeriodic(self):
        # We can read the distance in millimeters
        distanceMeters = self.rangeFinder.getRange()

        # We can also publish the data itself periodically
        SmartDashboard.putNumber("Distance[m]", distanceMeters)

    def testInit(self):
        # By default, the Ultrasonic class polls all ultrasonic sensors every in a round-robin to prevent
        # them from interfering from one another.
        # However, manual polling is also possible -- notes that this disables automatic mode!
        self.rangeFinder.ping()

    def testPeriodic(self):
        if self.rangeFinder.isRangeValid():
            # Data is valid, publish it
            SmartDashboard.putNumber("Distance[m]", self.rangeFinder.getRange())

            # Ping for next measurement
            self.rangeFinder.ping()

    def testExit(self):
        # Enable automatic mode
        self.rangeFinder.setAutomaticMode(True)


if __name__ == "__main__":
    wpilib.run(MyRobot)
