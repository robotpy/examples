# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.

from hal import SimDevice, SimDouble
import typing


class RomiGyro:

    simRateX: typing.Optional[SimDouble] = None
    simRateY: typing.Optional[SimDouble] = None
    simRateZ: typing.Optional[SimDouble] = None
    simAngleX: typing.Optional[SimDouble] = None
    simAngleY: typing.Optional[SimDouble] = None
    simAngleZ: typing.Optional[SimDouble] = None

    def __init__(self) -> None:
        self.gyroSimDevice = SimDevice("Gyro:RomiGyro")
        if self.gyroSimDevice:
            self.gyroSimDevice.createBoolean("init", SimDevice.Direction.kOutput, True)
            self.simRateX = self.gyroSimDevice.createDouble(
                "rate_x", SimDevice.Direction.kInput, 0.0
            )
            self.simRateY = self.gyroSimDevice.createDouble(
                "rate_y", SimDevice.Direction.kInput, 0.0
            )
            self.simRateZ = self.gyroSimDevice.createDouble(
                "rate_z", SimDevice.Direction.kInput, 0.0
            )

            self.simAngleX = self.gyroSimDevice.createDouble(
                "angle_x", SimDevice.Direction.kInput, 0.0
            )
            self.simAngleY = self.gyroSimDevice.createDouble(
                "angle_y", SimDevice.Direction.kInput, 0.0
            )
            self.simAngleZ = self.gyroSimDevice.createDouble(
                "angle_z", SimDevice.Direction.kInput, 0.0
            )

        self.angleXOffset: float = 0.0
        self.angleYOffset: float = 0.0
        self.angleZOffset: float = 0.0

    def getRateX(self) -> float:
        """Get the rate of turn in degrees-per-second around the X-axis.

        :returns: rate of turn in degrees-per-second
        """
        if self.simRateX:
            return self.simRateX.get()
        return 0.0

    def getRateY(self) -> float:
        """Get the rate of turn in degrees-per-second around the Y-axis.

        :returns: rate of turn in degrees-per-second
        """
        if self.simRateY:
            return self.simRateY.get()
        return 0.0

    def getRateZ(self) -> float:
        """Get the rate of turn in degrees-per-second around the Z-axis.

        :returns: rate of turn in degrees-per-second
        """
        if self.simRateZ:
            return self.simRateZ.get()
        return 0.0

    def getAngleX(self) -> float:
        """Get the currently reported angle around the X-axis.

        :returns: current angle around X-axis in degrees
        """
        if self.simAngleX:
            return self.simAngleX.get() - self.angleXOffset
        return 0.0

    def getAngleY(self) -> float:
        """Get the currently reported angle around the Y-axis.

        :returns: current angle around Y-axis in degrees
        """
        if self.simAngleY:
            return self.simAngleY.get() - self.angleYOffset
        return 0.0

    def getAngleZ(self) -> float:
        """Get the currently reported angle around the Z-axis.

        :returns: current angle around Z-axis in degrees
        """
        if self.simAngleZ:
            return self.simAngleZ.get() - self.angleZOffset
        return 0.0

    def reset(self) -> None:
        """Reset the gyro angles to 0."""
        if self.simRateX:
            self.angleXOffset = self.simRateX.get()
            self.angleYOffset = self.simRateY.get()
            self.angleZOffset = self.simRateZ.get()
