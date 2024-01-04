#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#


import ntcore
import numpy
from cscore import CameraServer
import cv2


#
# This code will work both on a RoboRIO and on other platforms. The exact mechanism
# to run it differs depending on whether you’re on a RoboRIO or a coprocessor
#
# https://robotpy.readthedocs.io/en/stable/vision/code.html


def main():
    # Get the Axis camera from CameraServer
    camera = CameraServer.addAxisCamera("axis-camera.local")

    # Set the resolution
    camera.setResolution(640, 480)

    # Get a CvSink. This will capture Mats from the camera
    cvSink = CameraServer.getVideo()

    # Setup a CvSource. This will send images back to the Dashboard
    outputStream = CameraServer.putVideo("Rectangle", 640, 480)

    # Mats are very memory expensive. Lets reuse this Mat.
    mat = numpy.zeros((480, 640, 3), dtype="uint8")

    # Declare the color of the rectangle
    rectColor = (255, 255, 255)

    # The camera code will be killed when the robot.py program exits. If you wish to perform cleanup,
    # you should register an atexit handler. The child process will NOT be launched when running the robot code in
    # simulation or unit testing mode

    while True:
        # Tell the CvSink to grab a frame from the camera and put it in the source mat.  If there is an error notify the
        # output.

        if cvSink.grabFrame(mat) == 0:
            # Send the output the error.
            outputStream.notifyError(cvSink.getError())

            # skip the rest of the current iteration
            continue

        # Put a rectangle on the image
        mat = cv2.rectangle(
            img=mat,
            pt1=(100, 100),
            pt2=(400, 400),
            color=rectColor,
            lineType=5,
        )

        # Give the output stream a new image to display
        outputStream.putFrame(mat)
