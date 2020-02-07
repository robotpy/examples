#!/usr/bin/env python3

import wpilib


import navx


def run():
    raise ValueError()


class MyRobot(wpilib.TimedRobot):
    def robotInit(self):

        self.timer = wpilib.Timer()

        #
        # Communicate w/navX MXP via the MXP SPI Bus.
        # - Alternatively, use the i2c bus.
        # See http://navx-mxp.kauailabs.com/guidance/selecting-an-interface/ for details
        #

        self.navx = navx.AHRS.create_spi()
        # self.navx = navx.AHRS.create_i2c()

        # Analog input
        # It seems as though analog is not currently supported. self.analog = wpilib.AnalogInput(navx.pins.getNavxAnalogInChannel(0))
        
    def robotPeriodic(self):

        self.logger.info("Entered disabled mode")

        self.timer.reset()
        self.timer.start()

        

        while self.isDisabled():

            if self.timer.hasPeriodPassed(0.5):
                wpilib.SmartDashboard.putNumber(
                    "Displacement X", self.navx.getDisplacementX()
                )
                wpilib.SmartDashboard.putNumber(
                    "Displacement Y", self.navx.getDisplacementY()
                )
                wpilib.SmartDashboard.putBoolean("IsCalibrating", self.navx.isCalibrating())
                wpilib.SmartDashboard.putBoolean("IsConnected", self.navx.isConnected())
                wpilib.SmartDashboard.putNumber("Angle", self.navx.getAngle())
                wpilib.SmartDashboard.putNumber("Pitch", self.navx.getPitch())
                wpilib.SmartDashboard.putNumber("Yaw", self.navx.getYaw())
                wpilib.SmartDashboard.putNumber("Roll", self.navx.getRoll())
                #wpilib.SmartDashboard.putNumber("Analog", self.analog.getVoltage())
                wpilib.SmartDashboard.putNumber("Timestamp", self.navx.getLastSensorTimestamp())

if __name__ == "__main__":
    wpilib.run(MyRobot)
