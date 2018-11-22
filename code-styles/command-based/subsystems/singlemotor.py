import wpilib
from wpilib.command.subsystem import Subsystem

from commands.followjoystick import FollowJoystick

class SingleMotor(Subsystem):
    '''
    This example subsystem controls a single Talon in PercentVBus mode.
    '''

    def __init__(self):
        '''Instantiates the motor object.'''

        super().__init__('SingleMotor')

        self.motor = wpilib.Talon(1)


    def setSpeed(self, speed):
        self.motor.set(speed)


    def initDefaultCommand(self):
        self.setDefaultCommand(FollowJoystick())
