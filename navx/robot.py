#!/usr/bin/env python3

import wpilib
from networktables import NetworkTables


import navx


def run():
    raise ValueError()


class MyRobot(wpilib.TimedRobot):
    def robotInit(self):

        self.sd = NetworkTables.getTable("SmartDashboard")

        self.timer = wpilib.Timer()

        #
        # Communicate w/navX MXP via the MXP SPI Bus.
        # - Alternatively, use the i2c bus.
        # See http://navx-mxp.kauailabs.com/guidance/selecting-an-interface/ for details
        #

        self.navx = navx.AHRS.create_spi()
        # self.navx = navx.AHRS.create_i2c()

        # Analog input
        # self.analog = wpilib.AnalogInput(navx.pins.getNavxAnalogInChannel(0)) <--It seems as though the analog channel is not currently supported.

    def disabledInit(self):
        self.logger.info("Entered disabled mode")

        self.timer.reset()
        self.timer.start()

    def disabledPeriodic(self):
        if self.timer.hasPeriodPassed(0.5):
            self.sd.putNumber("Displacement X", self.navx.getDisplacementX())
            self.sd.putNumber("Displacement Y", self.navx.getDisplacementY())
            self.sd.putBoolean("IsCalibrating", self.navx.isCalibrating())
            self.sd.putBoolean("IsConnected", self.navx.isConnected())
            self.sd.putNumber("Angle", self.navx.getAngle())
            self.sd.putNumber("Pitch", self.navx.getPitch())
            self.sd.putNumber("Yaw", self.navx.getYaw())
            print("YAW", self.navx.getYaw())
            self.sd.putNumber("Roll", self.navx.getRoll())
            # self.sd.putNumber("Analog", self.analog.getVoltage())
            self.sd.putNumber("Timestamp", self.navx.getLastSensorTimestamp())


if __name__ == "__main__":
    wpilib.run(MyRobot)
