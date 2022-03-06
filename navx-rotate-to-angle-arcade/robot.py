#!/usr/bin/env python3

import wpilib
import wpilib.drive
import wpimath.controller

from navx import AHRS


class MyRobot(wpilib.TimedRobot):
    """This is a demo program showing the use of the navX MXP to implement
    a "rotate to angle" feature. This demo works in the pyfrc simulator.

    This example will automatically rotate the robot to one of four
    angles (0, 90, 180 and 270 degrees).

    This rotation can occur when the robot is still, but can also occur
    when the robot is driving.  When using field-oriented control, this
    will cause the robot to drive in a straight line, in whatever direction
    is selected.

    This example also includes a feature allowing the driver to "reset"
    the "yaw" angle.  When the reset occurs, the new gyro angle will be
    0 degrees.  This can be useful in cases when the gyro drifts, which
    doesn't typically happen during a FRC match, but can occur during
    long practice sessions.

    Note that the PID Controller coefficients defined below will need to
    be tuned for your drive system.
    """

    # The following PID Controller coefficients will need to be tuned */
    # to match the dynamics of your drive system.  Note that the      */
    # SmartDashboard in Test mode has support for helping you tune    */
    # controllers by displaying a form where you can enter new P, I,  */
    # and D constants and test the mechanism.                         */

    # Often, you will find it useful to have different parameters in
    # simulation than what you use on the real robot

    if wpilib.RobotBase.isSimulation():
        # These PID parameters are used in simulation
        kP = 0.02
        kI = 0.00
        kD = 0.00
    else:
        # These PID parameters are used on a real robot
        kP = 0.03
        kI = 0.00
        kD = 0.00

    kToleranceDegrees = 2.0

    def robotInit(self):
        # Channels for the wheels
        self.l_motor = wpilib.Spark(1)
        self.r_motor = wpilib.Spark(2)

        self.drive = wpilib.drive.DifferentialDrive(self.l_motor, self.r_motor)
        self.stick = wpilib.Joystick(0)

        #
        # Communicate w/navX MXP via the MXP SPI Bus.
        # - Alternatively, use the i2c bus.
        # See http://navx-mxp.kauailabs.com/guidance/selecting-an-interface/ for details
        #

        self.ahrs = AHRS.create_spi()
        # self.ahrs = AHRS.create_i2c()

        turnController = wpimath.controller.PIDController(
            self.kP,
            self.kI,
            self.kD,
        )
        turnController.enableContinuousInput(-180.0, 180.0)
        turnController.setTolerance(self.kToleranceDegrees)

        self.turnController = turnController

    def teleopInit(self):
        self.tm = wpilib.Timer()
        self.tm.start()

    def teleopPeriodic(self):
        """Runs the motors with onnidirectional drive steering.

        Implements Field-centric drive control.

        Also implements "rotate to angle", where the angle
        being rotated to is defined by one of four buttons.

        Note that this "rotate to angle" approach can also
        be used while driving to implement "straight-line
        driving".
        """

        if self.tm.hasPeriodPassed(1.0):
            print("NavX Gyro", self.ahrs.getYaw(), self.ahrs.getAngle())

        rotateToAngle = False
        if self.stick.getRawButton(1):
            self.ahrs.reset()

        if self.stick.getRawButton(2):
            setpoint = 0.0
            rotateToAngle = True
        elif self.stick.getRawButton(3):
            setpoint = 90.0
            rotateToAngle = True
        elif self.stick.getRawButton(4):
            setpoint = 179.9
            rotateToAngle = True
        elif self.stick.getRawButton(5):
            setpoint = -90.0
            rotateToAngle = True

        if rotateToAngle:
            currentRotationRate = self.turnController.calculate(
                self.ahrs.getYaw(), setpoint
            )
        else:
            self.turnController.reset()
            currentRotationRate = self.stick.getX()

        # Use the joystick Y axis for forward movement,
        # and either the X axis for rotation or the current
        # calculated rotation rate depending upon whether
        # "rotate to angle" is active.
        #
        # This works better for mecanum drive robots, but this
        # illustrates one way you could implement this using
        # a 4 wheel drive robot

        self.drive.arcadeDrive(-self.stick.getY(), currentRotationRate)


if __name__ == "__main__":
    wpilib.run(MyRobot)
