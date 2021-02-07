#
# See the documentation for more details on how this works
#
# The idea here is you provide a simulation object that overrides specific
# pieces of WPILib, and modifies motors/sensors accordingly depending on the
# state of the simulation. An example of this would be measuring a motor
# moving for a set period of time, and then changing a limit switch to turn
# on after that period of time. This can help you do more complex simulations
# of your robot code without too much extra effort.
#

from wpilib.simulation import PWMSim

from pyfrc.physics import drivetrains

from pyfrc.physics.visionsim import VisionSim

from networktables.util import ntproperty


class PhysicsEngine:
    """
    Simulates a motor moving something that strikes two limit switches,
    one on each end of the track. Obviously, this is not particularly
    realistic, but it's good enough to illustrate the point
    """

    # array of (found, timestamp, angle)
    target = ntproperty("/camera/target", (0.0, float("inf"), 0.0))

    def __init__(self, physics_controller):
        """
        :param physics_controller: `pyfrc.physics.core.PhysicsInterface` object
                                   to communicate simulation effects to
        """

        self.physics_controller = physics_controller
        self.position = 0

        targets = [
            # right
            VisionSim.Target(15, 13, 250, 0),
            # middle
            VisionSim.Target(16.5, 15.5, 295, 65),
            # left
            VisionSim.Target(15, 18, 0, 110),
        ]

        self.vision = VisionSim(
            targets, 61.0, 1.5, 15, 15, physics_controller=physics_controller
        )
        
        # Simulate the drivetrain. 
        self.drivetrain = drivetrains.TwoMotorDrivetrain(deadzone=drivetrains.linear_deadzone(0.1))

        # Create the motors.
        self.l_motor = PWMSim(0)
        self.r_motor = PWMSim(1)

    def update_sim(self, now, tm_diff):
        """
        Called when the simulation parameters for the program need to be
        updated.

        :param now: The current time as a float
        :param tm_diff: The amount of time that has passed since the last
                        time that this function was called
        """
        
        l_speed = self.l_motor.getSpeed()
        r_speed = self.r_motor.getSpeed()

        # Compute chassis speeds based off of motor speeds. 
        speeds = self.drivetrain.calculate(l_speed, r_speed)

        self.physics_controller.drive(speeds, tm_diff)

        pose = self.physics_controller.get_pose()
        
        x = pose.translation().X()
        y = pose.translation().Y()
        
        angle = pose.rotation().degrees()

        data = self.vision.compute(now, x, y, angle)
        if data is not None:
            self.target = data[0][:3]
