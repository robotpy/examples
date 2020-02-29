#
# See the notes for the other physics sample
#


import hal.simulation

from pyfrc.physics.core import PhysicsInterface
from pyfrc.physics import motor_cfgs, tankmodel
from pyfrc.physics.units import units


class PhysicsEngine:
    """
       Simulates a 4-wheel robot using Tank Drive joystick control
    """

    def __init__(self, physics_controller):
        """
            :param physics_controller: `pyfrc.physics.core.Physics` object
                                       to communicate simulation effects to
        """

        self.physics_controller = physics_controller

        # Motors
        self.lf_motor = hal.simulation.PWMSim(1)
        # self.lr_motor = hal.simulation.PWMSim(2)
        self.rf_motor = hal.simulation.PWMSim(3)
        # self.rr_motor = hal.simulation.PWMSim(4)

        # Gyro
        self.gyro = hal.simulation.AnalogGyroSim(1)

        # Change these parameters to fit your robot!
        bumper_width = 3.25 * units.inch

        # fmt: off
        self.drivetrain = tankmodel.TankModel.theory(
            motor_cfgs.MOTOR_CFG_CIM,           # motor configuration
            110 * units.lbs,                    # robot mass
            10.71,                              # drivetrain gear ratio
            2,                                  # motors per side
            22 * units.inch,                    # robot wheelbase
            23 * units.inch + bumper_width * 2, # robot width
            32 * units.inch + bumper_width * 2, # robot length
            6 * units.inch,                     # wheel diameter
        )
        # fmt: on

    def update_sim(self, now, tm_diff):
        """
            Called when the simulation parameters for the program need to be
            updated.
            
            :param now: The current time as a float
            :param tm_diff: The amount of time that has passed since the last
                            time that this function was called
        """

        # Simulate the drivetrain (only front motors used because read should be in sync)
        lf_motor = self.lf_motor.getSpeed()
        rf_motor = self.rf_motor.getSpeed()

        transform = self.drivetrain.calculate(lf_motor, rf_motor, tm_diff)
        pose = self.physics_controller.move_robot(transform)

        # Update the gyro simulation
        # -> FRC gyros are positive clockwise, but the returned pose is positive
        #    counter-clockwise
        self.gyro.setAngle(-pose.rotation().degrees())
