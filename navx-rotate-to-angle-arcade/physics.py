
from pyfrc.physics import motor_cfgs, tankmodel
from pyfrc.physics.units import units

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
        #lr_motor = hal_data['pwm'][3]['value']
        rf_motor = hal_data['pwm'][1]['value']
        #rr_motor = hal_data['pwm'][0]['value']
        
        x, y, angle = self.drivetrain.get_distance(lf_motor, rf_motor, tm_diff)
        self.physics_controller.distance_drive(x, y, angle)
        
