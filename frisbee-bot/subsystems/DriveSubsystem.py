import wpilib
import wpilib.drive
import commands2
import constants


class DriveSubsystem(commands2.SubsystemBase):

    # The motors on the left side of the drive.
    leftMotors = wpilib.MotorControllerGroup(
        wpilib.PWMSparkMax(constants.Constants.DriveConstants.kLeftMotor1Port),
        wpilib.PWMSparkMax(constants.Constants.DriveConstants.kLeftMotor2Port),
    )

    # The motors on the right side of the drive.
    rightMotors = wpilib.MotorControllerGroup(
        wpilib.PWMSparkMax(constants.Constants.DriveConstants.kRightMotor1Port),
        wpilib.PWMSparkMax(constants.Constants.DriveConstants.kRightMotor2Port),
    )

    # The robot's drive
    drive = wpilib.drive.DifferentialDrive(leftMotors, rightMotors)

    # The left-side drive encoder
    leftEncoder = wpilib.Encoder(
        constants.Constants.DriveConstants.kLeftEncoderPorts[0],
        constants.Constants.DriveConstants.kLeftEncoderPorts[1],
        constants.Constants.DriveConstants.kLeftEncoderReversed,
    )

    # The right-side drive encoder
    rightEncoder = wpilib.Encoder(
        constants.Constants.DriveConstants.kRightEncoderPorts[0],
        constants.Constants.DriveConstants.kRightEncoderPorts[1],
        constants.Constants.DriveConstants.kRightEncoderReversed,
    )

    # Creates a new DriveSubsystem.
    def DriveSubsystemSetup(self):
        # We need to invert one side of the drivetrain so that positive voltages
        # result in both sides moving forward. Depending on how your robot's
        # gearbox is constructed, you might have to invert the left side instead.
        self.rightMotors.setInverted(True)

        # Sets the distance per pulse for the encoders
        self.leftEncoder.setDistancePerPulse(
            constants.Constants.DriveConstants.kEncoderDistancePerPulse
        )
        self.rightEncoder.setDistancePerPulse(
            constants.Constants.DriveConstants.kEncoderDistancePerPulse
        )

    def arcadeDrive(self, fwd: float, rot: float):
        self.drive.arcadeDrive(fwd, rot)

    def resetEncoders(self):
        self.leftEncoder.reset()
        self.rightEncoder.reset()

    def getAverageEncoderDistance(self):
        return (self.leftEncoder.getDistance() + self.rightEncoder.getDistance()) / 2

    def getLeftEncoder(self):
        return self.leftEncoder

    def getRightEncoder(self):
        return self.rightEncoder

    def maxOutputHalf(self):
        print("half")
        self.drive.setMaxOutput(0.5)

    def maxOutputFull(self):
        self.drive.setMaxOutput(1)
