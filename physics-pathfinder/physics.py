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
# NOTE: THIS API IS ALPHA AND WILL MOST LIKELY CHANGE!
#       ... if you have better ideas on how to implement, submit a patch!
#

import math
from pyfrc.physics import drivetrains


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
        
        # speed should be same as robot.MAX_VELOCITY
        self.drivetrain = drivetrains.TwoMotorDrivetrain(speed=5)
        
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
        
        speed, rotation = self.drivetrain.get_vector(l_motor, r_motor)
        self.physics_controller.drive(speed, rotation, tm_diff)
        
        # Update encoders
        self.l_distance += self.drivetrain.l_speed * tm_diff
        self.r_distance += self.drivetrain.r_speed * tm_diff
        
        hal_data['encoder'][0]['count'] = int(self.l_distance * self.kEncoder)
        hal_data['encoder'][1]['count'] = int(self.l_distance * self.kEncoder)
