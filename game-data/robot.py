#!/usr/bin/env python3
"""
Example file showing how to get game-data from your driver station / FMS
"""
import wpilib
from networktables import NetworkTables

class GameDataRobot(wpilib.IterativeRobot):
    def robotInit(self):
        # A way of demonstrating the difference between the game data strings
        self.blue = wpilib.Solenoid(0)
        self.red = wpilib.Solenoid(1)
        self.green = wpilib.Solenoid(2)
        self.yellow = wpilib.Solenoid(3)
        # Set game data to empty string by default
        self.gameData = ''
        # Get the SmartDashboard table from networktables
        self.sd = NetworkTables.getTable("SmartDashboard")

    def teleopPeriodic(self):
        data = self.ds.getGameSpecificMessage()
        if len(data) > 0:
            # Set the robot gamedata property and set a network tables value
            self.gameData = data
            self.sd.putString("gameData", self.gameData)

        # Solenoid based indicator of the current color
        self.blue.set(self.gameData == "B")
        self.red.set(self.gameData == "R")
        self.green.set(self.gameData == "G")
        self.yellow.set(self.gameData == "Y")


if __name__ == "__main__":
    wpilib.run(GameDataRobot)
