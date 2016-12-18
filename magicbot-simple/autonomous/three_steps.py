
from robotpy_ext.autonomous import StatefulAutonomous, timed_state
             
from components.component2 import Component2
                    
class TwoSteps(StatefulAutonomous):

    MODE_NAME = 'Two Steps'
    DEFAULT = True
    
    component2 = Component2

    def initialize(self):
        
        # This allows you to tune the variable via the SmartDashboard over
        # networktables
        self.register_sd_var('drive_speed', -1)

    @timed_state(duration=2, next_state='do_something', first=True)
    def dont_do_something(self):
        '''This happens first'''
        pass

    @timed_state(duration=5)
    def do_something(self):
        '''This happens second'''
        self.component2.do_something()
