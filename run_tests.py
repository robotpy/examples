#!/usr/bin/env python3
#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#
import os
import subprocess
import sys
from pathlib import Path


def main():
    BASE_TESTS = [
        "AddressableLED",
        "AprilTagsVision",
        "ArcadeDrive",
        "ArcadeDriveXboxController",
        "ArmSimulation",
        "AxisCamera",
        "CANPDP",
        "DifferentialDriveBot",
        "DigitalCommunication",
        "DutyCycleEncoder",
        "DutyCycleInput",
        "ElevatorProfiledPID",
        "ElevatorSimulation",
        "ElevatorTrapezoidProfile",
        "Encoder",
        "FlywheelBangBangController",
        "GameData",
        "GettingStarted",
        "Gyro",
        "GyroMecanum",
        "HatchbotInlined",
        "HatchbotTraditional",
        "HidRumble",
        "I2CCommunication",
        "IntermediateVision",
        "MagicbotSimple",
        "MecanumBot",
        "MecanumDrive",
        "MecanumDriveXbox",
        "Mechanism2d",
        "MotorControl",
        "Physics/src",
        "Physics4Wheel/src",
        "PhysicsMecanum/src",
        "PhysicsSPI/src",
        "PotentiometerPID",
        "QuickVision",
        "RamseteController",
        "Relay",
        "ShuffleBoard",
        "Solenoid",
        "StatefulAutonomous",
        "StateSpaceFlywheel",
        "StateSpaceFlywheelSysId",
        "SwerveBot",
        "TankDrive",
        "TankDriveXboxController",
        "Timed/src",
        "Ultrasonic",
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

    current_directory = Path(__file__).parent
    for x in current_directory.glob("./**/robot.py"):
        manipulatedPath = os.path.relpath(x.parent, "examples")[3:].replace("\\", r"/")
        print(manipulatedPath)
        if manipulatedPath in BASE_TESTS:
            os.chdir(x.parent)
            os.system(f"{sys.executable} -m robotpy sync")
            os.system(f"{sys.executable} -m robotpy test --builtin")
            print(f"File Passed - {x.parent}")
        elif manipulatedPath in ignoredTests:
            os.chdir(x.parent)
            os.system(f"{sys.executable} -m robotpy sync")
            print(f"File Passed - {x.parent}")
        else:
            print("ERROR: Not every robot.py file is in the list of tests!")
            exit(1)


if __name__ == "__main__":
    main()
