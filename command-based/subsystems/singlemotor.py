from wpilib.command.subsystem import Subsystem
from wpilib.cantalon import CANTalon

from commands.followjoystick import FollowJoystick
import robotmap

class SingleMotor(Subsystem):
    '''
    This example subsystem controls a single CAN Talon SRX in PercentVBus mode.
    '''

    def __init__(self):
        '''Instantiates the motor object.'''

        super().__init__('SingleMotor')

        self.motor = CANTalon(robotmap.singlemotor.motorCanID)


    def setSpeed(self, speed):
        self.motor.set(speed)


    def initDefaultCommand(self):
        self.setDefaultCommand(FollowJoystick())
