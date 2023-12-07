#!/usr/bin/env python3
"""
    This is a sample program demonstrating how to communicate to a light controller from the robot
    code using the roboRIO's I2C port.
"""

import wpilib

import string


class MyRobot(wpilib.TimedRobot):
    PORT = wpilib.I2C.Port.kOnboard
    DEVICE_ADDRESS = 4

    def robotInit(self):
        """Robot initialization function"""

        self.arduino = wpilib.I2C(self.PORT, self.DEVICE_ADDRESS)

    def writeString(self, input: string):
        # Creates a char array from the input string
        chars = bytearray(input, "ascii")

        # Writes bytes over I2C
        self.arduino.writeBulk(chars)

    def robotPeriodic(self):
        # Creates a string to hold current robot state information, including
        # alliance, enabled state, operation mode, and match time. The message
        # is sent in format "AEM###" where A is the alliance color, (R)ed or
        # (B)lue, E is the enabled state, (E)nabled or (D)isabled, M is the
        # operation mode, (A)utonomous or (T)eleop, and ### is the zero-padded
        # time remaining in the match.
        #
        # For example, "RET043" would indicate that the robot is on the red
        # alliance, enabled in teleop mode, with 43 seconds left in the match.
        allianceString = "U"
        alliance = wpilib.DriverStation.getAlliance()
        if alliance:
            allianceString = (
                "R" if alliance == wpilib.DriverStation.Alliance.kRed else "B"
            )

        stateMessage = "".join(
            [
                allianceString,
                "E" if wpilib.DriverStation.isEnabled() else "D",
                "A" if wpilib.DriverStation.isAutonomous() else "T",
                "{:03f}".format(wpilib.DriverStation.getMatchTime()),
            ]
        )

        self.writeString(stateMessage)


if __name__ == "__main__":
    wpilib.run(MyRobot)
