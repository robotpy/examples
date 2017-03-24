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

from pyfrc.physics import drivetrains
from pyfrc.physics.visionsim import VisionSim

from networktables.util import ntproperty

class PhysicsEngine(object):
    '''
        Simulates a motor moving something that strikes two limit switches,
        one on each end of the track. Obviously, this is not particularly
        realistic, but it's good enough to illustrate the point
    '''
    
    # array of (found, timestamp, angle)
    target = ntproperty('/camera/target', (0.0, float('inf'), 0.0))
    
    def __init__(self, physics_controller):
        '''
            :param physics_controller: `pyfrc.physics.core.PhysicsInterface` object
                                       to communicate simulation effects to
        '''
        
        self.physics_controller = physics_controller
        self.position = 0
        
        self.physics_controller.add_device_gyro_channel('adxrs450_spi_0_angle')
        
        targets = [
                # right
                VisionSim.Target(15, 13, 250, 0),
                # middle
                VisionSim.Target(16.5, 15.5, 295, 65),
                # left
                VisionSim.Target(15, 18, 0, 110)
            ]
            
        self.vision = VisionSim(targets, 61.0, 1.5, 15, 15,
                                physics_controller=physics_controller)
        
    def update_sim(self, hal_data, now, tm_diff):
        '''
            Called when the simulation parameters for the program need to be
            updated.
            
            :param now: The current time as a float
            :param tm_diff: The amount of time that has passed since the last
                            time that this function was called
        '''
        
        # Simulate the drivetrain
        l_motor = hal_data['pwm'][0]['value']
        r_motor = hal_data['pwm'][1]['value']
        
        speed, rotation = drivetrains.two_motor_drivetrain(l_motor, r_motor)
        self.physics_controller.drive(speed, rotation, tm_diff)
        
        x, y, angle = self.physics_controller.get_position()
            
        data = self.vision.compute(now, x, y, angle)
        if data is not None:
            self.target = data[0][:3]
