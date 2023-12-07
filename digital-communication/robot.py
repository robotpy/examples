#!/usr/bin/env python3
"""
    This is a sample program demonstrating how to communicate to a light controller from the robot
    code using the roboRIO's DIO ports.
"""

import wpilib


class MyRobot(wpilib.TimedRobot):

    # define ports for digitalcommunication with light controller
    ALLIANCE_PORT = 0
    ENABLED_PORT = 1
    AUTONOMOUS_PORT = 2
    ALERT_PORT = 3

    def robotInit(self):
        """Robot initialization function"""

        self.allianceOutput = wpilib.DigitalOutput(self.ALLIANCE_PORT)
        self.enabledOutput = wpilib.DigitalOutput(self.ENABLED_PORT)
        self.autonomousOutput = wpilib.DigitalOutput(self.AUTONOMOUS_PORT)
        self.alertOutput = wpilib.DigitalOutput(self.ALERT_PORT)

    def robotPeriodic(self):
        setAlliance = False
        alliance = wpilib.DriverStation.getAlliance()
        if alliance:
            setAlliance = alliance == wpilib.DriverStation.Alliance.kRed

        # pull alliance port high if on red alliance, pull low if on blue alliance
        self.allianceOutput.set(setAlliance)

        # pull enabled port high if enabled, low if disabled
        self.enabledOutput.set(wpilib.DriverStation.isEnabled())

        # pull auto port high if in autonomous, low if in teleop (or disabled)
        self.autonomousOutput.set(wpilib.DriverStation.isAutonomous())

        # pull alert port high if match time remaining is between 30 and 25 seconds
        matchTime = wpilib.DriverStation.getMatchTime()
        self.alertOutput.set(30 >= matchTime >= 25)


if __name__ == "__main__":
    wpilib.run(MyRobot)
