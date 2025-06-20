#!/usr/bin/env python3
#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#


import threading
import time

import cv2
import numpy as np

import wpilib
from cscore import CameraServer


class MyRobot(wpilib.TimedRobot):
    """
    This is a sample program showing how to overlay a red rectangle on a camera feed.
    The rectangle's position is controlled from robot code during teleop.
    This requires at least one USB camera connected to the robot.
    Use a dashboard client to view the camera stream. Two streams are available:
    - "Annotated Stream": The camera feed with the red rectangle overlay.
    - "<your camera name>": The raw camera feed without any annotations.
    """

    def robotInit(self):
        """Robot initialization function"""

        CameraServer.enableLogging()

        # State variables - this will be the center position of the rectangle, in units of pixels.
        self.rectX = 0
        self.rectY = 0

        # Start reading data from the camera, and serving the raw stream
        self.camera = CameraServer.startAutomaticCapture()
        self.camera.setResolution(640, 480)

        # Record a reference to the video source (which should be the first camera connected):
        self.source = self.camera.enumerateSources()

        # Set up a second server to provide an annotated stream
        self.cvSink = CameraServer.getVideo()
        self.outputStream = CameraServer.putVideo("Annotated Stream", 640, 480)

        # Allocate memory for creating the annotated image.
        self.img = np.zeros((480, 640, 3), dtype=np.uint8)

        # Start the background thread for image processing
        self.processingThread = threading.Thread(target=self.processImages, daemon=True)
        self.processingThread.start()


    def processImages(self):
        """Thread to read information from the camera, and provide the overlaid image"""

        while True:
            # Grab a frame from the camera
            frameTime, self.img = self.cvSink.grabFrame(self.img)

            if frameTime == 0:
                # If there's an error, skip processing
                print(self.cvSink.getError())
                continue

            # Draw a red box on the image
            width = 50
            height= 50
            topLeft  = (int(self.rectX-width/2), int(self.rectY-height/2))
            botRight = (int(self.rectX+width/2), int(self.rectY+height/2))
            colorBGR = (0, 0, 255)
            lineWidth = 2
            cv2.rectangle(self.img, 
                        topLeft, 
                        botRight,
                        colorBGR, 
                        lineWidth)

            # Publish the annotated image
            self.outputStream.putFrame(self.img)

            # Yield execution to other threads
            time.sleep(0.001)

    def teleopPeriodic(self):
        # Update the rectangle position.
        # For this example, we'll use a joystick as input.
        joystick = wpilib.Joystick(0)
        self.rectX += joystick.getX() * 5
        self.rectY += joystick.getY() * 5

        # Ensure the rectangle stays within bounds
        self.rectX = max(0, min(self.rectX, 640))
        self.rectY = max(0, min(self.rectY, 480))