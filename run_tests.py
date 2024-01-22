#!/usr/bin/env python3
#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#
import os
from pathlib import Path


BASE_TESTS = [
    "AddressableLED"
    "ArcadeDrive"
    "ArcadeDriveXboxController"
    "ArmSimulation"
    "CANPDP"
    "DifferentialDriveBot"
    "DigitalCommunication"
    "DutyCycleEncoder"
    "DutyCycleInput"
    "ElevatorProfiledPID"
    "ElevatorSimulation"
    "ElevatorTrapezoidProfile"
    "Encoder"
    "FlywheelBangBangController"
    "GameData"
    "GettingStarted"
    "Gyro"
    "GyroMecanum"
    "HatchbotInlined"
    "HatchbotTraditional"
    "HidRumble"
    "I2CCommunication"
    "IntermediateVision"
    "MagicbotSimple"
    "MecanumBot"
    "MecanumDrive"
    "MecanumDriveXbox"
    "Mechanism2d"
    "MotorControl"
    "Physics/src"
    "Physics4Wheel/src"
    "PhysicsMecanum/src"
    "PhysicsSPI/src"
    "PotentiometerPID"
    "QuickVision"
    "RamseteController"
    "Relay"
    "ShuffleBoard"
    "Solenoid"
    "StatefulAutonomous"
    "StateSpaceFlywheel"
    "StateSpaceFlywheelSysId"
    "SwerveBot"
    "TankDrive"
    "TankDriveXboxController"
    "Timed/src"
    "Ultrasonic"
    "UltrasonicPID"
]

ignoredTests = [
    "ArmBot",
    "ArmBotOffboard",
    "DriveDistanceOffboard",
    "FrisbeeBot",
    "GyroDriveCommands",
    "RamseteCommand",
    "SchedulerEventLogging",
    "SelectCommand",
    "RomiReference",
    "PhysicsCamSim/src"
]


def main():
    current_directory = Path(__file__).parent
    for x in current_directory.glob("./**/robot.py"):
        os.system(f"cd {x.parent}")
        os.system("python -m robotpy sync")


if __name__ == "__main__":
    main()
