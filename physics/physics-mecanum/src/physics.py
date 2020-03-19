#
# See the notes for the other physics sample
#

import hal.simulation

from pyfrc.physics.core import PhysicsInterface
from pyfrc.physics import drivetrains


class PhysicsEngine:
    """
       Simulates a 4-wheel mecanum robot using Tank Drive joystick control 
    """

    def __init__(self, physics_controller):
        """
            :param physics_controller: `pyfrc.physics.core.Physics` object
                                       to communicate simulation effects to
        """

        self.physics_controller = physics_controller

        # Motors
        self.lf_motor = hal.simulation.PWMSim(1)
        self.lr_motor = hal.simulation.PWMSim(2)
        self.rf_motor = hal.simulation.PWMSim(3)
        self.rr_motor = hal.simulation.PWMSim(4)

        # Gyro
        self.gyro = hal.simulation.AnalogGyroSim(1)

        self.drivetrain = drivetrains.MecanumDrivetrain()

    def update_sim(self, now, tm_diff):
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
        # -> FRC gyros are positive clockwise, but the returned pose is positive
        #    counter-clockwise
        self.gyro.setAngle(-pose.rotation().degrees())
