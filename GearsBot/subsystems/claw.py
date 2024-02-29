#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#

import wpilib
import commands2
import ..constants

class Claw(commands2.Subsystem):
    """The claw subsystem is a simple system with a motor for opening and closing. 
    If using stronger motors, you should probably use a sensor so that the motors don't stall."""

    def __init__(self) -> None:
        """Create a new claw subsystem."""
        super().__init__()

        self.motor = wpilib.Victor(constants.ClawConstants.kMotorPort)
        self.contact = wpilib.DigitalInput(constants.ClawConstants.kContactPort)

        # Let's name everything on the LiveWindow
        addChild("Motor", self.motor)
        addChild("Limit Switch", self.contact)

    def log(self) -> None:
        wpilib.SmartDashboard.putData("Claw switch", self.contact)

    def open(self) -> None:
        """Set the claw motor to move in the open direction."""
        self.motor.set(-1)

    def close(self) -> None:
        """Set the claw motor to move in the close direction."""
        self.motor.set(1)

    def stop(self) -> None:
        """Stops the claw motor from moving."""
        self.motor.set(0)

    def isGrabbing(self) -> bool:
        """Return true when the robot is grabbing an object hard enough to
        trigger the limit switch."""
        return self.contact.get()
    
    def periodic(self) -> None:
        """Call log method every loop."""
        self.log()
