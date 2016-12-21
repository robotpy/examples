from wpilib.command.commandgroup import CommandGroup

from wpilib.command.waitcommand import WaitCommand
from commands.setspeed import SetSpeed

class AutonomousProgram(CommandGroup):
    '''
    A simple program that spins the motor for two seconds, pauses for a second,
    and then spins it in the opposite direction for two seconds.
    '''

    def __init__(self):
        super().__init__('Autonomous Program')

        self.addSequential(SetSpeed(power=0.7, timeoutInSeconds=2))
        self.addSequential(WaitCommand(timeout=1))
        self.addSequential(SetSpeed(power=-0.7, timeoutInSeconds=2))
