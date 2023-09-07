#!/usr/bin/env python3
"""
    PWM Drivetrain Demo
"""

# The first lines should be the import of the needed modules
import wpilib
import wpilib.drive
import rev


# All code should be found in the MyRobot class. Note that in this example, the wpilib.TimedRobot robot base is used.
class MyRobot(wpilib.TimedRobot):
    def robotInit(self):
        """Robot initialization function"""

        # create motor controller objects
        m_left = rev.CANSparkMax(1, rev.CANSparkMax.MotorType.kBrushless)
        m_right = rev.CANSparkMax(2, rev.CANSparkMax.MotorType.kBrushless)
        self.robot_drive = wpilib.drive.DifferentialDrive(m_left, m_right)  # object that handles basic drive operations
        self.robot_drive.setExpiration(0.1)  # Configure protection in case of code slowdown or crash

        # joystick #0
        self.stick = wpilib.Joystick(0)

    def teleopInit(self):
        """Executed once at the start of teleop mode"""
        self.robot_drive.setSafetyEnabled(True)

    def teleopPeriodic(self):
        """Executed in loop while in teleop mode"""

        # Runs the motors with tank steering
        self.robot_drive.arcadeDrive(
            self.stick.getRawAxis(0), self.stick.getRawAxis(1), True
        )


# These lines should be found at the bottom and unchanged
if __name__ == "__main__":
    wpilib.run(MyRobot)
