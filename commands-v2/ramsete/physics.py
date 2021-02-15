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

from wpilib import RobotController, ADXRS450_Gyro
from wpilib.simulation import (
    PWMSim,
    DifferentialDrivetrainSim,
    EncoderSim,
    ADXRS450_GyroSim,
)
from wpimath.system import LinearSystemId
from wpimath.system.plant import DCMotor

import constants

from pyfrc.physics.core import PhysicsInterface


class PhysicsEngine:
    """
    Simulates a motor moving something that strikes two limit switches,
    one on each end of the track. Obviously, this is not particularly
    realistic, but it's good enough to illustrate the point
    """

    def __init__(self, physics_controller: PhysicsInterface):

        self.physics_controller = physics_controller

        # Motor simulation definitions. Each correlates to a motor defined in
        # the drivetrain subsystem.
        self.m_frontLeftMotor = PWMSim(constants.kLeftMotor1Port)
        self.m_backLeftMotor = PWMSim(constants.kLeftMotor2Port)
        self.m_frontRightMotor = PWMSim(constants.kRightMotor1Port)
        self.m_backRightMotor = PWMSim(constants.kRightMotor2Port)

        self.m_system = LinearSystemId.identifyDrivetrainSystem(
            constants.kvVoltSecondsPerMeter,  # The linear velocity gain in volt seconds per distance.
            constants.kaVoltSecondsSquaredPerMeter,  # The linear acceleration gain, in volt seconds^2 per distance.
            1.5,  # The angular velocity gain, in volt seconds per angle.
            0.3,  # The angular acceleration gain, in volt seconds^2 per angle.
        )

        self.m_drivesim = DifferentialDrivetrainSim(  # The simulation model of the drivetrain.
            self.m_system,  # The state-space model for a drivetrain.
            constants.kTrackWidthMeters,  # The robot's trackwidth, which is the distance between the wheels on the left side and those on the right side. The units is meters.
            DCMotor.NEO(constants.kDrivetrainMotorCount),  # Four NEO drivetrain setup.
            1,  # One to one output gearing.
            (
                constants.kWheelDiameterMeters / 2
            ),  # The radius of the drivetrain wheels in meters.
        )

        self.m_leftEncoderSim = EncoderSim.createForChannel(
            constants.kLeftEncoderPorts[0]
        )
        self.m_rightEncoderSim = EncoderSim.createForChannel(
            constants.kRightEncoderPorts[0]
        )

        self.m_gyro = ADXRS450_GyroSim(ADXRS450_Gyro())

    def update_sim(self, now: float, tm_diff: float) -> None:
        """
        Called when the simulation parameters for the program need to be
        updated.

        :param now: The current time as a float
        :param tm_diff: The amount of time that has passed since the last
                        time that this function was called
        """

        # Simulate the drivetrain
        l_motor = self.m_frontLeftMotor.getSpeed()
        r_motor = self.m_frontRightMotor.getSpeed()

        # self.m_gyro.setAngle(-self.m_drivesim.getHeading().degrees())

        voltage = RobotController.getInputVoltage()
        self.m_drivesim.setInputs(l_motor * voltage, -r_motor * voltage)
        self.m_drivesim.update(tm_diff)

        self.m_leftEncoderSim.setDistance(self.m_drivesim.getLeftPosition() * 39.37)
        self.m_leftEncoderSim.setRate(self.m_drivesim.getLeftVelocity() * 39.37)
        self.m_rightEncoderSim.setDistance(self.m_drivesim.getRightPosition() * 39.37)
        self.m_rightEncoderSim.setRate(self.m_drivesim.getRightVelocity() * 39.37)

        self.physics_controller.field.setRobotPose(self.m_drivesim.getPose())
