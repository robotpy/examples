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

from pyfrc.physics import motor_cfgs, tankmodel
from pyfrc.physics.units import units


class PhysicsEngine(object):
    '''
        Simulates a motor moving something that strikes two limit switches,
        one on each end of the track. Obviously, this is not particularly
        realistic, but it's good enough to illustrate the point
    '''
    
    def __init__(self, physics_controller):
        '''
            :param physics_controller: `pyfrc.physics.core.PhysicsInterface` object
                                       to communicate simulation effects to
        '''
        
        self.physics_controller = physics_controller
        self.position = 0
        
        # Change these parameters to fit your robot!
        bumper_width = 3.25*units.inch
        
        self.drivetrain = tankmodel.TankModel.theory(
            motor_cfgs.MOTOR_CFG_CIM,           # motor configuration
            110*units.lbs,                      # robot mass
            10.71,                              # drivetrain gear ratio
            2,                                  # motors per side
            22*units.inch,                      # robot wheelbase
            23*units.inch + bumper_width*2,     # robot width
            32*units.inch + bumper_width*2,     # robot length
            6*units.inch                        # wheel diameter
        )
        
        # Precompute the encoder constant
        # -> encoder counts per revolution / wheel circumference
        self.kEncoder = 360 / (0.5 * math.pi)
        
        self.l_distance = 0
        self.r_distance = 0
            
    def update_sim(self, hal_data, now, tm_diff):
        '''
            Called when the simulation parameters for the program need to be
            updated.
            
            :param now: The current time as a float
            :param tm_diff: The amount of time that has passed since the last
                            time that this function was called
        '''
        
        # Simulate the drivetrain
        l_motor = hal_data['pwm'][1]['value']
        r_motor = hal_data['pwm'][2]['value']
        
        x, y, angle = self.drivetrain.get_distance(l_motor, r_motor, tm_diff)
        self.physics_controller.distance_drive(x, y, angle)
        
        # Update encoders
        self.l_distance += self.drivetrain.l_velocity * tm_diff
        self.r_distance += self.drivetrain.r_velocity * tm_diff
        
        hal_data['encoder'][0]['count'] = int(self.l_distance * self.kEncoder)
        hal_data['encoder'][1]['count'] = int(self.r_distance * self.kEncoder)
