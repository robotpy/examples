import wpilib
import wpimath.controller
import commands2
import constants

class ShooterSubsystem(commands2.PIDSubsystem):

    shooterMotor = wpilib.PWMSparkMax(constants.Constants.ShooterConstants.kShooterMotorPort)
    feederMotor = wpilib.PWMSparkMax(constants.Constants.ShooterConstants.kFeederMotorPort)
    shooterEncoder = wpilib.Encoder(
        constants.Constants.ShooterConstants.kEncoderPorts[0],
        constants.Constants.ShooterConstants.kEncoderPorts[1],
        constants.Constants.ShooterConstants.kEncoderReversed
    )
    shooterFeedForward = wpimath.controller.SimpleMotorFeedforwardMeters(
        constants.Constants.ShooterConstants.kSVolts,
        constants.Constants.ShooterConstants.kVVoltSecondsPerRotation
    )

    def ShooterSubsystem(self):
        super(wpimath.controller.PIDController(
            constants.Constants.ShooterConstants.kP,
            constants.Constants.ShooterConstants.kI,
            constants.Constants.ShooterConstants.kD,
        ))
        self.getController().setTolerance(constants.Constants.ShooterConstants.kShooterToleranceRPS)
        self.shooterEncoder.setDistancePerPulse(constants.Constants.ShooterConstants.kEncoderCPR)
        self.setSetpoint(constants.Constants.ShooterConstants.kShooterTargetRPS)
    
    def useOutput(self, output:float, setpoint:float):
        self.shooterMotor.setVoltage(output + self.shooterFeedForward.calculate(setpoint))
    
    def getMeasurement(self):
        return self.shooterEncoder.getRate()
    
    def runFeeder(self):
        self.feederMotor.set(constants.Constants.ShooterConstants.kFeederSpeed)
    
    def stopFeeder(self):
        self.feederMotor.set(0)