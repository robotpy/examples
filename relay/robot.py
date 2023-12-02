#!/usr/bin/env python3

import wpilib


class MyRobot(wpilib.TimedRobot):
    """This is a sample program which uses joystick buttons to control a relay.
    A Relay (generally a spike) has two outputs, each of which can be at either
    0V or 12V and so can be used for actions such as turning a motor off, full
    forwards, or full reverse, and is generally used on the compressor. This
    program uses two buttons on a joystick and each button corresponds to one
    output; pressing the button sets the output to 12V and releasing sets it to 0V.
    """

    def robotInit(self):
        """Robot initialization function"""
        # create Relay object
        self.relay = wpilib.Relay(0)

        # create joystick object
        self.joystickChannel = 0  # usb number in DriverStation
        self.joystick = wpilib.Joystick(self.joystickChannel)

        # create variables to define the buttons
        self.relayForwardButton = 1
        self.relayReverseButton = 2

    def teleopPeriodic(self):
        """
        The relay can be set several ways. It has two outputs which each can be set for either 0V or 12V.
        This code uses buttons on a joystick to set each of the outputs.
        """

        forward = self.joystick.getRawButton(self.relayForwardButton)
        reverse = self.joystick.getRawButton(self.relayReverseButton)

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
