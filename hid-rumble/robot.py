#!/usr/bin/env python3
"""
    This is a demo program showing the use of GenericHID's rumble feature.
"""

import wpilib


class MyRobot(wpilib.TimedRobot):
    def robotInit(self):
        """Robot initialization function"""

        self.hid = wpilib.XboxController(0)

    def autonomousInit(self):
        # Turn on rumble at the start of auto
        self.hid.setRumble(wpilib.XboxController.RumbleType.kLeftRumble, 1.0)
        self.hid.setRumble(wpilib.XboxController.RumbleType.kRightRumble, 1.0)

    def disabledInit(self):
        # Stop the rumble when entering disabled
        self.hid.setRumble(wpilib.XboxController.RumbleType.kLeftRumble, 0.0)
        self.hid.setRumble(wpilib.XboxController.RumbleType.kRightRumble, 0.0)


if __name__ == "__main__":
    wpilib.run(MyRobot)
