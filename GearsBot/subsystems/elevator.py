#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#

import wpilib
import wpimath.controller
import commands2
import constants
import robot

class Elevator(commands2.PIDSubsystem):
    def __init__(self) -> None:
        """Create a new elevator subsystem."""
        super().__init__(
            wpimath.controller.PIDController(
                constants.ElevatorConstants.kP_real,
                constants.ElevatorConstants.kI_real,
                constants.ElevatorConstants.kD_real,
            )
        )

        self.motor = wpilib.Victor(constants.ElevatorConstants.kMotorPort)

        if robot.MyRobot.isSimulation(): # Check for simulation and update PID values
            self.getController().setPID(
                constants.ElevatorConstants.kP_simulation,
                constants.ElevatorConstants.kI_simulation,
                constants.ElevatorConstants.kD,
            )
        self.getController().setTolerance(constants.ElevatorConstants.kTolerance)

        # Conversion value of potentiometer varies between the real world and simulation
        if robot.MyRobot.isReal():
            self.pot = wpilib.AnalogPotentiometer(
                constants.ElevatorConstants.kPotentiometerPort, -2.0 / 5
            )
        else:
            # Defaults to meters
            self.pot = wpilib.AnalogPotentiometer(
                constants.ElevatorConstants.kPotentiometerPort
            )

        # Let's name everything on the LiveWindow
        self.addChild("Motor", self.motor);
        self.addChild("Pot", self.pot);
    
    def log(self) -> None:
        """The log method puts interesting information to the SmartDashboard."""
        wpilib.SmartDashboard.putData("Elevator Pot", self.pot)

    def getMeasurement(self) -> None:
        """Use the potentiometer as the PID sensor. This method is automatically 
        called by the subsystem."""
        return self.pot.get()
    
    def useOutput(self, output: float, setpoint: float) -> None:
        """Use the motor as the PID output. This method is automatically called
        by the subsystem."""
        self.motor.set(output)
    
    def periodic(self) -> None:
        """Call log method every loop."""
        self.log()
