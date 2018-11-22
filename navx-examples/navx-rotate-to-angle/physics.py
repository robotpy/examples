
from pyfrc.physics import drivetrains

class PhysicsEngine(object):
  
    def __init__(self, physics_controller):
        '''
            :param physics_controller: `pyfrc.physics.core.PhysicsInterface` object
                                       to communicate simulation effects to
        '''
        
        self.physics_controller = physics_controller
        self.position = 0
        
        self.physics_controller.add_device_gyro_channel('navxmxp_i2c_1_angle')
        self.physics_controller.add_device_gyro_channel('navxmxp_spi_4_angle')
            
    def update_sim(self, hal_data, now, tm_diff):
        '''
            Called when the simulation parameters for the program need to be
            updated.
            
            :param now: The current time as a float
            :param tm_diff: The amount of time that has passed since the last
                            time that this function was called
        '''
        
        # Simulate the drivetrain
        lf_motor = hal_data['pwm'][2]['value']
        lr_motor = hal_data['pwm'][3]['value']
        rf_motor = hal_data['pwm'][1]['value']
        rr_motor = hal_data['pwm'][0]['value']
        
        vx, vy, vw = drivetrains.mecanum_drivetrain(lr_motor, rr_motor, lf_motor, rf_motor)
        self.physics_controller.vector_drive(vx, vy, vw, tm_diff)
        
