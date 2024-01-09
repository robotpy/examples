from wpilib import Encoder, Spark
from wpimath.geometry import Rotation2d
from wpimath.kinematics import SwerveModulePosition, SwerveModuleState
from wpimath.trajectory import TrapezoidProfile
from wpimath.controller import PIDController, ProfiledPIDController
import constants

class SwerveModule:
    def __init__(
        self,
        driveMotorChannel,
        turningMotorChannel,
        driveEncoderChannels,
        turningEncoderChannels,
        driveEncoderReversed,
        turningEncoderReversed,
    ):
        self.m_driveMotor = Spark(driveMotorChannel)
        self.m_turningMotor = Spark(turningMotorChannel)

        self.m_driveEncoder = Encoder(*driveEncoderChannels)
        self.m_turningEncoder = Encoder(*turningEncoderChannels)

        self.m_drivePIDController = PIDController(
            constants.ModuleConstants.kPModuleDriveController, 0, 0
        )

        self.m_turningPIDController = ProfiledPIDController(
            ModuleConstants.kPModuleTurningController,
            0,
            0,
            TrapezoidProfile.Constraints(
                ModuleConstants.kMaxModuleAngularSpeedRadiansPerSecond,
                ModuleConstants.kMaxModuleAngularAccelerationRadiansPerSecondSquared,
            ),
        )

        # Set the distance per pulse for the drive encoder.
        self.m_driveEncoder.setDistancePerPulse(
            ModuleConstants.kDriveEncoderDistancePerPulse
        )
        self.m_driveEncoder.setReverseDirection(driveEncoderReversed)

        # Set the distance in radians per pulse for the turning encoder.
        self.m_turningEncoder.setDistancePerPulse(
            ModuleConstants.kTurningEncoderDistancePerPulse
        )
        self.m_turningEncoder.setReverseDirection(turningEncoderReversed)

        # Limit the PID Controller's input range between -pi and pi and set the input
        # to be continuous.
        self.m_turningPIDController.enableContinuousInput(-3.14159, 3.14159)

    def getState(self):
        return SwerveModuleState(
            self.m_driveEncoder.getRate(),
            Rotation2d(self.m_turningEncoder.getDistance()),
        )

    def getPosition(self):
        return SwerveModulePosition(
            self.m_driveEncoder.getDistance(),
            Rotation2d(self.m_turningEncoder.getDistance()),
        )

    def setDesiredState(self, desiredState):
        encoderRotation = Rotation2d(self.m_turningEncoder.getDistance())

        # Optimize the reference state to avoid spinning further than 90 degrees
        state = SwerveModuleState.optimize(desiredState, encoderRotation)

        # Scale speed by cosine of angle error.
        state.speedMetersPerSecond *= state.angle.minus(encoderRotation).getCos()

        # Calculate the drive output from the drive PID controller.
        driveOutput = self.m_drivePIDController.calculate(
            self.m_driveEncoder.getRate(), state.speedMetersPerSecond
        )

        # Calculate the turning motor output from the turning PID controller.
        turnOutput = self.m_turningPIDController.calculate(
            self.m_turningEncoder.getDistance(), state.angle.getRadians()
        )

        # Set motor outputs
        self.m_driveMotor.set(driveOutput)
        self.m_turningMotor.set(turnOutput)

    def resetEncoders(self):
        self.m_driveEncoder.reset()
        self.m_turningEncoder.reset()
