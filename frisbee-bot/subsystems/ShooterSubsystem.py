import wpilib
import wpimath.controller
import commands2
import commands2.cmd
import constants


class ShooterSubsystem(commands2.PIDSubsystem):
    def ShooterSubsystemSetup(self):
        self.shooterMotor = wpilib.PWMSparkMax(
            constants.Constants.ShooterConstants.kShooterMotorPort
        )
        self.feederMotor = wpilib.PWMSparkMax(
            constants.Constants.ShooterConstants.kFeederMotorPort
        )
        self.shooterEncoder = wpilib.Encoder(
            constants.Constants.ShooterConstants.kEncoderPorts[0],
            constants.Constants.ShooterConstants.kEncoderPorts[1],
            constants.Constants.ShooterConstants.kEncoderReversed,
        )
        self.shooterFeedForward = wpimath.controller.SimpleMotorFeedforwardMeters(
            constants.Constants.ShooterConstants.kSVolts,
            constants.Constants.ShooterConstants.kVVoltSecondsPerRotation,
        )
        self.getController().setTolerance(
            constants.Constants.ShooterConstants.kShooterToleranceRPS
        )
        self.shooterEncoder.setDistancePerPulse(
            constants.Constants.ShooterConstants.kEncoderCPR
        )
        self.setSetpoint(constants.Constants.ShooterConstants.kShooterTargetRPS)

    def _useOutput(self, output: float, setpoint: float):
        self.shooterMotor.setVoltage(
            output + self.shooterFeedForward.calculate(setpoint)
        )

    def _getMeasurement(self):
        return self.shooterEncoder.getRate()

    def runFeeder(self):
        self.feederMotor.set(constants.Constants.ShooterConstants.kFeederSpeed)

    def stopFeeder(self):
        self.feederMotor.set(0)
