#!/usr/bin/env python3
"""
    This is a sample program to demonstrate the use of a BangBangController with a flywheel to
    control RPM.
"""

import wpilib
import wpilib.simulation
import wpimath.controller
from wpimath.system.plant import DCMotor
import wpimath.units

import math


class MyRobot(wpilib.TimedRobot):

    MOTOR_PORT = 0
    ENCODER_A_CHANNEL = 0
    ENCODER_B_CHANNEL = 1

    # Max setpoint for joystick control in RPM
    MAX_SETPOINT_VALUE = 6000.0

    # Gains are for example purposes only - must be determined for your own robot!
    FLYWHEEL_KS = 0.0001  # V
    FLYWHEEL_KV = 0.000195  # V/RPM
    FLYWHEEL_KA = 0.0003  # V/(RPM/s)

    # Reduction between motors and encoder, as output over input. If the flywheel
    # spins slower than the motors, this number should be greater than one.
    FLYWHEEL_GEARING = 1.0

    # 1/2 MR²
    FLYWHEEL_MOMENT_OF_INERTIA = 0.5 * wpimath.units.lbsToKilograms(1.5) * math.pow(wpimath.units.inchesToMeters(4), 2)

    def robotInit(self):
        """Robot initialization function"""

        self.feedforward = wpimath.controller.SimpleMotorFeedforwardMeters(self.FLYWHEEL_KS, self.FLYWHEEL_KV, self.FLYWHEEL_KA)

        # Joystick to control setpoint
        self.joystick = wpilib.Joystick(0)

        self.flywheelMotor = wpilib.PWMSparkMax(self.MOTOR_PORT)
        self.encoder = wpilib.Encoder(self.ENCODER_A_CHANNEL, self.ENCODER_B_CHANNEL)

        self.bangBangControler = wpimath.controller.BangBangController()

        # Simulation classes help us simulate our robot
        self.flywheelSim = wpilib.simulation.FlywheelSim(DCMotor.NEO(1), self.FLYWHEEL_GEARING, self.FLYWHEEL_MOMENT_OF_INERTIA);
        self.encoderSim = wpilib.simulation.EncoderSim(self.encoder)

        # Add bang-bang controler to SmartDashboard and networktables.
        wpilib.SmartDashboard.putData(self.bangBangControler)

    def teleopPeriodic(self):
        """Controls flywheel to a set speed (RPM) controlled by a joystick."""

        # Scale setpoint value between 0 and maxSetpointValue
        setpoint = max(
           0.0,
           self.joystick.getRawAxis(0) * wpimath.units.rotationsPerMinuteToRadiansPerSecond(self.MAX_SETPOINT_VALUE)
        )

        # Set setpoint and measurement of the bang-bang controller
        bangOutput = self.bangBangControler.calculate(self.encoder.getRate(), setpoint) * 12.0

        # Controls a motor with the output of the BangBang controller and a
        # feedforward. The feedforward is reduced slightly to avoid overspeeding
        # the shooter.
        self.flywheelMotor.setVoltage(bangOutput + 0.9 * self.feedforward.calculate(setpoint))

    def _simulationPeriodic(self):
        """Update our simulation. This should be run every robot loop in simulation."""

        # To update our simulation, we set motor voltage inputs, update the
        # simulation, and write the simulated velocities to our simulated encoder
        self.flywheelSim.setInputVoltage(self.flywheelMotor.get() * wpilib.RobotController.getInputVoltage())
        self.flywheelSim.update(0.02)
        self.encoderSim.setRate(self.flywheelSim.getAngularVelocity())


if __name__ == "__main__":
    wpilib.run(MyRobot)
