
import wpilib
from magicbot import StateMachine, state

from .drivetrain import DriveTrain

class RobotAngle(StateMachine):
    '''
        Use this to manipulate the angle of the robot
    '''
    
    #
    # Magic imports
    #
    
    gyro = wpilib.ADXRS450_Gyro
    drivetrain = DriveTrain
    
    #
    # Tuning parameters
    #
    
    kToleranceDegrees = 2.0
    
    # Often, you will find it useful to have different parameters in
    # simulation than what you use on the real robot
    
    if wpilib.RobotBase.isSimulation():
        # These PID parameters are used in simulation
        kP = 0.03
        kI = 0.00
        kD = 0.00
        kF = 0.00
    else:
        # These PID parameters are used on a real robot
        kP = 0.03
        kI = 0.00
        kD = 0.00
        kF = 0.00
    
    def __init__(self):
        # Use PIDController to control angle
        turnController = wpilib.PIDController(self.kP, self.kI, self.kD, self.kF,
                                              self._pidGet, output=self._pidWrite)
        turnController.setInputRange(-180.0,  180.0)
        turnController.setOutputRange(-1.0, 1.0)
        turnController.setAbsoluteTolerance(self.kToleranceDegrees)
        turnController.setContinuous(True)
        self.turnController = turnController
        
        self.angle = None
        self.setpoint = None
    
    def getAngle(self):
        '''
            :returns: the current angle that the robot is pointing
        '''
        return self._normalizeAngle(self.gyro.getAngle())
    
    def rotateTo(self, angle):
        '''
            :returns: True if robot already pointing at that angle
        '''
        
        # normalize angle before sending to PIDController
        self.angle = self._normalizeAngle(angle)
        
        # compute whether we're on target or not
        error = angle - self.getAngle()
        if abs(error) > 180.0:
            if error > 0:
                error = error - 360.0
            else:
                error = error + 360.0
        
        if abs(error) < self.kToleranceDegrees:
            retval = True
        else:
            retval = False
        
        # engage the state machine
        self.engage()
        
        return retval
        
        # The problem with this is that the error gets cleared whenever
        # we call setSetpoint... 
        #return self.turnController.onTarget()
        
    @state(first=True)
    def engaged(self, initial_call):
        if initial_call:
            self.rotateToAngleRate = 0
            self.turnController.enable()
        
        if self.setpoint is None or abs(self.setpoint - self.angle) > 0.0001:
            self.turnController.setSetpoint(self.angle)
            self.setpoint = self.angle
        
        self.drivetrain.rotate(self.rotateToAngleRate)
    
    def done(self):
        self.turnController.disable()
        self.turnController.setSetpoint(0)
        self.setpoint = None
        super().done()
        
    def reset(self):
        self.gyro.reset()
    
    #
    # Utility methods
    #
    
    def _normalizeAngle(self, angle):
        '''Normalize angle to [-180,180]'''
        return ((angle + 180) % 360) - 180.0
    
    #
    # PIDController methods
    #
    
    def _pidGet(self):
        '''The angle to feed to PIDController must be between
           -180 and 180'''
        return self.getAngle()
    
    def _pidWrite(self, output):
        """This function is invoked periodically by the PID Controller"""
        self.rotateToAngleRate = output
