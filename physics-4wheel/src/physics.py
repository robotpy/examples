#
# See the notes for the other physics sample
#


from pyfrc.physics import motor_cfgs, tankmodel
from pyfrc.physics.units import units


class PhysicsEngine(object):
    '''
       Simulates a 4-wheel robot using Tank Drive joystick control
    '''
    
    
    def __init__(self, physics_controller):
        '''
            :param physics_controller: `pyfrc.physics.core.Physics` object
                                       to communicate simulation effects to
        '''
        
        self.physics_controller = physics_controller
        
        # Change these parameters to fit your robot!
        motor_cfg = motor_cfgs.MOTOR_CFG_CIM
        robot_mass = 110*units.lbs
        
        bumper_width = 3.25*units.inch
        robot_wheelbase = 22*units.inch
        robot_width = 23*units.inch + bumper_width*2
        robot_length = 32*units.inch + bumper_width*2
        
        wheel_diameter = 6*units.inch
        drivetrain_gear_ratio = 10.71
        motors_per_side = 2
        
        self.drivetrain = tankmodel.TankModel.theory(motor_cfg,
                                                     robot_mass, drivetrain_gear_ratio, motors_per_side,
                                                     robot_wheelbase,
                                                     robot_width,
                                                     robot_length,
                                                     wheel_diameter)

    def update_sim(self, hal_data, now, tm_diff):
        '''
            Called when the simulation parameters for the program need to be
            updated.
            
            :param now: The current time as a float
            :param tm_diff: The amount of time that has passed since the last
                            time that this function was called
        '''
        
        # Simulate the drivetrain
        lr_motor = hal_data['pwm'][1]['value']
        rr_motor = hal_data['pwm'][2]['value']
        
        # Not needed because front and rear should be in sync
        #lf_motor = hal_data['pwm'][3]['value']
        #rf_motor = hal_data['pwm'][4]['value']
        
        x, y, angle = self.drivetrain.get_distance(lr_motor, rr_motor, tm_diff)
        self.physics_controller.distance_drive(x, y, angle)
