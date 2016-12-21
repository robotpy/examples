'''
All subsystems should be imported here and instantiated inside the init method.
If you want your subsystem to be accessible to commands, you must add a variable
for it in the global scope.
'''

from wpilib.robotbase import RobotBase

from .singlemotor import SingleMotor
from .oi import OI

motor = None
oi = None

def init():
    '''
    Creates all subsystems. You must run this before any commands are
    instantiated. Do not run it more than once.
    '''
    global motor, oi

    '''
    Some tests call startCompetition multiple times, so don't throw an error if
    called more than once in that case.
    '''
    if oi is not None and not RobotBase.isSimulation():
        raise RuntimeError('Subsystems have already been initialized')

    motor = SingleMotor()

    '''
    Since OI instantiates commands as part of its construction, and those
    commands need access to the subsystems, OI must be instantiated last.
    '''
    oi = OI()
