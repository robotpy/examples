# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.

import enum
import typing

import commands2
import wpilib


class ChannelMode(enum.Enum):
    INPUT = 1
    OUTPUT = 2


class OnBoardIO(commands2.SubsystemBase):
    """This class represents the onboard IO of the Romi reference robot. This includes the pushbuttons
    and LEDs.

    DIO 0 - Button A (input only) DIO 1 - Button B (input) or Green LED (output) DIO 2 - Button C
    (input) or Red LED (output) DIO 3 - Yellow LED (output only)

    """

    MESSAGE_INTERVAL = 1.0

    def __init__(self, dio1: ChannelMode, dio2: ChannelMode) -> None:
        """Constructor.

        :param dio1: Mode for DIO 1 (input = Button B, output = green LED)
        :param dio2: Mode for DIO 2 (input = Button C, output = red LED)
        """
        super().__init__()

        self.nextMessageTime = 0

        self.buttonA = wpilib.DigitalInput(0)
        self.buttonB: typing.Optional[wpilib.DigitalInput] = None
        self.buttonC: typing.Optional[wpilib.DigitalInput] = None

        self.yellowLed = wpilib.DigitalOutput(3)
        self.greenLed: typing.Optional[wpilib.DigitalOutput] = None
        self.redLed: typing.Optional[wpilib.DigitalOutput] = None

        if dio1 == ChannelMode.INPUT:
            self.buttonB = wpilib.DigitalInput(1)
        else:
            self.greenLed = wpilib.DigitalOutput(1)

        if dio2 == ChannelMode.INPUT:
            self.buttonC = wpilib.DigitalInput(2)
        else:
            self.redLed = wpilib.DigitalOutput(2)

    def getButtonAPressed(self) -> bool:
        """Gets if the A button is pressed."""
        return self.buttonA.get()

    def getButtonBPressed(self) -> bool:
        """Gets if the B Bbutton is pressed."""
        if self.buttonB:
            return self.buttonB.get()

        now = wpilib.Timer.getFPGATimestamp()
        if now > self.nextMessageTime:
            wpilib.DriverStation.reportError("Button B was not configured", True)
            self.nextMessageTime = now + self.MESSAGE_INTERVAL

        return False

    def getButtonCPressed(self) -> bool:
        """Gets if the C button is pressed."""
        if self.buttonC:
            return self.buttonC.get()

        now = wpilib.Timer.getFPGATimestamp()
        if now > self.nextMessageTime:
            wpilib.DriverStation.reportError("Button C was not configured", True)
            self.nextMessageTime = now + self.MESSAGE_INTERVAL

        return False

    def setGreenLed(self, value: bool) -> None:
        """Sets the green LED."""
        if self.greenLed:
            self.greenLed.set(value)
        else:
            now = wpilib.Timer.getFPGATimestamp()
            if now > self.nextMessageTime:
                wpilib.DriverStation.reportError("Green LED was not configured", True)
                self.nextMessageTime = now + self.MESSAGE_INTERVAL

    def setRedLed(self, value: bool) -> None:
        """Sets the red LED."""
        if self.redLed:
            self.redLed.set(value)
        else:
            now = wpilib.Timer.getFPGATimestamp()
            if now > self.nextMessageTime:
                wpilib.DriverStation.reportError("Red LED was not configured", True)
                self.nextMessageTime = now + self.MESSAGE_INTERVAL

    def setYellowLed(self, value: bool) -> None:
        """Sets the yellow LED."""
        self.yellowLed.set(value)
