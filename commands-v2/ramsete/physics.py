#
# See the documentation for more details on how this works
#
# The idea here is you provide a simulation object that overrides specific
# pieces of WPILib, and modifies motors/sensors accordingly depending on the
# state of the simulation. An example of this would be measuring a motor
# moving for a set period of time, and then changing a limit switch to turn
# on after that period of time. This can help you do more complex simulations
# of your robot code without too much extra effort.
#

from wpilib import AnalogGyro, RobotController
from wpilib.simulation import (
    PWMSim,
    DifferentialDrivetrainSim,
    EncoderSim,
    AnalogGyroSim,
)
from wpimath.system import LinearSystemId
from wpimath.system.plant import DCMotor

from constants import constant

from pyfrc.physics.core import PhysicsInterface


class PhysicsEngine:
    """
    Simulates a motor moving something that strikes two limit switches,
    one on each end of the track. Obviously, this is not particularly
    realistic, but it's good enough to illustrate the point
    """

    def __init__(self, physics_controller: PhysicsInterface):

        self.physics_controller = physics_controller

        # Motors
        self.frontLeftMotor = PWMSim(constant.frontLeftMotorID)
        self.frontRightMotor = PWMSim(constant.frontRightMotorID)

        self.backLeftMotor = PWMSim(constant.backLeftMotorID)
        self.backRightMotor = PWMSim(constant.backRightMotorID)

        motor = DCMotor.CIM(constant.drivetrainMotorCount)

        self.system = LinearSystemId.identifyDrivetrainSystem(
            constant.kvVoltSecondsPerMeter,
            constant.kaVoltSecondsSquaredPerMeter,
            1.5,
            0.3,
        )
        self.drivesim = DifferentialDrivetrainSim(
            self.system,
            constant.trackWidth,
            motor,
            1,  # One to one output
            (constant.wheelDiameterMeters / 2),
        )

        self.leftEncoderSim = EncoderSim.createForChannel(constant.leftEncoderPorts[0])
        self.rightEncoderSim = EncoderSim.createForChannel(
            constant.rightEncoderPorts[0]
        )

        self.realGyro = constant.gyroObject
        self.gyro = AnalogGyroSim(self.realGyro)

    def update_sim(self, now: float, tm_diff: float) -> None:
        """
        Called when the simulation parameters for the program need to be
        updated.

        :param now: The current time as a float
        :param tm_diff: The amount of time that has passed since the last
                        time that this function was called
        """

        # Simulate the drivetrain
        l_motor = self.frontLeftMotor.getSpeed()
        r_motor = self.frontRightMotor.getSpeed()

        self.gyro.setAngle(-self.drivesim.getHeading().degrees())

        voltage = RobotController.getInputVoltage()
        self.drivesim.setInputs(l_motor * voltage, -r_motor * voltage)
        self.drivesim.update(tm_diff)

        self.leftEncoderSim.setDistance(self.drivesim.getLeftPosition() * 39.37)
        self.leftEncoderSim.setRate(self.drivesim.getLeftVelocity() * 39.37)
        self.rightEncoderSim.setDistance(self.drivesim.getRightPosition() * 39.37)
        self.rightEncoderSim.setRate(self.drivesim.getRightVelocity() * 39.37)

        self.physics_controller.field.setRobotPose(self.drivesim.getPose())
