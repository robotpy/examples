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
        super()