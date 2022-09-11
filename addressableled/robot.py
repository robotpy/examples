from wpilib import run, TimedRobot, AddressableLED

kLEDBuffer = 60

class MyRobot(TimedRobot):
    def robotInit(self):
        # PWM Port 9
        # Must be a PWM header, not MXP or DIO
        self.m_led = AddressableLED(9)
        
        # LED Data
        self.m_ledData = []

        # Store what the last hue of the first pixel is
        self.m_rainbowFirstPixelHue = 0

        # Default to a length of 60, start empty output
        # Length is expensive to set, so only set it once, then just update data
        self.m_led.setLength(kLEDBuffer)
        
        self.m_led.start()

    def robotPeriodic(self):
        # Fill the buffer with a rainbow
        self.rainbow()
        
        # Set the LEDs
        if len(self.m_ledData) <= kLEDBuffer:
            self.m_led.setData(self.m_ledData)

    def rainbow(self):
        # For every pixel
        for i in range(kLEDBuffer):
            # Calculate the hue - hue is easier for rainbows because the color
            # shape is a circle so only one value needs to precess
            hue = (self.m_rainbowFirstPixelHue + (i * 180 / kLEDBuffer)) % 180
            
            self.m_ledData.append(AddressableLED.LEDData())
            
            # Set the value
            self.m_ledData[i].setHSV(int(hue), 255, 128)

        # Increase by to make the rainbow "move"
        self.m_rainbowFirstPixelHue += 3

        # Check bounds
        self.m_rainbowFirstPixelHue %= 100

if __name__ == '__main__':
    run(MyRobot)
