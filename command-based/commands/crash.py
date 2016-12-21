from wpilib.command import InstantCommand

class Crash(InstantCommand):
    '''
    Causes an exception when activated. Not likely to be useful, but it's a
    simple way to test if exception recovery is working.
    '''

    def __init__(self):
        super().__init__('Crash Command')


    def initialize(self):
        raise RuntimeError('Crash command activated')
