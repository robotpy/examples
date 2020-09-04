#!/usr/bin/env python3

import wpilib

import wpilib.drive
import wpilib.controller

from networktables.util import ntproperty


class MyRobot(wpilib.IterativeRobot):
    """Main robot class"""

    # array of (found, timestamp, angle)
    target = ntproperty("/camera/target", (0.0, float("inf"), 0.0))

    # Often, you will find it useful to have different parameters in
    # simulation than what you use on the real robot

    if wpilib.RobotBase.isSimulation():
        # These PID parameters are used in simulation
        kP = 0.03
        kI = 0.00
        kD = 0.00
        kF = 0.00
    else:
        # These PID parameters are used on a real robot
        kP = 0.03
        kI = 0.00
        kD = 0.00
        kF = 0.00

    kToleranceDegrees = 2.0

    def robotInit(self):
        """Robot-wide initialization code should go here"""

        # Basic robot chassis setup
        self.stick = wpilib.Joystick(0)
        
        self.robot_drive = wpilib.drive.DifferentialDrive(wpilib.interfaces.SpeedController(), wpilib.interfaces.SpeedController())

        # Position gets automatically updated as robot moves
        self.gyro = wpilib.ADXRS450_Gyro()

        # Use PIDController to control angle
        turnController = wpilib.controller.PIDController(
            self.kP, self.kI, self.kD, self.kF
        )
        turnController.setTolerance(self.kToleranceDegrees)

        self.turnController = turnController

        self.rotateToAngleRate = 0

    def normalizeAngle(self, angle):
        """Normalize angle to [-180,180]"""
        return ((angle + 180) % 360) - 180.0

    def pidGet(self):
        """The angle to feed to PIDController must be between
           -180 and 180"""
        return self.normalizeAngle(self.gyro.getAngle())

    def pidWrite(self, output):
        """This function is invoked periodically by the PID Controller"""
        self.rotateToAngleRate = output

    def teleopPeriodic(self):
        """Called every 20ms in teleop"""

        # if trigger is pressed, then center the robot to the camera target
        if self.stick.getTrigger():

            found, timestamp, offset = self.target
            turnSpeed = 0.0

            if found > 0:
                self.turnController.enable()

                # remember: the camera tells you the *offset*, so the angle you
                # want the robot to go to is the angle + the offset
                angle = self.gyro.getAngle() + offset

                # setpoint needs to be normalized
                angle = self.normalizeAngle(angle)

                self.turnController.setSetpoint(angle)
                turnSpeed = self.rotateToAngleRate
            else:
                self.turnController.disable()

            self.robot_drive.arcadeDrive(0, turnSpeed)
        else:
            self.robot_drive.arcadeDrive(self.stick, True)


if __name__ == "__main__":
    wpilib.run(MyRobot)
