from wpilib.command import TimedCommand

import subsystems

class SetSpeed(TimedCommand):
    '''
    Spins the motor at the given power for a given number of seconds, then
    stops.
    '''

    def __init__(self, power, timeoutInSeconds):
        super().__init__('Set Speed %d' % power, timeoutInSeconds)

        self.power = power
        self.requires(subsystems.motor)

    def initialize(self):
        subsystems.motor.setSpeed(self.power)


    def end(self):
        subsystems.motor.setSpeed(0)
