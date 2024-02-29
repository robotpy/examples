#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#

import commands2
import wpilib
import wpimath.controller
import ..constants
import ..robot

class Wrist(commands2.PIDSubsystem):
    """The wrist subsystem is like the elevator, but with a rotational
    joint instead of a linear joint."""

    def __init__(self) -> None:
        """Create a new wrist subsystem."""
        super().__init__(
            wpimath.controller.PIDController(
                constants.WristConstants.kP,
                constants.WristConstants.kI,
                constants.WristConstants.kD,
            )
        )

        self.getController().setTolerance(constants.WristConstants.kTolerance)

        self.motor = wpilib.Victor(constants.WristConstants.kMotorPort)

        # Conversion value of potentiometer varies between the real world and simulation
        if robot.MyRobot.isReal():
            self.pot = wpilib.AnalogPotentiometer(
                constants.ElevatorConstants.kPotentiometerPort, -270.0 / 5
            )
        else:
            # Defaults to meters
            self.pot = wpilib.AnalogPotentiometer(
                constants.ElevatorConstants.kPotentiometerPort
            )
        
        # Let's name everything on the LiveWindow
        self.addChild("Motor", self.motor)
        self.addChild("Pot", self.pot)
    
    def log(self) -> None:
        """The log method puts interesting information to the SmartDashboard."""
        wpilib.SmartDashboard.putData("Wrist Angle", self.pot)

    def getMeasurement(self) -> float:
        """Use the potentiometer as the PID sensor. This method is automatically 
        called by the subsystem."""
        return self.pot.get()
    
    def useOutput(self, output: float, setpoint: float) -> None:
        """Use the motor as the PID output. This method is automatically called
        by the subsystem."""
        self.motor.set(output)

    def periodic(self) -> None:
        """Call log method every loop."""
        self.log();
