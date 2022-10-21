# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.

import commands2
import ..examplesmartmotorcontroller
import ..constants
import wpimath.controller

# A robot arm subsystem that moves with a motion profile.
class ArmSubsystem(commands2.TrapezoidProfileSubsystem):

    # Create a new ArmSubsystem
    def __init__(self) -> None:
        super().__init__(
            TrapezoidProfile(
                constants.kMaxVelocityRadPerSecond, constants.kMaxAccelerationRadPerSecSquared
            ), constants.kArmOffsetRads
        )
        self.motor = ExampleSmartMotorController(constants.kMotorPort)
        self.feedforward = wpimath.controller.ArmFeedforward(
            constants.kSVolts, constants.kGVolts,
            constants.kVVoltSecondPerRad, ArmConstants.kAVoltSecondSquaredPerRad
        )
        self.motor.setPID(constants.kP, 0, 0)
    
    def useState(self, setpoint: TrapezoidProfile.State) -> None:
        # Calculate the feedforward from the setpoint
        feedfwd = self.feedforward.calculate(setpoint.position, setpoint.velocity)

        # Add the feedforward to the PID output to get the motor output
        self.motor.setSetPoint(
            ExampleSmartMotorController.PIDMode.kPosition, setpoint.position, feedforward / 12.0
        )