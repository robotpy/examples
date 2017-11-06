#!/usr/bin/env python3

import wpilib

from robotpy_ext.common_drivers import navx

def run():
    raise ValueError()

class MyRobot(wpilib.SampleRobot):
    
    def robotInit(self):
        
        self.sd = wpilib.SmartDashboard
        self.timer = wpilib.Timer()
        
        #
        # Communicate w/navX MXP via the MXP SPI Bus.
        # - Alternatively, use the i2c bus.
        # See http://navx-mxp.kauailabs.com/guidance/selecting-an-interface/ for details
        #
        
        self.navx = navx.AHRS.create_spi()
        #self.navx = navx.AHRS.create_i2c()
        
        # Analog input
        self.analog = wpilib.AnalogInput(navx.getNavxAnalogInChannel(0))
    
    def disabled(self):
        
        self.logger.info("Entered disabled mode")
        
        self.timer.reset()
        self.timer.start()
        
        while self.isDisabled():
        
            if self.timer.hasPeriodPassed(0.5):
                self.sd.putBoolean('SupportsDisplacement', self.navx._isDisplacementSupported())
                self.sd.putBoolean('IsCalibrating', self.navx.isCalibrating())
                self.sd.putBoolean('IsConnected', self.navx.isConnected())
                self.sd.putNumber('Angle', self.navx.getAngle())
                self.sd.putNumber('Pitch', self.navx.getPitch())
                self.sd.putNumber('Yaw', self.navx.getYaw())
                self.sd.putNumber('Roll', self.navx.getRoll())
                self.sd.putNumber('Analog', self.analog.getVoltage())
                self.sd.putNumber('Timestamp', self.navx.getLastSensorTimestamp())
                
            wpilib.Timer.delay(0.010)

if __name__ == '__main__':
    wpilib.run(MyRobot)