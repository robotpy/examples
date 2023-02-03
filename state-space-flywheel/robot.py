#!/usr/bin/env python3
#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#

import wpilib
import wpimath
import wpimath.controller
import wpimath.system
import wpimath.system.plant
import wpimath.estimator

import math
import numpy

# A simple utility class for converting rpm to radians, as robotPY does not currently have a wpimath.util class.
import util.units

"""This is a sample program to demonstrate how to use a state-space controller to control a
flywheel.
"""


class MyRobot(wpilib.TimedRobot):
    kMotorPort = 0
    kEncoderAChannel = 0
    kEncoderBChannel = 1
    kJoystickPort = 0

    kFlywheelMomentOfInertia = 0.00032  # kg/m^2

    # Reduction between motors and encoder, as output over input. If the flywheel spins slower than
    # the motors, this number should be greater than one.
    kFlywheelGearing = 1

    def robotInit(self) -> None:
        self.kSpinUpRadPerSec = util.units.Units.rotationsPerMinuteToRadiansPerSecond(
            500
        )

        # The plant holds a state-space model of our flywheel. This system has the following properties:
        #
        # States: [velocity], in radians per second.
        # Inputs (what we can "put in"): [voltage], in volts.
        # Outputs (what we can measure): [velocity], in radians per second.
        self.flywheelPlant = wpimath.system.plant.LinearSystemId.flywheelSystem(
            wpimath.system.plant.DCMotor.NEO(2),
            self.kFlywheelMomentOfInertia,
            self.kFlywheelGearing,
        )

        # The observer fuses our encoder data and voltage inputs to reject noise.
        self.observer = wpimath.estimator.KalmanFilter_1_1_1(
            self.flywheelPlant,
            [3],  # How accurate we think our model is
            [0.01],  # How accurate we think our encoder data is
            0.020,
        )

        # A LQR uses feedback to create voltage commands.
        self.controller = wpimath.controller.LinearQuadraticRegulator_1_1(
            self.flywheelPlant,
            [8],  # qelms. Velocity error tolerance, in radians per second. Decrease
            # this to more heavily penalize state excursion, or make the controller behave more
            # aggressively.
            [12],  # relms. Control effort (voltage) tolerance. Decrease this to more
            # heavily penalize control effort, or make the controller less aggressive. 12 is a good
            # starting point because that is the (approximate) maximum voltage of a battery.
            0.020,  # Nominal time between loops. 0.020 for TimedRobot, but can be lower if using notifiers.
        )

        # The state-space loop combines a controller, observer, feedforward and plant for easy control.
        self.loop = wpimath.system.LinearSystemLoop_1_1_1(
            self.flywheelPlant, self.controller, self.observer, 12.0, 0.020
        )

        # An encoder set up to measure flywheel velocity in radians per second.
        self.encoder = wpilib.Encoder(self.kEncoderAChannel, self.kEncoderBChannel)

        self.motor = wpilib.PWMSparkMax(self.kMotorPort)

        # A joystick to read the trigger from.
        self.joystick = wpilib.Joystick(self.kJoystickPort)

        # We go 2 pi radians per 4096 clicks.
        self.encoder.setDistancePerPulse(2 * math.pi / 4096)

    def teleopInit(self) -> None:
        self.loop.reset([self.encoder.getRate()])

    def teleopPeriodic(self) -> None:
        # Sets the target speed of our flywheel. This is similar to setting the setpoint of a
        # PID controller.
        if self.joystick.getTriggerPressed():
            # We just pressed the trigger, so let's set our next reference
            self.loop.setNextR(numpy.array([self.kSpinUpRadPerSec]))

        elif self.joystick.getTriggerReleased():
            # We just released the trigger, so let's spin down
            self.loop.setNextR(numpy.array([self.kSpinUpRadPerSec]))

        # Correct our Kalman filter's state vector estimate with encoder data.
        self.loop.correct([self.encoder.getRate()])

        # Update our LQR to generate new voltage commands and use the voltages to predict the next
        # state with out Kalman filter.
        self.loop.predict(0.020)

        # Send the new calculated voltage to the motors.
        # voltage = duty cycle * battery voltage, so
        # duty cycle = voltage / battery voltage
        nextVoltage = self.loop.U()
        self.motor.setVoltage(nextVoltage)


if __name__ == "__main__":
    wpilib.run(MyRobot)
