#
# TODO: This example has been updated for 2020, but still needs
#       quite a bit of polish
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

import math
import hal.simulation


from pyfrc.physics import motor_cfgs, tankmodel
from pyfrc.physics.units import units


class Field:
    # TODO: this will be in a future pyfrc release

    def __init__(self):
        self.device = hal.SimDevice("Field2D")
        self.fx = self.device.createDouble("x", False, 0.0)
        self.fy = self.device.createDouble("y", False, 0.0)
        self.frot = self.device.createDouble("rot", False, 0.0)

        self.x = 0
        self.y = 0
        self.angle = 0

    def distance_drive(self, x, y, angle):
        """Call this from your :func:`PhysicsEngine.update_sim` function.
           Will update the robot's position on the simulation field.
           
           This moves the robot some relative distance and angle from
           its current position.
           
           :param x:     Feet to move the robot in the x direction
           :param y:     Feet to move the robot in the y direction
           :param angle: Radians to turn the robot
        """
        # TODO: use wpilib kinematics?

        self.angle += angle

        c = math.cos(self.angle)
        s = math.sin(self.angle)

        self.x += x * c - y * s
        self.y += x * s + y * c
        
        self.fx.set(self.x)
        self.fy.set(self.y)
        self.frot.set(math.degrees(self.angle))


class PhysicsEngine(object):
    """
        Simulates a motor moving something that strikes two limit switches,
        one on each end of the track. Obviously, this is not particularly
        realistic, but it's good enough to illustrate the point
    """

    def __init__(self):

        self.field = Field()

        # Motors
        self.l_motor = hal.simulation.PWMSim(1)
        self.r_motor = hal.simulation.PWMSim(2)

        self.dio1 = hal.simulation.DIOSim(1)
        self.dio2 = hal.simulation.DIOSim(2)
        self.ain2 = hal.simulation.AnalogInSim(2)

        self.motor = hal.simulation.PWMSim(4)

        self.position = 0

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

        # Simulate the drivetrain
        l_motor = self.l_motor.getSpeed()
        r_motor = self.r_motor.getSpeed()

        x, y, angle = self.drivetrain.get_distance(l_motor, r_motor, tm_diff)
        self.field.distance_drive(x, y, angle)

        # update position (use tm_diff so the rate is constant)
        self.position += self.motor.getSpeed() * tm_diff * 3

        # update limit switches based on position
        if self.position <= 0:
            switch1 = True
            switch2 = False

        elif self.position > 10:
            switch1 = False
            switch2 = True

        else:
            switch1 = False
            switch2 = False

        # set values here
        self.dio1.setValue(switch1)
        self.dio2.setValue(switch2)
        self.ain2.setVoltage(self.position)
