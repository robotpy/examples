#!/usr/bin/env python3

import wpilib


class MyRobot(wpilib.TimedRobot):
    """
    This is a sample program which uses joystick buttons to control a relay.
    A Relay (generally a spike) has two outputs, each of which can be at either
    0V or 12V and so can be used for actions such as turning a motor off, full
    forwards, or full reverse, and is generally used on the compressor. This
    program uses two buttons on a joystick and each button corresponds to one
    output; pressing the button sets the output to 12V and releasing sets it to 0V.
    """

    def robotInit(self):
        """Robot initialization function"""

        self.relay = wpilib.Relay(0)

        self.joystick = wpilib.Joystick(0)

        self.relayForwardButton = 1
        self.relayReverseButton = 2

    def teleopPeriodic(self):
        # Retrieve the button values. GetRawButton will
        # return true if the button is pressed and false if not.

        forward = self.joystick.getRawButton(self.relayForwardButton)
        reverse = self.joystick.getRawButton(self.relayReverseButton)

        ##
        # Depending on the button values, we want to use one of
        # kOn, kOff, kForward, or kReverse. kOn sets both outputs to 12V,
        # kOff sets both to 0V, kForward sets forward to 12V
        # and reverse to 0V, and kReverse sets reverse to 12V and forward to 0V.
        ##

        if forward and reverse:
            self.relay.set(wpilib.Relay.Value.kOn)
        elif forward:
            self.relay.set(wpilib.Relay.Value.kForward)
        elif reverse:
            self.relay.set(wpilib.Relay.Value.kReverse)
        else:
            self.relay.set(wpilib.Relay.Value.kOff)


if __name__ == "__main__":
    wpilib.run(MyRobot)
