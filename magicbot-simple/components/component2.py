
import wpilib
from .component1 import Component1

from magicbot import will_reset_to

class Component2:
    
    component1 = Component1
    some_motor = wpilib.Talon
    
    # This is changed to the value in robot.py
    SOME_CONSTANT = int
    
    # This gets reset after each invocation of execute()
    did_something = will_reset_to(False)
    
    def on_enable(self):
        '''Called when the robot enters teleop or autonomous mode'''
        self.logger.info("Robot is enabled: I have SOME_CONSTANT=%s", self.SOME_CONSTANT)

    def do_something(self):
        self.did_something = True

    def execute(self):
        if self.did_something:
            self.some_motor.set(1)
        else:
            self.some_motor.set(0)
