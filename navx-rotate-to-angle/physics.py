import wpilib.simulation

from pyfrc.physics.core import PhysicsInterface
from pyfrc.physics import drivetrains

import typing

if typing.TYPE_CHECKING:
    from robot import MyRobot


class PhysicsEngine:
    def __init__(self, physics_controller: PhysicsInterface, robot: "MyRobot"):
        """
        :param physics_controller: `pyfrc.physics.core.Physics` object
                                   to communicate simulation effects to
        :param robot: your robot object
        """

        self.physics_controller = physics_controller

        # Motors
        self.lf_motor = wpilib.simulation.PWMSim(robot.frontLeftMotor.getChannel())
        self.lr_motor = wpilib.simulation.PWMSim(robot.rearLeftMotor.getChannel())
        self.rf_motor = wpilib.simulation.PWMSim(robot.frontRightMotor.getChannel())
        self.rr_motor = wpilib.simulation.PWMSim(robot.rearRightMotor.getChannel())

        self.navx = wpilib.simulation.SimDeviceSim("navX-Sensor[4]")
        self.navx_yaw = self.navx.getDouble("Yaw")

        self.drivetrain = drivetrains.MecanumDrivetrain()

    def update_sim(self, now: float, tm_diff: float) -> None:
        """
        Called when the simulation parameters for the program need to be
        updated.

        :param now: The current time as a float
        :param tm_diff: The amount of time that has passed since the last
                        time that this function was called
        """

        # Simulate the drivetrain
        lf_motor = self.lf_motor.getSpeed()
        lr_motor = self.lr_motor.getSpeed()
        rf_motor = self.rf_motor.getSpeed()
        rr_motor = self.rr_motor.getSpeed()

        speeds = self.drivetrain.calculate(lf_motor, lr_motor, rf_motor, rr_motor)
        pose = self.physics_controller.drive(speeds, tm_diff)

        # Update the gyro simulation
        # -> FRC gyros like NavX are positive clockwise, but
        #    the returned pose is positive counter-clockwise
        self.navx_yaw.set(-pose.rotation().degrees())
