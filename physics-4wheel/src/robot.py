#!/usr/bin/env python3

import wpilib
import wpilib.drive


class MyRobot(wpilib.TimedRobot):
    """Main robot class"""

    def robotInit(self):
        """Robot-wide initialization code should go here"""

        self.lstick = wpilib.Joystick(0)
        self.rstick = wpilib.Joystick(1)

        self.lf_motor = wpilib.Jaguar(1)
        self.lr_motor = wpilib.Jaguar(2)
        self.rf_motor = wpilib.Jaguar(3)
        self.rr_motor = wpilib.Jaguar(4)

        l_motor = wpilib.SpeedControllerGroup(self.lf_motor, self.lr_motor)
        r_motor = wpilib.SpeedControllerGroup(self.rf_motor, self.rr_motor)

        self.drive = wpilib.drive.DifferentialDrive(l_motor, r_motor)

        # Position gets automatically updated as robot moves
        self.gyro = wpilib.AnalogGyro(1)

    def autonomousInit(self):
        """Called when autonomous mode is enabled"""

        self.timer = wpilib.Timer()
        self.timer.start()

    def autonomousPeriodic(self):
        if self.timer.get() < 2.0:
            self.drive.arcadeDrive(-1.0, -0.3)
        else:
            self.drive.arcadeDrive(0, 0)

    def teleopPeriodic(self):
        """Called when operation control mode is enabled"""
        self.drive.tankDrive(-self.lstick.getY(), -self.rstick.getY())


if __name__ == "__main__":
    wpilib.run(MyRobot)
