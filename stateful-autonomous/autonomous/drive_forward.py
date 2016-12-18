
from robotpy_ext.autonomous import StatefulAutonomous, timed_state
                    
class DriveForward(StatefulAutonomous):

    MODE_NAME = 'Drive Forward'

    def initialize(self):
        
        # This allows you to tune the variable via the SmartDashboard over
        # networktables
        self.register_sd_var('drive_speed', 1)
        

    @timed_state(duration=0.5, next_state='drive_forward', first=True)
    def drive_wait(self):
        pass

    @timed_state(duration=5)
    def drive_forward(self):
        self.drive.drive(self.drive_speed, 0)

