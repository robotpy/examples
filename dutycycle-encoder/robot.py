#!/usr/bin/env python3

import wpilib


class MyRobot(wpilib.TimedRobot):

    def robotInit(self):
        """Robot initialization function"""

        self.dutyCycleEncoder = wpilib.DutyCycleEncoder(0)

        self.dutyCycleEncoder.setDistancePerRotation(0.5)

    def robotPeriodic(self):
        # Connected can be checked, and uses the frequency of the encoder
        connected = self.dutyCycleEncoder.isConnected()

        # Duty Cycle Frequency in Hz
        frequency = self.dutyCycleEncoder.getFrequency()

        # Output of encoder
        output = self.dutyCycleEncoder.get()

        # Output scaled by DistancePerPulse
        distance = self.dutyCycleEncoder.getDistance()

        wpilib.SmartDashboard.putBoolean("Connected", connected)
        wpilib.SmartDashboard.putNumber("Frequency", frequency)
        wpilib.SmartDashboard.putNumber("Output", output)
        wpilib.SmartDashboard.putNumber("Distance", distance)


if __name__ == "__main__":
    wpilib.run(MyRobot)
