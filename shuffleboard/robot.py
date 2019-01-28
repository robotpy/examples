#!/usr/bin/env python3
# ----------------------------------------------------------------------------
# Copyright (c) FIRST 2008. All Rights Reserved.
# Open Source Software - may be modified and shared by FRC teams. The code
# must be accompanied by the FIRST BSD license file in the root directory of
# the project.
# ----------------------------------------------------------------------------

import wpilib
from wpilib.drive import DifferentialDrive
from wpilib.shuffleboard import Shuffleboard


class Robot(wpilib.TimedRobot):
    def robotInit(self):
        self.tankDrive = DifferentialDrive(
            wpilib.PWMVictorSPX(0), wpilib.PWMVictorSPX(1)
        )
        self.leftEncoder = wpilib.Encoder(0, 1)
        self.rightEncoder = wpilib.Encoder(2, 3)

        self.elevatorMotor = wpilib.PWMVictorSPX(2)
        self.elevatorPot = wpilib.AnalogPotentiometer(0)

        # Add a 'max speed' widget to a tab named 'Configuration', using a number slider
        # The widget will be placed in the second column and row and will be two columns wide
        self.maxSpeed = (
            Shuffleboard.getTab("Configuration")
            .add(title="Max Speed", value=1)
            .withWidget("Number Slider")
            .withPosition(1, 1)
            .withSize(2, 1)
            .getEntry()
        )

        # Add the tank drive and encoders to a 'Drivebase' tab
        driveBaseTab = Shuffleboard.getTab("Drivebase")
        driveBaseTab.add(title="Tank Drive", value=self.tankDrive)
        # Put both encoders in a list layout
        encoders = (
            driveBaseTab.getLayout(type="List Layout", title="Encoders")
            .withPosition(0, 0)
            .withSize(2, 2)
        )
        encoders.add(title="Left Encoder", value=self.leftEncoder)
        encoders.add(title="Right Encoder", value=self.rightEncoder)

        # Add the elevator motor and potentiometer to an 'Elevator' tab
        elevatorTab = Shuffleboard.getTab("Elevator")
        elevatorTab.add(title="Motor", value=self.elevatorMotor)
        elevatorTab.add(title="Potentiometer", value=self.elevatorPot)

    def autonomousInit(self):
        # Read the value of the 'max speed' widget from the dashboard
        self.tankDrive.setMaxOutput(self.maxSpeed.getDouble(1.0))


if __name__ == "__main__":
    wpilib.run(Robot)
