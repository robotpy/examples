#!/usr/bin/env python3
"""
This sample program shows how to use Mechanism2d - a visual representation of arms, elevators,
and other mechanisms on dashboards; driven by a node-based API.

Ligaments are based on other ligaments or roots, and roots are contained in the base
Mechanism2d object.
"""

import wpilib


class MyRobot(wpilib.TimedRobot):
    kMetersPerPulse = 0.01
    kElevatorMinimumLength = 0.5

    def robotInit(self):
        self.elevatorMotor = wpilib.PWMSparkMax(0)
        self.wristMotor = wpilib.PWMSparkMax(1)
        self.wristPot = wpilib.AnalogPotentiometer(1, 90)
        self.elevatorEncoder = wpilib.Encoder(0, 1)
        self.joystick = wpilib.Joystick(0)

        self.elevatorEncoder.setDistancePerPulse(self.kMetersPerPulse)

        # the main mechanism object
        self.mech = wpilib.Mechanism2d(3, 3)
        # the mechanism root node
        self.root = self.mech.getRoot("climber", 2, 0)

        # MechanismLigament2d objects represent each "section"/"stage" of the mechanism, and are based
        # off the root node or another ligament object
        self.elevator = self.root.appendLigament(
            "elevator", self.kElevatorMinimumLength, 90
        )
        self.wrist = self.elevator.appendLigament(
            "wrist", 0.5, 90, 6, wpilib.Color8Bit(wpilib.Color.kPurple)
        )

        # post the mechanism to the dashboard
        wpilib.SmartDashboard.putData("Mech2d", self.mech)

    def robotPeriodic(self):
        # update the dashboard mechanism's state
        self.elevator.setLength(
            self.kElevatorMinimumLength + self.elevatorEncoder.getDistance()
        )
        self.wrist.setAngle(self.wristPot.get())

    def teleopPeriodic(self):
        self.elevatorMotor.set(self.joystick.getRawAxis(0))
        self.wristMotor.set(self.joystick.getRawAxis(1))


if __name__ == "__main__":
    wpilib.run(MyRobot)
